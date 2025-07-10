# MCP Client Implementation for Tool Invocation

## Purpose

Product Requirements Prompt (PRP) for implementing a complete MCP (Model Context Protocol) client in Python that can connect to MCP servers and invoke tools. This PRP provides comprehensive context for one-pass implementation success.

## Goal

Build a production-ready MCP client in Python that:

- Implements the MCP protocol for structured message handling
- Connects to MCP servers via stdio transport
- Provides CLI interface for invoking tools: `roll_dice`, `get_weather`, and `get_date`
- Handles connection errors, timeouts, and retries gracefully
- Follows the project's established patterns and conventions
- Is modular, testable, and extensible for future tools

## Why

- **Standardization**: Implements the MCP protocol standard for AI tool integration
- **Modularity**: Creates a foundation for connecting to any MCP server
- **User Value**: Provides command-line access to remote tools via structured protocol
- **Learning**: Demonstrates best practices for building MCP clients in Python
- **Complement**: Works with the existing MCP server implementation in the codebase

## What

### User-visible behavior

- Client connects to MCP server via stdio transport
- CLI accepts tool invocation commands like `mcp-client roll_dice --notation 3d6`
- Returns structured responses with results or detailed error messages
- Handles server connection failures gracefully with informative feedback
- Supports interactive mode for multiple tool invocations

### Success Criteria

- [ ] MCP client connects to local MCP server via stdio transport
- [ ] All three tools (`roll_dice`, `get_weather`, `get_date`) can be invoked via CLI
- [ ] Connection error handling provides helpful user feedback
- [ ] Tool invocation validation prevents malformed requests
- [ ] JSON-RPC 2.0 protocol compliance for all messages
- [ ] All code passes linting (ruff) and type checking (mypy)
- [ ] Comprehensive test coverage for all client functionality
- [ ] Client follows project conventions and patterns

## All Needed Context

### Documentation & References

```yaml
# MUST READ - Include these in your context window
- url: https://github.com/modelcontextprotocol/python-sdk
  why: Official MCP Python SDK for protocol implementation
  section: Client implementation patterns and transport methods
  critical: Use mcp.ClientSession and StdioServerParameters for connections
  
- url: https://modelcontextprotocol.io/quickstart/client
  why: Official MCP client quickstart guide
  section: Client connection patterns and message handling
  critical: AsyncExitStack for resource management, proper session handling
  
- url: https://docs.python.org/3/library/argparse.html
  why: CLI argument parsing for tool invocation interface
  section: Subcommands and argument validation
  critical: Use subparsers for different tool commands
  
- url: https://docs.python.org/3/library/asyncio.html
  why: Asynchronous programming patterns for MCP client
  section: async/await patterns and event loop management
  critical: Use asyncio.run() for main entry point
  
- url: https://docs.python.org/3/library/json.html
  why: JSON message serialization/deserialization
  section: JSON encoding/decoding with proper error handling
  critical: Handle malformed JSON responses gracefully
  
- file: /workspaces/context-engineering-template/src/mcp_server/
  why: Complete MCP server implementation to connect to
  section: server.py shows the exact tool interface and message format
  critical: Tools available: roll_dice, get_weather, get_date with specific argument formats
  
- file: /workspaces/context-engineering-template/src/mcp_server/models/requests.py
  why: Pydantic models for request/response validation
  section: MCPRequest, MCPResponse, and tool-specific models
  critical: Exact JSON-RPC 2.0 message structure and validation rules
  
- file: /workspaces/context-engineering-template/context/examples/outputs
  why: Example request/response patterns for all tools
  section: roll_dice_example.json, get_weather_example.json, get_date_example.json
  critical: Exact JSON-RPC message format with method "tools/call"
  
- file: /workspaces/context-engineering-template/pyproject.toml
  why: Project configuration, dependencies, and tool settings
  section: Dependencies and development tool configuration
  critical: Must use existing dependency management patterns
```

### Current Codebase Structure

