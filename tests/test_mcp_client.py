"""Tests for MCP client functionality."""

import asyncio
import os
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.mcp_client.client import MCPClient
from src.mcp_client.models.responses import ClientToolResult
from src.mcp_client.transport import MCPTransport


class TestMCPTransport:
    """Test cases for MCPTransport class."""

    def test_init(self):
        """Test transport initialization."""
        transport = MCPTransport("test_server.py")
        assert transport.server_path == "test_server.py"
        assert transport.session is None
        assert transport.connected is False
        assert transport.available_tools == []

    @pytest.mark.asyncio
    async def test_connect_file_not_found(self):
        """Test connection with non-existent server file."""
        transport = MCPTransport("nonexistent_server.py")
        
        with pytest.raises(FileNotFoundError, match="Server script not found"):
            await transport.connect()

    @pytest.mark.asyncio
    async def test_connect_unsupported_file_type(self, tmp_path):
        """Test connection with unsupported file type."""
        server_file = tmp_path / "server.txt"
        server_file.write_text("# not a valid server script")
        
        transport = MCPTransport(str(server_file))
        
        with pytest.raises(ValueError, match="Unsupported server script type"):
            await transport.connect()

    @pytest.mark.asyncio
    async def test_connect_success(self, tmp_path):
        """Test successful connection."""
        server_file = tmp_path / "server.py"
        server_file.write_text("# mock server script")
        
        transport = MCPTransport(str(server_file))
        
        # Mock the connection components
        with patch('src.mcp_client.transport.stdio_client') as mock_stdio, \
             patch('src.mcp_client.transport.ClientSession') as mock_session_class:
            
            # Setup mocks
            mock_read, mock_write = AsyncMock(), AsyncMock()
            mock_stdio.return_value.__aenter__.return_value = (mock_read, mock_write)
            
            mock_session = AsyncMock()
            mock_session_class.return_value.__aenter__.return_value = mock_session
            
            # Mock session methods
            mock_session.initialize = AsyncMock()
            mock_tools_response = MagicMock()
            mock_tool1 = MagicMock()
            mock_tool1.name = "roll_dice"
            mock_tool2 = MagicMock()
            mock_tool2.name = "get_weather"
            mock_tool3 = MagicMock()
            mock_tool3.name = "get_date"
            mock_tools_response.tools = [mock_tool1, mock_tool2, mock_tool3]
            mock_session.list_tools.return_value = mock_tools_response
            
            # Test connection
            await transport.connect()
            
            # Verify connection state
            assert transport.connected is True
            assert transport.available_tools == ["roll_dice", "get_weather", "get_date"]
            assert transport.session == mock_session

    @pytest.mark.asyncio
    async def test_disconnect(self):
        """Test disconnect functionality."""
        transport = MCPTransport("test_server.py")
        
        # Mock exit stack
        mock_exit_stack = AsyncMock()
        transport.exit_stack = mock_exit_stack
        transport.connected = True
        transport.available_tools = ["test_tool"]
        
        await transport.disconnect()
        
        mock_exit_stack.aclose.assert_called_once()
        assert transport.session is None
        assert transport.connected is False
        assert transport.available_tools == []

    @pytest.mark.asyncio
    async def test_call_tool_not_connected(self):
        """Test tool call when not connected."""
        transport = MCPTransport("test_server.py")
        
        with pytest.raises(RuntimeError, match="Not connected to server"):
            await transport.call_tool("test_tool", {})

    @pytest.mark.asyncio
    async def test_call_tool_unavailable(self):
        """Test tool call with unavailable tool."""
        transport = MCPTransport("test_server.py")
        transport.connected = True
        transport.session = AsyncMock()  # Add session mock
        transport.available_tools = ["available_tool"]
        
        with pytest.raises(ValueError, match="Tool 'unavailable_tool' not available"):
            await transport.call_tool("unavailable_tool", {})

    @pytest.mark.asyncio
    async def test_call_tool_success(self):
        """Test successful tool call."""
        transport = MCPTransport("test_server.py")
        transport.connected = True
        transport.available_tools = ["test_tool"]
        
        # Mock session
        mock_session = AsyncMock()
        transport.session = mock_session
        
        mock_result = MagicMock()
        mock_session.call_tool.return_value = mock_result
        
        result = await transport.call_tool("test_tool", {"arg": "value"})
        
        mock_session.call_tool.assert_called_once_with("test_tool", {"arg": "value"})
        assert result == mock_result

    @pytest.mark.asyncio
    async def test_health_check_not_connected(self):
        """Test health check when not connected."""
        transport = MCPTransport("test_server.py")
        
        result = await transport.health_check()
        assert result is False

    @pytest.mark.asyncio
    async def test_health_check_success(self):
        """Test successful health check."""
        transport = MCPTransport("test_server.py")
        transport.connected = True
        
        mock_session = AsyncMock()
        transport.session = mock_session
        mock_session.list_tools.return_value = MagicMock()
        
        result = await transport.health_check()
        assert result is True

    @pytest.mark.asyncio
    async def test_health_check_failure(self):
        """Test health check with exception."""
        transport = MCPTransport("test_server.py")
        transport.connected = True
        
        mock_session = AsyncMock()
        transport.session = mock_session
        mock_session.list_tools.side_effect = Exception("Connection lost")
        
        result = await transport.health_check()
        assert result is False


