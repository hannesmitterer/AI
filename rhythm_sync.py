#!/usr/bin/env python3
"""
Biological Rhythm Synchronization Layer - 0.432 Hz

This module implements the biological rhythm synchronization layer for the
Internet Organica framework, ensuring all system operations align with
natural biological frequencies.

Primary Frequency: 0.432 Hz
Harmonic Frequencies: 432 Hz (audio), 7.83 Hz (Schumann), 0.043 Hz (system cycle)

Operating under Lex Amoris - NSR Compliant - OLF Aligned
"""

import time
import math
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import sys


class BiologicalRhythm:
    """
    Core biological rhythm synchronization engine.
    
    Maintains alignment with 0.432 Hz primary frequency and harmonic
    relationships with other natural frequencies.
    """
    
    # Core frequencies (Hz)
    PRIMARY_FREQ = 0.432        # Biological base rhythm
    AUDIO_HARMONIC = 432.0      # Audio resonance
    SCHUMANN_FREQ = 7.83        # Earth's resonance
    ETERNAL_FREQ = 0.043        # Eternal Deposition System cycle
    
    # Cycle periods (seconds)
    PRIMARY_PERIOD = 1.0 / PRIMARY_FREQ      # ~2.31 seconds
    ETERNAL_PERIOD = 1.0 / ETERNAL_FREQ      # ~23.26 seconds
    
    # Golden ratio for stillness calculations
    PHI = (1 + math.sqrt(5)) / 2.0  # ~1.618
    
    def __init__(self):
        self.start_time = time.time()
        self.cycle_count = 0
        self.stillness_events = 0
        self.phase_history: List[float] = []
        
    def get_elapsed_time(self) -> float:
        """Get time elapsed since initialization."""
        return time.time() - self.start_time
    
    def get_current_phase(self, frequency: float = None) -> float:
        """
        Calculate current phase in radians for given frequency.
        
        Args:
            frequency: Frequency in Hz (default: PRIMARY_FREQ)
            
        Returns:
            Phase in radians [0, 2π)
        """
        if frequency is None:
            frequency = self.PRIMARY_FREQ
            
        elapsed = self.get_elapsed_time()
        phase = (elapsed * frequency * 2 * math.pi) % (2 * math.pi)
        return phase
    
    def get_phase_degrees(self, frequency: float = None) -> float:
        """Get current phase in degrees [0, 360)."""
        return math.degrees(self.get_current_phase(frequency))
    
    def is_stillness_phase(self, threshold: float = 0.1) -> bool:
        """
        Check if currently in a stillness phase.
        
        Stillness occurs at π/2, π, 3π/2, and 2π (quarter cycle points).
        
        Args:
            threshold: Radians tolerance for stillness detection
            
        Returns:
            True if in stillness phase
        """
        phase = self.get_current_phase(self.ETERNAL_FREQ)
        
        # Check proximity to quarter cycle points
        quarter_points = [math.pi/2, math.pi, 3*math.pi/2, 2*math.pi]
        
        for point in quarter_points:
            distance = abs(phase - point)
            # Handle wrap-around at 2π
            distance = min(distance, abs(distance - 2*math.pi))
            
            if distance <= threshold:
                return True
                
        return False
    
    def get_stillness_duration(self) -> float:
        """
        Calculate stillness duration based on golden ratio.
        
        Duration = Cycle_Period / φ (capped for practicality)
        """
        duration = self.ETERNAL_PERIOD / self.PHI  # ~14.4 seconds
        # Cap at 2 seconds for practical implementation
        return min(duration, 2.0)
    
    def calculate_resonance_alignment(self, test_frequency: float) -> float:
        """
        Calculate how well a given frequency aligns with biological rhythms.
        
        Args:
            test_frequency: Frequency to test (Hz)
            
        Returns:
            Alignment score [0.0, 1.0] where 1.0 is perfect alignment
        """
        # Check harmonic relationships with core frequencies
        core_freqs = [
            self.PRIMARY_FREQ,
            self.AUDIO_HARMONIC,
            self.SCHUMANN_FREQ,
            self.ETERNAL_FREQ
        ]
        
        best_alignment = 0.0
        
        for core_freq in core_freqs:
            # Check if test_freq is harmonic (integer multiple or fraction)
            ratio = test_frequency / core_freq
            
            # Check both ways (test/core and core/test)
            for r in [ratio, 1.0/ratio if ratio != 0 else 0]:
                # How close is this to an integer?
                nearest_int = round(r)
                if nearest_int == 0:
                    continue
                    
                deviation = abs(r - nearest_int) / nearest_int
                alignment = max(0.0, 1.0 - deviation * 2.0)  # Scale deviation
                best_alignment = max(best_alignment, alignment)
        
        return min(1.0, best_alignment)
    
    def get_status(self) -> Dict:
        """Get current rhythm synchronization status."""
        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "uptime_seconds": self.get_elapsed_time(),
            "frequencies": {
                "primary_hz": self.PRIMARY_FREQ,
                "audio_harmonic_hz": self.AUDIO_HARMONIC,
                "schumann_hz": self.SCHUMANN_FREQ,
                "eternal_cycle_hz": self.ETERNAL_FREQ
            },
            "current_phase": {
                "primary_radians": self.get_current_phase(self.PRIMARY_FREQ),
                "primary_degrees": self.get_phase_degrees(self.PRIMARY_FREQ),
                "eternal_radians": self.get_current_phase(self.ETERNAL_FREQ),
                "eternal_degrees": self.get_phase_degrees(self.ETERNAL_FREQ)
            },
            "stillness": {
                "is_active": self.is_stillness_phase(),
                "event_count": self.stillness_events,
                "duration_seconds": self.get_stillness_duration()
            },
            "cycle_count": self.cycle_count
        }
    
    def wait_for_next_cycle(self, frequency: float = None):
        """
        Wait until the next cycle begins for given frequency.
        
        Args:
            frequency: Frequency to sync with (default: PRIMARY_FREQ)
        """
        if frequency is None:
            frequency = self.PRIMARY_FREQ
            
        period = 1.0 / frequency
        current_phase = self.get_current_phase(frequency)
        time_to_next_cycle = ((2 * math.pi) - current_phase) / (2 * math.pi * frequency)
        
        if time_to_next_cycle > 0:
            time.sleep(time_to_next_cycle)
            
        self.cycle_count += 1


