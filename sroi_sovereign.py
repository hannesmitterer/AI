#!/usr/bin/env python3
"""
S-ROI Sovereign Protocol - Enhanced State Management System
===========================================================

This module implements the S-ROI (Social Return on Investment) Sovereign
protocol with advanced state management, resonance tracking, and stealth
mode capabilities.

Key Features:
- Three-state system: STABLE, WARNING, CRITICAL
- Comprehensive logging for state changes and resonance values
- Cooldown mechanism for stealth mode activation
- Modular architecture for easy testing and maintenance
- Integration with resonance-based systems

Based on: COVENANT_OF_RESONANCE and S-ROI principles
"""

import time
import logging
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum


# Constants
SROI_TARGET = 0.950  # Target S-ROI value
RESONANCE_WARNING_THRESHOLD = 0.850  # WARNING state threshold
RESONANCE_CRITICAL_THRESHOLD = 0.700  # CRITICAL state threshold
STEALTH_COOLDOWN_SECONDS = 60.0  # Cooldown period for stealth mode
DEFAULT_LOG_LEVEL = logging.INFO


class SROIState(Enum):
    """Enumeration of possible S-ROI system states."""
    STABLE = "STABLE"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class StealthMode(Enum):
    """Enumeration of stealth mode states."""
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    COOLDOWN = "COOLDOWN"


@dataclass
class StateChangeLog:
    """Record of a state change event."""
    timestamp: datetime
    previous_state: SROIState
    new_state: SROIState
    resonance_value: float
    reason: str


@dataclass
class ResonanceLog:
    """Record of a resonance value measurement."""
    timestamp: datetime
    value: float
    state: SROIState
    stealth_active: bool


