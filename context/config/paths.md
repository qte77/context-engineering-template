# Default paths

Note: Update this file according to project needs.

## App

- `APP_PATH = src`: The core application logic. This is where most of your work will be.
- `TEST_PATH = tests/`: Contains all tests for the project.

### Important files

- `${APP_PATH}/main.py`: The main entry point for the CLI application.

## Context

- `CONTEXT_PATH = context`: Contains auxiliary context for coding agents.
- `CTX_CONFIG_PATH = ${CONTEXT_PATH}/config`
- `CTX_EXAMPLES_PATH = ${CONTEXT_PATH}/examples`
- `CTX_FEATURES_PATH = ${CONTEXT_PATH}/features`
- `CTX_LOGS_PATH = ${CONTEXT_PATH}/logs`
- `CTX_BUSINESS_INPUTS_PATH = ${CONTEXT_PATH}/business_inputs`: Contains initial business input documents for BRD generation.
- `CTX_BRD_PATH = ${CONTEXT_PATH}/BRDs`: Contains the business requirements definition files.
- `CTX_PRD_PATH = ${CONTEXT_PATH}/PRDs`: Contains the product requirements document files.
- `CTX_FRP_PATH = ${CONTEXT_PATH}/FRPs`: Contains the generated feature requirements prompt files.
- `CTX_TEMPLATES_PATH = ${CONTEXT_PATH}/templates`

## Project

- `DOCS_PATH = docs`: Contains auxiliary files for project documentation, like the Product Requirements Document (`PRD.md`) and architecture model visualizations.

### Important files

- `CTX_BUSINESS_INPUT_TEMPLATE = ${CTX_TEMPLATES_PATH}/business_input_base.md`: Template for initial business information input.
- `CTX_BRD_TEMPLATE = ${CTX_TEMPLATES_PATH}/brd_base.md`: Template for creating business requirements definitions.
- `CTX_PRD_TEMPLATE = ${CTX_TEMPLATES_PATH}/prd_base.md`: Template for creating product requirements documents.
- `CTX_FRP_TEMPLATE = ${CTX_TEMPLATES_PATH}/frp_base.md`: Template for creating feature requirements prompts.
- `CHANGELOG_PATH = CHANGELOG.md`: Contains the most important changes made in each version of the project.
- `LLMSTXT_PATH = ${DOCS_PATH}/llms.txt`: Contains the flattened project, i.e., the structure and content of the project in one text file to be ingested by LLMs. Might not reflect the current project state depending on update strategy.
- `PRD_PATH = ${DOCS_PATH}/PRD.md`: Contains the product requirements definitions for this project.
- `PROJECT_REQUIREMENTS = pyproject.toml`: Defines meta data like package name, dependencies and tool settings.