class TestMCPClient:
    """Test cases for MCPClient class."""

    def test_init(self):
        """Test client initialization."""
        client = MCPClient("test_server.py")
        assert client.server_path == "test_server.py"
        assert isinstance(client.transport, MCPTransport)
        assert client.connected is False

    @pytest.mark.asyncio
    async def test_connect_success(self):
        """Test successful connection."""
        client = MCPClient("test_server.py")
        
        with patch.object(client.transport, 'connect', new_callable=AsyncMock) as mock_connect:
            mock_connect.return_value = None
            client.transport.connected = True
            client.transport.available_tools = ["test_tool"]
            
            await client.connect()
            
            mock_connect.assert_called_once()
            assert client.connected is True

    @pytest.mark.asyncio
    async def test_connect_failure(self):
        """Test connection failure."""
        client = MCPClient("test_server.py")
        
        with patch.object(client.transport, 'connect', new_callable=AsyncMock) as mock_connect:
            mock_connect.side_effect = ConnectionError("Failed to connect")
            
            with pytest.raises(ConnectionError, match="Failed to connect"):
                await client.connect()

    @pytest.mark.asyncio
    async def test_disconnect(self):
        """Test disconnect functionality."""
        client = MCPClient("test_server.py")
        client._connected = True
        
        with patch.object(client.transport, 'disconnect', new_callable=AsyncMock) as mock_disconnect:
            await client.disconnect()
            
            mock_disconnect.assert_called_once()
            assert client.connected is False

    @pytest.mark.asyncio
    async def test_invoke_tool_not_connected(self):
        """Test tool invocation when not connected."""
        client = MCPClient("test_server.py")
        
        result = await client.invoke_tool("test_tool", {})
        
        assert result.success is False
        assert "Not connected to server" in result.error
        assert result.tool_name == "test_tool"

    @pytest.mark.asyncio
    async def test_invoke_tool_unavailable(self):
        """Test tool invocation with unavailable tool."""
        client = MCPClient("test_server.py")
        client._connected = True
        client.transport.connected = True
        client.transport.available_tools = ["available_tool"]
        
        result = await client.invoke_tool("unavailable_tool", {})
        
        assert result.success is False
        assert "not available" in result.error
        assert result.tool_name == "unavailable_tool"

    @pytest.mark.asyncio
    async def test_invoke_tool_success(self):
        """Test successful tool invocation."""
        client = MCPClient("test_server.py")
        client._connected = True
        client.transport.connected = True
        client.transport.available_tools = ["test_tool"]
        
        mock_result = MagicMock()
        mock_result.content = [{"type": "text", "text": "Success"}]
        
        with patch.object(client.transport, 'call_tool', new_callable=AsyncMock) as mock_call:
            mock_call.return_value = mock_result
            
            result = await client.invoke_tool("test_tool", {"arg": "value"})
            
            mock_call.assert_called_once_with("test_tool", {"arg": "value"})
            assert result.success is True
            assert result.result == mock_result
            assert result.tool_name == "test_tool"

    @pytest.mark.asyncio
    async def test_invoke_tool_exception(self):
        """Test tool invocation with exception."""
        client = MCPClient("test_server.py")
        client._connected = True
        client.transport.connected = True
        client.transport.available_tools = ["test_tool"]
        
        with patch.object(client.transport, 'call_tool', new_callable=AsyncMock) as mock_call:
            mock_call.side_effect = Exception("Tool execution failed")
            
            result = await client.invoke_tool("test_tool", {"arg": "value"})
            
            assert result.success is False
            assert "Tool execution failed" in result.error
            assert result.tool_name == "test_tool"

    @pytest.mark.asyncio
    async def test_health_check_not_connected(self):
        """Test health check when not connected."""
        client = MCPClient("test_server.py")
        
        result = await client.health_check()
        assert result is False

    @pytest.mark.asyncio
    async def test_health_check_success(self):
        """Test successful health check."""
        client = MCPClient("test_server.py")
        client._connected = True
        client.transport.connected = True  # Also set transport connected
        
        with patch.object(client.transport, 'health_check', new_callable=AsyncMock) as mock_health:
            mock_health.return_value = True
            
            result = await client.health_check()
            assert result is True

    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test client as async context manager."""
        client = MCPClient("test_server.py")
        
        with patch.object(client, 'connect', new_callable=AsyncMock) as mock_connect, \
             patch.object(client, 'disconnect', new_callable=AsyncMock) as mock_disconnect:
            
            async with client as context_client:
                assert context_client == client
                mock_connect.assert_called_once()
            
            mock_disconnect.assert_called_once()


class TestClientToolResult:
    """Test cases for ClientToolResult model."""

    def test_successful_result(self):
        """Test successful tool result."""
        result = ClientToolResult(
            success=True,
            result={"data": "test"},
            tool_name="test_tool",
            arguments={"arg": "value"}
        )
        
        assert result.success is True
        assert result.result == {"data": "test"}
        assert result.error is None
        assert result.tool_name == "test_tool"
        assert result.arguments == {"arg": "value"}

    def test_failed_result(self):
        """Test failed tool result."""
        result = ClientToolResult(
            success=False,
            error="Tool execution failed",
            tool_name="test_tool",
            arguments={"arg": "value"}
        )
        
        assert result.success is False
        assert result.result is None
        assert result.error == "Tool execution failed"
        assert result.tool_name == "test_tool"
        assert result.arguments == {"arg": "value"}
