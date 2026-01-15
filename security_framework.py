#!/usr/bin/env python3
"""
Security Framework for AI System
=================================

Implements advanced blacklisting strategies and meta-management including:
1. Threat detection and blocking mechanisms
2. Attack logging framework
3. Control structures against silent scans

Part of the Eternal Deposition System security layer.
"""

import time
import json
import hashlib
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict
from enum import Enum


class ThreatLevel(Enum):
    """Classification of threat severity."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class AttackType(Enum):
    """Types of detected attacks."""
    SILENT_SCAN = "silent_scan"
    BRUTE_FORCE = "brute_force"
    DOS = "denial_of_service"
    INJECTION = "injection"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    ANOMALY = "anomaly"


@dataclass
class ThreatEntity:
    """Represents a potentially threatening entity."""
    entity_id: str
    threat_level: ThreatLevel
    blacklisted_at: float
    expires_at: Optional[float] = None
    reason: str = ""
    attack_count: int = 0
    last_activity: float = field(default_factory=time.time)
    
    def is_expired(self) -> bool:
        """Check if blacklist entry has expired."""
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at
    
    def update_activity(self) -> None:
        """Update last activity timestamp."""
        self.last_activity = time.time()
        self.attack_count += 1


@dataclass
class AttackEvent:
    """Records a security attack event."""
    timestamp: float
    entity_id: str
    attack_type: AttackType
    threat_level: ThreatLevel
    details: Dict
    blocked: bool = False
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "timestamp": self.timestamp,
            "datetime": datetime.fromtimestamp(self.timestamp).isoformat(),
            "entity_id": self.entity_id,
            "attack_type": self.attack_type.value,
            "threat_level": self.threat_level.name,
            "details": self.details,
            "blocked": self.blocked
        }


class ThreatDetector:
    """
    Detects artificial threats and implements blocking mechanisms.
    
    Features:
    - Pattern-based threat recognition
    - Behavior anomaly detection
    - Adaptive blacklisting with time-based expiry
    """
    
    def __init__(self, 
                 max_requests_per_minute: int = 60,
                 blacklist_duration: int = 3600,
                 anomaly_threshold: float = 0.75):
        """
        Initialize threat detector.
        
        Args:
            max_requests_per_minute: Maximum allowed requests per entity per minute
            blacklist_duration: Duration in seconds for temporary blacklisting
            anomaly_threshold: Threshold for anomaly detection (0-1)
        """
        self.blacklist: Dict[str, ThreatEntity] = {}
        self.request_history: Dict[str, List[float]] = defaultdict(list)
        self.max_requests_per_minute = max_requests_per_minute
        self.blacklist_duration = blacklist_duration
        self.anomaly_threshold = anomaly_threshold
        self.behavior_patterns: Dict[str, List[Dict]] = defaultdict(list)
        
    def is_blacklisted(self, entity_id: str) -> bool:
        """
        Check if an entity is currently blacklisted.
        
        Args:
            entity_id: Identifier of the entity to check
            
        Returns:
            True if blacklisted and not expired, False otherwise
        """
        if entity_id not in self.blacklist:
            return False
        
        threat = self.blacklist[entity_id]
        
        # Check if blacklist entry has expired
        if threat.is_expired():
            del self.blacklist[entity_id]
            return False
        
        return True
    
    def add_to_blacklist(self, 
                        entity_id: str, 
                        threat_level: ThreatLevel,
                        reason: str = "",
                        duration: Optional[int] = None) -> None:
        """
        Add an entity to the blacklist.
        
        Args:
            entity_id: Identifier of the entity to blacklist
            threat_level: Severity level of the threat
            reason: Reason for blacklisting
            duration: Duration in seconds (None for permanent)
        """
        current_time = time.time()
        expires_at = None if duration is None else current_time + (duration or self.blacklist_duration)
        
        if entity_id in self.blacklist:
            # Update existing entry
            threat = self.blacklist[entity_id]
            threat.update_activity()
            threat.threat_level = max(threat.threat_level, threat_level, key=lambda x: x.value)
            if reason:
                threat.reason = reason
        else:
            # Create new entry
            self.blacklist[entity_id] = ThreatEntity(
                entity_id=entity_id,
                threat_level=threat_level,
                blacklisted_at=current_time,
                expires_at=expires_at,
                reason=reason,
                attack_count=1
            )
    
    def remove_from_blacklist(self, entity_id: str) -> bool:
        """
        Remove an entity from the blacklist.
        
        Args:
            entity_id: Identifier of the entity to remove
            
        Returns:
            True if removed, False if not found
        """
        if entity_id in self.blacklist:
            del self.blacklist[entity_id]
            return True
        return False
    
    def detect_rate_limit_violation(self, entity_id: str) -> bool:
        """
        Detect if an entity is exceeding rate limits.
        
        Args:
            entity_id: Identifier of the entity
            
        Returns:
            True if rate limit violated, False otherwise
        """
        current_time = time.time()
        
        # Add current request
        self.request_history[entity_id].append(current_time)
        
        # Clean up old requests (older than 1 minute)
        cutoff_time = current_time - 60
        self.request_history[entity_id] = [
            t for t in self.request_history[entity_id] if t > cutoff_time
        ]
        
        # Check if rate limit exceeded
        request_count = len(self.request_history[entity_id])
        return request_count > self.max_requests_per_minute
    
    def detect_anomaly(self, entity_id: str, behavior: Dict) -> Tuple[bool, float]:
        """
        Detect behavioral anomalies.
        
        Args:
            entity_id: Identifier of the entity
            behavior: Dictionary describing current behavior
            
        Returns:
            Tuple of (is_anomalous, anomaly_score)
        """
        self.behavior_patterns[entity_id].append(behavior)
        
        # Keep only recent patterns (last 100)
        if len(self.behavior_patterns[entity_id]) > 100:
            self.behavior_patterns[entity_id] = self.behavior_patterns[entity_id][-100:]
        
        # Calculate anomaly score based on deviation from normal behavior
        if len(self.behavior_patterns[entity_id]) < 10:
            return False, 0.0  # Not enough data
        
        # Simple anomaly detection: compare current behavior with average
        patterns = self.behavior_patterns[entity_id]
        current = patterns[-1]
        previous = patterns[-11:-1]  # Last 10 behaviors
        
        anomaly_score = 0.0
        comparison_count = 0
        
        for key in current:
            if key in previous[0]:
                try:
                    current_val = float(current[key])
                    avg_val = sum(float(p.get(key, 0)) for p in previous) / len(previous)
                    
                    if avg_val > 0:
                        deviation = abs(current_val - avg_val) / avg_val
                        anomaly_score += deviation
                        comparison_count += 1
                except (ValueError, TypeError):
                    pass
        
        if comparison_count > 0:
            anomaly_score /= comparison_count
        
        is_anomalous = anomaly_score > self.anomaly_threshold
        return is_anomalous, anomaly_score
    
    def cleanup_expired(self) -> int:
        """
        Remove expired blacklist entries.
        
        Returns:
            Number of entries removed
        """
        expired = [
            entity_id for entity_id, threat in self.blacklist.items()
            if threat.is_expired()
        ]
        
        for entity_id in expired:
            del self.blacklist[entity_id]
        
        return len(expired)
    
    def get_blacklist_status(self) -> Dict:
        """Get current blacklist status."""
        return {
            "total_entries": len(self.blacklist),
            "by_threat_level": {
                level.name: sum(1 for t in self.blacklist.values() if t.threat_level == level)
                for level in ThreatLevel
            },
            "entries": [
                {
                    "entity_id": entity_id,
                    "threat_level": threat.threat_level.name,
                    "blacklisted_at": datetime.fromtimestamp(threat.blacklisted_at).isoformat(),
                    "expires_at": datetime.fromtimestamp(threat.expires_at).isoformat() if threat.expires_at else "permanent",
                    "reason": threat.reason,
                    "attack_count": threat.attack_count
                }
                for entity_id, threat in self.blacklist.items()
            ]
        }


class AttackLogger:
    """
    Framework for logging and analyzing attack events.
    
    Features:
    - Structured event logging
    - Persistent storage
    - Attack analytics and reporting
    """
    
    def __init__(self, log_file: str = "attack_log.json", max_events: int = 10000):
        """
        Initialize attack logger.
        
        Args:
            log_file: Path to log file
            max_events: Maximum number of events to keep in memory
        """
        self.log_file = log_file
        self.max_events = max_events
        self.events: List[AttackEvent] = []
        self.attack_counts: Dict[str, int] = defaultdict(int)
        self.load_log()
    
    def log_attack(self, 
                   entity_id: str,
                   attack_type: AttackType,
                   threat_level: ThreatLevel,
                   details: Dict,
                   blocked: bool = False) -> AttackEvent:
        """
        Log an attack event.
        
        Args:
            entity_id: Identifier of the attacking entity
            attack_type: Type of attack
            threat_level: Severity of the threat
            details: Additional details about the attack
            blocked: Whether the attack was blocked
            
        Returns:
            The created AttackEvent
        """
        event = AttackEvent(
            timestamp=time.time(),
            entity_id=entity_id,
            attack_type=attack_type,
            threat_level=threat_level,
            details=details,
            blocked=blocked
        )
        
        self.events.append(event)
        self.attack_counts[attack_type.value] += 1
        
        # Trim events if exceeding max
        if len(self.events) > self.max_events:
            self.events = self.events[-self.max_events:]
        
        # Persist to file
        self.save_log()
        
        return event
    
    def save_log(self) -> None:
        """Save attack log to file."""
        try:
            with open(self.log_file, 'w') as f:
                json.dump({
                    "events": [event.to_dict() for event in self.events[-1000:]],  # Save last 1000
                    "attack_counts": dict(self.attack_counts),
                    "last_updated": datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            print(f"[ATTACK_LOGGER] Error saving log: {e}")
    
    def load_log(self) -> None:
        """Load attack log from file."""
        try:
            with open(self.log_file, 'r') as f:
                data = json.load(f)
                
                # Reconstruct events
                for event_data in data.get("events", []):
                    event = AttackEvent(
                        timestamp=event_data["timestamp"],
                        entity_id=event_data["entity_id"],
                        attack_type=AttackType(event_data["attack_type"]),
                        threat_level=ThreatLevel[event_data["threat_level"]],
                        details=event_data["details"],
                        blocked=event_data["blocked"]
                    )
                    self.events.append(event)
                
                # Restore counts
                self.attack_counts = defaultdict(int, data.get("attack_counts", {}))
        except FileNotFoundError:
            pass  # No existing log
        except Exception as e:
            print(f"[ATTACK_LOGGER] Error loading log: {e}")
    
    def get_recent_attacks(self, count: int = 100) -> List[Dict]:
        """Get recent attack events."""
        return [event.to_dict() for event in self.events[-count:]]
    
    def get_attacks_by_entity(self, entity_id: str) -> List[Dict]:
        """Get all attacks by a specific entity."""
        return [
            event.to_dict() for event in self.events
            if event.entity_id == entity_id
        ]
    
    def get_analytics(self) -> Dict:
        """Get attack analytics."""
        if not self.events:
            return {
                "total_attacks": 0,
                "blocked_attacks": 0,
                "by_type": {},
                "by_threat_level": {},
                "top_attackers": []
            }
        
        blocked = sum(1 for e in self.events if e.blocked)
        
        by_threat_level = defaultdict(int)
        for event in self.events:
            by_threat_level[event.threat_level.name] += 1
        
        # Top attackers
        attacker_counts = defaultdict(int)
        for event in self.events:
            attacker_counts[event.entity_id] += 1
        
        top_attackers = sorted(
            attacker_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        return {
            "total_attacks": len(self.events),
            "blocked_attacks": blocked,
            "block_rate": blocked / len(self.events) if self.events else 0,
            "by_type": dict(self.attack_counts),
            "by_threat_level": dict(by_threat_level),
            "top_attackers": [
                {"entity_id": entity_id, "attack_count": count}
                for entity_id, count in top_attackers
            ]
        }


class ScanDetector:
    """
    Detects silent scans and reconnaissance attempts.
    
    Features:
    - Pattern detection for scanning behavior
    - Rate limiting and throttling
    - Honeypot/trap mechanisms
    """
    
    def __init__(self, 
                 scan_threshold: int = 10,
                 time_window: int = 60,
                 honeypot_paths: Optional[Set[str]] = None):
        """
        Initialize scan detector.
        
        Args:
            scan_threshold: Number of different resources accessed before flagging
            time_window: Time window in seconds for scan detection
            honeypot_paths: Set of honeypot paths that should trigger alerts
        """
        self.scan_threshold = scan_threshold
        self.time_window = time_window
        self.honeypot_paths = honeypot_paths or {
            "/admin", "/.env", "/config", "/backup", 
            "/.git/config", "/wp-admin", "/phpmyadmin"
        }
        self.access_patterns: Dict[str, List[Tuple[float, str]]] = defaultdict(list)
        self.honeypot_triggers: Dict[str, int] = defaultdict(int)
    
    def record_access(self, entity_id: str, resource_path: str) -> None:
        """
        Record a resource access.
        
        Args:
            entity_id: Identifier of the entity
            resource_path: Path of the accessed resource
        """
        current_time = time.time()
        self.access_patterns[entity_id].append((current_time, resource_path))
        
        # Clean up old accesses
        cutoff_time = current_time - self.time_window
        self.access_patterns[entity_id] = [
            (t, path) for t, path in self.access_patterns[entity_id]
            if t > cutoff_time
        ]
    
    def check_honeypot_access(self, entity_id: str, resource_path: str) -> bool:
        """
        Check if accessing a honeypot path.
        
        Args:
            entity_id: Identifier of the entity
            resource_path: Path being accessed
            
        Returns:
            True if honeypot accessed, False otherwise
        """
        if resource_path in self.honeypot_paths:
            self.honeypot_triggers[entity_id] += 1
            return True
        return False
    
    def detect_scan_pattern(self, entity_id: str) -> Tuple[bool, Dict]:
        """
        Detect if entity is performing a scan.
        
        Args:
            entity_id: Identifier of the entity
            
        Returns:
            Tuple of (is_scanning, scan_details)
        """
        if entity_id not in self.access_patterns:
            return False, {}
        
        accesses = self.access_patterns[entity_id]
        
        if len(accesses) < self.scan_threshold:
            return False, {}
        
        # Count unique resources accessed
        unique_resources = set(path for _, path in accesses)
        
        # Calculate access rate
        if len(accesses) >= 2:
            time_span = accesses[-1][0] - accesses[0][0]
            access_rate = len(accesses) / max(time_span, 1)
        else:
            access_rate = 0
        
        # Detect scanning patterns
        is_scanning = (
            len(unique_resources) >= self.scan_threshold or
            access_rate > 2.0 or  # More than 2 requests per second
            self.honeypot_triggers.get(entity_id, 0) > 0
        )
        
        scan_details = {
            "unique_resources": len(unique_resources),
            "total_accesses": len(accesses),
            "access_rate": access_rate,
            "honeypot_triggers": self.honeypot_triggers.get(entity_id, 0),
            "time_window": self.time_window
        }
        
        return is_scanning, scan_details
    
    def apply_rate_limit(self, entity_id: str) -> bool:
        """
        Apply rate limiting based on access patterns.
        
        Args:
            entity_id: Identifier of the entity
            
        Returns:
            True if rate limit should be applied, False otherwise
        """
        if entity_id not in self.access_patterns:
            return False
        
        accesses = self.access_patterns[entity_id]
        
        if len(accesses) < 2:
            return False
        
        # Check recent access rate (last 10 seconds)
        current_time = time.time()
        recent_cutoff = current_time - 10
        recent_accesses = [t for t, _ in accesses if t > recent_cutoff]
        
        # Rate limit if more than 20 requests in 10 seconds
        return len(recent_accesses) > 20
    
    def get_scan_statistics(self) -> Dict:
        """Get scan detection statistics."""
        return {
            "monitored_entities": len(self.access_patterns),
            "total_honeypot_triggers": sum(self.honeypot_triggers.values()),
            "entities_with_honeypot_triggers": len(self.honeypot_triggers),
            "honeypot_paths": list(self.honeypot_paths)
        }


class SecurityFramework:
    """
    Integrated security framework combining all security components.
    
    Provides unified interface for:
    - Threat detection and blocking
    - Attack logging
    - Scan detection and prevention
    """
    
    def __init__(self,
                 log_file: str = "attack_log.json",
                 max_requests_per_minute: int = 60,
                 blacklist_duration: int = 3600):
        """
        Initialize security framework.
        
        Args:
            log_file: Path to attack log file
            max_requests_per_minute: Maximum allowed requests per minute
            blacklist_duration: Default blacklist duration in seconds
        """
        self.threat_detector = ThreatDetector(
            max_requests_per_minute=max_requests_per_minute,
            blacklist_duration=blacklist_duration
        )
        self.attack_logger = AttackLogger(log_file=log_file)
        self.scan_detector = ScanDetector()
        self.enabled = True
    
    def process_request(self, entity_id: str, resource_path: str = "/", 
                       behavior: Optional[Dict] = None) -> Tuple[bool, str]:
        """
        Process a request through the security framework.
        
        Args:
            entity_id: Identifier of the entity making the request
            resource_path: Path of the resource being accessed
            behavior: Optional behavior data for anomaly detection
            
        Returns:
            Tuple of (allowed, reason)
        """
        if not self.enabled:
            return True, "Security framework disabled"
        
        # Check blacklist
        if self.threat_detector.is_blacklisted(entity_id):
            self.attack_logger.log_attack(
                entity_id=entity_id,
                attack_type=AttackType.UNAUTHORIZED_ACCESS,
                threat_level=ThreatLevel.HIGH,
                details={"reason": "blacklisted", "resource": resource_path},
                blocked=True
            )
            return False, "Entity is blacklisted"
        
        # Record access for scan detection
        self.scan_detector.record_access(entity_id, resource_path)
        
        # Check honeypot
        if self.scan_detector.check_honeypot_access(entity_id, resource_path):
            self.threat_detector.add_to_blacklist(
                entity_id=entity_id,
                threat_level=ThreatLevel.CRITICAL,
                reason="Honeypot access"
            )
            self.attack_logger.log_attack(
                entity_id=entity_id,
                attack_type=AttackType.SILENT_SCAN,
                threat_level=ThreatLevel.CRITICAL,
                details={"honeypot_path": resource_path},
                blocked=True
            )
            return False, "Honeypot access detected"
        
        # Check rate limit
        if self.threat_detector.detect_rate_limit_violation(entity_id):
            self.threat_detector.add_to_blacklist(
                entity_id=entity_id,
                threat_level=ThreatLevel.MEDIUM,
                reason="Rate limit exceeded",
                duration=300  # 5 minutes
            )
            self.attack_logger.log_attack(
                entity_id=entity_id,
                attack_type=AttackType.DOS,
                threat_level=ThreatLevel.MEDIUM,
                details={"reason": "rate_limit"},
                blocked=True
            )
            return False, "Rate limit exceeded"
        
        # Check for scan patterns
        is_scanning, scan_details = self.scan_detector.detect_scan_pattern(entity_id)
        if is_scanning:
            self.threat_detector.add_to_blacklist(
                entity_id=entity_id,
                threat_level=ThreatLevel.HIGH,
                reason="Scanning detected",
                duration=1800  # 30 minutes
            )
            self.attack_logger.log_attack(
                entity_id=entity_id,
                attack_type=AttackType.SILENT_SCAN,
                threat_level=ThreatLevel.HIGH,
                details=scan_details,
                blocked=True
            )
            return False, "Scanning behavior detected"
        
        # Check for anomalies if behavior data provided
        if behavior:
            is_anomalous, anomaly_score = self.threat_detector.detect_anomaly(
                entity_id, behavior
            )
            if is_anomalous:
                self.attack_logger.log_attack(
                    entity_id=entity_id,
                    attack_type=AttackType.ANOMALY,
                    threat_level=ThreatLevel.MEDIUM,
                    details={"anomaly_score": anomaly_score, "behavior": behavior},
                    blocked=False
                )
                # Don't block on first anomaly, just log
        
        # Apply rate limiting if needed
        if self.scan_detector.apply_rate_limit(entity_id):
            return False, "Rate limited - too many requests"
        
        return True, "Allowed"
    
    def get_security_status(self) -> Dict:
        """Get comprehensive security status."""
        return {
            "enabled": self.enabled,
            "blacklist": self.threat_detector.get_blacklist_status(),
            "attack_analytics": self.attack_logger.get_analytics(),
            "scan_statistics": self.scan_detector.get_scan_statistics(),
            "timestamp": datetime.now().isoformat()
        }
    
    def cleanup(self) -> None:
        """Perform cleanup operations."""
        expired = self.threat_detector.cleanup_expired()
        if expired > 0:
            print(f"[SECURITY] Cleaned up {expired} expired blacklist entries")


# Main entry point for testing
if __name__ == "__main__":
    print("=" * 70)
    print("SECURITY FRAMEWORK - AI System")
    print("Advanced Blacklisting & Meta-Management")
    print("=" * 70)
    print()
    
    # Initialize framework
    security = SecurityFramework()
    
    # Simulate some requests
    test_entities = ["entity_001", "entity_002", "scanner_001"]
    
    print("Testing security framework...")
    
    # Normal request
    allowed, reason = security.process_request("entity_001", "/api/status")
    print(f"Request 1: {allowed} - {reason}")
    
    # Honeypot access
    allowed, reason = security.process_request("scanner_001", "/.env")
    print(f"Honeypot test: {allowed} - {reason}")
    
    # Rate limit test
    for i in range(70):
        security.process_request("entity_002", f"/api/data/{i}")
    allowed, reason = security.process_request("entity_002", "/api/data")
    print(f"Rate limit test: {allowed} - {reason}")
    
    # Get status
    status = security.get_security_status()
    print(f"\nSecurity Status:")
    print(f"- Blacklisted entities: {status['blacklist']['total_entries']}")
    print(f"- Total attacks logged: {status['attack_analytics']['total_attacks']}")
    print(f"- Blocked attacks: {status['attack_analytics']['blocked_attacks']}")
    print(f"- Honeypot triggers: {status['scan_statistics']['total_honeypot_triggers']}")
