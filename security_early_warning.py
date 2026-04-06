#!/usr/bin/env python3
"""
AI-Based Early Warning System
==============================

This module implements an AI-based anomaly detection system
for identifying protocol and frequency deviations, data poisoning,
and other security threats.

Uses lightweight neural networks for pattern recognition and threat classification.
Note: This is a standalone implementation without external dependencies. For production
use with TensorFlow, replace SimpleNeuralNetwork with TensorFlow models.
"""

import time
import math
import random
import json
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from collections import deque
from enum import Enum


class ThreatLevel(Enum):
    """Threat severity levels."""
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class ProtocolEvent:
    """Represents a protocol or network event."""
    timestamp: float
    event_type: str
    frequency_mhz: Optional[float] = None
    power_dbm: Optional[float] = None
    data_size_bytes: int = 0
    source_id: str = ""
    features: List[float] = field(default_factory=list)


@dataclass  
class ThreatDetection:
    """Represents a detected threat."""
    timestamp: float
    threat_type: str
    threat_level: ThreatLevel
    confidence: float
    description: str
    affected_events: List[ProtocolEvent] = field(default_factory=list)
    recommended_action: str = ""


class SimpleNeuralNetwork:
    """
    Simplified neural network for anomaly detection.
    
    This is a lightweight implementation for pattern recognition
    without external dependencies. In production, use TensorFlow/PyTorch.
    """
    
    def __init__(self, input_size: int, hidden_size: int = 10):
        """
        Initialize neural network.
        
        Args:
            input_size: Number of input features
            hidden_size: Number of hidden layer neurons
        """
        self.input_size = input_size
        self.hidden_size = hidden_size
        
        # Initialize weights with small random values
        self.w1 = [[random.uniform(-0.5, 0.5) for _ in range(input_size)] 
                   for _ in range(hidden_size)]
        self.b1 = [random.uniform(-0.1, 0.1) for _ in range(hidden_size)]
        
        self.w2 = [random.uniform(-0.5, 0.5) for _ in range(hidden_size)]
        self.b2 = random.uniform(-0.1, 0.1)
        
        # Training history
        self.training_samples = 0
        self.learning_rate = 0.01
    
    def _sigmoid(self, x: float) -> float:
        """Sigmoid activation function."""
        return 1.0 / (1.0 + math.exp(-max(-10, min(10, x))))
    
    def _relu(self, x: float) -> float:
        """ReLU activation function."""
        return max(0.0, x)
    
    def _forward(self, inputs: List[float]) -> float:
        """
        Forward pass through network.
        
        Args:
            inputs: Input feature vector
            
        Returns:
            Network output (anomaly score 0-1)
        """
        # Input layer to hidden layer
        hidden = []
        for i in range(self.hidden_size):
            activation = self.b1[i]
            for j in range(len(inputs)):
                activation += inputs[j] * self.w1[i][j]
            hidden.append(self._relu(activation))
        
        # Hidden layer to output
        output = self.b2
        for i in range(self.hidden_size):
            output += hidden[i] * self.w2[i]
        
        return self._sigmoid(output)
    
    def predict(self, inputs: List[float]) -> float:
        """
        Predict anomaly score for inputs.
        
        Args:
            inputs: Input feature vector
            
        Returns:
            Anomaly score between 0 (normal) and 1 (anomalous)
        """
        # Normalize inputs
        normalized = self._normalize_inputs(inputs)
        return self._forward(normalized)
    
    def _normalize_inputs(self, inputs: List[float]) -> List[float]:
        """Normalize input features to [0, 1] range."""
        if not inputs:
            return []
        
        max_val = max(abs(x) for x in inputs)
        if max_val == 0:
            return inputs
        
        return [x / max_val for x in inputs]
    
    def train_online(self, inputs: List[float], is_anomaly: bool) -> None:
        """
        Online training with single sample.
        
        Args:
            inputs: Input feature vector
            is_anomaly: True if sample is anomalous
        """
        normalized = self._normalize_inputs(inputs)
        prediction = self._forward(normalized)
        
        # Simple gradient descent update
        target = 1.0 if is_anomaly else 0.0
        error = target - prediction
        
        # Update output weights
        for i in range(self.hidden_size):
            self.w2[i] += self.learning_rate * error
        self.b2 += self.learning_rate * error
        
        self.training_samples += 1


