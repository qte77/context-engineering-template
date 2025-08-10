# Agent instructions for `Agents-eval` repository

This file is intended to serve as an entrypoint for AI coding agents, to provide baselines and guardrails concerning this project and as a tool for communication between humans and coding agents. As proposed by [agentsmd.net](https://agentsmd.net/) and used by [wandb weave AGENTS.md](https://github.com/wandb/weave/blob/master/AGENTS.md).

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

- Use the paths and structure defined in $DEFAULT_PATHS_MD (located at context/config/paths.md).
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
2. AGENTS.md rule? *"Always create Pytest unit tests"* ✅  
3. **Action:** Use pytest as specified

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

This is a Multi-Agent System (MAS) evaluation framework for assessing agentic AI systems. The project uses **PydanticAI** as the core framework for agent orchestration and is designed for evaluation purposes, not for production agent deployment.

### Data Flow

1. User input → Manager Agent (can be single-LLM)
2. Optional: Manager delegates to Researcher Agent (with DuckDuckGo search)
3. Optional: Researcher results → Analyst Agent for validation
4. Optional: Validated data → Synthesizer Agent for report generation
5. Results evaluated using configurable metrics

### Key Dependencies

- **PydanticAI**: Agent framework and orchestration
- **uv**: Fast Python dependency management
- **Streamlit**: GUI framework
- **Ruff**: Code formatting and linting
- **pyright**: Static type checking

## Codebase Structure & Modularity

### Main Components

See the "Important files" sections in $DEFAULT_PATHS_MD for key application entry points and core modules.

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

**Always create comprehensive tests** for new features following the testing hierarchy below:

#### Unit Tests (Always Required)

- **Mock external dependencies** (HTTP requests, file systems, APIs) using `@patch`
- **Test business logic** and data validation thoroughly
- **Test error handling** for all failure modes and edge cases
- **Ensure deterministic behavior** - tests should pass consistently
- Use `pytest` with clear arrange/act/assert structure
- Tests must live in the $TEST_PATH folder, mirroring the $APP_PATH structure

#### Integration Tests (Required for External Dependencies)

- **Test real external integrations** at least once during implementation
- **Verify actual URLs, APIs, and data formats** work as expected
- **Document any external dependencies** that could change over time
- **Use real test data** when feasible, fallback to representative samples
- **Include in implementation validation** but may be excluded from CI if unreliable

#### When to Mock vs Real Testing

- **Mock for**: Unit tests, CI/CD pipelines, deterministic behavior, fast feedback
- **Real test for**: Initial implementation validation, external API changes, data format verification
- **Always test real integrations** during feature development, then mock for ongoing automated tests
- **Document real test results** in implementation logs for future reference

#### Testing Anti-Patterns to Avoid

- ❌ **Only mocking external dependencies** without ever testing real integration
- ❌ **Assuming external APIs work** without verification during implementation
- ❌ **Testing only happy paths** - always include error cases
- ❌ **Brittle tests** that break with minor changes to implementation details

**To run tests** see the [Unified Command Reference](#unified-command-reference) for all testing commands with error recovery procedures.

## Style, Patterns & Documentation

### Coding Style

- **Use Pydantic** models in $DATAMODELS_PATH for all data validation and data contracts. **Always use or update these models** when modifying data flows.
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
- Document significant architectural decisions in $ADR_PATH.
- Document all significant changes, features, and bug fixes in $CHANGELOG_PATH.

### Code Pattern Examples

**Reference**: See `${CTX_EXAMPLES_PATH}/code-patterns.md` for comprehensive examples including:

- ✅ Pydantic model usage vs ❌ direct dictionaries
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

1. **Automated validation**: `make validate` - runs complete sequence (ruff + type_check + test_all)
2. **Quick validation** (development): `make quick_validate` - runs fast checks (ruff + type_check only)
3. Update documentation as described above.

**Manual fallback** (if make commands fail):

1. `uv run ruff format . && uv run ruff check . --fix`
2. `uv run pyright`
3. `uv run pytest`

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

- **All paths**: See cached variables from `context/config/paths.md`

### Standard Workflow Commands

**Pre-commit checklist** (automated):

1. `make validate` - Complete validation sequence (ruff + type_check + test_all)
2. Update documentation if needed

**Quick development cycle**:

1. `make quick_validate` - Fast validation (ruff + type_check only)
2. Continue development

| Command | Purpose | Prerequisites | Error Recovery |
|---------|---------|---------------|----------------|
| `make setup_dev` | Install all dev dependencies | Makefile exists, uv installed | Try `uv sync --dev` directly |
| `make setup_dev_claude` | Setup with Claude Code CLI | Above + Claude Code available | Manual setup per Claude docs |
| `make setup_dev_ollama` | Setup with Ollama local LLM | Above + Ollama installed | Check Ollama installation |
| `make run_cli` | Run CLI application | Dev environment setup | Try `uv run python src/app/main.py` |
| `make run_cli ARGS="--help"` | Run CLI with arguments | Above | Try `uv run python src/app/main.py --help` |
| `make run_gui` | Run Streamlit GUI | Above + Streamlit installed | Try `uv run streamlit run src/run_gui.py` |
| `make ruff` | Format code and fix linting | Ruff installed | Try `uv run ruff format . && uv run ruff check . --fix` |
| `make type_check` | Run pyright static type checking | pyright installed | Try `uv run pyright` |
| `make test_all` | Run all tests with pytest | Pytest installed | Try `uv run pytest` |
| `make coverage_all` | Run tests with coverage report | Above + coverage installed | Try `uv run coverage run -m pytest \|\| true && uv run coverage report -m` |
| `make validate` | Complete pre-commit validation | Above dependencies | Run individual commands manually |
| `make quick_validate` | Fast development validation | Ruff and pyright installed | Run `make ruff && make type_check` |
| `uv run pytest <path>` | Run specific test file/function | Pytest available | Check test file exists and syntax |

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

- [ ] The `agent_system.py` module has a `NotImplementedError` for streaming with Pydantic model outputs. Please clarify the intended approach for streaming structured data.
  - Human: `# TODO` but not of priority as of now. Remind me once a week.
- [ ] The `llm_model_funs.py` module has `NotImplementedError` for the Gemini and HuggingFace providers. Please provide the correct implementation or remove them if they are not supported.
  - Human: `# TODO` but not of priority as of now. Remind me once a week.
- [ ] The `agent_system.py` module contains a `FIXME` note regarding the use of a try-catch context manager. Please review and implement the intended error handling.
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
### Learned Pattern: Async Error Handling in Agents

- **Date**: 2025-07-20T14:30:00Z
- **Context**: PydanticAI agent processing with timeouts
- **Problem**: Agents hanging on long requests without proper timeout handling
- **Solution**: Use asyncio.wait_for with context manager for cleanup
- **Example**: See context/examples/async-timeout-pattern.py
- **Validation**: Test with deliberately slow mock responses
- **References**: src/app/agents/agent_system.py:142
```

### Active Learning Entries

Agents should add new patterns discovered during development here.

## Agent Quick Reference - Critical Reminders

**Before ANY task, verify:**

- All `$VARIABLE` paths resolve via `$DEFAULT_PATHS_MD`
- Libraries exist in `$PROJECT_REQUIREMENTS`
- No missing context assumptions

**Documentation tasks:**

- Apply [markdownlint rules](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)
- Use ISO 8601 timestamps (`YYYY-mm-DDTHH:MM:SSZ`)
- Consistent `$VARIABLE` syntax

**Code tasks:**

- Max 500 lines/file
- Create tests in `$TEST_PATH`
- Google-style docstrings
- Verify imports exist

**Always finish with:**

- Follow [pre-commit checklist](#standard-workflow-commands)
- Update AGENTS.md if learned something new

**🛑 STOP if blocked:** Add to "Requests to Humans" rather than assume or proceed with incomplete info
