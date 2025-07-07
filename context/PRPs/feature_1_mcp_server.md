# MCP Server Implementation with Three Core Tools

## Purpose

Product Requirements Prompt (PRP) for implementing a complete MCP (Model Context Protocol) server in Python that exposes three callable tools: dice rolling, weather retrieval, and date/time services. This PRP provides comprehensive context for one-pass implementation success.

## Goal

Build a production-ready MCP server in Python that:
- Implements the MCP protocol for structured message handling
- Exposes three tools: `roll_dice`, `get_weather`, and `get_date`
- Provides robust error handling and input validation
- Follows the project's established patterns and conventions
- Is modular, testable, and extensible for future tools

## Why

- **Standardization**: Implements the emerging MCP protocol standard for AI tool integration
- **Modularity**: Creates a foundation for adding more tools in the future
- **User Value**: Provides practical utilities (dice, weather, time) accessible via structured protocol
- **Learning**: Demonstrates best practices for building MCP servers in Python

## What

### User-visible behavior
- Server accepts MCP protocol messages in JSON format
- Tools can be invoked via structured requests like `{"tool": "roll_dice", "args": {"notation": "3d6"}}`
- Returns structured responses with results or detailed error messages
- Handles malformed inputs gracefully with informative feedback

### Success Criteria

- [ ] MCP server starts and accepts connections via stdio transport
- [ ] All three tools (`roll_dice`, `get_weather`, `get_date`) work correctly
- [ ] Input validation prevents crashes and provides helpful error messages
- [ ] Weather API integration handles rate limits and failures gracefully
- [ ] Timezone support works correctly for date/time requests
- [ ] All code passes linting (ruff) and type checking (mypy)
- [ ] Comprehensive test coverage for all tools and edge cases
- [ ] Server follows project conventions and patterns

## All Needed Context

### Documentation & References

```yaml
# MUST READ - Include these in your context window
- url: https://github.com/modelcontextprotocol/python-sdk
  why: Official MCP Python SDK for protocol implementation
  
- url: https://github.com/jlowin/fastmcp
  why: FastMCP framework for simplified MCP server development
  
- url: https://open-meteo.com/en/docs
  why: Weather API documentation for get_weather tool
  section: Current weather conditions and forecast endpoints
  critical: No API key required for basic usage, supports lat/lon coordinates
  
- url: https://docs.python.org/3/library/datetime.html
  why: Timezone handling and ISO 8601 formatting for get_date tool
  section: timezone-aware datetime objects and isoformat()
  critical: Use timezone.utc for UTC times, avoid naive datetimes
  
- url: https://docs.python.org/3/library/random.html
  why: Random number generation for dice rolling
  section: randint() for generating dice values
  critical: Use random.randint(1, sides) for each die roll
  
- file: /workspaces/context-engineering-template/context/examples/features/feature_1_mcp_server.md
  why: Original feature requirements with examples and considerations
  
- file: /workspaces/context-engineering-template/pyproject.toml
  why: Project configuration, dependencies, and tool settings
  
- file: /workspaces/context-engineering-template/src/main.py
  why: Current main entry point pattern to follow
```

### Current Codebase tree

```bash
/workspaces/context-engineering-template
├── AGENTS.md
├── assets/
├── CHANGELOG.md
├── CLAUDE.md
├── context/
│   ├── examples/
│   │   └── features/
│   │       └── feature_1_mcp_server.md
│   └── templates/
├── docs/
├── LICENSE
├── Makefile
├── mkdocs.yaml
├── pyproject.toml
├── README.md
├── src/
│   ├── __init__.py
│   ├── main.py
│   └── py.typed
└── uv.lock
```

### Desired Codebase tree with files to be added

