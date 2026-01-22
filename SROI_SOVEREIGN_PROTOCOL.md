# S-ROI Sovereign Protocol - Documentation

## Overview

The **S-ROI Sovereign Protocol** implements connected logical steps for the S-ROI (Social Return on Investment) Sovereign system with comprehensive features for enterprise-grade operation.

### Key Features

1. **Comprehensive Logging System**
   - Records entire logical flow
   - Tracks every state transition
   - Generates both text and JSON structured logs
   - Includes timestamps and contextual metadata

2. **State Validation System**
   - Validates all state transitions
   - Enforces transition rules
   - Prevents invalid state changes
   - Suggests appropriate states based on S-ROI values

3. **Automatic Notification System**
   - Monitors critical states
   - Detects threshold violations
   - Sends notifications at appropriate severity levels
   - Supports custom notification handlers

4. **Modular State Functions**
   - Each state implemented as individual function
   - Clear separation of concerns
   - Easy to extend and maintain
   - Reusable across different contexts

## Architecture

### State Machine

The protocol implements a robust state machine with the following states:

```
INITIALIZING → CALIBRATING → MONITORING → OPTIMIZING → STABLE
                    ↓             ↓            ↓
                WARNING ← ─── ─── ┘            |
                    ↓                          |
                CRITICAL                       |
                    ↓                          |
                RECOVERY → ─── ─── ─── ─── ─── ┘
                    ↓
                SHUTDOWN
```

### State Descriptions

- **INITIALIZING**: System startup and basic checks
- **CALIBRATING**: System calibration and baseline establishment
- **MONITORING**: Continuous monitoring of S-ROI metrics
- **OPTIMIZING**: Active optimization of S-ROI value
- **STABLE**: System operating at optimal levels
- **WARNING**: System requires attention
- **CRITICAL**: System in critical condition
- **RECOVERY**: System recovery procedures
- **SHUTDOWN**: Graceful system shutdown

### S-ROI Thresholds

| Threshold | Value | Description |
|-----------|-------|-------------|
| CRITICAL_LOW | 0.300 | Emergency threshold - requires immediate action |
| WARNING_LOW | 0.500 | Warning threshold - attention needed |
| OPTIMAL_MIN | 0.850 | Minimum optimal operating level |
| TARGET | 0.950 | Target S-ROI value |
| CRITICAL_HIGH | 0.990 | Near-saturation warning |

## Components

### 1. StateLogger

Comprehensive logging system that tracks:
- State transitions with validation status
- Logical flow events
- Notifications
- System metrics

**Log Files Generated:**
- `sroi_protocol.log` - Human-readable text log
- `sroi_state_log.json` - Structured JSON log for programmatic access

**Example Usage:**
```python
from sroi_sovereign_protocol import StateLogger

logger = StateLogger()
logger.log_flow_event("INITIALIZATION", "System starting up")
```

### 2. StateValidator

Validates state transitions to ensure system integrity:
- Checks transition validity against allowed transitions
- Verifies S-ROI value consistency with target state
- Suggests appropriate states based on current metrics

**Example Usage:**
```python
from sroi_sovereign_protocol import StateValidator, SROIState

validator = StateValidator()
is_valid, reason = validator.validate_transition(
    SROIState.MONITORING,
    SROIState.STABLE,
    0.900
)
```

### 3. NotificationSystem

Automatic notification system for critical events:
- Monitors S-ROI thresholds
- Detects critical states
- Sends notifications with appropriate severity
- Supports custom notification handlers

**Notification Levels:**
- **INFO**: Informational notifications
- **WARNING**: Warnings requiring attention
- **CRITICAL**: Critical situations
- **EMERGENCY**: Emergency situations requiring immediate action

**Example Usage:**
```python
from sroi_sovereign_protocol import NotificationSystem

def my_handler(notification):
    print(f"Alert: {notification.message}")

notif_system = NotificationSystem(logger)
notif_system.register_handler(my_handler)
```

### 4. SROISovereignProtocol

Main protocol implementation that orchestrates all components:
- Manages state machine
- Executes state-specific logic
- Coordinates logging, validation, and notifications
- Provides comprehensive status reporting

**Example Usage:**
```python
from sroi_sovereign_protocol import SROISovereignProtocol

protocol = SROISovereignProtocol(initial_sroi=0.5192)
protocol.run(max_cycles=50)
```

## State Functions

Each state is implemented as a modular function:

### state_initialize()
Performs system initialization and basic checks.

### state_calibrate()
Establishes baseline calibration and verifies system readiness.

### state_monitor()
Continuously monitors S-ROI metrics and determines next action.

### state_optimize()
Actively optimizes S-ROI value towards target through incremental adjustments.

### state_stable()
Maintains stable operation and monitors for degradation.

### state_warning()
Handles warning conditions and determines escalation or recovery.

### state_critical()
Manages critical conditions and initiates emergency procedures.

### state_recovery()
Executes recovery procedures to restore normal operation.

### state_shutdown()
Performs graceful system shutdown.

## Usage Examples

### Basic Usage

```python
from sroi_sovereign_protocol import SROISovereignProtocol

# Initialize protocol
protocol = SROISovereignProtocol(initial_sroi=0.5192)

# Run for 50 cycles
protocol.run(max_cycles=50)

# Get final status
status = protocol.get_status()
print(f"Final S-ROI: {status['sroi_value']:.4f}")
```

### With Custom Notification Handler

