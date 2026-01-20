
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
   forge create --rpc-url https://rpc.sepolia.org \
     --private-key $PRIVATE_KEY \
     --constructor-args "0x..." 10 \
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
