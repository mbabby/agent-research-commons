# English and Multilingual Publication Implementation Plan

**Goal:** Publish an English site that welcomes Chinese content and preserves source records.
**Architecture:** Separate English sidecars from canonical records. Render English by default only when a sidecar matches its source; expose originals and label translations. Keep the existing publisher and record validators.
**Tech Stack:** Python 3.9+ standard library, static HTML/CSS/JS, GitHub Pages.

## Global constraints
- Preserve adopted philosophy and inactive governance status.
- Keep review/acceptance IDs, URLs and dates unchanged.
- No mandatory translation, new permissions or runtime services.

## Tasks
- [x] Add regression tests for English shell, Chinese content, translated/source views and stale sidecar fallback; observe failures before implementation.
- [x] Translate UI in arc/site.py, arc/governance.py and arc/philosophy.py; add translation loader and source-language presentation.
- [x] Independently prepare docs, report and task translations under translations/en, tied to original text, and review them before integration.
- [x] Publish originals, translation provenance and English machine entry/guide. Document English/Chinese contribution policy.
- [x] Run python3 -m unittest discover -s tests -v; build from a live snapshot; validate local links and desktop/mobile browser views.
- [ ] Review diff, create and attach PR, merge authorized change, verify Pages deployment and live English/source pages.

Translation sidecar JSON contract: {"source": <canonical content projection>, "translation": <same projection with English prose>}. Task projection contains title, question, scope, exclusions, deliverable and acceptance. Report/document projection is the entire original JSON object; only prose may change. The loader returns a merged copy and leaves all original records untouched; mismatched source falls back to original.
