# MCP Server-Client Demo

A demonstration of Model Control Protocol (MCP) server-client infrastructure built with Claude Code CLI.

## Quick Start

```bash
# Setup development environment
make setup_dev

# Run GUI interface
make run_gui

# Run server only
make run_server

# Run with Docker Compose
make run_full
```

## Components

- **MCP Server**: Provides tools for date/time, weather, and dice rolling
- **MCP Client**: CLI interface for interacting with server
- **Streamlit GUI**: Web interface for server interaction

## Docker Usage

```bash
# Run all services
docker compose up --build

# Access GUI at http://localhost:8501
# Server runs on port 8000
```
