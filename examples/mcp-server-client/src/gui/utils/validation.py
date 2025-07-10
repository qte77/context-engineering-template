"""Validation utilities for GUI input."""

import re


def validate_dice_notation(notation: str) -> bool:
    """Validate dice notation format.

    Args:
        notation: Dice notation string (e.g., "2d6", "1d20")

    Returns:
        True if valid, False otherwise
    """
    if not notation or not isinstance(notation, str):
        return False

    # Pattern: number + 'd' + number
    pattern = r"^(\d+)d(\d+)$"
    match = re.match(pattern, notation.strip().lower())

    if not match:
        return False

    # Check reasonable limits
    num_dice = int(match.group(1))
    num_sides = int(match.group(2))

    # Validate ranges
    if num_dice < 1 or num_dice > 100:
        return False
    if num_sides < 2 or num_sides > 1000:
        return False

    return True


def validate_location(location: str) -> bool:
    """Validate location input for weather lookup.

    Args:
        location: Location string (city name or coordinates)

    Returns:
        True if valid, False otherwise
    """
    if not location or not isinstance(location, str):
        return False

    location = location.strip()

    # Check for coordinates format (lat,lon)
    coord_pattern = r"^-?\d+\.?\d*,-?\d+\.?\d*$"
    if re.match(coord_pattern, location):
        return True

    # Check for city name (at least 2 characters, letters and spaces)
    city_pattern = r"^[a-zA-Z\s]{2,}$"
    if re.match(city_pattern, location):
        return True

    return False


def validate_timezone(timezone: str) -> bool:
    """Validate timezone identifier.

    Args:
        timezone: Timezone string (IANA format)

    Returns:
        True if valid, False otherwise
    """
    if not timezone or not isinstance(timezone, str):
        return False

    timezone = timezone.strip()

    # Common timezone patterns
    common_timezones = [
        "UTC",
        "GMT",
        "EST",
        "PST",
        "CST",
        "MST",
        "America/New_York",
        "America/Los_Angeles",
        "America/Chicago",
        "Europe/London",
        "Europe/Paris",
        "Asia/Tokyo",
        "Australia/Sydney",
    ]

    if timezone in common_timezones:
        return True

    # IANA timezone format: Area/City or Area/Region/City
    iana_pattern = r"^[A-Za-z_]+/[A-Za-z_]+(?:/[A-Za-z_]+)?$"
    return bool(re.match(iana_pattern, timezone))


def validate_server_path(path: str) -> str | None:
    """Validate server path and return error message if invalid.

    Args:
        path: Server path string

    Returns:
        Error message if invalid, None if valid
    """
    if not path or not isinstance(path, str):
        return "Server path is required"

    path = path.strip()

    if not path:
        return "Server path cannot be empty"

    if not path.endswith(".py"):
        return "Server path must be a Python file (.py)"

    # Basic path validation
    if ".." in path or path.startswith("/"):
        return "Server path should be relative to project root"

    return None
