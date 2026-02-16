# Multi-Agent Orchestrator

A minimal multi-agent example: an Orchestrator that routes user queries to two sub-agents (Research + Writer), collects results and returns a combined answer.

Quick summary
- Orchestrator: decides route ("direct" or "research_and_write"), delegates work, combines outputs.
- Research Agent: gathers factual bullet points.
- Writer Agent: transforms research into a polished response.
- Simple CLI and Streamlit UI included.

Files
- orchestrator.py — orchestration logic + CLI
- research_agent.py — research sub-agent (uses local ChatOllama)
- writer_agent.py — writer sub-agent (uses local ChatOllama)
- app.py — Streamlit UI
- requirements.txt — Python deps (langchain-ollama, streamlit)

Prerequisites
1. Python 3.8+
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Ensure your local Ollama/ChatOllama setup is available and configured (the code uses `ChatOllama(model="gpt-oss:latest")`). Adjust model name and temperature in the agent files if needed.

Run (CLI)
1. Start CLI orchestrator:
```bash
cd multi_agent
python orchestrator.py
```
2. Type queries at the prompt. Use `quit` to exit.

Run (Streamlit UI)
```bash
cd multi_agent
streamlit run app.py
```
Open the local Streamlit URL shown in the console.

Notes and tips
- If you prefer another local LLM, replace `ChatOllama(...)` calls in the agent files with your LLM wrapper.
- Keep token/latency settings low for orchestration (e.g. temperature=0 or small max tokens) to get deterministic routing decisions.
- The agents are intentionally simple for teaching/demo purposes; replace with more advanced toolchains (retrievers, RAG, tool calling) as needed.

Contact / Next steps
- To integrate MCP or multi-process orchestration, expose agents as services (HTTP/MCP) and have the Orchestrator call them remotely.
