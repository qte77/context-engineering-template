"""Test fixtures for MCP messages and responses."""

from typing import Any


class MCPMessageFixtures:
    """Collection of MCP message fixtures for testing."""

    @staticmethod
    def tool_call_request(
        tool_name: str, arguments: dict[str, Any], request_id: int = 1
    ) -> dict[str, Any]:
        """Create a standard MCP tool call request."""
        return {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments,
            },
            "id": request_id,
        }

    @staticmethod
    def success_response(content: Any, request_id: int = 1) -> dict[str, Any]:
        """Create a successful MCP response."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": content,
                    }
                ],
                "isError": False,
            },
        }

    @staticmethod
    def error_response(error_message: str, request_id: int = 1) -> dict[str, Any]:
        """Create an error MCP response."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": error_message,
                    }
                ],
                "isError": True,
            },
        }


class WeatherAPIFixtures:
    """Collection of weather API response fixtures."""

    @staticmethod
    def current_weather_response(
        temperature: float = 20.0,
        weather_code: int = 0,
        wind_speed: float = 10.0,
        humidity: float = 65.0,
    ) -> dict[str, Any]:
        """Create a mock Open-Meteo API response."""
        return {
            "current": {
                "time": "2025-07-07T14:30:00Z",
                "temperature_2m": temperature,
                "relative_humidity_2m": humidity,
                "weather_code": weather_code,
                "wind_speed_10m": wind_speed,
            },
            "current_units": {
                "time": "iso8601",
                "temperature_2m": "°C",
                "relative_humidity_2m": "%",
                "weather_code": "wmo code",
                "wind_speed_10m": "km/h",
            },
        }

    @staticmethod
    def api_error_response(status_code: int = 500) -> dict[str, Any]:
        """Create a mock API error response."""
        return {
            "error": True,
            "reason": "Internal server error" if status_code == 500 else "Bad request",
        }
