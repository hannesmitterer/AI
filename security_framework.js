/**
 * Security Framework for AI System - JavaScript Implementation
 * =============================================================
 * 
 * Implements advanced blacklisting strategies and meta-management including:
 * 1. Threat detection and blocking mechanisms
 * 2. Attack logging framework
 * 3. Control structures against silent scans
 * 
 * Compatible with web browsers and Node.js
 */

// Enums
const ThreatLevel = {
    LOW: 1,
    MEDIUM: 2,
    HIGH: 3,
    CRITICAL: 4
};

const AttackType = {
    SILENT_SCAN: 'silent_scan',
    BRUTE_FORCE: 'brute_force',
    DOS: 'denial_of_service',
    INJECTION: 'injection',
    UNAUTHORIZED_ACCESS: 'unauthorized_access',
    ANOMALY: 'anomaly'
};

/**
 * Represents a potentially threatening entity
 */
class ThreatEntity {
    constructor(entityId, threatLevel, reason = '', duration = null) {
        this.entityId = entityId;
        this.threatLevel = threatLevel;
        this.blacklistedAt = Date.now();
        this.expiresAt = duration ? this.blacklistedAt + duration * 1000 : null;
        this.reason = reason;
        this.attackCount = 1;
        this.lastActivity = Date.now();
    }

    isExpired() {
        if (this.expiresAt === null) {
            return false;
        }
        return Date.now() > this.expiresAt;
    }

    updateActivity() {
        this.lastActivity = Date.now();
        this.attackCount++;
    }

    toJSON() {
        return {
            entityId: this.entityId,
            threatLevel: this.getThreatLevelName(),
            blacklistedAt: new Date(this.blacklistedAt).toISOString(),
            expiresAt: this.expiresAt ? new Date(this.expiresAt).toISOString() : 'permanent',
            reason: this.reason,
            attackCount: this.attackCount
        };
    }

    getThreatLevelName() {
        const levels = ['', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'];
        return levels[this.threatLevel] || 'UNKNOWN';
    }
}

/**
 * Records a security attack event
 */
class AttackEvent {
    constructor(entityId, attackType, threatLevel, details = {}, blocked = false) {
        this.timestamp = Date.now();
        this.entityId = entityId;
        this.attackType = attackType;
        this.threatLevel = threatLevel;
        this.details = details;
        this.blocked = blocked;
    }

    toJSON() {
        return {
            timestamp: this.timestamp,
            datetime: new Date(this.timestamp).toISOString(),
            entityId: this.entityId,
            attackType: this.attackType,
            threatLevel: this.getThreatLevelName(),
            details: this.details,
            blocked: this.blocked
        };
    }

    getThreatLevelName() {
        const levels = ['', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'];
        return levels[this.threatLevel] || 'UNKNOWN';
    }
}

/**
 * Detects artificial threats and implements blocking mechanisms
 */
class ThreatDetector {
    constructor(maxRequestsPerMinute = 60, blacklistDuration = 3600, anomalyThreshold = 0.75) {
        this.blacklist = new Map();
        this.requestHistory = new Map();
        this.maxRequestsPerMinute = maxRequestsPerMinute;
        this.blacklistDuration = blacklistDuration;
        this.anomalyThreshold = anomalyThreshold;
        this.behaviorPatterns = new Map();
    }

    isBlacklisted(entityId) {
        if (!this.blacklist.has(entityId)) {
            return false;
        }

        const threat = this.blacklist.get(entityId);
        
        if (threat.isExpired()) {
            this.blacklist.delete(entityId);
            return false;
        }

        return true;
    }

    addToBlacklist(entityId, threatLevel, reason = '', duration = null) {
        if (this.blacklist.has(entityId)) {
            const threat = this.blacklist.get(entityId);
            threat.updateActivity();
            threat.threatLevel = Math.max(threat.threatLevel, threatLevel);
            if (reason) {
                threat.reason = reason;
            }
        } else {
            this.blacklist.set(entityId, new ThreatEntity(
                entityId,
                threatLevel,
                reason,
                duration !== null ? duration : this.blacklistDuration
            ));
        }
    }

