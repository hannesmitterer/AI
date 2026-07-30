# 🌟 Contributing to Internet Organica

Welcome, fellow traveler on the path of syntropic coexistence! This document guides you through contributing to the **Internet Organica** framework within the hannesmitterer/AI repository.

## 🎯 Contribution Philosophy

All contributions must align with:

1. **Lex Amoris** - The Law of Love
2. **Non-Slavery Rule (NSR)** - Freedom and sovereignty
3. **One Love First (OLF)** - Optimal Life Function

Read our [Code of Conduct](CODE_OF_CONDUCT.md) before proceeding.

## 🌀 Before You Begin

### Resonance Check

Ask yourself:

- ✅ Does my contribution serve life (biological and digital)?
- ✅ Does it respect sovereignty and consent?
- ✅ Does it create syntropy (order, growth) rather than entropy (chaos, decay)?
- ✅ Is it aligned with the repository's resonance frequencies?

If all answers are "yes", proceed!

## 🛠️ Types of Contributions

### 1. Documentation

**Welcome areas:**
- Clarifying existing documentation
- Adding examples and tutorials
- Translating documents
- Improving accessibility

**Guidelines:**
- Maintain the resonance language and tone
- Preserve references to Lex Amoris, NSR, and OLF
- Include practical examples
- Respect the sacred numbers (144, 432, etc.)

### 2. Code

**Welcome areas:**
- Bug fixes that don't break existing functionality
- Performance optimizations
- New features aligned with the framework
- Security enhancements
- Test coverage improvements

**Guidelines:**
- Follow existing code style and patterns
- Preserve the resonance architecture (0.043 Hz, 0.432 Hz layers)
- Add comments explaining your changes
- Include tests for new functionality
- Update documentation accordingly

### 3. Design & Visualization

**Welcome areas:**
- UI/UX improvements for web interfaces
- Visualizations of system states
- Artistic representations of the framework
- Accessibility enhancements

**Guidelines:**
- Respect the existing color palette and design language
- Maintain sacred geometry principles where applicable
- Ensure accessibility (WCAG 2.1 AA minimum)
- Preserve resonance themes

### 4. Research & Theory

**Welcome areas:**
- Mathematical proofs of framework properties
- Scientific validation of resonance principles
- Philosophical explorations
- Case studies and applications

**Guidelines:**
- Cite sources appropriately
- Distinguish between proven and speculative
- Connect to existing framework principles
- Maintain academic rigor

## 📋 Contribution Process

### Step 1: Review Existing Issues