class ProtocolAnomalyDetector:
    """
    Detects protocol and frequency anomalies using AI.
    
    Monitors network events and identifies deviations from
    normal patterns.
    """
    
    def __init__(self, history_size: int = 1000):
        """
        Initialize anomaly detector.
        
        Args:
            history_size: Number of events to keep in history
        """
        self.history: deque = deque(maxlen=history_size)
        self.baseline_stats: Dict[str, float] = {}
        
        # Neural network for anomaly detection
        self.neural_net = SimpleNeuralNetwork(input_size=6)
        
        # Detection thresholds
        self.anomaly_threshold = 0.7
        self.critical_threshold = 0.9
        
        # Statistics
        self.total_events = 0
        self.anomalies_detected = 0
        self.false_positives = 0
        
    def _extract_features(self, event: ProtocolEvent) -> List[float]:
        """
        Extract feature vector from event.
        
        Args:
            event: Protocol event
            
        Returns:
            Feature vector
        """
        features = [
            event.frequency_mhz or 0.0,
            event.power_dbm or 0.0,
            float(event.data_size_bytes),
            event.timestamp % 1000,  # Time modulo
            hash(event.event_type) % 1000,  # Event type hash
            hash(event.source_id) % 1000  # Source hash
        ]
        return features
    
    def _calculate_baseline(self) -> None:
        """Calculate baseline statistics from history."""
        if len(self.history) < 10:
            return
        
        # Calculate mean and std for each feature
        frequencies = [e.frequency_mhz or 0 for e in self.history if e.frequency_mhz]
        powers = [e.power_dbm or 0 for e in self.history if e.power_dbm]
        sizes = [e.data_size_bytes for e in self.history]
        
        self.baseline_stats = {
            "freq_mean": sum(frequencies) / len(frequencies) if frequencies else 0,
            "freq_std": self._std_dev(frequencies),
            "power_mean": sum(powers) / len(powers) if powers else 0,
            "power_std": self._std_dev(powers),
            "size_mean": sum(sizes) / len(sizes) if sizes else 0,
            "size_std": self._std_dev(sizes)
        }
    
    def _std_dev(self, values: List[float]) -> float:
        """Calculate standard deviation."""
        if not values or len(values) < 2:
            return 0.0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return math.sqrt(variance)
    
    def _statistical_anomaly_score(self, event: ProtocolEvent) -> float:
        """
        Calculate anomaly score using statistical methods.
        
        Args:
            event: Event to analyze
            
        Returns:
            Anomaly score 0-1
        """
        if not self.baseline_stats:
            return 0.0
        
        score = 0.0
        count = 0
        
        # Check frequency deviation
        if event.frequency_mhz and self.baseline_stats.get("freq_std", 0) > 0:
            z_score = abs(event.frequency_mhz - self.baseline_stats["freq_mean"]) / \
                     self.baseline_stats["freq_std"]
            score += min(1.0, z_score / 3.0)  # 3-sigma rule
            count += 1
        
        # Check power deviation
        if event.power_dbm and self.baseline_stats.get("power_std", 0) > 0:
            z_score = abs(event.power_dbm - self.baseline_stats["power_mean"]) / \
                     self.baseline_stats["power_std"]
            score += min(1.0, z_score / 3.0)
            count += 1
        
        # Check size deviation
        if self.baseline_stats.get("size_std", 0) > 0:
            z_score = abs(event.data_size_bytes - self.baseline_stats["size_mean"]) / \
                     self.baseline_stats["size_std"]
            score += min(1.0, z_score / 3.0)
            count += 1
        
        return score / count if count > 0 else 0.0
    
    def analyze_event(self, event: ProtocolEvent) -> Optional[ThreatDetection]:
        """
        Analyze event for anomalies.
        
        Args:
            event: Event to analyze
            
        Returns:
            ThreatDetection if anomaly detected, None otherwise
        """
        # Add to history
        self.history.append(event)
        self.total_events += 1
        
        # Update baseline periodically
        if self.total_events % 100 == 0:
            self._calculate_baseline()
        
        # Extract features
        features = self._extract_features(event)
        
        # Get neural network score
        nn_score = self.neural_net.predict(features)
        
        # Get statistical score
        stat_score = self._statistical_anomaly_score(event)
        
        # Combined score (weighted average)
        combined_score = (nn_score * 0.6) + (stat_score * 0.4)
        
        # Determine threat level
        if combined_score >= self.critical_threshold:
            threat_level = ThreatLevel.CRITICAL
            self.anomalies_detected += 1
        elif combined_score >= self.anomaly_threshold:
            threat_level = ThreatLevel.HIGH
            self.anomalies_detected += 1
        elif combined_score >= 0.5:
            threat_level = ThreatLevel.MEDIUM
        else:
            return None  # No threat
        
        # Create threat detection
        threat = ThreatDetection(
            timestamp=event.timestamp,
            threat_type="PROTOCOL_ANOMALY",
            threat_level=threat_level,
            confidence=combined_score,
            description=f"Anomalous {event.event_type} detected",
            affected_events=[event],
            recommended_action=self._get_recommended_action(threat_level)
        )
        
        return threat
    
    def _get_recommended_action(self, threat_level: ThreatLevel) -> str:
        """Get recommended action for threat level."""
        actions = {
            ThreatLevel.CRITICAL: "IMMEDIATE: Isolate source, activate maximum shielding",
            ThreatLevel.HIGH: "Execute evasive frequency hopping, increase monitoring",
            ThreatLevel.MEDIUM: "Enhanced logging, prepare countermeasures",
            ThreatLevel.LOW: "Continue monitoring",
            ThreatLevel.NONE: "No action required"
        }
        return actions.get(threat_level, "Unknown")


