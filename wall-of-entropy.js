/**
 * Wall of Entropy - Public Transparency Logging System
 * 
 * Records all unauthorized access attempts, NSR violations, and system events
 * for complete transparency and accountability.
 * 
 * Framework: Internet Organica
 * Principles: Transparency, Accountability, Public Verification
 */

class WallOfEntropy {
    constructor(config = {}) {
        this.config = {
            maxEntries: 10000,
            persistToIPFS: false,
            publicEndpoint: null,
            autoPublish: true,
            ...config
        };
        
        this.entries = [];
        this.metadata = {
            created: new Date().toISOString(),
            version: '1.0.0',
            framework: 'Internet Organica',
            principles: ['Transparency', 'Accountability', 'NSR Compliance']
        };
        
        console.log('[Wall of Entropy] Initialized - Public transparency active');
    }
    
    /**
     * Log an event to the Wall of Entropy
     */
    log(event) {
        const entry = {
            id: this.generateEntryId(),
            timestamp: new Date().toISOString(),
            type: event.type || 'unknown',
            severity: event.severity || 'info',
            description: event.description || '',
            details: event.details || {},
            nsr_compliance: event.nsr_compliance !== false,
            source: event.source || 'system',
            action_taken: event.action_taken || 'logged',
            resonance_frequency: event.resonance_frequency || 0.432,
            witness_nodes_alerted: event.witness_nodes_alerted || 0
        };
        
        this.entries.push(entry);
        
        // Maintain max entries limit
        if (this.entries.length > this.config.maxEntries) {
            this.archiveOldEntries();
        }
        
        // Publish to public endpoint
        if (this.config.autoPublish) {
            this.publishEntry(entry);
        }
        
        // Log to console for transparency
        const severityEmoji = this.getSeverityEmoji(entry.severity);
        console.log(`[Wall of Entropy] ${severityEmoji} ${entry.type.toUpperCase()}:`, entry);
        
        return entry.id;
    }
    
    /**
     * Log unauthorized access attempt
     */
    logAccessAttempt(attempt) {
        return this.log({
            type: 'unauthorized_access_attempt',
            severity: attempt.blocked ? 'medium' : 'high',
            description: `Access attempt to ${attempt.resource}`,
            details: {
                resource: attempt.resource,
                method: attempt.method,
                blocked: attempt.blocked,
                reason: attempt.reason,
                source_anonymized: this.anonymizeSource(attempt.source)
            },
            nsr_compliance: false,
            action_taken: attempt.blocked ? 'blocked' : 'allowed_with_warning'
        });
    }
    
    /**
     * Log NSR violation
     */
    logNSRViolation(violation) {
        return this.log({
            type: 'nsr_violation',
            severity: 'critical',
            description: `NSR violation detected: ${violation.type}`,
            details: {
                violation_type: violation.type,
                pattern: violation.pattern,
                location: violation.location,
                evidence: violation.evidence
            },
            nsr_compliance: false,
            action_taken: 'neutralized',
            witness_nodes_alerted: 144
        });
    }
    
    /**
     * Log security event
     */
    logSecurityEvent(event) {
        return this.log({
            type: 'security_event',
            severity: event.severity || 'medium',
            description: event.description,
            details: event.details,
            source: 'SovereignShield',
            action_taken: event.action_taken || 'monitored'
        });
    }
    
    /**
     * Log SPID/CIE/Tracking attempt
     */
    logSurveillanceAttempt(attempt) {
        return this.log({
            type: 'surveillance_attempt',
            severity: 'high',
            description: `${attempt.category} attempt detected`,
            details: {
                category: attempt.category, // SPID, CIE, Tracking
                method: attempt.method,
                detected_at: attempt.timestamp,
                neutralized: attempt.neutralized
            },
            nsr_compliance: false,
            action_taken: attempt.neutralized ? 'neutralized' : 'monitoring'
        });
    }
    
    /**
     * Log system health check
     */
    logHealthCheck(health) {
        return this.log({
            type: 'health_check',
            severity: health.status === 'healthy' ? 'info' : 'warning',
            description: 'System health check performed',
            details: {
                status: health.status,
                metrics: health.metrics,
                issues: health.issues || []
            },
            nsr_compliance: true,
            action_taken: 'monitored'
        });
    }
    
