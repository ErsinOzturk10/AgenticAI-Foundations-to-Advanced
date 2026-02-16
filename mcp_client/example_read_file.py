"""Simple example: read a file.

Connects to the Filesystem MCP server and reads a file.

Usage: python example_read_file.py
"""

import asyncio
import logging
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# The directory the server is allowed to access
ALLOWED_DIR = Path(__file__).resolve().parent.parent
PREVIEW_CHARS = 500

SERVER_PARAMS = StdioServerParameters(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-filesystem", str(ALLOWED_DIR)],
)

logger = logging.getLogger(__name__)


async def main() -> None:
    """Connect to filesystem MCP server and read a README.md file (demo)."""
    async with stdio_client(SERVER_PARAMS) as (read, write), ClientSession(read, write) as session:
        await session.initialize()
        logger.info("✅ Connected!")

        # Read the project's README.md
        file_path = ALLOWED_DIR / "README.md"
        logger.info("Reading: %s", file_path)

        result = await session.call_tool("read_file", arguments={"path": str(file_path)})

        for content in result.content:
            if hasattr(content, "text"):
                # Print first PREVIEW_CHARS characters
                preview = content.text[:PREVIEW_CHARS]
                logger.info("%s", preview)
                if len(content.text) > PREVIEW_CHARS:
                    logger.info("... (%d total characters)", len(content.text))


if __name__ == "__main__":
    asyncio.run(main())
