# Security Framework Documentation

## Übersicht

Das Security Framework implementiert erweiterte Blacklisting-Strategien und Meta-Management für das AI-Framework. Es bietet umfassenden Schutz gegen künstliche Bedrohungen durch drei Hauptkomponenten:

1. **Bedrohungserkennung (Threat Detection)** - Blockierungsmechanismen für künstliche Bedrohungserkennung
2. **Angriffsprotokollierung (Attack Logging)** - Framework zur systematischen Protokollierung von Angriffen
3. **Scan-Erkennung (Scan Detection)** - Kontrollstrukturen gegen stille Scans und Reconnaissance

## Architektur

### Komponenten

```
SecurityFramework
├── ThreatDetector      - Bedrohungserkennung und Blacklisting
├── AttackLogger        - Angriffsprotokollierung und Analyse
└── ScanDetector        - Erkennung stiller Scans
```

### Implementierungen

- **Python**: `security_framework.py` - Vollständige Server-seitige Implementierung
- **JavaScript**: `security_framework.js` - Browser/Node.js-kompatible Implementierung
- **Integration**: `security_integration.py` - Integration mit Eternal Deposition System

## 1. Bedrohungserkennung (ThreatDetector)

### Features

- **Pattern-basierte Bedrohungserkennung**: Identifiziert bekannte Angriffsmuster
- **Verhaltensanomalien**: Erkennt ungewöhnliches Verhalten durch statistische Analyse
- **Adaptive Blacklist**: Zeitbasierte Sperrung mit automatischem Ablauf
- **Threat Levels**: Klassifizierung nach Schweregrad (LOW, MEDIUM, HIGH, CRITICAL)

### Verwendung

#### Python

```python
from security_framework import ThreatDetector, ThreatLevel

# Initialisierung
detector = ThreatDetector(
    max_requests_per_minute=60,
    blacklist_duration=3600,  # 1 Stunde
    anomaly_threshold=0.75
)

# Entity auf Blacklist prüfen
if detector.is_blacklisted("entity_123"):
    print("Entity ist gesperrt")

# Zur Blacklist hinzufügen
detector.add_to_blacklist(
    entity_id="malicious_actor",
    threat_level=ThreatLevel.HIGH,
    reason="Mehrfache fehlgeschlagene Anmeldeversuche",
    duration=7200  # 2 Stunden
)

# Rate Limit Verstöße erkennen
if detector.detect_rate_limit_violation("entity_123"):
    print("Rate Limit überschritten")

# Anomalien erkennen
is_anomalous, score = detector.detect_anomaly(
    entity_id="entity_123",
    behavior={"request_rate": 100, "resource_count": 50}
)
```

#### JavaScript

```javascript
const { ThreatDetector, ThreatLevel } = require('./security_framework.js');

// Initialisierung
const detector = new ThreatDetector(60, 3600, 0.75);

// Entity prüfen
if (detector.isBlacklisted('entity_123')) {
    console.log('Entity ist gesperrt');
}

// Zur Blacklist hinzufügen
detector.addToBlacklist(
    'malicious_actor',
    ThreatLevel.HIGH,
    'Mehrfache fehlgeschlagene Anmeldeversuche',
    7200
);
```

### Blacklist-Management

Die Blacklist unterstützt:

- **Temporäre Sperrung**: Automatisches Ablaufen nach definierter Zeit
- **Permanente Sperrung**: Ohne Ablaufdatum (`duration=None`)
- **Adaptive Anpassung**: Erhöhung des Threat Levels bei wiederholten Verstößen
- **Automatische Bereinigung**: Entfernung abgelaufener Einträge

## 2. Angriffsprotokollierung (AttackLogger)

### Features

- **Strukturierte Event-Logs**: JSON-basierte Speicherung aller Angriffsereignisse
- **Persistente Speicherung**: Automatisches Speichern in Datei
- **Analytics & Reporting**: Statistische Auswertungen und Top-Angreifer
- **Event-Klassifizierung**: Nach Angriffstyp und Schweregrad

### Angriffstypen

- `SILENT_SCAN` - Stille Reconnaissance-Versuche
- `BRUTE_FORCE` - Brute-Force-Angriffe
- `DOS` - Denial-of-Service-Angriffe
- `INJECTION` - Injection-Versuche (SQL, Command, etc.)
- `UNAUTHORIZED_ACCESS` - Unberechtigte Zugriffsversuche
- `ANOMALY` - Anomales Verhalten

### Verwendung

