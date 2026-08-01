#!/usr/bin/env python3
"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Phase 3 of the Portal test strategy: an orchestrator/analyzer that runs both
test tiers, and — only when something actually fails — triages the failures
instead of dumping a raw pass/fail log. Three things a flat test-runner
report can't do, which this exists to do instead:

  1. Tell a real regression apart from legitimate data drift (a golden-anchor
     test can fail because code broke, or because a content-pack update
     changed the seed data — same red X, different meaning).
  2. Cluster failures that share one root cause, instead of reporting N
     failing tests as if they were N unrelated bugs.
  3. Draft a root-cause hypothesis a human can confirm or reject, rather than
     making them re-read every traceback from scratch.

Cost model (deliberately cheap on the common case): on an all-green run,
this makes ZERO LLM calls — clustering/triage only runs proportional to
actual failures. On failures, it tries a LOCAL model first (Ollama,
OpenAI-compatible API on localhost:11434) and only escalates to Claude Code
headless (`claude -p`) if the local model's response doesn't parse as a
confident, structured answer — a cheap-first, expensive-fallback cascade
(the same shape as "FrugalGPT"-style model routing), not "call Claude on
every failure."

Guardrail: this NEVER modifies test assertions, source files, or auto-marks
anything as fixed/expected. It only writes a report. A human reads the
report and decides.

Usage (from this directory, i.e. tests/):
    python3 analyze.py

Requires: quickstart-pyegeria-web container running; Ollama running locally
with OLLAMA_MODEL pulled (default qwen2.5-coder:latest — override via the
env var); `claude` CLI on PATH for escalation (optional — if absent,
low-confidence clusters are just flagged as such in the report instead of
escalated).
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent
CONTAINER_NAME = os.environ.get("PORTAL_CONTAINER", "quickstart-pyegeria-web")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5-coder:latest")
REPORT_PATH = THIS_DIR / "TRIAGE_REPORT.md"

# Strips GUIDs, timestamps, and other per-run noise from a failure message so
# two failures with the same root cause but different dynamic values cluster
# together instead of each getting their own group.
_GUID_RE = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.I)
_TS_RE = re.compile(r"\d{4}-\d{2}-\d{2}T[\d:.+-]+")


@dataclass
class Failure:
    testsuite: str
    testcase: str
    message: str
    detail: str


@dataclass
class Cluster:
    signature: str
    failures: list = field(default_factory=list)


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    print(f"$ {' '.join(cmd)}")
    return subprocess.run(cmd, capture_output=True, text=True, **kwargs)


def run_container_suite() -> Path:
    xml_path_in_container = "tests/_results_container.xml"
    xml_path_on_host = THIS_DIR / "_results_container.xml"
    run([
        "docker", "exec", CONTAINER_NAME,
        "pytest", "tests/", "--ignore=tests/browser",
        f"--junit-xml={xml_path_in_container}", "-q",
    ])
    return xml_path_on_host


def run_browser_suite() -> Path:
    browser_dir = THIS_DIR / "browser"
    xml_path = browser_dir / "_results_browser.xml"
    venv_python = browser_dir / ".venv" / "bin" / "python3"
    if not venv_python.exists():
        print("browser/.venv not found — skipping browser tier (see browser/README.md)")
        return xml_path  # won't exist; parse_junit handles missing files
    run([
        str(venv_python), "-m", "pytest", ".",
        f"--junit-xml={xml_path.name}", "-q",
    ], cwd=browser_dir)
    return xml_path


def parse_junit(xml_path: Path) -> list[Failure]:
    if not xml_path.exists():
        return []
    root = ET.parse(xml_path).getroot()
    suites = [root] if root.tag == "testsuite" else root.findall("testsuite")
    out = []
    for suite in suites:
        for case in suite.findall("testcase"):
            for tag in ("failure", "error"):
                node = case.find(tag)
                if node is not None:
                    out.append(Failure(
                        testsuite=suite.get("name", xml_path.stem),
                        testcase=case.get("name", "?"),
                        message=(node.get("message") or "").strip(),
                        detail=(node.text or "").strip(),
                    ))
    return out


def normalize(text: str) -> str:
    text = _GUID_RE.sub("<GUID>", text)
    text = _TS_RE.sub("<TS>", text)
    return text


def cluster_failures(failures: list[Failure]) -> list[Cluster]:
    clusters: dict[str, Cluster] = {}
    for f in failures:
        # Signature: exception class / first line of the failure message,
        # normalized. Good enough for a v1 — same exception type + same
        # first line is a strong signal of shared root cause; refine if it
        # turns out too coarse or too fine in practice.
        first_line = normalize(f.message).splitlines()[0] if f.message else "(no message)"
        sig = first_line[:160]
        clusters.setdefault(sig, Cluster(signature=sig)).failures.append(f)
    return sorted(clusters.values(), key=lambda c: -len(c.failures))


def call_ollama(prompt: str) -> str | None:
    payload = json.dumps({
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }).encode()
    req = urllib.request.Request(OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = json.loads(resp.read())
            return body.get("response")
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"  (local LLM call failed: {exc})")
        return None


def call_claude(prompt: str) -> str | None:
    try:
        result = subprocess.run(
            ["claude", "-p", prompt, "--output-format", "text"],
            capture_output=True, text=True, timeout=180,
        )
        if result.returncode != 0:
            print(f"  (claude CLI exited {result.returncode}: {result.stderr[:300]})")
            return None
        return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        print(f"  (claude CLI unavailable: {exc})")
        return None


