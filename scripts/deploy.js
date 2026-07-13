// scripts/deploy.js
// Hardhat deployment script for SyntropicToken on Optimism L2.
//
// Usage:
//   npx hardhat run scripts/deploy.js --network optimism
//   npx hardhat run scripts/deploy.js --network optimismSepolia   (testnet)
//
// Ensure DEPLOYER_PRIVATE_KEY and OPTIMISM_RPC_URL are set in your .env file.

const { ethers } = require("hardhat");

async function main() {
  const [deployer] = await ethers.getSigners();

  console.log("=== SyntropicToken Deployment ===");
  console.log("Deploying with account:", deployer.address);

  const balance = await ethers.provider.getBalance(deployer.address);
  console.log("Account balance:", ethers.formatEther(balance), "ETH");

  const SyntropicToken = await ethers.getContractFactory("SyntropicToken");
  console.log("Deploying SyntropicToken...");

  const token = await SyntropicToken.deploy();
  await token.waitForDeployment();

  const address = await token.getAddress();
  console.log("SyntropicToken deployed to:", address);
  console.log("Initial supply (symbolic 144,000 STOK) minted to:", deployer.address);
  console.log("Golden ratio constant PHI:", (await token.PHI()).toString());
  console.log("=================================");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
