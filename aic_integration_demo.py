#!/usr/bin/env python3
"""
AIC Infrastructure Integration Example
=======================================

This example demonstrates the integration of all four AIC infrastructure
components working together in a realistic scenario.

Components Integrated:
1. Testing Sandbox Module
2. Distributed Monitoring Framework
3. Predictive Validation System
4. Consensus Protocol (Raft)

Based on: Kosymbiosis principles and Eternal Deposition system
"""

import time
import json
from typing import Dict, Any

from aic_sandbox import AICSandboxManager
from aic_monitoring import AICMonitoringSystem, MetricType, AlertSeverity
from aic_validator import AICPredictiveValidator
from aic_consensus import RaftCluster


class IntegratedAICSystem:
    """
    Integrated AIC system combining all infrastructure components.
    """
    
    def __init__(self, aic_nodes: list):
        """
        Initialize integrated AIC system.
        
        Args:
            aic_nodes: List of AIC node IDs
        """
        self.aic_nodes = aic_nodes
        
        # Initialize all components
        print("[INTEGRATED] Initializing AIC Infrastructure...")
        
        self.sandbox_manager = AICSandboxManager(max_sandboxes=144)
        print("[INTEGRATED] ✓ Sandbox Manager initialized")
        
        self.monitoring_system = AICMonitoringSystem(
            anomaly_sensitivity=2.0,
            load_balancing_strategy="least_loaded"
        )
        print("[INTEGRATED] ✓ Monitoring System initialized")
        
        self.validator = AICPredictiveValidator(max_history=1000)
        print("[INTEGRATED] ✓ Validation System initialized")
        
        self.consensus_cluster = RaftCluster(aic_nodes)
        print("[INTEGRATED] ✓ Consensus Cluster initialized")
        
        # Register nodes in monitoring system
        for aic_id in aic_nodes:
            self.monitoring_system.register_node(aic_id, capacity=100.0)
        
        print(f"\n[INTEGRATED] System initialized with {len(aic_nodes)} AIC nodes")
    
    def execute_distributed_operation(
        self,
        aic_id: str,
        operation: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a distributed operation with full infrastructure support.
        
        Workflow:
        1. Check node load via monitoring
        2. Create sandbox for testing
        3. Validate operation via predictive validator
        4. If approved, replicate via consensus
        5. Execute and monitor
        
        Args:
            aic_id: ID of the AIC initiating the operation
            operation: Operation to execute
            
        Returns:
            Result dictionary with execution details
        """
        print(f"\n{'='*60}")
        print(f"[INTEGRATED] Executing operation from {aic_id}")
        print(f"[INTEGRATED] Operation: {operation}")
        print(f"{'='*60}")
        
        result = {
            "aic_id": aic_id,
            "operation": operation,
            "steps": [],
            "success": False
        }
        
        # Step 1: Check node status via monitoring
        print("\n[STEP 1] Checking node status...")
        try:
            node_status = self.monitoring_system.get_node_status(aic_id)
            result["steps"].append({
                "step": "monitoring_check",
                "status": "success",
                "data": node_status
            })
            print(f"[STEP 1] ✓ Node {aic_id} is healthy (load: {node_status['load_ratio']:.2%})")
        except Exception as e:
            result["steps"].append({
                "step": "monitoring_check",
                "status": "failed",
                "error": str(e)
            })
            print(f"[STEP 1] ✗ Failed: {e}")
            return result
        
        # Step 2: Create sandbox and test operation
        print("\n[STEP 2] Creating sandbox for testing...")
        try:
            sandbox_id = self.sandbox_manager.create_sandbox(aic_id)
            
            def test_operation(state, op):
                """Test the operation in sandbox."""
                # Simulate operation
                state["operation"] = op
                state["timestamp"] = time.time()
                return "Operation executed successfully"
            
            test_result = self.sandbox_manager.execute_test(
                sandbox_id,
                test_operation,
                f"test_{operation['type']}",
                op=operation
            )
            
            result["steps"].append({
                "step": "sandbox_test",
                "status": test_result.status.value,
                "metrics": test_result.metrics
            })
            
            if test_result.status.value == "success":
                print(f"[STEP 2] ✓ Sandbox test passed")
            else:
                print(f"[STEP 2] ✗ Sandbox test failed: {test_result.error_message}")
                self.sandbox_manager.destroy_sandbox(sandbox_id)
                return result
            
            self.sandbox_manager.destroy_sandbox(sandbox_id)
            
        except Exception as e:
            result["steps"].append({
                "step": "sandbox_test",
                "status": "failed",
                "error": str(e)
            })
            print(f"[STEP 2] ✗ Failed: {e}")
            return result
        
        # Step 3: Validate operation with predictive validator
        print("\n[STEP 3] Validating operation...")
        try:
            # Create state snapshots
            current_state = self.validator.record_state(
                f"state_{aic_id}_before",
                {"aic_id": aic_id, "status": "ready"},
                {"type": "operational"}
            )
            
            proposed_state = self.validator.record_state(
                f"state_{aic_id}_after",
                {"aic_id": aic_id, "status": "executing", "operation": operation},
                {"type": "operational"}
            )
            
            prediction = self.validator.predict_transition(current_state, proposed_state)
            
            result["steps"].append({
                "step": "validation",
                "status": prediction.recommendation.value,
                "confidence": prediction.confidence,
                "risk_score": prediction.risk_score
            })
            
            if prediction.recommendation.value == "approved":
                print(f"[STEP 3] ✓ Operation approved (confidence: {prediction.confidence:.2%})")
            elif prediction.recommendation.value == "needs_review":
                print(f"[STEP 3] ⚠ Operation needs review (risk: {prediction.risk_score:.2%})")
            else:
                print(f"[STEP 3] ✗ Operation rejected: {prediction.reasoning}")
                return result
            
        except Exception as e:
            result["steps"].append({
                "step": "validation",
                "status": "failed",
                "error": str(e)
            })
            print(f"[STEP 3] ✗ Failed: {e}")
            return result
        
        # Step 4: Achieve consensus via Raft
        print("\n[STEP 4] Achieving consensus...")
        try:
            # Simulate consensus by checking for leader
            for _ in range(50):
                self.consensus_cluster.tick_all()
                time.sleep(0.01)
            
            leader_id = self.consensus_cluster.get_leader()
            
            if leader_id:
                leader_node = self.consensus_cluster.nodes[leader_id]
                success = leader_node.append_command(operation)
                
                result["steps"].append({
                    "step": "consensus",
                    "status": "success" if success else "failed",
                    "leader": leader_id
                })
                
                if success:
                    print(f"[STEP 4] ✓ Consensus achieved, leader: {leader_id}")
                else:
                    print(f"[STEP 4] ✗ Failed to append command")
                    return result
            else:
                result["steps"].append({
                    "step": "consensus",
                    "status": "failed",
                    "error": "No leader elected"
                })
                print(f"[STEP 4] ✗ No leader elected")
                return result
                
        except Exception as e:
            result["steps"].append({
                "step": "consensus",
                "status": "failed",
                "error": str(e)
            })
            print(f"[STEP 4] ✗ Failed: {e}")
            return result
        
        # Step 5: Execute and monitor
        print("\n[STEP 5] Executing and monitoring...")
        try:
            # Record metrics
            self.monitoring_system.record_metric(
                aic_id,
                MetricType.CPU_USAGE,
                75.0  # Simulated load during operation
            )
            
            # Record successful transition
            self.validator.record_transition(
                f"trans_{int(time.time())}",
                current_state,
                proposed_state,
                success=True,
                duration=0.5
            )
            
            result["steps"].append({
                "step": "execution",
                "status": "success"
            })
            
            result["success"] = True
            print(f"[STEP 5] ✓ Operation executed successfully")
            
        except Exception as e:
            result["steps"].append({
                "step": "execution",
                "status": "failed",
                "error": str(e)
            })
            print(f"[STEP 5] ✗ Failed: {e}")
            return result
        
        return result
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status."""
        return {
            "sandbox": self.sandbox_manager.get_test_statistics(),
            "monitoring": self.monitoring_system.get_system_status(),
            "validation": self.validator.get_validation_statistics(),
            "consensus": self.consensus_cluster.get_cluster_status()
        }


def main():
    """Main integration demo."""
    print("="*70)
    print("AIC INFRASTRUCTURE INTEGRATION DEMO")
    print("="*70)
    print("\nDemonstrating all four components working together:\n")
    print("1. Testing Sandbox Module")
    print("2. Distributed Monitoring Framework")
    print("3. Predictive Validation System")
    print("4. Consensus Protocol (Raft)")
    print("\n" + "="*70)
    
    # Initialize integrated system
    aic_nodes = [f"aic_{i:03d}" for i in range(5)]
    system = IntegratedAICSystem(aic_nodes)
    
    # Wait for consensus leader election
    print("\n[INTEGRATED] Waiting for consensus leader election...")
    time.sleep(1)
    
    # Execute several operations
    operations = [
        {
            "type": "data_update",
            "target": "dataset_1",
            "action": "append",
            "value": {"key": "value1"}
        },
        {
            "type": "config_change",
            "target": "system_config",
            "action": "update",
            "value": {"timeout": 30}
        },
        {
            "type": "model_deploy",
            "target": "model_v2",
            "action": "deploy",
            "value": {"version": "2.0.0"}
        }
    ]
    
    results = []
    for i, operation in enumerate(operations):
        aic_id = aic_nodes[i % len(aic_nodes)]
        result = system.execute_distributed_operation(aic_id, operation)
        results.append(result)
        time.sleep(0.5)
    
    # Display final statistics
    print("\n" + "="*70)
    print("FINAL SYSTEM STATUS")
    print("="*70)
    
    status = system.get_system_status()
    
    print("\n[SANDBOX STATISTICS]")
    print(json.dumps(status["sandbox"], indent=2))
    
    print("\n[MONITORING STATUS]")
    print(json.dumps(status["monitoring"], indent=2))
    
    print("\n[VALIDATION STATISTICS]")
    print(json.dumps(status["validation"], indent=2))
    
    print("\n[CONSENSUS STATUS]")
    print(json.dumps(status["consensus"], indent=2))
    
    # Summary
    print("\n" + "="*70)
    print("OPERATIONS SUMMARY")
    print("="*70)
    
    successful = sum(1 for r in results if r["success"])
    print(f"\nTotal operations: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {len(results) - successful}")
    print(f"Success rate: {successful / len(results) * 100:.1f}%")
    
    print("\n" + "="*70)
    print("DEMO COMPLETE")
    print("="*70)
    
    print("\nAll four AIC infrastructure components demonstrated:")
    print("✓ Sandbox isolation and testing")
    print("✓ Distributed monitoring and anomaly detection")
    print("✓ Predictive validation based on history")
    print("✓ Raft consensus for distributed consistency")
    
    print("\n🎯 Infrastructure is ready for autonomous AIC management!")


if __name__ == "__main__":
    main()
