from loguru import logger

def stub_func(*args, **kwargs):
    logger.warning(f"Stubbed function called with args: {args} and kwargs: {kwargs}")
    return {"status": "Not implemented"}

process_link_project_dependency_command = stub_func
process_link_project_hierarchy_command = stub_func
