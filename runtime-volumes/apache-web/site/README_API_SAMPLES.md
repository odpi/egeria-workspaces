# Dr. Egeria API Sample Scripts

This directory contains sample Python scripts that demonstrate how to interact with the Dr. Egeria process API.

## API Endpoint

The Dr. Egeria process API is available at:

```
http://localhost:8085/api/dr.egeria/process
```

This endpoint accepts a `file-name` query parameter and returns a JSON response.

## Sample Scripts

### 1. Command Line (using curl)

**File:** `curl_example.sh`

This shell script demonstrates how to make a REST call to the Dr. Egeria process API using curl from the command line.

**Dependencies:**
- bash
- curl
- Python 3.x (for URL encoding and JSON formatting)

**Usage:**
```bash
./curl_example.sh [options]
```

**Options:**
- `-f, --file FILE_NAME`: Name of the file to process (default: example.md)
- `-u, --url BASE_URL`: Base URL of the server (default: http://localhost:8085)
- `-h, --help`: Display help message

**Examples:**
```bash
# Process a specific file
./curl_example.sh --file document.md

# Specify a different server URL
./curl_example.sh --url http://example.com:8085 --file document.md
```

### 2. Basic REST Call (using requests)

**File:** `sample_rest_call.py`

This script demonstrates how to make a basic REST call to the Dr. Egeria process API using the `requests` library.

**Dependencies:**
- Python 3.x
- requests

**Usage:**
```bash
python sample_rest_call.py [file_name]
```

If no file name is provided, it defaults to "example.md".

### 2. Basic REST Call (using urllib)

**File:** `sample_rest_call_urllib.py`

This script demonstrates how to make a basic REST call to the Dr. Egeria process API using the standard library's `urllib` module, without any external dependencies.

**Dependencies:**
- Python 3.x (standard library only)

**Usage:**
```bash
python sample_rest_call_urllib.py [file_name]
```

If no file name is provided, it defaults to "example.md".

### 3. Batch Processing

**File:** `batch_process_files.py`

This script demonstrates how to process multiple files in parallel using the Dr. Egeria process API.

**Dependencies:**
- Python 3.x
- requests

**Usage:**
```bash
python batch_process_files.py [options]
```

**Options:**
- `--dir DIRECTORY`: Process all files in the specified directory
- `--files FILE1 FILE2 ...`: Process the specified list of files
- `--url URL`: Base URL of the Apache web server (default: http://localhost:8085)
- `--workers N`: Maximum number of parallel workers (default: 5)

**Examples:**
```bash
# Process all files in a directory
python batch_process_files.py --dir /path/to/files

# Process specific files
python batch_process_files.py --files file1.md file2.md file3.md

# Specify a different server URL
python batch_process_files.py --url http://example.com:8085 --files file1.md

# Use 10 parallel workers
python batch_process_files.py --dir /path/to/files --workers 10
```

## Response Format

All API calls return a JSON response with the following structure:

```json
{
  "status": "success|error",
  "message": "Message describing the result or error"
}
```

## Error Handling

All sample scripts include error handling for:
- Network errors (connection issues, timeouts, etc.)
- HTTP errors (404, 500, etc.)
- JSON parsing errors

## Integration with Other Systems

These sample scripts can be integrated with other systems by:

1. Importing the functions into your own Python code
2. Calling the API from shell scripts using curl or wget
3. Using the batch processing script as part of a data pipeline

## Troubleshooting

If you encounter issues:

1. Check that the Apache web server is running on port 8085
2. Verify that the CGI scripts are properly configured and executable
3. Check the Apache error logs for any server-side errors
4. Ensure that the required Python packages are installed
