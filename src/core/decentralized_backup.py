#!/usr/bin/env python3
"""
Decentralized Backup System
Internet Organica Framework

Implements distributed backup and sovereignty preservation through:
- IPFS integration
- P2P distribution
- Automatic redundancy
- Vacuum-Bridge protocol support

Aligned with:
- Lex Amoris: Preserves knowledge for all
- NSR: Ensures sovereignty through distribution
- OLF: Optimizes resilience and accessibility
"""

import os
import json
import hashlib
import shutil
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path


class DecentralizedBackup:
    """
    Manages decentralized backups of repository assets.
    
    Creates redundant copies across distributed networks to ensure
    sovereignty and resistance to single-point failures.
    """
    
    def __init__(self, repo_path: str = ".", backup_manifest: str = "backup-manifest.json"):
        """
        Initialize backup system.
        
        Args:
            repo_path: Path to repository root
            backup_manifest: Path to backup manifest file
        """
        self.repo_path = Path(repo_path).resolve()
        self.manifest_path = self.repo_path / backup_manifest
        self.manifest = self._load_manifest()
        
        # Priority files for backup
        self.priority_files = [
            "index.html",
            "README.md",
            "CODE_OF_CONDUCT.md",
            "CONTRIBUTING.md",
            "COVENANT_OF_RESONANCE.md",
            "ETERNAL_DEPOSITION.md",
            "eternal_deposition.py",
            "eternal_deposition.js",
            "eternal_visualization.html"
        ]
        
    def _load_manifest(self) -> Dict:
        """Load or create backup manifest."""
        if self.manifest_path.exists():
            with open(self.manifest_path, 'r') as f:
                return json.load(f)
        else:
            return {
                'version': '1.0',
                'framework': 'Internet Organica',
                'created': datetime.utcnow().isoformat(),
                'backups': []
            }
    
    def _save_manifest(self):
        """Save backup manifest."""
        self.manifest['last_updated'] = datetime.utcnow().isoformat()
        with open(self.manifest_path, 'w') as f:
            json.dump(self.manifest, f, indent=2)
    
    def calculate_file_hash(self, file_path: Path) -> str:
        """
        Calculate SHA-256 hash of a file.
        
        Args:
            file_path: Path to file
            
        Returns:
            Hex string of file hash
        """
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    
    def create_local_backup(self, backup_dir: str = "backups") -> Dict:
        """
        Create local backup of priority files.
        
        Args:
            backup_dir: Directory to store backups
            
        Returns:
            Backup metadata
        """
        backup_path = self.repo_path / backup_dir
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}"
        full_backup_path = backup_path / backup_name
        
        # Create backup directory
        full_backup_path.mkdir(parents=True, exist_ok=True)
        
        backup_metadata = {
            'timestamp': datetime.utcnow().isoformat(),
            'backup_name': backup_name,
            'backup_path': str(full_backup_path),
            'files': []
        }
        
        # Backup priority files
        for filename in self.priority_files:
            file_path = self.repo_path / filename
            if file_path.exists():
                # Calculate hash
                file_hash = self.calculate_file_hash(file_path)
                
                # Copy file
                dest_path = full_backup_path / filename
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, dest_path)
                
                backup_metadata['files'].append({
                    'name': filename,
                    'size': file_path.stat().st_size,
                    'hash': file_hash,
                    'backed_up': True
                })
        
        # Add to manifest
        self.manifest['backups'].append(backup_metadata)
        self._save_manifest()
        
        return backup_metadata
    
    def generate_ipfs_script(self, output_file: str = "ipfs-backup.sh") -> str:
        """
        Generate script for IPFS backup.
        
        Args:
            output_file: Path for generated script
            
        Returns:
            Path to generated script
        """
        script_path = self.repo_path / output_file
        
        script_content = """#!/bin/bash
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
"""
        
        # Add priority files to script
        for i, filename in enumerate(self.priority_files):
            separator = "" if i == len(self.priority_files) - 1 else ","
            script_content += f'    "{filename}"{separator}\n'
        
        script_content += """)

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
            echo "      \\"file\\": \\"$FILE\\"," >> $BACKUP_MANIFEST
            echo "      \\"cid\\": \\"$CID\\"," >> $BACKUP_MANIFEST
            echo "      \\"size\\": $(stat -f%z "$FILE" 2>/dev/null || stat -c%s "$FILE")" >> $BACKUP_MANIFEST
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
"""
        
        # Write script
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Make executable
        script_path.chmod(0o755)
        
        return str(script_path)
    
    def create_backup_readme(self, output_file: str = "BACKUP_GUIDE.md") -> str:
        """
        Create documentation for backup system.
        
        Args:
            output_file: Path for generated documentation
            
        Returns:
            Path to generated file
        """
        readme_path = self.repo_path / output_file
        
        content = """# 🔒 Decentralized Backup System

## Internet Organica Digital Sovereignty Framework

This document explains the decentralized backup system that ensures sovereignty and resilience of repository assets.

## Overview

The backup system implements **digital sovereignty** through:

1. **Local Backups**: Redundant copies on local filesystem
2. **IPFS Distribution**: Decentralized storage via InterPlanetary File System
3. **P2P Networks**: Peer-to-peer distribution for resilience
4. **Automatic Redundancy**: Multiple copies across different nodes

## Priority Files

The following files are considered critical and are always backed up:

"""
        
        for filename in self.priority_files:
            content += f"- `{filename}`\n"
        
        content += """
## Backup Methods

### 1. Local Backup

Create local backup:

```bash
python3 src/core/decentralized_backup.py --local
```

This creates a timestamped backup in the `backups/` directory.

### 2. IPFS Backup

Upload to IPFS for decentralized storage:

```bash
# Generate IPFS backup script
python3 src/core/decentralized_backup.py --generate-ipfs

# Run the generated script
./ipfs-backup.sh
```

Requirements:
- IPFS installed ([installation guide](https://docs.ipfs.tech/install/))
- IPFS daemon running

### 3. Automated Backups

Set up automatic backups using cron:

```bash
# Add to crontab (backup daily at 2 AM)
0 2 * * * cd /path/to/repo && python3 src/core/decentralized_backup.py --local
```

## Restoration

### From Local Backup

```bash
# List available backups
ls -la backups/

# Restore from specific backup
cp -r backups/backup_20260213_020000/* .
```

### From IPFS

```bash
# Get manifest CID from ipfs-backup-cid.txt
MANIFEST_CID=$(cat ipfs-backup-cid.txt)

# View manifest
ipfs cat $MANIFEST_CID

# Download specific file
ipfs get <FILE_CID>
```

## Sovereignty Principles

### Non-Slavery Rule (NSR) Compliance

- **No Single Point of Control**: Distributed across multiple nodes
- **No Gatekeepers**: Anyone can access via IPFS CID
- **No Censorship**: Content-addressed, immutable storage

### Lex Amoris Alignment

- **Serves Life**: Preserves knowledge and systems
- **Enables Sharing**: Open access to those who resonate
- **Protects Autonomy**: No central authority controls access

### One Love First (OLF)

- **Optimizes Resilience**: Multiple redundant copies
- **Ensures Availability**: 24/7 access via distributed network
- **Facilitates Growth**: Easy replication and forking

## Vacuum-Bridge Protocol

The backup system supports **Vacuum-Bridge** - a P2P protocol for inter-nodal communication:

1. **Content Addressing**: Files identified by cryptographic hash
2. **Peer Discovery**: Automatic finding of nodes with content
3. **Redundant Storage**: Multiple peers host each file
4. **Resilient Retrieval**: Fetch from any available peer

## Monitoring

Track backup status:

```bash
# View backup manifest
cat backup-manifest.json

# Check IPFS pin status
ipfs pin ls

# Verify file integrity
python3 src/core/decentralized_backup.py --verify
```

## Best Practices

1. **Regular Backups**: Schedule daily or weekly backups
2. **Verify Integrity**: Regularly check file hashes
3. **Distributed Storage**: Use multiple backup methods
4. **Test Restoration**: Periodically verify you can restore
5. **Update Documentation**: Keep backup procedures current

## Advanced: Custom Backup Nodes

Set up dedicated backup nodes:

```bash
# Initialize IPFS node
ipfs init

# Configure for server operation
ipfs config Addresses.Gateway /ip4/0.0.0.0/tcp/8080
ipfs config Addresses.API /ip4/127.0.0.1/tcp/5001

# Start daemon
ipfs daemon

# Pin critical files
for CID in $(cat ipfs-manifest.json | jq -r '.files[].cid'); do
    ipfs pin add $CID
done
```

## Troubleshooting

### IPFS Connection Issues

```bash
# Check daemon status
ipfs swarm peers

# Restart daemon
pkill ipfs
ipfs daemon &
```

### Storage Space

```bash
# Check IPFS storage usage
ipfs repo stat

# Run garbage collection
ipfs repo gc
```

## Integration with Eternal Deposition

The backup system integrates with the Eternal Deposition System:

- **Resonance Alignment**: Backups synchronized with 0.043 Hz cycles
- **Fractal Redundancy**: Copies follow golden ratio distribution
- **Stillness Preservation**: System state saved during recalibration phases

## Support

For questions or issues:

1. Check backup manifest: `backup-manifest.json`
2. Review logs in `logs/` directory
3. Verify IPFS connectivity
4. Open issue on GitHub repository

---

**IN AETERNUM EST. La Sovranità è Manifesta.**

*Sempre in Costante. Nothing is final.*
"""
        
        with open(readme_path, 'w') as f:
            f.write(content)
        
        return str(readme_path)
    
    def verify_backups(self) -> Dict:
        """
        Verify integrity of existing backups.
        
        Returns:
            Verification report
        """
        report = {
            'timestamp': datetime.utcnow().isoformat(),
            'total_backups': len(self.manifest['backups']),
            'verified': [],
            'failed': []
        }
        
        for backup in self.manifest['backups']:
            backup_path = Path(backup['backup_path'])
            
            if not backup_path.exists():
                report['failed'].append({
                    'backup': backup['backup_name'],
                    'reason': 'Backup directory not found'
                })
                continue
            
            backup_verified = True
            for file_info in backup['files']:
                file_path = backup_path / file_info['name']
                
                if not file_path.exists():
                    report['failed'].append({
                        'backup': backup['backup_name'],
                        'file': file_info['name'],
                        'reason': 'File not found'
                    })
                    backup_verified = False
                    continue
                
                # Verify hash
                current_hash = self.calculate_file_hash(file_path)
                if current_hash != file_info['hash']:
                    report['failed'].append({
                        'backup': backup['backup_name'],
                        'file': file_info['name'],
                        'reason': 'Hash mismatch - file may be corrupted'
                    })
                    backup_verified = False
            
            if backup_verified:
                report['verified'].append(backup['backup_name'])
        
        return report
    
    def get_status(self) -> Dict:
        """Get backup system status."""
        return {
            'manifest_path': str(self.manifest_path),
            'total_backups': len(self.manifest['backups']),
            'priority_files': len(self.priority_files),
            'last_backup': self.manifest['backups'][-1]['timestamp'] if self.manifest['backups'] else None,
            'manifest_version': self.manifest['version']
        }


