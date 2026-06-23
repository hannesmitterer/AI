# S-ROI Sovereign Protocol - Documentation

## Overview

The **S-ROI Sovereign Protocol** is an enhanced state management system designed to improve the management and scalability of S-ROI (Social Return on Investment) operations. The protocol implements a three-state system with comprehensive logging, stealth mode capabilities, and a modular architecture.

## Key Features

### 1. Three-State Management System

The protocol operates in three distinct states based on current resonance values:

- **STABLE** (≥ 0.850): Normal operations, optimal performance
- **WARNING** (0.700 - 0.849): Approaching critical threshold, monitoring required
- **CRITICAL** (< 0.700): Immediate attention needed, corrective action required

States automatically transition based on resonance value changes, with all transitions logged for audit and analysis.

### 2. Comprehensive Logging

All system events are logged with timestamps:

- **State Changes**: Tracks transitions between STABLE, WARNING, and CRITICAL
- **Resonance Values**: Records all resonance measurements with context
- **Stealth Mode Events**: Logs activation/deactivation attempts and results
- **History Tracking**: Maintains configurable history (default: 1000 entries)

### 3. Stealth Mode with Cooldown

Stealth mode provides protected operations with built-in safety mechanisms:

- **Activation Control**: Prevents simultaneous or rapid activations
- **Cooldown Period**: 60-second mandatory cooldown between deactivations and reactivations
- **Status Tracking**: Monitors activation/deactivation counts and cooldown state

### 4. Modular Architecture

The protocol is designed with modularity in mind:

- **SROILogger**: Independent logging subsystem
- **StealthModeController**: Self-contained stealth mode management
- **SROISovereign**: Main controller orchestrating all components

## Components

### SROILogger

Manages all logging operations and history tracking.

**Key Methods:**
- `log_state_change(previous_state, new_state, resonance_value, reason)`
- `log_resonance(value, state, stealth_active)`
- `log_stealth_activation(success, reason)`
- `get_state_change_history(limit=None)`
- `get_resonance_history(limit=None)`

### StealthModeController

Controls stealth mode activation with cooldown enforcement.

**Key Methods:**
- `can_activate()`: Check if activation is allowed
- `activate()`: Activate stealth mode
- `deactivate()`: Deactivate stealth mode and start cooldown
- `get_cooldown_remaining()`: Get remaining cooldown time
- `get_status()`: Get comprehensive stealth mode status

### SROISovereign

Main protocol controller integrating all subsystems.

**Key Methods:**
- `update_resonance(new_resonance, reason)`: Update resonance and handle state transitions
- `request_stealth_activation(reason)`: Request stealth mode activation
- `deactivate_stealth(reason)`: Deactivate stealth mode
- `get_status()`: Get complete system status
- `get_state_history(limit)`: Get recent state changes
- `get_resonance_history(limit)`: Get recent resonance values

## Usage Examples

### Python

```python
from sroi_sovereign import SROISovereign
import logging

# Initialize the protocol
sovereign = SROISovereign(
    initial_resonance=0.9,
    log_level=logging.INFO,
    cooldown_seconds=60.0
)

# Update resonance (triggers automatic state management)
sovereign.update_resonance(0.82, "Normal fluctuation")

# Activate stealth mode
success = sovereign.request_stealth_activation("Entering protected mode")
if success:
    print("Stealth mode active")
    
    # Perform protected operations
    # ...
    
    # Deactivate when done
    sovereign.deactivate_stealth("Operations complete")

# Get system status
status = sovereign.get_status()
print(f"Current state: {status['state']}")
print(f"Resonance: {status['current_resonance']:.4f}")

# View recent state changes
history = sovereign.get_state_history(limit=5)
for entry in history:
    print(f"{entry['timestamp']}: {entry['previous_state']} -> {entry['new_state']}")
```

### JavaScript

