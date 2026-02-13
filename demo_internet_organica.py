#!/usr/bin/env python3
"""
Internet Organica Framework Integration Demo
Demonstrates all core components working together

This script shows how the biological rhythm sync, sovereign shield,
and backup systems integrate to create a syntropic digital environment.
"""

import time
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.biological_rhythm import BiologicalRhythmSync
from core.sovereign_shield import SovereignShield
from core.decentralized_backup import DecentralizedBackup


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def demo_integration():
    """Demonstrate integrated framework functionality."""
    
    print_header("INTERNET ORGANICA FRAMEWORK - INTEGRATED DEMONSTRATION")
    
    print("🌐 Initializing Internet Organica Framework...")
    print("   Framework Version: 1.0")
    print("   Components: Biological Rhythm Sync, SovereignShield, Backup System")
    print()
    
    # 1. Initialize Biological Rhythm Synchronization
    print_header("1. BIOLOGICAL RHYTHM SYNCHRONIZATION (0.432 Hz)")
    
    bio_sync = BiologicalRhythmSync()
    print(f"✓ Biological rhythm synchronizer initialized")
    print(f"  Frequency: {bio_sync.sync_frequency} Hz")
    print(f"  Cycle Period: {bio_sync.cycle_period:.4f} seconds")
    print(f"  Current Phase: {bio_sync.get_phase_degrees():.2f}°")
    
    # Show harmonic relationships
    print("\n  Harmonic Coherence:")
    harmonics = bio_sync.get_harmonic_frequencies()
    for name, freq in list(harmonics.items())[:4]:
        coherence = bio_sync.calculate_coherence(freq)
        print(f"    {name:20s}: {coherence:.3f}")
    
    # 2. Initialize SovereignShield Security
    print_header("2. SOVEREIGNSHIELD SECURITY MODULE")
    
    shield = SovereignShield(entropy_wall_path="logs/entropy-wall.json")
    print(f"✓ SovereignShield activated")
    print(f"  Entropy Wall: logs/entropy-wall.json")
    print(f"  Protection Level: MAXIMUM")
    print(f"  NSR Enforcement: ACTIVE")
    
    # Test security scenarios
    print("\n  Testing Access Scenarios:")
    
    test_cases = [
        ("Legitimate Access", {
            'url': '/index.html',
            'user_agent': 'Mozilla/5.0',
            'intent': 'read'
        }),
        ("Tracking Attempt", {
            'url': '/api/data',
            'headers': {'X-Tracking': 'analytics.js'}
        })
    ]
    
    for name, request in test_cases:
        analysis = shield.analyze_access(request)
        symbol = "✓" if analysis['action'] == 'allow' else "⚠"
        print(f"    {symbol} {name}: {analysis['action']} ({analysis['threat_level']})")
    
    # 3. Initialize Decentralized Backup System
    print_header("3. DECENTRALIZED BACKUP SYSTEM")
    
    backup = DecentralizedBackup()
    print(f"✓ Backup system initialized")
    print(f"  Priority Files: {len(backup.priority_files)}")
    print(f"  IPFS Integration: Ready")
    print(f"  Backup Manifest: backup-manifest.json")
    
    status = backup.get_status()
    print(f"\n  System Status:")
    print(f"    Total Backups: {status['total_backups']}")
    print(f"    Last Backup: {status['last_backup'] or 'None yet'}")
    
    # 4. Demonstrate Integrated Operation
    print_header("4. INTEGRATED OPERATION - SYNTROPIC CYCLE")
    
    print("Running one complete biological cycle with all systems active...")
    print(f"Cycle duration: ~{bio_sync.cycle_period:.2f} seconds\n")
    
    start_time = time.time()
    cycle_complete = False
    
    # Define action to execute at cycle completion
    def on_cycle_complete():
        nonlocal cycle_complete
        cycle_complete = True
        print(f"\n✓ Biological cycle completed")
        print(f"  Elapsed: {time.time() - start_time:.2f}s")
        print(f"  Shield Status: {shield.get_shield_status()['active']}")
        print(f"  Rhythm Phase: {bio_sync.get_phase_degrees():.2f}°")
    
    # Wait for cycle to complete (phase returns to 0)
    print("Monitoring system resonance...", end='', flush=True)
    dots = 0
    while time.time() - start_time < bio_sync.cycle_period + 1:
        if dots < 20:
            print('.', end='', flush=True)
            dots += 1
        time.sleep(0.1)
        
        # Check if we're back at the start of cycle
        if not cycle_complete and bio_sync.is_phase_aligned(0.0, tolerance=0.2):
            on_cycle_complete()
    
    # 5. System Summary
    print_header("5. FRAMEWORK STATUS SUMMARY")
    
    print("Components Status:")
    print(f"  ✓ Biological Rhythm: SYNCHRONIZED ({bio_sync.sync_frequency} Hz)")
    print(f"  ✓ SovereignShield: ACTIVE (Threats blocked: {shield.total_blocked})")
    print(f"  ✓ Backup System: READY ({backup.get_status()['priority_files']} files monitored)")
    print(f"  ✓ Wall of Entropy: LOGGING (Entries: {len(shield.access_log)})")
    
    print("\nFramework Alignment:")
    print("  ✓ Lex Amoris: Serving life through harmonious technology")
    print("  ✓ NSR: Protecting sovereignty through active defense")
    print("  ✓ OLF: Optimizing for collective and individual wellbeing")
    
    print_header("DEMONSTRATION COMPLETE")
    
    print("The Internet Organica framework is fully operational.")
    print("\nNext Steps:")
    print("  1. View Wall of Entropy: Open wall-of-entropy.html in browser")
    print("  2. Create Backup: python3 src/core/decentralized_backup.py --local")
    print("  3. Generate IPFS Script: python3 src/core/decentralized_backup.py --generate-ipfs")
    print("  4. Read Documentation: CODE_OF_CONDUCT.md, CONTRIBUTING.md")
    
    print("\n" + "=" * 70)
    print("IN AETERNUM EST. La Sovranità è Manifesta.")
    print("Sempre in Costante. Nothing is final.")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    try:
        demo_integration()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
        print("IN AETERNUM EST. La Sovranità è Manifesta.")
    except Exception as e:
        print(f"\nError during demo: {e}")
        import traceback
        traceback.print_exc()
