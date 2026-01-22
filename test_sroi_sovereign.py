#!/usr/bin/env python3
"""
Unit tests for S-ROI Sovereign Protocol
========================================

Tests the S-ROI Sovereign protocol implementation including:
- State management
- Resonance tracking
- Stealth mode with cooldown
- Logging functionality
"""

import unittest
import time
import logging
from sroi_sovereign import (
    SROISovereign, SROIState, StealthMode,
    SROILogger, StealthModeController,
    SROI_TARGET, RESONANCE_WARNING_THRESHOLD, RESONANCE_CRITICAL_THRESHOLD
)


class TestSROILogger(unittest.TestCase):
    """Test cases for SROILogger class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.logger = SROILogger(log_level=logging.ERROR)  # Suppress output during tests
    
    def test_initialization(self):
        """Test logger initialization."""
        self.assertEqual(len(self.logger.state_change_history), 0)
        self.assertEqual(len(self.logger.resonance_history), 0)
        self.assertIsNotNone(self.logger.logger)
    
    def test_log_state_change(self):
        """Test state change logging."""
        self.logger.log_state_change(
            SROIState.STABLE,
            SROIState.WARNING,
            0.82,
            "Test transition"
        )
        
        self.assertEqual(len(self.logger.state_change_history), 1)
        entry = self.logger.state_change_history[0]
        
        self.assertEqual(entry.previous_state, SROIState.STABLE)
        self.assertEqual(entry.new_state, SROIState.WARNING)
        self.assertEqual(entry.resonance_value, 0.82)
        self.assertEqual(entry.reason, "Test transition")
    
    def test_log_resonance(self):
        """Test resonance logging."""
        self.logger.log_resonance(0.9, SROIState.STABLE, False)
        
        self.assertEqual(len(self.logger.resonance_history), 1)
        entry = self.logger.resonance_history[0]
        
        self.assertEqual(entry.value, 0.9)
        self.assertEqual(entry.state, SROIState.STABLE)
        self.assertFalse(entry.stealth_active)
    
    def test_history_limit(self):
        """Test history size limiting."""
        # Add more than max_history_size entries
        for i in range(1500):
            self.logger.log_resonance(0.5, SROIState.STABLE, False)
        
        # Should be trimmed to max_history_size
        self.assertEqual(len(self.logger.resonance_history), 1000)
    
    def test_get_history_with_limit(self):
        """Test retrieving limited history."""
        for i in range(20):
            self.logger.log_resonance(0.5 + i * 0.01, SROIState.STABLE, False)
        
        limited = self.logger.get_resonance_history(limit=5)
        self.assertEqual(len(limited), 5)


class TestStealthModeController(unittest.TestCase):
    """Test cases for StealthModeController class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Use short cooldown for testing (1 second)
        self.controller = StealthModeController(cooldown_seconds=1.0)
    
    def test_initialization(self):
        """Test controller initialization."""
        self.assertEqual(self.controller.mode, StealthMode.INACTIVE)
        self.assertIsNone(self.controller.last_deactivation_time)
        self.assertEqual(self.controller.activation_count, 0)
        self.assertEqual(self.controller.deactivation_count, 0)
    
    def test_can_activate_initially(self):
        """Test that activation is allowed initially."""
        self.assertTrue(self.controller.can_activate())
    
    def test_activation(self):
        """Test stealth mode activation."""
        success = self.controller.activate()
        
        self.assertTrue(success)
        self.assertEqual(self.controller.mode, StealthMode.ACTIVE)
        self.assertTrue(self.controller.is_active())
        self.assertEqual(self.controller.activation_count, 1)
    
    def test_cannot_activate_when_active(self):
        """Test that activation is denied when already active."""
        self.controller.activate()
        
        success = self.controller.activate()
        self.assertFalse(success)
        self.assertEqual(self.controller.activation_count, 1)  # Should not increment
    
    def test_deactivation(self):
        """Test stealth mode deactivation."""
        self.controller.activate()
        self.controller.deactivate()
        
        self.assertEqual(self.controller.mode, StealthMode.COOLDOWN)
        self.assertFalse(self.controller.is_active())
        self.assertEqual(self.controller.deactivation_count, 1)
        self.assertIsNotNone(self.controller.last_deactivation_time)
    
    def test_cooldown_period(self):
        """Test cooldown period enforcement."""
        # Activate and deactivate
        self.controller.activate()
        self.controller.deactivate()
        
        # Should not be able to activate immediately
        self.assertFalse(self.controller.can_activate())
        
        # Wait for cooldown
        time.sleep(1.1)
        
        # Should be able to activate now
        self.assertTrue(self.controller.can_activate())
    
    def test_cooldown_remaining(self):
        """Test cooldown remaining calculation."""
        # Initially no cooldown
        self.assertEqual(self.controller.get_cooldown_remaining(), 0.0)
        
        # Activate and deactivate
        self.controller.activate()
        self.controller.deactivate()
        
        # Should have cooldown remaining
        remaining = self.controller.get_cooldown_remaining()
        self.assertGreater(remaining, 0.0)
        self.assertLessEqual(remaining, 1.0)
    
    def test_update_transitions_from_cooldown(self):
        """Test that update() transitions from cooldown to inactive."""
        self.controller.activate()
        self.controller.deactivate()
        
        # Force cooldown to expire
        time.sleep(1.1)
        
        self.controller.update()
        self.assertEqual(self.controller.mode, StealthMode.INACTIVE)
    
    def test_get_status(self):
        """Test status retrieval."""
        status = self.controller.get_status()
        
        self.assertIn('mode', status)
        self.assertIn('is_active', status)
        self.assertIn('can_activate', status)
        self.assertIn('cooldown_remaining', status)
        self.assertIn('activation_count', status)
        self.assertIn('deactivation_count', status)