_TRIAGE_PROMPT_TEMPLATE = """You are triaging a failing test cluster in the egeria-workspaces Portal apps repo (PyegeriaWebHandler).

Cluster signature (normalized first line of the failure message): {signature}
Affected tests ({count}): {testcases}

Representative failure detail:
```
{detail}
```

The traceback usually names the file and line where the failing call
originates (look for a line like "tests/some_file.py:NN: in test_name" near
the TOP of the traceback, closest to the test function itself, not deep
inside library/stdlib frames) — use that for SUGGESTED_FIX_LOCATION whenever
it's present; only say "unknown" if the traceback genuinely doesn't show one.

Respond in EXACTLY this format, nothing else:
CONFIDENCE: <HIGH|MEDIUM|LOW>
ROOT_CAUSE: <one or two sentences>
SUGGESTED_FIX_LOCATION: <file path and/or function name if you can tell, else "unknown">
"""


def triage_cluster(cluster: Cluster) -> dict:
    representative = cluster.failures[0]
    prompt = _TRIAGE_PROMPT_TEMPLATE.format(
        signature=cluster.signature,
        count=len(cluster.failures),
        testcases=", ".join(f"{f.testsuite}::{f.testcase}" for f in cluster.failures[:5]),
        detail=representative.detail[-3000:],
    )

    source = "local"
    response = call_ollama(prompt)
    parsed = _parse_triage_response(response) if response else None

    # Escalate on low/missing confidence AND on a hollow "HIGH confidence but
    # no actual fix location" answer — the local model can claim confidence
    # without doing the work of reading the traceback for a file:line, which
    # is a real failure mode this needs to catch (observed with
    # qwen2.5-coder:latest on the very first real run of this script:
    # 2026-07-31, correct HIGH-confidence root cause but
    # SUGGESTED_FIX_LOCATION came back "unknown" despite the traceback
    # plainly showing tests/test_mcp_server_basic.py:44).
    _no_location = not parsed or (parsed.get("fix_location") or "").strip().lower() in ("", "unknown", "none", "n/a")
    if not parsed or parsed["confidence"] != "HIGH" or _no_location:
        escalation_prompt = prompt
        if response:
            escalation_prompt += f"\n\nA local model attempted this and produced:\n{response}\n\nGive your own independent assessment — confirm, correct, or replace it."
        claude_response = call_claude(escalation_prompt)
        if claude_response:
            claude_parsed = _parse_triage_response(claude_response)
            if claude_parsed:
                source = "claude (escalated)"
                parsed = claude_parsed
            else:
                source = "claude (escalated, unstructured)"
                parsed = {"confidence": "UNKNOWN", "root_cause": claude_response, "fix_location": "unknown"}

    if not parsed:
        parsed = {"confidence": "UNKNOWN", "root_cause": "(no triage available — local model and/or claude CLI unreachable)", "fix_location": "unknown"}
        source = "none"

    return {"source": source, **parsed}


def _parse_triage_response(response: str | None) -> dict | None:
    if not response:
        return None
    conf = re.search(r"CONFIDENCE:\s*(HIGH|MEDIUM|LOW)", response, re.I)
    cause = re.search(r"ROOT_CAUSE:\s*(.+?)(?:\nSUGGESTED_FIX_LOCATION:|$)", response, re.I | re.S)
    loc = re.search(r"SUGGESTED_FIX_LOCATION:\s*(.+)", response, re.I)
    if not (conf and cause):
        return None
    return {
        "confidence": conf.group(1).upper(),
        "root_cause": cause.group(1).strip(),
        "fix_location": loc.group(1).strip() if loc else "unknown",
    }


def write_report(container_failures: list[Failure], browser_failures: list[Failure], clusters: list[Cluster], triages: list[dict]) -> None:
    lines = ["# Test Triage Report", ""]
    total = len(container_failures) + len(browser_failures)
    if total == 0:
        lines += ["**All green.** Container suite and browser suite both passed with no failures.", ""]
    else:
        lines += [
            f"**{total} failing test(s)** across {len(clusters)} cluster(s) "
            f"({len(container_failures)} container-tier, {len(browser_failures)} browser-tier).",
            "",
        ]
        for cluster, triage in zip(clusters, triages):
            lines += [
                f"## Cluster: `{cluster.signature}`",
                "",
                f"- **Affected tests ({len(cluster.failures)}):** " + ", ".join(f"`{f.testsuite}::{f.testcase}`" for f in cluster.failures),
                f"- **Triage source:** {triage['source']}",
                f"- **Confidence:** {triage['confidence']}",
                f"- **Root cause:** {triage['root_cause']}",
                f"- **Suggested fix location:** {triage['fix_location']}",
                "",
                "<details><summary>Representative failure detail</summary>",
                "",
                "```",
                cluster.failures[0].detail[-2000:],
                "```",
                "</details>",
                "",
            ]
    REPORT_PATH.write_text("\n".join(lines))
    print(f"\nReport written to {REPORT_PATH}")


def main() -> int:
    container_xml = run_container_suite()
    browser_xml = run_browser_suite()

    container_failures = parse_junit(container_xml)
    browser_failures = parse_junit(browser_xml)
    all_failures = container_failures + browser_failures

    if not all_failures:
        print("\nAll green — no triage needed.")
        write_report([], [], [], [])
        return 0

    print(f"\n{len(all_failures)} failure(s) found — clustering and triaging...")
    clusters = cluster_failures(all_failures)
    triages = []
    for cluster in clusters:
        print(f"  triaging cluster: {cluster.signature[:80]!r} ({len(cluster.failures)} test(s))")
        triages.append(triage_cluster(cluster))

    write_report(container_failures, browser_failures, clusters, triages)
    return 1


if __name__ == "__main__":
    sys.exit(main())