```python
from sroi_sovereign_protocol import (
    SROISovereignProtocol,
    NotificationLevel,
    Notification
)

def email_handler(notification: Notification):
    if notification.level == NotificationLevel.EMERGENCY:
        # Send emergency email
        send_email(f"EMERGENCY: {notification.message}")

protocol = SROISovereignProtocol(initial_sroi=0.20)
protocol.notification_system.register_handler(email_handler)
protocol.run(max_cycles=30)
```

### Manual Cycle Execution

```python
from sroi_sovereign_protocol import SROISovereignProtocol

protocol = SROISovereignProtocol(initial_sroi=0.60)

# Execute cycles manually
for i in range(20):
    metrics = protocol.execute_cycle()
    print(f"Cycle {i}: S-ROI = {metrics['sroi_value']:.4f}")
    
    # Custom logic between cycles
    if metrics['state'] == 'stable':
        print("Optimal state achieved!")
        break
```

## Integration with Existing Systems

### Integration with eternal_deposition.py

The S-ROI Sovereign Protocol can be integrated with the Eternal Deposition System:

```python
from eternal_deposition import EternalDepositionEngine
from sroi_sovereign_protocol import SROISovereignProtocol

# Initialize both systems
eternal_engine = EternalDepositionEngine(initial_nodes=144)
sroi_protocol = SROISovereignProtocol(initial_sroi=0.5192)

# Use eternal engine metrics to update S-ROI
def update_sroi_from_eternal(eternal_metrics):
    # Map eternal engine metrics to S-ROI
    avg_energy = eternal_metrics.get('avg_energy', 0.5)
    sroi_protocol.sroi_value = avg_energy
    sroi_protocol.execute_cycle()

# Run with callback
eternal_engine.run_perpetual(
    max_cycles=100,
    callback=update_sroi_from_eternal
)
```

## Log File Analysis

### Text Log Format

```
2026-01-22 16:55:00,000 - SROI_Protocol - INFO - [STATE_TRANSITION] [VALID] initializing -> calibrating | S-ROI: 0.5192 | Reason: Initialization complete
2026-01-22 16:55:00,500 - SROI_Protocol - INFO - [FLOW_EVENT] CALIBRATION: System calibration in progress
2026-01-22 16:55:01,000 - SROI_Protocol - WARNING - [NOTIFICATION] [WARNING] State: warning | S-ROI: 0.4500 | Below threshold
```

### JSON Log Structure

```json
{
  "last_updated": "2026-01-22T16:55:00.000000",
  "state_transitions": [
    {
      "timestamp": "2026-01-22T16:55:00.000000",
      "from_state": "initializing",
      "to_state": "calibrating",
      "sroi_value": 0.5192,
      "reason": "Initialization complete",
      "valid": true,
      "metadata": {
        "validation_message": "Transition validated successfully"
      }
    }
  ],
  "notifications": [
    {
      "timestamp": "2026-01-22T16:55:01.000000",
      "level": "warning",
      "state": "warning",
      "message": "S-ROI below warning threshold",
      "sroi_value": 0.4500,
      "threshold_violated": "WARNING_LOW (0.500)"
    }
  ]
}
```

## Demo Scripts

Run the demo scripts to see the protocol in action:

### Basic Demo
```bash
python3 demo_sroi_protocol.py
```

This runs multiple demonstrations:
1. Basic protocol operation
2. State transition validation
3. Notification system
4. Modular state functions
5. S-ROI optimization flow
6. Log file generation

### Individual Demos

Run the main protocol:
```bash
python3 sroi_sovereign_protocol.py
```

## Best Practices

### 1. Initialization

Always initialize with a realistic S-ROI value:
```python
# Good
protocol = SROISovereignProtocol(initial_sroi=0.5192)

# Avoid extreme values
protocol = SROISovereignProtocol(initial_sroi=0.05)  # Too low
```

### 2. Notification Handlers

Keep handlers lightweight and non-blocking:
```python
def good_handler(notification):
    # Quick logging
    log.info(notification.message)

def bad_handler(notification):
    # Avoid slow operations
    time.sleep(10)  # BAD!
    send_http_request()  # Could block
```

### 3. State Monitoring

Check status periodically:
```python
status = protocol.get_status()
if status['current_state'] == 'critical':
    # Take immediate action
    handle_critical_state()
```

### 4. Log File Management

Rotate logs for long-running operations:
```python
import logging.handlers

handler = logging.handlers.RotatingFileHandler(
    'sroi_protocol.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
```

## Troubleshooting

### Invalid State Transitions

If you see invalid transition warnings:
1. Check the state transition graph
2. Verify S-ROI value is appropriate for target state
3. Review logs for validation messages

### S-ROI Not Converging

If S-ROI doesn't reach target:
1. Increase max_cycles
2. Check for critical states blocking optimization
3. Review optimization_attempts in status

### Missing Notifications

If expected notifications aren't sent:
1. Verify handler is registered
2. Check notification levels and thresholds
3. Review notification history in logs

## Performance Considerations

- **Cycle Duration**: Each cycle takes ~0.5 seconds by default
- **Log File Size**: Grows with number of cycles (~1KB per cycle)
- **Memory Usage**: Minimal, primarily for log history
- **CPU Usage**: Very low, mostly I/O bound

## Future Enhancements

Potential areas for extension:
1. Database backend for log storage
2. Real-time dashboard integration
3. Machine learning for S-ROI prediction
4. Distributed protocol coordination
5. Advanced recovery strategies
6. Custom optimization algorithms

## License

This implementation follows the repository license.

## References

- [COVENANT_OF_RESONANCE.md](COVENANT_OF_RESONANCE.md)
- [README.md](README.md)
- [eternal_deposition.py](eternal_deposition.py)

---

**Version**: 1.0.0  
**Last Updated**: January 22, 2026  
**Status**: Production Ready
