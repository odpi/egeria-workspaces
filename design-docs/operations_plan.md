
The egeria-operations tool supports an operator of Egeria in understanding the status of Egeria's runtime.  It uses the RuntimeManager client of pyegeria.  It has four tabs.

- Servers
- Integration Connectors
- Governance Engines
- Engine Actions

Each tab has a dropdown to select the platform to display and the appropriate server from that platform to display. 
If the user has selected a platform on another tab - use that as the default. 

Note: The server list is slightly different on each tab - this is explained later in each tab description section.

The list of platforms and the servers running on that platform can be retrieved using RuntimeManager.get_platforms_by_type(body={"filter" : "OMAG Server Platform", "graphQueryDepth" : 0, "includeOnlyRelationships" : "DeployedOn"}).  For each platform extract:

- the platform guid (from the elementHeader.guid)
- the platform display name (from properties.displayName - or if this is null use properties.qualifiedName)
- for each server listed in "deployedTo" extract:
     - the server_guid (from the elementHeader.guid)
     - the server display name (from properties.displayName - or if this is null use properties.qualifiedName)
     - the server type (from properties.deployedImplementationType)

This information is used for each tab and is slowly changing, so it is ok to cache it and retrieve only when the user requests a refresh.

Details about a server are retrieved using RuntimeManager.get_server_report(server_guid=selected server_guid).  The server report values are changing all of the time, so this information needs to be retrieved each time the user requests selects an element to display - or requests a display is refreshed.

