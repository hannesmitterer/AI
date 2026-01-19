#!/usr/bin/env python3
"""
EUYSTACIO Permanent Blacklist - Interactive Demo
Demonstrates the security features of the permanent blacklist system
"""

import time
from euystacio_blacklist import (
    get_blacklist,
    block_node,
    block_ip,
    block_identifier,
    ThreatLevel,
    EntityType
)
from eternal_deposition import EternalDepositionEngine

def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def print_section(text):
    """Print a formatted section."""
    print("\n" + "-"*70)
    print(f"  {text}")
    print("-"*70)

def demo_scenario_1():
    """Scenario 1: Detecting and blocking a malicious node."""
    print_header("SCENARIO 1: Malicious Node Detection")
    
    print("A suspicious node has been detected exhibiting abnormal behavior:")
    print("  Node ID: node_malicious_042")
    print("  Behavior: Abnormal traffic patterns, data exfiltration attempt")
    print("  Risk Level: HIGH")
    
    print("\n[ACTION] Adding node to permanent blacklist...")
    time.sleep(1)
    
    block_node(
        node_id="node_malicious_042",
        reason="Abnormal traffic pattern and data exfiltration attempt detected",
        threat_level=ThreatLevel.HIGH,
        misp_trigger="MISP_TRAFFIC_ANOMALY"
    )
    
    print("\n[RESULT] Node successfully blacklisted!")
    print("  ✓ All future communication from this node will be blocked")
    print("  ✓ Node will be removed from active network during next optimization")
    print("  ✓ Event logged in audit trail with MISP correlation")

def demo_scenario_2():
    """Scenario 2: Blocking upstream malicious IPs."""
    print_header("SCENARIO 2: Upstream IP Reputation Blocking")
    
    print("MISP intelligence feed reports compromised IP addresses:")
    print("  IP: 192.168.100.50 - Known botnet controller")
    print("  IP: 10.0.50.100 - Malware distribution server")
    print("  Risk Level: CRITICAL")
    
    print("\n[ACTION] Adding IPs to permanent blacklist...")
    time.sleep(1)
    
    block_ip(
        ip_address="192.168.100.50",
        reason="Known botnet controller from MISP threat feed",
        threat_level=ThreatLevel.CRITICAL,
        misp_trigger="MISP_IP_REPUTATION"
    )
    
    block_ip(
        ip_address="10.0.50.100",
        reason="Malware distribution server identified by MISP",
        threat_level=ThreatLevel.CRITICAL,
        misp_trigger="MISP_IP_REPUTATION"
    )
    
    print("\n[RESULT] IP addresses successfully blacklisted!")
    print("  ✓ All traffic from these IPs will be rejected")
    print("  ✓ ECOSYSTEM TESTING state protection active")
    print("  ✓ Permanent protection across system restarts")

def demo_scenario_3():
    """Scenario 3: AI entity compromise detection."""
    print_header("SCENARIO 3: AI Entity Policy Violation")
    
    print("AI monitoring system detected compromised entity:")
    print("  Entity ID: AI_ROGUE_ENTITY_7")
    print("  Issue: Suspected role compromise, unauthorized actions")
    print("  Risk Level: HIGH")
    
    print("\n[ACTION] Adding entity to permanent blacklist...")
    time.sleep(1)
    
    block_identifier(
        identifier="AI_ROGUE_ENTITY_7",
        reason="Suspected AI role compromise with unauthorized action patterns",
        threat_level=ThreatLevel.HIGH,
        misp_trigger="MISP_AI_POLICY_VIOLATION"
    )
    
    print("\n[RESULT] AI entity successfully blacklisted!")
    print("  ✓ Entity blocked from all system interactions")
    print("  ✓ KEY INT_MISP_POLICY_TRIGGER recorded")
    print("  ✓ Prevents future compromise attempts")

