# GitHub Actions Workflows

This directory contains automated workflows for the KOSYMBIOSIS AI repository as part of the "rhythm mind" initiative.

## Workflows Overview

### 1. Continuous Integration (`ci.yml`)
**Trigger:** Push to main/copilot branches, all pull requests
**Purpose:** Comprehensive validation of repository integrity

**Checks performed:**
- Repository structure validation
- HTML file validation
- Security scanning for exposed credentials
- File size monitoring
- General code quality checks

**Status:** Required for merging to main

### 2. Landing Page Verification (`landing-page-verification.yml`)
**Trigger:** Changes to `index.html` or workflow file
**Purpose:** Ensure landing page integrity and functionality

**Checks performed:**
- HTML structure validation (DOCTYPE, html, head, body tags)
- KOSYMBIOSIS-specific element verification
- JavaScript function validation
- CSS theme consistency checks

**Key validations:**
- Presence of `public-audit-dashboard`
- Presence of `seedbringer-console`
- Required functions: `handleOverride`, `connectSeedbringerWallet`
- CSS variables and theme colors

**Status:** Required for merging to main

### 3. Documentation Consistency Check (`documentation-check.yml`)
**Trigger:** Changes to `README.md` or `euystacio.core.v2.bin`
**Purpose:** Enforce documentation standards and binary integrity

**Checks performed:**
- README.md existence and content validation
- Binary asset documentation verification
- Binary file integrity check (SHA256)
- Version consistency between README and binary
- Documentation structure validation

**Status:** Required for merging to main

### 4. Deploy to GitHub Pages (`deploy-pages.yml`)
**Trigger:** Push to main branch, manual workflow dispatch
**Purpose:** Automated deployment to GitHub Pages

**Deployment process:**
1. Verify required files (index.html, euystacio.core.v2.bin)
2. Validate binary file integrity
3. Prepare deployment package
4. Create deployment manifest with checksums
5. Deploy to GitHub Pages

**Deployed files:**
- `index.html` - Landing page
- `euystacio.core.v2.bin` - Binary configuration
- `README.md` - Documentation
- `LICENSE` - License file
- `manifest.json` - Deployment metadata with checksums

**Permissions required:**
- `contents: read`
- `pages: write`
- `id-token: write`

## Workflow Dependencies

```
┌─────────────────────────────────────────┐
│         Pull Request Created            │
└────────────────┬────────────────────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
    ▼            ▼            ▼
┌───────┐  ┌──────────┐  ┌──────────┐
│  CI   │  │ Landing  │  │   Docs   │
│ Checks│  │   Page   │  │  Check   │
└───┬───┘  └────┬─────┘  └────┬─────┘
    │           │             │
    └───────────┴─────────────┘
                │
                ▼
         All checks pass
                │
                ▼
    ┌───────────────────────┐
    │  Merge to main        │
    └───────────┬───────────┘
                │
                ▼
    ┌───────────────────────┐
    │ Deploy to Pages       │
    └───────────────────────┘
```

## Security Considerations

1. **Binary Integrity**: Every deployment calculates and stores SHA256 checksums
2. **Credential Scanning**: CI workflow checks for exposed secrets
3. **Branch Protection**: See [BRANCH_PROTECTION.md](BRANCH_PROTECTION.md)
4. **Deployment Manifest**: Each deployment includes metadata for traceability

## Local Testing

### Test Landing Page Verification
```bash
# Validate HTML structure
grep -q "<!DOCTYPE html>" index.html && echo "✓ DOCTYPE found"
grep -q "KOSYMBIOSIS" index.html && echo "✓ KOSYMBIOSIS branding found"
grep -q "public-audit-dashboard" index.html && echo "✓ Audit dashboard found"
```

### Test Documentation Consistency
```bash
# Check README and binary
test -f README.md && echo "✓ README exists"
test -f euystacio.core.v2.bin && echo "✓ Binary exists"
grep -q "euystacio.core.v2.bin" README.md && echo "✓ Binary documented"

# Calculate checksum
sha256sum euystacio.core.v2.bin
```

### Test CI Checks
```bash
# Validate all HTML files
find . -name "*.html" -type f -exec grep -l "<!DOCTYPE" {} \;

# Check file sizes
ls -lh euystacio.core.v2.bin
```

## Manual Deployment

To manually trigger a deployment to GitHub Pages:

1. Navigate to Actions tab in GitHub
2. Select "Deploy to GitHub Pages" workflow
3. Click "Run workflow"
4. Select branch (usually main)
5. Click "Run workflow" button

## Monitoring

### Workflow Status
- View all workflow runs: `Actions` tab in GitHub
- Check specific workflow: Click on workflow name
- View logs: Click on individual run

### Deployment Status
- Check deployment: Repository Settings → Pages
- View site: Click on deployment URL
- Verify manifest: Visit `https://<your-pages-url>/manifest.json`

## Troubleshooting

### Workflow Fails on Pull Request
1. Check the workflow logs in the Actions tab
2. Ensure all required files are present
3. Validate local changes before pushing
4. Run local tests (see above)

### Deployment Fails
1. Verify GitHub Pages is enabled in repository settings
2. Check that required permissions are granted
3. Ensure binary file is present and valid
4. Review deployment logs for specific errors

### Binary Checksum Mismatch
1. Verify the binary file hasn't been corrupted
2. Check git LFS configuration if file is large
3. Re-verify the original binary source

## Updating Workflows

When modifying workflows:

1. Test changes in a feature branch first
2. Verify workflow syntax using GitHub's workflow validator
3. Use workflow dispatch for manual testing
4. Document any new requirements or dependencies

## Status Badges

Add to README.md:

```markdown
![CI](https://github.com/hannesmitterer/AI/actions/workflows/ci.yml/badge.svg)
![Landing Page](https://github.com/hannesmitterer/AI/actions/workflows/landing-page-verification.yml/badge.svg)
![Documentation](https://github.com/hannesmitterer/AI/actions/workflows/documentation-check.yml/badge.svg)
![Deploy](https://github.com/hannesmitterer/AI/actions/workflows/deploy-pages.yml/badge.svg)
```

## Support

For issues or questions:
1. Check workflow logs in Actions tab
2. Review this documentation
3. Consult [BRANCH_PROTECTION.md](BRANCH_PROTECTION.md) for branch rules
4. Open an issue in the repository
