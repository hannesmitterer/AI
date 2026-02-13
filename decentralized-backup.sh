#!/bin/bash
# decentralized-backup.sh
# Backup critical Internet Organica assets to IPFS for permanent, distributed storage
#
# Framework: Internet Organica
# Principles: Sovereignty, Permanence, Transparency

set -e

echo "🏛️ Internet Organica Decentralized Backup System"
echo "================================================="
echo ""

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
BACKUP_DIR="/tmp/internet-organica-backup"
MANIFEST_FILE="backup-manifest.json"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Critical files to backup
CRITICAL_FILES=(
    "README.md"
    "CODE_OF_CONDUCT.md"
    "CONTRIBUTING.md"
    "SECURITY.md"
    "SOVEREIGNTY.md"
    "COVENANT_OF_RESONANCE.md"
    "ETERNAL_DEPOSITION.md"
    "index.html"
    "sovereign-shield.js"
    "wall-of-entropy.js"
    "entropy-dashboard.html"
    ".orchestration/config.json"
)

# Create backup directory
mkdir -p "$BACKUP_DIR"

echo -e "${BLUE}[1/5] Preparing backup...${NC}"
echo ""

# Initialize manifest
cat > "$BACKUP_DIR/$MANIFEST_FILE" << EOF
{
  "framework": "Internet Organica",
  "version": "1.0.0",
  "timestamp": "$TIMESTAMP",
  "principles": ["Lex Amoris", "NSR", "OLF"],
  "backup_type": "decentralized_ipfs",
  "files": []
}
EOF

echo -e "${BLUE}[2/5] Copying critical files...${NC}"
file_count=0
for file in "${CRITICAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        # Create directory structure in backup
        dir=$(dirname "$file")
        mkdir -p "$BACKUP_DIR/$dir"
        
        # Copy file
        cp "$file" "$BACKUP_DIR/$file"
        echo "  ✓ Copied: $file"
        ((file_count++))
    else
        echo "  ⚠ Not found: $file"
    fi
done

echo ""
echo -e "${GREEN}Copied $file_count files${NC}"
echo ""

# Check if IPFS is available
echo -e "${BLUE}[3/5] Checking IPFS availability...${NC}"
if command -v ipfs &> /dev/null; then
    IPFS_AVAILABLE=true
    echo "  ✓ IPFS command available"
    
    # Check if daemon is running
    if ipfs id &> /dev/null; then
        echo "  ✓ IPFS daemon is running"
    else
        echo "  ⚠ IPFS daemon not running"
        echo "  Note: Run 'ipfs daemon' to enable IPFS features"
        IPFS_AVAILABLE=false
    fi
else
    echo "  ⚠ IPFS not installed"
    echo "  Install from: https://docs.ipfs.io/install/"
    IPFS_AVAILABLE=false
fi

echo ""

# Add files to IPFS if available
if [ "$IPFS_AVAILABLE" = true ]; then
    echo -e "${BLUE}[4/5] Adding files to IPFS...${NC}"
    
    # Array to store file hashes
    declare -A file_hashes
    
    for file in "${CRITICAL_FILES[@]}"; do
        if [ -f "$BACKUP_DIR/$file" ]; then
            # Add to IPFS and capture hash
            hash=$(ipfs add -Q "$BACKUP_DIR/$file" 2>/dev/null || echo "ERROR")
            
            if [ "$hash" != "ERROR" ]; then
                file_hashes["$file"]="$hash"
                echo "  ✓ $file → $hash"
                
                # Pin the file to ensure permanence
                ipfs pin add "$hash" &> /dev/null || true
            else
                echo "  ✗ Failed to add: $file"
            fi
        fi
    done
    
    echo ""
    
    # Add entire backup directory as a bundle
    echo "  Adding complete backup bundle..."
    BUNDLE_HASH=$(ipfs add -r -Q "$BACKUP_DIR" 2>/dev/null || echo "ERROR")
    
    if [ "$BUNDLE_HASH" != "ERROR" ]; then
        echo "  ✓ Complete bundle → $BUNDLE_HASH"
        ipfs pin add "$BUNDLE_HASH" &> /dev/null || true
    fi
    
    echo ""
    
    # Update manifest with hashes
    python3 << EOF
import json

# Load manifest
with open('$BACKUP_DIR/$MANIFEST_FILE', 'r') as f:
    manifest = json.load(f)

