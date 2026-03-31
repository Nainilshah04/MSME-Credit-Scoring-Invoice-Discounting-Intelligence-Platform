-- ================================================================
-- MSME CREDIT SCORING PLATFORM - DATABASE SCHEMA
-- SQLite Database Design for Credit Assessment & Invoice Discounting
-- ================================================================

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- ================================================================
-- TABLE 1: MSME PROFILES
-- Core business information and registration details
-- ================================================================

DROP TABLE IF EXISTS msme_profiles;

CREATE TABLE msme_profiles (
    -- Primary Key
    msme_id TEXT PRIMARY KEY,
    
    -- Business Information
    business_name TEXT NOT NULL,
    industry_type TEXT NOT NULL CHECK(industry_type IN (
        'Manufacturing', 'Retail', 'Services', 'Food & Beverage', 'Textile'
    )),
    business_age_years INTEGER NOT NULL CHECK(business_age_years > 0),
    state TEXT NOT NULL,
    udyam_registered BOOLEAN NOT NULL,
    
    -- GST Features
    gst_filing_months INTEGER CHECK(gst_filing_months BETWEEN 0 AND 12),
    avg_monthly_turnover REAL CHECK(avg_monthly_turnover >= 0),
    gst_compliance_score REAL CHECK(gst_compliance_score BETWEEN 0 AND 100),
    turnover_growth_rate REAL,
    
    -- UPI Transaction Features
    avg_monthly_upi_inflow REAL CHECK(avg_monthly_upi_inflow >= 0),
    upi_transaction_consistency REAL CHECK(upi_transaction_consistency BETWEEN 0 AND 1),
    num_unique_buyers INTEGER CHECK(num_unique_buyers >= 0),
    peak_to_offpeak_ratio REAL CHECK(peak_to_offpeak_ratio >= 1),
    
    -- Loan Features
    loan_amount_requested REAL CHECK(loan_amount_requested > 0),
    loan_purpose TEXT CHECK(loan_purpose IN (
        'Working Capital', 'Machinery', 'Expansion', 'Inventory'
    )),
    existing_loans BOOLEAN,
    collateral_available BOOLEAN,
    
    -- Credit Assessment (Model Output)
    credit_score REAL CHECK(credit_score BETWEEN 0 AND 100),
    credit_label TEXT CHECK(credit_label IN ('Approve', 'Review', 'Reject')),
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_msme_industry ON msme_profiles(industry_type);
CREATE INDEX idx_msme_state ON msme_profiles(state);
CREATE INDEX idx_msme_credit_label ON msme_profiles(credit_label);
CREATE INDEX idx_msme_credit_score ON msme_profiles(credit_score);

-- ================================================================
-- TABLE 2: INVOICE RECORDS
-- Invoice details for discounting/factoring
-- ================================================================

DROP TABLE IF EXISTS invoice_records;

CREATE TABLE invoice_records (
    -- Primary Key
    invoice_id TEXT PRIMARY KEY,
    
    -- Foreign Key to MSME
    msme_id TEXT NOT NULL,
    
    -- Invoice Details
    invoice_amount REAL NOT NULL CHECK(invoice_amount > 0),
    invoice_date DATE NOT NULL,
    due_date DATE NOT NULL,
    payment_term_days INTEGER CHECK(payment_term_days IN (30, 60, 90)),
    
    -- Buyer Information
    buyer_type TEXT CHECK(buyer_type IN (
        'Large Corporate', 'Government', 'SME', 'Retail'
    )),
    buyer_industry TEXT,
    historical_payment_delay_days INTEGER CHECK(historical_payment_delay_days >= 0),
    
    -- Seller Info
    seller_credit_score REAL CHECK(seller_credit_score BETWEEN 0 AND 100),
    invoice_frequency INTEGER CHECK(invoice_frequency > 0),
    
    -- Risk Assessment (Model Output)
    risk_score REAL CHECK(risk_score BETWEEN 0 AND 100),
    risk_label TEXT CHECK(risk_label IN ('Low', 'Medium', 'High')),
    payment_status TEXT CHECK(payment_status IN (
        'Paid_OnTime', 'Paid_Late', 'Defaulted'
    )),
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Key Constraint
    FOREIGN KEY (msme_id) REFERENCES msme_profiles(msme_id) ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX idx_invoice_msme ON invoice_records(msme_id);
CREATE INDEX idx_invoice_buyer_type ON invoice_records(buyer_type);
CREATE INDEX idx_invoice_risk_label ON invoice_records(risk_label);
CREATE INDEX idx_invoice_payment_status ON invoice_records(payment_status);
CREATE INDEX idx_invoice_date ON invoice_records(invoice_date);

-- ================================================================
-- TABLE 3: CREDIT ASSESSMENTS
-- Historical credit decisions and model predictions
-- ================================================================

DROP TABLE IF EXISTS credit_assessments;

CREATE TABLE credit_assessments (
    -- Primary Key
    assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Foreign Key
    msme_id TEXT NOT NULL,
    
    -- Assessment Details
    assessment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    model_version TEXT,
    
    -- Scores
    credit_score REAL CHECK(credit_score BETWEEN 0 AND 100),
    credit_decision TEXT CHECK(credit_decision IN ('Approve', 'Review', 'Reject')),
    
    -- Score Components (for explainability)
    compliance_component REAL,
    filing_component REAL,
    age_component REAL,
    consistency_component REAL,
    
    -- Additional Factors
    loan_amount_requested REAL,
    recommended_amount REAL,
    interest_rate_suggested REAL,
    
    -- Metadata
    assessed_by TEXT, -- 'Model' or 'Manual'
    notes TEXT,
    
    FOREIGN KEY (msme_id) REFERENCES msme_profiles(msme_id) ON DELETE CASCADE
);

CREATE INDEX idx_assessment_msme ON credit_assessments(msme_id);
CREATE INDEX idx_assessment_date ON credit_assessments(assessment_date);
CREATE INDEX idx_assessment_decision ON credit_assessments(credit_decision);

-- ================================================================
-- TABLE 4: INVOICE RISK ASSESSMENTS
-- Historical invoice risk predictions
-- ================================================================

DROP TABLE IF EXISTS invoice_risk_assessments;

CREATE TABLE invoice_risk_assessments (
    -- Primary Key
    risk_assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Foreign Key
    invoice_id TEXT NOT NULL,
    
    -- Assessment Details
    assessment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    model_version TEXT,
    
    -- Risk Scores
    risk_score REAL CHECK(risk_score BETWEEN 0 AND 100),
    risk_category TEXT CHECK(risk_category IN ('Low', 'Medium', 'High')),
    default_probability REAL CHECK(default_probability BETWEEN 0 AND 1),
    
    -- Discounting Recommendation
    recommended_discount_rate REAL,
    max_advance_percentage REAL,
    
    -- Risk Factors
    seller_risk_factor REAL,
    buyer_risk_factor REAL,
    amount_risk_factor REAL,
    
    -- Metadata
    assessed_by TEXT,
    notes TEXT,
    
    FOREIGN KEY (invoice_id) REFERENCES invoice_records(invoice_id) ON DELETE CASCADE
);

CREATE INDEX idx_risk_invoice ON invoice_risk_assessments(invoice_id);
CREATE INDEX idx_risk_date ON invoice_risk_assessments(assessment_date);
CREATE INDEX idx_risk_category ON invoice_risk_assessments(risk_category);

-- ================================================================
-- TABLE 5: KAGGLE CREDIT DATA (For Comparison)
-- Original Kaggle credit risk dataset
-- ================================================================

DROP TABLE IF EXISTS kaggle_credit_data;

CREATE TABLE kaggle_credit_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Person Information
    person_age INTEGER,
    person_income REAL,
    person_home_ownership TEXT,
    person_emp_length REAL,
    
    -- Loan Information
    loan_intent TEXT,
    loan_grade TEXT,
    loan_amnt REAL,
    loan_int_rate REAL,
    loan_status INTEGER, -- 0: paid, 1: default
    loan_percent_income REAL,
    
    -- Credit History
    cb_person_default_on_file TEXT,
    cb_person_cred_hist_length REAL,
    
    -- Metadata
    source TEXT DEFAULT 'Kaggle',
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_kaggle_loan_status ON kaggle_credit_data(loan_status);
CREATE INDEX idx_kaggle_loan_grade ON kaggle_credit_data(loan_grade);

-- ================================================================
-- VIEWS FOR ANALYSIS
-- ================================================================

-- View: High-risk MSMEs with pending invoices
DROP VIEW IF EXISTS high_risk_msmes;
CREATE VIEW high_risk_msmes AS
SELECT 
    m.msme_id,
    m.business_name,
    m.industry_type,
    m.credit_score,
    m.credit_label,
    COUNT(i.invoice_id) as total_invoices,
    SUM(i.invoice_amount) as total_invoice_value,
    AVG(i.risk_score) as avg_invoice_risk
FROM msme_profiles m
LEFT JOIN invoice_records i ON m.msme_id = i.msme_id
WHERE m.credit_label = 'Reject' OR m.credit_score < 50
GROUP BY m.msme_id, m.business_name, m.industry_type, m.credit_score, m.credit_label;

-- View: Invoice payment analysis
DROP VIEW IF EXISTS invoice_payment_summary;
CREATE VIEW invoice_payment_summary AS
SELECT 
    payment_status,
    risk_label,
    buyer_type,
    COUNT(*) as invoice_count,
    SUM(invoice_amount) as total_amount,
    AVG(invoice_amount) as avg_amount,
    AVG(risk_score) as avg_risk_score
FROM invoice_records
GROUP BY payment_status, risk_label, buyer_type;

-- View: MSME performance by industry
DROP VIEW IF EXISTS industry_performance;
CREATE VIEW industry_performance AS
SELECT 
    industry_type,
    COUNT(*) as total_msmes,
    AVG(credit_score) as avg_credit_score,
    AVG(avg_monthly_turnover) as avg_turnover,
    AVG(gst_compliance_score) as avg_compliance,
    SUM(CASE WHEN credit_label = 'Approve' THEN 1 ELSE 0 END) as approved_count,
    SUM(CASE WHEN credit_label = 'Reject' THEN 1 ELSE 0 END) as rejected_count
FROM msme_profiles
GROUP BY industry_type
ORDER BY avg_credit_score DESC;

-- ================================================================
-- TRIGGERS FOR AUTO-UPDATE
-- ================================================================

-- Auto-update timestamp on MSME profile update
DROP TRIGGER IF EXISTS update_msme_timestamp;
CREATE TRIGGER update_msme_timestamp 
AFTER UPDATE ON msme_profiles
FOR EACH ROW
BEGIN
    UPDATE msme_profiles 
    SET updated_at = CURRENT_TIMESTAMP 
    WHERE msme_id = NEW.msme_id;
END;

-- Auto-update timestamp on invoice update
DROP TRIGGER IF EXISTS update_invoice_timestamp;
CREATE TRIGGER update_invoice_timestamp 
AFTER UPDATE ON invoice_records
FOR EACH ROW
BEGIN
    UPDATE invoice_records 
    SET updated_at = CURRENT_TIMESTAMP 
    WHERE invoice_id = NEW.invoice_id;
END;

-- ================================================================
-- INITIAL STATISTICS QUERY
-- ================================================================

-- This query will be run after data load to verify
-- SELECT 'Database schema created successfully!' as status;
-- SELECT COUNT(*) as total_msmes FROM msme_profiles;
-- SELECT COUNT(*) as total_invoices FROM invoice_records;