#!/usr/bin/env python3
"""
AI Security Interface - Universal Blacklist & Threat Management
================================================================

This module implements security features for AI interfaces with focus on:
1. Protokollierung adaptiver Bedrohungen (Adaptive Threat Logging)
2. Optimierte Log-Befüllung (Optimized Log Population)
3. Fortschrittliches Firewall-Design (Progressive Firewall Design)

Based on: Kosymbiosis security principles and eternal deposition integration
"""

import time
import json
import hashlib
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum


# Blacklist expiry constants (in hours)
DEFAULT_HIGH_THREAT_EXPIRY_HOURS = 48
DEFAULT_MEDIUM_THREAT_EXPIRY_HOURS = 24


class ThreatLevel(Enum):
    """Threat severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ThreatType(Enum):
    """Types of adaptive threats."""
    MALICIOUS_INPUT = "malicious_input"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    PATTERN_ANOMALY = "pattern_anomaly"
    RESOURCE_ABUSE = "resource_abuse"
    DATA_EXFILTRATION = "data_exfiltration"
    INJECTION_ATTEMPT = "injection_attempt"


@dataclass
class ThreatLog:
    """
    Einzelner Bedrohungseintrag im adaptiven Log-System.
    (Single threat entry in adaptive logging system)
    """
    timestamp: str
    threat_id: str
    threat_type: ThreatType
    threat_level: ThreatLevel
    source_identifier: str
    description: str
    metadata: Dict = field(default_factory=dict)
    adaptive_score: float = 0.0
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "timestamp": self.timestamp,
            "threat_id": self.threat_id,
            "threat_type": self.threat_type.value,
            "threat_level": self.threat_level.value,
            "source_identifier": self.source_identifier,
            "description": self.description,
            "metadata": self.metadata,
            "adaptive_score": self.adaptive_score
        }


@dataclass
class BlacklistEntry:
    """Entry in the universal blacklist."""
    identifier: str
    reason: str
    threat_level: ThreatLevel
    first_seen: str
    last_seen: str
    occurrence_count: int = 1
    is_permanent: bool = False
    expiry_timestamp: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "identifier": self.identifier,
            "reason": self.reason,
            "threat_level": self.threat_level.value,
            "first_seen": self.first_seen,
            "last_seen": self.last_seen,
            "occurrence_count": self.occurrence_count,
            "is_permanent": self.is_permanent,
            "expiry_timestamp": self.expiry_timestamp
        }


class AdaptiveThreatLogger:
    """
    Schritt 1: Protokollierung adaptiver Bedrohungen
    (Step 1: Logging of Adaptive Threats)
    
    Implements adaptive threat detection and logging with learning capabilities.
    """
    
    def __init__(self, max_logs: int = 10000):
        """
        Initialize adaptive threat logger.
        
        Args:
            max_logs: Maximum number of logs to retain
        """
        self.threat_logs: List[ThreatLog] = []
        self.max_logs = max_logs
        self.threat_patterns: Dict[str, int] = {}
        self.adaptive_thresholds: Dict[ThreatType, float] = {
            threat_type: 0.5 for threat_type in ThreatType
        }
        
        print(f"[ADAPTIVE LOGGER] Initialized with capacity: {max_logs}")
    
    def log_threat(self, 
                   threat_type: ThreatType,
                   threat_level: ThreatLevel,
                   source_identifier: str,
                   description: str,
                   metadata: Optional[Dict] = None) -> str:
        """
        Log a detected threat with adaptive scoring.
        
        Args:
            threat_type: Type of threat
            threat_level: Severity level
            source_identifier: Source of the threat
            description: Human-readable description
            metadata: Additional context
            
        Returns:
            Unique threat ID
        """
        timestamp = datetime.now().isoformat()
        
        # Generate unique threat ID
        threat_id = hashlib.sha256(
            f"{timestamp}{source_identifier}{threat_type.value}".encode()
        ).hexdigest()[:16]
        
        # Calculate adaptive score based on historical patterns
        adaptive_score = self._calculate_adaptive_score(
            threat_type, source_identifier
        )
        
        # Create threat log entry
        threat_log = ThreatLog(
            timestamp=timestamp,
            threat_id=threat_id,
            threat_type=threat_type,
            threat_level=threat_level,
            source_identifier=source_identifier,
            description=description,
            metadata=metadata or {},
            adaptive_score=adaptive_score
        )
        
        # Add to logs
        self.threat_logs.append(threat_log)
        
        # Optimize log storage (automatic pruning)
        self._optimize_logs()
        
        # Update threat patterns for adaptive learning
        self._update_patterns(threat_type, source_identifier)
        
        print(f"[THREAT LOGGED] {threat_id} | {threat_type.value} | "
              f"Level: {threat_level.value} | Score: {adaptive_score:.3f}")
        
        return threat_id
    
    def _calculate_adaptive_score(self, 
                                  threat_type: ThreatType, 
                                  source: str) -> float:
        """
        Calculate adaptive threat score based on historical patterns.
        
        Higher scores indicate more dangerous patterns.
        """
        pattern_key = f"{threat_type.value}:{source}"
        
        # Base score from threat level threshold
        base_score = self.adaptive_thresholds.get(threat_type, 0.5)
        
        # Increase score if pattern is repeated
        pattern_count = self.threat_patterns.get(pattern_key, 0)
        pattern_multiplier = min(2.0, 1.0 + (pattern_count * 0.1))
        
        adaptive_score = min(1.0, base_score * pattern_multiplier)
        
        return adaptive_score
    
    def _update_patterns(self, threat_type: ThreatType, source: str) -> None:
        """Update threat pattern tracking for adaptive learning."""
        pattern_key = f"{threat_type.value}:{source}"
        self.threat_patterns[pattern_key] = self.threat_patterns.get(pattern_key, 0) + 1
        
        # Adaptively adjust threshold if pattern becomes common
        if self.threat_patterns[pattern_key] > 5:
            current_threshold = self.adaptive_thresholds[threat_type]
            self.adaptive_thresholds[threat_type] = min(1.0, current_threshold * 1.05)
    
    def _optimize_logs(self) -> None:
        """
        Schritt 2: Optimierte Log-Befüllung (Part of optimized log population)
        
        Automatically prune old logs when capacity is reached.
        Keeps highest priority threats.
        """
        if len(self.threat_logs) > self.max_logs:
            # Sort by adaptive score and timestamp
            self.threat_logs.sort(
                key=lambda x: (x.adaptive_score, x.timestamp),
                reverse=True
            )
            # Keep top max_logs entries
            self.threat_logs = self.threat_logs[:self.max_logs]
            
            print(f"[LOG OPTIMIZATION] Pruned to {self.max_logs} entries")
    
    def get_recent_threats(self, count: int = 10) -> List[ThreatLog]:
        """Get most recent threats."""
        return sorted(self.threat_logs, key=lambda x: x.timestamp, reverse=True)[:count]
    
    def get_high_priority_threats(self, min_score: float = 0.7) -> List[ThreatLog]:
        """Get threats above adaptive score threshold."""
        return [log for log in self.threat_logs if log.adaptive_score >= min_score]
    
    def export_logs(self, filepath: str = "threat_logs.json") -> None:
        """Export threat logs to file."""
        logs_data = [log.to_dict() for log in self.threat_logs]
        with open(filepath, 'w') as f:
            json.dump(logs_data, f, indent=2)
        print(f"[EXPORT] Saved {len(logs_data)} threat logs to {filepath}")


class OptimizedLogManager:
    """
    Schritt 2: Optimierte Log-Befüllung
    (Step 2: Optimized Log Population)
    
    Manages efficient log storage with intelligent rotation and compression.
    """
    
    def __init__(self, rotation_size: int = 5000, compression_enabled: bool = True):
        """
        Initialize optimized log manager.
        
        Args:
            rotation_size: Size threshold for log rotation
            compression_enabled: Enable log compression for older entries
        """
        self.rotation_size = rotation_size
        self.compression_enabled = compression_enabled
        self.current_logs: List[Dict] = []
        self.archived_logs: List[str] = []
        self.log_statistics: Dict = {
            "total_logs": 0,
            "rotations": 0,
            "compressions": 0
        }
        
        print(f"[LOG MANAGER] Initialized | Rotation: {rotation_size} | "
              f"Compression: {compression_enabled}")
    
    def populate_log(self, log_entry: Dict) -> None:
        """
        Add log entry with optimization.
        
        Automatically handles rotation and compression.
        """
        self.current_logs.append(log_entry)
        self.log_statistics["total_logs"] += 1
        
        # Check if rotation is needed
        if len(self.current_logs) >= self.rotation_size:
            self._rotate_logs()
    
    def _rotate_logs(self) -> None:
        """Rotate current logs to archive."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_file = f"logs_archive_{timestamp}.json"
        
        # Save current logs to archive
        with open(archive_file, 'w') as f:
            json.dump(self.current_logs, f)
        
        self.archived_logs.append(archive_file)
        self.log_statistics["rotations"] += 1
        
        # Clear current logs
        rotated_count = len(self.current_logs)
        self.current_logs = []
        
        print(f"[LOG ROTATION] Archived {rotated_count} logs to {archive_file}")
        
        # Compress if enabled
        if self.compression_enabled:
            self._compress_archive(archive_file)
    
    def _compress_archive(self, filepath: str) -> None:
        """
        Compress archived logs.
        
        Note: Currently a placeholder. In production, this would use gzip or similar
        compression to reduce storage space. The statistics counter is incremented
        for tracking purposes, but actual file compression is not yet implemented.
        """
        # TODO: Implement actual compression using gzip.compress() or similar
        self.log_statistics["compressions"] += 1
        print(f"[LOG COMPRESSION] Marked for compression: {filepath} (not yet compressed)")
    
    def get_statistics(self) -> Dict:
        """Get log management statistics."""
        return {
            "current_logs": len(self.current_logs),
            "archived_files": len(self.archived_logs),
            **self.log_statistics
        }


