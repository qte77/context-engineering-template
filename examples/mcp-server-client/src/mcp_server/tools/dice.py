"""Dice rolling tool for MCP server."""

import random
import re
from typing import Any

from ..models import DiceRollRequest, DiceRollResponse
from .base import BaseTool, ToolError


class DiceRollTool(BaseTool):
    """Tool for rolling dice using standard notation."""

    def __init__(self):
        super().__init__(
            name="roll_dice",
            description="Roll dice using standard notation like '2d6' or '1d20'",
        )
        self.notation_pattern = re.compile(r"^(\d+)d(\d+)$")

    async def execute(self, **kwargs: Any) -> DiceRollResponse:
        """Execute dice roll with the given notation."""
        notation = kwargs.get("notation")
        if not notation:
            raise ToolError("Missing required parameter: notation")

        # Validate input using Pydantic model
        request = self.validate_input({"notation": notation}, DiceRollRequest)

        # Parse the notation
        match = self.notation_pattern.match(request.notation)
        if not match:
            raise ToolError(f"Invalid dice notation: {notation}")

        dice_count = int(match.group(1))
        sides = int(match.group(2))

        self.logger.info(f"Rolling {dice_count}d{sides}")

        # Generate random values for each die
        values = []
        for _ in range(dice_count):
            roll = random.randint(1, sides)
            values.append(roll)

        total = sum(values)

        self.logger.info(f"Dice roll result: {values} (total: {total})")

        # Return structured response
        return DiceRollResponse(
            values=values,
            total=total,
            notation=str(notation),  # Return original notation as provided
        )

    def format_result(self, response: DiceRollResponse) -> str:
        """Format dice roll result for display."""
        if len(response.values) == 1:
            return f"🎲 Rolled {response.notation}: **{response.values[0]}**"
        else:
            values_str = ", ".join(map(str, response.values))
            return (
                f"🎲 Rolled {response.notation}: [{values_str}] = **{response.total}**"
            )

    async def safe_execute(self, **kwargs) -> dict[str, Any]:
        """Execute dice roll with formatted output."""
        try:
            result = await self.execute(**kwargs)
            formatted_result = self.format_result(result)

            return {
                "content": [
                    {
                        "type": "text",
                        "text": formatted_result,
                    }
                ],
                "isError": False,
            }
        except Exception as e:
            return self.create_error_response(e)
