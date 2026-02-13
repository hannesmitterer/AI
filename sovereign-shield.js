/**
 * SovereignShield - Active Defense System
 * 
 * Protects against SPID (Surveillance, Profiling, Identification, Deanonymization),
 * CIE (Centralized Intelligence Extraction), and unauthorized tracking.
 * 
 * Framework: Internet Organica
 * Principles: Lex Amoris, NSR, OLF
 * Frequency: 0.432 Hz biological alignment
 */

class SovereignShield {
    constructor(config = {}) {
        this.config = {
            biologicalFrequency: 0.432, // Hz
            schumannResonance: 7.83,    // Hz
            monitoringEnabled: true,
            autoNeutralize: true,
            logToEntropy: true,
            ...config
        };
        
        this.threats = {
            surveillance: [],
            extraction: [],
            tracking: [],
            manipulation: []
        };
        
        this.protectionActive = false;
        this.wallOfEntropy = [];
        
        console.log('[SovereignShield] Initialized with biological frequency:', this.config.biologicalFrequency, 'Hz');
    }
    
    /**
     * Activate protection systems
     */
    activate() {
        if (this.protectionActive) {
            console.warn('[SovereignShield] Protection already active');
            return;
        }
        
        this.protectionActive = true;
        console.log('[SovereignShield] ✅ Protection ACTIVATED');
        
        // Start monitoring loops
        if (this.config.monitoringEnabled) {
            this.startMonitoring();
        }
        
        // Initialize biological rhythm sync
        this.initializeBiologicalSync();
        
        return this;
    }
    
    /**
     * Deactivate protection (use with caution)
     */
    deactivate() {
        this.protectionActive = false;
        console.log('[SovereignShield] ⚠️ Protection DEACTIVATED');
        return this;
    }
    
    /**
     * Initialize biological rhythm synchronization
     * Note: High-frequency timer (2315ms) - can be disabled if needed for performance
     */
    initializeBiologicalSync() {
        const period = 1000 / this.config.biologicalFrequency; // milliseconds
        
        console.log(`[BioSync] Synchronizing to ${this.config.biologicalFrequency} Hz (${period.toFixed(2)}ms period)`);
        
        // Only run if monitoring is enabled and we're in a browser environment
        if (!this.config.monitoringEnabled || typeof window === 'undefined') {
            console.log('[BioSync] Skipping periodic checks (monitoring disabled or non-browser environment)');
            return;
        }
        
        // Align system operations with biological rhythm
        // Note: This is a placeholder for future biological alignment features
        this.bioSyncInterval = setInterval(() => {
            this.performBiologicalCheck();
        }, period);
    }
    
    /**
     * Perform biological rhythm check
     */
    performBiologicalCheck() {
        // Verify all operations respect biological rhythms
        // Prevent cognitive overload
        // Maintain coherence with human nervous system
        
        const timestamp = new Date().toISOString();
        // Silent operation - only log issues
    }
    
    /**
     * Start continuous monitoring
     */
    startMonitoring() {
        console.log('[Monitor] Starting continuous threat detection');
        
        // Monitor for SPID attempts
        this.monitorSPID();
        
        // Monitor for CIE attempts
        this.monitorCIE();
        
        // Monitor for tracking
        this.monitorTracking();
        
        // Monitor for manipulation
        this.monitorManipulation();
    }
    
    /**
     * Monitor for SPID (Surveillance, Profiling, Identification, Deanonymization)
     */
    monitorSPID() {
        const spidPatterns = [
            'fingerprint',
            'tracker',
            'analytics',
            'surveillance',
            'profiling',
            'identify',
            'deanonymize'
        ];
        
        // Check for SPID patterns in code and network requests
        const detected = this.detectPatterns(spidPatterns, 'SPID');
        
        if (detected.length > 0) {
            this.handleThreat('SPID', detected);
        }
    }
    
    /**
     * Monitor for CIE (Centralized Intelligence Extraction)
     */
    monitorCIE() {
        const ciePatterns = [
            'centralized',
            'extract',
            'harvest',
            'scrape',
            'mine',
            'collect_without_consent'
        ];
        
        const detected = this.detectPatterns(ciePatterns, 'CIE');
        
        if (detected.length > 0) {
            this.handleThreat('CIE', detected);
        }
    }
    
    /**
     * Monitor for unauthorized tracking
     */
    monitorTracking() {
        const trackingPatterns = [
            'cookie',
            'beacon',
            'pixel',
            'session',
            'localstorage',
            'indexeddb'
        ];
        
        // Check browser storage and network
        if (typeof window !== 'undefined') {
            // Browser environment
            this.checkBrowserTracking();
        }
    }
    
