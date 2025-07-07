"""MCP server implementation with dice, weather, and date/time tools."""

import logging
from typing import Any

from mcp.server.fastmcp import FastMCP

from .tools.date_time import DateTimeTool
from .tools.dice import DiceRollTool
from .tools.weather import WeatherTool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server instance
mcp = FastMCP("dice-weather-datetime-server")

# Initialize tool instances
dice_tool = DiceRollTool()
weather_tool = WeatherTool()
datetime_tool = DateTimeTool()


@mcp.tool()
async def roll_dice(notation: str) -> dict[str, Any]:
    """Roll dice using standard notation like '2d6' or '1d20'.

    Args:
        notation: Dice notation (e.g., "2d6", "1d20", "3d10")

    Returns:
        Dict containing dice roll results, total, and formatted display
    """
    logger.info(f"Tool call: roll_dice(notation='{notation}')")
    return await dice_tool.safe_execute(notation=notation)


@mcp.tool()
async def get_weather(location: str) -> dict[str, Any]:
    """Get current weather conditions for a location.

    Args:
        location: City name or coordinates (lat,lon)

    Returns:
        Dict containing weather data including temperature, condition, and wind speed
    """
    logger.info(f"Tool call: get_weather(location='{location}')")
    return await weather_tool.safe_execute(location=location)


@mcp.tool()
async def get_date(timezone: str = "UTC") -> dict[str, Any]:
    """Get current date and time for a specific timezone.

    Args:
        timezone: Timezone identifier (e.g., "UTC", "America/New_York") or alias

    Returns:
        Dict containing current date/time in ISO 8601 format with timezone info
    """
    logger.info(f"Tool call: get_date(timezone='{timezone}')")
    return await datetime_tool.safe_execute(timezone=timezone)


@mcp.resource("mcp://tools/help")
async def get_help() -> str:
    """Get help information about available tools."""
    help_text = """
🎲 **MCP Server - Available Tools**

**roll_dice** - Roll dice using standard notation
- Usage: roll_dice(notation="2d6")
- Examples: "1d20", "3d6", "2d10"
- Returns individual values and total

**get_weather** - Get current weather conditions  
- Usage: get_weather(location="San Francisco")
- Supports city names or coordinates (lat,lon)
- Returns temperature, condition, wind speed

**get_date** - Get current date and time
- Usage: get_date(timezone="UTC")
- Supports IANA timezones and common aliases
- Returns ISO 8601 formatted datetime

**Examples:**
- roll_dice("2d6") → Roll two six-sided dice
- get_weather("London") → Weather for London
- get_date("America/New_York") → NYC current time
"""
    return help_text


async def cleanup_server():
    """Cleanup server resources."""
    logger.info("Cleaning up server resources...")
    try:
        await weather_tool.cleanup()
        logger.info("Server cleanup completed")
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")


# Server lifecycle management
async def startup():
    """Server startup handler."""
    logger.info("MCP Server starting up...")
    logger.info("Tools available: roll_dice, get_weather, get_date")


async def shutdown():
    """Server shutdown handler."""
    logger.info("MCP Server shutting down...")
    await cleanup_server()


def run_server():
    """Run the MCP server."""
    try:
        logger.info("Starting MCP server...")
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise


if __name__ == "__main__":
    run_server()