```bash
/workspaces/context-engineering-template
├── src/
│   ├── __init__.py
│   ├── main.py  # Modified to support MCP server
│   ├── py.typed
│   ├── mcp_server/
│   │   ├── __init__.py
│   │   ├── server.py           # Main MCP server implementation
│   │   ├── tools/
│   │   │   ├── __init__.py
│   │   │   ├── base.py         # Base tool interface
│   │   │   ├── dice.py         # Roll dice tool
│   │   │   ├── weather.py      # Weather API tool
│   │   │   └── date_time.py    # Date/time tool
│   │   └── models/
│   │       ├── __init__.py
│   │       └── requests.py     # Pydantic models for requests/responses
├── tests/
│   ├── __init__.py
│   ├── test_mcp_server.py
│   ├── test_tools/
│   │   ├── __init__.py
│   │   ├── test_dice.py
│   │   ├── test_weather.py
│   │   └── test_date_time.py
│   └── fixtures/
│       ├── __init__.py
│       └── mcp_messages.py     # Test message fixtures
├── context/
│   └── examples/
│       ├── roll_dice_example.json      # Example request/response
│       ├── get_weather_example.json    # Example request/response
│       └── get_date_example.json       # Example request/response
```

### Known Gotchas & Library Quirks

```python
# CRITICAL: MCP protocol requires specific message structure
# Must follow exact JSON-RPC 2.0 format with method/params/id fields

# CRITICAL: FastMCP requires async functions for tool definitions
# Example: 
@mcp.tool()
async def roll_dice(notation: str) -> dict:
    # Implementation

# CRITICAL: Open-Meteo API requires lat/lon coordinates, not city names
# Must use geocoding service or coordinate lookup for city names
# API endpoint: https://api.open-meteo.com/v1/forecast?latitude=X&longitude=Y

# CRITICAL: Python datetime timezone handling
# Always use timezone-aware datetime objects
# Use datetime.now(timezone.utc) for UTC times
# Use zoneinfo (Python 3.9+) or pytz for timezone conversions

# CRITICAL: Dice notation validation
# Valid formats: "1d6", "2d10", "3d20" (number + 'd' + sides)
# Invalid: "d6", "1x6", "0d6", "1d0", "abc"
# Must validate both dice count and sides > 0

# CRITICAL: Error handling should not expose internal details
# Return user-friendly error messages without stack traces
# Log detailed errors internally for debugging
```

## Implementation Blueprint

### Data models and structure

Create core data models for type safety and validation:

```python
# src/mcp_server/models/requests.py
from pydantic import BaseModel, Field, validator
from typing import Optional, Union, Any

class MCPRequest(BaseModel):
    """Base MCP request structure"""
    jsonrpc: str = "2.0"
    method: str
    params: Optional[dict] = None
    id: Optional[Union[str, int]] = None

class MCPResponse(BaseModel):
    """Base MCP response structure"""
    jsonrpc: str = "2.0"
    id: Optional[Union[str, int]] = None
    result: Optional[Any] = None
    error: Optional[dict] = None

class DiceRollRequest(BaseModel):
    """Dice roll tool request"""
    notation: str = Field(..., description="Dice notation like '2d6' or '1d20'")
    
    @validator('notation')
    def validate_notation(cls, v):
        # Validate dice notation format
        pass

class WeatherRequest(BaseModel):
    """Weather tool request"""
    location: str = Field(..., description="City name or coordinates")

class DateTimeRequest(BaseModel):
    """Date/time tool request"""
    timezone: Optional[str] = Field("UTC", description="Timezone identifier")
```

### List of tasks to be completed in order

