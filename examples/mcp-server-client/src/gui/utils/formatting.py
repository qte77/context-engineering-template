"""Formatting utilities for GUI display."""

import json
from typing import Any


def format_json_for_display(data: Any, indent: int = 2) -> str:
    """Format JSON data for display with proper indentation.

    Args:
        data: Data to format as JSON
        indent: Number of spaces for indentation

    Returns:
        Formatted JSON string
    """
    try:
        return json.dumps(data, indent=indent, ensure_ascii=False)
    except (TypeError, ValueError) as e:
        return f"Error formatting JSON: {str(e)}"


def format_error_message(error: str) -> str:
    """Format error messages for user-friendly display.

    Args:
        error: Raw error message

    Returns:
        Formatted error message
    """
    # Remove common Python error prefixes
    error = error.replace("Exception: ", "")
    error = error.replace("Error: ", "")

    # Capitalize first letter
    if error:
        error = error[0].upper() + error[1:]

    return error


def format_execution_time(seconds: float) -> str:
    """Format execution time for display.

    Args:
        seconds: Execution time in seconds

    Returns:
        Formatted time string
    """
    if seconds < 1:
        return f"{seconds * 1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    else:
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds:.1f}s"


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text with ellipsis if too long.

    Args:
        text: Text to truncate
        max_length: Maximum length before truncation

    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."
