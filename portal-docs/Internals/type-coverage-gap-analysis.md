# Egeria Portal — Type Coverage Registry

A gap analysis of `PyegeriaWebHandler` (Egeria Explorer, Tech Catalog, Audit, Operations, Lineage Explorer, and everything built since) against the full Egeria v6 open metadata type system — 622 entity, relationship, and classification types across Areas 0–7, extracted fresh from `OpenMetadataType.java` in the local `odpi/egeria` checkout. Ranked for feature prioritization, not exhaustiveness.

Regenerated **2026-08-19**, superseding an earlier snapshot (2026-07-15/16) that had gone stale — several of its "open" gaps have since been built, and this pass's own methodology is a notch cruder than that snapshot's in one respect: see [Method](#method) below before trusting the raw numbers too far.

| | |
|---|---|
| Types in model | 622 |
| Referenced in UI | 281 (45%) |
| Curated gaps tracked | 10 |
| Areas surveyed | 8 |

---

## Method

Every `.py` and `.html` file in `PyegeriaWebHandler` was scanned for exact, whole-word occurrences of each type name from `OpenMetadataType.java`, matched against the four-digit model number embedded in each entry's Wikipage reference to bucket it into an Area (Area = the model number's second digit — `MODEL_0450` → Area 4).

**Weaker than the 2026-07-15 original in one specific way**: that pass was a genuine per-handler manual read — "checked for which Egeria types it actually queries or renders" — and explicitly filtered out internal relationship plumbing, abstract base types, and auto-riding subtypes. This pass is a mechanical whole-word text scan with no such filtering, so a type name mentioned only in a comment or a docstring explaining why something is *out* of scope counts as "present" here, inflating the raw number somewhat. Treat the 281/622 total as an upper bound on real UI coverage, not a precise count — the curated gap list below is the trustworthy part, since each entry there was individually re-verified against the actual handler code, not just text-matched.

One artifact of the earlier report worth flagging for whoever regenerates this next: the original `type-coverage-gap-analysis.html` file, sitting in the same directory being scanned, listed every "missing" type name in its own appendix — scanning it alongside the real handlers made almost everything look "covered." It's excluded from this pass's scan; exclude any future version of this report from itself too.

---

## Curated gaps — re-verified 2026-08-19

### Still open

**01 — Conceptual/logical data models are writable but not viewable.** Dr.Egeria commands can already *create* `ConceptModel`/`ConceptBead`/`DesignPattern`/`DataDictionary`/`DataDescription` — the write path exists. Data Design got a full browse tab for Spec/Structure/Field/Grain/Class; these sibling types didn't. Still true: `ConceptModel`/`ConceptBead` appear only in a one-line comment in `solution_architect_handler.py`, not in any real endpoint.

**02 — Solution component wiring isn't shown as its own topology.** Solution Architect stops at Blueprints → Components → Implementations. `SolutionPort`/`SolutionLinkingWire`/`SolutionComponentPort`/`SolutionComposition` — the actual port/wire connectivity that would let you trace data flow through an architecture — still has zero references anywhere in the handler code.

**03 — Security surface remains partial.** `SecurityTags`/`SecurityGroup`/`SecurityRole`/`SecurityAccessControl` are still not browsable. This is the one piece left of what used to be a single "highest value" gap (see next section) — most of it has since been built.

### Built since the last pass

