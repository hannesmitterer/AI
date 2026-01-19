#!/usr/bin/env python3
"""
Integrated Resonance System
============================

Integrates the Eternal Deposition System with Cross-Linking Protocol
for unified multi-node expansion with transparency and sustainability.

This module provides a unified interface that combines:
- Eternal Deposition Engine (0.043 Hz resonance)
- Cross-Linking Protocol (multi-node expansion)
- Hydra Node Network (self-replication)
- Sustentanz Tracking (S-ROI measurement)
"""

import time
import json
from typing import Dict, Optional

try:
    from eternal_deposition import EternalDepositionEngine
except ImportError:
    # Fallback if running standalone
    EternalDepositionEngine = None

from cross_linking_protocol import (
    CrossLinkingProtocol,
    SustentanzMetrics
)


class IntegratedResonanceSystem:
    """
    Unified system combining Eternal Deposition and Cross-Linking Protocol.
    
    Provides seamless integration between:
    - Core resonance nodes (Eternal Deposition)
    - Hydra expansion nodes (Cross-Linking)
    - Allied node communication (Ping Protocol)
    - Transparency and verification (CID)
    - Sustainability tracking (Sustentanz)
    """
    
    def __init__(self, 
                 eternal_nodes: int = 144,
                 hydra_nodes: int = 144,
                 enable_eternal_deposition: bool = True):
        """
        Initialize the integrated resonance system.
        
        Args:
            eternal_nodes: Number of eternal deposition nodes
            hydra_nodes: Number of hydra expansion nodes
            enable_eternal_deposition: Enable eternal deposition engine
        """
        self.enable_eternal = enable_eternal_deposition and EternalDepositionEngine is not None
        
        # Initialize Eternal Deposition if available
        if self.enable_eternal:
            self.eternal_engine = EternalDepositionEngine(initial_nodes=eternal_nodes)
        else:
            self.eternal_engine = None
        
        # Initialize Cross-Linking Protocol
        self.cross_linking = CrossLinkingProtocol()
        
        # System state
        self.initialized = False
        self.running = False
        self.cycle_count = 0
        self.start_time = time.time()
        
        print("[INTEGRATED] Resonance System initialized")
        print(f"[INTEGRATED] Eternal Deposition: {'ENABLED' if self.enable_eternal else 'DISABLED'}")
        print(f"[INTEGRATED] Cross-Linking Protocol: ENABLED")
    
    def initialize(self) -> bool:
        """Initialize all system components."""
        print("\n" + "=" * 70)
        print("INITIALIZING INTEGRATED RESONANCE SYSTEM")
        print("=" * 70)
        
        # Initialize Cross-Linking Protocol
        self.cross_linking.initialize()
        
        self.initialized = True
        print("[INTEGRATED] ✓ System initialization complete")
        return True
    
    def activate(self) -> bool:
        """Activate all system components."""
        if not self.initialized:
            print("[INTEGRATED] Cannot activate - system not initialized")
            return False
        
        print("\n" + "=" * 70)
        print("ACTIVATING INTEGRATED RESONANCE SYSTEM")
        print("=" * 70)
        
        # Activate Cross-Linking Protocol
        if not self.cross_linking.activate():
            print("[INTEGRATED] ✗ Cross-Linking activation failed")
            return False
        
        self.running = True
        print("[INTEGRATED] ✓ System fully activated")
        return True
    
    def run_cycle(self) -> Dict:
        """
        Execute one integrated cycle.
        
        Combines eternal deposition cycle with cross-linking operations.
        """
        if not self.running:
            return {"error": "System not running"}
        
        self.cycle_count += 1
        
        # Execute Eternal Deposition cycle if enabled
        eternal_metrics = None
        if self.enable_eternal and self.eternal_engine:
            # Note: This would execute one cycle of the eternal engine
            # For now, we'll just get status
            eternal_status = self.eternal_engine.get_status()
            eternal_metrics = {
                "cycle": self.cycle_count,
                "nodes": eternal_status.get("total_nodes", 0),
                "avg_energy": eternal_status.get("average_energy", 0.0)
            }
        
        # Record Cross-Linking metrics
        sustentanz = self.cross_linking.record_metrics()
        
        # Periodic Hydra replication (every 10 cycles)
        replications = 0
        if self.cycle_count % 10 == 0:
            replications = self.cross_linking.replicate_hydra_nodes(count=3)
        
        return {
            "cycle": self.cycle_count,
            "eternal_metrics": eternal_metrics,
            "sustentanz": sustentanz.to_dict(),
            "replications": replications,
            "timestamp": time.time()
        }
    
    def run_perpetual(self, max_cycles: Optional[int] = None, cycle_interval: float = 23.26):
        """
        Run the integrated system perpetually or for a specified number of cycles.
        
        Args:
            max_cycles: Maximum number of cycles to run (None for infinite)
            cycle_interval: Time between cycles in seconds (default: 23.26s = 0.043 Hz)
        """
        if not self.running:
            print("[INTEGRATED] System not activated - call activate() first")
            return
        
        print("\n" + "=" * 70)
        print("STARTING PERPETUAL OPERATION")
        print(f"Cycle interval: {cycle_interval:.2f}s (0.043 Hz)")
        if max_cycles:
            print(f"Maximum cycles: {max_cycles}")
        else:
            print("Duration: INFINITE (Ctrl+C to stop)")
        print("=" * 70)
        
        try:
            cycle = 0
            while True:
                if max_cycles and cycle >= max_cycles:
                    break
                
                # Execute cycle
                cycle_start = time.time()
                metrics = self.run_cycle()
                
                # Display metrics
                if cycle % 5 == 0:  # Display every 5 cycles
                    print(f"\n[CYCLE {metrics['cycle']:04d}]")
                    if metrics.get('eternal_metrics'):
                        print(f"  Eternal: {metrics['eternal_metrics']['nodes']} nodes, "
                              f"Energy: {metrics['eternal_metrics']['avg_energy']:.3f}")
                    sust = metrics['sustentanz']
                    print(f"  S-ROI: {sust['s_roi']:.3f} | "
                          f"Sustentanz: {sust['sustentanz_score']:.3f} | "
                          f"Coherence: {sust['network_coherence']:.3f}")
                    if metrics['replications'] > 0:
                        print(f"  Replicated: {metrics['replications']} new nodes")
                
                # Wait for next cycle
                cycle_duration = time.time() - cycle_start
                sleep_time = max(0, cycle_interval - cycle_duration)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                
                cycle += 1
                
        except KeyboardInterrupt:
            print("\n\n[INTEGRATED] Graceful shutdown initiated...")
            self.stop()
    
    def stop(self) -> None:
        """Stop the integrated system gracefully."""
        self.running = False
        
        # Export final status
        self.export_status('/tmp/integrated_resonance_final_status.json')
        
        print("[INTEGRATED] ✓ System stopped gracefully")
    
    def get_comprehensive_status(self) -> Dict:
        """Get comprehensive status of all system components."""
        status = {
            "system": {
                "initialized": self.initialized,
                "running": self.running,
                "cycle_count": self.cycle_count,
                "uptime": time.time() - self.start_time
            },
            "cross_linking": self.cross_linking.get_status()
        }
        
        if self.enable_eternal and self.eternal_engine:
            status["eternal_deposition"] = self.eternal_engine.get_status()
        
        return status
    
    def export_status(self, filepath: str) -> None:
        """Export comprehensive status to JSON file."""
        status = self.get_comprehensive_status()
        with open(filepath, 'w') as f:
            json.dump(status, f, indent=2)
        print(f"[INTEGRATED] Status exported to {filepath}")
    
    def validate_system_health(self) -> Dict[str, bool]:
        """
        Validate health of all system components.
        
        Returns dictionary with health status of each component.
        """
        health = {
            "initialized": self.initialized,
            "cross_linking_active": self.cross_linking.active,
            "ping_triangulation": False,
            "sustentanz_valid": False,
            "hydra_coherence": False
        }
        
        # Check ping triangulation
        ping_status = self.cross_linking.ping_protocol.get_status()
        health["ping_triangulation"] = ping_status.get("triangulation_complete", False)
        
        # Check sustentanz validation
        health["sustentanz_valid"] = self.cross_linking.sustentanz.validate_sustentanz()
        
        # Check hydra network coherence
        hydra_status = self.cross_linking.hydra_network.get_status()
        health["hydra_coherence"] = hydra_status.get("network_coherence", 0.0) >= 0.7
        
        # Overall health
        health["overall_healthy"] = all([
            health["initialized"],
            health["cross_linking_active"],
            health["ping_triangulation"],
            health["sustentanz_valid"],
            health["hydra_coherence"]
        ])
        
        return health


