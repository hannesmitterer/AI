#!/bin/bash

# Check if the path to the file is provided
if [ -z "$1" ]; then
  echo "Please provide the path to the file."
  exit 1
fi

FILE_PATH="$1"

# Check if the file exists
if [ ! -f "$FILE_PATH" ]; then
  echo "File not found!"
  exit 1
fi

# Calculate SHA-256 hash of the file
HASH=$(sha256sum "$FILE_PATH" | awk '{ print $1 }')

echo "SHA-256 Hash: $HASH"

# IPFS API endpoint
IPFS_API="https://api.ipfs.io/api/v0/add"

# Upload the file to IPFS and retrieve the CID
CID=$(curl -s -X POST -F file=@"$FILE_PATH" "$IPFS_API" | jq -r '.Hash')

if [ "$CID" == "null" ]; then
  echo "Failed to upload to IPFS."
  exit 1
fi

echo "CID: $CID"