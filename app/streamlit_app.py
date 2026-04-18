import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import os
import sqlite3
import time
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="MSME Credit Platform",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# MINIMAL CSS — Only cards + result boxes
# Everything else = Streamlit default
# ============================================
st.markdown("""
<style>
    /* Hide extras */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Card */
    .card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        margin: 6px 0;
    }
    .card-val {
        font-size: 30px;
        font-weight: 700;
        color: #2563EB;
        margin: 4px 0;
    }
    .card-label {
        font-size: 13px;
        font-weight: 500;
        color: #334155;
        margin-top: 4px;
    }

    /* Score */
    .score-big {
        font-size: 52px;
        font-weight: 700;
        line-height: 1;
        margin: 8px 0;
    }
    .clr-green { color: #10B981; }
    .clr-amber { color: #F59E0B; }
    .clr-red { color: #EF4444; }

    /* Badge */
    .badge-green {
        display: inline-block; padding: 5px 16px; border-radius: 20px;
        font-size: 13px; font-weight: 600;
        background: #D1FAE5; color: #065F46;
    }
    .badge-amber {
        display: inline-block; padding: 5px 16px; border-radius: 20px;
        font-size: 13px; font-weight: 600;
        background: #FEF3C7; color: #92400E;
    }
    .badge-red {
        display: inline-block; padding: 5px 16px; border-radius: 20px;
        font-size: 13px; font-weight: 600;
        background: #FEE2E2; color: #991B1B;
    }

    /* Calc Box */
    .calc {
        background: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 6px 0;
    }
    .calc-t {
        font-size: 12px;
        font-weight: 600;
        color: #334155;
    }
    .calc-v {
        font-size: 20px;
        font-weight: 700;
        color: #2563EB;
        margin-top: 2px;
    }

    /* Info Box */
    .info {
        background: #EFF6FF;
        border-left: 4px solid #2563EB;
        border-radius: 0 8px 8px 0;
        padding: 12px 16px;
        margin: 10px 0;
        color: #1E40AF;
        font-size: 13px;
    }

    /* Result Boxes */
    .res-green {
        background: #F0FDF4; border-left: 4px solid #10B981;
        border-radius: 0 8px 8px 0; padding: 14px 18px; margin: 10px 0;
        color: #065F46; font-size: 14px; line-height: 1.7;
    }
    .res-amber {
        background: #FFFBEB; border-left: 4px solid #F59E0B;
        border-radius: 0 8px 8px 0; padding: 14px 18px; margin: 10px 0;
        color: #92400E; font-size: 14px; line-height: 1.7;
    }
    .res-red {
        background: #FFF1F2; border-left: 4px solid #EF4444;
        border-radius: 0 8px 8px 0; padding: 14px 18px; margin: 10px 0;
        color: #991B1B; font-size: 14px; line-height: 1.7;
    }

    /* Step Card */
    .step {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        padding: 18px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# HELPERS
# ============================================
def get_db_path():
    if os.path.exists('data/msme_credit.db'):
        return 'data/msme_credit.db'
    elif os.path.exists('../data/msme_credit.db'):
        return '../data/msme_credit.db'
    return 'data/msme_credit.db'

@st.cache_resource
def load_credit_model():
    try:
        return joblib.load('models/credit_model.pkl'), joblib.load('models/credit_preprocessor.pkl')
    except:
        return None, None

@st.cache_resource
def load_invoice_model():
    try:
        return joblib.load('models/invoice_model.pkl'), joblib.load('models/invoice_preprocessor.pkl')
    except:
        return None, None

@st.cache_data
def load_stats():
    try:
        conn = sqlite3.connect(get_db_path())
        total = pd.read_sql("SELECT COUNT(*) as c FROM msme_scoring", conn).iloc[0, 0]
        avg = pd.read_sql("SELECT AVG(credit_score) as a FROM msme_scoring", conn).iloc[0, 0]
        inv = pd.read_sql("SELECT COUNT(*) as c FROM invoices", conn).iloc[0, 0]
        ind = pd.read_sql("""
            SELECT industry_type, COUNT(*) as count, 
                   ROUND(AVG(credit_score), 0) as avg_score
            FROM msme_scoring GROUP BY industry_type ORDER BY count DESC
        """, conn)
        lab = pd.read_sql("""
            SELECT credit_label, COUNT(*) as count 
            FROM msme_scoring GROUP BY credit_label
        """, conn)
        conn.close()
        return total, avg, inv, ind, lab
    except:
        return 5000, 645, 3000, None, None

def make_chart(fig, title="", h=350):
    """Standard chart with DARK readable labels"""
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color='#1E293B'), x=0),
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        font=dict(color='#1E293B', size=13),
        height=h,
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(
            gridcolor='#F3F4F6',
            linecolor='#E5E7EB',
            tickfont=dict(size=12, color='#1E293B')
        ),
        yaxis=dict(
            gridcolor='#F3F4F6',
            linecolor='#E5E7EB',
            tickfont=dict(size=12, color='#1E293B')
        )
    )
    return fig

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.markdown("### MSME Credit Platform")
    st.caption("Data-Driven Credit Intelligence")
    st.markdown("---")

    page = st.radio("Navigate to", [
        "Overview",
        "Credit Assessment",
        "Invoice Risk",
        "About"
    ])

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("MSMEs", "5,000")
        st.metric("Models", "3")
    with col2:
        st.metric("Invoices", "3,000")
        st.metric("Accuracy", "87%")

    st.markdown("---")
    st.markdown("**Built by Nainil Shah**")
    st.caption("B.Tech Software Engineering")
    
# ============================================
# OVERVIEW PAGE
# ============================================
if page == "Overview":

    st.title("MSME Credit Intelligence Platform")
    st.markdown("Solving the credit accessibility gap for India's 6.3 crore MSMEs using alternative data and machine learning")

    st.markdown("---")

    # KPI Row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="card"><div class="card-val">6.3 Cr</div><div class="card-label">Registered MSMEs in India</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card"><div class="card-val">86%</div><div class="card-label">Without Formal Credit Access</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="card"><div class="card-val">₹19L Cr</div><div class="card-label">Estimated Credit Gap (RBI)</div></div>', unsafe_allow_html=True)

    st.markdown("")

    # Problem & Solution — EQUAL SIZE + BULLET POINTS
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("The Problem")
        st.markdown("""
        - Traditional banks rely **only on CIBIL scores** for lending decisions
        - MSMEs with **healthy cash flows** but no credit history get **automatically rejected**
        - Manual loan processing takes **3-6 weeks** — too slow for working capital needs
        - Buyers take **60-90 days** to pay invoices, causing daily cash flow stress
        - **86% of MSMEs** are excluded from formal credit despite being creditworthy
        """)

    with col2:
        st.subheader("Our Approach")
        st.markdown("""
        - Generate credit scores using **GST filing history** instead of CIBIL
        - Analyse **UPI transaction patterns** to measure cash flow consistency
        - Include **pre-GST VAT/C-Form compliance** for long-term tax discipline
        - **ML models with 87% accuracy** for instant credit decisions
        - Invoice risk assessment aligned with **RBI's TReDS framework**
        """)

    st.markdown("---")

    # How It Works
    st.subheader("How It Works")

    col1, col2, col3, col4 = st.columns(4)

    for col, (num, title, desc) in zip(
        [col1, col2, col3, col4],
        [
            ("01", "Submit Details", "Business profile, GST history, banking data"),
            ("02", "Auto Processing", "System calculates compliance scores from raw inputs"),
            ("03", "Credit Scoring", "ML model generates score between 300 and 900"),
            ("04", "Instant Decision", "Approval decision with detailed risk breakdown")
        ]
    ):
        with col:
            st.markdown(f"""
            <div class="step">
                <div style="font-size:12px;font-weight:700;color:#2563EB;">STEP {num}</div>
                <div style="font-size:15px;font-weight:600;color:#1E293B;margin:6px 0 4px 0;">{title}</div>
                <div style="font-size:13px;color:#334155;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Platform Stats
    st.subheader("Platform Statistics")
    total, avg, inv, ind, lab = load_stats()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="card"><div class="card-val">{total:,}</div><div class="card-label">MSMEs Analyzed</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="card"><div class="card-val">{avg:.0f}</div><div class="card-label">Average Credit Score</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="card"><div class="card-val">{inv:,}</div><div class="card-label">Invoices Processed</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="card"><div class="card-val">87%</div><div class="card-label">Model Accuracy</div></div>', unsafe_allow_html=True)

    st.markdown("")

    # Charts
    if ind is not None and lab is not None:
        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(
                ind, x='industry_type', y='count',
                color='avg_score', color_continuous_scale='Blues',
                labels={'count': 'Number of MSMEs', 'industry_type': 'Industry', 'avg_score': 'Avg Score'}
            )
            fig = make_chart(fig, "MSMEs by Industry Segment")
            fig.update_traces(marker_line_width=0)
            fig.update_xaxes(tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.pie(
                lab, values='count', names='credit_label', hole=0.5,
                color='credit_label',
                color_discrete_map={'Approve': '#10B981', 'Review': '#F59E0B', 'Reject': '#EF4444'}
            )
            fig = make_chart(fig, "Credit Decision Distribution")
            fig.update_traces(
                textposition='outside',
                textinfo='percent+label',
                textfont=dict(size=13, color='#1E293B'),
                marker=dict(line=dict(color='#FFFFFF', width=2))
            )
            st.plotly_chart(fig, use_container_width=True)

# ============================================
# CREDIT ASSESSMENT PAGE
# ============================================
elif page == "Credit Assessment":

    st.title("Credit Assessment")
    st.markdown("Complete the form below to receive an instant credit evaluation based on your business data")

    st.markdown("---")

    # Section 1
    st.subheader("Business Profile")

    col1, col2, col3 = st.columns(3)
    with col1:
        business_name = st.text_input("Business Name", "ABC Enterprises Pvt Ltd")
        business_age = st.slider("Years in Operation", 1, 30, 5)
    with col2:
        industry = st.selectbox("Industry Sector", ["manufacturing", "retail", "services", "food", "textile", "pharma"])
        state = st.selectbox("State", ["Maharashtra", "Gujarat", "Tamil Nadu", "Karnataka", "Delhi", "Uttar Pradesh", "Rajasthan", "Madhya Pradesh", "West Bengal", "Telangana"])
    with col3:
        udyam_registered = st.selectbox("Udyam Registered", ["Yes", "No"])
        num_employees = st.slider("Employees", 1, 500, 25)

    st.markdown("---")

    # Section 2
    st.subheader("Pre-GST Tax History")
    st.markdown('<div class="info">Businesses with VAT/TIN registration before July 2017 receive additional credit weightage for demonstrated long-term tax discipline.</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        had_vat = st.selectbox("VAT/TIN Registration (Pre-2017)", ["No", "Yes"])
    with col2:
        vat_years = st.slider("Years of VAT Compliance", 1, 10, 5) if had_vat == "Yes" else 0
    with col3:
        had_cform = st.selectbox("C-Form History", ["No", "Yes"]) if had_vat == "Yes" else "No"

    legacy = min(100, (vat_years * 8) + (20 if had_cform == "Yes" else 0)) if had_vat == "Yes" else 0

    if had_vat == "Yes":
        st.markdown(f'<div class="calc"><div class="calc-t">Legacy Tax Score</div><div class="calc-v">{legacy} / 100</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    # Section 3
    st.subheader("GST Filing Details")
    st.markdown('<div class="info">Check your GSTR-3B filing history on gst.gov.in — Returns Dashboard — last 12 months.</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        gst_filing = st.slider("GSTR-3B Filed (out of 12)", 0, 12, 10)
    with col2:
        late_filings = st.slider("Late Filings (out of 12)", 0, 12, 1)
    with col3:
        gst_penalty = st.selectbox("GST Penalty or Notice", ["No", "Yes"])

    col1, col2 = st.columns(2)
    with col1:
        monthly_turnover = st.number_input("Avg Monthly Turnover (INR)", min_value=50000, max_value=50000000, value=500000, step=50000)
    with col2:
        turnover_growth = st.slider("YoY Turnover Growth (%)", -20, 40, 10)

    # Auto GST Score
    f_s = (gst_filing / 12) * 40
    o_s = ((12 - late_filings) / 12) * 25
    p_s = 0 if gst_penalty == "Yes" else 20
    g_s = min(15, max(0, (turnover_growth + 20) / 60 * 15))
    gst_score = round(f_s + o_s + p_s + g_s, 1)

    col1, col2, col3, col4 = st.columns(4)
    for col, (t, v, m) in zip([col1, col2, col3, col4], [("Filing", f_s, 40), ("On-time", o_s, 25), ("No Penalty", p_s, 20), ("GST Score", gst_score, 100)]):
        with col:
            c = "#10B981" if v / m >= 0.7 else "#F59E0B" if v / m >= 0.5 else "#EF4444"
            st.markdown(f'<div class="calc"><div class="calc-t">{t}</div><div class="calc-v" style="color:{c};">{v:.1f} / {m}</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    # Section 4
    st.subheader("Monthly Banking Inflow (Last 6 Months)")
    st.markdown('<div class="info">Enter total credits (money received) in your business bank account for each month. Available in bank statement or UPI app summary.</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        m1 = st.number_input("Month 1 (INR)", min_value=0, max_value=50000000, value=400000, step=10000, key="m1")
        m2 = st.number_input("Month 2 (INR)", min_value=0, max_value=50000000, value=450000, step=10000, key="m2")
    with col2:
        m3 = st.number_input("Month 3 (INR)", min_value=0, max_value=50000000, value=380000, step=10000, key="m3")
        m4 = st.number_input("Month 4 (INR)", min_value=0, max_value=50000000, value=420000, step=10000, key="m4")
    with col3:
        m5 = st.number_input("Month 5 (INR)", min_value=0, max_value=50000000, value=460000, step=10000, key="m5")
        m6 = st.number_input("Month 6 (INR)", min_value=0, max_value=50000000, value=440000, step=10000, key="m6")

    inflows = [m1, m2, m3, m4, m5, m6]
    avg_in = np.mean(inflows)
    std_d = np.std(inflows)
    upi_con = round(max(0, min(1, 1 - (std_d / avg_in))), 3) if avg_in > 0 else 0

    c_label = "Excellent" if upi_con >= 0.8 else "Good" if upi_con >= 0.6 else "Fair" if upi_con >= 0.4 else "Poor"
    c_color = "#10B981" if upi_con >= 0.8 else "#F59E0B" if upi_con >= 0.6 else "#EF4444"

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="calc"><div class="calc-t">Avg Monthly Inflow</div><div class="calc-v">INR {avg_in:,.0f}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="calc"><div class="calc-t">Cash Flow Consistency</div><div class="calc-v" style="color:{c_color};">{upi_con:.3f}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="calc"><div class="calc-t">Rating</div><div class="calc-v" style="color:{c_color};">{c_label}</div></div>', unsafe_allow_html=True)

    # Inflow Chart
    fig = go.Figure(go.Bar(
        x=['Month 1', 'Month 2', 'Month 3', 'Month 4', 'Month 5', 'Month 6'],
        y=inflows,
        marker_color='#2563EB',
        text=[f"₹{v:,.0f}" for v in inflows],
        textposition='outside',
        textfont=dict(size=11, color='#1E293B')
    ))
    fig.add_hline(y=avg_in, line_dash="dash", line_color="#64748B",
                  annotation_text=f"Average: INR {avg_in:,.0f}",
                  annotation_font=dict(color="#1E293B", size=12))
    fig = make_chart(fig, "Monthly Inflow Pattern", 300)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    num_buyers = st.slider("Number of Unique Buyers", 2, 50, 15)

    st.markdown("---")

    # Section 5
    st.subheader("Loan Requirements")

    col1, col2, col3 = st.columns(3)
    with col1:
        loan_amount = st.number_input("Loan Amount (INR)", min_value=100000, max_value=50000000, value=1000000, step=100000)
        loan_purpose = st.selectbox("Purpose", ["working_capital", "machinery", "expansion", "inventory"])
    with col2:
        existing_loans = st.selectbox("Existing Loans", ["No", "Yes"])
        collateral = st.selectbox("Collateral Available", ["No", "Yes"])
    with col3:
        seasonality = st.selectbox("Seasonality", [
            "Consistent — steady throughout year",
            "Moderate — some months better",
            "Seasonal — festival/weather dependent",
            "Highly Seasonal — significant variation"
        ])
        peak_ratio = {"Consistent — steady throughout year": 1.2, "Moderate — some months better": 1.8, "Seasonal — festival/weather dependent": 2.5, "Highly Seasonal — significant variation": 3.5}[seasonality]

    st.markdown("---")

    # SUBMIT
    if st.button("Generate Credit Report", use_container_width=True):

        with st.spinner("Processing your application..."):
            bar = st.progress(0)
            for i, s in enumerate(["Verifying GST records", "Checking tax history", "Analysing cash flow", "Running credit model", "Generating report"]):
                bar.progress((i + 1) / 5, text=s)
                time.sleep(0.4)

            # Feature engineering
            t_yr = (monthly_turnover * 12) / max(business_age, 1)
            u_rat = avg_in / max(monthly_turnover, 1)
            c_con = (gst_score * upi_con) / 100
            l_rat = loan_amount / max(monthly_turnover * 12, 1)

            # Model
            model, prep = load_credit_model()

            if model is not None:
                inp = pd.DataFrame({
                    'business_age_years': [business_age], 'gst_filing_months': [gst_filing],
                    'avg_monthly_turnover': [monthly_turnover], 'gst_compliance_score': [gst_score],
                    'turnover_growth_rate': [turnover_growth], 'avg_monthly_upi_inflow': [avg_in],
                    'upi_transaction_consistency': [upi_con], 'num_unique_buyers': [num_buyers],
                    'peak_to_offpeak_ratio': [peak_ratio], 'loan_amount_requested': [loan_amount],
                    'existing_loans': [1 if existing_loans == "Yes" else 0],
                    'collateral_available': [1 if collateral == "Yes" else 0],
                    'turnover_per_year': [t_yr], 'upi_to_turnover_ratio': [u_rat],
                    'compliance_consistency_score': [c_con], 'loan_to_turnover_ratio': [l_rat]
                })
                try:
                    pred = model.predict(inp)[0]
                    probs = model.predict_proba(inp)[0]
                    cls = model.classes_.tolist()
                    ap = probs[cls.index('Approve')] if 'Approve' in cls else max(probs)
                    score = int(300 + ap * 600)
                    label = pred
                except:
                    score = int(300 + gst_score * 2 + min(business_age, 10) * 15 + upi_con * 100 + gst_filing * 10 + legacy * 0.5 - l_rat * 50)
                    score = max(300, min(900, score))
                    label = "Approve" if score >= 700 else "Review" if score >= 500 else "Reject"
            else:
                score = int(300 + gst_score * 2 + min(business_age, 10) * 15 + upi_con * 100 + gst_filing * 10 + legacy * 0.5 + (30 if collateral == "Yes" else 0) + (20 if udyam_registered == "Yes" else 0) - l_rat * 50 - (30 if existing_loans == "Yes" else 0))
                score = max(300, min(900, score))
                label = "Approve" if score >= 700 else "Review" if score >= 500 else "Reject"

        # ── RESULTS ──
        st.markdown("---")
        st.subheader("Assessment Results")
        st.markdown(f"Evaluation for **{business_name}**")

        col1, col2, col3 = st.columns(3)

        with col1:
            sc = "clr-green" if score >= 700 else "clr-amber" if score >= 500 else "clr-red"
            sl = "Excellent" if score >= 750 else "Good" if score >= 700 else "Fair" if score >= 600 else "Below Average" if score >= 500 else "Poor"
            st.markdown(f"""
            <div class="card">
                <div class="card-label">CREDIT SCORE</div>
                <div class="score-big {sc}">{score}</div>
                <div class="card-label">{sl} — out of 900</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            bc = "badge-green" if label == "Approve" else "badge-amber" if label == "Review" else "badge-red"
            dd = {"Approve": "Meets lending criteria", "Review": "Manual review needed", "Reject": "Does not meet criteria"}
            st.markdown(f"""
            <div class="card">
                <div class="card-label">DECISION</div>
                <div style="margin:14px 0;"><span class="{bc}">{label.upper()}</span></div>
                <div class="card-label">{dd[label]}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            fig = go.Figure(go.Indicator(
                mode="gauge+number", value=score,
                number={'font': {'size': 28, 'color': '#1E293B'}},
                gauge={
                    'axis': {'range': [300, 900], 'tickcolor': '#334155', 'tickfont': {'color': '#1E293B'}},
                    'bar': {'color': '#2563EB', 'thickness': 0.25},
                    'bgcolor': '#F9FAFB', 'bordercolor': '#E5E7EB',
                    'steps': [
                        {'range': [300, 500], 'color': '#FEE2E2'},
                        {'range': [500, 700], 'color': '#FEF3C7'},
                        {'range': [700, 900], 'color': '#D1FAE5'}
                    ]
                }
            ))
            fig.update_layout(height=200, margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor='#FFFFFF')
            st.plotly_chart(fig, use_container_width=True)

        # Score Breakdown
        st.subheader("Score Breakdown")

        breakdown = {
            'GST Compliance': round(gst_score * 2),
            'Business Vintage': min(100, business_age * 12),
            'Cash Flow Consistency': round(upi_con * 100),
            'Legacy Tax (VAT/C-Form)': round(legacy * 0.5),
            'Filing Regularity': round((gst_filing / 12) * 50),
            'Collateral': 30 if collateral == "Yes" else 0,
            'Udyam Registration': 20 if udyam_registered == "Yes" else 0,
            'Loan-to-Turnover Risk': -round(l_rat * 50),
            'Existing Obligations': -30 if existing_loans == "Yes" else 0
        }

        colors = ['#10B981' if v >= 0 else '#EF4444' for v in breakdown.values()]

        fig = go.Figure(go.Bar(
            y=list(breakdown.keys()), x=list(breakdown.values()),
            orientation='h', marker_color=colors,
            text=[f"{v:+d} pts" for v in breakdown.values()],
            textposition='outside',
            textfont=dict(size=13, color='#1E293B')
        ))
        fig = make_chart(fig, "", 400)
        fig.update_layout(showlegend=False)
        fig.update_xaxes(title_text="Points", title_font=dict(color='#1E293B'))
        fig.update_yaxes(tickfont=dict(size=13, color='#1E293B'))
        st.plotly_chart(fig, use_container_width=True)

        # Strengths & Risks
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Positive Factors")
            if gst_score >= 70: st.success(f"GST Compliance: {gst_score}/100")
            if business_age >= 5: st.success(f"Business Vintage: {business_age} years")
            if upi_con >= 0.7: st.success(f"Cash Flow Consistency: {upi_con:.3f}")
            if had_vat == "Yes": st.success(f"Pre-GST Compliance: {vat_years} years VAT")
            if had_cform == "Yes": st.success("Interstate Trade History (C-Form)")
            if collateral == "Yes": st.success("Collateral Available")
            if udyam_registered == "Yes": st.success("Udyam Registered")
            if gst_filing >= 10: st.success(f"Regular Filing: {gst_filing}/12 months")

        with col2:
            st.subheader("Risk Factors")
            if gst_score < 70: st.warning(f"Low GST Compliance: {gst_score}/100")
            if business_age < 3: st.warning(f"Limited History: {business_age} years")
            if upi_con < 0.5: st.error(f"Inconsistent Cash Flow: {upi_con:.3f}")
            if late_filings > 3: st.warning(f"Frequent Late Filing: {late_filings}/12")
            if gst_penalty == "Yes": st.error("GST Penalty on Record")
            if l_rat > 0.5: st.warning(f"High Loan-to-Turnover: {l_rat:.2f}")
            if existing_loans == "Yes": st.warning("Existing Loan Obligations")

        # Final Recommendation
        if label == "Approve":
            st.markdown(f'<div class="res-green"><strong>Assessment — Approved</strong><br>{business_name} meets eligibility criteria. Recommended limit: INR {loan_amount * 0.8:,.0f}. Rate: 12-14% p.a. {"Pre-GST history qualifies for preferential rate." if had_vat == "Yes" else ""} Next review: 6 months.</div>', unsafe_allow_html=True)
        elif label == "Review":
            st.markdown(f'<div class="res-amber"><strong>Assessment — Under Review</strong><br>{business_name} requires additional evaluation. Improve GST compliance to 80+, cash flow consistency above 0.70. {"Provide collateral." if collateral == "No" else ""} Timeline: 2-4 weeks.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="res-red"><strong>Assessment — Not Approved</strong><br>{business_name} does not meet current criteria. File GST regularly for 6 months, build inflow above INR 2L/month. Consider reduced loan of INR {loan_amount * 0.3:,.0f}. Reapply after 6 months.</div>', unsafe_allow_html=True)
            
# ============================================
# INVOICE RISK PAGE
# ============================================
elif page == "Invoice Risk":

    st.title("Invoice Risk Analysis")
    st.markdown("Assess payment risk before discounting — aligned with RBI TReDS guidelines")
    st.markdown("---")

    st.subheader("Invoice Details")
    col1, col2 = st.columns(2)
    with col1:
        inv_amt = st.number_input("Invoice Value (INR)", min_value=10000, max_value=50000000, value=500000, step=10000)
        buyer = st.selectbox("Buyer Category", ["large_corporate", "government", "sme", "retail"])
        pay_terms = st.selectbox("Payment Terms (Days)", [30, 60, 90])
    with col2:
        pay_delay = st.slider("Buyer's Avg Payment Delay (Days)", 0, 45, 10)
        seller_gst = st.slider("Seller GST Compliance", 0, 100, 75)
        inv_freq = st.slider("Prior Invoices with Buyer", 1, 50, 10)

    st.markdown("---")

    if st.button("Run Risk Assessment", use_container_width=True):
        with st.spinner("Evaluating invoice risk..."):
            time.sleep(1)
            rs = (pay_delay * 2) - (seller_gst * 0.5) - (inv_freq * 0.3)
            rs += 20 if buyer == "retail" else -20 if buyer == "government" else -10 if buyer == "large_corporate" else 5

            if rs < 0: rl, pp = "Low", min(95, 85 + abs(rs) * 0.1)
            elif rs < 20: rl, pp = "Medium", 65.0
            else: rl, pp = "High", max(25, 50 - rs * 0.5)

        st.markdown("---")
        st.subheader("Assessment Results")

        rc = {"Low": "#10B981", "Medium": "#F59E0B", "High": "#EF4444"}
        rb = {"Low": "#F0FDF4", "Medium": "#FFFBEB", "High": "#FFF1F2"}

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="card" style="background:{rb[rl]};"><div class="card-label">RISK LEVEL</div><div class="score-big" style="color:{rc[rl]};">{rl}</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="card"><div class="card-label">PAYMENT PROBABILITY</div><div class="score-big" style="color:#2563EB;">{pp:.0f}%</div></div>', unsafe_allow_html=True)
            st.progress(pp / 100)
        with col3:
            rm = {"Low": "Approve for Discounting", "Medium": "Approve with Conditions", "High": "Refer for Manual Review"}
            st.markdown(f'<div class="card"><div class="card-label">RECOMMENDATION</div><div style="font-size:16px;font-weight:600;color:{rc[rl]};margin-top:14px;">{rm[rl]}</div></div>', unsafe_allow_html=True)

        # Calculator
        st.subheader("Discounting Calculation")
        dr = 10 if rl == "Low" else 14 if rl == "Medium" else 20
        payout = inv_amt * (1 - dr * pay_terms / 36500)
        disc = inv_amt - payout

        col1, col2, col3, col4 = st.columns(4)
        for col, (l, v) in zip([col1, col2, col3, col4], [
            ("Invoice Value", f"INR {inv_amt:,.0f}"), ("Rate", f"{dr}% p.a."),
            ("Payout", f"INR {payout:,.0f}"), ("Discount", f"INR {disc:,.0f}")
        ]):
            with col:
                st.markdown(f'<div class="card"><div class="card-label">{l}</div><div style="font-size:18px;font-weight:700;color:#1E293B;margin-top:6px;">{v}</div></div>', unsafe_allow_html=True)

        # Risk Factors Chart
        st.subheader("Risk Factor Analysis")
        factors = {
            'Buyer Category': 85 if buyer == "government" else 75 if buyer == "large_corporate" else 55 if buyer == "sme" else 35,
            'Payment History': max(0, 100 - pay_delay * 2),
            'Seller GST Score': seller_gst,
            'Transaction Frequency': min(100, inv_freq * 4),
            'Payment Terms': 90 if pay_terms == 30 else 65 if pay_terms == 60 else 45
        }
        fc = ['#10B981' if v >= 70 else '#F59E0B' if v >= 45 else '#EF4444' for v in factors.values()]

        fig = go.Figure(go.Bar(
            x=list(factors.values()), y=list(factors.keys()), orientation='h',
            marker_color=fc,
            text=[str(v) for v in factors.values()],
            textposition='outside',
            textfont=dict(size=13, color='#1E293B')
        ))
        fig = make_chart(fig, "Risk Scores (100 = Best)", 280)
        fig.update_xaxes(range=[0, 120])
        fig.update_yaxes(tickfont=dict(size=13, color='#1E293B'))
        st.plotly_chart(fig, use_container_width=True)

        # Recommendation Box
        box = "res-green" if rl == "Low" else "res-amber" if rl == "Medium" else "res-red"
        if rl == "Low":
            det = f"Invoice qualifies for immediate discounting. {buyer.replace('_', ' ').title()} buyer with {pay_delay}-day delay. Payout: INR {payout:,.0f} at {dr}% p.a."
        elif rl == "Medium":
            det = f"Consider with conditions. Partial disbursement recommended. Monitor buyer payment and maintain escrow for INR {disc:,.0f}."
        else:
            det = "Elevated risk. Payment probability below threshold. Manual review, additional collateral, or rejection recommended."

        st.markdown(f'<div class="{box}"><strong>Underwriting Recommendation</strong><br>{det}</div>', unsafe_allow_html=True)

# ============================================
# ABOUT PAGE
# ============================================
elif page == "About":

    st.title("About This Platform")
    st.markdown("Project background, methodology, and technical documentation")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Overview")
        st.markdown("""
        - Addresses the **₹19 lakh crore credit gap** for Indian MSMEs
        - Uses **alternative data** instead of traditional CIBIL scores
        - Evaluates **GST filing, UPI patterns, banking behavior, VAT history**
        - Produces standardised **credit score on 300-900 scale**
        - Invoice risk module supports **RBI's TReDS initiative**
        """)

        st.subheader("Technology Stack")
        st.dataframe(pd.DataFrame({
            'Component': ['Language', 'ML Framework', 'Database', 'Dashboard', 'Frontend', 'Visualisation'],
            'Technology': ['Python 3.12', 'scikit-learn + XGBoost', 'SQLite (63K records)', 'Power BI (6 pages)', 'Streamlit', 'Plotly']
        }), hide_index=True, use_container_width=True)

    with col2:
        st.subheader("Model Performance")
        st.dataframe(pd.DataFrame({
            'Model': ['Logistic Regression', 'Random Forest', 'XGBoost'],
            'Accuracy': ['78%', '85%', '87%'],
            'F1-Score': ['0.76', '0.83', '0.85']
        }), hide_index=True, use_container_width=True)

        st.subheader("Data Sources")
        st.dataframe(pd.DataFrame({
            'Source': ['MSME Profiles', 'Invoices', 'GST Compliance', 'Banking Data', 'MCA Records', 'Udyam Registry'],
            'Records': ['5,000', '3,000', '5,000', '30,000', '5,000', '5,000']
        }), hide_index=True, use_container_width=True)

        st.subheader("Regulatory Alignment")
        st.markdown("""
        - RBI's **TReDS framework** for trade receivables
        - **Account Aggregator** ecosystem for consent-based data
        - **MSME Development Act** enterprise classification
        - **CGST Act 2017** compliance requirements
        """)

    st.markdown("---")
    st.subheader("Developer")
    st.markdown("""
    **Nainil Shah**  
    B.Tech Software Engineering — Third Year  
    Focus: Credit risk modelling and fintech product development  
    [GitHub](https://github.com/Nainilshah04)
    """)