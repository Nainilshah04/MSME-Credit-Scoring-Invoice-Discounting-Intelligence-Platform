-- ========================================
-- DROP OLD VIEWS (Clean Start)
-- ========================================
DROP VIEW IF EXISTS vw_msme_portfolio;
DROP VIEW IF EXISTS vw_invoice_intelligence;
DROP VIEW IF EXISTS vw_lender_dashboard;


-- ========================================
-- VIEW 1: MSME Portfolio Dashboard View
-- ========================================
CREATE VIEW vw_msme_portfolio AS
SELECT 
    -- Business Identity
    m.msme_id,
    m.business_name,
    m.industry_type,
    m.state,
    m.business_age_years,
    
    -- Financial Metrics
    ROUND(m.avg_monthly_turnover / 100000, 2) AS monthly_turnover_lakhs,
    ROUND(m.avg_monthly_turnover * 12 / 10000000, 2) AS annual_turnover_cr,
    ROUND(m.loan_amount_requested / 100000, 2) AS loan_requested_lakhs,
    ROUND(m.avg_monthly_upi_inflow / 100000, 2) AS monthly_upi_lakhs,
    
    -- Credit & Risk Scores
    m.credit_score,
    m.credit_label,
    m.gst_compliance_score,
    m.upi_transaction_consistency,
    m.num_unique_buyers,
    
    -- Registration & Compliance
    m.udyam_registered,
    m.gst_filing_months,
    m.existing_loans,
    m.collateral_available,
    m.loan_purpose,
    m.turnover_growth_rate,
    m.peak_to_offpeak_ratio,
    
    -- Credit Score Bands
    CASE 
        WHEN m.credit_score >= 750 THEN 'Excellent (750+)'
        WHEN m.credit_score >= 650 THEN 'Good (650-749)'
        WHEN m.credit_score >= 550 THEN 'Fair (550-649)'
        ELSE 'Poor (<550)'
    END AS credit_band,
    
    -- Risk Flags
    CASE 
        WHEN m.gst_filing_months < 6 THEN 1 
        ELSE 0 
    END AS poor_gst_compliance,
    
    CASE 
        WHEN m.upi_transaction_consistency < 0.5 THEN 1 
        ELSE 0 
    END AS low_upi_consistency,
    
    -- GST Compliance Data
    g.filed_months,
    g.total_months,
    
    -- Bank Analysis Data
    b.avg_monthly_balance_lakhs,
    b.total_bounces,
    b.low_balance_days_pct

FROM msme_scoring m
LEFT JOIN gst_compliance g ON m.msme_id = g.msme_id
LEFT JOIN bank_analysis b ON m.msme_id = b.msme_id;


-- ========================================
-- VIEW 2: Invoice Intelligence View
-- ========================================
CREATE VIEW vw_invoice_intelligence AS
SELECT 
    -- Invoice Details
    i.invoice_id,
    i.invoice_date,
    i.due_date,
    ROUND(i.invoice_amount / 100000, 2) AS invoice_amount_lakhs,
    i.invoice_amount AS invoice_amount_raw,
    i.buyer_type,
    i.buyer_industry,
    i.payment_status,
    i.risk_label,
    ROUND(i.risk_score, 2) AS risk_score,
    i.payment_term_days,
    i.historical_payment_delay_days,
    i.invoice_frequency,
    
    -- MSME (Seller) Info
    m.business_name AS seller_name,
    i.msme_id,
    m.industry_type AS seller_industry,
    m.credit_score AS seller_credit_score,
    m.credit_label AS seller_credit_label,
    m.state AS seller_state,
    
    -- Time Metrics
    JULIANDAY(i.due_date) - JULIANDAY('now') AS days_to_due,
    JULIANDAY('now') - JULIANDAY(i.invoice_date) AS invoice_age_days,
    
    -- Aging Bucket
    CASE 
        WHEN JULIANDAY('now') - JULIANDAY(i.due_date) <= 0 THEN 'Not Due'
        WHEN JULIANDAY('now') - JULIANDAY(i.due_date) BETWEEN 1 AND 30 THEN '0-30 Days Overdue'
        WHEN JULIANDAY('now') - JULIANDAY(i.due_date) BETWEEN 31 AND 60 THEN '31-60 Days Overdue'
        WHEN JULIANDAY('now') - JULIANDAY(i.due_date) BETWEEN 61 AND 90 THEN '61-90 Days Overdue'
        ELSE '90+ Days (NPA)'
    END AS aging_bucket,
    
    -- Discounting Metrics
    ROUND(i.invoice_amount / 100000 * 0.88, 2) AS estimated_payout_lakhs,
    ROUND(i.invoice_amount / 100000 * 0.12, 2) AS estimated_discount_lakhs,
    
    -- Deal Quality Score
    CASE 
        WHEN i.risk_label = 'Low' 
             AND JULIANDAY(i.due_date) - JULIANDAY('now') BETWEEN 15 AND 90 
             AND i.invoice_amount >= 500000 
        THEN 'Prime Deal'
        WHEN i.risk_label IN ('Low', 'Medium') 
             AND JULIANDAY(i.due_date) - JULIANDAY('now') > 0 
        THEN 'Standard Deal'
        ELSE 'High Risk / Review'
    END AS deal_quality,
    
    -- Discounting Transaction (if any)
    d.lender_name,
    d.discount_rate_pct,
    ROUND(d.funded_amount / 100000, 2) AS funded_amount_lakhs,
    d.funding_date,
    d.settlement_date,
    d.status AS transaction_status

