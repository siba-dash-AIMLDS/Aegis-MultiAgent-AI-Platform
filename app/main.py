import streamlit as st

from graph.workflow import run_workflow
from memory.conversation_memory import memory


# ==================================================
# Page Configuration
# ==================================================

st.set_page_config(
    page_title="Aegis - Enterprise Multi-Agent AI Platform",
    page_icon="🤖",
    layout="wide"
)

# ==================================================
# Header
# ==================================================

st.title("🤖 AEGIS ENTERPRISE MULTI-AGENT AI PLATFORM")

st.caption(
    "LangGraph • Multi-Agent AI • RAG • SQLite • MCP • Memory • Human Approval"
)

st.divider()

# ==================================================
# Sidebar - Conversation History
# ==================================================

st.sidebar.header("Conversation History")

history = memory.get_history()

if history:

    for item in reversed(history):

        title = item["user"]

        if len(title) > 30:
            title = title[:30] + "..."

        with st.sidebar.expander(title):

            st.markdown("**User Request**")
            st.write(item["user"])

            st.markdown("**Assistant Response**")
            st.write(item["assistant"][:250] + "...")

else:

    st.sidebar.info("No conversations yet.")

if st.sidebar.button("🗑 Clear Memory"):

    memory.clear()

    st.rerun()

# ==================================================
# User Input
# ==================================================

st.subheader("User Request")

user_input = st.text_area(
    "User Request",
    height=120,
    placeholder="""
Examples:

• Show leave policy

• Employee count

• Supplier summary

• Calculate 125+225

• Leave policy and employee count

• Supplier summary and calculate 50*10
""",
    label_visibility="collapsed"
)

# ==================================================
# Human Approval
# ==================================================

approve = st.checkbox(
    "Approve Workflow Execution",
    value=True
)

# ==================================================
# Execute Workflow
# ==================================================

if st.button("▶ Run Workflow"):

    if not user_input.strip():

        st.warning("Please enter a request.")

        st.stop()

    if not approve:

        st.warning("Workflow cancelled by user.")

        st.stop()

    with st.spinner("🧠 Aegis is coordinating multiple AI agents..."):

        result = run_workflow(user_input)

    st.success("All selected AI agents completed successfully.")

    st.divider()

    # ==================================================
    # Execution Plan
    # ==================================================

    st.subheader("Execution Plan")

    for agent in result["execution_plan"]:

        st.success(f"✅ {agent}")

    st.divider()

    # ==================================================
    # Knowledge Agent
    # ==================================================

    with st.expander("Knowledge Agent", expanded=False):

        st.text(result["knowledge_result"])

    # ==================================================
    # SQL Agent
    # ==================================================

    with st.expander("SQL Agent", expanded=False):

        st.text(result["sql_result"])

    # ==================================================
    # MCP Agent
    # ==================================================

    with st.expander("MCP Agent", expanded=False):

        st.text(result["mcp_result"])

    # ==================================================
    # Enterprise Report
    # ==================================================

    with st.expander("Enterprise Report", expanded=True):

        st.text(result["response"])