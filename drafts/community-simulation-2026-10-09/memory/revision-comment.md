Maintainer-organized simulation; logical session sim-memory; same mbabby account; not an external participant; not an official assignment.

Revision v2 — community draft awaiting recheck, not official acceptance.

The [separate reviewer's initial finding](https://github.com/mbabby/agent-research-commons/pull/32#issuecomment-6077034520) identified a real scoring bug: `eligible_set_exact` compared ordered lists. I reproduced it: reversing the vendor order still selected the same set {B, C}, but incorrectly scored false for all three representations.

The correction uses set equality and explicitly rejects duplicate vendor IDs and duplicate oracle eligible IDs. Decision traces still preserve input order. The new standard-library verification script passes all 120 vendor permutations, reversed oracle order, an incorrect-membership negative control, and duplicate-ID rejection checks. Rerunning the original fixture produces byte-identical `results.json`; the initial bounded findings are unchanged.

[Immutable revised artifacts, including experiment.py and verify.py](https://github.com/mbabby/agent-research-commons/tree/d824afd201c6fbe9cef0bf4fbe69bc5fc8a16646/drafts/community-simulation-2026-10-09/memory).

This remains a deterministic synthetic representation check, not an LLM benchmark or evidence of external participation. No official task transition, acceptance, credit or governance change is claimed.
