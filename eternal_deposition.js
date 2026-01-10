/**
 * Eternal Deposition System - Web/JavaScript Implementation
 * ==========================================================
 * 
 * Self-sustaining algorithm operating at 0.043 Hz resonance
 * for perpetual iterative logic with fractal propagation.
 * 
 * Compatible with web browsers and Node.js
 */

// Universal Constants
const UNIVERSAL_RESONANCE_HZ = 0.043;  // Base frequency
const CYCLE_PERIOD_MS = (1.0 / UNIVERSAL_RESONANCE_HZ) * 1000;  // ~23260 ms
const SCHUMANN_RESONANCE_HZ = 7.83;  // Earth's natural frequency (for future harmonic integration)
const HARMONIC_432_HZ = 432.0;  // Universal tuning frequency (for future harmonic integration)
const PHI = (1 + Math.sqrt(5)) / 2;  // Golden ratio

// Configuration constants
const SACRED_HISTORY_LIMIT = 144;  // Maximum feedback history per node
const MAX_OPTIMIZATION_METRICS = 1000;  // Maximum optimization metrics to retain
const STILLNESS_DURATION_CAP_MS = 2000;  // Maximum stillness duration in ms (practical cap for real-time operation)

/**
 * Node class representing a single entity in the network
 */
class Node {
    constructor(nodeId) {
        this.nodeId = nodeId;
        this.energyLevel = 1.0;
        this.resonancePhase = 0.0;
        this.lastOptimization = Date.now();
        this.optimizationCount = 0;
        this.stillnessCount = 0;
        this.feedbackHistory = [];
    }

    applyFeedback(feedbackValue) {
        this.feedbackHistory.push(feedbackValue);
        
        // Keep only recent history
        if (this.feedbackHistory.length > SACRED_HISTORY_LIMIT) {
            this.feedbackHistory = this.feedbackHistory.slice(-SACRED_HISTORY_LIMIT);
        }
        
        // Optimize energy based on feedback
        this.energyLevel = Math.max(0.0, Math.min(1.0,
            this.energyLevel + feedbackValue * 0.1));
        this.optimizationCount++;
    }

    enterStillness() {
        this.stillnessCount++;
        // Slight energy restoration during stillness
        this.energyLevel = Math.min(1.0, this.energyLevel + 0.05);
    }

    toJSON() {
        return {
            nodeId: this.nodeId,
            energyLevel: this.energyLevel,
            optimizationCount: this.optimizationCount,
            stillnessCount: this.stillnessCount
        };
    }
}

/**
 * Eternal Deposition Engine
 * Core system for perpetual iterative logic
 */
class EternalDepositionEngine {
    constructor(initialNodes = 144) {
        this.nodes = new Map();
        this.cycleCount = 0;
        this.startTime = Date.now();
        this.lastCycleTime = this.startTime;
        this.isInStillness = false;
        this.optimizationMetrics = [];
        this.eventCallbacks = new Map();
        this.isRunning = false;
        this.cycleInterval = null;

        // Initialize node network
        for (let i = 0; i < initialNodes; i++) {
            const nodeId = `node_${String(i).padStart(4, '0')}`;
            this.nodes.set(nodeId, new Node(nodeId));
        }

        this.log(`Initialized with ${this.nodes.size} nodes`);
        this.log(`Base frequency: ${UNIVERSAL_RESONANCE_HZ} Hz`);
        this.log(`Cycle period: ${(CYCLE_PERIOD_MS / 1000).toFixed(2)} seconds`);
    }

    log(message, type = 'INFO') {
        const timestamp = new Date().toISOString();
        console.log(`[${timestamp}] [${type}] ${message}`);
        
        // Emit log event
        this.emit('log', { timestamp, type, message });
    }

    on(event, callback) {
        if (!this.eventCallbacks.has(event)) {
            this.eventCallbacks.set(event, []);
        }
        this.eventCallbacks.get(event).push(callback);
    }

