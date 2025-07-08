"""Transport layer for MCP client connections."""

import os
from contextlib import AsyncExitStack
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPTransport:
    """Handles MCP server connections via stdio transport."""

    def __init__(self, server_path: str):
        """Initialize transport with server path.

        Args:
            server_path: Path to the MCP server script
        """
        self.server_path = server_path
        self.session: ClientSession | None = None
        self.exit_stack: AsyncExitStack | None = None
        self.connected = False
        self.available_tools: list[str] = []

    async def connect(self) -> None:
        """Connect to MCP server via stdio transport.

        Raises:
            FileNotFoundError: If server script doesn't exist
            ConnectionError: If connection fails
            ValueError: If server script type is not supported
        """
        # Validate server script exists
        if not os.path.exists(self.server_path):
            raise FileNotFoundError(f"Server script not found: {self.server_path}")

        # Determine server type and command
        if self.server_path.endswith(".py"):
            # Use uv run python for proper environment
            command = "uv"
            args = ["run", "python", self.server_path]
        elif self.server_path.endswith(".js"):
            command = "node"
            args = [self.server_path]
        else:
            raise ValueError(f"Unsupported server script type: {self.server_path}")

        # Create server parameters
        server_params = StdioServerParameters(command=command, args=args, env=None)

        try:
            # Setup resource management
            self.exit_stack = AsyncExitStack()

            # Connect to server
            read, write = await self.exit_stack.enter_async_context(
                stdio_client(server_params)
            )

            # Create session
            self.session = await self.exit_stack.enter_async_context(
                ClientSession(read, write)
            )

            # Initialize connection
            await self.session.initialize()

            # Discover available tools
            tools_response = await self.session.list_tools()
            self.available_tools = [tool.name for tool in tools_response.tools]

            self.connected = True

        except Exception as e:
            # Clean up on connection failure
            if self.exit_stack:
                await self.exit_stack.aclose()
                self.exit_stack = None
            raise ConnectionError(f"Failed to connect to server: {e}")

    async def disconnect(self) -> None:
        """Disconnect from MCP server."""
        if self.exit_stack:
            await self.exit_stack.aclose()
            self.exit_stack = None

        self.session = None
        self.connected = False
        self.available_tools = []

    async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        """Call a tool on the connected server.

        Args:
            tool_name: Name of the tool to call
            arguments: Arguments to pass to the tool

        Returns:
            Tool response content

        Raises:
            RuntimeError: If not connected to server
            ValueError: If tool is not available
        """
        if not self.connected or not self.session:
            raise RuntimeError("Not connected to server")

        if tool_name not in self.available_tools:
            raise ValueError(
                f"Tool '{tool_name}' not available. "
                f"Available tools: {self.available_tools}"
            )

        # Call the tool
        result = await self.session.call_tool(tool_name, arguments)
        return result

    async def health_check(self) -> bool:
        """Check if connection is healthy.

        Returns:
            True if connection is healthy, False otherwise
        """
        if not self.connected or not self.session:
            return False

        try:
            # Try to list tools as a health check
            await self.session.list_tools()
            return True
        except Exception:
            return False

    async def __aenter__(self) -> "MCPTransport":
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.disconnect()
