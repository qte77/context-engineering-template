"""Tests for the weather tool."""

from unittest.mock import AsyncMock, patch

import httpx
import pytest

from src.mcp_server.tools.base import (
    ExternalServiceError,
    ToolError,
)
from src.mcp_server.tools.weather import WeatherTool
from tests.fixtures.mcp_messages import WeatherAPIFixtures


class TestWeatherTool:
    """Test suite for WeatherTool."""

    @pytest.fixture
    def weather_tool(self):
        """Create a WeatherTool instance for testing."""
        return WeatherTool()

    @pytest.fixture
    def mock_http_client(self):
        """Create a mock HTTP client."""
        client = AsyncMock()
        return client

    def test_parse_location_known_city(self, weather_tool):
        """Test parsing known city names."""
        lat, lon = weather_tool.parse_location("San Francisco")
        assert lat == 37.7749
        assert lon == -122.4194

        lat, lon = weather_tool.parse_location("new york")
        assert lat == 40.7128
        assert lon == -74.0060

    def test_parse_location_coordinates(self, weather_tool):
        """Test parsing coordinate strings."""
        lat, lon = weather_tool.parse_location("37.7749,-122.4194")
        assert lat == 37.7749
        assert lon == -122.4194

        lat, lon = weather_tool.parse_location("51.5074, -0.1278")
        assert lat == 51.5074
        assert lon == -0.1278

    def test_parse_location_invalid(self, weather_tool):
        """Test parsing invalid locations raises ToolError."""
        with pytest.raises(ToolError) as exc_info:
            weather_tool.parse_location("Unknown City")

        assert "Unknown location" in str(exc_info.value)

    def test_parse_location_invalid_coordinates(self, weather_tool):
        """Test parsing invalid coordinates raises ToolError."""
        with pytest.raises(ToolError):
            weather_tool.parse_location("abc,def")

        with pytest.raises(ToolError):
            weather_tool.parse_location("200,300")  # Out of range

    def test_weather_code_to_text(self, weather_tool):
        """Test weather code conversion."""
        assert weather_tool.weather_code_to_text(0) == "Clear sky"
        assert weather_tool.weather_code_to_text(61) == "Slight rain"
        assert weather_tool.weather_code_to_text(95) == "Thunderstorm"
        assert "Unknown weather condition" in weather_tool.weather_code_to_text(999)

    @pytest.mark.asyncio
    async def test_execute_success_known_city(self, weather_tool, mock_http_client):
        """Test successful weather retrieval for known city."""
        # Mock the API response
        mock_response = WeatherAPIFixtures.current_weather_response(
            temperature=18.5, weather_code=2, wind_speed=12.3, humidity=65.0
        )

        with patch.object(weather_tool, "make_request", return_value=mock_response):
            result = await weather_tool.execute(location="San Francisco")

            assert result.location == "San Francisco"
            assert result.temperature == 18.5
            assert result.condition == "Partly cloudy"
            assert result.wind_speed == 12.3
            assert result.humidity == 65.0

    @pytest.mark.asyncio
    async def test_execute_success_coordinates(self, weather_tool):
        """Test successful weather retrieval using coordinates."""
        mock_response = WeatherAPIFixtures.current_weather_response()

        with patch.object(weather_tool, "make_request", return_value=mock_response):
            result = await weather_tool.execute(location="37.7749,-122.4194")

            assert result.location == "37.7749,-122.4194"
            assert result.temperature == 20.0
            assert result.condition == "Clear sky"

    @pytest.mark.asyncio
    async def test_execute_invalid_location(self, weather_tool):
        """Test execution with invalid location."""
        with pytest.raises(ToolError) as exc_info:
            await weather_tool.execute(location="Unknown City")

        assert "Unknown location" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_execute_empty_location(self, weather_tool):
        """Test execution with empty location."""
        with pytest.raises(ToolError) as exc_info:
            await weather_tool.execute(location="")

        assert "Missing required parameter" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_execute_api_timeout(self, weather_tool):
        """Test handling of API timeout."""
        with patch.object(
            weather_tool, "make_request", side_effect=httpx.TimeoutException("Timeout")
        ):
            with pytest.raises(ExternalServiceError) as exc_info:
                await weather_tool.execute(location="San Francisco")

            assert "timeout" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_execute_api_http_error(self, weather_tool):
        """Test handling of HTTP errors."""
        error = httpx.HTTPStatusError(
            "500 Server Error",
            request=httpx.Request("GET", "http://test"),
            response=httpx.Response(500, text="Server Error"),
        )

        with patch.object(weather_tool, "make_request", side_effect=error):
            with pytest.raises(ExternalServiceError) as exc_info:
                await weather_tool.execute(location="San Francisco")

            assert "500" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_execute_incomplete_data(self, weather_tool):
        """Test handling of incomplete API data."""
        incomplete_response = {"current": {"time": "2025-07-07T14:30:00Z"}}

        with patch.object(
            weather_tool, "make_request", return_value=incomplete_response
        ):
            with pytest.raises(ExternalServiceError) as exc_info:
                await weather_tool.execute(location="San Francisco")

            assert "Incomplete weather data" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_execute_no_current_data(self, weather_tool):
        """Test handling of missing current weather data."""
        no_current_response = {"forecast": {}}

        with patch.object(
            weather_tool, "make_request", return_value=no_current_response
        ):
            with pytest.raises(ExternalServiceError) as exc_info:
                await weather_tool.execute(location="San Francisco")

            assert "No current weather data" in str(exc_info.value)

    def test_format_result(self, weather_tool):
        """Test formatting weather result for display."""
        from src.mcp_server.models import WeatherResponse

        response = WeatherResponse(
            location="San Francisco",
            temperature=18.5,
            condition="Partly cloudy",
            wind_speed=12.3,
            humidity=65.0,
            timestamp="2025-07-07T14:30:00Z",
        )

        formatted = weather_tool.format_result(response)

        assert "🌤️" in formatted
        assert "San Francisco" in formatted
        assert "18.5°C" in formatted
        assert "Partly cloudy" in formatted
        assert "12.3 km/h" in formatted
        assert "65.0%" in formatted

    def test_format_result_no_humidity(self, weather_tool):
        """Test formatting weather result without humidity."""
        from src.mcp_server.models import WeatherResponse

        response = WeatherResponse(
            location="Test City",
            temperature=20.0,
            condition="Clear sky",
            wind_speed=10.0,
            humidity=None,
            timestamp=None,
        )

        formatted = weather_tool.format_result(response)

        assert "🌤️" in formatted
        assert "Test City" in formatted
        assert "20.0°C" in formatted
        assert "💧" not in formatted  # Humidity should not appear

    @pytest.mark.asyncio
    async def test_safe_execute_success(self, weather_tool):
        """Test safe_execute returns proper success format."""
        mock_response = WeatherAPIFixtures.current_weather_response()

        with patch.object(weather_tool, "make_request", return_value=mock_response):
            result = await weather_tool.safe_execute(location="San Francisco")

            assert "content" in result
            assert "isError" in result
            assert result["isError"] is False
            assert len(result["content"]) == 1
            assert result["content"][0]["type"] == "text"
            assert "🌤️" in result["content"][0]["text"]

    @pytest.mark.asyncio
    async def test_safe_execute_error(self, weather_tool):
        """Test safe_execute returns proper error format."""
        result = await weather_tool.safe_execute(location="Unknown City")

        assert "content" in result
        assert "isError" in result
        assert result["isError"] is True
        assert len(result["content"]) == 1
        assert result["content"][0]["type"] == "text"
        assert "Unknown location" in result["content"][0]["text"]

    @pytest.mark.asyncio
    async def test_cleanup(self, weather_tool):
        """Test cleanup method closes HTTP client."""
        # Mock the HTTP client
        mock_client = AsyncMock()
        weather_tool._http_client = mock_client

        await weather_tool.cleanup()

        mock_client.aclose.assert_called_once()
        assert weather_tool._http_client is None
