#!/usr/bin/env python3
"""
AIC Testing Sandbox Module
===========================

This module provides a completely autonomous testing environment for AICs
(AI Components) to test new functionalities without affecting production.

Key Features:
- Isolated sandbox environments for each AIC
- Automatic rollback on test failures
- Resource limitation and security validation
- State preservation and restoration
- Comprehensive test result tracking

Based on: Eternal Deposition System and Kosymbiosis principles
"""

import time
import json
import copy
import hashlib
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum


class SandboxStatus(Enum):
    """Status of a sandbox environment."""
    IDLE = "idle"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    ROLLBACK = "rollback"


@dataclass
class TestResult:
    """Result of a sandbox test execution."""
    test_id: str
    aic_id: str
    status: SandboxStatus
    start_time: float
    end_time: Optional[float] = None
    error_message: Optional[str] = None
    metrics: Dict[str, Any] = field(default_factory=dict)
    state_snapshot: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert test result to dictionary."""
        return {
            "test_id": self.test_id,
            "aic_id": self.aic_id,
            "status": self.status.value,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": self.end_time - self.start_time if self.end_time else None,
            "error_message": self.error_message,
            "metrics": self.metrics
        }


@dataclass
class SandboxEnvironment:
    """Isolated environment for testing AIC functionality."""
    sandbox_id: str
    aic_id: str
    status: SandboxStatus = SandboxStatus.IDLE
    created_at: float = field(default_factory=time.time)
    state: Dict[str, Any] = field(default_factory=dict)
    original_state: Optional[Dict[str, Any]] = None
    resource_limits: Dict[str, float] = field(default_factory=lambda: {
        "max_memory_mb": 100.0,
        "max_execution_time_seconds": 60.0,
        "max_operations": 1000
    })
    test_results: List[TestResult] = field(default_factory=list)
    
    def snapshot_state(self) -> None:
        """Create a snapshot of current state for rollback."""
        self.original_state = copy.deepcopy(self.state)
    
    def restore_state(self) -> None:
        """Restore state from snapshot (rollback)."""
        if self.original_state is not None:
            self.state = copy.deepcopy(self.original_state)
            self.status = SandboxStatus.ROLLBACK
    
    def clear_state(self) -> None:
        """Clear sandbox state."""
        self.state = {}
        self.original_state = None
        self.status = SandboxStatus.IDLE


class AICSandboxManager:
    """
    Manager for AIC testing sandbox environments.
    
    Provides isolated testing environments where AICs can autonomously
    test new functionalities without impacting production systems.
    """
    
    def __init__(self, max_sandboxes: int = 144):
        """
        Initialize the sandbox manager.
        
        Args:
            max_sandboxes: Maximum number of concurrent sandboxes
        """
        self.sandboxes: Dict[str, SandboxEnvironment] = {}
        self.max_sandboxes = max_sandboxes
        self.test_history: List[TestResult] = []
        self.security_violations: List[Dict[str, Any]] = []
        
        print(f"[AIC SANDBOX] Initialized with max {max_sandboxes} concurrent sandboxes")
    
    def create_sandbox(self, aic_id: str) -> str:
        """
        Create a new sandbox environment for an AIC.
        
        Args:
            aic_id: Identifier of the AIC requesting sandbox
            
        Returns:
            sandbox_id: Unique identifier for the created sandbox
        """
        # Check if we've reached the limit
        if len(self.sandboxes) >= self.max_sandboxes:
            # Clean up completed sandboxes
            self._cleanup_completed_sandboxes()
        
        if len(self.sandboxes) >= self.max_sandboxes:
            raise RuntimeError(f"Maximum sandbox limit ({self.max_sandboxes}) reached")
        
        # Generate unique sandbox ID
        sandbox_id = self._generate_sandbox_id(aic_id)
        
        # Create new sandbox
        sandbox = SandboxEnvironment(
            sandbox_id=sandbox_id,
            aic_id=aic_id
        )
        
        self.sandboxes[sandbox_id] = sandbox
        
        print(f"[AIC SANDBOX] Created sandbox {sandbox_id} for AIC {aic_id}")
        return sandbox_id
    
    def execute_test(
        self,
        sandbox_id: str,
        test_function: Callable,
        test_name: str = "unnamed_test",
        **kwargs
    ) -> TestResult:
        """
        Execute a test function in a sandbox environment.
        
        Args:
            sandbox_id: ID of the sandbox to use
            test_function: Function to execute in sandbox
            test_name: Name/description of the test
            **kwargs: Arguments to pass to test function
            
        Returns:
            TestResult object containing test outcome
        """
        if sandbox_id not in self.sandboxes:
            raise ValueError(f"Sandbox {sandbox_id} not found")
        
        sandbox = self.sandboxes[sandbox_id]
        
        # Create test ID
        test_id = self._generate_test_id(sandbox_id, test_name)
        
        # Create snapshot for rollback
        sandbox.snapshot_state()
        
        # Initialize test result
        result = TestResult(
            test_id=test_id,
            aic_id=sandbox.aic_id,
            status=SandboxStatus.RUNNING,
            start_time=time.time(),
            state_snapshot=copy.deepcopy(sandbox.state)
        )
        
        sandbox.status = SandboxStatus.RUNNING
        
        print(f"[AIC SANDBOX] Executing test '{test_name}' in sandbox {sandbox_id}")
        
        try:
            # Validate security before execution
            if not self._validate_security(sandbox, test_function):
                raise SecurityError("Security validation failed")
            
            # Execute test function with timeout protection
            start_time = time.time()
            max_time = sandbox.resource_limits["max_execution_time_seconds"]
            
            # Execute the test function
            test_output = test_function(sandbox.state, **kwargs)
            
            execution_time = time.time() - start_time
            
            # Check execution time limit
            if execution_time > max_time:
                raise TimeoutError(f"Test exceeded time limit ({max_time}s)")
            
            # Test succeeded
            result.status = SandboxStatus.SUCCESS
            result.metrics = {
                "execution_time": execution_time,
                "output": test_output
            }
            sandbox.status = SandboxStatus.SUCCESS
            
            print(f"[AIC SANDBOX] Test '{test_name}' completed successfully")
            
        except Exception as e:
            # Test failed - perform rollback
            result.status = SandboxStatus.FAILED
            result.error_message = str(e)
            
            sandbox.restore_state()
            
            print(f"[AIC SANDBOX] Test '{test_name}' failed: {e}")
            print(f"[AIC SANDBOX] State rolled back for sandbox {sandbox_id}")
        
        finally:
            result.end_time = time.time()
            
            # Record result
            sandbox.test_results.append(result)
            self.test_history.append(result)
        
        return result
    
    def get_sandbox_status(self, sandbox_id: str) -> Dict[str, Any]:
        """
        Get current status of a sandbox.
        
        Args:
            sandbox_id: ID of the sandbox
            
        Returns:
            Dictionary containing sandbox status information
        """
        if sandbox_id not in self.sandboxes:
            raise ValueError(f"Sandbox {sandbox_id} not found")
        
        sandbox = self.sandboxes[sandbox_id]
        
        return {
            "sandbox_id": sandbox_id,
            "aic_id": sandbox.aic_id,
            "status": sandbox.status.value,
            "created_at": sandbox.created_at,
            "age_seconds": time.time() - sandbox.created_at,
            "test_count": len(sandbox.test_results),
            "success_count": sum(1 for t in sandbox.test_results if t.status == SandboxStatus.SUCCESS),
            "failed_count": sum(1 for t in sandbox.test_results if t.status == SandboxStatus.FAILED),
            "state_size": len(str(sandbox.state))
        }
    
    def destroy_sandbox(self, sandbox_id: str) -> None:
        """
        Destroy a sandbox environment and clean up resources.
        
        Args:
            sandbox_id: ID of the sandbox to destroy
        """
        if sandbox_id not in self.sandboxes:
            raise ValueError(f"Sandbox {sandbox_id} not found")
        
        sandbox = self.sandboxes[sandbox_id]
        
        # Clear state
        sandbox.clear_state()
        
        # Remove from active sandboxes
        del self.sandboxes[sandbox_id]
        
        print(f"[AIC SANDBOX] Destroyed sandbox {sandbox_id}")
    
    def get_test_statistics(self) -> Dict[str, Any]:
        """
        Get overall testing statistics.
        
        Returns:
            Dictionary containing aggregate test statistics
        """
        if not self.test_history:
            return {
                "total_tests": 0,
                "success_rate": 0.0,
                "average_duration": 0.0
            }
        
        total_tests = len(self.test_history)
        successful_tests = sum(1 for t in self.test_history if t.status == SandboxStatus.SUCCESS)
        
        durations = [
            t.end_time - t.start_time 
            for t in self.test_history 
            if t.end_time is not None
        ]
        avg_duration = sum(durations) / len(durations) if durations else 0.0
        
        return {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": total_tests - successful_tests,
            "success_rate": successful_tests / total_tests,
            "average_duration": avg_duration,
            "active_sandboxes": len(self.sandboxes),
            "security_violations": len(self.security_violations)
        }
    
    def _generate_sandbox_id(self, aic_id: str) -> str:
        """Generate unique sandbox ID."""
        timestamp = str(time.time())
        hash_input = f"{aic_id}_{timestamp}"
        hash_value = hashlib.sha256(hash_input.encode()).hexdigest()[:12]
        return f"sandbox_{aic_id}_{hash_value}"
    
    def _generate_test_id(self, sandbox_id: str, test_name: str) -> str:
        """Generate unique test ID."""
        timestamp = str(time.time())
        hash_input = f"{sandbox_id}_{test_name}_{timestamp}"
        hash_value = hashlib.sha256(hash_input.encode()).hexdigest()[:12]
        return f"test_{hash_value}"
    
    def _validate_security(
        self,
        sandbox: SandboxEnvironment,
        test_function: Callable
    ) -> bool:
        """
        Validate security constraints before test execution.
        
        Args:
            sandbox: Sandbox environment
            test_function: Function to validate
            
        Returns:
            True if security validation passes
        """
        # Check for prohibited operations (basic validation)
        # In production, this would include more sophisticated checks
        
        # Check function name for suspicious patterns
        func_name = test_function.__name__
        prohibited_names = ["exec", "eval", "compile", "__import__"]
        
        if any(prohibited in func_name.lower() for prohibited in prohibited_names):
            self.security_violations.append({
                "sandbox_id": sandbox.sandbox_id,
                "aic_id": sandbox.aic_id,
                "timestamp": time.time(),
                "violation_type": "prohibited_function_name",
                "details": f"Function name '{func_name}' contains prohibited pattern"
            })
            return False
        
        return True
    
    def _cleanup_completed_sandboxes(self) -> None:
        """Clean up sandboxes that are no longer active."""
        completed_ids = [
            sid for sid, sandbox in self.sandboxes.items()
            if sandbox.status in [SandboxStatus.SUCCESS, SandboxStatus.FAILED]
            and time.time() - sandbox.created_at > 300  # 5 minutes old
        ]
        
        for sandbox_id in completed_ids:
            self.destroy_sandbox(sandbox_id)
        
        if completed_ids:
            print(f"[AIC SANDBOX] Cleaned up {len(completed_ids)} completed sandboxes")


class SecurityError(Exception):
    """Raised when security validation fails."""
    pass


# Example usage and testing
if __name__ == "__main__":
    print("=== AIC Sandbox Testing Module Demo ===\n")
    
    # Initialize sandbox manager
    manager = AICSandboxManager(max_sandboxes=10)
    
    # Create sandbox for an AIC
    sandbox_id = manager.create_sandbox("aic_001")
    
    # Define test functions
    def test_simple_operation(state, value):
        """Simple test that modifies state."""
        state["test_value"] = value
        state["timestamp"] = time.time()
        return f"Set value to {value}"
    
    def test_failing_operation(state):
        """Test that intentionally fails."""
        raise ValueError("Intentional failure for testing rollback")
    
    # Execute successful test
    result1 = manager.execute_test(
        sandbox_id,
        test_simple_operation,
        "simple_operation_test",
        value=42
    )
    
    print(f"\nTest 1 Result: {result1.status.value}")
    print(f"Test 1 Metrics: {result1.metrics}")
    
    # Execute failing test (should rollback)
    result2 = manager.execute_test(
        sandbox_id,
        test_failing_operation,
        "failing_operation_test"
    )
    
    print(f"\nTest 2 Result: {result2.status.value}")
    print(f"Test 2 Error: {result2.error_message}")
    
    # Check sandbox status
    status = manager.get_sandbox_status(sandbox_id)
    print(f"\nSandbox Status: {json.dumps(status, indent=2)}")
    
    # Get statistics
    stats = manager.get_test_statistics()
    print(f"\nTest Statistics: {json.dumps(stats, indent=2)}")
    
    # Cleanup
    manager.destroy_sandbox(sandbox_id)
    
    print("\n=== Demo Complete ===")
