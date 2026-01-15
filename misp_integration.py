#!/usr/bin/env python3
"""
MISP Integration and Token Validation Module
============================================

This module implements token validation integrated with MISP
(Malware Information Sharing Platform) trigger functions for
threat intelligence sharing and coordination.

Features:
- Secure token validation
- MISP event trigger integration
- Threat intelligence sharing
- Coordinated defense response
- Integration with security monitoring and adaptive defense

Part of: Blacklist Defense Strategies and Meta-Management
"""

import time
import hashlib
import hmac
import secrets
import json
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class TokenStatus(Enum):
    """Token validation status."""
    VALID = "valid"
    INVALID = "invalid"
    EXPIRED = "expired"
    REVOKED = "revoked"
    SUSPICIOUS = "suspicious"


class MISPEventType(Enum):
    """MISP event types for threat intelligence."""
    ATTACK_DETECTED = "attack_detected"
    BLACKLIST_UPDATE = "blacklist_update"
    THREAT_INDICATOR = "threat_indicator"
    INCIDENT_RESPONSE = "incident_response"
    VULNERABILITY_ALERT = "vulnerability_alert"


@dataclass
class Token:
    """Represents a security token."""
    token_id: str
    token_hash: str
    created_at: float
    expires_at: Optional[float]
    user_id: str
    permissions: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    revoked: bool = False
    
    def is_expired(self) -> bool:
        """Check if token has expired."""
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at
    
    def is_valid(self) -> bool:
        """Check if token is valid."""
        return not self.revoked and not self.is_expired()
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "token_id": self.token_id,
            "created_at": self.created_at,
            "created_datetime": datetime.fromtimestamp(self.created_at).isoformat(),
            "expires_at": self.expires_at,
            "user_id": self.user_id,
            "permissions": self.permissions,
            "metadata": self.metadata,
            "revoked": self.revoked,
            "valid": self.is_valid()
        }


@dataclass
class MISPEvent:
    """Represents a MISP threat intelligence event."""
    event_id: str
    event_type: MISPEventType
    timestamp: float
    threat_level: str
    description: str
    indicators: List[str] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)
    shared: bool = False
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "timestamp": self.timestamp,
            "datetime": datetime.fromtimestamp(self.timestamp).isoformat(),
            "threat_level": self.threat_level,
            "description": self.description,
            "indicators": self.indicators,
            "attributes": self.attributes,
            "shared": self.shared
        }


