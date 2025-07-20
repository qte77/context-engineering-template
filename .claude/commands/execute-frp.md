# Execute Feature Requirements Prompt (FRP)

Implement a feature using the template FRP file and the feature desciption file provided by the user.

- Extract only the filename and extension from `$ARGUMENTS` into `$FILE_NAME`. Append extension `.md` if necessary.
- Use the paths defined in `context/config/paths.md`
- Important ! Write your outputs from CLI in real-time to the log file `<timestamp>_Claude_ExecFRP_${FILE_NAME}` in `$CTX_LOGS_PATH`. Also include your internal thinking steps. Use the configured time stamp formatting.
- `CTX_FRP_FILE = ${CTX_FRP_PATH}/${FILE_NAME}`

## Execution Process

1. **Load FRP**
   - Read the specified `$CTX_FRP_FILE`
   - Understand all context and requirements
   - Follow all instructions in the FRP and extend the research if needed
   - Ensure you have all needed context to implement the FRP fully
   - Do more web searches and codebase exploration as needed

2. **ULTRATHINK**
   - Think hard before you execute the plan. Create a comprehensive plan addressing all requirements.
   - Break down complex tasks into smaller, manageable steps using your todos tools.
   - Use the TodoWrite tool to create and track your implementation plan.
   - Identify implementation patterns from existing code to follow.

3. **Execute the plan**
   - Execute the FRP
   - Implement all the code

4. **Validate**
   - Run each validation command
   - Fix any failures
   - Re-run until all pass

5. **Complete**
   - Ensure all checklist items done
   - Run final validation suite
   - Report completion status
   - Read the FRP again to ensure you have implemented everything

6. **Reference the FRP**
   - You can always reference the FRP again if needed

Note: If validation fails, use error patterns in FRP to fix and retry.
