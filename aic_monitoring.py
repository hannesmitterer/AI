#!/usr/bin/env python3
"""
AIC Distributed Monitoring Framework
=====================================

This module implements a distributed monitoring system that allows AICs
to detect anomalies and manage distributed loads autonomously.

Key Features:
- Real-time metric collection and analysis
- Anomaly detection using statistical methods
- Distributed load balancing across AICs
- Automatic alerting and response
- Scalable monitoring across multiple nodes

Based on: Eternal Deposition System and Kosymbiosis principles
"""

import time
import math
import json
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from collections import deque


class AlertSeverity(Enum):
    """Severity levels for monitoring alerts."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class MetricType(Enum):
    """Types of metrics that can be monitored."""
    CPU_USAGE = "cpu_usage"
    MEMORY_USAGE = "memory_usage"
    REQUEST_RATE = "request_rate"
    ERROR_RATE = "error_rate"
    RESPONSE_TIME = "response_time"
    CUSTOM = "custom"


@dataclass
class Metric:
    """Represents a single metric measurement."""
    metric_type: MetricType
    value: float
    timestamp: float = field(default_factory=time.time)
    aic_id: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Alert:
    """Represents a monitoring alert."""
    alert_id: str
    severity: AlertSeverity
    message: str
    timestamp: float = field(default_factory=time.time)
    aic_id: str = ""
    metric_type: Optional[MetricType] = None
    current_value: Optional[float] = None
    threshold: Optional[float] = None
    resolved: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert alert to dictionary."""
        return {
            "alert_id": self.alert_id,
            "severity": self.severity.value,
            "message": self.message,
            "timestamp": self.timestamp,
            "aic_id": self.aic_id,
            "metric_type": self.metric_type.value if self.metric_type else None,
            "current_value": self.current_value,
            "threshold": self.threshold,
            "resolved": self.resolved
        }


@dataclass
class AICNode:
    """Represents a monitored AIC node in the distributed system."""
    aic_id: str
    load: float = 0.0
    capacity: float = 100.0
    active: bool = True
    last_heartbeat: float = field(default_factory=time.time)
    metrics: Dict[MetricType, deque] = field(default_factory=dict)
    alert_count: int = 0
    
    def update_heartbeat(self) -> None:
        """Update last heartbeat timestamp."""
        self.last_heartbeat = time.time()
    
    def is_healthy(self, timeout_seconds: float = 30.0) -> bool:
        """Check if node is healthy based on heartbeat."""
        return time.time() - self.last_heartbeat < timeout_seconds
    
    def add_metric(self, metric: Metric, max_history: int = 1000) -> None:
        """Add a metric measurement to node history."""
        if metric.metric_type not in self.metrics:
            self.metrics[metric.metric_type] = deque(maxlen=max_history)
        
        self.metrics[metric.metric_type].append(metric)
    
    def get_metric_average(self, metric_type: MetricType, window_size: int = 10) -> Optional[float]:
        """Calculate average value for a metric over recent history."""
        if metric_type not in self.metrics or not self.metrics[metric_type]:
            return None
        
        recent_metrics = list(self.metrics[metric_type])[-window_size:]
        if not recent_metrics:
            return None
        
        return sum(m.value for m in recent_metrics) / len(recent_metrics)


class AnomalyDetector:
    """
    Detects anomalies in metric data using statistical methods.
    """
    
    def __init__(self, sensitivity: float = 2.0):
        """
        Initialize anomaly detector.
        
        Args:
            sensitivity: Number of standard deviations for anomaly threshold
        """
        self.sensitivity = sensitivity
    
    def detect_anomaly(
        self,
        current_value: float,
        historical_values: List[float],
        method: str = "zscore"
    ) -> bool:
        """
        Detect if current value is anomalous compared to history.
        
        Args:
            current_value: Current metric value
            historical_values: Historical values for comparison
            method: Detection method ('zscore', 'iqr')
            
        Returns:
            True if anomaly detected
        """
        if not historical_values or len(historical_values) < 3:
            return False
        
        if method == "zscore":
            return self._zscore_detection(current_value, historical_values)
        elif method == "iqr":
            return self._iqr_detection(current_value, historical_values)
        
        return False
    
    def _zscore_detection(self, value: float, history: List[float]) -> bool:
        """Detect anomaly using Z-score method."""
        mean = sum(history) / len(history)
        variance = sum((x - mean) ** 2 for x in history) / len(history)
        std_dev = math.sqrt(variance)
        
        if std_dev == 0:
            return False
        
        z_score = abs((value - mean) / std_dev)
        return z_score > self.sensitivity
    
    def _iqr_detection(self, value: float, history: List[float]) -> bool:
        """Detect anomaly using Interquartile Range method."""
        sorted_history = sorted(history)
        n = len(sorted_history)
        
        q1_idx = n // 4
        q3_idx = 3 * n // 4
        
        q1 = sorted_history[q1_idx]
        q3 = sorted_history[q3_idx]
        iqr = q3 - q1
        
        lower_bound = q1 - self.sensitivity * iqr
        upper_bound = q3 + self.sensitivity * iqr
        
        return value < lower_bound or value > upper_bound