class ProgressiveFirewall:
    """
    Schritt 3: Fortschrittliches Firewall-Design
    (Step 3: Progressive Firewall Design)
    
    Implements adaptive firewall with universal blacklist and intelligent filtering.
    """
    
    def __init__(self):
        """Initialize progressive firewall."""
        self.blacklist: Dict[str, BlacklistEntry] = {}
        self.whitelist: Set[str] = set()
        self.firewall_rules: List[Dict] = []
        self.blocked_attempts: int = 0
        self.allowed_requests: int = 0
        
        # Initialize default rules
        self._initialize_default_rules()
        
        print("[FIREWALL] Progressive firewall initialized")
    
    def _initialize_default_rules(self) -> None:
        """Initialize default firewall rules."""
        self.firewall_rules = [
            {
                "rule_id": "RULE_001",
                "description": "Block known malicious patterns",
                "action": "block",
                "priority": 1
            },
            {
                "rule_id": "RULE_002",
                "description": "Rate limit suspicious sources",
                "action": "rate_limit",
                "priority": 2
            },
            {
                "rule_id": "RULE_003",
                "description": "Allow whitelisted sources",
                "action": "allow",
                "priority": 0
            }
        ]
    
    def add_to_blacklist(self,
                        identifier: str,
                        reason: str,
                        threat_level: ThreatLevel,
                        is_permanent: bool = False,
                        expiry_hours: Optional[int] = None) -> None:
        """
        Add entry to universal blacklist.
        
        Args:
            identifier: Source identifier to blacklist
            reason: Reason for blacklisting
            threat_level: Severity level
            is_permanent: If True, never expires
            expiry_hours: Hours until expiry (if not permanent)
        """
        timestamp = datetime.now().isoformat()
        
        if identifier in self.blacklist:
            # Update existing entry
            entry = self.blacklist[identifier]
            entry.last_seen = timestamp
            entry.occurrence_count += 1
            print(f"[BLACKLIST] Updated {identifier} | Count: {entry.occurrence_count}")
        else:
            # Create new entry
            expiry_timestamp = None
            if not is_permanent and expiry_hours:
                expiry_time = datetime.now() + timedelta(hours=expiry_hours)
                expiry_timestamp = expiry_time.isoformat()
            
            entry = BlacklistEntry(
                identifier=identifier,
                reason=reason,
                threat_level=threat_level,
                first_seen=timestamp,
                last_seen=timestamp,
                is_permanent=is_permanent,
                expiry_timestamp=expiry_timestamp
            )
            
            self.blacklist[identifier] = entry
            print(f"[BLACKLIST] Added {identifier} | Reason: {reason} | "
                  f"Permanent: {is_permanent}")
    
    def remove_from_blacklist(self, identifier: str) -> bool:
        """Remove entry from blacklist."""
        if identifier in self.blacklist:
            del self.blacklist[identifier]
            print(f"[BLACKLIST] Removed {identifier}")
            return True
        return False
    
    def add_to_whitelist(self, identifier: str) -> None:
        """Add trusted source to whitelist."""
        self.whitelist.add(identifier)
        print(f"[WHITELIST] Added {identifier}")
    
    def check_access(self, source_identifier: str) -> Tuple[bool, str]:
        """
        Check if access should be allowed.
        
        Args:
            source_identifier: Source to check
            
        Returns:
            Tuple of (allowed: bool, reason: str)
        """
        # Whitelist has highest priority
        if source_identifier in self.whitelist:
            self.allowed_requests += 1
            return True, "Whitelisted source"
        
        # Check blacklist
        if source_identifier in self.blacklist:
            entry = self.blacklist[source_identifier]
            
            # Check if entry has expired
            if not entry.is_permanent and entry.expiry_timestamp:
                try:
                    expiry = datetime.fromisoformat(entry.expiry_timestamp)
                    if datetime.now() > expiry:
                        # Entry expired, remove and allow
                        self.remove_from_blacklist(source_identifier)
                        self.allowed_requests += 1
                        return True, "Blacklist entry expired"
                except (ValueError, TypeError):
                    # Invalid timestamp format, entry remains active
                    pass
            
            # Active blacklist entry
            self.blocked_attempts += 1
            return False, f"Blacklisted: {entry.reason}"
        
        # Default allow (progressive approach)
        self.allowed_requests += 1
        return True, "No matching rule, default allow"
    
    def update_blacklist_from_threats(self, 
                                     threat_logs: List[ThreatLog],
                                     auto_blacklist_threshold: float = 0.8) -> int:
        """
        Update universal blacklist from threat logs.
        
        Args:
            threat_logs: List of threat logs to process
            auto_blacklist_threshold: Adaptive score threshold for auto-blacklist
            
        Returns:
            Number of new blacklist entries added
        """
        added_count = 0
        
        for threat in threat_logs:
            # Auto-blacklist high-score threats
            if threat.adaptive_score >= auto_blacklist_threshold:
                if threat.source_identifier not in self.blacklist:
                    # Determine expiry hours based on threat level
                    expiry_hours = None
                    if threat.threat_level == ThreatLevel.HIGH:
                        expiry_hours = DEFAULT_HIGH_THREAT_EXPIRY_HOURS
                    elif threat.threat_level == ThreatLevel.MEDIUM:
                        expiry_hours = DEFAULT_MEDIUM_THREAT_EXPIRY_HOURS
                    
                    self.add_to_blacklist(
                        identifier=threat.source_identifier,
                        reason=f"{threat.threat_type.value}: {threat.description}",
                        threat_level=threat.threat_level,
                        is_permanent=threat.threat_level == ThreatLevel.CRITICAL,
                        expiry_hours=expiry_hours
                    )
                    added_count += 1
        
        if added_count > 0:
            print(f"[BLACKLIST UPDATE] Added {added_count} entries from threat analysis")
        
        return added_count
    
    def export_blacklist(self, filepath: str = "blacklist.json") -> None:
        """Export blacklist to file."""
        blacklist_data = {
            identifier: entry.to_dict() 
            for identifier, entry in self.blacklist.items()
        }
        
        with open(filepath, 'w') as f:
            json.dump(blacklist_data, f, indent=2)
        
        print(f"[EXPORT] Saved {len(blacklist_data)} blacklist entries to {filepath}")
    
    def get_statistics(self) -> Dict:
        """Get firewall statistics."""
        total_requests = self.blocked_attempts + self.allowed_requests
        block_rate = self.blocked_attempts / max(1, total_requests)
        
        return {
            "blacklist_entries": len(self.blacklist),
            "whitelist_entries": len(self.whitelist),
            "blocked_attempts": self.blocked_attempts,
            "allowed_requests": self.allowed_requests,
            "firewall_rules": len(self.firewall_rules),
            "block_rate": block_rate
        }


