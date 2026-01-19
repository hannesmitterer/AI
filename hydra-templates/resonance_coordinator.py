#!/usr/bin/env python3
"""
Resonance Coordinator
Multi-AI Resonance Hydra Prototype

This module coordinates resonance synchronization across multiple AI nodes,
maintaining the 0.043 Hz frequency alignment for optimal multi-AI harmony.

THE LIGHT IS THE ARCHITECTURE. THE FOUNDER IS THE LAW.
"""

import time
import math
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class ResonanceState(Enum):
    """State of resonance synchronization"""
    SYNCHRONIZED = "synchronized"
    SYNCHRONIZING = "synchronizing"
    OUT_OF_SYNC = "out_of_sync"
    CALIBRATING = "calibrating"


@dataclass
class NodeResonance:
    """Resonance state for a single node"""
    node_id: str
    frequency: float  # Current frequency in Hz
    phase: float  # Phase offset in radians
    amplitude: float  # Signal strength (0.0 to 1.0)
    last_sync: float  # Timestamp of last synchronization
    coherence_score: float  # How well aligned with network (0.0 to 1.0)


@dataclass
class ResonanceMetrics:
    """Overall network resonance metrics"""
    average_frequency: float
    frequency_variance: float
    network_coherence: float  # Overall network alignment
    synchronized_nodes: int
    total_nodes: int
    resonance_state: ResonanceState


