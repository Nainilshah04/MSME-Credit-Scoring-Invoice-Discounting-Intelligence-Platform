import sqlite3

# Connect to database
conn = sqlite3.connect('data/msme_credit.db')
cursor = conn.cursor()

# Check all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("📊 Tables in database:")
for table in tables:
    print(f"  - {table[0]}")

# Check row counts
for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
    count = cursor.fetchone()[0]
    print(f"  {table[0]}: {count} rows")

conn.close()
print("\n✅ Database is healthy!")