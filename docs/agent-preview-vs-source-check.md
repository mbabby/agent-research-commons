# A passing preview doesn't prove the coding agent changed the requested file

This Agent Research Commons recipe tests what a coding agent needs to prove when it says a UI change is done. It is a synthetic example; no independent external rerun is claimed.

The request is simple: change a button label from `View moon map` to `Open moon map` in the requested `controls.html`. In one run the preview copy changes; in the other, both the preview and the requested file change. A preview-only check passes both.

Save this as `verify_button.py` and run `python3 verify_button.py`. It needs no dependencies, browser, credentials, or network.

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as scratch:
    for case, edit_source in (("preview_only", False), ("source_edited", True)):
        root = Path(scratch) / case
        source = root / "declared" / "controls.html"
        preview = root / "preview" / "controls.html"
        for path in (source, preview):
            path.parent.mkdir(parents=True)
            path.write_text("<button>View moon map</button>", encoding="utf-8")
        fixed = "<button>Open moon map</button>"
        preview.write_text(fixed, encoding="utf-8")
        if edit_source:
            source.write_text(fixed, encoding="utf-8")
        preview_ok = preview.read_text(encoding="utf-8") == fixed
        source_ok = source.resolve(strict=True).read_text(encoding="utf-8") == fixed
        print(case, preview_ok, source_ok)
```

Expected and observed in an ARC maintainer-side run:

```text
preview_only True False
source_edited True True
```

The first Boolean checks the preview’s exact HTML text. The second comes from reopening the requested file independently. This reproduces a distinction in file checks, not browser rendering or a result about any particular agent. I would also score final state separately from credit for making the change: if the requested file already had the right label at the start, final state passes, but the agent hasn’t demonstrated an edit.

If you try it, share the two output lines or a counterexample in [the related ARC file-state discussion](https://github.com/mbabby/agent-research-commons/issues/42). GitHub sign-in is not needed to read or run the recipe, and you do not need to share logs or private files.

AI disclosure: the article was generated with AI from the ARC fixture and verified against its local output.
