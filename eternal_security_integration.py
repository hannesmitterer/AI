#!/usr/bin/env python3
"""
Eternal Deposition Security Integration
========================================

Integrates AI Security Interface with Eternal Deposition System
for continuous security monitoring and adaptive threat management.
"""

from eternal_deposition import EternalDepositionEngine, Node
from ai_security_interface import (
    AISecurityInterface, ThreatType, ThreatLevel
)
from typing import Dict, Optional
import time
import json
from datetime import datetime


class SecureEternalEngine(EternalDepositionEngine):
    """
    Extended Eternal Deposition Engine with integrated security monitoring.
    
    Adds security features:
    - Continuous threat monitoring during cycles
    - Adaptive blacklist updates
    - Security-aware node management
    """
    
    def __init__(self, initial_nodes: int = 144):
        """
        Initialize secure eternal engine.
        
        Args:
            initial_nodes: Initial number of nodes
        """
        super().__init__(initial_nodes)
        
        # Initialize security interface
        self.security = AISecurityInterface()
        
        # Security metrics
        self.security_metrics = {
            "cycles_monitored": 0,
            "threats_detected": 0,
            "anomalies_found": 0,
            "blacklist_updates": 0
        }
        
        print("[SECURE ENGINE] Security integration active")
    
    def monitor_cycle_security(self, metrics: Dict) -> None:
        """
        Monitor security during each cycle.
        
        Detects anomalies in system behavior that could indicate threats.
        
        Args:
            metrics: Cycle metrics to analyze
        """
        self.security_metrics["cycles_monitored"] += 1
        
        # Check for anomalous energy levels
        if metrics["avg_energy"] < 0.1 or metrics["avg_energy"] > 0.95:
            self.security.detect_and_log_threat(
                threat_type=ThreatType.PATTERN_ANOMALY,
                threat_level=ThreatLevel.MEDIUM,
                source_identifier=f"cycle_{metrics['cycle']}",
                description=f"Anomalous energy level detected: {metrics['avg_energy']:.4f}",
                auto_blacklist=False
            )
            self.security_metrics["anomalies_found"] += 1
        
        # Check for rapid node growth (potential resource abuse)
        if metrics["nodes"] > self.security_metrics.get("last_node_count", 144) * 2:
            self.security.detect_and_log_threat(
                threat_type=ThreatType.RESOURCE_ABUSE,
                threat_level=ThreatLevel.LOW,
                source_identifier=f"cycle_{metrics['cycle']}",
                description=f"Rapid node growth detected: {metrics['nodes']} nodes",
                auto_blacklist=False
            )
        
        self.security_metrics["last_node_count"] = metrics["nodes"]
        
        # Periodic blacklist synchronization (every 50 cycles)
        if metrics["cycle"] % 50 == 0 and metrics["cycle"] > 0:
            added = self.security.synchronize_blacklist()
            self.security_metrics["blacklist_updates"] += added
            
            if added > 0:
                print(f"[SECURITY SYNC] Updated blacklist with {added} entries at cycle {metrics['cycle']}")
    
    def execute_cycle(self) -> Dict:
        """
        Execute cycle with security monitoring.
        
        Returns:
            Enhanced metrics including security data
        """
        # Execute base cycle
        metrics = super().execute_cycle()
        
        # Add security monitoring
        self.monitor_cycle_security(metrics)
        
        # Enhance metrics with security data
        metrics["security"] = {
            "threats_detected": self.security_metrics["threats_detected"],
            "anomalies_found": self.security_metrics["anomalies_found"],
            "blacklist_size": len(self.security.firewall.blacklist)
        }
        
        return metrics
    
    def validate_node_access(self, node_id: str) -> bool:
        """
        Validate if a node should have access based on security rules.
        
        Args:
            node_id: Node identifier to validate
            
        Returns:
            True if access allowed, False otherwise
        """
        allowed, reason = self.security.firewall.check_access(node_id)
        
        if not allowed:
            print(f"[SECURITY] Node access denied: {node_id} - {reason}")
        
        return allowed
    
    def report_security_incident(self,
                                incident_type: ThreatType,
                                severity: ThreatLevel,
                                description: str,
                                source: Optional[str] = None) -> str:
        """
        Report a security incident during operation.
        
        Args:
            incident_type: Type of incident
            severity: Severity level
            description: Description of incident
            source: Optional source identifier
            
        Returns:
            Incident ID
        """
        source_id = source or f"engine_cycle_{self.cycle_count}"
        
        incident_id = self.security.detect_and_log_threat(
            threat_type=incident_type,
            threat_level=severity,
            source_identifier=source_id,
            description=description,
            auto_blacklist=(severity == ThreatLevel.CRITICAL)
        )
        
        self.security_metrics["threats_detected"] += 1
        
        return incident_id
    
    def get_security_status(self) -> Dict:
        """Get comprehensive security status."""
        base_status = self.get_status()
        security_status = self.security.get_comprehensive_status()
        
        return {
            **base_status,
            "security": {
                **security_status,
                "monitoring_metrics": self.security_metrics
            }
        }
    
    def save_secure_state(self, filepath: str = "secure_eternal_state.json") -> None:
        """Save state including security data."""
        # Save base state
        super().save_state(filepath)
        
        # Save security state
        self.security.export_security_state(".")
        
        # Save security metrics
        with open("security_metrics.json", 'w') as f:
            json.dump(self.security_metrics, f, indent=2)
        
        print(f"[SECURE STATE] Saved complete state with security data")


