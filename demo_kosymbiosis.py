#!/usr/bin/env python3
"""
Demo script for the integrated Kosymbiosis Framework
Demonstrates Peacebond and Living Covenant working together
"""

from kosymbiosis_framework import KosymbiosisFramework

def main():
    """Run a simple demonstration of the framework."""
    print("\n" + "="*70)
    print("KOSYMBIOSIS FRAMEWORK DEMO")
    print("Peacebond + Living Covenant + Eternal Deposition")
    print("="*70 + "\n")
    
    # Initialize framework with fewer nodes for quick demo
    framework = KosymbiosisFramework(initial_nodes=50)
    
    print("\n" + "="*70)
    print("Running 20 unified cycles")
    print("="*70 + "\n")
    
    # Run 20 cycles
    for i in range(20):
        metrics = framework.execute_unified_cycle()
        
        if i % 5 == 0:
            print(f"[Cycle {metrics['framework_cycle']:03d}] "
                  f"Coherence: {metrics['system_coherence']:.4f}")
    
    print("\n" + "="*70)
    print("OPERATION LOG (Last 10 entries)")
    print("="*70 + "\n")
    
    framework.display_operation_log(last_n=10)
    
    print("\n" + "="*70)
    print("FINAL STATUS")
    print("="*70 + "\n")
    
    status = framework.get_comprehensive_status()
    
    print("[Framework]")
    print(f"  Cycles: {status['framework']['framework_cycle']}")
    print(f"  Operations Logged: {status['framework']['operations_logged']}")
    
    print("\n[Eternal Deposition]")
    print(f"  Nodes: {status['eternal_deposition']['nodes']}")
    print(f"  Energy: {status['eternal_deposition']['avg_energy']:.4f}")
    
    print("\n[Peacebond]")
    print(f"  Nexuses: {status['peacebond']['total_nexuses']}")
    print(f"  Harmony: {status['peacebond']['global_harmony']:.4f}")
    
    print("\n[Living Covenant]")
    print(f"  Clauses: {status['living_covenant']['total_clauses']}")
    print(f"  Alignment: {status['living_covenant']['global_alignment']:.4f}")
    
    print("\n" + "="*70)
    print("Demo complete!")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
