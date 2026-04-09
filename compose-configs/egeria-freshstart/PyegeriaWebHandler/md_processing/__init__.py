from loguru import logger
import pyegeria.view.md_processing_utils as mpu

# Re-export available from pyegeria
extract_command = getattr(mpu, 'extract_command', None)
process_glossary_upsert_command = getattr(mpu, 'process_glossary_upsert_command', None)
process_term_upsert_command = getattr(mpu, 'process_term_upsert_command', None)
process_provenance_command = getattr(mpu, 'process_provenance_command', None)
get_current_datetime_string = getattr(mpu, 'get_current_datetime_string', lambda: "")
process_project_upsert_command = getattr(mpu, 'process_project_upsert_command', None)
command_list = getattr(mpu, 'command_list', [])
process_blueprint_upsert_command = getattr(mpu, 'process_blueprint_upsert_command', None)
process_solution_component_upsert_command = getattr(mpu, 'process_solution_component_upsert_command', None)

# Stubs for other missing functions that might be imported from md_processing directly
def stub_func(*args, **kwargs):
    logger.warning(f"Stubbed function called with args: {args} and kwargs: {kwargs}")
    return {"status": "Not implemented"}

process_component_link_unlink_command = stub_func
process_csv_element_upsert_command = stub_func
process_link_term_term_relationship_command = stub_func
process_information_supply_chain_upsert_command = stub_func
process_information_supply_chain_link_unlink_command = stub_func
process_digital_product_upsert_command = stub_func
process_agreement_upsert_command = stub_func
process_collection_upsert_command = stub_func
process_link_agreement_item_command = stub_func
process_gov_definition_upsert_command = stub_func
GOV_COM_LIST = []
GOV_LINK_LIST = []
process_governed_by_link_detach_command = stub_func
process_gov_def_link_detach_command = stub_func
process_product_dependency_command = stub_func
process_add_to_collection_command = stub_func
process_attach_collection_command = stub_func
process_gov_def_context_command = stub_func
process_supporting_gov_def_link_detach_command = stub_func
process_attach_subscriber_command = stub_func
process_output_command = stub_func
COLLECTIONS_LIST = []
SIMPLE_COLLECTIONS = []
LIST_COMMANDS = []
PROJECT_COMMANDS = []
process_link_project_hierarchy_command = stub_func
process_external_reference_upsert_command = stub_func
process_link_to_external_reference_command = stub_func
process_link_to_media_reference_command = stub_func
process_link_to_cited_document_command = stub_func
EXT_REF_UPSERT = []
LINK_CITED_DOC = []
LINK_MEDIA = []
LINK_EXT_REF = []
