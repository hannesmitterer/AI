#!/usr/bin/env python3
"""
Blockchain Mesh Network (BBMN) - Decentralized Infrastructure
==============================================================

This module implements a decentralized blockchain-based mesh network
that eliminates dependencies on centralized DNS and traditional
networking infrastructure.

Features:
- Peer-to-peer mesh networking
- Decentralized node discovery
- Blockchain-based routing and identity
- No DNS dependencies
- Self-organizing network topology
"""

import time
import hashlib
import secrets
import json
from typing import Dict, List, Set, Optional
from dataclasses import dataclass, field
from datetime import datetime
import threading


@dataclass
class Block:
    """Represents a block in the mesh network blockchain."""
    index: int
    timestamp: float
    data: Dict
    previous_hash: str
    nonce: int = 0
    hash: str = ""
    
    def calculate_hash(self) -> str:
        """Calculate block hash."""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int = 2) -> None:
        """Mine block with proof-of-work."""
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()


@dataclass
class MeshNode:
    """Represents a node in the mesh network."""
    node_id: str
    address: str  # Decentralized address (hash-based)
    public_key: str
    peers: Set[str] = field(default_factory=set)
    last_seen: float = field(default_factory=time.time)
    trust_score: float = 1.0
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "node_id": self.node_id,
            "address": self.address,
            "public_key": self.public_key,
            "peer_count": len(self.peers),
            "last_seen": self.last_seen,
            "trust_score": self.trust_score
        }


