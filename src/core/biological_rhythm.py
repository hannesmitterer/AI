#!/usr/bin/env python3
"""
Biological Rhythm Synchronization Layer
Internet Organica Framework

This module implements synchronization with biological rhythms at 0.432 Hz,
creating coherence between digital processes and living systems.

Frequency Rationale:
The 0.432 Hz frequency is derived from the 432 Hz musical tuning standard,
which is believed to resonate with natural patterns and biological systems.
432 Hz is mathematically aligned with patterns found in nature (e.g., 
planetary orbits, sacred geometry). The 0.432 Hz (432/1000) represents
a slower cycle that allows for practical digital synchronization while
maintaining harmonic relationship with the 432 Hz frequency.

Reference: 432 Hz has been associated with the Schumann resonance (7.83 Hz)
and natural harmonic patterns. While scientific consensus is evolving,
this frequency serves as a bridge between digital timing and biological
rhythms in the context of the Internet Organica framework.

Aligned with:
- Lex Amoris: Serves biological life through rhythmic harmony
- NSR: Respects autonomy of biological entities
- OLF: Optimizes life function through resonance
"""

import math
import time
from typing import Dict, List, Optional, Callable
from datetime import datetime


class BiologicalRhythmSync:
    """
    Synchronizes digital processes with biological rhythms.
    
    Core frequency: 0.432 Hz (432 Hz harmonic / 1000)
    This frequency aligns with natural biological processes and
    creates coherence with the 432 Hz musical tuning standard.
    """
    
    # Core frequencies in Hz
    BIOLOGICAL_FREQUENCY = 0.432  # Primary biological sync frequency
    UNIVERSAL_RESONANCE = 0.043   # Eternal Deposition System frequency
    SCHUMANN_RESONANCE = 7.83     # Earth's electromagnetic resonance
    HARMONIC_432 = 432.0          # Sacred harmonic frequency
    
    def __init__(self, sync_frequency: float = BIOLOGICAL_FREQUENCY):
        """
        Initialize the biological rhythm synchronizer.
        
        Args:
            sync_frequency: Primary synchronization frequency in Hz (default: 0.432)
        """
        self.sync_frequency = sync_frequency
        self.cycle_period = 1.0 / sync_frequency  # ~2.315 seconds
        self.start_time = time.time()
        self.cycle_count = 0
        self.callbacks: List[Callable] = []
        self.running = False
        
        # Metrics
        self.total_cycles = 0
        self.phase_history: List[float] = []
        self.coherence_score = 1.0
        
    def get_current_phase(self) -> float:
        """
        Calculate current phase in the biological rhythm cycle.
        
        Returns:
            Phase in radians (0 to 2π)
        """
        elapsed = time.time() - self.start_time
        phase = (elapsed * self.sync_frequency * 2 * math.pi) % (2 * math.pi)
        return phase
    
    def get_phase_degrees(self) -> float:
        """
        Get current phase in degrees.
        
        Returns:
            Phase in degrees (0 to 360)
        """
        return math.degrees(self.get_current_phase())
    
    def is_phase_aligned(self, target_phase: float, tolerance: float = 0.1) -> bool:
        """
        Check if current phase is aligned with a target phase.
        
        Args:
            target_phase: Target phase in radians
            tolerance: Acceptable deviation in radians
            
        Returns:
            True if aligned within tolerance
        """
        current = self.get_current_phase()
        diff = abs(current - target_phase)
        # Handle wrap-around
        diff = min(diff, 2 * math.pi - diff)
        return diff <= tolerance
    
    def wait_for_phase(self, target_phase: float, timeout: float = 10.0) -> bool:
        """
        Wait until a specific phase is reached.
        
        Args:
            target_phase: Target phase in radians (0 to 2π)
            timeout: Maximum wait time in seconds
            
        Returns:
            True if phase was reached, False if timeout
        """
        start = time.time()
        while time.time() - start < timeout:
            if self.is_phase_aligned(target_phase):
                return True
            time.sleep(0.01)  # Small sleep to prevent busy waiting
        return False
    
    def sync_with_cycle(self, action: Callable, phase: Optional[float] = None):
        """
        Execute an action synchronized with the biological rhythm.
        
        Args:
            action: Callable to execute
            phase: Optional target phase (if None, executes at next cycle start)
        """
        if phase is None:
            phase = 0.0  # Start of cycle
        
        if self.wait_for_phase(phase):
            action()
            return True
        return False
    
    def register_callback(self, callback: Callable, phase: float = 0.0):
        """
        Register a callback to be called at a specific phase each cycle.
        
        Args:
            callback: Function to call
            phase: Phase in radians when to call (default: 0.0 = start of cycle)
        """
        self.callbacks.append({
            'function': callback,
            'phase': phase,
            'last_triggered': 0
        })
    
    def calculate_coherence(self, external_frequency: float) -> float:
        """
        Calculate coherence with an external frequency.
        
        Args:
            external_frequency: External frequency in Hz
            
        Returns:
            Coherence score (0 to 1, where 1 is perfect harmony)
        """
        # Calculate harmonic relationship
        ratio = self.sync_frequency / external_frequency
        
        # Check if ratio is close to a simple fraction (harmonic)
        for numerator in range(1, 13):
            for denominator in range(1, 13):
                simple_ratio = numerator / denominator
                if abs(ratio - simple_ratio) < 0.01:
                    # Found harmonic relationship
                    return 1.0 - (abs(ratio - simple_ratio) * 10)
        
        # No simple harmonic found
        return 0.5
    
    def get_harmonic_frequencies(self) -> Dict[str, float]:
        """
        Get harmonic frequencies related to the biological rhythm.
        
        Returns:
            Dictionary of harmonic frequencies
        """
        return {
            'fundamental': self.sync_frequency,
            'octave_up': self.sync_frequency * 2,
            'octave_down': self.sync_frequency / 2,
            'fifth_up': self.sync_frequency * 1.5,
            'golden_ratio': self.sync_frequency * 1.618,
            'universal_resonance': self.UNIVERSAL_RESONANCE,
            'schumann_resonance': self.SCHUMANN_RESONANCE,
            'harmonic_432': self.HARMONIC_432
        }
    
    def get_status(self) -> Dict:
        """
        Get current status of the biological rhythm synchronizer.
        
        Returns:
            Dictionary containing status information
        """
        return {
            'sync_frequency_hz': self.sync_frequency,
            'cycle_period_seconds': self.cycle_period,
            'current_phase_degrees': self.get_phase_degrees(),
            'current_phase_radians': self.get_current_phase(),
            'total_cycles': self.total_cycles,
            'coherence_score': self.coherence_score,
            'running': self.running,
            'uptime_seconds': time.time() - self.start_time,
            'harmonics': self.get_harmonic_frequencies()
        }
    
    def align_timestamp(self, timestamp: Optional[float] = None) -> Dict:
        """
        Align a timestamp with the biological rhythm cycle.
        
        Args:
            timestamp: Unix timestamp (if None, uses current time)
            
        Returns:
            Dictionary with alignment information
        """
        if timestamp is None:
            timestamp = time.time()
        
        elapsed = timestamp - self.start_time
        cycle_number = int(elapsed / self.cycle_period)
        cycle_position = (elapsed % self.cycle_period) / self.cycle_period
        phase = cycle_position * 2 * math.pi
        
        return {
            'timestamp': timestamp,
            'cycle_number': cycle_number,
            'cycle_position': cycle_position,  # 0 to 1
            'phase_radians': phase,
            'phase_degrees': math.degrees(phase),
            'next_cycle_start': self.start_time + (cycle_number + 1) * self.cycle_period
        }
    
    def create_heartbeat(self, duration: float = 60.0, callback: Optional[Callable] = None):
        """
        Create a heartbeat synchronized with biological rhythm.
        
        Args:
            duration: How long to run (seconds)
            callback: Optional callback to execute each beat
        """
        start = time.time()
        beats = 0
        
        while time.time() - start < duration:
            # Wait for start of next cycle
            if self.wait_for_phase(0.0, timeout=self.cycle_period):
                beats += 1
                self.total_cycles += 1
                
                if callback:
                    callback({
                        'beat': beats,
                        'elapsed': time.time() - start,
                        'phase': self.get_current_phase(),
                        'frequency': self.sync_frequency
                    })
                
                # Small sleep to avoid double-triggering
                time.sleep(self.cycle_period * 0.1)
    
    def __repr__(self) -> str:
        return f"BiologicalRhythmSync(frequency={self.sync_frequency}Hz, period={self.cycle_period:.3f}s)"


