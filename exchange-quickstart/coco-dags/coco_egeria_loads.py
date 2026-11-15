# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Egeria project.
"""
Coco Pharmaceuticals subscription loads for Egeria.

Egeria subscribes to three of the strategic digital products, once a day, so that its catalogue of people and
organization is filled from Coco's own systems rather than by hand:

    Worker Master Data            -> actor profiles (a Person for each worker), actor roles (job roles), locations
    Corporate Directory Entries   -> the people's names, job titles and work phones, and their departments
    Access Entitlements           -> user identities, and the security groups each belongs to

Egeria's provisioning services deliver each product into Egeria's own schema in the subscription_staging database
(coco_egeria__<product schema>), as they do for every other subscriber.  The DAG coco_subscriptions_egeria takes it
from there.  Unlike the other coco_subscriptions_* DAGs it has no apply scripts: the destination is not a database,
so each task converts the delivered rows into calls to Egeria's REST APIs (see coco_egeria_client.py).

The DAG runs continuously:

1. wait_for_deliveries - a sensor that looks every few minutes for rows with processing_status 'delivered' in
   Egeria's three subscriptions, and finishes as soon as it finds some.
2. egeria.apply__worker_master_data, egeria.apply__corporate_directory_entries, egeria.apply__access_entitlements -
   run one after the other, because the later ones add to the people the first one creates.  Each applies the rows
   waiting in its own subscription and then marks them: processed, with 'applied' as the processing_message, or
   failed, with the error.  A failed row stays failed until its processing_status is set back to 'delivered'.

How the product data becomes open metadata:

* A worker is known to the products only by a pseudonym.  Where a Person with an employee number and the same name
  as the worker's directory entry is already in the catalogue, that Person is the worker.  Those profiles come from
  Coco's metadata archive, which is their master, and Egeria does not let them be changed: so nothing about the
  Person itself is updated, and only its links - location, roles, department, user identities, work phone - are
  added.  Otherwise a new Person::Coco::<pseudonym> is created, with the pseudonym recorded in
  additionalProperties.workerPseudonymIdentifier, and is kept in step with the products from then on.
* A site code becomes a KnownLocation link from the Person to a Location.  The products carry only the code, so
  coco-egeria-loads/site-locations.csv names the catalogued Location for each known code; a code that is not listed
  gets a new Location named after the code.
* A job role becomes a PersonRole (PersonRole::Coco::Job Role::<role code>) that the Person is appointed to.
* A department becomes a Team of type Dept.  A catalogued department is reused when its name is the department's
  and that is unambiguous; otherwise Department::Coco::<site code>::<department name> is created.  Its members are
  appointed to its TeamMembers role, as the departments already in the catalogue are organized.  A person who
  changes department is removed from the old one - except where both the person and the old department came from
  the archive, since nothing then records that the appointment was made here.
* An account becomes a UserIdentity linked to the Person, and its current entitlements become the identity's
  security groups.
* A worker who has left keeps their Person and user identities, but is removed from their job role and department.

Everything is applied by comparing with what Egeria already holds, so applying the same rows again changes nothing.

Connections (set as AIRFLOW_CONN_* in airflow-marquez.yaml): subscription_staging, and egeria - the platform URL,
with the view server as its schema and the user that the changes are made as.
"""
from __future__ import annotations

import csv
import importlib
import logging
from datetime import date, datetime, timedelta
from pathlib import Path

from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.sensors.python import PythonSensor
from airflow.sdk import DAG, Asset, Connection, PokeReturnValue, TaskGroup

# coco_egeria_client.py is beside this file, in the DAG bundle's folder, which airflow-marquez.yaml puts on PYTHONPATH.
# A DAG processor that was already running when the module was added has cached the folder's old contents, and
# passes that cache to the processes that parse the DAGs - so make Python look at the folder again.
importlib.invalidate_caches()
from coco_egeria_client import ACTOR_MANAGER, LOCATION_ARENA, Egeria  # noqa: E402

log = logging.getLogger(__name__)

