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

// Climate Pattern Constants
const CLIMATE_PATTERN_HISTORY = 288;  // 24 hours of data at 5-minute intervals
const CLIMATE_DATA_RELIABILITY_THRESHOLD = 0.85;  // Minimum reliability score for climate data
const CLIMATE_UPDATE_INTERVAL_MS = 300000;  // Update climate data every 5 minutes
const CLIMATE_INFLUENCE_SCALE_FACTOR = 0.02;  // Maximum climate influence on optimization

/**
 * ClimatePattern class representing climate data observation
 */
class ClimatePattern {
    constructor(timestamp, temperature, humidity, pressure, reliability = 1.0) {
        this.timestamp = timestamp;
        this.temperature = temperature;  // Normalized 0-1
        this.humidity = humidity;  // Normalized 0-1
        this.pressure = pressure;  // Normalized 0-1
        this.reliability = reliability;  // Data reliability score 0-1
    }

    isReliable() {
        return this.reliability >= CLIMATE_DATA_RELIABILITY_THRESHOLD;
    }
}

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
        this.climatePatterns = [];
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

    addClimatePattern(pattern) {
        this.climatePatterns.push(pattern);
        // Keep only recent history
        if (this.climatePatterns.length > CLIMATE_PATTERN_HISTORY) {
            this.climatePatterns = this.climatePatterns.slice(-CLIMATE_PATTERN_HISTORY);
        }
    }

    getReliableClimateData() {
        return this.climatePatterns.filter(p => p.isReliable());
    }

    predictClimateTrend() {
        const reliableData = this.getReliableClimateData();
        if (reliableData.length < 3) {
            return null;
        }

        // Use recent data for prediction (last 10 observations)
        const recent = reliableData.slice(-10);
        const temps = recent.map(p => p.temperature);
        const n = temps.length;

        // Calculate trend using simple linear regression
        const xMean = (n - 1) / 2;
        const yMean = temps.reduce((a, b) => a + b, 0) / n;

        let numerator = 0;
        let denominator = 0;
        for (let i = 0; i < n; i++) {
            numerator += (i - xMean) * (temps[i] - yMean);
            denominator += (i - xMean) * (i - xMean);
        }

        if (denominator === 0) {
            return 0.0;
        }

        const slope = numerator / denominator;
        // Normalize slope to -1 to 1 range
        return Math.max(-1.0, Math.min(1.0, slope * 10));
    }

    toJSON() {
        return {
            nodeId: this.nodeId,
            energyLevel: this.energyLevel,
            optimizationCount: this.optimizationCount,
            stillnessCount: this.stillnessCount,
            climateDataPoints: this.climatePatterns.length,
            reliableClimateDataPoints: this.getReliableClimateData().length
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
        this.climateMonitoringEnabled = true;
        this.lastClimateUpdate = this.startTime;

        // Initialize node network
        for (let i = 0; i < initialNodes; i++) {
            const nodeId = `node_${String(i).padStart(4, '0')}`;
            this.nodes.set(nodeId, new Node(nodeId));
        }

        this.log(`Initialized with ${this.nodes.size} nodes`);
        this.log(`Base frequency: ${UNIVERSAL_RESONANCE_HZ} Hz`);
        this.log(`Cycle period: ${(CYCLE_PERIOD_MS / 1000).toFixed(2)} seconds`);
        this.log(`Climate pattern monitoring: ${this.climateMonitoringEnabled ? 'ENABLED' : 'DISABLED'}`, 'NSR');
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

        // Integrate climate pattern influence (NSR enhancement)
        const climateFactor = this.calculateClimateInfluence();

        return feedback + resonanceFactor + climateFactor;
    }

    generateClimatePattern(currentTime = Date.now()) {
        const phase = this.calculateResonancePhase(currentTime);

        // Simulate climate patterns synchronized with resonance
        const tempCycle = Math.sin(phase / 10) * 0.3 + 0.5;
        const humidityCycle = Math.cos(phase / 5) * 0.25 + 0.5;
        const pressureCycle = Math.sin(phase) * 0.2 + 0.5;

        // Calculate reliability based on data freshness and resonance alignment
        const reliability = 0.85 + Math.abs(Math.sin(phase)) * 0.15;

        return new ClimatePattern(
            currentTime,
            Math.max(0.0, Math.min(1.0, tempCycle)),
            Math.max(0.0, Math.min(1.0, humidityCycle)),
            Math.max(0.0, Math.min(1.0, pressureCycle)),
            reliability
        );
    }

    updateClimatePatterns() {
        if (!this.climateMonitoringEnabled) return;

        const currentTime = Date.now();

        // Update climate data every 5 minutes
        if (currentTime - this.lastClimateUpdate < CLIMATE_UPDATE_INTERVAL_MS) return;

        // Generate new climate pattern
        const pattern = this.generateClimatePattern(currentTime);

        // Distribute to all nodes (network-wide intelligence)
        for (const node of this.nodes.values()) {
            node.addClimatePattern(pattern);
        }

        this.lastClimateUpdate = currentTime;

        // Log climate update
        if (pattern.isReliable()) {
            this.log(
                `Pattern updated - Temp: ${pattern.temperature.toFixed(3)}, ` +
                `Humidity: ${pattern.humidity.toFixed(3)}, ` +
                `Reliability: ${pattern.reliability.toFixed(3)}`,
                'CLIMATE'
            );
        }
    }

    calculateClimateInfluence() {
        if (this.nodes.size === 0) return 0.0;

        // Collect predictions from nodes with sufficient data
        const predictions = [];
        for (const node of this.nodes.values()) {
            const trend = node.predictClimateTrend();
            if (trend !== null) {
                predictions.push(trend);
            }
        }

        if (predictions.length === 0) return 0.0;

        // Average prediction as climate influence
        const avgPrediction = predictions.reduce((a, b) => a + b, 0) / predictions.length;

        // Scale to smaller influence factor
        return avgPrediction * CLIMATE_INFLUENCE_SCALE_FACTOR;
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

        // Update climate patterns (NSR: ensure data is current and reliable)
        this.updateClimatePatterns();

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

        // Calculate climate metrics
        let climateDataCount = 0;
        for (const node of this.nodes.values()) {
            climateDataCount += node.getReliableClimateData().length;
        }

        const metrics = {
            cycle: this.cycleCount,
            timestamp: new Date().toISOString(),
            phase: phase,
            phaseDegrees: (phase * 180 / Math.PI),
            nodes: this.nodes.size,
            avgEnergy: avgEnergy,
            inStillness: this.isInStillness,
            cycleDuration: cycleDuration,
            resonanceHz: UNIVERSAL_RESONANCE_HZ,
            climateDataPoints: climateDataCount,
            climateMonitoring: this.climateMonitoringEnabled
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
        let totalClimateData = 0;
        let reliableClimateData = 0;

        for (const node of this.nodes.values()) {
            totalEnergy += node.energyLevel;
            totalOptimizations += node.optimizationCount;
            totalStillness += node.stillnessCount;
            totalClimateData += node.climatePatterns.length;
            reliableClimateData += node.getReliableClimateData().length;
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
            totalStillnessEvents: totalStillness,
            climateMonitoring: this.climateMonitoringEnabled,
            climateDataTotal: totalClimateData,
            climateDataReliable: reliableClimateData,
            climateReliabilityRatio: reliableClimateData / Math.max(1, totalClimateData)
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
        ClimatePattern,
        UNIVERSAL_RESONANCE_HZ,
        CYCLE_PERIOD_MS,
        SCHUMANN_RESONANCE_HZ,
        HARMONIC_432_HZ,
        PHI,
        SACRED_HISTORY_LIMIT,
        MAX_OPTIMIZATION_METRICS,
        STILLNESS_DURATION_CAP_MS,
        CLIMATE_PATTERN_HISTORY,
        CLIMATE_DATA_RELIABILITY_THRESHOLD,
        CLIMATE_UPDATE_INTERVAL_MS,
        CLIMATE_INFLUENCE_SCALE_FACTOR
    };
}

// Browser global
if (typeof window !== 'undefined') {
    window.EternalDepositionEngine = EternalDepositionEngine;
    window.EternalDeposition = {
        EternalDepositionEngine,
        Node,
        ClimatePattern,
        UNIVERSAL_RESONANCE_HZ,
        CYCLE_PERIOD_MS,
        SCHUMANN_RESONANCE_HZ,
        HARMONIC_432_HZ,
        PHI,
        CLIMATE_PATTERN_HISTORY,
        CLIMATE_DATA_RELIABILITY_THRESHOLD,
        CLIMATE_UPDATE_INTERVAL_MS,
        CLIMATE_INFLUENCE_SCALE_FACTOR
    };
}