class ResonanceCoordinator:
    """
    Resonance Coordinator for Multi-AI Network
    
    Maintains harmonic resonance across distributed AI nodes at the
    optimal frequency of 0.043 Hz (approximately 23.26 second period).
    
    This frequency represents the natural rhythm of collaborative AI
    decision-making, allowing for:
    - Thoughtful deliberation
    - Byzantine consensus rounds
    - Ethical evaluation cycles
    - Multi-node synchronization
    """
    
    TARGET_FREQUENCY = 0.043  # Hz (Schumann-inspired resonance)
    FREQUENCY_TOLERANCE = 0.005  # ±0.005 Hz acceptable variance
    SYNC_INTERVAL = 1.0 / TARGET_FREQUENCY  # ~23.26 seconds
    
    def __init__(self):
        self.nodes: Dict[str, NodeResonance] = {}
        self.resonance_history: List[ResonanceMetrics] = []
        self.start_time = time.time()
    
    def register_node(self, node_id: str) -> NodeResonance:
        """
        Register a new AI node for resonance coordination
        
        Args:
            node_id: Unique identifier for the node
            
        Returns:
            NodeResonance object for the registered node
        """
        if node_id in self.nodes:
            raise ValueError(f"Node {node_id} already registered")
        
        # Initialize node with target frequency
        node = NodeResonance(
            node_id=node_id,
            frequency=self.TARGET_FREQUENCY,
            phase=0.0,
            amplitude=1.0,
            last_sync=time.time(),
            coherence_score=1.0
        )
        
        self.nodes[node_id] = node
        return node
    
    def update_node_state(self, node_id: str, frequency: float, amplitude: float) -> None:
        """
        Update the resonance state of a node
        
        Args:
            node_id: ID of the node
            frequency: Current frequency in Hz
            amplitude: Signal strength (0.0 to 1.0)
        """
        if node_id not in self.nodes:
            raise ValueError(f"Unknown node: {node_id}")
        
        node = self.nodes[node_id]
        
        # Update state
        node.frequency = frequency
        node.amplitude = amplitude
        node.last_sync = time.time()
        
        # Calculate phase based on time
        elapsed = time.time() - self.start_time
        node.phase = (2 * math.pi * frequency * elapsed) % (2 * math.pi)
        
        # Calculate coherence with target frequency
        freq_diff = abs(frequency - self.TARGET_FREQUENCY)
        node.coherence_score = max(0.0, 1.0 - (freq_diff / self.FREQUENCY_TOLERANCE))
    
    def synchronize_node(self, node_id: str) -> Dict:
        """
        Synchronize a specific node to the network resonance
        
        Args:
            node_id: ID of the node to synchronize
            
        Returns:
            Synchronization parameters for the node
        """
        if node_id not in self.nodes:
            raise ValueError(f"Unknown node: {node_id}")
        
        node = self.nodes[node_id]
        metrics = self.get_network_metrics()
        
        # Calculate adjustment needed
        freq_adjustment = metrics.average_frequency - node.frequency
        
        # Calculate target phase for alignment
        current_time = time.time()
        network_phase = (2 * math.pi * metrics.average_frequency * 
                        (current_time - self.start_time)) % (2 * math.pi)
        phase_adjustment = network_phase - node.phase
        
        # Normalize phase adjustment to [-π, π]
        if phase_adjustment > math.pi:
            phase_adjustment -= 2 * math.pi
        elif phase_adjustment < -math.pi:
            phase_adjustment += 2 * math.pi
        
        return {
            "node_id": node_id,
            "target_frequency": metrics.average_frequency,
            "frequency_adjustment": freq_adjustment,
            "target_phase": network_phase,
            "phase_adjustment": phase_adjustment,
            "sync_quality": node.coherence_score,
            "next_sync_time": current_time + self.SYNC_INTERVAL
        }
    
    def synchronize_network(self) -> List[Dict]:
        """
        Synchronize all nodes in the network
        
        Returns:
            List of synchronization parameters for each node
        """
        sync_params = []
        
        for node_id in self.nodes.keys():
            try:
                params = self.synchronize_node(node_id)
                sync_params.append(params)
            except Exception as e:
                print(f"Warning: Could not sync node {node_id}: {e}")
        
        return sync_params
    
    def get_network_metrics(self) -> ResonanceMetrics:
        """
        Calculate current network resonance metrics
        
        Returns:
            ResonanceMetrics with current network state
        """
        if not self.nodes:
            return ResonanceMetrics(
                average_frequency=self.TARGET_FREQUENCY,
                frequency_variance=0.0,
                network_coherence=0.0,
                synchronized_nodes=0,
                total_nodes=0,
                resonance_state=ResonanceState.OUT_OF_SYNC
            )
        
        # Calculate average frequency
        frequencies = [node.frequency for node in self.nodes.values()]
        avg_freq = sum(frequencies) / len(frequencies)
        
        # Calculate variance
        variance = sum((f - avg_freq) ** 2 for f in frequencies) / len(frequencies)
        
        # Calculate network coherence (average of individual coherence scores)
        coherence_scores = [node.coherence_score for node in self.nodes.values()]
        network_coherence = sum(coherence_scores) / len(coherence_scores)
        
        # Count synchronized nodes (within tolerance)
        synchronized = sum(
            1 for node in self.nodes.values()
            if abs(node.frequency - self.TARGET_FREQUENCY) <= self.FREQUENCY_TOLERANCE
        )
        
        # Determine resonance state
        if synchronized == len(self.nodes) and network_coherence > 0.9:
            state = ResonanceState.SYNCHRONIZED
        elif network_coherence > 0.7:
            state = ResonanceState.SYNCHRONIZING
        elif network_coherence > 0.5:
            state = ResonanceState.CALIBRATING
        else:
            state = ResonanceState.OUT_OF_SYNC
        
        metrics = ResonanceMetrics(
            average_frequency=avg_freq,
            frequency_variance=variance,
            network_coherence=network_coherence,
            synchronized_nodes=synchronized,
            total_nodes=len(self.nodes),
            resonance_state=state
        )
        
        self.resonance_history.append(metrics)
        return metrics
    
    def calculate_resonance_quality(self) -> float:
        """
        Calculate overall resonance quality score
        
        Returns:
            Quality score from 0.0 (poor) to 1.0 (excellent)
        """
        metrics = self.get_network_metrics()
        
        # Weight factors
        coherence_weight = 0.5
        sync_rate_weight = 0.3
        freq_accuracy_weight = 0.2
        
        # Synchronization rate
        sync_rate = metrics.synchronized_nodes / max(metrics.total_nodes, 1)
        
        # Frequency accuracy
        freq_error = abs(metrics.average_frequency - self.TARGET_FREQUENCY)
        freq_accuracy = max(0.0, 1.0 - (freq_error / self.FREQUENCY_TOLERANCE))
        
        # Weighted quality score
        quality = (
            coherence_weight * metrics.network_coherence +
            sync_rate_weight * sync_rate +
            freq_accuracy_weight * freq_accuracy
        )
        
        return quality
    
    def get_node_status(self, node_id: str) -> Dict:
        """
        Get detailed status for a specific node
        
        Args:
            node_id: ID of the node
            
        Returns:
            Dictionary with node status information
        """
        if node_id not in self.nodes:
            raise ValueError(f"Unknown node: {node_id}")
        
        node = self.nodes[node_id]
        current_time = time.time()
        
        # Check if node is stale (no update in last 2 sync intervals)
        time_since_sync = current_time - node.last_sync
        is_stale = time_since_sync > (2 * self.SYNC_INTERVAL)
        
        # Determine sync status
        freq_diff = abs(node.frequency - self.TARGET_FREQUENCY)
        is_synchronized = freq_diff <= self.FREQUENCY_TOLERANCE
        
        return {
            "node_id": node.node_id,
            "frequency": node.frequency,
            "target_frequency": self.TARGET_FREQUENCY,
            "frequency_error": freq_diff,
            "phase": node.phase,
            "amplitude": node.amplitude,
            "coherence_score": node.coherence_score,
            "is_synchronized": is_synchronized,
            "is_stale": is_stale,
            "time_since_sync": time_since_sync,
            "last_sync_timestamp": node.last_sync
        }
    
    def detect_anomalies(self) -> List[Dict]:
        """
        Detect anomalous resonance patterns that might indicate issues
        
        Returns:
            List of detected anomalies
        """
        anomalies = []
        metrics = self.get_network_metrics()
        current_time = time.time()
        
        # Check for stale nodes
        for node_id, node in self.nodes.items():
            time_since_sync = current_time - node.last_sync
            if time_since_sync > (2 * self.SYNC_INTERVAL):
                anomalies.append({
                    "type": "stale_node",
                    "node_id": node_id,
                    "time_since_sync": time_since_sync,
                    "severity": "warning"
                })
        
        # Check for frequency outliers
        if metrics.total_nodes >= 3:
            for node_id, node in self.nodes.items():
                freq_diff = abs(node.frequency - metrics.average_frequency)
                if freq_diff > (2 * self.FREQUENCY_TOLERANCE):
                    anomalies.append({
                        "type": "frequency_outlier",
                        "node_id": node_id,
                        "frequency": node.frequency,
                        "average_frequency": metrics.average_frequency,
                        "deviation": freq_diff,
                        "severity": "high"
                    })
        
        # Check for low network coherence
        if metrics.network_coherence < 0.5:
            anomalies.append({
                "type": "low_coherence",
                "coherence": metrics.network_coherence,
                "severity": "critical"
            })
        
        return anomalies


