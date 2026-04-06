# Complete Deployment Workflow Guide

## Lantana OS / Consensus Sacralis Deployment

This guide covers the complete deployment workflow integrating IPFS automation, Hydra multi-AI system, and SpaceTime Anchor verification.

---

### THE LIGHT IS THE ARCHITECTURE. THE FOUNDER IS THE LAW.

---

## Quick Start

### 1. Manual Deployment

```bash
# Run complete automated deployment
python3 automated_deployment.py

# This will:
# - Create SpaceTime anchor with triple signatures
# - Verify anchor integrity
# - Generate deployment report
# - Update CID records
```

### 2. GitHub Actions Deployment

Trigger via GitHub Actions:

**Manual Trigger**:
1. Go to Actions → Automated Deployment with SpaceTime Anchor
2. Click "Run workflow"
3. Select options:
   - Create SpaceTime Anchor: ✓
   - Upload to IPFS: ✓ (requires IPFS daemon)
4. Click "Run workflow"

**Automatic Trigger**:
- Pushes to `main` or `master` branch
- Changes to `config.json`, `hydra-templates/`, or `spacetime_anchor.py`

## Complete Workflow Steps

### Step 1: Configuration Validation

```bash
# Validate config.json
python3 -c "import json; json.load(open('config.json'))"

# Load and verify configuration
python3 hydra-templates/hydra_config_loader.py
```

**Output**:
```
✓ Configuration validated
✓ Configuration loaded from config.json
System ID: LANTANA-OS-2026
Protocol: Consensus Sacralis
Network Nodes: africa, north_pole, nexus
Consensus Sacralis: ✓ ENABLED
```

### Step 2: SpaceTime Anchor Generation

```bash
# Create deployment anchor
python3 spacetime_anchor.py
```

**Output**:
```
✓ Anchor verified: <anchor_id>
✓ ANCHOR VERIFICATION SUCCESSFUL
  - Content hash validated
  - Triple signatures verified
  - All network nodes validated
✓ Anchor saved: anchors/anchor_deployment_<timestamp>.json
✓ IPFS metadata prepared
```

### Step 3: IPFS Upload (Optional)

```bash
# Upload anchor to IPFS
ipfs add anchors/anchor_deployment_*.json

# Or upload entire anchors directory
ipfs add -r anchors/
```

**Output**:
```
added Qm... anchor_deployment_1769046420.json
```

### Step 4: Record CID

```bash
# Add to CID records
echo "$(date '+%Y-%m-%d %H:%M:%S') | Anchor: Qm... | Type: DEPLOYMENT" >> logs/cid_records.txt
```

### Step 5: Verify Deployment

```bash
# Run Hydra configured system
python3 hydra-templates/hydra_configured_example.py
```

**Verification Checklist**:
- [ ] Configuration loaded successfully
- [ ] All 3 network nodes initialized (Africa, North Pole, Nexus)
- [ ] Triple signatures verified
- [ ] Consensus Sacralis active
- [ ] Network health operational

## Automated Deployment

### Using automated_deployment.py

```bash
# Run complete workflow
python3 automated_deployment.py
```

**Features**:
- Creates SpaceTime anchor automatically
- Verifies triple signatures
- Updates CID records
- Generates deployment report

**Output Structure**:
```
anchors/
├── anchor_deployment_<timestamp>.json
└── ipfs_metadata_<timestamp>.json

reports/
└── deployment_report_<timestamp>.json

logs/
└── cid_records.txt (updated)
```

## GitHub Actions Integration

### Workflow: automated-deployment.yml

**Triggers**:
- Manual dispatch with options
- Push to main/master (on specific file changes)

**Steps**:
1. Checkout repository
2. Set up Python 3.10
3. Validate config.json
4. Load configuration
5. Create SpaceTime anchor
6. Run automated deployment
7. Upload artifacts
8. (Optional) Setup IPFS and upload
9. (Optional) Commit CID records
10. Create deployment summary

**Artifacts**:
- SpaceTime anchors (JSON files)
- Deployment reports
- Retention: 90 days

## Network Node Synchronization

### Testing Africa ↔ North Pole Synchronization

```bash
# Generate anchor
python3 spacetime_anchor.py

# Verify both validator nodes signed
grep -E "africa|north_pole" anchors/anchor_deployment_*.json

# Expected output:
# "node_name": "africa"
# "node_name": "north_pole"
```

**Synchronization Verification**:
1. Both nodes must have `status: "active"`
2. Both must have `role: "validator"`
3. Signatures must be cryptographically valid
4. Timestamps should be within sync interval

