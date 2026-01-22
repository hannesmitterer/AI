#!/usr/bin/env python3
"""
AIC Consensus Protocol - Raft Implementation
=============================================

This module implements the Raft consensus protocol for ensuring consistency
among AICs during distributed operations.

Key Features:
- Leader election
- Log replication across AIC nodes
- Commit consensus
- Node failure handling
- State machine consistency

Based on: Raft consensus algorithm and Kosymbiosis principles
Reference: https://raft.github.io/
"""

import time
import random
import json
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum
from collections import deque


class NodeState(Enum):
    """Possible states for a Raft node."""
    FOLLOWER = "follower"
    CANDIDATE = "candidate"
    LEADER = "leader"


class LogEntryType(Enum):
    """Types of log entries."""
    OPERATION = "operation"
    CONFIGURATION = "configuration"
    NO_OP = "no_op"


@dataclass
class LogEntry:
    """Entry in the replicated log."""
    index: int
    term: int
    entry_type: LogEntryType
    command: Any
    timestamp: float = field(default_factory=time.time)
    committed: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert log entry to dictionary."""
        return {
            "index": self.index,
            "term": self.term,
            "type": self.entry_type.value,
            "command": self.command,
            "timestamp": self.timestamp,
            "committed": self.committed
        }


@dataclass
class VoteRequest:
    """Request for vote during leader election."""
    term: int
    candidate_id: str
    last_log_index: int
    last_log_term: int


@dataclass
class VoteResponse:
    """Response to vote request."""
    term: int
    vote_granted: bool
    voter_id: str


@dataclass
class AppendEntriesRequest:
    """Request to append entries to log (also used as heartbeat)."""
    term: int
    leader_id: str
    prev_log_index: int
    prev_log_term: int
    entries: List[LogEntry]
    leader_commit: int


@dataclass
class AppendEntriesResponse:
    """Response to append entries request."""
    term: int
    success: bool
    follower_id: str
    match_index: int = 0


class RaftNode:
    """
    A node in the Raft consensus cluster.
    
    Implements the Raft consensus algorithm for distributed consistency.
    """
    
    def __init__(
        self,
        node_id: str,
        cluster_nodes: List[str],
        election_timeout_range: tuple = (150, 300),  # milliseconds
        heartbeat_interval: int = 50  # milliseconds
    ):
        """
        Initialize a Raft node.
        
        Args:
            node_id: Unique identifier for this node
            cluster_nodes: List of all node IDs in the cluster
            election_timeout_range: Range for random election timeout
            heartbeat_interval: Interval for leader heartbeats
        """
        self.node_id = node_id
        self.cluster_nodes = [n for n in cluster_nodes if n != node_id]
        
        # Persistent state
        self.current_term = 0
        self.voted_for: Optional[str] = None
        self.log: List[LogEntry] = []
        
        # Volatile state
        self.state = NodeState.FOLLOWER
        self.commit_index = 0
        self.last_applied = 0
        
        # Leader state
        self.next_index: Dict[str, int] = {}
        self.match_index: Dict[str, int] = {}
        
        # Timing
        self.election_timeout_range = election_timeout_range
        self.heartbeat_interval = heartbeat_interval / 1000.0  # Convert to seconds
        self.last_heartbeat = time.time()
        self.election_timeout = self._get_random_election_timeout()
        
        # Statistics
        self.votes_received: Set[str] = set()
        self.election_count = 0
        self.append_entries_sent = 0
        self.append_entries_received = 0
        
        print(f"[RAFT] Node {node_id} initialized as FOLLOWER")
    
    def _get_random_election_timeout(self) -> float:
        """Get random election timeout in seconds."""
        timeout_ms = random.randint(*self.election_timeout_range)
        return timeout_ms / 1000.0
    
    def tick(self) -> List[Any]:
        """
        Process one tick of the Raft algorithm.
        
        Returns:
            List of messages to send to other nodes
        """
        messages = []
        current_time = time.time()
        
        if self.state == NodeState.LEADER:
            # Send heartbeats
            if current_time - self.last_heartbeat >= self.heartbeat_interval:
                messages.extend(self._send_heartbeats())
                self.last_heartbeat = current_time
        
        elif self.state in [NodeState.FOLLOWER, NodeState.CANDIDATE]:
            # Check election timeout
            if current_time - self.last_heartbeat >= self.election_timeout:
                messages.extend(self._start_election())
        
        return messages
    
    def _start_election(self) -> List[VoteRequest]:
        """Start leader election."""
        self.state = NodeState.CANDIDATE
        self.current_term += 1
        self.voted_for = self.node_id
        self.votes_received = {self.node_id}
        self.election_count += 1
        self.last_heartbeat = time.time()
        self.election_timeout = self._get_random_election_timeout()
        
        print(f"[RAFT] Node {self.node_id} starting election for term {self.current_term}")
        
        # Get last log info
        last_log_index = len(self.log) - 1 if self.log else -1
        last_log_term = self.log[-1].term if self.log else 0
        
        # Send vote requests to all other nodes
        vote_requests = []
        for node_id in self.cluster_nodes:
            vote_requests.append(VoteRequest(
                term=self.current_term,
                candidate_id=self.node_id,
                last_log_index=last_log_index,
                last_log_term=last_log_term
            ))
        
        return vote_requests
    
    def _send_heartbeats(self) -> List[AppendEntriesRequest]:
        """Send heartbeat (empty AppendEntries) to all followers."""
        heartbeats = []
        
        for node_id in self.cluster_nodes:
            prev_log_index = self.next_index.get(node_id, 0) - 1
            prev_log_term = self.log[prev_log_index].term if prev_log_index >= 0 else 0
            
            heartbeats.append(AppendEntriesRequest(
                term=self.current_term,
                leader_id=self.node_id,
                prev_log_index=prev_log_index,
                prev_log_term=prev_log_term,
                entries=[],
                leader_commit=self.commit_index
            ))
        
        self.append_entries_sent += len(heartbeats)
        return heartbeats
    
    def handle_vote_request(self, request: VoteRequest) -> VoteResponse:
        """
        Handle vote request from candidate.
        
        Args:
            request: Vote request
            
        Returns:
            Vote response
        """
        # Update term if necessary
        if request.term > self.current_term:
            self.current_term = request.term
            self.state = NodeState.FOLLOWER
            self.voted_for = None
        
        vote_granted = False
        
        # Grant vote if:
        # 1. Haven't voted in this term, or already voted for this candidate
        # 2. Candidate's log is at least as up-to-date as ours
        if request.term == self.current_term:
            if self.voted_for is None or self.voted_for == request.candidate_id:
                # Check if candidate's log is up-to-date
                our_last_log_index = len(self.log) - 1 if self.log else -1
                our_last_log_term = self.log[-1].term if self.log else 0
                
                log_ok = (
                    request.last_log_term > our_last_log_term or
                    (request.last_log_term == our_last_log_term and
                     request.last_log_index >= our_last_log_index)
                )
                
                if log_ok:
                    vote_granted = True
                    self.voted_for = request.candidate_id
                    self.last_heartbeat = time.time()  # Reset election timeout
        
        print(f"[RAFT] Node {self.node_id} {'granted' if vote_granted else 'denied'} vote to {request.candidate_id} for term {request.term}")
        
        return VoteResponse(
            term=self.current_term,
            vote_granted=vote_granted,
            voter_id=self.node_id
        )
    
    def handle_vote_response(self, response: VoteResponse) -> None:
        """
        Handle vote response.
        
        Args:
            response: Vote response
        """
        if self.state != NodeState.CANDIDATE:
            return
        
        # Update term if necessary
        if response.term > self.current_term:
            self.current_term = response.term
            self.state = NodeState.FOLLOWER
            self.voted_for = None
            return
        
        if response.vote_granted and response.term == self.current_term:
            self.votes_received.add(response.voter_id)
            
            # Check if we have majority
            total_nodes = len(self.cluster_nodes) + 1  # Include self
            if len(self.votes_received) > total_nodes / 2:
                self._become_leader()
    
    def _become_leader(self) -> None:
        """Become the leader."""
        self.state = NodeState.LEADER
        
        # Initialize leader state
        last_log_index = len(self.log)
        for node_id in self.cluster_nodes:
            self.next_index[node_id] = last_log_index
            self.match_index[node_id] = 0
        
        print(f"[RAFT] Node {self.node_id} became LEADER for term {self.current_term}")
        
        # Send initial heartbeat
        self.last_heartbeat = time.time()
    
    def handle_append_entries(self, request: AppendEntriesRequest) -> AppendEntriesResponse:
        """
        Handle append entries request from leader.
        
        Args:
            request: Append entries request
            
        Returns:
            Append entries response
        """
        self.append_entries_received += 1
        
        # Update term if necessary
        if request.term > self.current_term:
            self.current_term = request.term
            self.state = NodeState.FOLLOWER
            self.voted_for = None
        
        success = False
        match_index = 0
        
        if request.term == self.current_term:
            # Recognize leader and reset election timeout
            self.state = NodeState.FOLLOWER
            self.last_heartbeat = time.time()
            
            # Check if log matches at prev_log_index
            if request.prev_log_index == -1:
                log_ok = True
            elif request.prev_log_index < len(self.log):
                log_ok = self.log[request.prev_log_index].term == request.prev_log_term
            else:
                log_ok = False
            
            if log_ok:
                success = True
                
                # Append new entries
                if request.entries:
                    # Remove conflicting entries
                    insert_index = request.prev_log_index + 1
                    self.log = self.log[:insert_index]
                    
                    # Append new entries
                    self.log.extend(request.entries)
                    match_index = len(self.log) - 1
                else:
                    match_index = request.prev_log_index
                
                # Update commit index
                if request.leader_commit > self.commit_index:
                    self.commit_index = min(request.leader_commit, len(self.log) - 1)
                    self._apply_committed_entries()
        
        return AppendEntriesResponse(
            term=self.current_term,
            success=success,
            follower_id=self.node_id,
            match_index=match_index
        )
    
    def handle_append_entries_response(
        self,
        follower_id: str,
        response: AppendEntriesResponse
    ) -> Optional[AppendEntriesRequest]:
        """
        Handle append entries response from follower.
        
        Args:
            follower_id: ID of the follower
            response: Append entries response
            
        Returns:
            Next append entries request if needed
        """
        if self.state != NodeState.LEADER:
            return None
        
        # Update term if necessary
        if response.term > self.current_term:
            self.current_term = response.term
            self.state = NodeState.FOLLOWER
            self.voted_for = None
            return None
        
        if response.success:
            # Update next_index and match_index
            self.match_index[follower_id] = response.match_index
            self.next_index[follower_id] = response.match_index + 1
            
            # Update commit_index if possible
            self._update_commit_index()
        else:
            # Decrement next_index and retry
            self.next_index[follower_id] = max(0, self.next_index[follower_id] - 1)
            
            # Send updated AppendEntries
            return self._create_append_entries_for_follower(follower_id)
        
        return None
    
    def append_command(self, command: Any) -> bool:
        """
        Append a new command to the log (leader only).
        
        Args:
            command: Command to append
            
        Returns:
            True if successfully appended (this node is leader)
        """
        if self.state != NodeState.LEADER:
            return False
        
        entry = LogEntry(
            index=len(self.log),
            term=self.current_term,
            entry_type=LogEntryType.OPERATION,
            command=command
        )
        
        self.log.append(entry)
        
        print(f"[RAFT] Leader {self.node_id} appended command at index {entry.index}")
        
        return True
    
    def _create_append_entries_for_follower(self, follower_id: str) -> AppendEntriesRequest:
        """Create AppendEntries request for specific follower."""
        next_idx = self.next_index.get(follower_id, 0)
        prev_log_index = next_idx - 1
        prev_log_term = self.log[prev_log_index].term if prev_log_index >= 0 else 0
        
        # Get entries to send
        entries = self.log[next_idx:] if next_idx < len(self.log) else []
        
        return AppendEntriesRequest(
            term=self.current_term,
            leader_id=self.node_id,
            prev_log_index=prev_log_index,
            prev_log_term=prev_log_term,
            entries=entries,
            leader_commit=self.commit_index
        )
    
    def _update_commit_index(self) -> None:
        """Update commit index based on majority replication."""
        if self.state != NodeState.LEADER:
            return
        
        # Find highest index replicated on majority
        for index in range(self.commit_index + 1, len(self.log)):
            if self.log[index].term != self.current_term:
                continue
            
            # Count replications
            replications = 1  # Count self
            for follower_id in self.cluster_nodes:
                if self.match_index.get(follower_id, 0) >= index:
                    replications += 1
            
            # Check majority
            total_nodes = len(self.cluster_nodes) + 1
            if replications > total_nodes / 2:
                self.commit_index = index
                self.log[index].committed = True
                print(f"[RAFT] Leader {self.node_id} committed entry at index {index}")
                self._apply_committed_entries()
    
    def _apply_committed_entries(self) -> None:
        """Apply committed but not yet applied log entries."""
        while self.last_applied < self.commit_index:
            self.last_applied += 1
            entry = self.log[self.last_applied]
            print(f"[RAFT] Node {self.node_id} applied entry {self.last_applied}: {entry.command}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current node status."""
        return {
            "node_id": self.node_id,
            "state": self.state.value,
            "current_term": self.current_term,
            "voted_for": self.voted_for,
            "log_size": len(self.log),
            "commit_index": self.commit_index,
            "last_applied": self.last_applied,
            "election_count": self.election_count,
            "append_entries_sent": self.append_entries_sent,
            "append_entries_received": self.append_entries_received
        }


