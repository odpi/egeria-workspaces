#!/usr/bin/env python3
"""Generate a loadable Dr.Egeria doc for the Overview dashboard's Governance
Metrics -- one GovernanceMetric + Report + GovernanceResults link + a
per-metric InformationSupplyChain "data flow" per FIXED (non-generic)
function in pyegeria.view.analytic_registry. Single source of truth: the
registry's own description/binding_note/returns text and
analytic_demo_specs.py's fuller description -- no hand-authored prose per
metric, so this stays honest and in sync as functions are added/changed.

Generic functions (count_elements, counts_by_type, growth_series,
metric_trend, sum_type_counts, count_elements_by_property) are deliberately
excluded -- their subject is itself a parameter, so a single GovernanceMetric
per function would be meaningless (see OVERVIEW_NEXT_STEPS.md's rollout
writeup for the full reasoning).

The InformationSupplyChain per metric is a *documented* flow, not true
DataFlow lineage -- FormatSet/the analytic function itself aren't Egeria
elements yet (see BACKLOG.md's "GovernanceMetric lineage" items), so its
Purposes/Scope carry the conceptual data-source -> analytic-function -> Report
-> GovernanceMetric chain as text, while its real Collection membership only
covers the two real elements (the Report and the GovernanceMetric) --
extend this once the missing links become real Egeria types.

Run inside the quickstart-pyegeria-web container (needs pyegeria installed;
/app is bind-mounted 1:1 to this host directory, so the output lands in the
real repo file either way):
  docker exec quickstart-pyegeria-web python3 /app/gen_governance_metrics.py
Then load the output with dr_egeria --validate / --process, same as any
other .dr-egeria.md file.
"""
from pathlib import Path

from pyegeria.view.analytic_registry import get_analytic_registry
from pyegeria.view.analytic_demo_specs import get_analytic_demo_specs

OUT = Path(__file__).resolve().parent / "OVERVIEW_GOVERNANCE_METRICS.dr-egeria.md"


def esc(s):
    return (s or "").strip()


def build_entries():
    reg = get_analytic_registry()
    demos = get_analytic_demo_specs()
    func_to_demo = {}
    for spec_name, fs in demos.items():
        fn = fs.action.analytic_function
        func_to_demo[fn] = (spec_name, fs.description, fs.heading)

    entries = []
    for name, spec in sorted(reg.items()):
        if spec.generic:
            continue
        demo_name, demo_desc, heading = func_to_demo.get(spec.function, (None, None, None))
        if not demo_name:
            continue
        entries.append({
            "name": name, "function": spec.function, "summary": spec.description,
            "returns": spec.returns, "binding_note": spec.binding_note,
            "demo_spec": demo_name, "demo_desc": demo_desc, "heading": heading,
        })
    return entries


def render(entries):
    out = []
    out.append("<!-- SPDX-License-Identifier: CC-BY-4.0 -->")
    out.append("<!-- Copyright Contributors to the ODPi Egeria project. -->")
    out.append("")
    out.append("# Egeria Overview — Governance Metrics")
    out.append("")
    out.append("> Loadable **Dr.Egeria** document that materialises the Overview dashboard's")
    out.append("> fixed (non-generic) `pyegeria.view.overview_metrics` functions as real")
    out.append("> `GovernanceMetric` elements, each linked via `GovernanceResults` to a real")
    out.append("> `Report` (report-spec-backed, runnable via `/api/report-specs/execute`), plus")
    out.append("> a per-metric `InformationSupplyChain` documenting the conceptual data flow")
    out.append("> (data source → analytic function → Report → GovernanceMetric) — a real")
    out.append("> Collection membership for the two real artifacts today, text-only for the")
    out.append("> two stages that aren't Egeria elements yet. Generated from")
    out.append("> `pyegeria.view.analytic_registry` + `analytic_demo_specs` — the single")
    out.append("> source of truth. Regenerate with `gen_governance_metrics.py`. Upsert-safe —")
    out.append("> re-running this file (e.g. after a repository reset) is always correct.")
    out.append("> **Run with VALIDATE first, then PROCESS.**")
    out.append("")
    out.append("---")
    out.append("")

    for e in entries:
        title = e["heading"]
        report_name = f"{title} Metric Report"
        flow_name = f"{title} Data Flow"
        scope = e["binding_note"] or "Catalog-wide -- no additional population scoping applied."
        impl = (f"pyegeria.view.overview_metrics.{e['name']}() -- exposed as Report Spec "
                f"\"{e['demo_spec']}\" via pyegeria's analytic function registry "
                f"(analytic_registry.py). Returns: {e['returns']}.")
        measurement = f"{e['returns']}. {e['binding_note']}".strip()
        flow_purpose = (
            f"Documents (not yet true DataFlow lineage -- see BACKLOG.md) the conceptual "
            f"chain behind the \"{title}\" governance metric: a data source (the Egeria "
            f"relationship/classification/property {e['name']}() actually reads -- see its "
            f"own Implementation Description) feeds the analytic function "
            f"pyegeria.view.overview_metrics.{e['name']}(), exposed as Report Spec "
            f"\"{e['demo_spec']}\", instantiated as the Report \"{report_name}\", measured "
            f"by the GovernanceMetric \"{title}\". Real Collection membership below covers "
            f"the Report and GovernanceMetric (both real elements today); the data-source "
            f"and analytic-function stages are text-only until FormatSet/the analytic "
            f"function itself become real Egeria types."
        )

        out.append(f"""## Create Report
> Defines a report with optional default parameters set, that can be placed on a Dashboard.

### Display Name
{report_name}

### Description
Live computation backing the {title} governance metric.

### Report Spec
{e['demo_spec']}

### Output Format
DICT

___

## Create Governance Metric
> A governance metric describes measurements that support governance requirements.

### Display Name
{title}

### Summary
{esc(e['summary'])}

### Scope
{esc(scope)}

### Usage
{esc(e['demo_desc'])}

### Implementation Description
{esc(impl)}

### Measurement
{esc(measurement)}

### Target
No formal target set yet -- part of the 2026-08-17 GovernanceMetric/Report rollout, piloted on Orphan Glossary Terms.

___

## Link Governance Results
> Attach a governance metric to a data asset that describes where its measurements are kept.

### Governance Metric
{title}

### Data Asset
{report_name}

___

## Create Information Supply Chain
> Creates or updates an information supply chain -- a description of the flow of a particular type of data across a digital landscape.

### Display Name
{flow_name}

### Purposes
{esc(flow_purpose)}

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
{flow_name}

### Element Id
{report_name}

___

## Add Member to Collection
> Add/Remove a member to/from a collection.

### Collection Id
{flow_name}

### Element Id
{title}

___
""")

    return "\n".join(out)


if __name__ == "__main__":
    entries = build_entries()
    md = render(entries)
    with open(OUT, "w") as f:
        f.write(md)
    print(f"{len(entries)} metrics written to {OUT}")