- **Governance classifications & zones** (was the original's #1 "highest value" gap): now substantially covered — `governance_classifications_handler.py` (bulk classify/declassify for Confidentiality/Criticality/Impact), `governance_zones_handler.py` (zone browsing), `subject_area_handler.py` (SubjectArea hierarchy). Security-specific types (above) are what's left.
- **Business Capability model** (was #7): `business_capability_handler.py` now covers `BusinessCapability`/`BusinessCapabilityDependency`.
- **Glossary term semantic relationships** (was #2): fixed 2026-07-15, still correct — `glossary_handler.py`'s `_group_related_terms()` groups by relationship type instead of collapsing everything into one undifferentiated list.
- **Duplicate resolution review** (was #5): built as a read-only Duplicate Review pane (Egeria Explorer), still wired (`duplicate_review_router`).
- **Social/collaboration layer — Action Center** (was #6): built, still wired (`action_center_router`); scope-extension still pending per the original write-up.
- **Privacy execution detail** (was #8): fixed 2026-07-16 — turned out to need no code change, the Governance Definitions detail view already generically renders relationship keys.
- **Policy enforcement architecture** (was #9): built as a classification-search pane, still wired (`policy_enforcement_router`); scope-extension still pending.
- **Naming-standard vocabulary** (was #10): built as a classification-search pane, still wired (`naming_vocabulary_router`); scope-extension still pending.

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

The mechanical, unfiltered comparison this analysis was built from — every type in each of Egeria's eight model Areas, checked against whether its exact name appears anywhere in a portal handler or its HTML. Includes subtypes, relationships, and internal types the curated list above deliberately excludes. Use this to audit the method, not to re-derive priorities from it (see [Method](#method) above for why the raw percentage overstates real coverage).

### Area 0 — Basic definitions & Infrastructure (61/123)

Missing (62):

`AdjacentLocation`, `AttachedStorage`, `CapabilityAssetUse`, `CatalogTemplate`, `ChangeManagementLibrary`, `CitedDocumentLink`, `CloudPlatform`, `CloudTenant`, `CollectionKind`, `ContentCollectionManager`, `CyberLocation`, `DataAccessManager`, `DataLineageRelationship`, `DataManager`, `EventManager`, `ExternalReferenceLink`, `ExternalSourceCode`, `ExternalStandard`, `FileManager`, `FixedLocation`, `HomeCollection`, `HostClusterMember`, `ITSubsystem`, `InventoryCatalog`, `KnownLocation`, `LabeledRelationship`, `LineageRelationship`, `MediaReference`, `MetadataCohortPeer`, `MetadataRepositoryCohort`, `MobileResource`, `MoreInformation`, `NestedLocation`, `NetworkGatewayLink`, `OperatingPlatformManifest`, `OperatingPlatformUse`, `PropertyFacet`, `RESTAPIManager`, `ReferenceList`, `ReferenceableFacet`, `ResourceList`, `ResourceManager`, `RoledRelationship`, `SampleData`, `SearchKeyword`, `SearchKeywordLink`, `SecureLocation`, `ServerEndpoint`, `SoftwareArchive`, `SoftwareLibrary`, `SoftwarePackageDependency`, `SoftwarePackageManifest`, `SoftwareService`, `SourceControlLibrary`, `SupportedSoftwareCapability`, `TranslationDetail`, `TranslationLink`, `UserAccessDirectory`, `UserAuthenticationManager`, `UserProfileManager`, `VisibleEndpoint`, `WorkingSet`

### Area 1 — Collaboration (41/66)

Missing (25):

`AcceptedAnswer`, `AssociatedSkillSet`, `AttachedNoteLogEntry`, `BlogEntry`, `CommunityMember`, `ContactThrough`, `CrowdSourcingContribution`, `CrowdSourcingContributor`, `Experiment`, `ITInfrastructureProfile`, `ITProfileRole`, `ITProfileRoleAppointment`, `JournalEntry`, `NoteLogAuthor`, `ProfileIdentity`, `ProjectClassification`, `ProjectHierarchy`, `ProjectKind`, `Skill`, `SkillSet`, `TeamLeader`, `TeamMember`, `TeamRole`, `TeamRoleAppointment`, `TeamStructure`

### Area 2 — Assets (30/83)

Missing (53):

`APIEndpoint`, `AnalyticsModelRun`, `ArchiveContents`, `ArchiveFile`, `AssetConnection`, `AssociatedLog`, `AudioFile`, `AvroFile`, `BuildInstructionFile`, `CohortRegistryStore`, `ConnectToEndpoint`, `ConnectionConnectorType`, `DataAssetEncoding`, `DataScope`, `DataSetContent`, `DeployedAnalyticsModel`, `EmbeddedConnection`, `EmbeddedProcess`, `ExecutableFile`, `FolderHierarchy`, `Form`, `FunctionCall`, `JSONFile`, `KeyStoreFile`, `LinkedFile`, `LinkedMedia`, `ListenerInterface`, `LogFile`, `MetadataCollection`, `MetadataRepository`, `NestedFile`, `ParquetFile`, `ProcessHierarchy`, `PropertiesFile`, `PublisherInterface`, `RasterFile`, `ReferenceCodeMappingTable`, `ReportDependency`, `ReportOriginator`, `ReportSubject`, `ReportType`, `RequestResponseInterface`, `ScriptFile`, `SecretsCollection`, `SourceCodeFile`, `StoredOn`, `ThreeDImageFile`, `TransientEmbeddedProcess`, `UserAccountProfile`, `VectorFile`, `VideoFile`, `XMLFile`, `YAMLFile`

### Area 3 — Glossary (11/24)

Missing (13):

`AbstractConcept`, `ActivityDescription`, `CanonicalVocabulary`, `ContextDefinition`, `DataValueMeaning`, `EditingCollection`, `ElementSupplement`, `ScopingCollection`, `SemanticDefinition`, `StagingCollection`, `SupplementaryProperties`, `Taxonomy`, `UsedInContext`

### Area 4 — Governance (74/146)

Missing (72):

`ApprovedPurpose`, `AssetOwner`, `AssociatedSecurityList`, `AuditLog`, `BusinessOwner`, `ComponentOwner`, `ConnectorActivityReport`, `ContextEventCollection`, `ContextEventEvidence`, `ContextEventForTimelineEffects`, `ContextEventImpact`, `ControlPoint`, `DataItemOwner`, `DataProcessingAction`, `DataProcessingSpecification`, `DataProcessingTarget`, `DependentContextEvent`, `DetailedProcessingAction`, `EnforcementPoint`, `ExceptionBacklog`, `ExecutionPoint`, `ExplorerActionEngine`, `ExplorerActionService`, `GovernanceAction`, `GovernanceActionEngine`, `GovernanceActionExecutor`, `GovernanceActionProcessFlow`, `GovernanceActionProcessStep`, `GovernanceActionService`, `GovernanceControlLink`, `GovernanceDriverLink`, `GovernanceExpectations`, `GovernanceMeasurements`, `GovernanceMechanism`, `GovernancePolicyLink`, `GovernanceProject`, `GovernanceRepresentative`, `GovernanceResponse`, `GovernedBy`, `ImpactedResource`, `LineageLog`, `LocationOwner`, `LogAnalysis`, `MeteringLog`, `MonitoredResource`, `NamingStandardRuleSet`, `NextGovernanceActionProcessStep`, `NotificationSubscriber`, `PermittedProcessing`, `RegisteredIntegrationConnector`, `RegulationCertificationType`, `Regulator`, `RelatedContextEvent`, `RepositoryGovernanceEngine`, `RepositoryGovernanceService`, `ResourcePermissions`, `SecretsCollectionSecurityList`, `SecurityList`, `SecurityListMembership`, `SecurityLog`, `SecurityRole`, `SolutionOwner`, `SubjectAreaOwner`, `SupportedGovernanceService`, `SurveyActionEngine`, `SurveyActionService`, `TargetForGovernanceAction`, `VerificationPoint`, `WatchdogActionEngine`, `WatchdogActionService`, `ZoneHierarchy`, `ZoneMembershipProfile`

### Area 5 — Schemas (36/114)

Missing (78):

`APIHeader`, `APIOperations`, `APIParameterList`, `APIRequest`, `APIResponse`, `CalculatedValue`, `ComplexSchemaType`, `ConceptBeadAttribute`, `ConceptBeadAttributeLink`, `ConceptBeadExtension`, `ConceptBeadRelationship`, `ConceptBeadRelationshipEnd`, `ConceptDesign`, `ConceptModel`, `ConceptModelElement`, `ConsistentValidValues`, `DataClassComposition`, `DataDescription`, `DataStructureDefinition`, `DataValueAssignment`, `DataValueDefinition`, `DataValueHierarchy`, `DerivedSchemaTypeQueryTarget`, `DesignModel`, `DesignModelElement`, `DesignPattern`, `DisplayDataContainer`, `DisplayDataField`, `DisplayDataSchemaType`, `DocumentSchemaAttribute`, `DocumentSchemaType`, `EnumSchemaType`, `EventTypeList`, `ExternalSchemaType`, `ForeignKey`, `GraphEdge`, `GraphEdgeLink`, `GraphSchemaType`, `GraphVertex`, `ImplementationSnippet`, `InstanceMetadata`, `IsAConceptBead`, `LinkedDataField`, `LinkedExternalSchemaType`, `LiteralSchemaType`, `MapSchemaType`, `MemberDataField`, `MetamodelInstance`, `NestedDataField`, `NestedDesignPattern`, `ObjectAttribute`, `ObjectSchemaType`, `PrimaryKey`, `PrimitiveSchemaType`, `QueryDataContainer`, `QueryDataField`, `QuerySchemaType`, `ReferenceData`, `ReferenceValueAssignment`, `RelatedDesignPattern`, `RelationalTableType`, `RootSchemaType`, `SchemaAttributeDefinition`, `SchemaTypeChoice`, `SchemaTypeDefinition`, `SchemaTypeOption`, `SimpleSchemaType`, `SpecializedDesignPattern`, `SpecificationPropertyAssignment`, `StructSchemaType`, `TabularFileColumn`, `TypeEmbeddedAttribute`, `TypedByConceptBead`, `ValidValueAssociation`, `ValidValueMember`, `ValidValuesAssignment`, `ValidValuesImplementation`, `ValidValuesMapping`

### Area 6 — Metadata Surveys (8/22)

Missing (14):

`AnnotationExtension`, `AnnotationMatch`, `AnnotationReview`, `AssociatedAnnotation`, `DataClassAnnotation`, `DataGrainAnnotation`, `FingerprintAnnotation`, `RelationshipAdviceAnnotation`, `ReportedAnnotation`, `RequestForActionTarget`, `ResourcePhysicalStatusAnnotation`, `ResourceProfileData`, `ResourceProfileLogAnnotation`, `SemanticAnnotation`

### Area 7 — Lineage & Usage (20/44)

Missing (24):

`AccountingCodes`, `AgreementActor`, `AgreementItem`, `BusinessSignificant`, `ContractLink`, `DataSharingHub`, `DataSharingRequest`, `DigitalProductDependency`, `DigitalProductManager`, `DigitalResourceOrigin`, `DigitalSubscriber`, `DigitalSupport`, `ImplementationResource`, `Incomplete`, `InformationSupplyChainLink`, `ProcessCall`, `SolutionComponentActor`, `SolutionComponentPort`, `SolutionComposition`, `SolutionDesign`, `SolutionLinkingWire`, `SolutionPortDelegation`, `UltimateDestination`, `UltimateSource`

---

Source: `~/localGit/egeria-v6/egeria-workspaces-fs` (`compose-configs/egeria-quickstart/PyegeriaWebHandler`) against `OpenMetadataType.java`, local `odpi/egeria` checkout. Coverage counts are name-presence checks, not a claim about relationship-level completeness within covered types — see [Method](#method).
