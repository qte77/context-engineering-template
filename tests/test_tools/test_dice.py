"""Tests for the dice rolling tool."""

import pytest

from src.mcp_server.tools.dice import DiceRollTool
from src.mcp_server.tools.base import ValidationToolError


class TestDiceRollTool:
    """Test suite for DiceRollTool."""

    @pytest.fixture
    def dice_tool(self):
        """Create a DiceRollTool instance for testing."""
        return DiceRollTool()

    @pytest.mark.asyncio
    async def test_roll_dice_valid_notation(self, dice_tool):
        """Test valid dice notation works correctly."""
        result = await dice_tool.execute(notation="2d6")

        assert isinstance(result.values, list)
        assert len(result.values) == 2
        assert all(1 <= v <= 6 for v in result.values)
        assert result.total == sum(result.values)
        assert result.notation == "2d6"

    @pytest.mark.asyncio
    async def test_roll_dice_single_die(self, dice_tool):
        """Test rolling a single die."""
        result = await dice_tool.execute(notation="1d20")

        assert len(result.values) == 1
        assert 1 <= result.values[0] <= 20
        assert result.total == result.values[0]
        assert result.notation == "1d20"

    @pytest.mark.asyncio
    async def test_roll_dice_multiple_dice(self, dice_tool):
        """Test rolling multiple dice."""
        result = await dice_tool.execute(notation="4d10")

        assert len(result.values) == 4
        assert all(1 <= v <= 10 for v in result.values)
        assert result.total == sum(result.values)
        assert result.notation == "4d10"

    @pytest.mark.asyncio
    async def test_roll_dice_invalid_notation_format(self, dice_tool):
        """Test invalid dice notation raises ValidationError."""
        with pytest.raises(ValidationToolError) as exc_info:
            await dice_tool.execute(notation="d6")

        assert "Invalid dice notation" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_roll_dice_invalid_notation_no_d(self, dice_tool):
        """Test notation without 'd' raises ValidationError."""
        with pytest.raises(ValidationToolError) as exc_info:
            await dice_tool.execute(notation="2x6")

        assert "Invalid dice notation" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_roll_dice_zero_dice_count(self, dice_tool):
        """Test zero dice count raises ValidationError."""
        with pytest.raises(ValidationToolError) as exc_info:
            await dice_tool.execute(notation="0d6")

        assert "Dice count must be greater than 0" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_roll_dice_zero_sides(self, dice_tool):
        """Test zero sides raises ValidationError."""
        with pytest.raises(ValidationToolError) as exc_info:
            await dice_tool.execute(notation="1d0")

        assert "Number of sides must be greater than 0" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_roll_dice_too_many_dice(self, dice_tool):
        """Test too many dice raises ValidationError."""
        with pytest.raises(ValidationToolError) as exc_info:
            await dice_tool.execute(notation="101d6")

        assert "Dice count must not exceed 100" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_roll_dice_too_many_sides(self, dice_tool):
        """Test too many sides raises ValidationError."""
        with pytest.raises(ValidationToolError) as exc_info:
            await dice_tool.execute(notation="1d1001")

        assert "Number of sides must not exceed 1000" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_roll_dice_random_text(self, dice_tool):
        """Test random text raises ValidationError."""
        with pytest.raises(ValidationToolError) as exc_info:
            await dice_tool.execute(notation="abc")

        assert "Invalid dice notation" in str(exc_info.value)

    def test_format_result_single_die(self, dice_tool):
        """Test formatting result for single die."""
        from src.mcp_server.models import DiceRollResponse

        response = DiceRollResponse(values=[15], total=15, notation="1d20")
        formatted = dice_tool.format_result(response)

        assert "🎲" in formatted
        assert "1d20" in formatted
        assert "**15**" in formatted

    def test_format_result_multiple_dice(self, dice_tool):
        """Test formatting result for multiple dice."""
        from src.mcp_server.models import DiceRollResponse

        response = DiceRollResponse(values=[4, 2, 6], total=12, notation="3d6")
        formatted = dice_tool.format_result(response)

        assert "🎲" in formatted
        assert "3d6" in formatted
        assert "[4, 2, 6]" in formatted
        assert "**12**" in formatted

    @pytest.mark.asyncio
    async def test_safe_execute_success(self, dice_tool):
        """Test safe_execute returns proper success format."""
        result = await dice_tool.safe_execute(notation="2d6")

        assert "content" in result
        assert "isError" in result
        assert result["isError"] is False
        assert len(result["content"]) == 1
        assert result["content"][0]["type"] == "text"
        assert "🎲" in result["content"][0]["text"]

    @pytest.mark.asyncio
    async def test_safe_execute_error(self, dice_tool):
        """Test safe_execute returns proper error format."""
        result = await dice_tool.safe_execute(notation="invalid")

        assert "content" in result
        assert "isError" in result
        assert result["isError"] is True
        assert len(result["content"]) == 1
        assert result["content"][0]["type"] == "text"
        assert "Invalid input" in result["content"][0]["text"]

    @pytest.mark.asyncio
    async def test_roll_dice_case_insensitive(self, dice_tool):
        """Test dice notation is case insensitive."""
        result1 = await dice_tool.execute(notation="2D6")
        result2 = await dice_tool.execute(notation="2d6")

        # Both should work and produce valid results
        assert len(result1.values) == 2
        assert len(result2.values) == 2
        assert all(1 <= v <= 6 for v in result1.values)
        assert all(1 <= v <= 6 for v in result2.values)