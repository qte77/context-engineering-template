# Create Feature Requirements Prompt (FRP)

This command aims to extract core intent from feature description and create targeted FRP. Furthermore structure inputs to optimize agent reasoning within project constraints.

## Rules

- Extract filename from `$ARGUMENTS` into `$FILE_NAME` (append `.md` if needed)
- Use TodoWrite tool to track progress throughout the process
- Input: `$CTX_FEATURES_PATH/$FILE_NAME`
- Template: `$CTX_FRP_TEMPLATE`
- Output: `$CTX_FRP_PATH/$FILE_NAME`

## Research Process

1. **Codebase Analysis**
   - Search for similar features and patterns
   - Use Agent tool for multi-file searches when scope unclear
   - Use Grep tool for specific pattern searches
   - Document patterns in TodoWrite tool

2. **Context Gathering**
   - Verify file paths exist before referencing
   - Check test patterns in `$TEST_PATH`
   - Note integration points in existing agent system

**Research Completeness:** Conduct comprehensive research during FRP generation to minimize additional research needed during execution phase.

## FRP Generation

Use `$CTX_FRP_TEMPLATE` as base template.

### Include in FRP

- **Code Examples**: Real patterns from codebase analysis
- **Dependencies**: Verified libraries from `$PROJECT_REQUIREMENTS`
- **Integration Points**: Existing agent system touchpoints
- **Error Handling**: Project-defined error functions

### Implementation Structure

- Clear objective and deliverable
- Implementation tasks in order
- Reference patterns from codebase

## Planning and Execution

**Before writing the FRP:**

1. Create TodoWrite plan for FRP generation
2. Validate all research findings
3. Structure FRP for one-pass implementation success

## Quality Checklist

**FRP-Specific:**

- [ ] Clear implementation objective defined
- [ ] Real code examples from codebase included
- [ ] File paths confirmed to exist
- [ ] Integration points with agent system identified
- [ ] TodoWrite plan created for implementation tracking

## FRP Validation Checklist

**Before handoff to execution:**

- [ ] All template sections populated with specific information
- [ ] Code examples reference actual files from codebase
- [ ] Implementation tasks ordered logically
- [ ] Integration points clearly identified
- [ ] Quality evaluation scores meet AGENTS.md thresholds
- [ ] FRP self-contained (minimal additional research needed during execution)

## Success Metrics

- Apply AGENTS.md Quality Evaluation Framework to FRP
- **Must** proceed only if all scores meet AGENTS.md minimum thresholds
