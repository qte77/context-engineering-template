"""Tool-specific form components for MCP tools."""

import asyncio
import logging
import re
import time

import streamlit as st

from src.gui.models.gui_models import GUIInteraction

logger = logging.getLogger(__name__)


class ToolForms:
    """Manages tool-specific form interfaces."""

    def render(self) -> None:
        """Render tool selection and forms."""
        available_tools = st.session_state.gui_session.available_tools

        if not available_tools:
            st.warning("No tools available")
            return

        # Tool selection
        selected_tool = st.selectbox(
            "Select Tool", options=available_tools, help="Choose a tool to invoke"
        )

        # Tool-specific forms
        if selected_tool == "roll_dice":
            self._render_dice_form()
        elif selected_tool == "get_weather":
            self._render_weather_form()
        elif selected_tool == "get_date":
            self._render_date_form()

    def _render_dice_form(self) -> None:
        """Render dice rolling form."""
        with st.form("dice_form"):
            st.subheader("🎲 Roll Dice")

            notation = st.text_input(
                "Dice Notation",
                value="2d6",
                help="Enter dice notation (e.g., 2d6, 1d20, 3d10)",
            )

            # Help text with examples
            st.caption("Examples: 1d20 (single 20-sided die), 3d6 (three 6-sided dice)")

            submitted = st.form_submit_button("Roll Dice")

            if submitted:
                if self._validate_dice_notation(notation):
                    self._execute_tool("roll_dice", {"notation": notation})
                else:
                    st.error("Invalid dice notation. Use format like '2d6' or '1d20'")

    def _render_weather_form(self) -> None:
        """Render weather lookup form."""
        with st.form("weather_form"):
            st.subheader("🌤️ Get Weather")

            location = st.text_input(
                "Location",
                value="San Francisco",
                help="Enter city name or coordinates (lat,lon)",
            )

            # Common location examples
            st.caption("Examples: London, New York, 37.7749,-122.4194")

            submitted = st.form_submit_button("Get Weather")

            if submitted:
                if location.strip():
                    self._execute_tool("get_weather", {"location": location})
                else:
                    st.error("Please enter a location")

    def _render_date_form(self) -> None:
        """Render date/time lookup form."""
        with st.form("date_form"):
            st.subheader("🕐 Get Date & Time")

            timezone = st.selectbox(
                "Timezone",
                options=[
                    "UTC",
                    "America/New_York",
                    "America/Los_Angeles",
                    "Europe/London",
                    "Asia/Tokyo",
                    "Australia/Sydney",
                ],
                help="Select timezone or enter custom IANA timezone",
            )

            custom_timezone = st.text_input(
                "Custom Timezone (optional)",
                placeholder="e.g., America/Chicago",
                help="Enter custom IANA timezone identifier",
            )

            submitted = st.form_submit_button("Get Date & Time")

            if submitted:
                tz = custom_timezone.strip() if custom_timezone.strip() else timezone
                self._execute_tool("get_date", {"timezone": tz})

    def _execute_tool(self, tool_name: str, arguments: dict[str, str]) -> None:
        """Execute tool and update GUI state."""
        if not st.session_state.mcp_client:
            st.error("Not connected to server")
            return

        try:
            with st.spinner(f"Executing {tool_name}..."):
                # Time execution for performance metrics
                start_time = time.time()

                # Use existing MCP client - handle async in Streamlit
                try:
                    loop = asyncio.get_running_loop()
                    import threading
                    import concurrent.futures
                    
                    def run_in_thread():
                        return asyncio.run(
                            st.session_state.mcp_client.invoke_tool(tool_name, arguments)
                        )
                    
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(run_in_thread)
                        result = future.result()  # Wait for completion
                        
                except RuntimeError:
                    # No event loop running, use asyncio.run
                    result = asyncio.run(
                        st.session_state.mcp_client.invoke_tool(tool_name, arguments)
                    )

                execution_time = time.time() - start_time

                # Create interaction record
                interaction = GUIInteraction(
                    tool_name=tool_name,
                    arguments=arguments,
                    request_payload={"tool": tool_name, "arguments": arguments},
                    response_payload=result.model_dump(),
                    success=result.success,
                    error_message=result.error if not result.success else None,
                    execution_time=execution_time,
                )

                # Update session state
                st.session_state.gui_session.interaction_history.append(interaction)

                # Display result
                if result.success:
                    st.success(f"✅ {tool_name} executed successfully!")
                    st.json(result.model_dump())
                else:
                    st.error(f"❌ {tool_name} failed: {result.error}")

                st.rerun()

        except Exception as e:
            logger.error(f"Tool execution error: {e}")
            st.error(f"Execution error: {str(e)}")

    def _validate_dice_notation(self, notation: str) -> bool:
        """Validate dice notation format."""
        pattern = r"^(\d+)d(\d+)$"
        return bool(re.match(pattern, notation.strip().lower()))