class TokenValidator:
    """
    Token validation system with security features.
    """
    
    def __init__(self, secret_key: Optional[str] = None):
        """
        Initialize token validator.
        
        Args:
            secret_key: Secret key for HMAC signing (generated if not provided)
        """
        self.secret_key = secret_key or secrets.token_hex(32)
        self.tokens: Dict[str, Token] = {}
        self.revoked_tokens: set = set()
        self.validation_statistics: Dict[str, int] = {
            "total_validations": 0,
            "valid_tokens": 0,
            "invalid_tokens": 0,
            "expired_tokens": 0,
            "revoked_tokens": 0,
            "suspicious_tokens": 0
        }
        
        print(f"[TOKEN VALIDATOR] Initialized")
    
    def generate_token(self, user_id: str, 
                      permissions: Optional[List[str]] = None,
                      duration: Optional[float] = None,
                      metadata: Optional[Dict] = None) -> Tuple[str, Token]:
        """
        Generate a new security token.
        
        Args:
            user_id: User identifier
            permissions: List of permissions
            duration: Token duration in seconds (None = no expiration)
            metadata: Optional metadata
        
        Returns:
            Tuple of (token_string, Token object)
        """
        # Generate token ID
        token_id = secrets.token_urlsafe(32)
        
        # Create token data
        timestamp = time.time()
        expires_at = timestamp + duration if duration else None
        
        # Generate token string
        token_data = f"{token_id}:{user_id}:{timestamp}"
        token_hash = hmac.new(
            self.secret_key.encode(),
            token_data.encode(),
            hashlib.sha256
        ).hexdigest()
        
        token_string = f"{token_id}.{token_hash}"
        
        # Create token object
        token = Token(
            token_id=token_id,
            token_hash=token_hash,
            created_at=timestamp,
            expires_at=expires_at,
            user_id=user_id,
            permissions=permissions or [],
            metadata=metadata or {}
        )
        
        # Store token
        self.tokens[token_id] = token
        
        print(f"[TOKEN] Generated for user {user_id} (expires: {expires_at or 'never'})")
        
        return token_string, token
    
    def validate_token(self, token_string: str) -> Tuple[TokenStatus, Optional[Token]]:
        """
        Validate a token string.
        
        Args:
            token_string: Token string to validate
        
        Returns:
            Tuple of (TokenStatus, Token object or None)
        """
        self.validation_statistics["total_validations"] += 1
        
        try:
            # Parse token
            parts = token_string.split('.')
            if len(parts) != 2:
                self.validation_statistics["invalid_tokens"] += 1
                return TokenStatus.INVALID, None
            
            token_id, provided_hash = parts
            
            # Check if token exists
            if token_id not in self.tokens:
                self.validation_statistics["invalid_tokens"] += 1
                return TokenStatus.INVALID, None
            
            token = self.tokens[token_id]
            
            # Verify hash
            expected_hash = token.token_hash
            if not hmac.compare_digest(provided_hash, expected_hash):
                self.validation_statistics["invalid_tokens"] += 1
                return TokenStatus.INVALID, None
            
            # Check revocation
            if token.revoked or token_id in self.revoked_tokens:
                self.validation_statistics["revoked_tokens"] += 1
                return TokenStatus.REVOKED, token
            
            # Check expiration
            if token.is_expired():
                self.validation_statistics["expired_tokens"] += 1
                return TokenStatus.EXPIRED, token
            
            # Token is valid
            self.validation_statistics["valid_tokens"] += 1
            return TokenStatus.VALID, token
        
        except Exception as e:
            print(f"[ERROR] Token validation failed: {e}")
            self.validation_statistics["invalid_tokens"] += 1
            return TokenStatus.INVALID, None
    
    def revoke_token(self, token_id: str) -> bool:
        """
        Revoke a token.
        
        Args:
            token_id: Token ID to revoke
        
        Returns:
            True if token was revoked
        """
        if token_id in self.tokens:
            self.tokens[token_id].revoked = True
            self.revoked_tokens.add(token_id)
            print(f"[TOKEN] Revoked token {token_id}")
            return True
        return False
    
    def cleanup_expired_tokens(self) -> int:
        """
        Remove expired tokens from storage.
        
        Returns:
            Number of tokens removed
        """
        expired = [
            token_id for token_id, token in self.tokens.items()
            if token.is_expired()
        ]
        
        for token_id in expired:
            del self.tokens[token_id]
        
        if expired:
            print(f"[CLEANUP] Removed {len(expired)} expired tokens")
        
        return len(expired)
    
    def get_statistics(self) -> Dict:
        """Get validation statistics."""
        return {
            "total_validations": self.validation_statistics["total_validations"],
            "valid_tokens": self.validation_statistics["valid_tokens"],
            "invalid_tokens": self.validation_statistics["invalid_tokens"],
            "expired_tokens": self.validation_statistics["expired_tokens"],
            "revoked_tokens": self.validation_statistics["revoked_tokens"],
            "suspicious_tokens": self.validation_statistics["suspicious_tokens"],
            "active_tokens": len([t for t in self.tokens.values() if t.is_valid()])
        }


