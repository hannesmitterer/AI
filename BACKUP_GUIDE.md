# 🔒 Decentralized Backup System

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

- `index.html`
- `README.md`
- `CODE_OF_CONDUCT.md`
- `CONTRIBUTING.md`
- `COVENANT_OF_RESONANCE.md`
- `ETERNAL_DEPOSITION.md`
- `eternal_deposition.py`
- `eternal_deposition.js`
- `eternal_visualization.html`

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
