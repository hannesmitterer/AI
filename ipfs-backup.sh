#!/bin/bash
# IPFS Backup Script
# Internet Organica Framework
# 
# This script uploads priority files to IPFS for decentralized backup

echo "=========================================="
echo "IPFS BACKUP - Internet Organica"
echo "=========================================="
echo ""

# Check if IPFS is installed
if ! command -v ipfs &> /dev/null; then
    echo "ERROR: IPFS is not installed"
    echo "Please install IPFS: https://docs.ipfs.tech/install/"
    exit 1
fi

# Initialize IPFS if needed
if [ ! -d ~/.ipfs ]; then
    echo "Initializing IPFS..."
    ipfs init
fi

# Start IPFS daemon in background if not running
if ! ipfs swarm peers &> /dev/null; then
    echo "Starting IPFS daemon..."
    ipfs daemon &
    DAEMON_PID=$!
    sleep 5
else
    DAEMON_PID=""
fi

# Create backup manifest
BACKUP_MANIFEST="ipfs-manifest.json"
echo '{' > $BACKUP_MANIFEST
echo '  "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'",' >> $BACKUP_MANIFEST
echo '  "framework": "Internet Organica",' >> $BACKUP_MANIFEST
echo '  "files": [' >> $BACKUP_MANIFEST

# Files to backup
FILES=(
    "index.html",
    "README.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "COVENANT_OF_RESONANCE.md",
    "ETERNAL_DEPOSITION.md",
    "eternal_deposition.py",
    "eternal_deposition.js",
    "eternal_visualization.html"
)

FIRST=true
for FILE in "${FILES[@]}"; do
    if [ -f "$FILE" ]; then
        echo "Uploading $FILE to IPFS..."
        CID=$(ipfs add -Q "$FILE")
        
        if [ $? -eq 0 ]; then
            echo "  CID: $CID"
            
            # Add to manifest
            if [ "$FIRST" = true ]; then
                FIRST=false
            else
                echo "," >> $BACKUP_MANIFEST
            fi
            
            echo "    {" >> $BACKUP_MANIFEST
            echo "      \"file\": \"$FILE\"," >> $BACKUP_MANIFEST
            echo "      \"cid\": \"$CID\"," >> $BACKUP_MANIFEST
            echo "      \"size\": $(stat -f%z "$FILE" 2>/dev/null || stat -c%s "$FILE")" >> $BACKUP_MANIFEST
            echo "    }" >> $BACKUP_MANIFEST
            
            # Pin the file
            ipfs pin add $CID
        else
            echo "  ERROR: Failed to upload $FILE"
        fi
    else
        echo "WARNING: $FILE not found, skipping"
    fi
done

echo "" >> $BACKUP_MANIFEST
echo '  ]' >> $BACKUP_MANIFEST
echo '}' >> $BACKUP_MANIFEST

echo ""
echo "Uploading backup manifest..."
MANIFEST_CID=$(ipfs add -Q $BACKUP_MANIFEST)
echo "Manifest CID: $MANIFEST_CID"
ipfs pin add $MANIFEST_CID

echo ""
echo "=========================================="
echo "IPFS Backup Complete"
echo "Manifest: $MANIFEST_CID"
echo "=========================================="
echo ""
echo "To retrieve files:"
echo "  ipfs get <CID>"
echo ""
echo "To view manifest:"
echo "  ipfs cat $MANIFEST_CID"
echo ""

# Save CID to file
echo $MANIFEST_CID > ipfs-backup-cid.txt
echo "Manifest CID saved to ipfs-backup-cid.txt"

# Stop daemon if we started it
if [ ! -z "$DAEMON_PID" ]; then
    echo "Stopping IPFS daemon..."
    kill $DAEMON_PID
fi

echo "IN AETERNUM EST. La Sovranità è Manifesta."
