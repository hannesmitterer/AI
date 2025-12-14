# Branch Protection Configuration

This document outlines the branch protection rules that should be configured for the `main` branch to ensure the integrity and quality of the codebase.

## Main Branch Protection Rules

### Access Restrictions
- **Require pull request before merging**: Enabled
  - Required approving reviews: 1 (can be adjusted based on team size)
  - Dismiss stale pull request approvals when new commits are pushed: Enabled
  - Require review from Code Owners: Optional (if CODEOWNERS file is created)

### Status Checks
- **Require status checks to pass before merging**: Enabled
  - Required checks:
    - `ci-checks` (from CI workflow)
    - `verify-landing-page` (from Landing Page Verification workflow)
    - `check-documentation` (from Documentation Check workflow)
  - Require branches to be up to date before merging: Enabled

### Additional Protections
- **Require signed commits**: Optional (recommended for enhanced security)
- **Require linear history**: Optional (prevents merge commits)
- **Include administrators**: Disabled (allows admins to override in emergencies)
- **Restrict who can push to matching branches**: Optional
- **Allow force pushes**: Disabled
- **Allow deletions**: Disabled

## How to Configure

### Via GitHub Web Interface

1. Navigate to the repository: https://github.com/hannesmitterer/AI
2. Click on **Settings** tab
3. Select **Branches** from the left sidebar
4. Click **Add branch protection rule** or edit existing rule
5. Enter branch name pattern: `main`
6. Configure the following settings:

   **Protect matching branches:**
   - ✓ Require a pull request before merging
     - Required number of approvals before merging: 1
     - ✓ Dismiss stale pull request approvals when new commits are pushed
   
   - ✓ Require status checks to pass before merging
     - ✓ Require branches to be up to date before merging
     - Status checks to require:
       - `ci-checks`
       - `verify-landing-page`
       - `check-documentation`
   
   - ✓ Restrict who can dismiss pull request reviews (Optional)
   
   - ✓ Require conversation resolution before merging (Recommended)
   
   - Do not allow bypassing the above settings
   
   - ✗ Allow force pushes (Keep disabled)
   
   - ✗ Allow deletions (Keep disabled)

7. Click **Create** or **Save changes**

### Via GitHub CLI (Alternative)

If you have the GitHub CLI installed, you can configure branch protection with:

```bash
# Install GitHub CLI first if not available
# https://cli.github.com/

# Example command (adjust parameters as needed)
gh api repos/hannesmitterer/AI/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["ci-checks","verify-landing-page","check-documentation"]}' \
  --field enforce_admins=false \
  --field required_pull_request_reviews='{"required_approving_review_count":1,"dismiss_stale_reviews":true}' \
  --field restrictions=null \
  --field allow_force_pushes=false \
  --field allow_deletions=false
```

## Verification

After configuring branch protection, verify by:

1. Attempting to push directly to `main` (should fail)
2. Creating a pull request and ensuring all checks run
3. Verifying that merging is blocked until all checks pass

## Emergency Override

As a repository administrator, you retain the ability to override branch protection rules in emergency situations. However, this should be:
- Documented when used
- Reviewed post-incident
- Used sparingly and only when absolutely necessary

## Notes

- These protections apply to the `main` branch only
- Feature branches (e.g., `copilot/**`) are not protected by default
- All automated workflows will run on pull requests to validate changes before merge
- The GitHub Pages deployment only triggers on successful merges to `main`

## Review Schedule

Branch protection rules should be reviewed:
- Quarterly to ensure they align with current workflow
- After any security incidents
- When team size or structure changes
