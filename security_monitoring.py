#!/usr/bin/env python3
"""
Security Monitoring Module - Real-time Protocol Monitoring
==========================================================

This module implements real-time monitoring for protocol operations,
providing comprehensive logging and event tracking for security purposes.

Features:
- Real-time log monitoring and analysis
- Protocol operation validation
- Event tracking and alerting
- Integration with eternal deposition system
- Blacklist management and enforcement

Part of: Blacklist Defense Strategies and Meta-Management
"""

import time
import json
import hashlib
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from datetime import datetime
from collections import deque
from enum import Enum


class EventSeverity(Enum):
    """Severity levels for security events."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class ProtocolStatus(Enum):
    """Status codes for protocol operations."""
    NORMAL = "normal"
    SUSPICIOUS = "suspicious"
    BLOCKED = "blocked"
    VERIFIED = "verified"


@dataclass
class SecurityEvent:
    """Represents a security event in the system."""
    event_id: str
    timestamp: float
    event_type: str
    severity: EventSeverity
    source: str
    description: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert event to dictionary."""
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "datetime": datetime.fromtimestamp(self.timestamp).isoformat(),
            "event_type": self.event_type,
            "severity": self.severity.value,
            "source": self.source,
            "description": self.description,
            "metadata": self.metadata
        }


@dataclass
class ProtocolLog:
    """Represents a protocol operation log entry."""
    log_id: str
    timestamp: float
    operation: str
    status: ProtocolStatus
    details: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert log to dictionary."""
        return {
            "log_id": self.log_id,
            "timestamp": self.timestamp,
            "datetime": datetime.fromtimestamp(self.timestamp).isoformat(),
            "operation": self.operation,
            "status": self.status.value,
            "details": self.details
        }


class SecurityMonitor:
    """
    Real-time security monitoring system.
    
    Provides comprehensive monitoring of protocol operations,
    event tracking, and security event management.
    """
    
    def __init__(self, max_events: int = 10000, max_logs: int = 10000):
        """
        Initialize security monitor.
        
        Args:
            max_events: Maximum number of events to retain in memory
            max_logs: Maximum number of logs to retain in memory
        """
        self.events: deque = deque(maxlen=max_events)
        self.protocol_logs: deque = deque(maxlen=max_logs)
        self.event_handlers: Dict[str, List[Callable]] = {}
        self.is_monitoring: bool = False
        self.start_time: float = time.time()
        self.statistics: Dict[str, int] = {
            "total_events": 0,
            "total_logs": 0,
            "critical_events": 0,
            "blocked_operations": 0,
            "verified_operations": 0
        }
        
        print(f"[SECURITY MONITOR] Initialized")
        print(f"[SECURITY MONITOR] Max events: {max_events}")
        print(f"[SECURITY MONITOR] Max logs: {max_logs}")
    
    def start_monitoring(self) -> None:
        """Start real-time monitoring."""
        self.is_monitoring = True
        self.start_time = time.time()
        print(f"[SECURITY MONITOR] Monitoring started at {datetime.now().isoformat()}")
    
    def stop_monitoring(self) -> None:
        """Stop real-time monitoring."""
        self.is_monitoring = False
        print(f"[SECURITY MONITOR] Monitoring stopped")
        self._print_statistics()
    
    def log_event(self, event_type: str, severity: EventSeverity,
                  source: str, description: str, 
                  metadata: Optional[Dict] = None) -> SecurityEvent:
        """
        Log a security event.
        
        Args:
            event_type: Type of the event
            severity: Severity level
            source: Source of the event
            description: Event description
            metadata: Optional metadata dictionary
        
        Returns:
            SecurityEvent object
        """
        if metadata is None:
            metadata = {}
        
        # Generate event ID
        event_id = self._generate_event_id(event_type, source)
        
        # Create event
        event = SecurityEvent(
            event_id=event_id,
            timestamp=time.time(),
            event_type=event_type,
            severity=severity,
            source=source,
            description=description,
            metadata=metadata
        )
        
        # Store event
        self.events.append(event)
        self.statistics["total_events"] += 1
        
        if severity == EventSeverity.CRITICAL or severity == EventSeverity.EMERGENCY:
            self.statistics["critical_events"] += 1
        
        # Trigger event handlers
        self._trigger_handlers(event_type, event)
        
        # Print critical events immediately
        if severity in [EventSeverity.CRITICAL, EventSeverity.EMERGENCY]:
            print(f"[{severity.value.upper()}] {event_type}: {description}")
        
        return event
    
    def log_protocol_operation(self, operation: str, status: ProtocolStatus,
                               details: Optional[Dict] = None) -> ProtocolLog:
        """
        Log a protocol operation.
        
        Args:
            operation: Operation name
            status: Operation status
            details: Optional details dictionary
        
        Returns:
            ProtocolLog object
        """
        if details is None:
            details = {}
        
        # Generate log ID
        log_id = self._generate_log_id(operation)
        
        # Create log entry
        log = ProtocolLog(
            log_id=log_id,
            timestamp=time.time(),
            operation=operation,
            status=status,
            details=details
        )
        
        # Store log
        self.protocol_logs.append(log)
        self.statistics["total_logs"] += 1
        
        if status == ProtocolStatus.BLOCKED:
            self.statistics["blocked_operations"] += 1
        elif status == ProtocolStatus.VERIFIED:
            self.statistics["verified_operations"] += 1
        
        return log
    
    def register_event_handler(self, event_type: str, 
                               handler: Callable[[SecurityEvent], None]) -> None:
        """
        Register a handler for specific event types.
        
        Args:
            event_type: Type of event to handle
            handler: Callback function to handle the event
        """
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        
        self.event_handlers[event_type].append(handler)
        print(f"[SECURITY MONITOR] Registered handler for event type: {event_type}")
    
    def get_events(self, event_type: Optional[str] = None,
                   severity: Optional[EventSeverity] = None,
                   limit: int = 100) -> List[SecurityEvent]:
        """
        Get events with optional filtering.
        
        Args:
            event_type: Filter by event type
            severity: Filter by severity
            limit: Maximum number of events to return
        
        Returns:
            List of SecurityEvent objects
        """
        events = list(self.events)
        
        # Filter by event type
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        
        # Filter by severity
        if severity:
            events = [e for e in events if e.severity == severity]
        
        # Return most recent events up to limit
        return events[-limit:]
    
    def get_protocol_logs(self, operation: Optional[str] = None,
                          status: Optional[ProtocolStatus] = None,
                          limit: int = 100) -> List[ProtocolLog]:
        """
        Get protocol logs with optional filtering.
        
        Args:
            operation: Filter by operation
            status: Filter by status
            limit: Maximum number of logs to return
        
        Returns:
            List of ProtocolLog objects
        """
        logs = list(self.protocol_logs)
        
        # Filter by operation
        if operation:
            logs = [l for l in logs if l.operation == operation]
        
        # Filter by status
        if status:
            logs = [l for l in logs if l.status == status]
        
        # Return most recent logs up to limit
        return logs[-limit:]
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get monitoring statistics.
        
        Returns:
            Dictionary containing statistics
        """
        uptime = time.time() - self.start_time
        
        return {
            "is_monitoring": self.is_monitoring,
            "uptime_seconds": uptime,
            "total_events": self.statistics["total_events"],
            "total_logs": self.statistics["total_logs"],
            "critical_events": self.statistics["critical_events"],
            "blocked_operations": self.statistics["blocked_operations"],
            "verified_operations": self.statistics["verified_operations"],
            "events_in_memory": len(self.events),
            "logs_in_memory": len(self.protocol_logs),
            "registered_handlers": sum(len(handlers) for handlers in self.event_handlers.values())
        }
    
    def export_events(self, filepath: str, limit: Optional[int] = None) -> None:
        """
        Export events to JSON file.
        
        Args:
            filepath: Path to output file
            limit: Optional limit on number of events to export
        """
        events = list(self.events)
        if limit:
            events = events[-limit:]
        
        data = {
            "export_timestamp": datetime.now().isoformat(),
            "total_events": len(events),
            "events": [e.to_dict() for e in events]
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"[SECURITY MONITOR] Exported {len(events)} events to {filepath}")
    
    def export_logs(self, filepath: str, limit: Optional[int] = None) -> None:
        """
        Export protocol logs to JSON file.
        
        Args:
            filepath: Path to output file
            limit: Optional limit on number of logs to export
        """
        logs = list(self.protocol_logs)
        if limit:
            logs = logs[-limit:]
        
        data = {
            "export_timestamp": datetime.now().isoformat(),
            "total_logs": len(logs),
            "logs": [l.to_dict() for l in logs]
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"[SECURITY MONITOR] Exported {len(logs)} logs to {filepath}")
    
    def _generate_event_id(self, event_type: str, source: str) -> str:
        """Generate unique event ID."""
        data = f"{event_type}:{source}:{time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def _generate_log_id(self, operation: str) -> str:
        """Generate unique log ID."""
        data = f"{operation}:{time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def _trigger_handlers(self, event_type: str, event: SecurityEvent) -> None:
        """Trigger all registered handlers for an event type."""
        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                try:
                    handler(event)
                except Exception as e:
                    print(f"[ERROR] Handler failed for {event_type}: {e}")
    
    def _print_statistics(self) -> None:
        """Print monitoring statistics."""
        stats = self.get_statistics()
        print("\n" + "="*60)
        print("SECURITY MONITORING STATISTICS")
        print("="*60)
        for key, value in stats.items():
            print(f"  {key}: {value}")
        print("="*60)