class MISPIntegration:
    """
    MISP (Malware Information Sharing Platform) integration
    for threat intelligence sharing and coordination.
    """
    
    def __init__(self):
        """Initialize MISP integration."""
        self.events: Dict[str, MISPEvent] = {}
        self.event_handlers: Dict[MISPEventType, List] = {
            event_type: [] for event_type in MISPEventType
        }
        self.shared_indicators: set = set()
        self.statistics: Dict[str, int] = {
            "total_events": 0,
            "shared_events": 0,
            "triggered_responses": 0
        }
        
        print(f"[MISP] Integration initialized")
    
    def create_event(self, event_type: MISPEventType,
                    threat_level: str,
                    description: str,
                    indicators: Optional[List[str]] = None,
                    attributes: Optional[Dict] = None) -> MISPEvent:
        """
        Create a MISP event for threat intelligence.
        
        Args:
            event_type: Type of MISP event
            threat_level: Threat level (low/medium/high/critical)
            description: Event description
            indicators: Optional threat indicators
            attributes: Optional event attributes
        
        Returns:
            MISPEvent object
        """
        # Generate event ID
        event_id = hashlib.sha256(
            f"{event_type.value}:{time.time()}".encode()
        ).hexdigest()[:16]
        
        # Create event
        event = MISPEvent(
            event_id=event_id,
            event_type=event_type,
            timestamp=time.time(),
            threat_level=threat_level,
            description=description,
            indicators=indicators or [],
            attributes=attributes or {}
        )
        
        # Store event
        self.events[event_id] = event
        self.statistics["total_events"] += 1
        
        # Trigger event handlers
        self._trigger_event_handlers(event_type, event)
        
        print(f"[MISP] Created event: {event_type.value} (threat: {threat_level})")
        
        return event
    
    def share_event(self, event_id: str) -> bool:
        """
        Share a MISP event with the community.
        
        Args:
            event_id: Event ID to share
        
        Returns:
            True if event was shared
        """
        if event_id in self.events:
            event = self.events[event_id]
            event.shared = True
            
            # Add indicators to shared set
            for indicator in event.indicators:
                self.shared_indicators.add(indicator)
            
            self.statistics["shared_events"] += 1
            
            print(f"[MISP] Shared event {event_id} with {len(event.indicators)} indicators")
            return True
        
        return False
    
    def trigger_on_token_validation(self, token_status: TokenStatus,
                                    token_data: Optional[Dict] = None) -> Optional[MISPEvent]:
        """
        Trigger MISP event based on token validation result.
        
        Args:
            token_status: Result of token validation
            token_data: Optional token data
        
        Returns:
            MISPEvent if triggered, None otherwise
        """
        # Trigger event for suspicious or invalid tokens
        if token_status in [TokenStatus.INVALID, TokenStatus.SUSPICIOUS, TokenStatus.REVOKED]:
            threat_level = "high" if token_status == TokenStatus.SUSPICIOUS else "medium"
            
            event = self.create_event(
                event_type=MISPEventType.THREAT_INDICATOR,
                threat_level=threat_level,
                description=f"Token validation failed: {token_status.value}",
                indicators=[token_data.get("token_id", "unknown") if token_data else "unknown"],
                attributes={
                    "token_status": token_status.value,
                    "timestamp": time.time(),
                    "source": "token_validator"
                }
            )
            
            self.statistics["triggered_responses"] += 1
            return event
        
        return None
    
    def trigger_on_attack_detection(self, attack_type: str,
                                   indicators: List[str],
                                   metadata: Optional[Dict] = None) -> MISPEvent:
        """
        Trigger MISP event for attack detection.
        
        Args:
            attack_type: Type of attack detected
            indicators: Attack indicators
            metadata: Optional metadata
        
        Returns:
            MISPEvent object
        """
        event = self.create_event(
            event_type=MISPEventType.ATTACK_DETECTED,
            threat_level="high",
            description=f"Attack detected: {attack_type}",
            indicators=indicators,
            attributes=metadata or {}
        )
        
        # Auto-share critical events
        if metadata and metadata.get("auto_share", False):
            self.share_event(event.event_id)
        
        self.statistics["triggered_responses"] += 1
        return event
    
    def trigger_on_blacklist_update(self, blacklist_entry: Dict) -> MISPEvent:
        """
        Trigger MISP event for blacklist updates.
        
        Args:
            blacklist_entry: Blacklist entry data
        
        Returns:
            MISPEvent object
        """
        event = self.create_event(
            event_type=MISPEventType.BLACKLIST_UPDATE,
            threat_level=blacklist_entry.get("threat_level", "medium"),
            description=f"Blacklist updated: {blacklist_entry.get('reason', 'unknown')}",
            indicators=[blacklist_entry.get("identifier", "unknown")],
            attributes=blacklist_entry
        )
        
        self.statistics["triggered_responses"] += 1
        return event
    
    def register_event_handler(self, event_type: MISPEventType,
                              handler: Any) -> None:
        """
        Register a handler for specific MISP event types.
        
        Args:
            event_type: Type of event to handle
            handler: Handler function
        """
        self.event_handlers[event_type].append(handler)
        print(f"[MISP] Registered handler for {event_type.value}")
    
    def get_events(self, event_type: Optional[MISPEventType] = None,
                  limit: int = 100) -> List[MISPEvent]:
        """
        Get MISP events with optional filtering.
        
        Args:
            event_type: Optional event type filter
            limit: Maximum number of events to return
        
        Returns:
            List of MISPEvent objects
        """
        events = list(self.events.values())
        
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        
        # Sort by timestamp (most recent first)
        events.sort(key=lambda e: e.timestamp, reverse=True)
        
        return events[:limit]
    
    def get_statistics(self) -> Dict:
        """Get MISP statistics."""
        return {
            "total_events": self.statistics["total_events"],
            "shared_events": self.statistics["shared_events"],
            "triggered_responses": self.statistics["triggered_responses"],
            "shared_indicators": len(self.shared_indicators),
            "registered_handlers": sum(len(handlers) for handlers in self.event_handlers.values())
        }
    
    def export_events(self, filepath: str, limit: Optional[int] = None) -> None:
        """
        Export MISP events to JSON file.
        
        Args:
            filepath: Output file path
            limit: Optional limit on events to export
        """
        events = list(self.events.values())
        if limit:
            events = events[-limit:]
        
        data = {
            "export_timestamp": datetime.now().isoformat(),
            "total_events": len(events),
            "events": [e.to_dict() for e in events]
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"[MISP] Exported {len(events)} events to {filepath}")
    
    def _trigger_event_handlers(self, event_type: MISPEventType, 
                               event: MISPEvent) -> None:
        """Trigger registered handlers for an event type."""
        for handler in self.event_handlers[event_type]:
            try:
                handler(event)
            except Exception as e:
                print(f"[ERROR] MISP handler failed: {e}")


