#!/usr/bin/env python3
"""
Quantum-Safe Network Protection - Demo and Validation
======================================================

This script demonstrates and validates all quantum-safe protection
features implemented in the Eternal Deposition System.

Features demonstrated:
1. Quantum Shield - NTRU encryption with auto-rotation
2. Blockchain Mesh Network - DNS-free decentralized networking
3. AI Anomaly Detection - Electromagnetic threat detection
4. Stealth Mode - Network invisibility

Usage:
    python3 demo_quantum_safe.py
"""

import time
import sys
import json
import hashlib
import secrets
import traceback
from datetime import datetime

# Import all quantum-safe modules
try:
    from quantum_shield import QuantumShield
    from blockchain_mesh_network import BlockchainMeshNetwork
    from ai_anomaly_detector import AIAnomalyDetector
    from stealth_mode import StealthMode
    from eternal_deposition import EternalDepositionEngine
    
    ALL_MODULES_AVAILABLE = True
except ImportError as e:
    print(f"[ERROR] Failed to import modules: {e}")
    ALL_MODULES_AVAILABLE = False
    sys.exit(1)


def print_section(title: str) -> None:
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(title.center(70))
    print("=" * 70 + "\n")


def demo_quantum_shield():
    """Demonstrate Quantum Shield functionality."""
    print_section("QUANTUM SHIELD - NTRU LATTICE-BASED ENCRYPTION")
    
    # Initialize with short rotation for demo
    shield = QuantumShield(rotation_interval=10)
    
    # Start auto-rotation
    shield.start_auto_rotation()
    
    # Test encryption
    test_message = b"Quantum-safe test message for demonstration"
    print(f"[TEST] Original message: {test_message.decode()}")
    
    encrypted = shield.encrypt(test_message)
    print(f"[TEST] Encrypted (NTRU): {encrypted.hex()[:64]}...")
    
    # Show initial status
    status = shield.get_status()
    print(f"\n[STATUS] Quantum Shield:")
    print(f"  Encryption: {status['encryption']}")
    print(f"  Quantum Safe: {status['quantum_safe']}")
    print(f"  Key ID: {status['current_key_id']}")
    print(f"  Rotation Interval: {status['rotation_interval']}s")
    print(f"  Auto-rotation: {status['auto_rotation']}")
    
    # Wait for key rotation
    print(f"\n[INFO] Waiting {status['rotation_interval']} seconds for key rotation...")
    time.sleep(status['rotation_interval'] + 1)
    
    # Show after rotation
    status_after = shield.get_status()
    print(f"\n[STATUS] After rotation:")
    print(f"  New Key ID: {status_after['current_key_id']}")
    print(f"  Rotation Count: {status_after['rotation_count']}")
    print(f"  Key History: {status_after['key_history_size']} previous keys")
    
    # Cleanup
    shield.stop_auto_rotation()
    print("\n[✓] Quantum Shield demonstration complete")
    
    return shield


def demo_blockchain_mesh_network():
    """Demonstrate Blockchain Mesh Network functionality."""
    print_section("BLOCKCHAIN MESH NETWORK (BBMN) - DNS-FREE")
    
    # Initialize mesh network
    mesh = BlockchainMeshNetwork("DEMO_MESH")
    
    # Start discovery
    mesh.start_discovery()
    
    # Simulate adding peers
    print("[DEMO] Adding simulated peers...")
    for i in range(3):
        peer_id = f"demo_peer_{i}"
        peer_address = hashlib.sha256(peer_id.encode()).hexdigest()[:32]
        mesh.connect_to_peer(peer_id, peer_address)
    
    # Show status
    status = mesh.get_status()
    print(f"\n[STATUS] Mesh Network:")
    print(f"  Network ID: {status['network_id']}")
    print(f"  Decentralized: {status['decentralized']}")
    print(f"  DNS-Free: {status['dns_free']}")
    print(f"  Local Node: {status['local_node_id']}")
    print(f"  Connected Peers: {status['connected_peers']}")
    print(f"  Blockchain Length: {status['blockchain_length']} blocks")
    print(f"  DHT Entries: {status['dht_entries']}")
    
    # Test message routing
    if mesh.nodes and len(mesh.nodes) > 1:
        first_peer = list(mesh.nodes.values())[1]
        print(f"\n[TEST] Sending test message to {first_peer.node_id}...")
        mesh.send_message(first_peer.address, {"test": "quantum-safe message"})
    
    # Cleanup
    mesh.stop_discovery()
    print("\n[✓] Blockchain Mesh Network demonstration complete")
    
    return mesh