```bash
/workspaces/context-engineering-template
├── AGENTS.md                    # Agent behavior guidelines
├── CLAUDE.md                    # Project instructions
├── pyproject.toml               # Python project configuration
├── src/
│   ├── __init__.py
│   ├── main.py                  # Main entry point (will be modified)
│   ├── py.typed
│   └── mcp_server/              # Existing MCP server implementation
│       ├── __init__.py
│       ├── server.py            # MCP server with 3 tools
│       ├── models/
│       │   ├── __init__.py
│       │   └── requests.py      # Pydantic models for validation
│       └── tools/
│           ├── __init__.py
│           ├── base.py          # Base tool interface
│           ├── dice.py          # roll_dice implementation
│           ├── weather.py       # get_weather implementation
│           └── date_time.py     # get_date implementation
├── tests/
│   ├── __init__.py
│   └── test_mcp_server.py       # Existing server tests
└── context/
    └── examples/outputs
        ├── roll_dice_example.json     # Tool invocation examples
        ├── get_weather_example.json   # Tool invocation examples
        └── get_date_example.json      # Tool invocation examples
```

### Desired Codebase Structure with Files to be Added

```bash
/workspaces/context-engineering-template
├── src/
│   ├── __init__.py
│   ├── main.py                  # Modified to support MCP client CLI
│   ├── py.typed
│   ├── mcp_server/              # Existing (unchanged)
│   └── mcp_client/              # NEW - MCP client implementation
│       ├── __init__.py
│       ├── client.py            # Main MCP client class
│       ├── cli.py               # CLI interface for tool invocation
│       ├── transport.py         # Connection and transport handling
│       └── models/
│           ├── __init__.py
│           └── responses.py     # Client-specific response models
├── tests/
│   ├── __init__.py
│   ├── test_mcp_server.py       # Existing (unchanged)
│   ├── test_mcp_client.py       # NEW - Client tests
│   └── test_cli.py              # NEW - CLI interface tests
└── context/
    └── examples/outputs
        ├── client_roll_dice_input.json    # Simple input format
        ├── client_get_weather_input.json  # Simple input format
        ├── client_get_date_input.json     # Simple input format
        └── client_invalid_tool.json       # Error handling example
```

### Known Gotchas & Library Quirks

```python
# CRITICAL: MCP protocol requires exact JSON-RPC 2.0 message structure
# Client messages must include: jsonrpc, method, params, id
# Example:
{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
        "name": "roll_dice",
        "arguments": {"notation": "2d6"}
    },
    "id": 1
}

# CRITICAL: MCP Python SDK client connection pattern
# Must use AsyncExitStack for proper resource management
async with AsyncExitStack() as stack:
    session = await stack.enter_async_context(
        stdio_client(StdioServerParameters(
            command="python",
            args=[server_script_path]
        ))
    )

# CRITICAL: Tool invocation through MCP client session
# Use session.call_tool() method with exact tool name and arguments
result = await session.call_tool("roll_dice", {"notation": "2d6"})

# CRITICAL: Server connection validation
# Must check if server is running and tools are available
tools = await session.list_tools()
if not any(tool.name == "roll_dice" for tool in tools.tools):
    raise ValueError("roll_dice tool not available")

# CRITICAL: CLI argument parsing for tool commands
# Use subparsers for different tool commands
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='tool', help='Available tools')
dice_parser = subparsers.add_parser('roll_dice', help='Roll dice')
dice_parser.add_argument('--notation', required=True, help='Dice notation (e.g., 2d6)')

# CRITICAL: Error handling for connection failures
# Distinguish between connection errors and tool execution errors
try:
    result = await session.call_tool(tool_name, arguments)
except Exception as e:
    if "connection" in str(e).lower():
        print(f"Connection error: {e}")
    else:
        print(f"Tool execution error: {e}")

# CRITICAL: JSON serialization for complex tool arguments
# Some tools accept complex arguments that need proper JSON handling
import json
arguments = json.loads(args.arguments) if args.arguments else {}
```

## Implementation Blueprint

### Data Models and Structure

Create client-specific models for type safety and validation:

```python
# src/mcp_client/models/responses.py
from pydantic import BaseModel, Field
from typing import Optional, Union, Any, List

class MCPToolResponse(BaseModel):
    """Response from MCP tool execution"""
    content: List[dict] = Field(..., description="Response content")
    isError: bool = Field(False, description="Whether response indicates error")

class ClientToolResult(BaseModel):
    """Processed tool result for client consumption"""
    success: bool
    result: Optional[Any] = None
    error: Optional[str] = None
    tool_name: str
    arguments: dict

class ClientSession(BaseModel):
    """Client session information"""
    server_path: str
    connected: bool = False
    available_tools: List[str] = Field(default_factory=list)
```

