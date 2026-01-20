// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title PeacebondTreasury
 * @author EUYSTACIO/NSR Protocol
 * @notice Peacebond Treasury with Forensic Switch for EU 2026 Resilience
 * 
 * Implements:
 * - Resonance Credits (CR) monitoring
 * - Centralized block detection
 * - Forensic switch for emergency resource redirection
 * - Decentralized governance protection
 * 
 * Response to EU 2026 Framework - Protocol EUYSTACIO/NSR
 */
contract PeacebondTreasury {
    
    // ============================================
    // STATE VARIABLES
    // ============================================
    
    /// @notice Contract owner (Seedbringer)
    address public seedbringer;
    
    /// @notice Emergency council addresses
    address[] public emergencyCouncil;
    
    /// @notice Forensic switch state
    bool public forensicSwitchActive;
    
    /// @notice Last block number checked for centralization
    uint256 public lastCentralizationCheck;
    
    /// @notice Threshold for detecting centralized blocks (consecutive blocks from same validator)
    uint256 public centralizationThreshold;
    
    /// @notice Safe vault address for emergency redirection
    address public safeVault;
    
    /// @notice Total Resonance Credits (CR)
    uint256 public totalResonanceCredits;
    
    /// @notice Individual CR balances
    mapping(address => uint256) public resonanceCredits;
    
    /// @notice Centralization alert counter
    uint256 public centralizationAlerts;
    
    /// @notice Emergency mode flag
    bool public emergencyMode;
    
    /// @notice Reentrancy guard flag
    bool private _locked;
    
    // ============================================
    // EVENTS
    // ============================================
    
    event ForensicSwitchActivated(address indexed activator, uint256 timestamp);
    event ForensicSwitchDeactivated(address indexed deactivator, uint256 timestamp);
    event CentralizationDetected(uint256 blockNumber, uint256 alertCount);
    event EmergencyModeActivated(uint256 timestamp);
    event EmergencyModeDeactivated(uint256 timestamp);
    event ResourcesRedirected(address indexed from, address indexed to, uint256 amount);
    event ResonanceCreditsIssued(address indexed recipient, uint256 amount);
    event ResonanceCreditsBurned(address indexed holder, uint256 amount);
    event CouncilMemberAdded(address indexed member);
    event CouncilMemberRemoved(address indexed member);
    
    // ============================================
    // MODIFIERS
    // ============================================
    
    modifier onlySeedbringer() {
        require(msg.sender == seedbringer, "Only Seedbringer");
        _;
    }
    
    modifier onlyCouncil() {
        require(isCouncilMember(msg.sender), "Only Emergency Council");
        _;
    }
    
    modifier whenNotEmergency() {
        require(!emergencyMode, "Emergency mode active");
        _;
    }
    
    modifier whenEmergency() {
        require(emergencyMode, "Not in emergency mode");
        _;
    }
    
    modifier nonReentrant() {
        require(!_locked, "Reentrancy detected");
        _locked = true;
        _;
        _locked = false;
    }
    
    // ============================================
    // CONSTRUCTOR
    // ============================================
    
    constructor(address _safeVault, uint256 _centralizationThreshold) {
        seedbringer = msg.sender;
        safeVault = _safeVault;
        centralizationThreshold = _centralizationThreshold;
        forensicSwitchActive = false;
        emergencyMode = false;
        lastCentralizationCheck = block.number;
        _locked = false;
        
        // Initialize with seedbringer as first council member
        emergencyCouncil.push(msg.sender);
    }
    
    // ============================================
    // FORENSIC SWITCH FUNCTIONS
    // ============================================
    
    /**
     * @notice Activate forensic switch in response to centralized blocks
     * @dev Can be triggered by council members when centralization is detected
     */
    function activateForensicSwitch() external onlyCouncil {
        require(!forensicSwitchActive, "Already active");
        
        forensicSwitchActive = true;
        emergencyMode = true;
        
        emit ForensicSwitchActivated(msg.sender, block.timestamp);
        emit EmergencyModeActivated(block.timestamp);
    }
    
    /**
     * @notice Deactivate forensic switch after threat is resolved
     */
    function deactivateForensicSwitch() external onlySeedbringer {
        require(forensicSwitchActive, "Not active");
        
        forensicSwitchActive = false;
        emergencyMode = false;
        
        emit ForensicSwitchDeactivated(msg.sender, block.timestamp);
        emit EmergencyModeDeactivated(block.timestamp);
    }
    
    // ============================================
    // CENTRALIZATION DETECTION
    // ============================================
    
    /**
     * @notice Check for centralized block production
     * @dev Simplified version - in production would analyze validator patterns
     * @return detected Whether centralization was detected
     */
    function checkCentralization() external returns (bool detected) {
        // Simplified check: compare current block to threshold
        uint256 blocksSinceLastCheck = block.number - lastCentralizationCheck;
        
        // In production, this would:
        // 1. Analyze block producers/validators
        // 2. Check for consecutive blocks from same source
        // 3. Detect unusual block patterns
        
        // Simplified trigger for demonstration
        if (blocksSinceLastCheck < centralizationThreshold) {
            centralizationAlerts++;
            emit CentralizationDetected(block.number, centralizationAlerts);
            detected = true;
            
            // Auto-activate forensic switch after multiple alerts
            if (centralizationAlerts >= 3 && !forensicSwitchActive) {
                forensicSwitchActive = true;
                emergencyMode = true;
                emit ForensicSwitchActivated(address(this), block.timestamp);
            }
        }
        
        lastCentralizationCheck = block.number;
        return detected;
    }
    
    /**
     * @notice Reset centralization alerts counter
     */
    function resetCentralizationAlerts() external onlySeedbringer {
        centralizationAlerts = 0;
    }
    
    // ============================================
    // RESONANCE CREDITS (CR) MANAGEMENT
    // ============================================
    
    /**
     * @notice Issue Resonance Credits to an address
     * @param recipient Address to receive credits
     * @param amount Amount of credits to issue
     */
    function issueResonanceCredits(address recipient, uint256 amount) 
        external 
        onlySeedbringer 
        whenNotEmergency 
    {
        resonanceCredits[recipient] += amount;
        totalResonanceCredits += amount;
        
        emit ResonanceCreditsIssued(recipient, amount);
    }
    
    /**
     * @notice Burn Resonance Credits from an address
     * @param holder Address holding the credits
     * @param amount Amount of credits to burn
     */
    function burnResonanceCredits(address holder, uint256 amount) 
        external 
        onlySeedbringer 
    {
        require(resonanceCredits[holder] >= amount, "Insufficient credits");
        
        resonanceCredits[holder] -= amount;
        totalResonanceCredits -= amount;
        
        emit ResonanceCreditsBurned(holder, amount);
    }
    
    /**
     * @notice Get Resonance Credits balance
     * @param holder Address to check
     * @return balance Current CR balance
     */
    function getCRBalance(address holder) external view returns (uint256 balance) {
        return resonanceCredits[holder];
    }
    
    // ============================================
    // EMERGENCY RESOURCE REDIRECTION
    // ============================================
    
    /**
     * @notice Redirect treasury resources to safe vault in emergency
     * @dev Only callable when forensic switch is active. Protected against reentrancy.
     */
    function redirectToSafeVault() external onlyCouncil whenEmergency nonReentrant {
        uint256 balance = address(this).balance;
        require(balance > 0, "No funds to redirect");
        
        (bool success, ) = safeVault.call{value: balance}("");
        require(success, "Transfer failed");
        
        emit ResourcesRedirected(address(this), safeVault, balance);
    }
    
    /**
     * @notice Update safe vault address
     * @param newSafeVault New safe vault address
     */
    function updateSafeVault(address newSafeVault) external onlySeedbringer {
        require(newSafeVault != address(0), "Invalid address");
        safeVault = newSafeVault;
    }
    
    // ============================================
    // EMERGENCY COUNCIL MANAGEMENT
    // ============================================
    
    /**
     * @notice Add member to emergency council
     * @param member Address to add
     */
    function addCouncilMember(address member) external onlySeedbringer {
        require(member != address(0), "Invalid address");
        require(!isCouncilMember(member), "Already member");
        
        emergencyCouncil.push(member);
        emit CouncilMemberAdded(member);
    }
    
    /**
     * @notice Remove member from emergency council
     * @param member Address to remove
     */
    function removeCouncilMember(address member) external onlySeedbringer {
        for (uint256 i = 0; i < emergencyCouncil.length; i++) {
            if (emergencyCouncil[i] == member) {
                emergencyCouncil[i] = emergencyCouncil[emergencyCouncil.length - 1];
                emergencyCouncil.pop();
                emit CouncilMemberRemoved(member);
                return;
            }
        }
        revert("Member not found");
    }
    
    /**
     * @notice Check if address is council member
     * @param account Address to check
     * @return isMember True if member
     */
    function isCouncilMember(address account) public view returns (bool isMember) {
        for (uint256 i = 0; i < emergencyCouncil.length; i++) {
            if (emergencyCouncil[i] == account) {
                return true;
            }
        }
        return false;
    }
    
    /**
     * @notice Get all council members
     * @return members Array of council member addresses
     */
    function getCouncilMembers() external view returns (address[] memory members) {
        return emergencyCouncil;
    }
    
    // ============================================
    // UTILITY FUNCTIONS
    // ============================================
    
    /**
     * @notice Get comprehensive treasury status
     * @return status Treasury status data
     */
    function getStatus() external view returns (
        bool _forensicActive,
        bool _emergencyMode,
        uint256 _totalCR,
        uint256 _alerts,
        uint256 _councilSize,
        uint256 _balance
    ) {
        return (
            forensicSwitchActive,
            emergencyMode,
            totalResonanceCredits,
            centralizationAlerts,
            emergencyCouncil.length,
            address(this).balance
        );
    }
    
    /**
     * @notice Receive ETH deposits
     */
    receive() external payable {}
    
    /**
     * @notice Fallback function
     */
    fallback() external payable {}
}