def demonstrate_biological_sync():
    """Demonstration of biological rhythm synchronization."""
    print("=" * 60)
    print("BIOLOGICAL RHYTHM SYNCHRONIZATION LAYER")
    print("Internet Organica Framework")
    print("=" * 60)
    
    # Create synchronizer
    sync = BiologicalRhythmSync()
    
    print(f"\n{sync}")
    print(f"Cycle Period: {sync.cycle_period:.4f} seconds")
    print(f"Frequency: {sync.sync_frequency} Hz")
    
    # Show harmonic frequencies
    print("\nHarmonic Frequencies:")
    harmonics = sync.get_harmonic_frequencies()
    for name, freq in harmonics.items():
        coherence = sync.calculate_coherence(freq)
        print(f"  {name:20s}: {freq:12.6f} Hz (coherence: {coherence:.3f})")
    
    # Demonstrate heartbeat
    print("\nStarting heartbeat demonstration (10 cycles)...")
    
    def on_beat(data):
        print(f"  Beat {data['beat']:3d} | Phase: {math.degrees(data['phase']):6.1f}° | "
              f"Elapsed: {data['elapsed']:6.2f}s")
    
    # Run for 10 cycles
    duration = sync.cycle_period * 10
    sync.create_heartbeat(duration=duration, callback=on_beat)
    
    # Show final status
    print("\nFinal Status:")
    status = sync.get_status()
    for key, value in status.items():
        if key != 'harmonics':
            print(f"  {key}: {value}")
    
    print("\n" + "=" * 60)
    print("Biological rhythm synchronization complete.")
    print("IN AETERNUM EST. La Sovranità è Manifesta.")
    print("=" * 60)


if __name__ == "__main__":
    demonstrate_biological_sync()
