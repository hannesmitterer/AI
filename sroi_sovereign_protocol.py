#!/usr/bin/env python3
"""
S-ROI Sovereign Protocol - Connected Logical Steps Implementation
================================================================

This module implements the S-ROI (Social Return on Investment) Sovereign protocol
with comprehensive logging, state validation, automatic notifications, and modular
state management.

Key Features:
- Complete logical flow logging with state tracking
- State transition validation system
- Automatic notifications for critical states and threshold violations
- Modular state functions for reusability and clarity

Based on: Kosymbiosis principles and COVENANT_OF_RESONANCE
"""

import time
import json
import logging
from typing import Dict, List, Optional, Callable, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path


# S-ROI Constants
SROI_TARGET = 0.950  # Target S-ROI value (from README.md)
SROI_CRITICAL_LOW = 0.300  # Critical low threshold
SROI_WARNING_LOW = 0.500  # Warning low threshold
SROI_OPTIMAL_MIN = 0.850  # Optimal minimum threshold
SROI_CRITICAL_HIGH = 0.990  # Critical high threshold (near saturation)

# Operational Constants
CALIBRATION_BASELINE = 0.5  # Baseline S-ROI value for calibration
MAX_OPTIMIZATION_ATTEMPTS = 10  # Maximum optimization attempts before escalation
RECOVERY_BOOST_AMOUNT = 0.05  # S-ROI boost amount during recovery
CYCLE_SLEEP_DURATION = 0.5  # Sleep duration between cycles (seconds)
LOG_WRITE_FREQUENCY = 5  # Write JSON log every N operations (for performance)


class SROIState(Enum):
    """Enumeration of possible S-ROI system states."""
    INITIALIZING = "initializing"
    CALIBRATING = "calibrating"
    MONITORING = "monitoring"
    OPTIMIZING = "optimizing"
    STABLE = "stable"
    WARNING = "warning"
    CRITICAL = "critical"
    RECOVERY = "recovery"
    SHUTDOWN = "shutdown"