class LoadBalancer:
    """
    Manages distributed load balancing across AIC nodes.
    """
    
    def __init__(self, strategy: str = "least_loaded"):
        """
        Initialize load balancer.
        
        Args:
            strategy: Load balancing strategy ('least_loaded', 'round_robin', 'weighted')
        """
        self.strategy = strategy
        self.round_robin_index = 0
    
    def select_node(self, nodes: List[AICNode]) -> Optional[AICNode]:
        """
        Select optimal node for task assignment.
        
        Args:
            nodes: List of available AIC nodes
            
        Returns:
            Selected AIC node or None if no nodes available
        """
        # Filter only healthy and active nodes
        available_nodes = [n for n in nodes if n.active and n.is_healthy()]
        
        if not available_nodes:
            return None
        
        if self.strategy == "least_loaded":
            return self._least_loaded_selection(available_nodes)
        elif self.strategy == "round_robin":
            return self._round_robin_selection(available_nodes)
        elif self.strategy == "weighted":
            return self._weighted_selection(available_nodes)
        
        return available_nodes[0]
    
    def _least_loaded_selection(self, nodes: List[AICNode]) -> AICNode:
        """Select node with lowest current load."""
        return min(nodes, key=lambda n: n.load / n.capacity)
    
    def _round_robin_selection(self, nodes: List[AICNode]) -> AICNode:
        """Select node using round-robin strategy."""
        selected = nodes[self.round_robin_index % len(nodes)]
        self.round_robin_index += 1
        return selected
    
    def _weighted_selection(self, nodes: List[AICNode]) -> AICNode:
        """Select node based on capacity-weighted probability."""
        # Simple weighted selection: prefer nodes with higher capacity
        return max(nodes, key=lambda n: (n.capacity - n.load) / n.capacity)
    
    def rebalance_load(self, nodes: List[AICNode]) -> List[Dict[str, Any]]:
        """
        Analyze and suggest load rebalancing actions.
        
        Args:
            nodes: List of AIC nodes
            
        Returns:
            List of rebalancing suggestions
        """
        active_nodes = [n for n in nodes if n.active and n.is_healthy()]
        
        if len(active_nodes) < 2:
            return []
        
        # Calculate average load ratio
        avg_load_ratio = sum(n.load / n.capacity for n in active_nodes) / len(active_nodes)
        
        suggestions = []
        
        for node in active_nodes:
            load_ratio = node.load / node.capacity
            deviation = load_ratio - avg_load_ratio
            
            # If node is significantly overloaded
            if deviation > 0.2:  # 20% above average
                suggestions.append({
                    "action": "reduce_load",
                    "aic_id": node.aic_id,
                    "current_load_ratio": load_ratio,
                    "target_load_ratio": avg_load_ratio,
                    "load_to_transfer": deviation * node.capacity
                })
            # If node is significantly underloaded
            elif deviation < -0.2:  # 20% below average
                suggestions.append({
                    "action": "increase_load",
                    "aic_id": node.aic_id,
                    "current_load_ratio": load_ratio,
                    "target_load_ratio": avg_load_ratio,
                    "load_capacity_available": abs(deviation) * node.capacity
                })
        
        return suggestions


