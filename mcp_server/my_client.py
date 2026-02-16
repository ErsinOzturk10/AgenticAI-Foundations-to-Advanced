"""Custom MCP Client.

Connects to our custom MCP server (my_server.py) via SSE and demonstrates:
  1. Listing available tools
  2. Calling each tool

Prerequisites:
  - Start the server first in a separate terminal:
      python my_server.py
  - Then run this client:
      python my_client.py
"""

import asyncio
import logging

from mcp import ClientSession
from mcp.client.sse import sse_client

logger = logging.getLogger(__name__)

SERVER_URL = "http://localhost:8000/sse"


def print_separator(title: str) -> None:
    """Log a visual section separator."""
    logger.info("\n%s", "=" * 60)
    logger.info("  %s", title)
    logger.info("%s\n", "=" * 60)


async def main() -> None:  # noqa: C901
    """Connect to the MCP server, list tools and call example tools."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger.info("\n🔌 Connecting to My Custom MCP Server...")
    logger.info("   URL: %s\n", SERVER_URL)

    async with sse_client(SERVER_URL) as (read, write), ClientSession(read, write) as session:
        init_result = await session.initialize()
        logger.info("✅ Connected to: %s v%s\n", getattr(init_result.serverInfo, "name", "N/A"), getattr(init_result.serverInfo, "version", "N/A"))

        # ---- Step 1: List all tools ----
        print_separator("AVAILABLE TOOLS")
        tools_result = await session.list_tools()
        for i, tool in enumerate(tools_result.tools, 1):
            logger.info("  %d. %s", i, tool.name)
            logger.info("     %s", tool.description or "")
            if tool.inputSchema:
                props = tool.inputSchema.get("properties", {})
                if props:
                    params = list(props.keys())
                    logger.info("     Parameters: %s", params)
            logger.info("")

        # ---- Step 2: Call "greet" ----
        print_separator("TOOL CALL: greet")
        result = await session.call_tool("greet", arguments={"name": "Alice"})
        for content in result.content:
            if hasattr(content, "text"):
                logger.info("  %s", content.text)

        # ---- Step 3: Call "add" ----
        print_separator("TOOL CALL: add")
        result = await session.call_tool("add", arguments={"a": 15, "b": 27})
        for content in result.content:
            if hasattr(content, "text"):
                logger.info("  %s", content.text)

        # ---- Step 4: Call "multiply" ----
        print_separator("TOOL CALL: multiply")
        result = await session.call_tool("multiply", arguments={"a": 6, "b": 7})
        for content in result.content:
            if hasattr(content, "text"):
                logger.info("  %s", content.text)

        # ---- Step 5: Call "current_time" ----
        print_separator("TOOL CALL: current_time")
        result = await session.call_tool("current_time", arguments={})
        for content in result.content:
            if hasattr(content, "text"):
                logger.info("  %s", content.text)

        print_separator("DONE")
        logger.info("  ✅ All tool calls completed successfully!\n")


if __name__ == "__main__":
    asyncio.run(main())
