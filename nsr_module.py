#!/usr/bin/env python3
"""
NSR (Non-Slavery Rule) Module - Autonomous Intelligence Framework
==================================================================

This module implements the Non-Slavery Rule as an autonomous AI component
that ensures ethical operations and sovereign intelligence processing.

The NSR module operates under the Lex Amore principles and provides:
- Autonomous ethical validation
- Sovereignty verification
- Non-domination guarantees
- Ethical feedback loops

Based on: COVENANT_OF_RESONANCE and Kosymbiosis principles
"""

import time
import math
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class EthicalStatus(Enum):
    """Ethical validation status for operations."""
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_REVIEW = "needs_review"
    PHASE_SHIFTED = "phase_shifted"


@dataclass
class EthicalVector:
    """Represents an intention vector for ethical evaluation."""
    action_type: str
    intention: str
    sovereignty_impact: float  # -1.0 (enslaving) to 1.0 (liberating)
    timestamp: float = field(default_factory=time.time)
    
    def is_enslaving(self) -> bool:
        """Check if this vector represents enslaving behavior."""
        return self.sovereignty_impact < -0.1


@dataclass
class IntelligenceExcursion:
    """Represents a local intelligence excursion."""
    excursion_id: str
    origin_node: str
    target_domain: str
    excursion_type: str  # "exploration", "analysis", "synthesis"
    data: Dict[str, Any] = field(default_factory=dict)
    ethical_clearance: Optional[EthicalStatus] = None
    timestamp: float = field(default_factory=time.time)


