import sqlite3
from pathlib import Path

DB_PATH = Path("app/data/aegis.db")

if not DB_PATH.exists():
    print(f"Database not found: {DB_PATH.resolve()}")
    raise SystemExit(1)

print("=" * 60)
print(f"Database: {DB_PATH.resolve()}")
print("=" * 60)

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

# Get tables
cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name;
""")

tables = [row[0] for row in cursor.fetchall()]

print(f"\nTables found: {len(tables)}")

for table in tables:
    print("\n" + "-" * 60)
    print(f"TABLE: {table}")
    print("-" * 60)

    # Structure
    cursor.execute(f'PRAGMA table_info("{table}")')
    columns = cursor.fetchall()

    print("Columns:")
    for col in columns:
        print(f"  {col[1]:20} {col[2]}")

    # Row count
    cursor.execute(f'SELECT COUNT(*) FROM "{table}"')
    count = cursor.fetchone()[0]

    print(f"\nRow count: {count}")

    # Sample data
    cursor.execute(f'SELECT * FROM "{table}" LIMIT 5')
    rows = cursor.fetchall()

    if rows:
        print("\nSample rows:")
        for row in rows:
            print(" ", row)
    else:
        print("\nNo data.")

conn.close()

print("\n" + "=" * 60)
print("Database inspection completed.")
print("=" * 60)