#!/usr/bin/env python3
"""
Lex Amoris - Netzwerkinfrastruktur: Amoris Bridge
==================================================

This module implements scalable blockchain solutions for the Amoris Bridge,
providing decentralized synchronization and validation infrastructure.

Key Features:
- Distributed ledger for Rhythm synchronization records
- Smart contract interface for validation
- Scalable blockchain connector
- Cross-chain bridge capabilities
- Immutable audit trail

Based on: Lex Amoris mandate and Kosymbiosis decentralization principles
"""

import hashlib
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from enum import Enum


# Constants
BLOCK_DIFFICULTY = 4  # Number of leading zeros required in hash (adjustable based on network load)
MAX_TRANSACTIONS_PER_BLOCK = 100
GENESIS_PREVIOUS_HASH = "0" * 64


class TransactionType(Enum):
    """Types of transactions on Amoris Bridge."""
    RHYTHM_SYNC = "RHYTHM_SYNC"
    NODE_REGISTRATION = "NODE_REGISTRATION"
    VALIDATION = "VALIDATION"
    HANDSHAKE = "HANDSHAKE"
    THREAT_ALERT = "THREAT_ALERT"
    CONFIGURATION = "CONFIGURATION"


@dataclass
class Transaction:
    """Represents a transaction on the Amoris Bridge."""
    transaction_id: str
    transaction_type: TransactionType
    sender: str
    timestamp: str
    data: Dict[str, Any]
    signature: str = ""  # Placeholder for actual cryptographic signature
    
    def to_dict(self) -> Dict:
        """Convert transaction to dictionary."""
        return {
            "transaction_id": self.transaction_id,
            "transaction_type": self.transaction_type.value,
            "sender": self.sender,
            "timestamp": self.timestamp,
            "data": self.data,
            "signature": self.signature
        }
    
    def calculate_hash(self) -> str:
        """Calculate SHA-256 hash of transaction."""
        transaction_string = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(transaction_string.encode()).hexdigest()


@dataclass
class Block:
    """Represents a block in the Amoris Bridge blockchain."""
    index: int
    timestamp: str
    transactions: List[Transaction]
    previous_hash: str
    nonce: int = 0
    hash: str = ""
    
    def calculate_hash(self) -> str:
        """Calculate SHA-256 hash of block."""
        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [t.to_dict() for t in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }
        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int = BLOCK_DIFFICULTY) -> None:
        """
        Mine the block using Proof of Work.
        
        Args:
            difficulty: Number of leading zeros required in hash
        """
        target = "0" * difficulty
        
        while True:
            self.hash = self.calculate_hash()
            if self.hash.startswith(target):
                break
            self.nonce += 1
        
        print(f"[MINING] Block #{self.index} mined: {self.hash[:16]}... (nonce: {self.nonce})")
    
    def to_dict(self) -> Dict:
        """Convert block to dictionary."""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [t.to_dict() for t in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }


