# This Makefile automates the build, test, and clean processes for the project.
# It provides a convenient way to run common tasks using the 'make' command.
# Run `make help` to see all available recipes.

.SILENT:
.ONESHELL:
.PHONY: all setup_dev setup_prod setup_uv setup_claude_code setup_plantuml brd_gen_claude prd_gen_claude frp_gen_claude frp_exe_claude frp_gen_legacy_claude frp_exe_legacy_claude run_puml_interactive run_puml_single ruff test_all test_hypothesis_verbose test_hypothesis_quick test_hypothesis_thorough test_single test_debug check_types coverage_all output_unset_app_env_sh run_example_gui run_example_server run_example_client run_example_full help
.DEFAULT_GOAL := help


ENV_FILE := .env
SRC_PATH := src
APP_PATH := $(SRC_PATH)
EXAMPLES_PATH := examples/mcp-server-client
PLANTUML_CONTAINER := plantuml/plantuml:latest
PLANTUML_SCRIPT := scripts/generate-plantuml-png.sh

# Context engineering paths
BRD_DEF_PATH := context/BRDs
PRD_DEF_PATH := context/PRDs
FEAT_DEF_PATH := context/features
FRP_DEF_PATH := context/FRPs

# Claude commands
BRD_CLAUDE_GEN_CMD := generate-brd
PRD_CLAUDE_GEN_CMD := generate-prd-from-brd
FRP_CLAUDE_GEN_CMD := generate-frp-from-prd
FRP_CLAUDE_EXE_CMD := execute-frp
FRP_CLAUDE_LEGACY_GEN_CMD := generate-frp


# MARK: claude commands


# construct the full paths and execute Claude Code commands
# TODO switch folder by function called ()
# TODO Claude Code non-interactive headless mode tee to CLI
define CLAUDE_FRP_RUNNER
	echo "Starting Claude Code FRP runner ..."
	dest_file=$(firstword $(strip $(1)))
	dest_cmd=$(firstword $(strip $(2)))
	if [ -z "$${dest_file}" ]; then
		echo "Error: ARGS for FRP filename is empty. Please provide a FRP filename."
		exit 1
	fi
	case "$${dest_cmd}" in
		generate)
			dest_cmd=$(FRP_CLAUDE_LEGACY_GEN_CMD)
			dest_path=$(FEAT_DEF_PATH);;
  		execute)
			dest_cmd=$(FRP_CLAUDE_EXE_CMD)
			dest_path=$(FRP_DEF_PATH);;
		*)
    		echo "Unknown command: $${dest_cmd}. Exiting ..."
    		exit 1;;
	esac
	dest_cmd="/project:$${dest_cmd} $${dest_path}/$${dest_file}"
	echo "Executing command '$${dest_cmd}' ..."
	claude -p "$${dest_cmd}" 2>&1
	claude -p "/cost" 2>&1
endef


# MARK: setup


setup_dev:  ## Install dependencies, Download and start Ollama 
	echo "Setting up dev environment ..."
	echo $(python --version)
	$(MAKE) -s setup_uv
	uv sync --all-groups
	echo "npm version: $$(npm --version)"
	$(MAKE) -s setup_claude_code
	$(MAKE) -s setup_gemini_cli


setup_prod:  ## Install dependencies, Download and start Ollama 
	echo "Setting up prod environment ..."
	$(MAKE) -s setup_uv
	uv sync --frozen


setup_uv:  ## Install uv
	echo "Installing uv ..."
	pip install uv -q
	echo $(uv --version)


setup_claude_code:  ## Setup Claude Code CLI, node.js and npm have to be present
	echo "Setting up Claude Code CLI ..."
	npm install -gs @anthropic-ai/claude-code
	echo "Claude Code CLI version: $$(claude --version)"

setup_gemini_cli:  ## Setup Gemini CLI, node.js and npm have to be present
	echo "Setting up Gemini CLI ..."
	npm install -gs @google/gemini-cli
	echo "Gemini CLI version: $$(gemini --version)"


setup_plantuml:  ## Setup PlantUML with docker, $(PLANTUML_SCRIPT) and $(PLANTUML_CONTAINER)
	echo "Setting up PlantUML docker ..."
	chmod +x $(PLANTUML_SCRIPT)
	docker pull $(PLANTUML_CONTAINER)
	echo "PlantUML docker version: $$(docker run --rm $(PLANTUML_CONTAINER) --version)"


output_unset_env_sh:  ## Unset app environment variables
	uf="./unset_env.sh"
	echo "Outputing '$${uf}' ..."
	printenv | awk -F= '/_API_KEY=/ {print "unset " $$1}' > $$uf


# MARK: context engineering

# Business-driven workflow (new)
brd_gen_claude:  ## Generate BRD from business input "ARGS=project_name.md"
	echo "Starting BRD generation ..."
	dest_file=$(firstword $(strip $(ARGS)))
	if [ -z "$${dest_file}" ]; then
		echo "Error: ARGS for project filename is empty. Please provide a project filename."
		exit 1
	fi
	echo "Executing BRD generation for $${dest_file} ..."
	claude -p "/project:$(BRD_CLAUDE_GEN_CMD) $${dest_file}" 2>&1
	claude -p "/cost" 2>&1

prd_gen_claude:  ## Generate PRD from BRD "ARGS=project_name.md"
	echo "Starting PRD generation ..."
	dest_file=$(firstword $(strip $(ARGS)))
	if [ -z "$${dest_file}" ]; then
		echo "Error: ARGS for project filename is empty. Please provide a project filename."
		exit 1
	fi
	echo "Executing PRD generation for $${dest_file} ..."
	claude -p "/project:$(PRD_CLAUDE_GEN_CMD) $${dest_file}" 2>&1
	claude -p "/cost" 2>&1

