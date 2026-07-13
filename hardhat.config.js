// hardhat.config.js
// Network configuration for deploying SyntropicToken to Optimism L2.
//
// Required environment variables (set in .env):
//   DEPLOYER_PRIVATE_KEY  – private key of the deploying wallet
//   OPTIMISM_RPC_URL      – RPC endpoint for Optimism Mainnet
//   OPTIMISM_SEPOLIA_RPC_URL – RPC endpoint for Optimism Sepolia testnet (optional)

require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

/** @type {import('hardhat/config').HardhatUserConfig} */
module.exports = {
  solidity: {
    version: "0.8.24",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200,
      },
    },
  },
  networks: {
    // Optimism Mainnet (L2)
    optimism: {
      url: process.env.OPTIMISM_RPC_URL || "https://mainnet.optimism.io",
      accounts: process.env.DEPLOYER_PRIVATE_KEY
        ? [process.env.DEPLOYER_PRIVATE_KEY]
        : [],
      chainId: 10,
    },
    // Optimism Sepolia Testnet (L2)
    optimismSepolia: {
      url:
        process.env.OPTIMISM_SEPOLIA_RPC_URL ||
        "https://sepolia.optimism.io",
      accounts: process.env.DEPLOYER_PRIVATE_KEY
        ? [process.env.DEPLOYER_PRIVATE_KEY]
        : [],
      chainId: 11155420,
    },
  },
};
