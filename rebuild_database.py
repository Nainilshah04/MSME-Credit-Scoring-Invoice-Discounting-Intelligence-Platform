import sqlite3
import pandas as pd

print("🔧 Rebuilding database from CSV files...\n")

# Connect to new database
conn = sqlite3.connect('data/msme_credit.db')
cursor = conn.cursor()

# ========================================
# Load Schema
# ========================================
print("📋 Creating tables from schema...")
with open('sql/schema.sql', 'r') as f:
    schema_sql = f.read()
    conn.executescript(schema_sql)
print("✅ Schema created\n")

# ========================================
# Load MSME Data
# ========================================
print("📊 Loading MSME data...")
msme_df = pd.read_csv('data/raw/msme_data.csv')
print(f"   Loaded {len(msme_df)} MSMEs")

msme_df.to_sql('msme_scoring', conn, if_exists='append', index=False)
print("✅ MSME data loaded\n")

# ========================================
# Load Invoice Data
# ========================================
print("📄 Loading Invoice data...")
invoice_df = pd.read_csv('data/raw/invoice_data.csv')
print(f"   Loaded {len(invoice_df)} invoices")

invoice_df.to_sql('invoices', conn, if_exists='append', index=False)
print("✅ Invoice data loaded\n")

# ========================================
# Generate Supporting Tables
# ========================================
print("🔄 Generating supporting tables...\n")

# GST Compliance Table
print("   → GST Compliance...")
cursor.execute("""
INSERT INTO gst_compliance (msme_id, total_months, filed_months)
SELECT 
    msme_id,
    12 as total_months,
    gst_filing_months as filed_months
FROM msme_scoring
""")

# Bank Analysis Table
print("   → Bank Analysis...")
cursor.execute("""
INSERT INTO bank_analysis (msme_id, avg_monthly_balance_lakhs, total_bounces, low_balance_days_pct)
SELECT 
    msme_id,
    ROUND(avg_monthly_turnover / 100000 * 0.15, 2) as avg_monthly_balance_lakhs,
    CASE 
        WHEN credit_score >= 750 THEN 0
        WHEN credit_score >= 650 THEN CAST(ABS(RANDOM() % 3) AS INTEGER)
        WHEN credit_score >= 550 THEN CAST(ABS(RANDOM() % 5) + 2 AS INTEGER)
        ELSE CAST(ABS(RANDOM() % 8) + 5 AS INTEGER)
    END as total_bounces,
    ROUND((100 - gst_compliance_score) / 2.5, 1) as low_balance_days_pct
FROM msme_scoring
""")

# Udyam Data Table
print("   → Udyam Data...")
cursor.execute("""
INSERT INTO udyam_data (msme_id, udyam_number, business_name, registration_date, is_active)
SELECT 
    msme_id,
    'UDYAM-' || UPPER(SUBSTR(state, 1, 2)) || '-' || printf('%07d', ABS(RANDOM() % 9999999)) as udyam_number,
    business_name,
    DATE('now', '-' || business_age_years || ' years') as registration_date,
    udyam_registered as is_active
FROM msme_scoring
""")

# ITR Data Table
print("   → ITR Data...")
cursor.execute("""
INSERT INTO itr_data (msme_id, assessment_year, total_income_lakhs, tax_paid_lakhs)
SELECT 
    msme_id,
    '2023-24' as assessment_year,
    ROUND(avg_monthly_turnover * 12 / 100000 * 0.65, 2) as total_income_lakhs,
    ROUND(avg_monthly_turnover * 12 / 100000 * 0.65 * 0.25, 2) as tax_paid_lakhs
FROM msme_scoring
""")

# MCA Director Info Table
print("   → MCA Director Info...")
cursor.execute("""
INSERT INTO mca_director_info (msme_id, company_name, director_name, din, status)
SELECT 
    msme_id,
    business_name,
    CASE (ABS(RANDOM()) % 10)
        WHEN 0 THEN 'Rajesh Kumar'
        WHEN 1 THEN 'Priya Sharma'
        WHEN 2 THEN 'Amit Patel'
        WHEN 3 THEN 'Sunita Desai'
        WHEN 4 THEN 'Vikram Singh'
        WHEN 5 THEN 'Neha Gupta'
        WHEN 6 THEN 'Rohit Mehta'
        WHEN 7 THEN 'Anjali Reddy'
        WHEN 8 THEN 'Sanjay Joshi'
        ELSE 'Deepak Verma'
    END as director_name,
    printf('%08d', ABS(RANDOM() % 99999999)) as din,
    CASE WHEN credit_label = 'Reject' THEN 'Struck Off' ELSE 'Active' END as status
FROM msme_scoring
""")

# Monthly Bank Summary Table
print("   → Monthly Bank Summary...")
months = ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06']
for month in months:
    multiplier = 0.85 + (months.index(month) * 0.03)
    cursor.execute(f"""
    INSERT INTO monthly_bank_summary (msme_id, month_year, total_credits_lakhs, total_debits_lakhs)
    SELECT 
        msme_id,
        '{month}' as month_year,
        ROUND(avg_monthly_turnover / 100000 * {multiplier}, 2) as total_credits_lakhs,
        ROUND(avg_monthly_turnover / 100000 * {multiplier} * 0.92, 2) as total_debits_lakhs
    FROM msme_scoring
    """)

# Discounting Transactions Table
print("   → Discounting Transactions...")
cursor.execute("""
INSERT INTO discounting_transactions (
    invoice_id, msme_id, lender_name, invoice_amount, 
    discount_rate_pct, funded_amount, funding_date, 
    settlement_date, status
)
SELECT 
    invoice_id,
    msme_id,
    CASE (ABS(RANDOM()) % 6)
        WHEN 0 THEN 'HDFC Capital'
        WHEN 1 THEN 'Bajaj Finserv'
        WHEN 2 THEN 'Tata Capital'
        WHEN 3 THEN 'ICICI Direct'
        WHEN 4 THEN 'Kotak Mahindra'
        ELSE 'Axis Finance'
    END as lender_name,
    invoice_amount,
    ROUND(8 + (ABS(RANDOM()) % 8), 2) as discount_rate_pct,
    ROUND(invoice_amount * 0.88, 2) as funded_amount,
    DATE(invoice_date, '+2 days') as funding_date,
    DATE(due_date, '+3 days') as settlement_date,
    CASE 
        WHEN payment_status = 'Paid_OnTime' THEN 'Settled'
        WHEN payment_status = 'Paid_Late' THEN 'Settled'
        ELSE 'Defaulted'
    END as status
FROM invoices
WHERE risk_label IN ('Low', 'Medium')
LIMIT 800
""")

conn.commit()
print("\n✅ All supporting tables generated!\n")

# ========================================
# Verification
# ========================================
print("=" * 50)
print("🔍 DATABASE VERIFICATION")
print("=" * 50 + "\n")

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()

total_rows = 0
for table in tables:
    table_name = table[0]
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    total_rows += count
    print(f"   ✓ {table_name}: {count:,} rows")

conn.close()

print("\n" + "=" * 50)
print(f"🎉 DATABASE REBUILD COMPLETE!")
print(f"   Total Records: {total_rows:,}")
print("=" * 50)
print("\n📁 File: data/msme_credit.db")
print("✅ Ready for SQL queries, Views & Power BI!\n")