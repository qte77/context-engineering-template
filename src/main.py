"""Main entry point for the MCP server application."""

import argparse
import logging
import sys
from asyncio import run

from .mcp_server import run_server


def setup_logging(level: str = "INFO"):
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


async def main():
    """Main entry point for the MCP server."""
    parser = argparse.ArgumentParser(
        description="MCP Server with dice, weather, and date/time tools"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Set the logging level",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="MCP Server v1.0.0",
    )

    args = parser.parse_args()

    # Setup logging
    setup_logging(args.log_level)

    logger = logging.getLogger(__name__)
    logger.info("Starting MCP Server application")

    try:
        # Run the MCP server (this will block until server shuts down)
        run_server()
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run(main())
