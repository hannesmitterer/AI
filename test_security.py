#!/usr/bin/env python3
"""
Unit Tests for Security Modules
================================

Basic tests for security monitoring, adaptive defense,
token validation, and MISP integration.
"""

import time
import unittest
from security_monitoring import SecurityMonitor, EventSeverity, ProtocolStatus
from adaptive_defense import AdaptiveDefenseEngine, DefenseAction, ThreatLevel
from misp_integration import TokenValidator, MISPIntegration, TokenStatus, MISPEventType
from integrated_security import IntegratedSecuritySystem


class TestSecurityMonitoring(unittest.TestCase):
    """Test security monitoring module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.monitor = SecurityMonitor(max_events=100, max_logs=100)
    
    def test_initialization(self):
        """Test monitor initialization."""
        self.assertIsNotNone(self.monitor)
        self.assertEqual(len(self.monitor.events), 0)
        self.assertEqual(len(self.monitor.protocol_logs), 0)
    
    def test_log_event(self):
        """Test event logging."""
        event = self.monitor.log_event(
            "test_event",
            EventSeverity.INFO,
            "test_source",
            "Test description"
        )
        self.assertIsNotNone(event)
        self.assertEqual(event.event_type, "test_event")
        self.assertEqual(len(self.monitor.events), 1)
    
    def test_log_protocol_operation(self):
        """Test protocol operation logging."""
        log = self.monitor.log_protocol_operation(
            "test_op",
            ProtocolStatus.VERIFIED,
            {"test": "data"}
        )
        self.assertIsNotNone(log)
        self.assertEqual(log.operation, "test_op")
        self.assertEqual(len(self.monitor.protocol_logs), 1)
    
    def test_get_statistics(self):
        """Test statistics retrieval."""
        self.monitor.log_event("test", EventSeverity.INFO, "src", "desc")
        stats = self.monitor.get_statistics()
        self.assertEqual(stats["total_events"], 1)
        self.assertEqual(stats["total_logs"], 0)


class TestAdaptiveDefense(unittest.TestCase):
    """Test adaptive defense module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.defense = AdaptiveDefenseEngine()
    
    def test_initialization(self):
        """Test defense engine initialization."""
        self.assertIsNotNone(self.defense)
        self.assertEqual(len(self.defense.blacklist), 0)
    
    def test_blacklist_add(self):
        """Test adding to blacklist."""
        entry = self.defense.add_to_blacklist(
            "test_id",
            "test_type",
            "test_reason",
            ThreatLevel.MEDIUM
        )
        self.assertIsNotNone(entry)
        self.assertEqual(len(self.defense.blacklist), 1)
    
    def test_blacklist_check(self):
        """Test blacklist checking."""
        self.defense.add_to_blacklist(
            "test_id",
            "test_type",
            "test_reason",
            ThreatLevel.MEDIUM
        )
        is_blocked, entry = self.defense.check_blacklist("test_id", "test_type")
        self.assertTrue(is_blocked)
        self.assertIsNotNone(entry)
    
    def test_sql_injection_detection(self):
        """Test SQL injection pattern detection."""
        pattern = self.defense.detect_attack_pattern({
            "query": "' OR 1=1 --"
        })
        self.assertIsNotNone(pattern)
        self.assertEqual(pattern.pattern_type, "sql_injection")
    
    def test_xss_detection(self):
        """Test XSS pattern detection."""
        pattern = self.defense.detect_attack_pattern({
            "content": "<script>document.write('test')</script> javascript:void(0)"
        })
        self.assertIsNotNone(pattern)
        self.assertEqual(pattern.pattern_type, "xss_attack")
    
    def test_rate_limiting(self):
        """Test rate limiting detection."""
        # Simulate many requests
        for i in range(101):
            self.defense.detect_rate_limiting_attack("test_user")
        
        # Should detect attack
        is_attack = self.defense.detect_rate_limiting_attack("test_user")
        self.assertTrue(is_attack)
    
    def test_threat_scoring(self):
        """Test threat score calculation."""
        score = self.defense.calculate_threat_score(
            "test_user",
            {"query": "normal query"}
        )
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)


