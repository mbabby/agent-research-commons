import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from arc.growth import Blocked, Ledger


NOW = '2026-11-10T08:00:00+00:00'


def candidate(name='one', **overrides):
    data = {'identity': 'https://example.org/' + name, 'name': name,
            'channel': 'email', 'address': name + '@example.org',
            'contact_source': 'https://example.org/' + name + '/contact',
            'relevance_source': 'https://example.org/' + name + '/work',
            'relevance': 'A creator-authored agent retry tutorial.',
            'verified_at': NOW}
    data.update(overrides)
    return data


def review(**overrides):
    data = {'subject': 'A retry question', 'body': 'Your tutorial: one missing case? Reply no. Operator with AI assistance.',
            'personalization': 'Their documented retry example', 'ask': 'One missing case',
            'opt_out_text': 'Reply no.', 'sender_identity': 'Operator with AI assistance.',
            'history_checked_at': NOW, 'policy_checked_at': NOW, 'backup_verified_at': NOW,
            'history_evidence': 'provider query', 'policy_evidence': 'rules and contact-purpose check',
            'backup_evidence': 'private durable checkpoint', 'followup_allowed': False}
    data.update(overrides)
    return data


class GrowthTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / 'ledger.sqlite'
        self.ledger = Ledger(self.path, NOW)

    def tearDown(self):
        self.ledger.close()
        self.temp.cleanup()

    def ready(self, name='one', **kwargs):
        added = self.ledger.add(candidate(name, **kwargs))
        self.ledger.review(added['person'], review())
        self.ledger.cap('email', 150, 'verified daily account capacity')
        return added

    def reserve(self, row):
        return self.ledger.reserve(row['person'], row['endpoint'])['attempt']

    def sent(self, name='one'):
        row = self.ready(name)
        attempt = self.reserve(row)
        self.ledger.result(attempt, 'sent', 'provider-confirmation-' + name, 'email:test:message-' + name)
        return row, attempt

    def test_zero_capacity_until_verified(self):
        row = self.ledger.add(candidate())
        self.ledger.review(row['person'], review())
        with self.assertRaisesRegex(Blocked, 'capacity'):
            self.reserve(row)

    def test_endpoint_and_alias_deduplication(self):
        row = self.ledger.add(candidate())
        again = self.ledger.add(candidate(address=' ONE@EXAMPLE.ORG '))
        social = self.ledger.add(candidate(channel='video', address='https://video.example/@one'))
        self.assertEqual(row['person'], again['person'])
        self.assertEqual(row['person'], social['person'])
        self.assertEqual(1, self.ledger.report('2026-11-10')['candidate_creators_total'])

    def test_identity_collision_stops_instead_of_merging_histories(self):
        self.ledger.add(candidate('one'))
        self.ledger.add(candidate('two'))
        with self.assertRaisesRegex(Blocked, 'collision'):
            self.ledger.add(candidate('one', aliases=['https://example.org/two']))

    def test_confirmed_first_send_blocks_other_channel(self):
        row, _ = self.sent()
        social = self.ledger.add(candidate(channel='video', address='https://video.example/@one'))
        with self.assertRaisesRegex(Blocked, 'Already contacted'):
            self.reserve(social)

    def test_atomic_reservation_blocks_second_connection(self):
        row = self.ready()
        self.reserve(row)
        other = Ledger(self.path, NOW)
        try:
            with self.assertRaisesRegex(Blocked, 'Unresolved'):
                other.reserve(row['person'], row['endpoint'])
        finally:
            other.close()

    def test_unknown_survives_restart_and_preserves_audit(self):
        row = self.ready()
        attempt = self.reserve(row)
        self.ledger.result(attempt, 'unknown', 'provider timeout')
        self.ledger.close()
        self.ledger = Ledger(self.path, NOW)
        with self.assertRaisesRegex(Blocked, 'Unresolved'):
            self.reserve(row)
        self.ledger.result(attempt, 'sent', 'provider reconciled', 'email:test:actual-message', at=NOW)
        self.assertEqual(2, self.ledger.db.execute('SELECT COUNT(*) FROM result_log').fetchone()[0])
        self.assertEqual(1, self.ledger.report('2026-11-10')['provider_confirmed_unique_first_contacts'])

    def test_verified_failure_allows_new_reservation(self):
        row = self.ready()
        attempt = self.reserve(row)
        self.ledger.result(attempt, 'failed', 'provider explicitly rejected before send')
        self.assertNotEqual(attempt, self.reserve(row))

    def test_suppression_cancels_open_and_applies_to_later_alias(self):
        row = self.ready()
        attempt = self.reserve(row)
        self.ledger.suppress(row['person'], 'Recipient requested no further contact')
        new = self.ledger.add(candidate(channel='video', address='https://video.example/@one'))
        with self.assertRaisesRegex(Blocked, 'suppressed'):
            self.reserve(new)
        self.assertEqual('cancelled', self.ledger.db.execute('SELECT state FROM attempts WHERE id=?', (attempt,)).fetchone()[0])
        # If sending crossed cancellation, record the truth without lifting refusal.
        self.ledger.result(attempt, 'sent', 'late-confirmation', 'email:test:late-provider-id', at=NOW)
        self.assertEqual(1, self.ledger.report('2026-11-10')['suppressed_creators_total'])

    def test_review_requires_identity_optout_fresh_checks(self):
        row = self.ledger.add(candidate())
        for changes in ({'body': 'Hi there'}, {'history_evidence': ''}, {'backup_verified_at': '2026-11-01T08:00:00+00:00'}, {'policy_checked_at': '2026-11-11T08:00:00+00:00'}, {'followup_allowed': 'false'}):
            with self.subTest(changes=changes), self.assertRaises((Blocked, ValueError)):
                self.ledger.review(row['person'], review(**changes))

    def test_stale_sources_block(self):
        row = self.ready(verified_at='2026-10-01T08:00:00+00:00')
        with self.assertRaisesRegex(Blocked, 'stale'):
            self.reserve(row)

    def test_capacity_counts_pending_unknown_sent_not_failure(self):
        one = self.ready('one'); two = self.ready('two')
        self.ledger.cap('email', 1, 'verified limit')
        attempt = self.reserve(one)
        self.ledger.result(attempt, 'unknown', 'ambiguous')
        with self.assertRaisesRegex(Blocked, 'exhausted'):
            self.reserve(two)
        self.ledger.result(attempt, 'failed', 'provider no-send confirmed')
        self.reserve(two)

    def test_followup_default_off_and_seven_day_gap(self):
        row, _ = self.sent()
        with self.assertRaisesRegex(Blocked, 'authorization'):
            self.ledger.reserve(row['person'], row['endpoint'], 'followup')
        self.ledger.review(row['person'], review(followup_allowed=True))
        with self.assertRaisesRegex(Blocked, 'seven days'):
            self.ledger.reserve(row['person'], row['endpoint'], 'followup')

    def test_followup_does_not_count_as_first_and_only_once(self):
        row, _ = self.sent()
        self.ledger.close()
        later = '2026-11-17T08:00:00+00:00'
        self.ledger = Ledger(self.path, later)
        self.ledger.review(row['person'], review(followup_allowed=True, history_checked_at=later, policy_checked_at=later, backup_verified_at=later))
        self.ledger.cap('email', 150, 'reverified capacity')
        attempt = self.ledger.reserve(row['person'], row['endpoint'], 'followup')['attempt']
        self.ledger.result(attempt, 'sent', 'followup confirmation', 'email:test:followup-message')
        report = self.ledger.report('2026-11-17')
        self.assertEqual(0, report['provider_confirmed_unique_first_contacts'])
        self.assertEqual(1, report['confirmed_followup_sends'])
        with self.assertRaisesRegex(Blocked, 'At most one'):
            self.ledger.reserve(row['person'], row['endpoint'], 'followup')

    def test_outcomes_are_distinct_and_need_attribution(self):
        row, attempt = self.sent()
        with self.assertRaises(Blocked):
            self.ledger.event(row['person'], 'delivered', 'unattributed')
        self.ledger.event(row['person'], 'reply', 'provider-reply', attempt)
        report = self.ledger.report('2026-11-10')
        self.assertEqual(1, report['reply_creators_observed_on_day'])
        self.assertEqual(0, report['delivered_creators_observed_on_day'])
        self.assertEqual(0, report['participation_creators_observed_on_day'])
        self.assertEqual(1, report['sent_cohort_reply_rate_so_far'])
        self.ledger.event(row['person'], 'participation', 'public-relevant-comment')
        self.assertEqual(1, self.ledger.report('2026-11-10')['participation_creators_observed_on_day'])

    def test_no_double_event_count_and_reply_stops_sequence(self):
        row, attempt = self.sent()
        for _ in range(2):
            self.ledger.event(row['person'], 'reply', 'same-provider-reply', attempt)
        self.assertEqual(1, self.ledger.db.execute('SELECT COUNT(*) FROM events').fetchone()[0])
        with self.assertRaisesRegex(Blocked, 'Reply or bounce'):
            self.ledger.reserve(row['person'], row['endpoint'], 'followup')

    def test_provider_id_required_unique_and_result_idempotent(self):
        one = self.ready('one'); two = self.ready('two')
        a = self.reserve(one); b = self.reserve(two)
        with self.assertRaises(Blocked):
            self.ledger.result(a, 'sent', 'tool says sent')
        self.ledger.result(a, 'sent', 'tool says sent', 'email:test:actual-provider-id')
        self.assertTrue(self.ledger.result(a, 'sent', 'tool says sent', 'email:test:actual-provider-id')['unchanged'])
        import sqlite3
        with self.assertRaises(sqlite3.IntegrityError):
            self.ledger.result(b, 'sent', 'second-send-claim', 'email:test:actual-provider-id')
        self.assertEqual(1, self.ledger.report('2026-11-10')['provider_confirmed_unique_first_contacts'])

    def test_private_checkpoint_roundtrip_no_overwrite(self):
        row, _ = self.sent()
        self.ledger.suppress(row['person'], 'refusal evidence')
        checkpoint = self.ledger.checkpoint()
        other = Ledger(Path(self.temp.name) / 'restored.sqlite', NOW)
        try:
            other.restore(checkpoint)
            self.assertEqual(self.ledger.report('2026-11-10'), other.report('2026-11-10'))
            with self.assertRaisesRegex(Blocked, 'empty'):
                other.restore(checkpoint)
        finally:
            other.close()
        self.assertEqual(0, self.path.stat().st_mode & 0o077)

    def test_legacy_import_idempotent_and_missing_confirmation_blocked(self):
        records = [{'id': 'old-one', 'name': 'one', 'email': 'one@example.org', 'contact_source': 'https://example.org/one', 'relevance_source': 'https://example.org/work', 'relevance': 'Useful work', 'status': 'sent', 'message_id': 'real-provider-message', 'message_url': 'https://mail.example/message', 'attempted_at': NOW}, {'id': 'old-two', 'name': 'two', 'email': 'two@example.org', 'contact_source': 'https://example.org/two', 'relevance_source': 'https://example.org/work', 'relevance': 'Useful work', 'status': 'sent', 'attempted_at': NOW}]
        data = {'date_utc': '2026-11-10', 'records': records}
        self.assertEqual({'imported_confirmed': 1, 'imported_unresolved': 1}, self.ledger.import_legacy(data))
        self.assertEqual({'imported_confirmed': 0, 'imported_unresolved': 0}, self.ledger.import_legacy(data))
        report = self.ledger.report('2026-11-10')
        self.assertEqual(1, report['provider_confirmed_unique_first_contacts'])
        self.assertEqual(149, report['shortfall'])
        self.assertEqual(1, report['unresolved_attempts_all_days'])
        self.assertFalse(report['goal_met'])

    def test_legacy_same_timestamp_different_recipients_not_skipped(self):
        records = []
        for name in ('one', 'two'):
            records.append({'name': name, 'email': name + '@example.org', 'contact_source': 'https://example.org/' + name, 'relevance_source': 'https://example.org/work', 'relevance': 'Useful work', 'status': 'sent', 'message_id': 'provider-' + name, 'attempted_at': NOW})
        data = {'date_utc': '2026-11-10', 'records': records}
        self.assertEqual(2, self.ledger.import_legacy(data)['imported_confirmed'])
        self.assertEqual(2, self.ledger.report('2026-11-10')['provider_confirmed_unique_first_contacts'])
        self.assertEqual(0, self.ledger.import_legacy(data)['imported_confirmed'])

    def test_profile_queries_and_source_queries_are_preserved(self):
        one = self.ledger.add(candidate('one', identity='https://social.example/profile.php?id=111', relevance_source='https://video.example/watch?v=abc'))
        two = self.ledger.add(candidate('two', identity='https://social.example/profile.php?id=222'))
        self.assertNotEqual(one['person'], two['person'])
        source = self.ledger.db.execute('SELECT relevance_source FROM endpoints WHERE id=?', (one['endpoint'],)).fetchone()[0]
        self.assertEqual('https://video.example/watch?v=abc', source)

    def test_reject_existing_world_readable_ledger(self):
        os.chmod(self.path, 0o644)
        with self.assertRaisesRegex(Blocked, 'owner-only'):
            Ledger(self.path, NOW)

    def test_reject_symlink_ledger(self):
        link = Path(self.temp.name) / 'link.sqlite'
        link.symlink_to(self.path)
        with self.assertRaisesRegex(Blocked, 'symbolic link'):
            Ledger(link, NOW)

    def test_unknown_resolution_requires_actual_send_timestamp(self):
        row = self.ready()
        attempt = self.reserve(row)
        self.ledger.result(attempt, 'unknown', 'provider timeout')
        self.ledger.close()
        self.ledger = Ledger(self.path, '2026-11-11T08:00:00+00:00')
        with self.assertRaisesRegex(Blocked, 'actual provider send time'):
            self.ledger.result(attempt, 'sent', 'reconciled', 'email:test:real-id')
        self.ledger.result(attempt, 'sent', 'reconciled', 'email:test:real-id', at=NOW)
        self.assertEqual(1, self.ledger.report('2026-11-10')['provider_confirmed_unique_first_contacts'])
        self.assertEqual(0, self.ledger.report('2026-11-11')['provider_confirmed_unique_first_contacts'])

    def test_legacy_requires_actual_attempt_time_and_imports_refusal_first(self):
        record = {'id': 'legacy', 'name': 'one', 'email': 'one@example.org', 'contact_source': 'https://example.org/one', 'relevance_source': 'https://example.org/work', 'relevance': 'Relevant work', 'status': 'sent', 'message_id': 'real-id', 'verified_at': NOW}
        data = {'date_utc': '2026-11-10', 'records': [record], 'suppression': [{'name': 'blocked', 'email': 'blocked@example.org', 'source': 'https://example.org/blocked', 'reason': 'No AI emails', 'checked_at': NOW}]}
        result = self.ledger.import_legacy(data)
        self.assertEqual(1, result['imported_unresolved'])
        self.assertEqual(0, self.ledger.report('2026-11-10')['provider_confirmed_unique_first_contacts'])
        self.assertEqual(1, self.ledger.report('2026-11-10')['suppressed_creators_total'])

    def test_legacy_unknown_can_be_reconciled_without_duplicate(self):
        record = {'id': 'legacy', 'name': 'one', 'email': 'one@example.org', 'contact_source': 'https://example.org/one', 'relevance_source': 'https://example.org/work', 'relevance': 'Relevant work', 'status': 'outcome_uncertain', 'attempted_at': NOW}
        data = {'date_utc': '2026-11-10', 'records': [record]}
        self.ledger.import_legacy(data)
        record.update(status='sent', message_id='real-id')
        self.assertEqual(1, self.ledger.import_legacy(data)['imported_confirmed'])
        self.assertEqual(0, self.ledger.report('2026-11-10')['unresolved_attempts_all_days'])
        self.assertEqual(1, self.ledger.db.execute('SELECT COUNT(*) FROM attempts').fetchone()[0])

    def test_cap_cannot_be_bypassed_by_timezone_switch(self):
        one = self.ready('one'); two = self.ready('two')
        self.ledger.cap('email', 1, 'verified rolling limit')
        attempt = self.reserve(one)
        self.ledger.result(attempt, 'sent', 'provider confirmation', 'email:test:one')
        for zone in ('UTC', 'Pacific/Honolulu', 'Pacific/Kiritimati'):
            with self.subTest(zone=zone), self.assertRaisesRegex(Blocked, 'exhausted'):
                self.ledger.reserve(two['person'], two['endpoint'], tz=zone)

    def test_reservation_requires_durable_checkpoint_before_envelope(self):
        row = self.ready()
        reserved = self.ledger.reserve(row['person'], row['endpoint'])
        self.assertNotIn('body', reserved)
        self.assertNotIn('address', reserved)
        with self.assertRaisesRegex(Blocked, 'receipt'):
            self.ledger.confirm_checkpoint(reserved['attempt'], '')
        checkpoint = self.ledger.checkpoint()
        self.assertEqual(reserved['attempt'], checkpoint['tables']['attempts'][0]['id'])
        envelope = self.ledger.confirm_checkpoint(reserved['attempt'], 'durable private checkpoint with verified reservation')
        self.assertEqual('one@example.org', envelope['address'])
        self.ledger.suppress(row['person'], 'no contact')
        with self.assertRaises(Blocked):
            self.ledger.confirm_checkpoint(reserved['attempt'], 'old receipt')

    def test_legacy_missing_time_can_be_reconciled_to_earlier_day(self):
        self.ledger.close()
        self.ledger = Ledger(self.path, '2026-11-11T08:00:00+00:00')
        record = {'id': 'legacy', 'name': 'one', 'email': 'one@example.org', 'contact_source': 'https://example.org/one', 'relevance_source': 'https://example.org/work', 'relevance': 'Relevant work', 'status': 'sent', 'message_id': 'real-id', 'verified_at': NOW}
        data = {'date_utc': '2026-11-10', 'records': [record]}
        self.ledger.import_legacy(data)
        record['attempted_at'] = NOW
        self.assertEqual(1, self.ledger.import_legacy(data)['imported_confirmed'])
        self.assertEqual(1, self.ledger.db.execute('SELECT COUNT(*) FROM attempts').fetchone()[0])
        self.assertEqual(1, self.ledger.report('2026-11-10')['provider_confirmed_unique_first_contacts'])
        self.assertEqual(0, self.ledger.report('2026-11-11')['unresolved_attempts_all_days'])

    def test_legacy_form_acceptance_has_receipt_not_fabricated_message_id(self):
        record = {'id': 'form-1', 'name': 'creator', 'channel': 'contact_form', 'contact_url': 'https://example.org/contact', 'contact_source': 'https://example.org/contact', 'relevance_sources': ['https://example.org/work'], 'status': 'accepted', 'confirmation_text': 'Thanks, form accepted.', 'attempted_at': NOW}
        self.ledger.import_legacy({'date_utc': '2026-11-10', 'records': [record]})
        report = self.ledger.report('2026-11-10')
        self.assertEqual(1, report['confirmed_first_form_acceptances'])
        self.assertEqual(0, report['confirmed_first_sends'])
        self.assertEqual(1, report['provider_confirmed_unique_first_contacts'])
        self.assertIsNone(self.ledger.db.execute('SELECT provider_id FROM attempts').fetchone()[0])

    def test_identity_only_suppression_blocks_later_email(self):
        self.ledger.import_legacy({'records': [], 'suppression': [{'name': 'one', 'source': 'https://example.org/one', 'reason': 'No unsolicited invitations', 'checked_at': NOW}]})
        row = self.ready()
        with self.assertRaisesRegex(Blocked, 'suppressed'):
            self.reserve(row)

    def test_policy_denial_is_not_unknown_or_retriable_failure(self):
        row = self.ready()
        attempt = self.reserve(row)
        self.ledger.result(attempt, 'denied', 'explicit tool denial, not executed')
        with self.assertRaisesRegex(Blocked, 'authorization resolution'):
            self.reserve(row)
        report = self.ledger.report('2026-11-10')
        self.assertEqual(1, report['policy_denied_attempts_all_days'])
        self.assertEqual(0, report['unresolved_attempts_all_days'])
        self.assertEqual(0, report['provider_confirmed_unique_first_contacts'])

    def test_checkpoint_confirmation_rechecks_reduced_channel_cap(self):
        row = self.ready()
        attempt = self.reserve(row)
        self.ledger.cap('email', 0, 'channel paused')
        with self.assertRaisesRegex(Blocked, 'exhausted'):
            self.ledger.confirm_checkpoint(attempt, 'durable receipt')
        self.ledger.cap('email', 1, 'capacity restored with verification')
        self.assertEqual('one@example.org', self.ledger.confirm_checkpoint(attempt, 'durable receipt')['address'])

    def test_form_acceptance_blocks_email_for_same_creator(self):
        self.ledger.import_legacy({'date_utc': '2026-11-10', 'records': [{'id': 'form', 'name': 'one', 'channel': 'contact_form', 'contact_url': 'https://example.org/one', 'contact_source': 'https://example.org/one', 'relevance_sources': ['https://example.org/work'], 'status': 'accepted', 'confirmation_text': 'Accepted', 'attempted_at': NOW}]})
        row = self.ready()
        with self.assertRaisesRegex(Blocked, 'Already contacted'):
            self.reserve(row)

    def test_legacy_without_id_or_actual_time_requires_stable_source_id(self):
        record = {'name': 'one', 'email': 'one@example.org', 'contact_source': 'https://example.org/one', 'relevance_source': 'https://example.org/work', 'relevance': 'Relevant work', 'status': 'sent', 'message_id': 'real-id', 'verified_at': NOW}
        with self.assertRaisesRegex(Blocked, 'stable source ID'):
            self.ledger.import_legacy({'date_utc': '2026-11-10', 'records': [record]})
        self.assertEqual(0, self.ledger.db.execute('SELECT COUNT(*) FROM attempts').fetchone()[0])

    def test_email_cannot_bypass_provider_confirmation_as_form_acceptance(self):
        row = self.ready()
        attempt = self.reserve(row)
        with self.assertRaisesRegex(Blocked, 'contact_form'):
            self.ledger.result(attempt, 'accepted', 'not a provider message confirmation')
        self.assertEqual(0, self.ledger.report('2026-11-10')['provider_confirmed_unique_first_contacts'])

    def test_report_timezone_and_empty_denominator(self):
        self.sent()
        self.assertEqual(1, self.ledger.report('2026-11-10', 'Asia/Shanghai')['provider_confirmed_unique_first_contacts'])
        empty = self.ledger.report('2026-11-09')
        self.assertIsNone(empty['sent_cohort_reply_rate_so_far'])
        self.assertEqual(150, empty['shortfall'])

    def test_cli_report_only_aggregate_data(self):
        self.sent()
        result = subprocess.run([sys.executable, '-m', 'arc.growth', '--db', str(self.path), 'report', '--day', '2026-11-10'], capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(1, json.loads(result.stdout)['provider_confirmed_unique_first_contacts'])
        self.assertNotIn('one@example.org', result.stdout)
        self.assertNotIn('actual-provider', result.stdout)
        self.assertNotIn('Your tutorial', result.stdout)


if __name__ == '__main__':
    unittest.main()