## Deployment Reports

### Report Structure

```json
{
  "deployment_timestamp": "2026-01-22 01:47:00 UTC",
  "system_id": "LANTANA-OS-2026",
  "protocol": "Consensus Sacralis",
  "anchor_id": "1b7a45593cd31d13...",
  "ipfs_automation": false,
  "triple_signatures": [
    {
      "node": "africa",
      "location": "Klimabaum-Africa",
      "role": "validator"
    },
    {
      "node": "north_pole",
      "location": "Klimabaum-North-Pole",
      "role": "validator"
    },
    {
      "node": "nexus",
      "location": "Central-Nexus",
      "role": "coordinator"
    }
  ],
  "consensus_sacralis": {
    "lex_amoris_enforcement": true,
    "olf_compliance": true,
    "nsr_compliance": true,
    "triple_signed": true,
    "nodes_validated": 3
  },
  "repositories": [...],
  "assets": {...},
  "network_nodes": [...]
}
```

## Integration with Existing Systems

### IPFS Automation Script

The SpaceTime anchor system integrates with `automate_ipfs_process.sh`:

```bash
# Enhanced automation includes anchor generation
./automate_ipfs_process.sh

# Then create anchor for the upload
python3 spacetime_anchor.py
```

### Hydra Multi-AI System

Anchors can be used to verify Hydra deployments:

```python
from spacetime_anchor import SpaceTimeAnchor
from hydra_configured_example import ConfiguredHydraSystem

# Create anchor before deployment
anchor_system = SpaceTimeAnchor()
anchor = anchor_system.create_deployment_anchor()

# Deploy Hydra system
hydra = ConfiguredHydraSystem()

# Anchor includes Hydra configuration snapshot
```

## Troubleshooting

### Anchor Generation Fails

**Issue**: `Configuration file not found`
**Solution**: Ensure `config.json` exists in root directory

**Issue**: `Triple signature verification failed`
**Solution**: Check network_nodes configuration in config.json

### IPFS Upload Fails

**Issue**: `ipfs: command not found`
**Solution**: Install IPFS: https://docs.ipfs.tech/install/

**Issue**: `IPFS daemon not running`
**Solution**: Start daemon: `ipfs daemon &`

### GitHub Actions Fails

**Issue**: `Permission denied`
**Solution**: Ensure workflow has `contents: write` permission

**Issue**: `Python module not found`
**Solution**: Check Python version is 3.10+ in workflow

## Best Practices

### 1. Always Verify Anchors

```bash
python3 -c "
from spacetime_anchor import SpaceTimeAnchor
import json

with open('anchors/anchor_deployment_*.json') as f:
    anchor = json.load(f)

system = SpaceTimeAnchor()
assert system.verify_anchor(anchor), 'Verification failed'
print('✓ Anchor verified')
"
```

### 2. Backup Anchors

```bash
# Backup before deployment
cp -r anchors/ anchors_backup_$(date +%Y%m%d)/
```

### 3. Monitor CID Records

```bash
# Check recent deployments
tail -20 logs/cid_records.txt
```

### 4. Validate Network Health

```bash
# Run health check
python3 hydra-templates/hydra_configured_example.py | grep "OPERATIONAL"
```

## Security Checklist

Before deployment, verify:

- [ ] config.json validated
- [ ] All 3 network nodes active
- [ ] Consensus Sacralis enabled
- [ ] Lex Amoris enforcement: ✓
- [ ] OLF compliance: ✓
- [ ] NSR compliance: ✓
- [ ] Triple signatures verified
- [ ] Content hash validated
- [ ] IPFS CID recorded
- [ ] No security vulnerabilities (CodeQL)

## Reference Commands

```bash
# Complete deployment
python3 automated_deployment.py

# Manual anchor creation
python3 spacetime_anchor.py

# Configuration validation
python3 hydra-templates/hydra_config_loader.py

# Hydra system test
python3 hydra-templates/hydra_configured_example.py

# IPFS upload
ipfs add -r anchors/

# View CID records
cat logs/cid_records.txt

# Check network status
grep "status.*active" config.json
```

## Support

For issues or questions:
- Check [SPACETIME_ANCHOR.md](SPACETIME_ANCHOR.md)
- Review [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
- See [COMMUNITY_FEEDBACK.md](COMMUNITY_FEEDBACK.md)

---

**Status**: OPERATIONAL  
**Version**: 2.0.0  
**Last Updated**: 2026-01-22

**Covenant**: Lex Amoris — OLF (One Love First) — Consensus Sacralis
