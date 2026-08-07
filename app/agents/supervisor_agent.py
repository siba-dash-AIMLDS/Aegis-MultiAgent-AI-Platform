from graph.state import AgentState
from agents.planner_agent import planner_agent


def supervisor_agent(state: AgentState):

    print("===== Supervisor Agent =====")

    return planner_agent(state)