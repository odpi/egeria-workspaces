#!/usr/bin/env bash
# List every SSH key that has signed a commit in this repo, and say whether
# each one is trusted by gpg.ssh.allowedSignersFile.
#
# Signing keys are per-machine, so this is how you find out which machines have
# committed here and whether the local allowed_signers roster is complete.
#
# Usage: .claude/skills/setup-git-signing/list-signing-keys.sh [git-log-args...]
set -euo pipefail
exec python3 - "$@" <<'PY'
import base64, collections, os, struct, subprocess, sys

def rd(b, o):
    (n,) = struct.unpack(">I", b[o:o+4])
    return b[o+4:o+4+n], o+4+n

allowed = subprocess.run(["git", "config", "--get", "gpg.ssh.allowedSignersFile"],
                         capture_output=True, text=True).stdout.strip()
allowed = os.path.expanduser(allowed) if allowed else ""
trusted = set()
if allowed and os.path.exists(allowed):
    for line in open(allowed):
        line = line.strip()
        if line and not line.startswith("#"):
            trusted.update(t for t in line.split() if t.startswith("AAAA"))
else:
    print("WARNING: gpg.ssh.allowedSignersFile is unset or missing; "
          "every key will show as UNTRUSTED.\n", file=sys.stderr)

log = subprocess.run(["git", "log", "--format=%H %cI"] + sys.argv[1:],
                     capture_output=True, text=True).stdout

keys = collections.defaultdict(lambda: {"dates": [], "emails": collections.Counter()})
for line in log.split("\n"):
    if not line.strip():
        continue
    sha, date = line.split()
    raw = subprocess.run(["git", "cat-file", "commit", sha],
                         capture_output=True, text=True).stdout
    sig, in_sig, email = [], False, ""
    for ln in raw.split("\n"):
        if ln.startswith("author ") and "<" in ln:
            email = ln.split("<")[1].split(">")[0]
        if ln.startswith("gpgsig "):
            in_sig = True
            continue
        if in_sig:
            if ln.startswith(" "):
                sig.append(ln[1:])
            else:
                in_sig = False
    body = "".join(l for l in sig if not l.startswith("-----")).strip()
    if not body:
        continue
    try:
        blob = base64.b64decode(body)
        if blob[:6] != b"SSHSIG":   # PGP-signed (e.g. GitHub web merge commits)
            continue
        pk, _ = rd(blob, 10)        # 6-byte magic + 4-byte version
        ktype, _ = rd(pk, 0)
        key = base64.b64encode(pk).decode()
    except Exception:
        continue
    entry = keys[(ktype.decode(), key)]
    entry["dates"].append(date)
    entry["emails"][email] += 1

if not keys:
    print("No SSH-signed commits found in the selected range.")
    sys.exit(0)

for (ktype, key), v in sorted(keys.items(), key=lambda x: -len(x[1]["dates"])):
    mark = "trusted  " if key in trusted else "UNTRUSTED"
    n, lo, hi = len(v["dates"]), min(v["dates"])[:10], max(v["dates"])[:10]
    authors = ", ".join("%s (%d)" % (e, c) for e, c in v["emails"].most_common())
    print("[%s] %5d commits  %s .. %s" % (mark, n, lo, hi))
    print("             %s %s" % (ktype, key))
    print("             authors: %s" % authors)
PY