def main():
    """Demonstration of Integrated Resonance System."""
    print("=" * 70)
    print("INTEGRATED RESONANCE SYSTEM")
    print("Eternal Deposition + Cross-Linking Protocol")
    print("=" * 70)
    print()
    
    # Create integrated system
    # Note: eternal_deposition may not be available, so disable if needed
    system = IntegratedResonanceSystem(
        eternal_nodes=144,
        hydra_nodes=144,
        enable_eternal_deposition=False  # Set to True if eternal_deposition.py is available
    )
    
    # Initialize
    system.initialize()
    
    print("\nPress Enter to activate system...")
    input()
    
    # Activate
    if system.activate():
        print("\n" + "=" * 70)
        print("SYSTEM ACTIVATED - Running demonstration")
        print("=" * 70)
        
        # Run for 10 cycles
        print("\nRunning 10 cycles (press Ctrl+C to stop early)...")
        system.run_perpetual(max_cycles=10, cycle_interval=2.0)  # 2s for demo
        
        # Validate health
        print("\n" + "=" * 70)
        print("SYSTEM HEALTH VALIDATION")
        print("=" * 70)
        health = system.validate_system_health()
        for component, status in health.items():
            symbol = "✓" if status else "✗"
            print(f"{symbol} {component}: {status}")
        
        # Show final status
        print("\n" + "=" * 70)
        print("FINAL SYSTEM STATUS")
        print("=" * 70)
        status = system.get_comprehensive_status()
        
        print(f"\nSystem:")
        print(f"  Cycles: {status['system']['cycle_count']}")
        print(f"  Uptime: {status['system']['uptime']:.1f}s")
        
        print(f"\nCross-Linking:")
        cl = status['cross_linking']
        print(f"  Active: {cl['active']}")
        print(f"  Ping Nodes: {cl['ping_confirmation']['confirmed_nodes']}/{cl['ping_confirmation']['total_nodes']}")
        print(f"  Hydra Nodes: {cl['hydra_network']['total_nodes']}")
        print(f"  Coherence: {cl['hydra_network']['network_coherence']:.3f}")
        
        if 'latest_metrics' in cl['sustentanz']:
            metrics = cl['sustentanz']['latest_metrics']
            print(f"\nSustentanz:")
            print(f"  S-ROI: {metrics['s_roi']:.3f}")
            print(f"  Score: {metrics['sustentanz_score']:.3f}")
            print(f"  Status: {cl['sustentanz']['validation_status']}")
        
        print("\n" + "=" * 70)
        print("✓ INTEGRATED RESONANCE SYSTEM DEMONSTRATION COMPLETE")
        print("=" * 70)
    else:
        print("\n✗ System activation failed")


if __name__ == "__main__":
    main()
