#!/usr/bin/env node

/**
 * Validation Script for Lex Amoris Files
 * Tests lexamoris.html and manifest.json for compliance
 */

const fs = require('fs');
const path = require('path');

// ANSI color codes
const colors = {
    reset: '\x1b[0m',
    green: '\x1b[32m',
    red: '\x1b[31m',
    yellow: '\x1b[33m',
    cyan: '\x1b[36m',
    bold: '\x1b[1m'
};

class Validator {
    constructor() {
        this.passed = 0;
        this.failed = 0;
        this.warnings = 0;
    }

    log(message, type = 'info') {
        const prefix = {
            pass: `${colors.green}✓${colors.reset}`,
            fail: `${colors.red}✗${colors.reset}`,
            warn: `${colors.yellow}⚠${colors.reset}`,
            info: `${colors.cyan}ℹ${colors.reset}`
        };
        console.log(`${prefix[type]} ${message}`);
    }

    test(description, condition, isWarning = false) {
        if (condition) {
            this.passed++;
            this.log(description, 'pass');
            return true;
        } else {
            if (isWarning) {
                this.warnings++;
                this.log(description, 'warn');
            } else {
                this.failed++;
                this.log(description, 'fail');
            }
            return false;
        }
    }

    summary() {
        console.log('\n' + colors.bold + '═'.repeat(60) + colors.reset);
        console.log(colors.bold + 'TEST SUMMARY' + colors.reset);
        console.log('═'.repeat(60));
        console.log(`Total: ${this.passed + this.failed + this.warnings}`);
        console.log(`${colors.green}Passed: ${this.passed}${colors.reset}`);
        console.log(`${colors.red}Failed: ${this.failed}${colors.reset}`);
        console.log(`${colors.yellow}Warnings: ${this.warnings}${colors.reset}`);
        console.log('═'.repeat(60) + '\n');
        
        return this.failed === 0;
    }
}

async function validateManifest() {
    console.log('\n' + colors.bold + colors.cyan + '📋 VALIDATING MANIFEST.JSON' + colors.reset + '\n');
    const validator = new Validator();
    
    try {
        const manifestPath = path.join(__dirname, 'manifest.json');
        const manifestContent = fs.readFileSync(manifestPath, 'utf8');
        const manifest = JSON.parse(manifestContent);
        
        // Required fields
        validator.test('Has name field', !!manifest.name);
        validator.test('Has short_name field', !!manifest.short_name);
        validator.test('Has start_url field', !!manifest.start_url);
        validator.test('Has display field', !!manifest.display);
        
        // Display mode
        validator.test('Display mode is "standalone"', manifest.display === 'standalone');
        
        // Colors
        validator.test('Has theme_color (#d4af37)', manifest.theme_color === '#d4af37');
        validator.test('Has background_color (#0a0a0a)', manifest.background_color === '#0a0a0a');
        
        // Language
        validator.test('Language is German (de)', manifest.lang === 'de');
        
        // Icons
        validator.test('Has icons array', Array.isArray(manifest.icons));
        validator.test('Has at least one icon', manifest.icons && manifest.icons.length > 0);
        
        const hasMaskable = manifest.icons.some(icon => 
            icon.purpose && icon.purpose.includes('maskable')
        );
        validator.test('Has maskable icon', hasMaskable);
        
        // Shortcuts
        validator.test('Has shortcuts array', Array.isArray(manifest.shortcuts));
        validator.test('Has at least one shortcut', manifest.shortcuts && manifest.shortcuts.length > 0);
        
        const hasWaterStatus = manifest.shortcuts.some(s => 
            s.url && s.url.includes('water-status')
        );
        validator.test('Has water-status shortcut', hasWaterStatus);
        
        // URLs
        validator.test('start_url is "/"', manifest.start_url === '/');
        validator.test('scope is "/" or relative', manifest.scope === '/' || manifest.scope.startsWith('./'));
        
        // W3C PWA compliance checks
        validator.test('Name is descriptive', manifest.name.length > 5);
        validator.test('Short name is concise', manifest.short_name.length <= 12, true);
        
    } catch (error) {
        validator.test(`Parse manifest.json: ${error.message}`, false);
    }
    
    return validator.summary();
}

