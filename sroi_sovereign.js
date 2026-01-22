/**
 * S-ROI Sovereign Protocol - Enhanced State Management System
 * =============================================================
 * 
 * JavaScript/Web implementation of the S-ROI (Social Return on Investment)
 * Sovereign protocol with advanced state management, resonance tracking,
 * and stealth mode capabilities.
 * 
 * Key Features:
 * - Three-state system: STABLE, WARNING, CRITICAL
 * - Comprehensive logging for state changes and resonance values
 * - Cooldown mechanism for stealth mode activation
 * - Modular architecture for easy testing and maintenance
 * - Compatible with web browsers and Node.js
 */

// Constants
const SROI_TARGET = 0.950;  // Target S-ROI value
const RESONANCE_WARNING_THRESHOLD = 0.850;  // WARNING state threshold
const RESONANCE_CRITICAL_THRESHOLD = 0.700;  // CRITICAL state threshold
const STEALTH_COOLDOWN_MS = 60000;  // Cooldown period in milliseconds (60 seconds)

// Enumerations
const SROIState = {
    STABLE: 'STABLE',
    WARNING: 'WARNING',
    CRITICAL: 'CRITICAL'
};

const StealthMode = {
    ACTIVE: 'ACTIVE',
    INACTIVE: 'INACTIVE',
    COOLDOWN: 'COOLDOWN'
};

/**
 * Logger for S-ROI Sovereign protocol
 */
class SROILogger {
    constructor() {
        this.stateChangeHistory = [];
        this.resonanceHistory = [];
        this.maxHistorySize = 1000;
    }

    logStateChange(previousState, newState, resonanceValue, reason) {
        const logEntry = {
            timestamp: new Date(),
            previousState,
            newState,
            resonanceValue,
            reason
        };

        this.stateChangeHistory.push(logEntry);
        this._trimHistory(this.stateChangeHistory);

        this._log('WARN', 
            `STATE CHANGE: ${previousState} -> ${newState} | ` +
            `Resonance: ${resonanceValue.toFixed(4)} | Reason: ${reason}`
        );
    }

    logResonance(value, state, stealthActive) {
        const logEntry = {
            timestamp: new Date(),
            value,
            state,
            stealthActive
        };

        this.resonanceHistory.push(logEntry);
        this._trimHistory(this.resonanceHistory);

        this._log('DEBUG',
            `RESONANCE: ${value.toFixed(4)} | State: ${state} | ` +
            `Stealth: ${stealthActive ? 'ACTIVE' : 'INACTIVE'}`
        );
    }

    logStealthActivation(success, reason) {
        const level = success ? 'INFO' : 'WARN';
        const status = success ? 'ACTIVATED' : 'DENIED';
        this._log(level, `STEALTH MODE ${status}: ${reason}`);
    }

    logInfo(message) {
        this._log('INFO', message);
    }

    logWarning(message) {
        this._log('WARN', message);
    }

    logError(message) {
        this._log('ERROR', message);
    }

    _log(level, message) {
        const timestamp = new Date().toISOString();
        const logMessage = `[${timestamp}] [SROI_Sovereign] [${level}] ${message}`;
        
        switch(level) {
            case 'ERROR':
                console.error(logMessage);
                break;
            case 'WARN':
                console.warn(logMessage);
                break;
            case 'DEBUG':
                // Only log debug in development or if explicitly enabled
                if (this.debugEnabled) {
                    console.log(logMessage);
                }
                break;
            default:
                console.log(logMessage);
        }
    }

    _trimHistory(historyList) {
        if (historyList.length > this.maxHistorySize) {
            historyList.splice(0, historyList.length - this.maxHistorySize);
        }
    }

    getStateChangeHistory(limit = null) {
        if (limit) {
            return this.stateChangeHistory.slice(-limit);
        }
        return [...this.stateChangeHistory];
    }

    getResonanceHistory(limit = null) {
        if (limit) {
            return this.resonanceHistory.slice(-limit);
        }
        return [...this.resonanceHistory];
    }

    enableDebug(enabled = true) {
        this.debugEnabled = enabled;
    }
}

/**
 * Controller for stealth mode with cooldown mechanism
 */
class StealthModeController {
    constructor(cooldownMs = STEALTH_COOLDOWN_MS) {
        this.cooldownMs = cooldownMs;
        this.mode = StealthMode.INACTIVE;
        this.lastDeactivationTime = null;
        this.activationCount = 0;
        this.deactivationCount = 0;
    }

    canActivate() {
        if (this.mode === StealthMode.ACTIVE) {
            return false;
        }

        if (this.lastDeactivationTime === null) {
            return true;
        }

        const elapsed = Date.now() - this.lastDeactivationTime;
        return elapsed >= this.cooldownMs;
    }

    activate() {
        if (!this.canActivate()) {
            return false;
        }

        this.mode = StealthMode.ACTIVE;
        this.activationCount++;
        return true;
    }

    deactivate() {
        if (this.mode === StealthMode.ACTIVE) {
            this.mode = StealthMode.COOLDOWN;
            this.lastDeactivationTime = Date.now();
            this.deactivationCount++;
        }
    }

    update() {
        if (this.mode === StealthMode.COOLDOWN) {
            if (this.canActivate()) {
                this.mode = StealthMode.INACTIVE;
            }
        }
    }

    getCooldownRemaining() {
        if (this.lastDeactivationTime === null) {
            return 0;
        }

        const elapsed = Date.now() - this.lastDeactivationTime;
        const remaining = this.cooldownMs - elapsed;
        return Math.max(0, remaining);
    }

    isActive() {
        return this.mode === StealthMode.ACTIVE;
    }

