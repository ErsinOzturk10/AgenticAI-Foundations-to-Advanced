"""Multi-Agent Orchestrator — Streamlit UI.

A simple UI that shows the orchestrator workflow:
  1. User enters a query
  2. Research Agent gathers facts
  3. Writer Agent writes a polished response
  4. Both outputs are displayed

Usage:
  streamlit run app.py
"""

import streamlit as st
from orchestrator import Orchestrator

st.set_page_config(page_title="Multi-Agent Orchestrator", page_icon="🤖")

st.title("🤖 Multi-Agent Orchestrator")
st.markdown(
    "Enter a question below. The **Orchestrator** will delegate work to a **Research Agent** and a **Writer Agent**, then combine their results.",
)

# Initialize orchestrator
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = Orchestrator()

# User input
query = st.text_input("Your question:", placeholder="e.g. What is quantum computing?")

if st.button("Ask", type="primary") and query:
    with st.spinner("🎯 Orchestrator is routing your query..."):
        result = st.session_state.orchestrator.run(query)

    # Show the route taken
    st.info(f"**Route:** {result['route']}")

    # Show research findings if available
    if result["research"]:
        with st.expander("🔍 Research Agent Output", expanded=False):
            st.markdown(result["research"])

    # Show final response
    st.subheader("📝 Final Response")
    st.markdown(result["response"])

# Sidebar with architecture info
with st.sidebar:
    st.header("Architecture")
    st.code(
        """
User Query
    │
    ▼
┌──────────────┐
│ Orchestrator │ ← decides route
└──────┬───────┘
       │
   ┌───┴───┐
   ▼       ▼
┌──────┐ ┌──────┐
│Research│ │Writer│
│Agent  │ │Agent │
└──┬───┘ └──┬───┘
   │        │
   └───┬────┘
       ▼
  Final Response
""",
        language=None,
    )

    st.header("Agent Roles")
    st.markdown(
        """
- **Orchestrator**: Routes queries and combines results
- **Research Agent**: Gathers key facts and data points
- **Writer Agent**: Transforms research into a polished response
""",
    )
