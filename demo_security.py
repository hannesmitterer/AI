#!/usr/bin/env python3
"""
AI Security Interface - Comprehensive Demo
===========================================

Demonstrates all three security components:
1. Adaptive Threat Logging
2. Optimized Log Population
3. Progressive Firewall Design
"""

from ai_security_interface import (
    AISecurityInterface, 
    AdaptiveThreatLogger,
    OptimizedLogManager,
    ProgressiveFirewall,
    ThreatType, 
    ThreatLevel
)
from eternal_security_integration import SecureEternalEngine
import time
import json


def demo_1_adaptive_threat_logging():
    """Demo 1: Adaptive Threat Logging System"""
    print("="*70)
    print("DEMO 1: ADAPTIVE THREAT LOGGING")
    print("="*70)
    print()
    
    logger = AdaptiveThreatLogger(max_logs=100)
    print()
    
    # Simulate various threats
    print("[DEMO] Logging different threat types...")
    print()
    
    threats = [
        (ThreatType.MALICIOUS_INPUT, ThreatLevel.HIGH, "192.168.1.100", "SQL injection detected"),
        (ThreatType.UNAUTHORIZED_ACCESS, ThreatLevel.MEDIUM, "192.168.1.101", "Failed authentication attempt"),
        (ThreatType.PATTERN_ANOMALY, ThreatLevel.LOW, "192.168.1.102", "Unusual traffic pattern"),
        (ThreatType.MALICIOUS_INPUT, ThreatLevel.HIGH, "192.168.1.100", "XSS attempt from same source"),
    ]
    
    for threat_type, level, source, desc in threats:
        threat_id = logger.log_threat(threat_type, level, source, desc)
        time.sleep(0.1)
    
    print()
    print("[DEMO] Adaptive Learning in Action:")
    print("  - First threat from 192.168.1.100 had score: 0.500")
    print("  - Second threat from same source had higher score (adaptive learning)")
    print()
    
    # Show recent threats
    recent = logger.get_recent_threats(count=3)
    print(f"[STATS] Total threats logged: {len(logger.threat_logs)}")
    print(f"[STATS] Recent threats: {len(recent)}")
    print()


def demo_2_optimized_log_management():
    """Demo 2: Optimized Log Population"""
    print("="*70)
    print("DEMO 2: OPTIMIZED LOG POPULATION")
    print("="*70)
    print()
    
    log_manager = OptimizedLogManager(rotation_size=10, compression_enabled=True)
    print()
    
    print("[DEMO] Populating logs to trigger rotation...")
    print()
    
    # Add logs to trigger rotation
    for i in range(12):
        log_entry = {
            "id": f"log_{i:03d}",
            "message": f"Test log entry {i}",
            "timestamp": time.time()
        }
        log_manager.populate_log(log_entry)
        
        if i == 9:
            print(f"  → Added {i+1} logs, approaching rotation threshold...")
        elif i == 10:
            print(f"  → Rotation triggered at {i+1} logs!")
    
    print()
    stats = log_manager.get_statistics()
    print("[STATS] Log Management Statistics:")
    print(f"  - Current logs: {stats['current_logs']}")
    print(f"  - Archived files: {stats['archived_files']}")
    print(f"  - Total rotations: {stats['rotations']}")
    print(f"  - Compression events: {stats['compressions']}")
    print()


def demo_3_progressive_firewall():
    """Demo 3: Progressive Firewall Design"""
    print("="*70)
    print("DEMO 3: PROGRESSIVE FIREWALL DESIGN")
    print("="*70)
    print()
    
    firewall = ProgressiveFirewall()
    print()
    
    print("[DEMO] Adding entries to blacklist...")
    print()
    
    # Add some blacklist entries
    firewall.add_to_blacklist(
        identifier="192.168.1.100",
        reason="Multiple attack attempts",
        threat_level=ThreatLevel.HIGH,
        is_permanent=False,
        expiry_hours=24
    )
    
    firewall.add_to_blacklist(
        identifier="10.0.0.50",
        reason="Critical security incident",
        threat_level=ThreatLevel.CRITICAL,
        is_permanent=True
    )
    
    # Add whitelist entry
    firewall.add_to_whitelist("192.168.1.200")
    
    print()
    print("[DEMO] Testing access control...")
    print()
    
    test_sources = [
        "192.168.1.100",  # Blacklisted
        "10.0.0.50",      # Permanently blacklisted
        "192.168.1.200",  # Whitelisted
        "192.168.1.150"   # Unknown (default allow)
    ]
    
    for source in test_sources:
        allowed, reason = firewall.check_access(source)
        status = "✓ ALLOWED" if allowed else "✗ BLOCKED"
        print(f"  {source:20s} → {status:12s} | {reason}")
    
    print()
    stats = firewall.get_statistics()
    print("[STATS] Firewall Statistics:")
    print(f"  - Blacklist entries: {stats['blacklist_entries']}")
    print(f"  - Whitelist entries: {stats['whitelist_entries']}")
    print(f"  - Blocked attempts: {stats['blocked_attempts']}")
    print(f"  - Allowed requests: {stats['allowed_requests']}")
    print(f"  - Block rate: {stats['block_rate']:.1%}")
    print()