class AICMonitoringSystem:
    """
    Distributed monitoring system for autonomous AIC management.
    
    Provides real-time monitoring, anomaly detection, and load balancing
    across a distributed network of AIC nodes.
    """
    
    def __init__(
        self,
        anomaly_sensitivity: float = 2.0,
        load_balancing_strategy: str = "least_loaded"
    ):
        """
        Initialize the monitoring system.
        
        Args:
            anomaly_sensitivity: Sensitivity for anomaly detection
            load_balancing_strategy: Strategy for load balancing
        """
        self.nodes: Dict[str, AICNode] = {}
        self.alerts: List[Alert] = []
        self.alert_counter = 0
        
        self.anomaly_detector = AnomalyDetector(sensitivity=anomaly_sensitivity)
        self.load_balancer = LoadBalancer(strategy=load_balancing_strategy)
        
        print(f"[AIC MONITORING] Initialized distributed monitoring system")
        print(f"[AIC MONITORING] Anomaly sensitivity: {anomaly_sensitivity}")
        print(f"[AIC MONITORING] Load balancing: {load_balancing_strategy}")
    
    def register_node(
        self,
        aic_id: str,
        capacity: float = 100.0
    ) -> None:
        """
        Register a new AIC node for monitoring.
        
        Args:
            aic_id: Unique identifier for the AIC
            capacity: Processing capacity of the node
        """
        if aic_id in self.nodes:
            print(f"[AIC MONITORING] Node {aic_id} already registered, updating")
        
        self.nodes[aic_id] = AICNode(
            aic_id=aic_id,
            capacity=capacity
        )
        
        print(f"[AIC MONITORING] Registered node {aic_id} with capacity {capacity}")
    
    def record_metric(
        self,
        aic_id: str,
        metric_type: MetricType,
        value: float,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Record a metric measurement for an AIC node.
        
        Args:
            aic_id: AIC node identifier
            metric_type: Type of metric
            value: Metric value
            metadata: Optional metadata
        """
        if aic_id not in self.nodes:
            self.register_node(aic_id)
        
        node = self.nodes[aic_id]
        
        metric = Metric(
            metric_type=metric_type,
            value=value,
            aic_id=aic_id,
            metadata=metadata or {}
        )
        
        node.add_metric(metric)
        node.update_heartbeat()
        
        # Check for anomalies
        self._check_metric_anomaly(node, metric)
        
        # Update node load if metric is load-related
        if metric_type == MetricType.CPU_USAGE:
            node.load = value
    
    def update_node_load(self, aic_id: str, load: float) -> None:
        """
        Update current load for an AIC node.
        
        Args:
            aic_id: AIC node identifier
            load: Current load value
        """
        if aic_id not in self.nodes:
            self.register_node(aic_id)
        
        self.nodes[aic_id].load = load
        self.nodes[aic_id].update_heartbeat()
    
    def select_node_for_task(self) -> Optional[str]:
        """
        Select optimal node for task assignment using load balancing.
        
        Returns:
            AIC ID of selected node, or None if no nodes available
        """
        nodes_list = list(self.nodes.values())
        selected_node = self.load_balancer.select_node(nodes_list)
        
        return selected_node.aic_id if selected_node else None
    
    def get_load_balancing_suggestions(self) -> List[Dict[str, Any]]:
        """
        Get suggestions for load rebalancing.
        
        Returns:
            List of rebalancing suggestions
        """
        nodes_list = list(self.nodes.values())
        return self.load_balancer.rebalance_load(nodes_list)
    
    def create_alert(
        self,
        severity: AlertSeverity,
        message: str,
        aic_id: str = "",
        metric_type: Optional[MetricType] = None,
        current_value: Optional[float] = None,
        threshold: Optional[float] = None
    ) -> Alert:
        """
        Create a monitoring alert.
        
        Args:
            severity: Alert severity level
            message: Alert message
            aic_id: Associated AIC node
            metric_type: Associated metric type
            current_value: Current metric value
            threshold: Threshold that was exceeded
            
        Returns:
            Created Alert object
        """
        self.alert_counter += 1
        alert = Alert(
            alert_id=f"alert_{self.alert_counter:06d}",
            severity=severity,
            message=message,
            aic_id=aic_id,
            metric_type=metric_type,
            current_value=current_value,
            threshold=threshold
        )
        
        self.alerts.append(alert)
        
        if aic_id in self.nodes:
            self.nodes[aic_id].alert_count += 1
        
        print(f"[AIC MONITORING] {severity.value.upper()} Alert: {message}")
        
        return alert
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get overall system status.
        
        Returns:
            Dictionary containing system status information
        """
        active_nodes = [n for n in self.nodes.values() if n.active and n.is_healthy()]
        
        total_capacity = sum(n.capacity for n in active_nodes)
        total_load = sum(n.load for n in active_nodes)
        avg_load_ratio = total_load / total_capacity if total_capacity > 0 else 0
        
        unresolved_alerts = [a for a in self.alerts if not a.resolved]
        critical_alerts = [a for a in unresolved_alerts if a.severity == AlertSeverity.CRITICAL]
        
        return {
            "total_nodes": len(self.nodes),
            "active_nodes": len(active_nodes),
            "inactive_nodes": len(self.nodes) - len(active_nodes),
            "total_capacity": total_capacity,
            "total_load": total_load,
            "average_load_ratio": avg_load_ratio,
            "total_alerts": len(self.alerts),
            "unresolved_alerts": len(unresolved_alerts),
            "critical_alerts": len(critical_alerts),
            "timestamp": time.time()
        }
    
    def get_node_status(self, aic_id: str) -> Dict[str, Any]:
        """
        Get status for a specific node.
        
        Args:
            aic_id: AIC node identifier
            
        Returns:
            Dictionary containing node status
        """
        if aic_id not in self.nodes:
            raise ValueError(f"Node {aic_id} not found")
        
        node = self.nodes[aic_id]
        
        return {
            "aic_id": aic_id,
            "active": node.active,
            "healthy": node.is_healthy(),
            "load": node.load,
            "capacity": node.capacity,
            "load_ratio": node.load / node.capacity,
            "last_heartbeat": node.last_heartbeat,
            "heartbeat_age": time.time() - node.last_heartbeat,
            "alert_count": node.alert_count,
            "metrics_tracked": len(node.metrics)
        }
    
    def _check_metric_anomaly(self, node: AICNode, metric: Metric) -> None:
        """Check if metric value is anomalous and create alert if needed."""
        if metric.metric_type not in node.metrics:
            return
        
        # Get historical values
        historical_values = [
            m.value for m in node.metrics[metric.metric_type]
            if m.timestamp < metric.timestamp
        ]
        
        if len(historical_values) < 10:  # Need sufficient history
            return
        
        # Detect anomaly
        is_anomaly = self.anomaly_detector.detect_anomaly(
            metric.value,
            historical_values[-100:]  # Use last 100 values
        )
        
        if is_anomaly:
            # Calculate severity based on deviation
            avg = sum(historical_values[-100:]) / len(historical_values[-100:])
            deviation_ratio = abs(metric.value - avg) / avg if avg != 0 else 0
            
            if deviation_ratio > 1.0:  # >100% deviation
                severity = AlertSeverity.CRITICAL
            elif deviation_ratio > 0.5:  # >50% deviation
                severity = AlertSeverity.WARNING
            else:
                severity = AlertSeverity.INFO
            
            self.create_alert(
                severity=severity,
                message=f"Anomaly detected in {metric.metric_type.value}",
                aic_id=node.aic_id,
                metric_type=metric.metric_type,
                current_value=metric.value,
                threshold=avg
            )


# Example usage
if __name__ == "__main__":
    print("=== AIC Distributed Monitoring System Demo ===\n")
    
    # Initialize monitoring system
    monitor = AICMonitoringSystem(
        anomaly_sensitivity=2.0,
        load_balancing_strategy="least_loaded"
    )
    
    # Register nodes
    for i in range(5):
        monitor.register_node(f"aic_{i:03d}", capacity=100.0)
    
    # Simulate metric recording
    print("\n--- Recording metrics ---")
    for cycle in range(20):
        for i in range(5):
            aic_id = f"aic_{i:03d}"
            
            # Normal load pattern
            base_load = 50.0 + 10 * math.sin(cycle * 0.5 + i)
            
            # Introduce anomaly in aic_002 at cycle 15
            if aic_id == "aic_002" and cycle == 15:
                base_load = 95.0  # Spike
            
            monitor.record_metric(
                aic_id,
                MetricType.CPU_USAGE,
                base_load
            )
            
            monitor.update_node_load(aic_id, base_load)
        
        time.sleep(0.1)  # Simulate time passing
    
    # Get system status
    print("\n--- System Status ---")
    status = monitor.get_system_status()
    print(json.dumps(status, indent=2))
    
    # Get load balancing suggestions
    print("\n--- Load Balancing Suggestions ---")
    suggestions = monitor.get_load_balancing_suggestions()
    for suggestion in suggestions:
        print(json.dumps(suggestion, indent=2))
    
    # Select node for new task
    print("\n--- Task Assignment ---")
    selected = monitor.select_node_for_task()
    print(f"Selected node for task: {selected}")
    
    if selected:
        node_status = monitor.get_node_status(selected)
        print(f"Node status: {json.dumps(node_status, indent=2)}")
    
    print("\n=== Demo Complete ===")