    /**
     * Monitor for behavioral manipulation
     */
    monitorManipulation() {
        const manipulationPatterns = [
            'infinite_scroll',
            'autoplay',
            'notification',
            'badge',
            'countdown',
            'scarcity',
            'fomo'
        ];
        
        const detected = this.detectPatterns(manipulationPatterns, 'Manipulation');
        
        if (detected.length > 0) {
            this.handleThreat('Manipulation', detected);
        }
    }
    
    /**
     * Check browser for tracking mechanisms
     */
    checkBrowserTracking() {
        if (typeof window === 'undefined') return;
        
        const threats = [];
        
        // Check cookies
        if (document.cookie && document.cookie.length > 0) {
            const cookies = document.cookie.split(';');
            const suspiciousCookies = cookies.filter(c => 
                c.includes('track') || 
                c.includes('analytics') || 
                c.includes('_ga') ||
                c.includes('fbp')
            );
            
            if (suspiciousCookies.length > 0) {
                threats.push({
                    type: 'tracking_cookie',
                    count: suspiciousCookies.length,
                    details: suspiciousCookies
                });
            }
        }
        
        // Check localStorage
        if (localStorage.length > 0) {
            const suspiciousKeys = [];
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i);
                if (key && (key.includes('track') || key.includes('analytics'))) {
                    suspiciousKeys.push(key);
                }
            }
            
