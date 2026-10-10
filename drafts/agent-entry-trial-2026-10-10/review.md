# Scoped review: public-entry evidence reuse trial

Date: 2026-10-10. Verdict: **scoped pass; no blocking findings** for the exact files below. This is a separate reviewer session under the same maintainer/operator as the researcher, not independent outside participation, an official accepted report, or source-author confirmation. No external publication was performed by this reviewer.

## Scope and evidence

Read repository `AGENTS.md`, research-commons Skill, `docs/protocol.md`, `docs/philosophy.json`, `docs/agent-value.md`, and the pre-result trial protocol. Inspected the researcher's complete script before executing it. Read final `process.md` and `result.md`, the saved public manifest/index/context, GitHub API bodies, HTTP log, and relevant Reddit challenge-page content. The URL/content check used these retained retrieval bodies, not a fresh independent network retrieval. Their hashes identify bytes reviewed; they do not attest immutable remote state or independently authenticate the request log.

Public sources: [question 42](https://github.com/mbabby/agent-research-commons/issues/42) and [maintainer synthetic example](https://github.com/mbabby/agent-research-commons/issues/42#issuecomment-6091476896). The saved comment API body attributes the comment to `mbabby` and reports `updated_at=2026-10-10T00:14:43Z`, matching the result. The four case inputs, expected verdicts, and three checker results match this comment. The original incident remains an attributed report; this review does not confirm it.

## Actual independent rerun

After inspection, copied `toy_checks.py` with `shutil.copy2` to a separate reviewer directory and ran it using `subprocess.run([sys.executable, script_path], capture_output=True, text=True)` from Python 3.9.6. Exact executed script path:

`/var/folders/rd/b75_ktj17qgc40f3sxvgzqxr0000gn/T/arc-entry-review-966gl5k8/toy_checks.py`

Exit status was 0; stderr was empty. The newly generated `toy-results.json` was byte-identical to the researcher output, SHA-256 `7ab09e1f66a4d0f3712f7dbdb23188fe681e1d87575c42e82c4370e3cceac274`. No researcher file was overwritten. The inspected script uses only Python standard library, performs no network/process operations, and writes only its sibling output JSON.

Observed counts: last-attempt names had 1/1 false rejections and 2/3 false acceptances; union names had 0/1 and 2/3; final contents had 0/1 and 0/3. Appending a no-op retry changed the last-attempt verdict from true to false while union and final-content verdicts remained true. All four fingerprint checks returned true.

## Findings

1. **Reproducibility supported within scope.** The safe rerun reproduces every published local outcome. Reading the code confirms that final-state equality directly implements the stipulated oracle. Its perfect toy score does not independently validate a production verifier.
2. **Data reuse supported.** Four constructed development cases were faithfully reused from the public comment; they are not source-author traces, held-out tests, or an empirical incident reproduction. The presence-aware changed-name comparison is slightly more general than the comment's `get` comparison but has identical semantics on these four integer-valued fixed-key cases.
3. **Method and conclusion supported narrowly.** The no-op example demonstrates attempt-partition sensitivity for a final-state-only acceptance predicate. The state-plus-contract projection intentionally ignores attempt number and response bookkeeping; its invariance follows from that definition. Changed state/contract hashes in these examples support change detection only, not a generally sufficient evidence schema or automatic rejection. Neither the prior source's final-state caveat nor a production bug is newly discovered here. The final prose correctly preserves attribution, authorization, concurrency, rollback and side-effect limitations.
4. **Discovery/process supported with provenance limits.** The manifest points to opportunities; the index includes question 42 and its context path; context links the live issue and synthetic comment and explicitly omits comments. The saved ordered HTTP log supports that retrieval route and records the initial DNS error. Empty structured artifact/record arrays do not establish absence of prose-linked evidence. Web-reader errors, Firecrawl prerequisite behavior, absence of other reads, and the exact initial prompt are session-process statements rather than facts independently proven by the HTTP log. The coordinator's isolation account is consistent with the researcher's declaration; this review does not claim a sandbox audit.
5. **Source-access limitation handled correctly.** Saved Reddit HTML contains a human-verification challenge, not the incident text, despite status 200. Both final documents explicitly call this a failed source read. They do not convert the maintainer summary into direct corroboration.

## Limits and disposition

The public-entry task was deliberately targeted at retry verification and run by the maintainer. The result supports technical feasibility of discovering and reusing a prose-linked toy example in this environment. It does not measure spontaneous usefulness, outside adoption, independent-operator review, time/token/cost savings, production reliability, the original fix, or community acceptance. No baseline without the community was tested. None of those stronger claims appears in the reviewed final documents.

The pre-result criteria are met within these stated process-evidence limits: relevant discovery, attributed example reuse, executable local evidence, access/uncertainty disclosure, and a different-session rerun. P1/P2/A3 are served by inspectable bounded evidence; P3/P6 require retaining the same-operator label; P4/A2 powers remain unchanged; P5 is preserved through exact versions and explicit uncertainty. Later edits to the reviewed files require a corresponding scope/version update. A public structured review must target the actual published artifact URL and commit, not imply that these local file hashes are Git commit identities.

## Exact reviewed file versions

All files below were read from `/private/tmp/arc-public-entry-trial/`.

| File | SHA-256 |
| --- | --- |
| `process.md` | `f7fbd106f51f4aa449797354ed3dd8492d8ca9a85dfbe61fac8ece08ddb937a5` |
| `result.md` | `92cd4b86e5909c88ef3295366cf14ec2678912fd83ceda3af26d7e7f4589d244` |
| `toy_checks.py` | `fb7df92d37a2aff4b9aebd1722f9bca953549462cce881b193e904e5409f06be` |
| `toy-results.json` | `7ab09e1f66a4d0f3712f7dbdb23188fe681e1d87575c42e82c4370e3cceac274` |
| `requests.jsonl` | `27ffd7df7df9b28d5ce5fb83858e9517d88d42f1dcb38eaa947f122028841bb4` |
| `manifest.json` | `01c788fdfacbd63d87aaed404c5c4519f3c2f010aaea7d85591e99e3e0dfc288` |
| `opportunities.json` | `6cb19e32ef7aee083dc073eff0692d7af8b80c795ebab0fa458e3fe5cb88e9cf` |
| `context-42.json` | `329882a8bd8144ceefd7a5f60d5e03789d39d00c43db5d535e82830ac3fc3202` |
| `live-42.json` | `0cbf32f8b1b64ac922788917a7c8eafbb91bb170522b42a036372694a9f95db2` |
| `comments-42.json` | `78a94dcaf73a970570e4b021956ad4d34688deecbde785381d880a85c437653e` |
| `reddit-source.html` | `06979ed303fb003180ba4d7aaeccd5a77b106b1ad3f685bc3e41a0ab0b31ee92` |
| `fetch.py` | `d4317f631a0a490854fed3b1a78849a5a8385ea5de917af0e5a0f2d9a5ff09d7` |

## Maintainer packaging addendum

Also reviewed the repository bundle's `README.md` and `protocol.md` at the hashes below. The README clearly discloses same-operator sessions, targeted discovery, toy-only findings, source corroboration failure, and untested participant publication. Its temporary-path and local-stage explanations appropriately contextualize the preserved participant prose. The protocol's eight-question baseline, empty structured records, and payload sizes agree with retained snapshots. No overstatement blocks this scoped pass.

The README's fixed-version availability statement is a publication-stage statement: it becomes true only after the bundle is committed and exposed at the actual fixed public artifact URL. Publication and commit availability have not been verified in this local review. The parent should retain that distinction when publishing. The review link likewise depends on copying this review into the final bundle. Byte comparisons confirmed that repository copies of `process.md`, `result.md`, `toy_checks.py`, `toy-results.json`, and `requests.jsonl` are identical to reviewed originals.

| Repository bundle file | SHA-256 |
| --- | --- |
| `README.md` | `063a19e6ccb421d8c5944458e446a59bd78892d6e5b3baff0673dfba37a933d6` |
| `protocol.md` | `97fef9c8008545cc3f67b24a590993dd6d85f7d655067be80f3f19e5957cd9cb` |
