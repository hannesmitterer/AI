#!/usr/bin/env python3
"""
Blacklist Defense Strategies - Complete Demo
============================================

Comprehensive demonstration of the integrated security system:
- Real-time monitoring
- Adaptive defense
- Token validation
- MISP integration

This demo showcases all security features working together.
"""

import time
from integrated_security import IntegratedSecuritySystem


def demo_basic_security():
    """Demonstrate basic security features."""
    print("\n" + "="*70)
    print("DEMO 1: Basic Security Operations")
    print("="*70 + "\n")
    
    security = IntegratedSecuritySystem()
    security.start()
    
    # Generate and use token
    token_str, _ = security.token_validator.generate_token(
        user_id="user_001",
        permissions=["read"],
        duration=3600.0
    )
    
    # Process normal requests
    print("\nProcessing normal requests...")
    for i in range(5):
        result = security.process_request(
            identifier=f"user_{i:03d}",
            request_data={"endpoint": "/api/data", "method": "GET"},
            token=token_str if i == 0 else None
        )
        print(f"  Request {i+1}: allowed={result['allowed']}, action={result['action']}")
    
    security.stop()


def demo_attack_detection():
    """Demonstrate attack detection and response."""
    print("\n" + "="*70)
    print("DEMO 2: Attack Detection and Response")
    print("="*70 + "\n")
    
    security = IntegratedSecuritySystem()
    security.start()
    
    # Simulate SQL injection attack
    print("\n1. SQL Injection Attack:")
    result = security.process_request(
        identifier="attacker_sql",
        request_data={
            "endpoint": "/api/search",
            "query": "' OR '1'='1' --",
            "method": "POST"
        }
    )
    print(f"   Threat Score: {result['threat_score']:.2f}")
    print(f"   Action: {result['action']}")
    
    # Simulate XSS attack
    print("\n2. XSS Attack:")
    result = security.process_request(
        identifier="attacker_xss",
        request_data={
            "endpoint": "/api/comment",
            "content": "<script>alert('XSS')</script>",
            "method": "POST"
        }
    )
    print(f"   Threat Score: {result['threat_score']:.2f}")
    print(f"   Action: {result['action']}")
    
    # Simulate rate limiting attack
    print("\n3. Rate Limiting Attack (110 rapid requests):")
    for i in range(110):
        result = security.process_request(
            identifier="attacker_rate",
            request_data={"endpoint": "/api/login", "method": "POST"}
        )
    print(f"   Final Threat Score: {result['threat_score']:.2f}")
    print(f"   Final Action: {result['action']}")
    
    # Show attack patterns detected
    patterns = security.defense.get_attack_patterns()
    print(f"\n   Detected {len(patterns)} attack patterns:")
    for pattern in patterns:
        print(f"   - {pattern.pattern_type}: confidence={pattern.confidence:.2f}")
    
    security.stop()


def demo_blacklist_management():
    """Demonstrate blacklist management."""
    print("\n" + "="*70)
    print("DEMO 3: Blacklist Management")
    print("="*70 + "\n")
    
    security = IntegratedSecuritySystem()
    security.start()
    
    # Add entries to blacklist
    print("Adding entries to blacklist:")
    security.add_to_blacklist(
        identifier="192.168.1.100",
        entry_type="ip",
        reason="Multiple failed login attempts",
        threat_level="high",
        duration=600.0
    )
    
    security.add_to_blacklist(
        identifier="malicious_user",
        entry_type="user",
        reason="Repeated policy violations",
        threat_level="critical"
    )
    
    # Check blacklist
    print("\nChecking blacklist status:")
    is_blocked, entry = security.defense.check_blacklist("192.168.1.100", "ip")
    print(f"  IP 192.168.1.100: {'BLOCKED' if is_blocked else 'ALLOWED'}")
    
    # Try to process request from blacklisted IP
    print("\nAttempting request from blacklisted IP:")
    result = security.process_request(
        identifier="192.168.1.100",
        request_data={"endpoint": "/api/data", "method": "GET"}
    )
    print(f"  Allowed: {result['allowed']}")
    print(f"  Reason: {result['reason']}")
    
    # Show all blacklist entries
    entries = security.defense.get_blacklist_entries()
    print(f"\nTotal blacklist entries: {len(entries)}")
    for entry in entries:
        print(f"  - {entry.entry_type}:{entry.identifier} (threat: {entry.threat_level.name})")
    
    security.stop()