STAGING_CONN_ID = "subscription_staging"
EGERIA_CONN_ID = "egeria"
SITE_LOCATIONS_FILE = Path(__file__).parent / "coco-egeria-loads" / "site-locations.csv"
# Where the staging database lives, as the Airflow containers see it - used only to name the assets.
POSTGRES_AUTHORITY = "host.docker.internal:5442"
POKE_INTERVAL = timedelta(minutes=5)
SENSOR_TIMEOUT = timedelta(hours=12)

# Egeria's subscriptions: the product schema, and its tables with their primary keys.
SUBSCRIPTIONS = {
    "worker_master_data": {"worker": ["worker_pseudonym_identifier"],
                           "worker_assignment": ["worker_pseudonym_identifier"]},
    "corporate_directory_entries": {"directory_entry": ["worker_pseudonym_identifier"]},
    "access_entitlements": {"account": ["user_account_identifier"],
                            "entitlement": ["user_account_identifier", "entitlement_code"]},
}

PSEUDONYM = "workerPseudonymIdentifier"
DEPARTMENT_ROLE = "departmentRoleQualifiedName"
DEPARTMENT_ROLE_PREFIX = "TeamMembers::Department::Coco::"
JOB_ROLE_PREFIX = "PersonRole::Coco::Job Role::"


def staging_schema(product_schema: str) -> str:
    return f"coco_egeria__{product_schema}"


def asset(schema: str, table: str) -> Asset:
    return Asset(name=f"{STAGING_CONN_ID}.{schema}.{table}",
                 uri=f"postgres://{POSTGRES_AUTHORITY}/{STAGING_CONN_ID}/{schema}/{table}")


def find_deliveries() -> PokeReturnValue:
    """Done when at least one of Egeria's subscriptions has rows waiting to be applied."""
    conn = PostgresHook(postgres_conn_id=STAGING_CONN_ID).get_conn()
    waiting = []
    try:
        with conn.cursor() as cur:
            for product_schema, tables in SUBSCRIPTIONS.items():
                cur.execute(" UNION ALL ".join(
                    f'SELECT 1 FROM "{staging_schema(product_schema)}"."{t}" WHERE processing_status = \'delivered\''
                    for t in tables) + " LIMIT 1")
                if cur.fetchone():
                    waiting.append(product_schema)
    finally:
        conn.rollback()
        conn.close()
    if waiting:
        log.info("Deliveries are waiting for Egeria in: %s", ", ".join(waiting))
    return PokeReturnValue(is_done=bool(waiting), xcom_value=waiting)


# ----------------------------------------------------------------------------------------------------------------
# The staged product data


class Staging:
    """Egeria's copy of the three products: every row for looking things up, and the rows waiting to be applied."""

    def __init__(self, conn):
        self.conn = conn
        self.rows: dict[str, list[dict]] = {}
        with conn.cursor() as cur:
            for product_schema, tables in SUBSCRIPTIONS.items():
                for table in tables:
                    cur.execute(f'SELECT * FROM "{staging_schema(product_schema)}"."{table}"')
                    names = [d[0] for d in cur.description]
                    self.rows[table] = [dict(zip(names, r)) for r in cur.fetchall()]
        conn.rollback()
        self.worker = {r["worker_pseudonym_identifier"]: r for r in self.rows["worker"]}
        self.directory = {r["worker_pseudonym_identifier"]: r for r in self.rows["directory_entry"]}
        self.account = {r["user_account_identifier"]: r for r in self.rows["account"]}

    def waiting(self, table: str) -> list[dict]:
        return [r for r in self.rows[table] if r["processing_status"] == "delivered"]

    def has_left(self, pseudonym: str) -> bool:
        worker = self.worker.get(pseudonym)
        return bool(worker) and worker["worker_current_status"] == "left"

    def mark(self, product_schema: str, table: str, row: dict, error: str | None) -> None:
        """Mark a row processed or failed - unless it has been delivered again since it was read."""
        key = SUBSCRIPTIONS[product_schema][table]
        with self.conn.cursor() as cur:
            cur.execute(
                f'UPDATE "{staging_schema(product_schema)}"."{table}" SET processing_status = %s, '
                f"processing_timestamp = now(), processing_message = %s WHERE "
                + " AND ".join(f'"{k}" = %s' for k in key) + " AND delivery_timestamp = %s",
                ["failed" if error else "processed", error or "applied"] + [row[k] for k in key]
                + [row["delivery_timestamp"]])
        self.conn.commit()


