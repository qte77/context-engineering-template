"""GUI-specific models for state management and type safety."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class GUIInteraction(BaseModel):
    """Single tool interaction record for GUI history."""

    timestamp: datetime = Field(default_factory=datetime.now)
    tool_name: str
    arguments: dict[str, Any]
    request_payload: dict[str, Any]
    response_payload: dict[str, Any]
    success: bool
    error_message: str | None = None
    execution_time: float | None = None


class GUISession(BaseModel):
    """GUI session state management."""

    connected: bool = False
    server_path: str = "src/mcp_server/server.py"
    available_tools: list[str] = Field(default_factory=list)
    interaction_history: list[GUIInteraction] = Field(default_factory=list)
    current_tool: str | None = None


class ConnectionStatus(BaseModel):
    """Connection status information."""

    connected: bool = False
    server_path: str
    last_health_check: datetime | None = None
    available_tools: list[str] = Field(default_factory=list)
    error_message: str | None = None
