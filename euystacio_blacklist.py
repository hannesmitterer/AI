#!/usr/bin/env python3
"""
EUYSTACIO Permanent Blacklist System
=====================================

This module implements a permanent blacklist (playlist permanente) for the
EUYSTACIO framework to block communication from suspicious nodes and entities
that threaten system security.

Key Features:
- Permanent storage of blacklisted entities
- Support for multiple entity types (nodes, IPs, identifiers)
- Integration with MISP policy triggers
- Automatic persistence to disk
- Thread-safe operations
- Audit logging of all blacklist operations

Based on: EUYSTACIO Framework security requirements
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import hashlib
import threading


class EntityType(Enum):
    """Types of entities that can be blacklisted."""
    NODE = "node"              # Network nodes
    IP_ADDRESS = "ip_address"  # IP addresses from upstream
    IDENTIFIER = "identifier"  # Generic identifiers (AI roles, etc.)


class ThreatLevel(Enum):
    """Threat levels for blacklisted entities."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class BlacklistEntry:
    """Represents a single blacklist entry."""
    entity_id: str
    entity_type: EntityType
    threat_level: ThreatLevel
    reason: str
    timestamp: str
    added_by: str = "EUYSTACIO_SYSTEM"
    misp_trigger: Optional[str] = None
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert entry to dictionary for serialization."""
        return {
            "entity_id": self.entity_id,
            "entity_type": self.entity_type.value,
            "threat_level": self.threat_level.value,
            "reason": self.reason,
            "timestamp": self.timestamp,
            "added_by": self.added_by,
            "misp_trigger": self.misp_trigger,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'BlacklistEntry':
        """Create entry from dictionary."""
        return cls(
            entity_id=data["entity_id"],
            entity_type=EntityType(data["entity_type"]),
            threat_level=ThreatLevel(data["threat_level"]),
            reason=data["reason"],
            timestamp=data["timestamp"],
            added_by=data.get("added_by", "EUYSTACIO_SYSTEM"),
            misp_trigger=data.get("misp_trigger"),
            metadata=data.get("metadata", {})
        )


class PermanentBlacklist:
    """
    Permanent blacklist system for EUYSTACIO framework.
    
    Provides persistent storage and management of blacklisted entities
    to protect the system from security threats.
    """
    
    def __init__(self, storage_path: str = "euystacio_blacklist.json",
                 audit_log_path: str = "euystacio_blacklist_audit.log"):
        """
        Initialize the permanent blacklist.
        
        Args:
            storage_path: Path to permanent storage file
            audit_log_path: Path to audit log file
        """
        self.storage_path = storage_path
        self.audit_log_path = audit_log_path
        self.blacklist: Dict[str, BlacklistEntry] = {}
        self._lock = threading.Lock()
        
        # Load existing blacklist
        self._load_from_disk()
        
        # Log initialization
        self._audit_log("SYSTEM", "Blacklist system initialized")
    
    def _generate_entry_hash(self, entity_id: str, entity_type: EntityType) -> str:
        """Generate unique hash for blacklist entry."""
        data = f"{entity_id}:{entity_type.value}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def _audit_log(self, action: str, details: str) -> None:
        """Write to audit log."""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {action}: {details}\n"
        
        try:
            with open(self.audit_log_path, 'a') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"[BLACKLIST] Warning: Could not write to audit log: {e}")
    
    def _load_from_disk(self) -> None:
        """Load blacklist from permanent storage."""
        if not os.path.exists(self.storage_path):
            self._audit_log("LOAD", "No existing blacklist file, starting fresh")
            return
        
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
            
            # Load entries
            for entry_hash, entry_data in data.get("entries", {}).items():
                entry = BlacklistEntry.from_dict(entry_data)
                self.blacklist[entry_hash] = entry
            
            self._audit_log("LOAD", f"Loaded {len(self.blacklist)} entries from disk")
            print(f"[BLACKLIST] Loaded {len(self.blacklist)} blacklisted entities")
        
        except Exception as e:
            self._audit_log("ERROR", f"Failed to load blacklist: {e}")
            print(f"[BLACKLIST] Error loading blacklist: {e}")
    
    def _save_to_disk(self) -> None:
        """Save blacklist to permanent storage."""
        try:
            data = {
                "version": "1.0.0",
                "last_updated": datetime.now().isoformat(),
                "total_entries": len(self.blacklist),
                "entries": {
                    entry_hash: entry.to_dict()
                    for entry_hash, entry in self.blacklist.items()
                }
            }
            
            # Write atomically using temporary file
            temp_path = f"{self.storage_path}.tmp"
            with open(temp_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            # Atomic rename
            os.replace(temp_path, self.storage_path)
            
            self._audit_log("SAVE", f"Saved {len(self.blacklist)} entries to disk")
        
        except Exception as e:
            self._audit_log("ERROR", f"Failed to save blacklist: {e}")
            print(f"[BLACKLIST] Error saving blacklist: {e}")
    
    def add_entry(self, entity_id: str, entity_type: EntityType,
                  threat_level: ThreatLevel, reason: str,
                  misp_trigger: Optional[str] = None,
                  metadata: Optional[Dict] = None) -> bool:
        """
        Add an entity to the permanent blacklist.
        
        Args:
            entity_id: Unique identifier of the entity to blacklist
            entity_type: Type of entity (NODE, IP_ADDRESS, IDENTIFIER)
            threat_level: Severity of the threat
            reason: Human-readable reason for blacklisting
            misp_trigger: Optional MISP policy trigger identifier
            metadata: Optional additional metadata
        
        Returns:
            True if added successfully, False if already exists
        """
        with self._lock:
            entry_hash = self._generate_entry_hash(entity_id, entity_type)
            
            # Check if already blacklisted
            if entry_hash in self.blacklist:
                self._audit_log("ADD_DUPLICATE", f"Entity already blacklisted: {entity_id}")
                return False
            
            # Create new entry
            entry = BlacklistEntry(
                entity_id=entity_id,
                entity_type=entity_type,
                threat_level=threat_level,
                reason=reason,
                timestamp=datetime.now().isoformat(),
                misp_trigger=misp_trigger,
                metadata=metadata or {}
            )
            
            # Add to blacklist
            self.blacklist[entry_hash] = entry
            
            # Persist to disk
            self._save_to_disk()
            
            # Audit log
            self._audit_log("ADD", 
                f"{entity_type.value}:{entity_id} - {threat_level.value} - {reason}")
            
            print(f"[BLACKLIST] Added: {entity_id} ({entity_type.value}) - {threat_level.value}")
            
            return True
    
    def is_blacklisted(self, entity_id: str, entity_type: EntityType) -> bool:
        """
        Check if an entity is blacklisted.
        
        Args:
            entity_id: Entity identifier to check
            entity_type: Type of entity
        
        Returns:
            True if entity is blacklisted, False otherwise
        """
        with self._lock:
            entry_hash = self._generate_entry_hash(entity_id, entity_type)
            return entry_hash in self.blacklist
    
    def get_entry(self, entity_id: str, entity_type: EntityType) -> Optional[BlacklistEntry]:
        """
        Get blacklist entry for an entity.
        
        Args:
            entity_id: Entity identifier
            entity_type: Type of entity
        
        Returns:
            BlacklistEntry if found, None otherwise
        """
        with self._lock:
            entry_hash = self._generate_entry_hash(entity_id, entity_type)
            return self.blacklist.get(entry_hash)
    
    def remove_entry(self, entity_id: str, entity_type: EntityType) -> bool:
        """
        Remove an entity from the blacklist.
        
        Args:
            entity_id: Entity identifier to remove
            entity_type: Type of entity
        
        Returns:
            True if removed, False if not found
        """
        with self._lock:
            entry_hash = self._generate_entry_hash(entity_id, entity_type)
            
            if entry_hash not in self.blacklist:
                return False
            
            # Remove entry
            del self.blacklist[entry_hash]
            
            # Persist to disk
            self._save_to_disk()
            
            # Audit log
            self._audit_log("REMOVE", f"{entity_type.value}:{entity_id}")
            
            print(f"[BLACKLIST] Removed: {entity_id} ({entity_type.value})")
            
            return True
    
    def get_all_entries(self, entity_type: Optional[EntityType] = None,
                       threat_level: Optional[ThreatLevel] = None) -> List[BlacklistEntry]:
        """
        Get all blacklist entries, optionally filtered.
        
        Args:
            entity_type: Optional filter by entity type
            threat_level: Optional filter by threat level
        
        Returns:
            List of matching blacklist entries
        """
        with self._lock:
            entries = list(self.blacklist.values())
            
            # Apply filters
            if entity_type is not None:
                entries = [e for e in entries if e.entity_type == entity_type]
            
            if threat_level is not None:
                entries = [e for e in entries if e.threat_level == threat_level]
            
            return entries
    
    def get_statistics(self) -> Dict:
        """
        Get blacklist statistics.
        
        Returns:
            Dictionary containing statistics
        """
        with self._lock:
            stats = {
                "total_entries": len(self.blacklist),
                "by_type": {},
                "by_threat_level": {},
                "with_misp_trigger": 0
            }
            
            # Count by type
            for entity_type in EntityType:
                count = sum(1 for e in self.blacklist.values() 
                          if e.entity_type == entity_type)
                stats["by_type"][entity_type.value] = count
            
            # Count by threat level
            for threat_level in ThreatLevel:
                count = sum(1 for e in self.blacklist.values() 
                          if e.threat_level == threat_level)
                stats["by_threat_level"][threat_level.value] = count
            
            # Count MISP triggers
            stats["with_misp_trigger"] = sum(1 for e in self.blacklist.values() 
                                            if e.misp_trigger is not None)
            
            return stats
    
    def clear_all(self, confirm: bool = False) -> bool:
        """
        Clear all entries from blacklist.
        
        Args:
            confirm: Must be True to actually clear
        
        Returns:
            True if cleared, False otherwise
        """
        if not confirm:
            print("[BLACKLIST] Clear operation requires explicit confirmation")
            return False
        
        with self._lock:
            count = len(self.blacklist)
            self.blacklist.clear()
            self._save_to_disk()
            self._audit_log("CLEAR", f"Cleared {count} entries")
            print(f"[BLACKLIST] Cleared all {count} entries")
            return True


# Global blacklist instance for EUYSTACIO framework
_global_blacklist: Optional[PermanentBlacklist] = None


def get_blacklist() -> PermanentBlacklist:
    """Get or create the global blacklist instance."""
    global _global_blacklist
    if _global_blacklist is None:
        _global_blacklist = PermanentBlacklist()
    return _global_blacklist


def initialize_blacklist(storage_path: Optional[str] = None,
                        audit_log_path: Optional[str] = None) -> PermanentBlacklist:
    """
    Initialize or reinitialize the global blacklist.
    
    Args:
        storage_path: Optional custom storage path
        audit_log_path: Optional custom audit log path
    
    Returns:
        Initialized blacklist instance
    """
    global _global_blacklist
    kwargs = {}
    if storage_path:
        kwargs['storage_path'] = storage_path
    if audit_log_path:
        kwargs['audit_log_path'] = audit_log_path
    
    _global_blacklist = PermanentBlacklist(**kwargs)
    return _global_blacklist


# Convenience functions for common operations
def block_node(node_id: str, reason: str, threat_level: ThreatLevel = ThreatLevel.MEDIUM,
               misp_trigger: Optional[str] = None) -> bool:
    """Block a network node."""
    return get_blacklist().add_entry(node_id, EntityType.NODE, threat_level, reason, misp_trigger)


def block_ip(ip_address: str, reason: str, threat_level: ThreatLevel = ThreatLevel.HIGH,
             misp_trigger: Optional[str] = None) -> bool:
    """Block an IP address."""
    return get_blacklist().add_entry(ip_address, EntityType.IP_ADDRESS, threat_level, reason, misp_trigger)


def block_identifier(identifier: str, reason: str, threat_level: ThreatLevel = ThreatLevel.MEDIUM,
                     misp_trigger: Optional[str] = None) -> bool:
    """Block a generic identifier (e.g., AI role, entity ID)."""
    return get_blacklist().add_entry(identifier, EntityType.IDENTIFIER, threat_level, reason, misp_trigger)


def is_node_blocked(node_id: str) -> bool:
    """Check if a node is blocked."""
    return get_blacklist().is_blacklisted(node_id, EntityType.NODE)


def is_ip_blocked(ip_address: str) -> bool:
    """Check if an IP address is blocked."""
    return get_blacklist().is_blacklisted(ip_address, EntityType.IP_ADDRESS)


def is_identifier_blocked(identifier: str) -> bool:
    """Check if an identifier is blocked."""
    return get_blacklist().is_blacklisted(identifier, EntityType.IDENTIFIER)


if __name__ == "__main__":
    """Demo and testing of blacklist functionality."""
    print("="*70)
    print("EUYSTACIO PERMANENT BLACKLIST SYSTEM - DEMO")
    print("="*70)
    print()
    
    # Initialize blacklist
    blacklist = get_blacklist()
    
    # Demo: Add some test entries
    print("Adding test entries...")
    block_node("node_suspicious_001", "Abnormal traffic pattern detected", 
               ThreatLevel.HIGH, "MISP_TRAFFIC_ANOMALY")
    block_node("node_malicious_042", "Attempted unauthorized access", 
               ThreatLevel.CRITICAL, "MISP_UNAUTHORIZED_ACCESS")
    block_ip("192.168.100.50", "Known malicious IP from upstream", 
             ThreatLevel.CRITICAL, "MISP_IP_REPUTATION")
    block_identifier("AI_ROGUE_ENTITY_7", "Suspected AI role compromise", 
                     ThreatLevel.HIGH, "MISP_AI_POLICY_VIOLATION")
    
    print()
    
    # Demo: Check if blocked
    print("Checking blocked status...")
    test_entities = [
        ("node_suspicious_001", EntityType.NODE),
        ("node_legitimate_123", EntityType.NODE),
        ("192.168.100.50", EntityType.IP_ADDRESS),
    ]
    
    for entity_id, entity_type in test_entities:
        blocked = blacklist.is_blacklisted(entity_id, entity_type)
        status = "BLOCKED" if blocked else "ALLOWED"
        print(f"  {entity_id} ({entity_type.value}): {status}")
    
    print()
    
    # Demo: Get statistics
    print("Blacklist Statistics:")
    stats = blacklist.get_statistics()
    print(f"  Total entries: {stats['total_entries']}")
    print(f"  By type:")
    for entity_type, count in stats['by_type'].items():
        print(f"    {entity_type}: {count}")
    print(f"  By threat level:")
    for threat_level, count in stats['by_threat_level'].items():
        print(f"    {threat_level}: {count}")
    print(f"  With MISP trigger: {stats['with_misp_trigger']}")
    
    print()
    
    # Demo: List all entries
    print("All blacklisted entities:")
    for entry in blacklist.get_all_entries():
        print(f"  [{entry.threat_level.value.upper()}] {entry.entity_type.value}:{entry.entity_id}")
        print(f"    Reason: {entry.reason}")
        if entry.misp_trigger:
            print(f"    MISP Trigger: {entry.misp_trigger}")
        print()
    
    print("="*70)
    print("Demo complete. Blacklist persisted to:", blacklist.storage_path)
    print("Audit log available at:", blacklist.audit_log_path)
    print("="*70)
