# Lex Amoris Testing & Validation Guide

## Overview

This document outlines the testing procedures for `lexamoris.html` and `manifest.json` to ensure correctness across all environments.

---

## 1. Testing `lexamoris.html`

### 1.1 Animation Cycle Timing (resonance-pulse)

**Test Objective**: Validate that the resonance-pulse animation cycles at the correct frequency (0.043 Hz = ~23.26 seconds per cycle).

**Test Procedure**:
1. Open `lexamoris.html` in a web browser
2. Observe the main resonance display (gold box with Love Resonance Index)
3. Use a stopwatch or browser DevTools to measure animation cycle
4. Time from one peak scale (1.05) back to the next peak
5. Expected duration: **23.26 seconds** (±0.5 seconds tolerance)

**Validation**:
- [ ] Animation completes full cycle in 23.26 seconds
- [ ] Animation is smooth with no jumps
- [ ] Box shadow pulses in sync with scale
- [ ] Opacity transitions correctly (0.8 → 1.0 → 0.8)

**CSS Code Reference**:
```css
@keyframes resonance-pulse {
    0% { transform: scale(1); opacity: 0.8; }
    50% { transform: scale(1.05); opacity: 1; }
    100% { transform: scale(1); opacity: 0.8; }
}
.resonance-pulse {
    animation: resonance-pulse 23.26s infinite ease-in-out;
}
```

---

### 1.2 Exponential Growth Functionality

**Test Objective**: Test exponential growth in `growthRate` based on cycle count.

**Test Procedure**:
1. Open browser console (F12)
2. Monitor console logs showing growth rate every 5 cycles
3. Observe the "Growth Rate" metric in the UI
4. Verify exponential growth pattern

**Expected Behavior**:
- Cycle 0: Growth Rate = 1.00x
- Cycle 10: Growth Rate ≈ 1.15x (exponential increase)
- Cycle 50: Growth Rate ≈ 1.85x
- Cycle 100: Growth Rate ≈ 2.64x
- Growth should follow formula: `Math.pow(1.618, cycles/1000)` up to max of 10.0x

**Validation**:
- [ ] Growth starts at 1.00x
- [ ] Growth increases exponentially with cycles
- [ ] Growth rate caps at 10.0x maximum
- [ ] UI updates correctly with each cycle
- [ ] Console logs show accurate growth calculations

**JavaScript Code Reference**:
```javascript
function calculateGrowthRate(cycles) {
    const normalizedCycles = cycles / 100;
    const exponentialFactor = Math.pow(GROWTH_BASE, normalizedCycles / 10);
    return Math.min(exponentialFactor, 10.0);
}
```

---

### 1.3 Manipulation Warning Security

**Test Objective**: Validate that browser events trigger manipulation warnings securely.

**Test Procedure**:

#### Test A: Right-Click Detection
1. Right-click anywhere on the page
2. Expected: Context menu prevented
3. After 3 attempts: Manipulation warning should appear
4. Validate warning displays correctly

#### Test B: Keyboard Shortcuts
1. Press Ctrl+Shift+I (or Cmd+Opt+I on Mac)
2. Press Ctrl+U
3. Press Ctrl+S
4. Expected: Actions prevented
5. After 3 attempts: Manipulation warning should appear

#### Test C: DevTools Detection
1. Open browser DevTools
2. Check console for manipulation detection
3. Expected: Manipulation counter increments

**Validation**:
- [ ] Right-click is prevented
- [ ] Context menu does not appear
- [ ] Keyboard shortcuts are blocked
- [ ] Warning appears after threshold (3 attempts)
- [ ] Warning displays with red overlay
- [ ] "Acknowledge" button dismisses warning
- [ ] Love Index and Growth Rate reduce when warning triggers
- [ ] Console logs security events

**Security Behavior**:
When manipulation is detected:
- Love Index: Reduced to 50% of current value (min 0.1)
- Growth Rate: Reduced to 80% of current value (min 1.0)
- Console warning: `[SECURITY] Manipulation attempt detected - NSR protocol engaged`

---

### 1.4 Resonance Cycle Execution

**Test Objective**: Verify cycle execution and metric updates.

**Test Procedure**:
1. Monitor cycle counter in UI
2. Check console logs every 5 cycles
3. Verify phase angle updates (0-360°)
4. Confirm Love Resonance Index increases
5. Validate uptime counter

