"""Simple RAG Engine.

A minimal Retrieval-Augmented Generation engine:
  - Stores documents as embeddings in memory
  - Uses sentence-transformers for embedding
  - Uses cosine similarity for retrieval
  - Returns top-k most relevant documents for a query.
"""

import logging

import numpy as np
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class RAGEngine:
    """In-memory RAG engine: embeddings, vector store and retrieval."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        """Initialize the RAG engine with a sentence-transformer model."""
        logger.info("Loading embedding model: %s...", model_name)
        self.model = SentenceTransformer(model_name)
        self.documents: list[str] = []
        self.embeddings: np.ndarray | None = None
        logger.info("Model loaded.")

    def add_documents(self, documents: list[str]) -> None:
        """Add documents to the vector store and compute embeddings."""
        self.documents.extend(documents)
        self.embeddings = self.model.encode(self.documents, convert_to_numpy=True)
        logger.info("Added %d documents. Total: %d", len(documents), len(self.documents))

    def query(self, question: str, top_k: int = 3) -> list[dict]:
        """Retrieve the top-k most relevant documents for the given question."""
        if not self.documents or self.embeddings is None:
            return []

        query_embedding = self.model.encode([question], convert_to_numpy=True)[0]
        scores = np.dot(self.embeddings, query_embedding) / (np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding))
        top_indices = np.argsort(scores)[::-1][:top_k]

        results = []
        for rank, idx in enumerate(top_indices, 1):
            results.append({"rank": rank, "score": float(scores[idx]), "document": self.documents[idx]})
        return results


# ============================================================
# Sample documents for demo purposes
# ============================================================
SAMPLE_DOCUMENTS = [
    "Python is a high-level programming language known for its simplicity and readability.",
    "Machine learning is a subset of artificial intelligence that enables systems to learn from data.",
    "Docker is a platform for developing, shipping, and running applications in containers.",
    "Kubernetes is an open-source container orchestration system for automating deployment and scaling.",
    "FastAPI is a modern Python web framework for building APIs with automatic documentation.",
    "PostgreSQL is a powerful open-source relational database management system.",
    "Redis is an in-memory data structure store used as a database, cache, and message broker.",
    "Git is a distributed version control system for tracking changes in source code.",
    "React is a JavaScript library for building user interfaces, maintained by Meta.",
    "Transformers are deep learning models that use self-attention mechanisms for NLP tasks.",
    "Vector databases store data as high-dimensional vectors for similarity search.",
    "RAG (Retrieval-Augmented Generation) combines information retrieval with text generation.",
    "LangChain is a framework for developing applications powered by large language models.",
    "MCP (Model Context Protocol) is a standard for connecting LLMs to external tools and data.",
    "Embeddings are numerical representations of text that capture semantic meaning.",
]