# ----------------------------------------------------------------------------------------------------------------
# What Egeria holds


def qualified_name(element: dict) -> str:
    return element["properties"].get("qualifiedName", "")


def related(element: dict, attribute: str) -> list[dict]:
    """The elements related to an element through one of the attributes of its retrieved form."""
    value = element.get(attribute) or []
    return [r["relatedElement"] for r in (value if isinstance(value, list) else [value])]


class Catalogue:
    """The people, roles, departments, locations and user identities in Egeria, and the changes made to them."""

    def __init__(self, egeria: Egeria, staging: Staging):
        self.egeria = egeria
        self.staging = staging
        profiles = egeria.find(ACTOR_MANAGER, "actor-profiles", "ActorProfile",
                               ["PersonRoleAppointment", "ProfileIdentity", "ContactThrough", "KnownLocation"])
        self.people = [p for p in profiles if p["elementHeader"]["type"]["typeName"] == "Person"]
        self.teams = {qualified_name(p): p for p in profiles if p["elementHeader"]["type"]["typeName"] == "Team"}
        self.roles = {qualified_name(r): r for r in
                      egeria.find(ACTOR_MANAGER, "actor-roles", "PersonRole", ["AssignmentScope"])}
        self.locations = {qualified_name(e): e for e in egeria.find(LOCATION_ARENA, "locations", "Location")}
        self.identities = {qualified_name(e): e for e in
                           egeria.find(ACTOR_MANAGER, "user-identities", "UserIdentity", ["ProfileIdentity"])}
        self.by_pseudonym = {p["properties"].get("additionalProperties", {}).get(PSEUDONYM): p for p in self.people}
        self.by_pseudonym.pop(None, None)
        with open(SITE_LOCATIONS_FILE, newline="") as f:
            self.site_locations = {r["site_code"]: r["location_qualified_name"] for r in csv.DictReader(f)}

    # People

    def person(self, pseudonym: str) -> dict:
        """The Person for a worker: the one created for the pseudonym, one already catalogued under the worker's
        name, or a new one."""
        if pseudonym in self.by_pseudonym:
            return self.by_pseudonym[pseudonym]
        entry = self.staging.directory.get(pseudonym)
        person = None
        if entry:
            first, last = entry["person_first_name"].strip().lower(), entry["person_last_name"].strip().lower()
            matches = [p for p in self.people
                       if p["properties"].get("employeeNumber") and not self.maintained_here(p)
                       and ((p["properties"].get("givenNames", "").strip().lower(),
                             p["properties"].get("surname", "").strip().lower()) == (first, last)
                            or p["properties"].get("displayName", "").strip().lower() == f"{first} {last}")]
            if len(matches) == 1:
                person = matches[0]
                log.info("Worker %s is %s, already in the catalogue", pseudonym, qualified_name(person))
        if person is None:
            properties = {"qualifiedName": f"Person::Coco::{pseudonym}", "displayName": pseudonym,
                          "additionalProperties": {PSEUDONYM: pseudonym}}
            guid = self.egeria.create(ACTOR_MANAGER, "actor-profiles", "PersonProperties", **properties)
            person = {"elementHeader": {"guid": guid, "type": {"typeName": "Person"}}, "properties": properties}
            self.people.append(person)
        self.by_pseudonym[pseudonym] = person
        return person

    @staticmethod
    def maintained_here(person: dict) -> bool:
        """True for a Person this DAG created.  The others come from Coco's metadata archive, which Egeria does
        not let be changed, so only links are added to them."""
        return qualified_name(person).startswith("Person::Coco::")

    def set_properties(self, person: dict, **properties) -> None:
        """Set properties of a Person this DAG maintains, where they differ from what Egeria holds."""
        changes = {k: v for k, v in properties.items() if v is not None and person["properties"].get(k) != v}
        if changes and self.maintained_here(person):
            self.egeria.update(ACTOR_MANAGER, "actor-profiles", person["elementHeader"]["guid"], "PersonProperties",
                               **changes)
            person["properties"].update(changes)

    def note(self, person: dict, **values) -> None:
        """Record values in the additionalProperties of a Person this DAG maintains.  None removes the entry."""
        current = person["properties"].get("additionalProperties", {})
        merged = {k: v for k, v in {**current, **values}.items() if v is not None}
        if merged != current and self.maintained_here(person):
            # additionalProperties is replaced as a whole, so the entries already there are sent back with it.
            self.egeria.update(ACTOR_MANAGER, "actor-profiles", person["elementHeader"]["guid"], "PersonProperties",
                               additionalProperties=merged)
            person["properties"]["additionalProperties"] = merged

    # Roles

    def role(self, name: str, **properties) -> dict:
        role = self.roles.get(name)
        if role is None:
            guid = self.egeria.create(ACTOR_MANAGER, "actor-roles", "PersonRoleProperties", qualifiedName=name,
                                      **properties)
            role = self.roles[name] = {"elementHeader": {"guid": guid}, "properties": {"qualifiedName": name}}
        return role

    def appoint(self, person: dict, role: dict) -> None:
        if qualified_name(role) not in {qualified_name(r) for r in related(person, "performsRoles")}:
            self.egeria.attach(ACTOR_MANAGER, f"actor-roles/{role['elementHeader']['guid']}/person-role-appointments/"
                                              f"{person['elementHeader']['guid']}", "PersonRoleAppointmentProperties")
            person.setdefault("performsRoles", []).append({"relatedElement": role})

    def relieve(self, person: dict, keep: str | None, prefix: str | None = None, name: str | None = None) -> None:
        """End the Person's appointments to the roles with a prefix, or to one named role, except the one to keep."""
        for role in related(person, "performsRoles"):
            role_name = qualified_name(role)
            if role_name != keep and (role_name == name or (prefix and role_name.startswith(prefix))):
                self.egeria.detach(ACTOR_MANAGER, f"actor-roles/{role['elementHeader']['guid']}/"
                                                  f"person-role-appointments/{person['elementHeader']['guid']}")
                log.info("%s no longer performs %s", qualified_name(person), role_name)
        person["performsRoles"] = [r for r in (person.get("performsRoles") or [])
                                   if qualified_name(r["relatedElement"]) == keep
                                   or not (qualified_name(r["relatedElement"]) == name
                                           or (prefix and qualified_name(r["relatedElement"]).startswith(prefix)))]

    # Locations

    def location(self, site_code: str) -> dict:
        name = self.site_locations.get(site_code, f"Site::Coco::{site_code}")
        if name not in self.locations:
            if site_code in self.site_locations:
                raise RuntimeError(f"{SITE_LOCATIONS_FILE.name} maps site {site_code} to {name}, which is not in "
                                   f"Egeria")
            guid = self.egeria.create(LOCATION_ARENA, "locations", "LocationProperties", qualifiedName=name,
                                      identifier=site_code, displayName=f"Site {site_code}",
                                      description=f"The site with code {site_code} in the Worker Master Data and "
                                                  f"Corporate Directory Entries digital products.")
            self.locations[name] = {"elementHeader": {"guid": guid}, "properties": {"qualifiedName": name}}
        return self.locations[name]

    def place(self, element: dict, site_code: str) -> None:
        """Link a Person or Team to its site's Location, replacing a link to another site's Location."""
        location = self.location(site_code)
        sites = {self.site_locations.get(code, f"Site::Coco::{code}")
                 for code in {w["site_code"] for w in self.staging.worker.values()}
                 | {d["site_code"] for d in self.staging.directory.values()}}
        linked = {qualified_name(known): known for known in related(element, "knownLocations")}
        for name, known in linked.items():
            if name != qualified_name(location) and name in sites:
                self.egeria.detach(LOCATION_ARENA, f"elements/{element['elementHeader']['guid']}/known-locations/"
                                                  f"{known['elementHeader']['guid']}")
        if qualified_name(location) not in linked:
            self.egeria.attach(LOCATION_ARENA, f"elements/{element['elementHeader']['guid']}/known-locations/"
                                               f"{location['elementHeader']['guid']}", "KnownLocationProperties")
        element["knownLocations"] = [{"relatedElement": location}]

    # Departments

    def department(self, site_code: str, department_name: str) -> dict:
        """The Team for a department at a site, with its TeamMembers role.  Returns the role."""
        sites = {d["site_code"] for d in self.staging.directory.values() if d["department_name"] == department_name}
        catalogued = [t for t in self.teams.values() if t["properties"].get("displayName") == department_name
                      and not qualified_name(t).startswith("Department::Coco::")]
        if len(sites) == 1 and len(catalogued) == 1:
            team = catalogued[0]
        else:
            name = f"Department::Coco::{site_code}::{department_name}"
            team = self.teams.get(name)
            if team is None:
                guid = self.egeria.create(
                    ACTOR_MANAGER, "actor-profiles", "TeamProperties", qualifiedName=name,
                    identifier=f"{site_code}::{department_name}", displayName=department_name, teamType="Dept",
                    description=f"The {department_name} department at site {site_code}, from the Corporate "
                                f"Directory Entries digital product.")
                team = self.teams[name] = {"elementHeader": {"guid": guid}, "properties": {"qualifiedName": name}}
                self.place(team, site_code)
        role_name = f"TeamMembers::{qualified_name(team)}"
        role = self.role(role_name, identifier=role_name, actorRoleGroups=["team-member"])
        if qualified_name(team) not in {qualified_name(s) for s in related(role, "assignmentScope")}:
            self.egeria.attach(ACTOR_MANAGER, f"elements/{team['elementHeader']['guid']}/actors/"
                                              f"{role['elementHeader']['guid']}", "AssignmentScopeProperties",
                               assignmentType="Contributor")
            role["assignmentScope"] = [{"relatedElement": team}]
        return role


