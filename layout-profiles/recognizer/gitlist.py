"""List the files of ONE commit of a git repository as `path<TAB>size`, sorted. Names and sizes ONLY: it runs `git ls-tree -r -l`, which
reports each blob's size from the object database and never writes or reads a working tree, so a dirty tree cannot leak in.
Symlinks (mode 120000) and submodules (mode 160000) are skipped, as the directory walker skips symlinks.

    python gitlist.py REPO COMMIT OUT.tsv
"""
import subprocess
import sys


def list_commit(repo, commit):
    out = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "-l", "-z", "--full-tree", commit], check=True, capture_output=True).stdout
    rows = []
    for rec in out.split(b"\0"):
        if not rec:
            continue
        meta, _, path = rec.partition(b"\t")
        mode, kind, _sha, size = meta.split()
        if kind != b"blob" or mode not in (b"100644", b"100755"):
            continue
        rows.append((path.decode("utf-8", "surrogateescape"), int(size)))
    return sorted(rows)


def main(argv):
    if len(argv) != 4:
        sys.exit(__doc__)
    rows = list_commit(argv[1], argv[2])
    with open(argv[3], "w", encoding="utf-8", newline="\n", errors="surrogateescape") as fh:
        for p, s in rows:
            fh.write(f"{p}\t{s}\n")
    print(f"{len(rows)} files at {argv[2]} listed to {argv[3]}")


if __name__ == "__main__":
    main(sys.argv)
