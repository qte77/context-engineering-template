# Agent instructions for `Agents-eval` repository

As proposed by [agentsmd.net](https://agentsmd.net/) and used by [wandb weave AGENTS.md](https://github.com/wandb/weave/blob/master/AGENTS.md).

## Core Rules & AI Behavior

* When you learn something new about the codebase or introduce a new concept, **update this file (`AGENTS.md`)** to reflect the new knowledge. This is YOUR FILE! It should grow and evolve with you.
* If something doesn't make sense architecturally, from a developer experience standpoint, or product-wise, please add it to the **`Requests to Humans`** section below.
* Always follow the established coding patterns, conventions, and architectural decisions documented here and in the `docs/` directory.
* **Never assume missing context.** Ask questions if you are uncertain about requirements or implementation details.
* **Never hallucinate libraries or functions.** Only use known, verified Python packages listed in `pyproject.toml`.
* **Always confirm file paths and module names** exist before referencing them in code or tests.
* **Never delete or overwrite existing code** unless explicitly instructed to or as part of a documented refactoring task.

## Architecture Overview

This is a multi-agent evaluation system for assessing agentic AI systems. The project uses **PydanticAI** as the core framework for agent orchestration and is designed for evaluation purposes, not for production agent deployment.

### Data Flow

1. User input → Manager Agent
2. Manager delegates to Researcher Agent (with DuckDuckGo search)
3. Researcher results → Analyst Agent for validation
4. Validated data → Synthesizer Agent for report generation
5. Results evaluated using configurable metrics

### Key Dependencies

* **PydanticAI**: Agent framework and orchestration
* **uv**: Fast Python dependency management
* **Streamlit**: GUI framework
* **Ruff**: Code formatting and linting
* **MyPy**: Static type checking

## Codebase Structure & Modularity

### Main Components

* `src/app/`: The core application logic. This is where most of your work will be.
  * `main.py`: The main entry point for the CLI application.
  * `agents/agent_system.py`: Defines the multi-agent system, their interactions, and orchestration. **This is the central logic for agent behavior.**
  * `config/data_models.py`: Contains all **Pydantic** models that define the data contracts. This is a critical file for understanding data flow.
  * `config/config_chat.json`: Holds provider settings and system prompts for agents.
  * `config/config_eval.json`: Defines evaluation metrics and their weights.
  * `evals/metrics.py`: Implements the evaluation metrics.
* `src/gui/`: Contains the source code for the Streamlit GUI.
* `docs/`: Contains project documentation, including the Product Requirements Document (`PRD.md`) and the C4 architecture model.
* `tests/`: Contains all tests for the project, written using **pytest**.

### Code Organization Rules

* **Never create a file longer than 500 lines of code.** If a file approaches this limit, refactor by splitting it into smaller, more focused modules or helper files.
* Organize code into clearly separated modules grouped by feature.
* Use clear, consistent, and absolute imports within packages.

## Development Commands & Environment

### Environment Setup

The project requirements are stated in `pyproject.toml`. Your development environment should be set up automatically using the provided `Makefile`, which configures the virtual environment.

* `make setup_dev`: Install all dev dependencies.
* `make setup_dev_claude`: Setup dev environment with Claude Code CLI.
* `make setup_dev_ollama`: Setup dev environment with Ollama local LLM.

### Running the Application

* `make run_cli`: Run the CLI application.
* `make run_cli ARGS="--help"`: Run CLI with specific arguments.
* `make run_gui`: Run the Streamlit GUI.

### Testing and Code Quality

* `make test_all`: Run all tests with pytest.
* `make coverage_all`: Run tests and generate a coverage report.
* `make ruff`: Format code and fix linting issues with Ruff.
* `make type_check`: Run mypy static type checking on `src/app/`.

## Testing & Reliability

* **Always create Pytest unit tests** for new features (functions, classes, etc.).
* Tests must live in the `tests/` folder, mirroring the `src/app` structure.
* After updating any logic, check whether existing unit tests need to be updated. If so, do it.
* For each new feature, include at least:
  * 1 test for the expected use case (happy path).
  * 1 test for a known edge case.
  * 1 test for an expected failure case (e.g., invalid input).
* **To run a specific test file or function, use `uv run pytest` directly:**
  * `uv run pytest tests/test_specific_file.py`
  * `uv run pytest tests/test_specific_file.py::test_function`

## Style, Patterns & Documentation

### Coding Style

* **Use Pydantic** models in `src/app/config/data_models.py` for all data validation and data contracts. **Always use or update these models** when modifying data flows.
* Use the predefined error message functions from `src/app/utils/error_messages.py` for consistency.
* When writing complex logic, **add an inline `# Reason:` comment** explaining the *why*, not just the *what*.
* Comment non-obvious code to ensure it is understandable to a mid-level developer.

### Documentation

* Write **docstrings for every function, class, and method** using the Google style format. This is critical as the documentation site is built automatically from docstrings.

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

* Update this `AGENTS.md` file when introducing new patterns or concepts.
* Document significant architectural decisions in `docs/ADR.md`.
* Document all significant changes, features, and bug fixes in `docs/CHANGELOG.md`.

## Code Review & PR Guidelines

### PR Requirements

* **Title Format**: Commit messages and PR titles must follow the **Conventional Commits** specification, as outlined in the `.gitmessage` template.
* Provide detailed PR summaries including the purpose of the changes and the testing performed.

### Pre-commit Checklist

1. Run the linter and formatter: `make ruff`.
2. Ensure all tests pass: `make test_all`.
3. Ensure static type checks pass: `make type_check`.
4. Update documentation as described below.

## Requests to Humans

This section contains a list of questions, clarifications, or tasks that AI agents wish to have humans complete or elaborate on.

* [ ] The `agent_system.py` module has a `NotImplementedError` for streaming with Pydantic model outputs. Please clarify the intended approach for streaming structured data.
* [ ] The `llm_model_funs.py` module has `NotImplementedError` for the Gemini and HuggingFace providers. Please provide the correct implementation or remove them if they are not supported.
* [ ] The `agent_system.py` module contains a `FIXME` note regarding the use of a try-catch context manager. Please review and implement the intended error handling.
* [ ] Add TypeScript testing guidelines (if a TypeScript frontend is planned for the future).