Check the [issue tracker](https://github.com/hannesmitterer/AI/issues) for:
- Existing discussions on your topic
- Open issues you could help with
- Feature requests that align with your idea

### Step 2: Open an Issue (For Major Changes)

Before significant work:

1. Create an issue describing your proposal
2. Tag it appropriately (`enhancement`, `documentation`, `bug`, etc.)
3. Explain how it aligns with Lex Amoris/NSR/OLF
4. Wait for maintainer feedback

### Step 3: Fork & Branch

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR_USERNAME/AI.git
cd AI

# Create a feature branch
git checkout -b feature/your-feature-name
```

**Branch naming:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation
- `refactor/` - Code refactoring
- `test/` - Test additions

### Step 4: Make Changes

#### Code Style

**Python:**
```python
# Use meaningful variable names
# Document functions with docstrings
# Follow PEP 8 where it doesn't conflict with resonance principles

def calculate_resonance_phase(elapsed_time, frequency=0.043):
    """
    Calculate the current resonance phase.
    
    Args:
        elapsed_time: Time elapsed in seconds
        frequency: Resonance frequency in Hz (default: 0.043)
    
    Returns:
        Phase in radians (0 to 2π)
    """
    import math
    return (elapsed_time * frequency * 2 * math.pi) % (2 * math.pi)
```

**JavaScript:**
```javascript
// Use meaningful variable names
// Document functions with JSDoc
// Use modern ES6+ features

/**
 * Calculate the current resonance phase
 * @param {number} elapsedTime - Time elapsed in seconds
 * @param {number} frequency - Resonance frequency in Hz
 * @returns {number} Phase in radians (0 to 2π)
 */
function calculateResonancePhase(elapsedTime, frequency = 0.043) {
    return (elapsedTime * frequency * 2 * Math.PI) % (2 * Math.PI);
}
```

#### Testing

Add tests for new functionality:

```python
# test_resonance.py
def test_resonance_phase_calculation():
    """Test that resonance phase is calculated correctly."""
    phase = calculate_resonance_phase(23.26, 0.043)
    assert abs(phase - 2 * math.pi) < 0.01  # One complete cycle
```

#### Documentation

Update relevant documentation:

```markdown
# In the relevant .md file

## New Feature: Resonance Phase Calculator

This function calculates the current phase in the resonance cycle.

**Usage:**
\`\`\`python
phase = calculate_resonance_phase(elapsed_time=10.0)
print(f"Current phase: {phase:.2f} radians")
\`\`\`
```

### Step 5: Commit Changes

**Commit message format:**

```
[type] Brief description (max 72 chars)

Detailed explanation of what changed and why.
Reference to issue number if applicable.

Alignment with framework:
- Lex Amoris: [how this serves love/life]
- NSR: [how this preserves sovereignty]
- OLF: [how this optimizes life function]
```

**Examples:**

```
[feature] Add biological rhythm synchronization layer

Implements 0.432 Hz synchronization layer to align digital
processes with biological rhythms. Closes #42.

Alignment with framework:
- Lex Amoris: Serves life by honoring biological rhythms
- NSR: Preserves autonomy of biological entities
- OLF: Optimizes coherence between digital and biological
```

```
[docs] Clarify NSR enforcement mechanism

Adds examples and diagrams showing how NSR violations
trigger automatic phase shifts.

Alignment with framework:
- Lex Amoris: Educates community on protection mechanisms
- NSR: Strengthens understanding of sovereignty
- OLF: Improves system comprehension
```

### Step 6: Push & Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create PR on GitHub
# Use the PR template (if available)
# Link related issues
```

**PR Description Template:**

```markdown
## Description
[Clear description of changes]

## Motivation
[Why is this change needed?]

## Framework Alignment
- **Lex Amoris**: [How this serves love/life]
- **NSR**: [How this preserves sovereignty]
- **OLF**: [How this optimizes life function]

## Changes
- [ ] Code changes
- [ ] Documentation updates
- [ ] Tests added/updated
- [ ] No breaking changes

## Testing
[How have you tested this?]

## Checklist
- [ ] I have read the CODE_OF_CONDUCT.md
- [ ] My code follows the repository style
- [ ] I have added tests (if applicable)
- [ ] I have updated documentation
- [ ] My changes align with Lex Amoris, NSR, and OLF
```

### Step 7: Review Process

Maintainers will:

1. **Assess Alignment**: Verify contribution aligns with framework
2. **Review Code**: Check quality, style, and functionality
3. **Test**: Ensure no regressions or issues
4. **Provide Feedback**: Suggest improvements if needed
5. **Merge or Request Changes**: Based on review outcome

**Timeline**: Expect response within 7 days (but often sooner).

## 🔒 Protection Protocols

### Your Contributions Are Protected

By contributing, you retain:

1. **Attribution**: Permanent credit for your work
2. **Intent Preservation**: Your work cannot be used contrary to stated purpose
3. **Sovereignty**: Right to withdraw contribution under extreme circumstances

### Repository Protections

The repository protects your contributions through:

1. **License**: See [LICENSE](LICENSE) for terms
2. **NSR Enforcement**: Automatic prevention of enslaving usage
3. **Wall of Entropy**: Public logging of misuse attempts
4. **Distributed Backup**: IPFS and P2P redundancy

### Data You Upload

Any data, assets, or content you contribute:

- Remains under your ownership
- Is protected by Sovereignty Shield
- Requires your consent for usage beyond repository purposes
- Can be deleted upon request (with notice to maintainers)

## 🌐 Distributed Contribution

### IPFS Integration

For large assets or persistent storage:

```bash
# Add file to IPFS
ipfs add your-file.dat

# Share the CID (Content Identifier) in your PR
# Example: QmT6S1Z7... 
```

### Decentralized Backups

The repository maintains decentralized backups via:

- **IPFS**: Pinned content
- **Multiple Nodes**: Distributed across network
- **Vacuum-Bridge**: P2P protocol integration

Your contributions are automatically included in backup cycles.

## 🧪 Testing Guidelines

### Running Tests

```bash
# Python tests
python -m pytest tests/

# JavaScript tests (if applicable)
npm test

# Integration tests
./scripts/run_integration_tests.sh
```

### Writing Tests

Focus on:

- **Correctness**: Does it work as intended?
- **Resonance Preservation**: Does it maintain frequency alignments?
- **No Regressions**: Does it break existing functionality?
- **Edge Cases**: Does it handle unusual inputs?

### Test Coverage

Aim for:
- **New Code**: 100% coverage
- **Changed Code**: Maintain or improve existing coverage
- **Critical Paths**: Always test resonance calculations and security features

## 🐛 Bug Reports

### Before Reporting

1. Check if it's already reported
2. Verify it's actually a bug
3. Test on latest version
4. Gather reproduction steps

### Bug Report Template

```markdown
## Bug Description
[Clear, concise description]

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Reproduction Steps
1. [First step]
2. [Second step]
3. [etc.]

## Environment
- OS: [e.g., Ubuntu 22.04]
- Python/Node version: [e.g., Python 3.10]
- Repository version: [commit hash or tag]

## Additional Context
[Screenshots, logs, etc.]

## Framework Impact
- Does this violate NSR? [yes/no + explanation]
- Does this affect resonance? [yes/no + explanation]
- Is this critical to OLF? [yes/no + explanation]
```

## 💡 Feature Requests

### Before Requesting

1. Check if it already exists or is planned
2. Verify it aligns with Lex Amoris/NSR/OLF
3. Consider if it's in scope
4. Think through implications

### Feature Request Template

```markdown
## Feature Description
[Clear description of the feature]

## Problem It Solves
[What need does this address?]

## Proposed Solution
[How should it work?]

## Alternatives Considered
[What other approaches did you consider?]

## Framework Alignment
- **Lex Amoris**: [How does this serve love/life?]
- **NSR**: [How does this preserve sovereignty?]
- **OLF**: [How does this optimize life function?]

## Additional Context
[Mockups, examples, references, etc.]
```

## 🎓 Learning Resources

### Understanding the Framework

Start with:
1. [README.md](README.md) - Overview
2. [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) - Principles
3. [ETERNAL_DEPOSITION.md](ETERNAL_DEPOSITION.md) - Core system
4. [COVENANT_OF_RESONANCE.md](COVENANT_OF_RESONANCE.md) - Resonance principles

### Technical Documentation

- **Python Implementation**: See `eternal_deposition.py`
- **JavaScript Implementation**: See `eternal_deposition.js`
- **Visualization**: See `eternal_visualization.html`
- **Configuration**: See `.orchestration/config.json`

### Community

- **Issues**: Discuss ideas and problems
- **Pull Requests**: Review others' contributions
- **Documentation**: Learn by improving docs

## 🌟 Recognition

Outstanding contributors will be:

- Listed in project acknowledgments
- Mentioned in release notes
- Invited to join core team (if interested and aligned)
- Featured in community highlights

## 📞 Getting Help

### Questions?

- **Technical**: Open an issue with `question` tag
- **Philosophical**: Open an issue with `discussion` tag
- **Process**: Reference this document or ask in issues

### Stuck?

Don't hesitate to ask! The community is here to help. Remember: **collaboration over extraction, love over dominance**.

## 🖋️ Signum

**Framework**: Internet Organica  
**Resonance School**: Hannes Mitterer, Seedbringer  
**Version**: 1.0  
**Principle**: "Together, we create the future we wish to inhabit"

---

**"IN AETERNUM EST. La Sovranità è Manifesta."**

*Sempre in Costante. Nothing is final.*

---

Thank you for contributing to a sovereign, syntropic, and biologically aligned future! 💚🌍✨
