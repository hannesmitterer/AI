#!/usr/bin/env python3
"""
S-ROI Sovereign Protocol Demo Script
=====================================

Demonstrates the capabilities of the S-ROI Sovereign protocol including:
- State management and transitions
- Resonance tracking
- Stealth mode with cooldown
- Logging and history
"""

import time
import logging
from sroi_sovereign import SROISovereign, SROI_TARGET


def print_separator(title=""):
    """Print a section separator."""
    if title:
        print(f"\n{'=' * 70}")
        print(f"  {title}")
        print('=' * 70)
    else:
        print('-' * 70)


def print_status(sovereign):
    """Print current system status."""
    status = sovereign.get_status()
    print(f"\nCurrent Status:")
    print(f"  Resonance:     {status['current_resonance']:.4f}")
    print(f"  State:         {status['state']}")
    print(f"  Target S-ROI:  {status['target_sroi']:.4f}")
    print(f"  Stealth Mode:  {status['stealth']['mode']}")
    print(f"  Updates:       {status['update_count']}")
    print(f"  Uptime:        {status['uptime_seconds']:.1f}s")


def demo_basic_initialization():
    """Demo 1: Basic initialization and state management."""
    print_separator("DEMO 1: Initialization and Basic State Management")
    
    print("\nInitializing S-ROI Sovereign with resonance 0.9...")
    sovereign = SROISovereign(initial_resonance=0.9, log_level=logging.INFO)
    
    print_status(sovereign)
    
    return sovereign


def demo_state_transitions(sovereign):
    """Demo 2: State transitions through resonance changes."""
    print_separator("DEMO 2: State Transitions")
    
    print("\nSimulating resonance changes to demonstrate state transitions...")
    
    # STABLE -> WARNING
    print("\n[1] Decreasing resonance to WARNING threshold...")
    sovereign.update_resonance(0.82, "Normal operational variance")
    time.sleep(1)
    print_status(sovereign)
    
    # WARNING -> CRITICAL
    print("\n[2] Further decrease to CRITICAL threshold...")
    sovereign.update_resonance(0.65, "System stress detected")
    time.sleep(1)
    print_status(sovereign)
    
    # CRITICAL -> WARNING
    print("\n[3] Recovery to WARNING threshold...")
    sovereign.update_resonance(0.75, "Recovery in progress")
    time.sleep(1)
    print_status(sovereign)
    
    # WARNING -> STABLE
    print("\n[4] Full recovery to STABLE state...")
    sovereign.update_resonance(0.92, "System stabilized")
    time.sleep(1)
    print_status(sovereign)


def demo_stealth_mode(sovereign):
    """Demo 3: Stealth mode with cooldown mechanism."""
    print_separator("DEMO 3: Stealth Mode and Cooldown")
    
    print("\n[1] Activating stealth mode...")
    success = sovereign.request_stealth_activation("Entering protected operations")
    print(f"    Activation {'successful' if success else 'failed'}")
    time.sleep(0.5)
    
    print("\n[2] Attempting to activate again (should fail - already active)...")
    success = sovereign.request_stealth_activation("Redundant activation attempt")
    print(f"    Activation {'successful' if success else 'failed (expected)'}")
    time.sleep(0.5)
    
    print("\n[3] Deactivating stealth mode...")
    sovereign.deactivate_stealth("Returning to normal operations")
    status = sovereign.get_status()
    print(f"    Stealth mode: {status['stealth']['mode']}")
    print(f"    Cooldown remaining: {status['stealth']['cooldown_remaining']:.1f}s")
    time.sleep(0.5)
    
    print("\n[4] Attempting immediate reactivation (should fail - cooldown)...")
    success = sovereign.request_stealth_activation("Immediate reactivation")
    status = sovereign.get_status()
    print(f"    Activation {'successful' if success else 'failed (expected - in cooldown)'}")
    print(f"    Cooldown remaining: {status['stealth']['cooldown_remaining']:.1f}s")
    
    print("\n[5] Waiting for cooldown to expire...")
    print("    (This demo uses reduced cooldown of 3 seconds for demonstration)")
    
    # Show countdown
    for i in range(3, 0, -1):
        print(f"    {i}...", end='', flush=True)
        time.sleep(1)
    print(" Done!")
    
    print("\n[6] Activating after cooldown...")
    success = sovereign.request_stealth_activation("Post-cooldown activation")
    print(f"    Activation {'successful' if success else 'failed'}")
    
    # Clean up
    sovereign.deactivate_stealth("Demo cleanup")