> ### 🔎 Review — overview & backend (Claude, 2026-06-22)
> 💬 **Architecture.** New standalone SPA, same shape as `egeria-audit.html`: `egeria-operations.html`
> + `operations_handler.py` (FastAPI router) + a portal tile in `demo-portal.html` + an Apache
> `<Location>` proxy route — all in **both** quickstart and freshstart (dual-file convention; pick a
> `78xx`/`88xx` route, e.g. `/egeria-operations`). Reuse `egeria-shared-ui.js`: `egeriaFetch` +
> token auth, `useColumnResize`, the **docked resizable side-panel** just built for the audit Users
> tab (perfect for the per-server full report + per-connector "all details"), `Collapsible`,
> `crossAppNavigate`/`resolveElementNav` for the Catalog cross-links, and copy the App-level
> connect/persona bootstrap straight from `egeria-audit.html` (local quickstart has no portal
> identity, and every operation here needs a privileged Egeria user).
>
> 💬 **Backend verified (deployed pyegeria, today).** Every method exists — with 3 name fixes, and
> **both "Note to Dan / missing" items are already resolved** in the running container:
>   • `RuntimeManager.refresh_integration_connectors` — **plural** (spec says `_connector`). Present.
>     `(connector_name=None, server_guid=None, body=None)`; body = `NameRequestBody{name: connector}`.
>   • `RuntimeManager.refresh_governance_engine(gov_engine_name=…, server_guid=…)` — present; note the
>     param is **`gov_engine_name`**, not `governance_engine_name`.
>   • `AssetMaker.find_processes(…)` — **snake_case** (spec says `findProcesses`). Has native params
>     (`search_string`, `activity_status_list`, `metadata_element_subtypes`, `graph_query_depth`,
>     `as_of_time`) so you can skip the hand-built body — see Engine Actions note.
>   • Verified present: `get_platforms_by_type`, `get_server_report`,
>     `activate_server_with_stored_config(server_guid)`, `shutdown_server(server_guid)`,
>     `start_connector`, `stop_connector`, `AssetMaker.get_catalog_targets(integration_connector_guid,
>     graph_query_depth)`, `AutomatedCuration.cancel_engine_action(engine_action_guid)`.
>   • All three classes (`RuntimeManager`, `AssetMaker`, `AutomatedCuration`) ARE top-level in the
>     `pyegeria` namespace (unlike `SecurityOfficer` in audit). `cancel_engine_action` lives on
>     `AutomatedCuration` — a 4th client beyond the RuntimeManager the intro mentions.
>
> 💬 **Privileged operations = confirm + gate.** start/stop server, activate/shutdown, start/stop/
> refresh connector, refresh engine, cancel engine action are all **writes**. Reuse the audit pattern:
> `_is_admin` gate (from `demo_feedback_handler`) + a confirmation dialog before firing. Don't expose
> the controls to non-admins. `activate_server_with_stored_config` is slow (`timeout=240`) — run it
> async with a spinner and don't let auto-refresh stack on top of it.
>
> 💬 **Shared, modular pieces (the MOD-2/3 / audit lesson).** Lift the **platform selector to
> App-level shared state** so a platform chosen on one tab is the default on the others (spec line 10).
> Cache the platforms+servers list (slowly changing) with an explicit Refresh. The **server** picker
> is per-tab because each tab filters by server type, so: shared platform, per-tab server list. Build
> ONE reusable `RefreshControl` (manual button + interval-in-seconds → `setInterval`) used by all four
> tabs — pause polling while a confirm dialog is open and when `document.hidden`. Servers / Integration
> Connectors / Governance Engines are all "`get_server_report` → project one sub-list", so model them
> as one report fetch + a per-tab projection rather than three separate fetch paths.
>
> 💬 **✅ get_platforms_by_type — VERIFIED RECIPE (garygeeke, quickstart, 2026-06-22).** With Dan's
>   four corrections it works. Use:
>   ```python
>   body = {"class":"FilterRequestBody", "filter":"OMAG Server Platform",
>           "graphQueryDepth": 1, "includeOnlyRelationships": ["DeployedOn"]}
>   r = runtime.get_platforms_by_type(body=body, output_format="JSON")   # raw payload
>   ```
>   - `includeOnlyRelationships` is a **list** (string is rejected by pydantic).
>   - `graphQueryDepth` is **1** (depth 0 returns no relationships).
>   - Per platform: `elementHeader.guid`, `properties.displayName` (‖ `qualifiedName`).
>   - Servers are under **`hostedITAssets`** (key present ONLY when the platform has servers — e.g. the
>     "Local" platform has none, "Quickstart" has 4). Each entry is a DeployedOn **relationship**; the
>     server element is under **`relatedElement`**:
>       • `relatedElement.elementHeader.guid`  → server_guid
>       • `relatedElement.properties.displayName` (‖ qualifiedName) → server name
>       • `relatedElement.properties.deployedImplementationType` → server type (used for per-tab filter)
>   - **deployedImplementationType strings (verified):** `Integration Daemon` (exact ✓),
>     **`Engine Host Server`** (spec said "Engine Host" — note trailing "Server"), `View Server`,
>     `Metadata Access Store`. Filter the Integration Connectors / Governance Engines tabs on these.
>   ⚠️ Demo GUIDs change on every container reload (audit lesson): fetch platforms/servers live; do NOT
>   persist `?guid=` deep-links to servers.
>
> 💬 **Enums need value→label maps (only Engine Actions' is given).** `serverActiveStatus`,
> connector `connectorStatus`, and `governanceEngineStatus` are all enums but the spec doesn't list
> their values. Supply them (like the audit `UserAccountStatus` map) so the tables show friendly
> labels + colour, not raw enum names. The Engine-Action `activityStatus` enum IS fully given below.
> **→ Resolved: all four enums captured below (confirmed by Dan, 2026-06-22).**

## Enums (confirmed by Dan, 2026-06-22)

Build value→label maps in shared-ui (suggested colour intent in brackets — green=healthy,
amber=transitional/waiting, red=fault, grey=inactive/unknown):

```js
// serverActiveStatus
var SERVER_STATUS_LABEL = {
  UNKNOWN:  'Unknown',   // [grey]
  STARTING: 'Starting',  // [amber]
  RUNNING:  'Running',   // [green]
  STOPPING: 'Stopping',  // [amber]
  INACTIVE: 'Inactive',  // [grey]
};
// integration connectorStatus
var CONNECTOR_STATUS_LABEL = {
  INITIALIZED:       'Initialized',           // [amber]
  WAITING:           'Waiting',               // [green]
  REFRESHING:        'Refreshing',            // [green]
  RUNNING:           'Running',               // [green]
  STOPPED:           'Stopped',               // [grey]
  INITIALIZE_FAILED: 'Initialize Failed',     // [red]
  CONFIG_FAILED:     'Configuration Failed',  // [red]
  SHUTDOWN:          'Shutdown',              // [grey]
  FAILED:            'Connector Failed',      // [red]
};
// governanceEngineStatus
var GOV_ENGINE_STATUS_LABEL = {
  ASSIGNED:    'Assigned',     // [grey]
  CONFIGURING: 'Configuring',  // [amber]
  RUNNING:     'Running',      // [green]
  FAILED:      'Failed',       // [red]
  DISABLED:    'Disabled',     // [grey]
};
// engine-action activityStatus (from spec)
var ACTIVITY_STATUS_LABEL = {
  REQUESTED: 'Requested', APPROVED: 'Approved', WAITING: 'Waiting', ACTIVATING: 'Activating',
  IN_PROGRESS: 'In Progress', PAUSED: 'Paused', COMPLETED: 'Completed', INVALID: 'Invalid',
  IGNORED: 'Ignored', FAILED: 'Failed', CANCELLED: 'Cancelled', ABANDONED: 'Abandoned',
};
```

Also confirmed: **governanceEngineSummaries carry a GUID** (use it for the Catalog cross-link).

## Servers tab

The servers tab is for understanding the configuration and status of each server running on the selected platform.

It works off of details for each server retrieved using RuntimeManager.get_server_report(server_guid=selected server_guid)

At the top of the table is a table showing the following details of the server:

- Server Name - from element.serverName
- Server Type - from element.serverType
- Description - from element.description
- Organization - from element.organizationName
- Status - from element.serverActiveStatus - this is an enum

The user can manually refresh or set a refresh interval in seconds.

The user can also select a server and all information returned by the server report is displayed.  This is refreshed whenever the server table is refreshed.  It should also be possible to start or stop a server.  This uses the RuntimeManager activate_server_with_stored_config(server_guid=selected server_guid) and shutdown_server(server_guid=selected server_guid)

> ### 🔎 Review — Servers tab
> 💬 Confirm the `get_server_report` top-level shape: spec reads `element.serverName`,
>    `element.serverActiveStatus`, etc. — verify the report is `{element:{…}}` (vs flat) and that
>    `report_spec='OMAGServers'` (the default) is the right spec for all server types here.
> 💬 `serverActiveStatus` enum → supply the value list + a label/colour map (UNKNOWN / STARTING /
>    RUNNING / STOPPING / INACTIVE …). Start/Stop button enablement keys off this status.
> 💬 "Select a server → full report" is a textbook fit for the new docked resizable side-panel.
> 💬 Start/Stop = privileged writes → admin-gate + confirm dialog. `activate_…` is slow (timeout=240):
>    async + spinner; suppress auto-refresh until it returns so you don't queue overlapping activations.

## Integration Connectors

The Integration Connectors tab is for understanding and updating the status of the integration connectors running on the integration daemon servers.  Again it is possible to select a platform from the dropdown.  The list of servers to select is restricted to those of type Integration Daemon.

When the server report for this type of server is returned, there are two special lists returned:

- integrationGroups - is a lookup table for the integration group that an integration connector belongs to.
- integrationConnectorReports - is a list of integration connectors to display.  For each integration connector, also retrieve the list of catalog targets using the connectorGUID and AssetMaker.get_catalog_targets(integration_connector_guid=connectorGUID, graph_query_depth=0)

This information is used to build the table of integration connectors running on the selected integration daemon server. The columns of this table are:

- Connector Name - from integrationConnectorReport.connectorName
- Connector Status - from integrationConnectorReport.connectorName - this is an enum
- Catalog Targets - This is a table within this table column showing details from the list of catalog targets.  Display:
	- Catalog Target Name - from catalogTargetName from the catalog target relationship
	- Catalog Target Type - from the relatedElement.elementHeader.type.typeName
	- Catalog Target Element GUID - from the relatedElement.elementHeader.guid
	- Catalog Target Element Name - from the relatedElement.properties.displayName (or qualifiedName if displayName is null)
- Integration Group - integration group name matched to integrationConnectorReport.integrationGroupName in the lookup table. Note this value may be null.
- Last Status Change - from integrationConnectorReport.lastStatusChange  
- Last Refresh Time - from integrationConnectorReport.lastRefreshTime
- Refresh Interval (mins) - from integrationConnectorReport.minMinutesBetweenRefresh
- Failing Message - from integrationConnectorReport.failingExceptionMessage

There are options to display all details retrieved about an integration connector, and to start, stop and refresh each connector.  It is also possible to navigate to the integration connector asset in The Catalog under Processes.

Starting a connector uses RuntimeManager.start_connector(server_guid=selected server_guid, connector_name=selected connectorName)
Stopping a connector uses RuntimeManager.stop_connector(server_guid=selected server_guid, connector_name=selected connectorName)
Refreshing a connector uses RuntimeManager.refresh_integration_connector(server_guid=selected server_guid, connector_name=selected connectorName)

**Note to Dan**
The refresh_integration_connector() method is missing from Runtime Manager.  The REST API is:
==> done
```
###  
# @name refreshConnectors  
# Issue a refresh() request on all connectors running in the integration daemon, or a specific connector if the connector name is specified.  
POST {{baseURL}}/servers/{{viewServer}}/api/open-metadata/runtime-manager/integration-daemons/{{serverGUID}}/integration-connectors/refresh  
Authorization: Bearer {{token}}  
Content-Type: application/json  
  
{  
  "class" : "NameRequestBody",  
  "name" : "add connector name here"
}
```

It should be possible to filter the table display by integration group or connector name.
The user can manually refresh the table or set a refresh interval in seconds.

> ### 🔎 Review — Integration Connectors
> 💬 ⚠️ TYPO line 56: "Connector Status - from integrationConnectorReport.connectorName" → should be
>    **connectorStatus**. (`connectorStatus` is the enum; needs a label map.)
> 💬 Server filter = `deployedImplementationType == "Integration Daemon"` (verified exact ✓).
> 💬 N+1 warning: `get_catalog_targets` is one call **per connector**. A busy daemon = many calls →
>    fan them out concurrently (asyncio.gather + Semaphore, exactly the audit Users-tab fix) so the
>    tab doesn't time out. Use `graph_query_depth=0`; note `page_size` defaults to 0 — set it so you
>    actually get all targets.
> 💬 Refresh: the method is `refresh_integration_connectors` today (you said you'll rename to the
>    **singular** `refresh_integration_connector` — once renamed, reinstall pyegeria + cycle the
>    container before the handler imports it). Call form: `(server_guid=…, connector_name=…)` or
>    body `NameRequestBody{name: connectorName}`. Start/Stop/Refresh = writes → admin-gate + confirm.
> 💬 Cross-link "connector asset in Catalog under Processes": use `connectorGUID` through
>    `crossAppNavigate` — confirm the connector element's type resolves to the Catalog Processes view.
> 💬 Filters (integration group / connector name) are client-side over the already-fetched rows.

## Governance Engines

The governance engines tab is for understanding the governance engines running on an engine host server and to be able to refresh its configuration. Again it is possible to select a platform from the dropdown.  The list of servers to select is restricted to those of type Engine Host.

When the server report for this type of server is returned, there is an additional list returned called governanceEngineSummaries.  This contains the information to display on this tab.  Display a table where each row is a governance engine returned in the governanceEngineSummaries.  The columns of this table are.

- Name - from governanceEngineName
- Type - from governanceEngineTypeName 
- Service Name - from governanceEngineService
- Description - from governanceEngineDescription 
- Status - from governanceEngineStatus - this is an enum
- Request Types - from governanceRequestTypes - this is a list of strings
- Last Refresh Time - from lastRefreshTime

It should be possible to filter the table display by governance engine name.  It should also be possible to refresh a governance engine (RuntimeManager.refresh_governance_engine(server_guid=selected server_guid, governance_engine_name=selected governanceEngineName)).  It should also be possible to navigate to the governance engine details in The catalog under Infrastructure Asset/Software Capabilities.

The user can manually refresh the table or set a refresh interval in seconds.


**Note to Dan**
RuntimeManager is missing refresh_governance_engine method - this is the REST API:
==> done
```
###  
# @namerefreshConfig  
# Request that the governance engine refresh its configuration by calling the metadata server.  
# This request is useful if the metadata server has an outage, particularly while the  
# governance server is initializing.  This request just ensures that the latest configuration  
# is in use. See https://egeria-project.org/concepts/governance-engine-definition/  
GET {{baseURL}}/servers/{{viewServer}}/api/open-metadata/runtime-manager/engine-hosts/{{serverGUID}}/governance-engines/{{governanceEngineName}}/refresh-config  
Authorization: Bearer {{token}}
```

> ### 🔎 Review — Governance Engines
> 💬 `refresh_governance_engine` IS present in the deployed container — the "missing" note is stale.
>    Param name is **`gov_engine_name`**: `refresh_governance_engine(gov_engine_name=…, server_guid=…)`.
> 💬 Server filter = `deployedImplementationType == "Engine Host Server"` (verified — note trailing "Server", spec said "Engine Host").
> 💬 `governanceEngineStatus` enum → supply value list + label map.
> 💬 ⚠️ Cross-link gap: the columns (Name/Type/Service/Description/Status/RequestTypes/LastRefresh)
>    include **no GUID**, but "navigate to the engine in the Catalog under Infrastructure/Software
>    Capabilities" needs one. Confirm `governanceEngineSummaries[*]` carries a `governanceEngineGUID`
>    (or similar) — required for the cross-link.
> 💬 Refresh = write → admin-gate + confirm.

## Engine Actions

Engine actions allow a user to review the status of the engine actions executing in the open metadata ecosystem.  There are a lot of them so the query needs to be controlled by user selection:

- a search string - default `*`
- a list of activity statuses from:
    - REQUESTED  -    "Requested" - The description of the activity has been created and is pending." 
    - APPROVED     -   "Approved" - The activity is approved to run. This means that the mandatory preconditions have been satisfied. 
	- WAITING - "Waiting" - The activity is waiting for its start time or an actor to claim it.
	- ACTIVATING - "Activating" - The process that will perform the activity is being activated.
	- IN_PROGRESS - "In Progress" - The work for the activity is in progress.
	- PAUSED - "Paused" - The work for the activity has been paused.
	- COMPLETED - "Completed" - The work for the activity has successfully completed.
	- INVALID - "Invalid" - The activity has not happened because it is not appropriate (for example, created by an automated process as a result of a false positive).
	- IGNORED  - "Ignored" - The activity has not been actioned because it is not important, or another activity has superseded it.
	- FAILED - "Failed" - The process that is performing the work (normally an automated process) failed during start up or execution. 
	 - CANCELLED - "Cancelled" - The activity was cancelled by an external caller.
	 - ABANDONED -  "Abandoned",  The activity was abandoned because it is no longer relevant.  Some work may have occurred but is what stopped, probably in an incomplete state.  
  
Engine actions are retrieved using AssetMaker.findProcesses(body={}).  
The body for this method is as follows:

```
{  
  "class" : "ActivityStatusSearchString",  
  "metadataElementTypeName": ["EngineAction"],  
  "searchString" : value from user,
  "activityStatusList" : [add selected status list here],
  "graphQueryDepth" : 0
}
```
of class "ActivityStatusSearchString"


Given the user's select, display a table of the engine actions returned with the following columns:

- Display Name - properties.displayName - or use qualifiedName if displayName is null
- Request Type - properties.requestType
- Status - properties.actvityStatus
- Process Name - properties.processName
- Start Time - properties.startTime
- Completion Time - properties.completionTime
- Description - properties.description
- Completion Guards - properties.completionGuards - this is list
- Completion Message - properties.completionMessage
- GUID - elementHeader.guid

It should be possible to sort the rows based on any column value
It should also be possible to navigate to the engine action details in The Catalog under Processes
It is also possible to cancel an engine action using AutomatedCuration.cancel_engine_action()

> ### 🔎 Review — Engine Actions
> 💬 ⚠️ This tab is **ecosystem-wide** (`find_processes` takes no server_guid) — it does NOT fit the
>    "each tab has a platform/server dropdown" rule from the intro (line 9). Confirm: drop the
>    platform/server selector here, or is there a reason to scope it? Recommend dropping it.
> 💬 ⚠️ TYPOs: `properties.actvityStatus` → **activityStatus**; method `findProcesses` →
>    **find_processes** (snake_case).
> 💬 Skip the hand-built body — `find_processes` has native params:
>    `find_processes(search_string=…, activity_status_list=[…], metadata_element_subtypes=["EngineAction"],
>    graph_query_depth=0)`. (Spec's body uses `metadataElementTypeName:["EngineAction"]`, but
>    find_processes already scopes to Process and EngineAction is a Process **subtype** → use
>    `metadata_element_subtypes`.) The `ActivityStatusSearchString` body form also works if preferred.
> 💬 UI: multi-select over the 11 statuses (enum fully given — good) + a search string (default `*`).
> 💬 Sortable-by-any-column is a NEW shared capability — build a small reusable sortable-header helper
>    in shared-ui (other tables will want it too). `completionGuards` is a list → render as chips.
> 💬 Cancel = write on `AutomatedCuration.cancel_engine_action(engine_action_guid=elementHeader.guid)`
>    → admin-gate + confirm. Cross-link via `elementHeader.guid` → Catalog Processes (`crossAppNavigate`).








