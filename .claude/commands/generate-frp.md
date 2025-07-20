# Generate Feature Requirements Prompt (FRP)

Generate a complete FRP for general feature implementation with thorough research. Ensure context is passed to the AI agent to enable self-validation and iterative refinement. Read the feature file first to understand what needs to be created, how the examples provided help, and any other considerations.

The AI agent only gets the context you are appending to the FRP and training data. Assume the AI agent has access to the codebase and the same knowledge cutoff as you, so its important that your research findings are included or referenced in the FRP. The Agent has Websearch capabilities, so pass urls to documentation and examples.

- Extract only the filename and extension from `$ARGUMENTS` into `$FILE_NAME`. Append extension `.md` if necessary.
- Use the paths defined in `context/config/paths.md`
- Important ! Write your outputs from CLI in real-time to the log file `<timestamp>_Claude_GenFRP_${FILE_NAME}` in `$CTX_LOGS_PATH`. Also include your itnernalt thinking steps. Use the configured time stamp formatting.
- `CTX_FEATURE_FILE = ${CTX_FEATURES_PATH}/${FILE_NAME}`
- `CTX_FRP_FILE = ${CTX_FRP_PATH}/${FILE_NAME}`
- `CTX_FRP_TEMPLATE = ${CTX_TEMPLATES_PATH}/${FRP_base.md}`
- Input file: `$CTX_FEATURE_FILE`
- Output file: `$CTX_FRP_FILE`

## Research Process

1. **Codebase Analysis**
   - Search for similar features/patterns in the codebase
   - Identify files to reference in `$CTX_FRP_FILE`
   - Note existing conventions to follow
   - Check test patterns for validation approach

2. **External Research**
   - Search for similar features/patterns online
   - Library documentation (include specific URLs)
   - Implementation examples (GitHub/StackOverflow/blogs)
   - Best practices and common pitfalls

3. **User Clarification** (if needed)
   - Specific patterns to mirror and where to find them?
   - Integration requirements and where to find them?

## FRP Generation

Use `$CTX_FRP_TEMPLATE` as template

### Critical Context to Include and pass to the AI agent as part of the FRP

- **Documentation**: URLs with specific sections
- **Code Examples**: Real snippets from codebase
- **Gotchas**: Library quirks, version issues
- **Patterns**: Existing approaches to follow

### Implementation Blueprint

- Start with pseudocode showing approach
- Reference real files for patterns
- Include error handling strategy
- list tasks to be completed to fullfill the FRP in the order they should be completed

### Validation Gates (Must be Executable) e.g. for python

```bash
# Syntax/Style
make ruff
make type_check

# Unit Tests
# make coverage_all
```

***CRITICAL AFTER YOU ARE DONE RESEARCHING AND EXPLORING THE CODEBASE BEFORE YOU START WRITING THE FRP***

***ULTRATHINK ABOUT THE FRP AND PLAN YOUR APPROACH THEN START WRITING THE FRP***

## Quality Checklist

- [ ] All necessary context included
- [ ] References existing patterns
- [ ] Clear implementation path
- [ ] Error handling documented
- [ ] Validation gates are executable by AI

Score the FRP on a scale of 1-10 (confidence level to succeed in one-pass implementation using claude codes)

Remember: The goal is one-pass implementation success through comprehensive context.
