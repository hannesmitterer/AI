#!/usr/bin/env python3
"""
Integrated Security System - Blacklist Defense Strategies
=========================================================

This module integrates all security components:
- Real-time security monitoring
- Adaptive defense mechanisms
- Token validation with MISP integration

Provides a unified interface for comprehensive security management
integrated with the eternal deposition system.

Part of: Blacklist Defense Strategies and Meta-Management
"""

import time
import json
from typing import Dict, Optional, Any, List
from datetime import datetime

# Import security modules
from security_monitoring import SecurityMonitor, EventSeverity, ProtocolStatus
from adaptive_defense import AdaptiveDefenseEngine, DefenseAction, ThreatLevel
from misp_integration import TokenValidator, MISPIntegration, MISPEventType, TokenStatus


class IntegratedSecuritySystem:
    """
    Unified security system integrating monitoring, defense, and MISP.
    
    Provides comprehensive security management with:
    - Real-time monitoring
    - Adaptive defense
    - Token validation
    - MISP threat intelligence
    - Integration with eternal deposition
    """
    
    def __init__(self):
        """Initialize integrated security system."""
        print("="*70)
        print("INTEGRATED SECURITY SYSTEM")
        print("Initializing Blacklist Defense Strategies...")
        print("="*70)
        print()
        
        # Initialize components
        self.monitor = SecurityMonitor(max_events=10000, max_logs=10000)
        self.defense = AdaptiveDefenseEngine()
        self.token_validator = TokenValidator()
        self.misp = MISPIntegration()
        
        # Setup integration callbacks
        self._setup_integration()
        
        # System state
        self.is_active = False
        self.start_time = None
        
        print("[INTEGRATED SECURITY] All components initialized")
        print("[INTEGRATED SECURITY] System ready")
    
    def _setup_integration(self) -> None:
        """Setup integration between components."""
        # Register MISP event handlers
        def handle_attack_detected(event):
            """Handle attack detection events."""
            self.monitor.log_event(
                "misp_attack_alert",
                EventSeverity.CRITICAL,
                "misp_integration",
                f"MISP attack alert: {event.description}",
                metadata=event.to_dict()
            )
        
        def handle_blacklist_update(event):
            """Handle blacklist update events."""
            self.monitor.log_event(
                "misp_blacklist_update",
                EventSeverity.WARNING,
                "misp_integration",
                f"MISP blacklist update: {event.description}",
                metadata=event.to_dict()
            )
        
        self.misp.register_event_handler(MISPEventType.ATTACK_DETECTED, handle_attack_detected)
        self.misp.register_event_handler(MISPEventType.BLACKLIST_UPDATE, handle_blacklist_update)
        
        # Register security monitor handlers
        def handle_critical_event(event):
            """Handle critical security events."""
            # Create MISP event for critical security events
            self.misp.create_event(
                event_type=MISPEventType.THREAT_INDICATOR,
                threat_level="critical",
                description=event.description,
                indicators=[event.source],
                attributes=event.metadata
            )
        
        self.monitor.register_event_handler("attack_detected", handle_critical_event)
        
        print("[INTEGRATION] Component callbacks configured")
    
    def start(self) -> None:
        """Start integrated security system."""
        self.is_active = True
        self.start_time = time.time()
        
        # Start monitoring
        self.monitor.start_monitoring()
        
        # Log system start
        self.monitor.log_event(
            "system_start",
            EventSeverity.INFO,
            "integrated_security",
            "Integrated security system started"
        )
        
        print(f"[INTEGRATED SECURITY] System started at {datetime.now().isoformat()}")
    
    def stop(self) -> None:
        """Stop integrated security system."""
        # Log system stop
        self.monitor.log_event(
            "system_stop",
            EventSeverity.INFO,
            "integrated_security",
            "Integrated security system stopped"
        )
        
        # Stop monitoring
        self.monitor.stop_monitoring()
        
        self.is_active = False
        
        # Cleanup
        self._cleanup()
        
        print(f"[INTEGRATED SECURITY] System stopped")
    
    def process_request(self, identifier: str, 
                       request_data: Dict,
                       token: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a request through the integrated security system.
        
        Args:
            identifier: Request identifier (IP, user ID, etc.)
            request_data: Request data
            token: Optional security token
        
        Returns:
            Dictionary containing processing results
        """
        result = {
            "allowed": False,
            "action": None,
            "token_status": None,
            "threat_score": 0.0,
            "reason": None,
            "timestamp": time.time()
        }
        
        # Step 1: Validate token if provided
        if token:
            token_status, token_obj = self.token_validator.validate_token(token)
            result["token_status"] = token_status.value
            
            # Log token validation
            protocol_status = ProtocolStatus.VERIFIED if token_status == TokenStatus.VALID else ProtocolStatus.BLOCKED
            self.monitor.log_protocol_operation(
                "token_validation",
                protocol_status,
                {"identifier": identifier, "status": token_status.value}
            )
            
            # Trigger MISP on suspicious tokens
            if token_status in [TokenStatus.INVALID, TokenStatus.REVOKED, TokenStatus.SUSPICIOUS]:
                self.misp.trigger_on_token_validation(
                    token_status,
                    token_obj.to_dict() if token_obj else {"token_id": "unknown"}
                )
                
                result["allowed"] = False
                result["reason"] = f"Token validation failed: {token_status.value}"
                return result
        
        # Step 2: Run through adaptive defense
        defense_action, defense_meta = self.defense.process_request(identifier, request_data)
        result["action"] = defense_action.value
        result["threat_score"] = defense_meta["threat_score"]
        
        # Step 3: Log protocol operation
        if defense_action in [DefenseAction.BLOCK, DefenseAction.BLACKLIST]:
            protocol_status = ProtocolStatus.BLOCKED
            result["allowed"] = False
            result["reason"] = f"Blocked by adaptive defense: {defense_action.value}"
            
            # Log security event
            self.monitor.log_event(
                "request_blocked",
                EventSeverity.WARNING,
                "adaptive_defense",
                f"Request blocked: {identifier}",
                metadata=defense_meta
            )
            
            # Trigger MISP for blacklist actions
            if defense_action == DefenseAction.BLACKLIST:
                self.misp.trigger_on_blacklist_update({
                    "identifier": identifier,
                    "reason": "Adaptive defense triggered blacklist",
                    "threat_level": "high",
                    "threat_score": result["threat_score"]
                })
        
        elif defense_action == DefenseAction.THROTTLE:
            protocol_status = ProtocolStatus.SUSPICIOUS
            result["allowed"] = True
            result["reason"] = "Request throttled - monitoring"
            
            self.monitor.log_event(
                "request_throttled",
                EventSeverity.WARNING,
                "adaptive_defense",
                f"Request throttled: {identifier}",
                metadata=defense_meta
            )
        
        else:  # ALLOW or MONITOR
            protocol_status = ProtocolStatus.VERIFIED if defense_action == DefenseAction.ALLOW else ProtocolStatus.NORMAL
            result["allowed"] = True
            result["reason"] = f"Request {defense_action.value}"
        
        # Log the operation
        self.monitor.log_protocol_operation(
            "request_processing",
            protocol_status,
            {
                "identifier": identifier,
                "action": defense_action.value,
                "threat_score": result["threat_score"]
            }
        )
        
        return result
    
    def add_to_blacklist(self, identifier: str, entry_type: str,
                        reason: str, threat_level: str = "medium",
                        duration: Optional[float] = None) -> None:
        """
        Add entry to blacklist with MISP integration.
        
        Args:
            identifier: Identifier to blacklist
            entry_type: Type of identifier
            reason: Reason for blacklisting
            threat_level: Threat level
            duration: Optional duration in seconds
        """
        # Map string threat level to enum
        threat_map = {
            "low": ThreatLevel.LOW,
            "medium": ThreatLevel.MEDIUM,
            "high": ThreatLevel.HIGH,
            "critical": ThreatLevel.CRITICAL
        }
        threat_enum = threat_map.get(threat_level.lower(), ThreatLevel.MEDIUM)
        
        # Add to defense blacklist
        entry = self.defense.add_to_blacklist(
            identifier=identifier,
            entry_type=entry_type,
            reason=reason,
            threat_level=threat_enum,
            duration=duration
        )
        
        # Log event
        self.monitor.log_event(
            "blacklist_add",
            EventSeverity.WARNING,
            "integrated_security",
            f"Added to blacklist: {entry_type}:{identifier}",
            metadata=entry.to_dict()
        )
        
        # Trigger MISP event
        self.misp.trigger_on_blacklist_update(entry.to_dict())
    
    def get_comprehensive_status(self) -> Dict[str, Any]:
        """
        Get comprehensive system status.
        
        Returns:
            Dictionary containing status from all components
        """
        uptime = time.time() - self.start_time if self.start_time else 0
        
        return {
            "system": {
                "active": self.is_active,
                "uptime_seconds": uptime,
                "uptime_readable": f"{uptime/3600:.2f} hours" if uptime > 3600 else f"{uptime/60:.2f} minutes"
            },
            "monitoring": self.monitor.get_statistics(),
            "defense": self.defense.get_statistics(),
            "token_validation": self.token_validator.get_statistics(),
            "misp": self.misp.get_statistics()
        }
    
    def export_security_report(self, filepath: str) -> None:
        """
        Export comprehensive security report.
        
        Args:
            filepath: Path to output file
        """
        report = {
            "report_timestamp": datetime.now().isoformat(),
            "system_status": self.get_comprehensive_status(),
            "recent_events": [e.to_dict() for e in self.monitor.get_events(limit=50)],
            "recent_logs": [l.to_dict() for l in self.monitor.get_protocol_logs(limit=50)],
            "blacklist_entries": [e.to_dict() for e in self.defense.get_blacklist_entries()],
            "attack_patterns": [
                {
                    "pattern_type": p.pattern_type,
                    "detection_count": p.detection_count,
                    "confidence": p.confidence
                }
                for p in self.defense.get_attack_patterns()
            ],
            "misp_events": [e.to_dict() for e in self.misp.get_events(limit=50)]
        }
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"[INTEGRATED SECURITY] Exported security report to {filepath}")
    
    def _cleanup(self) -> None:
        """Cleanup expired entries and optimize storage."""
        # Cleanup expired blacklist entries
        self.defense.cleanup_expired_entries()
        
        # Cleanup expired tokens
        self.token_validator.cleanup_expired_tokens()
        
        print("[CLEANUP] System cleanup completed")


def main():
    """Demo of integrated security system."""
    print("\n" + "="*70)
    print("INTEGRATED SECURITY SYSTEM - DEMO")
    print("="*70)
    print()
    
    # Initialize system
    security = IntegratedSecuritySystem()
    security.start()
    
    # Generate a token
    print("\n--- Token Generation ---")
    token_str, token = security.token_validator.generate_token(
        user_id="demo_user",
        permissions=["read", "write"],
        duration=3600.0
    )
    print(f"Generated token: {token_str[:32]}...")
    
    # Process normal request with valid token
    print("\n--- Processing Normal Request (with valid token) ---")
    result = security.process_request(
        identifier="user_123",
        request_data={"endpoint": "/api/data", "method": "GET"},
        token=token_str
    )
    print(f"Result: allowed={result['allowed']}, action={result['action']}, reason={result['reason']}")
    
    # Process request without token
    print("\n--- Processing Request (no token) ---")
    result = security.process_request(
        identifier="user_456",
        request_data={"endpoint": "/api/search", "method": "GET"}
    )
    print(f"Result: allowed={result['allowed']}, action={result['action']}, reason={result['reason']}")
    
    # Process suspicious request
    print("\n--- Processing Suspicious Request (SQL Injection) ---")
    result = security.process_request(
        identifier="attacker_789",
        request_data={
            "endpoint": "/api/query",
            "query": "' OR 1=1 --",
            "method": "POST"
        }
    )
    print(f"Result: allowed={result['allowed']}, action={result['action']}, threat_score={result['threat_score']:.2f}")
    
    # Add manual blacklist entry
    print("\n--- Adding Manual Blacklist Entry ---")
    security.add_to_blacklist(
        identifier="192.168.1.100",
        entry_type="ip",
        reason="Manual blacklist - repeated violations",
        threat_level="high",
        duration=600.0
    )
    
    # Get comprehensive status
    print("\n--- System Status ---")
    status = security.get_comprehensive_status()
    print(json.dumps(status, indent=2))
    
    # Export security report
    print("\n--- Exporting Security Report ---")
    security.export_security_report("/tmp/security_report.json")
    
    # Stop system
    print("\n--- Stopping System ---")
    security.stop()
    
    print("\n" + "="*70)
    print("Demo completed!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
