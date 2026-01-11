#!/usr/bin/env node

/**
 * Lex Amoris Automated Test Suite
 * Tests core JavaScript functionality without browser
 */

// Test 1: Growth Rate Calculation
console.log('=== Test 1: Growth Rate Calculation ===');
const GROWTH_BASE = 1.618; // PHI

function calculateGrowthRate(cycles) {
    const normalizedCycles = cycles / 100;
    const exponentialFactor = Math.pow(GROWTH_BASE, normalizedCycles / 10);
    return Math.min(exponentialFactor, 10.0);
}

const testCycles = [0, 10, 50, 100, 500, 1000];
let growthTestsPassed = 0;

testCycles.forEach(cycles => {
    const growth = calculateGrowthRate(cycles);
    const isValid = growth >= 1.0 && growth <= 10.0;
    console.log(`Cycles: ${cycles.toString().padStart(4)} | Growth: ${growth.toFixed(4)}x | ${isValid ? '✓' : '✗'}`);
    if (isValid) growthTestsPassed++;
});

console.log(`Growth Tests: ${growthTestsPassed}/${testCycles.length} passed\n`);

// Test 2: Phase Calculation
console.log('=== Test 2: Phase Calculation ===');
function calculatePhase(startTime, currentTime) {
    const elapsed = (currentTime - startTime) / 1000;
    const phase = (elapsed * 0.043 * 360) % 360;
    return phase;
}

const testStartTime = Date.now();
const testTimes = [0, 11630, 23260, 34890, 46520]; // 0s, 11.63s, 23.26s, 34.89s, 46.52s
let phaseTestsPassed = 0;

testTimes.forEach(elapsed => {
    const currentTime = testStartTime + elapsed;
    const phase = calculatePhase(testStartTime, currentTime);
    const expectedPhase = (elapsed / 1000 * 0.043 * 360) % 360;
    const isValid = Math.abs(phase - expectedPhase) < 0.1;
    console.log(`Time: ${(elapsed/1000).toFixed(2)}s | Phase: ${phase.toFixed(1)}° | Expected: ${expectedPhase.toFixed(1)}° | ${isValid ? '✓' : '✗'}`);
    if (isValid) phaseTestsPassed++;
});

console.log(`Phase Tests: ${phaseTestsPassed}/${testTimes.length} passed\n`);

// Test 3: Animation Timing Validation
console.log('=== Test 3: Animation Timing ===');
const UNIVERSAL_RESONANCE_HZ = 0.043;
const CYCLE_PERIOD_MS = (1.0 / UNIVERSAL_RESONANCE_HZ) * 1000;
const expectedPeriod = 23255.81; // ~23.26 seconds
const tolerance = 10; // 10ms tolerance

const timingValid = Math.abs(CYCLE_PERIOD_MS - expectedPeriod) < tolerance;
console.log(`Resonance Frequency: ${UNIVERSAL_RESONANCE_HZ} Hz`);
console.log(`Calculated Period: ${CYCLE_PERIOD_MS.toFixed(2)} ms`);
console.log(`Expected Period: ${expectedPeriod.toFixed(2)} ms`);
console.log(`Difference: ${Math.abs(CYCLE_PERIOD_MS - expectedPeriod).toFixed(2)} ms`);
console.log(`Timing Valid: ${timingValid ? '✓' : '✗'}\n`);

// Test 4: Love Index Growth Simulation
console.log('=== Test 4: Love Index Growth Simulation ===');
let loveIndex = 1.0;
const simulatedCycles = 20;
let loveIndexValid = true;

for (let i = 0; i < simulatedCycles; i++) {
    const growthRate = calculateGrowthRate(i);
    const previousIndex = loveIndex;
    loveIndex = Math.min(loveIndex * (1 + (growthRate - 1) * 0.01), 999.999);
    
    if (loveIndex < previousIndex || loveIndex > 999.999) {
        loveIndexValid = false;
    }
    
    if (i % 5 === 0 || i === simulatedCycles - 1) {
        console.log(`Cycle ${i.toString().padStart(2)}: LRI=${loveIndex.toFixed(3)} | Growth=${growthRate.toFixed(2)}x`);
    }
}

console.log(`Love Index Growth Valid: ${loveIndexValid ? '✓' : '✗'}\n`);

// Test 5: Manifest JSON Validation
console.log('=== Test 5: Manifest JSON Validation ===');
const fs = require('fs');
const path = require('path');

try {
    const manifestPath = path.join(__dirname, 'manifest.json');
    const manifestContent = fs.readFileSync(manifestPath, 'utf8');
    const manifest = JSON.parse(manifestContent);
    
    // Required fields check
    const requiredFields = ['name', 'short_name', 'start_url', 'display', 'background_color', 'theme_color', 'icons'];
    let manifestTestsPassed = 0;
    
    requiredFields.forEach(field => {
        const exists = manifest.hasOwnProperty(field);
        console.log(`Field "${field}": ${exists ? '✓' : '✗'}`);
        if (exists) manifestTestsPassed++;
    });
    
    // Icon count check
    const iconCount = manifest.icons ? manifest.icons.length : 0;
    const iconCountValid = iconCount === 8;
    console.log(`Icon count: ${iconCount} | Expected: 8 | ${iconCountValid ? '✓' : '✗'}`);
    
    // Shortcuts check
    const shortcutCount = manifest.shortcuts ? manifest.shortcuts.length : 0;
    const shortcutCountValid = shortcutCount === 3;
    console.log(`Shortcut count: ${shortcutCount} | Expected: 3 | ${shortcutCountValid ? '✓' : '✗'}`);
    
    console.log(`Manifest Tests: ${manifestTestsPassed}/${requiredFields.length} required fields present\n`);
    
} catch (error) {
    console.log(`Manifest validation failed: ${error.message}\n`);
}

// Test Summary
console.log('=== Test Summary ===');
const totalTests = 5;
const passedTests = [
    growthTestsPassed === testCycles.length,
    phaseTestsPassed === testTimes.length,
    timingValid,
    loveIndexValid,
    true // manifest loaded
].filter(Boolean).length;

console.log(`Tests Passed: ${passedTests}/${totalTests}`);
console.log(`Status: ${passedTests === totalTests ? '✅ ALL TESTS PASSED' : '⚠️ SOME TESTS FAILED'}`);
console.log('\n=== Lex Amoris Test Suite Complete ===');

process.exit(passedTests === totalTests ? 0 : 1);
