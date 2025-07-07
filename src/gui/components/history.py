"""History management component for interaction tracking."""

import streamlit as st

from ..models.gui_models import GUIInteraction


class HistoryManager:
    """Manages session history display and interaction."""

    def render(self) -> None:
        """Render interaction history interface."""
        history = st.session_state.gui_session.interaction_history

        if not history:
            st.info(
                "No interactions yet. Connect to a server and use tools to see history."
            )
            return

        # History controls
        col1, col2 = st.columns([1, 1])

        with col1:
            st.write(f"**Total Interactions:** {len(history)}")

        with col2:
            if st.button("Clear History"):
                st.session_state.gui_session.interaction_history = []
                st.rerun()

        # Display history
        for i, interaction in enumerate(reversed(history)):
            self._render_interaction(i, interaction)

    def _render_interaction(self, index: int, interaction: GUIInteraction) -> None:
        """Render a single interaction."""
        # Create expander with status indicator
        status_icon = "✅" if interaction.success else "❌"
        timestamp = interaction.timestamp.strftime("%H:%M:%S")

        with st.expander(
            f"{status_icon} {interaction.tool_name} - {timestamp}",
            expanded=index == 0,  # Expand latest interaction
        ):
            # Basic info
            col1, col2 = st.columns([1, 1])

            with col1:
                st.write(f"**Tool:** {interaction.tool_name}")
                st.write(
                    f"**Status:** {'Success' if interaction.success else 'Failed'}"
                )
                if interaction.execution_time:
                    st.write(f"**Execution Time:** {interaction.execution_time:.2f}s")

            with col2:
                timestamp_str = interaction.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                st.write(f"**Timestamp:** {timestamp_str}")
                if interaction.error_message:
                    st.write(f"**Error:** {interaction.error_message}")

            # Request/Response payloads
            req_col, resp_col = st.columns([1, 1])

            with req_col:
                st.subheader("Request")
                st.json(interaction.request_payload)

            with resp_col:
                st.subheader("Response")
                st.json(interaction.response_payload)
