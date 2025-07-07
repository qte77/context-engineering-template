"""Client-specific response models for MCP tool invocation."""

from typing import Any

from pydantic import BaseModel, Field


class MCPToolResponse(BaseModel):
    """Response from MCP tool execution."""

    content: list[dict[str, Any]] = Field(..., description="Response content")
    isError: bool = Field(False, description="Whether response indicates error")


class ClientToolResult(BaseModel):
    """Processed tool result for client consumption."""

    success: bool = Field(..., description="Whether tool execution was successful")
    result: Any | None = Field(None, description="Tool execution result")
    error: str | None = Field(None, description="Error message if execution failed")
    tool_name: str = Field(..., description="Name of the tool that was executed")
    arguments: dict[str, Any] = Field(..., description="Arguments passed to the tool")


class ClientSession(BaseModel):
    """Client session information."""

    server_path: str = Field(..., description="Path to the MCP server script")
    connected: bool = Field(False, description="Whether client is connected to server")
    available_tools: list[str] = Field(
        default_factory=list, description="List of available tools"
    )
