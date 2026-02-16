"""RAG MCP Server.

An MCP server that exposes a RAG system as tools:
  - rag_query: Search documents using natural language.
  - rag_add_document: Add a new document to the knowledge base.
  - rag_list_documents: List all documents in the knowledge base.
"""

import logging

from mcp.server.fastmcp import FastMCP
from rag_engine import SAMPLE_DOCUMENTS, RAGEngine

logger = logging.getLogger(__name__)

# ---- Initialize RAG engine ----
logger.info("Initializing RAG Engine...")
rag = RAGEngine()
rag.add_documents(SAMPLE_DOCUMENTS)
logger.info("RAG Engine initialized.")

# ---- Create MCP server ----
server = FastMCP(
    name="RAG MCP Server",
    host="localhost",
    port=8001,
)


@server.tool()
def rag_query(question: str, top_k: int = 3) -> str:
    """Search the knowledge base using a natural language question."""
    results = rag.query(question, top_k=top_k)

    if not results:
        return "No documents found in the knowledge base."

    output = f"Query: {question}\n"
    output += f"Top {len(results)} results:\n\n"

    for r in results:
        output += f"  #{r['rank']} [score: {r['score']:.4f}]\n"
        output += f"  {r['document']}\n\n"

    return output


@server.tool()
def rag_add_document(document: str) -> str:
    """Add a new document to the knowledge base."""
    rag.add_documents([document])
    return f"✅ Document added. Total documents: {len(rag.documents)}"


@server.tool()
def rag_list_documents() -> str:
    """List all documents currently in the knowledge base."""
    if not rag.documents:
        return "Knowledge base is empty."

    output = f"Knowledge base ({len(rag.documents)} documents):\n\n"
    for i, doc in enumerate(rag.documents, 1):
        output += f"  {i}. {doc}\n"

    return output


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    # use module logger for messages
    logger.info("🚀 Starting RAG MCP Server...")
    logger.info("   Host: localhost")
    logger.info("   Port: 8001")
    logger.info("   Transport: SSE")
    logger.info("   Documents loaded: %d", len(rag.documents))
    logger.info("\n   Press Ctrl+C to stop.\n")
    server.run(transport="sse")
