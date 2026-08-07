from langgraph.graph import StateGraph, END

from graph.state import AgentState

from agents.supervisor_agent import supervisor_agent
from agents.knowledge_agent import knowledge_agent
from agents.sql_agent import sql_agent
from agents.mcp_agent import mcp_agent
from agents.report_agent import report_agent


# --------------------------------------------------
# Build LangGraph Workflow
# --------------------------------------------------

def build_graph():

    workflow = StateGraph(AgentState)

    # -----------------------------
    # Register Nodes
    # -----------------------------

    workflow.add_node("Supervisor", supervisor_agent)

    workflow.add_node("KnowledgeAgent", knowledge_agent)

    workflow.add_node("SQLAgent", sql_agent)

    workflow.add_node("MCPAgent", mcp_agent)

    workflow.add_node("ReportAgent", report_agent)

    # -----------------------------
    # Entry Point
    # -----------------------------

    workflow.set_entry_point("Supervisor")

    # -----------------------------
    # Workflow
    # -----------------------------

    workflow.add_edge("Supervisor", "KnowledgeAgent")

    workflow.add_edge("KnowledgeAgent", "SQLAgent")

    workflow.add_edge("SQLAgent", "MCPAgent")

    workflow.add_edge("MCPAgent", "ReportAgent")

    workflow.add_edge("ReportAgent", END)

    return workflow.compile()


# --------------------------------------------------
# Compile Graph
# --------------------------------------------------

graph = build_graph()


# --------------------------------------------------
# Execute Workflow
# --------------------------------------------------

def run_workflow(user_request: str):

    state = {

        "user_request": user_request,

        "execution_plan": [],

        "plan_result": "",

        "knowledge_result": "",

        "sql_result": "",

        "mcp_result": "",

        "report_result": "",

        "response": ""

    }

    result = graph.invoke(state)

    return result