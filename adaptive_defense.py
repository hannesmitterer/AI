#!/usr/bin/env python3
"""
Adaptive Defense Module - Attack Defense and Blacklist Management
=================================================================

This module implements adaptive algorithms for attack defense,
including blacklist management, attack pattern detection, and
adaptive response mechanisms.

Features:
- Dynamic blacklist management
- Attack pattern detection and learning
- Adaptive response strategies
- Integration with security monitoring
- Real-time threat assessment

Part of: Blacklist Defense Strategies and Meta-Management
"""

import time
import hashlib
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict
from enum import Enum


class ThreatLevel(Enum):
    """Threat level classifications."""
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class DefenseAction(Enum):
    """Possible defense actions."""
    ALLOW = "allow"
    MONITOR = "monitor"
    THROTTLE = "throttle"
    BLOCK = "block"
    BLACKLIST = "blacklist"


@dataclass
class BlacklistEntry:
    """Represents an entry in the blacklist."""
    identifier: str  # IP, token, user ID, etc.
    entry_type: str  # "ip", "token", "user", etc.
    reason: str
    timestamp: float
    threat_level: ThreatLevel
    expires_at: Optional[float] = None
    metadata: Dict = field(default_factory=dict)
    
    def is_expired(self) -> bool:
        """Check if entry has expired."""
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "identifier": self.identifier,
            "entry_type": self.entry_type,
            "reason": self.reason,
            "timestamp": self.timestamp,
            "datetime": datetime.fromtimestamp(self.timestamp).isoformat(),
            "threat_level": self.threat_level.name,
            "expires_at": self.expires_at,
            "metadata": self.metadata
        }


@dataclass
class AttackPattern:
    """Represents a detected attack pattern."""
    pattern_id: str
    pattern_type: str
    indicators: List[str]
    detection_count: int = 0
    first_detected: float = field(default_factory=time.time)
    last_detected: float = field(default_factory=time.time)
    confidence: float = 0.0  # 0.0 to 1.0
    
    def update_detection(self) -> None:
        """Update detection statistics."""
        self.detection_count += 1
        self.last_detected = time.time()
        # Increase confidence with repeated detections
        self.confidence = min(1.0, self.confidence + 0.1)


