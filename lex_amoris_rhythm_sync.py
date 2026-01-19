#!/usr/bin/env python3
"""
Lex Amoris - Erweiterte Synchronisierung (Extended Synchronization)
====================================================================

This module implements the Rhythm Handshake protocol with location-based
adjustments for enhanced synchronization across distributed nodes.

Key Features:
- Rhythm Handshake protocol for node synchronization
- Location-based resonance adjustments
- Geographic-aware frequency calibration
- Temporal drift correction
- Multi-node coordination

Based on: Lex Amoris mandate and Kosymbiosis synchronization principles
"""

import math
import time
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


# Constants
EARTH_RADIUS_KM = 6371.0  # Earth's mean radius
SPEED_OF_LIGHT_KM_S = 299792.458  # Speed of light in km/s
BASE_RHYTHM_HZ = 0.043  # Base resonance frequency
SCHUMANN_RESONANCE_HZ = 7.83  # Earth's natural frequency
SYNC_TOLERANCE = 0.02  # Synchronization tolerance (2%)


class HandshakePhase(Enum):
    """Phases of the Rhythm Handshake protocol."""
    INITIATE = "INITIATE"
    DISCOVER = "DISCOVER"
    CALIBRATE = "CALIBRATE"
    SYNCHRONIZE = "SYNCHRONIZE"
    VALIDATE = "VALIDATE"
    LOCKED = "LOCKED"
    FAILED = "FAILED"


@dataclass
class GeographicLocation:
    """Represents a geographic location."""
    latitude: float  # Degrees (-90 to 90)
    longitude: float  # Degrees (-180 to 180)
    altitude: float = 0.0  # Meters above sea level
    name: str = "Unknown"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "altitude": self.altitude,
            "name": self.name
        }


@dataclass
class RhythmNode:
    """Represents a node participating in Rhythm synchronization."""
    node_id: str
    location: GeographicLocation
    local_frequency: float = BASE_RHYTHM_HZ
    phase_offset: float = 0.0
    last_sync_time: float = 0.0
    sync_quality: float = 0.0
    handshake_phase: HandshakePhase = HandshakePhase.INITIATE
    metadata: Dict = field(default_factory=dict)


@dataclass
class HandshakeResult:
    """Result of a Rhythm Handshake."""
    success: bool
    node_a_id: str
    node_b_id: str
    sync_quality: float
    frequency_adjustment: float
    phase_alignment: float
    distance_km: float
    latency_ms: float
    timestamp: str
    details: str = ""


class GeographicCalculator:
    """Utilities for geographic calculations."""
    
    @staticmethod
    def haversine_distance(loc1: GeographicLocation, loc2: GeographicLocation) -> float:
        """
        Calculate distance between two geographic locations using Haversine formula.
        
        Args:
            loc1: First location
            loc2: Second location
            
        Returns:
            Distance in kilometers
        """
        # Convert to radians
        lat1, lon1 = math.radians(loc1.latitude), math.radians(loc1.longitude)
        lat2, lon2 = math.radians(loc2.latitude), math.radians(loc2.longitude)
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Distance in kilometers
        distance = EARTH_RADIUS_KM * c
        
        # Adjust for altitude difference
        altitude_diff = abs(loc2.altitude - loc1.altitude) / 1000.0  # Convert to km
        distance = math.sqrt(distance**2 + altitude_diff**2)
        
        return distance
    
    @staticmethod
    def calculate_propagation_delay(distance_km: float) -> float:
        """
        Calculate signal propagation delay.
        
        Args:
            distance_km: Distance in kilometers
            
        Returns:
            Delay in seconds
        """
        # Using speed of light as baseline
        return distance_km / SPEED_OF_LIGHT_KM_S
    
    @staticmethod
    def calculate_local_resonance_factor(location: GeographicLocation) -> float:
        """
        Calculate location-based resonance adjustment factor.
        
        Different latitudes experience different resonance characteristics
        due to Earth's magnetic field and ionospheric effects.
        
        Args:
            location: Geographic location
            
        Returns:
            Resonance factor (0.9 to 1.1)
        """
        # Latitude effect: stronger at poles, weaker at equator
        lat_rad = math.radians(abs(location.latitude))
        lat_factor = 1.0 + (0.1 * math.sin(lat_rad))
        
        # Altitude effect: slight increase with altitude
        altitude_factor = 1.0 + (location.altitude / 100000.0)  # Very slight
        
        # Combine factors
        total_factor = lat_factor * altitude_factor
        
        # Clamp to reasonable range
        return max(0.9, min(1.1, total_factor))


