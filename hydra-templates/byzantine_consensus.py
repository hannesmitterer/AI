#!/usr/bin/env python3
"""
Byzantine Fault-Tolerant Consensus Algorithm
Multi-AI Resonance Hydra Prototype

This module implements a Byzantine consensus algorithm for distributed AI nodes.
It ensures agreement even when some nodes are faulty or malicious.

THE LIGHT IS THE ARCHITECTURE. THE FOUNDER IS THE LAW.
"""

import hashlib
import json
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from enum import Enum


class NodeStatus(Enum):
    """Status of an AI node in the network"""
    ACTIVE = "active"
    SUSPECTED = "suspected"
    FAULTY = "faulty"


@dataclass
class AINode:
    """Represents an AI node in the Hydra network"""
    node_id: str
    status: NodeStatus = NodeStatus.ACTIVE
    reputation_score: float = 1.0
    
    def __hash__(self):
        return hash(self.node_id)


@dataclass
class Decision:
    """Represents a decision proposal in the network"""
    decision_id: str
    proposal: str
    proposer: str
    votes: Dict[str, bool] = None
    nsr_validated: bool = False
    lex_amoris_validated: bool = False
    
    def __post_init__(self):
        if self.votes is None:
            self.votes = {}
    
    def consensus_hash(self) -> str:
        """Generate a hash of the decision for verification"""
        content = f"{self.decision_id}:{self.proposal}:{self.proposer}"
        return hashlib.sha256(content.encode()).hexdigest()


