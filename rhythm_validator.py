#!/usr/bin/env python3
"""
Rhythm Validator - Dynamic Blacklist and Behavioral Security
=============================================================

This module implements rhythm validation for behavioral security based on
Lex Amoris principles. Every data packet is validated against the correct
resonance frequency (0.043 Hz) regardless of IP origin.

Key Features:
- Frequency-based packet validation
- Dynamic blacklist management
- Behavioral security through rhythm analysis
- Integration with Eternal Deposition System
"""

import time
import math
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime


# Universal resonance frequency (aligned with Eternal Deposition)
UNIVERSAL_RESONANCE_HZ = 0.043
FREQUENCY_TOLERANCE = 0.005  # ±0.005 Hz tolerance
MIN_FREQUENCY = UNIVERSAL_RESONANCE_HZ - FREQUENCY_TOLERANCE
MAX_FREQUENCY = UNIVERSAL_RESONANCE_HZ + FREQUENCY_TOLERANCE


@dataclass
class PacketSignature:
    """Represents a data packet with its rhythm signature."""
    packet_id: str
    source_ip: str
    timestamp: float
    frequency: float
    phase: float
    energy: float = 1.0
    
    def is_valid_rhythm(self) -> bool:
        """Check if packet vibrates at correct frequency."""
        return MIN_FREQUENCY <= self.frequency <= MAX_FREQUENCY
    
    def calculate_resonance_score(self) -> float:
        """
        Calculate how well the packet resonates with universal frequency.
        
        Returns:
            Score between 0.0 (no resonance) and 1.0 (perfect resonance)
        """
        frequency_deviation = abs(self.frequency - UNIVERSAL_RESONANCE_HZ)
        max_deviation = FREQUENCY_TOLERANCE
        
        if frequency_deviation > max_deviation:
            return 0.0
        
        # Linear decay from 1.0 (perfect) to 0.0 (max deviation)
        score = 1.0 - (frequency_deviation / max_deviation)
        return score


@dataclass
class BlacklistEntry:
    """Represents an entry in the dynamic blacklist."""
    source_ip: str
    reason: str
    timestamp: float
    violation_count: int = 1
    last_violation: float = field(default_factory=time.time)
    
    def should_expire(self, ttl_seconds: float = 3600) -> bool:
        """Check if blacklist entry should expire."""
        current_time = time.time()
        return (current_time - self.timestamp) > ttl_seconds


