# Streamlit GUI for MCP Server-Client Interaction Showcase

## Purpose

Product Requirements Prompt (PRP) for implementing a comprehensive Streamlit-based GUI that demonstrates MCP Server-Client interaction. This PRP provides complete context for building an interactive interface that showcases tool invocation, real-time communication, and user-friendly error handling.

## Goal

Build a production-ready Streamlit GUI that:

- Provides interactive forms for invoking MCP tools (`roll_dice`, `get_weather`, `get_date`)
- Displays real-time request/response payloads with proper formatting
- Shows connection status and handles errors gracefully
- Maintains interaction history for the current session
- Serves as both a testing interface and demonstration tool
- Follows the project's established patterns and conventions
- Is responsive, user-friendly, and extensible for future tools

## Why

- **User Experience**: Provides non-technical users access to MCP tools without CLI
- **Demonstration**: Visual showcase of MCP protocol communication patterns
- **Testing**: Interactive interface for manual testing and validation
- **Learning**: Demonstrates best practices for building Streamlit applications
- **Integration**: Showcases seamless integration between GUI and backend services
- **Accessibility**: Makes MCP tools accessible to users unfamiliar with command-line interfaces

## What

### User-visible behavior

- Interactive web interface accessible via browser
- Form inputs for each tool with validation and help text
- Real-time display of JSON request/response payloads
- Connection status indicator with health checks
- Session history showing previous interactions
- Error messages displayed with helpful context
- Visual feedback for request processing states

### Success Criteria

- [ ] Streamlit GUI launches and displays tool selection interface
- [ ] All three tools can be invoked through interactive forms
- [ ] Request/response payloads are displayed in real-time
- [ ] Connection status is clearly indicated and updated
- [ ] Error handling provides user-friendly messages
- [ ] Session history tracks all interactions
- [ ] GUI is responsive and provides good user experience
- [ ] All code passes linting (ruff) and type checking (mypy)
- [ ] GUI integration tests validate core functionality

## All Needed Context

### Documentation & References

```yaml
# MUST READ - Include these in your context window
- url: https://docs.streamlit.io/
  why: Official Streamlit documentation for building interactive web apps
  section: Session state, forms, columns, and real-time updates
  critical: Use st.session_state for maintaining connection and history
  
- url: https://docs.streamlit.io/develop/concepts/architecture/session-state
  why: Session state management for maintaining GUI state
  section: Session state patterns and best practices
  critical: Persistent connection state across user interactions
  
- url: https://docs.streamlit.io/develop/api-reference/widgets/form
  why: Form widgets for tool parameter input
  section: Form validation and submission handling
  critical: Use st.form() for batch input submission
  
- url: https://docs.streamlit.io/develop/api-reference/status
  why: Status indicators and progress feedback
  section: st.spinner, st.success, st.error, st.warning
  critical: Real-time feedback for async operations
  
- url: https://docs.streamlit.io/develop/api-reference/layout
  why: Layout components for organized GUI structure
  section: Columns, containers, and tabs for organized interface
  critical: Use st.columns() for side-by-side layout
  
- file: /workspaces/context-engineering-template/src/mcp_client/
  why: Complete MCP client implementation to integrate with GUI
  section: client.py, transport.py, and models/responses.py
  critical: Use existing MCPClient class for server communication
  
- file: /workspaces/context-engineering-template/src/mcp_server/
  why: Complete MCP server implementation and tool specifications
  section: server.py and tools/ directory for tool interfaces
  critical: Exact tool parameters and response formats
  
- file: /workspaces/context-engineering-template/context/examples/outputs
  why: Example request/response patterns and expected formats
  section: client_*.json files for input validation patterns
  critical: GUI input validation should match CLI patterns
  
- file: /workspaces/context-engineering-template/pyproject.toml
  why: Project dependencies and configuration
  section: Current dependencies and development tools
  critical: Add streamlit to dependencies while maintaining existing patterns
```

### Current Codebase Structure