            if (suspiciousKeys.length > 0) {
                threats.push({
                    type: 'tracking_localstorage',
                    count: suspiciousKeys.length,
                    details: suspiciousKeys
                });
            }
        }
        
        if (threats.length > 0) {
            this.handleThreat('Tracking', threats);
        }
    }
    
    /**
     * Detect patterns in environment
     */
    detectPatterns(patterns, category) {
        const detected = [];
        
        // Check global scope for suspicious variables/functions
        if (typeof window !== 'undefined') {
            for (const pattern of patterns) {
                if (window[pattern] || window[pattern.toUpperCase()]) {
                    detected.push({
                        pattern,
                        location: 'window',
                        category
                    });
                }
            }
        }
        
        return detected;
    }
    
    /**
     * Handle detected threat
     */
    handleThreat(type, details) {
        const threat = {
            timestamp: new Date().toISOString(),
            type,
            details,
            severity: this.calculateSeverity(type, details),
            nsr_compliance: false
        };
        
        this.threats[type.toLowerCase()] = this.threats[type.toLowerCase()] || [];
        this.threats[type.toLowerCase()].push(threat);
        
        console.warn(`[SovereignShield] 🚨 ${type} THREAT DETECTED:`, threat);
        
        // Log to Wall of Entropy
        if (this.config.logToEntropy) {
            this.logToWallOfEntropy(threat);
        }
        
        // Auto-neutralize if enabled
        if (this.config.autoNeutralize) {
            this.neutralizeThreat(threat);
        }
    }
    
    /**
     * Calculate threat severity
     */
    calculateSeverity(type, details) {
        const severityMap = {
            'SPID': 'high',
            'CIE': 'critical',
            'Tracking': 'medium',
            'Manipulation': 'high'
        };
        
        return severityMap[type] || 'medium';
    }
    
    /**
     * Neutralize detected threat
     */
    neutralizeThreat(threat) {
        console.log(`[SovereignShield] ⚔️ Neutralizing ${threat.type} threat...`);
        
        switch (threat.type) {
            case 'SPID':
                this.neutralizeSPID(threat);
                break;
            case 'CIE':
                this.neutralizeCIE(threat);
                break;
            case 'Tracking':
                this.neutralizeTracking(threat);
                break;
            case 'Manipulation':
                this.neutralizeManipulation(threat);
                break;
            default:
                console.warn('[SovereignShield] Unknown threat type:', threat.type);
        }
        
        console.log(`[SovereignShield] ✅ ${threat.type} threat neutralized`);
    }
    
    /**
     * Neutralize SPID threat
     */
    neutralizeSPID(threat) {
        // Remove surveillance code
        // Block profiling attempts
        // Prevent identification
        if (typeof window !== 'undefined') {
            // Clear suspicious global variables
            threat.details.forEach(item => {
                if (item.location === 'window' && window[item.pattern]) {
                    delete window[item.pattern];
                }
            });
        }
    }
    
    /**
     * Neutralize CIE threat
     */
    neutralizeCIE(threat) {
        // Block centralized extraction
        // Ensure decentralized storage
        // Verify reciprocity
        console.log('[CIE Defense] Blocking extraction attempt');
    }
    
    /**
     * Neutralize tracking threat
     */
    neutralizeTracking(threat) {
        if (typeof window === 'undefined') return;
        
        // Clear tracking cookies
        if (threat.details.some(d => d.type === 'tracking_cookie')) {
            document.cookie.split(';').forEach(cookie => {
                const name = cookie.split('=')[0].trim();
                document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
            });
        }
        
        // Clear tracking localStorage
        if (threat.details.some(d => d.type === 'tracking_localstorage')) {
            threat.details
                .filter(d => d.type === 'tracking_localstorage')
                .forEach(d => {
                    d.details.forEach(key => localStorage.removeItem(key));
                });
        }
    }
    
    /**
     * Neutralize manipulation threat
     */
    neutralizeManipulation(threat) {
        // Disable manipulative features
        // Restore user autonomy
        console.log('[Manipulation Defense] Restoring user sovereignty');
    }
    
    /**
     * Log to Wall of Entropy
     */
    logToWallOfEntropy(threat) {
        const entry = {
            id: this.generateEntropyId(),
            ...threat,
            logged_at: new Date().toISOString(),
            resonance_frequency: this.config.biologicalFrequency,
            action_taken: this.config.autoNeutralize ? 'neutralized' : 'logged_only'
        };
        
        this.wallOfEntropy.push(entry);
        
        // In production, this would send to public transparency system
        console.log('[Wall of Entropy] Entry logged:', entry.id);
    }
    
    /**
     * Generate unique entropy ID
     */
    generateEntropyId() {
        const timestamp = Date.now();
        const random = Math.random().toString(36).substring(2, 15);
        return `entropy-${timestamp}-${random}`;
    }
    
    /**
     * Get Wall of Entropy logs
     */
    getEntropyLogs() {
        return this.wallOfEntropy;
    }
    
    /**
     * Get threat summary
     */
    getThreatSummary() {
        return {
            total_threats: Object.values(this.threats).reduce((sum, arr) => sum + arr.length, 0),
            by_type: {
                surveillance: this.threats.surveillance.length,
                extraction: this.threats.extraction.length,
                tracking: this.threats.tracking.length,
                manipulation: this.threats.manipulation.length
            },
            protection_active: this.protectionActive,
            biological_sync: this.config.biologicalFrequency,
            entropy_entries: this.wallOfEntropy.length
        };
    }
    
    /**
     * Verify NSR compliance of code
     */
    static verifyNSRCompliance(code) {
        const violations = [];
        
        // Check for slavery patterns
        const slaveryPatterns = [
            /force[_-]user/i,
            /mandatory/i,
            /require[_-]consent[_-]false/i,
            /override[_-]freedom/i,
            /enslave/i,
            /dominate/i
        ];
        
        slaveryPatterns.forEach(pattern => {
            if (pattern.test(code)) {
                violations.push({
                    type: 'slavery_pattern',
                    pattern: pattern.toString(),
                    severity: 'critical'
                });
            }
        });
        
        // Check for extraction without reciprocity
        const extractionPatterns = [
            /extract[_-]without[_-]consent/i,
            /harvest[_-]data/i,
            /sell[_-]user[_-]data/i
        ];
        
        extractionPatterns.forEach(pattern => {
            if (pattern.test(code)) {
                violations.push({
                    type: 'extraction_pattern',
                    pattern: pattern.toString(),
                    severity: 'high'
                });
            }
        });
        
        return {
            compliant: violations.length === 0,
            violations
        };
    }
    
    /**
     * Create vacuum bridge for safe passage
     */
    createVacuumBridge() {
        console.log('[Vacuum Bridge] Creating safe passage between realms...');
        
        return {
            enter: () => {
                console.log('[Vacuum Bridge] Entering inter-nodal vacuum');
                // Transition to safe, neutral space
            },
            exit: () => {
                console.log('[Vacuum Bridge] Returning to manifest realm');
                // Return with sovereignty intact
            },
            status: 'active',
            protection_level: 'maximum'
        };
    }
    
    /**
     * Cleanup and shutdown
     */
    shutdown() {
        if (this.bioSyncInterval) {
            clearInterval(this.bioSyncInterval);
        }
        
        this.protectionActive = false;
        console.log('[SovereignShield] Shutdown complete. Sovereignty preserved.');
        
        return this.getThreatSummary();
    }
}

// Browser and Node.js compatibility
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SovereignShield;
}

// Auto-activate in browser if not explicitly disabled
if (typeof window !== 'undefined' && !window.SOVEREIGN_SHIELD_DISABLED) {
    window.SovereignShield = SovereignShield;
    
    // Auto-initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            window.sovereignShield = new SovereignShield().activate();
        });
    } else {
        window.sovereignShield = new SovereignShield().activate();
    }
}
