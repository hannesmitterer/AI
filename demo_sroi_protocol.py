#!/usr/bin/env python3
"""
S-ROI Sovereign Protocol - Demo Script
Demonstrates the connected logical steps implementation with
logging, validation, notifications, and modular states.
"""

import time
from sroi_sovereign_protocol import (
    SROISovereignProtocol,
    NotificationLevel,
    Notification,
    SROI_TARGET
)


def demo_basic_protocol():
    """Demonstrate basic protocol operation."""
    print("\n" + "="*70)
    print("DEMO 1: Basic Protocol Operation")
    print("="*70 + "\n")
    
    protocol = SROISovereignProtocol(initial_sroi=0.5192)
    
    # Register notification handler
    notification_count = {"count": 0}
    
    def count_notifications(notification: Notification):
        notification_count["count"] += 1
    
    protocol.notification_system.register_handler(count_notifications)
    
    # Run for 20 cycles
    print("Running protocol for 20 cycles...\n")
    protocol.run(max_cycles=20)
    
    # Display summary
    status = protocol.get_status()
    print("\n" + "-"*70)
    print("Summary:")
    print(f"  Final State: {status['current_state']}")
    print(f"  Final S-ROI: {status['sroi_value']:.4f}")
    print(f"  Target S-ROI: {SROI_TARGET:.4f}")
    print(f"  Total Cycles: {status['cycle_count']}")
    print(f"  Total Notifications: {notification_count['count']}")
    print("-"*70)


def demo_state_transitions():
    """Demonstrate state transition logging and validation."""
    print("\n" + "="*70)
    print("DEMO 2: State Transition Validation")
    print("="*70 + "\n")
    
    # Start with low S-ROI to trigger multiple states
    protocol = SROISovereignProtocol(initial_sroi=0.25)
    
    print("Starting with critically low S-ROI (0.25)...")
    print("This will trigger WARNING → CRITICAL → RECOVERY states\n")
    
    # Run cycles
    protocol.run(max_cycles=15)
    
    # Show state history
    summary = protocol.state_logger.get_state_summary()
    print("\n" + "-"*70)
    print("State Transition Summary:")
    print(f"  Total Transitions: {summary['total_transitions']}")
    print(f"  Valid Transitions: {summary['valid_transitions']}")
    print(f"  Invalid Transitions: {summary['invalid_transitions']}")
    print("-"*70)


def demo_notifications():
    """Demonstrate notification system with threshold violations."""
    print("\n" + "="*70)
    print("DEMO 3: Notification System")
    print("="*70 + "\n")
    
    # Collect notifications
    notifications_received = []
    
    def collect_notifications(notification: Notification):
        notifications_received.append(notification)
        if notification.level in [NotificationLevel.CRITICAL, NotificationLevel.EMERGENCY]:
            print(f"  [{notification.level.value.upper()}] {notification.message}")
    
    # Test with critical low S-ROI
    protocol = SROISovereignProtocol(initial_sroi=0.15)
    protocol.notification_system.register_handler(collect_notifications)
    
    print("Testing with critically low S-ROI (0.15)...\n")
    protocol.run(max_cycles=10)
    
    print("\n" + "-"*70)
    print("Notification Summary:")
    print(f"  Total Notifications: {len(notifications_received)}")
    
    # Count by level
    by_level = {}
    for notif in notifications_received:
        level = notif.level.value
        by_level[level] = by_level.get(level, 0) + 1
    
    for level, count in by_level.items():
        print(f"  {level.upper()}: {count}")
    print("-"*70)


def demo_modular_states():
    """Demonstrate modular state functions."""
    print("\n" + "="*70)
    print("DEMO 4: Modular State Functions")
    print("="*70 + "\n")
    
    protocol = SROISovereignProtocol(initial_sroi=0.52)
    
    print("Demonstrating individual state functions:")
    print("INITIALIZING → CALIBRATING → MONITORING → OPTIMIZING → STABLE\n")
    
    # Track states visited
    states_visited = set()
    
    def track_states(notification: Notification):
        states_visited.add(notification.state.value)
    
    protocol.notification_system.register_handler(track_states)
    
    # Run protocol
    protocol.run(max_cycles=25)
    
    # Also track from transitions
    for transition in protocol.state_logger.state_history:
        states_visited.add(transition.from_state.value)
        states_visited.add(transition.to_state.value)
    
    print("\n" + "-"*70)
    print("States Visited:")
    for state in sorted(states_visited):
        print(f"  • {state}")
    print("-"*70)


def demo_optimization_flow():
    """Demonstrate S-ROI optimization flow."""
    print("\n" + "="*70)
    print("DEMO 5: S-ROI Optimization Flow")
    print("="*70 + "\n")
    
    # Start below target to trigger optimization
    protocol = SROISovereignProtocol(initial_sroi=0.70)
    
    print(f"Starting S-ROI: 0.70")
    print(f"Target S-ROI: {SROI_TARGET}")
    print("Optimizing towards target...\n")
    
    # Track S-ROI progression
    sroi_history = [0.70]
    
    # Run optimization
    for i in range(30):
        metrics = protocol.execute_cycle()
        sroi_history.append(metrics['sroi_value'])
        
        if i % 5 == 0:
            print(f"Cycle {i:2d}: S-ROI = {metrics['sroi_value']:.4f}, "
                  f"State = {metrics['state']}")
    
    print("\n" + "-"*70)
    print("Optimization Results:")
    print(f"  Starting S-ROI: {sroi_history[0]:.4f}")
    print(f"  Final S-ROI: {sroi_history[-1]:.4f}")
    print(f"  Target S-ROI: {SROI_TARGET:.4f}")
    print(f"  Improvement: {(sroi_history[-1] - sroi_history[0]):.4f}")
    print(f"  Target Achieved: {'YES' if sroi_history[-1] >= SROI_TARGET else 'NO'}")
    print("-"*70)


def demo_log_files():
    """Demonstrate log file generation."""
    print("\n" + "="*70)
    print("DEMO 6: Log File Generation")
    print("="*70 + "\n")
    
    protocol = SROISovereignProtocol(initial_sroi=0.60)
    
    print("Running protocol to generate log files...")
    print("  • sroi_protocol.log (text log)")
    print("  • sroi_state_log.json (structured log)\n")
    
    protocol.run(max_cycles=15)
    
    print("\n" + "-"*70)
    print("Log files created:")
    
    import os
    for log_file in ['sroi_protocol.log', 'sroi_state_log.json']:
        if os.path.exists(log_file):
            size = os.path.getsize(log_file)
            print(f"  ✓ {log_file} ({size} bytes)")
        else:
            print(f"  ✗ {log_file} (not found)")
    
    print("\nCheck these files for complete state tracking and flow logging.")
    print("-"*70)


def main():
    """Run all demos."""
    print("=" * 70)
    print(" " * 10 + "S-ROI SOVEREIGN PROTOCOL - DEMO SUITE")
    print(" " * 15 + "Connected Logical Steps")
    print("=" * 70)
    
    try:
        demo_basic_protocol()
        time.sleep(1)
        
        demo_state_transitions()
        time.sleep(1)
        
        demo_notifications()
        time.sleep(1)
        
        demo_modular_states()
        time.sleep(1)
        
        demo_optimization_flow()
        time.sleep(1)
        
        demo_log_files()
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    
    print("\n" + "=" * 70)
    print("All demos complete!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
