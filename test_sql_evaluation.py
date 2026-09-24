import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent / "app")
)

from app.agents.sql_agent import sql_agent
from app.graph.state import AgentState


TEST_CASES = [
    ("How many employees are there?", "total_employees", 50),
    ("How many customers are there?", "total_customers", 500),
    ("How many products are there?", "total_products", 100),
    ("How many suppliers are there?", "total_suppliers", 25),
    ("How many orders are there?", "total_orders", 7986),
    ("How many payments are there?", "total_payments", 7986),
    ("How many inventory items are there?", "total_inventory", 100),
    ("How many categories are there?", "total_categories", 12),
    ("How many regions are there?", "total_regions", 10),
]


print("=" * 70)
print("AEGIS SQL EVALUATION")
print("=" * 70)


passed = 0


for query, expected_column, expected_value in TEST_CASES:

    state = {
        "user_request": query,
        "execution_plan": ["SQLAgent"],
        "sql_result": "",
    }

    result_state = sql_agent(state)

    result = result_state["sql_result"]

    expected_text = (
        f"{expected_column} : {expected_value}"
    )

    if expected_text in result:

        print("\nPASS")
        print(f"Query    : {query}")
        print(f"Expected : {expected_text}")
        print("Result   : Correct")

        passed += 1

    else:

        print("\nFAIL")
        print(f"Query    : {query}")
        print(f"Expected : {expected_text}")
        print(f"Actual   : {result}")


print("\n" + "=" * 70)
print(f"Passed: {passed}/{len(TEST_CASES)}")
print("=" * 70)