import sqlite3


conn = sqlite3.connect("app/data/aegis.db")

tables = [
    "employees",
    "customers",
    "products",
    "suppliers",
    "orders",
    "payments",
    "inventory",
    "categories",
    "regions",
]

for table in tables:

    count = conn.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]

    print(f"{table}: {count}")


conn.close()