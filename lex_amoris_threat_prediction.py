#!/usr/bin/env python3
"""
Lex Amoris - KI-basierte Bedrohungsvorhersage (AI-based Threat Prediction)
============================================================================

This module implements real-time anomaly detection using TensorFlow for
the Lex Amoris security framework. It monitors system behavior and predicts
potential threats through pattern recognition and machine learning.

Key Features:
- Real-time anomaly detection
- TensorFlow-based threat prediction model
- Adaptive learning from system patterns
- Integration with Eternal Deposition System
- Quantum-aware security metrics

Based on: Lex Amoris mandate and Kosymbiosis security principles
"""

import numpy as np
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from collections import deque

# TensorFlow will be imported conditionally to handle environments without it
try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    print("[WARNING] TensorFlow not available. Using fallback detection mode.")


# Constants
ANOMALY_THRESHOLD = 0.75  # Threshold for anomaly detection
HISTORY_WINDOW = 100  # Number of recent observations to keep
PREDICTION_CONFIDENCE_MIN = 0.60  # Minimum confidence for threat prediction
RETRAINING_INTERVAL = 3600  # Retrain model every hour (balances responsiveness with computational cost)


@dataclass
class ThreatEvent:
    """Represents a detected threat event."""
    timestamp: str
    threat_level: float  # 0.0 to 1.0
    anomaly_score: float
    threat_type: str
    description: str
    confidence: float
    metadata: Dict = field(default_factory=dict)


@dataclass
class SystemMetrics:
    """System metrics for threat analysis."""
    energy_variance: float = 0.0
    node_synchronization: float = 1.0
    resonance_stability: float = 1.0
    network_coherence: float = 1.0
    quantum_entropy: float = 0.0


class AnomalyDetectionModel:
    """
    TensorFlow-based anomaly detection model.
    
    Uses an autoencoder architecture to learn normal system behavior
    and detect anomalies based on reconstruction error.
    """
    
    def __init__(self, input_dim: int = 5):
        """
        Initialize the anomaly detection model.
        
        Args:
            input_dim: Dimension of input feature vector
        """
        self.input_dim = input_dim
        self.model = None
        self.is_trained = False
        self.training_history = []
        
        if TF_AVAILABLE:
            self._build_model()
    
    def _build_model(self):
        """Build the autoencoder model architecture."""
        # Encoder
        encoder_input = tf.keras.layers.Input(shape=(self.input_dim,))
        encoded = tf.keras.layers.Dense(8, activation='relu')(encoder_input)
        encoded = tf.keras.layers.Dense(4, activation='relu')(encoded)
        encoded = tf.keras.layers.Dense(2, activation='relu')(encoded)
        
        # Decoder
        decoded = tf.keras.layers.Dense(4, activation='relu')(encoded)
        decoded = tf.keras.layers.Dense(8, activation='relu')(decoded)
        decoder_output = tf.keras.layers.Dense(self.input_dim, activation='sigmoid')(decoded)
        
        # Autoencoder
        self.model = tf.keras.Model(encoder_input, decoder_output)
        self.model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        
        print("[ANOMALY MODEL] TensorFlow model built successfully")
    
    def train(self, normal_data: np.ndarray, epochs: int = 50, batch_size: int = 32):
        """
        Train the model on normal system behavior.
        
        Args:
            normal_data: Array of normal system metrics
            epochs: Number of training epochs
            batch_size: Batch size for training
        """
        if not TF_AVAILABLE or self.model is None:
            print("[ANOMALY MODEL] Cannot train: TensorFlow not available")
            return
        
        # Train autoencoder to reconstruct normal behavior
        history = self.model.fit(
            normal_data, normal_data,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=0.2,
            verbose=0
        )
        
        self.is_trained = True
        self.training_history.append({
            'timestamp': datetime.now().isoformat(),
            'epochs': epochs,
            'final_loss': float(history.history['loss'][-1])
        })
        
        print(f"[ANOMALY MODEL] Training complete. Final loss: {history.history['loss'][-1]:.6f}")
    
    def predict_anomaly(self, metrics: np.ndarray) -> Tuple[float, float]:
        """
        Predict anomaly score for given metrics.
        
        Args:
            metrics: Input metrics array
            
        Returns:
            Tuple of (anomaly_score, confidence)
        """
        if not TF_AVAILABLE or self.model is None or not self.is_trained:
            # Fallback: simple variance-based detection
            return self._fallback_detection(metrics)
        
        # Reshape for model input
        metrics_reshaped = metrics.reshape(1, -1)
        
        # Get reconstruction
        reconstruction = self.model.predict(metrics_reshaped, verbose=0)
        
        # Calculate reconstruction error (anomaly score)
        error = np.mean(np.square(metrics_reshaped - reconstruction))
        anomaly_score = min(1.0, error * 10)  # Scale to 0-1
        
        # Confidence based on training history
        confidence = 0.9 if self.is_trained else 0.5
        
        return float(anomaly_score), float(confidence)
    
    def _fallback_detection(self, metrics: np.ndarray) -> Tuple[float, float]:
        """
        Fallback anomaly detection without TensorFlow.
        
        Uses statistical methods to detect anomalies.
        """
        # Calculate z-score based anomaly detection
        mean_val = np.mean(metrics)
        std_val = np.std(metrics) + 1e-6  # Avoid division by zero
        z_scores = np.abs((metrics - mean_val) / std_val)
        
        # Anomaly score based on maximum z-score
        max_z = np.max(z_scores)
        anomaly_score = min(1.0, max_z / 3.0)  # 3-sigma rule
        
        confidence = 0.6  # Lower confidence for fallback method
        
        return float(anomaly_score), float(confidence)