    getStatus() {
        return {
            mode: this.mode,
            isActive: this.isActive(),
            canActivate: this.canActivate(),
            cooldownRemaining: this.getCooldownRemaining(),
            activationCount: this.activationCount,
            deactivationCount: this.deactivationCount
        };
    }
}

/**
 * S-ROI Sovereign Protocol - Main Controller
 */
class SROISovereign {
    constructor(options = {}) {
        const {
            initialResonance = 0.5,
            debugLogging = false,
            cooldownMs = STEALTH_COOLDOWN_MS
        } = options;

        this.currentResonance = initialResonance;
        this.state = this._determineState(initialResonance);

        // Initialize subsystems
        this.logger = new SROILogger();
        this.logger.enableDebug(debugLogging);
        this.stealthController = new StealthModeController(cooldownMs);

        // System metrics
        this.startTime = Date.now();
        this.updateCount = 0;

        // Event callbacks
        this.eventCallbacks = new Map();

        this.logger.logInfo(
            `S-ROI Sovereign initialized | ` +
            `Initial resonance: ${initialResonance.toFixed(4)} | ` +
            `State: ${this.state}`
        );
    }

    _determineState(resonance) {
        if (resonance >= RESONANCE_WARNING_THRESHOLD) {
            return SROIState.STABLE;
        } else if (resonance >= RESONANCE_CRITICAL_THRESHOLD) {
            return SROIState.WARNING;
        } else {
            return SROIState.CRITICAL;
        }
    }

    updateResonance(newResonance, reason = 'Manual update') {
        // Clamp resonance to valid range
        newResonance = Math.max(0.0, Math.min(1.0, newResonance));

        const previousResonance = this.currentResonance;
        this.currentResonance = newResonance;

        // Determine new state
        const newState = this._determineState(newResonance);

        // Log resonance change
        this.logger.logResonance(
            newResonance,
            newState,
            this.stealthController.isActive()
        );

        // Check for state change
        if (newState !== this.state) {
            const previousState = this.state;
            this.state = newState;
            
            this.logger.logStateChange(
                previousState,
                newState,
                newResonance,
                reason
            );

            // Emit state change event
            this._emit('stateChange', {
                previousState,
                newState,
                resonance: newResonance,
                reason
            });
        }

        // Emit resonance update event
        this._emit('resonanceUpdate', {
            resonance: newResonance,
            state: newState,
            previousResonance
        });

        this.updateCount++;
    }

    requestStealthActivation(reason = 'Manual request') {
        this.stealthController.update();

        if (this.stealthController.canActivate()) {
            const success = this.stealthController.activate();
            if (success) {
                this.logger.logStealthActivation(true, reason);
                this._emit('stealthActivated', { reason });
                return true;
            }
        }

        // Activation denied
        const cooldownRemaining = this.stealthController.getCooldownRemaining();
        const denialReason = `${reason} | Cooldown: ${(cooldownRemaining / 1000).toFixed(1)}s remaining`;
        this.logger.logStealthActivation(false, denialReason);
        this._emit('stealthDenied', { reason: denialReason, cooldownRemaining });
        return false;
    }

    deactivateStealth(reason = 'Manual deactivation') {
        if (this.stealthController.isActive()) {
            this.stealthController.deactivate();
            this.logger.logInfo(`Stealth mode deactivated: ${reason}`);
            this._emit('stealthDeactivated', { reason });
        }
    }

    getStatus() {
        const uptime = (Date.now() - this.startTime) / 1000;

        return {
            currentResonance: this.currentResonance,
            state: this.state,
            stealth: this.stealthController.getStatus(),
            uptimeSeconds: uptime,
            updateCount: this.updateCount,
            targetSROI: SROI_TARGET,
            warningThreshold: RESONANCE_WARNING_THRESHOLD,
            criticalThreshold: RESONANCE_CRITICAL_THRESHOLD
        };
    }

    getStateHistory(limit = 10) {
        const history = this.logger.getStateChangeHistory(limit);
        return history.map(entry => ({
            timestamp: entry.timestamp.toISOString(),
            previousState: entry.previousState,
            newState: entry.newState,
            resonanceValue: entry.resonanceValue,
            reason: entry.reason
        }));
    }

    getResonanceHistory(limit = 10) {
        const history = this.logger.getResonanceHistory(limit);
        return history.map(entry => ({
            timestamp: entry.timestamp.toISOString(),
            value: entry.value,
            state: entry.state,
            stealthActive: entry.stealthActive
        }));
    }

    // Event system
    on(event, callback) {
        if (!this.eventCallbacks.has(event)) {
            this.eventCallbacks.set(event, []);
        }
        this.eventCallbacks.get(event).push(callback);
    }

    _emit(event, data) {
        if (this.eventCallbacks.has(event)) {
            this.eventCallbacks.get(event).forEach(callback => {
                try {
                    callback(data);
                } catch (err) {
                    console.error(`Error in event callback for ${event}:`, err);
                }
            });
        }
    }
}

// Export for Node.js and browser
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        SROISovereign,
        SROILogger,
        StealthModeController,
        SROIState,
        StealthMode,
        SROI_TARGET,
        RESONANCE_WARNING_THRESHOLD,
        RESONANCE_CRITICAL_THRESHOLD,
        STEALTH_COOLDOWN_MS
    };
}

// Browser global
if (typeof window !== 'undefined') {
    window.SROISovereign = SROISovereign;
    window.SROIProtocol = {
        SROISovereign,
        SROILogger,
        StealthModeController,
        SROIState,
        StealthMode,
        SROI_TARGET,
        RESONANCE_WARNING_THRESHOLD,
        RESONANCE_CRITICAL_THRESHOLD,
        STEALTH_COOLDOWN_MS
    };
}
