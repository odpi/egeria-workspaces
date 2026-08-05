# pyegeria / Egeria Issue Tracker — moved

**This file has been consolidated into `egeria-python`'s
`PYEGERIA_ISSUES.md` (2026-08-05).** This repo (`egeria-workspaces-fs`) had
grown its own independent copy of the tracker (started 2026-06, `PY-#`
numbering up to `PY-23`) in parallel with `egeria-python`'s — the two
repos were accumulating overlapping and unique pyegeria/Egeria issues
separately instead of sharing one tracker. That's fixed now: **all pyegeria
and Egeria-server issues found while working in either repo are tracked in
one place going forward.**

**Canonical location:** `egeria-python/PYEGERIA_ISSUES.md`
(https://github.com/dwolfson/egeria-python/blob/main/PYEGERIA_ISSUES.md),
local checkout typically at `../egeria-python/PYEGERIA_ISSUES.md` or
`~/localGit/egeria-python/PYEGERIA_ISSUES.md` depending on machine layout.

**Where this file's old `PY-#` entries went:** `PY-1` through `PY-14` were
already duplicated there (as `ISSUE-# (PY-#)` aliases) and were dropped
here, not re-added. `PY-15` through `PY-22` were unique to this file and
are now `ISSUE-35` through `ISSUE-42` in the canonical file (same
`ISSUE-# (PY-#)` alias convention, so searching that file for `(PY-18)` —
or whichever number you remember — still finds the entry). `PY-23` was
merged into the canonical file's existing `ISSUE-34` (same investigation,
found independently in both repos on the same day).

**If you're adding a new pyegeria/Egeria issue found while working in this
repo:** add it to `egeria-python/PYEGERIA_ISSUES.md` directly, not here —
this file is not meant to grow a new set of entries. Code comments in this
repo that cite an `ISSUE-#`/`PY-#` (e.g. `insights_handler.py`,
`requirements.txt`) refer to that canonical file.
