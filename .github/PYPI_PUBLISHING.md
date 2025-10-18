# 📦 PyPI Publishing Guide

Automated PyPI publishing via GitHub Actions using **Trusted Publishing** (no API tokens needed!).

## 🎯 Overview

The publishing workflow automatically:
1. ✅ Builds the package
2. ✅ Verifies version matches git tag
3. ✅ Detects pre-release vs stable (rc/beta → pre-release)
4. ✅ Publishes directly to PyPI
5. ✅ Updates GitHub Release with artifacts
6. ✅ Generates release notes

**Trigger:** Push any tag matching `v*.*.*` (e.g., `v0.2.0rc1`, `v1.0.0`)

## 🔐 Setup: Trusted Publishing (Recommended)

GitHub Actions can publish to PyPI **without API tokens** using OpenID Connect (OIDC).

### Step 1: Configure PyPI Trusted Publisher

1. **Go to PyPI**: https://pypi.org/manage/account/publishing/
2. **Add Trusted Publisher** with these settings:
   - **PyPI Project Name**: `automagik-hive`
   - **Owner**: `namastexlabs`
   - **Repository**: `automagik-hive`
   - **Workflow name**: `publish-pypi.yml`
   - **Environment name**: `pypi`

### Step 2: Create GitHub Environment

1. **Go to**: https://github.com/namastexlabs/automagik-hive/settings/environments
2. **Create `pypi` environment**:
   - Click "New environment"
   - Name: `pypi`
   - **Recommended**: Add protection rules:
     - Required reviewers (optional, for extra safety)
     - Deployment branches: `dev` branch or tags only

### Step 3: Verify Permissions

The workflow uses `id-token: write` permission for OIDC. This is already configured in the workflow file.

## 🚀 Publishing Workflow

### Option 1: Using Make Commands (Simplified)

```bash
# 1. Bump version to release candidate
make bump-rc
# Output: Version bumped to 0.2.0rc1

# 2. Commit and push (triggers CI/CD tests)
git add pyproject.toml
git commit -m "release: v0.2.0rc1" \
  --trailer "Co-Authored-By: Automagik Genie 🧞 <genie@namastex.ai>"
git push origin dev

# 3. Create and push tag (triggers PyPI publishing)
git tag v0.2.0rc1 -m "Release candidate v0.2.0rc1"
git push origin v0.2.0rc1

# 4. Wait for GitHub Actions
# → TestPyPI: ~2-3 minutes
# → PyPI: ~5-10 minutes
```

### Option 2: All-in-One Script

Create `scripts/release.sh`:

```bash
#!/bin/bash
set -e

# Bump version
make bump-rc

# Get new version
VERSION=$(grep '^version = ' pyproject.toml | cut -d'"' -f2)

echo "📦 Releasing version $VERSION"

# Commit
git add pyproject.toml
git commit -m "release: v$VERSION" \
  --trailer "Co-Authored-By: Automagik Genie 🧞 <genie@namastex.ai>"

# Tag
git tag "v$VERSION" -m "Release v$VERSION"

# Push
git push origin dev
git push origin "v$VERSION"

echo "✅ Release v$VERSION pushed!"
echo "🔗 Check status: https://github.com/namastexlabs/automagik-hive/actions"
```

## 🎯 Pre-Release Detection

The workflow automatically detects release types:

- **Pre-release** (marked on GitHub): Versions containing `rc`, `b`, `a`, `alpha`, or `beta`
  - Example: `v0.2.0rc1`, `v1.0.0b2`
  - Shows as "Pre-release" on GitHub Releases

- **Stable release**: Clean version numbers
  - Example: `v1.0.0`, `v0.2.0`
  - Shows as "Latest" on GitHub Releases

Both types publish to PyPI with appropriate metadata.

## 📋 Version Naming

- **Release Candidates**: `v0.2.0rc1`, `v1.0.0rc2`
- **Beta Releases**: `v0.1.1b2`, `v0.2.0b1`
- **Stable Releases**: `v1.0.0`, `v2.1.0`

All formats are supported by the workflow.

## 🔍 Monitoring

1. **GitHub Actions**: https://github.com/namastexlabs/automagik-hive/actions
2. **PyPI Package**: https://pypi.org/project/automagik-hive/
3. **GitHub Releases**: https://github.com/namastexlabs/automagik-hive/releases

## 🆘 Troubleshooting

### Version Mismatch Error

```
❌ Version mismatch!
   pyproject.toml: 0.1.1b2
   Git tag: v0.2.0rc1
```

**Solution**: Tag doesn't match `pyproject.toml`. Run `make bump-rc` before tagging.

### Trusted Publishing Not Configured

```
Error: Trusted publishing exchange failure
```

**Solution**:
1. Verify PyPI trusted publisher settings
2. Ensure GitHub environment names match (`pypi`, `testpypi`)
3. Check workflow name is `publish-pypi.yml`

### Package Already Exists

```
Error: File already exists
```

**Solution**: Version already published. Bump version and retry.

## 🔧 Alternative: API Token Method

If you can't use trusted publishing, you can use API tokens:

1. **Create PyPI API token**: https://pypi.org/manage/account/token/
2. **Add to GitHub Secrets**:
   - Go to: https://github.com/namastexlabs/automagik-hive/settings/secrets/actions
   - Add secret: `PYPI_API_TOKEN`
3. **Update workflow** to use token authentication (not recommended)

## 📚 References

- [PyPI Trusted Publishers](https://docs.pypi.org/trusted-publishers/)
- [GitHub OIDC](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish)