### List of Tasks to be Completed in Order

```yaml
Task 1: Setup Dependencies
ADD to pyproject.toml:
  - mcp>=0.7.0 (official MCP Python SDK)
  - Use existing httpx, pydantic, and argparse dependencies

Task 2: Create MCP Client Core
CREATE src/mcp_client/client.py:
  - DEFINE MCPClient class with connection management
  - IMPLEMENT server connection via stdio transport
  - HANDLE tool discovery and validation
  - ESTABLISH session lifecycle management

Task 3: Create Transport Layer
CREATE src/mcp_client/transport.py:
  - IMPLEMENT stdio transport connection
  - HANDLE connection errors and retries
  - MANAGE server process lifecycle
  - PROVIDE connection health checks

Task 4: Create CLI Interface
CREATE src/mcp_client/cli.py:
  - IMPLEMENT argument parsing for tool commands
  - CREATE subcommands for each tool (roll_dice, get_weather, get_date)
  - HANDLE tool argument validation
  - PROVIDE user-friendly error messages

Task 5: Integrate with Main Entry Point
MODIFY src/main.py:
  - ADD MCP client CLI commands
  - PRESERVE existing functionality
  - HANDLE both client and server modes
  - MAINTAIN async pattern

Task 6: Create Simple Input Examples
CREATE context/examples/outputs/client_*.json:
  - GENERATE simple input format examples
  - INCLUDE error case example (invalid tool)
  - FOLLOW format from feature specification
  - ENABLE automated testing with these examples

Task 7: Implement Response Processing
CREATE src/mcp_client/models/responses.py:
  - DEFINE response processing models
  - HANDLE successful tool responses
  - PROCESS error responses with user-friendly messages
  - VALIDATE response format

Task 8: Implement Comprehensive Tests
CREATE tests/test_mcp_client.py and tests/test_cli.py:
  - UNIT tests for client connection and tool invocation
  - INTEGRATION tests with actual server
  - MOCK tests for connection failures
  - CLI command tests with argument validation

Task 9: Add Error Handling and Retry Logic
ENHANCE client.py and transport.py:
  - IMPLEMENT connection retry with exponential backoff
  - HANDLE server startup timeouts
  - PROVIDE graceful degradation for tool failures
  - LOG errors appropriately for debugging

Task 10: Final Integration and Validation
RUN validation commands:
  - EXECUTE make ruff (code formatting)
  - EXECUTE make type_check (mypy validation)
  - EXECUTE make test_all (pytest suite)
  - MANUAL test client-server integration
```

### Per Task Pseudocode

