from loguru import logger

def stub_func(*args, **kwargs):
    logger.warning(f"Stubbed function called with args: {args} and kwargs: {kwargs}")
    return {"status": "Not implemented"}

process_data_spec_upsert_command = stub_func
process_data_dict_upsert_command = stub_func
process_data_field_upsert_command = stub_func
process_data_structure_upsert_command = stub_func
process_data_class_upsert_command = stub_func
