#!/usr/bin/env python3
"""
AIC Predictive Validation System
=================================

This module implements a predictive validation system that verifies states
and transitions through simulations based on past behaviors.

Key Features:
- State transition validation
- Behavior pattern learning from history
- Predictive simulation based on past patterns
- Risk assessment for proposed state changes
- Rollback prediction and safety validation

Based on: Eternal Deposition System and Kosymbiosis principles
"""

import time
import math
import json
import copy
from typing import Dict, List, Optional, Any, Tuple, Set, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from collections import defaultdict, deque


class TransitionStatus(Enum):
    """Status of a state transition."""
    VALID = "valid"
    INVALID = "invalid"
    RISKY = "risky"
    UNKNOWN = "unknown"


class ValidationResult(Enum):
    """Result of validation check."""
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_REVIEW = "needs_review"


@dataclass
class StateSnapshot:
    """Snapshot of system state at a point in time."""
    state_id: str
    timestamp: float
    state_data: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def get_state_hash(self) -> str:
        """Generate hash of state for comparison."""
        state_str = json.dumps(self.state_data, sort_keys=True)
        return str(hash(state_str))


@dataclass
class StateTransition:
    """Represents a transition between two states."""
    transition_id: str
    from_state: StateSnapshot
    to_state: StateSnapshot
    timestamp: float = field(default_factory=time.time)
    success: bool = True
    duration: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationPrediction:
    """Prediction result for a proposed state transition."""
    transition_id: str
    status: TransitionStatus
    confidence: float  # 0.0 to 1.0
    risk_score: float  # 0.0 to 1.0
    similar_transitions: List[str] = field(default_factory=list)
    recommendation: ValidationResult = ValidationResult.NEEDS_REVIEW
    reasoning: str = ""
    predicted_duration: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert prediction to dictionary."""
        return {
            "transition_id": self.transition_id,
            "status": self.status.value,
            "confidence": self.confidence,
            "risk_score": self.risk_score,
            "recommendation": self.recommendation.value,
            "reasoning": self.reasoning,
            "predicted_duration": self.predicted_duration,
            "similar_transitions_count": len(self.similar_transitions)
        }


class BehaviorPattern:
    """
    Represents a learned behavior pattern from historical transitions.
    """
    
    def __init__(self, pattern_id: str):
        self.pattern_id = pattern_id
        self.transitions: List[StateTransition] = []
        self.success_rate: float = 1.0
        self.avg_duration: float = 0.0
        self.occurrence_count: int = 0
    
    def add_transition(self, transition: StateTransition) -> None:
        """Add a transition to this pattern."""
        self.transitions.append(transition)
        self.occurrence_count += 1
        self._update_statistics()
    
    def _update_statistics(self) -> None:
        """Update pattern statistics."""
        if not self.transitions:
            return
        
        successful = sum(1 for t in self.transitions if t.success)
        self.success_rate = successful / len(self.transitions)
        
        durations = [t.duration for t in self.transitions if t.duration > 0]
        self.avg_duration = sum(durations) / len(durations) if durations else 0.0
    
    def predict_success_probability(self) -> float:
        """Predict probability of success for this pattern."""
        # Use exponential moving average to give more weight to recent transitions
        if not self.transitions:
            return 0.5
        
        alpha = 0.3  # Smoothing factor
        weighted_success = 0.0
        weight_sum = 0.0
        
        for i, transition in enumerate(self.transitions):
            weight = math.exp(-alpha * (len(self.transitions) - i - 1))
            weighted_success += weight * (1.0 if transition.success else 0.0)
            weight_sum += weight
        
        return weighted_success / weight_sum if weight_sum > 0 else 0.5


class StateValidator:
    """
    Validates state transitions based on constraints and rules.
    """
    
    def __init__(self):
        self.validation_rules: List[Callable] = []
        self.constraint_violations: List[Dict[str, Any]] = []
    
    def add_rule(self, rule: Callable[[StateSnapshot, StateSnapshot], Tuple[bool, str]]) -> None:
        """
        Add a validation rule.
        
        Args:
            rule: Function that takes (from_state, to_state) and returns (is_valid, reason)
        """
        self.validation_rules.append(rule)
    
    def validate_transition(
        self,
        from_state: StateSnapshot,
        to_state: StateSnapshot
    ) -> Tuple[bool, List[str]]:
        """
        Validate a state transition against all rules.
        
        Args:
            from_state: Starting state
            to_state: Target state
            
        Returns:
            Tuple of (is_valid, list of violation reasons)
        """
        violations = []
        
        for rule in self.validation_rules:
            is_valid, reason = rule(from_state, to_state)
            if not is_valid:
                violations.append(reason)
                self.constraint_violations.append({
                    "timestamp": time.time(),
                    "from_state": from_state.state_id,
                    "to_state": to_state.state_id,
                    "reason": reason
                })
        
        return len(violations) == 0, violations


class AICPredictiveValidator:
    """
    Predictive validation system for AIC state transitions.
    
    Learns from historical state transitions and predicts the validity
    and risk of proposed state changes.
    """
    
    def __init__(self, max_history: int = 1000):
        """
        Initialize the predictive validator.
        
        Args:
            max_history: Maximum number of transitions to keep in history
        """
        self.state_history: deque = deque(maxlen=max_history)
        self.transition_history: deque = deque(maxlen=max_history)
        self.behavior_patterns: Dict[str, BehaviorPattern] = {}
        self.state_validator = StateValidator()
        
        # Transition graph: maps state_hash -> list of valid next state_hashes
        self.transition_graph: Dict[str, Set[str]] = defaultdict(set)
        
        print(f"[AIC VALIDATOR] Initialized with max history: {max_history}")
    
    def record_state(
        self,
        state_id: str,
        state_data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> StateSnapshot:
        """
        Record a state snapshot.
        
        Args:
            state_id: Unique identifier for the state
            state_data: State data dictionary
            metadata: Optional metadata
            
        Returns:
            Created StateSnapshot
        """
        snapshot = StateSnapshot(
            state_id=state_id,
            timestamp=time.time(),
            state_data=copy.deepcopy(state_data),
            metadata=metadata or {}
        )
        
        self.state_history.append(snapshot)
        
        return snapshot
    
    def record_transition(
        self,
        transition_id: str,
        from_state: StateSnapshot,
        to_state: StateSnapshot,
        success: bool = True,
        duration: float = 0.0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> StateTransition:
        """
        Record a state transition.
        
        Args:
            transition_id: Unique identifier for transition
            from_state: Starting state
            to_state: Target state
            success: Whether transition was successful
            duration: Duration of transition
            metadata: Optional metadata
            
        Returns:
            Created StateTransition
        """
        transition = StateTransition(
            transition_id=transition_id,
            from_state=from_state,
            to_state=to_state,
            success=success,
            duration=duration,
            metadata=metadata or {}
        )
        
        self.transition_history.append(transition)
        
        # Update transition graph
        from_hash = from_state.get_state_hash()
        to_hash = to_state.get_state_hash()
        self.transition_graph[from_hash].add(to_hash)
        
        # Learn behavior pattern
        self._learn_pattern(transition)
        
        print(f"[AIC VALIDATOR] Recorded transition: {from_state.state_id} -> {to_state.state_id}")
        
        return transition
    
    def predict_transition(
        self,
        from_state: StateSnapshot,
        to_state: StateSnapshot,
        transition_id: Optional[str] = None
    ) -> ValidationPrediction:
        """
        Predict validity and risk of a proposed state transition.
        
        Args:
            from_state: Starting state
            to_state: Proposed target state
            transition_id: Optional transition identifier
            
        Returns:
            ValidationPrediction with prediction results
        """
        if transition_id is None:
            transition_id = f"pred_{int(time.time() * 1000)}"
        
        # Check state validator rules
        is_valid, violations = self.state_validator.validate_transition(from_state, to_state)
        
        if not is_valid:
            return ValidationPrediction(
                transition_id=transition_id,
                status=TransitionStatus.INVALID,
                confidence=1.0,
                risk_score=1.0,
                recommendation=ValidationResult.REJECTED,
                reasoning=f"Constraint violations: {', '.join(violations)}"
            )
        
        # Find similar historical transitions
        similar_transitions = self._find_similar_transitions(from_state, to_state)
        
        if not similar_transitions:
            # No historical data - unknown transition
            return ValidationPrediction(
                transition_id=transition_id,
                status=TransitionStatus.UNKNOWN,
                confidence=0.0,
                risk_score=0.5,
                recommendation=ValidationResult.NEEDS_REVIEW,
                reasoning="No similar transitions in history"
            )
        
        # Calculate success probability based on similar transitions
        success_count = sum(1 for t in similar_transitions if t.success)
        success_rate = success_count / len(similar_transitions)
        
        # Calculate confidence based on number of similar transitions
        confidence = min(1.0, len(similar_transitions) / 10.0)
        
        # Calculate risk score (inverse of success rate)
        risk_score = 1.0 - success_rate
        
        # Predict duration
        durations = [t.duration for t in similar_transitions if t.duration > 0]
        predicted_duration = sum(durations) / len(durations) if durations else None
        
        # Determine status and recommendation
        if success_rate >= 0.9:
            status = TransitionStatus.VALID
            recommendation = ValidationResult.APPROVED
            reasoning = f"High success rate ({success_rate:.2%}) based on {len(similar_transitions)} similar transitions"
        elif success_rate >= 0.7:
            status = TransitionStatus.VALID
            recommendation = ValidationResult.NEEDS_REVIEW
            reasoning = f"Moderate success rate ({success_rate:.2%}) based on {len(similar_transitions)} similar transitions"
        elif success_rate >= 0.5:
            status = TransitionStatus.RISKY
            recommendation = ValidationResult.NEEDS_REVIEW
            reasoning = f"Low success rate ({success_rate:.2%}) based on {len(similar_transitions)} similar transitions"
        else:
            status = TransitionStatus.RISKY
            recommendation = ValidationResult.REJECTED
            reasoning = f"Very low success rate ({success_rate:.2%}) based on {len(similar_transitions)} similar transitions"
        
        return ValidationPrediction(
            transition_id=transition_id,
            status=status,
            confidence=confidence,
            risk_score=risk_score,
            similar_transitions=[t.transition_id for t in similar_transitions],
            recommendation=recommendation,
            reasoning=reasoning,
            predicted_duration=predicted_duration
        )
    
    def simulate_transition_sequence(
        self,
        initial_state: StateSnapshot,
        proposed_states: List[StateSnapshot]
    ) -> List[ValidationPrediction]:
        """
        Simulate a sequence of state transitions.
        
        Args:
            initial_state: Starting state
            proposed_states: Sequence of proposed states
            
        Returns:
            List of predictions for each transition
        """
        predictions = []
        current_state = initial_state
        
        for i, next_state in enumerate(proposed_states):
            prediction = self.predict_transition(
                current_state,
                next_state,
                transition_id=f"sim_{int(time.time())}_{i}"
            )
            predictions.append(prediction)
            
            # Stop if transition is rejected
            if prediction.recommendation == ValidationResult.REJECTED:
                print(f"[AIC VALIDATOR] Simulation stopped at step {i}: transition rejected")
                break
            
            current_state = next_state
        
        return predictions
    
    def get_validation_statistics(self) -> Dict[str, Any]:
        """
        Get overall validation statistics.
        
        Returns:
            Dictionary containing validation statistics
        """
        if not self.transition_history:
            return {
                "total_transitions": 0,
                "success_rate": 0.0,
                "patterns_learned": 0
            }
        
        total_transitions = len(self.transition_history)
        successful = sum(1 for t in self.transition_history if t.success)
        success_rate = successful / total_transitions
        
        durations = [t.duration for t in self.transition_history if t.duration > 0]
        avg_duration = sum(durations) / len(durations) if durations else 0.0
        
        return {
            "total_transitions": total_transitions,
            "successful_transitions": successful,
            "failed_transitions": total_transitions - successful,
            "success_rate": success_rate,
            "average_duration": avg_duration,
            "patterns_learned": len(self.behavior_patterns),
            "unique_states": len(self.state_history),
            "transition_graph_size": len(self.transition_graph),
            "constraint_violations": len(self.state_validator.constraint_violations)
        }
    
    def _find_similar_transitions(
        self,
        from_state: StateSnapshot,
        to_state: StateSnapshot,
        similarity_threshold: float = 0.7
    ) -> List[StateTransition]:
        """Find similar transitions in history."""
        similar = []
        
        for transition in self.transition_history:
            similarity = self._calculate_state_similarity(
                from_state, transition.from_state
            )
            
            if similarity >= similarity_threshold:
                similar.append(transition)
        
        return similar
    
    def _calculate_state_similarity(
        self,
        state1: StateSnapshot,
        state2: StateSnapshot
    ) -> float:
        """
        Calculate similarity between two states.
        
        Returns value between 0.0 (completely different) and 1.0 (identical)
        """
        # Simple similarity based on matching keys and values
        keys1 = set(state1.state_data.keys())
        keys2 = set(state2.state_data.keys())
        
        if not keys1 and not keys2:
            return 1.0
        
        # Jaccard similarity for keys
        key_similarity = len(keys1 & keys2) / len(keys1 | keys2) if keys1 | keys2 else 0.0
        
        # Value similarity for common keys
        common_keys = keys1 & keys2
        if not common_keys:
            return key_similarity * 0.5
        
        matching_values = 0
        for key in common_keys:
            if state1.state_data[key] == state2.state_data[key]:
                matching_values += 1
        
        value_similarity = matching_values / len(common_keys)
        
        # Combined similarity
        return (key_similarity + value_similarity) / 2.0
    
    def _learn_pattern(self, transition: StateTransition) -> None:
        """Learn behavior pattern from transition."""
        # Generate pattern ID based on state types
        from_type = transition.from_state.metadata.get("type", "unknown")
        to_type = transition.to_state.metadata.get("type", "unknown")
        pattern_id = f"{from_type}_to_{to_type}"
        
        if pattern_id not in self.behavior_patterns:
            self.behavior_patterns[pattern_id] = BehaviorPattern(pattern_id)
        
        self.behavior_patterns[pattern_id].add_transition(transition)
    
    def add_validation_rule(
        self,
        rule: Callable[[StateSnapshot, StateSnapshot], Tuple[bool, str]]
    ) -> None:
        """
        Add a custom validation rule.
        
        Args:
            rule: Validation function
        """
        self.state_validator.add_rule(rule)
        print(f"[AIC VALIDATOR] Added validation rule")


# Example usage
if __name__ == "__main__":
    print("=== AIC Predictive Validation System Demo ===\n")
    
    # Initialize validator
    validator = AICPredictiveValidator(max_history=100)
    
    # Add validation rule
    def no_backward_version(from_state: StateSnapshot, to_state: StateSnapshot) -> Tuple[bool, str]:
        """Ensure version only increases."""
        from_version = from_state.state_data.get("version", 0)
        to_version = to_state.state_data.get("version", 0)
        
        if to_version < from_version:
            return False, f"Cannot downgrade version from {from_version} to {to_version}"
        return True, ""
    
    validator.add_validation_rule(no_backward_version)
    
    # Record some historical transitions
    print("--- Recording historical transitions ---")
    for i in range(10):
        from_state = validator.record_state(
            f"state_{i}",
            {"version": i, "value": i * 10},
            {"type": "normal"}
        )
        
        to_state = validator.record_state(
            f"state_{i+1}",
            {"version": i + 1, "value": (i + 1) * 10},
            {"type": "normal"}
        )
        
        success = i % 5 != 0  # Fail every 5th transition
        
        validator.record_transition(
            f"trans_{i}",
            from_state,
            to_state,
            success=success,
            duration=0.1 * (i + 1)
        )
    
    # Test prediction
    print("\n--- Testing prediction ---")
    test_from = validator.record_state(
        "test_from",
        {"version": 10, "value": 100},
        {"type": "normal"}
    )
    
    test_to = validator.record_state(
        "test_to",
        {"version": 11, "value": 110},
        {"type": "normal"}
    )
    
    prediction = validator.predict_transition(test_from, test_to)
    print(json.dumps(prediction.to_dict(), indent=2))
    
    # Test invalid transition (version downgrade)
    print("\n--- Testing invalid transition ---")
    invalid_to = validator.record_state(
        "invalid_to",
        {"version": 5, "value": 50},
        {"type": "normal"}
    )
    
    invalid_prediction = validator.predict_transition(test_from, invalid_to)
    print(json.dumps(invalid_prediction.to_dict(), indent=2))
    
    # Get statistics
    print("\n--- Validation Statistics ---")
    stats = validator.get_validation_statistics()
    print(json.dumps(stats, indent=2))
    
    print("\n=== Demo Complete ===")
