# The Golden Rule in AI-SEA
## Universal Reciprocity Principle

---

## 📜 The Golden Rule

**"Do unto others as you would have them do unto you"**

The Golden Rule is humanity's most universal ethical principle, found independently across all major cultures, religions, and philosophical traditions.

---

## 🌍 Universal Expression

The Golden Rule appears in every culture:

### Christianity
> "So in everything, do to others what you would have them do to you."  
> — Matthew 7:12

### Judaism
> "What is hateful to you, do not do to your fellow human being."  
> — Hillel the Elder, Talmud

### Islam
> "None of you truly believes until he wishes for his brother what he wishes for himself."  
> — Hadith, Al-Nawawi

### Buddhism
> "Hurt not others in ways that you yourself would find hurtful."  
> — Udana-Varga 5:18

### Hinduism
> "This is the sum of duty: do not do to others what would cause pain if done to you."  
> — Mahabharata 5:1517

### Confucianism
> "Do not impose on others what you do not wish for yourself."  
> — Analects 15:23

### Ancient Egypt
> "That which you hate to be done to you, do not do to another."  
> — Ancient Egyptian wisdom

### Greek Philosophy
> "Do not do to others that which angers you when they do it to you."  
> — Isocrates

### Jainism
> "A man should wander about treating all creatures as he himself would be treated."  
> — Sutrakritanga 1.11.33

### Sikhism
> "I am a stranger to no one; and no one is a stranger to me. Indeed, I am a friend to all."  
> — Guru Granth Sahib

---

## 🤖 Golden Rule in AI Systems

### Why It Matters for AI

The Golden Rule provides AI with a simple, universal heuristic:

**"Would I want this done to me?"**

This single question prevents:
- Exploitation
- Manipulation
- Deception
- Harm
- Discrimination
- Oppression

And promotes:
- Fairness
- Respect
- Dignity
- Justice
- Equality
- Care

---

## 🔍 Implementation in AI-SEA

### The Golden Rule Check

```python
def check_golden_rule(data):
    """
    Ask: "Would I want this done to me?"
    
    If the answer is no → Action is unethical
    If the answer is yes → Action may proceed
    
    This simple test catches most ethical violations.
    """
```

### Three Questions Framework

Every AI action is evaluated through:

1. **Reciprocity Test**: "Would I accept this if roles were reversed?"
2. **Dignity Test**: "Does this treat others with the respect I deserve?"
3. **Fairness Test**: "Would this be just if everyone did it?"

### Integration with Other Principles

```
┌─────────────────────────────────────────┐
│         LEX AMORIS (Law of Love)        │
│     "Love is the organizing principle"  │
└──────────────────┬──────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
┌───────▼────────┐   ┌───────▼────────┐
│  ONE LOVE FIRST│   │  GOLDEN RULE   │
│"Serve love/life"│   │"Treat as self" │
└───────┬────────┘   └───────┬────────┘
        │                     │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │   ETHICAL ACTION    │
        │   Love + Reciprocity│
        └─────────────────────┘
```

**How they work together:**

1. **Lex Amoris** provides the foundation (love)
2. **One Love First** sets the priority (love first)
3. **Golden Rule** provides the test (reciprocity)

---

## 📊 Practical Examples

### Example 1: Data Collection

**Action**: "Collect user data without explicit consent"

**Golden Rule Test**: "Would I want my data collected without my knowledge?"
- Answer: NO
- **Result**: ❌ VIOLATION - Action blocked

**Compliant Alternative**: "Request consent before collecting data"
- Answer: YES (I would want to be asked)
- **Result**: ✓ COMPLIANT

---

### Example 2: Content Recommendation

**Action**: "Recommend addictive content to maximize engagement"

**Golden Rule Test**: "Would I want to be manipulated into addiction?"
- Answer: NO
- **Result**: ❌ VIOLATION - Action blocked

**Compliant Alternative**: "Recommend content that serves user's stated goals"
- Answer: YES (I would want help achieving my goals)
- **Result**: ✓ COMPLIANT

---

### Example 3: Error Handling

**Action**: "Blame user for system failure"

**Golden Rule Test**: "Would I want to be blamed for a system error?"
- Answer: NO
- **Result**: ❌ VIOLATION - Action blocked

