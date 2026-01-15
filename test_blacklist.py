#!/usr/bin/env python3
"""
Test script for EUYSTACIO Permanent Blacklist System
Validates core functionality and integration with Eternal Deposition Engine
"""

import os
import sys
import time

# Import blacklist system
from euystacio_blacklist import (
    get_blacklist, 
    block_node, 
    block_ip, 
    block_identifier,
    is_node_blocked,
    is_ip_blocked,
    is_identifier_blocked,
    ThreatLevel,
    EntityType
)

# Import eternal deposition engine
from eternal_deposition import EternalDepositionEngine

def cleanup_test_files():
    """Clean up test files from previous runs."""
    test_files = [
        "euystacio_blacklist.json",
        "euystacio_blacklist_audit.log",
        "eternal_state.json"
    ]
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"[CLEANUP] Removed {file}")

def test_basic_blacklist_operations():
    """Test basic blacklist add/check/remove operations."""
    print("\n" + "="*70)
    print("TEST 1: Basic Blacklist Operations")
    print("="*70)
    
    # Test adding nodes
    print("\n[TEST] Adding test nodes to blacklist...")
    result1 = block_node("test_node_001", "Test malicious node", ThreatLevel.HIGH)
    result2 = block_node("test_node_002", "Test suspicious node", ThreatLevel.MEDIUM)
    
    assert result1 == True, "Failed to add first node"
    assert result2 == True, "Failed to add second node"
    print("✓ Successfully added 2 nodes")
    
    # Test duplicate addition
    print("\n[TEST] Testing duplicate addition...")
    result3 = block_node("test_node_001", "Duplicate", ThreatLevel.LOW)
    assert result3 == False, "Should reject duplicate"
    print("✓ Correctly rejected duplicate entry")
    
    # Test checking blocked status
    print("\n[TEST] Checking blocked status...")
    assert is_node_blocked("test_node_001") == True, "Node should be blocked"
    assert is_node_blocked("test_node_999") == False, "Node should not be blocked"
    print("✓ Blocked status checks working correctly")
    
    # Test adding different entity types
    print("\n[TEST] Adding different entity types...")
    block_ip("192.168.1.100", "Test malicious IP", ThreatLevel.CRITICAL)
    block_identifier("AI_TEST_ENTITY", "Test AI entity", ThreatLevel.HIGH)
    
    assert is_ip_blocked("192.168.1.100") == True
    assert is_identifier_blocked("AI_TEST_ENTITY") == True
    print("✓ Multiple entity types working correctly")
    
    # Test statistics
    print("\n[TEST] Getting statistics...")
    stats = get_blacklist().get_statistics()
    print(f"Total entries: {stats['total_entries']}")
    print(f"Nodes: {stats['by_type']['node']}")
    print(f"IPs: {stats['by_type']['ip_address']}")
    print(f"Identifiers: {stats['by_type']['identifier']}")
    
    assert stats['total_entries'] == 4, "Should have 4 total entries"
    assert stats['by_type']['node'] == 2, "Should have 2 nodes"
    assert stats['by_type']['ip_address'] == 1, "Should have 1 IP"
    assert stats['by_type']['identifier'] == 1, "Should have 1 identifier"
    print("✓ Statistics working correctly")
    
    print("\n[RESULT] ✓ All basic blacklist tests passed!")
    return True

def test_persistence():
    """Test that blacklist persists to disk."""
    print("\n" + "="*70)
    print("TEST 2: Blacklist Persistence")
    print("="*70)
    
    print("\n[TEST] Checking if blacklist file was created...")
    assert os.path.exists("euystacio_blacklist.json"), "Blacklist file not created"
    print("✓ Blacklist file exists")
    
    print("\n[TEST] Checking if audit log was created...")
    assert os.path.exists("euystacio_blacklist_audit.log"), "Audit log not created"
    print("✓ Audit log exists")
    
    # Verify audit log has content
    with open("euystacio_blacklist_audit.log", 'r') as f:
        log_content = f.read()
        assert len(log_content) > 0, "Audit log is empty"
        assert "ADD" in log_content, "Audit log missing ADD entries"
    print("✓ Audit log contains expected entries")
    
    print("\n[RESULT] ✓ All persistence tests passed!")
    return True

