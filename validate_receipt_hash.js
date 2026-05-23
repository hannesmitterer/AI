const fs = require("fs");
const crypto = require("crypto");
const block = JSON.parse(fs.readFileSync("TRIPLE_SIGN_AUDIT.json"));
const canonical = JSON.stringify(block, Object.keys(block).sort());
const digest = crypto.createHash("sha256").update(canonical).digest("hex");
console.log("Manifest hash:", digest);
if (digest !== "8f3e9c2b4a1d7f6e5c8b3a2f1e0d9c8b7a6f5e4d3c2b1a0f9e8d7c6b5a4f3e2d")
  throw new Error("HASH MISMATCH!");
