# MCP Server-Client Example Makefile
# This Makefile provides commands for the MCP server-client example

.SILENT:
.ONESHELL:
.PHONY: setup_dev setup_prod ruff test_all check_types coverage_all run_gui run_server run_client help
.DEFAULT_GOAL := help

SRC_PATH := src
APP_PATH := $(SRC_PATH)

# MARK: setup

setup_dev:  ## Install uv and development dependencies
	echo "Setting up dev environment ..."
	pip install uv -q
	uv sync --all-groups

setup_prod:  ## Install uv and production dependencies
	echo "Setting up prod environment ..."
	pip install uv -q
	uv sync --frozen

# MARK: code quality

ruff:  ## Format and lint code with ruff
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

run_gui:  ## Launch Streamlit GUI
	uv run python -m src.main gui

run_server:  ## Run MCP server
	uv run python -m src.main server

run_client:  ## Run MCP client (requires ARGS)
	uv run python -m src.main client $(ARGS)

# MARK: help

help:  ## Display available commands
	echo "Usage: make [command]"
	echo "Commands:"
	awk '/^[a-zA-Z0-9_-]+:.*?##/ {
		helpMessage = match($$0, /## (.*)/)
		if (helpMessage) {
			recipe = $$1
			sub(/:/, "", recipe)
			printf "  \033[36m%-20s\033[0m %s\n", recipe, substr($$0, RSTART + 3, RLENGTH)
		}
	}' $(MAKEFILE_LIST)