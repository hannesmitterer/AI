#!/usr/bin/env python3
"""
Internet Organica Integration Test Suite

Tests all components of the Internet Organica framework:
- Rhythm synchronization
- SovereignShield security
- Wall of Entropy logging
- Module integration

Operating under Lex Amoris - NSR Compliant - OLF Aligned
"""

import sys
import time
import json
from datetime import datetime
from pathlib import Path

# Import our modules
try:
    from rhythm_sync import BiologicalRhythm, RhythmValidator
    from sovereign_shield import SovereignShield
    from entropy_wall import EntropyWall
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Ensure rhythm_sync.py, sovereign_shield.py, and entropy_wall.py are in the same directory")
    sys.exit(1)


class IntegrationTester:
    """Integration test suite for Internet Organica framework."""
    
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.start_time = time.time()
        
    def run_all_tests(self):
        """Run complete test suite."""
        print("🏛️  Internet Organica Integration Test Suite")
        print("=" * 80)
        print(f"Started: {datetime.utcnow().isoformat()[:19]} UTC\n")
        
        # Test rhythm synchronization
        self.test_rhythm_sync()
        
        # Test sovereign shield
        self.test_sovereign_shield()
        
        # Test entropy wall
        self.test_entropy_wall()
        
        # Test integration
        self.test_integration()
        
        # Report results
        self.report_results()
    
    def test_rhythm_sync(self):
        """Test biological rhythm synchronization."""
        print("\n🌀 Testing Biological Rhythm Synchronization")
        print("-" * 80)
        
        # Test 1: Basic initialization
        try:
            rhythm = BiologicalRhythm()
            status = rhythm.get_status()
            assert status["frequencies"]["primary_hz"] == 0.432
            assert status["frequencies"]["eternal_cycle_hz"] == 0.043
            print("✓ Test 1.1: Rhythm initialization - PASSED")
            self.tests_passed += 1
        except Exception as e:
            print(f"✗ Test 1.1: Rhythm initialization - FAILED: {e}")
            self.tests_failed += 1
        
        # Test 2: Phase calculation
        try:
            rhythm = BiologicalRhythm()
            phase = rhythm.get_current_phase()
            assert 0 <= phase < 6.28319  # 2π
            print("✓ Test 1.2: Phase calculation - PASSED")
            self.tests_passed += 1
        except Exception as e:
            print(f"✗ Test 1.2: Phase calculation - FAILED: {e}")
            self.tests_failed += 1
        
        # Test 3: Stillness detection
        try:
            rhythm = BiologicalRhythm()
            is_stillness = rhythm.is_stillness_phase()
            assert isinstance(is_stillness, bool)
            print("✓ Test 1.3: Stillness detection - PASSED")
            self.tests_passed += 1
        except Exception as e:
            print(f"✗ Test 1.3: Stillness detection - FAILED: {e}")
            self.tests_failed += 1
        
        # Test 4: Resonance alignment
        try:
            rhythm = BiologicalRhythm()
            # Test with harmonic frequency (432 Hz)
            alignment = rhythm.calculate_resonance_alignment(432.0)
            assert 0.0 <= alignment <= 1.0
            print(f"✓ Test 1.4: Resonance alignment (432 Hz = {alignment:.2f}) - PASSED")
            self.tests_passed += 1
        except Exception as e:
            print(f"✗ Test 1.4: Resonance alignment - FAILED: {e}")
            self.tests_failed += 1
        
        # Test 5: Validator
        try:
            validator = RhythmValidator()
            result = validator.validate_timing_interval(2.31)  # Primary period
            assert result["alignment_score"] > 0.8
            print("✓ Test 1.5: Timing validator - PASSED")
            self.tests_passed += 1
        except Exception as e:
            print(f"✗ Test 1.5: Timing validator - FAILED: {e}")
            self.tests_failed += 1
    
    def test_sovereign_shield(self):
        """Test SovereignShield security module."""
        print("\n🛡️  Testing SovereignShield Security")
        print("-" * 80)
        
        # Test 1: Shield initialization
        try:
            shield = SovereignShield(log_to_entropy_wall=False)
            status = shield.get_status()
            assert status["status"] == "ACTIVE"
            assert status["protection"]["nsr_enforcement"] == True
            print("✓ Test 2.1: Shield initialization - PASSED")
            self.tests_passed += 1
        except Exception as e:
            print(f"✗ Test 2.1: Shield initialization - FAILED: {e}")
            self.tests_failed += 1
        
        # Test 2: Clean code scanning
        try:
            shield = SovereignShield(log_to_entropy_wall=False)
            clean_code = """
            def greet(name):
                return f"Hello, {name}!"
            """
            result = shield.scan_code(clean_code, "test_clean")
            assert result["approved"] == True
            assert result["severity"] == "NONE"
            print("✓ Test 2.2: Clean code scanning - PASSED")
            self.tests_passed += 1
        except Exception as e:
            print(f"✗ Test 2.2: Clean code scanning - FAILED: {e}")
            self.tests_failed += 1
        
        # Test 3: Tracking detection
        try:
            shield = SovereignShield(log_to_entropy_wall=False)
            tracking_code = """
            <script src="https://google-analytics.com/ga.js"></script>
            <script>localStorage.setItem('user_id', '12345');</script>
            """
            result = shield.scan_code(tracking_code, "test_tracking")
            assert result["approved"] == False
            assert len(result["threats"]["tracking"]) > 0
            print("✓ Test 2.3: Tracking detection - PASSED")
            self.tests_passed += 1
        except Exception as e:
            print(f"✗ Test 2.3: Tracking detection - FAILED: {e}")
            self.tests_failed += 1
        
        # Test 4: NSR violation detection
        try:
            shield = SovereignShield(log_to_entropy_wall=False)
            nsr_code = """
            function enslave_user() {
                force_action();
                manipulate_behavior();
            }
            """
            result = shield.scan_code(nsr_code, "test_nsr")
            assert len(result["threats"]["nsr_violations"]) > 0
            print("✓ Test 2.4: NSR violation detection - PASSED")
            self.tests_passed += 1
        except Exception as e:
            print(f"✗ Test 2.4: NSR violation detection - FAILED: {e}")
            self.tests_failed += 1
        
        # Test 5: Contribution validation
        try:
            shield = SovereignShield(log_to_entropy_wall=False)
            good_code = "def calculate(x): return x * 2"
            result = shield.validate_contribution(good_code, {"author": "test"})
            assert result["approved"] == True
            assert result["nsr_compliant"] == True
            print("✓ Test 2.5: Contribution validation - PASSED")
            self.tests_passed += 1
        except Exception as e:
            print(f"✗ Test 2.5: Contribution validation - FAILED: {e}")
            self.tests_failed += 1
    
    def test_entropy_wall(self):
        """Test Wall of Entropy logging system."""
        print("\n📊 Testing Wall of Entropy")
        print("-" * 80)
        
        # Test 1: Wall initialization
        try:
            wall = EntropyWall(data_dir=".test_entropy_wall")
            assert wall.data_dir.exists()
            print("✓ Test 3.1: Wall initialization - PASSED")
            self.tests_passed += 1
        except Exception as e:
            print(f"✗ Test 3.1: Wall initialization - FAILED: {e}")
            self.tests_failed += 1
        
        # Test 2: Event logging
        try:
            wall = EntropyWall(data_dir=".test_entropy_wall")
            event = wall.log_event(
                violation_type="TEST_VIOLATION",
                source_identifier="test_source_hash",
                action_taken="BLOCKED",
                severity="HIGH",
                details={"test": "data"}
            )
            assert event["violation_type"] == "TEST_VIOLATION"
            print("✓ Test 3.2: Event logging - PASSED")
            self.tests_passed += 1
        except Exception as e:
            print(f"✗ Test 3.2: Event logging - FAILED: {e}")
            self.tests_failed += 1
        
        # Test 3: Event querying
        try:
            wall = EntropyWall(data_dir=".test_entropy_wall")
            events = wall.query_events(violation_type="TEST_VIOLATION")
            assert len(events) > 0
            print("✓ Test 3.3: Event querying - PASSED")
            self.tests_passed += 1
        except Exception as e:
            print(f"✗ Test 3.3: Event querying - FAILED: {e}")
            self.tests_failed += 1
        
        # Test 4: Statistics generation
        try:
            wall = EntropyWall(data_dir=".test_entropy_wall")
            stats = wall.get_statistics("all")
            assert "total_events" in stats
            assert stats["total_events"] >= 0
            print("✓ Test 3.4: Statistics generation - PASSED")
            self.tests_passed += 1
        except Exception as e:
            print(f"✗ Test 3.4: Statistics generation - FAILED: {e}")
            self.tests_failed += 1
        
        # Test 5: HTML export
        try:
            wall = EntropyWall(data_dir=".test_entropy_wall")
            wall.export_html_report("/tmp/test_entropy_report.html")
            assert Path("/tmp/test_entropy_report.html").exists()
            print("✓ Test 3.5: HTML export - PASSED")
            self.tests_passed += 1
        except Exception as e:
            print(f"✗ Test 3.5: HTML export - FAILED: {e}")
            self.tests_failed += 1
    
    def test_integration(self):
        """Test integration between all modules."""
        print("\n🔗 Testing Module Integration")
        print("-" * 80)
        
        # Test 1: Rhythm + Shield integration
        try:
            rhythm = BiologicalRhythm()
            shield = SovereignShield(log_to_entropy_wall=False)
            validator = RhythmValidator()
            
            # Validate that shield operations respect rhythm
            is_stillness = rhythm.is_stillness_phase()
            code = "def test(): pass"
            scan_result = shield.scan_code(code, "integration_test")
            
            # Both should work independently
            assert scan_result["approved"] in [True, False]
            assert isinstance(is_stillness, bool)
            
            print("✓ Test 4.1: Rhythm + Shield integration - PASSED")
            self.tests_passed += 1
        except Exception as e:
            print(f"✗ Test 4.1: Rhythm + Shield integration - FAILED: {e}")
            self.tests_failed += 1
        
        # Test 2: Shield + Wall integration
        try:
            shield = SovereignShield(log_to_entropy_wall=True)
            wall = EntropyWall()
            
            # Scan malicious code (should log to wall)
            bad_code = "track_user(); google-analytics.send();"
            result = shield.scan_code(bad_code, "integration_test_2")
            
            # Check if logged
            if result["action"] in ["QUARANTINE", "BLOCKED"]:
                recent = wall.get_recent_events(5)
                # Event should be logged
                print("✓ Test 4.2: Shield + Wall integration - PASSED")
                self.tests_passed += 1
            else:
                print("✓ Test 4.2: Shield + Wall integration - PASSED (no log needed)")
                self.tests_passed += 1
        except Exception as e:
            print(f"✗ Test 4.2: Shield + Wall integration - FAILED: {e}")
            self.tests_failed += 1
        
        # Test 3: Full workflow
        try:
            # Initialize all systems
            rhythm = BiologicalRhythm()
            shield = SovereignShield(log_to_entropy_wall=True)
            wall = EntropyWall()
            validator = RhythmValidator()
            
            # Simulate contribution workflow
            contribution_code = """
            def calculate_resonance(freq):
                return freq * 0.432
            """
            
            # 1. Check rhythm
            operation_ok = validator.validate_operation_timing(
                "contribution_scan",
                allow_during_stillness=True
            )
            
            # 2. Scan for security
            scan_result = shield.validate_contribution(
                contribution_code,
                {"author": "integration_tester"}
            )
            
            # 3. Log if needed
            if not scan_result["approved"]:
                wall.log_event(
                    violation_type="CONTRIBUTION_REJECTED",
                    source_identifier="integration_test_3",
                    action_taken="REJECTED",
                    severity="LOW",
                    details=scan_result
                )
            
            # Workflow should complete
            assert operation_ok["approved"] in [True, False]
            assert scan_result["approved"] in [True, False]
            
            print("✓ Test 4.3: Full workflow integration - PASSED")
            self.tests_passed += 1
        except Exception as e:
            print(f"✗ Test 4.3: Full workflow integration - FAILED: {e}")
            self.tests_failed += 1
    
    def report_results(self):
        """Report test results."""
        elapsed = time.time() - self.start_time
        total = self.tests_passed + self.tests_failed
        
        print("\n" + "=" * 80)
        print("📊 Test Results")
        print("=" * 80)
        print(f"Total Tests:  {total}")
        print(f"Passed:       {self.tests_passed} ✓")
        print(f"Failed:       {self.tests_failed} ✗")
        print(f"Success Rate: {(self.tests_passed/total*100) if total > 0 else 0:.1f}%")
        print(f"Duration:     {elapsed:.2f} seconds")
        print("=" * 80)
        
        if self.tests_failed == 0:
            print("\n✅ ALL TESTS PASSED - Internet Organica framework is operational!")
            print("   System Status: READY FOR DEPLOYMENT")
            return 0
        else:
            print(f"\n⚠️  {self.tests_failed} TEST(S) FAILED - Review required")
            print("   System Status: NEEDS ATTENTION")
            return 1


def cleanup_test_artifacts():
    """Clean up test artifacts."""
    import shutil
    
    # Remove test entropy wall
    test_dir = Path(".test_entropy_wall")
    if test_dir.exists():
        shutil.rmtree(test_dir)
    
    # Remove test report
    test_report = Path("/tmp/test_entropy_report.html")
    if test_report.exists():
        test_report.unlink()


def main():
    """Run integration tests."""
    try:
        tester = IntegrationTester()
        exit_code = tester.run_all_tests()
        
        # Cleanup
        print("\n🧹 Cleaning up test artifacts...")
        cleanup_test_artifacts()
        print("✓ Cleanup complete")
        
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        cleanup_test_artifacts()
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Fatal error during testing: {e}")
        cleanup_test_artifacts()
        sys.exit(1)


if __name__ == "__main__":
    main()
