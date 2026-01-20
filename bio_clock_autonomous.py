#!/usr/bin/env python3
"""
Bio-Clock Autonomous Signal Module - 0.0043 Hz Isolation
=========================================================

Implements autonomous operation of the 0.0043 Hz bio-clock signal
using decentralized time references, independent of EU NTP servers.

Features:
- Cryptographic timestamp verification
- Local hardware oscillator simulation
- NTP-free operation with drift compensation
- Resilient against digital blackouts

Response to EU 2026 Framework - Protocol EUYSTACIO/NSR
"""

import time
import hashlib
import hmac
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timezone
import math


# Bio-Clock Constants
BIO_CLOCK_FREQUENCY_HZ = 0.0043  # 0.0043 Hz signal (232.56 second cycle)
BIO_CLOCK_PERIOD_SECONDS = 1.0 / BIO_CLOCK_FREQUENCY_HZ  # ~232.56 seconds
MAX_DRIFT_TOLERANCE_MS = 50  # Maximum acceptable drift in milliseconds
CRYPTO_SIGNATURE_STRENGTH = 32  # SHA-256 bytes


@dataclass
class CryptoTimestamp:
    """
    Cryptographically signed timestamp for verification.
    Ensures temporal integrity without relying on external NTP.
    """
    epoch_time: float
    monotonic_time: float
    signature: str
    sequence_number: int
    previous_hash: Optional[str] = None
    
    def verify(self, secret_key: bytes) -> bool:
        """Verify the cryptographic signature of this timestamp."""
        data = f"{self.epoch_time}:{self.monotonic_time}:{self.sequence_number}".encode()
        expected_sig = hmac.new(secret_key, data, hashlib.sha256).hexdigest()
        return hmac.compare_digest(self.signature, expected_sig)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "epoch_time": self.epoch_time,
            "monotonic_time": self.monotonic_time,
            "signature": self.signature,
            "sequence_number": self.sequence_number,
            "previous_hash": self.previous_hash
        }


class HardwareOscillator:
    """
    Simulates a local hardware oscillator for autonomous timekeeping.
    
    In production, this would interface with actual hardware oscillators
    (e.g., crystal oscillators, atomic clocks, or GPS disciplined oscillators).
    """
    
    def __init__(self, base_frequency: float = BIO_CLOCK_FREQUENCY_HZ):
        """
        Initialize the hardware oscillator.
        
        Args:
            base_frequency: Target frequency in Hz
        """
        self.base_frequency = base_frequency
        self.period_seconds = 1.0 / base_frequency
        self.start_monotonic = time.monotonic()
        self.drift_compensation = 0.0  # Accumulated drift correction
        self.last_calibration = time.monotonic()
        
    def get_cycle_phase(self) -> float:
        """
        Get current phase in the oscillator cycle.
        
        Returns:
            Phase value between 0 and 2π
        """
        elapsed = time.monotonic() - self.start_monotonic + self.drift_compensation
        phase = (elapsed * self.base_frequency * 2 * math.pi) % (2 * math.pi)
        return phase
    
    def get_cycle_count(self) -> int:
        """Get the number of complete cycles since start."""
        elapsed = time.monotonic() - self.start_monotonic + self.drift_compensation
        return int(elapsed / self.period_seconds)
    
    def calibrate(self, reference_time: float) -> float:
        """
        Calibrate oscillator against a trusted reference.
        
        Args:
            reference_time: Trusted reference time
            
        Returns:
            Drift correction applied in seconds
        """
        current = time.monotonic()
        expected_cycles = (reference_time - self.start_monotonic) / self.period_seconds
        actual_cycles = self.get_cycle_count()
        
        drift = (expected_cycles - actual_cycles) * self.period_seconds
        self.drift_compensation += drift
        self.last_calibration = current
        
        return drift


