-- ========================================
-- MSME Credit Scoring Platform - Complete Schema
-- Matches CSV Structure Exactly
-- ========================================

-- Drop existing tables (fresh start)
DROP TABLE IF EXISTS discounting_transactions;
DROP TABLE IF EXISTS monthly_bank_summary;
DROP TABLE IF EXISTS mca_director_info;
DROP TABLE IF EXISTS itr_data;
DROP TABLE IF EXISTS udyam_data;
DROP TABLE IF EXISTS bank_analysis;
DROP TABLE IF EXISTS gst_compliance;
DROP TABLE IF EXISTS invoices;
DROP TABLE IF EXISTS msme_scoring;

-- ========================================
-- 1. MSME Master Table (Matches msme_data.csv)
-- ========================================
CREATE TABLE msme_scoring (
    msme_id TEXT PRIMARY KEY,
    business_name TEXT NOT NULL,
    industry_type TEXT,
    business_age_years INTEGER,
    state TEXT,
    udyam_registered INTEGER,
    gst_filing_months INTEGER,
    avg_monthly_turnover REAL,
    gst_compliance_score REAL,
    turnover_growth_rate REAL,
    avg_monthly_upi_inflow REAL,
    upi_transaction_consistency REAL,
    num_unique_buyers INTEGER,
    peak_to_offpeak_ratio REAL,
    loan_amount_requested REAL,
    loan_purpose TEXT,
    existing_loans INTEGER,
    collateral_available INTEGER,
    credit_score INTEGER,
    credit_label TEXT
);

CREATE INDEX idx_msme_id ON msme_scoring(msme_id);
CREATE INDEX idx_msme_state ON msme_scoring(state);
CREATE INDEX idx_msme_industry ON msme_scoring(industry_type);
CREATE INDEX idx_msme_credit_label ON msme_scoring(credit_label);

-- ========================================
-- 2. Invoice Table (Matches invoice_data.csv)
-- ========================================
CREATE TABLE invoices (
    invoice_id TEXT PRIMARY KEY,
    msme_id TEXT NOT NULL,
    invoice_amount REAL,
    buyer_type TEXT,
    buyer_industry TEXT,
    invoice_date TEXT,
    due_date TEXT,
    payment_term_days INTEGER,
    historical_payment_delay_days INTEGER,
    seller_credit_score INTEGER,
    invoice_frequency INTEGER,
    payment_status TEXT,
    risk_label TEXT,
    risk_score REAL,
    FOREIGN KEY (msme_id) REFERENCES msme_scoring(msme_id)
);

CREATE INDEX idx_invoice_msme ON invoices(msme_id);
CREATE INDEX idx_invoice_status ON invoices(payment_status);
CREATE INDEX idx_invoice_risk ON invoices(risk_label);

-- ========================================
-- 3. GST Compliance Table
-- ========================================
CREATE TABLE gst_compliance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    msme_id TEXT NOT NULL,
    total_months INTEGER DEFAULT 12,
    filed_months INTEGER,
    FOREIGN KEY (msme_id) REFERENCES msme_scoring(msme_id)
);

CREATE INDEX idx_gst_msme ON gst_compliance(msme_id);

-- ========================================
-- 4. Bank Analysis Table
-- ========================================
CREATE TABLE bank_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    msme_id TEXT NOT NULL,
    avg_monthly_balance_lakhs REAL,
    total_bounces INTEGER DEFAULT 0,
    low_balance_days_pct REAL DEFAULT 0,
    FOREIGN KEY (msme_id) REFERENCES msme_scoring(msme_id)
);

CREATE INDEX idx_bank_msme ON bank_analysis(msme_id);

-- ========================================
-- 5. Udyam Registration Data
-- ========================================
CREATE TABLE udyam_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    msme_id TEXT NOT NULL,
    udyam_number TEXT UNIQUE,
    business_name TEXT,
    registration_date TEXT,
    is_active INTEGER DEFAULT 1,
    FOREIGN KEY (msme_id) REFERENCES msme_scoring(msme_id)
);

CREATE INDEX idx_udyam_msme ON udyam_data(msme_id);

-- ========================================
-- 6. ITR Data Table
-- ========================================
CREATE TABLE itr_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    msme_id TEXT NOT NULL,
    assessment_year TEXT,
    total_income_lakhs REAL,
    tax_paid_lakhs REAL,
    FOREIGN KEY (msme_id) REFERENCES msme_scoring(msme_id)
);

CREATE INDEX idx_itr_msme ON itr_data(msme_id);

-- ========================================
-- 7. MCA Director Information
-- ========================================
CREATE TABLE mca_director_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    msme_id TEXT NOT NULL,
    company_name TEXT,
    director_name TEXT,
    din TEXT,
    status TEXT DEFAULT 'Active',
    FOREIGN KEY (msme_id) REFERENCES msme_scoring(msme_id)
);

CREATE INDEX idx_mca_msme ON mca_director_info(msme_id);
CREATE INDEX idx_mca_director ON mca_director_info(director_name);

-- ========================================
-- 8. Monthly Bank Summary
-- ========================================
CREATE TABLE monthly_bank_summary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    msme_id TEXT NOT NULL,
    month_year TEXT,
    total_credits_lakhs REAL,
    total_debits_lakhs REAL,
    FOREIGN KEY (msme_id) REFERENCES msme_scoring(msme_id)
);

CREATE INDEX idx_monthly_msme ON monthly_bank_summary(msme_id);
CREATE INDEX idx_monthly_month ON monthly_bank_summary(month_year);

-- ========================================
-- 9. Discounting Transactions
-- ========================================
CREATE TABLE discounting_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id TEXT NOT NULL,
    msme_id TEXT NOT NULL,
    lender_name TEXT,
    invoice_amount REAL,
    discount_rate_pct REAL,
    funded_amount REAL,
    funding_date TEXT,
    settlement_date TEXT,
    status TEXT DEFAULT 'Pending',
    FOREIGN KEY (invoice_id) REFERENCES invoices(invoice_id),
    FOREIGN KEY (msme_id) REFERENCES msme_scoring(msme_id)
);

CREATE INDEX idx_txn_invoice ON discounting_transactions(invoice_id);
CREATE INDEX idx_txn_msme ON discounting_transactions(msme_id);
CREATE INDEX idx_txn_lender ON discounting_transactions(lender_name);
CREATE INDEX idx_txn_status ON discounting_transactions(status);

-- ========================================
-- Schema Creation Complete
-- ========================================