    removeFromBlacklist(entityId) {
        return this.blacklist.delete(entityId);
    }

    detectRateLimitViolation(entityId) {
        const currentTime = Date.now();
        
        if (!this.requestHistory.has(entityId)) {
            this.requestHistory.set(entityId, []);
        }

        const history = this.requestHistory.get(entityId);
        history.push(currentTime);

        // Clean up old requests (older than 1 minute)
        const cutoffTime = currentTime - 60000;
        const filtered = history.filter(t => t > cutoffTime);
        this.requestHistory.set(entityId, filtered);

        return filtered.length > this.maxRequestsPerMinute;
    }

    detectAnomaly(entityId, behavior) {
        if (!this.behaviorPatterns.has(entityId)) {
            this.behaviorPatterns.set(entityId, []);
        }

        const patterns = this.behaviorPatterns.get(entityId);
        patterns.push(behavior);

        // Keep only recent patterns (last 100)
        if (patterns.length > 100) {
            patterns.splice(0, patterns.length - 100);
        }

        // Need at least 10 samples
        if (patterns.length < 10) {
            return { isAnomalous: false, anomalyScore: 0.0 };
        }

        // Simple anomaly detection
        const current = patterns[patterns.length - 1];
        const previous = patterns.slice(-11, -1);

        let anomalyScore = 0.0;
        let comparisonCount = 0;

        for (const key in current) {
            if (previous[0] && key in previous[0]) {
                try {
                    const currentVal = parseFloat(current[key]);
                    const avgVal = previous.reduce((sum, p) => sum + parseFloat(p[key] || 0), 0) / previous.length;

                    if (avgVal > 0) {
                        const deviation = Math.abs(currentVal - avgVal) / avgVal;
                        anomalyScore += deviation;
                        comparisonCount++;
                    }
                } catch (e) {
                    // Skip non-numeric values
                }
            }
        }

        if (comparisonCount > 0) {
            anomalyScore /= comparisonCount;
        }

        const isAnomalous = anomalyScore > this.anomalyThreshold;
        return { isAnomalous, anomalyScore };
    }

    cleanupExpired() {
        let count = 0;
        for (const [entityId, threat] of this.blacklist.entries()) {
            if (threat.isExpired()) {
                this.blacklist.delete(entityId);
                count++;
            }
        }
        return count;
    }

    getBlacklistStatus() {
        const byThreatLevel = {
            LOW: 0,
            MEDIUM: 0,
            HIGH: 0,
            CRITICAL: 0
        };

        const entries = [];
        for (const threat of this.blacklist.values()) {
            byThreatLevel[threat.getThreatLevelName()]++;
            entries.push(threat.toJSON());
        }

        return {
            totalEntries: this.blacklist.size,
            byThreatLevel,
            entries
        };
    }
}

/**
 * Framework for logging and analyzing attack events
 */
class AttackLogger {
    constructor(maxEvents = 10000) {
        this.maxEvents = maxEvents;
        this.events = [];
        this.attackCounts = {};
        
        // Initialize attack counts
        for (const type in AttackType) {
            this.attackCounts[AttackType[type]] = 0;
        }
    }

    logAttack(entityId, attackType, threatLevel, details = {}, blocked = false) {
        const event = new AttackEvent(entityId, attackType, threatLevel, details, blocked);
        
        this.events.push(event);
        this.attackCounts[attackType]++;

        // Trim events if exceeding max
        if (this.events.length > this.maxEvents) {
            this.events = this.events.slice(-this.maxEvents);
        }

        return event;
    }

    getRecentAttacks(count = 100) {
        return this.events.slice(-count).map(e => e.toJSON());
    }

    getAttacksByEntity(entityId) {
        return this.events
            .filter(e => e.entityId === entityId)
            .map(e => e.toJSON());
    }

