#!/usr/bin/env python3
"""
Electromagnetic Signature Hardening Module
==========================================

This module implements electromagnetic signature protection through:
1. Adaptive frequency hopping protocols
2. Faraday-based shielding simulation
3. Signal obfuscation and spread spectrum techniques

Protects against SDR (Software-Defined Radio) scanning and EM surveillance.
"""

import random
import hashlib
import time
import math
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass, field
from enum import Enum


class ShieldingLevel(Enum):
    """Faraday shielding effectiveness levels."""
    NONE = 0
    LOW = 30      # 30 dB attenuation
    MEDIUM = 60   # 60 dB attenuation  
    HIGH = 90     # 90 dB attenuation
    MAXIMUM = 120 # 120 dB attenuation


@dataclass
class FrequencyChannel:
    """Represents a frequency channel for communication."""
    frequency_mhz: float
    bandwidth_khz: float
    power_dbm: float
    is_active: bool = False
    last_used: float = 0.0
    usage_count: int = 0


@dataclass
class EMSignature:
    """Electromagnetic signature profile."""
    frequency_mhz: float
    power_dbm: float
    modulation: str
    timestamp: float
    shielding_db: float = 0.0


class AdaptiveFrequencyHopper:
    """
    Implements adaptive frequency hopping for EM signature obfuscation.
    
    Uses pseudo-random frequency selection with spread spectrum techniques
    to evade detection and analysis.
    """
    
    def __init__(self, base_freq_mhz: float = 2400.0, 
                 num_channels: int = 50,
                 hop_interval_ms: float = 100.0):
        """
        Initialize frequency hopper.
        
        Args:
            base_freq_mhz: Base frequency in MHz
            num_channels: Number of frequency channels
            hop_interval_ms: Time between hops in milliseconds
        """
        self.base_freq = base_freq_mhz
        self.num_channels = num_channels
        self.hop_interval = hop_interval_ms / 1000.0  # Convert to seconds
        
        # Generate frequency channels
        self.channels: List[FrequencyChannel] = []
        self._generate_channels()
        
        # Current state
        self.current_channel_idx = 0
        self.hop_sequence: List[int] = []
        self.last_hop_time = time.time()
        
        # Statistics
        self.total_hops = 0
        self.detection_events = 0
        
    def _generate_channels(self) -> None:
        """Generate spread spectrum frequency channels."""
        channel_spacing = 5.0  # MHz between channels
        
        for i in range(self.num_channels):
            freq = self.base_freq + (i * channel_spacing)
            channel = FrequencyChannel(
                frequency_mhz=freq,
                bandwidth_khz=200.0,  # 200 kHz bandwidth per channel
                power_dbm=random.uniform(-10, 10)  # Randomize power
            )
            self.channels.append(channel)
    
    def generate_hop_sequence(self, seed: Optional[str] = None) -> List[int]:
        """
        Generate pseudo-random frequency hopping sequence.
        
        Args:
            seed: Optional seed for reproducible sequences
            
        Returns:
            List of channel indices
        """
        if seed:
            # Use cryptographic hash for sequence generation
            hash_val = int(hashlib.sha256(seed.encode()).hexdigest(), 16)
            random.seed(hash_val)
        
        # Generate pseudo-random sequence using maximal length sequence approach
        sequence = list(range(self.num_channels))
        random.shuffle(sequence)
        
        self.hop_sequence = sequence
        return sequence
    
    def hop_to_next_channel(self) -> FrequencyChannel:
        """
        Hop to next channel in sequence.
        
        Returns:
            New active channel
        """
        current_time = time.time()
        
        # Check if hop interval has elapsed
        if current_time - self.last_hop_time < self.hop_interval:
            return self.channels[self.current_channel_idx]
        
        # Deactivate current channel
        self.channels[self.current_channel_idx].is_active = False
        
        # Move to next in sequence
        if not self.hop_sequence:
            self.generate_hop_sequence()
        
        self.current_channel_idx = self.hop_sequence[self.total_hops % len(self.hop_sequence)]
        
        # Activate new channel
        channel = self.channels[self.current_channel_idx]
        channel.is_active = True
        channel.last_used = current_time
        channel.usage_count += 1
        
        # Update statistics
        self.total_hops += 1
        self.last_hop_time = current_time
        
        return channel
    
    def adapt_to_interference(self, interfered_channels: List[int]) -> None:
        """
        Adapt hopping pattern to avoid interfered channels.
        
        Args:
            interfered_channels: List of channel indices to avoid
        """
        # Remove interfered channels from sequence
        self.hop_sequence = [ch for ch in self.hop_sequence 
                            if ch not in interfered_channels]
        
        # If sequence is too small, regenerate avoiding interference
        if len(self.hop_sequence) < 10:
            available = [i for i in range(self.num_channels) 
                        if i not in interfered_channels]
            random.shuffle(available)
            self.hop_sequence = available
    
    def get_current_signature(self) -> EMSignature:
        """
        Get current electromagnetic signature.
        
        Returns:
            Current EM signature
        """
        channel = self.channels[self.current_channel_idx]
        return EMSignature(
            frequency_mhz=channel.frequency_mhz,
            power_dbm=channel.power_dbm,
            modulation="FHSS",  # Frequency Hopping Spread Spectrum
            timestamp=time.time()
        )


