"""Simple example: list all tools.

Connects to the Everything MCP server and prints every available tool
along with its description and parameters.

Usage: python example_list_tools.py
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
    """Connect and list all tools."""
    async with stdio_client(SERVER_PARAMS) as (read, write), ClientSession(read, write) as session:
        await session.initialize()
        logger.info("✅ Connected!")

        # List all tools
        result = await session.list_tools()

        logger.info("Found %d tools:", len(result.tools))
        for i, tool in enumerate(result.tools, 1):
            logger.info("  %d. %s", i, tool.name)
            if tool.description:
                logger.info("     → %s", tool.description)


if __name__ == "__main__":
    asyncio.run(main())