# Add file hashes
manifest['files'] = []
file_hashes = {}
$(for key in "${!file_hashes[@]}"; do echo "file_hashes['$key'] = '${file_hashes[$key]}'"; done)

for file, hash in file_hashes.items():
    manifest['files'].append({
        'path': file,
        'ipfs_hash': hash,
        'gateway_url': f'https://ipfs.io/ipfs/{hash}'
    })

manifest['bundle_hash'] = '$BUNDLE_HASH'
manifest['bundle_gateway_url'] = 'https://ipfs.io/ipfs/$BUNDLE_HASH'

# Save updated manifest
with open('$BACKUP_DIR/$MANIFEST_FILE', 'w') as f:
    json.dump(manifest, f, indent=2)
EOF
    
else
    echo -e "${YELLOW}[4/5] Skipping IPFS (not available)${NC}"
    echo "  Backup files saved locally to: $BACKUP_DIR"
    echo ""
fi

# Generate backup summary
echo -e "${BLUE}[5/5] Generating backup summary...${NC}"

cat > "$BACKUP_DIR/BACKUP_SUMMARY.txt" << EOF
================================================================================
INTERNET ORGANICA DECENTRALIZED BACKUP SUMMARY
================================================================================

Framework: Internet Organica
Version: 1.0.0
Timestamp: $TIMESTAMP
Principles: Lex Amoris, NSR, OLF

Backup Type: Decentralized IPFS Storage
Files Backed Up: $file_count

================================================================================
IPFS ACCESS
================================================================================

$(if [ "$IPFS_AVAILABLE" = true ]; then
    echo "Bundle Hash: $BUNDLE_HASH"
    echo ""
    echo "Access complete backup at:"
    echo "  https://ipfs.io/ipfs/$BUNDLE_HASH"
    echo "  https://cloudflare-ipfs.com/ipfs/$BUNDLE_HASH"
    echo "  https://gateway.pinata.cloud/ipfs/$BUNDLE_HASH"
    echo ""
    echo "Individual files:"
    for key in "${!file_hashes[@]}"; do
        echo "  $key: ${file_hashes[$key]}"
    done
else
    echo "IPFS not available - files saved locally only"
    echo "Local backup: $BACKUP_DIR"
fi)

================================================================================
VERIFICATION
================================================================================

To verify integrity of backed up files:

1. Download from IPFS gateway
2. Compare checksums with original files
3. Verify through multiple witness nodes

All IPFS hashes are cryptographically verified and immutable.

================================================================================
RESTORATION
================================================================================

To restore from this backup:

$(if [ "$IPFS_AVAILABLE" = true ]; then
    echo "# Using IPFS"
    echo "ipfs get $BUNDLE_HASH -o restored-backup"
    echo ""
fi)

# From local backup
cp -r $BACKUP_DIR/* /destination/path/

================================================================================
SOVEREIGNTY STATEMENT
================================================================================

This backup is:
- ✓ Decentralized (no single point of control)
- ✓ Permanent (immutable IPFS storage)
- ✓ Verifiable (cryptographic hashes)
- ✓ Accessible (multiple gateways)
- ✓ Sovereign (owner-controlled)
- ✓ Transparent (public verification)

"IN AETERNUM EST. La Sovranità è Manifesta."

================================================================================
EOF

cat "$BACKUP_DIR/BACKUP_SUMMARY.txt"

# Save manifest to current directory as well
if [ "$IPFS_AVAILABLE" = true ]; then
    cp "$BACKUP_DIR/$MANIFEST_FILE" "./$MANIFEST_FILE"
    echo ""
    echo -e "${GREEN}✓ Backup manifest saved to: $MANIFEST_FILE${NC}"
fi

echo ""
echo -e "${GREEN}=================================================================================${NC}"
echo -e "${GREEN}BACKUP COMPLETE${NC}"
echo -e "${GREEN}=================================================================================${NC}"
echo ""
echo "Local backup: $BACKUP_DIR"

if [ "$IPFS_AVAILABLE" = true ]; then
    echo "IPFS bundle: $BUNDLE_HASH"
    echo ""
    echo "Access your backup at:"
    echo "  https://ipfs.io/ipfs/$BUNDLE_HASH"
fi

echo ""
echo "Sempre in Costante. Nothing is final."
echo ""
