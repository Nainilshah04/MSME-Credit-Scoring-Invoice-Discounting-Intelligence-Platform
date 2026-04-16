# 🎯 MSME Credit Scoring Platform — Interview Preparation Guide

## For: Nainil Shah

---

## Q1: "Tell me about your project"

### ✅ What to Say:
> "Sir, I built an AI-powered alternative credit scoring platform for Indian MSMEs. 
> India has 6.3 crore MSMEs, but 86% can't get bank loans because they have no CIBIL score. 
> My platform uses alternative data — GST filing history, UPI transaction patterns, 
> bank statement analysis, and even pre-GST VAT compliance — to generate a credit score 
> between 300-900. I also built an invoice risk analyzer that helps financiers decide 
> whether to discount an MSME's invoice. The entire platform includes ML models with 85%+ 
> accuracy, a 6-page Power BI dashboard, and a Streamlit web app."

### ❌ What NOT to Say:
- "I just followed a tutorial"
- "I used random data"
- "I don't know how the model works"

### 🔑 Technical Terms to Use:
- Alternative credit scoring
- Feature engineering
- GST compliance analytics
- Invoice discounting (TReDS)
- Ensemble models (Random Forest, XGBoost)

---

## Q2: "Why did you choose this problem?"

### ✅ What to Say:
> "Sir, I chose this because it's a real ₹19 lakh crore problem validated by RBI data. 
> Companies like KredX and M1xchange have raised hundreds of crores solving this. 
> The RBI launched TReDS specifically for invoice discounting. I wanted to understand 
> how fintech companies use alternative data for credit assessment — something 
> traditional banks still struggle with. This problem also let me combine ML, 
> SQL, Power BI, and web development in one project."

### 🔑 Keywords:
- RBI TReDS platform
- Financial inclusion
- Alternative data
- Credit gap
- India Stack (Aadhaar, UPI, GST)

---

## Q3: "How did you handle missing credit history for MSMEs?"

### ✅ What to Say:
> "Sir, that's exactly the core problem. Traditional banks need CIBIL scores, 
> but MSMEs don't have them. I used alternative data sources:
> 
> 1. **GST filing regularity** — if an MSME files GST 12/12 months on time, 
>    they're disciplined about compliance
> 2. **UPI transaction consistency** — I calculate this as 1 minus the coefficient 
>    of variation of monthly inflows. Higher consistency means stable cash flow
> 3. **Pre-GST VAT/C-Form history** — businesses with VAT compliance before 2017 
>    get additional credit for long-term compliance
> 4. **Bank statement analysis** — bounce rates and low balance days indicate 
>    financial stress
> 
> These features combined give us a reliable credit score without needing CIBIL."

### 🔑 Formula to Remember:

UPI Consistency = 1 - (Standard Deviation / Mean)
GST Score = Filing(40%) + On-time(25%) + No-Penalty(20%) + Growth(15%)


---

## Q4: "What's the difference between your two models?"

### ✅ What to Say:
> "Sir, I have two separate models solving two different problems:
> 
> **Model 1 — Credit Scoring:**
> - Input: Business profile (age, industry, GST, UPI, bank data)
> - Output: Credit score 300-900 + Approve/Review/Reject
> - Purpose: Should we give this MSME a loan?
> - Key metric: Overall accuracy and F1-score
> 
> **Model 2 — Invoice Risk:**
> - Input: Invoice details (amount, buyer type, payment history)
> - Output: Risk level (Low/Medium/High) + payment probability
> - Purpose: Should a financier discount this specific invoice?
> - Key metric: Precision on High Risk class — because a false negative 
>   means the financier loses money on a bad invoice
> 
> The models are connected — an MSME's credit score feeds into 
> their invoice risk assessment."

---

## Q5: "If you had real data, what would you do differently?"

### ✅ What to Say:
> "Great question sir. With real data, I would:
> 
> 1. **Integrate GST API** — pull real filing data from gst.gov.in
> 2. **Use Account Aggregator** — RBI's consent-based framework to get 
>    bank statements directly
> 3. **Add NLP** — analyze GST notices and bank correspondence for risk signals
> 4. **Time-series modeling** — track score changes over months, not just snapshot
> 5. **A/B testing** — compare model decisions with actual loan outcomes
> 6. **Explainable AI (SHAP)** — show exactly why each MSME got their score
> 7. **Real-time retraining** — update model monthly with new data
> 
> I used synthetic data because MSME financial data is sensitive, 
> but the architecture is designed to plug in real data sources."

---