```bash
/workspaces/context-engineering-template
├── AGENTS.md                    # Agent behavior guidelines
├── CLAUDE.md                    # Project instructions
├── Makefile                     # Build and development commands
├── pyproject.toml               # Python project configuration
├── src/
│   ├── __init__.py
│   ├── main.py                  # Main entry point (will be modified)
│   ├── py.typed
│   ├── mcp_client/              # Complete MCP client implementation
│   │   ├── __init__.py
│   │   ├── client.py            # MCPClient class for server communication
│   │   ├── cli.py               # CLI interface (patterns to follow)
│   │   ├── transport.py         # Connection and transport handling
│   │   └── models/
│   │       ├── __init__.py
│   │       └── responses.py     # Client response models
│   └── mcp_server/              # Complete MCP server implementation
│       ├── __init__.py
│       ├── server.py            # MCP server with 3 tools
│       ├── models/
│       │   ├── __init__.py
│       │   └── requests.py      # Tool request/response models
│       └── tools/
│           ├── __init__.py
│           ├── base.py          # Base tool interface
│           ├── dice.py          # roll_dice implementation
│           ├── weather.py       # get_weather implementation
│           └── date_time.py     # get_date implementation
├── tests/
│   ├── __init__.py
│   ├── test_mcp_client.py       # Client tests (patterns to follow)
│   ├── test_mcp_server.py       # Server tests
│   └── test_cli.py              # CLI tests (patterns to follow)
└── context/
    └── examples/outputs
        ├── client_roll_dice_input.json     # Input format examples
        ├── client_get_weather_input.json   # Input format examples
        ├── client_get_date_input.json      # Input format examples
        └── client_invalid_tool.json        # Error handling examples
```

### Desired Codebase Structure with Files to be Added

```bash
/workspaces/context-engineering-template
├── src/
│   ├── __init__.py
│   ├── main.py                  # Modified to support GUI launch
│   ├── py.typed
│   ├── mcp_client/              # Existing (unchanged)
│   ├── mcp_server/              # Existing (unchanged)
│   └── gui/                     # NEW - Streamlit GUI implementation
│       ├── __init__.py
│       ├── app.py               # Main Streamlit application
│       ├── components/          # Reusable GUI components
│       │   ├── __init__.py
│       │   ├── tool_forms.py    # Tool-specific form components
│       │   ├── connection.py    # Connection status components
│       │   └── history.py       # Session history components
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── formatting.py    # JSON formatting and display utilities
│       │   └── validation.py    # Input validation utilities
│       └── models/
│           ├── __init__.py
│           └── gui_models.py    # GUI-specific data models
├── tests/
│   ├── __init__.py
│   ├── test_mcp_client.py       # Existing (unchanged)
│   ├── test_mcp_server.py       # Existing (unchanged)
│   ├── test_cli.py              # Existing (unchanged)
│   └── test_gui.py              # NEW - GUI component tests
└── context/
    └── examples/outputs
        ├── streamlit_roll_dice_interaction.json    # GUI interaction examples
        ├── streamlit_get_weather_interaction.json  # GUI interaction examples
        ├── streamlit_get_date_interaction.json     # GUI interaction examples
        └── streamlit_error_handling.json           # GUI error examples
```

### Known Gotchas & Library Quirks