# ----------------------------------------------------------------------------------------------------------------
# Applying each product


def apply_worker_master_data(catalogue: Catalogue, staging: Staging, table: str, row: dict) -> None:
    pseudonym = row["worker_pseudonym_identifier"]
    person = catalogue.person(pseudonym)
    if table == "worker":
        catalogue.set_properties(person, employeeType=row["worker_type"])
        catalogue.note(person, workerStatus=row["worker_current_status"], legalEntityCode=row["legal_entity_code"],
                       siteCode=row["site_code"])
        catalogue.place(person, row["site_code"])
        if row["worker_current_status"] == "left":
            catalogue.relieve(person, keep=None, prefix=JOB_ROLE_PREFIX)
            catalogue.relieve(person, keep=None, prefix=DEPARTMENT_ROLE_PREFIX,
                              name=person["properties"].get("additionalProperties", {}).get(DEPARTMENT_ROLE))
            catalogue.note(person, **{DEPARTMENT_ROLE: None})
    else:
        catalogue.note(person, costCentreCode=row["cost_centre_code"],
                       managerPseudonymIdentifier=row["manager_pseudonym_identifier"])
        name = JOB_ROLE_PREFIX + row["role_code"]
        role = catalogue.role(name, identifier=row["role_code"], displayName=row["role_name"],
                              description=f"The job role {row['role_code']} in the Worker Master Data digital "
                                          f"product.")
        if staging.has_left(pseudonym):
            catalogue.relieve(person, keep=None, prefix=JOB_ROLE_PREFIX)
        else:
            catalogue.appoint(person, role)
            catalogue.relieve(person, keep=name, prefix=JOB_ROLE_PREFIX)