```python
# Task 2: MCP Client Core
class MCPClient:
    def __init__(self, server_path: str):
        self.server_path = server_path
        self.session: Optional[ClientSession] = None
        self.available_tools: List[str] = []
    
    async def connect(self) -> None:
        """Connect to MCP server via stdio"""
        # PATTERN: Use AsyncExitStack for resource management
        self.stack = AsyncExitStack()
        
        # CRITICAL: Validate server script exists
        if not os.path.exists(self.server_path):
            raise FileNotFoundError(f"Server script not found: {self.server_path}")
        
        # PATTERN: Create stdio connection
        server_params = StdioServerParameters(
            command="python" if self.server_path.endswith('.py') else "node",
            args=[self.server_path]
        )
        
        try:
            self.session = await self.stack.enter_async_context(
                stdio_client(server_params)
            )
            
            # CRITICAL: Discover available tools
            tools_result = await self.session.list_tools()
            self.available_tools = [tool.name for tool in tools_result.tools]
            
        except Exception as e:
            await self.stack.aclose()
            raise ConnectionError(f"Failed to connect to server: {e}")
    
    async def invoke_tool(self, tool_name: str, arguments: dict) -> ClientToolResult:
        """Invoke a tool on the connected server"""
        # PATTERN: Validate tool availability
        if tool_name not in self.available_tools:
            return ClientToolResult(
                success=False,
                error=f"Tool '{tool_name}' not available. Available: {self.available_tools}",
                tool_name=tool_name,
                arguments=arguments
            )
        
        try:
            # CRITICAL: Use session.call_tool() for invocation
            result = await self.session.call_tool(tool_name, arguments)
            
            return ClientToolResult(
                success=True,
                result=result.content,
                tool_name=tool_name,
                arguments=arguments
            )
            
        except Exception as e:
            return ClientToolResult(
                success=False,
                error=str(e),
                tool_name=tool_name,
                arguments=arguments
            )
    
    async def disconnect(self) -> None:
        """Disconnect from server"""
        if self.stack:
            await self.stack.aclose()

# Task 4: CLI Interface
class MCPClientCLI:
    def __init__(self):
        self.parser = self._create_parser()
        self.client: Optional[MCPClient] = None
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser with subcommands"""
        parser = argparse.ArgumentParser(
            description="MCP Client for tool invocation"
        )
        
        parser.add_argument(
            '--server', 
            required=True, 
            help='Path to MCP server script'
        )
        
        # PATTERN: Subcommands for each tool
        subparsers = parser.add_subparsers(dest='tool', help='Available tools')
        
        # Dice rolling tool
        dice_parser = subparsers.add_parser('roll_dice', help='Roll dice')
        dice_parser.add_argument(
            '--notation', 
            required=True, 
            help='Dice notation (e.g., 2d6, 1d20)'
        )
        
        # Weather tool
        weather_parser = subparsers.add_parser('get_weather', help='Get weather')
        weather_parser.add_argument(
            '--location', 
            required=True, 
            help='Location name or coordinates'
        )
        
        # Date tool
        date_parser = subparsers.add_parser('get_date', help='Get date/time')
        date_parser.add_argument(
            '--timezone', 
            default='UTC', 
            help='Timezone (default: UTC)'
        )
        
        return parser
    
    async def run(self, args: List[str]) -> None:
        """Run CLI with provided arguments"""
        parsed_args = self.parser.parse_args(args)
        
        if not parsed_args.tool:
            self.parser.print_help()
            return
        
        # PATTERN: Connect to server
        self.client = MCPClient(parsed_args.server)
        
        try:
            await self.client.connect()
            
            # PATTERN: Build tool arguments
            tool_args = {}
            if parsed_args.tool == 'roll_dice':
                tool_args = {'notation': parsed_args.notation}
            elif parsed_args.tool == 'get_weather':
                tool_args = {'location': parsed_args.location}
            elif parsed_args.tool == 'get_date':
                tool_args = {'timezone': parsed_args.timezone}
            
            # PATTERN: Invoke tool and display result
            result = await self.client.invoke_tool(parsed_args.tool, tool_args)
            
            if result.success:
                self._display_success(result)
            else:
                self._display_error(result)
                
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if self.client:
                await self.client.disconnect()
    
    def _display_success(self, result: ClientToolResult) -> None:
        """Display successful tool result"""
        print(f"✅ {result.tool_name} executed successfully:")
        
        # PATTERN: Handle different response formats
        if result.result and isinstance(result.result, list):
            for item in result.result:
                if isinstance(item, dict) and 'text' in item:
                    print(item['text'])
                else:
                    print(json.dumps(item, indent=2))
        else:
            print(json.dumps(result.result, indent=2))
    
    def _display_error(self, result: ClientToolResult) -> None:
        """Display tool execution error"""
        print(f"❌ {result.tool_name} failed:")
        print(f"Error: {result.error}")
```

### Integration Points

```yaml
DEPENDENCIES:
  - add to: pyproject.toml
  - packages: ["mcp>=0.7.0"]
  - note: Use existing httpx, pydantic, argparse dependencies
  
MAIN_ENTRY:
  - modify: src/main.py
  - pattern: "async def main() -> None:"
  - add client CLI command handling alongside server functionality
  
TESTING:
  - add to: tests/
  - pattern: "pytest fixtures for client-server integration"
  - mock server responses for unit tests
  - integration tests with actual server startup
```

## Validation Loop

### Level 1: Syntax & Style

