#!/usr/bin/env python3
"""
Lex Amoris Integration Demo
============================

Comprehensive demonstration of all strategic improvements integrated
with the Eternal Deposition System.

Modules:
1. Rhythm Validator - Dynamic blacklist and behavioral security
2. Lazy Security - Energy-based protection
3. IPFS Backup - Decentralized configuration mirroring
4. Rescue Channel - Emergency messaging and node recovery
"""

import time
import sys
from datetime import datetime

# Import all Lex Amoris modules
from eternal_deposition import EternalDepositionEngine, CYCLE_PERIOD_SECONDS
from rhythm_validator import RhythmValidator, create_test_packet, UNIVERSAL_RESONANCE_HZ
from lazy_security import LazySecurityEngine
from ipfs_backup import IPFSBackupEngine
from rescue_channel import RescueChannel, MessagePriority, NodeStatus


class LexAmorisIntegratedSystem:
    """
    Integrated system combining Eternal Deposition with Lex Amoris
    strategic improvements.
    """
    
    def __init__(self, initial_nodes: int = 144):
        """
        Initialize integrated system.
        
        Args:
            initial_nodes: Initial number of nodes for Eternal Deposition
        """
        print("=" * 70)
        print("LEX AMORIS INTEGRATED SYSTEM")
        print("Strategic Improvements for Eternal Deposition")
        print("=" * 70)
        print()
        
        # Initialize core eternal deposition engine
        print("[INIT] Eternal Deposition Engine...")
        self.eternal_engine = EternalDepositionEngine(initial_nodes=initial_nodes)
        
        # Initialize Lex Amoris modules
        print("\n[INIT] Rhythm Validator...")
        self.rhythm_validator = RhythmValidator(strict_mode=True)
        
        print("\n[INIT] Lazy Security Engine...")
        self.lazy_security = LazySecurityEngine(auto_scan=True)
        
        print("\n[INIT] IPFS Backup Engine...")
        self.ipfs_backup = IPFSBackupEngine(enable_pinning=True)
        
        print("\n[INIT] Rescue Channel...")
        self.rescue_channel = RescueChannel(universal_frequency=UNIVERSAL_RESONANCE_HZ)
        
        self.start_time = time.time()
        self.cycle_count = 0
        
        print("\n" + "=" * 70)
        print("SYSTEM INITIALIZATION COMPLETE")
        print("=" * 70)
        print()
    
    def execute_integrated_cycle(self) -> dict:
        """
        Execute one integrated system cycle combining all modules.
        
        Returns:
            Dictionary with cycle metrics from all systems
        """
        self.cycle_count += 1
        cycle_start = time.time()
        
        # 1. Execute eternal deposition cycle
        eternal_metrics = self.eternal_engine.execute_cycle()
        
        # 2. Perform security scan (Lazy Security)
        security_scan = self.lazy_security.scan_and_update()
        
        # 3. Validate incoming data packets (Rhythm Validator)
        # Simulate packet validation
        test_packet = create_test_packet(
            f"node_{self.cycle_count % 100:04d}",
            UNIVERSAL_RESONANCE_HZ
        )
        packet_valid, validation_reason = self.rhythm_validator.validate_packet(test_packet)
        
        # 4. Backup system state periodically (every 10 cycles)
        backup_created = False
        if self.cycle_count % 10 == 0:
            state_data = self.eternal_engine.get_status()
            backup = self.ipfs_backup.backup_system_state(state_data)
            backup_created = True
        
        # 5. Process rescue channel messages
        messages_processed = self.rescue_channel.process_pending_messages()
        
        # 6. Check for critical nodes and register if needed
        if eternal_metrics['avg_energy'] < 0.3:
            # Low energy detected, register as critical
            critical_node_id = f"node_{self.cycle_count:04d}"
            self.rescue_channel.register_critical_node(
                critical_node_id,
                NodeStatus.DEGRADED,
                "Low energy level detected"
            )
        
        cycle_duration = time.time() - cycle_start
        
        return {
            "cycle": self.cycle_count,
            "timestamp": datetime.now().isoformat(),
            "eternal_deposition": eternal_metrics,
            "security": {
                "field_strength_mv_m": security_scan.field_strength_mv_m,
                "threat_level": security_scan.threat_level,
                "protection_active": self.lazy_security.is_active
            },
            "rhythm_validation": {
                "packet_valid": packet_valid,
                "validation_reason": validation_reason
            },
            "backup": {
                "created": backup_created,
                "total_backups": len(self.ipfs_backup.backup_registry)
            },
            "rescue": {
                "messages_processed": messages_processed,
                "critical_nodes": len(self.rescue_channel.critical_nodes)
            },
            "cycle_duration_ms": cycle_duration * 1000
        }
    
    def run_demo(self, cycles: int = 30):
        """
        Run integrated system demo.
        
        Args:
            cycles: Number of cycles to run
        """
        print(f"\n[DEMO] Running {cycles} integrated cycles...")
        print("Press Ctrl+C to stop early\n")
        
        try:
            for i in range(cycles):
                metrics = self.execute_integrated_cycle()
                
                # Display periodic status
                if self.cycle_count % 5 == 0:
                    print(f"\n--- Cycle {metrics['cycle']:04d} ---")
                    print(f"Eternal: Phase {metrics['eternal_deposition']['phase_degrees']:.1f}°, "
                          f"{metrics['eternal_deposition']['nodes']} nodes, "
                          f"Energy {metrics['eternal_deposition']['avg_energy']:.4f}")
                    print(f"Security: {metrics['security']['field_strength_mv_m']:.2f} mV/m, "
                          f"Threat {metrics['security']['threat_level']}, "
                          f"Active: {metrics['security']['protection_active']}")
                    print(f"Rhythm: {'✓ Valid' if metrics['rhythm_validation']['packet_valid'] else '✗ Invalid'}")
                    print(f"Backup: {metrics['backup']['total_backups']} total, "
                          f"{'✓ Created' if metrics['backup']['created'] else '○'}")
                    print(f"Rescue: {metrics['rescue']['critical_nodes']} critical nodes, "
                          f"{metrics['rescue']['messages_processed']} msgs processed")
                
                # Sleep to simulate real-time operation
                time.sleep(0.5)
        
        except KeyboardInterrupt:
            print("\n\n[DEMO] Interrupted by user")
        
        # Display final statistics
        self._display_statistics()
    
    def _display_statistics(self):
        """Display comprehensive statistics from all modules."""
        print("\n" + "=" * 70)
        print("FINAL SYSTEM STATISTICS")
        print("=" * 70)
        
        # Eternal Deposition
        print("\n[1] ETERNAL DEPOSITION:")
        eternal_stats = self.eternal_engine.get_status()
        for key, value in eternal_stats.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.4f}")
            else:
                print(f"  {key}: {value}")
        
        # Rhythm Validator
        print("\n[2] RHYTHM VALIDATOR:")
        rhythm_stats = self.rhythm_validator.get_statistics()
        for key, value in rhythm_stats.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.4f}")
            else:
                print(f"  {key}: {value}")
        
        print("\n  Blacklist entries:")
        for entry in self.rhythm_validator.get_blacklist_entries():
            print(f"    {entry['source_ip']}: {entry['violations']} violations")
        
        # Lazy Security
        print("\n[3] LAZY SECURITY:")
        security_stats = self.lazy_security.get_statistics()
        for key, value in security_stats.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.4f}")
            else:
                print(f"  {key}: {value}")
        
        # IPFS Backup
        print("\n[4] IPFS BACKUP:")
        ipfs_stats = self.ipfs_backup.get_statistics()
        for key, value in ipfs_stats.items():
            if isinstance(value, dict):
                print(f"  {key}:")
                for k, v in value.items():
                    print(f"    {k}: {v}")
            elif isinstance(value, float):
                print(f"  {key}: {value:.4f}")
            else:
                print(f"  {key}: {value}")
        
        # Rescue Channel
        print("\n[5] RESCUE CHANNEL:")
        rescue_stats = self.rescue_channel.get_statistics()
        for key, value in rescue_stats.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.4f}")
            else:
                print(f"  {key}: {value}")
        
        print("\n  Critical nodes:")
        for node in self.rescue_channel.get_critical_nodes_status():
            print(f"    {node['node_id']}: {node['status']} "
                  f"({'FP' if node['false_positive'] else 'Real'})")
        
        print("\n" + "=" * 70)
        print("SYSTEM UPTIME: {:.2f} seconds".format(time.time() - self.start_time))
        print("=" * 70)


def main():
    """Main entry point for Lex Amoris integration demo."""
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  LEX AMORIS - STRATEGIC IMPROVEMENTS INTEGRATION DEMO  ".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("║" + "  Based on Lex Amoris Principles  ".center(68) + "║")
    print("║" + "  Hannes Mitterer - Resonance School  ".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    # Initialize integrated system
    system = LexAmorisIntegratedSystem(initial_nodes=144)
    
    # Run demo
    system.run_demo(cycles=30)
    
    print("\n" + "=" * 70)
    print("Demo complete!")
    print("All Lex Amoris strategic improvements successfully integrated.")
    print("=" * 70)


if __name__ == "__main__":
    main()
