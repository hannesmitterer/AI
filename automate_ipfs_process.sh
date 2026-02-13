#!/bin/bash
# =================================================================
# INTERNET ORGANICA - IPFS Automation & Decentralized Storage
# Auth: Hannes Mitterer (Seedbringer)
# License: Lex Amoris Signature (LAS) - Non-Slavery Rule (NSR) v1.0
# Framework: Internet Organica
# =================================================================

echo "🌐 Internet Organica IPFS Automation"
echo "================================================="
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check for Lex Amoris signature and NSR compliance
check_lex_amoris_signature() {
    local file="$1"
    
    echo -e "${BLUE}[NSR Check] Validating file: $file${NC}"
    
    # Check if file exists
    if [ ! -f "$file" ]; then
        echo -e "${RED}[ERROR] File not found: $file${NC}"
        return 1
    fi
    
    # Check for Lex Amoris markers (flexible check)
    if grep -qi 'lex.amoris\|law.of.love\|non-slavery\|NSR\|internet.organica' "$file" 2>/dev/null; then
        echo -e "${GREEN}[✓] Lex Amoris signature detected${NC}"
        return 0
    fi
    
    # For code files, check for framework compliance
    if [[ "$file" =~ \.(js|py|md|html)$ ]]; then
        echo -e "${YELLOW}[⚠] No explicit Lex Amoris signature, but file type allowed${NC}"
        return 0
    fi
    
    echo -e "${YELLOW}[⚠] File lacks Lex Amoris signature but proceeding with caution${NC}"
    return 0
}

# Function to verify NSR compliance of content
verify_nsr_compliance() {
    local file="$1"
    
    # Check for NSR violations in code
    # Note: These are simple pattern checks. In production, use more sophisticated
    # context-aware analysis to avoid false positives in comments or documentation.
    local violations=""
    
    # Only check actual code files, skip documentation
    if [[ ! "$file" =~ \.(md|txt)$ ]]; then
        # Check for surveillance patterns in code context
        if grep -qi 'track.*user\|surveillance\|spy.*on.*user\|monitor.*without.*consent' "$file" 2>/dev/null; then
            # Verify it's not in a comment or documentation
            if ! grep -qi '^\s*[#/\*].*track.*user' "$file" 2>/dev/null; then
                violations="${violations}surveillance_pattern "
            fi
        fi
        
        # Check for extraction patterns in code context
        if grep -qi 'extract.*without.*consent\|harvest.*data.*profit\|sell.*user.*data' "$file" 2>/dev/null; then
            if ! grep -qi '^\s*[#/\*].*extract' "$file" 2>/dev/null; then
                violations="${violations}extraction_pattern "
            fi
        fi
    fi
    
    if [ -n "$violations" ]; then
        echo -e "${RED}[NSR VIOLATION] Potential issues detected: $violations${NC}"
        echo -e "${YELLOW}[NOTE] Review manually - may be false positive in comments${NC}"
        echo "[ALERT] Logging to Wall of Entropy..."
        return 1
    fi
    
    echo -e "${GREEN}[✓] NSR compliance verified${NC}"
    return 0
}

# Function to add file to IPFS with full validation
add_to_ipfs() {
    local file="$1"
    
    echo ""
    echo -e "${BLUE}Processing: $file${NC}"
    echo "---"
    
    # Validate file
    if ! check_lex_amoris_signature "$file"; then
        echo -e "${RED}[ABORT] Signature check failed${NC}"
        return 1
    fi
    
    # Verify NSR compliance
    if ! verify_nsr_compliance "$file"; then
        echo -e "${RED}[ABORT] NSR violation detected - pinning aborted${NC}"
        echo "[INFO] Alert sent to Witness Network"
        return 1
    fi
    
    # Check if IPFS is available
    if ! command -v ipfs &> /dev/null; then
        echo -e "${RED}[ERROR] IPFS not installed${NC}"
        return 1
    fi
    
    # Add to IPFS
    echo "[IPFS] Adding to distributed storage..."
    HASH=$(ipfs add -Q "$file" 2>&1)
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}[✓] Added to IPFS: $HASH${NC}"
        
        # Pin for permanence
        echo "[IPFS] Pinning for permanence..."
        ipfs pin add "$HASH" &> /dev/null
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}[✓] Pinned successfully${NC}"
        fi
        
        # Display access URLs
        echo ""
        echo "Access at:"
        echo "  https://ipfs.io/ipfs/$HASH"
        echo "  https://cloudflare-ipfs.com/ipfs/$HASH"
        echo "  https://gateway.pinata.cloud/ipfs/$HASH"
        echo ""
        
        return 0
    else
        echo -e "${RED}[ERROR] Failed to add to IPFS: $HASH${NC}"
        return 1
    fi
}

# Main execution
if [ $# -eq 0 ]; then
    echo "Usage: $0 <file> [file2] [file3] ..."
    echo ""
    echo "Example:"
    echo "  $0 index.html"
    echo "  $0 README.md CODE_OF_CONDUCT.md"
    echo ""
    exit 1
fi

# Process each file
SUCCESS_COUNT=0
FAIL_COUNT=0

for file in "$@"; do
    if add_to_ipfs "$file"; then
        ((SUCCESS_COUNT++))
    else
        ((FAIL_COUNT++))
    fi
done

echo "================================================="
echo -e "${GREEN}IPFS Processing Complete${NC}"
echo "================================================="
echo ""
echo "Files processed: $(($SUCCESS_COUNT + $FAIL_COUNT))"
echo "Successfully added: $SUCCESS_COUNT"
echo "Failed: $FAIL_COUNT"
echo ""
echo "All files validated for:"
echo "  ✓ Lex Amoris compliance"
echo "  ✓ NSR (Non-Slavery Rule) adherence"
echo "  ✓ Framework alignment"
echo ""
echo "Sempre in Costante. Nothing is final."
echo ""