"""Main entry point for the MCP server and client applications."""

import argparse
import logging
import sys
from asyncio import run

from src.mcp_client.cli import MCPClientCLI
from src.mcp_server import run_server


def setup_logging(level: str = "INFO") -> None:
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


async def main() -> None:
    """Main entry point for MCP applications."""
    parser = argparse.ArgumentParser(
        description="MCP Server and Client with dice, weather, and date/time tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run MCP server
  %(prog)s server
  
  # Run MCP client
  %(prog)s client --server ./server.py roll_dice --notation 2d6
  %(prog)s client --server ./server.py get_weather --location "San Francisco"
  %(prog)s client --server ./server.py get_date --timezone UTC
"""
    )
    
    # Add subcommands
    subparsers = parser.add_subparsers(
        dest='mode',
        help='Choose server or client mode',
        metavar='MODE'
    )
    
    # Server subcommand
    server_parser = subparsers.add_parser(
        'server',
        help='Run MCP server'
    )
    server_parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Set the logging level",
    )
    server_parser.add_argument(
        "--version",
        action="version",
        version="MCP Server v1.0.0",
    )
    
    # Client subcommand
    client_parser = subparsers.add_parser(
        'client',
        help='Run MCP client'
    )
    client_parser.add_argument(
        '--server',
        required=True,
        help='Path to MCP server script'
    )
    client_parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Set logging level (default: INFO)'
    )
    client_parser.add_argument(
        '--timeout',
        type=int,
        default=30,
        help='Connection timeout in seconds (default: 30)'
    )
    
    # Tool subcommands for client
    tool_subparsers = client_parser.add_subparsers(
        dest='tool',
        help='Available tools',
        metavar='TOOL'
    )
    
    # Roll dice tool
    dice_parser = tool_subparsers.add_parser(
        'roll_dice',
        help='Roll dice using standard notation'
    )
    dice_parser.add_argument(
        '--notation',
        required=True,
        help='Dice notation (e.g., 2d6, 1d20, 3d10)'
    )
    
    # Weather tool
    weather_parser = tool_subparsers.add_parser(
        'get_weather',
        help='Get current weather conditions'
    )
    weather_parser.add_argument(
        '--location',
        required=True,
        help='Location name or coordinates (lat,lon)'
    )
    
    # Date/time tool
    date_parser = tool_subparsers.add_parser(
        'get_date',
        help='Get current date and time'
    )
    date_parser.add_argument(
        '--timezone',
        default='UTC',
        help='Timezone identifier (default: UTC)'
    )

    args = parser.parse_args()

    # Check if mode is specified
    if not args.mode:
        parser.print_help()
        sys.exit(1)

    # Setup logging
    log_level = getattr(args, 'log_level', 'INFO')
    setup_logging(log_level)

    logger = logging.getLogger(__name__)

    try:
        if args.mode == 'server':
            logger.info("Starting MCP Server application")
            # Run the MCP server (this will block until server shuts down)
            run_server()
        elif args.mode == 'client':
            logger.info("Starting MCP Client application")
            # Create client CLI and run it
            cli = MCPClientCLI()
            
            # Build client arguments from parsed args
            client_args = [
                '--server', args.server,
                '--log-level', args.log_level,
                '--timeout', str(args.timeout)
            ]
            
            if args.tool:
                client_args.append(args.tool)
                
                # Add tool-specific arguments
                if args.tool == 'roll_dice':
                    client_args.extend(['--notation', args.notation])
                elif args.tool == 'get_weather':
                    client_args.extend(['--location', args.location])
                elif args.tool == 'get_date':
                    client_args.extend(['--timezone', args.timezone])
            
            # Run the client
            exit_code = await cli.run(client_args)
            sys.exit(exit_code)
        else:
            parser.print_help()
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run(main())