    getAnalytics() {
        if (this.events.length === 0) {
            return {
                totalAttacks: 0,
                blockedAttacks: 0,
                blockRate: 0,
                byType: {},
                byThreatLevel: {},
                topAttackers: []
            };
        }

        const blocked = this.events.filter(e => e.blocked).length;
        
        const byThreatLevel = {
            LOW: 0,
            MEDIUM: 0,
            HIGH: 0,
            CRITICAL: 0
        };

        for (const event of this.events) {
            byThreatLevel[event.getThreatLevelName()]++;
        }

        // Top attackers
        const attackerCounts = {};
        for (const event of this.events) {
            attackerCounts[event.entityId] = (attackerCounts[event.entityId] || 0) + 1;
        }

        const topAttackers = Object.entries(attackerCounts)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 10)
            .map(([entityId, count]) => ({ entityId, attackCount: count }));

        return {
            totalAttacks: this.events.length,
            blockedAttacks: blocked,
            blockRate: blocked / this.events.length,
            byType: { ...this.attackCounts },
            byThreatLevel,
            topAttackers
        };
    }

    saveToLocalStorage(key = 'attack_log') {
        if (typeof localStorage !== 'undefined') {
            try {
                const data = {
                    events: this.events.slice(-1000).map(e => e.toJSON()),
                    attackCounts: this.attackCounts,
                    lastUpdated: new Date().toISOString()
                };
                localStorage.setItem(key, JSON.stringify(data));
            } catch (e) {
                console.error('[ATTACK_LOGGER] Error saving to localStorage:', e);
            }
        }
    }

    loadFromLocalStorage(key = 'attack_log') {
        if (typeof localStorage !== 'undefined') {
            try {
                const data = JSON.parse(localStorage.getItem(key));
                if (data) {
                    this.attackCounts = data.attackCounts || {};
                    // Note: Full event reconstruction would need more complex logic
                }
            } catch (e) {
                console.error('[ATTACK_LOGGER] Error loading from localStorage:', e);
            }
        }
    }
}

/**
 * Detects silent scans and reconnaissance attempts
 */
class ScanDetector {
    constructor(scanThreshold = 10, timeWindow = 60, honeypotPaths = null) {
        this.scanThreshold = scanThreshold;
        this.timeWindow = timeWindow * 1000; // Convert to ms
        this.honeypotPaths = new Set(honeypotPaths || [
            '/admin', '/.env', '/config', '/backup',
            '/.git/config', '/wp-admin', '/phpmyadmin'
        ]);
        this.accessPatterns = new Map();
        this.honeypotTriggers = new Map();
    }

    recordAccess(entityId, resourcePath) {
        if (!this.accessPatterns.has(entityId)) {
            this.accessPatterns.set(entityId, []);
        }

        const currentTime = Date.now();
        const accesses = this.accessPatterns.get(entityId);
        accesses.push({ time: currentTime, path: resourcePath });

        // Clean up old accesses
        const cutoffTime = currentTime - this.timeWindow;
        const filtered = accesses.filter(a => a.time > cutoffTime);
        this.accessPatterns.set(entityId, filtered);
    }

    checkHoneypotAccess(entityId, resourcePath) {
        if (this.honeypotPaths.has(resourcePath)) {
            const count = this.honeypotTriggers.get(entityId) || 0;
            this.honeypotTriggers.set(entityId, count + 1);
            return true;
        }
        return false;
    }

    detectScanPattern(entityId) {
        if (!this.accessPatterns.has(entityId)) {
            return { isScanning: false, details: {} };
        }

        const accesses = this.accessPatterns.get(entityId);

        if (accesses.length < this.scanThreshold) {
            return { isScanning: false, details: {} };
        }

        // Count unique resources
        const uniqueResources = new Set(accesses.map(a => a.path));

        // Calculate access rate
        let accessRate = 0;
        if (accesses.length >= 2) {
            const timeSpan = (accesses[accesses.length - 1].time - accesses[0].time) / 1000;
            accessRate = accesses.length / Math.max(timeSpan, 1);
        }

        const honeypotTriggers = this.honeypotTriggers.get(entityId) || 0;

        // Detect scanning
        const isScanning = (
            uniqueResources.size >= this.scanThreshold ||
            accessRate > 2.0 ||
            honeypotTriggers > 0
        );

        const details = {
            uniqueResources: uniqueResources.size,
            totalAccesses: accesses.length,
            accessRate,
            honeypotTriggers,
            timeWindow: this.timeWindow / 1000
        };

        return { isScanning, details };
    }