async function validateHTML() {
    console.log('\n' + colors.bold + colors.cyan + '🌐 VALIDATING LEXAMORIS.HTML' + colors.reset + '\n');
    const validator = new Validator();
    
    try {
        const htmlPath = path.join(__dirname, 'lexamoris.html');
        const html = fs.readFileSync(htmlPath, 'utf8');
        
        // Basic HTML structure
        validator.test('Has HTML5 DOCTYPE', html.trim().startsWith('<!DOCTYPE html>'));
        validator.test('Has <html> tag', html.includes('<html'));
        validator.test('Has <head> tag', html.includes('<head>'));
        validator.test('Has <body> tag', html.includes('<body'));
        
        // Language
        validator.test('Has lang="de" attribute', html.includes('lang="de"'));
        
        // Meta tags
        validator.test('Has charset UTF-8', html.includes('charset="UTF-8"'));
        validator.test('Has viewport meta', html.includes('name="viewport"'));
        validator.test('Has theme-color meta', html.includes('name="theme-color"'));
        
        // Manifest link
        validator.test('Links to manifest.json', html.includes('rel="manifest"'));
        validator.test('Manifest href is correct', html.includes('href="manifest.json"') || html.includes('href="/manifest.json"'));
        
        // Title
        validator.test('Has title tag', html.includes('<title>'));
        validator.test('Title includes "Lex Amoris"', html.includes('Lex Amoris'));
        
        // Branding
        validator.test('Includes "Sempre in Costante"', html.includes('Sempre in Costante'));
        
        // CSS Variables
        validator.test('Defines --resonance-freq', html.includes('--resonance-freq'));
        validator.test('Defines --resonance-period', html.includes('--resonance-period'));
        validator.test('Resonance freq is 0.043Hz', html.includes('0.043Hz'));
        validator.test('Resonance period is 23.26s', html.includes('23.26s'));
        
        // Animations
        validator.test('Has resonance-pulse animation', html.includes('@keyframes resonance-pulse'));
        validator.test('Has resonance-pulse class', html.includes('class="') && html.includes('resonance-pulse'));
        
        // JavaScript Classes
        validator.test('Has ExponentialGrowth class', html.includes('class ExponentialGrowth'));
        validator.test('Has RedShieldProtection class', html.includes('class RedShieldProtection'));
        validator.test('Has ResonancePulse class', html.includes('class ResonancePulse'));
        validator.test('Has GrowthVisualizer class', html.includes('class GrowthVisualizer'));
        
        // Functions
        validator.test('Has growthRate function', html.includes('growthRate('));
        
        // Red Shield Features
        validator.test('Has red-shield element', html.includes('id="red-shield"'));
        validator.test('Has blur event listener', html.includes("addEventListener('blur'"));
        validator.test('Has contextmenu prevention', html.includes("addEventListener('contextmenu'"));
        validator.test('Has selectstart prevention', html.includes("addEventListener('selectstart'"));
        validator.test('Has dragstart prevention', html.includes("addEventListener('dragstart'"));
        validator.test('Has visibilitychange listener', html.includes("addEventListener('visibilitychange'"));
        
        // Canvas for visualization
        validator.test('Has canvas element', html.includes('<canvas'));
        validator.test('Canvas is for growth chart', html.includes('id="growthCanvas"'));
        
        // Golden ratio
        validator.test('Uses golden ratio (φ)', html.includes('1.618033988749895'));
        
        // No errors in basic structure
        const openTags = (html.match(/<script/g) || []).length;
        const closeTags = (html.match(/<\/script>/g) || []).length;
        validator.test('Script tags are balanced', openTags === closeTags);
        
    } catch (error) {
        validator.test(`Parse lexamoris.html: ${error.message}`, false);
    }
    
    return validator.summary();
}

async function validateWaterStatus() {
    console.log('\n' + colors.bold + colors.cyan + '💧 VALIDATING WATER-STATUS.HTML' + colors.reset + '\n');
    const validator = new Validator();
    
    try {
        const htmlPath = path.join(__dirname, 'water-status.html');
        const html = fs.readFileSync(htmlPath, 'utf8');
        
        validator.test('Has HTML5 DOCTYPE', html.trim().startsWith('<!DOCTYPE html>'));
        validator.test('Has lang="de" attribute', html.includes('lang="de"'));
        validator.test('Has charset UTF-8', html.includes('charset="UTF-8"'));
        validator.test('Has viewport meta', html.includes('name="viewport"'));
        validator.test('Title includes "Water Status"', html.includes('Water Status'));
        validator.test('Links back to lexamoris.html', html.includes('href="lexamoris.html"') || html.includes('href="/lexamoris.html"'));
        validator.test('Includes "Sempre in Costante"', html.includes('Sempre in Costante'));
        
    } catch (error) {
        validator.test(`Parse water-status.html: ${error.message}`, false);
    }
    
    return validator.summary();
}

async function checkFileExistence() {
    console.log('\n' + colors.bold + colors.cyan + '📁 CHECKING FILE EXISTENCE' + colors.reset + '\n');
    const validator = new Validator();
    
    const files = [
        'lexamoris.html',
        'manifest.json',
        'water-status.html',
        'test-lexamoris.html'
    ];
    
    for (const file of files) {
        const filePath = path.join(__dirname, file);
        const exists = fs.existsSync(filePath);
        validator.test(`File exists: ${file}`, exists);
        
        if (exists) {
            const stats = fs.statSync(filePath);
            validator.test(`${file} is not empty`, stats.size > 0);
        }
    }
    
    return validator.summary();
}

async function main() {
    console.log('\n' + colors.bold + '╔════════════════════════════════════════════════════════╗' + colors.reset);
    console.log(colors.bold + '║        LEX AMORIS VALIDATION SUITE                     ║' + colors.reset);
    console.log(colors.bold + '║        Sempre in Costante                              ║' + colors.reset);
    console.log(colors.bold + '╚════════════════════════════════════════════════════════╝' + colors.reset);
    
    const results = {
        files: await checkFileExistence(),
        manifest: await validateManifest(),
        html: await validateHTML(),
        waterStatus: await validateWaterStatus()
    };
    
    console.log('\n' + colors.bold + '═'.repeat(60) + colors.reset);
    console.log(colors.bold + 'OVERALL RESULTS' + colors.reset);
    console.log('═'.repeat(60));
    
    const allPassed = Object.values(results).every(r => r === true);
    
    if (allPassed) {
        console.log(colors.green + colors.bold + '✓ ALL VALIDATIONS PASSED!' + colors.reset);
        console.log(colors.green + 'Lex Amoris is ready for deployment.' + colors.reset);
    } else {
        console.log(colors.yellow + '⚠ Some validations failed or have warnings.' + colors.reset);
        console.log(colors.yellow + 'Please review the results above.' + colors.reset);
    }
    
    console.log('═'.repeat(60) + '\n');
    
    process.exit(allPassed ? 0 : 1);
}

main().catch(error => {
    console.error(colors.red + 'Fatal error:', error.message + colors.reset);
    process.exit(1);
});
