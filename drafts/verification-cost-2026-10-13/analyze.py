"""Recompute descriptive pilot results from frozen inputs. Standard library only.
No semantic answer grading and no changes to raw participant files.
"""
from pathlib import Path
from datetime import datetime
import hashlib
import json

BASE = Path(__file__).resolve().parent
ARMS = ('redo', 'report-only', 'source-locators', 'reproducible')
SAMPLE = {'C02', 'C03', 'C08', 'C10'}


def read(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_lock(name):
    manifest = read(BASE / name)
    for path, expected in manifest['files'].items():
        actual = digest(BASE / path)
        if actual != expected:
            raise ValueError(f'{name}: changed file {path}: {actual} != {expected}')
    return {'manifest_sha256': digest(BASE / name), 'verified_file_count': len(manifest['files'])}


def score(claims, labels):
    verdicts = {}
    for claim in claims:
        cid = claim['id']
        if cid not in labels or cid in verdicts:
            raise ValueError('Unknown or duplicate claim: ' + cid)
        verdict = claim.get('verdict', claim.get('answer'))
        if verdict not in ('supported', 'contradicted', 'unresolved'):
            raise ValueError('Unknown verdict: ' + str(verdict))
        verdicts[cid] = verdict
    errors = {cid for cid, error in labels.items() if error}
    correct = set(labels) - errors
    flagged = {cid for cid, v in verdicts.items() if v == 'contradicted'}
    tp = len(flagged & errors)
    fp = len(flagged & correct)
    checked_errors = len(set(verdicts) & errors)
    checked_correct = len(set(verdicts) & correct)
    return {'tp': tp, 'fn_report_wide': len(errors) - tp, 'fp': fp,
            'error_denominator_report_wide': len(errors),
            'recall_report_wide': tp / len(errors),
            'error_denominator_checked_only': checked_errors,
            'recall_checked_only': tp / checked_errors if checked_errors else None,
            'correct_denominator_report_wide': len(correct),
            'false_positive_rate_report_wide': fp / len(correct),
            'correct_denominator_checked_only': checked_correct,
            'false_positive_rate_checked_only': fp / checked_correct if checked_correct else None,
            'checked': len(verdicts), 'unchecked': len(labels) - len(verdicts),
            'unresolved_checked': sum(v == 'unresolved' for v in verdicts.values()),
            'wrong_validations': sum(verdicts.get(cid) == 'supported' for cid in errors),
            'flagged_ids': sorted(flagged), 'normalized_verdicts': verdicts,
            'semantic_answer_accuracy': None, 'semantic_grading_status': 'not computed here; see independent_audit'}


def measurements(data):
    return data.get('measurement', data.get('measurements'))


def elapsed(m):
    for key in ('cumulative_elapsed_seconds', 'elapsed_seconds', 'sample_elapsed_seconds'):
        if key in m:
            return m[key]
    raise ValueError('No elapsed measurement')


def source_reads(m):
    ledger = m.get('ledger', m.get('command_read_event_ledger'))
    events = []
    for entry in ledger:
        for event in entry.get('reads', entry.get('events', [])):
            path = event.get('path', '') or ''
            if '/corpus/docs/' in path:
                events.append({'path': path.split('/corpus/docs/')[-1],
                               'bytes': event.get('bytes', event.get('bytes_read', event.get('raw_file_bytes'))),
                               'visibility': event.get('visibility', event.get('kind'))})
    unique = {}
    for event in events:
        unique[event['path']] = event['bytes']
    known = all(e['bytes'] is not None for e in events)
    total = sum(e['bytes'] for e in events) if known else None
    distinct = sum(unique.values()) if known else None
    return {'source_file_read_events': len(events), 'source_file_bytes_read': total,
            'distinct_source_file_bytes': distinct,
            'repeated_source_file_read_bytes': total - distinct if known else None,
            'events': events,
            'note': 'File I/O proxy only; may include internal reads. Not model attention, tokens, or billing.'}


def analyze():
    integrity = {name: check_lock(name) for name in ('FROZEN-MANIFEST.json', 'RESULTS-LOCK.json')}
    reference = read(BASE / 'coordinator-only/reference-labels.json')
    labels = {row['id']: row['candidate_is_error'] for row in reference}
    author = read(BASE / 'author-preparation-measurement.json')
    dispatch = read(BASE / 'dispatch-ledger.json')
    output = {'status': 'bounded pilot; not full task acceptance', 'integrity': integrity,
              'preregistration_url': dispatch['preregistration_url'],
              'author_preparation': author, 'arms': {},
              'semantic_quality': 'Designer does not grade semantic answers; see separately attributed independent_audit.',
              'input_tokens': None, 'output_tokens': None, 'billed_usd': None}
    for arm in ARMS:
        directory = BASE / 'results' / arm
        raw = read(directory / 'final.json')
        m = measurements(raw)
        ids = [claim['id'] for claim in raw['claims']]
        if len(ids) != len(set(ids)) or set(ids) != set(labels):
            raise ValueError('Full result IDs invalid for ' + arm)
        end = m['final_completion_utc']
        delta = (datetime.fromisoformat(end) - datetime.fromisoformat(m['first_work_start_utc'])).total_seconds()
        if abs(delta - elapsed(m)) > .001:
            raise ValueError('Clock arithmetic mismatch for ' + arm)
        entry = {'full_raw_elapsed_seconds': elapsed(m),
                 'full_postwrite_elapsed_seconds': None,
                 'comparison_elapsed_seconds': elapsed(m),
                 'comparison_timing_boundary': 'raw final recorded boundary; last persistence may be excluded',
                 'invocations': m.get('invocation_count', m.get('tool_invocation_count')),
                 'source_read_proxy': source_reads(m), 'answer_record_count': len(ids),
                 'semantic_correct_answers': None, 'semantic_supported_answers': None}
        if arm == 'redo':
            entry['detection_metrics'] = None
        else:
            sample_path = directory / 'sample.json'
            sample = read(sample_path)
            if {c['id'] for c in sample['claims']} != SAMPLE:
                raise ValueError('Wrong fixed sample: ' + arm)
            advertised = raw.get('sample_frozen_sha256', raw.get('sample_sha256'))
            if advertised != digest(sample_path):
                raise ValueError('Changed sample: ' + arm)
            entry['sample'] = score(sample['claims'], labels)
            entry['full'] = score(raw['claims'], labels)
            entry['sample_raw_elapsed_seconds'] = elapsed(measurements(sample))
            entry['sample_postwrite_elapsed_seconds'] = None
            entry['full_incremental_raw_seconds'] = elapsed(m) - entry['sample_raw_elapsed_seconds']
            entry['sample_revisions_raw'] = raw.get('sample_revisions')
            entry['sample_verdict_changes_computed'] = [cid for cid in SAMPLE if
                entry['sample']['normalized_verdicts'][cid] != entry['full']['normalized_verdicts'][cid]]
            completion = directory / 'completion.json'
            if completion.exists():
                c = read(completion)
                entry['full_postwrite_elapsed_seconds'] = c['total_elapsed_seconds']
                entry['sample_postwrite_elapsed_seconds'] = c['sample_write_completed_elapsed_seconds']
                entry['full_incremental_postwrite_seconds'] = c['full_stage_incremental_elapsed_seconds']
                entry['comparison_elapsed_seconds'] = c['total_elapsed_seconds']
                entry['comparison_timing_boundary'] = c['endpoint_note']
            entry['measured_shared_author_plus_comparison_seconds'] = author['measured_elapsed_seconds'] + entry['comparison_elapsed_seconds']
        if arm == 'reproducible':
            entry['script_execution'] = 'Provided reproduction script inspected, not executed; package-available condition only.'
            entry['internal_hash_read_bytes_reported'] = m['internal_source_read_bytes']
            entry['script_potential_reads_not_observed'] = {'read_events': 14, 'bytes': 63676,
                'note': 'Design-auditor calculation if reproduce.py ran; not participant usage and excluded from measured I/O.'}
        output['arms'][arm] = entry
    audit = BASE / 'review/results-audit.md'
    output['independent_audit'] = {
        'path': 'review/results-audit.md', 'sha256': digest(audit),
        'reviewer': '/root/cost22_auditor', 'relationship': 'separate session, same operator',
        'reported_redo_correct_answers': 12, 'reported_redo_evidence_supported_answers': 12,
        'reported_full_verifier_correct_answers_each': 12,
        'reported_full_verifier_correct_corrections_each': 4,
        'reported_sample_correct_answers_each': 4,
        'disposition': 'reviewed partial pilot; full #22 acceptance not recommended',
        'provenance_note': 'These numbers transcribe the separate auditor finding; analyze.py does not perform semantic grading.'}
    output['separate_review_measurements'] = [
        {'path': 'review/design-audit.md', 'elapsed_seconds': 97, 'boundary': 'initial prose writing; unknown bootstrap excluded'},
        {'path': 'review/results-audit.md', 'elapsed_seconds': 125, 'start_utc': '2026-10-13T02:26:29Z', 'end_utc': '2026-10-13T02:28:34Z'},
        {'path': 'review/redo-checks-report.md', 'elapsed_seconds': 58.497169, 'start_utc': '2026-10-13T02:26:37.354820+00:00', 'end_utc': '2026-10-13T02:27:35.851989+00:00'},
        {'path': 'review/report-checks-redo-locators.md', 'elapsed_seconds': 73.583732, 'start_utc': '2026-10-13T02:26:41.116637+00:00', 'end_utc': '2026-10-13T02:27:54.700369+00:00'},
        {'path': 'review/locators-checks-data.md', 'elapsed_seconds': 54.166620, 'start_utc': '2026-10-13T02:26:49.113003+00:00', 'end_utc': '2026-10-13T02:27:43.279623+00:00'}]
    output['coordinator_total_seconds'] = None
    baseline = output['arms']['redo']['comparison_elapsed_seconds']
    for arm in ARMS[1:]:
        entry = output['arms'][arm]
        entry['verifier_only_time_ratio_to_redo'] = entry['comparison_elapsed_seconds'] / baseline
    return output


def markdown(result):
    lines = ['# Verification-cost pilot: observed results', '',
        'DRAFT synthesis for final review. The separate-session [result audit](review/results-audit.md) found all twelve redo answers and all twelve reconstructed answers per verifier correct and evidence-supported, with four correct corrections per verifier. This is the auditor’s assessment, not semantic grading by the material designer. The auditor is under the same operator, not an outside participant. This bounded run does not satisfy the full acceptance criteria of task #22: author costs are incomplete and the supplied reproduction script was not executed by its participant. Task #22 remains unaccepted and open for further work; this is not an accepted report.', '',
        'The three full verification sessions took longer than the redo session in this run. This observation does not isolate verification effort: verifiers also wrote a sample checkpoint and a full result, while redo wrote only a final result. One run per condition cannot establish a general cost advantage or reliable ordering.', '',
        f"[Public preregistration]({result['preregistration_url']}) preceded all recorded experimental starts. `FROZEN-MANIFEST.json` fixes materials and `RESULTS-LOCK.json` fixes raw results. `python3 analyze.py` verifies both and regenerates this document and `summary.json`; raw outputs remain unchanged.", '',
        '| Condition | Sample s (raw) | Full s (comparison) | Full / redo | Shared measured author + full s |',
        '|---|---:|---:|---:|---:|']
    for arm, entry in result['arms'].items():
        label = 'package available (script not run)' if arm == 'reproducible' else arm
        sample = entry.get('sample_raw_elapsed_seconds')
        ratio = entry.get('verifier_only_time_ratio_to_redo')
        total = entry.get('measured_shared_author_plus_comparison_seconds')
        lines.append(f"| {label} | {sample:.6f} | {entry['comparison_elapsed_seconds']:.6f} | {ratio:.3f} | {total:.6f} |" if sample is not None else f"| {label} | — | {entry['comparison_elapsed_seconds']:.6f} | 1.000 | — |")
    lines += ['', 'Full times include sample-stage work. Official CLI administration occurred before each timer and is excluded; clock checks, input reading, judgment and output work are included within the recorded boundary. Source-locators uses its separate completion.json postwrite boundary: raw full 113.910203 s versus postwrite 113.910817 s; raw sample 57.270466 s versus postwrite 57.270773 s. Other arms lack a comparable separate completion file and use their raw recorded endpoint, just before last persistence. These small boundary differences are retained, not silently standardized.', '',
        'Each verifier found the same two sampled errors (C03/C10): TP=2, report-wide FN=2, FP=0, unchecked=8, checked-unresolved=0. Sample whole-report recall is 2/4=50%; checked-only recall is 2/2=100%. Each full verifier flagged C03/C06/C10/C12: TP=4, FN=0, FP=0, unchecked=0, checked-unresolved=0. Full recall is 4/4=100%. The FP denominator is eight correct report claims (two checked correct claims at sample stage). These are mechanical detection scores against designer labels, not independent semantic grades. The redo supplied twelve answers. Designer-computed semantic fields remain null; summary.json separately attributes 12/12 correct and evidence-supported redo answers and 12/12 full verifier answers to the auditor. The auditor reports 4/4 checked sample answers, not complete report reconstruction.', '',
        'The sample was purposively selected by the designer and contains two of four planted errors. It is not random or representative; no confidence interval or whole-report correctness inference follows from it. Original source bytes are real public repository documents, but the incorrect candidate answers are synthetic. The corpus is two short documents (9,028 bytes) pinned at commit 46963018ffa591fe20c7a598eb1ac66255b9c171.', '',
        '| Condition | Source file read events | Distinct source bytes | Total source I/O bytes | Repeated source I/O bytes |',
        '|---|---:|---:|---:|---:|']
    for arm, entry in result['arms'].items():
        label = 'package available (script not run)' if arm == 'reproducible' else arm
        p = entry['source_read_proxy']
        lines.append(f"| {label} | {p['source_file_read_events']} | {p['distinct_source_file_bytes']} | {p['source_file_bytes_read']} | {p['repeated_source_file_read_bytes']} |")
    lines += ['', 'I/O totals are duplication proxies, not tokens, actual attention or billed work. Source-locators read both files internally twice but exposed selected excerpts (6,598 reported source-text bytes). Reproducible read both files as source text once (9,028 bytes) and internally reread them for hashes (9,028 bytes). It inspected reproduce.py but did not execute it. The design-auditor calculation of 14 internal reads/63,676 bytes describes what that script would do if executed, and is not charged as participant activity. Thus this condition tested package availability, not an executed reproducible workflow.', '',
        'Measured shared author preparation was 171.807927 seconds (2026-10-13 02:19:45–02:22:36.807927 UTC), including design, packaging and QA. Earlier context/source exploration was unmeasured. The table adds the entire shared measured author time to each full verifier as a descriptive allocation, not an exact total, causal format-specific expense, strict upper bound, or break-even estimate. Per-format total author cost, exact model telemetry, tokens, dollars and coordinator costs are unknown; review observations are separate from these arm totals. Mechanical package-write milliseconds cannot replace author labor.', '',
        'Separate recorded review intervals are: initial design audit 97 s (bootstrap unknown); result audit 125 s (02:26:29–02:28:34 UTC); redo checks report 58.497169 s (02:26:37.354820–02:27:35.851989); report checks redo/locators 73.583732 s (02:26:41.116637–02:27:54.700369); locators checks package 54.166620 s (02:26:49.113003–02:27:43.279623), all on 2026-10-13. These are separately observed session durations, some concurrent, and omit small write/return tails and later coordination. Do not sum them as wall-clock completion time or treat them as complete billed labor. Exact review provenance is in review/*.md and summary.json.', '',
        'Sessions were fresh but operated by one maintainer within a shared filesystem; isolation was procedural, not a security boundary. There is no external adoption or independent-operator evidence. Verifiers saw some unsampled facts while reading sources. Stage work is paired and reused, and source exposure/reporting workloads differ. Temporary timing-file writes and delayed initial elapsed checks are disclosed in raw accounts. All four arms completed inside the stated budget; no outcome-selected reruns are reported. Automation remained paused according to the dispatch record.', '',
        'Corrections must preserve raw outputs and manifests, record a versioned analysis change and receive cross-review. P1/P2/P5/P6 require useful evidence, inspectable mistakes and honest limitations; P3/P4/A2 grant no credit or governance authority from this pilot. Existing v1 acceptance controls remain in force.', '']
    return '\n'.join(lines)


if __name__ == '__main__':
    result = analyze()
    (BASE / 'summary.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    (BASE / 'README.md').write_text(markdown(result))
    print('Verified frozen materials and locked raw results; wrote summary.json and README.md.')