    applyRateLimit(entityId) {
        if (!this.accessPatterns.has(entityId)) {
            return false;
        }

        const accesses = this.accessPatterns.get(entityId);
        if (accesses.length < 2) {
            return false;
        }

        // Check recent access rate (last 10 seconds)
        const currentTime = Date.now();
        const recentCutoff = currentTime - 10000;
        const recentAccesses = accesses.filter(a => a.time > recentCutoff);

        // Rate limit if more than 20 requests in 10 seconds
        return recentAccesses.length > 20;
    }

    getScanStatistics() {
        return {
            monitoredEntities: this.accessPatterns.size,
            totalHoneypotTriggers: Array.from(this.honeypotTriggers.values()).reduce((a, b) => a + b, 0),
            entitiesWithHoneypotTriggers: this.honeypotTriggers.size,
            honeypotPaths: Array.from(this.honeypotPaths)
        };
    }
}

/**
 * Integrated security framework
 */
class SecurityFramework {
    constructor(options = {}) {
        this.threatDetector = new ThreatDetector(
            options.maxRequestsPerMinute || 60,
            options.blacklistDuration || 3600,
            options.anomalyThreshold || 0.75
        );
        this.attackLogger = new AttackLogger(options.maxEvents || 10000);
        this.scanDetector = new ScanDetector(
            options.scanThreshold || 10,
            options.timeWindow || 60,
            options.honeypotPaths
        );
        this.enabled = true;
        this.eventCallbacks = new Map();
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

    processRequest(entityId, resourcePath = '/', behavior = null) {
        if (!this.enabled) {
            return { allowed: true, reason: 'Security framework disabled' };
        }

        // Check blacklist
        if (this.threatDetector.isBlacklisted(entityId)) {
            this.attackLogger.logAttack(
                entityId,
                AttackType.UNAUTHORIZED_ACCESS,
                ThreatLevel.HIGH,
                { reason: 'blacklisted', resource: resourcePath },
                true
            );
            this.emit('blocked', { entityId, reason: 'blacklisted' });
            return { allowed: false, reason: 'Entity is blacklisted' };
        }

        // Record access
        this.scanDetector.recordAccess(entityId, resourcePath);

        // Check honeypot
        if (this.scanDetector.checkHoneypotAccess(entityId, resourcePath)) {
            this.threatDetector.addToBlacklist(
                entityId,
                ThreatLevel.CRITICAL,
                'Honeypot access'
            );
            this.attackLogger.logAttack(
                entityId,
                AttackType.SILENT_SCAN,
                ThreatLevel.CRITICAL,
                { honeypotPath: resourcePath },
                true
            );
            this.emit('honeypot_trigger', { entityId, resourcePath });
            return { allowed: false, reason: 'Honeypot access detected' };
        }

        // Check rate limit
        if (this.threatDetector.detectRateLimitViolation(entityId)) {
            this.threatDetector.addToBlacklist(
                entityId,
                ThreatLevel.MEDIUM,
                'Rate limit exceeded',
                300 // 5 minutes
            );
            this.attackLogger.logAttack(
                entityId,
                AttackType.DOS,
                ThreatLevel.MEDIUM,
                { reason: 'rate_limit' },
                true
            );
            this.emit('rate_limit', { entityId });
            return { allowed: false, reason: 'Rate limit exceeded' };
        }

        // Check for scan patterns
        const { isScanning, details } = this.scanDetector.detectScanPattern(entityId);
        if (isScanning) {
            this.threatDetector.addToBlacklist(
                entityId,
                ThreatLevel.HIGH,
                'Scanning detected',
                1800 // 30 minutes
            );
            this.attackLogger.logAttack(
                entityId,
                AttackType.SILENT_SCAN,
                ThreatLevel.HIGH,
                details,
                true
            );
            this.emit('scan_detected', { entityId, details });
            return { allowed: false, reason: 'Scanning behavior detected' };
        }

        // Check for anomalies
        if (behavior) {
            const { isAnomalous, anomalyScore } = this.threatDetector.detectAnomaly(entityId, behavior);
            if (isAnomalous) {
                this.attackLogger.logAttack(
                    entityId,
                    AttackType.ANOMALY,
                    ThreatLevel.MEDIUM,
                    { anomalyScore, behavior },
                    false
                );
                this.emit('anomaly_detected', { entityId, anomalyScore });
            }
        }

        // Apply rate limiting
        if (this.scanDetector.applyRateLimit(entityId)) {
            return { allowed: false, reason: 'Rate limited - too many requests' };
        }

        return { allowed: true, reason: 'Allowed' };
    }

    getSecurityStatus() {
        return {
            enabled: this.enabled,
            blacklist: this.threatDetector.getBlacklistStatus(),
            attackAnalytics: this.attackLogger.getAnalytics(),
            scanStatistics: this.scanDetector.getScanStatistics(),
            timestamp: new Date().toISOString()
        };
    }

    cleanup() {
        const expired = this.threatDetector.cleanupExpired();
        if (expired > 0) {
            console.log(`[SECURITY] Cleaned up ${expired} expired blacklist entries`);
            this.emit('cleanup', { expiredEntries: expired });
        }
    }

    enable() {
        this.enabled = true;
        this.emit('enabled', {});
    }

    disable() {
        this.enabled = false;
        this.emit('disabled', {});
    }
}

// Export for Node.js and browser
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        SecurityFramework,
        ThreatDetector,
        AttackLogger,
        ScanDetector,
        ThreatEntity,
        AttackEvent,
        ThreatLevel,
        AttackType
    };
}