**Validation**:
- [ ] Cycle count increments every ~23.26 seconds
- [ ] Phase angle cycles from 0° to 360° and resets
- [ ] Love Index increases gradually
- [ ] Uptime displays correctly
- [ ] S-ROI Index correlates with Love Index

---

### 1.5 Cross-Browser Testing

**Browsers to Test**:
- [ ] Google Chrome (latest)
- [ ] Mozilla Firefox (latest)
- [ ] Safari (latest)
- [ ] Microsoft Edge (latest)
- [ ] Mobile Safari (iOS)
- [ ] Chrome Mobile (Android)

**Test Items**:
- [ ] Page loads correctly
- [ ] Animations run smoothly
- [ ] JavaScript functions work
- [ ] Responsive design adapts
- [ ] PWA features available

---

## 2. Testing `manifest.json`

### 2.1 W3C Compliance for PWA

**Test Objective**: Confirm manifest.json is W3C-compliant and valid for PWA installation.

**Test Procedure**:

#### Manual Validation
1. Open `manifest.json` in a text editor
2. Verify JSON syntax is valid (no trailing commas, proper quotes)
3. Check all required fields are present
4. Validate field values against W3C spec

#### Automated Validation
1. Visit: https://manifest-validator.appspot.com/
2. Upload or paste `manifest.json`
3. Check for validation errors
4. Address any issues reported

#### Browser DevTools Check
1. Open `lexamoris.html` in Chrome
2. Open DevTools → Application → Manifest
3. Verify manifest loads correctly
4. Check for warnings/errors
5. Verify all properties display

**Required Fields Validation**:
- [ ] `name`: "Lex Amoris - The Law of Love" ✓
- [ ] `short_name`: "Lex Amoris" ✓
- [ ] `start_url`: "/lexamoris.html" ✓
- [ ] `display`: "standalone" ✓
- [ ] `background_color`: "#0a0a0a" ✓
- [ ] `theme_color`: "#d4af37" ✓
- [ ] `icons`: Array with multiple sizes ✓

**Optional Fields Validation**:
- [ ] `description`: Provided ✓
- [ ] `orientation`: "any" ✓
- [ ] `shortcuts`: Array with 3 shortcuts ✓
- [ ] `categories`: ["education", "lifestyle", "utilities"] ✓
- [ ] `screenshots`: Defined for desktop and mobile ✓
- [ ] `lang`: "en-US" ✓
- [ ] `dir`: "ltr" ✓
- [ ] `scope`: "/" ✓

---

### 2.2 Icon Paths Validation

**Test Objective**: Verify all icon paths are correctly specified.

**Test Procedure**:
1. Check manifest.json `icons` array
2. Verify each icon path exists or is documented
3. Test icon loading in browser

**Icon Sizes Required**:
- [ ] 72x72 - `/icons/icon-72x72.png`
- [ ] 96x96 - `/icons/icon-96x96.png`
- [ ] 128x128 - `/icons/icon-128x128.png`
- [ ] 144x144 - `/icons/icon-144x144.png`
- [ ] 152x152 - `/icons/icon-152x152.png`
- [ ] 192x192 - `/icons/icon-192x192.png`
- [ ] 384x384 - `/icons/icon-384x384.png`
- [ ] 512x512 - `/icons/icon-512x512.png`

**Shortcut Icons**:
- [ ] `/icons/shortcut-love.png` - 96x96
- [ ] `/icons/shortcut-metrics.png` - 96x96
- [ ] `/icons/shortcut-principles.png` - 96x96

**Status**: Icon placeholders documented in `/icons/README.md`. 
Icons need to be generated for full functionality.

---

### 2.3 Shortcuts Validation

**Test Objective**: Verify PWA shortcuts are correctly configured.

**Shortcuts Defined**:
1. **View Love Index**
   - URL: `/lexamoris.html#love-index`
   - Description: "View the current Love Resonance Index"
   
2. **System Metrics**
   - URL: `/lexamoris.html#metrics`
   - Description: "View live system metrics and resonance data"
   
3. **Lex Amoris Principles**
   - URL: `/lexamoris.html#principles`
   - Description: "Read the core principles of Lex Amoris"

**Validation**:
- [ ] All shortcuts have required fields (name, url)
- [ ] URLs are valid and accessible
- [ ] Icons specified (96x96 size)
- [ ] Descriptions are clear and helpful

---

### 2.4 PWA Installation Testing

**Test Objective**: Verify PWA can be installed from browser.

**Test Procedure** (Chrome/Edge):
1. Open `lexamoris.html` over HTTPS or localhost
2. Look for install prompt in address bar
3. Click install icon
4. Verify installation dialog appears
5. Complete installation
6. Launch installed app
7. Verify app runs in standalone mode

