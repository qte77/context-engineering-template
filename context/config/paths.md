# Default paths

Note: Update this file according to project needs.

## App

- `APP_PATH = src`: The core application logic. This is where most of your work will be.
- `TEST_PATH = tests/`: Contains all tests for the project.

### Important files

- `${APP_PATH}/main.py`: The main entry point for the CLI application.

## Context

- `AGENTSMD_PATH`: Contains the main context for cading agents.
- `CONTEXT_PATH = context`: Contains auxiliary context for coding agents.
- `CTX_CONFIG_PATH = ${CONTEXT_PATH}/config`
- `CTX_EXAMPLES_PATH = ${CONTEXT_PATH}/examples`
- `CTX_FEATURES_PATH = ${CONTEXT_PATH}/features`
- `CTX_LOGS_PATH = ${CONTEXT_PATH}/logs`
- `CTX_FRP_PATH = ${CONTEXT_PATH}/FRPs`: Contains the generated feature requirements prompt files.
- `CTX_TEMPLATES_PATH = ${CONTEXT_PATH}/templates`

## Project

- `DOCS_PATH = docs`: Contains auxiliary files for project documentation, like the Product Requirements Document (`PRD.md`) and architecture model visualizations.

### Important files

- `CHANGELOG_PATH = CHANGELOG.md`: Contains the most important changes made in each version of the project.
- `LLMSTXT_PATH = ${DOCS_PATH}/llms.txt`: Contains the flattened project, i.e., the structure and content of the project in one text file to be ingested by LLMs. Might not reflect the current project state depending on update strategy.
- `PRD_PATH = ${DOCS_PATH}/PRD.md`: Contains the product requirements definitions for this project.
- `PROJECT_REQUIREMENTS = pyproject.toml`: Defines meta data like package name, dependencies and tool settings.
