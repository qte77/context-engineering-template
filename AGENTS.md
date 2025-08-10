# Agent instructions for Context Engineering Template

This file is intended to serve as an entrypoint for AI coding agents, to provide baselines and guardrails concerning this context engineering template project and as a tool for communication between humans and coding agents. As proposed by [agentsmd.net](https://agentsmd.net/) and used by [wandb weave AGENTS.md](https://github.com/wandb/weave/blob/master/AGENTS.md).

## Table of Contents

### Getting Started

- [Path Variables](#path-variables) - Variable resolution and caching
- [Decision Framework for Agents](#decision-framework-for-agents) - Conflict resolution and priorities
- [Core Rules & AI Behavior](#core-rules--ai-behavior) - Fundamental guidelines

### Project Understanding

- [Architecture Overview](#architecture-overview) - System design and data flow
- [Codebase Structure & Modularity](#codebase-structure--modularity) - Organization principles

### Development Workflow

- [Development Commands & Environment](#development-commands--environment) - Setup and execution
- [Unified Command Reference](#unified-command-reference) - All commands with error recovery
- [Style, Patterns & Documentation](#style-patterns--documentation) - Coding standards
- [Code Review & PR Guidelines](#code-review--pr-guidelines) - Quality assurance

### Utilities & References

- [Timestamping for CLI Operations](#timestamping-for-cli-operations) - ISO 8601 standards
- [Agent Quick Reference](#agent-quick-reference---critical-reminders) - Critical reminders
- [Requests to Humans](#requests-to-humans) - Escalation and clarifications

## Path Variables

**IMPORTANT**: All `$VARIABLE` path references in this document are defined in `context/config/paths.md`.

### Agent Setup - Read Once, Cache Locally

**Before starting any task**, agents should:

1. Read `context/config/paths.md` ONCE at the beginning of the session
2. Cache all path variables in memory for the entire session
3. Use cached values to resolve `$VARIABLE` references throughout the task

This eliminates the need to repeatedly read `paths.md` for every variable lookup, significantly improving workflow efficiency.

## Core Rules & AI Behavior

- Use the paths and structure defined in context/config/paths.md.
- Aim for Software Development Lifecycle (SDLC) principles like maintainability, modularity, reusability, and adaptability for coding agents and humans alike
- Adhere to a Behavior Driven Development (BDD) approach which focuses on generating concise goal-oriented Minimum Viable Products (MVPs) with minimal yet functional features sets.
  - Keep it simple!
  - The outlined behavior should be described by defining tests first and implementing corresponding code afterwards.
  - Then iteratively improve tests and code until the feature requirements are met.
  - The iterations should be as concise as possible to keep complexity low
  - All code quality and tests have to be passed to advance to the next step
- Always follow the established coding patterns, conventions, and architectural decisions documented here and in the $DOCS_PATH directory.
- **Never assume missing context.** Ask questions if you are uncertain about requirements or implementation details.
- **Never hallucinate libraries or functions.** Only use known, verified Python packages listed in $PROJECT_REQUIREMENTS.
- **Always confirm file paths and module names** exist before referencing them in code or tests.
- **Never delete or overwrite existing code** unless explicitly instructed to or as part of a documented refactoring task.
- If something doesn't make sense architecturally, from a developer experience standpoint, or product-wise, please add it to the **`Requests to Humans`** section below.
- When you learn something new about the codebase or introduce a new concept, **update this file (`AGENTS.md`)** to reflect the new knowledge. This is YOUR FILE! It should grow and evolve with you.

## Decision Framework for Agents

When facing conflicting instructions or ambiguous situations, use this priority hierarchy:

### Priority Hierarchy

1. **Explicit user instructions** - Always override all other guidelines
2. **AGENTS.md rules** - Override general best practices when specified
3. **paths.md structure** - Source of truth for all path references
4. **Project-specific patterns** - Found in existing codebase
5. **General best practices** - Default fallback for unspecified cases

### Common Conflict Resolution

#### Path Conflicts

- **Always use paths.md** as the definitive source
- If paths.md conflicts with other files, update the other files
- Never hardcode paths that exist as variables

#### Command Execution Conflicts

- **Prefer make commands** when available (e.g., `make ruff` over direct `uv run ruff`)
- If make commands fail, try direct commands as fallback
- Always document when deviating from standard commands

#### Documentation Update Conflicts

- Update **both AGENTS.md and related files** to maintain consistency
- When learning something new, add it to the appropriate section
- Prefer specific examples over vague instructions

### Decision Examples

#### Example 1: Missing Library

**Situation:** Code references library not in `pyproject.toml`

**Decision Process:**

1. User instruction? *(None given)*
2. AGENTS.md rule? *"Never hallucinate libraries"* ✅
3. **Action:** Ask user to confirm library or find alternative

#### Example 2: Test Framework Unclear

**Situation:** Need to write tests but framework not specified

**Decision Process:**

1. User instruction? *(None given)*
2. AGENTS.md rule? *"Always create Hypothesis property-based tests"* ✅  
3. **Action:** Use hypothesis as specified

#### Example 3: Code Organization

**Situation:** File approaching 500 lines

**Decision Process:**

1. User instruction? *(None given)*
2. AGENTS.md rule? *"Never create files longer than 500 lines"* ✅
3. **Action:** Refactor into smaller modules

### When to Stop and Ask

**Always stop and ask for clarification when:**

- Explicit user instructions conflict with safety/security practices
- Multiple AGENTS.md rules contradict each other  
- Required information is completely missing from all sources
- Actions would significantly change project architecture

**Don't stop to ask when:**

- Clear hierarchy exists to resolve the conflict
- Standard patterns can be followed safely
- Minor implementation details need decisions

## Architecture Overview

This is a context engineering template project designed to demonstrate effective AI agent workflows using structured documentation, custom commands, and subagent configurations. The project serves as a foundation for building context-aware AI development environments.

### Data Flow

1. User defines feature requirements in `$CTX_FEATURES_PATH`
2. Code agent generates Feature Requirements Prompts (FRPs) using custom commands
3. Agents execute FRPs with structured context from AGENTS.md and paths.md
4. Results are logged and tracked using standardized workflows
5. Multiple agent systems (Claude, Cline, Gemini) can coordinate through shared configuration

### Key Dependencies

- **uv**: Fast Python dependency management
- **Ruff**: Code formatting and linting  
- **pyright**: Static type checking
- **Hypothesis**: Property-based testing framework
- **Coverage**: Test coverage reporting
- **MkDocs**: Documentation generation (optional)

## Codebase Structure & Modularity

### Main Components

See the "Important files" sections in $CTX_CONFIG_PATH/paths.md for key application entry points and core modules.

**Key Files:**
- `src/main.py`: Main CLI entry point (currently minimal template)
- `$CTX_CONFIG_PATH/paths.md`: Path variable definitions
- `$CTX_FEATURES_PATH`: Feature requirement definitions
- `$CTX_FRP_PATH`: Generated Feature Requirements Prompts
- `$CTX_TEMPLATES_PATH`: Template files for code generation

### Code Organization Rules

- **Never create a file longer than 500 lines of code.** If a file approaches this limit, refactor by splitting it into smaller, more focused modules or helper files.
- Organize code into clearly separated modules grouped by feature.
- Use clear, consistent, and absolute imports within packages.
- **Never name modules/packages after existing Python libraries.** This creates import conflicts and pyright resolution issues.
  - ❌ `src/app/datasets/` (conflicts with HuggingFace `datasets` library)
  - ❌ `src/app/requests/` (conflicts with `requests` library)
  - ❌ `src/app/typing/` (conflicts with built-in `typing` module)
  - ✅ `src/app/utils/datasets_peerread.py` (specific, descriptive naming)
  - ✅ `src/app/api_client/` (instead of `requests`)
  - ✅ `src/app/datamodels/` (instead of `typing`)

## Development Commands & Environment

### Environment Setup

The project requirements are stated in $PROJECT_REQUIREMENTS. Your development environment should be set up automatically using the provided `Makefile`, which configures the virtual environment.

**See the [Unified Command Reference](#unified-command-reference) section for all available commands with error recovery procedures.**

### Code Quality

Code formatting and type checking are managed by **ruff** and **pyright** and orchestrated via the `Makefile`.

### Quality Evaluation Framework

Use this universal framework to assess task readiness before implementation:

**Rate task readiness (1-10 scale):**

- **Context Completeness**: All required information and patterns gathered from codebase, documentation, and requirements
- **Implementation Clarity**: Clear understanding and actionable implementation path of what needs to be built and how to build it.
- **Requirements Alignment**: Solution follows feature requirements, project patterns, conventions, and architectural decisions
- **Success Probability**: Confidence level for completing the task successfully in one pass

**Minimum thresholds for proceeding:**

- Context Completeness: 8/10 or higher
- Implementation Clarity: 7/10 or higher  
- Requirements Alignment: 8/10 or higher
- Success Probability: 7/10 or higher

**If any score is below threshold:** Stop and gather more context, clarify requirements, or escalate to humans using the [Decision Framework](#decision-framework-for-agents).

### Testing Strategy & Guidelines

**Always create comprehensive property-based tests** for new features using the Hypothesis framework:

#### Property-Based Tests (Always Required)

- **Generate test cases automatically** using Hypothesis strategies
- **Test business logic** across wide input ranges with property-based assertions  
- **Test error handling** for boundary conditions and invalid inputs
- **Ensure reproducible failures** with proper random seed management
- Use `hypothesis` with clear property-based testing structure
- Tests must live in the $TEST_PATH folder, mirroring the $APP_PATH structure

#### Integration Tests (When Required)

- **Test real integrations** with generated test data when external dependencies exist
- **Use Hypothesis strategies** to generate realistic test data for external APIs
- **Document external dependencies** and their expected data formats
- **Include in implementation validation** but may use mocked services for CI reliability

#### When to Mock vs Real Testing

- **Property-based for**: Core business logic, data validation, edge case discovery
- **Real integration for**: Initial validation, API contract verification
- **Generated test data for**: Comprehensive coverage across input domains
- **Document test properties** and assumptions in test docstrings

#### Testing Anti-Patterns to Avoid

- ❌ **Only testing fixed examples** without property-based generation
- ❌ **Assuming limited input ranges** without comprehensive coverage
- ❌ **Testing only expected inputs** - always include invalid/boundary cases
- ❌ **Overly specific tests** that fail on implementation refactoring rather than behavior changes

**To run tests** see the [Unified Command Reference](#unified-command-reference) for all testing commands with error recovery procedures.

## Style, Patterns & Documentation

### Coding Style

- Follow established patterns for data validation and contracts when implementing features.
- Use the predefined error message functions for consistency. Update or create new if necessary.
- When writing complex logic, **add an inline `# Reason:` comment** explaining the *why*, not just the *what*.
- Comment non-obvious code to ensure it is understandable to a mid-level developer.

### Documentation

- Write **docstrings for every file, function, class, and method** using the Google style format. This is critical as the documentation site is built automatically from docstrings.

    ```python
    def example_function(param1: int) -> str:
        """A brief summary of the function.

        Args:
            param1 (int): A description of the first parameter.

        Returns:
            str: A description of the return value.
        """
        return "example"
    ```

- Provide an example usage in regards to the whole project. How would your code be integrated, what entrypoints to use
- Update this `AGENTS.md` file when introducing new patterns or concepts.
- Document significant architectural decisions in appropriate documentation files.
- Document all significant changes, features, and bug fixes in $CHANGELOG_PATH.

### Code Pattern Examples

**Reference**: See `$CTX_EXAMPLES_PATH/code-patterns.md` for comprehensive examples including:

- ✅ Structured data handling vs ❌ unstructured approaches
- ✅ Absolute imports vs ❌ relative imports  
- ✅ Specific error handling vs ❌ generic try/catch
- ✅ Complete docstrings vs ❌ minimal documentation
- ✅ Structured testing patterns vs ❌ minimal tests
- ✅ Configuration validation patterns
- ✅ Structured logging approaches

**Quick Reference**: Always prefer type-validated, well-documented code with specific error handling over generic approaches.

## Code Review & PR Guidelines

### Commit and PR Requirements

- **Title Format**: Commit messages and PR titles must follow the **Conventional Commits** specification, as outlined in the `.gitmessage` template.
- Provide detailed PR summaries including the purpose of the changes and the testing performed.

### Pre-commit Checklist

1. **Complete validation**: See [Standard Workflow Commands](#standard-workflow-commands) for full sequence
2. **Quick validation** (development): See [Standard Workflow Commands](#standard-workflow-commands) for fast checks
3. Update documentation as described above.

**Manual fallback** (if make commands fail):

See individual command "Error Recovery" procedures in the [Unified Command Reference](#unified-command-reference) table.

## Timestamping for CLI Operations

- **Always use ISO 8601 timestamps** when creating logs or tracking CLI operations
- **File naming format**: `YYYY-mm-DDTHH-MM-SSZ` (hyphens for filesystem compatibility)
- **Content format**: `YYYY-mm-DDTHH:MM:SSZ` (standard ISO 8601)
- **Implementation**: Use `date -u "+FORMAT"` commands for accurate UTC timestamps

### Timestamp Commands

- Filename timestamp: `date -u "+%Y-%m-%dT%H-%M-%SZ"`
- Content timestamp: `date -u "+%Y-%m-%dT%H:%M:%SZ"`
- Log entry format: `[TIMESTAMP] Action description`

## Auxiliary

- Use [markdownlint's Rules.md](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md) to output well-formatted markdown

## Unified Command Reference

### Path References

- **All paths**: See cached variables from `$CTX_CONFIG_PATH/paths.md`

### Standard Workflow Commands

**Pre-commit checklist** (manual sequence):

1. `make ruff` - Format code and fix linting issues
2. `make check_types` - Run static type checking
3. `make test_all` - Run all property-based tests
4. Update documentation if needed

**Quick development cycle**:

See [Standard Workflow Commands](#standard-workflow-commands) for fast validation steps, then continue development

| Command | Purpose | Prerequisites | Error Recovery |
|---------|---------|---------------|----------------|
| `make setup_dev` | Install all dev dependencies | Makefile exists, uv installed | Try `uv sync --all-groups` directly |
| `make setup_claude_code` | Setup with Claude Code CLI | Above + Claude Code available | Manual setup per Claude docs |
| `make setup_gemini_cli` | Setup Gemini CLI | Above + npm available | Manual setup per Gemini docs |
| `make run_example_gui` | Run example GUI | Dev environment setup | Try manual execution of example |
| `make run_example_server` | Run example server | Above | Try manual execution of example |
| `make run_example_client` | Run example client | Above | Try manual execution of example |
| `make ruff` | Format code and fix linting | Ruff installed | Try `uv run ruff format . && uv run ruff check . --fix` |
| `make check_types` | Run pyright static type checking | pyright installed | Try `uv run pyright $APP_PATH` |
| `make test_all` | Run all hypothesis tests | Hypothesis installed | Try `for test_file in tests/test_*.py; do uv run python "$test_file"; done` |
| `make coverage_all` | Run tests with coverage report | Above + coverage installed | Try `uv run coverage erase && for test_file in tests/test_*.py; do uv run coverage run -a "$test_file"; done && uv run coverage report -m` |
| Sequential validation | Complete pre-commit validation | Above dependencies | See [Standard Workflow Commands](#standard-workflow-commands) |
| `make test_single FILE=<filename>` | Run specific test file | Test file exists | Check test file exists and syntax |

## Requests to Humans

This section contains a list of questions, clarifications, or tasks that AI agents wish to have humans complete or elaborate on.

### Escalation Process

**When to Escalate:**

- Explicit user instructions conflict with safety/security practices
- Rules in AGENTS.md or otherwise provided context contradict each other
- Required information completely missing from all sources
- Actions would significantly change project architecture
- Critical dependencies or libraries are unavailable

**How to Escalate:**

1. **Add to list below** using checkbox format with clear description
2. **Set priority**: `[HIGH]`, `[MEDIUM]`, `[LOW]` based on blocking impact
3. **Provide context**: Include relevant file paths, error messages, or requirements
4. **Suggest alternatives**: What could be done instead, if anything

**Response Format:**

- Human responses should be added as indented bullet points under each item
- Use `# TODO` for non-urgent items with reminder frequency
- Mark completed items with `[x]` checkbox

### Active Requests

- [ ] Consider adding example implementations for common context engineering patterns.
  - Human: `# TODO` but not of priority as of now. Remind me once a week.
- [ ] Improve integration between different agent systems (Claude, Cline, Gemini).
  - Human: `# TODO` but not of priority as of now. Remind me once a week.
- [ ] Add TypeScript testing guidelines (if a TypeScript frontend is planned for the future).
  - Human: `# TODO` but not of priority as of now. Remind me once a week.

## Agent Learning Documentation

When agents discover new patterns, solutions, or important insights, document them here using this template:

### Template for New Learnings

When documenting a new pattern, use this format:

**Structure:**

- **Date**: [ISO timestamp - use `date -u "+%Y-%m-%dT%H:%M:%SZ"`]
- **Context**: [When/where this pattern applies]
- **Problem**: [What issue this solves]
- **Solution**: [Implementation approach]
- **Example**: [Code example with language specified]
- **Validation**: [How to verify this works]
- **References**: [Related files, documentation, or PRs]

**Example Entry:**

```markdown
### Learned Pattern: Context Variable Resolution

- **Date**: 2025-08-10T14:30:00Z
- **Context**: Agent workflows requiring consistent path resolution
- **Problem**: Agents repeatedly reading paths.md causing inefficiency
- **Solution**: Cache path variables once at session start per AGENTS.md guidelines
- **Example**: Read $CTX_CONFIG_PATH/paths.md once, store variables in memory
- **Validation**: Verify path resolution works without repeated file reads
- **References**: AGENTS.md lines 37-43
```

### Active Learning Entries

Agents should add new patterns discovered during development here.

## Agent Quick Reference - Critical Reminders

**Before ANY task, verify:**

- All path variables resolve via $CTX_CONFIG_PATH/paths.md
- Libraries exist in $PROJECT_REQUIREMENTS
- No missing context assumptions

**Documentation tasks:**

- Apply [markdownlint rules](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)
- Use ISO 8601 timestamps (`YYYY-mm-DDTHH:MM:SSZ`)
- Consistent `$VARIABLE` syntax

**Code tasks:**

- Max 500 lines/file
- Create tests in $TEST_PATH directory
- Google-style docstrings
- Verify imports exist

**Always finish with:**

- Follow [pre-commit checklist](#standard-workflow-commands)
- Update AGENTS.md if learned something new

**🛑 STOP if blocked:** Add to "Requests to Humans" rather than assume or proceed with incomplete info
