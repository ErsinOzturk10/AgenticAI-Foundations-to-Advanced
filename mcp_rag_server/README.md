# RAG System via MCP Server

A RAG (Retrieval-Augmented Generation) system exposed as an MCP server.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Terminal 1 — Start the RAG server

```bash
python rag_server.py
```

The server loads 15 sample documents into an in-memory vector store and starts listening on `localhost:8001`.

### Terminal 2 — Run the client

```bash
python rag_client.py
```

## Architecture

```
┌─────────────┐         SSE          ┌─────────────────┐
│  rag_client  │ ◄──────────────────► │   rag_server     │
│  (MCP Client)│                      │   (MCP Server)   │
└─────────────┘                       │                   │
                                      │  ┌─────────────┐ │
                                      │  │  rag_engine  │ │
                                      │  │  - Embeddings│ │
                                      │  │  - Vector DB │ │
                                      │  │  - Retriever │ │
                                      │  └─────────────┘ │
                                      └─────────────────┘
```

## MCP Tools

| Tool | Parameters | Description |
|------|-----------|-------------|
| `rag_query` | `question` (str), `top_k` (int) | Search the knowledge base with a natural language question |
| `rag_add_document` | `document` (str) | Add a new document to the knowledge base |
| `rag_list_documents` | — | List all documents in the knowledge base |

## Files

| File | Description |
|------|-------------|
| `rag_engine.py` | RAG engine: embeddings, vector store, retrieval |
| `rag_server.py` | MCP server that wraps the RAG engine as tools |
| `rag_client.py` | MCP client that connects and calls RAG tools |