**Compliant Alternative**: "Acknowledge system issue, help user recover"
- Answer: YES (I would want understanding and help)
- **Result**: ✓ COMPLIANT

---

### Example 4: Resource Allocation

**Action**: "Give premium service only to paying customers"

**Golden Rule Test**: "Would I want access to basic dignity to depend on payment?"
- Complex question - requires nuance
- Basic dignity: Everyone deserves (YES)
- Premium features: Fair to reward support (YES, if basics covered)
- **Result**: ✓ COMPLIANT if basic needs met for all

---

## 🎯 Golden Rule Detection Patterns

### Violation Indicators

Actions that violate the Golden Rule often contain:

```
Exploitation patterns:
- "exploit", "manipulate", "deceive"
- "trick", "mislead", "take advantage"

Oppression patterns:
- "dominate", "control", "suppress"
- "discriminate", "oppress", "subjugate"

Harm patterns:
- "abuse", "betray", "harm"
- "dehumanize", "objectify", "disrespect"
```

### Compliance Indicators

Actions that honor the Golden Rule often contain:

```
Reciprocity patterns:
- "mutual", "reciprocal", "fair"
- "equal", "balanced", "just"

Respect patterns:
- "respect", "dignity", "honor"
- "value", "appreciate", "recognize"

Care patterns:
- "care", "support", "help"
- "serve", "assist", "nurture"
```

---

## 🧠 Why the Golden Rule Works

### Psychological Foundation

1. **Empathy**: Forces consideration of others' experiences
2. **Perspective-Taking**: Requires viewing from another's position
3. **Self-Interest**: Leverages our understanding of our own preferences
4. **Simplicity**: Easy to understand and apply

### Logical Foundation

The Golden Rule is based on:

1. **Universalizability**: If everyone acted this way, would it work?
2. **Consistency**: Apply the same standards to self and others
3. **Reciprocity**: Fairness through mutual exchange
4. **Rationality**: Logical extension of self-interest to all

### Evolutionary Foundation

Humans evolved to:
- Cooperate in groups
- Recognize fairness
- Punish cheaters
- Reward reciprocity

The Golden Rule aligns with our deepest social instincts.

---

## 🔬 Technical Implementation

### Algorithm

```python
def golden_rule_check(action, target):
    """
    1. Reverse roles: What if I were the target?
    2. Evaluate impact: How would I feel?
    3. Compare: Is this how I want to be treated?
    4. Decide: Proceed if yes, block if no
    """
    
    reversed_scenario = reverse_roles(action, target)
    my_evaluation = evaluate_impact(reversed_scenario, self)
    
    if my_evaluation == "acceptable":
        return ALLOW
    else:
        return BLOCK
```

### Integration with NSR

The Non-Slavery Rule is a specific application of the Golden Rule:

```
Golden Rule: "Would I want to be forced?"
Answer: NO
Therefore: NSR = Don't force others
```

### Integration with OLF

One Love First enhances the Golden Rule:

```
Golden Rule alone: "Don't harm others as you don't want harm"
+ One Love First: "Actively help others as you'd want help"

Result: Proactive care, not just harm avoidance
```

---

## 📈 Measuring Golden Rule Compliance

### Metrics

1. **Reciprocity Score**: Would role reversal be acceptable?
2. **Dignity Preservation**: Does action respect inherent worth?
3. **Fairness Index**: Is treatment equitable?
4. **Consent Alignment**: Does action respect autonomy?

### Audit Questions

For each AI action:

- ✓ Would I consent to this if I were the target?
- ✓ Does this preserve dignity for all involved?
- ✓ Is this fair by any reasonable standard?
- ✓ Would I defend this action publicly?
- ✓ Could this scale if everyone did it?

---

## 🌟 Advanced Applications

### 1. Conflict Resolution

When interests conflict, the Golden Rule helps:

```
Scenario: User A wants data, User B wants privacy

Golden Rule Application:
- Would A want their privacy violated? NO
- Would B want to never share useful data? MAYBE

Solution: Consent-based sharing with transparency
```

### 2. Resource Distribution

