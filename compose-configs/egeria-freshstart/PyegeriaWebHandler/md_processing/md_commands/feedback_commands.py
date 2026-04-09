from loguru import logger

def stub_func(*args, **kwargs):
    logger.warning(f"Stubbed function called with args: {args} and kwargs: {kwargs}")
    return {"status": "Not implemented"}

process_add_comment_command = stub_func
process_journal_entry_command = stub_func
process_upsert_note_command = stub_func
process_attach_note_log_command = stub_func
process_upsert_informal_tag_command = stub_func
process_tag_element_command = stub_func