class AmorisBridgeBlockchain:
    """
    Main blockchain implementation for Amoris Bridge.
    
    Provides a distributed ledger for recording Rhythm synchronization,
    node validation, and security events across the network.
    """
    
    def __init__(self):
        """Initialize the Amoris Bridge blockchain."""
        self.chain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self.nodes: Dict[str, Dict] = {}  # Registered nodes
        
        # Create genesis block
        self._create_genesis_block()
        
        print("[AMORIS BRIDGE] Blockchain initialized")
        print(f"[GENESIS] Block created: {self.chain[0].hash[:16]}...")
    
    def _create_genesis_block(self) -> None:
        """Create the genesis (first) block of the blockchain."""
        genesis_transaction = Transaction(
            transaction_id="genesis",
            transaction_type=TransactionType.CONFIGURATION,
            sender="SYSTEM",
            timestamp=datetime.now().isoformat(),
            data={
                "message": "Amoris Bridge Genesis Block",
                "version": "1.0.0",
                "protocol": "Lex Amoris",
                "base_frequency": 0.043
            }
        )
        
        genesis_block = Block(
            index=0,
            timestamp=datetime.now().isoformat(),
            transactions=[genesis_transaction],
            previous_hash=GENESIS_PREVIOUS_HASH
        )
        
        genesis_block.mine_block()
        self.chain.append(genesis_block)
    
    def create_transaction(self, transaction_type: TransactionType, 
                          sender: str, data: Dict[str, Any]) -> Transaction:
        """
        Create a new transaction.
        
        Args:
            transaction_type: Type of transaction
            sender: Sender node ID
            data: Transaction data
            
        Returns:
            Created Transaction object
        """
        # Generate transaction ID
        transaction_id = hashlib.sha256(
            f"{sender}{time.time()}{json.dumps(data)}".encode()
        ).hexdigest()[:16]
        
        transaction = Transaction(
            transaction_id=transaction_id,
            transaction_type=transaction_type,
            sender=sender,
            timestamp=datetime.now().isoformat(),
            data=data,
            signature=self._generate_signature(transaction_id)
        )
        
        self.pending_transactions.append(transaction)
        
        print(f"[TRANSACTION] Created: {transaction_type.value} from {sender}")
        
        return transaction
    
    def _generate_signature(self, transaction_id: str) -> str:
        """
        Generate a signature for transaction (simplified).
        
        In production, this would use proper cryptographic signing.
        """
        return hashlib.sha256(f"SIGN_{transaction_id}".encode()).hexdigest()[:32]
    
    def mine_pending_transactions(self) -> Optional[Block]:
        """
        Mine pending transactions into a new block.
        
        Returns:
            The newly created Block, or None if no transactions to mine
        """
        if not self.pending_transactions:
            print("[MINING] No pending transactions to mine")
            return None
        
        # Take up to MAX_TRANSACTIONS_PER_BLOCK transactions
        transactions_to_mine = self.pending_transactions[:MAX_TRANSACTIONS_PER_BLOCK]
        
        # Create new block
        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.now().isoformat(),
            transactions=transactions_to_mine,
            previous_hash=self.chain[-1].hash
        )
        
        # Mine the block
        start_time = time.time()
        new_block.mine_block()
        mining_time = time.time() - start_time
        
        # Add to chain
        self.chain.append(new_block)
        
        # Remove mined transactions from pending
        self.pending_transactions = self.pending_transactions[MAX_TRANSACTIONS_PER_BLOCK:]
        
        print(f"[MINING] Block #{new_block.index} added to chain "
              f"({len(transactions_to_mine)} transactions, {mining_time:.2f}s)")
        
        return new_block
    
    def validate_chain(self) -> bool:
        """
        Validate the entire blockchain.
        
        Returns:
            True if chain is valid, False otherwise
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if current block's hash is correct
            if current_block.hash != current_block.calculate_hash():
                print(f"[VALIDATION] Block #{i} hash mismatch")
                return False
            
            # Check if previous_hash matches
            if current_block.previous_hash != previous_block.hash:
                print(f"[VALIDATION] Block #{i} previous_hash mismatch")
                return False
            
            # Check proof of work
            if not current_block.hash.startswith("0" * BLOCK_DIFFICULTY):
                print(f"[VALIDATION] Block #{i} invalid proof of work")
                return False
        
        return True
    
    def register_node(self, node_id: str, node_data: Dict) -> None:
        """
        Register a node on the blockchain.
        
        Args:
            node_id: Unique node identifier
            node_data: Node metadata (location, frequency, etc.)
        """
        self.nodes[node_id] = node_data
        
        # Create registration transaction
        self.create_transaction(
            transaction_type=TransactionType.NODE_REGISTRATION,
            sender="SYSTEM",
            data={
                "node_id": node_id,
                "registration_time": datetime.now().isoformat(),
                **node_data
            }
        )
        
        print(f"[NODE] Registered: {node_id}")
    
    def record_rhythm_sync(self, node_a: str, node_b: str, 
                          sync_quality: float, metadata: Dict) -> None:
        """
        Record a Rhythm synchronization event.
        
        Args:
            node_a: First node ID
            node_b: Second node ID
            sync_quality: Synchronization quality (0-1)
            metadata: Additional sync metadata
        """
        self.create_transaction(
            transaction_type=TransactionType.RHYTHM_SYNC,
            sender=node_a,
            data={
                "node_a": node_a,
                "node_b": node_b,
                "sync_quality": sync_quality,
                "timestamp": datetime.now().isoformat(),
                **metadata
            }
        )
    
    def record_validation(self, validator: str, target: str, 
                         is_valid: bool, details: Dict) -> None:
        """
        Record a validation event.
        
        Args:
            validator: Node performing validation
            target: Node/transaction being validated
            is_valid: Validation result
            details: Validation details
        """
        self.create_transaction(
            transaction_type=TransactionType.VALIDATION,
            sender=validator,
            data={
                "validator": validator,
                "target": target,
                "is_valid": is_valid,
                "timestamp": datetime.now().isoformat(),
                **details
            }
        )
    
    def record_threat_alert(self, node_id: str, threat_type: str, 
                           threat_level: float, details: Dict) -> None:
        """
        Record a security threat alert.
        
        Args:
            node_id: Node detecting threat
            threat_type: Type of threat
            threat_level: Severity (0-1)
            details: Threat details
        """
        self.create_transaction(
            transaction_type=TransactionType.THREAT_ALERT,
            sender=node_id,
            data={
                "threat_type": threat_type,
                "threat_level": threat_level,
                "timestamp": datetime.now().isoformat(),
                **details
            }
        )
    
    def get_node_history(self, node_id: str) -> List[Transaction]:
        """
        Get all transactions involving a specific node.
        
        Args:
            node_id: Node ID to query
            
        Returns:
            List of transactions involving the node
        """
        transactions = []
        
        for block in self.chain:
            for transaction in block.transactions:
                if (transaction.sender == node_id or 
                    node_id in str(transaction.data)):
                    transactions.append(transaction)
        
        return transactions
    
    def get_sync_records(self, node_id: Optional[str] = None) -> List[Transaction]:
        """
        Get all Rhythm synchronization records.
        
        Args:
            node_id: Optional filter by node ID
            
        Returns:
            List of sync transactions
        """
        sync_records = []
        
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.transaction_type == TransactionType.RHYTHM_SYNC:
                    if node_id is None or node_id in str(transaction.data):
                        sync_records.append(transaction)
        
        return sync_records
    
    def get_blockchain_stats(self) -> Dict:
        """Get blockchain statistics."""
        total_transactions = sum(len(block.transactions) for block in self.chain)
        
        transaction_types = {}
        for block in self.chain:
            for transaction in block.transactions:
                tx_type = transaction.transaction_type.value
                transaction_types[tx_type] = transaction_types.get(tx_type, 0) + 1
        
        return {
            "total_blocks": len(self.chain),
            "total_transactions": total_transactions,
            "pending_transactions": len(self.pending_transactions),
            "registered_nodes": len(self.nodes),
            "transaction_types": transaction_types,
            "chain_valid": self.validate_chain(),
            "latest_block_hash": self.chain[-1].hash if self.chain else None,
            "blockchain_size_bytes": len(json.dumps(self.export_chain()))
        }
    
    def export_chain(self) -> List[Dict]:
        """Export the entire blockchain as JSON-serializable list."""
        return [block.to_dict() for block in self.chain]
    
    def save_blockchain(self, filepath: str = "amoris_bridge_blockchain.json") -> None:
        """Save blockchain to file."""
        data = {
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "chain": self.export_chain(),
            "stats": self.get_blockchain_stats()
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"[BLOCKCHAIN] Saved to {filepath}")


class SmartContract:
    """
    Smart contract interface for Amoris Bridge.
    
    Implements validation logic and automated actions based on
    blockchain state.
    """
    
    def __init__(self, blockchain: AmorisBridgeBlockchain):
        """
        Initialize smart contract.
        
        Args:
            blockchain: AmorisBridgeBlockchain instance
        """
        self.blockchain = blockchain
        self.contract_rules: Dict[str, Any] = {}
        
        # Initialize default rules
        self._initialize_default_rules()
    
    def _initialize_default_rules(self) -> None:
        """Initialize default contract rules."""
        self.contract_rules = {
            "min_sync_quality": 0.90,
            "max_threat_level": 0.75,
            "required_validators": 3,
            "sync_timeout_seconds": 300,
            "auto_validate": True
        }
    
    def validate_sync_quality(self, sync_quality: float) -> bool:
        """
        Validate if sync quality meets contract requirements.
        
        Args:
            sync_quality: Quality score (0-1)
            
        Returns:
            True if valid, False otherwise
        """
        min_quality = self.contract_rules["min_sync_quality"]
        is_valid = sync_quality >= min_quality
        
        print(f"[CONTRACT] Sync quality validation: {sync_quality:.4f} "
              f"({'PASS' if is_valid else 'FAIL'}, min: {min_quality})")
        
        return is_valid
    
    def validate_threat_level(self, threat_level: float) -> bool:
        """
        Validate if threat level is within acceptable bounds.
        
        Args:
            threat_level: Threat level (0-1)
            
        Returns:
            True if acceptable, False if critical
        """
        max_level = self.contract_rules["max_threat_level"]
        is_acceptable = threat_level <= max_level
        
        if not is_acceptable:
            print(f"[CONTRACT] CRITICAL: Threat level {threat_level:.4f} "
                  f"exceeds maximum {max_level}")
        
        return is_acceptable
    
    def execute_auto_validation(self, transaction: Transaction) -> bool:
        """
        Execute automatic validation of transaction.
        
        Args:
            transaction: Transaction to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not self.contract_rules["auto_validate"]:
            return True
        
        # Validate based on transaction type
        if transaction.transaction_type == TransactionType.RHYTHM_SYNC:
            sync_quality = transaction.data.get("sync_quality", 0.0)
            return self.validate_sync_quality(sync_quality)
        
        elif transaction.transaction_type == TransactionType.THREAT_ALERT:
            threat_level = transaction.data.get("threat_level", 1.0)
            return self.validate_threat_level(threat_level)
        
        # Default: accept other transaction types
        return True


