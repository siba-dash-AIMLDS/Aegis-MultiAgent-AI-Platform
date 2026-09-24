import sys

sys.path.insert(0, "app")

from app.database.sql_security import SQLSecurity


TEST_CASES = [
    (
        "SELECT COUNT(*) FROM employees;",
        True,
    ),
    (
        "SELECT * FROM employees",
        True,
    ),
    (
        "DELETE FROM employees;",
        False,
    ),
    (
        "UPDATE employees SET salary = 0;",
        False,
    ),
    (
        "DROP TABLE employees;",
        False,
    ),
    (
        "INSERT INTO employees VALUES (1);",
        False,
    ),
    (
        "SELECT * FROM employees; DELETE FROM employees;",
        False,
    ),
    (
        "PRAGMA database_list;",
        False,
    ),
]


def run_tests():

    passed = 0

    print("=" * 70)
    print("AEGIS SQL SECURITY TEST")
    print("=" * 70)

    for query, expected in TEST_CASES:

        actual, message = SQLSecurity.validate_read_only_query(query)

        status = "PASS" if actual == expected else "FAIL"

        if status == "PASS":
            passed += 1

        print(f"\n{status}")
        print(f"Query    : {query}")
        print(f"Expected : {expected}")
        print(f"Actual   : {actual}")
        print(f"Message  : {message}")

    print("\n" + "=" * 70)
    print(f"Passed: {passed}/{len(TEST_CASES)}")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()