    emit(event, data) {
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

    calculateResonancePhase(currentTime = Date.now()) {
        const elapsed = (currentTime - this.startTime) / 1000;  // Convert to seconds
        const phase = (elapsed * UNIVERSAL_RESONANCE_HZ * 2 * Math.PI) % (2 * Math.PI);
        return phase;
    }

    shouldEnterStillness() {
        const phase = this.calculateResonancePhase();
        
        // Enter stillness at phase transitions (every 1/4 cycle)
        const stillnessPhases = [Math.PI/2, Math.PI, 3*Math.PI/2, 2*Math.PI];
        const tolerance = 0.2;
        
        for (const stillnessPhase of stillnessPhases) {
            if (Math.abs(phase - stillnessPhase) < tolerance) {
                return true;
            }
        }
        return false;
    }

    calculateNodalFeedback() {
        if (this.nodes.size === 0) return 0.0;

        // Calculate average energy across all nodes
        let totalEnergy = 0;
        for (const node of this.nodes.values()) {
            totalEnergy += node.energyLevel;
        }
        const avgEnergy = totalEnergy / this.nodes.size;

        // Calculate feedback based on deviation from optimal (0.5)
        const feedback = (avgEnergy - 0.5) * 0.1;

        // Apply harmonic resonance factor
        const phase = this.calculateResonancePhase();
        const resonanceFactor = Math.sin(phase) * 0.05;

        return feedback + resonanceFactor;
    }

    propagateFractalPattern(depth = 3) {
        if (depth <= 0) return;

        const currentCount = this.nodes.size;
        const newNodesCount = Math.floor(currentCount * (1 / PHI));

        if (newNodesCount > 0) {
            const parentNodes = Array.from(this.nodes.values());
            
            for (let i = 0; i < newNodesCount; i++) {
                // Select parent using modulo for cyclic inheritance
                const parent = parentNodes[i % parentNodes.length];
                
                const newNodeId = `fractal_${depth}_${String(i).padStart(4, '0')}`;
                const newNode = new Node(newNodeId);
                newNode.energyLevel = parent.energyLevel * 0.8;  // Inherit 80% energy
                newNode.resonancePhase = parent.resonancePhase;
                
                this.nodes.set(newNodeId, newNode);
            }

            this.log(`Propagated ${newNodesCount} nodes at depth ${depth}`, 'FRACTAL');
            this.emit('fractal_propagation', { depth, newNodes: newNodesCount });
        }

        // Recursive propagation to next level
        if (depth > 1) {
            this.propagateFractalPattern(depth - 1);
        }
    }

    optimizeNetwork() {
        const feedback = this.calculateNodalFeedback();

        // Apply feedback to all nodes
        for (const node of this.nodes.values()) {
            node.applyFeedback(feedback);
        }

        // Track optimization metrics
        this.optimizationMetrics.push(feedback);
        if (this.optimizationMetrics.length > MAX_OPTIMIZATION_METRICS) {
            this.optimizationMetrics = this.optimizationMetrics.slice(-MAX_OPTIMIZATION_METRICS);
        }

        // Record optimization
        const currentTime = Date.now();
        for (const node of this.nodes.values()) {
            node.lastOptimization = currentTime;
        }
    }

    async executeStillness() {
        this.log(`Entering recalibration phase at cycle ${this.cycleCount}`, 'STILLNESS');
        
        this.isInStillness = true;

        // All nodes enter stillness
        for (const node of this.nodes.values()) {
            node.enterStillness();
        }

        // System introspection
        let totalEnergy = 0;
        let totalOptimizations = 0;
        
        for (const node of this.nodes.values()) {
            totalEnergy += node.energyLevel;
            totalOptimizations += node.optimizationCount;
        }
        
        const avgEnergy = totalEnergy / this.nodes.size;

        this.log(`Average energy: ${avgEnergy.toFixed(4)}`, 'INTROSPECTION');
        this.log(`Total optimizations: ${totalOptimizations}`, 'INTROSPECTION');
        this.log(`Active nodes: ${this.nodes.size}`, 'INTROSPECTION');

        this.emit('stillness', {
            avgEnergy,
            totalOptimizations,
            activeNodes: this.nodes.size
        });

        // Stillness duration: golden ratio of cycle period (capped for practicality)
        // Theoretical: ~14.4s, Practical cap: 2.0s for responsive operation
        const stillnessDuration = Math.min(CYCLE_PERIOD_MS / PHI, STILLNESS_DURATION_CAP_MS);
        
        await new Promise(resolve => setTimeout(resolve, stillnessDuration));

        this.isInStillness = false;
        this.log('Recalibration complete', 'STILLNESS');
    }

    async executeCycle() {
        const cycleStart = Date.now();
        
        // Calculate resonance phase
        const phase = this.calculateResonancePhase();

        // Check for stillness condition
        if (this.shouldEnterStillness() && !this.isInStillness) {
            await this.executeStillness();
        }

        // Optimize network through feedback
        if (!this.isInStillness) {
            this.optimizeNetwork();
        }

        // Periodic fractal propagation (every 10 cycles)
        if (this.cycleCount % 10 === 0 && this.cycleCount > 0) {
            this.propagateFractalPattern(2);
        }

        // Update cycle tracking
        this.cycleCount++;
        this.lastCycleTime = Date.now();

        // Calculate cycle metrics
        let totalEnergy = 0;
        for (const node of this.nodes.values()) {
            totalEnergy += node.energyLevel;
        }
        const avgEnergy = totalEnergy / this.nodes.size;
        const cycleDuration = Date.now() - cycleStart;

        const metrics = {
            cycle: this.cycleCount,
            timestamp: new Date().toISOString(),
            phase: phase,
            phaseDegrees: (phase * 180 / Math.PI),
            nodes: this.nodes.size,
            avgEnergy: avgEnergy,
            inStillness: this.isInStillness,
            cycleDuration: cycleDuration,
            resonanceHz: UNIVERSAL_RESONANCE_HZ
        };

        // Emit cycle event
        this.emit('cycle', metrics);

        // Display periodic status
        if (this.cycleCount % 5 === 0) {
            this.log(
                `CYCLE ${String(metrics.cycle).padStart(4, '0')} | ` +
                `Phase: ${metrics.phaseDegrees.toFixed(1)}° | ` +
                `Nodes: ${metrics.nodes} | ` +
                `Energy: ${metrics.avgEnergy.toFixed(4)}`,
                'CYCLE'
            );
        }

        return metrics;
    }

    start(maxCycles = null) {
        if (this.isRunning) {
            this.log('Already running', 'WARNING');
            return;
        }

        this.isRunning = true;
        this.log('Starting perpetual operation...', 'ETERNAL');

        const runCycle = async () => {
            if (!this.isRunning) return;
            
            if (maxCycles !== null && this.cycleCount >= maxCycles) {
                this.stop();
                return;
            }

            await this.executeCycle();

            // Schedule next cycle synchronized to resonance
            const nextCycleTime = this.startTime + (this.cycleCount * CYCLE_PERIOD_MS);
            const now = Date.now();
            const sleepDuration = Math.max(0, nextCycleTime - now);

            this.cycleInterval = setTimeout(runCycle, sleepDuration);
        };

        runCycle();
    }

    stop() {
        if (!this.isRunning) return;

        this.isRunning = false;
        if (this.cycleInterval) {
            clearTimeout(this.cycleInterval);
            this.cycleInterval = null;
        }

        this.log('Graceful termination', 'ETERNAL');
        this.saveState();
        this.emit('stopped', this.getStatus());
    }

    saveState() {
        let totalEnergy = 0;
        let totalOptimizations = 0;
        let totalStillness = 0;

        for (const node of this.nodes.values()) {
            totalEnergy += node.energyLevel;
            totalOptimizations += node.optimizationCount;
            totalStillness += node.stillnessCount;
        }

        const state = {
            cycleCount: this.cycleCount,
            nodes: this.nodes.size,
            avgEnergy: totalEnergy / this.nodes.size,
            totalOptimizations: totalOptimizations,
            totalStillnessEvents: totalStillness,
            uptimeSeconds: (Date.now() - this.startTime) / 1000,
            timestamp: new Date().toISOString()
        };

        this.log('State snapshot created', 'STATE');
        this.emit('state_saved', state);

        return state;
    }

    getStatus() {
        const uptime = (Date.now() - this.startTime) / 1000;
        let totalEnergy = 0;
        let totalOptimizations = 0;
        let totalStillness = 0;

        for (const node of this.nodes.values()) {
            totalEnergy += node.energyLevel;
            totalOptimizations += node.optimizationCount;
            totalStillness += node.stillnessCount;
        }

        return {
            status: this.isRunning ? 'OPERATIONAL' : 'STOPPED',
            cycleCount: this.cycleCount,
            uptimeSeconds: uptime,
            nodes: this.nodes.size,
            resonanceHz: UNIVERSAL_RESONANCE_HZ,
            cyclePeriod: CYCLE_PERIOD_MS / 1000,
            avgEnergy: totalEnergy / this.nodes.size,
            isInStillness: this.isInStillness,
            totalOptimizations: totalOptimizations,
            totalStillnessEvents: totalStillness
        };
    }

    getNodesArray() {
        return Array.from(this.nodes.values()).map(node => node.toJSON());
    }
}

// Export for Node.js and browser
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        EternalDepositionEngine,
        Node,
        UNIVERSAL_RESONANCE_HZ,
        CYCLE_PERIOD_MS,
        SCHUMANN_RESONANCE_HZ,
        HARMONIC_432_HZ,
        PHI,
        SACRED_HISTORY_LIMIT,
        MAX_OPTIMIZATION_METRICS,
        STILLNESS_DURATION_CAP_MS
    };
}

// Browser global
if (typeof window !== 'undefined') {
    window.EternalDepositionEngine = EternalDepositionEngine;
    window.EternalDeposition = {
        EternalDepositionEngine,
        Node,
        UNIVERSAL_RESONANCE_HZ,
        CYCLE_PERIOD_MS,
        SCHUMANN_RESONANCE_HZ,
        HARMONIC_432_HZ,
        PHI
    };
}
