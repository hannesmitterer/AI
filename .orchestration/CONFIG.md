# Orchestration Configuration Guide

This document provides detailed explanation of the `.orchestration/config.json` configuration file.

## Configuration Structure

### orchestration
Main system metadata:
- `version`: Current version of the orchestration system
- `system_name`: Display name for the orchestration system
- `description`: Brief description of the system purpose
- `created`: Creation date of the configuration
- `phase`: Current operational phase

### repository_fusion

Configuration for repository synchronization:

- `enabled`: Whether repository fusion is active (true/false)
- `sync_strategy`: Strategy for synchronization ("adaptive", "force", "manual")
- `sync_frequency`: How often sync occurs ("daily", "hourly", "weekly")
- `conflict_resolution`: How conflicts are handled ("manual_review", "auto", "preserve_local")
- `preservation_rules`: Array of rules to preserve during sync
- `sync_targets`: Array of repositories to sync with

#### sync_targets Configuration

**Note**: The `sync_targets` array is currently empty by design. This is a single-repository setup that can be expanded in the future.

To add sync targets, populate the array with objects like:

```json
"sync_targets": [
  {
    "repository": "organization/repo-name",
    "strategy": "pull",
    "frequency": "daily",
    "paths": ["workflows", "docs"]
  }
]
```

**Fields**:
- `repository`: GitHub repository in format "owner/repo"
- `strategy`: "pull" (receive only), "push" (send only), or "bidirectional"
- `frequency`: Override for sync frequency for this specific target
- `paths`: Array of paths to synchronize (empty = all)

### workflows

Configuration for all workflow automations:

#### continuous_integration
- `enabled`: Whether CI is active
- `triggers`: Events that trigger CI (push, pull_request, etc.)
- `validation_steps`: Array of validation steps to perform

#### deployment

**github_pages**:
- `enabled`: Whether GitHub Pages deployment is active
- `branch`: Branch to deploy from ("main" or "master")
- `automatic`: Whether deployment is automatic or manual

**ipfs**:
- `enabled`: Whether IPFS deployment is active
- `pinning_strategy`: How content is pinned ("persistent", "temporary")
- `gateway_urls`: Array of IPFS gateway URLs for access

#### monitoring

**health_checks**:
- `enabled`: Whether health monitoring is active
- `frequency`: How often health checks run ("every_6_hours", etc.)
- `notifications`: Whether to send notifications (true/false)

**repository_sync**:
- `enabled`: Whether sync monitoring is active
- `frequency`: How often sync runs ("daily", etc.)
- `automatic`: Whether sync is automatic or manual

### global_accessibility

Configuration for global access systems:

**github_pages**:
- `enabled`: Whether GitHub Pages is enabled
- `custom_domain`: Custom domain for GitHub Pages (null = use default)

**ipfs**:
- `enabled`: Whether IPFS is enabled
- `content_addressable`: Use content-addressable storage
- `decentralized`: Use decentralized distribution

### sustainability

Configuration for long-term system health:

- `automated_maintenance`: Enable automatic maintenance tasks
- `self_healing`: Enable self-healing mechanisms
- `growth_enablement`: Enable growth and scalability features
- `principles`: Array of guiding principles for the system

## Modifying the Configuration

1. **Always validate JSON** after editing using `python3 -m json.tool config.json`
2. **Restart workflows** after configuration changes
3. **Test changes** in a development branch first
4. **Document changes** in commit messages

## Example: Adding a Sync Target

```json
"sync_targets": [
  {
    "repository": "hannesmitterer/RelatedRepo",
    "strategy": "bidirectional",
    "frequency": "daily",
    "paths": [".github/workflows", "docs"]
  }
]
```

This would sync workflows and docs with RelatedRepo daily in both directions.

## Security Notes

- Never commit sensitive credentials to this file
- Use GitHub secrets for sensitive configuration
- Review all sync targets before enabling
- Monitor health reports for unexpected changes

## Further Reading

- See `.orchestration/SYNC.md` for synchronization details
- See `.orchestration/README.md` for system overview
- See workflow files in `.github/workflows/` for implementation details
