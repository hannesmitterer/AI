#!/usr/bin/env python3
"""
Peacebond Treasury - Deployment and Testing Script
===================================================

Provides utilities for deploying and testing the PeacebondTreasury
smart contract.

Requirements:
- web3.py: pip install web3
- solcx: pip install py-solc-x (for Solidity compilation)

Response to EU 2026 Framework - Protocol EUYSTACIO/NSR
"""

import json
import os
from typing import Dict, Optional
from datetime import datetime


class TreasuryDeploymentGuide:
    """
    Guide for deploying PeacebondTreasury smart contract.
    
    This class provides instructions and utilities for deployment
    on various networks (testnet and mainnet).
    """
    
    def __init__(self):
        """Initialize deployment guide."""
        self.contract_path = "contracts/PeacebondTreasury.sol"
        self.networks = {
            "sepolia": {
                "name": "Ethereum Sepolia Testnet",
                "chain_id": 11155111,
                "rpc": "https://rpc.sepolia.org",
                "explorer": "https://sepolia.etherscan.io"
            },
            "mainnet": {
                "name": "Ethereum Mainnet",
                "chain_id": 1,
                "rpc": "https://eth.llamarpc.com",
                "explorer": "https://etherscan.io"
            },
            "polygon": {
                "name": "Polygon Mainnet",
                "chain_id": 137,
                "rpc": "https://polygon-rpc.com",
                "explorer": "https://polygonscan.com"
            }
        }
    
    def generate_deployment_config(self, 
                                   safe_vault_address: str,
                                   centralization_threshold: int = 10) -> Dict:
        """
        Generate deployment configuration.
        
        Args:
            safe_vault_address: Address of the safe vault for emergency redirection
            centralization_threshold: Block threshold for centralization detection
            
        Returns:
            Deployment configuration dictionary
        """
        config = {
            "contract": "PeacebondTreasury",
            "constructor_params": {
                "_safeVault": safe_vault_address,
                "_centralizationThreshold": centralization_threshold
            },
            "deployment_timestamp": datetime.now().isoformat(),
            "networks": self.networks
        }
        
        return config
    
    def save_deployment_config(self, config: Dict, filename: str = "treasury_deployment.json") -> None:
        """
        Save deployment configuration to file.
        
        Args:
            config: Configuration dictionary
            filename: Output filename
        """
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"[DEPLOYMENT] Configuration saved to {filename}")
    
    def generate_deployment_instructions(self) -> str:
        """
        Generate deployment instructions.
        
        Returns:
            Markdown formatted instructions
        """
        instructions = """
# PeacebondTreasury Deployment Guide

## Prerequisites

1. **Install Required Tools**
   ```bash
   npm install -g hardhat
   npm install @nomicfoundation/hardhat-toolbox
   ```

2. **Install Python Dependencies**
   ```bash
   pip install web3 py-solc-x
   ```

## Deployment Steps

### Option 1: Using Hardhat

1. **Initialize Hardhat Project**
   ```bash
   cd contracts
   npx hardhat init
   ```

2. **Configure Network**
   
   Edit `hardhat.config.js`:
   ```javascript
   module.exports = {
     solidity: "0.8.20",
     networks: {
       sepolia: {
         url: "https://rpc.sepolia.org",
         accounts: [process.env.PRIVATE_KEY]
       }
     }
   };
   ```

3. **Create Deployment Script**
   
   Create `scripts/deploy.js`:
   ```javascript
   async function main() {
     const safeVault = "0x..."; // Your safe vault address
     const threshold = 10;
     
     const Treasury = await ethers.getContractFactory("PeacebondTreasury");
     const treasury = await Treasury.deploy(safeVault, threshold);
     await treasury.deployed();
     
     console.log("Treasury deployed to:", treasury.address);
   }
   
   main().catch((error) => {
     console.error(error);
     process.exitCode = 1;
   });
   ```

4. **Deploy**
   ```bash
   npx hardhat run scripts/deploy.js --network sepolia
   ```

### Option 2: Using Remix IDE

1. **Open Remix**: https://remix.ethereum.org
2. **Upload Contract**: Upload `PeacebondTreasury.sol`
3. **Compile**: Compiler version 0.8.20
4. **Deploy**:
   - Select "Injected Provider - MetaMask"
   - Enter constructor parameters:
     - `_safeVault`: Your safe vault address
     - `_centralizationThreshold`: e.g., 10
   - Click "Deploy"

### Option 3: Using Foundry

1. **Install Foundry**
   ```bash
   curl -L https://foundry.paradigm.xyz | bash
   foundryup
   ```

2. **Create Foundry Project**
   ```bash
   forge init treasury
   cd treasury
   ```

3. **Copy Contract**
   ```bash
   cp ../PeacebondTreasury.sol src/
   ```

4. **Deploy**
   ```bash
   forge create --rpc-url https://rpc.sepolia.org \\
     --private-key $PRIVATE_KEY \\
     --constructor-args "0x..." 10 \\
     src/PeacebondTreasury.sol:PeacebondTreasury
   ```

## Post-Deployment

### 1. Verify Contract

On Etherscan/Polygonscan:
```bash
npx hardhat verify --network sepolia <CONTRACT_ADDRESS> <SAFE_VAULT> <THRESHOLD>
```

### 2. Add Emergency Council Members

```javascript
const treasury = await ethers.getContractAt("PeacebondTreasury", address);
await treasury.addCouncilMember("0x...");
```

### 3. Issue Initial Resonance Credits

```javascript
await treasury.issueResonanceCredits("0x...", ethers.utils.parseUnits("1000", 18));
```

### 4. Test Forensic Switch

```javascript
// From council member account
await treasury.activateForensicSwitch();
const status = await treasury.getStatus();
console.log("Emergency mode:", status._emergencyMode);
```

## Security Checklist

- [ ] Safe vault address verified and secured
- [ ] Emergency council members added
- [ ] Centralization threshold appropriately set
- [ ] Contract verified on block explorer
- [ ] Initial test transactions completed
- [ ] Backup of deployment addresses stored
- [ ] Access control tested (onlySeedbringer, onlyCouncil)
- [ ] Emergency redirection tested on testnet

## Monitoring

Monitor contract events:
```javascript
treasury.on("ForensicSwitchActivated", (activator, timestamp) => {
  console.log(`Forensic switch activated by ${activator} at ${timestamp}`);
});

treasury.on("CentralizationDetected", (blockNumber, alertCount) => {
  console.log(`Centralization detected at block ${blockNumber}, alert #${alertCount}`);
});
```

## Emergency Procedures

### If Centralization Detected

1. **Automatic**: System auto-activates after 3 alerts
2. **Manual**: Council member calls `activateForensicSwitch()`
3. **Redirect**: Call `redirectToSafeVault()` to move funds

### Recovery

1. Verify threat has passed
2. Seedbringer calls `deactivateForensicSwitch()`
3. Resume normal operations

## Support

- GitHub: https://github.com/hannesmitterer/AI
- Protocol: EUYSTACIO/NSR
- Documentation: See README.md
"""
        return instructions
    
    def save_deployment_instructions(self, filename: str = "DEPLOYMENT_GUIDE.md") -> None:
        """
        Save deployment instructions to markdown file.
        
        Args:
            filename: Output filename
        """
        instructions = self.generate_deployment_instructions()
        
        with open(filename, 'w') as f:
            f.write(instructions)
        
        print(f"[DEPLOYMENT] Instructions saved to {filename}")


def main():
    """Main demonstration."""
    print("=" * 70)
    print("PEACEBOND TREASURY - DEPLOYMENT GUIDE")
    print("EU 2026 Resilience Protocol - EUYSTACIO/NSR")
    print("=" * 70)
    print()
    
    # Initialize guide
    guide = TreasuryDeploymentGuide()
    
    # Generate sample configuration
    print("[CONFIG] Generating deployment configuration...")
    config = guide.generate_deployment_config(
        safe_vault_address="0x5d61a4B25034393A37ef9307C8Ba3aE99e49944b",
        centralization_threshold=10
    )
    
    # Save configuration
    guide.save_deployment_config(config)
    
    # Generate and save instructions
    print("[INSTRUCTIONS] Generating deployment guide...")
    guide.save_deployment_instructions()
    
    print("\n[DEPLOYMENT] Setup complete!")
    print("  - treasury_deployment.json: Deployment configuration")
    print("  - DEPLOYMENT_GUIDE.md: Step-by-step instructions")
    print("\nNext steps:")
    print("  1. Review deployment configuration")
    print("  2. Follow deployment guide for your preferred method")
    print("  3. Test on testnet before mainnet deployment")


if __name__ == "__main__":
    main()
