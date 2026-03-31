import sqlite3

print("📊 Creating Power BI Views...\n")

conn = sqlite3.connect('data/msme_credit.db')

with open('sql/views.sql', 'r') as f:
    views_sql = f.read()
    conn.executescript(views_sql)

print("✅ All 3 views created successfully!\n")

# Verify
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='view'")
views = cursor.fetchall()

print("📋 Available Views:")
for view in views:
    print(f"   ✓ {view[0]}")

conn.close()