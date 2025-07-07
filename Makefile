# This Makefile automates the build, test, and clean processes for the project.
# It provides a convenient way to run common tasks using the 'make' command.
# Run `make help` to see all available recipes.

.SILENT:
.ONESHELL:
.PHONY: all setup_python_claude setup_dev setup_prod setup_claude_code prp_gen_claude prp_exe_claude ruff test_all check_types coverage_all output_unset_app_env_sh help
.DEFAULT_GOAL := help


ENV_FILE := .env
SRC_PATH := src
APP_PATH := $(SRC_PATH)
FEAT_DEF_PATH := /context/features
PRP_DEF_PATH := /context/PRPs
PRP_CLAUDE_GEN_CMD := generate-prp
PRP_CLAUDE_EXE_CMD := execute-prp


# construct the full paths and execute Claude Code commands
# TODO switch folder by function called ()
# TODO Claude Code non-interactive headless mode tee to CLI
define CLAUDE_PRP_RUNNER
	echo "Starting Claude Code PRP runner ..."
	dest_file=$(firstword $(strip $(1)))
	dest_cmd=$(firstword $(strip $(2)))
	if [ -z "$${dest_file}" ]; then
		echo "Error: ARGS for PRP filename is empty. Please provide a PRP filename."
		exit 1
	fi
	case "$${dest_cmd}" in
		start)
			dest_cmd=$(PRP_CLAUDE_GEN_CMD)
			dest_path=$(FEAT_DEF_PATH);;
  		stop)
			dest_cmd=$(PRP_CLAUDE_EXE_CMD)
			dest_path=$(PRP_DEF_PATH);;
		*)
    		echo "Unknown command: $${dest_cmd}. Exiting ..."
    		exit 1;;
	esac
	dest_cmd="/project:$${dest_cmd} $${dest_path}/$${dest_file}"
	echo "Executing command '$${dest_cmd}' ..."
	claude -p "$${dest_cmd}" 2>&1
	claude -p "/cost" 2>&1
endef


setup_python_claude:  # Set up environment and install Claude Code CLI
	$(MAKE) -s setup_dev
	$(MAKE) -s export_env_file
	$(MAKE) -s setup_claude_code


setup_dev:  ## Install uv and deps, Download and start Ollama 
	echo "Setting up dev environment ..."
	pip install uv -q
	uv sync --all-groups


setup_prod:  ## Install uv and deps, Download and start Ollama 
	echo "Setting up prod environment ..."
	pip install uv -q
	uv sync --frozen


setup_claude_code:  ## Setup Claude Code CLI, node.js and npm have to be present
	echo "Setting up claude code ..."
	npm install -g @anthropic-ai/claude-code
	claude config set --global preferredNotifChannel terminal_bell
	echo "npm version: $$(npm --version)"
	claude --version


prp_gen_claude:  ## generates the PRP from the file passed in "ARGS=file"
	$(call CLAUDE_PRP_RUNNER, $(ARGS), "generate")


prp_exe_claude:  ## executes the PRP from the file passed in "ARGS=file"
	$(call CLAUDE_PRP_RUNNER, $(ARGS), "execute")


export_env_file:  # Read ENV_FILE and export k=v to env
	while IFS='=' read -r key value || [ -n "$${key}" ]; do
		case "$${key}" in
			''|\#*) continue ;;
		esac
		value=$$(echo "$${value}" | sed -e 's/^"//' -e 's/"$$//')
		export "$${key}=$${value}"
	done < .env


output_unset_env_sh:  ## Unset app environment variables
	uf="./unset_env.sh"
	echo "Outputing '$${uf}' ..."
	printenv | awk -F= '/_API_KEY=/ {print "unset " $$1}' > $$uf


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
