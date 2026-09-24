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

    print("\n" + "=" * 60)
    print(f"TABLE: {table}")
    print("=" * 60)

    columns = conn.execute(
        f"PRAGMA table_info({table})"
    ).fetchall()

    for column in columns:
        print(
            f"{column[1]} | "
            f"type={column[2]} | "
            f"nullable={not column[3]} | "
            f"primary_key={bool(column[5])}"
        )

conn.close()