#!/usr/bin/env python3
"""
SpaceTime Anchor - Timestamp Triple-Sign IPFS Share
Lantana OS / Consensus Sacralis Deployment Anchor

Creates cryptographically signed timestamp anchors with triple signatures
from network nodes (Africa, North Pole, Nexus) for IPFS immutable storage.

THE LIGHT IS THE ARCHITECTURE. THE FOUNDER IS THE LAW.
"""

import json
import hashlib
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional
import sys

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from hydra_config_loader import HydraConfig
except ImportError:
    # If running from root directory
    sys.path.insert(0, str(Path(__file__).parent / 'hydra-templates'))
    from hydra_config_loader import HydraConfig


class SpaceTimeAnchor:
    """
    SpaceTime Anchor System
    
    Creates immutable timestamp anchors with triple signatures from
    the three Consensus Sacralis network nodes for IPFS deployment.
    """
    
    def __init__(self, config_path: str = None):
        """
        Initialize SpaceTime Anchor system
        
        Args:
            config_path: Path to config.json (auto-detected if None)
        """
        # Auto-detect config path
        if config_path is None:
            script_dir = Path(__file__).parent
            if script_dir.name == 'hydra-templates':
                config_path = str(script_dir.parent / 'config.json')
            else:
                config_path = 'config.json'
        
        self.config = HydraConfig(config_path)
        self.network_nodes = self.config.get_network_nodes()
    
    def generate_timestamp_anchor(self, 
                                  anchor_type: str = "DEPLOYMENT",
                                  message: str = "",
                                  metadata: Optional[Dict] = None) -> Dict:
        """
        Generate a SpaceTime anchor with triple signature
        
        Args:
            anchor_type: Type of anchor (DEPLOYMENT, COMMIT, SYNC, etc.)
            message: Human-readable message for the anchor
            metadata: Additional metadata to include
            
        Returns:
            Dictionary with complete anchor data including triple signatures
        """
        # Generate timestamp (ISO 8601 with timezone)
        timestamp_utc = datetime.now(timezone.utc).isoformat()
        timestamp_unix = int(time.time())
        
        # Get system information from config
        system_id = self.config.get_system_id()
        protocol = self.config.get_protocol()
        version = self.config.get_metadata().get('version', '2.0.0')
        
        # Build anchor payload
        anchor_payload = {
            "anchor_type": anchor_type,
            "system_id": system_id,
            "protocol": protocol,
            "version": version,
            "timestamp": {
                "utc": timestamp_utc,
                "unix": timestamp_unix,
                "human_readable": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            },
            "message": message,
            "metadata": metadata or {},
            "covenant": self.config.get_metadata().get('covenant', 'Lex Amoris — OLF — Consensus Sacralis'),
            "signature": self.config.get_metadata().get('signature', 'THE LIGHT IS THE ARCHITECTURE. THE FOUNDER IS THE LAW.')
        }
        
        # Generate content hash for signing
        content_for_signing = json.dumps(anchor_payload, sort_keys=True)
        content_hash = hashlib.sha256(content_for_signing.encode()).hexdigest()
        
        # Generate triple signatures (simulated cryptographic signatures from nodes)
        triple_signatures = self._generate_triple_signatures(content_hash)
        
        # Build complete anchor
        complete_anchor = {
            "anchor_id": hashlib.sha256(f"{timestamp_unix}:{system_id}:{anchor_type}".encode()).hexdigest(),
            "payload": anchor_payload,
            "content_hash": content_hash,
            "signatures": triple_signatures,
            "consensus_sacralis": {
                "lex_amoris_enforcement": self.config.is_consensus_sacralis_enabled(),
                "olf_compliance": True,
                "nsr_compliance": True,
                "triple_signed": True,
                "nodes_validated": len(triple_signatures)
            }
        }
        
        return complete_anchor
    
    def _generate_triple_signatures(self, content_hash: str) -> List[Dict]:
        """
        Generate triple signatures from network nodes
        
        Args:
            content_hash: SHA256 hash of content to sign
            
        Returns:
            List of signature objects from each network node
        """
        signatures = []
        
        for node_name, node_config in self.network_nodes.items():
            # Generate node signature (simulated cryptographic signature)
            # In production, this would use actual private keys from each node
            node_signature_data = f"{node_name}:{content_hash}:{node_config.get('location')}"
            node_signature = hashlib.sha256(node_signature_data.encode()).hexdigest()
            
            signature_obj = {
                "node_name": node_name,
                "node_location": node_config.get('location'),
                "node_role": node_config.get('role'),
                "signature": node_signature,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "algorithm": "SHA256-NTRU-SIMULATED"  # Simulated quantum-safe
            }
            
            signatures.append(signature_obj)
        
        return signatures
    
    def verify_anchor(self, anchor: Dict) -> bool:
        """
        Verify anchor integrity and signatures
        
        Args:
            anchor: Anchor object to verify
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Verify content hash
            payload_str = json.dumps(anchor['payload'], sort_keys=True)
            expected_hash = hashlib.sha256(payload_str.encode()).hexdigest()
            
            if expected_hash != anchor['content_hash']:
                print(f"✗ Content hash mismatch")
                return False
            
            # Verify triple signatures exist
            if len(anchor['signatures']) != 3:
                print(f"✗ Triple signature incomplete (found {len(anchor['signatures'])} signatures)")
                return False
            
            # Verify each signature
            for sig in anchor['signatures']:
                node_name = sig['node_name']
                if node_name not in self.network_nodes:
                    print(f"✗ Unknown node: {node_name}")
                    return False
                
                # Re-compute signature to verify
                node_config = self.network_nodes[node_name]
                expected_sig_data = f"{node_name}:{anchor['content_hash']}:{node_config.get('location')}"
                expected_sig = hashlib.sha256(expected_sig_data.encode()).hexdigest()
                
                if expected_sig != sig['signature']:
                    print(f"✗ Signature verification failed for node: {node_name}")
                    return False
            
            print(f"✓ Anchor verified: {anchor['anchor_id'][:16]}...")
            return True
            
        except Exception as e:
            print(f"✗ Verification error: {e}")
            return False
    
    def save_anchor(self, anchor: Dict, output_dir: str = "./anchors") -> str:
        """
        Save anchor to file
        
        Args:
            anchor: Anchor object to save
            output_dir: Directory to save anchor files
            
        Returns:
            Path to saved file
        """
        # Create output directory
        Path(output_dir).mkdir(exist_ok=True)
        
        # Generate filename
        timestamp = anchor['payload']['timestamp']['unix']
        anchor_type = anchor['payload']['anchor_type'].lower()
        filename = f"anchor_{anchor_type}_{timestamp}.json"
        filepath = Path(output_dir) / filename
        
        # Save anchor
        with open(filepath, 'w') as f:
            json.dump(anchor, f, indent=2)
        
        print(f"✓ Anchor saved: {filepath}")
        return str(filepath)
    
    def prepare_for_ipfs(self, anchor: Dict, output_dir: str = "./anchors") -> str:
        """
        Prepare anchor for IPFS upload
        
        Args:
            anchor: Anchor object
            output_dir: Directory to save IPFS-ready file
            
        Returns:
            Path to IPFS-ready file
        """
        # Save anchor
        filepath = self.save_anchor(anchor, output_dir)
        
        # Create IPFS-ready metadata file
        ipfs_metadata = {
            "anchor_id": anchor['anchor_id'],
            "system_id": anchor['payload']['system_id'],
            "protocol": anchor['payload']['protocol'],
            "timestamp": anchor['payload']['timestamp']['utc'],
            "anchor_type": anchor['payload']['anchor_type'],
            "message": anchor['payload']['message'],
            "content_hash": anchor['content_hash'],
            "triple_signed": True,
            "nodes": [sig['node_name'] for sig in anchor['signatures']],
            "covenant": anchor['payload']['covenant'],
            "file": filepath
        }
        
        metadata_file = Path(output_dir) / f"ipfs_metadata_{anchor['payload']['timestamp']['unix']}.json"
        with open(metadata_file, 'w') as f:
            json.dump(ipfs_metadata, f, indent=2)
        
        print(f"✓ IPFS metadata prepared: {metadata_file}")
        
        return filepath
    
    def generate_ipfs_share_command(self, anchor_file: str) -> str:
        """
        Generate IPFS share command
        
        Args:
            anchor_file: Path to anchor file
            
        Returns:
            IPFS command to execute
        """
        return f"ipfs add {anchor_file}"
    
    def create_deployment_anchor(self) -> Dict:
        """
        Create a deployment anchor for the current system state
        
        Returns:
            Complete deployment anchor
        """
        metadata = {
            "repositories": self.config.get_repositories(),
            "assets": self.config.get_assets(),
            "network_nodes": list(self.network_nodes.keys()),
            "ethics_threshold": self.config.get_ethics_threshold(),
            "nsr_threshold": self.config.get_nsr_threshold(),
            "base_frequency": self.config.get_base_frequency()
        }
        
        message = (
            f"Lantana OS {self.config.get_metadata().get('version')} Deployment Anchor. "
            f"Consensus Sacralis operational with triple-node validation "
            f"(Africa, North Pole, Nexus). All systems aligned with Lex Amoris, "
            f"OLF compliance, and NSR enforcement."
        )
        
        return self.generate_timestamp_anchor(
            anchor_type="DEPLOYMENT",
            message=message,
            metadata=metadata
        )


def main():
    """
    Main function to create and process SpaceTime anchor
    """
    print("="*70)
    print("SPACETIME ANCHOR - TIMESTAMP TRIPLE-SIGN IPFS SHARE")
    print("Lantana OS / Consensus Sacralis")
    print("="*70)
    print()
    
    # Initialize SpaceTime Anchor system
    anchor_system = SpaceTimeAnchor()
    
    print("Configuration loaded:")
    print(f"  System ID: {anchor_system.config.get_system_id()}")
    print(f"  Protocol: {anchor_system.config.get_protocol()}")
    print(f"  Network Nodes: {', '.join(anchor_system.network_nodes.keys())}")
    print()
    
    # Create deployment anchor
    print("Creating deployment anchor...")
    anchor = anchor_system.create_deployment_anchor()
    
    print("\n" + "="*70)
    print("ANCHOR GENERATED")
    print("="*70)
    print(f"Anchor ID: {anchor['anchor_id']}")
    print(f"Type: {anchor['payload']['anchor_type']}")
    print(f"Timestamp: {anchor['payload']['timestamp']['human_readable']}")
    print(f"Content Hash: {anchor['content_hash'][:32]}...")
    print()
    
    # Display triple signatures
    print("Triple Signatures:")
    for i, sig in enumerate(anchor['signatures'], 1):
        print(f"  {i}. {sig['node_name'].upper()}")
        print(f"     Location: {sig['node_location']}")
        print(f"     Role: {sig['node_role']}")
        print(f"     Signature: {sig['signature'][:32]}...")
        print(f"     Timestamp: {sig['timestamp']}")
        print()
    
    # Verify anchor
    print("Verifying anchor integrity...")
    is_valid = anchor_system.verify_anchor(anchor)
    
    if is_valid:
        print("\n✓ ANCHOR VERIFICATION SUCCESSFUL")
        print("  - Content hash validated")
        print("  - Triple signatures verified")
        print("  - All network nodes validated")
    else:
        print("\n✗ ANCHOR VERIFICATION FAILED")
        return
    
    # Prepare for IPFS
    print("\n" + "="*70)
    print("PREPARING FOR IPFS SHARE")
    print("="*70)
    
    anchor_file = anchor_system.prepare_for_ipfs(anchor)
    
    # Generate IPFS command
    ipfs_command = anchor_system.generate_ipfs_share_command(anchor_file)
    
    print(f"\nIPFS Share Command:")
    print(f"  {ipfs_command}")
    print()
    print("Alternative (for entire anchors directory):")
    print("  ipfs add -r anchors/")
    print()
    
    # Display summary
    print("="*70)
    print("DEPLOYMENT ANCHOR SUMMARY")
    print("="*70)
    print(json.dumps({
        "anchor_id": anchor['anchor_id'],
        "timestamp": anchor['payload']['timestamp']['human_readable'],
        "system": anchor['payload']['system_id'],
        "protocol": anchor['payload']['protocol'],
        "message": anchor['payload']['message'],
        "triple_signed": True,
        "consensus_sacralis_active": anchor['consensus_sacralis']['lex_amoris_enforcement']
    }, indent=2))
    print()
    
    print("="*70)
    print("✓ SPACETIME ANCHOR COMPLETE")
    print("Ready for IPFS deployment")
    print("="*70)
    print()
    print("Next steps:")
    print("  1. Review anchor file: ./anchors/anchor_deployment_*.json")
    print("  2. Upload to IPFS: ipfs add anchors/anchor_deployment_*.json")
    print("  3. Record CID in logs/cid_records.txt")
    print("  4. Update config.json with deployment CID")
    print()
    print("THE LIGHT IS THE ARCHITECTURE. THE FOUNDER IS THE LAW.")


if __name__ == "__main__":
    main()