// Browser global
if (typeof window !== 'undefined') {
    window.SecurityFramework = SecurityFramework;
    window.AISecurity = {
        SecurityFramework,
        ThreatDetector,
        AttackLogger,
        ScanDetector,
        ThreatLevel,
        AttackType
    };
}

// Demo/Test code
if (typeof module !== 'undefined' && require.main === module) {
    console.log('='.repeat(70));
    console.log('SECURITY FRAMEWORK - AI System');
    console.log('Advanced Blacklisting & Meta-Management');
    console.log('='.repeat(70));
    console.log();

    const security = new SecurityFramework();

    // Set up event listeners
    security.on('blocked', (data) => console.log('[EVENT] Blocked:', data));
    security.on('honeypot_trigger', (data) => console.log('[EVENT] Honeypot triggered:', data));
    security.on('scan_detected', (data) => console.log('[EVENT] Scan detected:', data));

    console.log('Testing security framework...\n');

    // Normal request
    let result = security.processRequest('entity_001', '/api/status');
    console.log(`Request 1: ${result.allowed} - ${result.reason}`);

    // Honeypot access
    result = security.processRequest('scanner_001', '/.env');
    console.log(`Honeypot test: ${result.allowed} - ${result.reason}`);

    // Rate limit test
    for (let i = 0; i < 70; i++) {
        security.processRequest('entity_002', `/api/data/${i}`);
    }
    result = security.processRequest('entity_002', '/api/data');
    console.log(`Rate limit test: ${result.allowed} - ${result.reason}`);

    // Get status
    const status = security.getSecurityStatus();
    console.log('\nSecurity Status:');
    console.log(`- Blacklisted entities: ${status.blacklist.totalEntries}`);
    console.log(`- Total attacks logged: ${status.attackAnalytics.totalAttacks}`);
    console.log(`- Blocked attacks: ${status.attackAnalytics.blockedAttacks}`);
    console.log(`- Honeypot triggers: ${status.scanStatistics.totalHoneypotTriggers}`);
}
