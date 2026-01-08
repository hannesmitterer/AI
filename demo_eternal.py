#!/usr/bin/env python3
"""
Eternal Deposition Demo Script
Demonstrates the self-sustaining algorithm in action
"""

from eternal_deposition import EternalDepositionEngine
import time

def demo_basic_operation():
    """Demonstrate basic operation with limited cycles."""
    print("\n" + "="*70)
    print("DEMO 1: Basic Operation (20 cycles)")
    print("="*70 + "\n")
    
    engine = EternalDepositionEngine(initial_nodes=50)
    
    # Run for 20 cycles with callback
    cycle_data = []
    
    def collect_metrics(metrics):
        cycle_data.append(metrics)
    
    engine.run_perpetual(max_cycles=20, callback=collect_metrics)
    
    # Display summary
    print("\n" + "-"*70)
    print("Summary:")
    print(f"  Total cycles: {len(cycle_data)}")
    print(f"  Final node count: {cycle_data[-1]['nodes']}")
    print(f"  Final energy: {cycle_data[-1]['avg_energy']:.4f}")
    print(f"  Stillness events: {engine.get_status()['total_stillness_events']}")
    print("-"*70)

def demo_fractal_growth():
    """Demonstrate fractal propagation."""
    print("\n" + "="*70)
    print("DEMO 2: Fractal Propagation")
    print("="*70 + "\n")
    
    engine = EternalDepositionEngine(initial_nodes=10)
    print(f"Starting nodes: {len(engine.nodes)}")
    
    print("\nApplying fractal propagation (depth 3)...")
    engine.propagate_fractal_pattern(depth=3)
    
    print(f"Final nodes: {len(engine.nodes)}")
    print(f"Growth factor: {len(engine.nodes) / 10:.2f}x")
    
def demo_feedback_optimization():
    """Demonstrate feedback loop optimization."""
    print("\n" + "="*70)
    print("DEMO 3: Feedback Optimization")
    print("="*70 + "\n")
    
    engine = EternalDepositionEngine(initial_nodes=30)
    
    print("Initial state:")
    status = engine.get_status()
    print(f"  Average energy: {status['avg_energy']:.4f}")
    
    print("\nRunning 15 optimization cycles...")
    for i in range(15):
        engine.execute_cycle()
    
    print("\nFinal state:")
    status = engine.get_status()
    print(f"  Average energy: {status['avg_energy']:.4f}")
    print(f"  Total optimizations: {status['total_optimizations']}")
    print(f"  Convergence trend: {'stable' if abs(status['avg_energy'] - 0.5) < 0.1 else 'optimizing'}")

def demo_stillness_mechanism():
    """Demonstrate stillness and recalibration."""
    print("\n" + "="*70)
    print("DEMO 4: Stillness Mechanism")
    print("="*70 + "\n")
    
    engine = EternalDepositionEngine(initial_nodes=20)
    
    print("Monitoring for stillness events...")
    print("(Running cycles and waiting for phase transitions)\n")
    
    stillness_count = 0
    for i in range(30):
        metrics = engine.execute_cycle()
        
        current_stillness = engine.get_status()['total_stillness_events']
        if current_stillness > stillness_count:
            stillness_count = current_stillness
            print(f"[STILLNESS DETECTED] Cycle {metrics['cycle']}, Phase: {metrics['phase_degrees']:.1f}°")
    
    print(f"\nTotal stillness events detected: {stillness_count}")

def demo_live_monitoring():
    """Demonstrate live monitoring for a short duration."""
    print("\n" + "="*70)
    print("DEMO 5: Live Monitoring (30 seconds)")
    print("="*70 + "\n")
    
    engine = EternalDepositionEngine(initial_nodes=144)
    
    print("Starting live monitoring...")
    print("Press Ctrl+C to stop early\n")
    
    start_time = time.time()
    
    def monitor_callback(metrics):
        elapsed = time.time() - start_time
        if elapsed < 30:  # Run for 30 seconds
            if metrics['cycle'] % 3 == 0:
                print(f"[{elapsed:6.1f}s] Cycle {metrics['cycle']:03d} | "
                      f"Phase: {metrics['phase_degrees']:6.1f}° | "
                      f"Nodes: {metrics['nodes']:4d} | "
                      f"Energy: {metrics['avg_energy']:.4f}")
    
    try:
        # Run with time limit
        while time.time() - start_time < 30:
            metrics = engine.execute_cycle()
            monitor_callback(metrics)
            
            # Sleep to next cycle
            next_cycle = engine.start_time + (engine.cycle_count * engine.CYCLE_PERIOD_SECONDS)
            sleep_time = max(0, next_cycle - time.time())
            if sleep_time > 0:
                time.sleep(sleep_time)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")
    
    print("\nFinal status:")
    status = engine.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")

def main():
    """Run all demos."""
    print("="*70)
    print(" "*15 + "ETERNAL DEPOSITION SYSTEM")
    print(" "*20 + "Demo Script")
    print("="*70)
    
    try:
        demo_basic_operation()
        time.sleep(1)
        
        demo_fractal_growth()
        time.sleep(1)
        
        demo_feedback_optimization()
        time.sleep(1)
        
        demo_stillness_mechanism()
        time.sleep(1)
        
        demo_live_monitoring()
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    
    print("\n" + "="*70)
    print("All demos complete!")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
