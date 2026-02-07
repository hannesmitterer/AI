#!/usr/bin/env python3
"""
Lazy Security - Energy-Based Protection System
===============================================

This module implements energy-efficient security based on Lex Amoris principles.
Protection algorithms activate only when the Rotesschild scan detects electromagnetic
pressure exceeding 50 mV/m, conserving energy during peaceful periods.

Key Features:
- Electromagnetic field monitoring (Rotesschild scan)
- Threshold-based activation (50 mV/m)
- Energy conservation during low-threat periods
- Integration with Eternal Deposition System
"""

import time
import math
import random
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime


# Security activation threshold
ROTESSCHILD_THRESHOLD_MV_M = 50.0  # Activation threshold in mV/m
SCAN_INTERVAL_SECONDS = 5.0  # How often to scan environment
DEACTIVATION_DELAY_SECONDS = 30.0  # Time to wait before deactivating after threat passes

# Simulation parameters
BASE_FIELD_STRENGTH_MV_M = 30.0  # Base electromagnetic field strength for simulation


@dataclass
class RotesschildScan:
    """Represents a Rotesschild electromagnetic field scan result."""
    timestamp: float
    field_strength_mv_m: float
    threat_level: str  # "none", "low", "medium", "high", "critical"
    location: str = "node_center"
    
    def exceeds_threshold(self) -> bool:
        """Check if field strength exceeds activation threshold."""
        return self.field_strength_mv_m >= ROTESSCHILD_THRESHOLD_MV_M
    
    def calculate_threat_level(self) -> str:
        """Calculate threat level based on field strength."""
        strength = self.field_strength_mv_m
        
        if strength < 20:
            return "none"
        elif strength < 50:
            return "low"
        elif strength < 100:
            return "medium"
        elif strength < 200:
            return "high"
        else:
            return "critical"


@dataclass
class ProtectionModule:
    """Represents a security protection module."""
    module_id: str
    name: str
    energy_cost: float  # Energy cost when active (arbitrary units)
    is_active: bool = False
    activation_count: int = 0
    total_active_time: float = 0.0
    last_activation: Optional[float] = None
    last_deactivation: Optional[float] = None
    
    def activate(self) -> None:
        """Activate the protection module."""
        if not self.is_active:
            self.is_active = True
            self.activation_count += 1
            self.last_activation = time.time()
    
    def deactivate(self) -> None:
        """Deactivate the protection module."""
        if self.is_active:
            self.is_active = False
            self.last_deactivation = time.time()
            
            if self.last_activation:
                self.total_active_time += (time.time() - self.last_activation)


