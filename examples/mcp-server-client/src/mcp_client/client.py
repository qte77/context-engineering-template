"""Main MCP client class for tool invocation."""

import logging
from typing import Any

from .models.responses import ClientToolResult
from .transport import MCPTransport

# Configure logging
logger = logging.getLogger(__name__)


class MCPClient:
    """MCP client for connecting to servers and invoking tools."""

    def __init__(self, server_path: str):
        """Initialize MCP client.

        Args:
            server_path: Path to the MCP server script
        """
        self.server_path = server_path
        self.transport = MCPTransport(server_path)
        self._connected = False

    @property
    def connected(self) -> bool:
        """Check if client is connected to server."""
        return self._connected and self.transport.connected

    @property
    def available_tools(self) -> list[str]:
        """Get list of available tools."""
        return self.transport.available_tools

    async def connect(self) -> None:
        """Connect to MCP server.

        Raises:
            FileNotFoundError: If server script doesn't exist
            ConnectionError: If connection fails
            ValueError: If server script type is not supported
        """
        logger.info(f"Connecting to MCP server: {self.server_path}")

        try:
            await self.transport.connect()
            self._connected = True
            logger.info(
                f"Connected successfully. Available tools: {self.available_tools}"
            )
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            raise

    async def disconnect(self) -> None:
        """Disconnect from MCP server."""
        logger.info("Disconnecting from MCP server")
        await self.transport.disconnect()
        self._connected = False

    async def invoke_tool(
        self, tool_name: str, arguments: dict[str, Any]
    ) -> ClientToolResult:
        """Invoke a tool on the connected server.

        Args:
            tool_name: Name of the tool to invoke
            arguments: Arguments to pass to the tool

        Returns:
            ClientToolResult with success status and result or error
        """
        logger.info(f"Invoking tool: {tool_name} with arguments: {arguments}")

        # Check if connected
        if not self.connected:
            error_msg = "Not connected to server"
            logger.error(error_msg)
            return ClientToolResult(
                success=False,
                result=None,
                error=error_msg,
                tool_name=tool_name,
                arguments=arguments,
            )

        # Check if tool is available
        if tool_name not in self.available_tools:
            error_msg = (
                f"Tool '{tool_name}' not available. "
                f"Available tools: {self.available_tools}"
            )
            logger.error(error_msg)
            return ClientToolResult(
                success=False,
                result=None,
                error=error_msg,
                tool_name=tool_name,
                arguments=arguments,
            )

        try:
            # Call the tool through transport
            result = await self.transport.call_tool(tool_name, arguments)

            # Process the result
            logger.info(f"Tool '{tool_name}' executed successfully")
            return ClientToolResult(
                success=True,
                result=result,
                error=None,
                tool_name=tool_name,
                arguments=arguments,
            )

        except Exception as e:
            error_msg = f"Tool execution failed: {str(e)}"
            logger.error(error_msg)
            return ClientToolResult(
                success=False,
                result=None,
                error=error_msg,
                tool_name=tool_name,
                arguments=arguments,
            )

    async def health_check(self) -> bool:
        """Check if connection is healthy.

        Returns:
            True if connection is healthy, False otherwise
        """
        if not self.connected:
            return False

        return await self.transport.health_check()

    async def __aenter__(self) -> "MCPClient":
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.disconnect()


class MCPClientError(Exception):
    """Base exception for MCP client errors."""

    pass


class MCPConnectionError(MCPClientError):
    """Raised when connection to MCP server fails."""

    pass


class MCPToolError(MCPClientError):
    """Raised when tool execution fails."""

    pass