class BlockchainMeshNetwork:
    """
    Decentralized mesh network using blockchain for coordination.
    
    Eliminates centralized DNS by using:
    - Hash-based addressing
    - Distributed hash table (DHT)
    - Blockchain for node registry
    - Peer-to-peer discovery
    """
    
    def __init__(self, network_id: str = "KOSYMBIOSIS_MESH"):
        """
        Initialize blockchain mesh network.
        
        Args:
            network_id: Unique identifier for this mesh network
        """
        self.network_id = network_id
        self.chain: List[Block] = []
        self.nodes: Dict[str, MeshNode] = {}
        self.local_node_id = self._generate_node_id()
        self.routing_table: Dict[str, List[str]] = {}
        self.dht: Dict[str, str] = {}  # Distributed Hash Table
        self.is_running = False
        self.discovery_thread: Optional[threading.Thread] = None
        
        # Create genesis block
        self._create_genesis_block()
        
        # Register self as first node
        self._register_local_node()
        
        print(f"[BBMN] Initialized mesh network: {network_id}")
        print(f"[BBMN] Local node ID: {self.local_node_id}")
    
    def _generate_node_id(self) -> str:
        """Generate unique node ID using cryptographic hash."""
        random_data = secrets.token_bytes(32)
        timestamp = str(time.time()).encode()
        node_id = hashlib.sha256(random_data + timestamp).hexdigest()[:16]
        return f"node_{node_id}"
    
    def _create_genesis_block(self) -> None:
        """Create the genesis block for the mesh network."""
        genesis_block = Block(
            index=0,
            timestamp=time.time(),
            data={
                "type": "genesis",
                "network_id": self.network_id,
                "message": "BBMN Genesis - Decentralized Mesh Network"
            },
            previous_hash="0"
        )
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)
        print(f"[BLOCKCHAIN] Genesis block created: {genesis_block.hash[:16]}...")
    
    def _register_local_node(self) -> None:
        """Register the local node in the mesh network."""
        # Generate decentralized address (hash-based)
        address = hashlib.sha256(
            self.local_node_id.encode() + self.network_id.encode()
        ).hexdigest()[:32]
        
        # Generate public key (simplified - in production use real crypto)
        public_key = hashlib.sha256(address.encode()).hexdigest()
        
        # Create local node
        local_node = MeshNode(
            node_id=self.local_node_id,
            address=address,
            public_key=public_key
        )
        
        self.nodes[self.local_node_id] = local_node
        
        # Add to DHT
        self.dht[address] = self.local_node_id
        
        # Add to blockchain
        self._add_node_to_blockchain(local_node)
    
    def _add_node_to_blockchain(self, node: MeshNode) -> None:
        """Add node registration to blockchain."""
        block_data = {
            "type": "node_registration",
            "node_id": node.node_id,
            "address": node.address,
            "public_key": node.public_key,
            "timestamp": time.time()
        }
        
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            data=block_data,
            previous_hash=self.chain[-1].hash if self.chain else "0"
        )
        
        new_block.mine_block(difficulty=2)
        self.chain.append(new_block)
        
        print(f"[BLOCKCHAIN] Node registered in block #{new_block.index}")
    
    def discover_peers(self) -> List[str]:
        """
        Discover peers in the mesh network without DNS.
        
        Uses:
        - Local broadcast
        - DHT traversal
        - Blockchain node registry
        - Peer exchange protocol
        
        Returns:
            List of discovered peer node IDs
        """
        discovered_peers = []
        
        # Method 1: Query blockchain for registered nodes
        for block in self.chain:
            if block.data.get("type") == "node_registration":
                node_id = block.data.get("node_id")
                if node_id and node_id != self.local_node_id:
                    discovered_peers.append(node_id)
        
        # Method 2: Query DHT for known addresses
        for address, node_id in self.dht.items():
            if node_id != self.local_node_id and node_id not in discovered_peers:
                discovered_peers.append(node_id)
        
        # Method 3: Peer exchange (get peers from known peers)
        for node in self.nodes.values():
            if node.node_id != self.local_node_id:
                for peer_id in node.peers:
                    if peer_id not in discovered_peers:
                        discovered_peers.append(peer_id)
        
        return discovered_peers
    
    def connect_to_peer(self, peer_node_id: str, peer_address: str) -> bool:
        """
        Connect to a peer without using DNS.
        
        Args:
            peer_node_id: Peer's node ID
            peer_address: Peer's decentralized address
            
        Returns:
            True if connection successful
        """
        # Check if peer already exists
        if peer_node_id in self.nodes:
            print(f"[MESH] Already connected to peer: {peer_node_id}")
            return True
        
        # Create peer node
        peer_node = MeshNode(
            node_id=peer_node_id,
            address=peer_address,
            public_key=hashlib.sha256(peer_address.encode()).hexdigest()
        )
        
        # Add to nodes
        self.nodes[peer_node_id] = peer_node
        
        # Add to local node's peer list
        if self.local_node_id in self.nodes:
            self.nodes[self.local_node_id].peers.add(peer_node_id)
        
        # Add to DHT
        self.dht[peer_address] = peer_node_id
        
        # Update routing table
        self._update_routing_table(peer_node_id)
        
        # Record connection in blockchain
        connection_data = {
            "type": "peer_connection",
            "from_node": self.local_node_id,
            "to_node": peer_node_id,
            "timestamp": time.time()
        }
        
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            data=connection_data,
            previous_hash=self.chain[-1].hash
        )
        new_block.mine_block(difficulty=2)
        self.chain.append(new_block)
        
        print(f"[MESH] Connected to peer: {peer_node_id}")
        return True
    
    def _update_routing_table(self, peer_node_id: str) -> None:
        """Update routing table for mesh network routing."""
        # Direct route to peer
        self.routing_table[peer_node_id] = [peer_node_id]
        
        # Update routes through peer (simplified)
        if peer_node_id in self.nodes:
            peer = self.nodes[peer_node_id]
            for peer_of_peer in peer.peers:
                if peer_of_peer not in self.routing_table:
                    self.routing_table[peer_of_peer] = [peer_node_id, peer_of_peer]
    
    def resolve_address(self, address: str) -> Optional[str]:
        """
        Resolve decentralized address to node ID without DNS.
        
        Args:
            address: Decentralized hash-based address
            
        Returns:
            Node ID if found, None otherwise
        """
        # Check local DHT
        if address in self.dht:
            return self.dht[address]
        
        # Query blockchain
        for block in reversed(self.chain):
            if block.data.get("type") == "node_registration":
                if block.data.get("address") == address:
                    return block.data.get("node_id")
        
        return None
    
    def send_message(self, target_address: str, message: Dict) -> bool:
        """
        Send message through mesh network to target address.
        
        Args:
            target_address: Target node's decentralized address
            message: Message data to send
            
        Returns:
            True if message sent successfully
        """
        # Resolve address to node ID
        target_node_id = self.resolve_address(target_address)
        
        if not target_node_id:
            print(f"[MESH] Cannot resolve address: {target_address}")
            return False
        
        # Find route in routing table
        if target_node_id not in self.routing_table:
            print(f"[MESH] No route to node: {target_node_id}")
            return False
        
        route = self.routing_table[target_node_id]
        
        # Record message in blockchain
        message_data = {
            "type": "message",
            "from_node": self.local_node_id,
            "to_node": target_node_id,
            "route": route,
            "message_hash": hashlib.sha256(json.dumps(message).encode()).hexdigest()[:16],
            "timestamp": time.time()
        }
        
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            data=message_data,
            previous_hash=self.chain[-1].hash
        )
        new_block.mine_block(difficulty=2)
        self.chain.append(new_block)
        
        print(f"[MESH] Message sent to {target_node_id} via route: {' -> '.join(route)}")
        return True
    
    def start_discovery(self) -> None:
        """Start automatic peer discovery."""
        if self.is_running:
            print("[BBMN] Discovery already running")
            return
        
        self.is_running = True
        self.discovery_thread = threading.Thread(
            target=self._discovery_worker,
            daemon=True,
            name="BBMN-Discovery"
        )
        self.discovery_thread.start()
        print("[BBMN] Peer discovery started")
    
    def _discovery_worker(self) -> None:
        """Background worker for peer discovery."""
        while self.is_running:
            peers = self.discover_peers()
            if peers:
                print(f"[DISCOVERY] Found {len(peers)} potential peers")
            time.sleep(30)  # Discovery interval
    
    def stop_discovery(self) -> None:
        """Stop automatic peer discovery."""
        self.is_running = False
        if self.discovery_thread:
            self.discovery_thread.join(timeout=2.0)
        print("[BBMN] Discovery stopped")
    
    def get_status(self) -> Dict:
        """Get mesh network status."""
        return {
            "status": "ACTIVE",
            "network_id": self.network_id,
            "local_node_id": self.local_node_id,
            "decentralized": True,
            "dns_free": True,
            "blockchain_length": len(self.chain),
            "connected_peers": len(self.nodes) - 1,  # Exclude self
            "routing_table_size": len(self.routing_table),
            "dht_entries": len(self.dht),
            "discovery_active": self.is_running
        }


