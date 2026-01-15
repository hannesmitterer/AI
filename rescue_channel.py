#!/usr/bin/env python3
"""
Rescue Channel (Canale di Soccorso) - Lex Amoris Messaging
===========================================================

This module implements emergency messaging based on Lex Amoris principles
to unblock critical nodes in case of temporary false positives. Provides
a communication channel for resolving deadlocks and conflicts.

Key Features:
- Lex Amoris-based messaging protocol
- False positive detection and resolution
- Critical node unblocking
- Integration with Eternal Deposition System
"""

import time
import math
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class MessagePriority(Enum):
    """Message priority levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
    EMERGENCY = 5


class NodeStatus(Enum):
    """Node operational status."""
    OPERATIONAL = "operational"
    DEGRADED = "degraded"
    BLOCKED = "blocked"
    CRITICAL = "critical"
    RECOVERING = "recovering"


@dataclass
class RescueMessage:
    """Represents a rescue channel message."""
    message_id: str
    sender_node: str
    recipient_node: Optional[str]  # None for broadcast
    priority: MessagePriority
    message_type: str  # "unblock", "resolve", "status", "resonance_sync"
    content: Dict
    timestamp: float
    lex_amoris_signature: float  # Resonance signature for authenticity
    processed: bool = False
    response: Optional[str] = None
    
    def is_authentic(self) -> bool:
        """
        Verify message authenticity via Lex Amoris signature.
        
        Authentic messages resonate at universal frequency (0.043 Hz).
        """
        # Signature should be close to 0.043 Hz resonance
        return 0.038 <= self.lex_amoris_signature <= 0.048
    
    def calculate_urgency_score(self) -> float:
        """
        Calculate message urgency based on priority and age.
        
        Returns:
            Urgency score (0.0 to 1.0)
        """
        # Base score from priority
        priority_score = self.priority.value / 5.0
        
        # Age factor (older messages may be less urgent)
        age_seconds = time.time() - self.timestamp
        age_factor = 1.0 / (1.0 + age_seconds / 60.0)  # Decay over minutes
        
        return priority_score * age_factor


@dataclass
class CriticalNode:
    """Represents a node in critical state needing rescue."""
    node_id: str
    status: NodeStatus
    issue_description: str
    timestamp: float
    false_positive_detected: bool = False
    rescue_requested: bool = False
    rescue_completed: bool = False
    attempts: int = 0
    
    def needs_rescue(self) -> bool:
        """Check if node needs rescue intervention."""
        return (
            self.status in [NodeStatus.BLOCKED, NodeStatus.CRITICAL] and
            not self.rescue_completed
        )


class RescueChannel:
    """
    Rescue Channel - Emergency messaging and node recovery.
    
    Implements Lex Amoris-based communication protocol for resolving
    false positives and unblocking critical nodes.
    """
    
    def __init__(self, universal_frequency: float = 0.043):
        """
        Initialize rescue channel.
        
        Args:
            universal_frequency: Resonance frequency for message signing (Hz)
        """
        self.universal_frequency = universal_frequency
        self.messages: List[RescueMessage] = []
        self.critical_nodes: Dict[str, CriticalNode] = {}
        self.message_count = 0
        self.successful_rescues = 0
        self.failed_rescues = 0
        self.start_time = time.time()
        self.message_handlers: Dict[str, Callable] = {}
        
        # Register default message handlers
        self._register_default_handlers()
        
        print(f"[RESCUE CHANNEL] Initialized")
        print(f"[RESCUE CHANNEL] Resonance frequency: {universal_frequency} Hz")
        print(f"[RESCUE CHANNEL] Based on Lex Amoris principles")
    
    def _register_default_handlers(self) -> None:
        """Register default message type handlers."""
        self.message_handlers["unblock"] = self._handle_unblock_request
        self.message_handlers["resolve"] = self._handle_resolve_request
        self.message_handlers["status"] = self._handle_status_request
        self.message_handlers["resonance_sync"] = self._handle_resonance_sync
    
    def _calculate_lex_amoris_signature(self, message_content: str) -> float:
        """
        Calculate Lex Amoris signature for message.
        
        Signature is based on universal resonance frequency with
        content-based phase adjustment.
        
        Args:
            message_content: Message content string
            
        Returns:
            Resonance signature (frequency in Hz)
        """
        # Base frequency
        signature = self.universal_frequency
        
        # Add small phase adjustment based on content
        content_hash = hash(message_content)
        phase_adjustment = (content_hash % 100) / 10000.0  # ±0.01 Hz
        
        signature += phase_adjustment - 0.005
        
        return signature
    
    def send_message(self, sender_node: str, recipient_node: Optional[str],
                    priority: MessagePriority, message_type: str,
                    content: Dict) -> RescueMessage:
        """
        Send a rescue channel message.
        
        Args:
            sender_node: Sending node ID
            recipient_node: Recipient node ID (None for broadcast)
            priority: Message priority
            message_type: Type of message
            content: Message content dictionary
            
        Returns:
            Created RescueMessage
        """
        self.message_count += 1
        message_id = f"rescue_{self.message_count:06d}_{int(time.time())}"
        
        # Calculate Lex Amoris signature
        content_str = str(content)
        signature = self._calculate_lex_amoris_signature(content_str)
        
        message = RescueMessage(
            message_id=message_id,
            sender_node=sender_node,
            recipient_node=recipient_node,
            priority=priority,
            message_type=message_type,
            content=content,
            timestamp=time.time(),
            lex_amoris_signature=signature,
            processed=False
        )
        
        self.messages.append(message)
        
        # Keep only recent messages (last 1000)
        if len(self.messages) > 1000:
            self.messages = self.messages[-1000:]
        
        print(f"[RESCUE CHANNEL] Message sent: {message_id}")
        print(f"[RESCUE CHANNEL] Type: {message_type} | Priority: {priority.name}")
        
        return message
    
    def process_message(self, message: RescueMessage) -> bool:
        """
        Process a rescue channel message.
        
        Args:
            message: Message to process
            
        Returns:
            True if processing successful
        """
        if message.processed:
            return True
        
        # Verify authenticity
        if not message.is_authentic():
            print(f"[RESCUE CHANNEL] ✗ Message {message.message_id} failed authenticity check")
            message.response = "REJECTED: Invalid Lex Amoris signature"
            message.processed = True
            return False
        
        # Get handler for message type
        handler = self.message_handlers.get(message.message_type)
        
        if not handler:
            print(f"[RESCUE CHANNEL] ✗ No handler for message type: {message.message_type}")
            message.response = f"ERROR: Unknown message type {message.message_type}"
            message.processed = True
            return False
        
        # Process with handler
        try:
            success = handler(message)
            message.processed = True
            return success
        except Exception as e:
            print(f"[RESCUE CHANNEL] ✗ Error processing message: {e}")
            message.response = f"ERROR: {str(e)}"
            message.processed = True
            return False
    
    def _handle_unblock_request(self, message: RescueMessage) -> bool:
        """Handle request to unblock a critical node."""
        node_id = message.content.get("node_id")
        
        if not node_id:
            message.response = "ERROR: node_id required"
            return False
        
        # Check if node is registered as critical
        if node_id in self.critical_nodes:
            critical_node = self.critical_nodes[node_id]
            
            if critical_node.status == NodeStatus.BLOCKED:
                # Perform unblock
                critical_node.status = NodeStatus.RECOVERING
                critical_node.rescue_requested = True
                critical_node.attempts += 1
                
                message.response = f"SUCCESS: Node {node_id} unblocking initiated"
                print(f"[RESCUE CHANNEL] ✓ Unblocking node {node_id}")
                
                return True
        
        message.response = f"INFO: Node {node_id} not in blocked state"
        return True
    
    def _handle_resolve_request(self, message: RescueMessage) -> bool:
        """Handle false positive resolution request."""
        node_id = message.content.get("node_id")
        
        if not node_id:
            message.response = "ERROR: node_id required"
            return False
        
        if node_id in self.critical_nodes:
            critical_node = self.critical_nodes[node_id]
            
            # Mark as false positive
            critical_node.false_positive_detected = True
            critical_node.status = NodeStatus.RECOVERING
            
            message.response = f"SUCCESS: False positive resolved for node {node_id}"
            print(f"[RESCUE CHANNEL] ✓ Resolved false positive for node {node_id}")
            
            self.successful_rescues += 1
            
            return True
        
        message.response = f"ERROR: Node {node_id} not found in critical nodes"
        return False
    
    def _handle_status_request(self, message: RescueMessage) -> bool:
        """Handle status request."""
        node_id = message.content.get("node_id")
        
        if node_id and node_id in self.critical_nodes:
            critical_node = self.critical_nodes[node_id]
            message.response = f"STATUS: {critical_node.status.value}"
        else:
            # Return overall channel status
            stats = self.get_statistics()
            message.response = f"CHANNEL_STATUS: {stats['critical_nodes_count']} critical nodes"
        
        return True
    
    def _handle_resonance_sync(self, message: RescueMessage) -> bool:
        """Handle resonance synchronization message."""
        target_frequency = message.content.get("frequency")
        
        if target_frequency and abs(target_frequency - self.universal_frequency) < 0.01:
            message.response = "SUCCESS: Resonance synchronized"
            print(f"[RESCUE CHANNEL] ✓ Resonance sync: {target_frequency} Hz")
            return True
        
        message.response = f"ERROR: Frequency {target_frequency} out of resonance"
        return False
    
    def register_critical_node(self, node_id: str, status: NodeStatus,
                              issue_description: str) -> CriticalNode:
        """
        Register a node as critical.
        
        Args:
            node_id: Node identifier
            status: Current node status
            issue_description: Description of the issue
            
        Returns:
            CriticalNode instance
        """
        critical_node = CriticalNode(
            node_id=node_id,
            status=status,
            issue_description=issue_description,
            timestamp=time.time()
        )
        
        self.critical_nodes[node_id] = critical_node
        
        print(f"[RESCUE CHANNEL] Node {node_id} registered as {status.value}")
        print(f"[RESCUE CHANNEL] Issue: {issue_description}")
        
        return critical_node
    
    def request_rescue(self, node_id: str, reason: str = "false_positive") -> RescueMessage:
        """
        Request rescue for a critical node.
        
        Args:
            node_id: Node needing rescue
            reason: Reason for rescue request
            
        Returns:
            Rescue message
        """
        content = {
            "node_id": node_id,
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        }
        
        return self.send_message(
            sender_node=node_id,
            recipient_node=None,  # Broadcast
            priority=MessagePriority.EMERGENCY,
            message_type="resolve",
            content=content
        )
    
    def process_pending_messages(self) -> int:
        """
        Process all pending messages.
        
        Returns:
            Number of messages processed
        """
        pending = [m for m in self.messages if not m.processed]
        
        # Sort by urgency
        pending.sort(key=lambda m: m.calculate_urgency_score(), reverse=True)
        
        processed_count = 0
        for message in pending:
            if self.process_message(message):
                processed_count += 1
        
        return processed_count
    
    def get_statistics(self) -> Dict:
        """Get rescue channel statistics."""
        uptime = time.time() - self.start_time
        
        return {
            "uptime_seconds": uptime,
            "total_messages": len(self.messages),
            "processed_messages": sum(1 for m in self.messages if m.processed),
            "pending_messages": sum(1 for m in self.messages if not m.processed),
            "critical_nodes_count": len(self.critical_nodes),
            "successful_rescues": self.successful_rescues,
            "failed_rescues": self.failed_rescues,
            "universal_frequency_hz": self.universal_frequency
        }
    
    def get_critical_nodes_status(self) -> List[Dict]:
        """Get status of all critical nodes."""
        return [
            {
                "node_id": node.node_id,
                "status": node.status.value,
                "issue": node.issue_description,
                "false_positive": node.false_positive_detected,
                "rescue_requested": node.rescue_requested,
                "rescue_completed": node.rescue_completed,
                "attempts": node.attempts,
                "age_seconds": time.time() - node.timestamp
            }
            for node in self.critical_nodes.values()
        ]


def main():
    """Demonstration of rescue channel system."""
    print("=" * 70)
    print("RESCUE CHANNEL - Lex Amoris Messaging Demo")
    print("Emergency Communication and Node Recovery")
    print("=" * 70)
    print()
    
    rescue = RescueChannel(universal_frequency=0.043)
    
    # Simulate critical nodes
    print("\n[SETUP] Registering critical nodes...")
    rescue.register_critical_node(
        "node_0042",
        NodeStatus.BLOCKED,
        "Rhythm validation false positive"
    )
    rescue.register_critical_node(
        "node_0137",
        NodeStatus.CRITICAL,
        "Energy threshold temporary anomaly"
    )
    
    # Test 1: Send unblock request
    print("\n[TEST 1] Sending unblock request...")
    msg1 = rescue.send_message(
        sender_node="control_center",
        recipient_node="node_0042",
        priority=MessagePriority.HIGH,
        message_type="unblock",
        content={"node_id": "node_0042"}
    )
    
    # Test 2: Send false positive resolution
    print("\n[TEST 2] Sending false positive resolution...")
    msg2 = rescue.request_rescue("node_0042", "rhythm_validation_false_positive")
    
    # Test 3: Status request
    print("\n[TEST 3] Requesting status...")
    msg3 = rescue.send_message(
        sender_node="monitor",
        recipient_node=None,
        priority=MessagePriority.MEDIUM,
        message_type="status",
        content={"node_id": "node_0042"}
    )
    
    # Test 4: Resonance sync
    print("\n[TEST 4] Sending resonance sync...")
    msg4 = rescue.send_message(
        sender_node="resonance_controller",
        recipient_node=None,
        priority=MessagePriority.CRITICAL,
        message_type="resonance_sync",
        content={"frequency": 0.043}
    )
    
    # Process all messages
    print("\n[PROCESSING] Processing pending messages...")
    processed = rescue.process_pending_messages()
    print(f"  Processed {processed} messages")
    
    # Display message results
    print("\n" + "-" * 70)
    print("Message Results:")
    for msg in rescue.messages:
        status = "✓ PROCESSED" if msg.processed else "○ PENDING"
        print(f"  [{status}] {msg.message_id}")
        print(f"    Type: {msg.message_type} | Priority: {msg.priority.name}")
        print(f"    Authentic: {'✓' if msg.is_authentic() else '✗'}")
        if msg.response:
            print(f"    Response: {msg.response}")
    
    # Display statistics
    print("\n" + "-" * 70)
    print("Statistics:")
    stats = rescue.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.4f}")
        else:
            print(f"  {key}: {value}")
    
    # Display critical nodes
    print("\n" + "-" * 70)
    print("Critical Nodes Status:")
    nodes = rescue.get_critical_nodes_status()
    for node in nodes:
        print(f"  Node: {node['node_id']}")
        print(f"    Status: {node['status']}")
        print(f"    Issue: {node['issue']}")
        print(f"    False Positive: {'✓' if node['false_positive'] else '○'}")
        print(f"    Rescue Attempts: {node['attempts']}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
