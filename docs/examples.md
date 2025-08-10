# Examples

This document provides detailed examples and demonstrations of the Context Engineering Template workflows.

## MCP Server-Client Example

The `examples/mcp-server-client` directory contains a complete implementation demonstrating the context engineering workflow with a real-world AI-powered assistant project.

### What It Demonstrates

The MCP server-client example shows:

- **Business Requirements**: AI-powered task automation for small businesses
- **Product Features**: Natural language interface, tool integration, real-time responses
- **Technical Implementation**: MCP protocol, Streamlit GUI, async client-server architecture

### Development Mode

Use these commands for development and testing:

```bash
# Launch interactive GUI (Streamlit)
make run_example_gui

# Run MCP server only
make run_example_server

# Run MCP client with specific tool
make run_example_client ARGS="get_weather"
make run_example_client ARGS="roll_dice"
make run_example_client ARGS="get_date"
```

### Production Mode

For production deployment:

```bash
# Run complete system with Docker Compose
make run_example_full

# Run with specific configuration
make run_example_full ARGS="--build"
```

### Detailed Documentation

See `examples/mcp-server-client/README.md` for:

- Complete setup instructions
- API documentation
- Architecture details
- Testing procedures

## Business Input Examples

### AI Assistant Project

Located at `context/business_inputs/example_ai_assistant.md`, this example shows:

- Complete business problem statement
- Target user personas and market analysis
- Success metrics and business constraints
- Stakeholder requirements and risk assessment

### Usage Pattern

```bash
# Use the existing example
make brd_gen_claude "ARGS=example_ai_assistant.md"

# Or create your own
cp context/templates/business_input_base.md context/business_inputs/my_project.md
# Edit with your business information
make brd_gen_claude "ARGS=my_project.md"
```

## Workflow Examples

### Complete Business-Driven Example

This example walks through the entire BRD → PRD → FRP workflow:

```bash
# 1. Start with business input
cp context/business_inputs/example_ai_assistant.md context/business_inputs/my_assistant.md

# 2. Generate business requirements
make brd_gen_claude "ARGS=my_assistant.md"

# 3. Create product specifications
make prd_gen_claude "ARGS=my_assistant.md"

# 4. Generate technical specifications for specific features
make frp_gen_claude "ARGS=my_assistant.md task_management"
make frp_gen_claude "ARGS=my_assistant.md email_integration"

# 5. Implement features
make frp_exe_claude "ARGS=my_assistant_task_management.md"
make frp_exe_claude "ARGS=my_assistant_email_integration.md"
```

### Legacy Quick Prototype Example

For rapid prototyping without business context:

```bash
# 1. Create feature description
echo "# Quick Chat Feature
A simple chat interface for user interaction" > context/features/quick_chat.md

# 2. Generate FRP
make frp_gen_legacy_claude "ARGS=quick_chat.md"

# 3. Implement
make frp_exe_legacy_claude "ARGS=quick_chat.md"
```

## Template Examples

### Business Input Template Usage

The business input template (`context/templates/business_input_base.md`) provides:

- Structured sections for business problem statement
- User persona and market context templates
- Success metrics and constraints frameworks
- Risk assessment guidelines

### BRD Template Features

The BRD template (`context/templates/brd_base.md`) includes:

- Comprehensive business analysis framework
- Stakeholder requirement mapping
- Risk mitigation strategies
- Success validation approaches

## Integration Examples

### Multiple Agent Workflows

The system supports multiple AI agent configurations:

- **Claude Code**: Primary development agent
- **Cline**: Alternative development environment
- **Gemini**: Additional agent support

### API Integration Patterns

Examples show integration with:

- Google Workspace APIs
- Microsoft 365 services
- Custom business APIs
- Third-party tool integrations

## Best Practices

### File Naming Conventions

- Business inputs: `context/business_inputs/project_name.md`
- Generated BRDs: `context/BRDs/project_name.md`
- Generated PRDs: `context/PRDs/project_name.md`
- Feature FRPs: `context/FRPs/project_name_feature_name.md`

### Workflow Recommendations

1. **Start Small**: Begin with one core feature
2. **Iterate Quickly**: Use the business-driven approach for comprehensive features
3. **Test Early**: Implement and test each feature independently
4. **Document Changes**: Update business requirements as you learn

### Common Patterns

- **Feature Dependencies**: Handle in PRD feature sequencing
- **Shared Components**: Identify in business requirements phase
- **Integration Points**: Plan during product requirements phase
- **Error Handling**: Include in feature requirements prompts

## Troubleshooting Examples

### Failed BRD Generation

If BRD generation fails:

```bash
# Check input file exists
ls -la context/business_inputs/

# Verify template accessibility
ls -la context/templates/business_input_base.md

# Try interactive approach instead
/generate-brd my_project.md
```

### Incomplete Feature Implementation

If feature implementation is incomplete:

```bash
# Check FRP quality
cat context/FRPs/project_feature.md

# Re-run with more context
make frp_exe_claude "ARGS=project_feature.md"

# Check for missing dependencies
make check_types
make test_all
```