class FaradayShield:
    """
    Simulates Faraday cage shielding for EM protection.
    
    Provides electromagnetic isolation and signal attenuation.
    """
    
    def __init__(self, shielding_level: ShieldingLevel = ShieldingLevel.HIGH):
        """
        Initialize Faraday shield.
        
        Args:
            shielding_level: Effectiveness level of shielding
        """
        self.shielding_level = shielding_level
        self.attenuation_db = shielding_level.value
        self.is_active = False
        self.power_consumption_watts = 0.0
        
    def activate(self) -> None:
        """Activate shielding."""
        self.is_active = True
        # Shielding requires power for active components
        self.power_consumption_watts = self.attenuation_db * 0.1
        
    def deactivate(self) -> None:
        """Deactivate shielding."""
        self.is_active = False
        self.power_consumption_watts = 0.0
    
    def apply_attenuation(self, signal_strength_dbm: float) -> float:
        """
        Apply shielding attenuation to signal.
        
        Args:
            signal_strength_dbm: Input signal strength in dBm
            
        Returns:
            Attenuated signal strength in dBm
        """
        if not self.is_active:
            return signal_strength_dbm
        
        # Apply logarithmic attenuation
        attenuated = signal_strength_dbm - self.attenuation_db
        
        # Signals below noise floor are effectively blocked
        noise_floor = -120.0  # dBm
        return max(attenuated, noise_floor)
    
    def measure_effectiveness(self, test_signal_dbm: float) -> Dict[str, float]:
        """
        Measure shielding effectiveness.
        
        Args:
            test_signal_dbm: Test signal strength
            
        Returns:
            Dictionary with effectiveness metrics
        """
        input_signal = test_signal_dbm
        output_signal = self.apply_attenuation(test_signal_dbm)
        actual_attenuation = input_signal - output_signal
        
        return {
            "input_signal_dbm": input_signal,
            "output_signal_dbm": output_signal,
            "attenuation_db": actual_attenuation,
            "effectiveness_percent": min(100.0, (actual_attenuation / 120.0) * 100),
            "shielding_level": self.shielding_level.name
        }