def apply_corporate_directory_entries(catalogue: Catalogue, staging: Staging, table: str, row: dict) -> None:
    pseudonym = row["worker_pseudonym_identifier"]
    person = catalogue.person(pseudonym)
    first, last = row["person_first_name"].strip(), row["person_last_name"].strip()
    catalogue.set_properties(person, displayName=f"{first} {last}", givenNames=first, surname=last,
                             fullName=f"{first} {last}", jobTitle=row["role_name"])
    egeria = catalogue.egeria
    phone = row["person_work_phone_number"]
    if phone:
        name = f"ContactDetails::Coco::{pseudonym}::Work Phone"
        details = {qualified_name(c): c for c in related(person, "contactDetails")}.get(name)
        if details is None:
            guid = egeria.create(ACTOR_MANAGER, "contact-details", "ContactDetailsProperties", qualifiedName=name,
                                 displayName="Work Phone", contactType="Work Phone", contactMethodType="PHONE",
                                 contactMethodValue=phone)
            egeria.attach(ACTOR_MANAGER, f"elements/{person['elementHeader']['guid']}/contact-details/{guid}",
                          "ContactThroughProperties")
            person.setdefault("contactDetails", []).append({"relatedElement": {
                "elementHeader": {"guid": guid}, "properties": {"qualifiedName": name, "contactMethodValue": phone}}})
        elif details["properties"].get("contactMethodValue") != phone:
            egeria.update(ACTOR_MANAGER, "contact-details", details["elementHeader"]["guid"],
                          "ContactDetailsProperties", contactMethodValue=phone)
            details["properties"]["contactMethodValue"] = phone
    previous = person["properties"].get("additionalProperties", {}).get(DEPARTMENT_ROLE)
    if staging.has_left(pseudonym):
        catalogue.relieve(person, keep=None, prefix=DEPARTMENT_ROLE_PREFIX, name=previous)
        catalogue.note(person, **{DEPARTMENT_ROLE: None})
    else:
        role = catalogue.department(row["site_code"], row["department_name"])
        catalogue.appoint(person, role)
        catalogue.relieve(person, keep=qualified_name(role), prefix=DEPARTMENT_ROLE_PREFIX, name=previous)
        catalogue.note(person, **{DEPARTMENT_ROLE: qualified_name(role)})


