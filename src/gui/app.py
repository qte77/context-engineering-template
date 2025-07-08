"""Main Streamlit application for MCP Tool Showcase."""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st

from src.gui.components.connection import ConnectionManager
from src.gui.components.history import HistoryManager
from src.gui.components.tool_forms import ToolForms
from src.gui.models.gui_models import GUISession


def main() -> None:
    """Main Streamlit application entry point."""
    st.set_page_config(
        page_title="MCP Tool Showcase",
        page_icon="🛠️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Initialize session state
    if "gui_session" not in st.session_state:
        st.session_state.gui_session = GUISession()

    if "mcp_client" not in st.session_state:
        st.session_state.mcp_client = None

    # Main layout with sidebar
    with st.sidebar:
        st.title("🛠️ MCP Tool Showcase")
        st.markdown("---")

        # Connection management
        connection_manager = ConnectionManager()
        connection_manager.render()

    # Main content area
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("Tool Invocation")
        if st.session_state.gui_session.connected:
            tool_forms = ToolForms()
            tool_forms.render()
        else:
            st.info("Please connect to the MCP server first")

    with col2:
        st.header("Request/Response")
        if st.session_state.gui_session.interaction_history:
            latest_interaction = st.session_state.gui_session.interaction_history[-1]
            st.subheader("Latest Request")
            st.json(latest_interaction.request_payload)
            st.subheader("Latest Response")
            st.json(latest_interaction.response_payload)
        else:
            st.info("No interactions yet")

    # History section
    st.header("Interaction History")
    history_manager = HistoryManager()
    history_manager.render()


if __name__ == "__main__":
    main()
