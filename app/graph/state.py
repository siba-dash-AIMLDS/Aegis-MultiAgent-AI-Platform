from typing import TypedDict


class AgentState(TypedDict):

    user_request: str

    execution_plan: list[str]

    plan_result: str

    knowledge_result: str

    sql_result: str

    report_result: str

    response: str
    
    mcp_result: str