class DataPoisoningDetector:
    """
    Detects AI data poisoning attacks.
    
    Identifies malicious data injected to corrupt AI models.
    """
    
    def __init__(self):
        """Initialize data poisoning detector."""
        self.data_samples: List[List[float]] = []
        self.labels: List[int] = []
        
        self.poisoning_threshold = 0.75
        self.suspicious_samples = 0
        
    def validate_training_data(self, samples: List[List[float]], 
                               labels: List[int]) -> Dict[str, any]:
        """
        Validate training data for poisoning.
        
        Args:
            samples: Training samples
            labels: Training labels
            
        Returns:
            Validation report
        """
        if len(samples) != len(labels):
            return {
                "is_poisoned": True,
                "confidence": 1.0,
                "reason": "Mismatched samples and labels"
            }
        
        # Check for label flipping attacks
        label_distribution = {}
        for label in labels:
            label_distribution[label] = label_distribution.get(label, 0) + 1
        
        # Check for extreme imbalance (potential poisoning)
        if label_distribution:
            max_count = max(label_distribution.values())
            min_count = min(label_distribution.values())
            imbalance_ratio = max_count / min_count if min_count > 0 else float('inf')
            
            if imbalance_ratio > 10:  # 10x imbalance threshold
                return {
                    "is_poisoned": True,
                    "confidence": 0.8,
                    "reason": f"Severe label imbalance: {imbalance_ratio:.1f}x",
                    "label_distribution": label_distribution
                }
        
        # Check for outlier samples
        outlier_count = 0
        for sample in samples:
            if self._is_outlier(sample, samples):
                outlier_count += 1
        
        outlier_ratio = outlier_count / len(samples) if samples else 0
        
        if outlier_ratio > 0.1:  # More than 10% outliers
            return {
                "is_poisoned": True,
                "confidence": 0.7,
                "reason": f"High outlier ratio: {outlier_ratio:.1%}",
                "outlier_count": outlier_count
            }
        
        return {
            "is_poisoned": False,
            "confidence": 0.9,
            "reason": "Data appears clean",
            "samples_validated": len(samples)
        }
    
    def _is_outlier(self, sample: List[float], all_samples: List[List[float]]) -> bool:
        """Check if sample is an outlier."""
        if not all_samples or not sample:
            return False
        
        # Simple outlier detection using distance from mean
        feature_means = []
        for i in range(len(sample)):
            values = [s[i] for s in all_samples if len(s) > i]
            if values:
                feature_means.append(sum(values) / len(values))
            else:
                feature_means.append(0)
        
        # Calculate distance from mean
        distance = math.sqrt(sum((sample[i] - feature_means[i]) ** 2 
                                for i in range(len(sample))))
        
        # Threshold based on dimension
        threshold = math.sqrt(len(sample)) * 3  # 3-sigma approximation
        
        return distance > threshold


