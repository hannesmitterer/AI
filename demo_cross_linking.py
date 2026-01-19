#!/usr/bin/env python3
"""
Cross-Linking Protocol - Quick Demonstration
=============================================

A simple script to demonstrate the Cross-Linking Protocol capabilities
without requiring user interaction.

Usage:
    python3 demo_cross_linking.py
    
    or
    
    chmod +x demo_cross_linking.py
    ./demo_cross_linking.py
"""

import time
import json
from cross_linking_protocol import CrossLinkingProtocol


def print_banner(text):
    """Print a formatted banner."""
    print("\n" + "=" * 70)
    print(text.center(70))
    print("=" * 70)


def print_section(title):
    """Print a section header."""
    print(f"\n--- {title} ---")


def main():
    print_banner("CROSS-LINKING PROTOCOL")
    print_banner("AUTOMATED DEMONSTRATION")
    
    print("\nThis demonstration will:")
    print("  1. Initialize Cross-Linking Protocol")
    print("  2. Activate multi-node synchronization")
    print("  3. Verify Hydra nodes")
    print("  4. Demonstrate node replication")
    print("  5. Track Sustentanz metrics")
    print("  6. Export final status")
    
    time.sleep(2)
    
    # Step 1: Initialize
    print_banner("STEP 1: INITIALIZATION")
    protocol = CrossLinkingProtocol()
    protocol.initialize()
    
    time.sleep(1)
    
    # Step 2: Activate
    print_banner("STEP 2: ACTIVATION")
    if not protocol.activate():
        print("\n✗ Activation failed!")
        return 1
    
    time.sleep(1)
    
    # Step 3: Show initial status
    print_banner("STEP 3: INITIAL STATUS")
    status = protocol.get_status()
    
    print_section("Ping Confirmation")
    pc = status['ping_confirmation']
    print(f"  Total Allied Nodes: {pc['total_nodes']}")
    print(f"  Confirmed Nodes: {pc['confirmed_nodes']}")
    print(f"  Triangulation: {'✓ Complete' if pc['triangulation_complete'] else '✗ Incomplete'}")
    print(f"  Sync Active: {pc['sync_active']} nodes")
    
    print_section("Hydra Network")
    hn = status['hydra_network']
    print(f"  Total Nodes: {hn['total_nodes']}")
    print(f"  Generations: {hn['generations']}")
    print(f"  Average Energy: {hn['avg_energy']:.3f}")
    print(f"  Network Coherence: {hn['network_coherence']:.3f}")
    print(f"  Compliant Nodes: {hn['compliant_nodes']}/{hn['total_nodes']}")
    
    print_section("Broadcast Protocol")
    bp = status['broadcast']
    print(f"  Status: {'✓ Active' if bp['broadcast_active'] else '✗ Inactive'}")
    print(f"  GitHub Pages: {bp['github_pages']}")
    print(f"  IPFS Pins: {bp['ipfs_pins']}")
    print(f"  Hydra Signals: {bp['hydra_signals']}")
    
    print_section("Sustentanz Metrics")
    sm = status['sustentanz']
    if 'latest_metrics' in sm:
        metrics = sm['latest_metrics']
        print(f"  S-ROI: {metrics['s_roi']:.3f} (target: 0.950)")
        print(f"  Sustentanz Score: {metrics['sustentanz_score']:.3f} (target: ≥0.7)")
        print(f"  Network Coherence: {metrics['network_coherence']:.3f}")
        print(f"  Replication Efficiency: {metrics['replication_efficiency']:.3f}")
        print(f"  Transparency Index: {metrics['transparency_index']:.3f}")
        print(f"  Validation: {sm['validation_status'].upper()}")
    
    time.sleep(2)
    
    # Step 4: Demonstrate replication
    print_banner("STEP 4: NODE REPLICATION")
    print("\nReplicating Hydra nodes...")
    
    for round_num in range(3):
        print(f"\n  Round {round_num + 1}:")
        replicated = protocol.replicate_hydra_nodes(count=5)
        print(f"    ✓ Successfully replicated {replicated} nodes")
        
        # Show updated count
        current_status = protocol.get_status()
        current_nodes = current_status['hydra_network']['total_nodes']
        print(f"    Total nodes now: {current_nodes}")
        
        time.sleep(1)
    
    # Step 5: Show metrics evolution
    print_banner("STEP 5: METRICS EVOLUTION")
    print("\nRecording metrics over 5 cycles...")
    
    for cycle in range(5):
        metrics = protocol.record_metrics()
        print(f"\n  Cycle {cycle + 1}:")
        print(f"    S-ROI: {metrics.s_roi:.3f}")
        print(f"    Sustentanz: {metrics.sustentanz_score:.3f}")
        print(f"    Coherence: {metrics.network_coherence:.3f}")
        
        time.sleep(0.5)
    
    # Step 6: Final status
    print_banner("STEP 6: FINAL STATUS")
    final_status = protocol.get_status()
    
    print_section("Network Growth")
    initial_nodes = 144
    final_nodes = final_status['hydra_network']['total_nodes']
    growth = final_nodes - initial_nodes
    growth_pct = (growth / initial_nodes) * 100
    print(f"  Initial Nodes: {initial_nodes}")
    print(f"  Final Nodes: {final_nodes}")
    print(f"  Growth: +{growth} nodes ({growth_pct:.1f}%)")
    print(f"  Generations: {final_status['hydra_network']['generations']}")
    
    print_section("Performance Metrics")
    total_reps = final_status['hydra_network']['total_replications']
    print(f"  Total Replications: {total_reps}")
    print(f"  Network Coherence: {final_status['hydra_network']['network_coherence']:.3f}")
    print(f"  Compliance Rate: {final_status['hydra_network']['compliant_nodes']}/{final_nodes}")
    
    print_section("Sustentanz Status")
    if 'latest_metrics' in final_status['sustentanz']:
        metrics = final_status['sustentanz']['latest_metrics']
        s_roi = metrics['s_roi']
        sustentanz = metrics['sustentanz_score']
        
        s_roi_status = "✓ PASS" if s_roi >= 0.950 else "✗ BELOW TARGET"
        sustentanz_status = "✓ PASS" if sustentanz >= 0.7 else "✗ BELOW TARGET"
        
        print(f"  S-ROI: {s_roi:.3f} / 0.950 [{s_roi_status}]")
        print(f"  Sustentanz: {sustentanz:.3f} / 0.700 [{sustentanz_status}]")
        print(f"  Aggregate Score: {metrics['aggregate']:.3f}")
    
    # Step 7: Export
    print_banner("STEP 7: EXPORT RESULTS")
    export_path = "/tmp/cross_linking_demo_status.json"
    protocol.export_status_json(export_path)
    print(f"\n  Status exported to: {export_path}")
    
    # Show sample of exported data
    with open(export_path, 'r') as f:
        exported = json.load(f)
    
    print(f"\n  Export contains:")
    print(f"    - Initialization status")
    print(f"    - {len(exported['ping_confirmation']['nodes'])} allied node statuses")
    print(f"    - Hydra network metrics")
    print(f"    - Broadcast protocol status")
    print(f"    - {exported['sustentanz']['history_count']} Sustentanz measurements")
    
    # Final summary
    print_banner("DEMONSTRATION COMPLETE")
    
    print("\n✓ All steps completed successfully!")
    print("\nKey Achievements:")
    print(f"  • Activated multi-node synchronization with {final_status['ping_confirmation']['sync_active']} allied nodes")
    print(f"  • Initialized {initial_nodes} Hydra nodes")
    print(f"  • Replicated to {final_nodes} total nodes (+{growth})")
    print(f"  • Maintained {final_status['hydra_network']['network_coherence']:.1%} network coherence")
    print(f"  • Verified all CIDs and enforced Lex Amoris principles")
    print(f"  • Broadcasted via GitHub Pages and IPFS")
    print(f"  • Tracked Sustentanz metrics continuously")
    
    print("\nNext Steps:")
    print("  1. Review exported status: cat /tmp/cross_linking_demo_status.json")
    print("  2. Read TRANSPARENCY_MANIFESTO.md for guidelines")
    print("  3. See CROSS_LINKING_GUIDE.md for usage examples")
    print("  4. Run integrated_resonance.py for full system integration")
    
    print_banner("IN AETERNUM EST")
    print("\n\"Sempre in Costante. Nothing is final.\"\n")
    
    return 0


if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        print("\n\n[INTERRUPT] Demonstration stopped by user")
        exit(1)
    except Exception as e:
        print(f"\n\n[ERROR] Demonstration failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
