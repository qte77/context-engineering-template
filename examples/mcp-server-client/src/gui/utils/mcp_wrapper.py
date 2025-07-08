"""MCP client wrapper for Streamlit GUI with persistent connection."""

import asyncio
import logging
import threading
import time
from queue import Empty, Queue
from typing import Any

from src.mcp_client.client import MCPClient

logger = logging.getLogger(__name__)


class MCPConnectionManager:
    """Manages a persistent MCP connection in a background thread."""

    def __init__(self):
        self._client = None
        self._thread = None
        self._loop = None
        self._connected = False
        self._available_tools = []
        self._request_queue = Queue()
        self._response_queue = Queue()
        self._shutdown_event = threading.Event()

    def connect(self, server_path: str) -> bool:
        """Connect to MCP server in background thread."""
        if self._connected:
            self.disconnect()

        self._shutdown_event.clear()
        self._thread = threading.Thread(
            target=self._run_connection, args=(server_path,)
        )
        self._thread.daemon = True
        self._thread.start()

        # Wait for connection to establish (with timeout)
        start_time = time.time()
        while not self._connected and time.time() - start_time < 10:
            time.sleep(0.1)

        return self._connected

    def disconnect(self) -> None:
        """Disconnect from MCP server."""
        if self._thread and self._thread.is_alive():
            self._shutdown_event.set()
            # Send disconnect command
            self._request_queue.put({"action": "disconnect"})
            self._thread.join(timeout=5)

        self._connected = False
        self._available_tools = []

    def invoke_tool(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """Invoke a tool and return the result."""
        if not self._connected:
            return {
                "success": False,
                "error": "Not connected to server",
                "tool_name": tool_name,
                "arguments": arguments,
            }

        # Send request
        request_id = f"{tool_name}_{time.time()}"
        self._request_queue.put(
            {
                "action": "invoke_tool",
                "id": request_id,
                "tool_name": tool_name,
                "arguments": arguments,
            }
        )

        # Wait for response (with timeout)
        start_time = time.time()
        while time.time() - start_time < 30:  # 30 second timeout
            try:
                response = self._response_queue.get(timeout=1)
                if response.get("id") == request_id:
                    return response.get(
                        "result",
                        {
                            "success": False,
                            "error": "No result in response",
                            "tool_name": tool_name,
                            "arguments": arguments,
                        },
                    )
            except Empty:
                continue

        return {
            "success": False,
            "error": "Request timeout",
            "tool_name": tool_name,
            "arguments": arguments,
        }

    def health_check(self) -> bool:
        """Check if connection is healthy."""
        if not self._connected:
            return False

        # Send health check request
        request_id = f"health_{time.time()}"
        self._request_queue.put({"action": "health_check", "id": request_id})

        # Wait for response
        start_time = time.time()
        while time.time() - start_time < 5:  # 5 second timeout
            try:
                response = self._response_queue.get(timeout=1)
                if response.get("id") == request_id:
                    return response.get("result", False)
            except Empty:
                continue

        return False

    @property
    def connected(self) -> bool:
        """Check if connected."""
        return self._connected

    @property
    def available_tools(self) -> list[str]:
        """Get available tools."""
        return self._available_tools.copy()

    def _run_connection(self, server_path: str) -> None:
        """Run the connection in background thread with its own event loop."""
        try:
            # Create new event loop for this thread
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)

            # Run the connection handler
            self._loop.run_until_complete(self._connection_handler(server_path))

        except Exception as e:
            logger.error(f"Connection thread error: {e}")
        finally:
            if self._loop:
                self._loop.close()
            self._connected = False

    async def _connection_handler(self, server_path: str) -> None:
        """Handle the MCP connection and requests."""
        try:
            # Create and connect client
            self._client = MCPClient(server_path)
            await self._client.connect()

            self._connected = True
            self._available_tools = self._client.available_tools.copy()
            logger.info(
                f"Connected to MCP server. Available tools: {self._available_tools}"
            )

            # Process requests until shutdown
            while not self._shutdown_event.is_set():
                try:
                    # Check for requests (non-blocking)
                    request = self._request_queue.get(timeout=0.1)

                    if request["action"] == "disconnect":
                        break
                    elif request["action"] == "invoke_tool":
                        await self._handle_invoke_tool(request)
                    elif request["action"] == "health_check":
                        await self._handle_health_check(request)

                except Empty:
                    # No request, continue
                    continue
                except Exception as e:
                    logger.error(f"Error processing request: {e}")

        except Exception as e:
            logger.error(f"Connection handler error: {e}")
            self._response_queue.put(
                {
                    "id": "connection_error",
                    "result": {"success": False, "error": str(e)},
                }
            )
        finally:
            # Clean up
            if self._client:
                try:
                    await self._client.disconnect()
                except Exception as e:
                    logger.error(f"Error disconnecting client: {e}")
            self._connected = False

    async def _handle_invoke_tool(self, request: dict[str, Any]) -> None:
        """Handle tool invocation request."""
        try:
            result = await self._client.invoke_tool(
                request["tool_name"], request["arguments"]
            )

            self._response_queue.put(
                {
                    "id": request["id"],
                    "result": result.model_dump()
                    if hasattr(result, "model_dump")
                    else {
                        "success": True,
                        "result": result,
                        "tool_name": request["tool_name"],
                        "arguments": request["arguments"],
                    },
                }
            )

        except Exception as e:
            logger.error(f"Tool invocation error: {e}")
            self._response_queue.put(
                {
                    "id": request["id"],
                    "result": {
                        "success": False,
                        "error": str(e),
                        "tool_name": request["tool_name"],
                        "arguments": request["arguments"],
                    },
                }
            )

    async def _handle_health_check(self, request: dict[str, Any]) -> None:
        """Handle health check request."""
        try:
            health = await self._client.health_check()
            self._response_queue.put({"id": request["id"], "result": health})
        except Exception as e:
            logger.error(f"Health check error: {e}")
            self._response_queue.put({"id": request["id"], "result": False})
