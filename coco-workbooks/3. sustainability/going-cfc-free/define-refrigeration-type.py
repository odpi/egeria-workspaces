import json
import time

# --- Archive Properties ---
ARCHIVE_GUID = "9404308b-492c-4ac1-b3e1-0702fbcf8c4b"
ARCHIVE_NAME = "SustainabilityTypes"
ARCHIVE_DESCRIPTION = "New refrigeration type for sustainability initiative."
ARCHIVE_TYPE = "CONTENT_PACK"
ORIGINATOR_NAME = "Egeria Project"
ORIGINATOR_LICENSE = "Apache 2.0"
CREATION_DATE = 1781469069911
DEPENDS_ON_ARCHIVES = ["bce3b0a0-662a-4f87-b8dc-844078a11a6e"] # Existing Open Metadata Types


# --- EntityDef: RefrigerationUnity ---
ENTITY_REFRIGERATION_UNIT_NAME = "RefrigerationUnity"
ENTITY_REFRIGERATION_UNIT_GUID = "f9bf44a5-3685-41b4-96fe-16db867201a3"
ENTITY_REFRIGERATION_UNIT_DESC = "Results from a patient biopsy."
ENTITY_REFRIGERATION_UNIT_VERSION = CREATION_DATE
ENTITY_REFRIGERATION_UNIT_VERSION_NAME = "1.0"
ENTITY_REFRIGERATION_UNIT_SUPER_TYPE_NAME = "Infrastructure"
ENTITY_REFRIGERATION_UNIT_SUPER_TYPE_GUID = "c19746ac-b3ec-49ce-af4b-83348fc55e07"

# BiopsyReport Attributes
ATTR_COOLANT_TYPE_NAME = "coolantType"
ATTR_COOLANT_TYPE_DESC = "What type of coolant does this refrigeration unit have?"


# --- Primitive and Collection Types (Constant for this archive) ---
STRING_TYPE_GUID = "b34a64b9-554a-42b1-8f8a-7d5c2339f9c4"
MAP_STRING_STRING_GUID = "005c7c14-ac84-4136-beed-959401b041f8"
MAP_STRING_STRING_DESC_GUID = "f285d0ca-50ab-4564-b129-c7e3ba4e8545"

def create_archive():
    # Constructing EntityDef
    refrigeration_unit_entity = {
        "@class": "EntityDef",
        "headerVersion": 1,
        "guid": ENTITY_REFRIGERATION_UNIT_GUID,
        "name": ENTITY_REFRIGERATION_UNIT_NAME,
        "status": "ACTIVE_TYPEDEF",
        "version": ENTITY_REFRIGERATION_UNIT_VERSION,
        "versionName": ENTITY_REFRIGERATION_UNIT_VERSION_NAME,
        "category": "ENTITY_DEF",
        "superType": {
            "headerVersion": 1,
            "guid": ENTITY_REFRIGERATION_UNIT_SUPER_TYPE_GUID,
            "name": ENTITY_REFRIGERATION_UNIT_SUPER_TYPE_NAME,
            "status": "ACTIVE_TYPEDEF"
        },
        "description": ENTITY_REFRIGERATION_UNIT_DESC,
        "origin": ARCHIVE_GUID,
        "createdBy": ORIGINATOR_NAME,
        "createTime": CREATION_DATE,
        "validInstanceStatusList": ["ACTIVE", "DELETED"],
        "initialStatus": "ACTIVE",
        "propertiesDefinition": [
            {
                "headerVersion": 1,
                "attributeName": ATTR_COOLANT_TYPE_NAME,
                "attributeType": STRING_TYPE_GUID,
                "attributeStatus": "ACTIVE_ATTRIBUTE",
                "attributeDescription": ATTR_COOLANT_TYPE_DESC,
                "valuesMinCount": 0,
                "valuesMaxCount": 1,
                "attributeCardinality": "AT_MOST_ONE",
                "indexable": True,
                "unique": False
            }
        ]
    }

    # Complete Archive
    archive = {
        "@class": "OpenMetadataArchive",
        "archiveProperties": {
            "@class": "OpenMetadataArchiveProperties",
            "archiveGUID": ARCHIVE_GUID,
            "archiveName": ARCHIVE_NAME,
            "archiveDescription": ARCHIVE_DESCRIPTION,
            "archiveType": "CONTENT_PACK",
            "originatorName": ORIGINATOR_NAME,
            "originatorLicense": ORIGINATOR_LICENSE,
            "creationDate": CREATION_DATE,
            "dependsOnArchives": DEPENDS_ON_ARCHIVES
        },
        "archiveTypeStore": {
            "@class": "OpenMetadataArchiveTypeStore",
            "newTypeDefs": [
                refrigeration_unit_entity
            ]
        }
    }

    return archive

if __name__ == "__main__":
    archive_data = create_archive()
    with open("coco-workbooks/creating-new-open-metadata-types/SustainabilityTypes.omarchive", "w") as f:
        json.dump(archive_data, f, separators=(',', ':'))
    print("Archive recreated successfully in SustainabilityTypes.omarchive")
