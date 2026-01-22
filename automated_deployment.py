#!/usr/bin/env python3
"""
Automated Deployment with SpaceTime Anchor
Integrates IPFS automation with SpaceTime Anchor generation

THE LIGHT IS THE ARCHITECTURE. THE FOUNDER IS THE LAW.
"""

import subprocess
import json
import sys
from pathlib import Path
from datetime import datetime

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent))
from spacetime_anchor import SpaceTimeAnchor


def run_ipfs_automation(directory: str = ".") -> bool:
    """
    Run IPFS automation script
    
    Args:
        directory: Directory to upload
        
    Returns:
        True if successful, False otherwise
    """
    script_path = Path(__file__).parent / "automate_ipfs_process.sh"
    
    if not script_path.exists():
        print(f"✗ IPFS automation script not found: {script_path}")
        return False
    
    print("Running IPFS automation...")
    try:
        result = subprocess.run(
            [str(script_path), directory],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        
        if result.returncode == 0:
            print("✓ IPFS automation completed")
            return True
        else:
            print(f"✗ IPFS automation failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ IPFS automation timed out")
        return False
    except Exception as e:
        print(f"✗ IPFS automation error: {e}")
        return False


def create_deployment_anchor() -> dict:
    """
    Create SpaceTime anchor for deployment
    
    Returns:
        Anchor dictionary
    """
    print("\nCreating SpaceTime deployment anchor...")
    anchor_system = SpaceTimeAnchor()
    anchor = anchor_system.create_deployment_anchor()
    
    # Verify anchor
    if anchor_system.verify_anchor(anchor):
        print("✓ Anchor created and verified")
        
        # Save anchor
        anchor_file = anchor_system.prepare_for_ipfs(anchor)
        print(f"✓ Anchor saved: {anchor_file}")
        
        return anchor
    else:
        print("✗ Anchor verification failed")
        return None


def update_cid_records(anchor: dict, ipfs_cid: str = None):
    """
    Update CID records with anchor information
    
    Args:
        anchor: Anchor dictionary
        ipfs_cid: IPFS CID if anchor was uploaded
    """
    log_file = Path("logs/cid_records.txt")
    log_file.parent.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    anchor_id = anchor['anchor_id'][:16]
    
    if ipfs_cid:
        entry = f"{timestamp} | Anchor: {anchor_id}... | CID: {ipfs_cid} | Type: DEPLOYMENT\n"
    else:
        entry = f"{timestamp} | Anchor: {anchor_id}... | Status: GENERATED | Type: DEPLOYMENT\n"
    
    with open(log_file, 'a') as f:
        f.write(entry)
    
    print(f"✓ CID records updated: {log_file}")


def generate_deployment_report(anchor: dict, ipfs_success: bool):
    """
    Generate deployment report
    
    Args:
        anchor: Anchor dictionary
        ipfs_success: Whether IPFS upload was successful
    """
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = report_dir / f"deployment_report_{timestamp}.json"
    
    report = {
        "deployment_timestamp": anchor['payload']['timestamp']['human_readable'],
        "system_id": anchor['payload']['system_id'],
        "protocol": anchor['payload']['protocol'],
        "anchor_id": anchor['anchor_id'],
        "ipfs_automation": ipfs_success,
        "triple_signatures": [
            {
                "node": sig['node_name'],
                "location": sig['node_location'],
                "role": sig['node_role']
            }
            for sig in anchor['signatures']
        ],
        "consensus_sacralis": anchor['consensus_sacralis'],
        "repositories": anchor['payload']['metadata'].get('repositories', []),
        "assets": anchor['payload']['metadata'].get('assets', {}),
        "network_nodes": anchor['payload']['metadata'].get('network_nodes', [])
    }
    
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"✓ Deployment report: {report_file}")


def main():
    """
    Main automated deployment workflow
    """
    print("="*70)
    print("AUTOMATED DEPLOYMENT WITH SPACETIME ANCHOR")
    print("Lantana OS / Consensus Sacralis")
    print("="*70)
    print()
    
    # Step 1: Create SpaceTime Anchor
    anchor = create_deployment_anchor()
    if not anchor:
        print("\n✗ Deployment failed: Could not create anchor")
        sys.exit(1)
    
    # Step 2: Run IPFS automation (optional, requires IPFS daemon)
    print("\n" + "="*70)
    print("IPFS AUTOMATION")
    print("="*70)
    print("Note: IPFS automation requires IPFS daemon running")
    print("Skipping automatic IPFS upload (run manually if needed)")
    ipfs_success = False
    
    # Uncomment to enable automatic IPFS upload:
    # ipfs_success = run_ipfs_automation()
    
    # Step 3: Update records
    update_cid_records(anchor)
    
    # Step 4: Generate report
    generate_deployment_report(anchor, ipfs_success)
    
    # Summary
    print("\n" + "="*70)
    print("DEPLOYMENT SUMMARY")
    print("="*70)
    print(f"Anchor ID: {anchor['anchor_id'][:32]}...")
    print(f"Timestamp: {anchor['payload']['timestamp']['human_readable']}")
    print(f"System: {anchor['payload']['system_id']}")
    print(f"Protocol: {anchor['payload']['protocol']}")
    print(f"Triple Signatures: ✓ VERIFIED")
    print(f"  - Africa: {anchor['signatures'][0]['node_location']}")
    print(f"  - North Pole: {anchor['signatures'][1]['node_location']}")
    print(f"  - Nexus: {anchor['signatures'][2]['node_location']}")
    print()
    print("Next steps:")
    print("  1. Upload anchor to IPFS: ipfs add anchors/anchor_deployment_*.json")
    print("  2. Record CID in logs/cid_records.txt")
    print("  3. Update config.json with deployment CID")
    print("  4. Verify node synchronization between Africa and North Pole")
    print()
    print("="*70)
    print("✓ AUTOMATED DEPLOYMENT COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()