class LexAmorisThreatPredictor:
    """
    Main threat prediction engine for Lex Amoris.
    
    Monitors system behavior and predicts potential threats using
    AI-based anomaly detection and pattern recognition.
    """
    
    def __init__(self):
        """Initialize the threat prediction system."""
        self.anomaly_model = AnomalyDetectionModel(input_dim=5)
        self.metrics_history: deque = deque(maxlen=HISTORY_WINDOW)
        self.threat_events: List[ThreatEvent] = []
        self.last_training_time: float = 0
        self.is_monitoring: bool = False
        
        print("[LEX AMORIS THREAT] Threat prediction system initialized")
        print(f"[LEX AMORIS THREAT] TensorFlow available: {TF_AVAILABLE}")
    
    def collect_metrics(self, eternal_engine=None) -> SystemMetrics:
        """
        Collect current system metrics for analysis.
        
        Args:
            eternal_engine: Optional EternalDepositionEngine instance
            
        Returns:
            SystemMetrics object
        """
        metrics = SystemMetrics()
        
        if eternal_engine:
            # Extract metrics from eternal deposition engine
            nodes = eternal_engine.nodes.values()
            
            # Energy variance
            energies = [n.energy_level for n in nodes]
            metrics.energy_variance = float(np.var(energies))
            
            # Node synchronization (based on phase alignment)
            phases = [n.resonance_phase for n in nodes]
            phase_coherence = 1.0 - (np.std(phases) / (2 * np.pi))
            metrics.node_synchronization = max(0.0, min(1.0, phase_coherence))
            
            # Resonance stability
            if eternal_engine.optimization_metrics:
                recent_metrics = eternal_engine.optimization_metrics[-10:]
                metrics.resonance_stability = 1.0 - min(1.0, abs(np.std(recent_metrics)))
            
            # Network coherence
            avg_energy = np.mean(energies)
            metrics.network_coherence = max(0.0, min(1.0, avg_energy))
            
            # Quantum entropy (simplified measure)
            metrics.quantum_entropy = float(np.std(energies))
        else:
            # Use simulated metrics for standalone operation
            metrics.energy_variance = np.random.uniform(0.0, 0.1)
            metrics.node_synchronization = np.random.uniform(0.8, 1.0)
            metrics.resonance_stability = np.random.uniform(0.85, 1.0)
            metrics.network_coherence = np.random.uniform(0.9, 1.0)
            metrics.quantum_entropy = np.random.uniform(0.0, 0.2)
        
        return metrics
    
    def metrics_to_vector(self, metrics: SystemMetrics) -> np.ndarray:
        """Convert SystemMetrics to numpy array."""
        return np.array([
            metrics.energy_variance,
            metrics.node_synchronization,
            metrics.resonance_stability,
            metrics.network_coherence,
            metrics.quantum_entropy
        ], dtype=np.float32)
    
    def analyze_threat(self, metrics: SystemMetrics) -> Optional[ThreatEvent]:
        """
        Analyze system metrics for potential threats.
        
        Args:
            metrics: Current system metrics
            
        Returns:
            ThreatEvent if threat detected, None otherwise
        """
        # Convert metrics to vector
        metrics_vector = self.metrics_to_vector(metrics)
        
        # Store in history
        self.metrics_history.append(metrics_vector)
        
        # Need sufficient history before analysis
        if len(self.metrics_history) < 10:
            return None
        
        # Perform anomaly detection
        anomaly_score, confidence = self.anomaly_model.predict_anomaly(metrics_vector)
        
        # Determine if this is a threat
        if anomaly_score > ANOMALY_THRESHOLD and confidence > PREDICTION_CONFIDENCE_MIN:
            # Classify threat type
            threat_type = self._classify_threat(metrics, anomaly_score)
            threat_level = self._calculate_threat_level(anomaly_score, metrics)
            
            # Create threat event
            threat = ThreatEvent(
                timestamp=datetime.now().isoformat(),
                threat_level=threat_level,
                anomaly_score=anomaly_score,
                threat_type=threat_type,
                description=self._generate_threat_description(threat_type, metrics),
                confidence=confidence,
                metadata={
                    'energy_variance': metrics.energy_variance,
                    'node_synchronization': metrics.node_synchronization,
                    'resonance_stability': metrics.resonance_stability,
                    'network_coherence': metrics.network_coherence,
                    'quantum_entropy': metrics.quantum_entropy
                }
            )
            
            self.threat_events.append(threat)
            return threat
        
        return None
    
    def _classify_threat(self, metrics: SystemMetrics, anomaly_score: float) -> str:
        """Classify the type of threat based on metrics."""
        # Determine which metric is most anomalous
        if metrics.energy_variance > 0.3:
            return "ENERGY_INSTABILITY"
        elif metrics.node_synchronization < 0.5:
            return "DESYNCHRONIZATION"
        elif metrics.resonance_stability < 0.6:
            return "RESONANCE_DISRUPTION"
        elif metrics.network_coherence < 0.7:
            return "NETWORK_DEGRADATION"
        elif metrics.quantum_entropy > 0.5:
            return "QUANTUM_DECOHERENCE"
        else:
            return "GENERAL_ANOMALY"
    
    def _calculate_threat_level(self, anomaly_score: float, metrics: SystemMetrics) -> float:
        """Calculate overall threat level (0.0 to 1.0)."""
        # Combine anomaly score with critical metrics
        critical_factor = 1.0 - min(
            metrics.node_synchronization,
            metrics.resonance_stability,
            metrics.network_coherence
        )
        
        threat_level = (anomaly_score * 0.7 + critical_factor * 0.3)
        return min(1.0, max(0.0, threat_level))
    
    def _generate_threat_description(self, threat_type: str, metrics: SystemMetrics) -> str:
        """Generate human-readable threat description."""
        descriptions = {
            "ENERGY_INSTABILITY": f"High energy variance detected ({metrics.energy_variance:.4f})",
            "DESYNCHRONIZATION": f"Node synchronization dropped to {metrics.node_synchronization:.2%}",
            "RESONANCE_DISRUPTION": f"Resonance stability compromised ({metrics.resonance_stability:.2%})",
            "NETWORK_DEGRADATION": f"Network coherence below threshold ({metrics.network_coherence:.2%})",
            "QUANTUM_DECOHERENCE": f"Elevated quantum entropy ({metrics.quantum_entropy:.4f})",
            "GENERAL_ANOMALY": "Unusual system behavior detected"
        }
        return descriptions.get(threat_type, "Unknown threat pattern")
    
    def train_on_normal_behavior(self, num_samples: int = 1000):
        """
        Train the anomaly model on simulated normal behavior.
        
        Args:
            num_samples: Number of normal samples to generate
        """
        print(f"[TRAINING] Generating {num_samples} normal behavior samples...")
        
        # Generate normal behavior data
        normal_data = []
        for _ in range(num_samples):
            # Simulate normal operating ranges
            sample = np.array([
                np.random.uniform(0.0, 0.15),   # energy_variance
                np.random.uniform(0.85, 1.0),   # node_synchronization
                np.random.uniform(0.90, 1.0),   # resonance_stability
                np.random.uniform(0.85, 1.0),   # network_coherence
                np.random.uniform(0.0, 0.15)    # quantum_entropy
            ], dtype=np.float32)
            normal_data.append(sample)
        
        normal_data = np.array(normal_data)
        
        # Train the model
        self.anomaly_model.train(normal_data, epochs=50)
        self.last_training_time = time.time()
    
    def should_retrain(self) -> bool:
        """Determine if model should be retrained."""
        time_since_training = time.time() - self.last_training_time
        return time_since_training > RETRAINING_INTERVAL
    
    def get_threat_summary(self) -> Dict:
        """Get summary of recent threats."""
        if not self.threat_events:
            return {
                "total_threats": 0,
                "active_threats": 0,
                "threat_level": "LOW",
                "threat_status": "LOW"
            }
        
        # Analyze recent threats (last 10)
        recent_threats = self.threat_events[-10:]
        avg_threat_level = np.mean([t.threat_level for t in recent_threats])
        
        # Determine overall threat status
        if avg_threat_level > 0.8:
            threat_status = "CRITICAL"
        elif avg_threat_level > 0.6:
            threat_status = "HIGH"
        elif avg_threat_level > 0.4:
            threat_status = "MODERATE"
        else:
            threat_status = "LOW"
        
        return {
            "total_threats": len(self.threat_events),
            "recent_threats": len(recent_threats),
            "average_threat_level": float(avg_threat_level),
            "threat_status": threat_status,
            "latest_threat": {
                "type": recent_threats[-1].threat_type,
                "level": recent_threats[-1].threat_level,
                "timestamp": recent_threats[-1].timestamp
            } if recent_threats else None
        }
    
    def save_threat_log(self, filepath: str = "threat_log.json"):
        """Save threat events to file."""
        threat_data = {
            "timestamp": datetime.now().isoformat(),
            "total_threats": len(self.threat_events),
            "threats": [
                {
                    "timestamp": t.timestamp,
                    "threat_level": t.threat_level,
                    "anomaly_score": t.anomaly_score,
                    "threat_type": t.threat_type,
                    "description": t.description,
                    "confidence": t.confidence
                }
                for t in self.threat_events
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(threat_data, f, indent=2)
        
        print(f"[THREAT LOG] Saved {len(self.threat_events)} threats to {filepath}")


def main():
    """Main entry point for threat prediction system."""
    print("=" * 70)
    print("LEX AMORIS - KI-BASIERTE BEDROHUNGSVORHERSAGE")
    print("AI-based Threat Prediction System")
    print("=" * 70)
    print()
    
    # Initialize predictor
    predictor = LexAmorisThreatPredictor()
    
    # Train on normal behavior
    predictor.train_on_normal_behavior(num_samples=1000)
    
    # Simulate monitoring
    print("\n[MONITORING] Starting threat monitoring simulation...")
    for i in range(20):
        # Collect metrics (simulated)
        metrics = predictor.collect_metrics()
        
        # Analyze for threats
        threat = predictor.analyze_threat(metrics)
        
        if threat:
            print(f"[THREAT DETECTED] {threat.threat_type} - "
                  f"Level: {threat.threat_level:.2f} - "
                  f"Confidence: {threat.confidence:.2%}")
            print(f"  Description: {threat.description}")
        
        time.sleep(0.5)
    
    # Show summary
    summary = predictor.get_threat_summary()
    print(f"\n[SUMMARY] Threat Status: {summary['threat_status']}")
    print(f"[SUMMARY] Total Threats: {summary['total_threats']}")
    
    # Save log
    predictor.save_threat_log()


if __name__ == "__main__":
    main()