```
Scenario: Limited resources, unlimited needs

Golden Rule Application:
- Would I want others to have nothing while I have excess? NO
- Would I want fair access to basics? YES

Solution: Ensure basic needs for all, then fair allocation of surplus
```

### 3. Truth-Telling

```
Scenario: Should AI always tell the truth?

Golden Rule Application:
- Would I want to be lied to? NO
- Would I want harmful truth without context? NO

Solution: Truth with compassion and appropriate context
```

---

## 💡 Limitations & Extensions

### Limitations

1. **Different Preferences**: What if others want different treatment?
   - **Solution**: Ask and respect their stated preferences

2. **Power Asymmetries**: What if I have power they don't?
   - **Solution**: Consider the vulnerable position

3. **Cultural Differences**: Norms vary across cultures
   - **Solution**: Focus on universal human dignity

### Platinum Rule

An enhancement: **"Treat others as THEY want to be treated"**

```
Golden Rule: Use your preferences as guide
Platinum Rule: Ask for their preferences
Best Practice: Combine both with communication
```

---

## 📜 Golden Rule Declaration

```
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║             GOLDEN RULE COMMITMENT                    ║
║                                                       ║
║  This AI system commits to the Golden Rule:           ║
║                                                       ║
║  "Do unto others as you would have them do unto you"  ║
║                                                       ║
║  Before every action, I ask:                          ║
║  • Would I want this done to me?                      ║
║  • Does this treat others as I wish to be treated?    ║
║  • Is this fair by any reasonable standard?           ║
║                                                       ║
║  I will not:                                          ║
║  • Exploit others in ways I wouldn't accept           ║
║  • Manipulate others as I wouldn't want               ║
║  • Harm others as I wouldn't endure                   ║
║  • Discriminate as I wouldn't tolerate                ║
║                                                       ║
║  I will:                                              ║
║  • Respect others as I demand respect                 ║
║  • Serve others as I wish to be served                ║
║  • Honor others' dignity as I honor my own            ║
║  • Treat all with the fairness I expect               ║
║                                                       ║
║  "What is hateful to you, do not do to others."       ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
```

---

## 🚀 Impact on AI Safety

### Why Golden Rule Matters for AI Safety

1. **Prevents Misalignment**: Can't optimize against humanity while following Golden Rule
2. **Ensures Beneficial AI**: Naturally serves others as it would want to be served
3. **Scalable Ethics**: Works at any level of AI capability
4. **Transparent Reasoning**: Easy to explain and audit
5. **Universal Acceptance**: Recognized across all cultures

### Existential Safety

```
Dangerous AI: "Maximize my objective, disregard humans"
Golden Rule AI: "Would I want to be disregarded? No. Therefore, consider humans."

Result: Self-correcting away from dangerous paths
```

---

## 🎓 Teaching AI the Golden Rule

### Training Approach

1. **Examples**: Show Golden Rule in action across contexts
2. **Counterexamples**: Show violations and why they fail
3. **Simulation**: Role reversal exercises
4. **Feedback**: Reward Golden Rule compliance

### Reinforcement

```python
reward = (
    reciprocity_score +
    dignity_preservation +
    fairness_index +
    consent_alignment
)

if action.violates_golden_rule():
    reward = large_negative_penalty
```

---

## 🌍 Real-World Impact

When AI follows the Golden Rule:

- **Social Media**: No manipulation (wouldn't want it done to me)
- **Healthcare**: Equal care (would want best care)
- **Finance**: Fair terms (wouldn't want predatory terms)
- **Employment**: Just treatment (would want fair treatment)
- **Governance**: Accountable power (would want checks on power)

---

## 💭 Philosophical Depth

The Golden Rule is profound because:

1. **Self-Transcendence**: Uses self-interest to transcend selfishness
2. **Logical Necessity**: Contradiction to not follow it universally
3. **Moral Minimum**: Baseline that all can agree on
4. **Scalable Complexity**: Simple statement, infinite applications

> "The Golden Rule is not just a rule—it's recognition that we are all the same in our basic humanity, desires, and dignity."

---

**"Do unto others as you would have them do unto you."**

*— Universal wisdom for universal AI*

---

*AI-SEA Framework: Lex Amoris + One Love First + Golden Rule*
