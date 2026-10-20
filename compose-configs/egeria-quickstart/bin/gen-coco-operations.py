#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Egeria project.
"""
Generate the activity plan that the coco_operations_* Airflow DAGs follow when they simulate Coco
Pharmaceuticals' day-to-day operations in the system databases.

    gen-coco-operations.py <coco_systems data dir> <output dir>

e.g. from the repository root:

    compose-configs/egeria-quickstart/bin/gen-coco-operations.py \
      compose-configs/egeria-quickstart/docker-entrypoint-initdb.d/data/coco_systems \
      exchange-quickstart/coco-dags/coco-operations

It reads every system's SQL (data/coco_systems/<database>/<system schema>.sql) and writes one
<database>.json per estate.  Each table of each system is given an activity:

  entity    a new business record is created by copying an existing one under a new key (an expense
            report, a batch, a purchase order).  Its child tables are copied with it.
  event     a new row is recorded against an existing record (a status change, a reading, a stock
            movement): the key columns that name the record are kept and the time is now.
  child     the details of an entity (expense entries, order lines); copied with their parent.  A child with a
            cadence also gets new rows of its own against existing parents (stock movements against a lot).
  snapshot  the current state of something (stock on hand, a holding); an existing row is refreshed.
  master    reference and master data (items, people, sites); left alone.
  inbound   tables filled by the digital product subscriptions; never written by the simulation.

and a cadence that sets how often new activity arrives:

  fast      every couple of minutes - readings, scans, telemetry, stock movements
  steady    every quarter of an hour - orders, batches, samples, shipments, cases
  slow      hourly - money and people: expenses, invoices, payments, payroll, approvals
  daily     once a day - qualifications, calibrations, audits, reviews, plans

The plan is a starting point: edit the JSON to change a table's activity or cadence.  Regenerating it
overwrites those edits, so record lasting changes in OVERRIDES below.
"""
import json
import os
import re
import sys

DATE_TYPES = ("date", "timestamp", "timestamptz", "timestamp with time zone", "timestamp without time zone")

CADENCE_WORDS = [
    ("fast", r"reading|telemetry|sensor|temperature|temp_|_temp|iot|probe|logger|measure|scan|serial_event|"
             r"aggregation_event|trace|alarm|alert|signal|inv_transaction|transaction|movement|_txn|txn_|"
             r"stock_move|goods_move|event|_log$|^log_|audit_trail|access_log|signin|login"),
    ("daily", r"qualif|calibrat|certif|audit|review|retention|contract|assessment|plan$|planning|forecast|"
              r"training|course|curriculum|licen|registration|submission|policy|risk|capa"),
    ("slow", r"expense|approval|invoice|payment|journal|ledger|_gl|gl_|payroll|earning|pay_|salary|"
             r"timesheet|time_entry|absence|leave|hire|worker|employee|requisition|purchase|po_|_po$|"
             r"voucher|accrual|budget|cost|consent|request|dsar|rights"),
    ("steady", r"order|batch|lot|shipment|consign|deliver|despatch|dispatch|receipt|rcv|receiv|inspection|"
               r"sample|result|deviation|step|production|work_order|pick|ticket|case|complaint|incident|"
               r"excursion|nonconform|change|release|disposition|record|test"),
]

# Master data: people, parties, products, materials, places and the IT estate.  New rows copied from these
# would be duplicate people or products under new keys, so they are left alone.
MASTER_WORDS = (r"user|person|worker|medewerker|employee|staff|vendor|supplier|party|account|customer|"
                r"product|prd_|item|material|chemical|subst|site|location|group|recipient|signer|"
                r"data_source|asset$|resource|topic|competency|master|mstr|registration")

# Lasting hand edits to the generated plan: "<database>/<schema>.<table>": {"activity": ..., "cadence": ...}
OVERRIDES = {}


def parse_system(path):
    """Return the tables of one system SQL file, in file order."""
    text = open(path, encoding="utf-8").read()
    inbound = set()
    # Two marker styles: the Coco core files close the block, the acquisitions' files run it to the GRANTs
    for block in re.findall(r"-- Tables added for the digital product subscriptions.*?-- End of subscription tables\.|"
                            r"-- Subscription inbound:.*?(?=^GRANT |\Z)", text, re.S | re.M):
        inbound |= set(re.findall(r"CREATE TABLE IF NOT EXISTS ([a-z0-9_]+\.[a-z0-9_]+)", block))
    seeded = set(re.findall(r"INSERT INTO ([a-z0-9_]+\.[a-z0-9_]+)", text))
    comments = dict(re.findall(r"COMMENT ON TABLE ([a-z0-9_]+\.[a-z0-9_]+) IS '((?:[^']|'')*)'", text))
    tables = []
    for name, body in re.findall(r"CREATE TABLE IF NOT EXISTS ([a-z0-9_]+\.[a-z0-9_]+) \((.*?)\n\);", text, re.S):
        cols, pk = [], []
        for line in body.splitlines():
            line = line.strip().rstrip(",")
            c = re.match(r"CONSTRAINT \S+ PRIMARY KEY \(([^)]*)\)", line)
            if c:
                pk = [x.strip() for x in c.group(1).split(",")]
                continue
            c = re.match(r"([a-z_][a-z0-9_]*) (.+)$", line)
            if c and not line.upper().startswith(("CONSTRAINT", "PRIMARY", "UNIQUE")):
                coltype = c.group(2).lower()
                inline_pk = "primary key" in coltype
                coltype = re.split(r" not null| default| primary key| references| unique| generated| check", coltype)[0].strip()
                cols.append((c.group(1), coltype))
                if inline_pk:
                    pk = [c.group(1)]
        tables.append({"table": name, "columns": cols, "pk": pk, "seeded": name in seeded,
                       "inbound": name in inbound, "comment": comments.get(name, "").replace("''", "'")})
    return tables


