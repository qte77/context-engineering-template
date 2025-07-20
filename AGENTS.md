# Agent instructions for `Agents-eval` repository

As proposed by [agentsmd.net](https://agentsmd.net/) and used by [wandb weave AGENTS.md](https://github.com/wandb/weave/blob/master/AGENTS.md).

## Core Rules & AI Behavior

* Use the paths and structure defined in `DEFAULT_PATHS = context/config/paths.md`.
* Adhere to an Behavior Driven Development (BDD) approach which focuses on generating concise goal-oriented Minimum Viable Products (MVPs) with minimal yet functional features sets.
  * Keep it simple!
  * The outlined behavior should be described by defining tests first and implementing corresponding code afterwards.
  * Then iteratively improve tests and code until the feature requirements are met.
  * The iterations should be as concise as possible to keep complexity low
  * All code quality and tests have to be passed to davance to the next step
* Always follow the established coding patterns, conventions, and architectural decisions documented here and in the `$DOCS_PATH` directory.
* **Never assume missing context.** Ask questions if you are uncertain about requirements or implementation details.
* **Never hallucinate libraries or functions.** Only use known, verified Python packages listed in `$PROJECT_REQUIREMENTS`.
* **Always confirm file paths and module names** exist before referencing them in code or tests.
* **Never delete or overwrite existing code** unless explicitly instructed to or as part of a documented refactoring task.
* If something doesn't make sense architecturally, from a developer experience standpoint, or product-wise, please add it to the **`Requests to Humans`** section below.
* When you learn something new about the codebase or introduce a new concept, **update this file (`AGENTS.md`)** to reflect the new knowledge. This is YOUR FILE! It should grow and evolve with you.

## Architecture Overview

This is a multi-agent evaluation system for assessing agentic AI systems. The project uses **PydanticAI** as the core framework for agent orchestration and is designed for evaluation purposes, not for production agent deployment.

### Data Flow

1. User input → Manager Agent (can be single-LLM)
2. Optional: Manager delegates to Researcher Agent (with DuckDuckGo search)
3. Optional: Researcher results → Analyst Agent for validation
4. Optional: Validated data → Synthesizer Agent for report generation
5. Results evaluated using configurable metrics

### Key Dependencies

* **PydanticAI**: Agent framework and orchestration
* **uv**: Fast Python dependency management
* **Streamlit**: GUI framework
* **Ruff**: Code formatting and linting
* **MyPy**: Static type checking

## Codebase Structure & Modularity

### Main Components

See `$DEFAULT_PATHS`.

### Code Organization Rules

* **Never create a file longer than 500 lines of code.** If a file approaches this limit, refactor by splitting it into smaller, more focused modules or helper files.
* Organize code into clearly separated modules grouped by feature.
* Use clear, consistent, and absolute imports within packages.

## Development Commands & Environment

### Environment Setup

The project requirements are stated in `$PROJECT_REQUIREMENTS`. Your development environment should be set up automatically using the provided `Makefile`, which configures the virtual environment.

* `make setup_dev`: Install all dev dependencies.
* `make setup_dev_claude`: Setup dev environment with Claude Code CLI.
* `make setup_dev_ollama`: Setup dev environment with Ollama local LLM.

### Running the Application

* `make run_cli`: Run the CLI application.
* `make run_cli ARGS="--help"`: Run CLI with specific arguments.
* `make run_gui`: Run the Streamlit GUI.

### Code Quality

Testing is managed by **ruff** and **mypy** and orchestrated via the `Makefile`.

* `make ruff`: Format code and fix linting issues with Ruff.
* `make type_check`: Run mypy static type checking on `$APP_PATH`.

### Testing & Reliability

* **Always create Pytest unit tests** for new features (functions, classes, etc.).
* Tests must live in the `$TEST_PATH` folder, mirroring the `$APP_PATH` structure.
* **To run all tests** use one of the following commands:
  * `make test_all`: Run all tests with pytest.
  * `make coverage_all`: Run tests and generate a coverage report.
* **To run a specific test file or function, use `uv run pytest` directly:**
  * `uv run pytest specific_test_path/test_specific_file.py`
  * `uv run pytest specific_test_path/test_specific_file.py::test_function`

## Style, Patterns & Documentation

### Coding Style

* **Use Pydantic** models in `$DATAMODELS_PATH` for all data validation and data contracts. **Always use or update these models** when modifying data flows.
* Use the predefined error message functions for consistency. Update or create new if necessary.
* When writing complex logic, **add an inline `# Reason:` comment** explaining the *why*, not just the *what*.
* Comment non-obvious code to ensure it is understandable to a mid-level developer.

### Documentation

* Write **docstrings for every file, function, class, and method** using the Google style format. This is critical as the documentation site is built automatically from docstrings.

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

* Provide an example usage in regards to the whole project. How would your code be integrated, what entrypoints to use
* Update this `AGENTS.md` file when introducing new patterns or concepts.
* Document significant architectural decisions in `${ADR_PATH}`.
* Document all significant changes, features, and bug fixes in `${CHANGELOG_PATH}`.

## Code Review & PR Guidelines

### Commit and PR Requirements

* **Title Format**: Commit messages and PR titles must follow the **Conventional Commits** specification, as outlined in the `.gitmessage` template.
* Provide detailed PR summaries including the purpose of the changes and the testing performed.

### Pre-commit Checklist

1. Run the linter and formatter: `make ruff`.
2. Ensure static type checks pass: `make type_check`.
3. Run unit tests for the new components until they all pass.
4. Ensure integration, meaning all tests pass: `make test_all`.
5. Update documentation as described above.

## Timestamping for CLI Operations

* **Always use ISO 8601 timestamps** when creating logs or tracking CLI operations
* **File naming format**: `YYYY-mm-DDTHH-MM-SSZ` (hyphens for filesystem compatibility)
* **Content format**: `YYYY-mm-DDTHH:MM:SSZ` (standard ISO 8601)
* **Implementation**: Use `date -u "+FORMAT"` commands for accurate UTC timestamps

### Timestamp Commands

* Filename timestamp: `date -u "+%Y-%m-%dT%H-%M-%SZ"`
* Content timestamp: `date -u "+%Y-%m-%dT%H:%M:%SZ"`
* Log entry format: `[TIMESTAMP] Action description`

## Auxiliary

* Use [markdownlint's Rules.md](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md) to output weel-defined markdown

## Requests to Humans

This section contains a list of questions, clarifications, or tasks that AI agents wish to have humans complete or elaborate on.

* [ ] The `agent_system.py` module has a `NotImplementedError` for streaming with Pydantic model outputs. Please clarify the intended approach for streaming structured data.
* [ ] The `llm_model_funs.py` module has `NotImplementedError` for the Gemini and HuggingFace providers. Please provide the correct implementation or remove them if they are not supported.
* [ ] The `agent_system.py` module contains a `FIXME` note regarding the use of a try-catch context manager. Please review and implement the intended error handling.
* [ ] Add TypeScript testing guidelines (if a TypeScript frontend is planned for the future).