class AISecurityInterface:
    """
    Unified AI Security Interface integrating all three components.
    
    Combines:
    - Adaptive Threat Logging
    - Optimized Log Management
    - Progressive Firewall
    """
    
    def __init__(self):
        """Initialize AI security interface."""
        self.threat_logger = AdaptiveThreatLogger()
        self.log_manager = OptimizedLogManager()
        self.firewall = ProgressiveFirewall()
        
        print("="*70)
        print("[AI SECURITY] Interface initialized with all components")
        print("="*70)
    
    def process_request(self, source_identifier: str, request_data: Dict) -> Tuple[bool, str]:
        """
        Process incoming request through security pipeline.
        
        Args:
            source_identifier: Source of the request
            request_data: Request data to analyze
            
        Returns:
            Tuple of (allowed: bool, message: str)
        """
        # Step 1: Check firewall
        allowed, reason = self.firewall.check_access(source_identifier)
        
        if not allowed:
            # Log blocked attempt as threat
            self.threat_logger.log_threat(
                threat_type=ThreatType.UNAUTHORIZED_ACCESS,
                threat_level=ThreatLevel.MEDIUM,
                source_identifier=source_identifier,
                description=f"Blocked by firewall: {reason}",
                metadata={"request": request_data}
            )
            
            return False, reason
        
        # Step 2: Analyze request for threats (simplified example)
        # In production, this would include actual threat analysis
        
        return True, "Request allowed"
    
    def detect_and_log_threat(self,
                             threat_type: ThreatType,
                             threat_level: ThreatLevel,
                             source_identifier: str,
                             description: str,
                             auto_blacklist: bool = True) -> str:
        """
        Detect and log a threat, optionally adding to blacklist.
        
        Args:
            threat_type: Type of threat
            threat_level: Severity
            source_identifier: Source
            description: Description
            auto_blacklist: Automatically add to blacklist if high severity
            
        Returns:
            Threat ID
        """
        # Log the threat
        threat_id = self.threat_logger.log_threat(
            threat_type=threat_type,
            threat_level=threat_level,
            source_identifier=source_identifier,
            description=description
        )
        
        # Populate optimized log
        log_entry = {
            "threat_id": threat_id,
            "type": threat_type.value,
            "level": threat_level.value,
            "source": source_identifier,
            "timestamp": datetime.now().isoformat()
        }
        self.log_manager.populate_log(log_entry)
        
        # Auto-blacklist if critical or high
        if auto_blacklist and threat_level in [ThreatLevel.CRITICAL, ThreatLevel.HIGH]:
            self.firewall.add_to_blacklist(
                identifier=source_identifier,
                reason=description,
                threat_level=threat_level,
                is_permanent=(threat_level == ThreatLevel.CRITICAL),
                expiry_hours=48
            )
        
        return threat_id
    
    def synchronize_blacklist(self) -> int:
        """
        Synchronize blacklist with threat logs.
        
        Returns:
            Number of new entries added
        """
        high_priority_threats = self.threat_logger.get_high_priority_threats(min_score=0.7)
        return self.firewall.update_blacklist_from_threats(high_priority_threats)
    
    def get_comprehensive_status(self) -> Dict:
        """Get status from all security components."""
        return {
            "timestamp": datetime.now().isoformat(),
            "threat_logs_count": len(self.threat_logger.threat_logs),
            "log_manager": self.log_manager.get_statistics(),
            "firewall": self.firewall.get_statistics(),
            "recent_threats": len(self.threat_logger.get_recent_threats(10)),
            "high_priority_threats": len(self.threat_logger.get_high_priority_threats())
        }
    
    def export_security_state(self, base_path: str = ".") -> None:
        """Export complete security state."""
        self.threat_logger.export_logs(f"{base_path}/threat_logs.json")
        self.firewall.export_blacklist(f"{base_path}/blacklist.json")
        
        # Export comprehensive status
        status = self.get_comprehensive_status()
        with open(f"{base_path}/security_status.json", 'w') as f:
            json.dump(status, f, indent=2)
        
        print(f"[EXPORT] Complete security state exported to {base_path}/")


