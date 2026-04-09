from loguru import logger

def stub_func(*args, **kwargs):
    logger.warning(f"Stubbed function called with args: {args} and kwargs: {kwargs}")
    return {"status": "Not implemented"}

process_csv_element_upsert_command = stub_func
