#!/usr/bin/env python3
"""
Security Integration for Eternal Deposition System
==================================================

Integrates the security framework with the Eternal Deposition Engine,
providing protection against artificial threats while maintaining
the system's operational integrity.
"""

import time
from typing import Dict, Optional
from eternal_deposition import EternalDepositionEngine, Node
from security_framework import (
    SecurityFramework, 
    ThreatLevel, 
    AttackType
)


class SecureEternalDepositionEngine(EternalDepositionEngine):
    """
    Enhanced Eternal Deposition Engine with integrated security.
    
    Extends the base engine with:
    - Request validation through security framework
    - Node access control
    - Attack detection and mitigation
    - Security event monitoring
    """
    
    def __init__(self, 
                 initial_nodes: int = 144,
                 enable_security: bool = True,
                 security_log_file: str = "eternal_security.json"):
        """
        Initialize secure eternal deposition engine.
        
        Args:
            initial_nodes: Initial number of nodes
            enable_security: Whether to enable security framework
            security_log_file: Path to security log file
        """
        # Initialize base engine
        super().__init__(initial_nodes=initial_nodes)
        
        # Initialize security framework
        self.security = SecurityFramework(
            log_file=security_log_file,
            max_requests_per_minute=100,  # Higher limit for operational nodes
            blacklist_duration=7200  # 2 hours default
        )
        self.security.enabled = enable_security
        
        print(f"[SECURITY] Framework initialized (enabled: {enable_security})")
    
    def validate_node_access(self, 
                            node_id: str, 
                            operation: str = "read") -> bool:
        """
        Validate access to a node through security framework.
        
        Args:
            node_id: Identifier of the node being accessed
            operation: Type of operation (read/write/execute)
            
        Returns:
            True if access allowed, False otherwise
        """
        if not self.security.enabled:
            return True
        
        # Use node_id as entity_id for security checks
        resource_path = f"/node/{node_id}/{operation}"
        
        # Get node energy level safely
        node = self.nodes.get(node_id)
        energy_level = node.energy_level if node else 0.0
        
        allowed, reason = self.security.process_request(
            entity_id=node_id,
            resource_path=resource_path,
            behavior={
                "energy_level": energy_level,
                "operation": operation,
                "cycle": self.cycle_count
            }
        )
        
        if not allowed:
            print(f"[SECURITY] Access denied for {node_id}: {reason}")
        
        return allowed
    
    def secure_execute_cycle(self) -> Dict:
        """
        Execute cycle with security checks.
        
        Returns:
            Dictionary containing cycle metrics including security stats
        """
        # Perform security cleanup periodically
        if self.cycle_count % 50 == 0:
            self.security.cleanup()
        
        # Execute normal cycle
        metrics = super().execute_cycle()
        
        # Add security metrics
        security_status = self.security.get_security_status()
        metrics["security"] = {
            "blacklisted_nodes": security_status["blacklist"]["total_entries"],
            "total_attacks": security_status["attack_analytics"]["total_attacks"],
            "blocked_attacks": security_status["attack_analytics"]["blocked_attacks"]
        }
        
        return metrics
    
    def get_comprehensive_status(self) -> Dict:
        """Get status including security information."""
        base_status = super().get_status()
        security_status = self.security.get_security_status()
        
        return {
            **base_status,
            "security": security_status
        }


class SecurityConfig:
    """
    Configuration management for security framework.
    
    Provides centralized configuration for all security components.
    """
    
    DEFAULT_CONFIG = {
        "threat_detection": {
            "max_requests_per_minute": 60,
            "blacklist_duration": 3600,
            "anomaly_threshold": 0.75
        },
        "scan_detection": {
            "scan_threshold": 10,
            "time_window": 60,
            "honeypot_paths": [
                "/admin", "/.env", "/config", "/backup",
                "/.git/config", "/wp-admin", "/phpmyadmin",
                "/debug", "/test", "/.aws/credentials"
            ]
        },
        "attack_logging": {
            "log_file": "attack_log.json",
            "max_events": 10000
        },
        "integration": {
            "enable_security": True,
            "periodic_cleanup_interval": 50,
            "node_access_validation": True
        }
    }
    
    @classmethod
    def get_config(cls) -> Dict:
        """Get default configuration."""
        return cls.DEFAULT_CONFIG.copy()
    
    @classmethod
    def create_security_framework(cls, config: Optional[Dict] = None) -> SecurityFramework:
        """
        Create a security framework instance from configuration.
        
        Args:
            config: Optional custom configuration (uses defaults if None)
            
        Returns:
            Configured SecurityFramework instance
        """
        if config is None:
            config = cls.DEFAULT_CONFIG
        
        threat_config = config.get("threat_detection", {})
        scan_config = config.get("scan_detection", {})
        log_config = config.get("attack_logging", {})
        
        framework = SecurityFramework(
            log_file=log_config.get("log_file", "attack_log.json"),
            max_requests_per_minute=threat_config.get("max_requests_per_minute", 60),
            blacklist_duration=threat_config.get("blacklist_duration", 3600)
        )
        
        # Configure scan detector
        framework.scan_detector.honeypot_paths.update(
            scan_config.get("honeypot_paths", [])
        )
        
        return framework


def demo_secure_engine():
    """Demonstrate the secure eternal deposition engine."""
    print("=" * 70)
    print("SECURE ETERNAL DEPOSITION SYSTEM")
    print("Perpetual Logic with Integrated Security")
    print("=" * 70)
    print()
    
    # Create secure engine
    engine = SecureEternalDepositionEngine(
        initial_nodes=144,
        enable_security=True
    )
    
    # Simulate some cycles with security
    print("\nRunning 10 secure cycles...\n")
    
    for i in range(10):
        metrics = engine.secure_execute_cycle()
        
        if i % 2 == 0:
            print(f"[CYCLE {metrics['cycle']:04d}] "
                  f"Nodes: {metrics['nodes']} | "
                  f"Energy: {metrics['avg_energy']:.4f} | "
                  f"Blacklisted: {metrics['security']['blacklisted_nodes']}")
        
        # Simulate some node access attempts
        if i % 3 == 0:
            node_id = f"node_{(i*10) % 144:04d}"
            allowed = engine.validate_node_access(node_id, "read")
            if not allowed:
                print(f"[SECURITY] Access denied for {node_id}")
        
        time.sleep(0.5)
    
    # Get comprehensive status
    print("\n" + "=" * 70)
    status = engine.get_comprehensive_status()
    
    print("SYSTEM STATUS:")
    print(f"- Status: {status['status']}")
    print(f"- Cycles: {status['cycle_count']}")
    print(f"- Nodes: {status['nodes']}")
    print(f"- Average Energy: {status['avg_energy']:.4f}")
    
    print("\nSECURITY STATUS:")
    print(f"- Framework Enabled: {status['security']['enabled']}")
    print(f"- Blacklisted Entities: {status['security']['blacklist']['total_entries']}")
    print(f"- Total Attacks: {status['security']['attack_analytics']['total_attacks']}")
    print(f"- Blocked Attacks: {status['security']['attack_analytics']['blocked_attacks']}")
    
    if status['security']['attack_analytics']['total_attacks'] > 0:
        print(f"- Block Rate: {status['security']['attack_analytics']['block_rate']:.2%}")
    
    print("=" * 70)


if __name__ == "__main__":
    demo_secure_engine()