class AutonomousBioClock:
    """
    Autonomous Bio-Clock Signal Generator (0.0043 Hz)
    
    Operates independently of EU NTP servers using:
    - Local hardware oscillator
    - Cryptographic timestamp chain
    - Self-calibrating drift compensation
    """
    
    def __init__(self, secret_key: Optional[bytes] = None):
        """
        Initialize autonomous bio-clock.
        
        Args:
            secret_key: Secret key for cryptographic signatures (auto-generated if None)
        """
        # Initialize secret key for cryptographic signatures
        if secret_key is None:
            secret_key = hashlib.sha256(
                f"EUYSTACIO_NSR_{time.time()}".encode()
            ).digest()
        self.secret_key = secret_key
        
        # Initialize local oscillator
        self.oscillator = HardwareOscillator(BIO_CLOCK_FREQUENCY_HZ)
        
        # Timestamp chain for verification
        self.timestamp_chain: List[CryptoTimestamp] = []
        self.sequence_counter = 0
        
        # Operational status
        self.is_autonomous = True  # Always true in autonomous mode
        self.last_ntp_sync = None  # Track when NTP was last available (if ever)
        self.drift_history: List[float] = []
        
        print("[BIO-CLOCK] Autonomous mode initialized")
        print(f"[BIO-CLOCK] Frequency: {BIO_CLOCK_FREQUENCY_HZ} Hz")
        print(f"[BIO-CLOCK] Period: {BIO_CLOCK_PERIOD_SECONDS:.2f} seconds")
        print("[BIO-CLOCK] NTP-independent operation enabled")
    
    def generate_timestamp(self) -> CryptoTimestamp:
        """
        Generate a cryptographically signed timestamp.
        
        Returns:
            CryptoTimestamp object with signature and chain link
        """
        epoch_time = time.time()
        monotonic_time = time.monotonic()
        
        # Create signature data
        data = f"{epoch_time}:{monotonic_time}:{self.sequence_counter}".encode()
        signature = hmac.new(self.secret_key, data, hashlib.sha256).hexdigest()
        
        # Link to previous timestamp (blockchain-like chain)
        previous_hash = None
        if self.timestamp_chain:
            prev_ts = self.timestamp_chain[-1]
            prev_data = json.dumps(prev_ts.to_dict(), sort_keys=True)
            previous_hash = hashlib.sha256(prev_data.encode()).hexdigest()
        
        timestamp = CryptoTimestamp(
            epoch_time=epoch_time,
            monotonic_time=monotonic_time,
            signature=signature,
            sequence_number=self.sequence_counter,
            previous_hash=previous_hash
        )
        
        # Add to chain
        self.timestamp_chain.append(timestamp)
        self.sequence_counter += 1
        
        # Maintain reasonable chain length (keep last 1000 timestamps)
        if len(self.timestamp_chain) > 1000:
            self.timestamp_chain = self.timestamp_chain[-1000:]
        
        return timestamp
    
    def verify_timestamp_chain(self) -> bool:
        """
        Verify the integrity of the timestamp chain.
        
        Returns:
            True if chain is valid, False otherwise
        """
        if not self.timestamp_chain:
            return True
        
        # Verify each timestamp signature
        for ts in self.timestamp_chain:
            if not ts.verify(self.secret_key):
                print(f"[BIO-CLOCK] Chain verification failed at sequence {ts.sequence_number}")
                return False
        
        # Verify chain links
        for i in range(1, len(self.timestamp_chain)):
            current = self.timestamp_chain[i]
            previous = self.timestamp_chain[i - 1]
            
            prev_data = json.dumps(previous.to_dict(), sort_keys=True)
            expected_hash = hashlib.sha256(prev_data.encode()).hexdigest()
            
            if current.previous_hash != expected_hash:
                print(f"[BIO-CLOCK] Chain link broken at sequence {current.sequence_number}")
                return False
        
        return True
    
    def get_signal_state(self) -> Dict:
        """
        Get current state of the bio-clock signal.
        
        Returns:
            Dictionary with signal parameters
        """
        phase = self.oscillator.get_cycle_phase()
        cycle_count = self.oscillator.get_cycle_count()
        timestamp = self.generate_timestamp()
        
        # Calculate signal amplitude (sine wave at bio-clock frequency)
        amplitude = math.sin(phase)
        
        return {
            "frequency_hz": BIO_CLOCK_FREQUENCY_HZ,
            "phase_radians": phase,
            "phase_degrees": math.degrees(phase),
            "cycle_count": cycle_count,
            "amplitude": amplitude,
            "timestamp": timestamp.to_dict(),
            "autonomous_mode": self.is_autonomous,
            "chain_valid": self.verify_timestamp_chain(),
            "drift_compensation": self.oscillator.drift_compensation
        }
    
    def sync_with_trusted_source(self, trusted_timestamp: float) -> None:
        """
        Optionally sync with a trusted decentralized time source.
        
        This could be blockchain timestamps, GPS time, or peer consensus.
        NOT EU NTP servers.
        
        Args:
            trusted_timestamp: Trusted reference timestamp
        """
        drift = self.oscillator.calibrate(trusted_timestamp)
        self.drift_history.append(drift)
        
        # Keep drift history manageable
        if len(self.drift_history) > 100:
            self.drift_history = self.drift_history[-100:]
        
        print(f"[BIO-CLOCK] Calibrated with trusted source, drift: {drift*1000:.2f} ms")
    
    def get_status(self) -> Dict:
        """Get comprehensive bio-clock status."""
        return {
            "autonomous_mode": self.is_autonomous,
            "frequency_hz": BIO_CLOCK_FREQUENCY_HZ,
            "period_seconds": BIO_CLOCK_PERIOD_SECONDS,
            "cycle_count": self.oscillator.get_cycle_count(),
            "sequence_number": self.sequence_counter,
            "timestamp_chain_length": len(self.timestamp_chain),
            "timestamp_chain_valid": self.verify_timestamp_chain(),
            "drift_compensation_ms": self.oscillator.drift_compensation * 1000,
            "avg_drift_ms": sum(self.drift_history) * 1000 / len(self.drift_history) if self.drift_history else 0
        }
    
    def export_chain(self, filepath: str) -> None:
        """
        Export timestamp chain for backup or verification.
        
        Args:
            filepath: Path to save the chain
        """
        chain_data = {
            "version": "1.0",
            "frequency_hz": BIO_CLOCK_FREQUENCY_HZ,
            "chain": [ts.to_dict() for ts in self.timestamp_chain],
            "exported_at": datetime.now(timezone.utc).isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(chain_data, f, indent=2)
        
        print(f"[BIO-CLOCK] Chain exported to {filepath}")


def main():
    """Demonstration of autonomous bio-clock operation."""
    print("=" * 70)
    print("AUTONOMOUS BIO-CLOCK SIGNAL - 0.0043 Hz")
    print("EU 2026 Resilience Protocol - EUYSTACIO/NSR")
    print("=" * 70)
    print()
    
    # Initialize autonomous bio-clock
    bio_clock = AutonomousBioClock()
    
    # Display status
    print("\n[STATUS]")
    status = bio_clock.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Generate a few signal states
    print("\n[SIGNAL STATES]")
    for i in range(5):
        state = bio_clock.get_signal_state()
        print(f"\nCycle {state['cycle_count']}:")
        print(f"  Phase: {state['phase_degrees']:.2f}°")
        print(f"  Amplitude: {state['amplitude']:.4f}")
        print(f"  Chain Valid: {state['chain_valid']}")
        time.sleep(1)
    
    # Export chain for verification
    bio_clock.export_chain("bio_clock_chain.json")
    
    print("\n[BIO-CLOCK] Autonomous operation verified")


if __name__ == "__main__":
    main()
