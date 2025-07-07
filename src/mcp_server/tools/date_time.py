"""Date and time tool for MCP server with timezone support."""

import zoneinfo
from datetime import UTC, datetime
from typing import Any

from ..models import DateTimeRequest, DateTimeResponse
from .base import BaseTool, ToolError


class DateTimeTool(BaseTool):
    """Tool for getting current date and time in various timezones."""

    def __init__(self):
        super().__init__(
            name="get_date",
            description="Get current date and time in ISO 8601 format for any timezone",
        )

        # Common timezone aliases for user convenience
        self.timezone_aliases = {
            "utc": "UTC",
            "gmt": "UTC",
            "est": "America/New_York",
            "pst": "America/Los_Angeles",
            "cst": "America/Chicago",
            "mst": "America/Denver",
            "edt": "America/New_York",
            "pdt": "America/Los_Angeles",
            "cdt": "America/Chicago",
            "mdt": "America/Denver",
            "bst": "Europe/London",
            "cet": "Europe/Paris",
            "jst": "Asia/Tokyo",
            "aest": "Australia/Sydney",
        }

    def parse_timezone(self, timezone_str: str) -> zoneinfo.ZoneInfo | type[UTC]:
        """Parse timezone string to ZoneInfo object."""
        # Normalize timezone string
        tz_lower = timezone_str.lower().strip()

        # Handle UTC as a special case
        if tz_lower in ("utc", "gmt"):
            return UTC

        # Check aliases
        if tz_lower in self.timezone_aliases:
            timezone_str = self.timezone_aliases[tz_lower]

        # Try to create ZoneInfo object
        try:
            if timezone_str.upper() == "UTC":
                return UTC
            else:
                return zoneinfo.ZoneInfo(timezone_str)
        except zoneinfo.ZoneInfoNotFoundError:
            # Provide helpful error message with suggestions
            common_timezones = [
                "UTC",
                "America/New_York",
                "America/Los_Angeles",
                "America/Chicago",
                "Europe/London",
                "Europe/Paris",
                "Asia/Tokyo",
                "Australia/Sydney",
            ]
            suggestions = ", ".join(common_timezones)
            aliases = ", ".join(self.timezone_aliases.keys())

            raise ToolError(
                f"Invalid timezone: '{timezone_str}'. "
                f"Common timezones: {suggestions}. "
                f"Aliases: {aliases}. "
                f"Use IANA timezone names (e.g., 'America/New_York') or aliases."
            )

    async def execute(self, **kwargs: Any) -> DateTimeResponse:
        """Get current date and time for the specified timezone."""
        timezone = kwargs.get("timezone", "UTC")

        # Validate input
        request = self.validate_input({"timezone": timezone}, DateTimeRequest)

        # Parse timezone
        tz = self.parse_timezone(request.timezone)

        self.logger.info(f"Getting current time for timezone: {timezone}")

        # Get current time in the specified timezone
        if isinstance(tz, zoneinfo.ZoneInfo):
            current_time = datetime.now(tz)
            tz_name = str(tz)
        else:  # UTC
            current_time = datetime.now(tz)
            tz_name = "UTC"

        # Format as ISO 8601
        iso_datetime = current_time.isoformat()

        # Get Unix timestamp
        timestamp = current_time.timestamp()

        self.logger.info(f"Current time in {tz_name}: {iso_datetime}")

        return DateTimeResponse(
            datetime=iso_datetime,
            timezone=tz_name,
            timestamp=timestamp,
        )

    def format_result(self, response: DateTimeResponse) -> str:
        """Format date/time data for display."""
        # Parse the ISO datetime to extract components
        try:
            dt = datetime.fromisoformat(response.datetime)
            date_part = dt.strftime("%Y-%m-%d")
            time_part = dt.strftime("%H:%M:%S")
            weekday = dt.strftime("%A")

            result = "🕐 **Current Date & Time**\n"
            result += f"📅 Date: **{date_part}** ({weekday})\n"
            result += f"⏰ Time: **{time_part}**\n"
            result += f"🌍 Timezone: **{response.timezone}**\n"
            result += f"📋 ISO 8601: `{response.datetime}`\n"
            result += f"🔢 Unix Timestamp: `{int(response.timestamp)}`"

            return result

        except ValueError:
            # Fallback if datetime parsing fails
            return (
                f"🕐 **Current Date & Time**\n"
                f"📋 ISO 8601: `{response.datetime}`\n"
                f"🌍 Timezone: **{response.timezone}**\n"
                f"🔢 Unix Timestamp: `{int(response.timestamp)}`"
            )

    async def safe_execute(self, **kwargs) -> dict[str, Any]:
        """Execute date/time lookup with formatted output."""
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

    def get_available_timezones(self) -> list[str]:
        """Get a list of common available timezones."""
        common_zones = [
            "UTC",
            "America/New_York",
            "America/Los_Angeles",
            "America/Chicago",
            "America/Denver",
            "America/Phoenix",
            "America/Anchorage",
            "America/Honolulu",
            "America/Toronto",
            "America/Vancouver",
            "Europe/London",
            "Europe/Paris",
            "Europe/Berlin",
            "Europe/Rome",
            "Europe/Madrid",
            "Europe/Amsterdam",
            "Europe/Stockholm",
            "Europe/Moscow",
            "Asia/Tokyo",
            "Asia/Shanghai",
            "Asia/Kolkata",
            "Asia/Dubai",
            "Asia/Singapore",
            "Australia/Sydney",
            "Australia/Melbourne",
            "Pacific/Auckland",
        ]
        return sorted(common_zones + list(self.timezone_aliases.values()))