#!/usr/bin/env python3
"""
AI Anomaly Detection - Electromagnetic Behavior Analysis
=========================================================

This module implements an AI-powered anomaly detection system
that monitors electromagnetic behaviors and activates encrypted
buffers when anomalies are detected.

Features:
- Electromagnetic signal pattern analysis
- Real-time anomaly detection using ML
- Encrypted buffer activation
- Predictive threat assessment
- Integration with quantum shield
"""

import time
import hashlib
import secrets
import math
import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import threading
import json

# Try to import numpy, fall back to pure Python if not available
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("[WARNING] NumPy not available, using pure Python implementation")


@dataclass
class EMSignal:
    """Represents an electromagnetic signal reading."""
    timestamp: float
    frequency: float  # Hz
    amplitude: float  # Normalized 0-1
    phase: float  # Radians
    source_vector: Tuple[float, float, float]  # 3D position
    
    def to_array(self):
        """Convert to array for ML processing."""
        data = [
            self.frequency,
            self.amplitude,
            self.phase,
            *self.source_vector
        ]
        if NUMPY_AVAILABLE:
            return np.array(data)
        return data


@dataclass
class AnomalyEvent:
    """Represents a detected anomaly."""
    timestamp: float
    anomaly_score: float
    signal: EMSignal
    event_type: str
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    encrypted_buffer_activated: bool = False
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "timestamp": self.timestamp,
            "anomaly_score": self.anomaly_score,
            "event_type": self.event_type,
            "severity": self.severity,
            "frequency": self.signal.frequency,
            "buffer_activated": self.encrypted_buffer_activated
        }


class EncryptedBuffer:
    """
    Encrypted buffer for storing sensitive data during anomalies.
    
    Activates invisibly when anomalies are detected to protect
    critical information from electromagnetic attacks.
    """
    
    def __init__(self, buffer_id: str):
        """Initialize encrypted buffer."""
        self.buffer_id = buffer_id
        self.is_active = False
        self.data: List[bytes] = []
        self.encryption_key = secrets.token_bytes(32)
        self.max_size = 1000
        self.activation_count = 0
    
    def activate(self) -> None:
        """Activate encrypted buffer (invisible operation)."""
        if not self.is_active:
            self.is_active = True
            self.activation_count += 1
            # Buffer activation is invisible - no external indicators
    
    def deactivate(self) -> None:
        """Deactivate encrypted buffer."""
        self.is_active = False
    
    def store(self, data: bytes) -> None:
        """Store data in encrypted buffer."""
        if not self.is_active:
            return
        
        # Encrypt data using XOR with key (simplified)
        # In production, use AES-256-GCM or similar
        key_repeat_count = len(data) // len(self.encryption_key) + 1
        extended_key = (self.encryption_key * key_repeat_count)[:len(data)]
        encrypted = bytes(a ^ b for a, b in zip(data, extended_key))
        
        self.data.append(encrypted)
        
        # Keep buffer size limited
        if len(self.data) > self.max_size:
            self.data = self.data[-self.max_size:]
    
    def get_status(self) -> Dict:
        """Get buffer status."""
        return {
            "buffer_id": self.buffer_id,
            "active": self.is_active,
            "stored_items": len(self.data),
            "activation_count": self.activation_count,
            "invisible": True  # Always invisible
        }