class LazySecurityEngine:
    """
    Lazy Security Engine - Energy-based protection activation.
    
    Monitors electromagnetic field strength via Rotesschild scans and
    activates protection modules only when necessary, conserving energy
    during peaceful periods.
    """
    
    def __init__(self, auto_scan: bool = True):
        """
        Initialize lazy security engine.
        
        Args:
            auto_scan: If True, automatically scan environment periodically
        """
        self.auto_scan = auto_scan
        self.is_active = False
        self.protection_modules: Dict[str, ProtectionModule] = {}
        self.scan_history: List[RotesschildScan] = []
        self.last_scan_time: Optional[float] = None
        self.last_threat_time: Optional[float] = None
        self.start_time = time.time()
        self.total_energy_saved = 0.0
        
        # Initialize default protection modules
        self._initialize_protection_modules()
        
        print(f"[LAZY SECURITY] Initialized")
        print(f"[LAZY SECURITY] Activation threshold: {ROTESSCHILD_THRESHOLD_MV_M} mV/m")
        print(f"[LAZY SECURITY] Auto-scan: {auto_scan}")
        print(f"[LAZY SECURITY] Protection modules: {len(self.protection_modules)}")
    
    def _initialize_protection_modules(self) -> None:
        """Initialize default protection modules."""
        default_modules = [
            ProtectionModule("firewall", "Adaptive Firewall", energy_cost=10.0),
            ProtectionModule("intrusion_detect", "Intrusion Detection", energy_cost=15.0),
            ProtectionModule("encryption", "Dynamic Encryption", energy_cost=20.0),
            ProtectionModule("anomaly_detect", "Anomaly Detection", energy_cost=12.0),
            ProtectionModule("ddos_protect", "DDoS Protection", energy_cost=18.0),
        ]
        
        for module in default_modules:
            self.protection_modules[module.module_id] = module
    
    def perform_rotesschild_scan(self, simulate: bool = True) -> RotesschildScan:
        """
        Perform electromagnetic field scan.
        
        Args:
            simulate: If True, simulate scan results (for demonstration)
            
        Returns:
            RotesschildScan result
        """
        current_time = time.time()
        
        if simulate:
            # Simulate field strength with some variability
            # Base level around BASE_FIELD_STRENGTH_MV_M with random fluctuations
            
            # Add time-based variations (simulated external factors)
            time_factor = math.sin(current_time * 0.1) * 20.0
            
            # Add random noise
            noise = random.gauss(0, 10.0)
            
            field_strength = max(0, BASE_FIELD_STRENGTH_MV_M + time_factor + noise)
        else:
            # In real implementation, this would interface with actual sensors
            field_strength = 0.0
        
        scan = RotesschildScan(
            timestamp=current_time,
            field_strength_mv_m=field_strength,
            threat_level=RotesschildScan.calculate_threat_level(
                RotesschildScan(current_time, field_strength, "")
            )
        )
        
        self.scan_history.append(scan)
        
        # Keep only recent history (last 1000 scans)
        if len(self.scan_history) > 1000:
            self.scan_history = self.scan_history[-1000:]
        
        self.last_scan_time = current_time
        
        return scan
    
    def should_activate_protection(self) -> bool:
        """
        Determine if protection should be activated based on recent scans.
        
        Returns:
            True if protection should be active
        """
        if not self.scan_history:
            return False
        
        latest_scan = self.scan_history[-1]
        
        # Activate if latest scan exceeds threshold
        if latest_scan.exceeds_threshold():
            self.last_threat_time = time.time()
            return True
        
        # Keep active for delay period after threat passes
        if self.last_threat_time:
            time_since_threat = time.time() - self.last_threat_time
            if time_since_threat < DEACTIVATION_DELAY_SECONDS:
                return True
        
        return False
    
    def activate_protection(self) -> None:
        """Activate all protection modules."""
        if self.is_active:
            return
        
        self.is_active = True
        
        for module in self.protection_modules.values():
            module.activate()
        
        print(f"[LAZY SECURITY] Protection ACTIVATED - {len(self.protection_modules)} modules online")
    
    def deactivate_protection(self) -> None:
        """Deactivate all protection modules to conserve energy."""
        if not self.is_active:
            return
        
        self.is_active = False
        
        # Calculate energy saved during this deactivation
        total_cost = sum(m.energy_cost for m in self.protection_modules.values())
        
        for module in self.protection_modules.values():
            module.deactivate()
        
        print(f"[LAZY SECURITY] Protection DEACTIVATED - conserving {total_cost:.2f} energy units")
        self.total_energy_saved += total_cost
    
    def update_protection_status(self) -> None:
        """Update protection status based on current threat level."""
        should_activate = self.should_activate_protection()
        
        if should_activate and not self.is_active:
            self.activate_protection()
        elif not should_activate and self.is_active:
            self.deactivate_protection()
    
    def scan_and_update(self) -> RotesschildScan:
        """
        Perform scan and update protection status.
        
        Returns:
            Latest scan result
        """
        scan = self.perform_rotesschild_scan()
        self.update_protection_status()
        
        return scan
    
    def get_current_energy_consumption(self) -> float:
        """
        Calculate current energy consumption.
        
        Returns:
            Energy consumption rate (units per second)
        """
        if not self.is_active:
            return 0.0
        
        return sum(m.energy_cost for m in self.protection_modules.values())
    
    def get_statistics(self) -> Dict:
        """Get security statistics."""
        uptime = time.time() - self.start_time
        
        # Calculate activation ratio
        total_active_time = sum(m.total_active_time for m in self.protection_modules.values())
        avg_active_time = total_active_time / len(self.protection_modules) if self.protection_modules else 0
        activation_ratio = avg_active_time / uptime if uptime > 0 else 0
        
        # Calculate average field strength
        avg_field_strength = 0.0
        if self.scan_history:
            avg_field_strength = sum(s.field_strength_mv_m for s in self.scan_history) / len(self.scan_history)
        
        return {
            "uptime_seconds": uptime,
            "is_active": self.is_active,
            "protection_modules": len(self.protection_modules),
            "total_scans": len(self.scan_history),
            "avg_field_strength_mv_m": avg_field_strength,
            "activation_threshold_mv_m": ROTESSCHILD_THRESHOLD_MV_M,
            "activation_ratio": activation_ratio,
            "total_energy_saved": self.total_energy_saved,
            "current_energy_consumption": self.get_current_energy_consumption()
        }
    
    def get_module_status(self) -> List[Dict]:
        """Get status of all protection modules."""
        return [
            {
                "module_id": module.module_id,
                "name": module.name,
                "is_active": module.is_active,
                "energy_cost": module.energy_cost,
                "activation_count": module.activation_count,
                "total_active_time": module.total_active_time
            }
            for module in self.protection_modules.values()
        ]
    
    def get_recent_scans(self, count: int = 10) -> List[Dict]:
        """
        Get recent scan results.
        
        Args:
            count: Number of recent scans to return
            
        Returns:
            List of scan dictionaries
        """
        recent = self.scan_history[-count:]
        
        return [
            {
                "timestamp": datetime.fromtimestamp(scan.timestamp).isoformat(),
                "field_strength_mv_m": scan.field_strength_mv_m,
                "threat_level": scan.threat_level,
                "exceeds_threshold": scan.exceeds_threshold()
            }
            for scan in recent
        ]


