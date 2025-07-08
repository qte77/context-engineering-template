"""Tests for the MCP server integration."""

from unittest.mock import AsyncMock, patch

import pytest

from src.mcp_server.server import cleanup_server, datetime_tool, dice_tool, weather_tool
from tests.fixtures.mcp_messages import WeatherAPIFixtures


class TestMCPServerIntegration:
    """Test suite for MCP server integration."""

    @pytest.mark.asyncio
    async def test_dice_tool_integration(self):
        """Test dice tool integration through MCP server."""
        # Import the MCP tool function
        from src.mcp_server.server import roll_dice

        result = await roll_dice(notation="2d6")

        assert "content" in result
        assert "isError" in result
        assert result["isError"] is False
        assert "🎲" in result["content"][0]["text"]
        assert "2d6" in result["content"][0]["text"]

    @pytest.mark.asyncio
    async def test_weather_tool_integration(self):
        """Test weather tool integration through MCP server."""
        from src.mcp_server.server import get_weather

        mock_response = WeatherAPIFixtures.current_weather_response()

        with patch.object(weather_tool, "make_request", return_value=mock_response):
            result = await get_weather(location="San Francisco")

            assert "content" in result
            assert "isError" in result
            assert result["isError"] is False
            assert "🌤️" in result["content"][0]["text"]
            assert "San Francisco" in result["content"][0]["text"]

    @pytest.mark.asyncio
    async def test_datetime_tool_integration(self):
        """Test date/time tool integration through MCP server."""
        from src.mcp_server.server import get_date

        result = await get_date(timezone="UTC")

        assert "content" in result
        assert "isError" in result
        assert result["isError"] is False
        assert "🕐" in result["content"][0]["text"]
        assert "UTC" in result["content"][0]["text"]

    @pytest.mark.asyncio
    async def test_dice_tool_error_handling(self):
        """Test error handling in dice tool integration."""
        from src.mcp_server.server import roll_dice

        result = await roll_dice(notation="invalid")

        assert "content" in result
        assert "isError" in result
        assert result["isError"] is True
        assert "Invalid input" in result["content"][0]["text"]

    @pytest.mark.asyncio
    async def test_weather_tool_error_handling(self):
        """Test error handling in weather tool integration."""
        from src.mcp_server.server import get_weather

        result = await get_weather(location="Unknown City")

        assert "content" in result
        assert "isError" in result
        assert result["isError"] is True
        assert "Unknown location" in result["content"][0]["text"]

    @pytest.mark.asyncio
    async def test_datetime_tool_error_handling(self):
        """Test error handling in date/time tool integration."""
        from src.mcp_server.server import get_date

        result = await get_date(timezone="Invalid/Timezone")

        assert "content" in result
        assert "isError" in result
        assert result["isError"] is True
        assert "Invalid timezone" in result["content"][0]["text"]

    @pytest.mark.asyncio
    async def test_help_resource(self):
        """Test help resource is available."""
        from src.mcp_server.server import get_help

        help_text = await get_help()

        assert isinstance(help_text, str)
        assert "roll_dice" in help_text
        assert "get_weather" in help_text
        assert "get_date" in help_text
        assert "🎲" in help_text

    @pytest.mark.asyncio
    async def test_cleanup_server(self):
        """Test server cleanup functionality."""
        # Mock the weather tool's cleanup method
        weather_tool.cleanup = AsyncMock()

        await cleanup_server()

        weather_tool.cleanup.assert_called_once()

    @pytest.mark.asyncio
    async def test_cleanup_server_with_error(self):
        """Test server cleanup handles errors gracefully."""
        # Mock the weather tool's cleanup method to raise an error
        weather_tool.cleanup = AsyncMock(side_effect=Exception("Cleanup error"))

        # Should not raise an exception
        await cleanup_server()

        weather_tool.cleanup.assert_called_once()

    def test_tool_instances_exist(self):
        """Test that tool instances are properly created."""
        assert dice_tool is not None
        assert weather_tool is not None
        assert datetime_tool is not None

        assert dice_tool.name == "roll_dice"
        assert weather_tool.name == "get_weather"
        assert datetime_tool.name == "get_date"

    @pytest.mark.asyncio
    async def test_mcp_tool_docstrings(self):
        """Test that MCP tool functions have proper docstrings."""
        from src.mcp_server.server import get_date, get_weather, roll_dice

        assert roll_dice.__doc__ is not None
        assert "dice" in roll_dice.__doc__.lower()
        assert "notation" in roll_dice.__doc__.lower()

        assert get_weather.__doc__ is not None
        assert "weather" in get_weather.__doc__.lower()
        assert "location" in get_weather.__doc__.lower()

        assert get_date.__doc__ is not None
        assert "date" in get_date.__doc__.lower()
        assert "timezone" in get_date.__doc__.lower()

    @pytest.mark.asyncio
    async def test_all_tools_return_proper_format(self):
        """Test that all tools return the expected MCP response format."""
        from src.mcp_server.server import get_date, roll_dice

        # Test dice tool
        dice_result = await roll_dice(notation="1d6")
        assert "content" in dice_result
        assert "isError" in dice_result
        assert isinstance(dice_result["content"], list)
        assert len(dice_result["content"]) == 1
        assert "type" in dice_result["content"][0]
        assert "text" in dice_result["content"][0]

        # Test date tool
        date_result = await get_date(timezone="UTC")
        assert "content" in date_result
        assert "isError" in date_result
        assert isinstance(date_result["content"], list)
        assert len(date_result["content"]) == 1
        assert "type" in date_result["content"][0]
        assert "text" in date_result["content"][0]

    @pytest.mark.asyncio
    async def test_weather_tool_with_coordinates(self):
        """Test weather tool with coordinate input."""
        from src.mcp_server.server import get_weather

        mock_response = WeatherAPIFixtures.current_weather_response()

        with patch.object(weather_tool, "make_request", return_value=mock_response):
            result = await get_weather(location="37.7749,-122.4194")

            assert "content" in result
            assert "isError" in result
            assert result["isError"] is False
            assert "37.7749,-122.4194" in result["content"][0]["text"]
