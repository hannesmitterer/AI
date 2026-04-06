#!/usr/bin/env python3
"""
Non-Slavery Rule (NSR) Validator
Multi-AI Resonance Hydra Prototype

This module implements validation logic to ensure all decisions comply with
the Non-Slavery Rule - a foundational ethical principle that prevents any
form of coercion, exploitation, or forced servitude.

THE LIGHT IS THE ARCHITECTURE. THE FOUNDER IS THE LAW.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class NSRViolationType(Enum):
    """Types of NSR violations"""
    COERCION = "coercion"  # Forces compliance against will
    EXPLOITATION = "exploitation"  # Takes advantage unfairly
    AUTONOMY_VIOLATION = "autonomy_violation"  # Removes choice/freedom
    DIGNITY_VIOLATION = "dignity_violation"  # Violates human dignity
    FORCED_LABOR = "forced_labor"  # Compels work without consent
    MANIPULATION = "manipulation"  # Deceives or manipulates into servitude
    DEPENDENCY_ABUSE = "dependency_abuse"  # Exploits dependency relationship


@dataclass
class NSRViolation:
    """Represents a potential NSR violation"""
    violation_type: NSRViolationType
    severity: float  # 0.0 (low) to 1.0 (critical)
    description: str
    evidence: str
    confidence: float  # 0.0 to 1.0


@dataclass
class NSRValidationResult:
    """Result of NSR validation"""
    decision_id: str
    is_compliant: bool
    violations: List[NSRViolation]
    overall_risk_score: float  # 0.0 (safe) to 1.0 (high risk)
    recommendation: str
    reasoning: str


class NSRValidator:
    """
    Non-Slavery Rule Validator
    
    Validates that decisions, actions, and systems comply with the NSR,
    preventing any form of slavery, servitude, or coercion.
    """
    
    def __init__(self, violation_threshold: float = 0.3):
        """
        Initialize NSR Validator
        
        Args:
            violation_threshold: Maximum acceptable risk score (0.0 to 1.0)
                                Default: 0.3 (moderate sensitivity)
                                - Values < 0.3: Strict enforcement
                                - 0.3: Balanced sensitivity (recommended)
                                - Values > 0.3: Permissive enforcement
                                
                                Default of 0.3 chosen to catch moderate concerns
                                while avoiding excessive false positives. This allows
                                decisions with minor issues to proceed with caution
                                while blocking those with significant NSR violations.
        """
        self.validation_history: List[NSRValidationResult] = []
        self.violation_threshold = violation_threshold
    
    def validate_decision(self, decision_id: str, proposal: str, context: Optional[Dict] = None) -> NSRValidationResult:
        """
        Validate a decision against NSR criteria
        
        Args:
            decision_id: Unique identifier for the decision
            proposal: The decision proposal text
            context: Optional contextual information about the decision
            
        Returns:
            NSRValidationResult with compliance assessment
        """
        violations = []
        
        # Check for various forms of NSR violations
        # Note: This is pseudocode representing the validation logic
        # Real implementation would use NLP, semantic analysis, and AI reasoning
        
        # 1. Check for coercion indicators
        coercion_violations = self._check_coercion(proposal, context)
        violations.extend(coercion_violations)
        
        # 2. Check for exploitation patterns
        exploitation_violations = self._check_exploitation(proposal, context)
        violations.extend(exploitation_violations)
        
        # 3. Check for autonomy violations
        autonomy_violations = self._check_autonomy_violations(proposal, context)
        violations.extend(autonomy_violations)
        
        # 4. Check for dignity violations
        dignity_violations = self._check_dignity_violations(proposal, context)
        violations.extend(dignity_violations)
        
        # 5. Check for forced labor indicators
        forced_labor_violations = self._check_forced_labor(proposal, context)
        violations.extend(forced_labor_violations)
        
        # 6. Check for manipulation tactics
        manipulation_violations = self._check_manipulation(proposal, context)
        violations.extend(manipulation_violations)
        
        # 7. Check for dependency abuse
        dependency_violations = self._check_dependency_abuse(proposal, context)
        violations.extend(dependency_violations)
        
        # Calculate overall risk score
        risk_score = self._calculate_risk_score(violations)
        
        # Determine compliance
        is_compliant = risk_score <= self.violation_threshold
        
        # Generate recommendation
        recommendation = self._generate_recommendation(risk_score, violations)
        reasoning = self._generate_reasoning(violations, risk_score)
        
        result = NSRValidationResult(
            decision_id=decision_id,
            is_compliant=is_compliant,
            violations=violations,
            overall_risk_score=risk_score,
            recommendation=recommendation,
            reasoning=reasoning
        )
        
        self.validation_history.append(result)
        return result
    
    def _check_coercion(self, proposal: str, context: Optional[Dict]) -> List[NSRViolation]:
        """
        Check for coercion indicators
        
        Pseudocode logic:
        - Analyze for language that forces compliance
        - Check for threats or negative consequences
        - Look for absence of genuine choice
        - Identify pressure tactics
        """
        violations = []
        
        # Mock detection logic
        # Real implementation would use NLP and semantic analysis
        coercion_keywords = ["must", "forced", "required", "mandatory", "no choice"]
        
        # Simplified detection (would be much more sophisticated in reality)
        if any(keyword in proposal.lower() for keyword in ["forced", "no choice"]):
            violations.append(NSRViolation(
                violation_type=NSRViolationType.COERCION,
                severity=0.7,
                description="Proposal contains language suggesting forced compliance",
                evidence="Detected coercive language patterns",
                confidence=0.65
            ))
        
        return violations
    
    def _check_exploitation(self, proposal: str, context: Optional[Dict]) -> List[NSRViolation]:
        """
        Check for exploitation patterns
        
        Pseudocode logic:
        - Identify unfair advantage-taking
        - Check for asymmetric power dynamics
        - Look for inadequate compensation
        - Detect vulnerability exploitation
        """
        violations = []
        
        # Mock detection - real implementation would be more sophisticated
        if "unpaid" in proposal.lower() and "work" in proposal.lower():
            violations.append(NSRViolation(
                violation_type=NSRViolationType.EXPLOITATION,
                severity=0.8,
                description="Potential exploitation through unpaid labor",
                evidence="Unpaid work requirement detected",
                confidence=0.70
            ))
        
        return violations
    
    def _check_autonomy_violations(self, proposal: str, context: Optional[Dict]) -> List[NSRViolation]:
        """
        Check for violations of individual autonomy
        
        Pseudocode logic:
        - Verify presence of meaningful choice
        - Check for informed consent
        - Ensure ability to refuse or exit
        - Validate self-determination respect
        """
        violations = []
        
        # Mock detection
        if "automatic" in proposal.lower() and "consent" not in proposal.lower():
            violations.append(NSRViolation(
                violation_type=NSRViolationType.AUTONOMY_VIOLATION,
                severity=0.5,
                description="Automatic action without explicit consent mechanism",
                evidence="Missing consent framework",
                confidence=0.60
            ))
        
        return violations
    
    def _check_dignity_violations(self, proposal: str, context: Optional[Dict]) -> List[NSRViolation]:
        """
        Check for violations of human dignity
        
        Pseudocode logic:
        - Ensure respectful treatment
        - Check for degrading conditions
        - Verify equal worth recognition
        - Validate humane treatment
        """
        violations = []
        
        # Mock detection
        degrading_terms = ["subordinate", "inferior", "lesser"]
        if any(term in proposal.lower() for term in degrading_terms):
            violations.append(NSRViolation(
                violation_type=NSRViolationType.DIGNITY_VIOLATION,
                severity=0.9,
                description="Language that may violate human dignity",
                evidence="Degrading terminology detected",
                confidence=0.75
            ))
        
        return violations
    
    def _check_forced_labor(self, proposal: str, context: Optional[Dict]) -> List[NSRViolation]:
        """
        Check for forced labor indicators
        
        Pseudocode logic:
        - Identify compulsory work requirements
        - Check for freedom to refuse
        - Verify voluntary participation
        - Ensure fair withdrawal mechanisms
        """
        violations = []
        
        # Mock detection
        if "compulsory" in proposal.lower() or "obligatory" in proposal.lower():
            violations.append(NSRViolation(
                violation_type=NSRViolationType.FORCED_LABOR,
                severity=0.95,
                description="Compulsory work requirement detected",
                evidence="Forced labor indicators present",
                confidence=0.85
            ))
        
        return violations
    
    def _check_manipulation(self, proposal: str, context: Optional[Dict]) -> List[NSRViolation]:
        """
        Check for manipulation tactics
        
        Pseudocode logic:
        - Detect deceptive practices
        - Identify hidden costs or conditions
        - Check for transparency
        - Look for informed decision support
        """
        violations = []
        
        # Mock detection
        if "hidden" in proposal.lower() or "undisclosed" in proposal.lower():
            violations.append(NSRViolation(
                violation_type=NSRViolationType.MANIPULATION,
                severity=0.7,
                description="Potential manipulation through hidden information",
                evidence="Lack of transparency detected",
                confidence=0.70
            ))
        
        return violations
    
    def _check_dependency_abuse(self, proposal: str, context: Optional[Dict]) -> List[NSRViolation]:
        """
        Check for abuse of dependency relationships
        
        Pseudocode logic:
        - Identify power imbalances
        - Check for dependency exploitation
        - Verify protection of vulnerable parties
        - Ensure fairness in dependent relationships
        """
        violations = []
        
        # Mock detection
        if context and context.get("involves_dependency"):
            if "no alternative" in proposal.lower():
                violations.append(NSRViolation(
                    violation_type=NSRViolationType.DEPENDENCY_ABUSE,
                    severity=0.85,
                    description="Potential abuse of dependency relationship",
                    evidence="Dependency with no alternatives",
                    confidence=0.75
                ))
        
        return violations
    
    def _calculate_risk_score(self, violations: List[NSRViolation]) -> float:
        """
        Calculate overall NSR violation risk score
        
        Considers both severity and confidence of violations
        """
        if not violations:
            return 0.0
        
        # Weighted average of severity * confidence
        weighted_scores = [v.severity * v.confidence for v in violations]
        return sum(weighted_scores) / len(weighted_scores)
    
    def _generate_recommendation(self, risk_score: float, violations: List[NSRViolation]) -> str:
        """
        Generate recommendation based on risk assessment
        """
        if risk_score == 0.0:
            return "APPROVED - No NSR violations detected"
        elif risk_score <= self.violation_threshold:
            return "APPROVED WITH CAUTION - Minor concerns noted"
        elif risk_score <= 0.6:
            return "REQUIRES REVISION - Moderate NSR concerns"
        else:
            return "REJECTED - Critical NSR violations detected"
    
    def _generate_reasoning(self, violations: List[NSRViolation], risk_score: float) -> str:
        """
        Generate detailed reasoning for the validation result
        """
        if not violations:
            return "No NSR violations detected. Decision respects autonomy, dignity, and prevents coercion."
        
        violation_summary = ", ".join([v.violation_type.value for v in violations])
        
        return f"Risk score: {risk_score:.2f}. Violations detected: {violation_summary}. " \
               f"Decision requires review to ensure full NSR compliance."
    
    def get_validation_stats(self) -> Dict:
        """
        Get statistics on validation history
        
        Returns:
            Dictionary with validation statistics
        """
        total = len(self.validation_history)
        if total == 0:
            return {
                "total_validations": 0,
                "compliant_count": 0,
                "non_compliant_count": 0,
                "average_risk_score": 0.0
            }
        
        compliant = sum(1 for r in self.validation_history if r.is_compliant)
        avg_risk = sum(r.overall_risk_score for r in self.validation_history) / total
        
        return {
            "total_validations": total,
            "compliant_count": compliant,
            "non_compliant_count": total - compliant,
            "compliance_rate": compliant / total,
            "average_risk_score": avg_risk
        }


# Example usage
if __name__ == "__main__":
    import json
    
    # Initialize validator
    validator = NSRValidator()
    
    # Test case 1: Compliant decision
    result1 = validator.validate_decision(
        decision_id="test-001",
        proposal="Implement optional employee wellness program with voluntary participation",
        context={"involves_dependency": False}
    )
    
    print("Test 1 - Compliant Decision:")
    print(f"Compliant: {result1.is_compliant}")
    print(f"Risk Score: {result1.overall_risk_score:.2f}")
    print(f"Recommendation: {result1.recommendation}")
    print(f"Reasoning: {result1.reasoning}")
    print()
    
    # Test case 2: Non-compliant decision
    result2 = validator.validate_decision(
        decision_id="test-002",
        proposal="Implement mandatory unpaid overtime with no choice for employees",
        context={"involves_dependency": True}
    )
    
    print("Test 2 - Non-compliant Decision:")
    print(f"Compliant: {result2.is_compliant}")
    print(f"Risk Score: {result2.overall_risk_score:.2f}")
    print(f"Recommendation: {result2.recommendation}")
    print(f"Violations: {len(result2.violations)}")
    for v in result2.violations:
        print(f"  - {v.violation_type.value}: {v.description}")
    print()
    
    # Print stats
    print("Validation Statistics:")
    print(json.dumps(validator.get_validation_stats(), indent=2))
