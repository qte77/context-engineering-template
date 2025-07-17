"""Base tool interface and common patterns for MCP server tools."""

import logging
from abc import ABC, abstractmethod
from typing import Any

import httpx
from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)


class ToolError(Exception):
    """Base exception for tool-related errors."""

    def __init__(
        self, message: str, code: int = -1, data: dict[str, Any] | None = None
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.data = data or {}


class ValidationToolError(ToolError):
    """Exception for input validation errors."""

    def __init__(self, message: str, validation_errors: list | None = None):
        super().__init__(message, code=-32602)  # Invalid params error code
        self.validation_errors = validation_errors or []


class ExternalServiceError(ToolError):
    """Exception for external service errors."""

    def __init__(self, message: str, service_name: str, status_code: int | None = None):
        super().__init__(message, code=-32603)  # Internal error code
        self.service_name = service_name
        self.status_code = status_code


class BaseTool(ABC):
    """Abstract base class for all MCP server tools."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    @abstractmethod
    async def execute(self, **kwargs: Any) -> Any:
        """Execute the tool with the given arguments."""
        pass

    def validate_input(
        self, input_data: dict[str, Any], model_class: type[BaseModel]
    ) -> BaseModel:
        """Validate input data against a Pydantic model."""
        try:
            return model_class(**input_data)
        except ValidationError as e:
            error_messages = []
            for error in e.errors():
                field = " -> ".join(str(x) for x in error["loc"])
                message = error["msg"]
                error_messages.append(f"{field}: {message}")

            raise ValidationToolError(
                f"Invalid input for {self.name}: {'; '.join(error_messages)}",
                validation_errors=e.errors(),
            )

    def create_success_response(self, data: Any) -> dict[str, Any]:
        """Create a successful tool response."""
        return {
            "content": [
                {
                    "type": "text",
                    "text": str(data) if not isinstance(data, dict | list) else data,
                }
            ],
            "isError": False,
        }

    def create_error_response(self, error: Exception) -> dict[str, Any]:
        """Create an error tool response."""
        if isinstance(error, ToolError):
            error_message = error.message
        else:
            error_message = f"An unexpected error occurred: {str(error)}"

        # Log the full error for debugging
        self.logger.error(f"Tool {self.name} error: {error}", exc_info=True)

        return {
            "content": [
                {
                    "type": "text",
                    "text": error_message,
                }
            ],
            "isError": True,
        }

    async def safe_execute(self, **kwargs) -> dict[str, Any]:
        """Execute the tool with error handling."""
        try:
            result = await self.execute(**kwargs)
            return self.create_success_response(result)
        except Exception as e:
            return self.create_error_response(e)


class AsyncHttpMixin:
    """Mixin for tools that need HTTP client capabilities."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._http_client = None

    @property
    def http_client(self):
        """Get or create HTTP client."""
        if self._http_client is None:
            import httpx

            self._http_client = httpx.AsyncClient(
                timeout=30.0,
                headers={"User-Agent": "MCP-Server/1.0"},
            )
        return self._http_client

    async def cleanup(self):
        """Cleanup HTTP client resources."""
        if self._http_client:
            await self._http_client.aclose()
            self._http_client = None

    async def make_request(
        self, method: str, url: str, timeout: float = 10.0, **kwargs
    ) -> dict[str, Any]:
        """Make an HTTP request with error handling."""
        try:
            response = await self.http_client.request(
                method=method, url=url, timeout=timeout, **kwargs
            )
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            raise ExternalServiceError(
                f"Request to {url} timed out after {timeout} seconds",
                service_name="HTTP",
            )
        except httpx.HTTPStatusError as e:
            raise ExternalServiceError(
                f"HTTP error {e.response.status_code}: {e.response.text}",
                service_name="HTTP",
                status_code=e.response.status_code,
            )
        except Exception as e:
            raise ExternalServiceError(
                f"Failed to make request to {url}: {str(e)}",
                service_name="HTTP",
            )
