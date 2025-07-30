#!/bin/bash
# Example script demonstrating how to use curl to call the Dr. Egeria process API

# Default values
BASE_URL="http://localhost:8085"
FILE_NAME="example.md"

# Display usage information
function show_usage {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  -f, --file FILE_NAME    Name of the file to process (default: example.md)"
    echo "  -u, --url BASE_URL      Base URL of the server (default: http://localhost:8085)"
    echo "  -h, --help              Display this help message"
    echo ""
    echo "Example:"
    echo "  $0 --file document.md"
    echo "  $0 --url http://example.com:8085 --file document.md"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -f|--file)
            FILE_NAME="$2"
            shift
            shift
            ;;
        -u|--url)
            BASE_URL="$2"
            shift
            shift
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# URL encode the file name
ENCODED_FILE_NAME=$(echo -n "$FILE_NAME" | python3 -c "import sys, urllib.parse; print(urllib.parse.quote(sys.stdin.read()))")

# Construct the full URL
FULL_URL="${BASE_URL}/api/dr.egeria/process?file-name=${ENCODED_FILE_NAME}"

echo "Calling Dr. Egeria process API..."
echo "URL: $FULL_URL"
echo ""

# Make the API call using curl
curl -s "$FULL_URL" | python3 -m json.tool

# Check if curl was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to make API call"
    exit 1
fi

echo ""
echo "API call completed successfully."