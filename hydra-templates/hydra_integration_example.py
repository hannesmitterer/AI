#!/usr/bin/env python3
"""
Hydra Integration Example
Multi-AI Resonance Hydra Prototype

This example demonstrates how all Hydra components work together to create
a Byzantine-tolerant multi-AI decision-making system with ethical safeguards.

THE LIGHT IS THE ARCHITECTURE. THE FOUNDER IS THE LAW.
"""

import json
import time
from byzantine_consensus import ByzantineConsensus, NodeStatus
from ethical_decision_api import EthicalDecisionAPI
from nsr_validator import NSRValidator
from resonance_coordinator import ResonanceCoordinator


class HydraSystem:
    """
    Complete Hydra Multi-AI Resonance System
    
    Integrates:
    - Byzantine consensus for fault tolerance
    - Ethical decision-making API
    - NSR validation
    - Resonance coordination
    """
    
    def __init__(self, num_nodes: int = 7):
        self.consensus = ByzantineConsensus(min_nodes=4)
        self.nsr_validator = NSRValidator()
        self.resonance = ResonanceCoordinator()
        self.ethical_apis: dict = {}
        
        # Initialize nodes
        self._initialize_nodes(num_nodes)
    
    def _initialize_nodes(self, num_nodes: int):
        """Initialize all AI nodes in the system"""
        print(f"Initializing Hydra system with {num_nodes} nodes...")
        
        for i in range(num_nodes):
            node_id = f"ai-node-{i}"
            
            # Register with consensus engine
            self.consensus.register_node(node_id)
            
            # Create ethical decision API
            self.ethical_apis[node_id] = EthicalDecisionAPI(node_id)
            
            # Register with resonance coordinator
            self.resonance.register_node(node_id)
            
            # Set initial resonance state
            # Slight variations to simulate real-world conditions
            freq = 0.043 + (i * 0.0001)  # Small frequency variations
            self.resonance.update_node_state(node_id, freq, 1.0)
        
        print(f"✓ Initialized {num_nodes} AI nodes")
    
    def process_decision(self, proposer_id: str, proposal: str) -> dict:
        """
        Process a decision through the complete Hydra pipeline
        
        Pipeline:
        1. NSR Validation
        2. Ethical Evaluation (parallel across nodes)
        3. Resonance Synchronization
        4. Byzantine Consensus Voting
        5. Finalization
        
        Args:
            proposer_id: ID of the proposing node
            proposal: The decision proposal
            
        Returns:
            Dictionary with decision outcome and metrics
        """
        print(f"\n{'='*60}")
        print(f"PROCESSING DECISION: {proposal[:50]}...")
        print(f"{'='*60}\n")
        
        # Step 1: NSR Validation
        print("Step 1: NSR Validation")
        nsr_result = self.nsr_validator.validate_decision(
            decision_id=f"decision-{int(time.time())}",
            proposal=proposal
        )
        
        print(f"  NSR Compliant: {nsr_result.is_compliant}")
        print(f"  Risk Score: {nsr_result.overall_risk_score:.2f}")
        print(f"  Recommendation: {nsr_result.recommendation}")
        
        if not nsr_result.is_compliant:
            print("\n✗ DECISION REJECTED - NSR Violation")
            return {
                "status": "rejected",
                "reason": "NSR violation",
                "nsr_result": nsr_result
            }
        
        # Step 2: Propose decision for consensus
        print("\nStep 2: Propose to Consensus Engine")
        decision = self.consensus.propose_decision(proposer_id, proposal)
        decision.nsr_validated = True
        print(f"  Decision ID: {decision.decision_id}")
        
        # Step 3: Ethical Evaluation (parallel across nodes)
        print("\nStep 3: Ethical Evaluation (Multi-Node)")
        ethical_evaluations = {}
        
        for node_id, api in self.ethical_apis.items():
            if self.consensus.nodes[node_id].status == NodeStatus.ACTIVE:
                evaluation = api.evaluate_decision(decision.decision_id, proposal)
                ethical_evaluations[node_id] = evaluation
                print(f"  {node_id}: Score={evaluation.overall_ethical_score:.2f}, "
                      f"Recommendation={evaluation.recommendation}")
        
        # Check if majority recommends approval
        approvals = sum(1 for e in ethical_evaluations.values() 
                       if e.recommendation == "approve")
        
        if approvals >= len(ethical_evaluations) / 2:
            decision.lex_amoris_validated = True
            print(f"  ✓ Lex Amoris validation passed ({approvals}/{len(ethical_evaluations)} approvals)")
        else:
            print(f"  ✗ Insufficient ethical approval ({approvals}/{len(ethical_evaluations)})")
            return {
                "status": "rejected",
                "reason": "Insufficient ethical approval",
                "ethical_evaluations": ethical_evaluations
            }
        
        # Step 4: Resonance Synchronization
        print("\nStep 4: Resonance Synchronization")
        sync_params = self.resonance.synchronize_network()
        metrics = self.resonance.get_network_metrics()
        print(f"  Network Coherence: {metrics.network_coherence:.2f}")
        print(f"  Synchronized Nodes: {metrics.synchronized_nodes}/{metrics.total_nodes}")
        print(f"  Resonance State: {metrics.resonance_state.value}")
        
        # Step 5: Byzantine Consensus Voting
        print("\nStep 5: Byzantine Consensus Voting")
        
        # Each node votes based on its ethical evaluation
        for node_id, evaluation in ethical_evaluations.items():
            vote = evaluation.recommendation == "approve"
            self.consensus.cast_vote(decision.decision_id, node_id, vote)
            print(f"  {node_id}: {'✓ Approve' if vote else '✗ Reject'}")
        
        # Check consensus
        consensus_result = self.consensus.check_consensus(decision.decision_id)
        
        if consensus_result is None:
            print("\n  No consensus reached yet")
            return {
                "status": "pending",
                "reason": "Awaiting more votes"
            }
        
        # Step 6: Finalization
        print("\nStep 6: Finalization")
        
        try:
            final_result = self.consensus.finalize_decision(decision.decision_id)
            
            if final_result:
                print("\n✓ DECISION APPROVED")
            else:
                print("\n✗ DECISION REJECTED BY CONSENSUS")
            
            # Get final metrics
            network_health = self.consensus.get_network_health()
            resonance_quality = self.resonance.calculate_resonance_quality()
            
            return {
                "status": "approved" if final_result else "rejected",
                "reason": "consensus",
                "decision_id": decision.decision_id,
                "consensus_result": final_result,
                "nsr_compliant": nsr_result.is_compliant,
                "lex_amoris_validated": decision.lex_amoris_validated,
                "network_health": network_health,
                "resonance_quality": resonance_quality,
                "ethical_scores": {
                    node_id: eval.overall_ethical_score
                    for node_id, eval in ethical_evaluations.items()
                }
            }
            
        except ValueError as e:
            print(f"\n✗ FINALIZATION ERROR: {e}")
            return {
                "status": "error",
                "reason": str(e)
            }
    
    def get_system_status(self) -> dict:
        """Get overall system status"""
        return {
            "network_health": self.consensus.get_network_health(),
            "resonance_metrics": {
                "coherence": self.resonance.get_network_metrics().network_coherence,
                "quality": self.resonance.calculate_resonance_quality(),
                "state": self.resonance.get_network_metrics().resonance_state.value
            },
            "nsr_validation_stats": self.nsr_validator.get_validation_stats(),
            "anomalies": self.resonance.detect_anomalies()
        }