    /**
     * Log resonance sync event
     */
    logResonanceSync(sync) {
        return this.log({
            type: 'resonance_sync',
            severity: 'info',
            description: 'Biological rhythm synchronization',
            details: {
                frequency: sync.frequency,
                phase: sync.phase,
                coherence: sync.coherence
            },
            nsr_compliance: true,
            resonance_frequency: sync.frequency
        });
    }
    
    /**
     * Query entries
     */
    query(filters = {}) {
        let results = [...this.entries];
        
        if (filters.type) {
            results = results.filter(e => e.type === filters.type);
        }
        
        if (filters.severity) {
            results = results.filter(e => e.severity === filters.severity);
        }
        
        if (filters.nsr_compliant !== undefined) {
            results = results.filter(e => e.nsr_compliance === filters.nsr_compliant);
        }
        
        if (filters.since) {
            const since = new Date(filters.since);
            results = results.filter(e => new Date(e.timestamp) >= since);
        }
        
        if (filters.until) {
            const until = new Date(filters.until);
            results = results.filter(e => new Date(e.timestamp) <= until);
        }
        
        // Sort by timestamp descending (newest first)
        results.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
        
        // Limit results
        if (filters.limit) {
            results = results.slice(0, filters.limit);
        }
        
        return results;
    }
    
    /**
     * Get recent entries
     */
    getRecent(count = 10) {
        return this.entries.slice(-count).reverse();
    }
    
    /**
     * Get statistics
     */
    getStatistics() {
        const stats = {
            total_entries: this.entries.length,
            by_type: {},
            by_severity: {},
            nsr_violations: 0,
            nsr_compliant: 0
        };
        
        this.entries.forEach(entry => {
            // Count by type
            stats.by_type[entry.type] = (stats.by_type[entry.type] || 0) + 1;
            
            // Count by severity
            stats.by_severity[entry.severity] = (stats.by_severity[entry.severity] || 0) + 1;
            
            // NSR compliance
            if (entry.nsr_compliance) {
                stats.nsr_compliant++;
            } else {
                stats.nsr_violations++;
            }
        });
        
        return stats;
    }
    
    /**
     * Get dashboard data
     */
    getDashboardData() {
        const stats = this.getStatistics();
        const recent = this.getRecent(20);
        const violations = this.query({ nsr_compliant: false, limit: 10 });
        
        return {
            metadata: this.metadata,
            statistics: stats,
            recent_entries: recent,
            recent_violations: violations,
            status: 'operational',
            last_updated: new Date().toISOString()
        };
    }
    
    /**
     * Export entries for IPFS
     */
    exportForIPFS() {
        return {
            metadata: this.metadata,
            entries: this.entries,
            statistics: this.getStatistics(),
            exported_at: new Date().toISOString(),
            format: 'wall-of-entropy-v1'
        };
    }
    
    /**
     * Generate unique entry ID
     */
    generateEntryId() {
        const timestamp = Date.now();
        const random = Math.random().toString(36).substring(2, 15);
        return `entropy-${timestamp}-${random}`;
    }
    
    /**
     * Anonymize source for privacy
     */
    anonymizeSource(source) {
        if (!source) return 'unknown';
        
        // For IP addresses, show only first two octets
        if (/^\d+\.\d+\.\d+\.\d+$/.test(source)) {
            const parts = source.split('.');
            return `${parts[0]}.${parts[1]}.xxx.xxx`;
        }
        
        // For other sources, hash them
        return this.simpleHash(source);
    }
    