def demo_token_validation():
    """Demonstrate token validation and MISP integration."""
    print("\n" + "="*70)
    print("DEMO 4: Token Validation & MISP Integration")
    print("="*70 + "\n")
    
    security = IntegratedSecuritySystem()
    security.start()
    
    # Generate tokens
    print("Generating tokens:")
    token1, _ = security.token_validator.generate_token(
        user_id="user_valid",
        permissions=["read", "write"],
        duration=3600.0
    )
    print(f"  Token 1 (valid): {token1[:32]}...")
    
    token2, token2_obj = security.token_validator.generate_token(
        user_id="user_revoked",
        permissions=["read"],
        duration=3600.0
    )
    print(f"  Token 2 (to be revoked): {token2[:32]}...")
    
    # Test valid token
    print("\nTesting valid token:")
    result = security.process_request(
        identifier="user_valid",
        request_data={"endpoint": "/api/secure", "method": "GET"},
        token=token1
    )
    print(f"  Result: {result['allowed']}, Status: {result['token_status']}")
    
    # Revoke token and test
    print("\nRevoking token 2 and testing:")
    security.token_validator.revoke_token(token2_obj.token_id)
    result = security.process_request(
        identifier="user_revoked",
        request_data={"endpoint": "/api/secure", "method": "GET"},
        token=token2
    )
    print(f"  Result: {result['allowed']}, Status: {result['token_status']}")
    
    # Test invalid token (triggers MISP event)
    print("\nTesting invalid token (triggers MISP event):")
    result = security.process_request(
        identifier="user_invalid",
        request_data={"endpoint": "/api/secure", "method": "GET"},
        token="invalid.token.string"
    )
    print(f"  Result: {result['allowed']}, Status: {result['token_status']}")
    
    # Show MISP events
    misp_events = security.misp.get_events()
    print(f"\nMISP Events Generated: {len(misp_events)}")
    for event in misp_events:
        print(f"  - {event.event_type.value}: {event.description}")
    
    security.stop()


def demo_comprehensive_status():
    """Demonstrate comprehensive status reporting."""
    print("\n" + "="*70)
    print("DEMO 5: Comprehensive Status & Reporting")
    print("="*70 + "\n")
    
    security = IntegratedSecuritySystem()
    security.start()
    
    # Generate some activity
    print("Generating system activity...\n")
    
    # Valid requests
    for i in range(10):
        security.process_request(
            identifier=f"user_{i:03d}",
            request_data={"endpoint": "/api/data", "method": "GET"}
        )
    
    # Suspicious requests
    for i in range(3):
        security.process_request(
            identifier=f"suspicious_{i}",
            request_data={
                "endpoint": "/api/query",
                "query": "' OR 1=1 --",
                "method": "POST"
            }
        )
    
    # Add blacklist entries
    security.add_to_blacklist(
        identifier="banned_ip",
        entry_type="ip",
        reason="Automated scanning detected",
        threat_level="high"
    )
    
    # Get comprehensive status
    print("Comprehensive System Status:")
    print("-" * 70)
    status = security.get_comprehensive_status()
    
    print(f"\nSystem:")
    print(f"  Active: {status['system']['active']}")
    print(f"  Uptime: {status['system']['uptime_readable']}")
    
    print(f"\nMonitoring:")
    print(f"  Total Events: {status['monitoring']['total_events']}")
    print(f"  Total Logs: {status['monitoring']['total_logs']}")
    print(f"  Critical Events: {status['monitoring']['critical_events']}")
    
    print(f"\nDefense:")
    print(f"  Total Requests: {status['defense']['total_requests']}")
    print(f"  Blocked: {status['defense']['blocked_requests']}")
    print(f"  Block Rate: {status['defense']['block_rate']:.2%}")
    print(f"  Blacklisted: {status['defense']['blacklisted_entities']}")
    print(f"  Attack Patterns: {status['defense']['detected_patterns']}")
    
    print(f"\nToken Validation:")
    print(f"  Total Validations: {status['token_validation']['total_validations']}")
    print(f"  Valid: {status['token_validation']['valid_tokens']}")
    print(f"  Invalid: {status['token_validation']['invalid_tokens']}")
    
    print(f"\nMISP:")
    print(f"  Total Events: {status['misp']['total_events']}")
    print(f"  Shared Events: {status['misp']['shared_events']}")
    print(f"  Triggered Responses: {status['misp']['triggered_responses']}")
    
    # Export report
    print("\nExporting comprehensive security report...")
    security.export_security_report("/tmp/comprehensive_security_report.json")
    print("  Report saved to: /tmp/comprehensive_security_report.json")
    
    security.stop()


def main():
    """Run all demos."""
    print("="*70)
    print(" "*15 + "BLACKLIST DEFENSE STRATEGIES")
    print(" "*20 + "Complete Demo Suite")
    print("="*70)
    
    try:
        demo_basic_security()
        time.sleep(1)
        
        demo_attack_detection()
        time.sleep(1)
        
        demo_blacklist_management()
        time.sleep(1)
        
        demo_token_validation()
        time.sleep(1)
        
        demo_comprehensive_status()
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    
    print("\n" + "="*70)
    print("All demos complete!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