class SimpleMLDetector:
    """
    Simplified machine learning detector for anomalies.
    
    NOTE: This is a lightweight implementation. For production,
    integrate TensorFlow/PyTorch with proper neural networks.
    Uses statistical methods for real-time detection without
    requiring TensorFlow dependency.
    """
    
    def __init__(self, window_size: int = 100):
        """
        Initialize detector.
        
        Args:
            window_size: Number of samples for baseline calculation
        """
        self.window_size = window_size
        self.baseline_samples: List = []
        self.mean: Optional[List[float]] = None
        self.std: Optional[List[float]] = None
        self.is_trained = False
    
    def _calculate_mean(self, samples: List) -> List[float]:
        """Calculate mean across samples."""
        if not samples:
            return []
        n_features = len(samples[0])
        means = []
        for i in range(n_features):
            values = [sample[i] for sample in samples]
            means.append(sum(values) / len(values))
        return means
    
    def _calculate_std(self, samples: List, mean: List[float]) -> List[float]:
        """Calculate standard deviation across samples."""
        if not samples:
            return []
        n_features = len(samples[0])
        stds = []
        for i in range(n_features):
            values = [sample[i] for sample in samples]
            variance = sum((x - mean[i]) ** 2 for x in values) / len(values)
            stds.append(math.sqrt(variance) + 1e-6)  # Avoid division by zero
        return stds
    
    def update_baseline(self, signal: EMSignal) -> None:
        """Update baseline with new normal signal."""
        signal_array = signal.to_array()
        self.baseline_samples.append(signal_array)
        
        # Keep only recent samples
        if len(self.baseline_samples) > self.window_size:
            self.baseline_samples = self.baseline_samples[-self.window_size:]
        
        # Recalculate statistics
        if len(self.baseline_samples) >= 10:
            self.mean = self._calculate_mean(self.baseline_samples)
            self.std = self._calculate_std(self.baseline_samples, self.mean)
            self.is_trained = True
    
    def detect_anomaly(self, signal: EMSignal) -> Tuple[bool, float]:
        """
        Detect if signal is anomalous.
        
        Returns:
            Tuple of (is_anomaly, anomaly_score)
        """
        if not self.is_trained:
            return False, 0.0
        
        signal_array = signal.to_array()
        
        # Calculate z-score (number of standard deviations from mean)
        z_scores = []
        for i in range(len(signal_array)):
            if isinstance(signal_array, list):
                z = abs((signal_array[i] - self.mean[i]) / self.std[i])
            else:  # numpy array
                z = abs((signal_array[i] - self.mean[i]) / self.std[i])
            z_scores.append(z)
        
        # Anomaly score is max z-score
        anomaly_score = float(max(z_scores))
        
        # Threshold for anomaly detection
        threshold = 3.0  # 3 standard deviations
        is_anomaly = anomaly_score > threshold
        
        return is_anomaly, anomaly_score


