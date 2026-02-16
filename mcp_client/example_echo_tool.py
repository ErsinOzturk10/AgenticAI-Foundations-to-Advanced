"""Simple example: echo tool.

Connects to the Everything MCP server and calls the "echo" tool.
The echo tool simply returns the message you send it.

Usage: python example_echo_tool.py
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
    """Connect and call echo."""
    async with stdio_client(SERVER_PARAMS) as (read, write), ClientSession(read, write) as session:
        await session.initialize()
        logger.info("✅ Connected!")

        # Call the echo tool
        result = await session.call_tool("echo", arguments={"message": "Hello MCP!"})

        for content in result.content:
            if hasattr(content, "text"):
                logger.info("Echo response: %s", content.text)


if __name__ == "__main__":
    asyncio.run(main())
