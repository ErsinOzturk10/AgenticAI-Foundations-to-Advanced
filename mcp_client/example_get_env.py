"""Simple example: get environment variable.

Connects to the Everything MCP server and calls the "get-env" tool.
The get-env tool reads an environment variable from the server process.

Usage: python example_get_env.py
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
    """Connect and call get-env."""
    async with stdio_client(SERVER_PARAMS) as (read, write), ClientSession(read, write) as session:
        await session.initialize()
        logger.info("✅ Connected!")

        env_var = "PATH"
        logger.info("Reading environment variable: %s", env_var)

        result = await session.call_tool("get-env", arguments={"name": env_var})

        for content in result.content:
            if hasattr(content, "text"):
                logger.info("$%s = %s", env_var, content.text)


if __name__ == "__main__":
    asyncio.run(main())
