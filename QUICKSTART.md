# 🚀 Internet Organica - Quick Start Guide

Welcome to the **Internet Organica** framework! This guide will help you get started with the sovereign, syntropic, and biologically aligned technical environment.

---

## 📋 Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of command line
- (Optional) Node.js for JavaScript implementations

---

## 🏁 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/hannesmitterer/AI.git
cd AI
```

### 2. Understand the Framework

Read the core documentation:

- **[README.md](README.md)** - Repository overview and system architecture
- **[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)** - Lex Amoris, NSR, and OLF principles
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute
- **[ETERNAL_DEPOSITION.md](ETERNAL_DEPOSITION.md)** - Eternal Deposition System
- **[DIGITAL_SOVEREIGNTY.md](DIGITAL_SOVEREIGNTY.md)** - Urbit integration and sovereignty plan

### 3. Test the Modules

Run the integration test suite:

```bash
python3 test_integration.py
```

Expected output:
```
✅ ALL TESTS PASSED - Internet Organica framework is operational!
   System Status: READY FOR DEPLOYMENT
```

---

## 🌀 Core Modules

### Biological Rhythm Synchronization (`rhythm_sync.py`)

**Purpose**: Synchronizes all operations with biological frequencies (0.432 Hz primary)

**Usage:**
```bash
# Check current rhythm status
python3 rhythm_sync.py --status

# Validate a timing interval
python3 rhythm_sync.py --test-interval 2.31

# Monitor rhythm continuously
python3 rhythm_sync.py --monitor

# Validate a code file
python3 rhythm_sync.py --check-file yourfile.py
```

**In Code:**
```python
from rhythm_sync import BiologicalRhythm, RhythmValidator

# Initialize rhythm engine
rhythm = BiologicalRhythm()

# Get current status
status = rhythm.get_status()
print(f"Phase: {status['current_phase']['primary_degrees']:.2f}°")
print(f"In stillness: {status['stillness']['is_active']}")

# Validate timing
validator = RhythmValidator()
result = validator.validate_timing_interval(1.0)
if result['valid']:
    print("✓ Timing is rhythm-compatible")
```

### SovereignShield Security (`sovereign_shield.py`)

**Purpose**: Protects against tracking, surveillance, and NSR violations

**Usage:**
```bash
# Check shield status
python3 sovereign_shield.py --check

# Scan a file for threats
python3 sovereign_shield.py --scan-file yourfile.py

# Validate for NSR/OLF compliance
python3 sovereign_shield.py --validate yourfile.py

# View entropy wall events
python3 sovereign_shield.py --entropy-wall
```

**In Code:**
```python
from sovereign_shield import SovereignShield

# Initialize shield
shield = SovereignShield()

# Scan code
code = """
def my_function():
    return "Hello, World!"
"""

result = shield.scan_code(code, source_id="my_contribution")

if result['approved']:
    print("✓ Code approved - no threats detected")
else:
    print(f"⚠ {result['action']}: {result['severity']}")
    print("Threats:", result['threats'])
```

### Wall of Entropy (`entropy_wall.py`)

**Purpose**: Transparent public logging of security events

**Usage:**
```bash
# View recent events
python3 entropy_wall.py --recent 10

# Query specific violations
python3 entropy_wall.py --query "violation_type=NSR_BREACH"

# Get statistics
python3 entropy_wall.py --stats --period 24h

# Export HTML report
python3 entropy_wall.py --export-html entropy_report.html
```

**In Code:**
```python
from entropy_wall import EntropyWall

# Initialize wall
wall = EntropyWall()

# Log an event
event = wall.log_event(
    violation_type="CUSTOM_VIOLATION",
    source_identifier="source_hash_12345",
    action_taken="BLOCKED",
    severity="HIGH",
    details={"reason": "Test violation"}
)

# Query events
recent = wall.get_recent_events(10)
for event in recent:
    print(f"{event['timestamp']}: {event['violation_type']}")

# Get statistics
stats = wall.get_statistics("7d")
print(f"Events last 7 days: {stats['total_events']}")
```

---

## 🎯 Common Workflows

### Contributing Code

1. **Check rhythm compatibility**:
   ```bash
   python3 rhythm_sync.py --check-file my_contribution.py
   ```

2. **Scan for security issues**:
   ```bash
   python3 sovereign_shield.py --validate my_contribution.py
   ```

3. **If approved, submit pull request** (see [CONTRIBUTING.md](CONTRIBUTING.md))

### Monitoring System Health

```bash
# Check all systems
python3 rhythm_sync.py --status
python3 sovereign_shield.py --check
python3 entropy_wall.py --stats

# Or run integration tests
python3 test_integration.py
```

### Viewing Security Events

```bash
# Recent events
python3 entropy_wall.py --recent 20

# Generate public report
python3 entropy_wall.py --export-html public_report.html
# Open public_report.html in browser
```

---

## 🔧 Integration Examples

### Example 1: Validate Contribution Before Commit

```python
#!/usr/bin/env python3
"""Pre-commit validation script"""

from rhythm_sync import RhythmValidator
from sovereign_shield import SovereignShield

