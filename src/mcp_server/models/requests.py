"""Pydantic models for MCP server request/response validation."""

import re
from typing import Any

from pydantic import BaseModel, Field, field_validator


class MCPRequest(BaseModel):
    """Base MCP request structure following JSON-RPC 2.0 format."""

    jsonrpc: str = "2.0"
    method: str
    params: dict | None = None
    id: str | int | None = None


class MCPResponse(BaseModel):
    """Base MCP response structure following JSON-RPC 2.0 format."""

    jsonrpc: str = "2.0"
    id: str | int | None = None
    result: Any | None = None
    error: dict | None = None


class MCPError(BaseModel):
    """MCP error structure."""

    code: int
    message: str
    data: dict | None = None


class DiceRollRequest(BaseModel):
    """Dice roll tool request with notation validation."""

    notation: str = Field(..., description="Dice notation like '2d6' or '1d20'")

    @field_validator("notation")
    @classmethod
    def validate_notation(cls, v: str) -> str:
        """Validate dice notation format."""
        if not isinstance(v, str):
            raise ValueError("Notation must be a string")

        # Remove spaces and convert to lowercase
        notation = v.strip().lower()

        # Validate format using regex
        pattern = re.compile(r"^(\d+)d(\d+)$")
        match = pattern.match(notation)

        if not match:
            raise ValueError(
                f"Invalid dice notation: '{v}'. "
                f"Expected format: 'XdY' (e.g., '2d6', '1d20')"
            )

        dice_count = int(match.group(1))
        sides = int(match.group(2))

        # Validate reasonable limits
        if dice_count <= 0:
            raise ValueError("Dice count must be greater than 0")
        if dice_count > 100:
            raise ValueError("Dice count must not exceed 100")

        if sides <= 0:
            raise ValueError("Number of sides must be greater than 0")
        if sides > 1000:
            raise ValueError("Number of sides must not exceed 1000")

        return notation


class DiceRollResponse(BaseModel):
    """Dice roll tool response."""

    values: list[int] = Field(..., description="Individual dice roll results")
    total: int = Field(..., description="Sum of all dice rolls")
    notation: str = Field(..., description="Original dice notation")


class WeatherRequest(BaseModel):
    """Weather tool request with location validation."""

    location: str = Field(..., description="City name or coordinates (lat,lon)")

    @field_validator("location")
    @classmethod
    def validate_location(cls, v: str) -> str:
        """Validate location format."""
        if not isinstance(v, str):
            raise ValueError("Location must be a string")

        location = v.strip()
        if not location:
            raise ValueError("Location cannot be empty")

        return location


class WeatherResponse(BaseModel):
    """Weather tool response."""

    location: str = Field(..., description="Requested location")
    temperature: float = Field(..., description="Temperature in Celsius")
    condition: str = Field(..., description="Weather condition description")
    wind_speed: float = Field(..., description="Wind speed in km/h")
    humidity: float | None = Field(None, description="Humidity percentage")
    timestamp: str | None = Field(None, description="Data timestamp")


class DateTimeRequest(BaseModel):
    """Date/time tool request with timezone validation."""

    timezone: str = Field(
        "UTC", description="Timezone identifier (e.g., 'UTC', 'America/New_York')"
    )

    @field_validator("timezone")
    @classmethod
    def validate_timezone(cls, v: str) -> str:
        """Validate timezone format."""
        if not isinstance(v, str):
            raise ValueError("Timezone must be a string")

        timezone = v.strip()
        if not timezone:
            raise ValueError("Timezone cannot be empty")

        return timezone


class DateTimeResponse(BaseModel):
    """Date/time tool response."""

    datetime: str = Field(..., description="ISO 8601 formatted date/time")
    timezone: str = Field(..., description="Timezone identifier")
    timestamp: float = Field(..., description="Unix timestamp")


class ToolCallRequest(BaseModel):
    """Generic tool call request."""

    name: str = Field(..., description="Tool name")
    arguments: dict = Field(..., description="Tool arguments")


class ToolCallResponse(BaseModel):
    """Generic tool call response."""

    content: list[dict] = Field(..., description="Tool response content")
    isError: bool = Field(False, description="Whether this is an error response")