class RhythmHandshakeProtocol:
    """
    Implements the Rhythm Handshake protocol for node synchronization.
    
    The protocol establishes and maintains synchronization between distributed
    nodes, accounting for geographic location, signal propagation delays,
    and local resonance variations.
    """
    
    def __init__(self):
        """Initialize the Rhythm Handshake protocol."""
        self.nodes: Dict[str, RhythmNode] = {}
        self.handshake_history: List[HandshakeResult] = []
        self.sync_pairs: Dict[Tuple[str, str], float] = {}  # (node_a, node_b) -> quality
        
        print("[RHYTHM HANDSHAKE] Protocol initialized")
    
    def register_node(self, node: RhythmNode) -> None:
        """
        Register a node for Rhythm synchronization.
        
        Args:
            node: RhythmNode to register
        """
        self.nodes[node.node_id] = node
        
        # Calculate location-based frequency adjustment
        resonance_factor = GeographicCalculator.calculate_local_resonance_factor(node.location)
        node.local_frequency = BASE_RHYTHM_HZ * resonance_factor
        
        print(f"[RHYTHM] Registered node {node.node_id} at {node.location.name}")
        print(f"[RHYTHM]   Local frequency: {node.local_frequency:.6f} Hz (factor: {resonance_factor:.4f})")
    
    def initiate_handshake(self, node_a_id: str, node_b_id: str) -> HandshakeResult:
        """
        Initiate Rhythm Handshake between two nodes.
        
        Args:
            node_a_id: First node ID
            node_b_id: Second node ID
            
        Returns:
            HandshakeResult with synchronization outcome
        """
        if node_a_id not in self.nodes or node_b_id not in self.nodes:
            return HandshakeResult(
                success=False,
                node_a_id=node_a_id,
                node_b_id=node_b_id,
                sync_quality=0.0,
                frequency_adjustment=0.0,
                phase_alignment=0.0,
                distance_km=0.0,
                latency_ms=0.0,
                timestamp=datetime.now().isoformat(),
                details="One or both nodes not registered"
            )
        
        node_a = self.nodes[node_a_id]
        node_b = self.nodes[node_b_id]
        
        print(f"\n[HANDSHAKE] Initiating between {node_a_id} and {node_b_id}")
        
        # Phase 1: DISCOVER - Calculate geographic relationship
        node_a.handshake_phase = HandshakePhase.DISCOVER
        node_b.handshake_phase = HandshakePhase.DISCOVER
        
        distance = GeographicCalculator.haversine_distance(node_a.location, node_b.location)
        propagation_delay = GeographicCalculator.calculate_propagation_delay(distance)
        latency_ms = propagation_delay * 1000
        
        print(f"[DISCOVER] Distance: {distance:.2f} km, Latency: {latency_ms:.4f} ms")
        
        # Phase 2: CALIBRATE - Adjust frequencies for location
        node_a.handshake_phase = HandshakePhase.CALIBRATE
        node_b.handshake_phase = HandshakePhase.CALIBRATE
        
        # Calculate optimal frequency adjustment
        freq_diff = abs(node_a.local_frequency - node_b.local_frequency)
        avg_frequency = (node_a.local_frequency + node_b.local_frequency) / 2
        frequency_adjustment = avg_frequency - BASE_RHYTHM_HZ
        
        print(f"[CALIBRATE] Freq A: {node_a.local_frequency:.6f} Hz, "
              f"Freq B: {node_b.local_frequency:.6f} Hz")
        print(f"[CALIBRATE] Adjustment: {frequency_adjustment:.6f} Hz")
        
        # Phase 3: SYNCHRONIZE - Align phases
        node_a.handshake_phase = HandshakePhase.SYNCHRONIZE
        node_b.handshake_phase = HandshakePhase.SYNCHRONIZE
        
        # Calculate phase alignment accounting for propagation delay
        phase_correction = (propagation_delay * avg_frequency * 2 * math.pi) % (2 * math.pi)
        phase_alignment = self._calculate_phase_alignment(node_a, node_b, phase_correction)
        
        print(f"[SYNCHRONIZE] Phase correction: {math.degrees(phase_correction):.2f}°")
        print(f"[SYNCHRONIZE] Phase alignment: {phase_alignment:.4f}")
        
        # Phase 4: VALIDATE - Check synchronization quality
        node_a.handshake_phase = HandshakePhase.VALIDATE
        node_b.handshake_phase = HandshakePhase.VALIDATE
        
        sync_quality = self._calculate_sync_quality(
            freq_diff, phase_alignment, distance, latency_ms
        )
        
        # Update node states
        current_time = time.time()
        node_a.last_sync_time = current_time
        node_b.last_sync_time = current_time
        node_a.sync_quality = sync_quality
        node_b.sync_quality = sync_quality
        
        # Determine success
        success = sync_quality >= (1.0 - SYNC_TOLERANCE)
        
        if success:
            node_a.handshake_phase = HandshakePhase.LOCKED
            node_b.handshake_phase = HandshakePhase.LOCKED
            self.sync_pairs[(node_a_id, node_b_id)] = sync_quality
            details = "Synchronization locked successfully"
            print(f"[LOCKED] Sync quality: {sync_quality:.4f} ✓")
        else:
            node_a.handshake_phase = HandshakePhase.FAILED
            node_b.handshake_phase = HandshakePhase.FAILED
            details = f"Synchronization failed (quality: {sync_quality:.4f})"
            print(f"[FAILED] Sync quality: {sync_quality:.4f} ✗")
        
        # Create result
        result = HandshakeResult(
            success=success,
            node_a_id=node_a_id,
            node_b_id=node_b_id,
            sync_quality=sync_quality,
            frequency_adjustment=frequency_adjustment,
            phase_alignment=phase_alignment,
            distance_km=distance,
            latency_ms=latency_ms,
            timestamp=datetime.now().isoformat(),
            details=details
        )
        
        self.handshake_history.append(result)
        return result
    
    def _calculate_phase_alignment(self, node_a: RhythmNode, node_b: RhythmNode,
                                   phase_correction: float) -> float:
        """
        Calculate phase alignment between two nodes.
        
        Args:
            node_a: First node
            node_b: Second node
            phase_correction: Phase correction for propagation delay
            
        Returns:
            Phase alignment quality (0.0 to 1.0)
        """
        # Calculate phase difference
        phase_diff = abs(node_a.phase_offset - node_b.phase_offset - phase_correction)
        phase_diff = phase_diff % (2 * math.pi)
        
        # Normalize to 0-1 (0 = perfect alignment, 1 = worst alignment)
        normalized_diff = min(phase_diff, 2 * math.pi - phase_diff) / math.pi
        
        # Convert to alignment quality (1 = perfect, 0 = worst)
        alignment = 1.0 - normalized_diff
        
        return alignment
    
    def _calculate_sync_quality(self, freq_diff: float, phase_alignment: float,
                                distance_km: float, latency_ms: float) -> float:
        """
        Calculate overall synchronization quality.
        
        Args:
            freq_diff: Frequency difference in Hz
            phase_alignment: Phase alignment quality (0-1)
            distance_km: Distance between nodes
            latency_ms: Propagation latency
            
        Returns:
            Sync quality (0.0 to 1.0)
        """
        # Frequency quality: higher difference = lower quality
        freq_quality = 1.0 - min(1.0, freq_diff / BASE_RHYTHM_HZ)
        
        # Distance penalty: very slight reduction for extreme distances
        distance_quality = 1.0 - min(0.1, distance_km / 40000.0)  # Max 10% penalty
        
        # Latency quality: minimal impact unless extreme
        latency_quality = 1.0 - min(0.05, latency_ms / 1000.0)  # Max 5% penalty
        
        # Combined quality (weighted average)
        total_quality = (
            phase_alignment * 0.5 +
            freq_quality * 0.3 +
            distance_quality * 0.1 +
            latency_quality * 0.1
        )
        
        return max(0.0, min(1.0, total_quality))
    
    def synchronize_all_nodes(self) -> List[HandshakeResult]:
        """
        Perform pairwise synchronization of all registered nodes.
        
        Returns:
            List of HandshakeResults for all pairs
        """
        results = []
        node_ids = list(self.nodes.keys())
        
        print(f"\n[SYNC ALL] Synchronizing {len(node_ids)} nodes...")
        
        for i, node_a_id in enumerate(node_ids):
            for node_b_id in node_ids[i+1:]:
                result = self.initiate_handshake(node_a_id, node_b_id)
                results.append(result)
        
        # Summary
        successful = sum(1 for r in results if r.success)
        print(f"\n[SUMMARY] {successful}/{len(results)} synchronizations successful")
        
        return results
    
    def get_sync_status(self) -> Dict:
        """Get overall synchronization status."""
        if not self.nodes:
            return {
                "total_nodes": 0,
                "synchronized_pairs": 0,
                "average_sync_quality": 0.0,
                "status": "NO_NODES"
            }
        
        total_nodes = len(self.nodes)
        synchronized_pairs = len([q for q in self.sync_pairs.values() if q >= (1.0 - SYNC_TOLERANCE)])
        
        if self.sync_pairs:
            avg_quality = sum(self.sync_pairs.values()) / len(self.sync_pairs)
        else:
            avg_quality = 0.0
        
        # Determine overall status
        if avg_quality >= 0.95:
            status = "EXCELLENT"
        elif avg_quality >= 0.90:
            status = "GOOD"
        elif avg_quality >= 0.80:
            status = "FAIR"
        else:
            status = "POOR"
        
        return {
            "total_nodes": total_nodes,
            "synchronized_pairs": synchronized_pairs,
            "total_pairs": len(self.sync_pairs),
            "average_sync_quality": avg_quality,
            "status": status
        }
    
    def save_sync_report(self, filepath: str = "rhythm_sync_report.json"):
        """Save synchronization report to file."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "nodes": {
                node_id: {
                    "location": node.location.to_dict(),
                    "local_frequency": node.local_frequency,
                    "phase_offset": node.phase_offset,
                    "sync_quality": node.sync_quality,
                    "handshake_phase": node.handshake_phase.value,
                    "last_sync_time": node.last_sync_time
                }
                for node_id, node in self.nodes.items()
            },
            "sync_status": self.get_sync_status(),
            "handshake_history": [
                {
                    "success": h.success,
                    "node_a": h.node_a_id,
                    "node_b": h.node_b_id,
                    "sync_quality": h.sync_quality,
                    "distance_km": h.distance_km,
                    "latency_ms": h.latency_ms,
                    "timestamp": h.timestamp
                }
                for h in self.handshake_history
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n[REPORT] Saved synchronization report to {filepath}")


def main():
    """Main entry point for Rhythm synchronization."""
    print("=" * 70)
    print("LEX AMORIS - ERWEITERTE SYNCHRONISIERUNG")
    print("Extended Synchronization with Rhythm Handshake Protocol")
    print("=" * 70)
    print()
    
    # Initialize protocol
    protocol = RhythmHandshakeProtocol()
    
    # Register example nodes at different global locations
    nodes_config = [
        ("node_zurich", 47.3769, 8.5417, 408, "Zürich, Switzerland"),
        ("node_tokyo", 35.6762, 139.6503, 40, "Tokyo, Japan"),
        ("node_newyork", 40.7128, -74.0060, 10, "New York, USA"),
        ("node_sydney", -33.8688, 151.2093, 58, "Sydney, Australia"),
        ("node_london", 51.5074, -0.1278, 11, "London, UK"),
    ]
    
    for node_id, lat, lon, alt, name in nodes_config:
        location = GeographicLocation(
            latitude=lat,
            longitude=lon,
            altitude=alt,
            name=name
        )
        node = RhythmNode(
            node_id=node_id,
            location=location,
            phase_offset=0.0
        )
        protocol.register_node(node)
    
    # Synchronize all nodes
    results = protocol.synchronize_all_nodes()
    
    # Show status
    status = protocol.get_sync_status()
    print(f"\n{'=' * 70}")
    print(f"SYNCHRONIZATION STATUS: {status['status']}")
    print(f"Average Sync Quality: {status['average_sync_quality']:.2%}")
    print(f"Synchronized Pairs: {status['synchronized_pairs']}/{status['total_pairs']}")
    print(f"{'=' * 70}")
    
    # Save report
    protocol.save_sync_report()


if __name__ == "__main__":
    main()