class RaftCluster:
    """
    Manages a cluster of Raft nodes for testing and simulation.
    """
    
    def __init__(self, node_ids: List[str]):
        """
        Initialize a Raft cluster.
        
        Args:
            node_ids: List of node IDs in the cluster
        """
        self.nodes: Dict[str, RaftNode] = {}
        
        for node_id in node_ids:
            self.nodes[node_id] = RaftNode(node_id, node_ids)
        
        print(f"[RAFT CLUSTER] Initialized with {len(node_ids)} nodes: {node_ids}")
    
    def tick_all(self) -> None:
        """Process one tick for all nodes."""
        for node in self.nodes.values():
            node.tick()
    
    def get_leader(self) -> Optional[str]:
        """Get current leader node ID."""
        for node_id, node in self.nodes.items():
            if node.state == NodeState.LEADER:
                return node_id
        return None
    
    def get_cluster_status(self) -> Dict[str, Any]:
        """Get status of entire cluster."""
        leader = self.get_leader()
        
        return {
            "total_nodes": len(self.nodes),
            "leader": leader,
            "node_states": {
                node_id: node.state.value
                for node_id, node in self.nodes.items()
            }
        }


# Example usage
if __name__ == "__main__":
    print("=== AIC Raft Consensus Protocol Demo ===\n")
    
    # Create cluster
    node_ids = [f"aic_{i:03d}" for i in range(5)]
    cluster = RaftCluster(node_ids)
    
    # Simulate until leader elected
    print("--- Simulating leader election ---")
    max_ticks = 100
    for tick in range(max_ticks):
        cluster.tick_all()
        time.sleep(0.01)
        
        leader = cluster.get_leader()
        if leader:
            print(f"\nLeader elected: {leader}")
            break
    
    # Get cluster status
    print("\n--- Cluster Status ---")
    status = cluster.get_cluster_status()
    print(json.dumps(status, indent=2))
    
    # Show individual node status
    print("\n--- Individual Node Status ---")
    for node_id, node in cluster.nodes.items():
        node_status = node.get_status()
        print(f"{node_id}: {json.dumps(node_status, indent=2)}")
    
    print("\n=== Demo Complete ===")
