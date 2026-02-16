"""Research Agent (Sub-Agent 1).

Role: Take a user query and gather key facts, bullet points, and relevant information.
This agent acts as a researcher and focuses on finding and organizing raw information.
"""

import logging

from langchain_ollama import ChatOllama

logger = logging.getLogger(__name__)

llm = ChatOllama(model="gpt-oss:latest", temperature=0.3)

SYSTEM_PROMPT = """You are a Research Agent. Your job is to:
1. Analyze the user's question
2. Gather key facts, data points, and relevant information
3. Return your findings as organized bullet points

Rules:
- Be factual and concise
- Include 5-8 key points
- Focus on accuracy over style
- Label your output clearly as "Research Findings"
"""


def run(query: str) -> str:
    """Run the research agent on the given query and return findings as text."""
    logger.info("  🔍 Research Agent: Working...")
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query},
    ]
    response = llm.invoke(messages)
    result = response.content
    logger.info("  🔍 Research Agent: Done.")
    return result
