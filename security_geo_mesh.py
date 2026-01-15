#!/usr/bin/env python3
"""
Geo-Zone Filtering & Mesh Network Module
========================================

This module implements geographic filtering and mesh-based network
architectures to defend against coordinated global attacks.

Features:
- Geo-zone based access control
- Suspicious activity isolation
- Mesh network topology
- Decentralized communication
- Network resilience mechanisms
"""

import time
import random
import hashlib
from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict


class GeoZone(Enum):
    """Geographic zones for filtering."""
    EUROPE = "EUROPE"
    NORTH_AMERICA = "NORTH_AMERICA"
    SOUTH_AMERICA = "SOUTH_AMERICA"
    ASIA = "ASIA"
    AFRICA = "AFRICA"
    OCEANIA = "OCEANIA"
    UNKNOWN = "UNKNOWN"


class ThrustLevel(Enum):
    """Trust levels for geo-zones."""
    TRUSTED = 3
    NEUTRAL = 2
    SUSPICIOUS = 1
    BLOCKED = 0


@dataclass
class GeoLocation:
    """Geographic location information."""
    latitude: float
    longitude: float
    zone: GeoZone
    country_code: str
    
    def distance_to(self, other: 'GeoLocation') -> float:
        """
        Calculate approximate distance to another location (km).
        
        Args:
            other: Other geo location
            
        Returns:
            Distance in kilometers
        """
        # Haversine formula
        R = 6371  # Earth radius in km
        
        lat1, lon1 = self.latitude, self.longitude
        lat2, lon2 = other.latitude, other.longitude
        
        import math
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = (math.sin(dlat/2) ** 2 + 
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
             math.sin(dlon/2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c


@dataclass
class NetworkNode:
    """Mesh network node."""
    node_id: str
    location: GeoLocation
    is_active: bool = True
    trust_level: ThrustLevel = ThrustLevel.NEUTRAL
    connections: Set[str] = field(default_factory=set)
    
    # Statistics
    packets_sent: int = 0
    packets_received: int = 0
    packets_dropped: int = 0
    last_activity: float = 0.0


@dataclass
class NetworkPacket:
    """Network packet for mesh routing."""
    packet_id: str
    source_node: str
    destination_node: str
    data: bytes
    timestamp: float
    ttl: int = 10  # Time to live (hop count)
    route_history: List[str] = field(default_factory=list)


class GeoZoneFilter:
    """
    Geographic zone-based filtering system.
    
    Isolates suspicious activities based on geographic origin.
    """
    
    def __init__(self):
        """Initialize geo-zone filter."""
        self.zone_trust_levels: Dict[GeoZone, ThrustLevel] = {
            zone: ThrustLevel.NEUTRAL for zone in GeoZone
        }
        
        self.blocked_zones: Set[GeoZone] = set()
        self.suspicious_ips: Set[str] = set()
        
        # Activity tracking
        self.zone_activity: Dict[GeoZone, int] = defaultdict(int)
        self.zone_threats: Dict[GeoZone, int] = defaultdict(int)
        
    def set_zone_trust(self, zone: GeoZone, trust_level: ThrustLevel) -> None:
        """
        Set trust level for a geographic zone.
        
        Args:
            zone: Geographic zone
            trust_level: Trust level to set
        """
        self.zone_trust_levels[zone] = trust_level
        
        if trust_level == ThrustLevel.BLOCKED:
            self.blocked_zones.add(zone)
        elif zone in self.blocked_zones:
            self.blocked_zones.remove(zone)
    
    def check_access(self, location: GeoLocation, ip_address: str) -> bool:
        """
        Check if access should be granted based on location.
        
        Args:
            location: Geographic location
            ip_address: IP address
            
        Returns:
            True if access granted
        """
        # Check if zone is blocked
        if location.zone in self.blocked_zones:
            return False
        
        # Check if IP is suspicious
        if ip_address in self.suspicious_ips:
            return False
        
        # Check trust level
        trust = self.zone_trust_levels.get(location.zone, ThrustLevel.NEUTRAL)
        
        # Record activity
        self.zone_activity[location.zone] += 1
        
        return trust != ThrustLevel.BLOCKED
    
    def report_suspicious_activity(self, location: GeoLocation, 
                                   ip_address: str) -> None:
        """
        Report suspicious activity from a location.
        
        Args:
            location: Geographic location
            ip_address: IP address
        """
        self.zone_threats[location.zone] += 1
        self.suspicious_ips.add(ip_address)
        
        # Auto-adjust trust level based on threat count
        threat_count = self.zone_threats[location.zone]
        activity_count = self.zone_activity[location.zone]
        
        if activity_count > 0:
            threat_ratio = threat_count / activity_count
            
            if threat_ratio > 0.5:  # More than 50% threats
                self.set_zone_trust(location.zone, ThrustLevel.BLOCKED)
            elif threat_ratio > 0.2:  # More than 20% threats
                self.set_zone_trust(location.zone, ThrustLevel.SUSPICIOUS)
    
    def isolate_zone(self, zone: GeoZone) -> Dict[str, any]:
        """
        Isolate a geographic zone (block all traffic).
        
        Args:
            zone: Zone to isolate
            
        Returns:
            Isolation report
        """
        self.set_zone_trust(zone, ThrustLevel.BLOCKED)
        
        return {
            "zone": zone.value,
            "action": "ISOLATED",
            "trust_level": ThrustLevel.BLOCKED.value,
            "timestamp": time.time(),
            "threat_count": self.zone_threats[zone],
            "activity_count": self.zone_activity[zone]
        }
    
    def get_zone_statistics(self) -> Dict[str, any]:
        """Get statistics for all zones."""
        stats = {}
        
        for zone in GeoZone:
            stats[zone.value] = {
                "trust_level": self.zone_trust_levels[zone].value,
                "is_blocked": zone in self.blocked_zones,
                "activity_count": self.zone_activity[zone],
                "threat_count": self.zone_threats[zone],
                "threat_ratio": (self.zone_threats[zone] / self.zone_activity[zone]
                               if self.zone_activity[zone] > 0 else 0)
            }
        
        return stats


class MeshNetwork:
    """
    Decentralized mesh network for resilient communication.
    
    Implements peer-to-peer routing without central authority.
    """
    
    def __init__(self):
        """Initialize mesh network."""
        self.nodes: Dict[str, NetworkNode] = {}
        self.routing_table: Dict[Tuple[str, str], List[str]] = {}
        
        # Statistics
        self.total_packets_routed = 0
        self.failed_routes = 0
        
    def add_node(self, node: NetworkNode) -> None:
        """
        Add node to mesh network.
        
        Args:
            node: Network node to add
        """
        self.nodes[node.node_id] = node
        self._update_routing_table()
    
    def remove_node(self, node_id: str) -> None:
        """
        Remove node from mesh network.
        
        Args:
            node_id: Node ID to remove
        """
        if node_id in self.nodes:
            # Remove connections to this node
            for other_node in self.nodes.values():
                if node_id in other_node.connections:
                    other_node.connections.remove(node_id)
            
            del self.nodes[node_id]
            self._update_routing_table()
    
    def connect_nodes(self, node1_id: str, node2_id: str) -> bool:
        """
        Create bidirectional connection between nodes.
        
        Args:
            node1_id: First node ID
            node2_id: Second node ID
            
        Returns:
            True if connected successfully
        """
        if node1_id not in self.nodes or node2_id not in self.nodes:
            return False
        
        self.nodes[node1_id].connections.add(node2_id)
        self.nodes[node2_id].connections.add(node1_id)
        
        self._update_routing_table()
        return True
    
    def _find_route(self, source: str, destination: str) -> Optional[List[str]]:
        """
        Find route from source to destination using breadth-first search.
        
        Args:
            source: Source node ID
            destination: Destination node ID
            
        Returns:
            List of node IDs forming the route, or None
        """
        if source not in self.nodes or destination not in self.nodes:
            return None
        
        if source == destination:
            return [source]
        
        # BFS for shortest path
        from collections import deque
        
        queue = deque([(source, [source])])
        visited = {source}
        
        while queue:
            current, path = queue.popleft()
            
            # Check neighbors
            for neighbor in self.nodes[current].connections:
                if neighbor == destination:
                    return path + [neighbor]
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None  # No route found
    
    def _update_routing_table(self) -> None:
        """Update routing table for all node pairs."""
        # Clear existing routes
        self.routing_table.clear()
        
        # Compute routes for all pairs
        node_ids = list(self.nodes.keys())
        for source in node_ids:
            for dest in node_ids:
                if source != dest:
                    route = self._find_route(source, dest)
                    if route:
                        self.routing_table[(source, dest)] = route
    
    def route_packet(self, packet: NetworkPacket) -> bool:
        """
        Route packet through mesh network.
        
        Args:
            packet: Packet to route
            
        Returns:
            True if delivered successfully
        """
        # Check TTL
        if packet.ttl <= 0:
            self.failed_routes += 1
            return False
        
        # Get route
        route_key = (packet.source_node, packet.destination_node)
        route = self.routing_table.get(route_key)
        
        if not route:
            self.failed_routes += 1
            return False
        
        # Simulate routing through each hop
        for hop in route:
            if hop not in self.nodes or not self.nodes[hop].is_active:
                self.failed_routes += 1
                return False
            
            # Update node statistics
            node = self.nodes[hop]
            node.last_activity = time.time()
            
            if hop == packet.source_node:
                node.packets_sent += 1
            elif hop == packet.destination_node:
                node.packets_received += 1
            
            packet.route_history.append(hop)
            packet.ttl -= 1
        
        self.total_packets_routed += 1
        return True
    
    def get_network_resilience(self) -> Dict[str, any]:
        """
        Calculate network resilience metrics.
        
        Returns:
            Resilience metrics
        """
        total_nodes = len(self.nodes)
        active_nodes = sum(1 for n in self.nodes.values() if n.is_active)
        
        # Calculate connectivity (percentage of node pairs with routes)
        total_pairs = total_nodes * (total_nodes - 1)
        connected_pairs = len(self.routing_table)
        connectivity = connected_pairs / total_pairs if total_pairs > 0 else 0
        
        # Calculate average path length
        if self.routing_table:
            avg_path_length = sum(len(route) for route in self.routing_table.values()) / \
                            len(self.routing_table)
        else:
            avg_path_length = 0
        
        return {
            "total_nodes": total_nodes,
            "active_nodes": active_nodes,
            "connectivity": connectivity,
            "average_path_length": avg_path_length,
            "total_packets_routed": self.total_packets_routed,
            "failed_routes": self.failed_routes,
            "success_rate": (self.total_packets_routed / 
                           (self.total_packets_routed + self.failed_routes)
                           if self.total_packets_routed + self.failed_routes > 0 
                           else 0)
        }


def main():
    """Demonstrate geo-filtering and mesh networking."""
    print("=" * 70)
    print("GEO-ZONE FILTERING & MESH NETWORK")
    print("=" * 70)
    
    # Initialize geo-zone filter
    print("\n[1] Initializing geo-zone filter...")
    geo_filter = GeoZoneFilter()
    print("    Filter initialized")
    
    # Test access control
    print("\n[2] Testing geo-zone access control...")
    test_location = GeoLocation(
        latitude=48.8566,
        longitude=2.3522,
        zone=GeoZone.EUROPE,
        country_code="FR"
    )
    
    access_granted = geo_filter.check_access(test_location, "192.168.1.100")
    print(f"    Access from {test_location.zone.value}: {access_granted}")
    
    # Simulate suspicious activity
    print("\n[3] Simulating suspicious activity...")
    suspicious_location = GeoLocation(
        latitude=40.7128,
        longitude=-74.0060,
        zone=GeoZone.NORTH_AMERICA,
        country_code="US"
    )
    
    for i in range(10):
        geo_filter.check_access(suspicious_location, f"10.0.0.{i}")
        if i % 2 == 0:
            geo_filter.report_suspicious_activity(suspicious_location, f"10.0.0.{i}")
    
    # Check zone statistics
    stats = geo_filter.get_zone_statistics()
    print(f"    {GeoZone.NORTH_AMERICA.value} threat ratio: "
          f"{stats[GeoZone.NORTH_AMERICA.value]['threat_ratio']:.2%}")
    
    # Initialize mesh network
    print("\n[4] Initializing mesh network...")
    mesh = MeshNetwork()
    
    # Create nodes
    nodes = []
    for i in range(6):
        location = GeoLocation(
            latitude=random.uniform(-90, 90),
            longitude=random.uniform(-180, 180),
            zone=random.choice(list(GeoZone)),
            country_code="XX"
        )
        node = NetworkNode(
            node_id=f"node_{i}",
            location=location
        )
        nodes.append(node)
        mesh.add_node(node)
    
    print(f"    Created {len(nodes)} mesh nodes")
    
    # Create mesh connections
    print("\n[5] Creating mesh connections...")
    mesh.connect_nodes("node_0", "node_1")
    mesh.connect_nodes("node_1", "node_2")
    mesh.connect_nodes("node_2", "node_3")
    mesh.connect_nodes("node_0", "node_3")
    mesh.connect_nodes("node_3", "node_4")
    mesh.connect_nodes("node_4", "node_5")
    mesh.connect_nodes("node_2", "node_5")
    print("    Mesh topology created")
    
    # Route packets
    print("\n[6] Routing packets through mesh...")
    for i in range(5):
        packet = NetworkPacket(
            packet_id=f"pkt_{i}",
            source_node="node_0",
            destination_node="node_5",
            data=f"Message {i}".encode(),
            timestamp=time.time()
        )
        
        success = mesh.route_packet(packet)
        print(f"    Packet {i}: {'✓ Delivered' if success else '✗ Failed'} "
              f"(route: {' -> '.join(packet.route_history)})")
    
    # Network resilience
    resilience = mesh.get_network_resilience()
    print(f"\n[7] Network resilience metrics:")
    print(f"    Active nodes: {resilience['active_nodes']}/{resilience['total_nodes']}")
    print(f"    Connectivity: {resilience['connectivity']:.2%}")
    print(f"    Avg path length: {resilience['average_path_length']:.1f} hops")
    print(f"    Success rate: {resilience['success_rate']:.2%}")
    
    print("\n" + "=" * 70)
    print("Geo-filtering and mesh network demonstration complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
