# Feature Requirements Prompt (FRP) template

This template is optimized for AI agents to implement features with sufficient context and self-validation capabilities to achieve working code through iterative refinement.

Use the paths defined in `context/config/paths.md`

## Core Principles

1. **Context is King**
   - Include ALL necessary documentation, examples, and caveats
   - Include docstrings for files, classes, methods and functions
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from the codebase
4. **Progressive Success**: Start simple, validate, then enhance
5. **Global rules**: Be sure to follow all rules in AGENTS.md
6. **Top-to-Bottom**: Use a Behavior Driven (BDD) and Test Driven development (TDD) approach, i.e.
   - Thinking about the desired properties and their role in the system
   - Write simple tests, then simple implementations and improve iteratively
   - [ ] Behavior described
   - [ ] Tests written
   - [ ] Logic code implemented
   - [ ] Iteratively improved tests and code
   - [ ] Tests passed
7. **Keep it simple**: Think of MVP, not full-featured production

## Goal

[What needs to be built - be specific about the end state and desires]

Provide functional tests and logic code implementation which can be integrated with other components.

## Why

- [Business value and user impact]
- [Integration with existing features]
- [Problems this solves and for whom]

## What

[User-visible behavior and technical requirements]

### Success Criteria

- [ ] List most important criteria to let the feature pass requirements

## All Needed Context

### Documentation & References (list all context needed to implement the feature)

```yaml
# Examples:
# MUST READ - Include these in your context window
- url: [Official API docs URL]
  why: [Specific sections/methods you'll need]
  
- file: [path/to/example.py]
  why: [Pattern to follow, gotchas to avoid]
  
- doc: [Library documentation URL] 
  section: [Specific section about common pitfalls]
  critical: [Key insight that prevents common errors]
```

### Current Codebase tree (run `tree` in the root of the project) to get an overview of the codebase

```bash

```

### Desired Codebase tree with files to be added and responsibility of file

```bash

```

### Known Gotchas of our codebase & Library Quirks

```python
# CRITICAL: [Library name] requires [specific setup]
# Example: FastAPI requires async functions for endpoints
# Example: This ORM doesn't support batch inserts over 1000 records
# Example: We use pydantic v2 and  
```

## Implementation Blueprint

### Data models and structure

Create the core data models, we ensure type safety and consistency.

```python
# Examples: 
# - orm models
# - pydantic models
# - pydantic schemas
# - pydantic validators
```

### list of tasks to be completed to fullfill the FRP in the order they should be completed

```yaml
Task 1:
MODIFY src/existing_module.py:
  - FIND pattern: "class OldImplementation"
  - INJECT after line containing "def __init__"
  - PRESERVE existing method signatures

CREATE src/new_feature.py:
  - MIRROR pattern from: src/similar_feature.py
  - MODIFY class name and core logic
  - KEEP error handling pattern identical

...(...)

Task N:
...
```

### Integration Points

```yaml
# Examples:
DATABASE:
  - migration: "Add column 'feature_enabled' to users table"
  - index: "CREATE INDEX idx_feature_lookup ON users(feature_id)"
  
CONFIG:
  - add to: config/settings.py
  - pattern: "FEATURE_TIMEOUT = int(os.getenv('FEATURE_TIMEOUT', '30'))"
  
ROUTES:
  - add to: src/api/routes.py  
  - pattern: "router.include_router(feature_router, prefix='/feature')"
```

## Validation Loop

### Level 1: Write tests

```python
# Examples:
# CREATE test_new_feature.py with these test cases:
def test_happy_path():
    """Basic functionality works"""
    result = new_feature("valid_input")
    assert result.status == "success"

def test_validation_error():
    """Invalid input raises ValidationError"""
    with pytest.raises(ValidationError):
        new_feature("")

def test_external_api_timeout():
    """Handles timeouts gracefully"""
    with mock.patch('external_api.call', side_effect=TimeoutError):
        result = new_feature("valid")
        assert result.status == "error"
        assert "timeout" in result.message
```

### Level 2: Syntax & Style

```bash
# Run these FIRST - fix any errors before proceeding
make ruff
make type_check
# Expected: No errors. If errors, READ the error and fix.
```

### Level 3: Implement logic code

```python
def happy_path():
  """Short description"""
  code_here
```

### Level 4: Syntax & Style

```bash
# Run these FIRST - fix any errors before proceeding
make ruff
make type_check
# Expected: No errors. If errors, READ the error and fix.
```

### Level 5: Unit Tests each new feature/file/function use existing test patterns

```bash
# Run and iterate until passing:
uv run pytest tests/<test_file_to_run>.md
# If failing: Read error, understand root cause, fix code, re-run (never mock to pass)
```

### Level 6: Integration Test

```bash
# Start the service
uv run python -m src.main --dev

# Test the endpoint
curl -X POST http://localhost:8000/feature \
  -H "Content-Type: application/json" \
  -d '{"param": "test_value"}'

# Expected: {"status": "success", "data": {...}}
# If error: Check logs at logs/app.log for stack trace
```

## Final validation Checklist

- [ ] All tests pass: `uv run pytest tests/ -v`
- [ ] No linting errors: `uv run ruff check src/`
- [ ] No type errors: `uv run mypy src/`
- [ ] Manual test successful: [specific curl/command]
- [ ] Error cases handled gracefully
- [ ] Logs are informative but not verbose
- [ ] Documentation updated if needed

## Anti-Patterns to Avoid

- ❌ Don't create new patterns when existing ones work
- ❌ Don't skip validation because "it should work"  
- ❌ Don't ignore failing tests - fix them
- ❌ Don't use sync functions in async context
- ❌ Don't hardcode values that should be config
- ❌ Don't catch all exceptions - be specific
