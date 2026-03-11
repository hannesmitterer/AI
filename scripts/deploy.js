// scripts/deploy.js
// Hardhat deployment script for the AUFHOR (AH) token on Optimism L2.
//
// Usage:
//   npx hardhat run scripts/deploy.js --network optimism
//
// Ensure your hardhat.config.js has the "optimism" network entry configured
// with the correct RPC URL and a funded signer before running.

const { ethers } = require("hardhat");

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying AUFHOR with account:", deployer.address);

  const balance = await ethers.provider.getBalance(deployer.address);
  console.log("Account balance:", ethers.formatEther(balance), "ETH");

  // Deploy AufhorToken; the deployer becomes the initial owner and receives
  // the initial supply of 144,000 AH.
  const AufhorToken = await ethers.getContractFactory("AufhorToken");
  const aufhor = await AufhorToken.deploy(deployer.address);

  await aufhor.waitForDeployment();

  const address = await aufhor.getAddress();
  console.log("AUFHOR (AH) token deployed to:", address);
  console.log("Initial supply minted to deployer: 144,000 AH");
  console.log(
    "\nVerify on Etherscan (Optimism):\n",
    `npx hardhat verify --network optimism ${address} "${deployer.address}"`
  );
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
