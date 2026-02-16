"""Orchestrator Agent.

Receive a user query, delegate work to two sub-agents, and combine results into a final answer.
"""

import logging

import research_agent
import writer_agent
from langchain_ollama import ChatOllama

logger = logging.getLogger(__name__)

llm = ChatOllama(model="gpt-oss:latest", temperature=0)

ROUTING_PROMPT = """You are an Orchestrator Agent. Given a user query, decide if it needs:
1. "research_and_write" — needs factual research then a written response (most queries)
2. "direct" — a simple greeting or trivial question that needs no research

Respond with ONLY one word: either "research_and_write" or "direct".
"""


class Orchestrator:
    """Orchestrate two sub-agents: Research Agent and Writer Agent."""

    def run(self, query: str) -> dict:
        """Process a user query through the multi-agent pipeline and return results."""
        logger.info("%s", "=" * 60)
        logger.info("  🎯 Orchestrator: Received query")
        logger.info('     "%s"', query)
        logger.info("%s\n", "=" * 60)

        # Step 1: Decide routing
        route = self._decide_route(query)
        logger.info("  📋 Orchestrator: Route → %s", route)

        if route == "direct":
            response = self._direct_response(query)
            return {"query": query, "route": "direct", "research": None, "response": response}

        # Step 2: Call Research Agent
        logger.info("%s", "-" * 40)
        logger.info("  Step 1/2: Calling Research Agent")
        logger.info("%s", "-" * 40)
        research = research_agent.run(query)

        # Step 3: Call Writer Agent with research findings
        logger.info("%s", "-" * 40)
        logger.info("  Step 2/2: Calling Writer Agent")
        logger.info("%s", "-" * 40)
        response = writer_agent.run(query, research)

        logger.info("  ✅ Orchestrator: All agents finished.")
        return {"query": query, "route": "research_and_write", "research": research, "response": response}

    def _decide_route(self, query: str) -> str:
        """Decide routing using the local LLM and return the route string."""
        messages = [{"role": "system", "content": ROUTING_PROMPT}, {"role": "user", "content": query}]
        response = llm.invoke(messages)
        route = response.content.strip().lower()
        if route not in ("research_and_write", "direct"):
            route = "research_and_write"
        return route

    def _direct_response(self, query: str) -> str:
        """Return a direct short response for trivial queries."""
        messages = [{"role": "system", "content": "You are a friendly assistant. Answer briefly."}, {"role": "user", "content": query}]
        response = llm.invoke(messages)
        return response.content


# CLI usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    orch = Orchestrator()
    logger.info("\n🤖 Multi-Agent Orchestrator (type 'quit' to exit)\n")

    while True:
        query = input("You: ").strip()
        if query.lower() in ("quit", "exit", "q"):
            logger.info("\n👋 Goodbye!\n")
            break
        if not query:
            continue

        result = orch.run(query)
        if result["research"]:
            logger.info("\n📊 Research Findings:\n%s", result["research"])

        logger.info("\n📝 Final Response:\n%s\n", result["response"])