def demo_logging_and_history(sovereign):
    """Demo 4: Logging and history tracking."""
    print_separator("DEMO 4: Logging and History")
    
    print("\nGenerating some activity for history tracking...")
    
    # Generate various state changes
    resonance_values = [0.95, 0.88, 0.78, 0.68, 0.72, 0.85, 0.92]
    for i, resonance in enumerate(resonance_values):
        sovereign.update_resonance(resonance, f"Test cycle {i+1}")
        time.sleep(0.2)
    
    print("\n--- State Change History (last 5 entries) ---")
    state_history = sovereign.get_state_history(limit=5)
    for entry in state_history:
        print(f"  {entry['timestamp'][:19]}: "
              f"{entry['previous_state']} -> {entry['new_state']} "
              f"(resonance: {entry['resonance_value']:.4f})")
        print(f"    Reason: {entry['reason']}")
    
    print("\n--- Resonance History (last 5 entries) ---")
    resonance_history = sovereign.get_resonance_history(limit=5)
    for entry in resonance_history:
        print(f"  {entry['timestamp'][:19]}: "
              f"Value: {entry['value']:.4f}, "
              f"State: {entry['state']}, "
              f"Stealth: {entry['stealth_active']}")


def demo_edge_cases(sovereign):
    """Demo 5: Edge cases and boundary conditions."""
    print_separator("DEMO 5: Edge Cases and Boundary Conditions")
    
    print("\n[1] Testing resonance clamping (values outside 0-1 range)...")
    print("    Setting resonance to 1.5 (should clamp to 1.0)...")
    sovereign.update_resonance(1.5, "Overflow test")
    status = sovereign.get_status()
    print(f"    Actual resonance: {status['current_resonance']:.4f}")
    
    print("\n    Setting resonance to -0.3 (should clamp to 0.0)...")
    sovereign.update_resonance(-0.3, "Underflow test")
    status = sovereign.get_status()
    print(f"    Actual resonance: {status['current_resonance']:.4f}")
    
    print("\n[2] Testing exact threshold values...")
    print("    Setting to WARNING threshold exactly (0.850)...")
    sovereign.update_resonance(0.850, "Exact threshold test")
    status = sovereign.get_status()
    print(f"    State: {status['state']} (should be STABLE)")
    
    print("\n[3] Testing rapid consecutive updates...")
    print("    Performing 50 rapid updates...")
    start_count = sovereign.update_count
    for i in range(50):
        sovereign.update_resonance(0.5 + (i % 20) * 0.02, "Rapid update")
    print(f"    Updates processed: {sovereign.update_count - start_count}")


def demo_comprehensive_status():
    """Demo 6: Comprehensive status display."""
    print_separator("DEMO 6: Comprehensive System Status")
    
    # Create fresh instance with some activity
    sovereign = SROISovereign(
        initial_resonance=0.85,
        log_level=logging.WARNING,
        cooldown_seconds=3.0
    )
    
    # Generate some activity
    sovereign.update_resonance(0.90, "Optimization")
    sovereign.request_stealth_activation("Protective measure")
    time.sleep(0.5)
    sovereign.deactivate_stealth("Resume normal")
    sovereign.update_resonance(0.78, "Minor fluctuation")
    
    print("\n--- Complete System Status ---")
    status = sovereign.get_status()
    
    for key, value in status.items():
        if key == 'stealth':
            print(f"\nStealth Mode Details:")
            for sk, sv in value.items():
                print(f"  {sk}: {sv}")
        else:
            print(f"{key}: {value}")


def main():
    """Run all demos."""
    print("=" * 70)
    print("  S-ROI SOVEREIGN PROTOCOL - COMPREHENSIVE DEMONSTRATION")
    print("=" * 70)
    print()
    print("This demo showcases the enhanced S-ROI Sovereign protocol with:")
    print("  • Three-state management (STABLE, WARNING, CRITICAL)")
    print("  • Resonance tracking and logging")
    print("  • Stealth mode with cooldown mechanism")
    print("  • Comprehensive history tracking")
    print()
    input("Press Enter to begin...")
    
    # Demo 1: Initialization
    sovereign = demo_basic_initialization()
    input("\nPress Enter to continue to Demo 2...")
    
    # Demo 2: State transitions
    demo_state_transitions(sovereign)
    input("\nPress Enter to continue to Demo 3...")
    
    # Demo 3: Stealth mode (with reduced cooldown for demo)
    # Create new instance with shorter cooldown for demo purposes
    sovereign_stealth = SROISovereign(
        initial_resonance=0.9,
        log_level=logging.INFO,
        cooldown_seconds=3.0  # Reduced from default 60s for demo
    )
    demo_stealth_mode(sovereign_stealth)
    input("\nPress Enter to continue to Demo 4...")
    
    # Demo 4: Logging and history
    demo_logging_and_history(sovereign)
    input("\nPress Enter to continue to Demo 5...")
    
    # Demo 5: Edge cases
    demo_edge_cases(sovereign)
    input("\nPress Enter to continue to Demo 6...")
    
    # Demo 6: Comprehensive status
    demo_comprehensive_status()
    
    print_separator("DEMONSTRATION COMPLETE")
    print("\nAll S-ROI Sovereign protocol features have been demonstrated.")
    print("Key achievements:")
    print("  ✓ Modular architecture")
    print("  ✓ Three-state management system")
    print("  ✓ Comprehensive logging")
    print("  ✓ Stealth mode with cooldown")
    print("  ✓ Edge case handling")
    print("  ✓ History tracking")
    print("\nThe protocol is ready for integration with larger systems.")
    print("=" * 70)


if __name__ == "__main__":
    main()