def main():
    """Demo of MISP integration and token validation."""
    print("="*70)
    print("MISP INTEGRATION & TOKEN VALIDATION - DEMO")
    print("="*70)
    print()
    
    # Initialize systems
    token_validator = TokenValidator()
    misp = MISPIntegration()
    
    # Register MISP event handler
    def attack_handler(event: MISPEvent):
        print(f"[HANDLER] Attack event received: {event.description}")
    
    misp.register_event_handler(MISPEventType.ATTACK_DETECTED, attack_handler)
    
    # Generate tokens
    print("\n--- Token Generation ---")
    token_str1, token1 = token_validator.generate_token(
        user_id="user_123",
        permissions=["read", "write"],
        duration=3600.0
    )
    print(f"Token 1: {token_str1[:32]}...")
    
    token_str2, token2 = token_validator.generate_token(
        user_id="admin_456",
        permissions=["admin"],
        duration=7200.0
    )
    print(f"Token 2: {token_str2[:32]}...")
    
    # Validate tokens
    print("\n--- Token Validation ---")
    status1, token_obj1 = token_validator.validate_token(token_str1)
    print(f"Token 1 status: {status1.value}")
    
    # Trigger MISP on token validation
    misp.trigger_on_token_validation(status1, token1.to_dict())
    
    # Simulate invalid token
    print("\n--- Invalid Token Validation ---")
    status_invalid, _ = token_validator.validate_token("invalid.token.string")
    print(f"Invalid token status: {status_invalid.value}")
    misp.trigger_on_token_validation(status_invalid, {"token_id": "unknown"})
    
    # Revoke token
    print("\n--- Token Revocation ---")
    token_validator.revoke_token(token1.token_id)
    status_revoked, _ = token_validator.validate_token(token_str1)
    print(f"Revoked token status: {status_revoked.value}")
    
    # Trigger MISP on attack
    print("\n--- MISP Attack Event ---")
    misp.trigger_on_attack_detection(
        attack_type="sql_injection",
        indicators=["192.168.1.100", "user_suspicious"],
        metadata={"severity": "high", "auto_share": True}
    )
    
    # Get statistics
    print("\n--- Token Validator Statistics ---")
    token_stats = token_validator.get_statistics()
    for key, value in token_stats.items():
        print(f"  {key}: {value}")
    
    print("\n--- MISP Statistics ---")
    misp_stats = misp.get_statistics()
    for key, value in misp_stats.items():
        print(f"  {key}: {value}")
    
    # Export MISP events
    misp.export_events("/tmp/misp_events.json")


if __name__ == "__main__":
    main()
