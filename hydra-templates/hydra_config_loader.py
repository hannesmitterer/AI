#!/usr/bin/env python3
"""
Hydra System Configuration Loader
Loads and validates the config.json for Lantana OS and Hydra integration

THE LIGHT IS THE ARCHITECTURE. THE FOUNDER IS THE LAW.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional


class HydraConfig:
    """
    Configuration manager for the Hydra Multi-AI Resonance System
    
    Loads configuration from config.json and provides validated access
    to system parameters for IPFS automation, Byzantine consensus,
    ethical decision-making, and resonance coordination.
    """
    
    def __init__(self, config_path: str = "config.json"):
        """
        Initialize configuration loader
        
        Args:
            config_path: Path to config.json file
        """
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self.load_config()
    
    def load_config(self) -> None:
        """Load and validate configuration from JSON file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        try:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
            
            self._validate_config()
            print(f"✓ Configuration loaded from {self.config_path}")
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file: {e}")
    
    def _validate_config(self) -> None:
        """Validate required configuration sections"""
        required_sections = [
            'system_id',
            'protocol',
            'base_frequency',
            'ethics_engine',
            'hydra_system',
            'ipfs_automation'
        ]
        
        for section in required_sections:
            if section not in self.config:
                raise ValueError(f"Missing required configuration section: {section}")
        
        # Validate ethics engine
        ethics = self.config['ethics_engine']
        if ethics.get('nsr_validation') != 'enabled':
            print("Warning: NSR validation is not enabled")
        
        if ethics.get('lex_amoris_seal') != 'active':
            print("Warning: Lex Amoris seal is not active")
        
        print("✓ Configuration validated")
    
    def get_system_id(self) -> str:
        """Get system identifier"""
        return self.config.get('system_id', 'UNKNOWN')
    
    def get_protocol(self) -> str:
        """Get consensus protocol name"""
        return self.config.get('protocol', 'Unknown Protocol')
    
    def get_base_frequency(self) -> float:
        """Get base resonance frequency in Hz"""
        freq_str = self.config.get('base_frequency', '0.043Hz')
        return float(freq_str.replace('Hz', ''))
    
    def get_ethics_threshold(self) -> float:
        """Get ethics approval threshold"""
        return self.config.get('ethics_engine', {}).get('threshold', 0.85)
    
    def get_nsr_threshold(self) -> float:
        """Get NSR violation threshold"""
        return self.config.get('hydra_system', {}).get('nsr_validator', {}).get('violation_threshold', 0.3)
    
    def get_repositories(self) -> list:
        """Get list of managed repositories"""
        return self.config.get('repositories', [])
    
    def get_assets(self) -> Dict[str, str]:
        """Get IPFS asset mappings"""
        return self.config.get('assets', {})
    
    def get_ipfs_gateway(self) -> str:
        """Get IPFS gateway URL"""
        return self.config.get('deployment', {}).get('gateway', 'https://ipfs.io/ipfs/')
    
    def get_automation_script(self) -> str:
        """Get automation script path"""
        return self.config.get('deployment', {}).get('automation_script', 'automate_ipfs_process.sh')
    
    def get_hydra_consensus_config(self) -> Dict[str, Any]:
        """Get Byzantine consensus configuration"""
        return self.config.get('hydra_system', {}).get('consensus', {})
    
    def get_resonance_config(self) -> Dict[str, Any]:
        """Get resonance coordination configuration"""
        return self.config.get('hydra_system', {}).get('resonance', {})
    
    def get_ethical_framework_config(self) -> Dict[str, Any]:
        """Get ethical decision framework configuration"""
        return self.config.get('hydra_system', {}).get('ethical_framework', {})
    
    def get_ipfs_automation_config(self) -> Dict[str, Any]:
        """Get IPFS automation configuration"""
        return self.config.get('ipfs_automation', {})
    
    def get_network_nodes(self) -> Dict[str, Any]:
        """Get network node configuration"""
        return self.config.get('network_nodes', {})
    
    def is_consensus_sacralis_enabled(self) -> bool:
        """Check if Consensus Sacralis is fully enabled"""
        cs = self.config.get('consensus_sacralis', {})
        return (
            cs.get('lex_amoris_enforcement', False) and
            cs.get('olf_compliance', False) and
            cs.get('nsr_compliance', False)
        )
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get system metadata"""
        return self.config.get('metadata', {})
    
    def print_summary(self) -> None:
        """Print configuration summary"""
        print("\n" + "="*60)
        print("HYDRA SYSTEM CONFIGURATION SUMMARY")
        print("="*60)
        print(f"System ID: {self.get_system_id()}")
        print(f"Protocol: {self.get_protocol()}")
        print(f"Base Frequency: {self.get_base_frequency()} Hz")
        print(f"Ethics Threshold: {self.get_ethics_threshold()}")
        print(f"NSR Threshold: {self.get_nsr_threshold()}")
        print(f"Repositories: {len(self.get_repositories())}")
        print(f"Assets: {len(self.get_assets())}")
        print(f"Network Nodes: {len(self.get_network_nodes())}")
        print(f"Consensus Sacralis: {'✓ ENABLED' if self.is_consensus_sacralis_enabled() else '✗ DISABLED'}")
        
        metadata = self.get_metadata()
        print(f"\nVersion: {metadata.get('version', 'Unknown')}")
        print(f"Status: {metadata.get('status', 'Unknown')}")
        print(f"Signature: {metadata.get('signature', 'None')}")
        print("="*60 + "\n")
    
    def export_for_hydra_system(self) -> Dict[str, Any]:
        """
        Export configuration in format suitable for HydraSystem initialization
        
        Returns:
            Dictionary with configuration parameters for Hydra components
        """
        return {
            'system_id': self.get_system_id(),
            'protocol': self.get_protocol(),
            'resonance_frequency': self.get_base_frequency(),
            'ethics_threshold': self.get_ethics_threshold(),
            'nsr_threshold': self.get_nsr_threshold(),
            'consensus_config': self.get_hydra_consensus_config(),
            'resonance_config': self.get_resonance_config(),
            'ethical_framework': self.get_ethical_framework_config(),
            'ipfs_config': self.get_ipfs_automation_config(),
            'network_nodes': self.get_network_nodes()
        }


def validate_configuration(config_path: str = "config.json") -> bool:
    """
    Validate configuration file
    
    Args:
        config_path: Path to config.json
        
    Returns:
        True if valid, False otherwise
    """
    try:
        config = HydraConfig(config_path)
        config.print_summary()
        
        # Additional validation checks
        if not config.is_consensus_sacralis_enabled():
            print("⚠ WARNING: Consensus Sacralis is not fully enabled")
            print("  Lex Amoris enforcement, OLF compliance, and NSR compliance are required")
            return False
        
        print("✓ Configuration is valid and ready for deployment")
        return True
        
    except Exception as e:
        print(f"✗ Configuration validation failed: {e}")
        return False


# Example usage
if __name__ == "__main__":
    import os
    
    # Look for config.json in parent directory if running from hydra-templates
    script_dir = Path(__file__).parent
    if script_dir.name == 'hydra-templates':
        config_path = script_dir.parent / 'config.json'
    else:
        config_path = 'config.json'
    
    print("="*60)
    print("LANTANA OS / HYDRA SYSTEM")
    print("Configuration Validation and Loading")
    print("="*60)
    print()
    
    # Validate configuration
    if validate_configuration(str(config_path)):
        print("\n✓ System ready for initialization")
        print("\nTo use in your code:")
        print("  from hydra_config_loader import HydraConfig")
        print("  config = HydraConfig('config.json')")
        print("  hydra_params = config.export_for_hydra_system()")
    else:
        print("\n✗ Configuration validation failed")
        print("Please review config.json and ensure all required settings are correct")
        sys.exit(1)