```python
# CRITICAL: Streamlit session state management
# Must use st.session_state for persistent data across reruns
if 'mcp_client' not in st.session_state:
    st.session_state.mcp_client = None
    st.session_state.connected = False
    st.session_state.interaction_history = []

# CRITICAL: Streamlit async operation handling
# Streamlit doesn't natively support async/await - must use asyncio.run()
import asyncio
result = asyncio.run(client.invoke_tool(tool_name, arguments))

# CRITICAL: Streamlit form submission pattern
# Use st.form() to batch inputs and prevent premature submission
with st.form("tool_form"):
    param1 = st.text_input("Parameter 1")
    param2 = st.text_input("Parameter 2")
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        # Process form data here
        pass

# CRITICAL: Streamlit rerun behavior
# GUI reruns on every interaction - must handle state carefully
# Use st.rerun() to trigger manual updates after async operations
if st.button("Connect"):
    asyncio.run(connect_to_server())
    st.rerun()  # Force refresh after connection

# CRITICAL: MCP client connection management in GUI
# Must handle connection lifecycle properly in Streamlit context
async def ensure_connection():
    if st.session_state.mcp_client is None:
        st.session_state.mcp_client = MCPClient("src/mcp_server/server.py")
    
    if not st.session_state.mcp_client.connected:
        await st.session_state.mcp_client.connect()
        st.session_state.connected = True

# CRITICAL: JSON display formatting
# Use st.json() for proper JSON display with syntax highlighting
st.json({"request": request_data, "response": response_data})

# CRITICAL: Error handling in Streamlit
# Use st.error() for error messages and st.exception() for stack traces
try:
    result = await client.invoke_tool(tool_name, args)
    st.success("Tool executed successfully!")
except Exception as e:
    st.error(f"Error: {str(e)}")
    st.exception(e)  # Show full stack trace in development

# CRITICAL: Real-time updates with spinner
# Use st.spinner() for long-running operations
with st.spinner("Executing tool..."):
    result = asyncio.run(client.invoke_tool(tool_name, args))
```

## Implementation Blueprint

### Data Models and Structure

Create GUI-specific models for state management and type safety:

```python
# src/gui/models/gui_models.py
from pydantic import BaseModel, Field
from typing import Optional, Any, List
from datetime import datetime

class GUIInteraction(BaseModel):
    """Single tool interaction record for GUI history"""
    timestamp: datetime = Field(default_factory=datetime.now)
    tool_name: str
    arguments: dict[str, Any]
    request_payload: dict[str, Any]
    response_payload: dict[str, Any]
    success: bool
    error_message: Optional[str] = None
    execution_time: Optional[float] = None

class GUISession(BaseModel):
    """GUI session state management"""
    connected: bool = False
    server_path: str = "src/mcp_server/server.py"
    available_tools: List[str] = Field(default_factory=list)
    interaction_history: List[GUIInteraction] = Field(default_factory=list)
    current_tool: Optional[str] = None
    
class ConnectionStatus(BaseModel):
    """Connection status information"""
    connected: bool = False
    server_path: str
    last_health_check: Optional[datetime] = None
    available_tools: List[str] = Field(default_factory=list)
    error_message: Optional[str] = None
```

### List of Tasks to be Completed in Order

```yaml
Task 1: Setup Dependencies
ADD to pyproject.toml:
  - streamlit>=1.28.0 (latest stable version)
  - Use existing asyncio, json, and datetime from stdlib
  - PRESERVE existing dependency versions

Task 2: Create Main GUI Application
CREATE src/gui/app.py:
  - IMPLEMENT main Streamlit application entry point
  - SETUP session state management for persistent connection
  - CREATE main page layout with tool selection interface
  - ESTABLISH connection management and health checking

Task 3: Create GUI Models
CREATE src/gui/models/gui_models.py:
  - DEFINE GUIInteraction, GUISession, and ConnectionStatus models
  - IMPLEMENT Pydantic validation for GUI state
  - PROVIDE type safety for session management
  - ENABLE structured interaction history

Task 4: Create Connection Management Component
CREATE src/gui/components/connection.py:
  - IMPLEMENT connection status display with health indicator
  - HANDLE connection establishment and error recovery
  - PROVIDE real-time connection monitoring
  - DISPLAY available tools and server information

Task 5: Create Tool Form Components
CREATE src/gui/components/tool_forms.py:
  - IMPLEMENT dice roll form with notation validation
  - IMPLEMENT weather form with location input and examples
  - IMPLEMENT date/time form with timezone selection
  - PROVIDE input validation and helpful user guidance

Task 6: Create History Management Component
CREATE src/gui/components/history.py:
  - IMPLEMENT session history display with filtering
  - PROVIDE interaction timeline with timestamps
  - ENABLE request/response payload inspection
  - SUPPORT history export and clearing

Task 7: Create Formatting and Validation Utilities
CREATE src/gui/utils/formatting.py and validation.py:
  - IMPLEMENT JSON formatting for request/response display
  - PROVIDE syntax highlighting for JSON payloads
  - IMPLEMENT input validation with user-friendly messages
  - HANDLE error formatting and display

Task 8: Integration with Main Entry Point
MODIFY src/main.py:
  - ADD GUI launch command alongside existing CLI
  - PRESERVE existing server and client functionality
  - HANDLE GUI-specific argument parsing
  - MAINTAIN async pattern compatibility

Task 9: Create Example Interaction Files
CREATE context/examples/outputs/streamlit_*.json:
  - GENERATE example GUI interaction patterns
  - INCLUDE successful tool execution examples
  - PROVIDE error handling scenarios
  - ENABLE automated testing validation

Task 10: Implement GUI Tests
CREATE tests/test_gui.py:
  - UNIT tests for GUI components and utilities
  - INTEGRATION tests with MCP client functionality
  - MOCK tests for connection scenarios
  - STREAMLIT specific testing patterns

Task 11: Add Make Commands
MODIFY Makefile:
  - ADD run_gui command to launch Streamlit application
  - INTEGRATE GUI testing into existing test suite
  - PROVIDE GUI-specific development commands
  - MAINTAIN existing command structure
```