class EarlyWarningSystem:
    """
    Comprehensive AI-based early warning system.
    
    Integrates protocol monitoring, anomaly detection, and
    data poisoning detection.
    """
    
    def __init__(self):
        """Initialize early warning system."""
        self.protocol_detector = ProtocolAnomalyDetector()
        self.poisoning_detector = DataPoisoningDetector()
        
        # Alert management
        self.active_threats: List[ThreatDetection] = []
        self.threat_history: deque = deque(maxlen=500)
        
        # System status
        self.is_active = True
        self.monitoring_start_time = time.time()
        
    def process_event(self, event: ProtocolEvent) -> Optional[ThreatDetection]:
        """
        Process network/protocol event.
        
        Args:
            event: Event to process
            
        Returns:
            ThreatDetection if threat found
        """
        threat = self.protocol_detector.analyze_event(event)
        
        if threat:
            self.active_threats.append(threat)
            self.threat_history.append(threat)
        
        return threat
    
    def validate_ai_training_data(self, samples: List[List[float]], 
                                 labels: List[int]) -> Dict[str, any]:
        """
        Validate AI training data.
        
        Args:
            samples: Training samples
            labels: Training labels
            
        Returns:
            Validation report
        """
        return self.poisoning_detector.validate_training_data(samples, labels)
    
    def get_status(self) -> Dict[str, any]:
        """Get comprehensive system status."""
        uptime = time.time() - self.monitoring_start_time
        
        return {
            "is_active": self.is_active,
            "uptime_seconds": uptime,
            "events_processed": self.protocol_detector.total_events,
            "anomalies_detected": self.protocol_detector.anomalies_detected,
            "active_threats": len(self.active_threats),
            "threat_history_size": len(self.threat_history),
            "detection_rate": (self.protocol_detector.anomalies_detected / 
                             self.protocol_detector.total_events 
                             if self.protocol_detector.total_events > 0 else 0)
        }


def main():
    """Demonstrate early warning system."""
    print("=" * 70)
    print("AI-BASED EARLY WARNING SYSTEM")
    print("=" * 70)
    
    # Initialize system
    print("\n[1] Initializing early warning system...")
    ews = EarlyWarningSystem()
    print("    System initialized")
    
    # Simulate normal events
    print("\n[2] Processing normal protocol events...")
    for i in range(20):
        event = ProtocolEvent(
            timestamp=time.time(),
            event_type="DATA_TRANSMISSION",
            frequency_mhz=2400.0 + random.uniform(-5, 5),
            power_dbm=random.uniform(-15, -5),
            data_size_bytes=random.randint(100, 1000),
            source_id=f"node_{i % 5}"
        )
        ews.process_event(event)
    
    # Simulate anomalous event
    print("\n[3] Injecting anomalous event...")
    anomalous_event = ProtocolEvent(
        timestamp=time.time(),
        event_type="DATA_TRANSMISSION",
        frequency_mhz=2800.0,  # Way outside normal range
        power_dbm=10.0,  # Abnormally high
        data_size_bytes=50000,  # Abnormally large
        source_id="unknown_node"
    )
    
    threat = ews.process_event(anomalous_event)
    if threat:
        print(f"    ⚠ THREAT DETECTED!")
        print(f"    Type: {threat.threat_type}")
        print(f"    Level: {threat.threat_level.name}")
        print(f"    Confidence: {threat.confidence:.2%}")
        print(f"    Action: {threat.recommended_action}")
    
    # Test data poisoning detection
    print("\n[4] Testing data poisoning detection...")
    
    # Clean data
    clean_samples = [[random.uniform(0, 1) for _ in range(5)] for _ in range(100)]
    clean_labels = [random.randint(0, 1) for _ in range(100)]
    
    clean_result = ews.validate_ai_training_data(clean_samples, clean_labels)
    print(f"    Clean data: Poisoned={clean_result['is_poisoned']}, "
          f"Confidence={clean_result['confidence']:.2%}")
    
    # Poisoned data (extreme imbalance)
    poisoned_labels = [0] * 95 + [1] * 5
    poisoned_result = ews.validate_ai_training_data(clean_samples, poisoned_labels)
    print(f"    Poisoned data: Poisoned={poisoned_result['is_poisoned']}, "
          f"Confidence={poisoned_result['confidence']:.2%}")
    
    # System status
    status = ews.get_status()
    print(f"\n[5] System status:")
    print(f"    Events processed: {status['events_processed']}")
    print(f"    Anomalies detected: {status['anomalies_detected']}")
    print(f"    Detection rate: {status['detection_rate']:.2%}")
    
    print("\n" + "=" * 70)
    print("Early warning system demonstration complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
