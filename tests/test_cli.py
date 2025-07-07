"""Tests for MCP client CLI interface."""

import asyncio
import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.mcp_client.cli import MCPClientCLI
from src.mcp_client.models.responses import ClientToolResult


class TestMCPClientCLI:
    """Test cases for MCPClientCLI class."""

    def test_init(self):
        """Test CLI initialization."""
        cli = MCPClientCLI()
        assert cli.parser is not None
        assert cli.client is None

    def test_parser_creation(self):
        """Test argument parser creation."""
        cli = MCPClientCLI()
        parser = cli.parser
        
        # Test that parser exists and has expected subcommands
        assert parser is not None
        
        # Test help doesn't crash
        help_text = parser.format_help()
        assert "MCP Client" in help_text
        assert "--server" in help_text

    def test_build_tool_arguments_roll_dice(self):
        """Test building arguments for roll_dice tool."""
        cli = MCPClientCLI()
        
        # Mock parsed arguments
        args = MagicMock()
        args.tool = 'roll_dice'
        args.notation = '2d6'
        
        result = cli._build_tool_arguments(args)
        assert result == {'notation': '2d6'}

    def test_build_tool_arguments_get_weather(self):
        """Test building arguments for get_weather tool."""
        cli = MCPClientCLI()
        
        # Mock parsed arguments
        args = MagicMock()
        args.tool = 'get_weather'
        args.location = 'San Francisco'
        
        result = cli._build_tool_arguments(args)
        assert result == {'location': 'San Francisco'}

    def test_build_tool_arguments_get_date(self):
        """Test building arguments for get_date tool."""
        cli = MCPClientCLI()
        
        # Mock parsed arguments
        args = MagicMock()
        args.tool = 'get_date'
        args.timezone = 'UTC'
        
        result = cli._build_tool_arguments(args)
        assert result == {'timezone': 'UTC'}

    def test_build_tool_arguments_unknown(self):
        """Test building arguments for unknown tool."""
        cli = MCPClientCLI()
        
        # Mock parsed arguments
        args = MagicMock()
        args.tool = 'unknown_tool'
        
        result = cli._build_tool_arguments(args)
        assert result == {}

    def test_parse_roll_dice_arguments(self):
        """Test parsing roll_dice command arguments."""
        cli = MCPClientCLI()
        
        args = cli.parser.parse_args([
            '--server', 'test_server.py',
            'roll_dice',
            '--notation', '3d6'
        ])
        
        assert args.server == 'test_server.py'
        assert args.tool == 'roll_dice'
        assert args.notation == '3d6'
        assert args.log_level == 'INFO'  # default
        assert args.timeout == 30  # default

    def test_parse_get_weather_arguments(self):
        """Test parsing get_weather command arguments."""
        cli = MCPClientCLI()
        
        args = cli.parser.parse_args([
            '--server', 'test_server.py',
            '--log-level', 'DEBUG',
            'get_weather',
            '--location', 'London'
        ])
        
        assert args.server == 'test_server.py'
        assert args.tool == 'get_weather'
        assert args.location == 'London'
        assert args.log_level == 'DEBUG'

    def test_parse_get_date_arguments(self):
        """Test parsing get_date command arguments."""
        cli = MCPClientCLI()
        
        args = cli.parser.parse_args([
            '--server', 'test_server.py',
            '--timeout', '60',
            'get_date',
            '--timezone', 'America/New_York'
        ])
        
        assert args.server == 'test_server.py'
        assert args.tool == 'get_date'
        assert args.timezone == 'America/New_York'
        assert args.timeout == 60

    def test_parse_missing_server(self):
        """Test parsing with missing required --server argument."""
        cli = MCPClientCLI()
        
        with pytest.raises(SystemExit):
            cli.parser.parse_args(['roll_dice', '--notation', '2d6'])

    def test_parse_missing_tool_arguments(self):
        """Test parsing with missing required tool arguments."""
        cli = MCPClientCLI()
        
        with pytest.raises(SystemExit):
            cli.parser.parse_args(['--server', 'test.py', 'roll_dice'])

    @pytest.mark.asyncio
    async def test_run_no_tool_specified(self, capsys):
        """Test running CLI without specifying a tool."""
        cli = MCPClientCLI()
        
        exit_code = await cli.run(['--server', 'test_server.py'])
        
        assert exit_code == 1
        captured = capsys.readouterr()
        assert "usage:" in captured.out

    @pytest.mark.asyncio
    async def test_run_connection_timeout(self):
        """Test running CLI with connection timeout."""
        cli = MCPClientCLI()
        
        with patch('src.mcp_client.cli.MCPClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client_class.return_value = mock_client
            mock_client.connect.side_effect = asyncio.TimeoutError()
            
            exit_code = await cli.run([
                '--server', 'test_server.py',
                '--timeout', '1',
                'roll_dice',
                '--notation', '2d6'
            ])
            
            assert exit_code == 1

    @pytest.mark.asyncio
    async def test_run_connection_error(self):
        """Test running CLI with connection error."""
        cli = MCPClientCLI()
        
        with patch('src.mcp_client.cli.MCPClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client_class.return_value = mock_client
            mock_client.connect.side_effect = ConnectionError("Server not found")
            
            exit_code = await cli.run([
                '--server', 'test_server.py',
                'roll_dice',
                '--notation', '2d6'
            ])
            
            assert exit_code == 1

    @pytest.mark.asyncio
    async def test_run_successful_tool_execution(self):
        """Test running CLI with successful tool execution."""
        cli = MCPClientCLI()
        
        # Mock successful result
        mock_result = ClientToolResult(
            success=True,
            result=MagicMock(content=[{"text": "🎲 Rolled 2d6: [3, 5] = **8**"}]),
            tool_name="roll_dice",
            arguments={"notation": "2d6"}
        )
        
        with patch('src.mcp_client.cli.MCPClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client_class.return_value = mock_client
            mock_client.connect.return_value = None
            mock_client.invoke_tool.return_value = mock_result
            mock_client.disconnect.return_value = None
            
            exit_code = await cli.run([
                '--server', 'test_server.py',
                'roll_dice',
                '--notation', '2d6'
            ])
            
            assert exit_code == 0
            mock_client.connect.assert_called_once()
            mock_client.invoke_tool.assert_called_once_with(
                'roll_dice', {'notation': '2d6'}
            )
            mock_client.disconnect.assert_called_once()

    @pytest.mark.asyncio
    async def test_run_failed_tool_execution(self):
        """Test running CLI with failed tool execution."""
        cli = MCPClientCLI()
        
        # Mock failed result
        mock_result = ClientToolResult(
            success=False,
            error="Tool execution failed",
            tool_name="roll_dice",
            arguments={"notation": "invalid"}
        )
        
        with patch('src.mcp_client.cli.MCPClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client_class.return_value = mock_client
            mock_client.connect.return_value = None
            mock_client.invoke_tool.return_value = mock_result
            mock_client.disconnect.return_value = None
            
            exit_code = await cli.run([
                '--server', 'test_server.py',
                'roll_dice',
                '--notation', 'invalid'
            ])
            
            assert exit_code == 1
            mock_client.invoke_tool.assert_called_once_with(
                'roll_dice', {'notation': 'invalid'}
            )

    @pytest.mark.asyncio
    async def test_run_keyboard_interrupt(self):
        """Test running CLI with keyboard interrupt."""
        cli = MCPClientCLI()
        
        with patch('src.mcp_client.cli.MCPClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client_class.return_value = mock_client
            mock_client.connect.side_effect = KeyboardInterrupt()
            
            exit_code = await cli.run([
                '--server', 'test_server.py',
                'roll_dice',
                '--notation', '2d6'
            ])
            
            assert exit_code == 130

    @pytest.mark.asyncio
    async def test_run_unexpected_error(self):
        """Test running CLI with unexpected error."""
        cli = MCPClientCLI()
        
        with patch('src.mcp_client.cli.MCPClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client_class.return_value = mock_client
            mock_client.connect.side_effect = RuntimeError("Unexpected error")
            
            exit_code = await cli.run([
                '--server', 'test_server.py',
                'roll_dice',
                '--notation', '2d6'
            ])
            
            assert exit_code == 1

    @pytest.mark.asyncio
    async def test_run_cleanup_on_success(self):
        """Test that client is properly cleaned up on success."""
        cli = MCPClientCLI()
        
        mock_result = ClientToolResult(
            success=True,
            result=MagicMock(content=[{"text": "Success"}]),
            tool_name="roll_dice",
            arguments={"notation": "2d6"}
        )
        
        with patch('src.mcp_client.cli.MCPClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client_class.return_value = mock_client
            mock_client.connect.return_value = None
            mock_client.invoke_tool.return_value = mock_result
            mock_client.disconnect.return_value = None
            
            await cli.run([
                '--server', 'test_server.py',
                'roll_dice',
                '--notation', '2d6'
            ])
            
            # Verify cleanup was called
            mock_client.disconnect.assert_called_once()

    @pytest.mark.asyncio
    async def test_run_cleanup_on_error(self):
        """Test that client is properly cleaned up on error."""
        cli = MCPClientCLI()
        
        with patch('src.mcp_client.cli.MCPClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client_class.return_value = mock_client
            mock_client.connect.return_value = None
            mock_client.invoke_tool.side_effect = Exception("Test error")
            mock_client.disconnect.return_value = None
            
            await cli.run([
                '--server', 'test_server.py',
                'roll_dice',
                '--notation', '2d6'
            ])
            
            # Verify cleanup was called even on error
            mock_client.disconnect.assert_called_once()

    def test_display_success_with_text_content(self, capsys):
        """Test displaying successful result with text content."""
        cli = MCPClientCLI()
        
        result = ClientToolResult(
            success=True,
            result=MagicMock(content=[{"text": "🎲 Rolled 2d6: [3, 5] = **8**"}]),
            tool_name="roll_dice",
            arguments={"notation": "2d6"}
        )
        
        cli._display_success(result)
        
        captured = capsys.readouterr()
        assert "✅ roll_dice executed successfully" in captured.out
        assert "🎲 Rolled 2d6: [3, 5] = **8**" in captured.out

    def test_display_success_with_json_content(self, capsys):
        """Test displaying successful result with JSON content."""
        cli = MCPClientCLI()
        
        result = ClientToolResult(
            success=True,
            result=MagicMock(content=[{"data": "test", "value": 42}]),
            tool_name="test_tool",
            arguments={}
        )
        
        cli._display_success(result)
        
        captured = capsys.readouterr()
        assert "✅ test_tool executed successfully" in captured.out
        assert '"data": "test"' in captured.out
        assert '"value": 42' in captured.out

    def test_display_error(self, capsys):
        """Test displaying error result."""
        cli = MCPClientCLI()
        
        result = ClientToolResult(
            success=False,
            error="Tool execution failed",
            tool_name="roll_dice",
            arguments={"notation": "invalid"}
        )
        
        cli._display_error(result)
        
        captured = capsys.readouterr()
        assert "❌ roll_dice failed" in captured.out
        assert "Error: Tool execution failed" in captured.out
        assert "Tool: roll_dice" in captured.out
        assert '"notation": "invalid"' in captured.out

    def test_display_connection_error(self, capsys):
        """Test displaying connection error."""
        cli = MCPClientCLI()
        
        error = ConnectionError("Server not found")
        cli._display_connection_error(error)
        
        captured = capsys.readouterr()
        assert "❌ Connection failed" in captured.out
        assert "Error: Server not found" in captured.out
        assert "Troubleshooting:" in captured.out
        assert "Check that the server script exists" in captured.out


@pytest.mark.asyncio
async def test_main_function():
    """Test main function."""
    with patch('src.mcp_client.cli.MCPClientCLI') as mock_cli_class:
        mock_cli = AsyncMock()
        mock_cli_class.return_value = mock_cli
        mock_cli.run.return_value = 0
        
        from src.mcp_client.cli import main
        
        with patch('sys.argv', ['cli.py', '--server', 'test.py', 'roll_dice', '--notation', '2d6']):
            result = await main()
            
        assert result == 0
        mock_cli.run.assert_called_once()
