# Context Engineering Template

Business workflow system with AI agent support. Evolving toward intelligent orchestration: from business analysis to requirements to implementation.

[![License](https://img.shields.io/badge/license-GNUGPLv3-green.svg)](LICENSE)
![Version](https://img.shields.io/badge/version-0.0.2-58f4c2)
[![CodeQL](https://github.com/qte77/context-engineering-template/actions/workflows/codeql.yaml/badge.svg)](https://github.com/qte77/context-engineering-template/actions/workflows/codeql.yaml)
[![CodeFactor](https://www.codefactor.io/repository/github/qte77/context-engineering-template/badge)](https://www.codefactor.io/repository/github/qte77/context-engineering-template)
[![ruff](https://github.com/qte77/context-engineering-template/actions/workflows/ruff.yaml/badge.svg)](https://github.com/qte77/context-engineering-template/actions/workflows/ruff.yaml)
[![pytest](https://github.com/qte77/context-engineering-template/actions/workflows/pytest.yaml/badge.svg)](https://github.com/qte77/context-engineering-template/actions/workflows/pytest.yaml)

**DevEx**  [![vscode.dev](https://img.shields.io/static/v1?logo=visualstudiocode&label=&message=vscode.dev&labelColor=2c2c32&color=007acc&logoColor=007acc)](https://vscode.dev/github/qte77/context-engineering-template)
[![Codespace](https://img.shields.io/static/v1?logo=visualstudiocode&label=&message=Codespace%20Dev&labelColor=2c2c32&color=007acc&logoColor=007acc)](https://github.com/codespaces/new?repo=qte77/context-engineering-template&devcontainer_path=.devcontainer/devcontainer.json)

## Product State & Vision

### Current State

- **Template-based business workflow system** for small teams (5-25 people) using BRD→PRD→FRP generation via make commands with Claude Code. Cline and Gemini configurations are present as fall-back solutions.

### CABIO Vision

- **Context-aware business intelligence orchestration** (CABIO) evolving from enhanced templates with agent orchestration (8-12 weeks) to real-time market data integration and enterprise scalability (12+ months)

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

**Template-based business workflow system for small teams (5-25 people).**

Structured BRD → PRD → FRP workflow with AI agent configurations. Currently uses templates and make commands, evolving toward automated business intelligence orchestration.

**Problem**: Small teams need structured business analysis but lack dedicated resources for professional frameworks.

**Current Solution**: Template-driven workflow with Claude Code, Cline, and Gemini agent support

**Evolution Path**: Enhanced templates → context management → intelligent agent orchestration (CABIO)

### Current Capabilities (Template System)

- **Business-Driven Development**: Complete BRD → PRD → FRP workflow via templates
- **AI Agent Configurations**: Ready-to-use prompts for Claude Code, Cline, and Gemini
- **Quality Automation**: Integrated testing, linting, and validation workflows
- **Professional Output**: Business documentation ready for stakeholders

### Enhanced Templates (8-12 weeks)

- **Agent Orchestration**: Automated handoffs between specialized AI agents
- **Context Compression**: Smart information filtering and allocation
- **Market Research Integration**: Templates with competitive analysis frameworks
- **Context Preservation**: Better information flow between analysis phases
- **Streamlined Workflow**: Reduced manual editing and refinement time

### CABIO Vision (12+ months)

- **Real-time Intelligence**: Live market data and competitive monitoring
- **Enterprise Scalability**: Advanced workflows for larger organizations
- **Accessible Intelligence**: Professional business analysis without dedicated specialists
- **Faster Iterations**: Complete business requirements in hours rather than days

## Evolution: CABIO (Context-Aware Business Intelligence Orchestration)

**Goal**: Transform template-based workflow into intelligent agent orchestration.

Building on proven BRD→PRD→FRP foundation, CABIO represents our evolution path: enhanced templates (8-12 weeks) → agent orchestration → comprehensive business intelligence for small teams scaling to larger organizations.

### Learn More

- **[CABIO Vision](docs/CABIO-vision.md)** - Why business intelligence should be automated and contextual
- **[CABIO Product Roadmap](docs/CABIO-product-roadmap.md)** - Customer value, target markets, and feature development  
- **[CABIO Implementation Guide](docs/CABIO-implementation-guide.md)** - Technical architecture and implementation roadmap

**Development**: Iterative approach starting with enhanced templates for small teams (8-12 weeks), then agent orchestration, expanding based on validation and user feedback. Current BRD→PRD→FRP workflow remains the foundation.

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

**Current**: Template-based BRD→PRD→FRP workflow functional for small teams. Enhanced templates in development (8-12 weeks), CABIO orchestration planned (12+ months).

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Documentation

- **[Usage Guide](docs/usage-guide.md)** - Detailed workflow instructions
- **[Examples](docs/examples.md)** - Complete examples and demonstrations
- **[AGENTS.md](AGENTS.md)** - Agent configuration and behavior
- **[examples/mcp-server-client/](examples/mcp-server-client/)** - Working MCP implementation
