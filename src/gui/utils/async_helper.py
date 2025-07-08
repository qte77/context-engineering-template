"""Async helper utilities for Streamlit GUI."""

import asyncio
import threading
from typing import Any, Awaitable, Callable, TypeVar

T = TypeVar('T')


def run_async(coro: Awaitable[T]) -> T:
    """Run an async function in Streamlit context.
    
    This handles the case where Streamlit might already have an event loop running.
    
    Args:
        coro: The coroutine to run
        
    Returns:
        The result of the coroutine
    """
    try:
        # Try to get the current event loop
        loop = asyncio.get_running_loop()
        
        # If we're already in an event loop, we need to run in a new thread
        # with its own event loop
        result = None
        exception = None
        
        def run_in_new_loop():
            nonlocal result, exception
            try:
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                try:
                    result = new_loop.run_until_complete(coro)
                finally:
                    new_loop.close()
            except Exception as e:
                exception = e
        
        thread = threading.Thread(target=run_in_new_loop)
        thread.start()
        thread.join()
        
        if exception:
            raise exception
        return result
        
    except RuntimeError:
        # No event loop running, can use asyncio.run directly
        return asyncio.run(coro)


class AsyncContextManager:
    """Helper to manage async context across multiple calls."""
    
    def __init__(self):
        self._client = None
        self._loop = None
        self._thread = None
        
    def run_async(self, coro: Awaitable[T]) -> T:
        """Run async function maintaining context."""
        return run_async(coro)