def main():
    """Demonstration of AI Security Interface."""
    print("="*70)
    print("AI SECURITY INTERFACE - DEMONSTRATION")
    print("="*70)
    print()
    
    # Initialize interface
    security = AISecurityInterface()
    print()
    
    # Simulate some threats
    print("[DEMO] Simulating threat scenarios...")
    print()
    
    # Scenario 1: Malicious input
    security.detect_and_log_threat(
        threat_type=ThreatType.MALICIOUS_INPUT,
        threat_level=ThreatLevel.HIGH,
        source_identifier="192.168.1.100",
        description="SQL injection attempt detected"
    )
    
    # Scenario 2: Resource abuse
    security.detect_and_log_threat(
        threat_type=ThreatType.RESOURCE_ABUSE,
        threat_level=ThreatLevel.MEDIUM,
        source_identifier="192.168.1.101",
        description="Excessive request rate detected"
    )
    
    # Scenario 3: Critical threat
    security.detect_and_log_threat(
        threat_type=ThreatType.DATA_EXFILTRATION,
        threat_level=ThreatLevel.CRITICAL,
        source_identifier="10.0.0.50",
        description="Attempted unauthorized data access"
    )
    
    print()
    print("[DEMO] Testing firewall access control...")
    print()
    
    # Test access for different sources
    test_sources = ["192.168.1.100", "192.168.1.102", "10.0.0.50"]
    
    for source in test_sources:
        allowed, reason = security.firewall.check_access(source)
        status = "ALLOWED" if allowed else "BLOCKED"
        print(f"  {source}: {status} - {reason}")
    
    print()
    print("[DEMO] Synchronizing blacklist with threat data...")
    added = security.synchronize_blacklist()
    print(f"  Added {added} new blacklist entries")
    print()
    
    # Display comprehensive status
    print("[STATUS] Security Interface Statistics:")
    status = security.get_comprehensive_status()
    print(json.dumps(status, indent=2))
    print()
    
    # Export state
    print("[EXPORT] Exporting security state...")
    security.export_security_state()
    print()
    
    print("="*70)
    print("DEMONSTRATION COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()