def demo_4_integrated_security():
    """Demo 4: Integrated AI Security Interface"""
    print("="*70)
    print("DEMO 4: INTEGRATED AI SECURITY INTERFACE")
    print("="*70)
    print()
    
    security = AISecurityInterface()
    print()
    
    print("[DEMO] Processing requests through security pipeline...")
    print()
    
    # Simulate some requests
    requests = [
        ("legitimate_user", {"action": "read", "resource": "data"}),
        ("suspicious_user", {"action": "admin", "resource": "config"}),
        ("malicious_user", {"action": "delete", "resource": "all"}),
    ]
    
    for source, request_data in requests:
        # First request - should be allowed
        allowed, message = security.process_request(source, request_data)
        status = "✓" if allowed else "✗"
        print(f"  [{status}] {source:20s} → {message}")
        
        # Simulate threat detection for suspicious activity
        if "admin" in request_data.get("action", ""):
            security.detect_and_log_threat(
                threat_type=ThreatType.UNAUTHORIZED_ACCESS,
                threat_level=ThreatLevel.MEDIUM,
                source_identifier=source,
                description="Unauthorized admin action attempt"
            )
        
        if "delete" in request_data.get("action", ""):
            security.detect_and_log_threat(
                threat_type=ThreatType.MALICIOUS_INPUT,
                threat_level=ThreatLevel.CRITICAL,
                source_identifier=source,
                description="Attempted destructive action"
            )
    
    print()
    print("[DEMO] Synchronizing blacklist from threats...")
    added = security.synchronize_blacklist()
    print(f"  → Added {added} entries to blacklist")
    print()
    
    # Test access again after blacklist update
    print("[DEMO] Re-checking access after blacklist sync...")
    print()
    
    for source, _ in requests:
        allowed, reason = security.firewall.check_access(source)
        status = "✓ ALLOWED" if allowed else "✗ BLOCKED"
        print(f"  {source:20s} → {status:12s}")
    
    print()
    status = security.get_comprehensive_status()
    print("[STATS] Comprehensive Security Status:")
    print(f"  - Total threats: {status['threat_logs_count']}")
    print(f"  - High priority: {status['high_priority_threats']}")
    print(f"  - Blacklist size: {status['firewall']['blacklist_entries']}")
    print()


def demo_5_eternal_integration():
    """Demo 5: Integration with Eternal Deposition"""
    print("="*70)
    print("DEMO 5: ETERNAL DEPOSITION SECURITY INTEGRATION")
    print("="*70)
    print()
    
    engine = SecureEternalEngine(initial_nodes=30)
    print()
    
    print("[DEMO] Running secure eternal engine with monitoring...")
    print("  (Executing 10 cycles with security checks)")
    print()
    
    for i in range(10):
        metrics = engine.execute_cycle()
        
        if (i + 1) % 3 == 0:
            print(f"  [Cycle {metrics['cycle']:02d}] "
                  f"Energy: {metrics['avg_energy']:.3f} | "
                  f"Nodes: {metrics['nodes']:3d} | "
                  f"Threats: {metrics['security']['threats_detected']}")
        
        time.sleep(0.3)
    
    print()
    print("[DEMO] Security monitoring summary:")
    status = engine.get_security_status()
    metrics = status['security']['monitoring_metrics']
    
    print(f"  - Cycles monitored: {metrics['cycles_monitored']}")
    print(f"  - Anomalies detected: {metrics['anomalies_found']}")
    print(f"  - Threats logged: {metrics['threats_detected']}")
    print(f"  - Blacklist updates: {metrics['blacklist_updates']}")
    print()


def main():
    """Run all demos"""
    print("\n")
    print("*" * 70)
    print("*" + " " * 68 + "*")
    print("*" + " " * 15 + "AI SECURITY INTERFACE" + " " * 32 + "*")
    print("*" + " " * 20 + "COMPREHENSIVE DEMO" + " " * 31 + "*")
    print("*" + " " * 68 + "*")
    print("*" * 70)
    print("\n")
    
    try:
        demo_1_adaptive_threat_logging()
        time.sleep(1)
        
        demo_2_optimized_log_management()
        time.sleep(1)
        
        demo_3_progressive_firewall()
        time.sleep(1)
        
        demo_4_integrated_security()
        time.sleep(1)
        
        demo_5_eternal_integration()
        
    except KeyboardInterrupt:
        print("\n\n[DEMO] Interrupted by user")
    
    print()
    print("="*70)
    print("ALL DEMOS COMPLETE")
    print("="*70)
    print()
    print("For more information, see: AI_SECURITY_DOCUMENTATION.md")
    print()


if __name__ == "__main__":
    main()
