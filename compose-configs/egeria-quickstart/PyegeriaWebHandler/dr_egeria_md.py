import os
import sys
import asyncio
from loguru import logger
from rich.console import Console
from pyegeria import EgeriaTech
from md_processing.dr_egeria import process_md_file_v2
async def process_md_file_async(input_file, output_folder, directive, server, url, userid, user_pass):
    client = EgeriaTech(server, url, user_id=userid)
    client.create_egeria_bearer_token(userid, user_pass)
    if os.environ.get('EGERIA_INBOX_PATH') and os.environ.get('EGERIA_INBOX_PATH') + '/' in input_file:
        input_file = input_file.split(os.environ.get('EGERIA_INBOX_PATH') + '/')[-1]
    await process_md_file_v2(input_file=input_file, output_folder=output_folder, directive=directive, client=client)
def process_markdown_file(input_file, output_folder, directive, server, url, userid, user_pass):
    try:
        asyncio.run(process_md_file_async(input_file, output_folder, directive, server, url, userid, user_pass))
    except Exception as e:
        print(f'Async processing failed: {e}')
process_md_file = process_markdown_file