class TestSROISovereign(unittest.TestCase):
    """Test cases for SROISovereign main controller."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Suppress logging during tests
        self.sovereign = SROISovereign(
            initial_resonance=0.9,
            log_level=logging.ERROR,
            cooldown_seconds=1.0
        )
    
    def test_initialization(self):
        """Test sovereign initialization."""
        self.assertEqual(self.sovereign.current_resonance, 0.9)
        self.assertEqual(self.sovereign.state, SROIState.STABLE)
        self.assertEqual(self.sovereign.update_count, 0)
        self.assertIsNotNone(self.sovereign.logger)
        self.assertIsNotNone(self.sovereign.stealth_controller)
    
    def test_state_determination_stable(self):
        """Test state determination for STABLE range."""
        sovereign = SROISovereign(initial_resonance=0.95, log_level=logging.ERROR)
        self.assertEqual(sovereign.state, SROIState.STABLE)
    
    def test_state_determination_warning(self):
        """Test state determination for WARNING range."""
        sovereign = SROISovereign(initial_resonance=0.80, log_level=logging.ERROR)
        self.assertEqual(sovereign.state, SROIState.WARNING)
    
    def test_state_determination_critical(self):
        """Test state determination for CRITICAL range."""
        sovereign = SROISovereign(initial_resonance=0.60, log_level=logging.ERROR)
        self.assertEqual(sovereign.state, SROIState.CRITICAL)
    
    def test_update_resonance(self):
        """Test resonance update."""
        self.sovereign.update_resonance(0.75, "Test update")
        
        self.assertEqual(self.sovereign.current_resonance, 0.75)
        self.assertEqual(self.sovereign.state, SROIState.WARNING)
        self.assertEqual(self.sovereign.update_count, 1)
    
    def test_resonance_clamping(self):
        """Test that resonance is clamped to valid range."""
        self.sovereign.update_resonance(1.5, "Test high")
        self.assertEqual(self.sovereign.current_resonance, 1.0)
        
        self.sovereign.update_resonance(-0.5, "Test low")
        self.assertEqual(self.sovereign.current_resonance, 0.0)
    
    def test_state_transition_logging(self):
        """Test that state transitions are logged."""
        initial_state = self.sovereign.state
        
        # Trigger state change
        self.sovereign.update_resonance(0.60, "Trigger WARNING to CRITICAL")
        
        # Check that state changed
        self.assertNotEqual(self.sovereign.state, initial_state)
        
        # Check that it was logged
        history = self.sovereign.logger.get_state_change_history()
        self.assertGreater(len(history), 0)
    
    def test_stealth_activation_success(self):
        """Test successful stealth activation."""
        success = self.sovereign.request_stealth_activation("Test activation")
        
        self.assertTrue(success)
        self.assertTrue(self.sovereign.stealth_controller.is_active())
    
    def test_stealth_activation_during_active(self):
        """Test that stealth activation fails when already active."""
        self.sovereign.request_stealth_activation("First activation")
        success = self.sovereign.request_stealth_activation("Second activation")
        
        self.assertFalse(success)
    
    def test_stealth_deactivation(self):
        """Test stealth deactivation."""
        self.sovereign.request_stealth_activation("Activate")
        self.sovereign.deactivate_stealth("Deactivate")
        
        self.assertFalse(self.sovereign.stealth_controller.is_active())
    
    def test_stealth_cooldown_enforcement(self):
        """Test that cooldown prevents immediate reactivation."""
        # Activate and deactivate
        self.sovereign.request_stealth_activation("Activate")
        self.sovereign.deactivate_stealth("Deactivate")
        
        # Try to reactivate immediately
        success = self.sovereign.request_stealth_activation("Reactivate")
        self.assertFalse(success)
        
        # Wait for cooldown
        time.sleep(1.1)
        
        # Should succeed now
        success = self.sovereign.request_stealth_activation("Reactivate after cooldown")
        self.assertTrue(success)
    
    def test_get_status(self):
        """Test status retrieval."""
        status = self.sovereign.get_status()
        
        self.assertIn('current_resonance', status)
        self.assertIn('state', status)
        self.assertIn('stealth', status)
        self.assertIn('uptime_seconds', status)
        self.assertIn('update_count', status)
        self.assertIn('target_sroi', status)
        self.assertIn('warning_threshold', status)
        self.assertIn('critical_threshold', status)
        
        self.assertEqual(status['target_sroi'], SROI_TARGET)
        self.assertEqual(status['warning_threshold'], RESONANCE_WARNING_THRESHOLD)
        self.assertEqual(status['critical_threshold'], RESONANCE_CRITICAL_THRESHOLD)
    
    def test_get_state_history(self):
        """Test state history retrieval."""
        # Generate some state changes
        self.sovereign.update_resonance(0.80, "Change 1")
        self.sovereign.update_resonance(0.65, "Change 2")
        self.sovereign.update_resonance(0.90, "Change 3")
        
        history = self.sovereign.get_state_history(limit=5)
        
        self.assertIsInstance(history, list)
        self.assertGreater(len(history), 0)
        
        # Verify structure
        if len(history) > 0:
            entry = history[0]
            self.assertIn('timestamp', entry)
            self.assertIn('previous_state', entry)
            self.assertIn('new_state', entry)
            self.assertIn('resonance_value', entry)
            self.assertIn('reason', entry)
    
    def test_get_resonance_history(self):
        """Test resonance history retrieval."""
        # Generate some updates
        self.sovereign.update_resonance(0.85, "Update 1")
        self.sovereign.update_resonance(0.90, "Update 2")
        
        history = self.sovereign.get_resonance_history(limit=5)
        
        self.assertIsInstance(history, list)
        self.assertGreater(len(history), 0)
        
        # Verify structure
        if len(history) > 0:
            entry = history[0]
            self.assertIn('timestamp', entry)
            self.assertIn('value', entry)
            self.assertIn('state', entry)
            self.assertIn('stealth_active', entry)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_resonance_at_exact_thresholds(self):
        """Test behavior at exact threshold values."""
        # At WARNING threshold
        sovereign = SROISovereign(
            initial_resonance=RESONANCE_WARNING_THRESHOLD,
            log_level=logging.ERROR
        )
        self.assertEqual(sovereign.state, SROIState.STABLE)
        
        # Just below WARNING threshold
        sovereign = SROISovereign(
            initial_resonance=RESONANCE_WARNING_THRESHOLD - 0.001,
            log_level=logging.ERROR
        )
        self.assertEqual(sovereign.state, SROIState.WARNING)
        
        # At CRITICAL threshold
        sovereign = SROISovereign(
            initial_resonance=RESONANCE_CRITICAL_THRESHOLD,
            log_level=logging.ERROR
        )
        self.assertEqual(sovereign.state, SROIState.WARNING)
        
        # Just below CRITICAL threshold
        sovereign = SROISovereign(
            initial_resonance=RESONANCE_CRITICAL_THRESHOLD - 0.001,
            log_level=logging.ERROR
        )
        self.assertEqual(sovereign.state, SROIState.CRITICAL)
    
    def test_rapid_resonance_updates(self):
        """Test rapid consecutive resonance updates."""
        sovereign = SROISovereign(initial_resonance=0.9, log_level=logging.ERROR)
        
        # Perform many rapid updates
        for i in range(100):
            sovereign.update_resonance(0.5 + (i % 50) * 0.01, f"Update {i}")
        
        self.assertEqual(sovereign.update_count, 100)
    
    def test_stealth_deactivation_when_inactive(self):
        """Test that deactivating inactive stealth is safe."""
        sovereign = SROISovereign(initial_resonance=0.9, log_level=logging.ERROR)
        
        # Should not raise error
        sovereign.deactivate_stealth("Deactivate inactive")
        
        # Should still be inactive
        self.assertFalse(sovereign.stealth_controller.is_active())
    
    def test_zero_cooldown(self):
        """Test stealth controller with zero cooldown."""
        controller = StealthModeController(cooldown_seconds=0.0)
        
        controller.activate()
        controller.deactivate()
        
        # Should be able to activate immediately
        self.assertTrue(controller.can_activate())
        success = controller.activate()
        self.assertTrue(success)


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSROILogger))
    suite.addTests(loader.loadTestsFromTestCase(TestStealthModeController))
    suite.addTests(loader.loadTestsFromTestCase(TestSROISovereign))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    exit(run_tests())
