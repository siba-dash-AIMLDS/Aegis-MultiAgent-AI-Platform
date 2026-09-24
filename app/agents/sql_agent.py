from graph.state import AgentState

from database.query_executor import QueryExecutor
from database.query_library import QUERY_LIBRARY
from database.sql_generator import SQLGenerator


def sql_agent(state: AgentState):

    print("===== SQL Agent =====")

    user_query = state["user_request"].lower()

    executor = QueryExecutor()

    found = False

    # ---------------------------------------------------------
    # 1. Deterministic query library
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # 2. Governed NL-to-SQL fallback
    # ---------------------------------------------------------

    if not found:

        try:

            generator = SQLGenerator()

            generated_sql = generator.generate_sql(
                state["user_request"]
            )

            print("Generated SQL:")
            print(generated_sql)

            columns, rows = executor.execute(
                generated_sql
            )

            if rows:

                result = f"""
SQL Agent

Generated SQL

--------------------------------

{columns[0]} : {rows[0][0]}

SQL:
{generated_sql}
"""

            else:

                result = f"""
SQL Agent

Generated SQL

--------------------------------

No rows returned.

SQL:
{generated_sql}
"""

            state["sql_result"] = result

        except ValueError as exc:

            state["sql_result"] = f"""
SQL Agent

SQL query rejected by security governance.

Reason:
{exc}
"""

        except Exception as exc:

            state["sql_result"] = f"""
SQL Agent

SQL execution failed.

Reason:
{exc}
"""

    return state