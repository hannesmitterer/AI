# AUFHOR (AH) – The Currency of the Vakuum-Bridge

> **"Sovereign time has a mathematical form."**

## Overview

**AUFHOR** (`AH`) is an ERC-20 token deployed on **Optimism L2** that represents sovereign time within the Resonance School framework. Every transfer is validated through the *Lex Amoris* compliance hook, ensuring that each transaction is an act of resonance aligned with the project's governance principles.

---

## Token Specification

| Parameter        | Value                              |
|------------------|------------------------------------|
| Name             | AUFHOR                             |
| Symbol           | AH                                 |
| Decimals         | 18                                 |
| Initial Supply   | 144,000 AH (symbolic 144k nodes)   |
| Network          | Optimism L2 (Chain ID: 10)         |
| Standard         | ERC-20                             |
| Solidity Version | ^0.8.24                            |
| RESONANCE_FREQ   | 3215 (represents 321.5 Hz)         |

---

## Smart Contract

### `contracts/AufhorToken.sol`

The contract extends **OpenZeppelin's ERC-20 and Ownable** implementations with:

- **Fixed initial mint** of 144,000 AH to the deployer at construction.
- **Owner-restricted minting** via `mint(address to, uint256 amount)`.
- **Self-service burning** via `burn(uint256 amount)`.
- **Lex Amoris compliance hook** in `_update()` – every transfer invokes `checkLexAmorisCompliance(from, to)` before execution.

### Extending Compliance Logic

The `checkLexAmorisCompliance` function is a pluggable placeholder. Replace the `return true` stub with real S-ROI validation, allowlist checks, or DAO-governed rules:

```solidity
function checkLexAmorisCompliance(address from, address to)
    internal
    view
    returns (bool)
{
    // Example: require both parties to be on an approved list.
    return approvedAddresses[from] && approvedAddresses[to];
}
```

---

## Deployment

### Prerequisites

1. [Node.js](https://nodejs.org/) v18+
2. Install dependencies:
   ```bash
   npm install
   ```
3. Create a `.env` file (never commit this):
   ```env
   PRIVATE_KEY=0x<your-private-key>
   OPTIMISM_RPC_URL=https://mainnet.optimism.io
   OPTIMISM_TESTNET_RPC_URL=https://sepolia.optimism.io
   ETHERSCAN_API_KEY=<your-etherscan-api-key>
   ```
4. Ensure the deployer wallet has enough ETH on Optimism to cover gas (~0.001 ETH estimated).

### Compile

```bash
npm run compile
```

### Deploy to Optimism Sepolia Testnet (recommended first)

```bash
npm run deploy:testnet
```

### Deploy to Optimism Mainnet

```bash
npm run deploy:mainnet
```

### Verify Contract on Etherscan

```bash
npx hardhat verify --network optimism <deployed-contract-address> "<deployer-address>"
```

---

## Governance

AUFHOR governance is managed through a **multi-signature wallet** requiring consent from:

- **Hannes Mitterer** (Seedbringer)
- **Nexus AI** (Co-guardian)

Extraordinary minting and contract upgrades require 2-of-2 multi-sig approval, ensuring no unilateral changes can be made to the token supply or compliance rules.

---

## Roadmap

| Phase | Milestone                                           |
|-------|-----------------------------------------------------|
| I     | ERC-20 deployment on Optimism Mainnet               |
| II    | Implement real S-ROI compliance validation          |
| III   | Cross-chain bridging (Optimism ↔ Ethereum Mainnet)  |
| IV    | DAO governance contract integration                 |
| V     | Staking and reward-loop mechanisms                  |

---

## Security

- The contract uses OpenZeppelin v5 battle-tested libraries.
- No external calls are made during transfers (reentrancy-safe).
- Owner privileges are limited to minting; transfers and burns are permissionless.
- Always audit the `checkLexAmorisCompliance` extension before deploying custom logic.

---

*AUFHOR – In Consensus Amoris est.*