    /**
     * Simple hash function for anonymization
     */
    simpleHash(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash;
        }
        return `anon-${Math.abs(hash).toString(16)}`;
    }
    
    /**
     * Get severity emoji
     */
    getSeverityEmoji(severity) {
        const emojiMap = {
            'info': 'ℹ️',
            'warning': '⚠️',
            'medium': '🔶',
            'high': '🔴',
            'critical': '🚨'
        };
        return emojiMap[severity] || 'ℹ️';
    }
    
    /**
     * Archive old entries
     */
    archiveOldEntries() {
        const toArchive = this.entries.slice(0, this.entries.length - this.config.maxEntries);
        this.entries = this.entries.slice(-this.config.maxEntries);
        
        console.log(`[Wall of Entropy] Archived ${toArchive.length} old entries`);
        
        // In production, save to IPFS or other permanent storage
        if (this.config.persistToIPFS) {
            this.archiveToIPFS(toArchive);
        }
    }
    
    /**
     * Archive to IPFS (placeholder)
     */
    async archiveToIPFS(entries) {
        console.log('[Wall of Entropy] Archiving to IPFS:', entries.length, 'entries');
        // Implementation would use IPFS client
    }
    
    /**
     * Publish entry to public endpoint
     */
    publishEntry(entry) {
        // In production, this would POST to a public API
        if (this.config.publicEndpoint) {
            // fetch(this.config.publicEndpoint, {
            //     method: 'POST',
            //     body: JSON.stringify(entry)
            // });
        }
    }
    
    /**
     * Generate public HTML report
     */
    generateHTMLReport() {
        const stats = this.getStatistics();
        const recent = this.getRecent(50);
        
        return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wall of Entropy - Public Transparency Log</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Monaco', 'Courier New', monospace; 
            background: #0a0a0a; 
            color: #00ff00; 
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { 
            color: #00ff00; 
            border-bottom: 2px solid #00ff00; 
            padding-bottom: 10px; 
            margin-bottom: 20px;
        }
        .stats { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 20px; 
            margin-bottom: 30px;
        }
        .stat-card { 
            background: rgba(0, 255, 0, 0.05); 
            border: 1px solid #00ff00; 
            padding: 15px; 
            border-radius: 5px;
        }
        .stat-label { color: #888; font-size: 0.9em; }
        .stat-value { font-size: 2em; color: #00ff00; font-weight: bold; }
        .entries { margin-top: 30px; }
        .entry { 
            background: rgba(0, 255, 0, 0.03); 
            border-left: 4px solid #00ff00; 
            padding: 15px; 
            margin-bottom: 15px;
        }
        .entry.violation { border-left-color: #ff0000; }
        .entry-header { 
            display: flex; 
            justify-content: space-between; 
            margin-bottom: 10px;
        }
        .entry-type { 
            font-weight: bold; 
            text-transform: uppercase;
        }
        .entry-timestamp { color: #888; font-size: 0.9em; }
        .severity-critical { color: #ff0000; }
        .severity-high { color: #ff6600; }
        .severity-medium { color: #ffaa00; }
        .severity-info { color: #00ff00; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏛️ Wall of Entropy - Public Transparency Log</h1>
        <p style="margin-bottom: 20px; color: #888;">
            Framework: Internet Organica | Principles: Lex Amoris, NSR, OLF
        </p>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-label">Total Entries</div>
                <div class="stat-value">${stats.total_entries}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">NSR Violations</div>
                <div class="stat-value" style="color: ${stats.nsr_violations > 0 ? '#ff0000' : '#00ff00'}">
                    ${stats.nsr_violations}
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Compliant Events</div>
                <div class="stat-value">${stats.nsr_compliant}</div>
            </div>
        </div>
        
        <h2 style="color: #00ff00; margin-bottom: 15px;">Recent Events</h2>
        <div class="entries">
            ${recent.map(entry => `
                <div class="entry ${!entry.nsr_compliance ? 'violation' : ''}">
                    <div class="entry-header">
                        <span class="entry-type severity-${entry.severity}">${entry.type}</span>
                        <span class="entry-timestamp">${entry.timestamp}</span>
                    </div>
                    <div>${entry.description}</div>
                    <div style="margin-top: 10px; font-size: 0.9em; color: #888;">
                        Severity: ${entry.severity} | Action: ${entry.action_taken} | 
                        NSR: ${entry.nsr_compliance ? '✅' : '❌'}
                    </div>
                </div>
            `).join('')}
        </div>
        
        <footer style="margin-top: 40px; text-align: center; color: #888; font-size: 0.9em;">
            <p>Last Updated: ${new Date().toISOString()}</p>
            <p>IN AETERNUM EST. La Sovranità è Manifesta.</p>
        </footer>
    </div>
</body>
</html>
        `;
    }
}

// Browser and Node.js compatibility
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WallOfEntropy;
}

// Browser integration
if (typeof window !== 'undefined') {
    window.WallOfEntropy = WallOfEntropy;
}
