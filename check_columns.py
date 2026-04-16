import sqlite3

conn = sqlite3.connect('data/msme_credit.db')
cursor = conn.cursor()

tables = ['msme_scoring', 'invoices', 'discounting_transactions']

for table in tables:
    print(f"\n📋 {table.upper()} COLUMNS:")
    print("=" * 50)
    cursor.execute(f"PRAGMA table_info({table})")
    columns = cursor.fetchall()
    for col in columns:
        print(f"   {col[1]} ({col[2]})")

conn.close()