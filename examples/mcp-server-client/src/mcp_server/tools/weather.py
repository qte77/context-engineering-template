"""Weather tool for MCP server using Open-Meteo API."""

from datetime import datetime
from typing import Any

from ..models import WeatherRequest, WeatherResponse
from .base import AsyncHttpMixin, BaseTool, ExternalServiceError, ToolError


class WeatherTool(BaseTool, AsyncHttpMixin):
    """Tool for getting current weather data."""

    def __init__(self):
        super().__init__(
            name="get_weather",
            description="Get current weather conditions for a location",
        )
        self.api_base = "https://api.open-meteo.com/v1"

        # Basic city to coordinates mapping
        # In production, this would use a proper geocoding service
        self.city_coords = {
            "san francisco": (37.7749, -122.4194),
            "new york": (40.7128, -74.0060),
            "london": (51.5074, -0.1278),
            "paris": (48.8566, 2.3522),
            "tokyo": (35.6762, 139.6503),
            "sydney": (-33.8688, 151.2093),
            "los angeles": (34.0522, -118.2437),
            "chicago": (41.8781, -87.6298),
            "miami": (25.7617, -80.1918),
            "seattle": (47.6062, -122.3321),
            "vancouver": (49.2827, -123.1207),
            "toronto": (43.6532, -79.3832),
            "berlin": (52.5200, 13.4050),
            "rome": (41.9028, 12.4964),
            "madrid": (40.4168, -3.7038),
            "moscow": (55.7558, 37.6176),
            "beijing": (39.9042, 116.4074),
            "mumbai": (19.0760, 72.8777),
            "cairo": (30.0444, 31.2357),
            "lagos": (6.5244, 3.3792),
        }

        # Weather code to description mapping (subset of WMO codes)
        self.weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail",
        }

    def parse_location(self, location: str) -> tuple[float, float]:
        """Parse location string to get coordinates."""
        location_lower = location.lower().strip()

        # Check if it's in our city mapping
        if location_lower in self.city_coords:
            return self.city_coords[location_lower]

        # Try to parse as "lat,lon" coordinates
        try:
            parts = location.split(",")
            if len(parts) == 2:
                lat = float(parts[0].strip())
                lon = float(parts[1].strip())

                # Basic validation for reasonable coordinate ranges
                if -90 <= lat <= 90 and -180 <= lon <= 180:
                    return lat, lon
        except ValueError:
            pass

        # If we can't parse the location, raise an error
        available_cities = ", ".join(sorted(self.city_coords.keys()))
        raise ToolError(
            f"Unknown location: '{location}'. "
            f"Please use coordinates (lat,lon) or one of: {available_cities}"
        )

    def weather_code_to_text(self, code: int) -> str:
        """Convert weather code to readable description."""
        return self.weather_codes.get(code, f"Unknown weather condition (code: {code})")

    async def execute(self, **kwargs: Any) -> WeatherResponse:
        """Get weather data for the specified location."""
        location = kwargs.get("location")
        if not location:
            raise ToolError("Missing required parameter: location")

        # Validate input
        request = self.validate_input({"location": location}, WeatherRequest)

        # Parse location to coordinates
        lat, lon = self.parse_location(request.location)

        self.logger.info(f"Getting weather for {location} ({lat}, {lon})")

        # Make API request to Open-Meteo
        try:
            data = await self.make_request(
                method="GET",
                url=f"{self.api_base}/forecast",
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "current": (
                        "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
                    ),
                    "timezone": "auto",
                },
                timeout=15.0,
            )

            # Extract current weather data
            current = data.get("current", {})
            if not current:
                raise ExternalServiceError(
                    "No current weather data available",
                    service_name="Open-Meteo",
                )

            temperature = current.get("temperature_2m")
            humidity = current.get("relative_humidity_2m")
            weather_code = current.get("weather_code")
            wind_speed = current.get("wind_speed_10m")
            timestamp = current.get("time")

            if temperature is None or weather_code is None or wind_speed is None:
                raise ExternalServiceError(
                    "Incomplete weather data received",
                    service_name="Open-Meteo",
                )

            condition = self.weather_code_to_text(weather_code)

            self.logger.info(
                f"Weather data retrieved: {temperature}°C, {condition}, "
                f"{wind_speed} km/h wind"
            )

            return WeatherResponse(
                location=str(location),
                temperature=temperature,
                condition=condition,
                wind_speed=wind_speed,
                humidity=humidity,
                timestamp=timestamp,
            )

        except ExternalServiceError:
            raise
        except Exception as e:
            raise ExternalServiceError(
                f"Failed to retrieve weather data: {str(e)}",
                service_name="Open-Meteo",
            )

    def format_result(self, response: WeatherResponse) -> str:
        """Format weather data for display."""
        result = f"🌤️ **Weather for {response.location}**\n"
        result += f"🌡️ Temperature: **{response.temperature}°C**\n"
        result += f"☁️ Condition: **{response.condition}**\n"
        result += f"💨 Wind Speed: **{response.wind_speed} km/h**"

        if response.humidity is not None:
            result += f"\n💧 Humidity: **{response.humidity}%**"

        if response.timestamp:
            try:
                # Parse and format timestamp
                dt = datetime.fromisoformat(response.timestamp.replace("Z", "+00:00"))
                result += f"\n🕐 Updated: {dt.strftime('%Y-%m-%d %H:%M UTC')}"
            except ValueError:
                pass

        return result

    async def safe_execute(self, **kwargs) -> dict[str, Any]:
        """Execute weather lookup with formatted output."""
        try:
            result = await self.execute(**kwargs)
            formatted_result = self.format_result(result)

            return {
                "content": [
                    {
                        "type": "text",
                        "text": formatted_result,
                    }
                ],
                "isError": False,
            }
        except Exception as e:
            return self.create_error_response(e)
