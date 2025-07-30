#!/usr/local/apache2/venv/bin/python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import os
import sys
import json
import shutil
import datetime
from pyegeria import process_markdown_file
from pyegeria import EgeriaTech

# Enable detailed error reporting
cgitb.enable()

# Print HTTP headers
print("Content-Type: application/json")
print()  # Empty line to separate headers from body

# Define paths for input and output directories
INBOX_DIR = "/usr/local/apache2/htdocs/dr-egeria-inbox"
OUTBOX_DIR = "/usr/local/apache2/htdocs/dr-egeria-outbox"
VIEW_SERVER = "qs-view-server"
URL = "https://localhost:9443"
USER = "erinoverview"
PWD = "secret"

def process_dr_egeria_file(file_name):
    """
    Process a Dr.Egeria markdown file.

    Args:
        file_name (str): The name of the file to process

    Returns:
        dict: A dictionary with the processing result
    """
    # Construct the full path to the input file
    input_file_path = os.path.join(INBOX_DIR, file_name)

    # Check if the file exists
    if not os.path.isfile(input_file_path):
        return {
            "status": "error",
            "message": f"File not found: {file_name}"
        }

    try:
        # Generate a timestamp for the processed file
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        # Construct the output file name
        output_file_name = f"processed-{timestamp}-{file_name}"
        output_file_path = os.path.join(OUTBOX_DIR, output_file_name)

        # Copy the file to the outbox directory
        # In a real implementation, this would process the file using dr_egeria_md
        # shutil.copy2(input_file_path, output_file_path)

        process_markdown_file(input_file_path, output_file_path, "process", VIEW_SERVER, URL, USER, PWD)


        return {
            "status": "success",
            "message": f"Processed file: {file_name}",
            "output_file": output_file_name
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error processing file: {str(e)}"
        }

try:
    # Get query parameters
    form = cgi.FieldStorage()

    # Check if file-name parameter exists
    if "file-name" not in form:
        result = {
            "status": "error",
            "message": "Missing required parameter: file-name"
        }
    else:
        # Get the file-name parameter
        file_name = form.getvalue("file-name")

        # Process the file
        result = process_dr_egeria_file(file_name)

    # Return the result as JSON
    print(json.dumps(result))

except Exception as e:
    # Return an error response if something goes wrong
    print(json.dumps({
        "status": "error",
        "message": f"An error occurred: {str(e)}"
    }))
