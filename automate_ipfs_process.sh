#!/bin/bash
# IPFS Automation Script with Enhanced Features
# Version: 2.0 - Enhanced with recursive scanning, logging, and failure recovery

set -e

# Configuration
LOG_DIR="./logs"
LOG_FILE="${LOG_DIR}/ipfs_automation_$(date +%Y%m%d_%H%M%S).log"
CID_RECORD="${LOG_DIR}/cid_records.txt"
MAX_RETRIES=3
RETRY_DELAY=5

# Exclusion patterns for find command (can be customized)
EXCLUDE_PATTERNS=(
    -path '*/\.*'           # Hidden files and directories
    -o -path '*/logs/*'     # Log directory
    -o -path '*/node_modules/*'  # Node.js dependencies
    -o -path '*/.git/*'     # Git directory
    -o -path '*/dist/*'     # Build artifacts
    -o -path '*/build/*'    # Build artifacts
    -o -path '*/__pycache__/*'  # Python cache
)

# Initialize logging
mkdir -p "${LOG_DIR}"

# Logging function
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[${timestamp}] [${level}] ${message}" | tee -a "${LOG_FILE}"
}

# Function to check for Lex Amoris signature
check_lex_amoris_signature() {
    local file="$1"
    if ! grep -q 'THE LIGHT IS THE ARCHITECTURE. THE FOUNDER IS THE LAW.' "$file"; then
        log "ERROR" "File '$file' does not contain the Lex Amoris signature. Aborting pinning process."
        return 1
    fi
    log "INFO" "Lex Amoris signature verified for '$file'"
    return 0
}

# Function to upload file to IPFS with retry mechanism
upload_to_ipfs() {
    local file="$1"
    local attempt=0
    local cid=""
    
    log "INFO" "Starting IPFS upload for: $file"
    
    while [ $attempt -lt $MAX_RETRIES ]; do
        attempt=$((attempt + 1))
        log "INFO" "Upload attempt $attempt of $MAX_RETRIES for '$file'"
        
        if cid=$(ipfs add -Q "$file" 2>&1); then
            log "SUCCESS" "File uploaded successfully: $file -> CID: $cid"
            
            # Record CID and hash
            local file_hash=$(sha256sum "$file" | awk '{print $1}')
            echo "$(date '+%Y-%m-%d %H:%M:%S') | File: $file | CID: $cid | SHA256: $file_hash" >> "${CID_RECORD}"
            log "INFO" "Recorded CID and hash in ${CID_RECORD}"
            
            echo "$cid"
            return 0
        else
            log "WARNING" "Upload attempt $attempt failed for '$file': $cid"
            if [ $attempt -lt $MAX_RETRIES ]; then
                log "INFO" "Retrying in ${RETRY_DELAY} seconds..."
                sleep $RETRY_DELAY
            fi
        fi
    done
    
    log "ERROR" "Failed to upload '$file' after $MAX_RETRIES attempts"
    return 1
}

# Function to recursively scan and upload directory
process_directory() {
    local dir="$1"
    local file_count=0
    local success_count=0
    local fail_count=0
    
    log "INFO" "Starting recursive scan of directory: $dir"
    
    # Build find command with exclusions
    # Find all files excluding patterns defined above
    while IFS= read -r -d '' file; do
        file_count=$((file_count + 1))
        
        # Skip non-text files for signature check, but still upload them
        if file --mime-type "$file" | grep -q "text/"; then
            if check_lex_amoris_signature "$file"; then
                if upload_to_ipfs "$file"; then
                    success_count=$((success_count + 1))
                else
                    fail_count=$((fail_count + 1))
                fi
            else
                log "WARNING" "Skipping '$file' due to missing signature"
                fail_count=$((fail_count + 1))
            fi
        else
            # Upload binary files without signature check
            log "INFO" "Binary file detected, skipping signature check: $file"
            if upload_to_ipfs "$file"; then
                success_count=$((success_count + 1))
            else
                fail_count=$((fail_count + 1))
            fi
        fi
    done < <(find "$dir" -type f \( "${EXCLUDE_PATTERNS[@]}" \) -prune -o -type f -print0)
    
    log "INFO" "Processing complete. Total files: $file_count, Successful: $success_count, Failed: $fail_count"
    
    return 0
}

# Main execution
main() {
    log "INFO" "=== IPFS Automation Script Started ==="
    log "INFO" "Log file: ${LOG_FILE}"
    log "INFO" "CID records: ${CID_RECORD}"
    
    # Check if IPFS daemon is running
    if ! ipfs swarm peers > /dev/null 2>&1; then
        log "WARNING" "IPFS daemon not responding, attempting to start..."
        ipfs daemon &
        sleep 5
    fi
    
    # Process current directory or specified directory
    target_dir="${1:-.}"
    
    if [ ! -d "$target_dir" ]; then
        log "ERROR" "Directory not found: $target_dir"
        exit 1
    fi
    
    process_directory "$target_dir"
    
    log "INFO" "=== IPFS Automation Script Completed ==="
    log "INFO" "Check ${CID_RECORD} for all uploaded file CIDs"
}

# Run main function if script is executed directly
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi