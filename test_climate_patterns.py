#!/usr/bin/env python3
"""
Test Suite for Climate Pattern NSR Extension
Tests the climate monitoring and prediction capabilities
"""

import time
import sys
from eternal_deposition import (
    EternalDepositionEngine, 
    ClimatePattern, 
    CLIMATE_DATA_RELIABILITY_THRESHOLD,
    CLIMATE_PATTERN_HISTORY
)


def test_climate_pattern_creation():
    """Test ClimatePattern data class creation and validation."""
    print("Test 1: ClimatePattern Creation")
    
    # Test reliable pattern
    pattern1 = ClimatePattern(
        timestamp=time.time(),
        temperature=0.5,
        humidity=0.6,
        pressure=0.7,
        reliability=0.9
    )
    assert pattern1.is_reliable(), "Pattern should be reliable with 0.9 reliability"
    
    # Test unreliable pattern
    pattern2 = ClimatePattern(
        timestamp=time.time(),
        temperature=0.5,
        humidity=0.6,
        pressure=0.7,
        reliability=0.7
    )
    assert not pattern2.is_reliable(), "Pattern should be unreliable with 0.7 reliability"
    
    print("  ✓ ClimatePattern creation and validation works correctly\n")


def test_node_climate_storage():
    """Test node climate pattern storage and history management."""
    print("Test 2: Node Climate Pattern Storage")
    
    engine = EternalDepositionEngine(initial_nodes=1)
    node = list(engine.nodes.values())[0]
    
    # Add patterns
    initial_count = 10
    for i in range(initial_count):
        pattern = ClimatePattern(
            timestamp=time.time() + i,
            temperature=0.5 + i * 0.01,
            humidity=0.6,
            pressure=0.7,
            reliability=0.9
        )
        node.add_climate_pattern(pattern)
    
    assert len(node.climate_patterns) == initial_count, \
        f"Expected {initial_count} patterns, got {len(node.climate_patterns)}"
    
    # Test history limit
    for i in range(CLIMATE_PATTERN_HISTORY + 50):
        pattern = ClimatePattern(
            timestamp=time.time() + i,
            temperature=0.5,
            humidity=0.6,
            pressure=0.7,
            reliability=0.9
        )
        node.add_climate_pattern(pattern)
    
    assert len(node.climate_patterns) == CLIMATE_PATTERN_HISTORY, \
        f"Pattern history should be limited to {CLIMATE_PATTERN_HISTORY}"
    
    print(f"  ✓ Node stores patterns with proper history limit ({CLIMATE_PATTERN_HISTORY})\n")


def test_reliable_data_filtering():
    """Test filtering of reliable climate data."""
    print("Test 3: Reliable Data Filtering")
    
    engine = EternalDepositionEngine(initial_nodes=1)
    node = list(engine.nodes.values())[0]
    
    # Add mix of reliable and unreliable patterns
    reliable_count = 0
    for i in range(10):
        reliability = 0.9 if i % 2 == 0 else 0.7  # Alternate reliable/unreliable
        pattern = ClimatePattern(
            timestamp=time.time() + i,
            temperature=0.5,
            humidity=0.6,
            pressure=0.7,
            reliability=reliability
        )
        node.add_climate_pattern(pattern)
        if reliability >= CLIMATE_DATA_RELIABILITY_THRESHOLD:
            reliable_count += 1
    
    reliable_data = node.get_reliable_climate_data()
    assert len(reliable_data) == reliable_count, \
        f"Expected {reliable_count} reliable patterns, got {len(reliable_data)}"
    
    print(f"  ✓ Correctly filters {reliable_count} reliable patterns from 10 total\n")


def test_climate_trend_prediction():
    """Test climate trend prediction using local intelligence."""
    print("Test 4: Climate Trend Prediction")
    
    engine = EternalDepositionEngine(initial_nodes=1)
    node = list(engine.nodes.values())[0]
    
    # Test with insufficient data
    trend = node.predict_climate_trend()
    assert trend is None, "Should return None with insufficient data"
    
    # Add warming trend
    for i in range(10):
        pattern = ClimatePattern(
            timestamp=time.time() + i,
            temperature=0.5 + i * 0.02,  # Increasing temperature
            humidity=0.6,
            pressure=0.7,
            reliability=0.9
        )
        node.add_climate_pattern(pattern)
    
    trend = node.predict_climate_trend()
    assert trend is not None, "Should return trend with sufficient data"
    assert trend > 0, f"Should detect warming trend, got {trend}"
    
    # Test cooling trend
    node.climate_patterns = []  # Clear for next test - direct access for testing only
    for i in range(10):
        pattern = ClimatePattern(
            timestamp=time.time() + i,
            temperature=0.8 - i * 0.02,  # Decreasing temperature
            humidity=0.6,
            pressure=0.7,
            reliability=0.9
        )
        node.add_climate_pattern(pattern)
    
    trend = node.predict_climate_trend()
    assert trend < 0, f"Should detect cooling trend, got {trend}"
    
    print(f"  ✓ Climate trend prediction works correctly\n")


def test_climate_pattern_generation():
    """Test climate pattern generation by engine."""
    print("Test 5: Climate Pattern Generation")
    
    engine = EternalDepositionEngine(initial_nodes=5)
    
    # Generate multiple patterns
    patterns = []
    for i in range(5):
        pattern = engine.generate_climate_pattern(time.time() + i * 100)
        patterns.append(pattern)
        
        # Validate pattern values are normalized
        assert 0 <= pattern.temperature <= 1, "Temperature should be normalized 0-1"
        assert 0 <= pattern.humidity <= 1, "Humidity should be normalized 0-1"
        assert 0 <= pattern.pressure <= 1, "Pressure should be normalized 0-1"
        assert 0 <= pattern.reliability <= 1, "Reliability should be normalized 0-1"
    
    print("  ✓ Climate patterns generated with proper normalization\n")


def test_climate_monitoring_integration():
    """Test climate monitoring integration in engine cycles."""
    print("Test 6: Climate Monitoring Integration")
    
    engine = EternalDepositionEngine(initial_nodes=10)
    
    # Force climate update
    engine.last_climate_update = 0  # Force update on next cycle
    
    # Execute cycle with climate update
    metrics = engine.execute_cycle()
    
    assert 'climate_data_points' in metrics, "Metrics should include climate data points"
    assert 'climate_monitoring' in metrics, "Metrics should include climate monitoring status"
    assert metrics['climate_monitoring'] == True, "Climate monitoring should be enabled"
    
    # Check that nodes received climate data
    total_patterns = sum(len(n.climate_patterns) for n in engine.nodes.values())
    assert total_patterns > 0, "Nodes should have climate patterns after update"
    
    print(f"  ✓ Climate monitoring integrated in engine cycles\n")


def test_climate_influence_on_optimization():
    """Test that climate patterns influence system optimization."""
    print("Test 7: Climate Influence on Optimization")
    
    engine = EternalDepositionEngine(initial_nodes=10)
    
    # Add climate data to nodes
    for node in engine.nodes.values():
        for i in range(10):
            pattern = ClimatePattern(
                timestamp=time.time() + i,
                temperature=0.5 + i * 0.01,
                humidity=0.6,
                pressure=0.7,
                reliability=0.9
            )
            node.add_climate_pattern(pattern)
    
    # Calculate climate influence
    influence = engine.calculate_climate_influence()
    
    assert influence != 0.0, "Climate should have influence when data is present"
    assert -0.02 <= influence <= 0.02, "Climate influence should be scaled properly"
    
    print(f"  ✓ Climate patterns influence optimization (influence: {influence:.6f})\n")


def test_status_reporting():
    """Test that status includes climate information."""
    print("Test 8: Status Reporting")
    
    engine = EternalDepositionEngine(initial_nodes=10)
    
    # Add some climate data
    engine.last_climate_update = 0
    engine.execute_cycle()
    
    status = engine.get_status()
    
    required_fields = [
        'climate_monitoring',
        'climate_data_total',
        'climate_data_reliable',
        'climate_reliability_ratio'
    ]
    
    for field in required_fields:
        assert field in status, f"Status should include '{field}'"
    
    assert isinstance(status['climate_monitoring'], bool), "climate_monitoring should be boolean"
    assert status['climate_reliability_ratio'] >= 0, "Reliability ratio should be non-negative"
    assert status['climate_reliability_ratio'] <= 1, "Reliability ratio should not exceed 1"
    
    print("  ✓ Status reporting includes all climate metrics\n")


def run_all_tests():
    """Run all test cases."""
    print("=" * 70)
    print("NSR Climate Pattern Extension - Test Suite")
    print("=" * 70 + "\n")
    
    tests = [
        test_climate_pattern_creation,
        test_node_climate_storage,
        test_reliable_data_filtering,
        test_climate_trend_prediction,
        test_climate_pattern_generation,
        test_climate_monitoring_integration,
        test_climate_influence_on_optimization,
        test_status_reporting
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ FAILED: {e}\n")
            failed += 1
        except Exception as e:
            print(f"  ✗ ERROR: {e}\n")
            failed += 1
    
    print("=" * 70)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 70 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
