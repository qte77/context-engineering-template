"""CLI interface for MCP client tool invocation."""

import argparse
import asyncio
import json
import logging
import sys
from typing import Any

from .client import MCPClient
from .models.responses import ClientToolResult

# Configure logging
logger = logging.getLogger(__name__)


class MCPClientCLI:
    """CLI interface for MCP client tool invocation."""

    def __init__(self) -> None:
        """Initialize CLI interface."""
        self.parser = self._create_parser()
        self.client: MCPClient | None = None

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser with subcommands.
        
        Returns:
            Configured argument parser
        """
        parser = argparse.ArgumentParser(
            description="MCP Client for tool invocation",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""Examples:
  %(prog)s --server ./server.py roll_dice --notation 2d6
  %(prog)s --server ./server.py get_weather --location "San Francisco"
  %(prog)s --server ./server.py get_date --timezone UTC
"""
        )
        
        # Global arguments
        parser.add_argument(
            '--server',
            required=True,
            help='Path to MCP server script'
        )
        
        parser.add_argument(
            '--log-level',
            choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
            default='INFO',
            help='Set logging level (default: INFO)'
        )
        
        parser.add_argument(
            '--timeout',
            type=int,
            default=30,
            help='Connection timeout in seconds (default: 30)'
        )
        
        # Subcommands for tools
        subparsers = parser.add_subparsers(
            dest='tool',
            help='Available tools',
            metavar='TOOL'
        )
        
        # Roll dice tool
        dice_parser = subparsers.add_parser(
            'roll_dice',
            help='Roll dice using standard notation'
        )
        dice_parser.add_argument(
            '--notation',
            required=True,
            help='Dice notation (e.g., 2d6, 1d20, 3d10)'
        )
        
        # Weather tool
        weather_parser = subparsers.add_parser(
            'get_weather',
            help='Get current weather conditions'
        )
        weather_parser.add_argument(
            '--location',
            required=True,
            help='Location name or coordinates (lat,lon)'
        )
        
        # Date/time tool
        date_parser = subparsers.add_parser(
            'get_date',
            help='Get current date and time'
        )
        date_parser.add_argument(
            '--timezone',
            default='UTC',
            help='Timezone identifier (default: UTC)'
        )
        
        return parser

    def _setup_logging(self, level: str) -> None:
        """Setup logging configuration.
        
        Args:
            level: Logging level string
        """
        logging.basicConfig(
            level=getattr(logging, level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def _build_tool_arguments(self, args: argparse.Namespace) -> dict[str, Any]:
        """Build tool arguments from parsed CLI arguments.
        
        Args:
            args: Parsed command line arguments
            
        Returns:
            Dictionary of tool arguments
        """
        if args.tool == 'roll_dice':
            return {'notation': args.notation}
        elif args.tool == 'get_weather':
            return {'location': args.location}
        elif args.tool == 'get_date':
            return {'timezone': args.timezone}
        else:
            return {}

    def _display_success(self, result: ClientToolResult) -> None:
        """Display successful tool result.
        
        Args:
            result: Successful tool result
        """
        print(f"✅ {result.tool_name} executed successfully:")
        print()
        
        # Handle MCP response format
        if result.result and hasattr(result.result, 'content'):
            content = result.result.content
            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and 'text' in item:
                        print(item['text'])
                    else:
                        print(json.dumps(item, indent=2))
            else:
                print(json.dumps(content, indent=2))
        else:
            print(json.dumps(result.result, indent=2))

    def _display_error(self, result: ClientToolResult) -> None:
        """Display tool execution error.
        
        Args:
            result: Failed tool result
        """
        print(f"❌ {result.tool_name} failed:")
        print(f"Error: {result.error}")
        print()
        print(f"Tool: {result.tool_name}")
        print(f"Arguments: {json.dumps(result.arguments, indent=2)}")

    def _display_connection_error(self, error: Exception) -> None:
        """Display connection error.
        
        Args:
            error: Connection error
        """
        print("❌ Connection failed:")
        print(f"Error: {error}")
        print()
        print("Troubleshooting:")
        print("1. Check that the server script exists")
        print("2. Verify the server script is executable")
        print("3. Ensure required dependencies are installed")
        print("4. Check that the server starts correctly")

    async def run(self, args: list[str] | None = None) -> int:
        """Run CLI with provided arguments.
        
        Args:
            args: Command line arguments (uses sys.argv if None)
            
        Returns:
            Exit code (0 for success, 1 for error)
        """
        try:
            # Parse arguments
            parsed_args = self.parser.parse_args(args)
            
            # Setup logging
            self._setup_logging(parsed_args.log_level)
            
            # Check if tool specified
            if not parsed_args.tool:
                self.parser.print_help()
                return 1
            
            # Create client
            self.client = MCPClient(parsed_args.server)
            
            # Connect to server with timeout
            try:
                await asyncio.wait_for(
                    self.client.connect(),
                    timeout=parsed_args.timeout
                )
            except TimeoutError:
                print(f"❌ Connection timeout after {parsed_args.timeout} seconds")
                return 1
            except Exception as e:
                self._display_connection_error(e)
                return 1
            
            # Build tool arguments
            tool_args = self._build_tool_arguments(parsed_args)
            
            # Invoke tool
            result = await self.client.invoke_tool(parsed_args.tool, tool_args)
            
            # Display result
            if result.success:
                self._display_success(result)
                return 0
            else:
                self._display_error(result)
                return 1
                
        except KeyboardInterrupt:
            print("\n❌ Interrupted by user")
            return 130
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            print(f"❌ Unexpected error: {e}")
            return 1
        finally:
            # Cleanup
            if self.client:
                await self.client.disconnect()


async def main() -> int:
    """Main CLI entry point.
    
    Returns:
        Exit code
    """
    cli = MCPClientCLI()
    return await cli.run()


if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