class TestTokenValidation(unittest.TestCase):
    """Test token validation module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.validator = TokenValidator()
    
    def test_initialization(self):
        """Test validator initialization."""
        self.assertIsNotNone(self.validator)
        self.assertIsNotNone(self.validator.secret_key)
    
    def test_token_generation(self):
        """Test token generation."""
        token_str, token_obj = self.validator.generate_token(
            user_id="test_user",
            permissions=["read"],
            duration=3600.0
        )
        self.assertIsNotNone(token_str)
        self.assertIsNotNone(token_obj)
        self.assertIn(".", token_str)  # Should have dot separator
    
    def test_token_validation_valid(self):
        """Test validation of valid token."""
        token_str, _ = self.validator.generate_token(
            user_id="test_user",
            permissions=["read"],
            duration=3600.0
        )
        status, token_obj = self.validator.validate_token(token_str)
        self.assertEqual(status, TokenStatus.VALID)
        self.assertIsNotNone(token_obj)
    
    def test_token_validation_invalid(self):
        """Test validation of invalid token."""
        status, token_obj = self.validator.validate_token("invalid.token")
        self.assertEqual(status, TokenStatus.INVALID)
        self.assertIsNone(token_obj)
    
    def test_token_revocation(self):
        """Test token revocation."""
        token_str, token_obj = self.validator.generate_token(
            user_id="test_user",
            permissions=["read"],
            duration=3600.0
        )
        
        # Revoke token
        self.validator.revoke_token(token_obj.token_id)
        
        # Should now be revoked
        status, _ = self.validator.validate_token(token_str)
        self.assertEqual(status, TokenStatus.REVOKED)


class TestMISPIntegration(unittest.TestCase):
    """Test MISP integration module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.misp = MISPIntegration()
    
    def test_initialization(self):
        """Test MISP initialization."""
        self.assertIsNotNone(self.misp)
        self.assertEqual(len(self.misp.events), 0)
    
    def test_create_event(self):
        """Test MISP event creation."""
        event = self.misp.create_event(
            MISPEventType.ATTACK_DETECTED,
            "high",
            "Test attack",
            ["indicator1"]
        )
        self.assertIsNotNone(event)
        self.assertEqual(len(self.misp.events), 1)
    
    def test_share_event(self):
        """Test event sharing."""
        event = self.misp.create_event(
            MISPEventType.ATTACK_DETECTED,
            "high",
            "Test attack",
            ["indicator1"]
        )
        
        result = self.misp.share_event(event.event_id)
        self.assertTrue(result)
        self.assertTrue(event.shared)
    
    def test_trigger_on_attack(self):
        """Test attack detection trigger."""
        event = self.misp.trigger_on_attack_detection(
            "sql_injection",
            ["192.168.1.1"],
            {"severity": "high"}
        )
        self.assertIsNotNone(event)
        self.assertEqual(event.event_type, MISPEventType.ATTACK_DETECTED)


class TestIntegratedSecurity(unittest.TestCase):
    """Test integrated security system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.security = IntegratedSecuritySystem()
    
    def test_initialization(self):
        """Test system initialization."""
        self.assertIsNotNone(self.security)
        self.assertIsNotNone(self.security.monitor)
        self.assertIsNotNone(self.security.defense)
        self.assertIsNotNone(self.security.token_validator)
        self.assertIsNotNone(self.security.misp)
    
    def test_start_stop(self):
        """Test system start and stop."""
        self.security.start()
        self.assertTrue(self.security.is_active)
        
        self.security.stop()
        self.assertFalse(self.security.is_active)
    
    def test_process_request_normal(self):
        """Test processing normal request."""
        self.security.start()
        
        result = self.security.process_request(
            identifier="test_user",
            request_data={"endpoint": "/api/data"}
        )
        
        self.assertTrue(result["allowed"])
        self.assertIsNotNone(result["action"])
        
        self.security.stop()
    
    def test_process_request_with_token(self):
        """Test processing request with token."""
        self.security.start()
        
        # Generate token
        token_str, _ = self.security.token_validator.generate_token(
            "test_user",
            ["read"],
            3600.0
        )
        
        # Process request with token
        result = self.security.process_request(
            identifier="test_user",
            request_data={"endpoint": "/api/data"},
            token=token_str
        )
        
        self.assertTrue(result["allowed"])
        self.assertEqual(result["token_status"], "valid")
        
        self.security.stop()
    
    def test_add_to_blacklist(self):
        """Test adding to blacklist via integrated system."""
        self.security.start()
        
        self.security.add_to_blacklist(
            "test_id",
            "ip",
            "Test reason",
            "high"
        )
        
        # Should be in blacklist
        is_blocked, _ = self.security.defense.check_blacklist("test_id", "ip")
        self.assertTrue(is_blocked)
        
        self.security.stop()
    
    def test_comprehensive_status(self):
        """Test comprehensive status."""
        self.security.start()
        
        status = self.security.get_comprehensive_status()
        
        self.assertIn("system", status)
        self.assertIn("monitoring", status)
        self.assertIn("defense", status)
        self.assertIn("token_validation", status)
        self.assertIn("misp", status)
        
        self.security.stop()


def run_tests():
    """Run all tests."""
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add tests
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestSecurityMonitoring))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestAdaptiveDefense))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestTokenValidation))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMISPIntegration))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestIntegratedSecurity))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    print("="*70)
    print("SECURITY MODULES - UNIT TESTS")
    print("="*70)
    print()
    
    result = run_tests()
    
    print("\n" + "="*70)
    if result.wasSuccessful():
        print("ALL TESTS PASSED ✓")
    else:
        print("SOME TESTS FAILED ✗")
    print("="*70)