FROM invoices i
JOIN msme_scoring m ON i.msme_id = m.msme_id
LEFT JOIN discounting_transactions d ON i.invoice_id = d.invoice_id;


-- ========================================
-- VIEW 3: Lender Performance Dashboard
-- ========================================
CREATE VIEW vw_lender_dashboard AS
SELECT 
    -- Lender Identity
    d.lender_name,
    
    -- Volume Metrics
    COUNT(DISTINCT d.invoice_id) AS total_deals,
    ROUND(SUM(d.invoice_amount) / 100000, 2) AS total_portfolio_lakhs,
    ROUND(SUM(d.funded_amount) / 100000, 2) AS total_funded_lakhs,
    ROUND(AVG(d.invoice_amount) / 100000, 2) AS avg_deal_size_lakhs,
    
    -- Yield & Returns
    ROUND(AVG(d.discount_rate_pct), 2) AS avg_discount_rate_pct,
    ROUND(SUM(d.invoice_amount - d.funded_amount) / 100000, 2) AS total_earnings_lakhs,
    ROUND(
        100.0 * SUM(d.invoice_amount - d.funded_amount) / NULLIF(SUM(d.funded_amount), 0), 
        2
    ) AS portfolio_yield_pct,
    
    -- Settlement Performance
    ROUND(AVG(JULIANDAY(d.settlement_date) - JULIANDAY(d.funding_date)), 1) AS avg_settlement_days,
    SUM(CASE WHEN d.status = 'Settled' THEN 1 ELSE 0 END) AS settled_count,
    SUM(CASE WHEN d.status = 'Pending' THEN 1 ELSE 0 END) AS pending_count,
    SUM(CASE WHEN d.status = 'Defaulted' THEN 1 ELSE 0 END) AS defaulted_count,
    ROUND(100.0 * SUM(CASE WHEN d.status = 'Settled' THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS settlement_rate_pct,
    
    -- Risk Exposure by Credit Label
    ROUND(SUM(CASE WHEN m.credit_label = 'Reject' THEN d.funded_amount ELSE 0 END) / 100000, 2) AS high_risk_exposure_lakhs,
    ROUND(SUM(CASE WHEN m.credit_label = 'Review' THEN d.funded_amount ELSE 0 END) / 100000, 2) AS medium_risk_exposure_lakhs,
    ROUND(SUM(CASE WHEN m.credit_label = 'Approve' THEN d.funded_amount ELSE 0 END) / 100000, 2) AS low_risk_exposure_lakhs,
    
    ROUND(
        100.0 * SUM(CASE WHEN m.credit_label = 'Reject' THEN d.funded_amount ELSE 0 END) 
        / NULLIF(SUM(d.funded_amount), 0), 
        2
    ) AS high_risk_pct,
    
    -- Time Metrics
    MIN(d.funding_date) AS first_deal_date,
    MAX(d.funding_date) AS latest_deal_date

FROM discounting_transactions d
JOIN msme_scoring m ON d.msme_id = m.msme_id
GROUP BY d.lender_name;