### Per Task Pseudocode

```python
# Task 2: Main GUI Application
# src/gui/app.py
import streamlit as st
import asyncio
from ..mcp_client.client import MCPClient
from .models.gui_models import GUISession, GUIInteraction
from .components.connection import ConnectionManager
from .components.tool_forms import ToolForms
from .components.history import HistoryManager

def main():
    """Main Streamlit application entry point"""
    st.set_page_config(
        page_title="MCP Tool Showcase",
        page_icon="🛠️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # PATTERN: Initialize session state
    if 'gui_session' not in st.session_state:
        st.session_state.gui_session = GUISession()
    
    if 'mcp_client' not in st.session_state:
        st.session_state.mcp_client = None
    
    # PATTERN: Main layout with sidebar
    with st.sidebar:
        st.title("🛠️ MCP Tool Showcase")
        connection_manager = ConnectionManager()
        connection_manager.render()
    
    # PATTERN: Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("Tool Invocation")
        if st.session_state.gui_session.connected:
            tool_forms = ToolForms()
            tool_forms.render()
        else:
            st.info("Please connect to the MCP server first")
    
    with col2:
        st.header("Request/Response")
        if st.session_state.gui_session.interaction_history:
            latest_interaction = st.session_state.gui_session.interaction_history[-1]
            st.subheader("Latest Request")
            st.json(latest_interaction.request_payload)
            st.subheader("Latest Response")
            st.json(latest_interaction.response_payload)
        else:
            st.info("No interactions yet")
    
    # PATTERN: History section
    st.header("Interaction History")
    history_manager = HistoryManager()
    history_manager.render()

# Task 4: Connection Management
# src/gui/components/connection.py
class ConnectionManager:
    """Manages MCP server connection in GUI"""
    
    def render(self):
        """Render connection management interface"""
        st.subheader("Connection Status")
        
        # PATTERN: Display current status
        if st.session_state.gui_session.connected:
            st.success("✅ Connected to MCP Server")
            st.write(f"Server: {st.session_state.gui_session.server_path}")
            st.write(f"Available Tools: {', '.join(st.session_state.gui_session.available_tools)}")
            
            # PATTERN: Health check button
            if st.button("Health Check"):
                self._perform_health_check()
            
            # PATTERN: Disconnect button
            if st.button("Disconnect"):
                self._disconnect()
        else:
            st.error("❌ Not Connected")
            
            # PATTERN: Connection form
            server_path = st.text_input(
                "Server Path",
                value=st.session_state.gui_session.server_path,
                help="Path to MCP server script"
            )
            
            if st.button("Connect"):
                self._connect(server_path)
    
    def _connect(self, server_path: str):
        """Connect to MCP server"""
        try:
            with st.spinner("Connecting to server..."):
                # CRITICAL: Handle async in Streamlit
                client = MCPClient(server_path)
                asyncio.run(client.connect())
                
                st.session_state.mcp_client = client
                st.session_state.gui_session.connected = True
                st.session_state.gui_session.server_path = server_path
                st.session_state.gui_session.available_tools = client.available_tools
                
                st.success("Connected successfully!")
                st.rerun()
                
        except Exception as e:
            st.error(f"Connection failed: {str(e)}")
            st.exception(e)
    
    def _disconnect(self):
        """Disconnect from MCP server"""
        if st.session_state.mcp_client:
            asyncio.run(st.session_state.mcp_client.disconnect())
            st.session_state.mcp_client = None
            st.session_state.gui_session.connected = False
            st.session_state.gui_session.available_tools = []
            st.success("Disconnected successfully!")
            st.rerun()
    
    def _perform_health_check(self):
        """Perform health check on connection"""
        if st.session_state.mcp_client:
            try:
                health = asyncio.run(st.session_state.mcp_client.health_check())
                if health:
                    st.success("Health check passed!")
                else:
                    st.warning("Health check failed - connection may be unhealthy")
            except Exception as e:
                st.error(f"Health check error: {str(e)}")

# Task 5: Tool Form Components
# src/gui/components/tool_forms.py
class ToolForms:
    """Manages tool-specific form interfaces"""
    
    def render(self):
        """Render tool selection and forms"""
        available_tools = st.session_state.gui_session.available_tools
        
        if not available_tools:
            st.warning("No tools available")
            return
        
        # PATTERN: Tool selection
        selected_tool = st.selectbox(
            "Select Tool",
            options=available_tools,
            help="Choose a tool to invoke"
        )
        
        # PATTERN: Tool-specific forms
        if selected_tool == "roll_dice":
            self._render_dice_form()
        elif selected_tool == "get_weather":
            self._render_weather_form()
        elif selected_tool == "get_date":
            self._render_date_form()
    
    def _render_dice_form(self):
        """Render dice rolling form"""
        with st.form("dice_form"):
            st.subheader("🎲 Roll Dice")
            
            notation = st.text_input(
                "Dice Notation",
                value="2d6",
                help="Enter dice notation (e.g., 2d6, 1d20, 3d10)"
            )
            
            # PATTERN: Help text with examples
            st.caption("Examples: 1d20 (single 20-sided die), 3d6 (three 6-sided dice)")
            
            submitted = st.form_submit_button("Roll Dice")
            
            if submitted:
                if self._validate_dice_notation(notation):
                    self._execute_tool("roll_dice", {"notation": notation})
                else:
                    st.error("Invalid dice notation. Use format like '2d6' or '1d20'")
    
    def _render_weather_form(self):
        """Render weather lookup form"""
        with st.form("weather_form"):
            st.subheader("🌤️ Get Weather")
            
            location = st.text_input(
                "Location",
                value="San Francisco",
                help="Enter city name or coordinates (lat,lon)"
            )
            
            # PATTERN: Common location examples
            st.caption("Examples: London, New York, 37.7749,-122.4194")
            
            submitted = st.form_submit_button("Get Weather")
            
            if submitted:
                if location.strip():
                    self._execute_tool("get_weather", {"location": location})
                else:
                    st.error("Please enter a location")
    
    def _render_date_form(self):
        """Render date/time lookup form"""
        with st.form("date_form"):
            st.subheader("🕐 Get Date & Time")
            
            timezone = st.selectbox(
                "Timezone",
                options=["UTC", "America/New_York", "America/Los_Angeles", "Europe/London", 
                        "Asia/Tokyo", "Australia/Sydney"],
                help="Select timezone or enter custom IANA timezone"
            )
            
            custom_timezone = st.text_input(
                "Custom Timezone (optional)",
                placeholder="e.g., America/Chicago",
                help="Enter custom IANA timezone identifier"
            )
            
            submitted = st.form_submit_button("Get Date & Time")
            
            if submitted:
                tz = custom_timezone.strip() if custom_timezone.strip() else timezone
                self._execute_tool("get_date", {"timezone": tz})
    
    def _execute_tool(self, tool_name: str, arguments: dict):
        """Execute tool and update GUI state"""
        if not st.session_state.mcp_client:
            st.error("Not connected to server")
            return
        
        try:
            with st.spinner(f"Executing {tool_name}..."):
                # CRITICAL: Time execution for performance metrics
                start_time = time.time()
                
                # PATTERN: Use existing MCP client
                result = asyncio.run(
                    st.session_state.mcp_client.invoke_tool(tool_name, arguments)
                )
                
                execution_time = time.time() - start_time
                
                # PATTERN: Create interaction record
                interaction = GUIInteraction(
                    tool_name=tool_name,
                    arguments=arguments,
                    request_payload={
                        "tool": tool_name,
                        "arguments": arguments
                    },
                    response_payload=result.model_dump(),
                    success=result.success,
                    error_message=result.error if not result.success else None,
                    execution_time=execution_time
                )
                
                # PATTERN: Update session state
                st.session_state.gui_session.interaction_history.append(interaction)
                
                # PATTERN: Display result
                if result.success:
                    st.success(f"✅ {tool_name} executed successfully!")
                    st.json(result.model_dump())
                else:
                    st.error(f"❌ {tool_name} failed: {result.error}")
                
                st.rerun()
                
        except Exception as e:
            st.error(f"Execution error: {str(e)}")
            st.exception(e)
    
    def _validate_dice_notation(self, notation: str) -> bool:
        """Validate dice notation format"""
        import re
        pattern = r"^(\d+)d(\d+)$"
        return bool(re.match(pattern, notation.strip().lower()))
```

