"""RAG MCP Client.

Connect to the RAG MCP server and demonstrate queries, adding documents and listing.
"""

import asyncio
import logging

from mcp import ClientSession
from mcp.client.sse import sse_client

logger = logging.getLogger(__name__)
SERVER_URL = "http://localhost:8001/sse"


def print_separator(title: str) -> None:
    """Log a visual section separator."""
    logger.info("\n%s", "=" * 60)
    logger.info("  %s", title)
    logger.info("%s\n", "=" * 60)


async def main() -> None:  # noqa: C901, PLR0912
    """Connect to the RAG MCP server and demonstrate RAG tool usage."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger.info("🔌 Connecting to RAG MCP Server...")
    logger.info("   URL: %s", SERVER_URL)

    async with sse_client(SERVER_URL) as (read, write), ClientSession(read, write) as session:
        init_result = await session.initialize()
        logger.info("✅ Connected to: %s v%s", getattr(init_result.serverInfo, "name", "N/A"), getattr(init_result.serverInfo, "version", "N/A"))

        # ---- Step 1: List tools ----
        print_separator("AVAILABLE TOOLS")
        tools_result = await session.list_tools()
        for i, tool in enumerate(tools_result.tools, 1):
            logger.info("  %d. %s", i, tool.name)
            logger.info("     %s", tool.description or "")
            logger.info("")

        # ---- Step 2: Query about Python ----
        print_separator("QUERY: 'What is Python?'")
        result = await session.call_tool("rag_query", arguments={"question": "What is Python?", "top_k": 3})
        for content in result.content:
            if hasattr(content, "text"):
                logger.info("%s", content.text)

        # ---- Step 3: Query about containers ----
        print_separator("QUERY: 'How do containers work?'")
        result = await session.call_tool("rag_query", arguments={"question": "How do containers work?", "top_k": 3})
        for content in result.content:
            if hasattr(content, "text"):
                logger.info("%s", content.text)

        # ---- Step 4: Query about RAG ----
        print_separator("QUERY: 'What is RAG and how does it work?'")
        result = await session.call_tool("rag_query", arguments={"question": "What is RAG and how does it work?", "top_k": 3})
        for content in result.content:
            if hasattr(content, "text"):
                logger.info("%s", content.text)

        # ---- Step 5: Add a new document ----
        print_separator("ADDING A NEW DOCUMENT")
        new_doc = "Streamlit is a Python framework for building interactive data science web applications quickly."
        logger.info("  Adding: %s", new_doc)
        result = await session.call_tool("rag_add_document", arguments={"document": new_doc})
        for content in result.content:
            if hasattr(content, "text"):
                logger.info("  %s", content.text)

        # ---- Step 6: Query for the new document ----
        print_separator("QUERY: 'How to build data science web apps?'")
        result = await session.call_tool("rag_query", arguments={"question": "How to build data science web apps?", "top_k": 3})
        for content in result.content:
            if hasattr(content, "text"):
                logger.info("%s", content.text)

        # ---- Step 7: List all documents ----
        print_separator("ALL DOCUMENTS IN KNOWLEDGE BASE")
        result = await session.call_tool("rag_list_documents", arguments={})
        for content in result.content:
            if hasattr(content, "text"):
                logger.info("%s", content.text)

        print_separator("DONE")
        logger.info("  ✅ All RAG operations completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
