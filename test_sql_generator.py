import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent / "app")
)

from database.sql_generator import SQLGenerator


generator = SQLGenerator()


TEST_CASES = [
    "How many employees are there?",
    "How many customers are there?",
    "How many orders are there?",
    "How many products are there?",
]


print("=" * 70)
print("AEGIS NL-TO-SQL GENERATION TEST")
print("=" * 70)


for question in TEST_CASES:

    print("\n" + "-" * 70)
    print(f"Question: {question}")
    print("-" * 70)

    sql = generator.generate_sql(question)

    print("Generated SQL:")
    print(sql)


print("\n" + "=" * 70)
print("GENERATION TEST COMPLETED")
print("=" * 70)