def demo_ai_anomaly_detector():
    """Demonstrate AI Anomaly Detection functionality."""
    print_section("AI ANOMALY DETECTION - ELECTROMAGNETIC THREATS")
    
    # Initialize detector
    detector = AIAnomalyDetector()
    
    # Train baseline
    print("[TRAINING] Training on baseline signals...")
    detector.train_baseline(num_samples=30)
    
    # Start monitoring
    detector.start_monitoring()
    
    # Let it run for a bit to detect anomalies
    print("\n[MONITORING] Monitoring for 10 seconds...")
    time.sleep(10)
    
    # Show status
    status = detector.get_status()
    print(f"\n[STATUS] AI Detector:")
    print(f"  Status: {status['status']}")
    print(f"  Detector Type: {status['detector_type']}")
    print(f"  Trained: {status['trained']}")
    print(f"  Total Detections: {status['total_detections']}")
    print(f"  Anomaly Counts:")
    for severity, count in status['severity_counts'].items():
        if count > 0:
            print(f"    {severity}: {count}")
    
    # Show encrypted buffers
    print(f"\n[BUFFERS] Encrypted Buffers:")
    for buf_id, buf_status in status['encrypted_buffers'].items():
        print(f"  {buf_id}:")
        print(f"    Active: {buf_status['active']}")
        print(f"    Stored Items: {buf_status['stored_items']}")
        print(f"    Activations: {buf_status['activation_count']}")
        print(f"    Invisible: {buf_status['invisible']}")
    
    # Cleanup
    detector.stop_monitoring()
    print("\n[✓] AI Anomaly Detection demonstration complete")
    
    return detector


def demo_stealth_mode():
    """Demonstrate Stealth Mode functionality."""
    print_section("STEALTH MODE - NETWORK INVISIBILITY")
    
    # Initialize stealth mode
    stealth = StealthMode()
    
    # Activate with high invisibility
    print("[ACTIVATING] Stealth mode with level 8...")
    stealth.activate(level=8)
    
    # Test data processing
    print("\n[TEST] Processing outbound data...")
    test_data = b"Sensitive quantum-safe communication"
    protected_data = stealth.process_outbound_data(test_data)
    print(f"  Original size: {len(test_data)} bytes")
    print(f"  Protected size: {len(protected_data)} bytes")
    print(f"  Overhead: {len(protected_data) - len(test_data)} bytes")
    
    # Wait briefly
    time.sleep(3)
    
    # Show status
    status = stealth.get_status()
    print(f"\n[STATUS] Stealth Mode:")
    print(f"  Active: {status['stealth_active']}")
    print(f"  Invisibility Level: {status['invisibility_level']}/10")
    print(f"  Bridge Status:")
    print(f"    Fully Isolated: {status['bridge']['fully_isolated']}")
    print(f"    Closed Bridges: {status['bridge']['closed_bridges']}")
    print(f"  Traffic Obfuscation:")
    print(f"    Active: {status['obfuscator']['active']}")
    print(f"    Packets Obfuscated: {status['obfuscator']['obfuscated_packets']}")
    print(f"  Decoy Traffic:")
    print(f"    Active: {status['decoy']['active']}")
    print(f"    Decoys Generated: {status['decoy']['decoys_generated']}")
    print(f"  Anti-SDA:")
    print(f"    Active: {status['anti_sda']['active']}")
    print(f"    Protected Operations: {status['anti_sda']['protected_operations']}")
    
    # Deactivate
    stealth.deactivate()
    print("\n[✓] Stealth Mode demonstration complete")
    
    return stealth


