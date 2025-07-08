# Context Engineering Template

This project aims to implement a template for context engineering with coding agents. As suggested by several resources, including [context-engineering-intro](https://github.com/coleam00/context-engineering-intro), [The rise of "context engineering"](https://blog.langchain.com/the-rise-of-context-engineering/), [Context Engineering](https://blog.langchain.com/context-engineering-for-agents/) and somewhat [He Built 40 Startups Using Just Prompts — Here’s His System](https://youtu.be/CIAu6WeckQ0).

[![License](https://img.shields.io/badge/license-GNUGPLv3-green.svg)](LICENSE)
![Version](https://img.shields.io/badge/version-0.0.2-58f4c2)
[![CodeQL](https://github.com/qte77/context-engineering-template/actions/workflows/codeql.yaml/badge.svg)](https://github.com/qte77/context-engineering-template/actions/workflows/codeql.yaml)
[![CodeFactor](https://www.codefactor.io/repository/github/qte77/context-engineering-template/badge)](https://www.codefactor.io/repository/github/qte77/context-engineering-template)
[![ruff](https://github.com/qte77/context-engineering-template/actions/workflows/ruff.yaml/badge.svg)](https://github.com/qte77/context-engineering-template/actions/workflows/ruff.yaml)
[![pytest](https://github.com/qte77/context-engineering-template/actions/workflows/pytest.yaml/badge.svg)](https://github.com/qte77/context-engineering-template/actions/workflows/pytest.yaml)
[![Link Checker](https://github.com/qte77/context-engineering-template/actions/workflows/links-fail-fast.yaml/badge.svg)](https://github.com/qte77/context-engineering-template/actions/workflows/links-fail-fast.yaml)
[![Deploy Docs](https://github.com/qte77/context-engineering-template/actions/workflows/generate-deploy-mkdocs-ghpages.yaml/badge.svg)](https://github.com/qte77/context-engineering-template/actions/workflows/generate-deploy-mkdocs-ghpages.yaml)

**DevEx** [![vscode.dev](https://img.shields.io/static/v1?logo=visualstudiocode&label=&message=vscode.dev&labelColor=2c2c32&color=007acc&logoColor=007acc)](https://vscode.dev/github/qte77/context-engineering-template)
[![Codespace Python Claude](https://img.shields.io/static/v1?logo=visualstudiocode&label=&message=Codespace%20Dev&labelColor=2c2c32&color=007acc&logoColor=007acc)](https://github.com/codespaces/new?repo=qte77/context-engineering-template&devcontainer_path=.devcontainer/setup_python_claude/devcontainer.json)
[![TalkToGithub](https://img.shields.io/badge/TalkToGithub-7a83ff.svg)](https://talktogithub.com/qte77/context-engineering-template)
[![llms.txt (UitHub)](https://img.shields.io/badge/llms.txt-uithub-800080.svg)](https://github.com/qte77/context-engineering-template)
[![llms.txt (GitToDoc)](https://img.shields.io/badge/llms.txt-GitToDoc-fe4a60.svg)](https://gittodoc.com/qte77/context-engineering-template)

## Status

(DRAFT) (WIP) ----> Not fully implemented yet

For version history have a look at the [CHANGELOG](CHANGELOG.md).

## Purpose

Let the Coding Agent do the heavy lifting. Build code base from top to bottom: Define Business Requirements (BRD) and afterwards features to be implemented. The goal could be to to implement some kind of guided top-down BDD: behavior > tests > implementation.

## Features

- Runs tests, linting and type checks: only

<details>
  <summary>Show Sequence Diagram</summary>
  <a href="assets/images/sequence_diagram.png">
    <img src="assets/images/sequence_diagram.png#gh-light-mode-only" alt="Sequence Diagram" title="Sequence Diagram" width="111%" />
  </a>
  <a href="assets/images/sequence_diagram.png">
    <img src="assets/images/sequence_diagram.png#gh-dark-mode-only" alt="Sequence Diagram" title="Sequence Diagram" width="111%" />
  </a>
</details>

## Setup

1. `make setup_python_claude`
2. If .env to be used: `make export_env_file`

## Usage

1. Update [Agents.md](AGENTS.md) to your needs.
2. Describe desired feature in `/context/features/feature_XXX.md`, like shown in [feature_base.md](/context/templates/feature_base.md).
3. Place optional examples into [/context/examples](/context/examples).
4. Let the Product Requirements Prompt (PRP) be generated:
   - In Claude Code CLI: `/generate-prp feature_XXX.md`
   - or: `make prp_gen_claude "ARGS=feature_XXX.md"`
5. Let the feature be implemented based on the PRP:
   - In Claude Code CLI: `/execute-prp feature_XXX.md`
   - or: `make prp_exe_claude "ARGS=feature_XXX.md"`

### Configuration

- General system behavior: `AGENTS.md`, redirected from `CLAUDE.md`
- Claude settings: `.claude/settings.local.json`
- CLaude commands: `.claude/commands`
- Feature template: `context/templates/feature_base.md`
- PRP template: `context/templates/prp_base.md`

### Environment

[.env.example](.env.example) contains examples for usage of API keys and variables.

```text
ANTHROPIC_API_KEY="sk-abc-xyz"
GEMINI_API_KEY="xyz"
GITHUB_API_KEY="ghp_xyz"
...
```

## TODO

- Implement business process as discussed in [He Built 40 Startups Using Just Prompts — Here’s His System](https://youtu.be/CIAu6WeckQ0)
- Refine `AGENTS.md` to let the agent not do bulk but incremental changes, also implement tests first, then code and iterate until functional (red > green > blue).