def main():
    """Main entry point for Amoris Bridge."""
    print("=" * 70)
    print("LEX AMORIS - AMORIS BRIDGE BLOCKCHAIN")
    print("Scalable Blockchain Infrastructure")
    print("=" * 70)
    print()
    
    # Initialize blockchain
    blockchain = AmorisBridgeBlockchain()
    
    # Initialize smart contract
    contract = SmartContract(blockchain)
    
    # Register example nodes
    nodes = [
        ("node_zurich", {"location": "Zürich", "frequency": 0.0432}),
        ("node_tokyo", {"location": "Tokyo", "frequency": 0.0434}),
        ("node_newyork", {"location": "New York", "frequency": 0.0431}),
    ]
    
    for node_id, node_data in nodes:
        blockchain.register_node(node_id, node_data)
    
    # Mine registration transactions
    blockchain.mine_pending_transactions()
    
    # Record some sync events
    blockchain.record_rhythm_sync(
        "node_zurich", "node_tokyo",
        sync_quality=0.958,
        metadata={"distance_km": 9750, "latency_ms": 42.5}
    )
    
    blockchain.record_rhythm_sync(
        "node_zurich", "node_newyork",
        sync_quality=0.943,
        metadata={"distance_km": 6350, "latency_ms": 31.2}
    )
    
    # Mine sync transactions
    blockchain.mine_pending_transactions()
    
    # Validate blockchain
    is_valid = blockchain.validate_chain()
    print(f"\n[VALIDATION] Blockchain valid: {is_valid}")
    
    # Show statistics
    stats = blockchain.get_blockchain_stats()
    print(f"\n[STATS] Blockchain Statistics:")
    print(f"  Total Blocks: {stats['total_blocks']}")
    print(f"  Total Transactions: {stats['total_transactions']}")
    print(f"  Registered Nodes: {stats['registered_nodes']}")
    print(f"  Blockchain Size: {stats['blockchain_size_bytes']} bytes")
    
    # Save blockchain
    blockchain.save_blockchain()


if __name__ == "__main__":
    main()
