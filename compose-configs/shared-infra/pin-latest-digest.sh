#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
#
# Re-resolve <image:tag>'s current registry digest and rewrite the given
# Dockerfile's FROM line to pin it -- e.g. `FROM quay.io/odpi/egeria-platform
# :latest@sha256:<old>` becomes `...@sha256:<new>`.
#
# Why this exists: every Dockerfile's FROM line in this repo is pinned to a
# digest (OpenSSF Scorecard's Pinned-Dependencies check), which is good for
# reproducibility but means a floating tag like `:latest` (egeria-platform,
# scipy-notebook) would otherwise never actually move -- `docker build --pull`
# just re-confirms the SAME pinned digest forever. This script is the
# explicit, on-demand escape hatch: quick-start-local / fresh-start-local's
# --refresh-platform flag calls it (only for the egeria-platform Dockerfile,
# the one thing --refresh-platform has ever targeted) right before the
# rebuild, so "give me whatever's newest right now" still works. Every other
# pinned Dockerfile in the repo relies on Dependabot's docker ecosystem
# (.github/dependabot.yml) to open a PR when a new digest is published for
# its same version tag instead -- this script is deliberately not run
# automatically anywhere.
#
# Usage: pin-latest-digest.sh <dockerfile> <image:tag>
# Leaves the Dockerfile untouched (with a warning, not a hard failure) if the
# registry can't be reached -- a refresh attempt failing offline shouldn't
# block starting up with whatever's already pinned.
set -euo pipefail

dockerfile="${1:?usage: pin-latest-digest.sh <dockerfile> <image:tag>}"
image_tag="${2:?usage: pin-latest-digest.sh <dockerfile> <image:tag>}"

if [[ ! -f "$dockerfile" ]]; then
  echo "[pin-latest-digest] ERROR: no such file: ${dockerfile}" >&2
  exit 1
fi

manifest_json="$(docker buildx imagetools inspect "$image_tag" --format '{{json .Manifest}}' 2>/dev/null || true)"
digest="$(printf '%s' "$manifest_json" | python3 -c "import json,sys; print(json.load(sys.stdin)['digest'])" 2>/dev/null || true)"

if [[ -z "$digest" ]]; then
  echo "[pin-latest-digest] WARNING: could not resolve current digest for ${image_tag} (offline, or registry unreachable) -- leaving ${dockerfile}'s existing pin as-is." >&2
  exit 0
fi

image_no_tag="${image_tag%%:*}"

DOCKERFILE="$dockerfile" IMAGE_NO_TAG="$image_no_tag" IMAGE_TAG="$image_tag" DIGEST="$digest" python3 <<'PYEOF'
import os, re

path = os.environ["DOCKERFILE"]
image_no_tag = os.environ["IMAGE_NO_TAG"]
image_tag = os.environ["IMAGE_TAG"]
digest = os.environ["DIGEST"]
new_from_prefix = f"FROM {image_tag}@{digest}"

with open(path) as f:
    lines = f.readlines()

out = []
changed = False
for line in lines:
    m = re.match(r'^(FROM\s+)(\S+)((?:\s+[Aa][Ss]\s+\S+)?\s*\n?)$', line)
    if m and m.group(2).split('@')[0].split(':')[0] == image_no_tag:
        out.append(new_from_prefix + m.group(3))
        changed = True
    else:
        out.append(line)

with open(path, 'w') as f:
    f.writelines(out)

print(("updated" if changed else "no matching FROM line found in"), path)
PYEOF

echo "[pin-latest-digest] ${dockerfile}: pinned ${image_tag} -> ${digest}"
