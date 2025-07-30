#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import sys
import os
import time
import argparse
from concurrent.futures import ThreadPoolExecutor

def process_file(file_name, base_url="http://localhost:8085"):
    """
    Process a single file using the Dr. Egeria process API.
    
    Args:
        file_name (str): The name of the file to process
        base_url (str): The base URL of the Apache web server
        
    Returns:
        tuple: (file_name, result_dict) containing the file name and the API response
    """
    url = f"{base_url}/api/dr.egeria/process"
    params = {"file-name": file_name}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        result = response.json()
        return file_name, result
    except requests.exceptions.RequestException as e:
        return file_name, {"status": "error", "message": str(e)}
    except json.JSONDecodeError as e:
        return file_name, {"status": "error", "message": f"Invalid JSON response: {e}"}

def batch_process_files(file_list, base_url="http://localhost:8085", max_workers=5):
    """
    Process multiple files in parallel using the Dr. Egeria process API.
    
    Args:
        file_list (list): List of file names to process
        base_url (str): The base URL of the Apache web server
        max_workers (int): Maximum number of parallel workers
        
    Returns:
        dict: Dictionary mapping file names to their processing results
    """
    results = {}
    
    print(f"Starting batch processing of {len(file_list)} files...")
    start_time = time.time()
    
    # Process files in parallel using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks and create a future-to-filename mapping
        future_to_file = {
            executor.submit(process_file, file_name, base_url): file_name 
            for file_name in file_list
        }
        
        # Process results as they complete
        for i, future in enumerate(future_to_file):
            file_name, result = future.result()
            results[file_name] = result
            
            # Print progress
            print(f"Processed {i+1}/{len(file_list)}: {file_name} - {result['status']}")
    
    elapsed_time = time.time() - start_time
    print(f"Batch processing completed in {elapsed_time:.2f} seconds")
    
    return results

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Batch process files using Dr. Egeria API')
    parser.add_argument('--dir', type=str, help='Directory containing files to process')
    parser.add_argument('--files', nargs='+', help='List of files to process')
    parser.add_argument('--url', type=str, default='http://localhost:8085', 
                        help='Base URL of the Apache web server')
    parser.add_argument('--workers', type=int, default=5, 
                        help='Maximum number of parallel workers')
    
    args = parser.parse_args()
    
    # Get list of files to process
    file_list = []
    
    if args.dir:
        # Process all files in the specified directory
        if os.path.isdir(args.dir):
            file_list = [f for f in os.listdir(args.dir) if os.path.isfile(os.path.join(args.dir, f))]
            file_list = [os.path.join(args.dir, f) for f in file_list]
        else:
            print(f"Error: Directory {args.dir} does not exist")
            sys.exit(1)
    elif args.files:
        # Process the specified list of files
        file_list = args.files
    else:
        # Use default example files
        file_list = ["example1.md", "example2.md", "example3.md"]
    
    # Process the files
    results = batch_process_files(file_list, args.url, args.workers)
    
    # Print summary
    print("\nProcessing Summary:")
    success_count = sum(1 for result in results.values() if result.get('status') == 'success')
    error_count = len(results) - success_count
    
    print(f"Total files: {len(results)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {error_count}")
    
    # Print details of any errors
    if error_count > 0:
        print("\nErrors:")
        for file_name, result in results.items():
            if result.get('status') != 'success':
                print(f"  {file_name}: {result.get('message')}")

if __name__ == "__main__":
    main()