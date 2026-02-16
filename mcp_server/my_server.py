"""Custom MCP Server.

A simple MCP server that exposes the following tools:
  - greet: Return a greeting message.
  - add: Add two numbers.
  - multiply: Multiply two numbers.
  - current_time: Return the current date and time.

Run this server in one terminal:
  python my_server.py

Then connect to it from another terminal using my_client.py.
"""

import logging
from datetime import UTC, datetime

from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)

# Create the server
server = FastMCP(
    name="My Custom MCP Server",
    host="localhost",
    port=8000,
)


@server.tool()
def greet(name: str) -> str:
    """Return a friendly greeting message for the given name."""
    return f"Hello, {name}! Welcome to our custom MCP server. 👋"


@server.tool()
def add(a: float, b: float) -> str:
    """Add two numbers and return the result."""
    result = a + b
    return f"{a} + {b} = {result}"


@server.tool()
def multiply(a: float, b: float) -> str:
    """Multiply two numbers and return the result."""
    result = a * b
    return f"{a} * {b} = {result}"


@server.tool()
def current_time() -> str:
    """Return the current date and time in UTC."""
    now = datetime.now(tz=UTC)
    return f"Current date and time (UTC): {now.strftime('%Y-%m-%d %H:%M:%S')}"


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger.info("🚀 Starting My Custom MCP Server...")
    logger.info("   Host: localhost")
    logger.info("   Port: 8000")
    logger.info("   Transport: SSE")
    logger.info("\n   Press Ctrl+C to stop.\n")
    server.run(transport="sse")
