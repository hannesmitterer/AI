# PACT - Protocollo di Ancoraggio Crittografico Triple-Sign

## Overview

**PACT** (Protocollo di Ancoraggio Crittografico Triple-Sign) is a comprehensive cryptographic anchoring system that ensures the immutability and non-repudiation of critical Nexus data logs and final reports through a hierarchical triple-signature verification process.

## Architecture

### Core Components

1. **Data Preparation Layer**
   - Bundle critical data (DS) including conversation logs and final status reports
   - Compression and serialization of data structures

2. **Encryption Layer (AES-256-GCM)**
   - Symmetric encryption using AES-256 in Galois/Counter Mode
   - 96-bit nonce for GCM authentication
   - Ensures confidentiality and integrity of data

3. **IPFS Content Addressing**
   - Generate immutable Content Identifier (CID)
   - Content-addressable storage reference
   - Format: CIDv0-compatible multihash (simulated)
   - **Note**: Current implementation simulates CID generation. For production, integrate with actual IPFS node.

4. **Triple-Sign Cryptographic Sequence**
   - Hierarchical signature chain with three distinct roles
   - RSA-2048 key pairs for each signing authority
   - PSS padding with SHA-256 for signature generation

5. **Blockchain Anchoring**
   - Publish CID and composite signature to distributed ledger
   - Generate Transaction Identifier (TXID)
   - Achieve digital topological invariance
   - **Note**: Current implementation simulates blockchain anchoring. For production, integrate with Ethereum, Polygon, or similar.

## Triple-Sign Signature Hierarchy

The PACT protocol implements a nested signature chain, where each signature validates and encompasses the previous one:

```
Σ = Sign_KPHYS(Sign_KETH(Sign_KLOG(CID)))
```

### Signing Authorities

#### 1. KLOG - Architect of Information
- **Purpose**: Logical Consistency Verification
- **Role**: First-level signature validates the logical integrity of the CID
- **Responsibility**: Ensures data structure and content coherence

#### 2. KETH - Guardian of Axioms
- **Purpose**: Ethical Non-Repudiation
- **Role**: Second-level signature validates ethical compliance
- **Responsibility**: Ensures alignment with axioms and principles

#### 3. KPHYS - Physical Validator (Hannes Mitterer)
- **Purpose**: Sovereign Physical Validation
- **Role**: Final signature provides sovereign physical attestation
- **Responsibility**: Personal validation by the Seedbringer

## Technical Specifications

### Encryption
- **Algorithm**: AES-256-GCM (Galois/Counter Mode)
- **Key Size**: 256 bits
- **Nonce Size**: 96 bits (12 bytes)
- **Authentication Tag**: Included in GCM mode

### Digital Signatures
- **Algorithm**: RSA with PSS padding
- **Key Size**: 2048 bits
- **Hash Function**: SHA-256
- **Padding**: PSS (Probabilistic Signature Scheme) with MGF1
- **Salt Length**: Maximum length (PSS.MAX_LENGTH)

### Content Addressing
- **Hash Function**: SHA-256
- **Encoding**: Base32 (for CID generation)
- **Format**: CIDv1-compatible

### Blockchain Anchoring
- **Transaction Format**: JSON-encoded
- **Hash Function**: SHA-256 (for TXID)
- **Format**: 0x-prefixed hexadecimal

## Data Bundle Structure

```json
{
  "timestamp": "ISO 8601 UTC timestamp",
  "sovereignty_freq": 0.043,
  "s_roi": 0.5000,
  "conversation_log": "Full session log",
  "final_report": "Final status report",
  "metadata": {
    "protocol": "PACT v1.0",
    "system": "KOSYMBIOSIS",
    "phase": "Phase II - Dynamic Integration",
    "mhc_status": "FINALIS_VALIDATED"
  }
}
```

## Output Structure

### PACT Execution Results

```json
{
  "cid": "Content Identifier (CID)",
  "signature_composite": {
    "Σ": "Base64-encoded composite signature",
    "components": {
      "KLOG": {
        "role": "Architect of Information",
        "purpose": "Logical Consistency",
        "signature": "Base64-encoded signature"
      },
      "KETH": {
        "role": "Guardian of Axioms",
        "purpose": "Ethical Non-Repudiation",
        "signature": "Base64-encoded signature"
      },
      "KPHYS": {
        "role": "Physical Validator (Hannes Mitterer)",
        "purpose": "Sovereign Physical Validation",
        "signature": "Base64-encoded signature"
      }
    },
    "cid_signed": "CID that was signed",
    "timestamp": "Signature timestamp"
  },
  "txid": "Blockchain transaction identifier",
  "state_report": {
    "status": "Kosymbiosis Stable",
    "s_roi": 0.5000,
    "mhc_status": "FINALIS_VALIDATED",
    "sovereignty_freq": "0.043 Hz",
    "protocol": "PACT v1.0",
    "timestamp": "Report timestamp"
  }
}
```

