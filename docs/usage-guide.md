# Usage Guide

This guide provides detailed instructions for using the Context Engineering Template with both business-driven and legacy development approaches.

## Business-Driven Development (Recommended)

Complete workflow from business requirements to feature implementation using the BRD → PRD → FRP approach.

### 1. Define Business Context

Choose one of the following approaches based on your available business information:

#### Option A: Business Input Document (Recommended)

Start with a structured business input document:

```bash
# Step 1a: Create business input using template
cp context/templates/business_input_base.md context/business_inputs/my_project.md
# Edit the file with your business information

# Step 1b: Generate comprehensive BRD
/generate-brd my_project.md
# Or via make:
make brd_gen_claude "ARGS=my_project.md"
```

#### Option B: Interactive Session

Let the AI interview you to gather requirements:

```bash
# AI will ask questions to gather business requirements
/generate-brd my_project.md
# Or via make:
make brd_gen_claude "ARGS=my_project.md"
```

#### Option C: Complete Partial BRD

Start with the BRD template and fill some sections:

```bash
# Step 1c: Start with BRD template, fill some sections
cp context/templates/brd_base.md context/BRDs/my_project.md
# Edit file partially, then let AI complete it

# Step 1d: Generate completed BRD
/generate-brd my_project.md
# Or via make:
make brd_gen_claude "ARGS=my_project.md"
```

### 2. Create Product Requirements

Translate business objectives into product features and user stories:

```bash
# Translates BRD business objectives into product features and user stories
/generate-prd-from-brd my_project.md
# Or via make:
make prd_gen_claude "ARGS=my_project.md"
```

### 3. Generate Feature-Specific FRPs

Create technical specifications for each feature (repeat for each feature):

```bash
# Example: Generate FRP for "task_automation" feature
/generate-frp-from-prd my_project.md task_automation
# Or via make:
make frp_gen_claude "ARGS=my_project.md task_automation"

# This creates: context/FRPs/my_project_task_automation.md
```

### 4. Implement Features

Implement features one at a time:

```bash
# Implement the task automation feature
/execute-frp my_project_task_automation.md
# Or via make:
make frp_exe_claude "ARGS=my_project_task_automation.md"
```

### Complete Example Workflow

Here's a complete example using the AI assistant project:

```bash
# 1. Create business input document
cp context/templates/business_input_base.md context/business_inputs/ai_assistant.md
# Edit ai_assistant.md with your business details

# 2. Generate comprehensive BRD
make brd_gen_claude "ARGS=ai_assistant.md"

# 3. Create product requirements from BRD
make prd_gen_claude "ARGS=ai_assistant.md"

# 4. Generate FRPs for each feature
make frp_gen_claude "ARGS=ai_assistant.md task_automation"
make frp_gen_claude "ARGS=ai_assistant.md calendar_integration"
make frp_gen_claude "ARGS=ai_assistant.md email_processing"

# 5. Implement features one by one
make frp_exe_claude "ARGS=ai_assistant_task_automation.md"
make frp_exe_claude "ARGS=ai_assistant_calendar_integration.md"  
make frp_exe_claude "ARGS=ai_assistant_email_processing.md"
```

## Legacy Development Approach {#legacy}

Quick prototyping without comprehensive business context:

### Steps

1. Update [AGENTS.md](../AGENTS.md) to your needs
2. Describe desired feature in `/context/features/feature_XXX.md`, using [feature_base.md](../context/templates/feature_base.md) as template
3. Place optional examples into `/context/examples/`
4. Generate Feature Requirements Prompt (FRP):
   - In Claude Code CLI: `/generate-frp feature_XXX.md`
   - Or via make: `make frp_gen_legacy_claude "ARGS=feature_XXX.md"`
5. Implement feature based on the FRP:
   - In Claude Code CLI: `/execute-frp feature_XXX.md`
   - Or via make: `make frp_exe_legacy_claude "ARGS=feature_XXX.md"`

## Configuration

### System Configuration

- **General system behavior**: `AGENTS.md`, redirected from `CLAUDE.md`
- **Claude settings**: `.claude/settings.local.json`
- **Claude commands**: `.claude/commands`

### Document Templates

- **Business Input**: `context/templates/business_input_base.md` (initial business info)
- **Business Requirements**: `context/templates/brd_base.md`
- **Product Requirements**: `context/templates/prd_base.md`
- **Feature Requirements**: `context/templates/frp_base.md`
- **Feature Description**: `context/templates/feature_base.md` (legacy)

### Document Organization

```bash
context/
├── business_inputs/  # Initial business information documents
├── BRDs/            # Business Requirements Definitions
├── PRDs/            # Product Requirements Documents
├── FRPs/            # Feature Requirements Prompts
├── features/        # Direct feature descriptions (legacy)
└── templates/       # Document templates
```

## Environment Setup

### API Keys

[.env.example](../.env.example) contains examples for usage of API keys and variables:

```text
ANTHROPIC_API_KEY="sk-abc-xyz"
GEMINI_API_KEY="xyz"
GITHUB_API_KEY="ghp_xyz"
```

### Development Environment

1. `make setup_dev` - Complete development setup
2. `make export_env_file` - Export environment variables (if using .env)

## Troubleshooting

### Common Issues

- **Missing API Keys**: Ensure your API keys are set in `.env` or environment variables
- **Claude Code CLI Issues**: Run `make setup_claude_code` to reinstall
- **Permission Issues**: Ensure you have write permissions to the context directories

### Getting Help

- Check [AGENTS.md](../AGENTS.md) for system behavior configuration
- Review command definitions in `.claude/commands/`
- See example implementations in `examples/`
