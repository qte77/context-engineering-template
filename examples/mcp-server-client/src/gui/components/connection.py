"""Connection management component for MCP server."""

import logging

import streamlit as st

from src.gui.utils.mcp_wrapper import MCPConnectionManager

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages MCP server connection in GUI."""

    def render(self) -> None:
        """Render connection management interface."""
        st.subheader("Connection Status")

        # Display current status
        if st.session_state.gui_session.connected:
            st.success("✅ Connected to MCP Server")
            st.write(f"Server: {st.session_state.gui_session.server_path}")
            tools = ", ".join(st.session_state.gui_session.available_tools)
            st.write(f"Available Tools: {tools}")

            # Health check button
            if st.button("Health Check"):
                self._perform_health_check()

            # Disconnect button
            if st.button("Disconnect"):
                self._disconnect()
        else:
            st.error("❌ Not Connected")

            # Connection form
            server_path = st.text_input(
                "Server Path",
                value=st.session_state.gui_session.server_path,
                help="Path to MCP server script",
            )

            if st.button("Connect"):
                self._connect(server_path)

    def _connect(self, server_path: str) -> None:
        """Connect to MCP server."""
        try:
            with st.spinner("Connecting to server..."):
                # Create connection manager if it doesn't exist
                if "mcp_connection_manager" not in st.session_state:
                    st.session_state.mcp_connection_manager = MCPConnectionManager()

                manager = st.session_state.mcp_connection_manager

                # Connect to server
                success = manager.connect(server_path)

                if success:
                    st.session_state.gui_session.connected = True
                    st.session_state.gui_session.server_path = server_path
                    st.session_state.gui_session.available_tools = (
                        manager.available_tools
                    )

                    st.success("Connected successfully!")
                    st.rerun()
                else:
                    st.error("Failed to connect to server")

        except Exception as e:
            logger.error(f"Connection failed: {e}")
            st.error(f"Connection failed: {str(e)}")

    def _disconnect(self) -> None:
        """Disconnect from MCP server."""
        if "mcp_connection_manager" in st.session_state:
            try:
                manager = st.session_state.mcp_connection_manager
                manager.disconnect()

                st.session_state.gui_session.connected = False
                st.session_state.gui_session.available_tools = []
                st.success("Disconnected successfully!")
                st.rerun()
            except Exception as e:
                logger.error(f"Disconnect failed: {e}")
                st.error(f"Disconnect failed: {str(e)}")

    def _perform_health_check(self) -> None:
        """Perform health check on connection."""
        if "mcp_connection_manager" in st.session_state:
            try:
                manager = st.session_state.mcp_connection_manager
                health = manager.health_check()

                if health:
                    st.success("Health check passed!")
                else:
                    st.warning("Health check failed - connection may be unhealthy")
            except Exception as e:
                logger.error(f"Health check error: {e}")
                st.error(f"Health check error: {str(e)}")