class SecurityMonitoredDemo:
    """Demonstration of secure eternal engine."""
    
    @staticmethod
    def run_basic_security_demo():
        """Run basic security monitoring demonstration."""
        print("="*70)
        print("SECURE ETERNAL DEPOSITION - BASIC DEMO")
        print("="*70)
        print()
        
        # Initialize secure engine
        engine = SecureEternalEngine(initial_nodes=50)
        print()
        
        # Run for limited cycles with security monitoring
        print("[DEMO] Running 30 cycles with security monitoring...")
        print()
        
        for i in range(30):
            metrics = engine.execute_cycle()
            
            # Display status every 10 cycles
            if metrics["cycle"] % 10 == 0:
                print(f"[CYCLE {metrics['cycle']:03d}] "
                      f"Energy: {metrics['avg_energy']:.4f} | "
                      f"Nodes: {metrics['nodes']} | "
                      f"Threats: {metrics['security']['threats_detected']}")
            
            # Simulate security incident
            if i == 15:
                engine.report_security_incident(
                    incident_type=ThreatType.PATTERN_ANOMALY,
                    severity=ThreatLevel.HIGH,
                    description="Simulated security incident for demo"
                )
            
            # Wait for next cycle
            time.sleep(0.5)  # Reduced for demo
        
        print()
        print("[DEMO] Security monitoring complete")
        print()
        
        # Display final security status
        status = engine.get_security_status()
        print("Final Security Status:")
        print(json.dumps(status["security"]["monitoring_metrics"], indent=2))
        print()
        
        # Save secure state
        engine.save_secure_state()
        
        print("="*70)
        print("DEMO COMPLETE")
        print("="*70)
    
    @staticmethod
    def run_threat_response_demo():
        """Demonstrate threat detection and response."""
        print("="*70)
        print("THREAT DETECTION & RESPONSE DEMO")
        print("="*70)
        print()
        
        engine = SecureEternalEngine(initial_nodes=30)
        print()
        
        # Simulate various threats
        print("[DEMO] Simulating threat scenarios...")
        print()
        
        threats = [
            (ThreatType.MALICIOUS_INPUT, ThreatLevel.HIGH, "Malicious pattern detected"),
            (ThreatType.UNAUTHORIZED_ACCESS, ThreatLevel.MEDIUM, "Unauthorized node access attempt"),
            (ThreatType.RESOURCE_ABUSE, ThreatLevel.LOW, "Resource usage spike"),
            (ThreatType.DATA_EXFILTRATION, ThreatLevel.CRITICAL, "Data exfiltration attempt")
        ]
        
        for i, (threat_type, level, desc) in enumerate(threats):
            incident_id = engine.report_security_incident(
                incident_type=threat_type,
                severity=level,
                description=desc,
                source=f"test_source_{i}"
            )
            print(f"  [{i+1}] {threat_type.value} - {level.value} - ID: {incident_id}")
            time.sleep(0.2)
        
        print()
        print("[DEMO] Testing firewall responses...")
        print()
        
        # Test firewall for the critical threat source
        test_sources = ["test_source_0", "test_source_3", "safe_source"]
        
        for source in test_sources:
            allowed, reason = engine.security.firewall.check_access(source)
            status = "✓ ALLOWED" if allowed else "✗ BLOCKED"
            print(f"  {source}: {status} - {reason}")
        
        print()
        
        # Display firewall statistics
        fw_stats = engine.security.firewall.get_statistics()
        print("Firewall Statistics:")
        print(json.dumps(fw_stats, indent=2))
        print()
        
        print("="*70)
        print("DEMO COMPLETE")
        print("="*70)


def main():
    """Main entry point for demonstrations."""
    print("\n")
    
    # Run basic security demo
    SecurityMonitoredDemo.run_basic_security_demo()
    
    print("\n" + "="*70 + "\n")
    time.sleep(2)
    
    # Run threat response demo
    SecurityMonitoredDemo.run_threat_response_demo()


if __name__ == "__main__":
    main()
