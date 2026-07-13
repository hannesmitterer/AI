// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/// @title SyntropicToken – ERC-20 token derived from Urformel principles
/// @notice Implements a syntropic ERC-20 token with harmony validation.
///         Growth and transfer logic is based on golden ratio principles.
///         Derived from the Urformel (Primordial Formula) for syntropic growth
///         and harmony: every transaction must respect harmonic proportions or
///         it is rejected.
///
/// @dev Harmonic validation: transfer amounts must be non-zero and divisible by
///      PHI (1618) or PHI-1 (1617), where PHI = floor(1.618 * 1000) is the
///      golden ratio scaled by 1000 for integer arithmetic.
///      Examples of valid (non-zero) transfer amounts (in base units, before
///      applying decimals): 1617, 1618, 3234, 3236, 4851, 4854, …
///      To transfer whole STOK tokens multiply by 10**18; e.g. to send 1617
///      base-unit tokens call transfer(to, 1617).
contract SyntropicToken is ERC20, Ownable {
    /// @notice Golden ratio scaled by 1000 for integer arithmetic
    ///         (PHI = floor(1.618 × 1000) = 1618).
    uint256 public constant PHI = 1618;

    /// @notice Emitted when a transfer is validated as harmonic.
    event HarmonicTransfer(address indexed from, address indexed to, uint256 amount);

    /// @dev Initializes the token with symbolic initial supply (144,000 units),
    ///      a number resonant with syntropic principles.
    constructor() ERC20("SyntropicToken", "STOK") Ownable(msg.sender) {
        _mint(msg.sender, 144_000 * 10 ** decimals());
    }

    /// @notice Validates whether an amount respects golden ratio-derived harmonic logic.
    /// @dev Returns false for zero to prevent no-op transfers from passing validation.
    /// @param amount The token amount to validate.
    /// @return True if amount is non-zero and divisible by PHI (1618) or PHI-1 (1617).
    function isHarmonic(uint256 amount) public pure returns (bool) {
        if (amount == 0) return false;
        return amount % PHI == 0 || amount % (PHI - 1) == 0;
    }

    /// @notice Overrides ERC-20 transfer to enforce harmonic validation.
    /// @dev Minting (from == address(0)) and burning (to == address(0)) bypass
    ///      harmonic checks to allow the initial symbolic supply to be created.
    function _update(
        address from,
        address to,
        uint256 amount
    ) internal override {
        // Only enforce harmony check on regular transfers (not mint/burn).
        if (from != address(0) && to != address(0)) {
            require(
                isHarmonic(amount),
                "SyntropicToken: transfer rejected – does not conform to harmonic principles"
            );
            emit HarmonicTransfer(from, to, amount);
        }
        super._update(from, to, amount);
    }
}