def apply_access_entitlements(catalogue: Catalogue, staging: Staging, table: str, row: dict) -> None:
    """Applies an account, with all of its entitlements.  An entitlement row is applied through its account."""
    account = staging.account.get(row["user_account_identifier"])
    if account is None:
        raise RuntimeError(f"No account {row['user_account_identifier']} has been delivered for this entitlement")
    egeria = catalogue.egeria
    account_id = account["user_account_identifier"]
    if account_id in catalogue.applied_accounts:
        return
    person = catalogue.person(account["worker_pseudonym_identifier"])
    name = f"UserIdentity::Coco::{account_id}"
    properties = {
        "userId": account_id.rsplit("\\", 1)[-1].rsplit(":", 1)[-1],
        "distinguishedName": account_id,
        "displayName": account_id,
        "additionalProperties": {k: str(v) for k, v in {
            "systemIdentifier": account["system_identifier"],
            "userAccountStatus": account["user_account_current_status"],
            "userAccountStartDate": account["user_account_start_date"],
            "userAccountEndDate": account["user_account_end_date"]}.items() if v is not None},
    }
    identity = catalogue.identities.get(name)
    if identity is None:
        guid = egeria.create(ACTOR_MANAGER, "user-identities", "UserIdentityProperties", qualifiedName=name,
                             **properties)
        identity = catalogue.identities[name] = {"elementHeader": {"guid": guid},
                                                 "properties": {"qualifiedName": name, **properties}}
    else:
        changes = {k: v for k, v in properties.items() if identity["properties"].get(k) != v}
        if changes:
            egeria.update(ACTOR_MANAGER, "user-identities", identity["elementHeader"]["guid"],
                          "UserIdentityProperties", **changes)
            identity["properties"].update(changes)
    guid = identity["elementHeader"]["guid"]
    if person["elementHeader"]["guid"] not in {p["elementHeader"]["guid"] for p in related(identity, "userProfile")}:
        egeria.attach(ACTOR_MANAGER, f"user-identities/{guid}/profile-identity/{person['elementHeader']['guid']}",
                      "ProfileIdentityProperties", description=f"Account on {account['system_identifier']}.")
        identity["userProfile"] = {"relatedElement": person}

    # The security groups are the entitlements the account holds today.
    today = date.today()
    groups = sorted(e["entitlement_code"] for e in staging.rows["entitlement"]
                    if e["user_account_identifier"] == account_id
                    and account["user_account_current_status"] == "active"
                    and e["entitlement_start_date"] <= today
                    and (e["entitlement_end_date"] is None or e["entitlement_end_date"] > today))
    membership = identity["elementHeader"].get("securityListMembership")
    current = sorted((membership or {}).get("classificationProperties", {}).get("securityGroups") or [])
    if groups != current:
        if groups:
            egeria.classify(ACTOR_MANAGER, f"user-identities/{guid}/security-group-memberships",
                            "SecurityGroupMembershipProperties", securityGroups=groups)
        elif membership:
            egeria.declassify(ACTOR_MANAGER, f"user-identities/{guid}/security-group-memberships")
        identity["elementHeader"]["securityListMembership"] = \
            {"classificationProperties": {"securityGroups": groups}} if groups else None
    catalogue.applied_accounts.add(account_id)


