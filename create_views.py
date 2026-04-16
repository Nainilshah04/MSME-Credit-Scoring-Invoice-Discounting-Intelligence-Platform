import sqlite3

print("📊 Recreating Power BI Views...\n")

conn = sqlite3.connect('data/msme_credit.db')

with open('sql/views.sql', 'r') as f:
    views_sql = f.read()
    conn.executescript(views_sql)

print("✅ All 3 views recreated successfully!\n")

# Verify
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='view'")
views = cursor.fetchall()

print("📋 Available Views:")
for view in views:
    print(f"   ✓ {view[0]}")

# Test each view
print("\n🔍 Testing Views:\n")

for view in views:
    view_name = view[0]
    cursor.execute(f"SELECT COUNT(*) FROM {view_name}")
    count = cursor.fetchone()[0]
    print(f"   {view_name}: {count} rows")

conn.close()

print("\n✅ Views ready for Power BI!")