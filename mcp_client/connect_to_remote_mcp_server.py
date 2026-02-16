"""MCP Client - Connecting to an External MCP Server.

This server uses the Model Context Protocol (MCP). Once connected, it:
  1. Lists available tools
  2. Lists available resources
  3. Lists available prompts
  4. Makes example tool calls

MCP Server used: @modelcontextprotocol/server-everything (test/demo server)
This server is automatically downloaded and launched via npx.

Requirements:
  - Python 3.10+
  - pip install mcp
  - Node.js and npm must be installed (for npx)

Usage:
  python connect_to_remote_mcp_server.py
"""

import asyncio
import json
import logging

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.shared.exceptions import McpError

# ============================================================
# MCP Server Configuration
# ============================================================
# "Everything" MCP Server - a test/demo server with many tools/resources/prompts
# Automatically downloaded and run via npx
SERVER_PARAMS = StdioServerParameters(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-everything"],
    env=None,  # Inherits environment variables from the parent process
)

logger = logging.getLogger(__name__)


def print_separator(title: str) -> None:
    """Log a section separator."""
    logger.info("\n%s", "=" * 60)
    logger.info("  %s", title)
    logger.info("%s\n", "=" * 60)


async def list_tools(session: ClientSession) -> list | None:
    """List the available tools on the server."""
    print_separator("AVAILABLE TOOLS")

    result = await session.list_tools()
    if not result.tools:
        logger.info("  No tools found.")
        return None

    for i, tool in enumerate(result.tools, 1):
        logger.info("  %d. %s", i, tool.name)
        if tool.description:
            logger.info("     Description: %s", tool.description)
        if tool.inputSchema:
            params = tool.inputSchema.get("properties", {})
            if params:
                param_names = list(params.keys())
                logger.info("     Parameters: %s", param_names)
        logger.info("")

    return result.tools


async def list_resources(session: ClientSession) -> list | None:
    """List the available resources on the server."""
    print_separator("AVAILABLE RESOURCES")

    result = await session.list_resources()
    if not result.resources:
        logger.info("  No resources found.")
        return None

    for i, resource in enumerate(result.resources, 1):
        logger.info("  %d. %s", i, resource.name)
        logger.info("     URI: %s", resource.uri)
        if resource.description:
            logger.info("     Description: %s", resource.description)
        logger.info("")

    return result.resources


async def list_prompts(session: ClientSession) -> list | None:
    """List the available prompts on the server."""
    print_separator("AVAILABLE PROMPTS")

    result = await session.list_prompts()
    if not result.prompts:
        logger.info("  No prompts found.")
        return None

    for i, prompt in enumerate(result.prompts, 1):
        logger.info("  %d. %s", i, prompt.name)
        if prompt.description:
            logger.info("     Description: %s", prompt.description)
        logger.info("")

    return result.prompts


async def call_tool_example(session: ClientSession) -> None:
    """Call a simple example tool (echo)."""
    print_separator("TOOL CALL EXAMPLE")

    tool_name = "echo"
    tool_args = {"message": "Hello MCP! This is a test message."}

    logger.info("  Tool: %s", tool_name)
    logger.info("  Arguments: %s", json.dumps(tool_args, ensure_ascii=False, indent=4))
    logger.info("")

    try:
        result = await session.call_tool(tool_name, arguments=tool_args)
        logger.info("  Result:")
        for content in result.content:
            logger.info("    - Type: %s", content.type)
            if hasattr(content, "text"):
                logger.info("      Text: %s", content.text)
        if result.isError:
            logger.warning("  ⚠️  Tool returned an error!")
    except McpError:
        logger.exception("Tool call failed.")


async def call_add_tool_example(session: ClientSession) -> None:
    """Call the math tool example (get-sum)."""
    print_separator("MATH TOOL CALL EXAMPLE")

    tool_name = "get-sum"
    tool_args = {"a": 42, "b": 58}

    logger.info("  Tool: %s", tool_name)
    logger.info("  Arguments: %s", json.dumps(tool_args, indent=4))
    logger.info("")

    try:
        result = await session.call_tool(tool_name, arguments=tool_args)
        logger.info("  Result:")
        for content in result.content:
            if hasattr(content, "text"):
                logger.info("    %s + %s = %s", tool_args["a"], tool_args["b"], content.text)
    except McpError:
        logger.exception("Math tool call failed.")


async def main() -> None:
    """Connect to the MCP server and perform example operations."""
    logger.info("\n%s", "🚀" * 20)
    logger.info("  MCP CLIENT - Connecting to an External MCP Server")
    logger.info("%s", "🚀" * 20)
    logger.info("\n  Server: @modelcontextprotocol/server-everything")
    logger.info("  Connection type: stdio (via npx)")
    logger.info("\n  Connecting...\n")

    try:
        async with stdio_client(SERVER_PARAMS) as (read_stream, write_stream), ClientSession(read_stream, write_stream) as session:
            init_result = await session.initialize()
            logger.info("  ✅ Connection established successfully!\n")

            print_separator("SERVER INFO")
            if init_result:
                server_info = getattr(init_result, "serverInfo", None)
                logger.info("  Server Name: %s", getattr(server_info, "name", "N/A"))
                logger.info("  Server Version: %s", getattr(server_info, "version", "N/A"))
                caps = getattr(init_result, "capabilities", None)
                if caps:
                    logger.info("  Capabilities:")
                    if getattr(caps, "tools", False):
                        logger.info("    - Tools: ✅")
                    if getattr(caps, "resources", False):
                        logger.info("    - Resources: ✅")
                    if getattr(caps, "prompts", False):
                        logger.info("    - Prompts: ✅")

            await list_tools(session)
            await list_resources(session)
            await list_prompts(session)

            await call_tool_example(session)
            await call_add_tool_example(session)

            print_separator("COMPLETED")
            logger.info("  ✅ All operations completed successfully!")
            logger.info("  💡 To use this client with a different MCP server, simply modify SERVER_PARAMS.\n")

    except FileNotFoundError:
        logger.exception("  ❌ ERROR: 'npx' command not found! Make sure Node.js and npm are installed.")
    except McpError:
        logger.exception("  ❌ MCP error occurred.")


if __name__ == "__main__":
    asyncio.run(main())