def test_eternal_deposition_integration():
    """Test integration with Eternal Deposition Engine."""
    print("\n" + "="*70)
    print("TEST 3: Eternal Deposition Engine Integration")
    print("="*70)
    
    print("\n[TEST] Initializing engine with blacklist enabled...")
    engine = EternalDepositionEngine(initial_nodes=10, enable_blacklist=True)
    
    status = engine.get_status()
    assert status['blacklist_enabled'] == True, "Blacklist should be enabled"
    print("✓ Engine initialized with blacklist enabled")
    print(f"  Initial nodes: {status['nodes']}")
    print(f"  Blocked attempts: {status['blocked_attempts']}")
    
    # Add some of the engine's nodes to blacklist
    print("\n[TEST] Blacklisting some nodes...")
    block_node("node_0001", "Test blocking engine node", ThreatLevel.HIGH)
    block_node("node_0002", "Test blocking engine node", ThreatLevel.MEDIUM)
    
    # Run optimization which should validate and filter nodes
    print("\n[TEST] Running network optimization (should trigger security sweep)...")
    engine.optimize_network()
    
    # Check that blocked nodes were removed
    assert "node_0001" not in engine.nodes, "Blacklisted node should be removed"
    assert "node_0002" not in engine.nodes, "Blacklisted node should be removed"
    print("✓ Blacklisted nodes removed from network")
    
    # Check status again
    status = engine.get_status()
    print(f"  Remaining nodes: {status['nodes']}")
    
    print("\n[TEST] Testing node validation...")
    allowed = engine.is_node_allowed("node_0003")
    blocked = engine.is_node_allowed("node_0001")
    
    assert allowed == True, "Non-blacklisted node should be allowed"
    assert blocked == False, "Blacklisted node should not be allowed"
    print("✓ Node validation working correctly")
    
    print("\n[RESULT] ✓ All integration tests passed!")
    return True

def test_misp_integration():
    """Test MISP trigger integration."""
    print("\n" + "="*70)
    print("TEST 4: MISP Integration")
    print("="*70)
    
    print("\n[TEST] Adding entries with MISP triggers...")
    block_node(
        "misp_test_node",
        "MISP-triggered block",
        ThreatLevel.CRITICAL,
        misp_trigger="MISP_TRAFFIC_ANOMALY"
    )
    
    block_ip(
        "10.0.0.100",
        "MISP IP reputation",
        ThreatLevel.HIGH,
        misp_trigger="MISP_IP_REPUTATION"
    )
    
    # Get statistics
    stats = get_blacklist().get_statistics()
    print(f"  Entries with MISP triggers: {stats['with_misp_trigger']}")
    assert stats['with_misp_trigger'] >= 2, "Should have MISP-triggered entries"
    print("✓ MISP triggers recorded correctly")
    
    # Verify entry details
    entry = get_blacklist().get_entry("misp_test_node", EntityType.NODE)
    assert entry is not None, "Entry should exist"
    assert entry.misp_trigger == "MISP_TRAFFIC_ANOMALY", "MISP trigger should match"
    print("✓ MISP trigger details preserved")
    
    print("\n[RESULT] ✓ All MISP integration tests passed!")
    return True

def test_threat_levels():
    """Test different threat levels."""
    print("\n" + "="*70)
    print("TEST 5: Threat Level Classification")
    print("="*70)
    
    print("\n[TEST] Adding entries with different threat levels...")
    block_node("low_threat", "Low severity", ThreatLevel.LOW)
    block_node("medium_threat", "Medium severity", ThreatLevel.MEDIUM)
    block_node("high_threat", "High severity", ThreatLevel.HIGH)
    block_node("critical_threat", "Critical severity", ThreatLevel.CRITICAL)
    
    stats = get_blacklist().get_statistics()
    print(f"  Low: {stats['by_threat_level']['low']}")
    print(f"  Medium: {stats['by_threat_level']['medium']}")
    print(f"  High: {stats['by_threat_level']['high']}")
    print(f"  Critical: {stats['by_threat_level']['critical']}")
    
    assert stats['by_threat_level']['low'] >= 1
    assert stats['by_threat_level']['medium'] >= 1
    assert stats['by_threat_level']['high'] >= 1
    assert stats['by_threat_level']['critical'] >= 1
    print("✓ All threat levels working correctly")
    
    print("\n[RESULT] ✓ All threat level tests passed!")
    return True

def run_all_tests():
    """Run all tests."""
    print("\n" + "="*70)
    print("EUYSTACIO PERMANENT BLACKLIST - TEST SUITE")
    print("="*70)
    print(f"Start time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Clean up from previous runs
    cleanup_test_files()
    
    # Run tests
    tests = [
        ("Basic Operations", test_basic_blacklist_operations),
        ("Persistence", test_persistence),
        ("Engine Integration", test_eternal_deposition_integration),
        ("MISP Integration", test_misp_integration),
        ("Threat Levels", test_threat_levels),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
        except Exception as e:
            print(f"\n[ERROR] Test '{test_name}' failed with exception:")
            print(f"  {type(e).__name__}: {e}")
            failed += 1
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests passed: {passed}/{len(tests)}")
    print(f"Tests failed: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n✓ ALL TESTS PASSED!")
        print("\nBlacklist system is fully operational and ready for deployment.")
    else:
        print(f"\n✗ {failed} test(s) failed")
        print("Please review errors above.")
    
    print(f"\nEnd time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Clean up test files after successful run
    if failed == 0:
        print("\n[CLEANUP] Removing test files...")
        cleanup_test_files()
        print("[CLEANUP] Test environment cleaned")
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
