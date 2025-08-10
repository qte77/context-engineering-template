# Execute Feature Requirements Prompt (FRP)

Implement a feature using the FRP file provided.

## Rules

- Extract filename from `$ARGUMENTS` into `$FILE_NAME` (append `.md` if needed)
- Write outputs to log file using AGENTS.md timestamp format `<timestamp>_Claude_ExecFRP_${FILE_NAME}` in `$CTX_LOGS_PATH` (for future agent and human analysis)
- Use TodoWrite tool to track implementation progress
- Input FRP: `$CTX_FRP_PATH/$FILE_NAME`

## Execution Process

1. **Load and Validate FRP**
   - Read the specified FRP file
   - Understand all context and requirements
   - Apply AGENTS.md Quality Evaluation Framework to assess readiness
   - **Research Policy**: Focus on execution; extend research only if significant gaps discovered during implementation. See [Failure Recovery](#failure-recovery).

2. **Plan Implementation**
   - Apply AGENTS.md Quality Evaluation Framework to assess FRP readiness
   - Create comprehensive TodoWrite plan addressing all FRP requirements
   - Break down into manageable steps following AGENTS.md BDD approach
   - Identify patterns from existing codebase to follow

3. **Implement Features**
   - Follow TodoWrite plan step-by-step
   - Mark tasks as in_progress/completed as you work
   - Create tests first (BDD/TDD approach per AGENTS.md)
   - Implement minimal viable solution then iterate

4. **Validate Implementation**
   - Use AGENTS.md unified command reference with error recovery
   - Fix failures following project patterns
   - Update TodoWrite and log progress

5. **Final Verification**
   - Complete all FRP checklist items
   - Verify against AGENTS.md Quality Evaluation Framework
   - Mark TodoWrite tasks as completed
   - Log completion status

## Escalation

Use AGENTS.md Decision Framework if:

- FRP requirements conflict with AGENTS.md
- Implementation requires architectural changes
- Critical context is missing

## Failure Recovery

**If implementation fails despite good FRP:**

1. **Analyze Failure**
   - Review logs and error messages
   - Identify specific failure points
   - Document findings in TodoWrite

2. **Iterative Improvement**
   - Update FRP with new learnings (mark as "execution-discovered gaps")
   - Adjust implementation approach
   - Re-run AGENTS.md Quality Evaluation Framework

3. **Escalate if Persistent**
   - Use AGENTS.md Decision Framework
   - Document architectural or requirement issues
   - **Report Research Gaps**: If significant research gaps caused failure, document for future FRP generation improvement
   - Request human guidance
