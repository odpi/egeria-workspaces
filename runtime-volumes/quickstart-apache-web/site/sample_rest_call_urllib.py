#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
import urllib.error
import json
import sys

def call_dr_egeria_process(file_name="meow.md", base_url="http://localhost:8085"):
    """
    Make a REST call to the Dr. Egeria process API endpoint using urllib.
    
    Args:
        file_name (str): The name of the file to process
        base_url (str): The base URL of the Apache web server
        
    Returns:
        dict: The JSON response from the API
    """
    # Construct the full URL with the query parameter
    params = urllib.parse.urlencode({"file-name": file_name})
    url = f"{base_url}/api/dr.egeria/process?{params}"
    
    try:
        # Make the GET request
        with urllib.request.urlopen(url) as response:
            # Read and decode the response
            response_data = response.read().decode('utf-8')
            
            # Parse the JSON response
            result = json.loads(response_data)
            
            print(f"API call successful: {result}")
            return result
            
    except urllib.error.URLError as e:
        print(f"Error making API request: {e}")
        return {"status": "error", "message": str(e)}
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        return {"status": "error", "message": f"Invalid JSON response: {e}"}

if __name__ == "__main__":
    # Get the file name from command line arguments or use a default
    file_name = sys.argv[1] if len(sys.argv) > 1 else "example.md"
    
    # Call the API
    result = call_dr_egeria_process(file_name)
    
    # Print the result in a formatted way
    print("\nResult:")
    print(f"Status: {result.get('status')}")
    print(f"Message: {result.get('message')}")