```yaml
Task 1: Setup Dependencies
ADD to pyproject.toml:
  - fastmcp>=2.0.0 (or mcp package if using official SDK)
  - httpx (for weather API calls)
  - pydantic>=2.0.0 (for data validation)
  - python-dateutil (for timezone handling)

Task 2: Create Base Tool Interface
CREATE src/mcp_server/tools/base.py:
  - DEFINE abstract base class for all tools
  - ESTABLISH common interface for tool registration
  - INCLUDE error handling patterns

Task 3: Implement Dice Rolling Tool
CREATE src/mcp_server/tools/dice.py:
  - IMPLEMENT dice notation parsing (regex: r'(\d+)d(\d+)')
  - VALIDATE dice count > 0 and sides > 0
  - GENERATE random values using random.randint(1, sides)
  - RETURN structured result with individual values and total

Task 4: Implement Weather Tool
CREATE src/mcp_server/tools/weather.py:
  - IMPLEMENT city name to coordinates lookup (basic hardcoded mapping)
  - INTEGRATE with Open-Meteo API using httpx
  - HANDLE API failures and rate limits gracefully
  - RETURN structured weather data (temperature, condition, wind)

Task 5: Implement Date/Time Tool
CREATE src/mcp_server/tools/date_time.py:
  - IMPLEMENT timezone parsing using zoneinfo
  - GENERATE current datetime for requested timezone
  - FORMAT output as ISO 8601 string
  - HANDLE invalid timezone names gracefully

Task 6: Create MCP Server
CREATE src/mcp_server/server.py:
  - IMPLEMENT FastMCP server with tool registration
  - SETUP message routing and error handling
  - INTEGRATE all three tools with proper decorators
  - HANDLE protocol-level errors and validation

Task 7: Update Main Entry Point
MODIFY src/main.py:
  - IMPORT MCP server module
  - SETUP server initialization and startup
  - HANDLE graceful shutdown
  - PRESERVE existing async pattern

Task 8: Create Example Files
CREATE context/examples/*.json:
  - GENERATE realistic request/response examples
  - INCLUDE both success and error cases
  - FOLLOW exact JSON structure from feature requirements

Task 9: Implement Comprehensive Tests
CREATE tests/test_*.py:
  - UNIT tests for each tool with edge cases
  - INTEGRATION tests for MCP server
  - MOCK external API calls for weather tool
  - VALIDATE error handling and edge cases

Task 10: Final Integration and Validation
RUN validation commands:
  - EXECUTE make ruff (code formatting)
  - EXECUTE make type_check (mypy validation)
  - EXECUTE make test_all (pytest suite)
  - MANUAL test server startup and tool execution
```

### Per task pseudocode

```python
# Task 3: Dice Rolling Tool
class DiceRoller:
    def __init__(self):
        self.notation_pattern = re.compile(r'^(\d+)d(\d+)$')
    
    async def roll_dice(self, notation: str) -> dict:
        # PATTERN: Always validate input first
        match = self.notation_pattern.match(notation.lower())
        if not match:
            raise ValueError(f"Invalid dice notation: {notation}")
        
        dice_count, sides = int(match.group(1)), int(match.group(2))
        
        # GOTCHA: Validate reasonable limits
        if dice_count <= 0 or dice_count > 100:
            raise ValueError("Dice count must be 1-100")
        if sides <= 0 or sides > 1000:
            raise ValueError("Sides must be 1-1000")
        
        # PATTERN: Generate results
        values = [random.randint(1, sides) for _ in range(dice_count)]
        
        return {
            "values": values,
            "total": sum(values),
            "notation": notation
        }

# Task 4: Weather Tool
class WeatherTool:
    def __init__(self):
        self.api_base = "https://api.open-meteo.com/v1"
        self.city_coords = {
            "san francisco": (37.7749, -122.4194),
            "new york": (40.7128, -74.0060),
            # Add more as needed
        }
    
    async def get_weather(self, location: str) -> dict:
        # PATTERN: Input validation and preprocessing
        location_lower = location.lower()
        
        # GOTCHA: Handle coordinate lookup
        if location_lower in self.city_coords:
            lat, lon = self.city_coords[location_lower]
        else:
            # Try to parse as "lat,lon" format
            try:
                lat, lon = map(float, location.split(','))
            except ValueError:
                raise ValueError(f"Unknown location: {location}")
        
        # CRITICAL: API call with proper error handling
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.api_base}/forecast",
                    params={
                        "latitude": lat,
                        "longitude": lon,
                        "current": "temperature_2m,weather_code,wind_speed_10m"
                    },
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                
                return {
                    "location": location,
                    "temperature": data["current"]["temperature_2m"],
                    "condition": self._weather_code_to_text(data["current"]["weather_code"]),
                    "wind_speed": data["current"]["wind_speed_10m"]
                }
            except httpx.TimeoutException:
                raise Exception("Weather service timeout")
            except httpx.HTTPStatusError as e:
                raise Exception(f"Weather service error: {e.response.status_code}")

# Task 5: Date/Time Tool
class DateTimeTool:
    async def get_date(self, timezone: str = "UTC") -> str:
        # PATTERN: Timezone validation
        try:
            if timezone.upper() == "UTC":
                tz = timezone.utc
            else:
                tz = zoneinfo.ZoneInfo(timezone)
        except zoneinfo.ZoneInfoNotFoundError:
            raise ValueError(f"Invalid timezone: {timezone}")
        
        # PATTERN: Generate timezone-aware datetime
        current_time = datetime.now(tz)
        
        # CRITICAL: Return ISO 8601 format
        return current_time.isoformat()

# Task 6: MCP Server Integration
from fastmcp import FastMCP

mcp = FastMCP("dice-weather-datetime-server")

@mcp.tool()
async def roll_dice(notation: str) -> dict:
    """Roll dice using standard notation like '2d6' or '1d20'"""
    return await dice_tool.roll_dice(notation)

@mcp.tool()
async def get_weather(location: str) -> dict:
    """Get current weather for a location"""
    return await weather_tool.get_weather(location)

@mcp.tool()
async def get_date(timezone: str = "UTC") -> str:
    """Get current date and time for a timezone"""
    return await datetime_tool.get_date(timezone)
```