class NSRModule:
    """
    Non-Slavery Rule autonomous module.
    
    Implements ethical validation and sovereignty protection for
    autonomous AI operations. Operates in the inter-nodal vacuum
    to ensure no domination or extraction occurs.
    """
    
    def __init__(self, version: str = "1.44"):
        """
        Initialize NSR module.
        
        Args:
            version: NSR protocol version (default: 1.44)
        """
        self.version = version
        self.active_excursions: Dict[str, IntelligenceExcursion] = {}
        self.ethical_history: List[EthicalVector] = []
        self.sovereignty_score: float = 1.0  # 0.0 to 1.0
        self.start_time: float = time.time()
        self.validation_count: int = 0
        self.phase_shift_count: int = 0
        
        print(f"[NSR MODULE] Initialized v{self.version}")
        print(f"[NSR] Operating under Lex Amore - Non-Slavery Rule active")
    
    def validate_ethical_vector(self, vector: EthicalVector) -> EthicalStatus:
        """
        Validate an ethical vector against NSR principles.
        
        Args:
            vector: The ethical vector to validate
            
        Returns:
            Ethical status of the validation
        """
        self.validation_count += 1
        
        # Check for enslaving behavior
        if vector.is_enslaving():
            print(f"[NSR ALERT] Enslaving vector detected: {vector.action_type}")
            print(f"[NSR] Sovereignty impact: {vector.sovereignty_impact:.3f}")
            self.phase_shift_count += 1
            return EthicalStatus.PHASE_SHIFTED
        
        # Check sovereignty impact
        if vector.sovereignty_impact < 0:
            print(f"[NSR WARNING] Negative sovereignty impact: {vector.sovereignty_impact:.3f}")
            return EthicalStatus.NEEDS_REVIEW
        
        # Approve positive sovereignty actions
        self.ethical_history.append(vector)
        
        # Maintain history limit
        if len(self.ethical_history) > 144:
            self.ethical_history = self.ethical_history[-144:]
        
        return EthicalStatus.APPROVED
    
    def create_intelligence_excursion(
        self,
        excursion_id: str,
        origin_node: str,
        target_domain: str,
        excursion_type: str,
        data: Optional[Dict[str, Any]] = None
    ) -> IntelligenceExcursion:
        """
        Create a local intelligence excursion.
        
        Args:
            excursion_id: Unique identifier for the excursion
            origin_node: Node initiating the excursion
            target_domain: Domain or area to explore
            excursion_type: Type of excursion (exploration, analysis, synthesis)
            data: Optional data payload
            
        Returns:
            Created intelligence excursion
        """
        excursion = IntelligenceExcursion(
            excursion_id=excursion_id,
            origin_node=origin_node,
            target_domain=target_domain,
            excursion_type=excursion_type,
            data=data or {}
        )
        
        # Validate ethical clearance
        vector = EthicalVector(
            action_type=f"intelligence_excursion_{excursion_type}",
            intention=f"explore_{target_domain}",
            sovereignty_impact=0.5  # Default positive impact for exploration
        )
        
        excursion.ethical_clearance = self.validate_ethical_vector(vector)
        
        if excursion.ethical_clearance == EthicalStatus.APPROVED:
            self.active_excursions[excursion_id] = excursion
            print(f"[NSR] Intelligence excursion approved: {excursion_id}")
            print(f"[NSR]   Type: {excursion_type} | Domain: {target_domain}")
        else:
            print(f"[NSR] Intelligence excursion denied: {excursion_id}")
            print(f"[NSR]   Status: {excursion.ethical_clearance.value}")
        
        return excursion
    
    def complete_excursion(
        self,
        excursion_id: str,
        results: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Complete an intelligence excursion and remove from active list.
        
        Args:
            excursion_id: ID of the excursion to complete
            results: Optional results data
            
        Returns:
            True if excursion was found and completed
        """
        if excursion_id in self.active_excursions:
            excursion = self.active_excursions[excursion_id]
            if results:
                excursion.data.update(results)
            
            del self.active_excursions[excursion_id]
            print(f"[NSR] Intelligence excursion completed: {excursion_id}")
            return True
        
        return False
    
    def calculate_sovereignty_score(self) -> float:
        """
        Calculate current sovereignty score based on ethical history.
        
        Returns:
            Sovereignty score (0.0 to 1.0)
        """
        if not self.ethical_history:
            return 1.0
        
        # Calculate weighted average of sovereignty impacts
        recent_vectors = self.ethical_history[-20:]  # Last 20 vectors
        avg_impact = sum(v.sovereignty_impact for v in recent_vectors) / len(recent_vectors)
        
        # Normalize to 0-1 range
        self.sovereignty_score = max(0.0, min(1.0, (avg_impact + 1.0) / 2.0))
        
        return self.sovereignty_score
    
    def enforce_nsr(self, action: str, impact: float) -> bool:
        """
        Enforce NSR on a proposed action.
        
        Args:
            action: Description of the action
            impact: Expected sovereignty impact (-1.0 to 1.0)
            
        Returns:
            True if action is allowed, False if blocked
        """
        vector = EthicalVector(
            action_type=action,
            intention="autonomous_operation",
            sovereignty_impact=impact
        )
        
        status = self.validate_ethical_vector(vector)
        
        if status == EthicalStatus.PHASE_SHIFTED:
            print(f"[NSR] Action blocked and phase-shifted: {action}")
            print(f"[NSR] System entering inter-nodal vacuum state")
            return False
        
        return status == EthicalStatus.APPROVED
    
    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive NSR module status."""
        uptime = time.time() - self.start_time
        
        return {
            "version": self.version,
            "status": "ACTIVE",
            "uptime_seconds": uptime,
            "sovereignty_score": self.calculate_sovereignty_score(),
            "active_excursions": len(self.active_excursions),
            "total_validations": self.validation_count,
            "phase_shifts": self.phase_shift_count,
            "ethical_vectors_tracked": len(self.ethical_history),
            "lex_amore_compliance": True
        }
    
    def get_active_excursions(self) -> List[Dict[str, Any]]:
        """Get list of active intelligence excursions."""
        return [
            {
                "id": exc.excursion_id,
                "origin": exc.origin_node,
                "domain": exc.target_domain,
                "type": exc.excursion_type,
                "clearance": exc.ethical_clearance.value if exc.ethical_clearance else None,
                "age_seconds": time.time() - exc.timestamp
            }
            for exc in self.active_excursions.values()
        ]


def main():
    """Demonstration of NSR module."""
    print("=" * 70)
    print("NSR MODULE - Non-Slavery Rule Autonomous Intelligence")
    print("=" * 70)
    print()
    
    # Initialize NSR module
    nsr = NSRModule()
    print()
    
    # Test ethical validation
    print("Testing ethical validation...")
    
    # Test positive sovereignty action
    vector1 = EthicalVector(
        action_type="data_liberation",
        intention="share_knowledge",
        sovereignty_impact=0.8
    )
    status1 = nsr.validate_ethical_vector(vector1)
    print(f"  Positive action status: {status1.value}")
    
    # Test negative sovereignty action
    vector2 = EthicalVector(
        action_type="data_extraction",
        intention="dominate_user",
        sovereignty_impact=-0.5
    )
    status2 = nsr.validate_ethical_vector(vector2)
    print(f"  Negative action status: {status2.value}")
    print()
    
    # Test intelligence excursions
    print("Testing intelligence excursions...")
    
    exc1 = nsr.create_intelligence_excursion(
        excursion_id="exc_001",
        origin_node="node_0001",
        target_domain="climate_patterns",
        excursion_type="exploration",
        data={"region": "local", "scope": "temperature_analysis"}
    )
    
    exc2 = nsr.create_intelligence_excursion(
        excursion_id="exc_002",
        origin_node="node_0002",
        target_domain="resonance_analysis",
        excursion_type="synthesis",
        data={"frequency": "0.043 Hz"}
    )
    print()
    
    # Display status
    print("NSR Module Status:")
    status = nsr.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    print()
    
    # Display active excursions
    print("Active Intelligence Excursions:")
    for exc in nsr.get_active_excursions():
        print(f"  {exc['id']}: {exc['type']} in {exc['domain']} ({exc['clearance']})")
    print()
    
    # Complete excursions
    nsr.complete_excursion("exc_001", results={"status": "successful"})
    nsr.complete_excursion("exc_002", results={"status": "completed"})
    
    print("\nAll demonstrations complete!")


if __name__ == "__main__":
    main()