```javascript
// Initialize the protocol
const sovereign = new SROISovereign({
    initialResonance: 0.9,
    debugLogging: true,
    cooldownMs: 60000
});

// Listen to events
sovereign.on('stateChange', (data) => {
    console.log(`State changed: ${data.previousState} -> ${data.newState}`);
});

sovereign.on('resonanceUpdate', (data) => {
    console.log(`Resonance: ${data.resonance.toFixed(4)}`);
});

// Update resonance
sovereign.updateResonance(0.82, 'Normal fluctuation');

// Activate stealth mode
const success = sovereign.requestStealthActivation('Entering protected mode');
if (success) {
    console.log('Stealth mode active');
    
    // Perform protected operations
    // ...
    
    // Deactivate when done
    sovereign.deactivateStealth('Operations complete');
}

// Get system status
const status = sovereign.getStatus();
console.log(`Current state: ${status.state}`);
console.log(`Resonance: ${status.currentResonance.toFixed(4)}`);
```

## Configuration

### Constants

| Constant | Default Value | Description |
|----------|---------------|-------------|
| `SROI_TARGET` | 0.950 | Target S-ROI value |
| `RESONANCE_WARNING_THRESHOLD` | 0.850 | Threshold for WARNING state |
| `RESONANCE_CRITICAL_THRESHOLD` | 0.700 | Threshold for CRITICAL state |
| `STEALTH_COOLDOWN_SECONDS` (Python) | 60.0 | Cooldown period in seconds |
| `STEALTH_COOLDOWN_MS` (JavaScript) | 60000 | Cooldown period in milliseconds |

### Customization

All constants can be customized by modifying the configuration at initialization:

**Python:**
```python
sovereign = SROISovereign(
    initial_resonance=0.85,
    log_level=logging.DEBUG,  # More verbose logging
    cooldown_seconds=30.0      # Reduced cooldown
)
```

**JavaScript:**
```javascript
const sovereign = new SROISovereign({
    initialResonance: 0.85,
    debugLogging: true,        // Enable debug logging
    cooldownMs: 30000          // Reduced cooldown
});
```

## Testing

### Running Tests

**Python:**
```bash
python3 test_sroi_sovereign.py
```

The test suite includes:
- Logger functionality tests
- Stealth mode controller tests
- Main sovereign controller tests
- Edge case and boundary condition tests

### Running Demos

**Python:**
```bash
python3 demo_sroi_sovereign.py
```

The demo showcases:
- Basic initialization
- State transitions
- Stealth mode with cooldown
- Logging and history
- Edge case handling

## Integration

### With Eternal Deposition System

The S-ROI Sovereign protocol can be integrated with the Eternal Deposition System:

```python
from eternal_deposition import EternalDepositionEngine
from sroi_sovereign import SROISovereign

# Initialize both systems
engine = EternalDepositionEngine(initial_nodes=144)
sovereign = SROISovereign(initial_resonance=0.9)

# Update S-ROI based on eternal system metrics
def update_callback(metrics):
    # Calculate S-ROI from eternal system
    sroi = metrics['avg_energy'] * 0.95  # Example calculation
    sovereign.update_resonance(sroi, f"Eternal cycle {metrics['cycle']}")
    
    # Use stealth mode during stillness
    if metrics['in_stillness']:
        sovereign.request_stealth_activation("Stillness recalibration")
    elif sovereign.stealth_controller.is_active():
        sovereign.deactivate_stealth("Stillness complete")

# Run eternal system with S-ROI updates
engine.run_perpetual(callback=update_callback)
```

## API Reference

### Python API

See inline documentation in `sroi_sovereign.py` for complete API reference.

### JavaScript API

See inline documentation in `sroi_sovereign.js` for complete API reference.

## Best Practices

1. **Always handle state transitions**: Monitor state change events to respond appropriately
2. **Respect cooldown periods**: Don't attempt to bypass stealth mode cooldown
3. **Log meaningful reasons**: Provide descriptive reasons for resonance updates
4. **Monitor history**: Periodically review state and resonance history for patterns
5. **Test edge cases**: Ensure your integration handles boundary conditions properly

## Changelog

### Version 1.0.0 (2026-01-22)

Initial release with:
- Three-state management system (STABLE, WARNING, CRITICAL)
- Comprehensive logging for state changes and resonance values
- Stealth mode with 60-second cooldown mechanism
- Modular architecture for easy testing and maintenance
- Python and JavaScript implementations
- Comprehensive test suite
- Demo scripts and documentation

## License

Part of the Resonance School / AIC NEXUS repository.
See repository LICENSE for details.

## Support

For issues, questions, or contributions, please refer to the main repository documentation.