class AdaptiveDefenseEngine:
    """
    Adaptive defense system with intelligent attack detection
    and response mechanisms.
    """
    
    def __init__(self):
        """Initialize adaptive defense engine."""
        self.blacklist: Dict[str, BlacklistEntry] = {}
        self.attack_patterns: Dict[str, AttackPattern] = {}
        self.threat_scores: Dict[str, float] = defaultdict(float)
        self.request_history: Dict[str, List[float]] = defaultdict(list)
        self.defense_statistics: Dict[str, int] = {
            "total_requests": 0,
            "blocked_requests": 0,
            "blacklisted_entities": 0,
            "detected_patterns": 0,
            "adaptive_responses": 0
        }
        
        # Configuration
        self.rate_limit_window = 60.0  # seconds
        self.rate_limit_threshold = 100  # requests per window
        self.threat_score_threshold = 0.7
        self.pattern_confidence_threshold = 0.5
        
        print(f"[ADAPTIVE DEFENSE] Initialized")
        print(f"[ADAPTIVE DEFENSE] Rate limit: {self.rate_limit_threshold} req/{self.rate_limit_window}s")
    
    def check_blacklist(self, identifier: str, entry_type: str) -> Tuple[bool, Optional[BlacklistEntry]]:
        """
        Check if identifier is blacklisted.
        
        Args:
            identifier: Identifier to check
            entry_type: Type of identifier
        
        Returns:
            Tuple of (is_blacklisted, entry)
        """
        key = f"{entry_type}:{identifier}"
        
        if key in self.blacklist:
            entry = self.blacklist[key]
            
            # Check if expired
            if entry.is_expired():
                self._remove_from_blacklist(key)
                return False, None
            
            return True, entry
        
        return False, None
    
    def add_to_blacklist(self, identifier: str, entry_type: str,
                        reason: str, threat_level: ThreatLevel,
                        duration: Optional[float] = None,
                        metadata: Optional[Dict] = None) -> BlacklistEntry:
        """
        Add an entry to the blacklist.
        
        Args:
            identifier: Identifier to blacklist
            entry_type: Type of identifier
            reason: Reason for blacklisting
            threat_level: Threat level
            duration: Optional duration in seconds (None = permanent)
            metadata: Optional metadata
        
        Returns:
            BlacklistEntry object
        """
        key = f"{entry_type}:{identifier}"
        timestamp = time.time()
        expires_at = timestamp + duration if duration else None
        
        entry = BlacklistEntry(
            identifier=identifier,
            entry_type=entry_type,
            reason=reason,
            timestamp=timestamp,
            threat_level=threat_level,
            expires_at=expires_at,
            metadata=metadata or {}
        )
        
        self.blacklist[key] = entry
        self.defense_statistics["blacklisted_entities"] += 1
        
        print(f"[BLACKLIST] Added {entry_type}:{identifier} - {reason} (threat: {threat_level.name})")
        
        return entry
    
    def detect_rate_limiting_attack(self, identifier: str) -> bool:
        """
        Detect if identifier is performing rate limiting attack.
        
        Args:
            identifier: Identifier to check
        
        Returns:
            True if attack detected
        """
        current_time = time.time()
        
        # Add current request
        self.request_history[identifier].append(current_time)
        
        # Clean old requests outside window
        cutoff_time = current_time - self.rate_limit_window
        self.request_history[identifier] = [
            t for t in self.request_history[identifier] 
            if t > cutoff_time
        ]
        
        # Check if threshold exceeded
        request_count = len(self.request_history[identifier])
        
        if request_count > self.rate_limit_threshold:
            print(f"[ATTACK DETECTED] Rate limiting attack from {identifier}: {request_count} requests")
            return True
        
        return False
    
    def detect_attack_pattern(self, request_data: Dict) -> Optional[AttackPattern]:
        """
        Detect known attack patterns in request data.
        
        Args:
            request_data: Request data to analyze
        
        Returns:
            AttackPattern if detected, None otherwise
        """
        patterns_to_check = [
            ("sql_injection", ["'", "OR", "1=1", "DROP", "SELECT", "--"]),
            ("xss_attack", ["<script>", "javascript:", "onerror=", "onclick="]),
            ("path_traversal", ["../", "..\\", "/etc/passwd", "C:\\"]),
            ("command_injection", [";", "&&", "||", "|", "`", "$("])
        ]
        
        # Check request content for patterns
        request_str = str(request_data).lower()
        
        for pattern_type, indicators in patterns_to_check:
            matches = sum(1 for indicator in indicators if indicator.lower() in request_str)
            
            if matches >= 2:  # At least 2 indicators found
                pattern_id = hashlib.sha256(f"{pattern_type}:{time.time()}".encode()).hexdigest()[:16]
                
                if pattern_type not in self.attack_patterns:
                    pattern = AttackPattern(
                        pattern_id=pattern_id,
                        pattern_type=pattern_type,
                        indicators=indicators,
                        confidence=matches / len(indicators)
                    )
                    self.attack_patterns[pattern_type] = pattern
                    self.defense_statistics["detected_patterns"] += 1
                else:
                    pattern = self.attack_patterns[pattern_type]
                    pattern.update_detection()
                
                print(f"[PATTERN DETECTED] {pattern_type} attack pattern (confidence: {pattern.confidence:.2f})")
                return pattern
        
        return None
    
    def calculate_threat_score(self, identifier: str, 
                              request_data: Dict) -> float:
        """
        Calculate adaptive threat score for an identifier.
        
        Args:
            identifier: Identifier to assess
            request_data: Request data
        
        Returns:
            Threat score (0.0 to 1.0)
        """
        score = 0.0
        
        # Check blacklist status
        is_blacklisted, _ = self.check_blacklist(identifier, "entity")
        if is_blacklisted:
            score += 1.0
            return min(1.0, score)
        
        # Check rate limiting
        if self.detect_rate_limiting_attack(identifier):
            score += 0.4
        
        # Check attack patterns
        pattern = self.detect_attack_pattern(request_data)
        if pattern:
            score += pattern.confidence * 0.5
        
        # Historical threat score (decay over time)
        if identifier in self.threat_scores:
            historical_score = self.threat_scores[identifier]
            # Decay by 10% per calculation
            historical_score *= 0.9
            score = max(score, historical_score)
        
        # Update threat score
        self.threat_scores[identifier] = min(1.0, score)
        
        return self.threat_scores[identifier]
    
    def determine_defense_action(self, identifier: str,
                                 threat_score: float,
                                 request_data: Dict) -> DefenseAction:
        """
        Determine appropriate defense action based on threat assessment.
        
        Args:
            identifier: Identifier being assessed
            threat_score: Calculated threat score
            request_data: Request data
        
        Returns:
            DefenseAction to take
        """
        # Check blacklist first
        is_blacklisted, entry = self.check_blacklist(identifier, "entity")
        if is_blacklisted:
            return DefenseAction.BLOCK
        
        # Adaptive response based on threat score
        if threat_score >= 0.9:
            # Very high threat - blacklist
            self.add_to_blacklist(
                identifier=identifier,
                entry_type="entity",
                reason="Adaptive defense - high threat score",
                threat_level=ThreatLevel.CRITICAL,
                duration=3600.0,  # 1 hour
                metadata={"threat_score": threat_score}
            )
            self.defense_statistics["adaptive_responses"] += 1
            return DefenseAction.BLACKLIST
        
        elif threat_score >= 0.7:
            # High threat - block
            return DefenseAction.BLOCK
        
        elif threat_score >= 0.5:
            # Medium threat - throttle
            return DefenseAction.THROTTLE
        
        elif threat_score >= 0.3:
            # Low threat - monitor
            return DefenseAction.MONITOR
        
        else:
            # No threat - allow
            return DefenseAction.ALLOW
    
    def process_request(self, identifier: str, 
                       request_data: Dict) -> Tuple[DefenseAction, Dict]:
        """
        Process a request through the adaptive defense system.
        
        Args:
            identifier: Request identifier
            request_data: Request data
        
        Returns:
            Tuple of (action, metadata)
        """
        self.defense_statistics["total_requests"] += 1
        
        # Calculate threat score
        threat_score = self.calculate_threat_score(identifier, request_data)
        
        # Determine action
        action = self.determine_defense_action(identifier, threat_score, request_data)
        
        # Update statistics
        if action in [DefenseAction.BLOCK, DefenseAction.BLACKLIST]:
            self.defense_statistics["blocked_requests"] += 1
        
        # Prepare metadata
        metadata = {
            "threat_score": threat_score,
            "timestamp": time.time(),
            "identifier": identifier
        }
        
        if action != DefenseAction.ALLOW:
            print(f"[DEFENSE] {action.value.upper()} - {identifier} (threat: {threat_score:.2f})")
        
        return action, metadata
    
    def cleanup_expired_entries(self) -> int:
        """
        Remove expired blacklist entries.
        
        Returns:
            Number of entries removed
        """
        expired_keys = [
            key for key, entry in self.blacklist.items()
            if entry.is_expired()
        ]
        
        for key in expired_keys:
            self._remove_from_blacklist(key)
        
        if expired_keys:
            print(f"[CLEANUP] Removed {len(expired_keys)} expired blacklist entries")
        
        return len(expired_keys)
    
    def get_statistics(self) -> Dict:
        """Get defense statistics."""
        return {
            "total_requests": self.defense_statistics["total_requests"],
            "blocked_requests": self.defense_statistics["blocked_requests"],
            "block_rate": (self.defense_statistics["blocked_requests"] / 
                          max(1, self.defense_statistics["total_requests"])),
            "blacklisted_entities": len(self.blacklist),
            "detected_patterns": len(self.attack_patterns),
            "adaptive_responses": self.defense_statistics["adaptive_responses"],
            "tracked_identifiers": len(self.threat_scores)
        }
    
    def get_blacklist_entries(self) -> List[BlacklistEntry]:
        """Get all current blacklist entries."""
        return [entry for entry in self.blacklist.values() if not entry.is_expired()]
    
    def get_attack_patterns(self) -> List[AttackPattern]:
        """Get all detected attack patterns."""
        return list(self.attack_patterns.values())
    
    def _remove_from_blacklist(self, key: str) -> None:
        """Remove entry from blacklist."""
        if key in self.blacklist:
            del self.blacklist[key]


