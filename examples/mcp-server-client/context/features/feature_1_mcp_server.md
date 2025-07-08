# Feature description for: MCP Server with tools

## FEATURE

Implement an **MCP (Message Control Protocol) Server** in Python that exposes three callable tools via structured messages. The server should receive well-formed MCP messages and dispatch tool invocations accordingly. The three tools to be exposed are:

1. **Roll Dice**: Accepts a format like `2d6` or `1d20` and returns the rolled values and total.
2. **Get Weather**: Accepts a city name or coordinates and returns the current weather conditions using a public weather API.
3. **Get Date**: Returns the current date and time in ISO 8601 format or based on a requested timezone.

The server should be modular, testable, and extensible for future tools. Logging, error handling, and message validation should be considered first-class concerns.

## EXAMPLES

Located in `/context/examples`:

* `roll_dice_example.json`: Demonstrates sending `{"tool": "roll_dice", "args": {"notation": "3d6"}}` and receiving `{"result": {"values": [4,2,6], "total": 12}}`.
* `get_weather_example.json`: Sends `{"tool": "get_weather", "args": {"location": "San Francisco"}}` and expects weather data such as temperature, condition, and wind speed.
* `get_date_example.json`: Sends `{"tool": "get_date", "args": {"timezone": "UTC"}}` and receives `{"result": "2025-07-06T16:22:00Z"}`.

These examples cover correct usage and malformed inputs to validate tool response and error handling.

## DOCUMENTATION

* [Open-Meteo API](https://open-meteo.com/en/docs): For retrieving weather information.
* [Python `datetime` module](https://docs.python.org/3/library/datetime.html): For implementing date and time tool.
* [random module (Python)](https://docs.python.org/3/library/random.html): For rolling dice.
* \[MCP Protocol Overview (proprietary/internal if applicable)] or general protocol documentation, if using a specific spec.

Additional context from [context-engineering-intro](https://github.com/qte77/context-engineering-template) will inform message structure and processing strategy.

## OTHER CONSIDERATIONS

* **Tool routing logic** should be clearly separated to allow clean expansion.
* **Input validation** is critical: especially for `roll_dice`, invalid formats (e.g., `3x5`, `0d6`, `d10`) must return informative errors.
* **Weather API failures or rate limits** should be gracefully handled with fallback messages.
* **Timezone parsing** for `get_date` should use `pytz` or `zoneinfo`, and clearly inform users when timezones are unsupported.
* **Security note**: Weather and date APIs should not expose sensitive request metadata or leak internal server details in errors.
* AI coding assistants often:

  * Miss edge case handling (e.g., zero dice, negative sides)
  * Forget to structure results consistently across tools
  * Fail to modularize tool logic, making future expansion difficult