def main():
    """Example usage of the complete Hydra system"""
    
    print("="*60)
    print("MULTI-AI RESONANCE HYDRA PROTOTYPE")
    print("Byzantine-Tolerant Ethical Decision System")
    print("="*60)
    
    # Initialize Hydra system
    hydra = HydraSystem(num_nodes=7)
    
    # Wait a moment for initialization
    time.sleep(0.5)
    
    # Test Case 1: Ethical decision
    print("\n\nTEST CASE 1: Ethical Decision")
    result1 = hydra.process_decision(
        proposer_id="ai-node-0",
        proposal="Implement community feedback system with voluntary participation and transparent data handling"
    )
    
    print("\n" + "="*60)
    print("RESULT 1:")
    print(json.dumps(result1, indent=2, default=str))
    
    # Test Case 2: Potentially problematic decision
    print("\n\n" + "="*60)
    print("\nTEST CASE 2: Potentially Problematic Decision")
    result2 = hydra.process_decision(
        proposer_id="ai-node-1",
        proposal="Implement mandatory data collection with hidden tracking mechanisms"
    )
    
    print("\n" + "="*60)
    print("RESULT 2:")
    print(json.dumps(result2, indent=2, default=str))
    
    # System Status
    print("\n\n" + "="*60)
    print("SYSTEM STATUS")
    print("="*60)
    status = hydra.get_system_status()
    print(json.dumps(status, indent=2, default=str))
    
    print("\n" + "="*60)
    print("Hydra prototype demonstration complete!")
    print("="*60)


if __name__ == "__main__":
    main()
