"""Tests for the date/time tool."""

import pytest
import zoneinfo
from datetime import datetime, timezone
from unittest.mock import patch

from src.mcp_server.tools.date_time import DateTimeTool
from src.mcp_server.tools.base import ValidationToolError, ToolError


class TestDateTimeTool:
    """Test suite for DateTimeTool."""

    @pytest.fixture
    def datetime_tool(self):
        """Create a DateTimeTool instance for testing."""
        return DateTimeTool()

    def test_parse_timezone_utc(self, datetime_tool):
        """Test parsing UTC timezone."""
        tz = datetime_tool.parse_timezone("UTC")
        assert tz == timezone.utc

        tz = datetime_tool.parse_timezone("utc")
        assert tz == timezone.utc

        tz = datetime_tool.parse_timezone("GMT")
        assert tz == timezone.utc

    def test_parse_timezone_iana(self, datetime_tool):
        """Test parsing IANA timezone names."""
        tz = datetime_tool.parse_timezone("America/New_York")
        assert isinstance(tz, zoneinfo.ZoneInfo)
        assert str(tz) == "America/New_York"

        tz = datetime_tool.parse_timezone("Europe/London")
        assert isinstance(tz, zoneinfo.ZoneInfo)
        assert str(tz) == "Europe/London"

    def test_parse_timezone_aliases(self, datetime_tool):
        """Test parsing timezone aliases."""
        tz = datetime_tool.parse_timezone("est")
        assert isinstance(tz, zoneinfo.ZoneInfo)
        assert str(tz) == "America/New_York"

        tz = datetime_tool.parse_timezone("pst")
        assert isinstance(tz, zoneinfo.ZoneInfo)
        assert str(tz) == "America/Los_Angeles"

    def test_parse_timezone_invalid(self, datetime_tool):
        """Test parsing invalid timezone raises ToolError."""
        with pytest.raises(ToolError) as exc_info:
            datetime_tool.parse_timezone("Invalid/Timezone")

        assert "Invalid timezone" in str(exc_info.value)
        assert "Invalid/Timezone" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_execute_utc(self, datetime_tool):
        """Test execution with UTC timezone."""
        with patch('src.mcp_server.tools.date_time.datetime') as mock_datetime:
            mock_now = datetime(2025, 7, 7, 14, 30, 25, tzinfo=timezone.utc)
            mock_datetime.now.return_value = mock_now
            mock_datetime.fromisoformat = datetime.fromisoformat

            result = await datetime_tool.execute(timezone="UTC")

            assert result.timezone == "UTC"
            assert result.datetime == "2025-07-07T14:30:25+00:00"
            assert isinstance(result.timestamp, float)

    @pytest.mark.asyncio
    async def test_execute_iana_timezone(self, datetime_tool):
        """Test execution with IANA timezone."""
        with patch('src.mcp_server.tools.date_time.datetime') as mock_datetime:
            ny_tz = zoneinfo.ZoneInfo("America/New_York")
            mock_now = datetime(2025, 7, 7, 10, 30, 25, tzinfo=ny_tz)
            mock_datetime.now.return_value = mock_now
            mock_datetime.fromisoformat = datetime.fromisoformat

            result = await datetime_tool.execute(timezone="America/New_York")

            assert result.timezone == "America/New_York"
            assert "2025-07-07T10:30:25" in result.datetime
            assert isinstance(result.timestamp, float)

    @pytest.mark.asyncio
    async def test_execute_alias(self, datetime_tool):
        """Test execution with timezone alias."""
        with patch('src.mcp_server.tools.date_time.datetime') as mock_datetime:
            ny_tz = zoneinfo.ZoneInfo("America/New_York")
            mock_now = datetime(2025, 7, 7, 10, 30, 25, tzinfo=ny_tz)
            mock_datetime.now.return_value = mock_now
            mock_datetime.fromisoformat = datetime.fromisoformat

            result = await datetime_tool.execute(timezone="est")

            assert result.timezone == "America/New_York"
            assert isinstance(result.timestamp, float)

    @pytest.mark.asyncio
    async def test_execute_default_timezone(self, datetime_tool):
        """Test execution with default timezone (UTC)."""
        with patch('src.mcp_server.tools.date_time.datetime') as mock_datetime:
            mock_now = datetime(2025, 7, 7, 14, 30, 25, tzinfo=timezone.utc)
            mock_datetime.now.return_value = mock_now
            mock_datetime.fromisoformat = datetime.fromisoformat

            result = await datetime_tool.execute()  # No timezone argument

            assert result.timezone == "UTC"
            assert "2025-07-07T14:30:25" in result.datetime

    @pytest.mark.asyncio
    async def test_execute_invalid_timezone(self, datetime_tool):
        """Test execution with invalid timezone."""
        with pytest.raises(ToolError) as exc_info:
            await datetime_tool.execute(timezone="Invalid/Timezone")

        assert "Invalid timezone" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_execute_empty_timezone(self, datetime_tool):
        """Test execution with empty timezone."""
        with pytest.raises(ValidationToolError) as exc_info:
            await datetime_tool.execute(timezone="")

        assert "Timezone cannot be empty" in str(exc_info.value)

    def test_format_result(self, datetime_tool):
        """Test formatting date/time result for display."""
        from src.mcp_server.models import DateTimeResponse

        response = DateTimeResponse(
            datetime="2025-07-07T14:30:25+00:00",
            timezone="UTC",
            timestamp=1720360225.0
        )

        formatted = datetime_tool.format_result(response)

        assert "🕐" in formatted
        assert "2025-07-07" in formatted
        assert "14:30:25" in formatted
        assert "UTC" in formatted
        assert "2025-07-07T14:30:25+00:00" in formatted
        assert "1720360225" in formatted

    def test_format_result_weekday(self, datetime_tool):
        """Test formatting includes weekday information."""
        from src.mcp_server.models import DateTimeResponse

        # Monday
        response = DateTimeResponse(
            datetime="2025-07-07T14:30:25+00:00",
            timezone="UTC",
            timestamp=1720360225.0
        )

        formatted = datetime_tool.format_result(response)
        assert "Monday" in formatted

    def test_format_result_invalid_datetime(self, datetime_tool):
        """Test formatting with invalid datetime falls back gracefully."""
        from src.mcp_server.models import DateTimeResponse

        response = DateTimeResponse(
            datetime="invalid-datetime",
            timezone="UTC",
            timestamp=1720360225.0
        )

        formatted = datetime_tool.format_result(response)

        # Should still show the basic information
        assert "🕐" in formatted
        assert "UTC" in formatted
        assert "invalid-datetime" in formatted
        assert "1720360225" in formatted

    @pytest.mark.asyncio
    async def test_safe_execute_success(self, datetime_tool):
        """Test safe_execute returns proper success format."""
        with patch('src.mcp_server.tools.date_time.datetime') as mock_datetime:
            mock_now = datetime(2025, 7, 7, 14, 30, 25, tzinfo=timezone.utc)
            mock_datetime.now.return_value = mock_now
            mock_datetime.fromisoformat = datetime.fromisoformat

            result = await datetime_tool.safe_execute(timezone="UTC")

            assert "content" in result
            assert "isError" in result
            assert result["isError"] is False
            assert len(result["content"]) == 1
            assert result["content"][0]["type"] == "text"
            assert "🕐" in result["content"][0]["text"]

    @pytest.mark.asyncio
    async def test_safe_execute_error(self, datetime_tool):
        """Test safe_execute returns proper error format."""
        result = await datetime_tool.safe_execute(timezone="Invalid/Timezone")

        assert "content" in result
        assert "isError" in result
        assert result["isError"] is True
        assert len(result["content"]) == 1
        assert result["content"][0]["type"] == "text"
        assert "Invalid timezone" in result["content"][0]["text"]

    def test_get_available_timezones(self, datetime_tool):
        """Test get_available_timezones returns a list."""
        timezones = datetime_tool.get_available_timezones()

        assert isinstance(timezones, list)
        assert "UTC" in timezones
        assert "America/New_York" in timezones
        assert "Europe/London" in timezones
        assert len(timezones) > 10

    @pytest.mark.asyncio
    async def test_timezone_case_insensitive(self, datetime_tool):
        """Test timezone aliases are case insensitive."""
        with patch('src.mcp_server.tools.date_time.datetime') as mock_datetime:
            ny_tz = zoneinfo.ZoneInfo("America/New_York")
            mock_now = datetime(2025, 7, 7, 10, 30, 25, tzinfo=ny_tz)
            mock_datetime.now.return_value = mock_now
            mock_datetime.fromisoformat = datetime.fromisoformat

            result1 = await datetime_tool.execute(timezone="EST")
            result2 = await datetime_tool.execute(timezone="est")

            assert result1.timezone == result2.timezone == "America/New_York"

    @pytest.mark.asyncio
    async def test_whitespace_handling(self, datetime_tool):
        """Test timezone input with whitespace is handled correctly."""
        with patch('src.mcp_server.tools.date_time.datetime') as mock_datetime:
            mock_now = datetime(2025, 7, 7, 14, 30, 25, tzinfo=timezone.utc)
            mock_datetime.now.return_value = mock_now
            mock_datetime.fromisoformat = datetime.fromisoformat

            result = await datetime_tool.execute(timezone="  UTC  ")

            assert result.timezone == "UTC"