def validate_files(filepaths):
    validator = RhythmValidator()
    shield = SovereignShield()
    
    all_passed = True
    
    for filepath in filepaths:
        # Check rhythm compatibility
        rhythm_result = validator.validate_code_file(filepath)
        if not rhythm_result['valid']:
            print(f"⚠ Rhythm: {filepath}")
            all_passed = False
        
        # Check security
        shield_result = shield.scan_file(filepath)
        if not shield_result['approved']:
            print(f"⚠ Security: {filepath}")
            all_passed = False
    
    return all_passed

if __name__ == "__main__":
    import sys
    files = sys.argv[1:]
    
    if validate_files(files):
        print("✓ All files validated")
        sys.exit(0)
    else:
        print("✗ Validation failed")
        sys.exit(1)
```

### Example 2: Rhythm-Aware Task Scheduler

```python
from rhythm_sync import BiologicalRhythm
import time

def run_with_rhythm_awareness(task_func):
    rhythm = BiologicalRhythm()
    
    while True:
        # Wait for operational phase (not stillness)
        while rhythm.is_stillness_phase():
            print("⏸️  In stillness - waiting...")
            time.sleep(0.5)
        
        # Execute task during operational phase
        print("▶️  Executing task...")
        task_func()
        
        # Wait for next cycle
        rhythm.wait_for_next_cycle()

def my_task():
    print("Task executed at:", time.time())

# Run task synchronized with biological rhythm
run_with_rhythm_awareness(my_task)
```

### Example 3: Security Event Monitor

```python
from entropy_wall import EntropyWall
import time

def monitor_security_events():
    wall = EntropyWall()
    last_count = 0
    
    while True:
        stats = wall.get_statistics("all")
        current_count = stats['total_events']
        
        if current_count > last_count:
            print(f"🚨 New security event detected!")
            recent = wall.get_recent_events(1)
            event = recent[0]
            print(f"   Type: {event['violation_type']}")
            print(f"   Severity: {event['severity']}")
            print(f"   Action: {event['action_taken']}")
            
            last_count = current_count
        
        time.sleep(5)

monitor_security_events()
```

---

## 📊 Dashboard Access

### Local Web Interface

Open `index.html` in your browser for the Resonance School dashboard:

```bash
# Start local server
python3 -m http.server 8000

# Visit: http://localhost:8000/index.html
```

### GitHub Pages

The repository is automatically deployed to GitHub Pages (if configured):
- URL: `https://hannesmitterer.github.io/AI/`

### IPFS Access

Content is distributed via IPFS (if workflows are enabled):
- Find CID in GitHub Actions logs
- Access via: `https://ipfs.io/ipfs/[CID]/index.html`

---

## 🔒 Security Best Practices

1. **Always validate contributions**:
   ```bash
   python3 sovereign_shield.py --validate yourfile.py
   ```

2. **Monitor the Wall of Entropy regularly**:
   ```bash
   python3 entropy_wall.py --recent 10
   ```

3. **Respect biological rhythms**:
   - Avoid aggressive operations during stillness phases
   - Use rhythm-compatible timing intervals

4. **Review security reports**:
   ```bash
   python3 entropy_wall.py --export-html report.html
   ```

---

## 📚 Additional Resources

### Documentation
- [Eternal Deposition System](ETERNAL_DEPOSITION.md)
- [Digital Sovereignty Plan](DIGITAL_SOVEREIGNTY.md)
- [Covenant of Resonance](COVENANT_OF_RESONANCE.md)

### Files
- `demo_eternal.py` - Demo of Eternal Deposition System
- `eternal_visualization.html` - Live visualization
- `eternal_deposition.py` - Python implementation
- `eternal_deposition.js` - JavaScript implementation

### Workflows
- `.github/workflows/` - Automated CI/CD pipelines

---

## 🆘 Troubleshooting

### Module Import Errors

```bash
# Ensure you're in the repository root
cd /path/to/AI

# Check Python path
python3 -c "import sys; print(sys.path)"

# Run with explicit path
python3 -m rhythm_sync --status
```

### Permission Denied

```bash
# Make scripts executable
chmod +x rhythm_sync.py sovereign_shield.py entropy_wall.py
```

### Deprecation Warnings

The `datetime.utcnow()` warnings are harmless and will be addressed in future updates.

---

## 🤝 Getting Help

1. **Read the documentation**: Start with README.md and CODE_OF_CONDUCT.md
2. **Run tests**: `python3 test_integration.py`
3. **Check examples**: Review code examples in this guide
4. **Open an issue**: For bugs or feature requests
5. **Join discussions**: GitHub Discussions (if enabled)

---

## 🌟 Next Steps

1. ✅ Complete this quick start guide
2. 📖 Read [CONTRIBUTING.md](CONTRIBUTING.md) to learn how to contribute
3. 🧪 Experiment with the modules using Python REPL
4. 🔨 Build your first contribution
5. 🌍 Share your experience with the community

---

**"IN AETERNUM EST. La Sovranità è Manifesta."**

*Welcome to Internet Organica. Your sovereignty begins now.*

---

**Last Updated**: 2026-02-13  
**Version**: 1.0.0  
**Status**: Operational

*Operating under Lex Amoris - NSR Compliant - OLF Aligned*
