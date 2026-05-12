# MCP Universe benchmarks (template)

Monorepo for **MCP-backed agent benchmarks**: domains live under `domains/`, execution goes through the bundled CLI submodule, and tools ship in the mothership submodule. See [BENCHMARK_FRAMEWORK.md](BENCHMARK_FRAMEWORK.md) and [REPO_LAYOUT.md](REPO_LAYOUT.md) for what is core versus optional dashboard/API code (`frontend/`, `backend/`).

## 🚀 Quick Start

```bash
# Init and update all git submodules
git submodule update --init --recursive

# Install dependencies
uv sync

# Copy the example environment file
cp .env.example .env

# Edit .env with your actual API keys
# You only need to populate the keys for the services you plan to use

# Run CLI command examples and --help
uv run alignerr_mcp --help
uv run alignerr_mcp list
```

## 🏆 Reference Implementation Included

This template ships a **reference domain** [**web_search**](domains/web_search) and additional examples such as [**google_workspace**](domains/google_workspace).

- High-quality task sets
- **Domain-specific evaluators**
- **Complete documentation**
- **Best practices demonstrated**

Use this as your guide when creating new domains!


## Contribution

Below you will find a high level steps explaining how to contribute to the new domain creation.
For details instructions, please visit [this google docs link](https://docs.google.com/document/d/1X7-J5zLNQvFVwqk6PX0lFW22rQf5WTBj11g_v5d6tTc).

### 1. Create your own domain

```bash
# Create domain structure
uv run alignerr_mcp create-domain --name {your-domain}
```

### 2. Implement your domain

Edit the generated files to implement your domain logic. Refer to the [STRUCTURE_GUIDE.md](STRUCTURE_GUIDE.md) to learn about the files and contents formats.

**⚠️ Critical**: You **must** follow the exact structure and format of existing domains in the `domains/` directory. Review reference implementations thoroughly and replicate their:
- File structure and naming conventions
- JSON schema and field formats  
- Evaluator implementation patterns
- Documentation style

Deviations from the established structure will cause validation failures.

### 3. Test locally

```bash
# Validate domain
uv run alignerr_mcp validate --domain {your-domain}

# Pass@k validation
uv run alignerr_mcp validate --domain {your-domain} --runs 3

# Parallel execution with specific model
uv run alignerr_mcp validate --domain {your-domain} --model claude-3-5-sonnet-20241022 --parallel 8
```

### 4. Create a Pull Request

**Fork the repository first**, then:

```bash
# Create feature branch
git checkout -b domains/{your-domain}/v1

# Commit your domain
git add domains/{your-domain}/
git commit -m "Add {your-domain} domain with variation_1"

# Push to your fork
git push origin domains/{your-domain}/v1

# Create a PR from your fork to the main repository
```

**Automated Evaluation**: Once you create a PR, the evaluator will automatically run and post an HTML report as a comment. The same comment will be updated every time you push changes to your PR branch.

### Key Principle

> **Model failures are the goal.** We're building a benchmark to identify where models struggle, not to showcase their successes. Reproducible task design is paramount.

## Best Practices

- **Test locally** before pushing
- **Keep submodules updated** regularly
- **Never commit secrets** to git
- **Design for difficulty**: Create challenging tasks that expose model limitations
- **Verify expected outputs**: Ensure 100% confidence in expected results
- **Test reproducibility**: Run multiple times to confirm consistent results

## Troubleshooting

### CLI Commands Not Found

**Problem**: Running `alignerr_mcp` or `alignerr` shows "command not found"

**Solutions**:

1. **Use `uv run` (recommended)**:
   ```bash
   uv run alignerr_mcp --help
   ```

2. **Check your Python environment**:
   ```bash
   which python  # Should point to .venv/bin/python
   uv pip list | grep alignerr  # Should show alignerr-cli
   ```

3. **Reinstall if needed**:
   ```bash
   uv sync --reinstall
   ```

### Submodule Issues

**Problem**: CLI submodule is empty or missing

**Solution**:
```bash
# Initialize and update submodules
git submodule update --init --recursive

# Then reinstall
uv sync
```

**Problem**: Failures to install MCP Servers

**Solution**:
```bash
# Install required servers
uv run alignerr_mcp servers install google_search

# Install server in uv environment (in case the above does not work)
uv pip install -e "<path to lbx_mcp_universe_mcp_servers_mothership>/servers/<server name>"
```