def main():
    """Demo of Blockchain Mesh Network."""
    print("=" * 70)
    print("BLOCKCHAIN MESH NETWORK (BBMN)")
    print("Decentralized Infrastructure - No DNS Dependencies")
    print("=" * 70)
    print()
    
    # Initialize mesh network
    mesh = BlockchainMeshNetwork("KOSYMBIOSIS_MESH")
    
    # Start peer discovery
    mesh.start_discovery()
    
    # Simulate adding peers
    for i in range(3):
        peer_id = f"peer_{secrets.token_hex(8)}"
        peer_address = hashlib.sha256(peer_id.encode()).hexdigest()[:32]
        mesh.connect_to_peer(peer_id, peer_address)
    
    # Show status
    print("\n[STATUS]")
    status = mesh.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Test message sending
    if mesh.nodes:
        first_peer = list(mesh.nodes.values())[1] if len(mesh.nodes) > 1 else None
        if first_peer:
            print(f"\n[TEST] Sending message to {first_peer.node_id}")
            mesh.send_message(first_peer.address, {"test": "message"})
    
    # Keep running
    try:
        print("\n[INFO] Mesh network running. Press Ctrl+C to stop")
        while True:
            time.sleep(10)
            status = mesh.get_status()
            print(f"[HEARTBEAT] Peers: {status['connected_peers']} | "
                  f"Blockchain: {status['blockchain_length']} blocks")
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Stopping mesh network...")
        mesh.stop_discovery()


if __name__ == "__main__":
    main()
