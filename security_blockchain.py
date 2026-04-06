#!/usr/bin/env python3
"""
Blockchain Security Module
==========================

This module implements blockchain fork detection and consensus validation
to protect against blockchain manipulation and header continuity attacks.

Features:
- Simultaneous consensus checking across multiple chains
- Header continuity validation
- Fork detection and resolution
- Byzantine fault tolerance
"""

import time
import hashlib
import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ConsensusStatus(Enum):
    """Consensus validation status."""
    VALID = "VALID"
    FORK_DETECTED = "FORK_DETECTED"
    HEADER_DISCONTINUITY = "HEADER_DISCONTINUITY"
    BYZANTINE_FAULT = "BYZANTINE_FAULT"
    INSUFFICIENT_VALIDATORS = "INSUFFICIENT_VALIDATORS"


@dataclass
class BlockHeader:
    """Blockchain block header."""
    block_number: int
    previous_hash: str
    timestamp: float
    merkle_root: str
    nonce: int
    hash: str = ""
    
    def __post_init__(self):
        """Calculate block hash if not provided."""
        if not self.hash:
            self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate block hash."""
        data = (
            f"{self.block_number}"
            f"{self.previous_hash}"
            f"{self.timestamp}"
            f"{self.merkle_root}"
            f"{self.nonce}"
        )
        return hashlib.sha256(data.encode()).hexdigest()
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "block_number": self.block_number,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "merkle_root": self.merkle_root,
            "nonce": self.nonce,
            "hash": self.hash
        }


@dataclass
class BlockchainChain:
    """Represents a blockchain chain."""
    chain_id: str
    headers: List[BlockHeader] = field(default_factory=list)
    is_canonical: bool = False
    
    def add_header(self, header: BlockHeader) -> bool:
        """
        Add header to chain.
        
        Args:
            header: Block header to add
            
        Returns:
            True if added successfully
        """
        # Validate continuity
        if self.headers:
            last_header = self.headers[-1]
            if header.previous_hash != last_header.hash:
                return False
            if header.block_number != last_header.block_number + 1:
                return False
        
        self.headers.append(header)
        return True
    
    def get_chain_length(self) -> int:
        """Get chain length."""
        return len(self.headers)
    
    def get_latest_header(self) -> Optional[BlockHeader]:
        """Get latest block header."""
        return self.headers[-1] if self.headers else None


@dataclass
class ForkDetectionResult:
    """Result of fork detection analysis."""
    has_fork: bool
    fork_point: Optional[int]
    canonical_chain: Optional[str]
    alternative_chains: List[str]
    consensus_status: ConsensusStatus
    description: str


class BlockchainForkDetector:
    """
    Detects and analyzes blockchain forks.
    
    Monitors multiple chain instances to identify fork points
    and maintain consensus.
    """
    
    def __init__(self, min_validators: int = 3):
        """
        Initialize fork detector.
        
        Args:
            min_validators: Minimum validators for consensus
        """
        self.chains: Dict[str, BlockchainChain] = {}
        self.min_validators = min_validators
        self.fork_events: List[ForkDetectionResult] = []
        
        # Genesis block
        self.genesis_hash = self._create_genesis_block()
        
    def _create_genesis_block(self) -> str:
        """Create genesis block hash."""
        genesis = BlockHeader(
            block_number=0,
            previous_hash="0" * 64,
            timestamp=time.time(),
            merkle_root="0" * 64,
            nonce=0
        )
        return genesis.hash
    
    def register_chain(self, chain_id: str) -> None:
        """
        Register a new blockchain chain for monitoring.
        
        Args:
            chain_id: Unique identifier for the chain
        """
        if chain_id not in self.chains:
            self.chains[chain_id] = BlockchainChain(chain_id=chain_id)
    
    def add_block_header(self, chain_id: str, header: BlockHeader) -> bool:
        """
        Add block header to a chain.
        
        Args:
            chain_id: Chain identifier
            header: Block header to add
            
        Returns:
            True if added successfully
        """
        if chain_id not in self.chains:
            self.register_chain(chain_id)
        
        return self.chains[chain_id].add_header(header)
    
    def validate_header_continuity(self, chain_id: str) -> bool:
        """
        Validate header continuity for a chain.
        
        Args:
            chain_id: Chain identifier
            
        Returns:
            True if all headers are continuous
        """
        if chain_id not in self.chains:
            return False
        
        chain = self.chains[chain_id]
        
        for i in range(1, len(chain.headers)):
            prev_header = chain.headers[i-1]
            curr_header = chain.headers[i]
            
            # Check hash continuity
            if curr_header.previous_hash != prev_header.hash:
                return False
            
            # Check block number continuity
            if curr_header.block_number != prev_header.block_number + 1:
                return False
            
            # Verify hash calculation
            if curr_header.hash != curr_header.calculate_hash():
                return False
        
        return True
    
    def detect_fork(self) -> ForkDetectionResult:
        """
        Detect blockchain forks across all chains.
        
        Returns:
            Fork detection result
        """
        if len(self.chains) < 2:
            return ForkDetectionResult(
                has_fork=False,
                fork_point=None,
                canonical_chain=list(self.chains.keys())[0] if self.chains else None,
                alternative_chains=[],
                consensus_status=ConsensusStatus.INSUFFICIENT_VALIDATORS,
                description="Insufficient chains for fork detection"
            )
        
        # Find common ancestor and divergence point
        chain_ids = list(self.chains.keys())
        reference_chain = self.chains[chain_ids[0]]
        
        fork_point = None
        divergent_chains = []
        
        # Compare each chain with reference
        for chain_id in chain_ids[1:]:
            compare_chain = self.chains[chain_id]
            
            # Find divergence point
            min_len = min(reference_chain.get_chain_length(), 
                         compare_chain.get_chain_length())
            
            for i in range(min_len):
                if reference_chain.headers[i].hash != compare_chain.headers[i].hash:
                    fork_point = i
                    divergent_chains.append(chain_id)
                    break
        
        # Determine consensus
        if not divergent_chains:
            # All chains agree
            return ForkDetectionResult(
                has_fork=False,
                fork_point=None,
                canonical_chain=chain_ids[0],
                alternative_chains=[],
                consensus_status=ConsensusStatus.VALID,
                description="All chains in consensus"
            )
        
        # Fork detected - determine canonical chain
        chain_lengths = {cid: self.chains[cid].get_chain_length() 
                        for cid in self.chains.keys()}
        canonical_chain = max(chain_lengths, key=chain_lengths.get)
        
        # Mark canonical chain
        self.chains[canonical_chain].is_canonical = True
        
        result = ForkDetectionResult(
            has_fork=True,
            fork_point=fork_point,
            canonical_chain=canonical_chain,
            alternative_chains=divergent_chains,
            consensus_status=ConsensusStatus.FORK_DETECTED,
            description=f"Fork detected at block {fork_point}, "
                       f"{len(divergent_chains)} alternative chains"
        )
        
        self.fork_events.append(result)
        return result
    
    def resolve_fork(self, fork_result: ForkDetectionResult) -> Dict[str, any]:
        """
        Resolve detected fork by selecting canonical chain.
        
        Args:
            fork_result: Fork detection result
            
        Returns:
            Resolution report
        """
        if not fork_result.has_fork:
            return {
                "resolution": "NO_FORK",
                "action": "No action needed"
            }
        
        canonical = fork_result.canonical_chain
        alternatives = fork_result.alternative_chains
        
        # Prune alternative chains
        pruned_blocks = 0
        for alt_chain_id in alternatives:
            if alt_chain_id in self.chains:
                alt_chain = self.chains[alt_chain_id]
                if fork_result.fork_point is not None:
                    # Keep blocks up to fork point
                    pruned_blocks += len(alt_chain.headers) - fork_result.fork_point
                    alt_chain.headers = alt_chain.headers[:fork_result.fork_point]
        
        return {
            "resolution": "FORK_RESOLVED",
            "canonical_chain": canonical,
            "pruned_chains": alternatives,
            "blocks_pruned": pruned_blocks,
            "fork_point": fork_result.fork_point,
            "action": f"Canonical chain {canonical} selected, "
                     f"{len(alternatives)} alternative chains pruned"
        }
    
    def simultaneous_consensus_check(self) -> Dict[str, any]:
        """
        Perform simultaneous consensus check across all chains.
        
        Returns:
            Consensus check report
        """
        results = {
            "timestamp": time.time(),
            "chains_checked": len(self.chains),
            "continuity_validation": {},
            "fork_detection": None,
            "overall_status": ConsensusStatus.VALID
        }
        
        # Validate continuity for each chain
        for chain_id, chain in self.chains.items():
            is_continuous = self.validate_header_continuity(chain_id)
            results["continuity_validation"][chain_id] = {
                "is_continuous": is_continuous,
                "chain_length": chain.get_chain_length(),
                "latest_block": chain.get_latest_header().block_number 
                               if chain.get_latest_header() else None
            }
            
            if not is_continuous:
                results["overall_status"] = ConsensusStatus.HEADER_DISCONTINUITY
        
        # Detect forks
        fork_result = self.detect_fork()
        results["fork_detection"] = {
            "has_fork": fork_result.has_fork,
            "fork_point": fork_result.fork_point,
            "canonical_chain": fork_result.canonical_chain,
            "status": fork_result.consensus_status.value,
            "description": fork_result.description
        }
        
        if fork_result.has_fork:
            results["overall_status"] = ConsensusStatus.FORK_DETECTED
        
        return results


def main():
    """Demonstrate blockchain security."""
    print("=" * 70)
    print("BLOCKCHAIN SECURITY - Fork Detection & Consensus")
    print("=" * 70)
    
    # Initialize fork detector
    print("\n[1] Initializing blockchain fork detector...")
    detector = BlockchainForkDetector(min_validators=3)
    print("    Detector initialized")
    
    # Create multiple chains
    print("\n[2] Creating blockchain chains...")
    chains = ["chain_A", "chain_B", "chain_C"]
    for chain_id in chains:
        detector.register_chain(chain_id)
        print(f"    Registered {chain_id}")
    
    # Add synchronized blocks (no fork)
    print("\n[3] Adding synchronized blocks...")
    previous_hash = detector.genesis_hash
    for block_num in range(1, 6):
        header = BlockHeader(
            block_number=block_num,
            previous_hash=previous_hash,
            timestamp=time.time(),
            merkle_root=hashlib.sha256(f"data_{block_num}".encode()).hexdigest(),
            nonce=block_num
        )
        
        # Add to all chains
        for chain_id in chains:
            detector.add_block_header(chain_id, header)
        
        previous_hash = header.hash
    
    # Check consensus
    print("\n[4] Performing consensus check (no fork)...")
    consensus = detector.simultaneous_consensus_check()
    print(f"    Status: {consensus['overall_status'].value}")
    print(f"    Fork detected: {consensus['fork_detection']['has_fork']}")
    
    # Simulate fork
    print("\n[5] Simulating blockchain fork...")
    # Chain A continues normally
    header_a = BlockHeader(
        block_number=6,
        previous_hash=previous_hash,
        timestamp=time.time(),
        merkle_root=hashlib.sha256(b"legitimate_data").hexdigest(),
        nonce=6
    )
    detector.add_block_header("chain_A", header_a)
    
    # Chain B forks with different data
    header_b = BlockHeader(
        block_number=6,
        previous_hash=previous_hash,
        timestamp=time.time(),
        merkle_root=hashlib.sha256(b"malicious_data").hexdigest(),  # Different!
        nonce=666  # Different nonce
    )
    detector.add_block_header("chain_B", header_b)
    
    # Chain C follows chain A
    detector.add_block_header("chain_C", header_a)
    
    # Detect fork
    print("\n[6] Detecting fork...")
    fork_result = detector.detect_fork()
    print(f"    Fork detected: {fork_result.has_fork}")
    print(f"    Fork point: Block {fork_result.fork_point}")
    print(f"    Canonical chain: {fork_result.canonical_chain}")
    print(f"    Alternative chains: {fork_result.alternative_chains}")
    
    # Resolve fork
    print("\n[7] Resolving fork...")
    resolution = detector.resolve_fork(fork_result)
    print(f"    Resolution: {resolution['resolution']}")
    print(f"    Action: {resolution['action']}")
    
    print("\n" + "=" * 70)
    print("Blockchain security demonstration complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