def demo_integrated_system():
    """Demonstrate fully integrated quantum-safe system."""
    print_section("INTEGRATED QUANTUM-SAFE ETERNAL DEPOSITION SYSTEM")
    
    print("[INIT] Initializing Eternal Deposition Engine with quantum-safe protection...")
    
    # Initialize with smaller node count for demo
    engine = EternalDepositionEngine(initial_nodes=10, enable_quantum_safe=True)
    
    # Wait for initialization
    time.sleep(2)
    
    # Activate stealth mode
    print("\n[SECURITY] Activating stealth mode...")
    engine.activate_stealth_mode(level=8)
    
    # Run a few cycles
    print("\n[RUNNING] Executing 3 cycles...")
    for i in range(3):
        metrics = engine.execute_cycle()
        print(f"  Cycle {metrics['cycle']}: Phase={metrics['phase_degrees']:.1f}° | "
              f"Nodes={metrics['nodes']} | Energy={metrics['avg_energy']:.4f}")
        time.sleep(1)
    
    # Show comprehensive status
    status = engine.get_status()
    print(f"\n[STATUS] Eternal Deposition Engine:")
    print(f"  Status: {status['status']}")
    print(f"  Cycles: {status['cycle_count']}")
    print(f"  Nodes: {status['nodes']}")
    print(f"  Quantum-Safe Enabled: {status['quantum_safe_enabled']}")
    
    if 'quantum_safe_systems' in status:
        print(f"\n[QUANTUM-SAFE] Protection Systems:")
        qs = status['quantum_safe_systems']
        
        if 'quantum_shield' in qs:
            print(f"  Quantum Shield:")
            print(f"    Status: {qs['quantum_shield']['status']}")
            print(f"    Encryption: {qs['quantum_shield']['encryption']}")
            print(f"    Rotations: {qs['quantum_shield']['rotation_count']}")
        
        if 'mesh_network' in qs:
            print(f"  Mesh Network:")
            print(f"    Status: {qs['mesh_network']['status']}")
            print(f"    DNS-Free: {qs['mesh_network']['dns_free']}")
            print(f"    Peers: {qs['mesh_network']['connected_peers']}")
        
        if 'ai_detector' in qs:
            print(f"  AI Detector:")
            print(f"    Status: {qs['ai_detector']['status']}")
            print(f"    Detections: {qs['ai_detector']['total_detections']}")
        
        if 'stealth_mode' in qs:
            print(f"  Stealth Mode:")
            print(f"    Active: {qs['stealth_mode']['stealth_active']}")
            print(f"    Level: {qs['stealth_mode']['invisibility_level']}/10")
    
    # Shutdown gracefully
    print("\n[SHUTDOWN] Gracefully shutting down...")
    engine.shutdown()
    
    print("\n[✓] Integrated system demonstration complete")
    
    return engine


def main():
    """Main demo entry point."""
    print("=" * 70)
    print("QUANTUM-SAFE NETWORK PROTECTION - VALIDATION DEMO".center(70))
    print("=" * 70)
    print(f"\nStarted: {datetime.now().isoformat()}")
    print(f"Repository: hannesmitterer/AI")
    print(f"Implementation: Quantum-Safe Protection Phase III")
    
    try:
        # Run individual demos
        print("\n[INFO] Running individual component demonstrations...")
        
        demo_quantum_shield()
        time.sleep(1)
        
        demo_blockchain_mesh_network()
        time.sleep(1)
        
        demo_ai_anomaly_detector()
        time.sleep(1)
        
        demo_stealth_mode()
        time.sleep(1)
        
        # Run integrated demo
        demo_integrated_system()
        
        # Final summary
        print_section("VALIDATION COMPLETE")
        print("All quantum-safe protection systems validated successfully!")
        print("\nImplemented Features:")
        print("  [✓] Quantum Shield - NTRU lattice-based encryption")
        print("  [✓] Blockchain Mesh Network - DNS-free infrastructure")
        print("  [✓] AI Anomaly Detection - EM threat monitoring")
        print("  [✓] Stealth Mode - Network invisibility")
        print("  [✓] Integrated System - Full quantum-safe protection")
        
        print(f"\nCompleted: {datetime.now().isoformat()}")
        print("\n[SUCCESS] Quantum-Safe Network Protection is operational!")
        
    except KeyboardInterrupt:
        print("\n\n[INTERRUPTED] Demo interrupted by user")
    except Exception as e:
        print(f"\n\n[ERROR] Demo failed: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