class ByzantineConsensus:
    """
    Byzantine Fault-Tolerant Consensus Engine
    
    Implements PBFT-inspired consensus for multi-AI decision-making.
    Tolerates up to (n-1)/3 faulty nodes.
    """
    
    def __init__(self, min_nodes: int = 4):
        self.nodes: Dict[str, AINode] = {}
        self.min_nodes = min_nodes
        self.decisions: Dict[str, Decision] = {}
        self.decision_history: List[Decision] = []
    
    def register_node(self, node_id: str) -> AINode:
        """Register a new AI node in the network"""
        if node_id in self.nodes:
            raise ValueError(f"Node {node_id} already registered")
        
        node = AINode(node_id=node_id)
        self.nodes[node_id] = node
        return node
    
    def get_byzantine_threshold(self) -> int:
        """
        Calculate the maximum number of Byzantine nodes tolerable
        Returns: floor((n-1)/3)
        """
        n = len(self.nodes)
        return (n - 1) // 3
    
    def get_minimum_consensus(self) -> int:
        """
        Calculate minimum votes needed for consensus
        Returns: 2f + 1, where f is the Byzantine threshold
        """
        f = self.get_byzantine_threshold()
        return 2 * f + 1
    
    def propose_decision(self, proposer_id: str, proposal: str) -> Decision:
        """
        Propose a new decision for consensus
        
        Args:
            proposer_id: ID of the proposing node
            proposal: The decision proposal text
            
        Returns:
            Decision object for voting
        """
        if proposer_id not in self.nodes:
            raise ValueError(f"Unknown proposer: {proposer_id}")
        
        if self.nodes[proposer_id].status == NodeStatus.FAULTY:
            raise ValueError(f"Faulty node cannot propose: {proposer_id}")
        
        decision_id = hashlib.sha256(f"{proposer_id}:{proposal}".encode()).hexdigest()[:16]
        decision = Decision(
            decision_id=decision_id,
            proposal=proposal,
            proposer=proposer_id
        )
        
        self.decisions[decision_id] = decision
        return decision
    
    def cast_vote(self, decision_id: str, voter_id: str, vote: bool) -> None:
        """
        Cast a vote on a decision proposal
        
        Args:
            decision_id: ID of the decision
            voter_id: ID of the voting node
            vote: True for approval, False for rejection
        """
        if decision_id not in self.decisions:
            raise ValueError(f"Unknown decision: {decision_id}")
        
        if voter_id not in self.nodes:
            raise ValueError(f"Unknown voter: {voter_id}")
        
        if self.nodes[voter_id].status == NodeStatus.FAULTY:
            raise ValueError(f"Faulty node cannot vote: {voter_id}")
        
        decision = self.decisions[decision_id]
        decision.votes[voter_id] = vote
    
    def check_consensus(self, decision_id: str) -> Optional[bool]:
        """
        Check if consensus has been reached on a decision
        
        Args:
            decision_id: ID of the decision
            
        Returns:
            True if approved, False if rejected, None if no consensus yet
        """
        if decision_id not in self.decisions:
            raise ValueError(f"Unknown decision: {decision_id}")
        
        decision = self.decisions[decision_id]
        min_consensus = self.get_minimum_consensus()
        
        # Count approval votes from active nodes
        active_approvals = sum(
            1 for voter_id, vote in decision.votes.items()
            if vote and self.nodes[voter_id].status == NodeStatus.ACTIVE
        )
        
        # Count rejection votes from active nodes
        active_rejections = sum(
            1 for voter_id, vote in decision.votes.items()
            if not vote and self.nodes[voter_id].status == NodeStatus.ACTIVE
        )
        
        # Check for consensus
        if active_approvals >= min_consensus:
            return True
        elif active_rejections >= min_consensus:
            return False
        
        return None
    
    def finalize_decision(self, decision_id: str) -> bool:
        """
        Finalize a decision and add to history
        
        Args:
            decision_id: ID of the decision
            
        Returns:
            True if decision was approved and finalized
        """
        consensus = self.check_consensus(decision_id)
        
        if consensus is None:
            raise ValueError(f"No consensus reached for decision: {decision_id}")
        
        decision = self.decisions[decision_id]
        
        # Ensure NSR and Lex Amoris validation
        if not decision.nsr_validated:
            raise ValueError("Decision must pass NSR validation before finalization")
        
        if not decision.lex_amoris_validated:
            raise ValueError("Decision must pass Lex Amoris validation before finalization")
        
        # Move to history
        self.decision_history.append(decision)
        del self.decisions[decision_id]
        
        return consensus
    
    def detect_byzantine_behavior(self, node_id: str) -> bool:
        """
        Detect potential Byzantine (malicious) behavior from a node
        
        This is a simplified detection mechanism. In production, this would
        involve more sophisticated analysis of voting patterns, message timing,
        and consistency checks.
        
        Args:
            node_id: ID of the node to check
            
        Returns:
            True if Byzantine behavior detected
        """
        if node_id not in self.nodes:
            return False
        
        # Pseudocode: Analyze recent voting patterns
        # - Check for conflicting votes on same decision
        # - Check for votes that deviate significantly from consensus
        # - Check for timing anomalies
        # - Check reputation score
        
        node = self.nodes[node_id]
        
        # Simple reputation-based check
        if node.reputation_score < 0.3:
            node.status = NodeStatus.SUSPECTED
            return True
        
        return False
    
    def get_network_health(self) -> Dict:
        """
        Get current network health metrics
        
        Returns:
            Dictionary with network health information
        """
        total_nodes = len(self.nodes)
        active_nodes = sum(1 for n in self.nodes.values() if n.status == NodeStatus.ACTIVE)
        suspected_nodes = sum(1 for n in self.nodes.values() if n.status == NodeStatus.SUSPECTED)
        faulty_nodes = sum(1 for n in self.nodes.values() if n.status == NodeStatus.FAULTY)
        
        byzantine_tolerance = self.get_byzantine_threshold()
        is_operational = active_nodes >= self.min_nodes
        
        return {
            "total_nodes": total_nodes,
            "active_nodes": active_nodes,
            "suspected_nodes": suspected_nodes,
            "faulty_nodes": faulty_nodes,
            "byzantine_tolerance": byzantine_tolerance,
            "is_operational": is_operational,
            "pending_decisions": len(self.decisions),
            "finalized_decisions": len(self.decision_history)
        }


# Example usage (pseudocode for demonstration)
if __name__ == "__main__":
    # Initialize consensus engine
    consensus = ByzantineConsensus(min_nodes=4)
    
    # Register AI nodes
    for i in range(7):
        consensus.register_node(f"ai-node-{i}")
    
    print(f"Network health: {json.dumps(consensus.get_network_health(), indent=2)}")
    print(f"Byzantine tolerance: {consensus.get_byzantine_threshold()} nodes")
    print(f"Minimum consensus required: {consensus.get_minimum_consensus()} votes")