### Integration Points

```yaml
DEPENDENCIES:
  - add to: pyproject.toml
  - packages: ["fastmcp>=2.0.0", "httpx", "pydantic>=2.0.0", "python-dateutil"]
  
MAIN_ENTRY:
  - modify: src/main.py
  - pattern: "async def main() -> None:"
  - add server startup and stdio transport setup
  
TESTING:
  - add to: tests/
  - pattern: "pytest fixtures for mocking external APIs"
  - mock httpx responses for weather API
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
# CREATE test_dice.py
def test_roll_dice_valid_notation():
    """Test valid dice notation works"""
    result = await dice_tool.roll_dice("2d6")
    assert len(result["values"]) == 2
    assert all(1 <= v <= 6 for v in result["values"])
    assert result["total"] == sum(result["values"])

def test_roll_dice_invalid_notation():
    """Test invalid notation raises ValueError"""
    with pytest.raises(ValueError, match="Invalid dice notation"):
        await dice_tool.roll_dice("invalid")

def test_get_weather_known_city():
    """Test weather for known city"""
    with httpx_mock.HTTPXMock() as m:
        m.add_response(json={"current": {"temperature_2m": 20, "weather_code": 0, "wind_speed_10m": 5}})
        result = await weather_tool.get_weather("San Francisco")
        assert result["temperature"] == 20

def test_get_date_utc():
    """Test UTC date retrieval"""
    result = await datetime_tool.get_date("UTC")
    assert result.endswith("Z")  # UTC timezone indicator
```

```bash
# Run and iterate until passing:
uv run pytest tests/ -v
# If failing: Read error, fix code, re-run
```

### Level 3: Integration Test

```bash
# Test MCP server startup
uv run python -m src.main

# Test tool execution (manual verification)
# Send JSON-RPC message to stdin and verify response format
echo '{"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "roll_dice", "arguments": {"notation": "2d6"}}, "id": 1}' | uv run python -m src.main
```

## Final validation Checklist

- [ ] All tests pass: `uv run pytest tests/ -v`
- [ ] No linting errors: `uv run ruff check src/`
- [ ] No type errors: `uv run mypy src/`
- [ ] MCP server starts without errors
- [ ] All three tools respond correctly to valid inputs
- [ ] Invalid inputs return helpful error messages
- [ ] Weather API failures are handled gracefully
- [ ] Timezone handling works for common timezones
- [ ] Example JSON files are valid and match implementation

## Anti-Patterns to Avoid

- ❌ Don't use synchronous functions in async context
- ❌ Don't ignore MCP protocol message structure requirements
- ❌ Don't expose internal error details to users
- ❌ Don't hardcode API endpoints or configuration values
- ❌ Don't skip input validation because "it should work"
- ❌ Don't use naive datetime objects for timezone-aware operations
- ❌ Don't catch all exceptions - be specific about error handling
- ❌ Don't mock away all external dependencies in tests - verify integration points

---

## Quality Score: 8/10

This PRP provides comprehensive context for one-pass implementation:
- ✅ Complete MCP protocol documentation and examples
- ✅ Detailed implementation patterns and gotchas
- ✅ Specific API documentation and error handling strategies
- ✅ Executable validation commands and test patterns
- ✅ Clear task breakdown with pseudocode
- ✅ Anti-patterns and common pitfalls identified

**Areas for improvement:**
- Could include more city coordinate mappings for weather tool
- Could provide more specific timezone examples for testing

**Confidence Level:** High - This PRP contains sufficient technical detail and context for successful implementation by an AI agent with access to the codebase and web search capabilities.