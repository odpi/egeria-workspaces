"""List the files under a directory as `repo-relative-path<TAB>size`, sorted. Names and sizes ONLY: no file is ever opened or read.

Symlinked files and symlinked directories are neither followed nor listed (the same walk the Phase 0 census used), so the count
equals the census's. For a git tree prefer `git ls-files` / `git archive --format=tar HEAD | tar -t` (never a dirty working tree);
this walker is for trees that are not git (egeria-v6, tr131-sample).

    python listpaths.py ROOT OUT.tsv
"""
import os
import sys


def walk(root):
    root = os.path.abspath(root)
    for dp, dn, fn in os.walk(root, followlinks=False):
        dn[:] = sorted(d for d in dn if not os.path.islink(os.path.join(dp, d)))
        rel = os.path.relpath(dp, root)
        prefix = "" if rel == "." else rel.replace(os.sep, "/") + "/"
        for n in fn:
            p = os.path.join(dp, n)
            try:
                if os.path.islink(p):
                    continue
                size = os.stat(p).st_size
            except OSError:
                continue
            yield prefix + n, size


def main(argv):
    if len(argv) != 3:
        sys.exit(__doc__)
    rows = sorted(walk(argv[1]))
    with open(argv[2], "w", encoding="utf-8", newline="\n") as out:
        for path, size in rows:
            out.write(f"{path}\t{size}\n")
    print(f"{len(rows)} files listed to {argv[2]}")


if __name__ == "__main__":
    main(sys.argv)