class RhythmValidator:
    """
    Main rhythm validation engine for behavioral security.
    
    Validates data packets based on frequency resonance rather than
    traditional IP-based security. Implements dynamic blacklist for
    sources that consistently violate rhythm requirements.
    """
    
    def __init__(self, strict_mode: bool = True):
        """
        Initialize rhythm validator.
        
        Args:
            strict_mode: If True, reject any packet outside tolerance
        """
        self.strict_mode = strict_mode
        self.blacklist: Dict[str, BlacklistEntry] = {}
        self.validation_history: List[Dict] = []
        self.total_validated = 0
        self.total_rejected = 0
        self.start_time = time.time()
        
        print(f"[RHYTHM VALIDATOR] Initialized")
        print(f"[RHYTHM VALIDATOR] Universal frequency: {UNIVERSAL_RESONANCE_HZ} Hz")
        print(f"[RHYTHM VALIDATOR] Tolerance: ±{FREQUENCY_TOLERANCE} Hz")
        print(f"[RHYTHM VALIDATOR] Strict mode: {strict_mode}")
    
    def calculate_packet_frequency(self, packet_data: bytes) -> float:
        """
        Calculate frequency signature of a data packet.
        
        In a real implementation, this would analyze the packet's
        temporal characteristics. For demonstration, we use a 
        hash-based approach to derive frequency.
        
        Args:
            packet_data: Raw packet bytes
            
        Returns:
            Calculated frequency in Hz
        """
        # Hash-based frequency derivation (demonstration)
        packet_hash = hash(packet_data)
        # Map hash to frequency range around universal resonance
        normalized = (packet_hash % 1000) / 1000.0  # 0.0 to 1.0
        
        # Map to range: [0.038 to 0.048] Hz (±0.005 from 0.043)
        frequency_range = 0.010  # Total range
        min_freq = UNIVERSAL_RESONANCE_HZ - FREQUENCY_TOLERANCE
        frequency = min_freq + (normalized * frequency_range)
        
        return frequency
    
    def validate_packet(self, packet: PacketSignature) -> Tuple[bool, str]:
        """
        Validate a packet based on rhythm analysis.
        
        Args:
            packet: PacketSignature to validate
            
        Returns:
            Tuple of (is_valid, reason)
        """
        self.total_validated += 1
        
        # Check if source is blacklisted
        if packet.source_ip in self.blacklist:
            entry = self.blacklist[packet.source_ip]
            if not entry.should_expire():
                self.total_rejected += 1
                return False, f"Source blacklisted: {entry.reason}"
            else:
                # Remove expired entry
                del self.blacklist[packet.source_ip]
        
        # Validate rhythm/frequency
        if not packet.is_valid_rhythm():
            reason = f"Invalid frequency: {packet.frequency:.6f} Hz (expected {UNIVERSAL_RESONANCE_HZ} ± {FREQUENCY_TOLERANCE})"
            self._add_violation(packet.source_ip, reason)
            self.total_rejected += 1
            
            # Log rejection
            self._log_validation(packet, False, reason)
            
            return False, reason
        
        # Calculate resonance score
        resonance_score = packet.calculate_resonance_score()
        
        # In strict mode, require high resonance
        if self.strict_mode and resonance_score < 0.7:
            reason = f"Low resonance score: {resonance_score:.4f} (minimum 0.7 required)"
            self._add_violation(packet.source_ip, reason)
            self.total_rejected += 1
            
            self._log_validation(packet, False, reason)
            
            return False, reason
        
        # Packet validated successfully
        self._log_validation(packet, True, f"Resonance score: {resonance_score:.4f}")
        
        return True, f"Valid rhythm - resonance score: {resonance_score:.4f}"
    
    def _add_violation(self, source_ip: str, reason: str) -> None:
        """
        Add or update violation record for a source.
        
        Args:
            source_ip: Source IP address
            reason: Violation reason
        """
        current_time = time.time()
        
        if source_ip in self.blacklist:
            entry = self.blacklist[source_ip]
            entry.violation_count += 1
            entry.last_violation = current_time
            entry.reason = reason  # Update to latest reason
        else:
            # Add new blacklist entry after first violation
            self.blacklist[source_ip] = BlacklistEntry(
                source_ip=source_ip,
                reason=reason,
                timestamp=current_time,
                violation_count=1,
                last_violation=current_time
            )
        
        # Auto-blacklist after 3 violations
        if self.blacklist[source_ip].violation_count >= 3:
            print(f"[BLACKLIST] Source {source_ip} blacklisted after {self.blacklist[source_ip].violation_count} violations")
    
    def _log_validation(self, packet: PacketSignature, valid: bool, reason: str) -> None:
        """
        Log validation event.
        
        Args:
            packet: Validated packet
            valid: Whether validation passed
            reason: Validation reason/message
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "packet_id": packet.packet_id,
            "source_ip": packet.source_ip,
            "frequency": packet.frequency,
            "valid": valid,
            "reason": reason
        }
        
        self.validation_history.append(log_entry)
        
        # Keep only recent history (last 1000 validations)
        if len(self.validation_history) > 1000:
            self.validation_history = self.validation_history[-1000:]
    
    def cleanup_blacklist(self) -> int:
        """
        Remove expired entries from blacklist.
        
        Returns:
            Number of entries removed
        """
        expired = [
            ip for ip, entry in self.blacklist.items()
            if entry.should_expire()
        ]
        
        for ip in expired:
            del self.blacklist[ip]
        
        if expired:
            print(f"[BLACKLIST] Removed {len(expired)} expired entries")
        
        return len(expired)
    
    def get_statistics(self) -> Dict:
        """Get validation statistics."""
        uptime = time.time() - self.start_time
        
        return {
            "uptime_seconds": uptime,
            "total_validated": self.total_validated,
            "total_rejected": self.total_rejected,
            "rejection_rate": self.total_rejected / max(1, self.total_validated),
            "blacklist_size": len(self.blacklist),
            "strict_mode": self.strict_mode,
            "universal_frequency_hz": UNIVERSAL_RESONANCE_HZ,
            "frequency_tolerance_hz": FREQUENCY_TOLERANCE
        }
    
    def get_blacklist_entries(self) -> List[Dict]:
        """Get current blacklist entries."""
        return [
            {
                "source_ip": ip,
                "reason": entry.reason,
                "violations": entry.violation_count,
                "timestamp": datetime.fromtimestamp(entry.timestamp).isoformat(),
                "age_seconds": time.time() - entry.timestamp
            }
            for ip, entry in self.blacklist.items()
        ]


def create_test_packet(source_ip: str, frequency: Optional[float] = None,
                       packet_id: Optional[str] = None) -> PacketSignature:
    """
    Create a test packet with specified or random frequency.
    
    Args:
        source_ip: Source IP address
        frequency: Optional frequency (if None, uses universal resonance)
        packet_id: Optional packet ID (if None, auto-generated)
        
    Returns:
        PacketSignature instance
    """
    if packet_id is None:
        packet_id = f"pkt_{int(time.time() * 1000)}"
    
    if frequency is None:
        frequency = UNIVERSAL_RESONANCE_HZ
    
    current_time = time.time()
    phase = (current_time * frequency * 2 * math.pi) % (2 * math.pi)
    
    return PacketSignature(
        packet_id=packet_id,
        source_ip=source_ip,
        timestamp=current_time,
        frequency=frequency,
        phase=phase
    )


def main():
    """Demonstration of rhythm validation."""
    print("=" * 70)
    print("RHYTHM VALIDATOR - Behavioral Security Demo")
    print("Based on Lex Amoris Principles")
    print("=" * 70)
    print()
    
    validator = RhythmValidator(strict_mode=True)
    
    # Test 1: Valid packet at correct frequency
    print("\n[TEST 1] Valid packet at universal frequency:")
    packet1 = create_test_packet("192.168.1.100", UNIVERSAL_RESONANCE_HZ)
    valid, reason = validator.validate_packet(packet1)
    print(f"  Result: {'✓ ACCEPTED' if valid else '✗ REJECTED'}")
    print(f"  Reason: {reason}")
    
    # Test 2: Invalid packet - wrong frequency
    print("\n[TEST 2] Invalid packet - wrong frequency:")
    packet2 = create_test_packet("192.168.1.101", 0.055)  # Too high
    valid, reason = validator.validate_packet(packet2)
    print(f"  Result: {'✓ ACCEPTED' if valid else '✗ REJECTED'}")
    print(f"  Reason: {reason}")
    
    # Test 3: Multiple violations from same source
    print("\n[TEST 3] Multiple violations from same source:")
    for i in range(4):
        packet = create_test_packet("192.168.1.102", 0.030)  # Too low
        valid, reason = validator.validate_packet(packet)
        print(f"  Attempt {i+1}: {'✓ ACCEPTED' if valid else '✗ REJECTED'}")
    
    # Test 4: Valid packet at edge of tolerance
    print("\n[TEST 4] Valid packet at tolerance edge:")
    packet4 = create_test_packet("192.168.1.103", UNIVERSAL_RESONANCE_HZ + FREQUENCY_TOLERANCE * 0.8)
    valid, reason = validator.validate_packet(packet4)
    print(f"  Result: {'✓ ACCEPTED' if valid else '✗ REJECTED'}")
    print(f"  Reason: {reason}")
    
    # Display statistics
    print("\n" + "-" * 70)
    print("Statistics:")
    stats = validator.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.4f}")
        else:
            print(f"  {key}: {value}")
    
    # Display blacklist
    print("\n" + "-" * 70)
    print("Blacklist Entries:")
    blacklist = validator.get_blacklist_entries()
    if blacklist:
        for entry in blacklist:
            print(f"  IP: {entry['source_ip']}")
            print(f"    Violations: {entry['violations']}")
            print(f"    Reason: {entry['reason']}")
            print(f"    Age: {entry['age_seconds']:.2f}s")
    else:
        print("  (No blacklisted sources)")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
