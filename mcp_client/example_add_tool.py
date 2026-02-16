"""Simple example: get-sum tool.

Connects to the Everything MCP server and calls the "get-sum" tool.
The get-sum tool takes two numbers and returns their sum.

Usage: python example_add_tool.py
"""

import asyncio
import logging

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

logger = logging.getLogger(__name__)

SERVER_PARAMS = StdioServerParameters(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-everything"],
)


async def main() -> None:
    """Connect and call get-sum."""
    async with stdio_client(SERVER_PARAMS) as (read, write), ClientSession(read, write) as session:
        await session.initialize()
        logger.info("✅ Connected!")

        # Call the get-sum tool with two numbers
        a, b = 42, 58
        result = await session.call_tool("get-sum", arguments={"a": a, "b": b})

        for content in result.content:
            if hasattr(content, "text"):
                logger.info("%s + %s = %s", a, b, content.text)


if __name__ == "__main__":
    asyncio.run(main())