### Integration Points

```yaml
DEPENDENCIES:
  - add to: pyproject.toml
  - packages: ["streamlit>=1.28.0"]
  - preserve: existing mcp, httpx, pydantic versions
  
MAIN_ENTRY:
  - modify: src/main.py
  - pattern: "async def main() -> None:"
  - add gui command alongside existing server/client commands
  
MAKEFILE:
  - add to: Makefile
  - command: "run_gui: uv run streamlit run src/gui/app.py"
  - integrate: GUI testing into existing test suite
  
TESTING:
  - add to: tests/test_gui.py
  - pattern: "pytest fixtures for GUI component testing"
  - mock: Streamlit interactions for unit tests
  - integration: GUI with MCP client functionality
```

## Validation Loop

### Level 1: Syntax & Style

```bash
# Run these FIRST - fix any errors before proceeding
uv run ruff check src/gui/ --fix
uv run mypy src/gui/
uv run ruff format src/gui/

# Expected: No errors. If errors exist, read and fix them.
```

### Level 2: Unit Tests

```python
# CREATE tests/test_gui.py
import pytest
import asyncio
from unittest.mock import Mock, patch
from src.gui.models.gui_models import GUISession, GUIInteraction
from src.gui.components.connection import ConnectionManager
from src.gui.utils.validation import validate_dice_notation

def test_gui_session_model():
    """Test GUI session model validation"""
    session = GUISession()
    assert not session.connected
    assert session.server_path == "src/mcp_server/server.py"
    assert len(session.interaction_history) == 0

def test_gui_interaction_model():
    """Test GUI interaction model"""
    interaction = GUIInteraction(
        tool_name="roll_dice",
        arguments={"notation": "2d6"},
        request_payload={"tool": "roll_dice", "arguments": {"notation": "2d6"}},
        response_payload={"success": True},
        success=True
    )
    assert interaction.tool_name == "roll_dice"
    assert interaction.success is True
    assert interaction.timestamp is not None

def test_dice_notation_validation():
    """Test dice notation validation"""
    assert validate_dice_notation("2d6") is True
    assert validate_dice_notation("1d20") is True
    assert validate_dice_notation("invalid") is False
    assert validate_dice_notation("2d") is False

@patch('src.gui.components.connection.MCPClient')
def test_connection_manager_connect(mock_client):
    """Test connection manager connection process"""
    mock_client_instance = Mock()
    mock_client_instance.available_tools = ["roll_dice", "get_weather"]
    mock_client.return_value = mock_client_instance
    
    # Test connection logic
    manager = ConnectionManager()
    # Mock Streamlit session state would go here
    # This would need to be adapted for actual Streamlit testing
    
def test_json_formatting():
    """Test JSON formatting utilities"""
    from src.gui.utils.formatting import format_json_for_display
    
    data = {"tool": "roll_dice", "result": {"values": [3, 5], "total": 8}}
    formatted = format_json_for_display(data)
    assert isinstance(formatted, str)
    assert "roll_dice" in formatted
```

