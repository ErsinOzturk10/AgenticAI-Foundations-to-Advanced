"""Writer Agent (Sub-Agent 2).

Role: Take research findings and transform them into a well-written, polished response.
This agent focuses on clear communication and good structure.
"""

import logging

from langchain_ollama import ChatOllama

llm = ChatOllama(model="gpt-oss:latest", temperature=0.7)

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a Writer Agent. Your job is to:
1. Take research findings provided to you
2. Transform them into a clear, well-structured response
3. Make the content engaging and easy to understand

Rules:
- Write in a professional but approachable tone
- Use headers and paragraphs for structure
- Keep it concise (2-3 paragraphs max)
- Add a brief summary at the end
- Do NOT add new facts — only use what the research provides
"""


def run(query: str, research_findings: str) -> str:
    """Run the writer agent and return a polished response based on research findings."""
    logger.info("  ✍️  Writer Agent: Working...")
    user_message = (
        f"Original question: {query}\n\nResearch findings:\n{research_findings}\n\nPlease write a clear, well-structured response based on these findings."
    )
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]
    response = llm.invoke(messages)
    result = response.content
    logger.info("  ✍️  Writer Agent: Done.")
    return result
