# KOSYMBIOSIS AI - Phase II Core Configuration

## Overview

This repository contains the operational configuration for the **KOSYMBIOSIS** governance system Phase II deployment. The primary artifact is the `euystacio.core.v2.bin` configuration file, which encodes strategic decisions into immutable runtime parameters for distributed node operations.

## Binary Asset: euystacio.core.v2.bin

### File Role and Purpose

The `euystacio.core.v2.bin` file serves as the **core configuration specification** for Phase II of the KOSYMBIOSIS project. This file:

- **Documents Strategic Parameters**: Describes the binary format that encodes high-level governance decisions into concrete operational parameters
- **Ensures Consistency**: Provides a specification for the configuration format used by K-SYNC Daemon nodes
- **Defines Immutable Structure**: Documents the configuration parameters that are fixed at distribution time and cannot be altered at runtime
- **Enables Verification**: Specifies the binary structure including cryptographic headers and validation fields

**Note**: This file is a text-based specification document that describes the binary configuration format. For actual binary distribution, K-SYNC Daemon nodes generate or receive the compiled binary based on this specification.

### Binary Structure and Metadata Specification

The configuration file documents a structured binary format with the following fields:

| Byte Range | Field Name | Binary Value | Operational Meaning |
|------------|------------|--------------|---------------------|
| `0x00-0x07` | **MAGIC HEADER** | `45 55 59 53 54 41 43 49` | File identifier "EUYSTACI" - validates file format |
| `0x08-0x0B` | **VERSIONE FW** | `02 00 00 00` | Firmware version 2.0.0 (Phase II) |
| `0x0C-0x0F` | **TFK MINT TARGET** | `00 00 40 40` | Minimum TFK requirement (4.0) for operation |
| `0x10-0x17` | **CID RADICE FW** | `51 4D 54 36 53 31 5A 37` | IPFS hash of Master Document (QmT6S1Z7...) |
| `0x18-0x19` | **RED CODE ANCHOR** | `FF 00` | Anchoring status: Active |
| `0x1A-0x1B` | **MIN CONSENSO %** | `00 88` | Minimum consensus requirement: 88% for Phase II commitments |
| `0x1C-0x1D` | **WÄCHTER MODE** | `01 01` | IANUS mode: Active/Vigilant |
| `0x1E-0x1F` | **ECD PROTOCOL ID** | `51 45` | Protocol identifier: Quick-Ethical (QE) |

### Complete Binary Representation

```
4555595354414349 02000000 00004040 514d543653315a37 FF00 0088 0101 5145
```

## How to Use This Configuration

### For End Users

1. **Download the Configuration Specification**: The configuration file is available directly from this repository
   ```bash
   wget https://raw.githubusercontent.com/hannesmitterer/AI/main/euystacio.core.v2.bin
   ```

2. **View the Specification**: The file contains human-readable documentation of the binary structure
   ```bash
   cat euystacio.core.v2.bin
   ```

3. **Understand the Binary Format**: Review the byte range specifications to understand how configuration data should be encoded in the actual binary format used by nodes

### For System Integrators

1. **K-SYNC Daemon Integration**: 
   - K-SYNC Daemons use this specification to understand the binary configuration format
   - The binary configuration data is fetched from IPFS as referenced in the CID RADICE FW field
   - Nodes validate received binary data using the MAGIC HEADER pattern (bytes 0x00-0x07: `45 55 59 53 54 41 43 49`)

2. **Binary Implementation**:
   - When generating binary configuration data, follow the byte layout specified in this document
   - Read bytes 0x08-0x0B to encode/decode firmware version
   - Ensure compatibility with Phase II specification (version 2.0.0 or higher)

3. **Consensus Validation**:
   - Extract MIN CONSENSO % from bytes 0x1A-0x1B: value `00 88` represents 88% required for Phase II
   - Configure your DAO voting threshold to match this specification

## Distribution and Availability

### GitHub Repository
- **Direct Access**: Available in this repository at [`euystacio.core.v2.bin`](./euystacio.core.v2.bin)
- **Releases**: Tagged releases include the specification document as a downloadable artifact
- **Current Version**: v2.0.0 (Phase II)

### GitHub Pages
The configuration specification is accessible via GitHub Pages at:
```
https://hannesmitterer.github.io/AI/euystacio.core.v2.bin
```

### IPFS Distribution
For decentralized binary configuration distribution:
- Compiled binary configurations (following this specification) are pinned to IPFS
- The IPFS CID reference is embedded in the actual binary's CID RADICE FW field
- K-SYNC Daemon nodes fetch the compiled binary directly from IPFS using the embedded CID
- **Note**: This document serves as the specification; the actual binary data for node operation is distributed via IPFS

## Deployment Status

### Phase II Milestone Checklist

✅ **Configuration Specification Created**: `euystacio.core.v2.bin` documents Phase II binary format  
✅ **IPFS Integration Specified**: Binary data distribution via IPFS network documented  
✅ **Repository Published**: Specification committed to version control  
🔄 **Node Implementation**: K-SYNC Daemons implementing binary format based on this spec  
🔄 **Consensus Activation**: 88% threshold being communicated to DAO participants  

### Version History

- **v2.0.0** (Phase II) - Current
  - Initial Phase II release
  - 88% consensus requirement
  - IANUS vigilant mode activated
  - Quick-Ethical (QE) protocol integration

## Dashboard and Monitoring

An interactive governance dashboard is available at [`index.html`](./index.html) providing:
- Real-time audit trail of system compliance
- TFK drift score monitoring
- Consensus status tracking
- Executive override capabilities for critical situations

## License

See [LICENSE](./LICENSE) file for details.

## Support and Contact

For technical issues or questions about the Phase II deployment:
- Open an issue in this repository
- Review the governance dashboard for current system status
- Consult the embedded documentation in `euystacio.core.v2.bin` 
