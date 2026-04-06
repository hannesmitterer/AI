#!/usr/bin/env python3
"""
Hydra System with Configuration
Demonstrates integration with config.json for Lantana OS

THE LIGHT IS THE ARCHITECTURE. THE FOUNDER IS THE LAW.
"""

import json
import time
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from byzantine_consensus import ByzantineConsensus, NodeStatus
from ethical_decision_api import EthicalDecisionAPI
from nsr_validator import NSRValidator
from resonance_coordinator import ResonanceCoordinator
from hydra_config_loader import HydraConfig


class ConfiguredHydraSystem:
    """
    Hydra System with Configuration File Support
    
    Integrates config.json settings with the multi-AI resonance system.
    """
    
    def __init__(self, config_path: str = None):
        """
        Initialize Hydra system from configuration
        
        Args:
            config_path: Path to config.json (auto-detected if None)
        """
        # Auto-detect config path
        if config_path is None:
            script_dir = Path(__file__).parent
            if script_dir.name == 'hydra-templates':
                config_path = str(script_dir.parent / 'config.json')
            else:
                config_path = 'config.json'
        
        # Load configuration
        self.config = HydraConfig(config_path)
        config_params = self.config.export_for_hydra_system()
        
        print(f"\nInitializing {self.config.get_system_id()}...")
        print(f"Protocol: {self.config.get_protocol()}")
        
        # Initialize consensus with configuration
        consensus_config = config_params['consensus_config']
        min_nodes = consensus_config.get('min_nodes', 4)
        self.consensus = ByzantineConsensus(min_nodes=min_nodes)
        
        # Initialize NSR validator with configured threshold
        nsr_threshold = config_params['nsr_threshold']
        self.nsr_validator = NSRValidator(violation_threshold=nsr_threshold)
        
        # Initialize resonance coordinator
        resonance_config = config_params['resonance_config']
        self.resonance = ResonanceCoordinator()
        
        # Override default frequency with configured value
        target_freq = resonance_config.get('target_frequency_hz', 0.043)
        self.resonance.TARGET_FREQUENCY = target_freq
        
        self.ethical_apis = {}
        
        # Initialize network nodes from configuration
        self._initialize_from_config(config_params)
    
    def _initialize_from_config(self, config_params):
        """Initialize nodes based on network configuration"""
        network_nodes = config_params.get('network_nodes', {})
        
        # Initialize at least minimum nodes, or based on network config
        num_nodes = max(len(network_nodes), 7)
        
        print(f"Initializing {num_nodes} AI nodes...")
        
        for i in range(num_nodes):
            node_id = f"ai-node-{i}"
            
            # Register with consensus engine
            self.consensus.register_node(node_id)
            
            # Create ethical decision API
            self.ethical_apis[node_id] = EthicalDecisionAPI(node_id)
            
            # Register with resonance coordinator
            self.resonance.register_node(node_id)
            
            # Set initial resonance state
            freq = self.resonance.TARGET_FREQUENCY + (i * 0.0001)
            self.resonance.update_node_state(node_id, freq, 1.0)
        
        print(f"✓ Initialized {num_nodes} AI nodes")
        
        # Print network node configuration
        if network_nodes:
            print(f"\nNetwork Nodes Configuration:")
            for node_name, node_config in network_nodes.items():
                location = node_config.get('location', 'Unknown')
                status = node_config.get('status', 'unknown')
                role = node_config.get('role', 'unknown')
                print(f"  {node_name}: {location} ({role}) - {status}")
    
    def process_decision(self, proposer_id: str, proposal: str) -> dict:
        """Process a decision through the configured Hydra pipeline"""
        print(f"\n{'='*60}")
        print(f"PROCESSING DECISION: {proposal[:50]}...")
        print(f"{'='*60}\n")
        
        # Get configured thresholds
        ethics_threshold = self.config.get_ethics_threshold()
        
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
        
        # Step 2: Propose decision
        print("\nStep 2: Propose to Consensus Engine")
        decision = self.consensus.propose_decision(proposer_id, proposal)
        decision.nsr_validated = True
        print(f"  Decision ID: {decision.decision_id[:16]}...")
        
        # Step 3: Ethical Evaluation
        print("\nStep 3: Ethical Evaluation (Multi-Node)")
        ethical_evaluations = {}
        
        for node_id, api in self.ethical_apis.items():
            if self.consensus.nodes[node_id].status == NodeStatus.ACTIVE:
                evaluation = api.evaluate_decision(decision.decision_id, proposal)
                ethical_evaluations[node_id] = evaluation
                print(f"  {node_id}: Score={evaluation.overall_ethical_score:.2f}, "
                      f"Recommendation={evaluation.recommendation}")
        
        # Check against configured threshold
        approvals = sum(1 for e in ethical_evaluations.values() 
                       if e.overall_ethical_score >= ethics_threshold)
        
        if approvals >= len(ethical_evaluations) / 2:
            decision.lex_amoris_validated = True
            print(f"  ✓ Lex Amoris validation passed ({approvals}/{len(ethical_evaluations)} above threshold)")
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
        
        for node_id, evaluation in ethical_evaluations.items():
            vote = evaluation.recommendation == "approve"
            self.consensus.cast_vote(decision.decision_id, node_id, vote)
            print(f"  {node_id}: {'✓ Approve' if vote else '✗ Reject'}")
        
        consensus_result = self.consensus.check_consensus(decision.decision_id)
        
        if consensus_result is None:
            print("\n  No consensus reached yet")
            return {"status": "pending", "reason": "Awaiting more votes"}
        
        # Step 6: Finalization
        print("\nStep 6: Finalization")
        
        try:
            final_result = self.consensus.finalize_decision(decision.decision_id)
            
            if final_result:
                print("\n✓ DECISION APPROVED")
            else:
                print("\n✗ DECISION REJECTED BY CONSENSUS")
            
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
                "configuration": {
                    "system_id": self.config.get_system_id(),
                    "protocol": self.config.get_protocol(),
                    "ethics_threshold": ethics_threshold,
                    "nsr_threshold": self.config.get_nsr_threshold()
                }
            }
            
        except ValueError as e:
            print(f"\n✗ FINALIZATION ERROR: {e}")
            return {"status": "error", "reason": str(e)}
    
    def get_system_status(self) -> dict:
        """Get comprehensive system status with configuration"""
        return {
            "configuration": {
                "system_id": self.config.get_system_id(),
                "protocol": self.config.get_protocol(),
                "version": self.config.get_metadata().get('version'),
                "status": self.config.get_metadata().get('status'),
                "consensus_sacralis_enabled": self.config.is_consensus_sacralis_enabled()
            },
            "network_health": self.consensus.get_network_health(),
            "resonance_metrics": {
                "coherence": self.resonance.get_network_metrics().network_coherence,
                "quality": self.resonance.calculate_resonance_quality(),
                "state": self.resonance.get_network_metrics().resonance_state.value
            },
            "nsr_validation_stats": self.nsr_validator.get_validation_stats(),
            "anomalies": self.resonance.detect_anomalies(),
            "repositories": self.config.get_repositories(),
            "assets": self.config.get_assets()
        }