class NotificationLevel(Enum):
    """Notification severity levels."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


@dataclass
class StateTransition:
    """Represents a state transition event."""
    timestamp: str
    from_state: SROIState
    to_state: SROIState
    sroi_value: float
    reason: str
    valid: bool
    metadata: Dict = field(default_factory=dict)


@dataclass
class Notification:
    """Represents a system notification."""
    timestamp: str
    level: NotificationLevel
    state: SROIState
    message: str
    sroi_value: float
    threshold_violated: Optional[str] = None
    metadata: Dict = field(default_factory=dict)


class StateLogger:
    """
    Comprehensive logging system for S-ROI state tracking.
    Records entire logical flow and every state reached.
    """
    
    def __init__(self, log_file: str = "sroi_protocol.log", json_log_file: str = "sroi_state_log.json"):
        """
        Initialize the state logger.
        
        Args:
            log_file: Path to text log file
            json_log_file: Path to JSON structured log file
        """
        self.log_file = log_file
        self.json_log_file = json_log_file
        self.state_history: List[StateTransition] = []
        self.notification_history: List[Notification] = []
        self.operation_count = 0  # Track operations for batched writes
        
        # Configure text logger
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('SROI_Protocol')
        
        self.logger.info("=" * 70)
        self.logger.info("S-ROI Sovereign Protocol Logger Initialized")
        self.logger.info("=" * 70)
    
    def log_state_transition(self, transition: StateTransition) -> None:
        """
        Log a state transition with full context.
        
        Args:
            transition: StateTransition object to log
        """
        self.state_history.append(transition)
        self.operation_count += 1
        
        # Text log
        status = "VALID" if transition.valid else "INVALID"
        self.logger.info(
            f"[STATE_TRANSITION] [{status}] {transition.from_state.value} -> "
            f"{transition.to_state.value} | S-ROI: {transition.sroi_value:.4f} | "
            f"Reason: {transition.reason}"
        )
        
        # Save to JSON log periodically for performance
        if self.operation_count % LOG_WRITE_FREQUENCY == 0:
            self._save_json_log()
    
    def log_notification(self, notification: Notification) -> None:
        """
        Log a system notification.
        
        Args:
            notification: Notification object to log
        """
        self.notification_history.append(notification)
        self.operation_count += 1
        
        # Text log with appropriate level
        log_method = {
            NotificationLevel.INFO: self.logger.info,
            NotificationLevel.WARNING: self.logger.warning,
            NotificationLevel.CRITICAL: self.logger.critical,
            NotificationLevel.EMERGENCY: self.logger.critical
        }.get(notification.level, self.logger.info)
        
        threshold_info = f" | Threshold: {notification.threshold_violated}" if notification.threshold_violated else ""
        log_method(
            f"[NOTIFICATION] [{notification.level.value.upper()}] "
            f"State: {notification.state.value} | S-ROI: {notification.sroi_value:.4f} | "
            f"{notification.message}{threshold_info}"
        )
        
        # Save to JSON log periodically for performance
        if self.operation_count % LOG_WRITE_FREQUENCY == 0:
            self._save_json_log()
    
    def log_flow_event(self, event_type: str, description: str, metadata: Dict = None) -> None:
        """
        Log a logical flow event.
        
        Args:
            event_type: Type of event
            description: Event description
            metadata: Additional metadata
        """
        self.logger.info(f"[FLOW_EVENT] {event_type}: {description}")
        if metadata:
            self.logger.debug(f"[FLOW_METADATA] {json.dumps(metadata, indent=2)}")
    
    def _save_json_log(self) -> None:
        """Save structured log to JSON file."""
        log_data = {
            "last_updated": datetime.now().isoformat(),
            "state_transitions": [
                {
                    "timestamp": t.timestamp,
                    "from_state": t.from_state.value,
                    "to_state": t.to_state.value,
                    "sroi_value": t.sroi_value,
                    "reason": t.reason,
                    "valid": t.valid,
                    "metadata": t.metadata
                }
                for t in self.state_history
            ],
            "notifications": [
                {
                    "timestamp": n.timestamp,
                    "level": n.level.value,
                    "state": n.state.value,
                    "message": n.message,
                    "sroi_value": n.sroi_value,
                    "threshold_violated": n.threshold_violated,
                    "metadata": n.metadata
                }
                for n in self.notification_history
            ]
        }
        
        with open(self.json_log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
    
    def get_state_summary(self) -> Dict:
        """Get summary of state history."""
        return {
            "total_transitions": len(self.state_history),
            "valid_transitions": sum(1 for t in self.state_history if t.valid),
            "invalid_transitions": sum(1 for t in self.state_history if not t.valid),
            "total_notifications": len(self.notification_history),
            "critical_notifications": sum(
                1 for n in self.notification_history 
                if n.level in [NotificationLevel.CRITICAL, NotificationLevel.EMERGENCY]
            )
        }


class StateValidator:
    """
    State transition validation system.
    Verifies the correctness of every state transition.
    """
    
    def __init__(self):
        """Initialize the state validator with transition rules."""
        # Define valid state transitions
        self.valid_transitions = {
            SROIState.INITIALIZING: [SROIState.CALIBRATING, SROIState.CRITICAL],
            SROIState.CALIBRATING: [SROIState.MONITORING, SROIState.WARNING, SROIState.CRITICAL],
            SROIState.MONITORING: [SROIState.STABLE, SROIState.OPTIMIZING, SROIState.WARNING, SROIState.CRITICAL],
            SROIState.OPTIMIZING: [SROIState.STABLE, SROIState.MONITORING, SROIState.WARNING],
            SROIState.STABLE: [SROIState.MONITORING, SROIState.OPTIMIZING, SROIState.WARNING, SROIState.SHUTDOWN],
            SROIState.WARNING: [SROIState.MONITORING, SROIState.CRITICAL, SROIState.RECOVERY],
            SROIState.CRITICAL: [SROIState.RECOVERY, SROIState.SHUTDOWN],
            SROIState.RECOVERY: [SROIState.MONITORING, SROIState.WARNING, SROIState.CRITICAL],
            SROIState.SHUTDOWN: []  # Terminal state
        }
    
    def validate_transition(self, from_state: SROIState, to_state: SROIState, 
                          sroi_value: float) -> Tuple[bool, str]:
        """
        Validate a state transition.
        
        Args:
            from_state: Current state
            to_state: Target state
            sroi_value: Current S-ROI value
            
        Returns:
            Tuple of (is_valid, reason)
        """
        # Check if transition is allowed
        if to_state not in self.valid_transitions.get(from_state, []):
            return False, f"Invalid transition: {from_state.value} -> {to_state.value} not allowed"
        
        # Validate S-ROI value consistency with state
        if to_state == SROIState.CRITICAL and sroi_value >= SROI_WARNING_LOW:
            return False, f"S-ROI value {sroi_value} too high for CRITICAL state"
        
        if to_state == SROIState.STABLE and sroi_value < SROI_OPTIMAL_MIN:
            return False, f"S-ROI value {sroi_value} too low for STABLE state"
        
        return True, "Transition validated successfully"
    
    def suggest_state(self, sroi_value: float, current_state: SROIState) -> SROIState:
        """
        Suggest appropriate state based on S-ROI value.
        
        Args:
            sroi_value: Current S-ROI value
            current_state: Current state
            
        Returns:
            Suggested state
        """
        if sroi_value < SROI_CRITICAL_LOW:
            return SROIState.CRITICAL
        elif sroi_value < SROI_WARNING_LOW:
            return SROIState.WARNING
        elif sroi_value >= SROI_OPTIMAL_MIN:
            return SROIState.STABLE
        elif current_state in [SROIState.INITIALIZING, SROIState.CALIBRATING]:
            return SROIState.MONITORING
        else:
            return SROIState.OPTIMIZING


class NotificationSystem:
    """
    Automatic notification system for critical states and threshold violations.
    """
    
    def __init__(self, logger: StateLogger):
        """
        Initialize notification system.
        
        Args:
            logger: StateLogger instance for logging notifications
        """
        self.logger = logger
        self.notification_handlers: List[Callable] = []
        self.notification_count = 0
    
    def register_handler(self, handler: Callable[[Notification], None]) -> None:
        """
        Register a notification handler.
        
        Args:
            handler: Callable that receives Notification objects
        """
        self.notification_handlers.append(handler)
    
    def check_and_notify(self, state: SROIState, sroi_value: float, 
                        previous_value: Optional[float] = None) -> None:
        """
        Check thresholds and send notifications if needed.
        
        Args:
            state: Current state
            sroi_value: Current S-ROI value
            previous_value: Previous S-ROI value for change detection
        """
        notifications = []
        
        # Critical low threshold
        if sroi_value < SROI_CRITICAL_LOW:
            notifications.append(Notification(
                timestamp=datetime.now().isoformat(),
                level=NotificationLevel.EMERGENCY,
                state=state,
                message=f"EMERGENCY: S-ROI critically low at {sroi_value:.4f}",
                sroi_value=sroi_value,
                threshold_violated=f"CRITICAL_LOW ({SROI_CRITICAL_LOW})"
            ))
        
        # Warning low threshold
        elif sroi_value < SROI_WARNING_LOW:
            notifications.append(Notification(
                timestamp=datetime.now().isoformat(),
                level=NotificationLevel.WARNING,
                state=state,
                message=f"WARNING: S-ROI below warning threshold at {sroi_value:.4f}",
                sroi_value=sroi_value,
                threshold_violated=f"WARNING_LOW ({SROI_WARNING_LOW})"
            ))
        
        # Critical high threshold (near saturation)
        elif sroi_value > SROI_CRITICAL_HIGH:
            notifications.append(Notification(
                timestamp=datetime.now().isoformat(),
                level=NotificationLevel.WARNING,
                state=state,
                message=f"WARNING: S-ROI approaching saturation at {sroi_value:.4f}",
                sroi_value=sroi_value,
                threshold_violated=f"CRITICAL_HIGH ({SROI_CRITICAL_HIGH})"
            ))
        
        # Target achievement
        elif sroi_value >= SROI_TARGET and (previous_value is None or previous_value < SROI_TARGET):
            notifications.append(Notification(
                timestamp=datetime.now().isoformat(),
                level=NotificationLevel.INFO,
                state=state,
                message=f"SUCCESS: S-ROI target achieved at {sroi_value:.4f}",
                sroi_value=sroi_value,
                threshold_violated=None
            ))
        
        # Critical state notification
        if state == SROIState.CRITICAL:
            notifications.append(Notification(
                timestamp=datetime.now().isoformat(),
                level=NotificationLevel.CRITICAL,
                state=state,
                message="System in CRITICAL state - immediate attention required",
                sroi_value=sroi_value
            ))
        
        # Send all notifications
        for notification in notifications:
            self._send_notification(notification)
    
    def _send_notification(self, notification: Notification) -> None:
        """
        Send notification to all registered handlers.
        
        Args:
            notification: Notification to send
        """
        self.notification_count += 1
        
        # Log the notification
        self.logger.log_notification(notification)
        
        # Call all registered handlers
        for handler in self.notification_handlers:
            try:
                handler(notification)
            except Exception as e:
                self.logger.logger.error(f"Notification handler error: {e}")


class SROISovereignProtocol:
    """
    Main S-ROI Sovereign Protocol implementation.
    
    Implements connected logical steps with:
    - Comprehensive logging
    - State validation
    - Automatic notifications
    - Modular state functions
    """
    
    def __init__(self, initial_sroi: float = 0.5192):
        """
        Initialize the S-ROI Sovereign Protocol.
        
        Args:
            initial_sroi: Initial S-ROI value
        """
        self.current_state = SROIState.INITIALIZING
        self.sroi_value = initial_sroi
        self.previous_sroi = initial_sroi
        
        # Initialize subsystems
        self.state_logger = StateLogger()
        self.state_validator = StateValidator()
        self.notification_system = NotificationSystem(self.state_logger)
        
        # Operational metrics
        self.start_time = time.time()
        self.cycle_count = 0
        self.optimization_attempts = 0
        
        self.state_logger.log_flow_event(
            "INITIALIZATION",
            f"S-ROI Sovereign Protocol initialized with S-ROI={initial_sroi:.4f}",
            {"initial_state": self.current_state.value, "target": SROI_TARGET}
        )
    
    # === Modular State Functions ===
    
    def state_initialize(self) -> None:
        """
        INITIALIZING state: System startup and basic checks.
        """
        self.state_logger.log_flow_event(
            "STATE_FUNCTION",
            "Executing INITIALIZING state function"
        )
        
        # Perform initialization checks
        if self.sroi_value > 0:
            self._transition_to_state(SROIState.CALIBRATING, "Initialization complete, starting calibration")
        else:
            self._transition_to_state(SROIState.CRITICAL, "Invalid initial S-ROI value")
    
    def state_calibrate(self) -> None:
        """
        CALIBRATING state: System calibration and baseline establishment.
        """
        self.state_logger.log_flow_event(
            "STATE_FUNCTION",
            "Executing CALIBRATING state function"
        )
        
        # Calibration logic
        if abs(self.sroi_value - CALIBRATION_BASELINE) < 0.1:
            self._transition_to_state(SROIState.MONITORING, "Calibration successful")
        elif self.sroi_value < SROI_CRITICAL_LOW:
            self._transition_to_state(SROIState.CRITICAL, "Calibration failed - critical S-ROI")
        else:
            self._transition_to_state(SROIState.WARNING, "Calibration requires adjustment")
    
    def state_monitor(self) -> None:
        """
        MONITORING state: Continuous monitoring of S-ROI metrics.
        """
        self.state_logger.log_flow_event(
            "STATE_FUNCTION",
            f"Executing MONITORING state function - S-ROI: {self.sroi_value:.4f}"
        )
        
        # Determine next state based on S-ROI value
        if self.sroi_value >= SROI_OPTIMAL_MIN:
            self._transition_to_state(SROIState.STABLE, "Optimal S-ROI achieved")
        elif self.sroi_value < SROI_WARNING_LOW:
            self._transition_to_state(SROIState.WARNING, "S-ROI below warning threshold")
        elif self.sroi_value < SROI_TARGET:
            self._transition_to_state(SROIState.OPTIMIZING, "S-ROI optimization needed")
    
    def state_optimize(self) -> None:
        """
        OPTIMIZING state: Active optimization of S-ROI value.
        """
        self.state_logger.log_flow_event(
            "STATE_FUNCTION",
            f"Executing OPTIMIZING state function - Attempt {self.optimization_attempts}"
        )
        
        self.optimization_attempts += 1
        
        # Optimization algorithm (simple increment towards target)
        optimization_step = (SROI_TARGET - self.sroi_value) * 0.1
        self.sroi_value = min(SROI_TARGET, self.sroi_value + optimization_step)
        
        self.state_logger.log_flow_event(
            "OPTIMIZATION",
            f"S-ROI optimized to {self.sroi_value:.4f}",
            {"optimization_step": optimization_step}
        )
        
        # Transition based on result
        if self.sroi_value >= SROI_OPTIMAL_MIN:
            self._transition_to_state(SROIState.STABLE, "Optimization successful")
        elif self.optimization_attempts > MAX_OPTIMIZATION_ATTEMPTS:
            self._transition_to_state(SROIState.WARNING, "Optimization taking too long")
        else:
            self._transition_to_state(SROIState.MONITORING, "Continuing optimization monitoring")
    
    def state_stable(self) -> None:
        """
        STABLE state: System operating at optimal levels.
        """
        self.state_logger.log_flow_event(
            "STATE_FUNCTION",
            f"Executing STABLE state function - S-ROI: {self.sroi_value:.4f}"
        )
        
        # Monitor for degradation
        if self.sroi_value < SROI_OPTIMAL_MIN:
            self._transition_to_state(SROIState.MONITORING, "S-ROI degraded from stable level")
    
    def state_warning(self) -> None:
        """
        WARNING state: System requires attention.
        """
        self.state_logger.log_flow_event(
            "STATE_FUNCTION",
            f"Executing WARNING state function - S-ROI: {self.sroi_value:.4f}"
        )
        
        # Check if situation improved or worsened
        if self.sroi_value >= SROI_WARNING_LOW:
            self._transition_to_state(SROIState.RECOVERY, "Recovery from warning state")
        elif self.sroi_value < SROI_CRITICAL_LOW:
            self._transition_to_state(SROIState.CRITICAL, "Escalated to critical")
    
    def state_critical(self) -> None:
        """
        CRITICAL state: System in critical condition.
        """
        self.state_logger.log_flow_event(
            "STATE_FUNCTION",
            f"Executing CRITICAL state function - S-ROI: {self.sroi_value:.4f}",
            {"severity": "CRITICAL"}
        )
        
        # Attempt emergency recovery
        if self.sroi_value < SROI_CRITICAL_LOW:
            self._transition_to_state(SROIState.RECOVERY, "Initiating emergency recovery")
        else:
            self._transition_to_state(SROIState.RECOVERY, "Conditions allow recovery attempt")
    
    def state_recovery(self) -> None:
        """
        RECOVERY state: System recovery procedures.
        """
        self.state_logger.log_flow_event(
            "STATE_FUNCTION",
            f"Executing RECOVERY state function - S-ROI: {self.sroi_value:.4f}"
        )
        
        # Recovery algorithm
        self.sroi_value = min(1.0, self.sroi_value + RECOVERY_BOOST_AMOUNT)
        
        self.state_logger.log_flow_event(
            "RECOVERY",
            f"Recovery boost applied, S-ROI now {self.sroi_value:.4f}",
            {"recovery_boost": RECOVERY_BOOST_AMOUNT}
        )
        
        # Transition based on recovery progress
        if self.sroi_value >= SROI_WARNING_LOW:
            self._transition_to_state(SROIState.MONITORING, "Recovery successful")
        elif self.sroi_value < SROI_CRITICAL_LOW:
            self._transition_to_state(SROIState.CRITICAL, "Recovery insufficient")
        else:
            self._transition_to_state(SROIState.WARNING, "Partial recovery achieved")
    
    def state_shutdown(self) -> None:
        """
        SHUTDOWN state: Graceful system shutdown.
        """
        self.state_logger.log_flow_event(
            "STATE_FUNCTION",
            "Executing SHUTDOWN state function"
        )
        
        self.state_logger.logger.info("System entering shutdown state")
    
    # === Core Protocol Methods ===
    
    def _transition_to_state(self, new_state: SROIState, reason: str) -> None:
        """
        Transition to a new state with validation and logging.
        
        Args:
            new_state: Target state
            reason: Reason for transition
        """
        # Validate transition
        is_valid, validation_message = self.state_validator.validate_transition(
            self.current_state, new_state, self.sroi_value
        )
        
        # Create transition record
        transition = StateTransition(
            timestamp=datetime.now().isoformat(),
            from_state=self.current_state,
            to_state=new_state,
            sroi_value=self.sroi_value,
            reason=reason,
            valid=is_valid,
            metadata={"validation_message": validation_message}
        )
        
        # Log transition
        self.state_logger.log_state_transition(transition)
        
        # If valid, perform transition
        if is_valid:
            self.current_state = new_state
            
            # Check for notifications
            self.notification_system.check_and_notify(
                new_state, self.sroi_value, self.previous_sroi
            )
        else:
            self.state_logger.logger.warning(f"Invalid transition blocked: {validation_message}")
    
    def execute_cycle(self) -> Dict:
        """
        Execute a single protocol cycle.
        
        Returns:
            Dictionary containing cycle metrics
        """
        self.cycle_count += 1
        cycle_start = time.time()
        
        self.state_logger.log_flow_event(
            "CYCLE_START",
            f"Starting cycle {self.cycle_count}",
            {"state": self.current_state.value, "sroi": self.sroi_value}
        )
        
        # Execute current state function
        state_functions = {
            SROIState.INITIALIZING: self.state_initialize,
            SROIState.CALIBRATING: self.state_calibrate,
            SROIState.MONITORING: self.state_monitor,
            SROIState.OPTIMIZING: self.state_optimize,
            SROIState.STABLE: self.state_stable,
            SROIState.WARNING: self.state_warning,
            SROIState.CRITICAL: self.state_critical,
            SROIState.RECOVERY: self.state_recovery,
            SROIState.SHUTDOWN: self.state_shutdown
        }
        
        state_function = state_functions.get(self.current_state)
        if state_function:
            state_function()
        
        # Update previous S-ROI
        self.previous_sroi = self.sroi_value
        
        # Calculate metrics
        cycle_duration = time.time() - cycle_start
        uptime = time.time() - self.start_time
        
        metrics = {
            "cycle": self.cycle_count,
            "timestamp": datetime.now().isoformat(),
            "state": self.current_state.value,
            "sroi_value": self.sroi_value,
            "sroi_target": SROI_TARGET,
            "sroi_delta": SROI_TARGET - self.sroi_value,
            "uptime_seconds": uptime,
            "cycle_duration": cycle_duration,
            "optimization_attempts": self.optimization_attempts
        }
        
        self.state_logger.log_flow_event(
            "CYCLE_END",
            f"Completed cycle {self.cycle_count}",
            metrics
        )
        
        return metrics
    
    def run(self, max_cycles: Optional[int] = None) -> None:
        """
        Run the protocol for specified cycles or indefinitely.
        
        Args:
            max_cycles: Maximum number of cycles (None for infinite)
        """
        self.state_logger.logger.info(f"Starting S-ROI Sovereign Protocol")
        self.state_logger.logger.info(f"Target S-ROI: {SROI_TARGET}")
        
        try:
            while max_cycles is None or self.cycle_count < max_cycles:
                metrics = self.execute_cycle()
                
                # Display status periodically
                if self.cycle_count % 5 == 0:
                    print(f"[Cycle {metrics['cycle']:04d}] "
                          f"State: {metrics['state']:12s} | "
                          f"S-ROI: {metrics['sroi_value']:.4f} | "
                          f"Target: {SROI_TARGET:.4f}")
                
                # Exit if shutdown state
                if self.current_state == SROIState.SHUTDOWN:
                    break
                
                # Small delay between cycles
                time.sleep(CYCLE_SLEEP_DURATION)
        
        except KeyboardInterrupt:
            self.state_logger.logger.info("Protocol interrupted by user")
        
        finally:
            self._finalize()
    
    def _finalize(self) -> None:
        """Finalize protocol execution and save state."""
        # Ensure final JSON log is written
        self.state_logger._save_json_log()
        
        summary = self.state_logger.get_state_summary()
        
        self.state_logger.logger.info("=" * 70)
        self.state_logger.logger.info("S-ROI Sovereign Protocol Session Summary")
        self.state_logger.logger.info("=" * 70)
        self.state_logger.logger.info(f"Total cycles: {self.cycle_count}")
        self.state_logger.logger.info(f"Final state: {self.current_state.value}")
        self.state_logger.logger.info(f"Final S-ROI: {self.sroi_value:.4f}")
        self.state_logger.logger.info(f"Target S-ROI: {SROI_TARGET:.4f}")
        self.state_logger.logger.info(f"Total transitions: {summary['total_transitions']}")
        self.state_logger.logger.info(f"Valid transitions: {summary['valid_transitions']}")
        self.state_logger.logger.info(f"Invalid transitions: {summary['invalid_transitions']}")
        self.state_logger.logger.info(f"Total notifications: {summary['total_notifications']}")
        self.state_logger.logger.info(f"Critical notifications: {summary['critical_notifications']}")
        self.state_logger.logger.info("=" * 70)
    
    def get_status(self) -> Dict:
        """Get current protocol status."""
        return {
            "current_state": self.current_state.value,
            "sroi_value": self.sroi_value,
            "sroi_target": SROI_TARGET,
            "sroi_delta": SROI_TARGET - self.sroi_value,
            "cycle_count": self.cycle_count,
            "uptime_seconds": time.time() - self.start_time,
            "optimization_attempts": self.optimization_attempts,
            "state_summary": self.state_logger.get_state_summary()
        }


def main():
    """Main entry point for S-ROI Sovereign Protocol."""
    print("=" * 70)
    print(" " * 15 + "S-ROI SOVEREIGN PROTOCOL")
    print(" " * 10 + "Connected Logical Steps Implementation")
    print("=" * 70)
    print()
    
    # Initialize protocol
    protocol = SROISovereignProtocol(initial_sroi=0.5192)
    
    # Register example notification handler
    def console_notification_handler(notification: Notification):
        """Example notification handler that prints to console."""
        if notification.level in [NotificationLevel.CRITICAL, NotificationLevel.EMERGENCY]:
            print(f"\n!!! {notification.level.value.upper()}: {notification.message} !!!\n")
    
    protocol.notification_system.register_handler(console_notification_handler)
    
    # Run protocol
    protocol.run(max_cycles=50)


if __name__ == "__main__":
    main()
