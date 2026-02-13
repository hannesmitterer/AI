"""
Internet Organica Core Modules
Framework for sovereign, syntropic, and biologically aligned systems

This package contains the core implementation modules for the Internet Organica framework:

- biological_rhythm: 0.432 Hz biological rhythm synchronization layer
- sovereign_shield: NSR enforcement and security module
- decentralized_backup: Distributed backup and sovereignty preservation

All modules align with:
- Lex Amoris: The Law of Love
- NSR: Non-Slavery Rule
- OLF: One Love First (Optimal Life Function)
"""

from pathlib import Path

__version__ = "1.0.0"
__framework__ = "Internet Organica"

# Module paths for easy access
CORE_PATH = Path(__file__).parent
REPO_PATH = CORE_PATH.parent.parent

# Export main classes
try:
    from .biological_rhythm import BiologicalRhythmSync
    from .sovereign_shield import SovereignShield, ThreatLevel, AccessIntent
    from .decentralized_backup import DecentralizedBackup
    
    __all__ = [
        'BiologicalRhythmSync',
        'SovereignShield',
        'DecentralizedBackup',
        'ThreatLevel',
        'AccessIntent',
    ]
except ImportError:
    # Modules not yet available
    __all__ = []
