# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Egeria project.
"""
A small client for the Egeria REST APIs that coco_egeria_loads.py calls: the Actor Manager and Location Arena view
services of a view server.

It uses the REST APIs directly, rather than pyegeria, so that the DAG depends only on what the Airflow image already
has (requests) and not on the pyegeria release installed in it.

This module is not a DAG file: .airflowignore keeps the DAG processor from parsing it.
"""
from __future__ import annotations

import logging

import requests
import urllib3

log = logging.getLogger(__name__)

ACTOR_MANAGER = "actor-manager"
LOCATION_ARENA = "location-arena"
TIMEOUT = 180


class EgeriaError(RuntimeError):
    """Egeria rejected a request."""


class Egeria:
    """Calls one view server as one user.  Every call is a POST that returns Egeria's JSON response."""

    def __init__(self, platform_url: str, view_server: str, user_id: str, password: str, verify: bool = False):
        self.platform_url = platform_url.rstrip("/")
        self.view_server = view_server
        self.session = requests.Session()
        self.session.verify = verify          # the quickstart platform has a self-signed certificate
        if not verify:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = self.session.post(f"{self.platform_url}/api/token",
                                     json={"userId": user_id, "password": password}, timeout=TIMEOUT)
        if response.status_code != 200 or not response.text:
            raise EgeriaError(f"{user_id} could not log on to {self.platform_url}: HTTP {response.status_code}")
        self.session.headers["Authorization"] = f"Bearer {response.text}"

    def post(self, service: str, path: str, body: dict | None = None) -> dict:
        url = f"{self.platform_url}/servers/{self.view_server}/api/open-metadata/{service}/{path}"
        response = self.session.post(url, json=body, timeout=TIMEOUT)
        try:
            result = response.json() if response.text else {}
        except ValueError:
            result = {}
        if response.status_code != 200 or result.get("relatedHTTPCode", 200) != 200:
            raise EgeriaError(f"{service}/{path}: HTTP {response.status_code} "
                              f"{result.get('exceptionErrorMessage') or response.text[:500]}")
        return result

    # Elements

    def find(self, service: str, kind: str, type_name: str, relationships: list[str] | None = None) -> list[dict]:
        """Every element of a type, each with the related elements reached by the relationships named."""
        body = {"class": "SearchStringRequestBody", "metadataElementTypeName": type_name, "startFrom": 0,
                "pageSize": 0, "graphQueryDepth": 1 if relationships else 0}
        if relationships:
            body["includeOnlyRelationships"] = relationships
        return self.post(service, f"{kind}/by-search-string", body).get("elements") or []

    def create(self, service: str, kind: str, properties_class: str, **properties) -> str:
        body = {"class": "NewElementRequestBody", "properties": {"class": properties_class, **properties}}
        guid = self.post(service, kind, body)["guid"]
        log.info("Created %s %s", properties_class.removesuffix("Properties"), properties.get("qualifiedName"))
        return guid

    def update(self, service: str, kind: str, guid: str, properties_class: str, **properties) -> None:
        """Change the properties named, leaving the element's other properties as they are."""
        self.post(service, f"{kind}/{guid}/update",
                  {"class": "UpdateElementRequestBody", "mergeUpdate": True,
                   "properties": {"class": properties_class, **properties}})

    # Relationships and classifications

    def attach(self, service: str, path: str, properties_class: str, **properties) -> None:
        self.post(service, f"{path}/attach",
                  {"class": "NewRelationshipRequestBody", "properties": {"class": properties_class, **properties}})

    def detach(self, service: str, path: str) -> None:
        self.post(service, f"{path}/detach", {"class": "DeleteRelationshipRequestBody"})

    def classify(self, service: str, path: str, properties_class: str, **properties) -> None:
        self.post(service, f"{path}/classify",
                  {"class": "NewClassificationRequestBody", "properties": {"class": properties_class, **properties}})

    def declassify(self, service: str, path: str) -> None:
        self.post(service, f"{path}/declassify", {"class": "DeleteClassificationRequestBody"})
