from graph.state import AgentState


def planner_agent(state: AgentState):

    print("===== Planner Agent =====")

    query = state["user_request"].lower()

    execution_plan = []

    # --------------------------------------------------
    # Knowledge Agent Routing
    # --------------------------------------------------

    knowledge_keywords = [
        "leave",
        "policy",
        "insurance",
        "security",
        "hr",
        "document",
        "documents",
        "handbook"
    ]

    if any(keyword in query for keyword in knowledge_keywords):
        execution_plan.append("KnowledgeAgent")

    # --------------------------------------------------
    # SQL Agent Routing
    # --------------------------------------------------

    sql_keywords = [
        "employee",
        "employees",
        "customer",
        "customers",
        "supplier",
        "suppliers",
        "product",
        "products",
        "order",
        "orders",
        "inventory",
        "payment",
        "payments",
        "category",
        "categories",
        "region",
        "regions"
    ]

    if any(keyword in query for keyword in sql_keywords):
        execution_plan.append("SQLAgent")

    # --------------------------------------------------
    # MCP Agent Routing
    # --------------------------------------------------

    mcp_keywords = [
        "calculate",
        "calculator",
        "math",
        "+",
        "-",
        "*",
        "/"
    ]

    if any(keyword in query for keyword in mcp_keywords):
        execution_plan.append("MCPAgent")

    # --------------------------------------------------
    # Report Agent Always Executes
    # --------------------------------------------------

    execution_plan.append("ReportAgent")

    # --------------------------------------------------
    # Update Workflow State
    # --------------------------------------------------

    state["execution_plan"] = execution_plan

    state["plan_result"] = "\n".join(execution_plan)

    # --------------------------------------------------
    # Console Output
    # --------------------------------------------------

    print("\nExecution Plan")
    print("----------------------------")

    for agent in execution_plan:
        print(f"✓ {agent}")

    print("----------------------------\n")

    return state