<div align="center">

# 🏦 MSME Credit Scoring + Invoice Discounting Intelligence Platform

### AI-Powered Alternative Credit Assessment for India's 6.3 Crore MSMEs

[![Python](https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge&logo=streamlit)]https://msme-credit-scoring-invoice-discounting-intelligence-platform.streamlit.app/
[![Power BI](https://img.shields.io/badge/Power_BI-6_Pages-yellow?style=for-the-badge&logo=powerbi)](https://powerbi.microsoft.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML_Models-orange?style=for-the-badge&logo=scikit-learn)](https://scikit-learn.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-87%25_Accuracy-green?style=for-the-badge)](https://xgboost.readthedocs.io)
[![SQLite](https://img.shields.io/badge/SQLite-63K_Records-lightgrey?style=for-the-badge&logo=sqlite)](https://sqlite.org)
---

**🎯 Solving the ₹19 Lakh Crore MSME Credit Gap in India**

[Live Demo](#-live-demo) • [Features](#-features) • [Tech Stack](#-tech-stack) • [How to Run](#-how-to-run) • [Screenshots](#-screenshots)

</div>

---

## ❓ Problem Statement

India has **6.3 crore registered MSMEs**. Yet, **86% of them cannot get formal bank loans** — even if their GST filings and UPI transactions show healthy cash flows.

### Why?
- Traditional banks rely **only on CIBIL scores**
- MSMEs with **no credit history** get automatically rejected
- Manual loan processing takes **weeks to months**
- Buyers take **60-90 days** to pay invoices → working capital crisis

### The Numbers:
| Metric | Value |
|--------|-------|
| Registered MSMEs | 6.3 Crore |
| MSMEs without formal credit | 86% |
| MSME Credit Gap | ₹19 Lakh Crore |
| Average loan processing time | 3-6 weeks |
| Invoice payment delay | 60-90 days |

> **Source:** RBI Financial Stability Report, MSME Annual Report 2023-24

---

## ✅ Our Solution

This platform solves **two connected problems:**

### 1. 🤖 Alternative Credit Scoring
Generate a credit score (300-900) for MSMEs using **alternative data** instead of traditional CIBIL:

| Data Source | What It Tells Us |
|-------------|-----------------|
| GST Filing History | Tax compliance & regularity |
| UPI Transaction Patterns | Cash flow consistency |
| Bank Statement Analysis | Financial health |
| VAT/C-Form History | Pre-GST compliance (legacy) |
| Udyam Registration | Government recognition |
| Business Vintage | Stability & experience |

### 2. 📄 Invoice Discounting Intelligence
Assess whether an invoice will be paid on time and calculate risk level:
- **Low Risk** → Approve for Discounting
- **Medium Risk** → Approve with Conditions
- **High Risk** → Reject / Manual Review

---

## 🏗️ Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                      MSME CREDIT PLATFORM                   │
├─────────────┬─────────────┬─────────────┬───────────────────┤
│ DATA LAYER  │   ML LAYER  │  DASHBOARD  │     FRONTEND      │
│             │             │             │                   │
│  SQLite DB  │   Credit    │  Power BI   │   Streamlit App   │
│   63,807    │   Scoring   │   6 Pages   │      4 Pages      │
│   Records   │    Model    │             │                   │
│             │             │     DAX     │  • Credit Score   │
│   9 Tables  │   Invoice   │  Measures   │    Checker        │
│   3 Views   │    Risk     │             │  • Invoice Risk   │
│  25 Queries │    Model    │   Drill-    │    Analyzer       │
│             │             │  through    │  • Auto-calc      │
│  Synthetic  │   XGBoost   │             │    Scores         │
│  + Kaggle   │   Random    │   Slicers   │  • VAT/C-Form     │
│    Data     │   Forest    │             │    History        │
└─────────────┴─────────────┴─────────────┴───────────────────┘
```

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Language** | Python 3.12+ | Core development |
| **Data** | pandas, numpy, faker | Data generation & processing |
| **Database** | SQLite | Storage with 9 tables, 3 views |
| **ML Models** | scikit-learn, XGBoost | Credit scoring & invoice risk |
| **Dashboard** | Power BI | 6-page executive analytics |
| **Frontend** | Streamlit | Interactive web application |
| **Charts** | Plotly, Matplotlib, Seaborn | Visualizations |
| **Version Control** | Git + GitHub | Code management |

---

## ✨ Features

### 📊 Credit Score Checker
- **5-section input form** with realistic business questions
- **Auto-calculated** GST Compliance Score from filing data
- **Auto-calculated** UPI Consistency from 6-month inflow data
- **Pre-GST VAT/C-Form** history for legacy compliance
- **Visual score breakdown** with gauge chart
- **Personalized recommendations** based on risk factors

### 📄 Invoice Risk Analyzer
- **Buyer type analysis** (Government, Corporate, SME, Retail)
- **Payment probability** prediction with progress bar
- **Discount calculator** with dynamic rates
- **Risk factor breakdown** horizontal bar chart

### 📊 Power BI Dashboard (6 Pages)
| Page | Theme | Purpose |
|------|-------|---------|
| Executive Summary | CEO-level overview |
| Credit Analytics | Risk team deep dive |
| Invoice Marketplace | Lender opportunities |
| Lender Performance | Portfolio tracking |
| Advanced Analytics | Correlation & anomalies |
| MSME Detail | Drillthrough profiles |

### 🗄️ Database
- **63,807 total records** across 9 tables
- **25 production SQL queries** for analytics
- **6 Power BI-optimized views**

---

## 📁 Project Structure

```text
msme-fintech-platform/
│
├── app/
│   └── streamlit_app.py        # Streamlit web application
│
├── data/
│   ├── raw/                    # Original datasets (MSMEs, Invoices, Credit Risk)
│   ├── processed/              # Cleaned & Feature-engineered data
│   └── msme_credit.db          # Central SQLite database
│
├── dashboards/
│   └── MSME_Dashboard.pbix     # Power BI Dashboard file
│
├── models/
│   ├── credit_model.pkl        # XGBoost Credit Scoring model
│   └── invoice_model.pkl       # Random Forest Invoice Risk model
│
├── notebooks/
│   ├── 01_eda_analysis.ipynb   # Exploratory Data Analysis
│   ├── 02_credit_model.ipynb   # Model training & evaluation
│   └── 03_invoice_risk.ipynb   # Risk assessment logic
│
├── sql/
│   ├── schema.sql              # Database schema (9 tables)
│   ├── queries.sql             # 25 analytical queries for insights
│   └── views.sql               # 3 SQL views for Power BI connection
│
├── src/
│   ├── data_generator.py       # Python script for synthetic data
│   └── load_to_db.py           # ETL: Loading CSVs into SQLite
│
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## 📊 Model Performance

### 1. Credit Scoring Model
| Metric | Logistic Regression | Random Forest | XGBoost |
| :--- | :---: | :---: | :---: |
| **Accuracy** | ~78% | ~85% | **~87%** |
| **Precision** | ~76% | ~84% | **~86%** |
| **Recall** | ~77% | ~83% | **~85%** |
| **F1-Score** | ~76% | ~83% | **~85%** |

### 2. Invoice Risk Model
| Metric | Logistic Regression | Random Forest | XGBoost |
| :--- | :---: | :---: | :---: |
| **Accuracy** | ~75% | ~82% | **~84%** |
| **High Risk Precision** | ~73% | ~80% | **~83%** |

## 💡 Key Business Insights

> These insights were derived from the synthetic data modeling and exploratory analysis.

* **GST Compliance:** The #1 predictor of creditworthiness (**28% importance**).
* **Business Vintage:** Age ≥ 5 years shows a **78% higher approval rate**.
* **Sector Performance:** Manufacturing has the highest approval rate (**62%**).
* **Digital Footprint:** UPI consistency > 0.7 correlates with **85% approval**.
* **Risk Red Flags:** Total bounces > 5 lead to an **89% rejection rate**.
* **Payment Behavior:** Government buyers show **95% on-time** invoice payment.
* **Legacy Data:** Pre-GST VAT compliance adds a **15-20% credit score boost**.
* **Trust Factor:** Udyam registration significantly improves the trust score.

---

## 🌍 Real-World Context

This project is built considering the current MSME fintech landscape in India:

* **Credit Gap:** Addressing the **₹19 lakh crore** MSME credit gap in India.
* **Market Alignment:** Inspired by platforms like **TReDS (RBI)**, KredX, and Vayana Network.
* **India Stack:** Leverages the power of **UPI, GST, and Account Aggregator** frameworks for digital assessment.

---

## 🔮 Future Improvements

- [ ] **Real GST API:** Integration with `gst.gov.in`.
- [ ] **OCR Engine:** Bank statement PDF parser for automated data entry.
- [ ] **Account Aggregator:** RBI's AA framework for consent-based data sharing.
- [ ] **MLOps:** Real-time model retraining pipeline.
- [ ] **Localization:** Multi-language support (Hindi, Gujarati, Tamil).
- [ ] **Blockchain:** Decentralized invoice verification to prevent double-financing.

---

## 👨‍💻 Author

**Nainil Shah** *3rd Year IT Student | D.J. Sanghvi College of Engineering*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)]https://www.linkedin.com/in/nainil-shah-a440b728b/
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)]https://github.com/Nainilshah04

---

## 📄 License
This project is for educational and portfolio purposes.

<div align="center">

### ⭐ If you found this project helpful, please give it a star! ⭐

</div>