class AIAnomalyDetector:
    """
    AI-powered electromagnetic anomaly detection system.
    
    Monitors electromagnetic signals and activates encrypted
    buffers when anomalous behaviors are detected.
    """
    
    def __init__(self):
        """Initialize AI anomaly detector."""
        self.detector = SimpleMLDetector(window_size=100)
        self.encrypted_buffers: Dict[str, EncryptedBuffer] = {}
        self.anomaly_history: List[AnomalyEvent] = []
        self.max_history = 1000
        self.is_monitoring = False
        self.monitoring_thread: Optional[threading.Thread] = None
        self.detection_count = 0
        
        # Create default encrypted buffer
        self._create_buffer("primary")
        self._create_buffer("secondary")
        
        print("[AI-DETECTOR] Initialized electromagnetic anomaly detector")
        print("[AI-DETECTOR] Using statistical ML for real-time detection")
    
    def _create_buffer(self, buffer_id: str) -> None:
        """Create a new encrypted buffer."""
        self.encrypted_buffers[buffer_id] = EncryptedBuffer(buffer_id)
        print(f"[BUFFER] Created encrypted buffer: {buffer_id}")
    
    def _generate_synthetic_signal(self) -> EMSignal:
        """
        Generate synthetic electromagnetic signal for testing.
        
        In production, this would read from actual EM sensors.
        """
        # Base frequency with some variation
        base_freq = 7.83  # Schumann resonance
        frequency = base_freq + random.gauss(0, 0.5)
        
        # Amplitude with occasional spikes
        if random.random() < 0.05:  # 5% chance of spike
            amplitude = random.uniform(0.7, 1.0)  # Anomalous spike
        else:
            amplitude = random.uniform(0.2, 0.5)  # Normal range
        
        # Phase
        phase = random.uniform(0, 2 * math.pi)
        
        # 3D source vector
        source_vector = (
            random.gauss(0, 1),
            random.gauss(0, 1),
            random.gauss(0, 1)
        )
        
        return EMSignal(
            timestamp=time.time(),
            frequency=frequency,
            amplitude=amplitude,
            phase=phase,
            source_vector=source_vector
        )
    
    def train_baseline(self, num_samples: int = 100) -> None:
        """
        Train detector on baseline electromagnetic signals.
        
        Args:
            num_samples: Number of samples to use for baseline
        """
        print(f"[TRAINING] Collecting {num_samples} baseline samples...")
        
        for i in range(num_samples):
            signal = self._generate_synthetic_signal()
            # Ensure amplitude is in normal range for training
            signal.amplitude = random.uniform(0.2, 0.5)
            self.detector.update_baseline(signal)
            
            if (i + 1) % 20 == 0:
                print(f"[TRAINING] Progress: {i + 1}/{num_samples}")
        
        print("[TRAINING] Baseline training complete")
    
    def analyze_signal(self, signal: EMSignal) -> Optional[AnomalyEvent]:
        """
        Analyze electromagnetic signal for anomalies.
        
        Args:
            signal: EM signal to analyze
            
        Returns:
            AnomalyEvent if anomaly detected, None otherwise
        """
        # Detect anomaly
        is_anomaly, anomaly_score = self.detector.detect_anomaly(signal)
        
        if not is_anomaly:
            # Update baseline with normal signals
            self.detector.update_baseline(signal)
            return None
        
        # Classify severity based on anomaly score
        if anomaly_score > 6.0:
            severity = "CRITICAL"
            event_type = "CRITICAL_EM_ANOMALY"
        elif anomaly_score > 4.5:
            severity = "HIGH"
            event_type = "HIGH_EM_ANOMALY"
        elif anomaly_score > 3.5:
            severity = "MEDIUM"
            event_type = "MEDIUM_EM_ANOMALY"
        else:
            severity = "LOW"
            event_type = "LOW_EM_ANOMALY"
        
        # Create anomaly event
        anomaly = AnomalyEvent(
            timestamp=time.time(),
            anomaly_score=anomaly_score,
            signal=signal,
            event_type=event_type,
            severity=severity
        )
        
        # Activate encrypted buffers for medium+ severity
        if severity in ["MEDIUM", "HIGH", "CRITICAL"]:
            self._activate_buffers(anomaly)
            anomaly.encrypted_buffer_activated = True
        
        # Store in history
        self.anomaly_history.append(anomaly)
        if len(self.anomaly_history) > self.max_history:
            self.anomaly_history = self.anomaly_history[-self.max_history:]
        
        self.detection_count += 1
        
        return anomaly
    
    def _activate_buffers(self, anomaly: AnomalyEvent) -> None:
        """
        Activate encrypted buffers in response to anomaly.
        
        Buffers activate invisibly to protect against attacks.
        """
        for buffer in self.encrypted_buffers.values():
            buffer.activate()
            
            # Store anomaly data in buffer
            anomaly_data = json.dumps(anomaly.to_dict()).encode()
            buffer.store(anomaly_data)
        
        # Invisible activation - no external logging
    
    def start_monitoring(self) -> None:
        """Start continuous monitoring."""
        if self.is_monitoring:
            print("[AI-DETECTOR] Monitoring already active")
            return
        
        self.is_monitoring = True
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_worker,
            daemon=True,
            name="AI-AnomalyMonitor"
        )
        self.monitoring_thread.start()
        print("[AI-DETECTOR] Continuous monitoring started")
    
    def _monitoring_worker(self) -> None:
        """Background worker for continuous monitoring."""
        while self.is_monitoring:
            # Generate and analyze signal
            signal = self._generate_synthetic_signal()
            anomaly = self.analyze_signal(signal)
            
            if anomaly:
                print(f"[ANOMALY] Detected {anomaly.severity}: "
                      f"Score={anomaly.anomaly_score:.2f} | "
                      f"Freq={anomaly.signal.frequency:.2f}Hz | "
                      f"Buffer={'ACTIVE' if anomaly.encrypted_buffer_activated else 'inactive'}")
            
            time.sleep(0.5)  # Monitor every 500ms
    
    def stop_monitoring(self) -> None:
        """Stop continuous monitoring."""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=2.0)
        print("[AI-DETECTOR] Monitoring stopped")
    
    def get_status(self) -> Dict:
        """Get detector status."""
        # Count anomalies by severity
        severity_counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}
        for anomaly in self.anomaly_history:
            severity_counts[anomaly.severity] += 1
        
        return {
            "status": "ACTIVE" if self.is_monitoring else "IDLE",
            "detector_type": "STATISTICAL_ML",
            "trained": self.detector.is_trained,
            "monitoring": self.is_monitoring,
            "total_detections": self.detection_count,
            "anomaly_history_size": len(self.anomaly_history),
            "severity_counts": severity_counts,
            "encrypted_buffers": {
                buf_id: buf.get_status() 
                for buf_id, buf in self.encrypted_buffers.items()
            }
        }


def main():
    """Demo of AI Anomaly Detection system."""
    print("=" * 70)
    print("AI ELECTROMAGNETIC ANOMALY DETECTION")
    print("ML-Powered Threat Detection with Encrypted Buffers")
    print("=" * 70)
    print()
    
    # Initialize detector
    detector = AIAnomalyDetector()
    
    # Train on baseline
    detector.train_baseline(num_samples=100)
    
    # Start monitoring
    detector.start_monitoring()
    
    # Show status
    print("\n[STATUS]")
    status = detector.get_status()
    print(json.dumps(status, indent=2))
    
    # Keep running
    try:
        print("\n[INFO] AI detector monitoring. Press Ctrl+C to stop")
        while True:
            time.sleep(10)
            status = detector.get_status()
            print(f"[HEARTBEAT] Detections: {status['total_detections']} | "
                  f"Critical: {status['severity_counts']['CRITICAL']} | "
                  f"High: {status['severity_counts']['HIGH']}")
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Stopping AI detector...")
        detector.stop_monitoring()


if __name__ == "__main__":
    main()
