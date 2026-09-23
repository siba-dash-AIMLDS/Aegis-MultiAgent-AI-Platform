from graph.state import AgentState
from tools.calculator_tool import CalculatorTool



def mcp_agent(state: AgentState):

    print("===== MCP Agent =====")

    # ---------------------------------------------
    # Execute only if selected by Planner
    # ---------------------------------------------
    if "MCPAgent" not in state["execution_plan"]:

        print("MCP Agent Skipped")

        state["mcp_result"] = "MCP Agent Skipped."

        return state

    print("MCP Agent Executing...")

    query = state["user_request"].lower()

    expression = query.replace("calculate", "")
    expression = expression.replace("calculator", "")
    expression = expression.replace("math", "")
    expression = expression.strip()

    calculator = CalculatorTool()

    result = calculator.calculate(expression)

    state["mcp_result"] = f"""
MCP Agent

Calculator Tool

----------------------------------------

Expression

{expression}

----------------------------------------

Result

{result}
"""

    return state