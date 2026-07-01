import json
import time

# This file recreates the CocoTypesArchive.omarchive file to illustrate how to create different categories of open metadata types.

# --- Archive Properties ---
ARCHIVE_GUID = "50874908-01f1-47e2-83ea-e571109a946e"
ARCHIVE_NAME = "CocoTypes"
ARCHIVE_DESCRIPTION = "Specialized types for Coco Pharmaceuticals."
ARCHIVE_TYPE = "CONTENT_PACK"
ORIGINATOR_NAME = "Egeria Project"
ORIGINATOR_LICENSE = "Apache 2.0"
CREATION_DATE = 1639984840038
DEPENDS_ON_ARCHIVES = ["bce3b0a0-662a-4f87-b8dc-844078a11a6e"]

# --- EnumDef: BiopsyScope ---
ENUM_BIOPSY_SCOPE_NAME = "BiopsyScope"
ENUM_BIOPSY_SCOPE_GUID = "fdb05618-d0fe-4725-946f-138ba74f6f43"
ENUM_BIOPSY_SCOPE_DESC = "Defines scope of the tissue removal for a biopsy."
ENUM_BIOPSY_SCOPE_VERSION = 1781289565819
ENUM_BIOPSY_SCOPE_VERSION_NAME = "1.0"

ENUM_BIOPSY_SCOPE_ELEMENTS = [
    {"ordinal": 0, "value": "Unclassified", "description": "There is no information on the scope of the biopsy."},
    {"ordinal": 1, "value": "Excisional", "description": "The biopsy removed all of the suspicious tissue."},
    {"ordinal": 2, "value": "Incisional", "description": "The biopsy took a sample of the tissue under examination."},
    {"ordinal": 99, "value": "Other", "description": "Another biopsy scope."}
]

# --- EntityDef: BiopsyReport ---
ENTITY_BIOPSY_REPORT_NAME = "BiopsyReport"
ENTITY_BIOPSY_REPORT_GUID = "78479770-79ae-4bd8-b0ec-bf5e60c01e66"
ENTITY_BIOPSY_REPORT_DESC = "Results from a patient biopsy."
ENTITY_BIOPSY_REPORT_VERSION = 1781289565819
ENTITY_BIOPSY_REPORT_VERSION_NAME = "1.0"
ENTITY_BIOPSY_REPORT_SUPER_TYPE_NAME = "Document"
ENTITY_BIOPSY_REPORT_SUPER_TYPE_GUID = "b463827c-c0a0-4cfb-a2b2-ddc63746ded4"

# BiopsyReport Attributes
ATTR_BIOPSY_SCOPE_NAME = "biopsyScope"
ATTR_BIOPSY_SCOPE_DESC = "Is this biopsy excisional (targeted removal) or incisional (sample taken)."
ATTR_BIOPSY_TECHNIQUE_NAME = "biopsyTechniqueType"
ATTR_BIOPSY_TECHNIQUE_DESC = "How was the biopsy taken?"

# --- ClassificationDef: ReviewedByClinicalTrials ---
CLASS_REVIEWED_NAME = "ReviewedByClinicalTrials"
CLASS_REVIEWED_GUID = "c2fa7555-f366-4869-88f3-897d6f2ec5a4"
CLASS_REVIEWED_DESC = "Declares that a report or data set has been assessed by the clinical trials team."
CLASS_REVIEWED_VERSION = 1781289565819
CLASS_REVIEWED_VERSION_NAME = "1.0"

# ReviewedByClinicalTrials Attributes
ATTR_REVIEWER_NAME = "reviewer"
ATTR_REVIEWER_DESC = "Person responsible for maintaining this relationship."
ATTR_REVIEWER_TYPE_NAME = "reviewerTypeName"
ATTR_REVIEWER_TYPE_DESC = "Type of element used to identify the reviewer."
ATTR_REVIEWER_PROP_NAME = "reviewerPropertyName"
ATTR_REVIEWER_PROP_DESC = "Name of property used to identify the reviewer."
ATTR_REVIEW_NOTES_NAME = "notes"
ATTR_REVIEW_NOTES_DESC = "Information for the clinical trials team relating to the review."

# --- RelationshipDef: BiopsySupportingEvidence ---
REL_BIOPSY_EVIDENCE_NAME = "BiopsySupportingEvidence"
REL_BIOPSY_EVIDENCE_GUID = "54300f97-0140-4adb-b9a9-308514694f8d"
REL_BIOPSY_EVIDENCE_DESC = "Link between a biopsy report and other data sources."
REL_BIOPSY_EVIDENCE_VERSION = 1781289565819
REL_BIOPSY_EVIDENCE_VERSION_NAME = "1.0"

