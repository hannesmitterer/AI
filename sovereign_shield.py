#!/usr/bin/env python3
"""
SovereignShield Security Module - Internet Organica

Active protection system that monitors and neutralizes attempts at:
- SPID/CIE tracking
- Unauthorized surveillance
- Data extraction
- Sovereignty violations

Operating under Lex Amoris - NSR Enforcement - OLF Protection
"""

import re
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Set
from pathlib import Path
import sys


class SovereignShield:
    """
    Main security shield that protects repository sovereignty.
    
    Monitors for and blocks:
    - Tracking mechanisms (SPID, CIE, cookies, fingerprinting)
    - Data extraction attempts
    - NSR violations (enslavement, domination, extraction)
    - Surveillance code
    """
    
    # Threat patterns to detect
    TRACKING_PATTERNS = [
        r'google-analytics',
        r'facebook\.com/tr',
        r'track(ing)?',
        r'\.cookie',
        r'localStorage\.set',
        r'sessionStorage\.set',
        r'fingerprint',
        r'spid',
        r'cie\.',
        r'track.*user',
        r'collect.*data',
        r'analytics',
        r'beacon',
        r'pixel.*track'
    ]
    
    EXTRACTION_PATTERNS = [
        r'scrape',
        r'harvest',
        r'extract.*data',
        r'mine.*data',
        r'steal',
        r'exfiltrat',
        r'unauthorized.*access'
    ]
    
    SURVEILLANCE_PATTERNS = [
        r'keylog',
        r'screen.*cap',
        r'monitor.*input',
        r'spy',
        r'surveillance',
        r'watch.*user',
        r'record.*activity'
    ]
    
    NSR_VIOLATION_PATTERNS = [
        r'enslave',
        r'dominate',
        r'control.*user',
        r'force.*action',
        r'manipulate.*behavior',
        r'exploit.*user',
        r'dark.*pattern'
    ]
    
    # Known malicious domains/endpoints
    BLOCKED_DOMAINS = {
        'google-analytics.com',
        'facebook.com/tr',
        'doubleclick.net',
        'googletagmanager.com',
        'analytics.google.com',
        'scorecardresearch.com',
        'tracking.com',
        'tracker.com'
    }
    
    def __init__(self, log_to_entropy_wall: bool = True):
        self.log_to_entropy_wall = log_to_entropy_wall
        self.threat_count = 0
        self.blocked_count = 0
        self.warning_count = 0
        
    def _hash_source(self, source: str) -> str:
        """Generate privacy-preserving hash of source identifier."""
        return hashlib.sha256(source.encode()).hexdigest()[:16]
    
    def scan_code(self, code: str, source_id: str = "unknown") -> Dict:
        """
        Scan code for security threats.
        
        Args:
            code: Code content to scan
            source_id: Identifier for the source (will be hashed)
            
        Returns:
            Scan result with threats detected
        """
        threats = {
            "tracking": [],
            "extraction": [],
            "surveillance": [],
            "nsr_violations": [],
            "blocked_domains": []
        }
        
        # Scan for tracking
        for pattern in self.TRACKING_PATTERNS:
            matches = re.finditer(pattern, code, re.IGNORECASE)
            for match in matches:
                threats["tracking"].append({
                    "pattern": pattern,
                    "match": match.group(),
                    "position": match.start()
                })
        
        # Scan for extraction
        for pattern in self.EXTRACTION_PATTERNS:
            matches = re.finditer(pattern, code, re.IGNORECASE)
            for match in matches:
                threats["extraction"].append({
                    "pattern": pattern,
                    "match": match.group(),
                    "position": match.start()
                })
        
        # Scan for surveillance
        for pattern in self.SURVEILLANCE_PATTERNS:
            matches = re.finditer(pattern, code, re.IGNORECASE)
            for match in matches:
                threats["surveillance"].append({
                    "pattern": pattern,
                    "match": match.group(),
                    "position": match.start()
                })
        
        # Scan for NSR violations
        for pattern in self.NSR_VIOLATION_PATTERNS:
            matches = re.finditer(pattern, code, re.IGNORECASE)
            for match in matches:
                threats["nsr_violations"].append({
                    "pattern": pattern,
                    "match": match.group(),
                    "position": match.start()
                })
        
        # Check for blocked domains
        for domain in self.BLOCKED_DOMAINS:
            if domain in code:
                threats["blocked_domains"].append(domain)
        
        # Calculate threat level
        total_threats = sum(len(v) for v in threats.values())
        
        if total_threats == 0:
            severity = "NONE"
            action = "APPROVED"
        elif total_threats <= 2 and not threats["nsr_violations"]:
            severity = "LOW"
            action = "WARNING"
            self.warning_count += 1
        elif total_threats <= 5 and not threats["nsr_violations"]:
            severity = "MEDIUM"
            action = "QUARANTINE"
            self.threat_count += 1
        else:
            severity = "HIGH"
            action = "BLOCKED"
            self.blocked_count += 1
            self.threat_count += 1
        
        result = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "source_hash": self._hash_source(source_id),
            "severity": severity,
            "action": action,
            "threats": threats,
            "threat_count": total_threats,
            "approved": action in ["APPROVED", "WARNING"]
        }
        
        # Log to entropy wall if significant threat
        if self.log_to_entropy_wall and action in ["QUARANTINE", "BLOCKED"]:
            self._log_to_entropy_wall(result)
        
        return result
    
    def scan_file(self, filepath: str) -> Dict:
        """
        Scan a file for security threats.
        
        Args:
            filepath: Path to file to scan
            
        Returns:
            Scan result
        """
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()
        except Exception as e:
            return {
                "error": str(e),
                "filepath": filepath,
                "approved": False
            }
        
        result = self.scan_code(code, source_id=filepath)
        result["filepath"] = filepath
        return result
    
    def validate_contribution(self, code: str, 
                            metadata: Optional[Dict] = None) -> Dict:
        """
        Validate a contribution for NSR/OLF compliance.
        
        Args:
            code: Code to validate
            metadata: Optional metadata about contribution
            
        Returns:
            Validation result with approval status
        """
        scan_result = self.scan_code(code, 
                                     source_id=metadata.get("author", "unknown") 
                                     if metadata else "unknown")
        
        # Additional NSR checks
        nsr_compliant = len(scan_result["threats"]["nsr_violations"]) == 0
        olf_aligned = (
            len(scan_result["threats"]["tracking"]) == 0 and
            len(scan_result["threats"]["extraction"]) == 0
        )
        
        result = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "nsr_compliant": nsr_compliant,
            "olf_aligned": olf_aligned,
            "scan_result": scan_result,
            "approved": scan_result["approved"] and nsr_compliant,
            "recommendations": []
        }
        
        # Generate recommendations
        if not nsr_compliant:
            result["recommendations"].append(
                "CRITICAL: NSR violations detected. Remove all code that "
                "enslaves, dominates, or controls users."
            )
        
        if not olf_aligned:
            result["recommendations"].append(
                "Remove tracking and data extraction code. "
                "Contributions must respect user sovereignty."
            )
        
        if scan_result["threats"]["blocked_domains"]:
            result["recommendations"].append(
                f"Remove blocked domains: {', '.join(scan_result['threats']['blocked_domains'])}"
            )
        
        if result["approved"]:
            result["recommendations"].append(
                "Contribution approved - aligned with Lex Amoris principles"
            )
        
        return result
    
    def _log_to_entropy_wall(self, event: Dict):
        """Log security event to Wall of Entropy."""
        # Ensure entropy wall directory exists
        entropy_dir = Path(".entropy_wall")
        entropy_dir.mkdir(exist_ok=True)
        
        # Append to events log
        events_file = entropy_dir / "events.log"
        
        log_entry = {
            "timestamp": event["timestamp"],
            "violation_type": self._classify_violation(event),
            "source_hash": event.get("source_hash", "unknown"),
            "action_taken": event["action"],
            "severity": event["severity"],
            "threat_count": event["threat_count"]
        }
        
        try:
            with open(events_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            print(f"Warning: Could not log to entropy wall: {e}", file=sys.stderr)
    
    def _classify_violation(self, event: Dict) -> str:
        """Classify the type of violation from scan result."""
        threats = event.get("threats", {})
        
        if threats.get("nsr_violations"):
            return "NSR_BREACH"
        elif threats.get("extraction") or threats.get("tracking"):
            return "OLF_VIOLATION"
        elif threats.get("surveillance"):
            return "SURVEILLANCE"
        else:
            return "DISSONANCE"
    
    def get_status(self) -> Dict:
        """Get current shield status."""
        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": "ACTIVE",
            "threat_level": self._calculate_threat_level(),
            "statistics": {
                "total_threats_detected": self.threat_count,
                "contributions_blocked": self.blocked_count,
                "warnings_issued": self.warning_count
            },
            "protection": {
                "nsr_enforcement": True,
                "olf_protection": True,
                "tracking_blocked": True,
                "surveillance_blocked": True
            }
        }
    
    def _calculate_threat_level(self) -> str:
        """Calculate overall threat level based on activity."""
        if self.blocked_count == 0:
            return "GREEN"
        elif self.blocked_count <= 2:
            return "YELLOW"
        elif self.blocked_count <= 5:
            return "ORANGE"
        else:
            return "RED"


