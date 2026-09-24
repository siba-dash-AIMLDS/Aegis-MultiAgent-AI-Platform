import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent / "app")
)

from app.agents.sql_agent import sql_agent


TEST_CASES = [
    "What is the weather today?",
    "What is the leave policy?",
    "Tell me about the VPN policy.",
    "What is the capital of France?",
]


print("=" * 70)
print("AEGIS SQL NEGATIVE EVALUATION")
print("=" * 70)


passed = 0


for query in TEST_CASES:

    state = {
        "user_request": query,
        "execution_plan": ["SQLAgent"],
        "sql_result": "",
    }

    result_state = sql_agent(state)

    result = result_state["sql_result"]

    expected_text = "No database query required."

    if expected_text in result:

        print("\nPASS")
        print(f"Query    : {query}")
        print("Expected : No database query required.")
        print("Result   : Correct")

        passed += 1

    else:

        print("\nFAIL")
        print(f"Query    : {query}")
        print("Expected : No database query required.")
        print(f"Actual   : {result}")


print("\n" + "=" * 70)
print(f"Passed: {passed}/{len(TEST_CASES)}")
print("=" * 70)