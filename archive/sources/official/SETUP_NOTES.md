# Setup Notes

## Git Submodules Configuration

This template includes the CLI tools as a git submodule. The `.gitmodules` file contains a placeholder URL that needs to be updated when pushing to GitHub.

### Initial Setup (Local Development)

For local development, the CLI directory has been copied into this repository. When you're ready to push to GitHub:

1. **Push the CLI repository first:**

```bash
cd ../lbx_mcp_universe_cli
git remote add origin git@github.com:Alignerr-Code-Labeling/lbx_mcp_universe_cli.git
git push -u origin main
```

2. **Update the .gitmodules file in this template repo:**

Edit `.gitmodules` and replace `YOUR_ORG` with your actual GitHub organization/username:

```ini
[submodule "lbx_mcp_universe_cli"]
	path = lbx_mcp_universe_cli
	url = https://github.com/Alignerr-Code-Labeling/lbx_mcp_universe_cli.git
```

3. **Remove the copied CLI directory and add as proper submodule:**

```bash
# Remove the copied directory
git rm -rf lbx_mcp_universe_cli

# Add as proper submodule
git submodule add git@github.com:Alignerr-Code-Labeling/lbx_mcp_universe_cli.git lbx_mcp_universe_cli

# Commit the change
git add .gitmodules lbx_mcp_universe_cli
git commit -m "Set up CLI as proper git submodule"
```

4. **Update the sync workflow:**

Edit `.github/workflows/sync-to-mother.yml` and update the mothership repository URL:

```yaml
# Find this line:
git clone https://x-access-token:${GH_TOKEN}@github.com/Alignerr-Code-Labeling/lbx_mcp_universe_mothership.git mothership
```

5. **Push the template repository:**

```bash
git remote add origin git@github.com:Alignerr-Code-Labeling/lbx_mcp_universe_template.git
git push -u origin main
```

### Working with Submodules After Setup

Once properly configured with GitHub remotes:

```bash
# Clone with submodules
git clone --recurse-submodules git@github.com:Alignerr-Code-Labeling/lbx_mcp_universe_template.git

# Initialize submodules in existing clone
git submodule update --init --recursive

# Update submodules to latest version
git submodule update --remote --merge

# Check submodule status
git submodule status
```

## GitHub Secrets Required

Before using the CI/CD workflows, configure these secrets:

### Organization-level (Recommended)

```bash
gh secret set GH_ACCESS_TOKEN_WORKFLOW \
  --org Alignerr-Code-Labeling \
  --body "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

gh secret set ANTHROPIC_API_KEY \
  --org Alignerr-Code-Labeling \
  --body "sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### Repository-level (Alternative)

```bash
gh secret set GH_ACCESS_TOKEN_WORKFLOW \
  --body "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

## Creating the GH_ACCESS_TOKEN_WORKFLOW

1. Go to GitHub Settings → Developer Settings → Personal Access Tokens → Fine-grained tokens
2. Click "Generate new token"
3. Configure:
   - **Token name**: `lbx-mcp-workflow-token`
   - **Expiration**: 1 year
   - **Repository access**: Select repositories or organization-wide
   - **Permissions**:
     - Repository permissions:
       - Contents: Read and Write
       - Metadata: Read-only
       - Pull requests: Read and Write
       - Workflows: Read and Write

4. Generate and save the token securely

## Testing the Setup

```bash
# Install CLI
cd lbx_mcp_universe_cli
uv pip install -e .
cd ..

# Install template
uv pip install -e .

# Verify
lbx-cli --version
```

## Next Steps

1. Create your domain repository from this template
2. Implement your domain-specific logic
3. Test locally with validation commands
4. Create a PR to trigger CI/CD workflows
5. Merge to trigger sync to mothership

