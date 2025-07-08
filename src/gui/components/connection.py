"""Connection management component for MCP server."""

import asyncio
import logging

import streamlit as st

from src.mcp_client.client import MCPClient

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
            tools = ', '.join(st.session_state.gui_session.available_tools)
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
                # Handle async in Streamlit
                client = MCPClient(server_path)
                
                # Check if there's already an event loop running
                try:
                    loop = asyncio.get_running_loop()
                    # If there's already a loop, we need to use a different approach
                    import threading
                    import concurrent.futures
                    
                    def run_in_thread():
                        return asyncio.run(client.connect())
                    
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(run_in_thread)
                        future.result()  # Wait for completion
                        
                except RuntimeError:
                    # No event loop running, use asyncio.run
                    asyncio.run(client.connect())

                st.session_state.mcp_client = client
                st.session_state.gui_session.connected = True
                st.session_state.gui_session.server_path = server_path
                st.session_state.gui_session.available_tools = client.available_tools

                st.success("Connected successfully!")
                st.rerun()

        except Exception as e:
            logger.error(f"Connection failed: {e}")
            st.error(f"Connection failed: {str(e)}")

    def _disconnect(self) -> None:
        """Disconnect from MCP server."""
        if st.session_state.mcp_client:
            try:
                # Handle async in Streamlit
                try:
                    loop = asyncio.get_running_loop()
                    import threading
                    import concurrent.futures
                    
                    def run_in_thread():
                        return asyncio.run(st.session_state.mcp_client.disconnect())
                    
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(run_in_thread)
                        future.result()  # Wait for completion
                        
                except RuntimeError:
                    # No event loop running, use asyncio.run
                    asyncio.run(st.session_state.mcp_client.disconnect())
                
                st.session_state.mcp_client = None
                st.session_state.gui_session.connected = False
                st.session_state.gui_session.available_tools = []
                st.success("Disconnected successfully!")
                st.rerun()
            except Exception as e:
                logger.error(f"Disconnect failed: {e}")
                st.error(f"Disconnect failed: {str(e)}")

    def _perform_health_check(self) -> None:
        """Perform health check on connection."""
        if st.session_state.mcp_client:
            try:
                # Handle async in Streamlit
                try:
                    loop = asyncio.get_running_loop()
                    import threading
                    import concurrent.futures
                    
                    def run_in_thread():
                        return asyncio.run(st.session_state.mcp_client.health_check())
                    
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(run_in_thread)
                        health = future.result()  # Wait for completion
                        
                except RuntimeError:
                    # No event loop running, use asyncio.run
                    health = asyncio.run(st.session_state.mcp_client.health_check())
                
                if health:
                    st.success("Health check passed!")
                else:
                    st.warning("Health check failed - connection may be unhealthy")
            except Exception as e:
                logger.error(f"Health check error: {e}")
                st.error(f"Health check error: {str(e)}")
