# Release Process Documentation

## Overview

This document describes the release process for the KOSYMBIOSIS Phase II binary configuration deployment.

## Version Scheme

We follow Semantic Versioning (SemVer):
- **MAJOR.MINOR.PATCH** (e.g., 2.0.0)
- **MAJOR**: Incompatible configuration changes (Phase transitions)
- **MINOR**: Backward-compatible functionality additions
- **PATCH**: Backward-compatible bug fixes or minor updates

Current version is stored in the `VERSION` file.

## Creating a Release

### Prerequisites

1. Ensure all changes are committed and pushed to the main branch
2. Verify the binary file `euystacio.core.v2.bin` is present and correct
3. Update the `VERSION` file if not already done
4. Ensure README.md is up to date with the latest information

### Release Steps

#### 1. Create and Push a Version Tag

```bash
# Example for version 2.0.0
git tag -a v2.0.0 -m "Phase II Release v2.0.0"
git push origin v2.0.0
```

#### 2. Automatic Release Creation

Once the tag is pushed, the GitHub Actions workflow (`.github/workflows/release.yml`) will automatically:

- Verify the binary file exists
- Extract version information from the tag
- Validate the binary's magic header
- Generate release notes
- Create a GitHub Release with:
  - `euystacio.core.v2.bin` as a downloadable asset
  - `index.html` governance dashboard
  - Comprehensive release notes

#### 3. GitHub Pages Deployment

The `.github/workflows/pages.yml` workflow automatically deploys to GitHub Pages on every push to main, making the binary accessible at:

```
https://hannesmitterer.github.io/AI/euystacio.core.v2.bin
```

### Manual Release (Alternative)

If you need to create a release manually:

1. Go to the repository's "Releases" page
2. Click "Draft a new release"
3. Choose or create a tag (e.g., `v2.0.0`)
4. Fill in the release title: "Phase II Release v2.0.0"
5. Add release notes (see template below)
6. Attach the binary file and any other assets
7. Click "Publish release"

### Release Notes Template

```markdown
## KOSYMBIOSIS Phase II Configuration Release

This release includes the `euystacio.core.v2.bin` core configuration file for Phase II deployment.

### Binary Metadata

- **Version**: X.Y.Z
- **MAGIC HEADER**: `45 55 59 53 54 41 43 49` (EUYSTACI)
- **Firmware Version**: 2.0.0 (Phase II)
- **TFK Mint Target**: 4.0
- **Min Consensus**: 88%
- **WÄCHTER Mode**: IANUS (Active/Vigilant)
- **Protocol**: Quick-Ethical (QE)

### Download and Verification

Download the binary configuration file from the assets below.

### Distribution Channels

- **GitHub Release**: Download from this release's assets
- **GitHub Pages**: `https://hannesmitterer.github.io/AI/euystacio.core.v2.bin`
- **IPFS**: Pinned via CID referenced in binary

### Integration

K-SYNC Daemon nodes will automatically fetch and validate this configuration.
See the [README](https://github.com/hannesmitterer/AI#readme) for detailed usage instructions.
```

## Post-Release Tasks

1. **Verify GitHub Pages**: Check that the binary is accessible via the GitHub Pages URL
2. **IPFS Pinning**: Ensure the binary is pinned to IPFS (if applicable)
3. **Node Communication**: Notify K-SYNC Daemon operators of the new release
4. **DAO Notification**: Inform DAO participants of the consensus requirement changes
5. **Monitor Deployment**: Track node adoption through the governance dashboard

## IPFS Distribution

For decentralized distribution:

1. **Upload to IPFS**:
   ```bash
   ipfs add euystacio.core.v2.bin
   ```

2. **Pin the file**:
   ```bash
   ipfs pin add <CID>
   ```

3. **Update documentation** with the CID in README.md

4. **Verify availability**:
   ```bash
   ipfs cat <CID> > downloaded.bin
   diff euystacio.core.v2.bin downloaded.bin
   ```

## Rollback Process

If a release needs to be rolled back:

1. **Create a new patch version** with the previous stable configuration
2. **DO NOT delete or modify existing releases** - maintain version history
3. **Communicate the rollback** to all node operators
4. **Document the reason** for the rollback in the new release notes

## Version History

| Version | Date | Description |
|---------|------|-------------|
| v2.0.0  | 2024 | Initial Phase II release with 88% consensus requirement |

## Troubleshooting

### Release Workflow Fails

- Check GitHub Actions logs for detailed error messages
- Verify the tag format matches `v*.*.*` pattern
- Ensure binary file exists in the repository
- Check repository permissions for Actions

### GitHub Pages Not Updating

- Verify Pages is enabled in repository settings
- Check the Pages workflow run status
- May take a few minutes to propagate after deployment

### Binary Verification Issues

- Ensure the MAGIC HEADER is intact
- Verify file hasn't been corrupted during transfer
- Check file size matches expected value (1522 bytes for v2.0.0)

## Contact

For questions about the release process, open an issue in this repository.