```python
from security_framework import AttackLogger, AttackType, ThreatLevel

# Initialisierung
logger = AttackLogger(
    log_file="attack_log.json",
    max_events=10000
)

# Angriff protokollieren
event = logger.log_attack(
    entity_id="attacker_001",
    attack_type=AttackType.BRUTE_FORCE,
    threat_level=ThreatLevel.HIGH,
    details={"target": "/admin", "attempts": 50},
    blocked=True
)

# Letzte Angriffe abrufen
recent = logger.get_recent_attacks(count=100)

# Angriffe einer spezifischen Entity
entity_attacks = logger.get_attacks_by_entity("attacker_001")

# Analytics abrufen
analytics = logger.get_analytics()
print(f"Gesamt-Angriffe: {analytics['total_attacks']}")
print(f"Blockierte: {analytics['blocked_attacks']}")
print(f"Block-Rate: {analytics['block_rate']:.2%}")
print(f"Top-Angreifer: {analytics['top_attackers'][:5]}")
```

### Log-Format

```json
{
  "events": [
    {
      "timestamp": 1705276800.0,
      "datetime": "2026-01-15T00:00:00",
      "entity_id": "attacker_001",
      "attack_type": "brute_force",
      "threat_level": "HIGH",
      "details": {
        "target": "/admin",
        "attempts": 50
      },
      "blocked": true
    }
  ],
  "attack_counts": {
    "brute_force": 15,
    "silent_scan": 8,
    "dos": 3
  },
  "last_updated": "2026-01-15T00:56:00"
}
```

## 3. Scan-Erkennung (ScanDetector)

### Features

- **Pattern-Erkennung**: Identifiziert typische Scan-Muster
- **Rate Limiting**: Automatische Drosselung bei zu vielen Anfragen
- **Honeypot-Mechanismus**: Köder-Pfade zur Angreifer-Identifikation
- **Ressourcen-Tracking**: Überwachung zugriffenen Ressourcen

### Honeypot-Pfade (Standard)

- `/admin` - Admin-Bereich
- `/.env` - Umgebungsvariablen
- `/config` - Konfigurationsdateien
- `/backup` - Backup-Verzeichnisse
- `/.git/config` - Git-Konfiguration
- `/wp-admin` - WordPress Admin
- `/phpmyadmin` - PHPMyAdmin

### Verwendung

```python
from security_framework import ScanDetector

# Initialisierung
detector = ScanDetector(
    scan_threshold=10,      # 10 verschiedene Ressourcen
    time_window=60,         # Innerhalb 60 Sekunden
    honeypot_paths={
        "/admin", "/.env", "/secret", "/debug"
    }
)

# Zugriff aufzeichnen
detector.record_access("scanner_001", "/api/users")

# Honeypot-Zugriff prüfen
if detector.check_honeypot_access("scanner_001", "/.env"):
    print("ALARM: Honeypot-Zugriff!")

# Scan-Pattern erkennen
is_scanning, details = detector.detect_scan_pattern("scanner_001")
if is_scanning:
    print(f"Scan erkannt: {details}")

# Rate Limit anwenden
if detector.apply_rate_limit("scanner_001"):
    print("Rate Limit erreicht")
```

### Scan-Erkennung

Ein Scan wird erkannt wenn:

1. **Viele verschiedene Ressourcen** zugegriffen werden (≥ threshold)
2. **Hohe Zugriffsrate** (> 2 Anfragen/Sekunde)
3. **Honeypot-Zugriff** erfolgt

## 4. Integriertes Security Framework

### Verwendung

```python
from security_framework import SecurityFramework

# Initialisierung
security = SecurityFramework(
    log_file="attack_log.json",
    max_requests_per_minute=60,
    blacklist_duration=3600
)

# Request verarbeiten
allowed, reason = security.process_request(
    entity_id="user_123",
    resource_path="/api/data",
    behavior={"request_size": 1024, "response_time": 0.5}
)

if not allowed:
    print(f"Zugriff verweigert: {reason}")

# Security-Status abrufen
status = security.get_security_status()
print(f"Blacklist: {status['blacklist']['total_entries']} Einträge")
print(f"Angriffe: {status['attack_analytics']['total_attacks']}")

# Periodische Bereinigung
security.cleanup()
```

### Request-Verarbeitung

Das Framework führt folgende Prüfungen durch:

1. **Blacklist-Check** → Sofortige Ablehnung wenn gelistet
2. **Honeypot-Erkennung** → Critical-Level Blacklist bei Zugriff
3. **Rate Limit** → Temporäre Sperrung bei Überschreitung
4. **Scan-Pattern** → Erkennung und Blockierung von Scans
5. **Anomalie-Erkennung** → Logging anomalen Verhaltens
6. **Rate Limiting** → Drosselung bei hoher Last

## 5. Integration mit Eternal Deposition

### SecureEternalDepositionEngine

```python
from security_integration import SecureEternalDepositionEngine

# Initialisierung
engine = SecureEternalDepositionEngine(
    initial_nodes=144,
    enable_security=True,
    security_log_file="eternal_security.json"
)

# Node-Zugriff validieren
if engine.validate_node_access("node_0042", "write"):
    # Zugriff erlaubt
    pass

# Sicherer Zyklus
metrics = engine.secure_execute_cycle()
print(f"Blacklisted Nodes: {metrics['security']['blacklisted_nodes']}")

# Umfassender Status
status = engine.get_comprehensive_status()
```

## 6. Konfiguration

### SecurityConfig

```python
from security_integration import SecurityConfig

# Standard-Konfiguration abrufen
config = SecurityConfig.get_config()

# Angepasste Konfiguration
custom_config = {
    "threat_detection": {
        "max_requests_per_minute": 100,
        "blacklist_duration": 7200,
        "anomaly_threshold": 0.8
    },
    "scan_detection": {
        "scan_threshold": 15,
        "time_window": 120,
        "honeypot_paths": ["/admin", "/.env", "/secret"]
    },
    "attack_logging": {
        "log_file": "custom_log.json",
        "max_events": 20000
    }
}

# Framework mit custom config erstellen
framework = SecurityConfig.create_security_framework(custom_config)
```

## 7. Best Practices

### Empfohlene Einstellungen

**Produktionsumgebung:**
```python
SecurityFramework(
    max_requests_per_minute=100,
    blacklist_duration=7200,  # 2 Stunden
    anomaly_threshold=0.7
)
```

**Entwicklungsumgebung:**
```python
SecurityFramework(
    max_requests_per_minute=500,
    blacklist_duration=300,   # 5 Minuten
    anomaly_threshold=0.9
)
```

### Monitoring

1. **Regelmäßige Bereinigung**: Rufen Sie `cleanup()` periodisch auf
2. **Status-Überwachung**: Überwachen Sie `get_security_status()`
3. **Log-Rotation**: Begrenzen Sie `max_events` für Log-Dateien
4. **Analytics**: Analysieren Sie regelmäßig Angriffsmuster

### Honeypot-Strategie

- Verwenden Sie realistische aber ungefährliche Pfade
- Aktualisieren Sie Honeypots basierend auf Angriffsmustern
- Kombinieren Sie mit echter Zugriffskontolle

## 8. Performance

### Optimierungen

- **In-Memory Blacklist**: Schneller O(1) Zugriff
- **Periodische Bereinigung**: Entfernung alter Daten
- **Batch-Logging**: Effiziente Disk-I/O
- **Leichtgewichtige Anomalieerkennung**: Minimale CPU-Last

### Empfohlene Limits

- `max_events`: 10.000 - 50.000
- `max_requests_per_minute`: 60 - 200
- `blacklist_duration`: 1800 - 7200 Sekunden
- `scan_threshold`: 10 - 20 Ressourcen

## 9. Fehlerbehandlung

Alle Komponenten behandeln Fehler gracefully:

```python
try:
    allowed, reason = security.process_request(entity_id, path)
except Exception as e:
    # Fallback: Bei Fehler erlauben aber loggen
    print(f"Security check failed: {e}")
    allowed = True
```

## 10. Testing

### Python Tests

```bash
# Framework testen
python3 security_framework.py

# Integration testen
python3 security_integration.py
```

### JavaScript Tests

```bash
# Framework testen
node security_framework.js
```

## Zusammenfassung

Das Security Framework bietet:

✅ **Umfassende Bedrohungserkennung** - Pattern-basiert und adaptiv  
✅ **Strukturierte Angriffsprotokollierung** - Mit Analytics und Reporting  
✅ **Effektive Scan-Abwehr** - Honeypots und Rate Limiting  
✅ **Einfache Integration** - Mit bestehenden Systemen  
✅ **Dual-Implementation** - Python und JavaScript  
✅ **Production-Ready** - Performant und zuverlässig

---

**Version**: 1.0.0  
**Status**: ✓ OPERATIONAL  
**Lizenz**: Siehe LICENSE