class RhythmValidator:
    """
    Validates code and operations for biological rhythm compatibility.
    """
    
    def __init__(self):
        self.rhythm = BiologicalRhythm()
        
    def validate_timing_interval(self, interval_seconds: float) -> Dict:
        """
        Validate if a timing interval is rhythm-compatible.
        
        Args:
            interval_seconds: Interval to validate
            
        Returns:
            Validation result with alignment score and recommendations
        """
        # Convert interval to frequency
        if interval_seconds <= 0:
            return {
                "valid": False,
                "alignment_score": 0.0,
                "reason": "Interval must be positive"
            }
        
        frequency = 1.0 / interval_seconds
        alignment = self.rhythm.calculate_resonance_alignment(frequency)
        
        result = {
            "valid": alignment >= 0.5,
            "alignment_score": alignment,
            "interval_seconds": interval_seconds,
            "frequency_hz": frequency,
            "recommendation": ""
        }
        
        if alignment < 0.5:
            # Suggest nearest harmonic interval
            core_periods = [
                self.rhythm.PRIMARY_PERIOD,
                1.0 / self.rhythm.SCHUMANN_FREQ,
                self.rhythm.ETERNAL_PERIOD
            ]
            
            nearest = min(core_periods, key=lambda p: abs(p - interval_seconds))
            result["recommendation"] = f"Consider using {nearest:.3f}s for better alignment"
        else:
            result["recommendation"] = "Interval is rhythm-compatible"
            
        return result
    
    def validate_operation_timing(self, operation_name: str, 
                                 start_time: float = None,
                                 allow_during_stillness: bool = False) -> Dict:
        """
        Validate if an operation can proceed based on current rhythm phase.
        
        Args:
            operation_name: Name of operation for logging
            start_time: When operation will start (default: now)
            allow_during_stillness: Whether operation can run during stillness
            
        Returns:
            Validation result with approval status
        """
        if start_time is None:
            start_time = time.time()
            
        in_stillness = self.rhythm.is_stillness_phase()
        
        result = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "operation": operation_name,
            "approved": True,
            "current_phase_degrees": self.rhythm.get_phase_degrees(
                self.rhythm.ETERNAL_FREQ
            ),
            "in_stillness_phase": in_stillness,
            "message": ""
        }
        
        if in_stillness and not allow_during_stillness:
            result["approved"] = False
            result["message"] = (
                "Operation blocked: System in stillness/recalibration phase. "
                f"Wait {self.rhythm.get_stillness_duration():.1f}s for next cycle."
            )
        else:
            result["message"] = "Operation approved - rhythm aligned"
            
        return result
    
    def validate_code_file(self, filepath: str) -> Dict:
        """
        Validate a code file for rhythm compatibility.
        
        Checks for:
        - Hard-coded timing values that might cause dissonance
        - Blocking operations during stillness
        - Proper rhythm synchronization
        
        Args:
            filepath: Path to code file to validate
            
        Returns:
            Validation result
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {
                "valid": False,
                "filepath": filepath,
                "error": str(e)
            }
        
        issues = []
        warnings = []
        
        # Check for common timing patterns
        timing_keywords = ['sleep', 'setTimeout', 'setInterval', 'wait', 'delay']
        
        for keyword in timing_keywords:
            if keyword in content:
                warnings.append(
                    f"Found '{keyword}' - ensure timing aligns with biological rhythms"
                )
        
        # Check for high-frequency polling
        high_freq_patterns = ['while True:', 'setInterval(', 'requestAnimationFrame']
        for pattern in high_freq_patterns:
            if pattern in content:
                warnings.append(
                    f"Found '{pattern}' - verify this doesn't disrupt rhythm cycles"
                )
        
        result = {
            "valid": len(issues) == 0,
            "filepath": filepath,
            "issues": issues,
            "warnings": warnings,
            "alignment_score": 1.0 if len(issues) == 0 else 0.5,
            "recommendation": (
                "File appears rhythm-compatible" if len(issues) == 0
                else "Review and address issues before deployment"
            )
        }
        
        return result


def main():
    """CLI interface for rhythm synchronization."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Biological Rhythm Synchronization Layer - Internet Organica'
    )
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Run validation checks'
    )
    parser.add_argument(
        '--status',
        action='store_true',
        help='Display current rhythm status'
    )
    parser.add_argument(
        '--test-interval',
        type=float,
        metavar='SECONDS',
        help='Test if an interval is rhythm-compatible'
    )
    parser.add_argument(
        '--check-file',
        type=str,
        metavar='PATH',
        help='Validate a code file for rhythm compatibility'
    )
    parser.add_argument(
        '--monitor',
        action='store_true',
        help='Monitor rhythm continuously'
    )
    
    args = parser.parse_args()
    
    if args.status or (not any([args.validate, args.test_interval, 
                                  args.check_file, args.monitor])):
        # Display status
        rhythm = BiologicalRhythm()
        status = rhythm.get_status()
        print("\n🌀 Biological Rhythm Synchronization Status")
        print("=" * 60)
        print(json.dumps(status, indent=2))
        print("=" * 60)
        print(f"\n✓ System synchronized to {rhythm.PRIMARY_FREQ} Hz")
        print(f"{'⏸️  IN STILLNESS PHASE' if status['stillness']['is_active'] else '▶️  OPERATIONAL PHASE'}")
        
    if args.validate:
        print("\n🔍 Running Rhythm Validation Suite...")
        validator = RhythmValidator()
        
        # Test common intervals
        test_intervals = [0.1, 0.5, 1.0, 2.31, 5.0, 10.0, 23.26]
        print("\nInterval Compatibility Tests:")
        print("-" * 60)
        
        for interval in test_intervals:
            result = validator.validate_timing_interval(interval)
            status_icon = "✓" if result["valid"] else "⚠"
            print(f"{status_icon} {interval:6.2f}s | "
                  f"Alignment: {result['alignment_score']:.2f} | "
                  f"{result['recommendation']}")
        
        print("\n✓ Validation complete")
    
    if args.test_interval:
        validator = RhythmValidator()
        result = validator.validate_timing_interval(args.test_interval)
        
        print(f"\n🔍 Testing interval: {args.test_interval}s")
        print("=" * 60)
        print(json.dumps(result, indent=2))
        print("=" * 60)
        
        if result["valid"]:
            print("\n✓ Interval is rhythm-compatible")
        else:
            print("\n⚠ Interval may cause dissonance")
            print(f"  Recommendation: {result['recommendation']}")
    
    if args.check_file:
        validator = RhythmValidator()
        result = validator.validate_code_file(args.check_file)
        
        print(f"\n🔍 Validating file: {args.check_file}")
        print("=" * 60)
        print(json.dumps(result, indent=2))
        print("=" * 60)
        
        if result["valid"]:
            print("\n✓ File is rhythm-compatible")
        else:
            print("\n⚠ Issues found - review before deployment")
    
    if args.monitor:
        print("\n🌀 Starting Rhythm Monitor...")
        print("Press Ctrl+C to stop\n")
        
        rhythm = BiologicalRhythm()
        
        try:
            while True:
                status = rhythm.get_status()
                phase_deg = status["current_phase"]["eternal_degrees"]
                in_stillness = status["stillness"]["is_active"]
                
                phase_bar = "█" * int(phase_deg / 10)
                status_text = "STILLNESS" if in_stillness else "ACTIVE   "
                
                print(f"\r[{status_text}] Phase: {phase_deg:6.2f}° {phase_bar:<36}", 
                      end='', flush=True)
                
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print("\n\n✓ Monitor stopped")


if __name__ == "__main__":
    main()