frp_gen_claude:  ## Generate feature FRP from PRD "ARGS=project_name.md feature_name"
	echo "Starting FRP generation ..."
	project_file=$(firstword $(strip $(ARGS)))
	feature_name=$(word 2, $(strip $(ARGS)))
	if [ -z "$${project_file}" ] || [ -z "$${feature_name}" ]; then
		echo "Error: Need both project filename and feature name. Usage: ARGS=\"project.md feature_name\""
		exit 1
	fi
	echo "Executing FRP generation for project $${project_file}, feature $${feature_name} ..."
	claude -p "/project:$(FRP_CLAUDE_GEN_CMD) $${project_file} $${feature_name}" 2>&1
	claude -p "/cost" 2>&1

frp_exe_claude:  ## Execute FRP implementation "ARGS=project_feature.md"
	echo "Starting FRP execution ..."
	dest_file=$(firstword $(strip $(ARGS)))
	if [ -z "$${dest_file}" ]; then
		echo "Error: ARGS for FRP filename is empty. Please provide a FRP filename."
		exit 1
	fi
	echo "Executing FRP implementation for $${dest_file} ..."
	claude -p "/project:$(FRP_CLAUDE_EXE_CMD) $${dest_file}" 2>&1
	claude -p "/cost" 2>&1

# Legacy workflow (backward compatibility)
frp_gen_legacy_claude:  ## generates the legacy FRP from feature file "ARGS=feature.md"
	$(call CLAUDE_FRP_RUNNER, $(ARGS), "generate")

frp_exe_legacy_claude:  ## executes the legacy FRP "ARGS=feature.md"
	$(call CLAUDE_FRP_RUNNER, $(ARGS), "execute")


# MARK: run plantuml


run_puml_interactive:  ## Generate a themed diagram from a PlantUML file interactively.
	# https://github.com/plantuml/plantuml-server
	# plantuml/plantuml-server:tomcat
	docker run -d -p 8080:8080 "$(PLANTUML_CONTAINER)"

run_puml_single:  ## Generate a themed diagram from a PlantUML file.
	$(PLANTUML_SCRIPT) "$(INPUT_FILE)" "$(STYLE)" "$(OUTPUT_PATH)" \
		"$(CHECK_ONLY)" "$(PLANTUML_CONTAINER)"


# MARK: code sanity


ruff:  ## Lint: Format and check with ruff
	uv run ruff format
	uv run ruff check --fix


check_types:  ## Check for static typing errors
	uv run pyright $(APP_PATH)


# MARK: tests


test_all:  ## Run all hypothesis property-based tests
	for test_file in tests/test_*.py; do \
		echo "Running $$test_file..."; \
		uv run python "$$test_file" || exit 1; \
	done


test_hypothesis_verbose:  ## Run hypothesis tests with verbose output
	for test_file in tests/test_*.py; do \
		echo "Running $$test_file with verbose output..."; \
		HYPOTHESIS_VERBOSITY=verbose uv run python "$$test_file" || exit 1; \
	done


test_hypothesis_quick:  ## Run hypothesis tests with fewer examples (quick)
	for test_file in tests/test_*.py; do \
		echo "Running $$test_file (quick mode)..."; \
		HYPOTHESIS_MAX_EXAMPLES=10 uv run python "$$test_file" || exit 1; \
	done


test_hypothesis_thorough:  ## Run hypothesis tests with many examples (thorough)
	for test_file in tests/test_*.py; do \
		echo "Running $$test_file (thorough mode)..."; \
		HYPOTHESIS_MAX_EXAMPLES=1000 uv run python "$$test_file" || exit 1; \
	done


test_single:  ## Run a single hypothesis test file (usage: make test_single FILE=test_example.py)
	@if [ -z "$(FILE)" ]; then \
		echo "Error: FILE parameter is required. Usage: make test_single FILE=test_example.py"; \
		exit 1; \
	fi
	echo "Running tests/$(FILE)..."
	uv run python "tests/$(FILE)"


test_debug:  ## Run hypothesis tests with debug statistics
	for test_file in tests/test_*.py; do \
		echo "Running $$test_file with debug info..."; \
		HYPOTHESIS_VERBOSITY=debug uv run python "$$test_file" || exit 1; \
	done


coverage_all:  ## Get test coverage with hypothesis tests
	uv run coverage erase
	for test_file in tests/test_*.py; do \
		echo "Running $$test_file with coverage..."; \
		uv run coverage run -a "$$test_file" || true; \
	done
	uv run coverage report -m


# MARK: run


run_example_gui:  ## Launch MCP server-client example GUI
	$(MAKE) -C $(EXAMPLES_PATH) run_gui


run_example_server:  ## Run MCP server-client example server
	$(MAKE) -C $(EXAMPLES_PATH) run_server


run_example_client:  ## Run MCP server-client example client
	$(MAKE) -C $(EXAMPLES_PATH) run_client ARGS="$(ARGS)"


run_example_full: ## Run MCP server-client example with Docker Compose
	$(MAKE) -C $(EXAMPLES_PATH) run_full ARGS="$(ARGS)"


# MARK: help


# TODO add stackoverflow source
help:  ## Displays this message with available recipes
	echo "Usage: make [recipe]"
	echo "Recipes:"
	awk '/^[a-zA-Z0-9_-]+:.*?##/ {
		helpMessage = match($$0, /## (.*)/)
		if (helpMessage) {
			recipe = $$1
			sub(/:/, "", recipe)
			printf "  \033[36m%-20s\033[0m %s\n", recipe, substr($$0, RSTART + 3, RLENGTH)
		}
	}' $(MAKEFILE_LIST)