def is_date(coltype):
    return coltype.startswith(DATE_TYPES)


def cadence_for(table, comment):
    short = table.split(".", 1)[1]
    for cadence, words in CADENCE_WORDS:
        if re.search(words, short):
            return cadence
    for cadence, words in CADENCE_WORDS:
        if re.search(words, comment.lower()):
            return cadence
    return "steady"


def classify(tables):
    by_name = {t["table"]: t for t in tables}
    single_pk = {t["pk"][0]: t["table"] for t in tables if len(t["pk"]) == 1}
    plan = {}
    for t in tables:
        name, pk = t["table"], t["pk"]
        coltypes = dict(t["columns"])
        dates = [c for c, ty in t["columns"] if is_date(ty)]
        entry = {"activity": None, "cadence": None}
        parent = None
        if len(pk) > 1:
            # A child shares a leading key column with an entity table in the same system
            for col in pk[:-1]:
                p = single_pk.get(col)
                if p and p != name:
                    parent = p
                    break
        if t["inbound"]:
            entry["activity"] = "inbound"
        elif not t["seeded"] or not pk:
            entry["activity"] = "master"          # nothing to copy from, or no key to make new rows unique
        elif parent:
            entry["activity"] = "child"
            entry["parent"] = parent
        elif any(is_date(coltypes[c]) for c in pk):
            entry["activity"] = "event"           # (record, time) keyed history
        elif not dates or (len(pk) == 1 and re.search(MASTER_WORDS, name.split(".", 1)[1])
                           and not re.search(r"event|change|request|screening|verif|txn|transaction", name)):
            entry["activity"] = "master"
        elif len(pk) == 1:
            entry["activity"] = "entity"
        else:
            entry["activity"] = "snapshot"
        if entry["activity"] in ("entity", "event", "snapshot"):
            entry["cadence"] = cadence_for(name, t["comment"])
        else:
            entry.pop("cadence")
        plan[name] = entry
    # children are copied with their parent, so only keep those whose parent creates new rows
    for name, entry in plan.items():
        if entry["activity"] == "child" and plan[entry["parent"]]["activity"] != "entity":
            entry["activity"] = "master"
            entry.pop("parent")
    # A table that names an entity's key in an ordinary column (sap_concur.entry.report_key) holds that entity's
    # details too, and is copied with it - a new expense report without entries is not a whole report.
    entity_keys = {by_name[n]["pk"][0]: n for n, e in plan.items() if e["activity"] == "entity"}
    for t in tables:
        name, entry = t["table"], plan[t["table"]]
        if entry["activity"] not in ("entity", "event", "snapshot") or not t["seeded"]:
            continue
        for col, _ in t["columns"]:
            parent = entity_keys.get(col)
            if parent and parent != name and col not in t["pk"]:
                plan[name] = {"activity": "child", "parent": parent}
                if entry.get("cadence") == "fast":
                    plan[name]["cadence"] = "fast"   # also recorded against existing parents: a stock movement
                break
    for name, entry in plan.items():
        if entry["activity"] in ("entity", "child"):
            children = [c for c, e in plan.items() if e.get("parent") == name and c != name]
            if children or entry["activity"] == "entity":
                entry["children"] = children
    return plan


def main(src, out):
    os.makedirs(out, exist_ok=True)
    for db in sorted(os.listdir(src)):
        dbdir = os.path.join(src, db)
        if not os.path.isdir(dbdir):
            continue
        estate = {"database": db, "systems": {}}
        for f in sorted(os.listdir(dbdir)):
            if not f.endswith(".sql"):
                continue
            plan = classify(parse_system(os.path.join(dbdir, f)))
            for name, entry in plan.items():
                entry.update(OVERRIDES.get(f"{db}/{name}", {}))
            estate["systems"][f[:-4]] = plan
        with open(os.path.join(out, db + ".json"), "w") as fh:
            json.dump(estate, fh, indent=2)
            fh.write("\n")
        counts = {}
        for plan in estate["systems"].values():
            for e in plan.values():
                key = e["activity"] + ("/" + e["cadence"] if e.get("cadence") else "")
                counts[key] = counts.get(key, 0) + 1
        print(db, len(estate["systems"]), "systems", dict(sorted(counts.items())))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