APPLY = {
    "worker_master_data": apply_worker_master_data,
    "corporate_directory_entries": apply_corporate_directory_entries,
    "access_entitlements": apply_access_entitlements,
}


def apply_subscription(staging_conn, egeria: Egeria, product_schema: str) -> dict[str, int]:
    """Apply the rows waiting in one of Egeria's subscriptions, and mark each of them in subscription_staging."""
    staging = Staging(staging_conn)
    tables = list(SUBSCRIPTIONS[product_schema])
    counts = {"applied": 0, "failed": 0}
    if not any(staging.waiting(t) for t in tables):
        return counts
    catalogue = Catalogue(egeria, staging)
    catalogue.applied_accounts = set()
    for table in tables:
        for row in staging.waiting(table):
            error = None
            try:
                APPLY[product_schema](catalogue, staging, table, row)
            except Exception as e:
                error = f"{type(e).__name__}: {e}".strip()[:2000]
                log.error("Applying %s.%s %s failed: %s", staging_schema(product_schema), table,
                          [row[k] for k in SUBSCRIPTIONS[product_schema][table]], error)
            staging.mark(product_schema, table, row, error)
            counts["failed" if error else "applied"] += 1
    if counts["failed"]:
        raise RuntimeError(f"{staging_schema(product_schema)}: {counts['failed']} row(s) failed, "
                           f"{counts['applied']} applied - see processing_message in subscription_staging")
    return counts


def connect_to_egeria() -> Egeria:
    conn = Connection.get(EGERIA_CONN_ID)
    return Egeria(f"{conn.conn_type or 'https'}://{conn.host}:{conn.port}", conn.schema, conn.login, conn.password)


def apply(product_schema: str) -> None:
    staging_conn = PostgresHook(postgres_conn_id=STAGING_CONN_ID).get_conn()
    try:
        counts = apply_subscription(staging_conn, connect_to_egeria(), product_schema)
    finally:
        staging_conn.close()
    log.info("%s: %d row(s) applied to Egeria", staging_schema(product_schema), counts["applied"])


with DAG(
    dag_id="coco_subscriptions_egeria",
    description="Applies the digital product data delivered to Egeria to its catalogue of people and organization.",
    doc_md=__doc__,
    schedule="@continuous",
    max_active_runs=1,
    start_date=datetime(2026, 11, 1),
    catchup=False,
    is_paused_upon_creation=False,
    tags=["coco", "digital-product-subscription", "Coco core", "egeria"],
) as coco_subscriptions_egeria:
    previous = PythonSensor(
        task_id="wait_for_deliveries",
        python_callable=find_deliveries,
        mode="reschedule",
        poke_interval=POKE_INTERVAL.total_seconds(),
        timeout=SENSOR_TIMEOUT.total_seconds(),
        soft_fail=True,
        doc_md="Waits until at least one of Egeria's subscriptions has delivered rows waiting.",
    )
    with TaskGroup(group_id="egeria", tooltip="Applies to Egeria"):
        for _product_schema, _tables in SUBSCRIPTIONS.items():
            _task = PythonOperator(
                task_id=f"apply__{_product_schema}",
                python_callable=apply,
                op_kwargs={"product_schema": _product_schema},
                # A failure in one product should not hold back the others' rows.
                trigger_rule="all_done" if _product_schema != "worker_master_data" else "all_success",
                inlets=[asset(staging_schema(_product_schema), t) for t in _tables],
                doc_md=f"Applies the subscription `{staging_schema(_product_schema)}` to Egeria through its REST "
                       f"APIs.",
            )
            previous >> _task
            previous = _task
