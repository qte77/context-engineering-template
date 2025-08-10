# Context Engineering Template

Context-aware business analysis that orchestrates AI agents from requirements to implementation.

[![License](https://img.shields.io/badge/license-GNUGPLv3-green.svg)](LICENSE)
![Version](https://img.shields.io/badge/version-0.0.2-58f4c2)
[![CodeQL](https://github.com/qte77/context-engineering-template/actions/workflows/codeql.yaml/badge.svg)](https://github.com/qte77/context-engineering-template/actions/workflows/codeql.yaml)
[![CodeFactor](https://www.codefactor.io/repository/github/qte77/context-engineering-template/badge)](https://www.codefactor.io/repository/github/qte77/context-engineering-template)
[![ruff](https://github.com/qte77/context-engineering-template/actions/workflows/ruff.yaml/badge.svg)](https://github.com/qte77/context-engineering-template/actions/workflows/ruff.yaml)
[![pytest](https://github.com/qte77/context-engineering-template/actions/workflows/pytest.yaml/badge.svg)](https://github.com/qte77/context-engineering-template/actions/workflows/pytest.yaml)

**DevEx**  [![vscode.dev](https://img.shields.io/static/v1?logo=visualstudiocode&label=&message=vscode.dev&labelColor=2c2c32&color=007acc&logoColor=007acc)](https://vscode.dev/github/qte77/context-engineering-template)
[![Codespace](https://img.shields.io/static/v1?logo=visualstudiocode&label=&message=Codespace%20Dev&labelColor=2c2c32&color=007acc&logoColor=007acc)](https://github.com/codespaces/new?repo=qte77/context-engineering-template&devcontainer_path=.devcontainer/devcontainer.json)

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

## The Current Product

**AI-powered business intelligence for development teams.**

Structured business analysis workflow that transforms ideas into development requirements. Currently supports BRD → PRD → FRP generation with AI agents, evolving toward comprehensive business intelligence orchestration.

**Problem**: Business decisions often happen in silos - market research, strategy, and requirements development are disconnected and time-intensive.

**Approach**: Structured business analysis workflow with AI agent support, evolving toward intelligent orchestration that connects analysis phases and preserves context.

**Current**: BRD → PRD → FRP workflow with AI agent support

**Direction**: Context-aware business intelligence that scales from individual projects to organizational decision-making.

### Current Benefits

- **Structured Workflow**: Clear BRD → PRD → FRP development process
- **AI Agent Support**: Claude Code, Cline, and Gemini configurations
- **Template-Based Analysis**: Consistent business requirements generation
- **Quality Automation**: Integrated testing, linting, and validation

### Future Outlook

- **Connected Analysis**: Market research, strategy, and requirements in coordinated workflows
- **Context Preservation**: Insights that build progressively as analysis deepens  
- **Accessible Intelligence**: Professional business analysis without dedicated specialists
- **Faster Iterations**: Complete business requirements in hours rather than days

### Current Features

- **Business-Driven Development**: Complete BRD → PRD → FRP workflow  
- **Agent Orchestration**: Claude Code, Cline, and Gemini configurations
- **Context Engineering**: Smart information filtering and progressive analysis
- **Quality Assurance**: Automated validation, testing, and type checking

## Next Evolution: CABIO (Context-Aware Business Intelligence Orchestration)

**Goal**: Evolve from structured workflows to intelligent business analysis.

Building on the current BRD→PRD→FRP foundation, CABIO will orchestrate specialized AI agents for coordinated business intelligence - starting with market research and competitive analysis, expanding toward comprehensive strategic support.

### Learn More

- **[CABIO Vision](docs/CABIO-vision.md)** - Why business intelligence should be automated and contextual
- **[CABIO Product Roadmap](docs/CABIO-product-roadmap.md)** - Customer value, target markets, and feature development  
- **[CABIO Implementation Guide](docs/CABIO-implementation-guide.md)** - Technical architecture and implementation roadmap

**Development**: Iterative approach starting with core agent coordination, expanding capabilities based on validation and feedback

## Comprehensive Usage

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

## Status

**Current**: (DRAFT) (WIP) - Core BRD→PRD→FRP workflow functional, expanding toward intelligent orchestration

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Documentation

- **[Usage Guide](docs/usage-guide.md)** - Detailed workflow instructions
- **[Examples](docs/examples.md)** - Complete examples and demonstrations
- **[AGENTS.md](AGENTS.md)** - Agent configuration and behavior
- **[examples/mcp-server-client/](examples/mcp-server-client/)** - Working MCP implementation