class EMHardeningSystem:
    """
    Comprehensive electromagnetic hardening system.
    
    Combines frequency hopping, Faraday shielding, and adaptive protocols
    to protect against EM surveillance and attacks.
    """
    
    def __init__(self):
        """Initialize EM hardening system."""
        self.frequency_hopper = AdaptiveFrequencyHopper()
        self.faraday_shield = FaradayShield(ShieldingLevel.HIGH)
        
        # Generate initial hopping sequence with system entropy
        seed = hashlib.sha256(str(time.time()).encode()).hexdigest()
        self.frequency_hopper.generate_hop_sequence(seed)
        
        # Activate shielding by default
        self.faraday_shield.activate()
        
        # Threat detection
        self.detected_threats: List[Dict] = []
        self.threat_threshold_dbm = -30.0  # Signal strength threshold
        
    def detect_surveillance_attempt(self, ambient_signals: List[Tuple[float, float]]) -> bool:
        """
        Detect potential surveillance based on ambient EM signals.
        
        Args:
            ambient_signals: List of (frequency_mhz, power_dbm) tuples
            
        Returns:
            True if surveillance detected
        """
        # Check for signals near current operating frequency
        current_sig = self.frequency_hopper.get_current_signature()
        
        for freq, power in ambient_signals:
            freq_diff = abs(freq - current_sig.frequency_mhz)
            
            # If strong signal within 10 MHz and above threshold
            if freq_diff < 10.0 and power > self.threat_threshold_dbm:
                threat = {
                    "timestamp": time.time(),
                    "frequency_mhz": freq,
                    "power_dbm": power,
                    "frequency_diff_mhz": freq_diff,
                    "threat_type": "SURVEILLANCE_SCAN"
                }
                self.detected_threats.append(threat)
                return True
        
        return False
    
    def execute_evasive_action(self) -> None:
        """Execute evasive maneuvers when threat detected."""
        # Immediate frequency hop
        self.frequency_hopper.hop_to_next_channel()
        
        # Increase shielding if not at maximum
        if self.faraday_shield.shielding_level != ShieldingLevel.MAXIMUM:
            self.faraday_shield.shielding_level = ShieldingLevel.MAXIMUM
            self.faraday_shield.attenuation_db = ShieldingLevel.MAXIMUM.value
        
        # Regenerate hopping sequence with new entropy
        seed = hashlib.sha256(str(time.time()).encode()).hexdigest()
        self.frequency_hopper.generate_hop_sequence(seed)
    
    def transmit_protected(self, data: bytes) -> Dict[str, any]:
        """
        Transmit data with EM protection.
        
        Args:
            data: Data to transmit
            
        Returns:
            Transmission metadata
        """
        # Hop to next frequency
        channel = self.frequency_hopper.hop_to_next_channel()
        
        # Get current signature
        signature = self.frequency_hopper.get_current_signature()
        
        # Apply shielding to reduce external leakage
        effective_power = self.faraday_shield.apply_attenuation(signature.power_dbm)
        
        return {
            "data_size_bytes": len(data),
            "frequency_mhz": signature.frequency_mhz,
            "power_dbm": effective_power,
            "original_power_dbm": signature.power_dbm,
            "shielding_active": self.faraday_shield.is_active,
            "attenuation_db": signature.power_dbm - effective_power,
            "hop_count": self.frequency_hopper.total_hops,
            "timestamp": signature.timestamp
        }
    
    def get_protection_status(self) -> Dict[str, any]:
        """
        Get comprehensive protection status.
        
        Returns:
            Status dictionary
        """
        current_sig = self.frequency_hopper.get_current_signature()
        
        return {
            "frequency_hopping": {
                "active": True,
                "current_freq_mhz": current_sig.frequency_mhz,
                "total_hops": self.frequency_hopper.total_hops,
                "channels_available": len(self.frequency_hopper.channels),
                "hop_interval_ms": self.frequency_hopper.hop_interval * 1000
            },
            "faraday_shielding": {
                "active": self.faraday_shield.is_active,
                "level": self.faraday_shield.shielding_level.name,
                "attenuation_db": self.faraday_shield.attenuation_db,
                "power_consumption_watts": self.faraday_shield.power_consumption_watts
            },
            "threat_detection": {
                "threats_detected": len(self.detected_threats),
                "last_threat": self.detected_threats[-1] if self.detected_threats else None
            }
        }


def main():
    """Demonstrate EM hardening system."""
    print("=" * 70)
    print("ELECTROMAGNETIC HARDENING SYSTEM")
    print("=" * 70)
    
    # Initialize system
    print("\n[1] Initializing EM hardening system...")
    em_system = EMHardeningSystem()
    print("    System initialized")
    
    # Show initial status
    status = em_system.get_protection_status()
    print(f"\n[2] Initial protection status:")
    print(f"    Frequency: {status['frequency_hopping']['current_freq_mhz']:.2f} MHz")
    print(f"    Shielding: {status['faraday_shielding']['level']} ({status['faraday_shielding']['attenuation_db']} dB)")
    
    # Simulate transmissions with frequency hopping
    print(f"\n[3] Simulating protected transmissions...")
    for i in range(5):
        data = f"Message {i+1}".encode()
        tx_info = em_system.transmit_protected(data)
        print(f"    TX {i+1}: {tx_info['frequency_mhz']:.2f} MHz, "
              f"Power: {tx_info['power_dbm']:.1f} dBm (shielded)")
    
    # Simulate surveillance detection
    print(f"\n[4] Simulating surveillance scan...")
    ambient_signals = [
        (2405.0, -25.0),  # Strong signal near operating frequency
        (2450.0, -40.0),
        (2480.0, -35.0)
    ]
    
    detected = em_system.detect_surveillance_attempt(ambient_signals)
    if detected:
        print(f"    ⚠ THREAT DETECTED: Surveillance scan identified")
        print(f"    Executing evasive action...")
        em_system.execute_evasive_action()
        print(f"    ✓ Countermeasures deployed")
    
    # Final status
    final_status = em_system.get_protection_status()
    print(f"\n[5] Final protection status:")
    print(f"    Total hops: {final_status['frequency_hopping']['total_hops']}")
    print(f"    Threats detected: {final_status['threat_detection']['threats_detected']}")
    print(f"    Current frequency: {final_status['frequency_hopping']['current_freq_mhz']:.2f} MHz")
    
    print("\n" + "=" * 70)
    print("EM hardening demonstration complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