def main():
    """Demo of adaptive defense system."""
    print("="*70)
    print("ADAPTIVE DEFENSE SYSTEM - DEMO")
    print("="*70)
    print()
    
    # Initialize defense engine
    defense = AdaptiveDefenseEngine()
    
    # Simulate various requests
    print("\n--- Simulating normal request ---")
    action, meta = defense.process_request(
        "user_123",
        {"endpoint": "/api/data", "method": "GET"}
    )
    print(f"Action: {action.value}, Threat: {meta['threat_score']:.2f}")
    
    print("\n--- Simulating SQL injection attempt ---")
    action, meta = defense.process_request(
        "user_456",
        {"endpoint": "/api/search", "query": "' OR 1=1 --", "method": "POST"}
    )
    print(f"Action: {action.value}, Threat: {meta['threat_score']:.2f}")
    
    print("\n--- Simulating rate limiting attack ---")
    for i in range(120):
        action, meta = defense.process_request(
            "attacker_789",
            {"endpoint": "/api/login", "method": "POST"}
        )
    print(f"Final Action: {action.value}, Threat: {meta['threat_score']:.2f}")
    
    print("\n--- Adding manual blacklist entry ---")
    defense.add_to_blacklist(
        identifier="192.168.1.100",
        entry_type="ip",
        reason="Manual blacklist - suspicious activity",
        threat_level=ThreatLevel.HIGH,
        duration=300.0
    )
    
    # Check blacklist
    print("\n--- Checking blacklist ---")
    is_blocked, entry = defense.check_blacklist("192.168.1.100", "ip")
    print(f"IP 192.168.1.100 blocked: {is_blocked}")
    
    # Get statistics
    print("\n--- Defense Statistics ---")
    stats = defense.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n--- Attack Patterns Detected ---")
    patterns = defense.get_attack_patterns()
    for pattern in patterns:
        print(f"  {pattern.pattern_type}: confidence={pattern.confidence:.2f}, "
              f"detections={pattern.detection_count}")


if __name__ == "__main__":
    main()