# Relationship Attributes
ATTR_REL_NOTES_NAME = "notes"
ATTR_REL_NOTES_DESC = "Information for the clinical trials team relating to the evidence."

# Relationship Ends
REL_END1_ENTITY_TYPE = "BiopsyReport"
REL_END1_ENTITY_GUID = "78479770-79ae-4bd8-b0ec-bf5e60c01e66"
REL_END1_ATTR_NAME = "report"
REL_END1_ATTR_DESC = "Report that the evidence is being linked to."

REL_END2_ENTITY_TYPE = "Referenceable"
REL_END2_ENTITY_GUID = "a32316b8-dc8c-48c5-b12b-71c1b2a080bf"
REL_END2_ATTR_NAME = "evidence"
REL_END2_ATTR_DESC = "Further information to support the report."

# --- Primitive and Collection Types (Constant for this archive) ---
STRING_TYPE_GUID = "b34a64b9-554a-42b1-8f8a-7d5c2339f9c4"
MAP_STRING_STRING_GUID = "005c7c14-ac84-4136-beed-959401b041f8"
MAP_STRING_STRING_DESC_GUID = "f285d0ca-50ab-4564-b129-c7e3ba4e8545"

def create_archive():
    # Constructing EnumDef
    biopsy_scope_elements = [
        {
            "headerVersion": 1,
            "ordinal": el["ordinal"],
            "value": el["value"],
            "description": el["description"]
        } for el in ENUM_BIOPSY_SCOPE_ELEMENTS
    ]
    
    biopsy_scope_enum = {
        "@class": "EnumDef",
        "headerVersion": 1,
        "version": ENUM_BIOPSY_SCOPE_VERSION,
        "versionName": ENUM_BIOPSY_SCOPE_VERSION_NAME,
        "category": "ENUM_DEF",
        "guid": ENUM_BIOPSY_SCOPE_GUID,
        "name": ENUM_BIOPSY_SCOPE_NAME,
        "description": ENUM_BIOPSY_SCOPE_DESC,
        "elementDefs": biopsy_scope_elements,
        "defaultValue": biopsy_scope_elements[0]
    }

    # Constructing EntityDef
    biopsy_report_entity = {
        "@class": "EntityDef",
        "headerVersion": 1,
        "guid": ENTITY_BIOPSY_REPORT_GUID,
        "name": ENTITY_BIOPSY_REPORT_NAME,
        "status": "ACTIVE_TYPEDEF",
        "version": ENTITY_BIOPSY_REPORT_VERSION,
        "versionName": ENTITY_BIOPSY_REPORT_VERSION_NAME,
        "category": "ENTITY_DEF",
        "superType": {
            "headerVersion": 1,
            "guid": ENTITY_BIOPSY_REPORT_SUPER_TYPE_GUID,
            "name": ENTITY_BIOPSY_REPORT_SUPER_TYPE_NAME,
            "status": "ACTIVE_TYPEDEF"
        },
        "description": ENTITY_BIOPSY_REPORT_DESC,
        "origin": ARCHIVE_GUID,
        "createdBy": ORIGINATOR_NAME,
        "createTime": CREATION_DATE,
        "validInstanceStatusList": ["ACTIVE", "DELETED"],
        "initialStatus": "ACTIVE",
        "propertiesDefinition": [
            {
                "headerVersion": 1,
                "attributeName": ATTR_BIOPSY_SCOPE_NAME,
                "attributeType": biopsy_scope_enum,
                "attributeStatus": "ACTIVE_ATTRIBUTE",
                "attributeDescription": ATTR_BIOPSY_SCOPE_DESC,
                "valuesMinCount": 0,
                "valuesMaxCount": 1,
                "attributeCardinality": "AT_MOST_ONE",
                "indexable": True,
                "unique": False
            },
            {
                "headerVersion": 1,
                "attributeName": ATTR_BIOPSY_TECHNIQUE_NAME,
                "attributeType": {
                    "class": "PrimitiveDef",
                    "headerVersion": 1,
                    "version": 1,
                    "versionName": "6.1-SNAPSHOT",
                    "category": "PRIMITIVE",
                    "guid": STRING_TYPE_GUID,
                    "name": "string",
                    "primitiveDefCategory": "OM_PRIMITIVE_TYPE_STRING"
                },
                "attributeStatus": "ACTIVE_ATTRIBUTE",
                "attributeDescription": ATTR_BIOPSY_TECHNIQUE_DESC,
                "valuesMinCount": 0,
                "valuesMaxCount": 1,
                "attributeCardinality": "AT_MOST_ONE",
                "indexable": True,
                "unique": False
            }
        ]
    }

    # Constructing ClassificationDef
    reviewed_classification = {
        "@class": "ClassificationDef",
        "headerVersion": 1,
        "guid": CLASS_REVIEWED_GUID,
        "name": CLASS_REVIEWED_NAME,
        "status": "ACTIVE_TYPEDEF",
        "version": CLASS_REVIEWED_VERSION,
        "versionName": CLASS_REVIEWED_VERSION_NAME,
        "category": "CLASSIFICATION_DEF",
        "description": CLASS_REVIEWED_DESC,
        "origin": ARCHIVE_GUID,
        "createdBy": ORIGINATOR_NAME,
        "createTime": CREATION_DATE,
        "validInstanceStatusList": ["ACTIVE", "DELETED"],
        "initialStatus": "ACTIVE",
        "propertiesDefinition": [
            {
                "headerVersion": 1,
                "attributeName": ATTR_REVIEWER_NAME,
                "attributeType": {
                    "class": "PrimitiveDef",
                    "headerVersion": 1,
                    "version": 1,
                    "versionName": "6.1-SNAPSHOT",
                    "category": "PRIMITIVE",
                    "guid": STRING_TYPE_GUID,
                    "name": "string",
                    "primitiveDefCategory": "OM_PRIMITIVE_TYPE_STRING"
                },
                "attributeStatus": "ACTIVE_ATTRIBUTE",
                "attributeDescription": ATTR_REVIEWER_DESC,
                "valuesMinCount": 0,
                "valuesMaxCount": 1,
                "attributeCardinality": "AT_MOST_ONE",
                "indexable": True,
                "unique": False
            },
            {
                "headerVersion": 1,
                "attributeName": ATTR_REVIEWER_TYPE_NAME,
                "attributeType": {
                    "class": "PrimitiveDef",
                    "headerVersion": 1,
                    "version": 1,
                    "versionName": "6.1-SNAPSHOT",
                    "category": "PRIMITIVE",
                    "guid": STRING_TYPE_GUID,
                    "name": "string",
                    "primitiveDefCategory": "OM_PRIMITIVE_TYPE_STRING"
                },
                "attributeStatus": "ACTIVE_ATTRIBUTE",
                "attributeDescription": ATTR_REVIEWER_TYPE_DESC,
                "valuesMinCount": 0,
                "valuesMaxCount": 1,
                "attributeCardinality": "AT_MOST_ONE",
                "indexable": True,
                "unique": False
            },
            {
                "headerVersion": 1,
                "attributeName": ATTR_REVIEWER_PROP_NAME,
                "attributeType": {
                    "class": "PrimitiveDef",
                    "headerVersion": 1,
                    "version": 1,
                    "versionName": "6.1-SNAPSHOT",
                    "category": "PRIMITIVE",
                    "guid": STRING_TYPE_GUID,
                    "name": "string",
                    "primitiveDefCategory": "OM_PRIMITIVE_TYPE_STRING"
                },
                "attributeStatus": "ACTIVE_ATTRIBUTE",
                "attributeDescription": ATTR_REVIEWER_PROP_DESC,
                "valuesMinCount": 0,
                "valuesMaxCount": 1,
                "attributeCardinality": "AT_MOST_ONE",
                "indexable": True,
                "unique": False
            },
            {
                "headerVersion": 1,
                "attributeName": ATTR_REVIEW_NOTES_NAME,
                "attributeType": {
                    "class": "CollectionDef",
                    "headerVersion": 1,
                    "version": 1,
                    "versionName": "6.1-SNAPSHOT",
                    "category": "COLLECTION",
                    "guid": MAP_STRING_STRING_GUID,
                    "name": "map<string,string>",
                    "description": "A map from string to string.",
                    "descriptionGUID": MAP_STRING_STRING_DESC_GUID,
                    "collectionDefCategory": "OM_COLLECTION_MAP",
                    "argumentCount": 2,
                    "argumentTypes": ["OM_PRIMITIVE_TYPE_STRING", "OM_PRIMITIVE_TYPE_STRING"]
                },
                "attributeStatus": "ACTIVE_ATTRIBUTE",
                "attributeDescription": ATTR_REVIEW_NOTES_DESC,
                "valuesMinCount": 0,
                "valuesMaxCount": 1,
                "attributeCardinality": "AT_MOST_ONE",
                "indexable": True,
                "unique": False
            }
        ],
        "validEntityDefs": [
            {
                "headerVersion": 1,
                "guid": "896d14c2-7522-4f6c-8519-757711943fe6",
                "name": "Asset",
                "status": "ACTIVE_TYPEDEF"
            }
        ],
        "propagatable": False
    }

    # Constructing RelationshipDef
    biopsy_evidence_relationship = {
        "@class": "RelationshipDef",
        "headerVersion": 1,
        "guid": REL_BIOPSY_EVIDENCE_GUID,
        "name": REL_BIOPSY_EVIDENCE_NAME,
        "status": "ACTIVE_TYPEDEF",
        "version": REL_BIOPSY_EVIDENCE_VERSION,
        "versionName": REL_BIOPSY_EVIDENCE_VERSION_NAME,
        "category": "RELATIONSHIP_DEF",
        "description": REL_BIOPSY_EVIDENCE_DESC,
        "origin": ARCHIVE_GUID,
        "createdBy": ORIGINATOR_NAME,
        "createTime": CREATION_DATE,
        "validInstanceStatusList": ["ACTIVE", "DELETED"],
        "initialStatus": "ACTIVE",
        "propertiesDefinition": [
            {
                "headerVersion": 1,
                "attributeName": ATTR_REL_NOTES_NAME,
                "attributeType": {
                    "class": "CollectionDef",
                    "headerVersion": 1,
                    "version": 1,
                    "versionName": "6.1-SNAPSHOT",
                    "category": "COLLECTION",
                    "guid": MAP_STRING_STRING_GUID,
                    "name": "map<string,string>",
                    "description": "A map from string to string.",
                    "descriptionGUID": MAP_STRING_STRING_DESC_GUID,
                    "collectionDefCategory": "OM_COLLECTION_MAP",
                    "argumentCount": 2,
                    "argumentTypes": ["OM_PRIMITIVE_TYPE_STRING", "OM_PRIMITIVE_TYPE_STRING"]
                },
                "attributeStatus": "ACTIVE_ATTRIBUTE",
                "attributeDescription": ATTR_REL_NOTES_DESC,
                "valuesMinCount": 0,
                "valuesMaxCount": 1,
                "attributeCardinality": "AT_MOST_ONE",
                "indexable": True,
                "unique": False
            }
        ],
        "propagationRule": "NONE",
        "endDef1": {
            "headerVersion": 1,
            "entityType": {
                "headerVersion": 1,
                "guid": REL_END1_ENTITY_GUID,
                "name": REL_END1_ENTITY_TYPE,
                "status": "ACTIVE_TYPEDEF"
            },
            "attributeName": REL_END1_ATTR_NAME,
            "attributeDescription": REL_END1_ATTR_DESC,
            "attributeCardinality": "ANY_NUMBER"
        },
        "endDef2": {
            "headerVersion": 1,
            "entityType": {
                "headerVersion": 1,
                "guid": REL_END2_ENTITY_GUID,
                "name": REL_END2_ENTITY_TYPE,
                "status": "ACTIVE_TYPEDEF"
            },
            "attributeName": REL_END2_ATTR_NAME,
            "attributeDescription": REL_END2_ATTR_DESC,
            "attributeCardinality": "ANY_NUMBER"
        },
        "multiLink": False
    }

    # Complete Archive
    archive = {
        "@class": "OpenMetadataArchive",
        "archiveProperties": {
            "@class": "OpenMetadataArchiveProperties",
            "archiveGUID": ARCHIVE_GUID,
            "archiveName": ARCHIVE_NAME,
            "archiveDescription": ARCHIVE_DESCRIPTION,
            "archiveType": ARCHIVE_TYPE,
            "originatorName": ORIGINATOR_NAME,
            "originatorLicense": ORIGINATOR_LICENSE,
            "creationDate": CREATION_DATE,
            "dependsOnArchives": DEPENDS_ON_ARCHIVES
        },
        "archiveTypeStore": {
            "@class": "OpenMetadataArchiveTypeStore",
            "attributeTypeDefs": [biopsy_scope_enum],
            "newTypeDefs": [
                biopsy_report_entity,
                reviewed_classification,
                biopsy_evidence_relationship
            ]
        }
    }

    return archive

if __name__ == "__main__":
    archive_data = create_archive()
    with open("coco-workbooks/creating-new-open-metadata-types/CocoTypesArchive_recreated.omarchive", "w") as f:
        json.dump(archive_data, f, separators=(',', ':'))
    print("Archive recreated successfully in CocoTypesArchive_recreated.omarchive")
