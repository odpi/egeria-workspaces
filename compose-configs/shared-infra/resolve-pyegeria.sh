#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the ODPi Egeria project.
#
# Sourced by quick-start-local / fresh-start-local. Decides which pyegeria
# release the pyegeria-web and jupyter images should carry on this run, and
# produces the --build-arg flags that make the build actually install it.
#
# Why this exists: pyegeria is installed in its own cached Docker layer
# (Dockerfile-fast-api / Dockerfile-jupyter), and ensure_service_image skips
# the build entirely when an image already exists -- so without an explicit
# refresh every install/upgrade (e.g. --refresh-platform) recreated the
# containers from the old image and silently reverted pyegeria, discarding any
# in-container `pip install --upgrade` (hit 2026-09-29: both installs dropped
# back to 6.1.18/6.1.20, which can't read the new link attributes).
#
# Policy: default to the latest release on PyPI unless a version has been
# explicitly pinned. The resolved version is used as PYEGERIA_BUST, so when
# the latest hasn't changed the layer is a cache hit and the "refresh" costs
# nothing; when it has, only that layer (and the ones after it) rebuild.
#
# Pins persist in <env dir>/.env.pyegeria (gitignored) so a pinned install
# stays pinned across plain re-runs; `--pyegeria-version latest` clears it.
#
# Usage:
#   resolve_pyegeria_build_args <pin_file> <requested_version> <mode> <log_prefix>
#     requested_version  "" (use saved pin, else latest) | "latest" | X.Y.Z
#     mode               default | force (also bust when version unchanged) | skip
# Sets:
#   PYEGERIA_BUILD_ARGS  array of --build-arg flags; EMPTY means "don't
#                        rebuild" (skip mode, or PyPI unreachable with no pin)

resolve_pyegeria_build_args() {
  local pin_file="$1" requested="$2" mode="$3" log="$4"
  local pin="" version="" bust=""
  PYEGERIA_BUILD_ARGS=()

  if [[ "$requested" == "latest" ]]; then
    rm -f "$pin_file"
    echo "${log} pyegeria pin cleared; tracking the latest release."
  elif [[ -n "$requested" ]]; then
    if [[ ! "$requested" =~ ^[0-9][0-9A-Za-z.+-]*$ ]]; then
      echo "${log} ERROR: --pyegeria-version expects a version like 6.1.22 or 'latest', got '${requested}'." >&2
      return 1
    fi
    printf 'PYEGERIA_PIN=%s\n' "$requested" > "$pin_file"
    echo "${log} pyegeria pinned to ${requested} (saved to ${pin_file})."
  fi

  if [[ "$mode" == "skip" ]]; then
    echo "${log} --no-refresh-pyegeria: keeping the pyegeria already in the existing images."
    return 0
  fi

  if [[ -f "$pin_file" ]]; then
    pin="$(grep -E '^PYEGERIA_PIN=' "$pin_file" | head -n1 | cut -d= -f2- || true)"
  fi

  if [[ -n "$pin" ]]; then
    version="$pin"
    echo "${log} pyegeria: using pinned version ${version} (clear with --pyegeria-version latest)."
  else
    version="$(curl -fsS --max-time 15 https://pypi.org/pypi/pyegeria/json 2>/dev/null \
      | python3 -c 'import json,sys; print(json.load(sys.stdin)["info"]["version"])' 2>/dev/null || true)"
    if [[ -z "$version" ]]; then
      echo "${log} WARNING: couldn't reach PyPI to find the latest pyegeria; keeping the version in the existing images."
      return 0
    fi
    echo "${log} pyegeria: latest release on PyPI is ${version}."
  fi

  bust="$version"
  if [[ "$mode" == "force" ]]; then
    bust="${version}-$(date +%s)"
  fi
  PYEGERIA_BUILD_ARGS=(
    --build-arg "PYEGERIA_VERSION=pyegeria==${version}"
    --build-arg "PYEGERIA_BUST=${bust}"
  )
}