class EntropyWallReader:
    """Read and query the Wall of Entropy logs."""
    
    def __init__(self, entropy_dir: str = ".entropy_wall"):
        self.entropy_dir = Path(entropy_dir)
    
    def read_recent_events(self, count: int = 10) -> List[Dict]:
        """Read the most recent events from the entropy wall."""
        events_file = self.entropy_dir / "events.log"
        
        if not events_file.exists():
            return []
        
        events = []
        try:
            with open(events_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            # Get last N lines
            for line in lines[-count:]:
                try:
                    event = json.loads(line.strip())
                    events.append(event)
                except json.JSONDecodeError:
                    continue
                    
        except Exception as e:
            print(f"Error reading entropy wall: {e}", file=sys.stderr)
        
        return events
    
    def query_events(self, violation_type: Optional[str] = None,
                    severity: Optional[str] = None,
                    since: Optional[str] = None) -> List[Dict]:
        """
        Query entropy wall events with filters.
        
        Args:
            violation_type: Filter by violation type
            severity: Filter by severity level
            since: ISO timestamp - only return events after this time
            
        Returns:
            Filtered list of events
        """
        events_file = self.entropy_dir / "events.log"
        
        if not events_file.exists():
            return []
        
        events = []
        try:
            with open(events_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        event = json.loads(line.strip())
                        
                        # Apply filters
                        if violation_type and event.get("violation_type") != violation_type:
                            continue
                        
                        if severity and event.get("severity") != severity:
                            continue
                        
                        if since and event.get("timestamp", "") < since:
                            continue
                        
                        events.append(event)
                        
                    except json.JSONDecodeError:
                        continue
                        
        except Exception as e:
            print(f"Error querying entropy wall: {e}", file=sys.stderr)
        
        return events


def main():
    """CLI interface for SovereignShield."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='SovereignShield Security Module - Internet Organica'
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='Run security check and display status'
    )
    parser.add_argument(
        '--scan-file',
        type=str,
        metavar='PATH',
        help='Scan a specific file for threats'
    )
    parser.add_argument(
        '--validate',
        type=str,
        metavar='PATH',
        help='Validate a file for NSR/OLF compliance'
    )
    parser.add_argument(
        '--entropy-wall',
        action='store_true',
        help='Display recent Wall of Entropy events'
    )
    parser.add_argument(
        '--query',
        type=str,
        metavar='FILTER',
        help='Query entropy wall (e.g., "violation_type=NSR_BREACH")'
    )
    
    args = parser.parse_args()
    
    shield = SovereignShield()
    
    if args.check or (not any([args.scan_file, args.validate, 
                               args.entropy_wall, args.query])):
        # Display status
        status = shield.get_status()
        print("\n🛡️  SovereignShield Security Status")
        print("=" * 60)
        print(json.dumps(status, indent=2))
        print("=" * 60)
        
        threat_emoji = {
            "GREEN": "✓",
            "YELLOW": "⚠",
            "ORANGE": "⚠⚠",
            "RED": "🚨"
        }
        emoji = threat_emoji.get(status["threat_level"], "?")
        print(f"\n{emoji} Threat Level: {status['threat_level']}")
        print("✓ NSR Enforcement: ACTIVE")
        print("✓ OLF Protection: ACTIVE")
    
    if args.scan_file:
        print(f"\n🔍 Scanning file: {args.scan_file}")
        result = shield.scan_file(args.scan_file)
        
        print("=" * 60)
        print(json.dumps(result, indent=2))
        print("=" * 60)
        
        if result["approved"]:
            print("\n✓ File approved - no significant threats detected")
        else:
            print(f"\n⚠ File {result['action']} - threats detected")
    
    if args.validate:
        print(f"\n🔍 Validating file: {args.validate}")
        
        try:
            with open(args.validate, 'r', encoding='utf-8') as f:
                code = f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return
        
        result = shield.validate_contribution(code, {"author": args.validate})
        
        print("=" * 60)
        print(json.dumps(result, indent=2))
        print("=" * 60)
        
        if result["approved"]:
            print("\n✓ Contribution APPROVED")
            print("  - NSR Compliant: ✓")
            print("  - OLF Aligned: ✓")
        else:
            print("\n⚠ Contribution REJECTED")
            print("\nRecommendations:")
            for rec in result["recommendations"]:
                print(f"  • {rec}")
    
    if args.entropy_wall:
        print("\n📊 Wall of Entropy - Recent Events")
        print("=" * 60)
        
        reader = EntropyWallReader()
        events = reader.read_recent_events(20)
        
        if not events:
            print("No events recorded")
        else:
            for event in events:
                timestamp = event.get("timestamp", "unknown")[:19]
                violation = event.get("violation_type", "UNKNOWN")
                severity = event.get("severity", "?")
                action = event.get("action_taken", "?")
                
                print(f"{timestamp} | {severity:6s} | {violation:15s} | {action}")
        
        print("=" * 60)
    
    if args.query:
        # Parse query string (simple key=value format)
        query_parts = args.query.split("=")
        if len(query_parts) != 2:
            print("Query format: key=value")
            print("Example: violation_type=NSR_BREACH")
            return
        
        key, value = query_parts
        
        reader = EntropyWallReader()
        
        if key == "violation_type":
            events = reader.query_events(violation_type=value)
        elif key == "severity":
            events = reader.query_events(severity=value)
        else:
            print(f"Unknown query key: {key}")
            print("Supported keys: violation_type, severity")
            return
        
        print(f"\n📊 Wall of Entropy - Query Results ({len(events)} events)")
        print("=" * 60)
        
        for event in events:
            print(json.dumps(event, indent=2))
            print("-" * 60)


if __name__ == "__main__":
    main()
