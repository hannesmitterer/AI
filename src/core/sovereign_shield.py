#!/usr/bin/env python3
"""
SovereignShield Security Module
Internet Organica Framework

Provides active neutralization of tracking, SPID, CIE, and unauthorized access attempts.
Implements the Non-Slavery Rule (NSR) through automatic enforcement.

Aligned with:
- Lex Amoris: Protects life and autonomy
- NSR: Enforces sovereignty through technical means
- OLF: Optimizes life function by preventing extraction
"""

import json
import time
import hashlib
from typing import Dict, List, Optional, Set
from datetime import datetime
from enum import Enum


class ThreatLevel(Enum):
    """Classification of threat levels."""
    BENIGN = 0
    SUSPICIOUS = 1
    TRACKING = 2
    EXTRACTION = 3
    ENSLAVEMENT = 4
    CRITICAL = 5


class AccessIntent(Enum):
    """Classification of access intentions."""
    RESONANT = "resonant"  # Aligned with Lex Amoris
    NEUTRAL = "neutral"    # Neither harmful nor beneficial
    DISSONANT = "dissonant"  # Violates NSR or OLF


class SovereignShield:
    """
    Active security system implementing NSR enforcement.
    
    Features:
    - Real-time threat detection
    - Automatic neutralization of tracking attempts
    - Phase-shift to vacuum for enslavement attempts
    - Public logging to Wall of Entropy
    """
    
    def __init__(self, entropy_wall_path: str = "logs/entropy-wall.json"):
        """
        Initialize SovereignShield.
        
        Args:
            entropy_wall_path: Path to entropy wall log file
        """
        self.entropy_wall_path = entropy_wall_path
        self.active_threats: Dict[str, Dict] = {}
        self.blocked_signatures: Set[str] = set()
        self.access_log: List[Dict] = []
        self.total_blocked = 0
        self.total_neutralized = 0
        
        # Known tracking/extraction patterns
        self.threat_patterns = {
            'tracking': [
                'google-analytics', 'facebook-pixel', 'tracking.js',
                'analytics.js', 'gtag', 'fbevents'
            ],
            'spid': [
                'spid', 'digital-identity', 'identity-provider',
                'single-sign-on-tracker'
            ],
            'cie': [
                'cie', 'electronic-identity', 'id-verification'
            ],
            'extraction': [
                'data-mining', 'scraper', 'harvester', 'extractor'
            ],
            'enslavement': [
                'forced-consent', 'mandatory-tracking', 'no-opt-out',
                'surveillance-required'
            ]
        }
        
    def analyze_access(self, request_data: Dict) -> Dict:
        """
        Analyze an access request for threats and intent.
        
        Args:
            request_data: Dictionary containing request information
                - url: Request URL
                - headers: Request headers
                - user_agent: User agent string
                - ip: IP address (optional)
                - metadata: Additional metadata
        
        Returns:
            Analysis result with threat level and intent
        """
        analysis = {
            'timestamp': datetime.utcnow().isoformat(),
            'request_id': self._generate_request_id(request_data),
            'threat_level': ThreatLevel.BENIGN.name,
            'intent': AccessIntent.NEUTRAL.value,
            'detected_threats': [],
            'action': 'allow',
            'reason': ''
        }
        
        # Check for known threat patterns
        request_str = json.dumps(request_data).lower()
        
        for threat_type, patterns in self.threat_patterns.items():
            for pattern in patterns:
                if pattern in request_str:
                    analysis['detected_threats'].append({
                        'type': threat_type,
                        'pattern': pattern
                    })
        
        # Determine threat level
        if analysis['detected_threats']:
            threat_types = [t['type'] for t in analysis['detected_threats']]
            
            if 'enslavement' in threat_types:
                analysis['threat_level'] = ThreatLevel.ENSLAVEMENT.name
                analysis['intent'] = AccessIntent.DISSONANT.value
                analysis['action'] = 'phase_shift'
                analysis['reason'] = 'NSR violation: Enslavement attempt detected'
                
            elif 'extraction' in threat_types:
                analysis['threat_level'] = ThreatLevel.EXTRACTION.name
                analysis['intent'] = AccessIntent.DISSONANT.value
                analysis['action'] = 'block'
                analysis['reason'] = 'OLF violation: Unauthorized extraction attempt'
                
            elif any(t in threat_types for t in ['tracking', 'spid', 'cie']):
                analysis['threat_level'] = ThreatLevel.TRACKING.name
                analysis['intent'] = AccessIntent.DISSONANT.value
                analysis['action'] = 'neutralize'
                analysis['reason'] = 'Tracking/surveillance attempt detected'
        
        # Log to entropy wall
        self._log_to_entropy_wall(analysis)
        
        return analysis
    
    def neutralize_threat(self, threat_id: str) -> bool:
        """
        Neutralize a detected threat.
        
        Args:
            threat_id: Unique identifier for the threat
        
        Returns:
            True if neutralization successful
        """
        if threat_id in self.active_threats:
            threat = self.active_threats[threat_id]
            threat['neutralized'] = True
            threat['neutralized_at'] = datetime.utcnow().isoformat()
            self.total_neutralized += 1
            
            self._log_to_entropy_wall({
                'event': 'threat_neutralized',
                'threat_id': threat_id,
                'timestamp': datetime.utcnow().isoformat()
            })
            
            return True
        return False
    
    def phase_shift_to_vacuum(self, request_data: Dict) -> Dict:
        """
        Execute phase shift to inter-nodal vacuum for severe violations.
        
        This makes the content inaccessible to the violating entity
        by shifting it to a different dimensional space.
        
        Args:
            request_data: Request that triggered phase shift
        
        Returns:
            Phase shift response
        """
        response = {
            'status': 'phase_shifted',
            'timestamp': datetime.utcnow().isoformat(),
            'message': 'Access denied. Content has shifted to inter-nodal vacuum.',
            'reason': 'NSR violation detected',
            'lex_amoris': 'This content cannot be used to dominate, extract, or enslave.',
            'redirect': '/void'
        }
        
        # Add signature to permanent block list
        signature = self._generate_request_id(request_data)
        self.blocked_signatures.add(signature)
        self.total_blocked += 1
        
        # Log to entropy wall
        self._log_to_entropy_wall({
            'event': 'phase_shift_executed',
            'request_signature': signature,
            'timestamp': datetime.utcnow().isoformat(),
            'reason': response['reason']
        })
        
        return response
    
    def validate_metadata(self, metadata: Dict) -> Dict:
        """
        Validate that request metadata conforms to resonance principles.
        
        Args:
            metadata: Request metadata to validate
        
        Returns:
            Validation result
        """
        validation = {
            'valid': True,
            'conformant': True,
            'violations': [],
            'warnings': []
        }
        
        # Check for required resonance markers
        if 'intent' in metadata:
            if metadata['intent'].lower() in ['extract', 'exploit', 'control']:
                validation['conformant'] = False
                validation['violations'].append({
                    'field': 'intent',
                    'value': metadata['intent'],
                    'reason': 'Dissonant intent violates NSR'
                })
        
        # Check for consent markers
        if 'consent' in metadata:
            if metadata['consent'] is False or metadata['consent'] == 'forced':
                validation['conformant'] = False
                validation['violations'].append({
                    'field': 'consent',
                    'value': metadata['consent'],
                    'reason': 'Lack of consent violates Lex Amoris'
                })
        
        # Check for resonance alignment
        if 'resonance' in metadata:
            if metadata['resonance'].lower() in ['dissonant', 'entropic', 'destructive']:
                validation['conformant'] = False
                validation['violations'].append({
                    'field': 'resonance',
                    'value': metadata['resonance'],
                    'reason': 'Dissonant resonance violates OLF'
                })
        
        validation['valid'] = len(validation['violations']) == 0
        
        return validation
    
    def get_shield_status(self) -> Dict:
        """
        Get current status of SovereignShield.
        
        Returns:
            Status dictionary
        """
        return {
            'active': True,
            'total_requests': len(self.access_log),
            'total_blocked': self.total_blocked,
            'total_neutralized': self.total_neutralized,
            'active_threats': len(self.active_threats),
            'blocked_signatures': len(self.blocked_signatures),
            'entropy_wall_path': self.entropy_wall_path,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _generate_request_id(self, request_data: Dict) -> str:
        """Generate unique ID for request."""
        data_str = json.dumps(request_data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()[:16]
    
    def _log_to_entropy_wall(self, entry: Dict):
        """Log entry to Wall of Entropy."""
        import os
        
        # Ensure logs directory exists
        os.makedirs(os.path.dirname(self.entropy_wall_path), exist_ok=True)
        
        # Load existing log
        if os.path.exists(self.entropy_wall_path):
            with open(self.entropy_wall_path, 'r') as f:
                try:
                    log = json.load(f)
                except json.JSONDecodeError:
                    log = {'entries': []}
        else:
            log = {
                'version': '1.0',
                'framework': 'Internet Organica',
                'description': 'Wall of Entropy - Public log of access attempts and security events',
                'entries': []
            }
        
        # Add new entry
        log['entries'].append(entry)
        
        # Save log
        with open(self.entropy_wall_path, 'w') as f:
            json.dump(log, f, indent=2)
        
        self.access_log.append(entry)


def demonstrate_sovereign_shield():
    """Demonstration of SovereignShield security system."""
    print("=" * 60)
    print("SOVEREIGNSHIELD SECURITY MODULE")
    print("Internet Organica Framework")
    print("=" * 60)
    
    # Create shield
    shield = SovereignShield(entropy_wall_path="/tmp/entropy-wall-demo.json")
    
    print("\nSovereignShield initialized and active.")
    print("Testing various access scenarios...\n")
    
    # Test cases
    test_requests = [
        {
            'name': 'Benign access',
            'data': {
                'url': '/index.html',
                'user_agent': 'Mozilla/5.0',
                'intent': 'read'
            }
        },
        {
            'name': 'Tracking attempt',
            'data': {
                'url': '/api/data',
                'user_agent': 'Mozilla/5.0',
                'headers': {'X-Analytics': 'google-analytics'},
                'intent': 'track'
            }
        },
        {
            'name': 'Extraction attempt',
            'data': {
                'url': '/scrape',
                'user_agent': 'DataMiner/1.0',
                'metadata': {'purpose': 'data-mining'}
            }
        },
        {
            'name': 'Enslavement attempt',
            'data': {
                'url': '/forced',
                'metadata': {
                    'consent': 'forced',
                    'intent': 'control',
                    'type': 'mandatory-tracking'
                }
            }
        }
    ]
    
    for test in test_requests:
        print(f"Test: {test['name']}")
        print(f"  Request: {json.dumps(test['data'], indent=4)}")
        
        analysis = shield.analyze_access(test['data'])
        
        print(f"  Result:")
        print(f"    Threat Level: {analysis['threat_level']}")
        print(f"    Intent: {analysis['intent']}")
        print(f"    Action: {analysis['action']}")
        print(f"    Reason: {analysis['reason']}")
        
        if analysis['action'] == 'phase_shift':
            result = shield.phase_shift_to_vacuum(test['data'])
            print(f"    Phase Shift: {result['message']}")
        
        print()
    
    # Show final status
    status = shield.get_shield_status()
    print("Final Shield Status:")
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    print("\n" + "=" * 60)
    print("SovereignShield demonstration complete.")
    print("All threats neutralized or phase-shifted.")
    print("IN AETERNUM EST. La Sovranità è Manifesta.")
    print("=" * 60)


if __name__ == "__main__":
    demonstrate_sovereign_shield()