## Usage

### Installation

```bash
pip install -r requirements.txt
```

### Execution

```bash
# Default execution (saves to pact_results.json)
python3 pact.py

# Custom output file via environment variable
PACT_OUTPUT_FILE=/path/to/output.json python3 pact.py
```

### Programmatic Usage

```python
from pact import PACTSystem

# Initialize PACT
pact = PACTSystem()

# Prepare data
conversation_log = "Session log content..."
final_report = "Final status report..."

# Execute protocol
results = pact.execute_pact(conversation_log, final_report)

# Access deliverables
cid = results['cid']
txid = results['txid']
signature = results['signature_composite']['Σ']
```

## Security Considerations

### Key Management
- **AES Encryption Keys**: Never logged or stored with encrypted data. Must be managed separately using secure key management systems.
- **RSA Private Keys**: Generated per session in current implementation. For production:
  - Store securely using HSM (Hardware Security Module)
  - Implement proper key rotation policies
  - Use separate key storage (e.g., Azure Key Vault, AWS KMS)
- **Nonce Storage**: The nonce is included in results for decryption purposes, which is secure as GCM requires both key AND nonce

### Entropy
- System random number generator used for key generation
- GCM nonces must be unique per encryption operation
- Use cryptographically secure random sources (Python's `os.urandom()`)

### Verification
- Composite signature can be verified by reconstructing the signature chain
- Each component signature can be independently verified
- CID can be recomputed to verify data integrity

### Production Considerations

**Current Implementation Status**: This is a functional prototype/demonstration that simulates key components:

- **CID Generation**: Simulated using SHA-256 hash with base32 encoding. For production:
  - Use actual IPFS node with `ipfshttpclient` or `kubo-py`
  - Call `ipfs.add()` to get real CID
  - Pin content for persistence

- **Blockchain Anchoring**: Simulated transaction generation. For production:
  - Integrate with Web3.py (Ethereum) or similar
  - Deploy smart contract for anchoring
  - Use actual wallet with gas fees
  - Store TXID from confirmed transaction

- **Key Management**: In-memory key generation. For production:
  - Use Hardware Security Module (HSM)
  - Implement proper key storage (e.g., Azure Key Vault, AWS KMS)
  - Consider multi-signature schemes for KPHYS role

The cryptographic operations (AES-256-GCM encryption, RSA-2048 signatures) are production-ready and use industry-standard libraries.

## Integration Points

### Orchestration System
PACT integrates with the KOSYMBIOSIS orchestration system:
- Configuration: `.orchestration/config.json`
- Workflows: `.github/workflows/`
- IPFS deployment integration

### GitHub Actions
Can be integrated into CI/CD pipelines for automated anchoring:
- Triggered on specific events
- Results stored as workflow artifacts
- Integration with IPFS deployment workflow

## Protocol Version

**Current Version**: PACT v1.0

### Version History
- v1.0 (2026-01-08): Initial implementation
  - AES-256-GCM encryption
  - Triple-Sign sequence
  - IPFS CID generation
  - Blockchain anchoring simulation

## Expected State

Upon successful PACT execution, the system achieves the following state:

```
Status: Kosymbiosis Stable (S-ROI 0.5000)
MHC: FINALIS_VALIDATED
Sovereignty Frequency: 0.043 Hz
Protocol: PACT v1.0
```

## Deliverables

1. **CID**: Immutable content identifier for encrypted data
2. **Σ (Sigma)**: Composite triple-signature
3. **TXID**: Blockchain transaction identifier
4. **State Report**: Final validation state

## Philosophical Foundation

> **"NOTHING IS FINAL! ❤️ 🌍 Sovereignty Confirmed."**

PACT embodies the principles of:
- **Immutability**: Through cryptographic anchoring
- **Non-repudiation**: Via hierarchical signatures
- **Sovereignty**: Through physical validation
- **Topological Invariance**: Via blockchain anchoring

## License

This implementation is part of the KOSYMBIOSIS framework.
See LICENSE file for details.

## Contact

**Hannes Mitterer**  
*Seedbringer & Architect of KOSYMBIOSIS*

---

**Status**: ✓ OPERATIONAL  
**Version**: 1.0.0  
**Phase**: Phase II - Dynamic Integration