def main():
    """Demo of security monitoring system."""
    print("="*70)
    print("SECURITY MONITORING SYSTEM - DEMO")
    print("="*70)
    print()
    
    # Initialize monitor
    monitor = SecurityMonitor()
    monitor.start_monitoring()
    
    # Register example event handler
    def critical_event_handler(event: SecurityEvent):
        print(f"[HANDLER] Critical event detected: {event.description}")
    
    monitor.register_event_handler("attack_detected", critical_event_handler)
    
    # Log some events
    monitor.log_event("system_start", EventSeverity.INFO, 
                     "security_monitor", "Security monitoring started")
    
    monitor.log_event("attack_detected", EventSeverity.CRITICAL,
                     "blacklist_defense", "Suspicious activity detected",
                     {"ip": "192.168.1.100", "pattern": "brute_force"})
    
    # Log protocol operations
    monitor.log_protocol_operation("token_validation", ProtocolStatus.VERIFIED,
                                   {"token": "abc123", "user": "system"})
    
    monitor.log_protocol_operation("api_request", ProtocolStatus.BLOCKED,
                                   {"reason": "blacklisted_ip", "ip": "10.0.0.1"})
    
    # Get and display statistics
    time.sleep(1)
    stats = monitor.get_statistics()
    print("\nCurrent Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Export data
    monitor.export_events("/tmp/security_events.json")
    monitor.export_logs("/tmp/protocol_logs.json")
    
    monitor.stop_monitoring()


if __name__ == "__main__":
    main()