class SROILogger:
    """
    Logging system for S-ROI Sovereign protocol.
    
    Tracks state changes, resonance values, and system events.
    """
    
    def __init__(self, log_level: int = DEFAULT_LOG_LEVEL):
        """
        Initialize the S-ROI logger.
        
        Args:
            log_level: Python logging level (default: INFO)
        """
        self.logger = logging.getLogger("SROI_Sovereign")
        self.logger.setLevel(log_level)
        
        # Create console handler if not already configured
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setLevel(log_level)
            formatter = logging.Formatter(
                '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        # History tracking
        self.state_change_history: List[StateChangeLog] = []
        self.resonance_history: List[ResonanceLog] = []
        self.max_history_size = 1000
    
    def log_state_change(self, previous_state: SROIState, new_state: SROIState,
                        resonance_value: float, reason: str) -> None:
        """
        Log a state change event.
        
        Args:
            previous_state: Previous system state
            new_state: New system state
            resonance_value: Current resonance value
            reason: Reason for state change
        """
        log_entry = StateChangeLog(
            timestamp=datetime.now(),
            previous_state=previous_state,
            new_state=new_state,
            resonance_value=resonance_value,
            reason=reason
        )
        
        self.state_change_history.append(log_entry)
        self._trim_history(self.state_change_history)
        
        self.logger.warning(
            f"STATE CHANGE: {previous_state.value} -> {new_state.value} | "
            f"Resonance: {resonance_value:.4f} | Reason: {reason}"
        )
    
    def log_resonance(self, value: float, state: SROIState, 
                     stealth_active: bool) -> None:
        """
        Log a resonance value measurement.
        
        Args:
            value: Resonance value
            state: Current system state
            stealth_active: Whether stealth mode is active
        """
        log_entry = ResonanceLog(
            timestamp=datetime.now(),
            value=value,
            state=state,
            stealth_active=stealth_active
        )
        
        self.resonance_history.append(log_entry)
        self._trim_history(self.resonance_history)
        
        self.logger.debug(
            f"RESONANCE: {value:.4f} | State: {state.value} | "
            f"Stealth: {'ACTIVE' if stealth_active else 'INACTIVE'}"
        )
    
    def log_stealth_activation(self, success: bool, reason: str) -> None:
        """
        Log stealth mode activation attempt.
        
        Args:
            success: Whether activation was successful
            reason: Reason for activation or failure
        """
        level = logging.INFO if success else logging.WARNING
        status = "ACTIVATED" if success else "DENIED"
        self.logger.log(level, f"STEALTH MODE {status}: {reason}")
    
    def log_info(self, message: str) -> None:
        """Log an informational message."""
        self.logger.info(message)
    
    def log_warning(self, message: str) -> None:
        """Log a warning message."""
        self.logger.warning(message)
    
    def log_error(self, message: str) -> None:
        """Log an error message."""
        self.logger.error(message)
    
    def _trim_history(self, history_list: List) -> None:
        """Trim history list to maximum size."""
        if len(history_list) > self.max_history_size:
            del history_list[0:len(history_list) - self.max_history_size]
    
    def get_state_change_history(self, limit: Optional[int] = None) -> List[StateChangeLog]:
        """
        Get state change history.
        
        Args:
            limit: Maximum number of entries to return (None for all)
            
        Returns:
            List of state change log entries
        """
        if limit:
            return self.state_change_history[-limit:]
        return self.state_change_history.copy()
    
    def get_resonance_history(self, limit: Optional[int] = None) -> List[ResonanceLog]:
        """
        Get resonance history.
        
        Args:
            limit: Maximum number of entries to return (None for all)
            
        Returns:
            List of resonance log entries
        """
        if limit:
            return self.resonance_history[-limit:]
        return self.resonance_history.copy()


class StealthModeController:
    """
    Controller for stealth mode with cooldown mechanism.
    
    Prevents rapid activation/deactivation cycles and ensures
    stable operation.
    """
    
    def __init__(self, cooldown_seconds: float = STEALTH_COOLDOWN_SECONDS):
        """
        Initialize stealth mode controller.
        
        Args:
            cooldown_seconds: Cooldown period in seconds
        """
        self.cooldown_seconds = cooldown_seconds
        self.mode = StealthMode.INACTIVE
        self.last_deactivation_time: Optional[datetime] = None
        self.activation_count = 0
        self.deactivation_count = 0
    
    def can_activate(self) -> bool:
        """
        Check if stealth mode can be activated.
        
        Returns:
            True if activation is allowed, False otherwise
        """
        if self.mode == StealthMode.ACTIVE:
            return False
        
        if self.last_deactivation_time is None:
            return True
        
        elapsed = (datetime.now() - self.last_deactivation_time).total_seconds()
        return elapsed >= self.cooldown_seconds
    
    def activate(self) -> bool:
        """
        Activate stealth mode.
        
        Returns:
            True if activation was successful, False otherwise
        """
        if not self.can_activate():
            return False
        
        self.mode = StealthMode.ACTIVE
        self.activation_count += 1
        return True
    
    def deactivate(self) -> None:
        """Deactivate stealth mode and start cooldown."""
        if self.mode == StealthMode.ACTIVE:
            self.mode = StealthMode.COOLDOWN
            self.last_deactivation_time = datetime.now()
            self.deactivation_count += 1
    
    def update(self) -> None:
        """Update stealth mode state (e.g., check cooldown expiration)."""
        if self.mode == StealthMode.COOLDOWN:
            if self.can_activate():
                self.mode = StealthMode.INACTIVE
    
    def get_cooldown_remaining(self) -> float:
        """
        Get remaining cooldown time in seconds.
        
        Returns:
            Remaining cooldown time, or 0 if not in cooldown
        """
        if self.last_deactivation_time is None:
            return 0.0
        
        elapsed = (datetime.now() - self.last_deactivation_time).total_seconds()
        remaining = self.cooldown_seconds - elapsed
        return max(0.0, remaining)
    
    def is_active(self) -> bool:
        """Check if stealth mode is currently active."""
        return self.mode == StealthMode.ACTIVE
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get stealth mode status.
        
        Returns:
            Dictionary with stealth mode status information
        """
        return {
            "mode": self.mode.value,
            "is_active": self.is_active(),
            "can_activate": self.can_activate(),
            "cooldown_remaining": self.get_cooldown_remaining(),
            "activation_count": self.activation_count,
            "deactivation_count": self.deactivation_count
        }


class SROISovereign:
    """
    S-ROI Sovereign Protocol - Main Controller
    
    Manages system state based on current resonance values,
    with support for stealth mode and comprehensive logging.
    """
    
    def __init__(self, 
                 initial_resonance: float = 0.5,
                 log_level: int = DEFAULT_LOG_LEVEL,
                 cooldown_seconds: float = STEALTH_COOLDOWN_SECONDS):
        """
        Initialize S-ROI Sovereign protocol.
        
        Args:
            initial_resonance: Initial resonance value (0.0 - 1.0)
            log_level: Logging level
            cooldown_seconds: Stealth mode cooldown period
        """
        self.current_resonance = initial_resonance
        self.state = self._determine_state(initial_resonance)
        
        # Initialize subsystems
        self.logger = SROILogger(log_level=log_level)
        self.stealth_controller = StealthModeController(cooldown_seconds=cooldown_seconds)
        
        # System metrics
        self.start_time = datetime.now()
        self.update_count = 0
        
        self.logger.log_info(
            f"S-ROI Sovereign initialized | "
            f"Initial resonance: {initial_resonance:.4f} | "
            f"State: {self.state.value}"
        )
    
    def _determine_state(self, resonance: float) -> SROIState:
        """
        Determine system state based on resonance value.
        
        Args:
            resonance: Current resonance value
            
        Returns:
            Appropriate system state
        """
        if resonance >= RESONANCE_WARNING_THRESHOLD:
            return SROIState.STABLE
        elif resonance >= RESONANCE_CRITICAL_THRESHOLD:
            return SROIState.WARNING
        else:
            return SROIState.CRITICAL
    
    def update_resonance(self, new_resonance: float, reason: str = "Manual update") -> None:
        """
        Update current resonance value and adjust state accordingly.
        
        Args:
            new_resonance: New resonance value (0.0 - 1.0)
            reason: Reason for the update
        """
        # Clamp resonance to valid range
        new_resonance = max(0.0, min(1.0, new_resonance))
        
        previous_resonance = self.current_resonance
        self.current_resonance = new_resonance
        
        # Determine new state
        new_state = self._determine_state(new_resonance)
        
        # Log resonance change
        self.logger.log_resonance(
            new_resonance,
            new_state,
            self.stealth_controller.is_active()
        )
        
        # Check for state change
        if new_state != self.state:
            self.logger.log_state_change(
                self.state,
                new_state,
                new_resonance,
                reason
            )
            self.state = new_state
        
        self.update_count += 1
    
    def request_stealth_activation(self, reason: str = "Manual request") -> bool:
        """
        Request activation of stealth mode.
        
        Args:
            reason: Reason for activation request
            
        Returns:
            True if activation was successful, False otherwise
        """
        self.stealth_controller.update()
        
        if self.stealth_controller.can_activate():
            success = self.stealth_controller.activate()
            if success:
                self.logger.log_stealth_activation(True, reason)
                return True
        
        # Activation denied
        cooldown_remaining = self.stealth_controller.get_cooldown_remaining()
        denial_reason = f"{reason} | Cooldown: {cooldown_remaining:.1f}s remaining"
        self.logger.log_stealth_activation(False, denial_reason)
        return False
    
    def deactivate_stealth(self, reason: str = "Manual deactivation") -> None:
        """
        Deactivate stealth mode.
        
        Args:
            reason: Reason for deactivation
        """
        if self.stealth_controller.is_active():
            self.stealth_controller.deactivate()
            self.logger.log_info(f"Stealth mode deactivated: {reason}")
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get comprehensive system status.
        
        Returns:
            Dictionary with system status information
        """
        uptime = (datetime.now() - self.start_time).total_seconds()
        
        return {
            "current_resonance": self.current_resonance,
            "state": self.state.value,
            "stealth": self.stealth_controller.get_status(),
            "uptime_seconds": uptime,
            "update_count": self.update_count,
            "target_sroi": SROI_TARGET,
            "warning_threshold": RESONANCE_WARNING_THRESHOLD,
            "critical_threshold": RESONANCE_CRITICAL_THRESHOLD
        }
    
    def get_state_history(self, limit: Optional[int] = 10) -> List[Dict[str, Any]]:
        """
        Get recent state change history.
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of state change entries as dictionaries
        """
        history = self.logger.get_state_change_history(limit)
        return [
            {
                "timestamp": entry.timestamp.isoformat(),
                "previous_state": entry.previous_state.value,
                "new_state": entry.new_state.value,
                "resonance_value": entry.resonance_value,
                "reason": entry.reason
            }
            for entry in history
        ]
    
    def get_resonance_history(self, limit: Optional[int] = 10) -> List[Dict[str, Any]]:
        """
        Get recent resonance history.
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of resonance entries as dictionaries
        """
        history = self.logger.get_resonance_history(limit)
        return [
            {
                "timestamp": entry.timestamp.isoformat(),
                "value": entry.value,
                "state": entry.state.value,
                "stealth_active": entry.stealth_active
            }
            for entry in history
        ]


def main():
    """Demonstration of S-ROI Sovereign protocol."""
    print("=" * 70)
    print("S-ROI SOVEREIGN PROTOCOL")
    print("Enhanced State Management System")
    print("=" * 70)
    print()
    
    # Initialize protocol
    sovereign = SROISovereign(initial_resonance=0.9, log_level=logging.DEBUG)
    
    print("\nInitial status:")
    print(sovereign.get_status())
    
    # Simulate resonance changes
    print("\n--- Simulating resonance changes ---")
    
    sovereign.update_resonance(0.95, "System optimization")
    time.sleep(0.5)
    
    sovereign.update_resonance(0.82, "Minor fluctuation")
    time.sleep(0.5)
    
    sovereign.update_resonance(0.65, "Critical degradation detected")
    time.sleep(0.5)
    
    # Test stealth mode
    print("\n--- Testing stealth mode ---")
    
    sovereign.request_stealth_activation("Entering protected mode")
    sovereign.request_stealth_activation("Attempt during active stealth")
    
    time.sleep(1)
    sovereign.deactivate_stealth("Returning to normal operations")
    
    # Try to reactivate immediately (should fail due to cooldown)
    sovereign.request_stealth_activation("Immediate reactivation attempt")
    
    print("\n--- Final Status ---")
    status = sovereign.get_status()
    for key, value in status.items():
        print(f"{key}: {value}")
    
    print("\n--- Recent State Changes ---")
    for change in sovereign.get_state_history(limit=5):
        print(f"{change['timestamp']}: {change['previous_state']} -> {change['new_state']} "
              f"(resonance: {change['resonance_value']:.4f})")


if __name__ == "__main__":
    main()
