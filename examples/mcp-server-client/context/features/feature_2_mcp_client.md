# Feature description for: MCP Client for Tool Invocation

## FEATURE

Implement a **Python-based MCP Client** capable of sending structured requests to an MCP Server and handling the corresponding responses. The client should:

* Connect to the MCP server over a socket, HTTP, or another configured protocol.
* Serialize requests into the expected MCP message format (e.g., JSON or line-based protocol).
* Provide a command-line interface (CLI) and/or programmatic interface for interacting with the following tools:

  1. **Roll Dice** (`roll_dice`) – accepts dice notation like `2d6`, `1d20`.
  2. **Get Weather** (`get_weather`) – accepts a location name or coordinates.
  3. **Get Date** (`get_date`) – optionally accepts a timezone.

The client should also handle connection errors, invalid tool responses, and retry logic gracefully.

## EXAMPLES

Located in `/context/examples`:

* `client_roll_dice_input.json`: `{ "tool": "roll_dice", "args": { "notation": "2d6" } }`
* `client_get_weather_input.json`: `{ "tool": "get_weather", "args": { "location": "Berlin" } }`
* `client_get_date_input.json`: `{ "tool": "get_date", "args": { "timezone": "UTC" } }`
* `client_invalid_tool.json`: `{ "tool": "fly_to_mars", "args": {} }` → Should trigger a meaningful error from the server

These example requests and expected responses can be used for local testing and automated integration checks.

## DOCUMENTATION

* [Python `socket` module](https://docs.python.org/3/library/socket.html) or [requests](https://docs.python.org/3/library/urllib.request.html) depending on transport.
* [JSON module](https://docs.python.org/3/library/json.html) for message formatting.
* [argparse](https://docs.python.org/3/library/argparse.html) for implementing a simple CLI wrapper.
* Reference the MCP Server protocol spec or internal documentation (e.g. *MCP Protocol Overview* if proprietary).
* [context-engineering-template](https://github.com/qte/context-engineering-template) for usage conventions.

## OTHER CONSIDERATIONS

* Client must validate outgoing messages before sending to avoid malformed requests.
* Handle connection errors, timeouts, and retries in a user-friendly manner.
* The response handler should check for required fields (`result`, `error`, etc.) to avoid crashes on malformed server responses.
* Consider pluggability of tools so future expansions can be supported with minimal refactoring.
* AI assistants often:

  * Miss error handling around partial or no server responses.
  * Forget to properly close socket connections or handle timeouts.
  * Write overly rigid request builders, making CLI usage frustrating.