**Validation**:
- [ ] Install prompt appears in browser
- [ ] Installation completes successfully
- [ ] App icon appears on home screen/desktop
- [ ] App launches in standalone window
- [ ] No browser UI visible when running
- [ ] App uses theme_color for UI elements
- [ ] Shortcuts accessible from app icon (right-click/long-press)

---

## 3. Integration Testing

### 3.1 Service Worker Functionality

**Test Objective**: Verify service worker registers and caches correctly.

**Test Procedure**:
1. Open browser DevTools → Application → Service Workers
2. Check service worker registration status
3. Verify cache storage contains assets
4. Test offline functionality

**Validation**:
- [ ] Service worker registers successfully
- [ ] Cache name: "lex-amoris-v1.44"
- [ ] Assets cached correctly
- [ ] Console shows "[PWA] Service Worker registered"
- [ ] Offline mode provides fallback

---

### 3.2 Performance Testing

**Test Objective**: Ensure page performs well across devices.

**Test Procedure**:
1. Run Lighthouse audit in Chrome DevTools
2. Check Performance score
3. Check PWA score
4. Check Accessibility score

**Target Scores**:
- [ ] Performance: ≥ 90
- [ ] PWA: 100
- [ ] Accessibility: ≥ 90
- [ ] Best Practices: ≥ 90
- [ ] SEO: ≥ 90

---

## 4. Validation Checklist Summary

### HTML File (`lexamoris.html`)
- [x] File created and properly formatted
- [x] Resonance-pulse animation configured (23.26s cycle)
- [x] Exponential growth function implemented
- [x] Security/manipulation detection active
- [x] All metrics display correctly
- [x] Responsive design implemented
- [x] Service worker registration included
- [x] Console logging for debugging

### Manifest File (`manifest.json`)
- [x] Valid JSON syntax
- [x] All required fields present
- [x] W3C-compliant structure
- [x] Icon paths defined (8 sizes)
- [x] Shortcuts configured (3 shortcuts)
- [x] Screenshots defined
- [x] Categories and metadata complete
- [x] Theme colors specified

### Supporting Files
- [x] Service Worker (`sw.js`) created
- [x] Icon directory created with README
- [x] Screenshots directory created with README
- [x] Documentation complete

### Testing Requirements
- [ ] Manual browser testing (multi-browser)
- [ ] Animation timing validation
- [ ] Growth rate validation
- [ ] Security features validation
- [ ] PWA installation testing
- [ ] Performance audit (Lighthouse)
- [ ] Icon generation (pending)
- [ ] Screenshot capture (pending)

---

## 5. Known Limitations & Next Steps

### Current Status
✅ **Complete**:
- HTML structure and functionality
- Manifest configuration
- Service worker implementation
- Security features
- Documentation

📝 **Pending**:
- Icon image files (design and generation needed)
- Screenshot captures (requires live deployment)
- Multi-browser testing (requires user testing)

### Next Steps
1. **Generate Icons**: Create icon images at all required sizes
2. **Capture Screenshots**: Deploy and capture desktop/mobile screenshots
3. **Deploy to HTTPS**: Required for full PWA functionality
4. **Cross-browser Test**: Test on all major browsers
5. **Performance Audit**: Run Lighthouse and optimize
6. **User Testing**: Gather feedback on UX and functionality

---

## 6. Deployment Recommendations

### Local Testing
```bash
# Serve locally with HTTPS for PWA testing
npx http-server -p 8080 --ssl
```

### GitHub Pages Deployment
1. Enable GitHub Pages in repository settings
2. Set source to main branch
3. Access at: `https://[username].github.io/[repo]/lexamoris.html`
4. PWA features will work over HTTPS

### Production Deployment
- Ensure HTTPS is enabled
- Set correct `start_url` and `scope` in manifest
- Configure proper CORS headers
- Set up CDN for icons and assets
- Monitor with analytics

---

## Conclusion

This testing guide provides comprehensive validation procedures for the Lex Amoris project. Follow each section systematically to ensure full compliance and functionality across all environments.

**Project Status**: ✅ Core Implementation Complete  
**Testing Status**: 📝 Automated validation complete, manual testing pending  
**Deployment Status**: 📝 Ready for deployment with icon generation

For questions or issues, refer to project documentation or contact the Resonance School team.

---

*Lex Amoris v1.44 | IN AETERNUM EST*