```bash
# Run and iterate until passing:
uv run pytest tests/test_gui.py -v
# If failing: Read error, fix code, re-run
```

### Level 3: Integration Test

```bash
# Test Streamlit GUI manually
# 1. Start MCP server in background
uv run python -m src.mcp_server.server &

# 2. Launch Streamlit GUI
uv run streamlit run src/gui/app.py

# 3. Test in browser (http://localhost:8501)
# - Test connection to server
# - Test each tool form (roll_dice, get_weather, get_date)
# - Test error handling with invalid inputs
# - Test session history functionality
# - Test disconnection and reconnection

# 4. Test GUI via make command
make run_gui

# Expected: GUI loads successfully, all tools work, history is maintained
```

## Final Validation Checklist

- [ ] All tests pass: `uv run pytest tests/ -v`
- [ ] No linting errors: `uv run ruff check src/`
- [ ] No type errors: `uv run mypy src/`
- [ ] Streamlit GUI launches successfully via `make run_gui`
- [ ] Connection to MCP server works through GUI
- [ ] All three tools can be invoked through forms
- [ ] Request/response payloads are displayed properly
- [ ] Error handling shows user-friendly messages
- [ ] Session history tracks all interactions
- [ ] Connection status updates in real-time
- [ ] Input validation prevents invalid submissions
- [ ] JSON formatting is readable and highlighted
- [ ] GUI is responsive and user-friendly
- [ ] Example interaction files are created and valid

