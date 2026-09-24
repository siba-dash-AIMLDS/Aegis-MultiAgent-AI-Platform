import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent / "app")
)

from app.database.query_executor import QueryExecutor


print("=" * 70)
print("AEGIS SQL RESULT LIMIT TEST")
print("=" * 70)


executor = QueryExecutor()

query = """
SELECT *
FROM orders;
"""

columns, rows = executor.execute(query)

print(f"Columns returned : {len(columns)}")
print(f"Rows returned    : {len(rows)}")
print(f"Maximum allowed  : {executor.MAX_RESULT_ROWS}")


if len(rows) <= executor.MAX_RESULT_ROWS:

    print("\nPASS")
    print("Result row limit enforced.")

else:

    print("\nFAIL")
    print("Result row limit was exceeded.")


print("=" * 70)