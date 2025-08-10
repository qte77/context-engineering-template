# This Makefile automates the build, test, and clean processes for the project.
# It provides a convenient way to run common tasks using the 'make' command.
# Run `make help` to see all available recipes.

.SILENT:
.ONESHELL:
.PHONY: all setup_dev setup_prod setup_uv setup_claude_code frp_gen_claude frp_exe_claude ruff test_all check_types coverage_all output_unset_app_env_sh run_example_gui run_example_server run_example_client run_example_full help
.DEFAULT_GOAL := help


ENV_FILE := .env
SRC_PATH := src
APP_PATH := $(SRC_PATH)
EXAMPLES_PATH := examples/mcp-server-client
FEAT_DEF_PATH := /context/features
FRP_DEF_PATH := /context/FRPs
FRP_CLAUDE_GEN_CMD := generate-frp
FRP_CLAUDE_EXE_CMD := execute-frp


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
		start)
			dest_cmd=$(FRP_CLAUDE_GEN_CMD)
			dest_path=$(FEAT_DEF_PATH);;
  		stop)
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
	# TODO uncomment if python is needed
	# echo $(python --version)
	# $(MAKE) -s setup_uv
	# uv sync --all-groups
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


output_unset_env_sh:  ## Unset app environment variables
	uf="./unset_env.sh"
	echo "Outputing '$${uf}' ..."
	printenv | awk -F= '/_API_KEY=/ {print "unset " $$1}' > $$uf


# MARK: context engineering


frp_gen_claude:  ## generates the FRP from the file passed in "ARGS=file"
	$(call CLAUDE_FRP_RUNNER, $(ARGS), "generate")


frp_exe_claude:  ## executes the FRP from the file passed in "ARGS=file"
	$(call CLAUDE_FRP_RUNNER, $(ARGS), "execute")


# MARK: code quality


ruff:  ## Lint: Format and check with ruff
	uv run ruff format
	uv run ruff check --fix


test_all:  ## Run all tests
	uv run pytest


coverage_all:  ## Get test coverage
	uv run coverage run -m pytest || true
	uv run coverage report -m


check_types:  ## Check for static typing errors
	uv run mypy $(APP_PATH)


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