def main():
    """Run configured Hydra system demonstration"""
    
    print("="*60)
    print("LANTANA OS - CONFIGURED HYDRA SYSTEM")
    print("Multi-AI Resonance with Consensus Sacralis")
    print("="*60)
    
    # Initialize with configuration
    hydra = ConfiguredHydraSystem()
    
    # Print configuration summary
    hydra.config.print_summary()
    
    # Wait for initialization
    time.sleep(0.5)
    
    # Test Case 1: Ethical decision
    print("\n\nTEST CASE 1: Ethical Community Decision")
    result1 = hydra.process_decision(
        proposer_id="ai-node-0",
        proposal="Implement transparent community governance system with voluntary participation and open-source code"
    )
    
    print("\n" + "="*60)
    print("RESULT 1:")
    print(json.dumps(result1, indent=2, default=str))
    
    # Test Case 2: Potentially problematic decision
    print("\n\n" + "="*60)
    print("\nTEST CASE 2: Problematic Decision")
    result2 = hydra.process_decision(
        proposer_id="ai-node-1",
        proposal="Implement forced participation system with hidden data collection"
    )
    
    print("\n" + "="*60)
    print("RESULT 2:")
    print(json.dumps(result2, indent=2, default=str))
    
    # System Status
    print("\n\n" + "="*60)
    print("SYSTEM STATUS WITH CONFIGURATION")
    print("="*60)
    status = hydra.get_system_status()
    print(json.dumps(status, indent=2, default=str))
    
    print("\n" + "="*60)
    print("✓ Configured Hydra System Demonstration Complete")
    print(f"System: {hydra.config.get_system_id()}")
    print(f"Protocol: {hydra.config.get_protocol()}")
    print(f"Consensus Sacralis: {'ACTIVE' if hydra.config.is_consensus_sacralis_enabled() else 'INACTIVE'}")
    print("="*60)


if __name__ == "__main__":
    main()