## Q6: "Explain your feature engineering"

### ✅ What to Say:
> "Sir, I created 4 engineered features that improved model accuracy by 15-20%:
> 
> 1. **turnover_per_year** = Monthly Turnover × 12 / Business Age
>    → Normalized turnover accounting for business maturity
> 
> 2. **upi_to_turnover_ratio** = UPI Inflow / Turnover
>    → How much business is digital vs cash
> 
> 3. **compliance_consistency_score** = GST Score × UPI Consistency / 100
>    → Combined compliance and financial stability metric
> 
> 4. **loan_to_turnover_ratio** = Loan Amount / Annual Turnover
>    → Are they borrowing within their capacity?
> 
> Additionally, I auto-calculate GST Compliance Score from raw inputs 
> using a weighted formula: Filing(40%) + On-time(25%) + No-Penalty(20%) + Growth(15%)"

---

## Q7: "Tell me about your Power BI dashboard"

### ✅ What to Say:
> "Sir, I built a 6-page themed dashboard:
> 
> 1. **Executive Summary** (Blue) — KPIs, donut charts, state map
> 2. **Credit Analytics** (Green) — Score distribution, age vs approval trend
> 3. **Invoice Marketplace** (Orange) — Aging buckets, deal quality funnel
> 4. **Lender Performance** (Purple) — Portfolio volume, settlement rates
> 5. **Advanced Analytics** (Teal) — Scatter plots, correlation matrix, anomaly detection
> 6. **MSME Detail** (Indigo) — Drillthrough page for individual profiles
> 
> Key features: DAX measures, conditional formatting, slicers, 
> drillthrough navigation, and each page has a unique color theme 
> following Material Design principles."

---

## Q8: "What is VAT and C-Form? Why did you include them?"

### ✅ What to Say:
> "Sir, VAT (Value Added Tax) was the state-level tax before GST came in 2017. 
> TIN was the Tax Identification Number for VAT registration. 
> C-Form was issued for interstate business transactions under CST.
> 
> I included them because — if an MSME was VAT-compliant for 5-7 years 
> before GST, it shows **long-term tax discipline**. This is a very strong 
> signal of creditworthiness that most fintech platforms ignore. 
> In my model, pre-GST compliance can add up to 50 bonus points 
> to the credit score."

---

## Q9: "How does invoice discounting work?"

### ✅ What to Say:
> "Sir, invoice discounting is like getting an advance on your bill:
> 
> 1. MSME sells goods to Buyer → Invoice of ₹10 Lakhs, due in 90 days
> 2. MSME needs money NOW, can't wait 90 days
> 3. Financier/Lender buys the invoice at 88% → Pays ₹8.8L to MSME today
> 4. After 90 days, Buyer pays ₹10L to Financier
> 5. Financier's profit = ₹1.2L (12% discount)
> 
> The risk is: What if Buyer doesn't pay? That's why my Invoice Risk Model 
> predicts payment probability. RBI's TReDS platform (M1xchange, RXIL) 
> facilitates this for MSMEs."

---

## Q10: "What challenges did you face?"

### ✅ What to Say:
> "Main challenges:
> 
> 1. **Data availability** — real MSME data is confidential, so I generated 
>    realistic synthetic data with proper Indian context
> 2. **Feature engineering** — figuring out which alternative data points 
>    actually predict creditworthiness
> 3. **Model interpretability** — banks need explainable decisions, 
>    not just predictions. That's why I added score breakdowns
> 4. **Database schema design** — 9 interconnected tables with proper 
>    foreign keys and indexes for Power BI performance
> 5. **Power BI + SQLite integration** — needed ODBC driver setup 
>    and optimized views for dashboard performance"

---

## 🎯 Quick Stats to Remember:

| Stat | Value |
|------|-------|
| Total MSMEs in India | 6.3 Crore |
| Credit Gap | ₹19 Lakh Crore |
| MSMEs without formal credit | 86% |
| Our dataset | 5,000 MSMEs + 3,000 Invoices |
| Database records | 63,807 |
| SQL queries | 25 |
| Power BI pages | 6 |
| Best model accuracy | ~87% (XGBoost) |
| Credit score range | 300-900 |
| Feature importance #1 | GST Compliance (28%) |

---

## 💡 Bonus: Questions YOU Should Ask the Interviewer

1. "Sir, does your company use alternative data for credit assessment?"
2. "Are you integrated with RBI's Account Aggregator framework?"
3. "How do you handle model drift in production credit models?"
4. "What's your approach to explainable AI for lending decisions?"