```bash
# Run these FIRST - fix any errors before proceeding
uv run ruff check src/ --fix
uv run mypy src/

# Expected: No errors. If errors exist, read and fix them.
```

### Level 2: Unit Tests

```python
# CREATE test_mcp_client.py
async def test_client_connection():
    """Test client can connect to server"""
    client = MCPClient("src/mcp_server/server.py")
    await client.connect()
    assert len(client.available_tools) == 3
    assert "roll_dice" in client.available_tools
    await client.disconnect()

async def test_tool_invocation():
    """Test tool invocation works correctly"""
    client = MCPClient("src/mcp_server/server.py")
    await client.connect()
    
    result = await client.invoke_tool("roll_dice", {"notation": "2d6"})
    assert result.success
    assert result.tool_name == "roll_dice"
    
    await client.disconnect()

async def test_invalid_tool():
    """Test invalid tool handling"""
    client = MCPClient("src/mcp_server/server.py")
    await client.connect()
    
    result = await client.invoke_tool("invalid_tool", {})
    assert not result.success
    assert "not available" in result.error
    
    await client.disconnect()

def test_cli_argument_parsing():
    """Test CLI argument parsing"""
    cli = MCPClientCLI()
    
    # Test dice command
    args = ['--server', 'server.py', 'roll_dice', '--notation', '2d6']
    parsed = cli.parser.parse_args(args)
    assert parsed.tool == 'roll_dice'
    assert parsed.notation == '2d6'
    
    # Test weather command
    args = ['--server', 'server.py', 'get_weather', '--location', 'London']
    parsed = cli.parser.parse_args(args)
    assert parsed.tool == 'get_weather'
    assert parsed.location == 'London'
```

```bash
# Run and iterate until passing:
uv run pytest tests/test_mcp_client.py -v
uv run pytest tests/test_cli.py -v
# If failing: Read error, fix code, re-run
```

### Level 3: Integration Test

```bash
# Test client-server integration
# 1. Start server in background
uv run python -m src.mcp_server.server &

# 2. Test client connection and tool invocation
uv run python -m src.main --server src/mcp_server/server.py roll_dice --notation 2d6
uv run python -m src.main --server src/mcp_server/server.py get_weather --location "San Francisco"
uv run python -m src.main --server src/mcp_server/server.py get_date --timezone UTC

# 3. Test error handling
uv run python -m src.main --server src/mcp_server/server.py roll_dice --notation invalid
```

## Final Validation Checklist

- [ ] All tests pass: `uv run pytest tests/ -v`
- [ ] No linting errors: `uv run ruff check src/`
- [ ] No type errors: `uv run mypy src/`
- [ ] Client connects to server successfully
- [ ] All three tools can be invoked via CLI
- [ ] Invalid tool names return helpful error messages
- [ ] Invalid tool arguments return helpful error messages
- [ ] Connection errors are handled gracefully
- [ ] Simple input JSON files are created and valid
- [ ] CLI help messages are clear and informative

## Anti-Patterns to Avoid

- ❌ Don't use synchronous functions in async context
- ❌ Don't ignore MCP protocol message structure requirements
- ❌ Don't expose internal connection details to CLI users
- ❌ Don't hardcode server paths or tool names
- ❌ Don't skip connection validation before tool invocation
- ❌ Don't catch all exceptions - be specific about error types
- ❌ Don't assume server is always available - handle startup failures
- ❌ Don't block the event loop with synchronous operations
- ❌ Don't ignore resource cleanup - always close connections

---

## Quality Score: 9/10

This PRP provides comprehensive context for one-pass implementation:

- ✅ Complete MCP protocol documentation and client patterns
- ✅ Detailed existing server implementation to connect to
- ✅ Specific CLI interface requirements and argument parsing
- ✅ Executable validation commands and test patterns
- ✅ Clear task breakdown with pseudocode and examples
- ✅ Anti-patterns and common pitfalls identified
- ✅ Integration points with existing codebase clearly defined
- ✅ Example files structure and format specifications

**Areas for improvement:**

- Could include more specific error message examples
- Could provide more detailed transport layer specifications

**Confidence Level:** Very High - This PRP contains comprehensive technical detail, existing implementation context, and clear validation steps for successful implementation by an AI agent with access to the codebase and web search capabilities.