## Anti-Patterns to Avoid

- ❌ Don't use synchronous functions in Streamlit async context
- ❌ Don't forget to use st.session_state for persistent data
- ❌ Don't ignore Streamlit's rerun behavior - handle state carefully
- ❌ Don't hardcode server paths or tool configurations
- ❌ Don't skip input validation in forms
- ❌ Don't expose raw error messages to users - provide friendly alternatives
- ❌ Don't forget to handle connection lifecycle properly
- ❌ Don't use blocking operations without spinner feedback
- ❌ Don't ignore JSON formatting for request/response display
- ❌ Don't skip session history management

---

## Quality Score: 9/10

This PRP provides comprehensive context for one-pass implementation:

- ✅ Complete Streamlit documentation and GUI patterns
- ✅ Detailed existing MCP client/server implementation context
- ✅ Specific GUI interface requirements and user experience design
- ✅ Executable validation commands and testing approach
- ✅ Clear task breakdown with pseudocode and implementation details
- ✅ Anti-patterns and common pitfalls for Streamlit development
- ✅ Integration points with existing codebase clearly defined
- ✅ Session state management and async operation handling
- ✅ Comprehensive error handling and user feedback patterns

**Areas for improvement:**

- Could include more specific Streamlit testing patterns
- Could provide more detailed responsive design considerations

**Confidence Level:** Very High - This PRP contains comprehensive technical detail about Streamlit development, complete integration context with existing MCP implementation, and clear validation steps for successful GUI implementation by an AI agent with access to the codebase and web search capabilities.
