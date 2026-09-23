from graph.state import AgentState
from memory.conversation_memory import memory


def report_agent(state: AgentState):

    print("===== Report Agent =====")

    report = f"""
============================================================
               AEGIS ENTERPRISE AI PLATFORM
============================================================

User Request
------------------------------------------------------------
{state["user_request"]}

------------------------------------------------------------
Execution Plan
------------------------------------------------------------
{state["plan_result"]}

------------------------------------------------------------
Knowledge Agent
------------------------------------------------------------
{state["knowledge_result"]}

------------------------------------------------------------
SQL Agent
------------------------------------------------------------
{state["sql_result"]}

------------------------------------------------------------
MCP Agent
------------------------------------------------------------
{state["mcp_result"]}

------------------------------------------------------------
Workflow Status
------------------------------------------------------------
✓ Supervisor Agent

✓ Planner Agent

✓ Report Agent

============================================================
Workflow Completed Successfully
============================================================
"""

    state["response"] = report

    memory.add(
        state["user_request"],
        report
    )

    return state