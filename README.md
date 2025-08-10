# Context Engineering Template

AI-driven development using structured requirements: Business Requirements (BRD) → Product Requirements (PRD) → Feature Requirements Prompts (FRPs). Supports both comprehensive business-driven development and quick feature prototyping.

[![License](https://img.shields.io/badge/license-GNUGPLv3-green.svg)](LICENSE)
![Version](https://img.shields.io/badge/version-0.0.2-58f4c2)
[![CodeQL](https://github.com/qte77/context-engineering-template/actions/workflows/codeql.yaml/badge.svg)](https://github.com/qte77/context-engineering-template/actions/workflows/codeql.yaml)
[![CodeFactor](https://www.codefactor.io/repository/github/qte77/context-engineering-template/badge)](https://www.codefactor.io/repository/github/qte77/context-engineering-template)
[![ruff](https://github.com/qte77/context-engineering-template/actions/workflows/ruff.yaml/badge.svg)](https://github.com/qte77/context-engineering-template/actions/workflows/ruff.yaml)
[![pytest](https://github.com/qte77/context-engineering-template/actions/workflows/pytest.yaml/badge.svg)](https://github.com/qte77/context-engineering-template/actions/workflows/pytest.yaml)

**DevEx**  [![vscode.dev](https://img.shields.io/static/v1?logo=visualstudiocode&label=&message=vscode.dev&labelColor=2c2c32&color=007acc&logoColor=007acc)](https://vscode.dev/github/qte77/context-engineering-template)
[![Codespace](https://img.shields.io/static/v1?logo=visualstudiocode&label=&message=Codespace%20Dev&labelColor=2c2c32&color=007acc&logoColor=007acc)](https://github.com/codespaces/new?repo=qte77/context-engineering-template&devcontainer_path=.devcontainer/devcontainer.json)

## Features

- **Business-Driven Development**: Complete BRD → PRD → FRP workflow
- **Legacy Development**: Direct feature implementation (quick prototyping)
- **Quality Assurance**: Automated tests, linting, and type checks
- **Multiple Agent Support**: Claude Code, Cline, and Gemini configurations

## Quick Start

```bash
# 1. Setup environment
make setup_dev

# 2. Try business-driven approach with existing example
make brd_gen_claude "ARGS=example_ai_assistant.md"
make prd_gen_claude "ARGS=example_ai_assistant.md"  
make frp_gen_claude "ARGS=example_ai_assistant.md task_automation"
make frp_exe_claude "ARGS=example_ai_assistant_task_automation.md"
```

## Usage

### Business-Driven Development (Recommended)

1. **Create business input**: `cp context/templates/business_input_base.md context/business_inputs/my_project.md`
2. **Generate BRD**: `make brd_gen_claude "ARGS=my_project.md"`
3. **Generate PRD**: `make prd_gen_claude "ARGS=my_project.md"`
4. **Generate FRPs**: `make frp_gen_claude "ARGS=my_project.md feature_name"`
5. **Implement**: `make frp_exe_claude "ARGS=my_project_feature_name.md"`

### Legacy Development

1. **Create feature**: `cp context/templates/feature_base.md context/features/my_feature.md`
2. **Generate FRP**: `make frp_gen_legacy_claude "ARGS=my_feature.md"`
3. **Implement**: `make frp_exe_legacy_claude "ARGS=my_feature.md"`

## Documentation

- **[Usage Guide](docs/usage-guide.md)** - Detailed workflow instructions
- **[Examples](docs/examples.md)** - Complete examples and demonstrations
- **[AGENTS.md](AGENTS.md)** - Agent configuration and behavior
- **[examples/mcp-server-client/](examples/mcp-server-client/)** - Working MCP implementation

## Status

**Current**: (DRAFT) (WIP) - Core functionality implemented, refinements ongoing

See [CHANGELOG.md](CHANGELOG.md) for version history.
