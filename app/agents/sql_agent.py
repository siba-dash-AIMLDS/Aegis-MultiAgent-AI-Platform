from graph.state import AgentState

from database.query_executor import QueryExecutor
from database.query_library import QUERY_LIBRARY


def sql_agent(state: AgentState):

    print("===== SQL Agent =====")

    user_query = state["user_request"].lower()

    executor = QueryExecutor()

    found = False

    for keyword, value in QUERY_LIBRARY.items():

        if keyword in user_query:

            title, sql = value

            columns, rows = executor.execute(sql)

            result = f"""
SQL Agent

{title}

--------------------------------

{columns[0]} : {rows[0][0]}
"""

            state["sql_result"] = result

            found = True

            break

    if not found:

        state["sql_result"] = """
SQL Agent

No database query required.
"""

    return state