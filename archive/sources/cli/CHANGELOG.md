# Changelog

All notable changes to Alignerr CLI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-10-13

### Added

- **Core CLI Framework**
  - Renamed from `lbx-cli` to `alignerr` 
  - Implemented typer-based CLI with rich terminal output
  - Added comprehensive help documentation for all commands

- **Domain Management**
  - Self-contained domain structure (config, tasks, evaluators)
  - Domain registry for discovering and managing domains
  - Domain validation and structure checking
  - Support for loading domain configurations from YAML

- **Validation Commands**
  - `alignerr validate` - Run domain validations locally
  - Support for single domain or all domains
  - Configurable parallel execution (default: 4 workers)
  - Pass@k validation with multiple models and runs
  - Model override support
  - Quiet mode for CI/CD integration
  - Custom output directory for reports

- **Migration Tools**
  - `alignerr migrate` - Batch migrate domains from lbx-mcp-envs
  - Automatic conversion of test/ structure to domains/ structure
  - Selective domain migration
  - Custom output directory support
  - Progress tracking with rich console

- **Domain Creation**
  - `alignerr create-domain` - Create new domain structure
  - Template-based domain scaffolding
  - Migration from legacy lbx-mcp-envs structure
  - Automatic README generation

- **Template Cloning**
  - `alignerr clone` - Clone template repository
  - Complete repository structure creation
  - Git initialization and submodule setup
  - Remote URL configuration

- **Information Commands**
  - `alignerr list` - List all available domains
  - `alignerr info` - Show detailed domain/task information
  - `alignerr config` - Display current configuration
  - Detailed and summary views

- **Parallel Execution**
  - Thread-based parallel runner for CPU-bound operations
  - Async-based parallel runner for I/O-bound operations
  - Configurable worker count
  - Progress tracking and error handling
  - Graceful failure handling

- **Report Generation**
  - YAML report format
  - Markdown report format
  - Task summary reports
  - Validation summary reports
  - Timestamped report filenames
  - Pass@k validation metrics

- **Configuration Management**
  - Environment variable support
  - Configuration file support (~/.alignerr/config.json)
  - Configurable domains root, output dir, default model, max workers
  - Config viewing command

- **Core Components**
  - `Domain` - Self-contained domain representation
  - `DomainRegistry` - Domain discovery and management
  - `BenchmarkRunner` - Benchmark execution wrapper
  - `ValidationRunner` - Pass@k validation runner
  - `ParallelRunner` - Parallel execution manager
  - `ReportGenerator` - Multi-format report generation

- **Documentation**
  - Comprehensive README with examples
  - Quick start guide
  - Detailed examples document
  - Architecture documentation
  - Troubleshooting guide

### Features

- ✅ Local validation without external dependencies
- 🚀 Parallel execution for faster results
- 📊 Pass@k testing for quality assurance
- 🔄 Automated migration from lbx-mcp-envs
- 📦 Template cloning for rapid development
- 🎨 Beautiful terminal output with progress bars
- 📁 Self-contained domain structure
- ⚙️  Flexible configuration options

### Technical

- Python 3.12+ support
- Typer for CLI framework
- Rich for terminal output
- Pydantic for data validation
- PyYAML for configuration parsing
- GitPython for repository operations
- Asyncio for parallel execution

### Command Summary

```bash
alignerr validate       # Run domain validations
alignerr migrate        # Migrate from lbx-mcp-envs
alignerr clone          # Clone template repository
alignerr create-domain  # Create new domain
alignerr list           # List domains
alignerr info           # Show domain/task info
alignerr config         # Show configuration
```

## [Unreleased]

### Planned

- Integration with CI/CD pipelines
- Web dashboard for viewing reports
- Real-time validation monitoring
- Domain versioning support
- Task difficulty scoring
- Automatic evaluator generation
- Multi-language support (JS, TS, etc.)
- Docker support for isolated execution
- Cloud storage for reports (S3, GCS)
- Slack/Discord notifications
- Performance benchmarking
- Cost tracking for LLM calls
- Domain templates library
- Interactive domain creation wizard
- Domain composition (combine multiple domains)

### Under Consideration

- GUI application (Electron or Tauri)
- VS Code extension
- GitHub Actions integration
- Domain marketplace
- Collaborative domain development
- A/B testing support
- Historical trend analysis
- Custom evaluation DSL
- Domain dependencies management
- Automatic bug detection in domains

## Migration from lbx-mcp-envs

### Breaking Changes

- Changed CLI name from `lbx-cli` to `alignerr`
- Reorganized domain structure (test/ → domains/{domain}/)
- Renamed entry point from `lbx-cli` to `alignerr`
- Changed config format to self-contained domains

### Migration Guide

1. Install new CLI: `pip install -e .`
2. Migrate domains: `alignerr migrate --source /path/to/lbx-mcp-envs`
3. Validate domains: `alignerr validate --all`
4. Update any scripts to use `alignerr` instead of old commands

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Support

For issues or questions:
- Create an issue in the repository
- Check the documentation
- Contact the development team

---

[0.1.0]: https://github.com/YOUR_ORG/lbx_mcp_universe_cli/releases/tag/v0.1.0