def demo_integration_with_engine():
    """Demonstrate integration with Eternal Deposition Engine."""
    print_header("INTEGRATION: Eternal Deposition Engine")
    
    print("Initializing Eternal Deposition Engine with blacklist protection...")
    time.sleep(1)
    
    engine = EternalDepositionEngine(initial_nodes=20, enable_blacklist=True)
    
    print("\n[STATUS] Engine initialized with security protection active")
    status = engine.get_status()
    print(f"  Nodes: {status['nodes']}")
    print(f"  Blacklist: {'ENABLED' if status['blacklist_enabled'] else 'DISABLED'}")
    print(f"  Blocked attempts: {status['blocked_attempts']}")
    
    print("\n[SCENARIO] Malicious node attempts to join network...")
    print("  Node ID: node_0005 (previously blacklisted)")
    time.sleep(1)
    
    # Block the node
    block_node("node_0005", "Malicious node attempting to rejoin", ThreatLevel.HIGH)
    
    print("\n[ACTION] Running network optimization cycle...")
    time.sleep(1)
    engine.optimize_network()
    
    status = engine.get_status()
    print("\n[RESULT] Security sweep complete!")
    print(f"  Remaining nodes: {status['nodes']}")
    print(f"  Blocked attempts: {status['blocked_attempts']}")
    print("  ✓ Blacklisted node was automatically removed")
    print("  ✓ Network integrity maintained")

def show_statistics():
    """Display comprehensive blacklist statistics."""
    print_header("BLACKLIST STATISTICS & MONITORING")
    
    blacklist = get_blacklist()
    stats = blacklist.get_statistics()
    
    print("Current Blacklist Status:")
    print(f"  Total entries: {stats['total_entries']}")
    
    print_section("By Entity Type")
    print(f"  Nodes (NODE):       {stats['by_type']['node']}")
    print(f"  IPs (IP_ADDRESS):   {stats['by_type']['ip_address']}")
    print(f"  Identifiers (ID):   {stats['by_type']['identifier']}")
    
    print_section("By Threat Level")
    print(f"  Low:                {stats['by_threat_level']['low']}")
    print(f"  Medium:             {stats['by_threat_level']['medium']}")
    print(f"  High:               {stats['by_threat_level']['high']}")
    print(f"  Critical:           {stats['by_threat_level']['critical']}")
    
    print_section("MISP Integration")
    print(f"  MISP-triggered:     {stats['with_misp_trigger']}")
    
    print("\n" + "="*70)
    print("Detailed Blacklist Entries:")
    print("="*70)
    
    for entry in blacklist.get_all_entries():
        print(f"\n[{entry.threat_level.value.upper()}] {entry.entity_type.value}: {entry.entity_id}")
        print(f"  Reason: {entry.reason}")
        print(f"  Added: {entry.timestamp}")
        if entry.misp_trigger:
            print(f"  MISP Trigger: {entry.misp_trigger}")

def main():
    """Run the complete demonstration."""
    print("\n")
    print("="*70)
    print(" "*10 + "EUYSTACIO PERMANENT BLACKLIST SYSTEM")
    print(" "*15 + "Interactive Security Demo")
    print("="*70)
    print("\nThis demo shows how the permanent blacklist protects the EUYSTACIO")
    print("framework from malicious nodes, IPs, and compromised AI entities.")
    print("\nPress Ctrl+C at any time to stop the demo.")
    
    try:
        # Run demonstration scenarios
        demo_scenario_1()
        time.sleep(2)
        
        demo_scenario_2()
        time.sleep(2)
        
        demo_scenario_3()
        time.sleep(2)
        
        demo_integration_with_engine()
        time.sleep(2)
        
        show_statistics()
        
        # Final summary
        print_header("DEMO COMPLETE")
        print("The permanent blacklist system is now protecting your EUYSTACIO")
        print("framework from the following threats:")
        print("  ✓ Malicious network nodes")
        print("  ✓ Compromised upstream IP addresses")
        print("  ✓ Rogue AI entities and identifiers")
        print("\nKey Features Demonstrated:")
        print("  ✓ Permanent persistence across restarts")
        print("  ✓ Real-time blocking and network protection")
        print("  ✓ MISP policy trigger integration")
        print("  ✓ Comprehensive audit trail")
        print("  ✓ Automatic security sweeps")
        print("\nBlacklist Storage: euystacio_blacklist.json")
        print("Audit Log: euystacio_blacklist_audit.log")
        print("\n" + "="*70)
        
    except KeyboardInterrupt:
        print("\n\n[DEMO] Interrupted by user")
        print("Blacklist remains active and protecting the system.")
    
    print("\n")

if __name__ == "__main__":
    main()
