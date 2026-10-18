#!/usr/bin/env python3
"""Generate the coco_data_hub DDL from the Strategic Digital Product Catalog Dr.Egeria files.

One schema per digital product (the schemaName placeholder of its TabularDataSetCollection),
one table per data structure, one column per data field linked to that structure, in link
Position order, and a primary key on the fields whose link to the structure has the Coverage
Category IDENTIFIER.  Usage (from the repository root):
  compose-configs/egeria-quickstart/bin/gen-coco-data-hub-sql.py \\
    "coco-workbooks/1. coco-data-hub/strategic-digital-products" \\
    compose-configs/egeria-quickstart/docker-entrypoint-initdb.d/data/coco_data_hub.sql
"""
import re
import sys
from pathlib import Path

FILES = ["research.md", "master-data-management.md", "manufacturing.md", "quality-systems.md",
         "procurement.md", "warehouse.md", "delivery.md", "patient-treatment.md", "finance.md",
         "people-systems.md", "privacy-operations.md"]


def attr(block, name):
    m = re.search(r"^### " + re.escape(name) + r"\n(.*?)(?=\n### |\Z)", block, re.S | re.M)
    return m.group(1).strip() if m else None


def snake(name):
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def sql_str(text):
    return "'" + " ".join(text.split()).replace("'", "''") + "'"


def column_type(field):
    dt, name, length = field["type"], field["name"], field["length"]
    if dt == "string":
        return f"varchar({length})" if length else "text"
    if dt == "date":
        return "timestamptz" if name.endswith("Timestamp") else "date"
    return {"int": "integer", "float": "double precision", "bigdecimal": "numeric(18,2)",
            "boolean": "boolean"}[dt]


def parse(path):
    products, fields, structures, links = [], {}, {}, []
    product = None
    for block in path.read_text().split("\n___\n"):
        heads = re.findall(r"^## (.+)$", block, re.M)
        cmd = heads[-1].strip() if heads else ""
        if cmd == "Create Digital Product":
            product = {"name": attr(block, "Display Name"), "qn": attr(block, "Qualified Name"),
                       "description": attr(block, "Description"), "structures": []}
            products.append(product)
        elif cmd == "Create Data Structure":
            qn = attr(block, "Qualified Name")
            structures[qn] = {"name": attr(block, "Display Name"),
                              "description": attr(block, "Description"),
                              "namespace": attr(block, "Namespace Path"), "fields": []}
            product["structures"].append(qn)
        elif cmd == "Create Data Field":
            fields[attr(block, "Qualified Name")] = {
                "name": attr(block, "Display Name"), "description": attr(block, "Description"),
                "type": attr(block, "Data Type"), "length": attr(block, "Length"),
                "nullable": attr(block, "Is Nullable") != "false"}
        elif cmd == "Link Data Field to Data Structure":
            links.append((attr(block, "Data Structure"), int(attr(block, "Position")),
                          attr(block, "Data Field"), attr(block, "Coverage Category") == "IDENTIFIER"))
        elif cmd.startswith("Create Element"):
            ph = dict(re.findall(r"^- (\w+): (.*)$", attr(block, "Placeholder Property Values"), re.M))
            product["schema"], product["database"] = ph["schemaName"], ph["databaseName"]
            product["schema_description"] = ph["schemaDescription"]
    for s, pos, f, identifier in links:
        structures[s]["fields"].append((pos, dict(fields[f], primary_key=identifier)))
    return products, structures


def main(src, out):
    src = Path(src)
    lines = ["-- Coco Pharmaceuticals Data Sharing Hub: one schema per strategic digital product.",
             "-- GENERATED from coco-workbooks/1. coco-data-hub/strategic-digital-products/*.md",
             "-- (Create Data Structure / Create Data Field / Link Data Field to Data Structure).",
             "-- Do not edit by hand: change the product files and regenerate with",
             "-- compose-configs/egeria-quickstart/bin/gen-coco-data-hub-sql.py.",
             "-- Idempotent: every object is created only if it does not exist.", "",
             "SET client_min_messages = warning;", ""]
    n_s = n_t = n_c = n_k = 0
    for fname in FILES:
        products, structures = parse(src / fname)
        lines += [f"-- {'=' * 96}", f"-- {fname}", f"-- {'=' * 96}", ""]
        for p in products:
            assert p["database"] == "coco_data_hub", (p["name"], p["database"])
            schema = p["schema"]
            n_s += 1
            lines += [f"-- {p['name']}  ({p['qn']})",
                      f"CREATE SCHEMA IF NOT EXISTS {schema};",
                      f"GRANT ALL ON SCHEMA {schema} TO egeria_admin, egeria_user, airflow_user;",
                      f"COMMENT ON SCHEMA {schema} IS {sql_str(p['schema_description'])};", ""]
            for sqn in p["structures"]:
                s = structures[sqn]
                assert s["namespace"] == f"coco_data_hub.{schema}", (sqn, s["namespace"])
                table = f"{schema}.{snake(s['name'])}"
                cols = sorted(s["fields"], key=lambda x: x[0])
                assert [c[0] for c in cols] == list(range(1, len(cols) + 1)), sqn
                n_t += 1
                n_c += len(cols)
                width = max(len(snake(f["name"])) for _, f in cols)
                body = [f"  {snake(f['name']).ljust(width)} {column_type(f)}"
                        + ("" if f["nullable"] else " NOT NULL") for _, f in cols]
                key = [snake(f["name"]) for _, f in cols if f["primary_key"]]
                if key:
                    n_k += 1
                    body.append(f"  CONSTRAINT {snake(s['name'])}_pk PRIMARY KEY ({', '.join(key)})")
                lines += [f"CREATE TABLE IF NOT EXISTS {table} (", ",\n".join(body), ");",
                          f"COMMENT ON TABLE {table} IS {sql_str(s['description'])};"]
                lines += [f"COMMENT ON COLUMN {table}.{snake(f['name'])} IS {sql_str(f['description'])};"
                          for _, f in cols]
                lines.append("")
            lines += [f"GRANT ALL ON ALL TABLES IN SCHEMA {schema} TO egeria_admin, egeria_user, airflow_user;", ""]
    Path(out).write_text("\n".join(lines) + "\n")
    print(f"{n_s} schemas, {n_t} tables, {n_c} columns, {n_k} primary keys -> {out}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