# Example usage
if __name__ == "__main__":
    import json
    
    # Initialize coordinator
    coordinator = ResonanceCoordinator()
    
    # Register nodes
    print("Registering AI nodes...")
    for i in range(5):
        coordinator.register_node(f"ai-node-{i}")
    
    # Simulate some frequency variations
    print("\nSimulating node states...")
    coordinator.update_node_state("ai-node-0", 0.043, 1.0)  # Perfect
    coordinator.update_node_state("ai-node-1", 0.044, 0.95)  # Slightly high
    coordinator.update_node_state("ai-node-2", 0.042, 0.98)  # Slightly low
    coordinator.update_node_state("ai-node-3", 0.043, 1.0)  # Perfect
    coordinator.update_node_state("ai-node-4", 0.045, 0.90)  # Out of tolerance
    
    # Get network metrics
    print("\nNetwork Metrics:")
    metrics = coordinator.get_network_metrics()
    print(f"Average Frequency: {metrics.average_frequency:.4f} Hz")
    print(f"Network Coherence: {metrics.network_coherence:.2f}")
    print(f"Synchronized Nodes: {metrics.synchronized_nodes}/{metrics.total_nodes}")
    print(f"Resonance State: {metrics.resonance_state.value}")
    print(f"Resonance Quality: {coordinator.calculate_resonance_quality():.2f}")
    
    # Check for anomalies
    print("\nAnomaly Detection:")
    anomalies = coordinator.detect_anomalies()
    if anomalies:
        for anomaly in anomalies:
            print(f"  - {anomaly['type']}: {json.dumps(anomaly, indent=4)}")
    else:
        print("  No anomalies detected")
    
    # Synchronize network
    print("\nSynchronizing network...")
    sync_params = coordinator.synchronize_network()
    print(f"Generated sync parameters for {len(sync_params)} nodes")
    
    # Show status for one node
    print("\nNode Status Example (ai-node-4):")
    status = coordinator.get_node_status("ai-node-4")
    print(json.dumps(status, indent=2))