def main():
    """Demonstration of lazy security system."""
    print("=" * 70)
    print("LAZY SECURITY - Energy-Based Protection Demo")
    print("Based on Lex Amoris Principles")
    print("=" * 70)
    print()
    
    security = LazySecurityEngine(auto_scan=True)
    
    print("\n[DEMO] Simulating 20 scan cycles with varying field strength...")
    print()
    
    for i in range(20):
        scan = security.scan_and_update()
        
        status = "ACTIVE" if security.is_active else "DORMANT"
        threat = scan.threat_level.upper()
        
        print(f"Scan {i+1:2d}: {scan.field_strength_mv_m:6.2f} mV/m | "
              f"Threat: {threat:8s} | Status: {status}")
        
        time.sleep(0.5)  # Small delay for demo
    
    # Display statistics
    print("\n" + "-" * 70)
    print("Statistics:")
    stats = security.get_statistics()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.4f}")
        else:
            print(f"  {key}: {value}")
    
    # Display module status
    print("\n" + "-" * 70)
    print("Protection Modules:")
    modules = security.get_module_status()
    for module in modules:
        status = "✓ ACTIVE" if module["is_active"] else "○ DORMANT"
        print(f"  [{status}] {module['name']}")
        print(f"    Energy cost: {module['energy_cost']:.2f} units/s")
        print(f"    Activations: {module['activation_count']}")
        print(f"    Total active: {module['total_active_time']:.2f}s")
    
    # Display recent scans
    print("\n" + "-" * 70)
    print("Recent Scans (last 5):")
    recent = security.get_recent_scans(5)
    for scan in recent:
        print(f"  {scan['timestamp']}: {scan['field_strength_mv_m']:.2f} mV/m "
              f"({scan['threat_level']}) {'⚠' if scan['exceeds_threshold'] else '✓'}")
    
    print("\n" + "=" * 70)
    print(f"Energy saved: {security.total_energy_saved:.2f} units")
    print("=" * 70)


if __name__ == "__main__":
    main()