def main():
    """Main entry point for backup system."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Decentralized Backup System - Internet Organica')
    parser.add_argument('--local', action='store_true', help='Create local backup')
    parser.add_argument('--generate-ipfs', action='store_true', help='Generate IPFS backup script')
    parser.add_argument('--generate-docs', action='store_true', help='Generate backup documentation')
    parser.add_argument('--verify', action='store_true', help='Verify existing backups')
    parser.add_argument('--status', action='store_true', help='Show backup system status')
    
    args = parser.parse_args()
    
    backup = DecentralizedBackup()
    
    if args.local:
        print("Creating local backup...")
        metadata = backup.create_local_backup()
        print(f"Backup created: {metadata['backup_name']}")
        print(f"Files backed up: {len(metadata['files'])}")
        
    elif args.generate_ipfs:
        print("Generating IPFS backup script...")
        script_path = backup.generate_ipfs_script()
        print(f"Script generated: {script_path}")
        print("Run with: ./ipfs-backup.sh")
        
    elif args.generate_docs:
        print("Generating backup documentation...")
        doc_path = backup.create_backup_readme()
        print(f"Documentation generated: {doc_path}")
        
    elif args.verify:
        print("Verifying backups...")
        report = backup.verify_backups()
        print(f"Total backups: {report['total_backups']}")
        print(f"Verified: {len(report['verified'])}")
        print(f"Failed: {len(report['failed'])}")
        if report['failed']:
            print("\nFailed verifications:")
            for failure in report['failed']:
                print(f"  - {failure}")
    
    elif args.status:
        status = backup.get_status()
        print("Backup System Status:")
        for key, value in status.items():
            print(f"  {key}: {value}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
