require("@nomicfoundation/hardhat-toolbox");

// Load environment variables for private key and API keys.
// Create a .env file (never commit it!) with:
//   PRIVATE_KEY=0x...
//   OPTIMISM_RPC_URL=https://mainnet.optimism.io
//   ETHERSCAN_API_KEY=...
const PRIVATE_KEY = process.env.PRIVATE_KEY || "0x" + "0".repeat(64);

// Warn (rather than silently fail) when no real key is provided and a live
// network deployment is attempted. Hardhat will still compile and run tests
// on the built-in network without a key.
if (!process.env.PRIVATE_KEY) {
  console.warn(
    "WARNING: PRIVATE_KEY env variable is not set. " +
      "Deploying to a live network will fail or use an empty account."
  );
}
const OPTIMISM_RPC_URL =
  process.env.OPTIMISM_RPC_URL || "https://mainnet.optimism.io";
const OPTIMISM_TESTNET_RPC_URL =
  process.env.OPTIMISM_TESTNET_RPC_URL || "https://sepolia.optimism.io";
const ETHERSCAN_API_KEY = process.env.ETHERSCAN_API_KEY || "";

/** @type import('hardhat/config').HardhatUserConfig */
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
    // Local development network (default)
    hardhat: {},
    // Optimism Mainnet (Chain ID: 10)
    optimism: {
      url: OPTIMISM_RPC_URL,
      accounts: [PRIVATE_KEY],
      chainId: 10,
    },
    // Optimism Sepolia Testnet (Chain ID: 11155420)
    "optimism-sepolia": {
      url: OPTIMISM_TESTNET_RPC_URL,
      accounts: [PRIVATE_KEY],
      chainId: 11155420,
    },
  },
  etherscan: {
    apiKey: {
      optimisticEthereum: ETHERSCAN_API_KEY,
      optimismSepolia: ETHERSCAN_API_KEY,
    },
    customChains: [
      {
        network: "optimismSepolia",
        chainId: 11155420,
        urls: {
          apiURL: "https://api-sepolia-optimism.etherscan.io/api",
          browserURL: "https://sepolia-optimism.etherscan.io",
        },
      },
    ],
  },
};
