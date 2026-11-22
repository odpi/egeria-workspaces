# Egeria Portal — Type Coverage Registry

A gap analysis of `PyegeriaWebHandler` (Egeria Explorer, Tech Catalog, Audit, Operations, Lineage Explorer, and everything built since) against the full Egeria v6 open metadata type system — 671 entity, relationship, and classification types across Areas 0–7, extracted from `OpenMetadataType.java` in the local `odpi/egeria` checkout at commit `90232870b2` (the merge of odpi/egeria#9463, the Egeria 6.4 additions). Ranked for feature prioritization, not exhaustiveness.

Regenerated **2026-11-21**, with the Egeria 6.4 Explorer cards (branches E64 C1–C3), superseding the 2026-08-19 pass. Read [Method](#method) before trusting the raw numbers too far.

| | |
|---|---|
| Types in model | 671 |
| Referenced in UI | 364 (54%) |
| Curated gaps tracked | 3 open (all partly built), 9 built since |
| Areas surveyed | 8 |

---

## Method

Every `.py` and `.html` file in `compose-configs/egeria-quickstart/PyegeriaWebHandler` was scanned for exact, whole-word occurrences of each type name from `OpenMetadataType.java`, and each type was put in an Area by the four-digit model number in its Wikipage reference (Area = the model number's second digit — `MODEL_0450` → Area 4). `OpenMetadataType.java` was read with `git show 90232870b2:…`, so the Egeria checkout's working tree (still on `8de9572c4d`) was not touched.

**Why the numbers moved since 2026-08-19 (622 types, 281 referenced):** most of it is Egeria's type model growing, not the Portal.
- 622 → 653 types between the 2026-08-19 checkout and `8de9572c4d` (laz's build until 2026-11-21): Egeria 6.3's report-spec, measurement and dashboard types and others.
- 653 → 671 with `90232870b2`: 18 more. 11 are #9463's Egeria 6.4 additions (`Decision`, `Outcome`, `Assessment`, `ProjectTarget`, `DataValue`, `LiteralDataValue`, `DataValueSource`, `ProcessingVariable`, `EmbeddedDataValue`, `Branch`, `SupportedVariableType`); 7 came in on Egeria main before it (`AsOfDataField`, `BasisDataField`, `MeasurementSpecification`, `ReportRunOf`, `ReportSpec`, `ReportTypeInstance`, `Dashboard`).
- Referenced, on upstream/main before the 6.4 cards: 355. With them: 364. The 6.4 cards add 9 names. `Decision` and `Outcome` were already "present" before (as ordinary words in other handlers), which is exactly the kind of over-count described next.

**A text scan, not a per-handler read.** The original 2026-07-15 pass read each handler and filtered out internal relationship plumbing, abstract base types and auto-riding subtypes. This pass, like 2026-08-19's, is a mechanical whole-word scan: a type name in a comment or a docstring counts as "present". Treat 364/671 as an upper bound on real UI coverage, not a count. The curated list below is the trustworthy part: each entry was re-checked against the handler code.

**The self-scan trap:** an old `type-coverage-gap-analysis.html` still sits in `PyegeriaWebHandler` and lists every missing type name. It is excluded from the scan (any file named `type-coverage-gap-analysis*`); exclude any future copy too.

---

## Curated gaps — re-verified 2026-11-21

### Still open

**01 — Conceptual/logical data models are writable but not viewable.** Dr.Egeria can *create* `ConceptModel`/`ConceptBead`/`DesignPattern`/`DataDictionary`/`DataDescription`, but nothing browses them. Unchanged: `ConceptModel` has no reference in the handlers, and `ConceptBead` appears only in a comment in `solution_architect_handler.py`.

**02 — Solution ports still aren't shown; wiring now is.** Partly built since the last pass: `solution_architect_handler.py` now reads `SolutionLinkingWire` (a component's `wiredTo`/`wiredFrom`) and `SolutionComposition` (one relationships call per blueprint load). What's left: `SolutionPort`/`SolutionComponentPort`/`SolutionPortDelegation`, so data flow through a component's ports can't be traced. `SolutionPort` is named only in `type_system_handler.py`'s area table and a comment.

**03 — Security surface remains partial.** Partly built: `SecurityTags` is a Resource Browser badge and one of the classifications `governance_classifications_handler.py` lists, and `SecurityAccessControl` is shown as a governance definition type (`governance_definitions_handler.py`). Still not browsable: `SecurityGroup`, `SecurityRole`, `SecurityList`/`SecurityListMembership`.

### Built since the last pass

- **Egeria 6.4 process variables and decisions** (new types, odpi/egeria#9463; branches E64 C1–C3, `e64_handler.py`, `e64_router`):
  - a **Decisions** section (`/api/decisions`): disposition, importance and status; summary, scope, usage, implications and notes; review and expiry dates flagged against now; assessed inputs, one row per `Assessment` relationship; `Outcome`s;
  - a **Data Values** section (`/api/data-values`) for `DataValue` and `LiteralDataValue`: format and type, the value (literal, list or map), used by (`ProcessingVariable`, with position), stored in (`DataValueSource`), embedded values (`EmbeddedDataValue`) by position, part of;
  - the 6.4 rows on 23 Explorer cards and The Catalog's 3 detail cards (`/api/e64/elements/{guid}/related`): decisions, worked on by projects, project targets (`ProjectTarget`), processing variables, variable types (`SupportedVariableType`), data values provided, and a `Branch` badge.
  - On an Egeria before 6.4 each says "needs Egeria 6.4" in words, never an error or "none".
- **Governance classifications & zones** (the original's #1): `governance_classifications_handler.py`, `governance_zones_handler.py`, `subject_area_handler.py`; all still wired. The security-specific types are gap 03.
- **Business Capability model** (was #7): `business_capability_handler.py`, still wired.
- **Glossary term semantic relationships** (was #2): `glossary_handler.py`'s `_group_related_terms()` groups by relationship type.
- **Duplicate resolution review** (was #5): Duplicate Review pane, `duplicate_review_router`, still wired.
- **Action Center** (was #6): `action_center_router`, still wired; scope-extension still pending.
- **Privacy execution detail** (was #8): the Governance Definitions detail view renders the relationship keys generically; no code needed.
- **Policy enforcement architecture** (was #9): `policy_enforcement_router`, still wired; scope-extension still pending.
- **Naming-standard vocabulary** (was #10): `naming_vocabulary_router`, still wired; scope-extension still pending.

---

## Already covered — for calibration

Things that look like gaps in a raw name diff but aren't:

| Type surface | Where it actually lives |
|---|---|
| Physical schema | Per-asset in Tech Catalog's schema tree, not a standalone tab — `/api/tech-catalog/assets/{guid}/schema` |
| Governance drivers / policies / controls | Full three-panel tree in Governance Definitions |
| Digital products & agreements | Catalog hierarchy, subscriptions, contracts all browsable |
| Engines & engine actions | Egeria Operations page — Governance Engines, Engine Actions tabs |
| Exceptions, certifications, licenses | Egeria Audit page, zone-access-filtered per viewer |
| Data Initialization batches | Admin panel — see [Data Initialization](../tools/data-initialization.md) |

---

## Raw type diff, by Area

The mechanical, unfiltered comparison this analysis was built from: every type in each of Egeria's eight model Areas, checked against whether its exact name appears anywhere in a portal handler or its HTML. Includes subtypes, relationships, and internal types the curated list above deliberately excludes. Use this to audit the method, not to re-derive priorities from it (see [Method](#method)).

### Area 0 — Basic definitions & Infrastructure (68/127)

Missing (59):

`AdjacentLocation`, `AnalyticsEngine`, `AttachedStorage`, `AuthorizationManager`, `ChangeManagementLibrary`, `CitedDocumentLink`, `CloudPlatform`, `CloudTenant`, `CohortMember`, `ContentCollectionManager`, `CyberLocation`, `DataAccessManager`, `DataManager`, `DataVirtualizationEngine`, `EventManager`, `ExternalSourceCode`, `ExternalStandard`, `FileManager`, `FixedLocation`, `HomeCollection`, `HostClusterMember`, `ITSubsystem`, `InventoryCatalog`, `KnownLocation`, `MasterDataManager`, `MediaReference`, `MetadataCohortPeer`, `MetadataRepositoryCohort`, `MobileResource`, `NestedLocation`, `NetworkGateway`, `NetworkGatewayLink`, `NotificationManager`, `OperatingPlatform`, `OperatingPlatformManifest`, `OperatingPlatformUse`, `PropertyFacet`, `RESTAPIManager`, `ReferenceList`, `ReferenceableFacet`, `ReportingEngine`, `RoledRelationship`, `SampleData`, `SecureLocation`, `ServerEndpoint`, `SoftwareArchive`, `SoftwareLibrary`, `SoftwarePackageDependency`, `SoftwarePackageManifest`, `SoftwareServerPlatform`, `SoftwareService`, `SupportedSoftwareCapability`, `TranslationDetail`, `TranslationLink`, `UserAccessDirectory`, `UserAuthenticationManager`, `UserProfileManager`, `VisibleEndpoint`, `WorkflowEngine`

### Area 1 — Collaboration (49/68)

Missing (19):

`AcceptedAnswer`, `AssociatedSkillSet`, `AttachedNoteLogEntry`, `BlogEntry`, `CommunityMember`, `ContactThrough`, `CrowdSourcingContribution`, `CrowdSourcingContributor`, `Experiment`, `ITInfrastructureProfile`, `ITProfileRole`, `ITProfileRoleAppointment`, `Investigation`, `NoteLogAuthor`, `ProjectClassification`, `ProjectHierarchy`, `TeamRole`, `TeamRoleAppointment`, `TeamStructure`

### Area 2 — Assets (46/99)

Missing (53):

`AnalyticsModelRun`, `ArchiveContents`, `ArchiveFile`, `AssetConnection`, `AssociatedLog`, `AudioFile`, `AvroFile`, `BuildInstructionFile`, `CohortRegistryStore`, `ConnectToEndpoint`, `ConnectionConnectorType`, `DataAssetEncoding`, `DependentSoftwareComponent`, `DeployedAnalyticsModel`, `DocumentStore`, `EmbeddedConnection`, `ExecutableFile`, `Form`, `FunctionCall`, `GeneratedTarget`, `GraphStore`, `InformationView`, `JSONFile`, `LinkedFile`, `LinkedMedia`, `ListenerInterface`, `LogFile`, `MediaCollection`, `MediaFile`, `MetadataRepository`, `ParquetFile`, `ProcessHierarchy`, `PropertiesFile`, `PublisherInterface`, `RasterFile`, `ReferenceCodeMappingTable`, `ReportDependency`, `ReportOriginator`, `RequestResponseInterface`, `ReusableTechnique`, `ReusableTechniqueUse`, `RunMetrics`, `ScriptFile`, `SoftwareModule`, `SoftwareSource`, `SourceCodeFile`, `StoredOn`, `ThreeDImageFile`, `UserAccountProfile`, `VectorFile`, `VideoFile`, `XMLFile`, `YAMLFile`

### Area 3 — Glossary (11/24)

Missing (13):

`AbstractConcept`, `ActivityDescription`, `CanonicalVocabulary`, `ContextDefinition`, `DataValueMeaning`, `EditingCollection`, `ElementSupplement`, `ScopingCollection`, `SemanticDefinition`, `StagingCollection`, `SupplementaryProperties`, `Taxonomy`, `UsedInContext`

### Area 4 — Governance (93/157)

Missing (64):

`ApprovedPurpose`, `AssetOwner`, `AssociatedSecurityList`, `AuditLog`, `BusinessOwner`, `ComponentOwner`, `ContextEventEvidence`, `ContextEventForTimelineEffects`, `ContextEventImpact`, `ControlPoint`, `DataItemOwner`, `DataProcessingSpecification`, `DataProcessingTarget`, `DataQualityRule`, `DeletingActionProcess`, `DependentContextEvent`, `DetailedProcessingAction`, `EnforcementPoint`, `ExceptionBacklog`, `ExplorerActionEngine`, `ExplorerActionService`, `GovernanceAction`, `GovernanceActionEngine`, `GovernanceActionExecutor`, `GovernanceActionService`, `GovernanceControlLink`, `GovernanceDriverLink`, `GovernanceExpectations`, `GovernanceMeasurements`, `GovernanceMechanism`, `GovernancePolicyLink`, `GovernanceRepresentative`, `GovernanceResponse`, `ImpactedResource`, `LineageLog`, `LocationOwner`, `LogAnalysis`, `MeteringLog`, `NamingStandardsVocabulary`, `NotificationSubscriber`, `PermittedProcessing`, `RegisteredIntegrationConnector`, `RegulationCertificationType`, `Regulator`, `RelatedContextEvent`, `RepositoryGovernanceEngine`, `RepositoryGovernanceService`, `ResourcePermissions`, `SecretsCollectionSecurityList`, `SecurityGroup`, `SecurityListMembership`, `SecurityLog`, `SecurityRole`, `SolutionOwner`, `SubjectAreaOwner`, `SubscribingActionProcess`, `SupportedGovernanceService`, `SurveyActionEngine`, `SurveyActionService`, `VerificationPoint`, `WatchdogActionEngine`, `WatchdogActionService`, `ZoneHierarchy`, `ZoneMembershipProfile`

### Area 5 — Schemas (55/121)

Missing (66):

`APIHeader`, `APIParameterList`, `APIRequest`, `APIResponse`, `AsOfDataField`, `BasisDataField`, `CalculatedValue`, `ComplexSchemaType`, `ConceptBeadAttribute`, `ConceptBeadAttributeLink`, `ConceptBeadExtension`, `ConceptBeadRelationship`, `ConceptBeadRelationshipEnd`, `ConceptDesign`, `ConceptModel`, `ConceptModelElement`, `ConsistentValidValues`, `DataClassComposition`, `DataStructureDefinition`, `DataValueAssignment`, `DataValueDefinition`, `DataValueHierarchy`, `DisplayDataSchemaType`, `DocumentSchemaAttribute`, `DocumentSchemaType`, `EnumSchemaType`, `EventTypeList`, `ExternalSchemaType`, `GraphEdge`, `GraphEdgeLink`, `GraphSchemaType`, `GraphVertex`, `InstanceMetadata`, `IsAConceptBead`, `LinkedDataField`, `LinkedExternalSchemaType`, `LiteralSchemaType`, `MapSchemaType`, `MeasurementSpecification`, `MetamodelInstance`, `NestedDataField`, `ObjectAttribute`, `ObjectSchemaType`, `PrimitiveSchemaType`, `QueryDataContainer`, `QueryDataField`, `QuerySchemaType`, `ReferenceData`, `ReferenceValueAssignment`, `RelationalTableType`, `ReportType`, `ReportTypeInstance`, `RootSchemaType`, `SchemaAttributeDefinition`, `SchemaTypeChoice`, `SimpleSchemaType`, `SpecificationPropertyAssignment`, `StructSchemaType`, `TabularFileColumn`, `TypeEmbeddedAttribute`, `TypedByConceptBead`, `ValidValueAssociation`, `ValidValueMember`, `ValidValuesAssignment`, `ValidValuesImplementation`, `ValidValuesMapping`

### Area 6 — Metadata Surveys (12/28)

Missing (16):

`AnnotationExtension`, `AnnotationMatch`, `CodeAnalysisAnnotation`, `ContributorAnalysisAnnotation`, `DataClassAnnotation`, `DataGrainAnnotation`, `FingerprintAnnotation`, `PenetrationTestFindingAnnotation`, `RelationshipAdviceAnnotation`, `ResourcePhysicalStatusAnnotation`, `ResourceProfileData`, `ResourceProfileLogAnnotation`, `SecurityFindingAnnotation`, `SecurityPostureAnnotation`, `SemanticAnnotation`, `VulnerabilityAnnotation`

### Area 7 — Lineage & Usage (30/47)

Missing (17):

`AccountingCodes`, `AgreementActor`, `AgreementItem`, `BusinessSignificant`, `ContractLink`, `DigitalResourceOrigin`, `DigitalSubscriber`, `DigitalSupport`, `ImplementationResource`, `Incomplete`, `InformationSupplyChainLink`, `ReportRunOf`, `SolutionComponentActor`, `SolutionComponentPort`, `SolutionDesign`, `SolutionPortDelegation`, `UsageActivity`

---

Source: `compose-configs/egeria-quickstart/PyegeriaWebHandler` (branch `claude/e64-c3-reverse-rows`) against `OpenMetadataType.java` at odpi/egeria `90232870b2`. Coverage counts are name-presence checks, not a claim about relationship-level completeness within covered types — see [Method](#method).
