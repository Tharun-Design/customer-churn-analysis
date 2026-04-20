"""
streamlit_app.py
================
Customer Churn Analysis — Interactive Dashboard + ML Predictor
Author : Tharun Kumar Srinivasan
GitHub : https://github.com/Tharun-Design
Run    : python -m streamlit run app/streamlit_app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import os
import requests

BRAND = {
    "dark":    "#0d3b2e",
    "primary": "#1a7f5a",
    "accent":  "#4eca7f",
    "danger":  "#c0392b",
    "warning": "#d68910",
    "neutral": "#2e86ab",
    "bg":      "#f4f6f4",
    "surface": "#ffffff",
    "border":  "#dde8e4",
    "text":    "#0d1f1a",
    "muted":   "#5a7168",
}

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Customer Churn Analytics | Tharun Kumar",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
[data-testid="collapsedControl"] { display: none !important; }
section[data-testid="stSidebar"] {
    width: 280px !important;
    min-width: 280px !important;
    transform: translateX(0) !important;
    visibility: visible !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] {{ font-family: 'Inter', sans-serif !important; background-color: {BRAND['bg']} !important; }}
.block-container {{ padding-top: 1.5rem !important; padding-bottom: 2rem !important; }}
section[data-testid="stSidebar"] {{ background-color: {BRAND['dark']} !important; }}
section[data-testid="stSidebar"] .stMarkdown p, section[data-testid="stSidebar"] caption, section[data-testid="stSidebar"] small {{ color: #a8c4b8 !important; }}
section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {{ color: #ffffff !important; }}
section[data-testid="stSidebar"] label {{ color: #a8c4b8 !important; font-size: 11px !important; font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: 0.06em !important; }}
section[data-testid="stSidebar"] hr {{ border-color: #1f5c45 !important; }}
.page-header {{ background: linear-gradient(135deg, {BRAND['dark']} 0%, #1a5c42 100%); border-radius: 12px; padding: 24px 30px; margin-bottom: 22px; border-left: 5px solid {BRAND['accent']}; }}
.page-header-title {{ font-size: 22px; font-weight: 700; color: #ffffff; letter-spacing: -0.02em; margin: 0; }}
.page-header-sub {{ font-size: 13px; color: #a8c4b8; margin-top: 4px; }}
.page-header-meta {{ font-size: 12px; color: {BRAND['accent']}; margin-top: 8px; font-weight: 500; }}
.kpi-card {{ background: {BRAND['surface']}; border-radius: 10px; padding: 18px 20px; border: 1px solid {BRAND['border']}; border-top: 3px solid {BRAND['border']}; box-shadow: 0 1px 4px rgba(13,59,46,0.07); }}
.kpi-card.danger  {{ border-top-color: {BRAND['danger']}; }}
.kpi-card.warning {{ border-top-color: {BRAND['warning']}; }}
.kpi-card.neutral {{ border-top-color: {BRAND['neutral']}; }}
.kpi-card.primary {{ border-top-color: {BRAND['primary']}; }}
.kpi-label {{ font-size: 10px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: {BRAND['muted']}; margin-bottom: 8px; }}
.kpi-value {{ font-size: 28px; font-weight: 700; color: {BRAND['text']}; line-height: 1; letter-spacing: -0.02em; }}
.kpi-sub {{ font-size: 12px; color: {BRAND['muted']}; margin-top: 5px; }}
.kpi-badge {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; margin-top: 8px; }}
.kpi-badge.r {{ background: #fdecea; color: {BRAND['danger']}; }}
.kpi-badge.a {{ background: #fef9e7; color: {BRAND['warning']}; }}
.kpi-badge.b {{ background: #e8f4fd; color: {BRAND['neutral']}; }}
.kpi-badge.g {{ background: #e8f5ee; color: {BRAND['primary']}; }}
.section-title {{ font-size: 15px; font-weight: 700; color: {BRAND['text']}; margin: 26px 0 12px 0; padding-bottom: 8px; border-bottom: 2px solid {BRAND['border']}; }}
.insight-banner {{ background: #f0f7f4; border: 1px solid {BRAND['border']}; border-left: 3px solid {BRAND['primary']}; border-radius: 0 6px 6px 0; padding: 8px 14px; font-size: 12px; color: {BRAND['text']}; margin: 4px 0 12px 0; line-height: 1.5; }}
.risk-high   {{ background: #fdecea; border: 2px solid {BRAND['danger']};  border-radius: 12px; padding: 20px; text-align: center; }}
.risk-medium {{ background: #fef9e7; border: 2px solid {BRAND['warning']}; border-radius: 12px; padding: 20px; text-align: center; }}
.risk-low    {{ background: #e8f5ee; border: 2px solid {BRAND['primary']}; border-radius: 12px; padding: 20px; text-align: center; }}
.risk-title  {{ font-size: 20px; font-weight: 700; margin-bottom: 6px; }}
.risk-prob   {{ font-size: 36px; font-weight: 700; margin: 8px 0; }}
.risk-rec    {{ font-size: 13px; margin-top: 8px; }}
#MainMenu, footer, header {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    for p in ["data/churn.db", "../data/churn.db"]:
        if os.path.exists(p):
            conn = sqlite3.connect(p)
            df = pd.read_sql("SELECT * FROM customers", conn)
            conn.close()
            return df
    for p in ["data/cleaned/telco_churn_cleaned.csv", "../data/cleaned/telco_churn_cleaned.csv"]:
        if os.path.exists(p):
            return pd.read_csv(p)
    st.error("Data not found.")
    st.stop()

df_raw = load_data()
df_raw["Churn"] = pd.to_numeric(df_raw["Churn"], errors="coerce").fillna(0).astype(int)

CHART = dict(
    plot_bgcolor=BRAND["surface"], paper_bgcolor=BRAND["surface"],
    font=dict(family="Inter", color=BRAND["text"], size=11),
    title_font=dict(family="Inter", size=13, color=BRAND["text"]),
    margin=dict(t=42, b=24, l=10, r=10),
    xaxis=dict(gridcolor="#eef2f0", linecolor=BRAND["border"], tickfont=dict(size=11)),
    yaxis=dict(gridcolor="#eef2f0", linecolor=BRAND["border"], tickfont=dict(size=11)),
    legend=dict(bgcolor=BRAND["surface"], bordercolor=BRAND["border"], borderwidth=1),
)
CHART_NO_AX = {k: v for k, v in CHART.items() if k not in ("xaxis", "yaxis")}

def bar_colors(values):
    mx = max(values) if values else 1
    return [BRAND["danger"] if v/mx >= 0.70 else BRAND["warning"] if v/mx >= 0.40 else BRAND["primary"] for v in values]


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    logo_paths = ["app/logo.png", "logo.png", "../app/logo.png"]
    logo_found = next((p for p in logo_paths if os.path.exists(p)), None)
    col_logo, col_title = st.columns([1, 2.5])
    with col_logo:
        if logo_found:
            st.image(logo_found, width=56)
    with col_title:
        st.markdown("""<div style='color:white;font-weight:700;font-size:15px;'>Churn Analytics</div>
        <div style='color:#a8c4b8;font-size:11px;'>Tharun Kumar Srinivasan</div>""", unsafe_allow_html=True)
    st.divider()

    page = st.radio("Navigation", ["Dashboard", "Churn Predictor"], label_visibility="collapsed")

    if page == "Dashboard":
        st.markdown("**FILTERS**")
        contract_options = sorted(df_raw["Contract"].dropna().unique().tolist())
        sel_contract = st.multiselect("Contract Type", options=contract_options, default=contract_options)
        if not sel_contract: sel_contract = contract_options

        internet_options = sorted(df_raw["InternetService"].dropna().unique().tolist())
        sel_internet = st.multiselect("Internet Service", options=internet_options, default=internet_options)
        if not sel_internet: sel_internet = internet_options

        payment_options = sorted(df_raw["PaymentMethod"].dropna().unique().tolist())
        sel_payment = st.multiselect("Payment Method", options=payment_options, default=payment_options)
        if not sel_payment: sel_payment = payment_options

        t_min = int(df_raw["tenure"].min())
        t_max = int(df_raw["tenure"].max())
        sel_tenure = st.slider("Tenure Range (months)", t_min, t_max, (t_min, t_max))
        sel_senior = st.selectbox("Customer Type", ["All", "Senior Citizen", "Non-Senior"])
        sel_churn  = st.selectbox("Churn Status", ["All", "Churned", "Retained"])

    st.divider()
    st.caption("Dataset: Telco Customer Churn")
    st.caption(f"Records: {len(df_raw):,}")
    st.caption("github.com/Tharun-Design")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if page == "Dashboard":
    df = df_raw.copy()
    df = df[df["Contract"].isin(sel_contract)]
    df = df[df["InternetService"].isin(sel_internet)]
    df = df[df["PaymentMethod"].isin(sel_payment)]
    df = df[df["tenure"].between(sel_tenure[0], sel_tenure[1])]
    if sel_senior == "Senior Citizen": df = df[df["SeniorCitizen"] == 1]
    elif sel_senior == "Non-Senior":   df = df[df["SeniorCitizen"] == 0]
    if sel_churn == "Churned":    df = df[df["Churn"] == 1]
    elif sel_churn == "Retained": df = df[df["Churn"] == 0]

    if len(df) == 0:
        st.warning("No data matches the current filters.")
        st.stop()

    total      = len(df)
    churned    = int(df["Churn"].sum())
    retained   = total - churned
    churn_rate = round(churned/total*100, 1) if total > 0 else 0
    ret_rate   = round(retained/total*100, 1) if total > 0 else 0
    rev_risk   = round(df[df["Churn"]==1]["MonthlyCharges"].sum(), 0)
    rev_safe   = round(df[df["Churn"]==0]["MonthlyCharges"].sum(), 0)
    avg_ch     = round(df[df["Churn"]==1]["MonthlyCharges"].mean(), 2) if churned > 0 else 0
    avg_re     = round(df[df["Churn"]==0]["MonthlyCharges"].mean(), 2) if retained > 0 else 0

    is_default = (
        set(sel_contract) == set(contract_options) and
        set(sel_internet) == set(internet_options) and
        set(sel_payment)  == set(payment_options)  and
        sel_tenure == (t_min, t_max) and
        sel_senior == "All" and sel_churn == "All"
    )

    st.markdown(f"""
    <div class="page-header">
        <div class="page-header-title">Customer Churn Analytics Dashboard</div>
        <div class="page-header-sub">Telco Customer Retention Intelligence &nbsp;—&nbsp; Tharun Kumar Srinivasan</div>
        <div class="page-header-meta">
            {"Showing all 7,043 customers" if is_default else f"Showing {total:,} of {len(df_raw):,} customers (filters active)"}
            &nbsp;|&nbsp; Dataset: Telco Customer Churn (Kaggle)
        </div>
    </div>""", unsafe_allow_html=True)

    if not is_default:
        st.info(f"Filters active — {total:,} of {len(df_raw):,} customers in view")

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""<div class="kpi-card danger"><div class="kpi-label">Churn Rate</div><div class="kpi-value">{churn_rate}%</div><div class="kpi-sub">{churned:,} of {total:,} customers churned</div><span class="kpi-badge r">High Risk</span></div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""<div class="kpi-card warning"><div class="kpi-label">Revenue at Risk</div><div class="kpi-value">${rev_risk:,.0f}</div><div class="kpi-sub">Monthly revenue from churned customers</div><span class="kpi-badge a">Per Month</span></div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""<div class="kpi-card neutral"><div class="kpi-label">Avg Charge — Churned</div><div class="kpi-value">${avg_ch}</div><div class="kpi-sub">vs ${avg_re} for retained customers</div><span class="kpi-badge b">+${round(avg_ch-avg_re,2)} higher</span></div>""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""<div class="kpi-card primary"><div class="kpi-label">Retained Customers</div><div class="kpi-value">{retained:,}</div><div class="kpi-sub">{ret_rate}% retention rate</div><span class="kpi-badge g">Stable</span></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Churn by Customer Segment</div>', unsafe_allow_html=True)
    r1c1, r1c2 = st.columns(2)
    with r1c1:
        g = df.groupby("Contract")["Churn"].agg(Churned="sum", Total="count").reset_index()
        g["Rate"] = (g["Churned"]/g["Total"]*100).round(1)
        g = g.sort_values("Rate", ascending=False)
        fig = go.Figure(go.Bar(x=g["Contract"], y=g["Rate"], marker_color=bar_colors(g["Rate"].tolist()),
            marker_line_color="white", marker_line_width=1.5,
            text=[f"{v}%" for v in g["Rate"]], textposition="outside", textfont=dict(size=12, color=BRAND["text"])))
        fig.update_layout(title="Churn Rate by Contract Type", **CHART)
        fig.update_yaxes(title="Churn Rate (%)", range=[0, 55])
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="insight-banner">Month-to-month customers churn at 3x the rate of annual plan customers. Incentivising annual upgrades is the highest-impact retention lever.</div>', unsafe_allow_html=True)

    with r1c2:
        if "tenure_group" in df.columns and df["tenure_group"].notna().any():
            g2 = df.groupby("tenure_group")["Churn"].agg(Churned="sum", Total="count").reset_index()
            g2.columns = ["Tenure Group","Churned","Total"]
            g2["Rate"] = (g2["Churned"]/g2["Total"]*100).round(1)
            fig2 = go.Figure(go.Bar(x=g2["Tenure Group"], y=g2["Rate"], marker_color=bar_colors(g2["Rate"].tolist()),
                marker_line_color="white", marker_line_width=1.5,
                text=[f"{v}%" for v in g2["Rate"]], textposition="outside", textfont=dict(size=12, color=BRAND["text"])))
            fig2.update_layout(title="Churn Rate by Tenure Group", **CHART)
            fig2.update_yaxes(title="Churn Rate (%)", range=[0, 62])
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown('<div class="insight-banner">Nearly 1 in 2 customers leaves within the first 12 months. A structured onboarding programme is the most critical intervention point.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Churn by Service and Payment</div>', unsafe_allow_html=True)
    r2c1, r2c2 = st.columns(2)
    with r2c1:
        g3 = df.groupby("PaymentMethod")["Churn"].agg(Churned="sum", Total="count").reset_index()
        g3.columns = ["Payment Method","Churned","Total"]
        g3["Rate"] = (g3["Churned"]/g3["Total"]*100).round(1)
        g3 = g3.sort_values("Rate", ascending=True)
        fig3 = go.Figure(go.Bar(x=g3["Rate"], y=g3["Payment Method"], orientation="h",
            marker_color=bar_colors(g3["Rate"].tolist()), marker_line_color="white", marker_line_width=1.5,
            text=[f"{v}%" for v in g3["Rate"]], textposition="outside", textfont=dict(size=12, color=BRAND["text"])))
        fig3.update_layout(title="Churn Rate by Payment Method", **CHART)
        fig3.update_xaxes(title="Churn Rate (%)", range=[0, 58])
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('<div class="insight-banner">Electronic check users churn at nearly 3x the rate of auto-pay customers. A small discount to switch could significantly cut churn.</div>', unsafe_allow_html=True)

    with r2c2:
        g4 = df.groupby(["InternetService","TechSupport"])["Churn"].agg(Churned="sum", Total="count").reset_index()
        g4.columns = ["Internet Service","Tech Support","Churned","Total"]
        g4["Rate"] = (g4["Churned"]/g4["Total"]*100).round(1)
        fig4 = px.bar(g4, x="Internet Service", y="Rate", color="Tech Support", barmode="group",
            color_discrete_map={"Yes": BRAND["primary"], "No": BRAND["danger"]},
            text="Rate", labels={"Rate": "Churn Rate (%)"})
        fig4.update_traces(texttemplate="%{text}%", textposition="outside",
            textfont=dict(size=11), marker_line_color="white", marker_line_width=1.5)
        fig4.update_layout(title="Churn Rate: Internet Service + Tech Support", **CHART)
        fig4.update_yaxes(range=[0, 58], title="Churn Rate (%)")
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown('<div class="insight-banner">Tech Support reduces churn for Fiber Optic customers by more than half. Proactive upsell is a high-ROI retention action.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Revenue Analysis</div>', unsafe_allow_html=True)
    r3c1, r3c2 = st.columns(2)
    with r3c1:
        fig5 = go.Figure(go.Pie(labels=["Revenue Retained","Revenue at Risk"], values=[rev_safe, rev_risk], hole=0.62,
            marker=dict(colors=[BRAND["primary"], BRAND["danger"]], line=dict(color="white", width=3)),
            textinfo="percent+label", textfont=dict(size=12), pull=[0, 0.04]))
        fig5.update_layout(title="Monthly Revenue Split",
            annotations=[dict(text=f"<b>${(rev_safe+rev_risk):,.0f}</b><br>Total/mo", x=0.5, y=0.5, showarrow=False, font=dict(size=14, color=BRAND["text"]))],
            **CHART_NO_AX)
        st.plotly_chart(fig5, use_container_width=True)
    with r3c2:
        fig6 = go.Figure()
        fig6.add_trace(go.Histogram(x=df[df["Churn"]==0]["MonthlyCharges"], name="Retained", marker_color=BRAND["primary"], opacity=0.75, nbinsx=35))
        fig6.add_trace(go.Histogram(x=df[df["Churn"]==1]["MonthlyCharges"], name="Churned",  marker_color=BRAND["danger"],  opacity=0.75, nbinsx=35))
        fig6.update_layout(barmode="overlay", title="Monthly Charges Distribution — Churned vs Retained", **CHART)
        fig6.update_xaxes(title="Monthly Charges ($)")
        fig6.update_yaxes(title="Customer Count")
        st.plotly_chart(fig6, use_container_width=True)

    st.markdown('<div class="section-title">High-Risk Segment Analysis</div>', unsafe_allow_html=True)
    r4c1, r4c2 = st.columns(2)
    with r4c1:
        if "num_services" in df.columns:
            g5 = df.groupby("num_services")["Churn"].agg(mean="mean", count="count").reset_index()
            g5.columns = ["Num Services","Churn Rate","Customers"]
            g5["Rate"] = (g5["Churn Rate"]*100).round(1)
            fig7 = go.Figure()
            fig7.add_trace(go.Bar(x=g5["Num Services"], y=g5["Rate"], marker_color=BRAND["warning"],
                marker_line_color="white", marker_line_width=1.5, name="Churn Rate (%)",
                text=[f"{v}%" for v in g5["Rate"]], textposition="outside", textfont=dict(size=11, color=BRAND["text"])))
            fig7.add_trace(go.Scatter(x=g5["Num Services"], y=g5["Customers"], mode="lines+markers",
                name="Total Customers", yaxis="y2", line=dict(color=BRAND["dark"], width=2), marker=dict(size=6)))
            fig7.update_layout(title="Churn Rate by Number of Services",
                yaxis=dict(title="Churn Rate (%)", gridcolor="#eef2f0"),
                yaxis2=dict(title="Customers", overlaying="y", side="right"),
                xaxis=dict(title="Number of Services", dtick=1, gridcolor="#eef2f0"), **CHART_NO_AX)
            st.plotly_chart(fig7, use_container_width=True)
            st.markdown('<div class="insight-banner">Customers with more services churn significantly less. Cross-selling during onboarding boosts long-term retention.</div>', unsafe_allow_html=True)

    with r4c2:
        st.markdown("**Retention Priority List**")
        st.caption("Highest-risk segments ranked by churn rate")
        rdf = df.groupby(["Contract","PaymentMethod"]).agg(Customers=("Churn","count"), Churned=("Churn","sum")).reset_index()
        rdf["Churn Rate (%)"] = (rdf["Churned"]/rdf["Customers"]*100).round(1)
        rev_map = df[df["Churn"]==1].groupby(["Contract","PaymentMethod"])["MonthlyCharges"].sum().reset_index()
        rev_map.columns = ["Contract","PaymentMethod","Revenue at Risk ($)"]
        rdf = rdf.merge(rev_map, on=["Contract","PaymentMethod"], how="left").fillna(0)
        rdf["Revenue at Risk ($)"] = rdf["Revenue at Risk ($)"].round(0).astype(int)
        rdf = rdf[rdf["Customers"]>5].sort_values("Churn Rate (%)", ascending=False).head(10).reset_index(drop=True)
        st.dataframe(rdf[["Contract","PaymentMethod","Customers","Churn Rate (%)","Revenue at Risk ($)"]],
            use_container_width=True, hide_index=True,
            column_config={
                "Churn Rate (%)": st.column_config.ProgressColumn("Churn Rate (%)", min_value=0, max_value=100, format="%.1f%%"),
                "Revenue at Risk ($)": st.column_config.NumberColumn("Revenue at Risk ($)", format="$%d")
            })

    st.divider()
    fc1, fc2, fc3 = st.columns(3)
    with fc1: st.caption("Dataset: Telco Customer Churn — Kaggle (7,043 records)")
    with fc2: st.caption("Stack: Python · Streamlit · Plotly · SQLite · FastAPI · XGBoost")
    with fc3: st.caption("Author: Tharun Kumar Srinivasan — github.com/Tharun-Design")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — CHURN PREDICTOR
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Churn Predictor":
    st.markdown(f"""
    <div class="page-header">
        <div class="page-header-title">Customer Churn Predictor</div>
        <div class="page-header-sub">Enter customer details to get a real-time churn probability from the XGBoost model</div>
        <div class="page-header-meta">Powered by FastAPI &nbsp;|&nbsp; Model: XGBoost (Tuned) &nbsp;|&nbsp; ROC-AUC: 84.47%</div>
    </div>""", unsafe_allow_html=True)

    api_online = False
    try:
        r = requests.get(f"{API_URL}/", timeout=3)
        api_online = r.status_code == 200
    except Exception:
        api_online = False

    if not api_online:
        st.error("FastAPI is not running. Open a new terminal and run:")
        st.code("python -m uvicorn api.main:app --reload --port 8000")
        st.info("Keep that terminal running, then come back here and the predictor will work.")
        st.stop()
    else:
        st.success("API is online — XGBoost model ready for predictions")

    st.markdown('<div class="section-title">Customer Details</div>', unsafe_allow_html=True)

    with st.form("predict_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**Personal Info**")
            gender        = st.selectbox("Gender",          ["Male", "Female"])
            senior        = st.selectbox("Senior Citizen",  ["No", "Yes"])
            partner       = st.selectbox("Partner",         ["Yes", "No"])
            dependents    = st.selectbox("Dependents",      ["No", "Yes"])
            tenure        = st.slider("Tenure (months)", 0, 72, 12)
        with c2:
            st.markdown("**Services**")
            phone         = st.selectbox("Phone Service",      ["Yes", "No"])
            multi_lines   = st.selectbox("Multiple Lines",     ["No", "Yes"])
            internet      = st.selectbox("Internet Service",   ["Fiber optic", "DSL", "No"])
            online_sec    = st.selectbox("Online Security",    ["No", "Yes"])
            online_bkp    = st.selectbox("Online Backup",      ["No", "Yes"])
            device_prot   = st.selectbox("Device Protection",  ["No", "Yes"])
            tech_support  = st.selectbox("Tech Support",       ["No", "Yes"])
            streaming_tv  = st.selectbox("Streaming TV",       ["No", "Yes"])
            streaming_mov = st.selectbox("Streaming Movies",   ["No", "Yes"])
        with c3:
            st.markdown("**Account Info**")
            contract      = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
            paperless     = st.selectbox("Paperless Billing", ["Yes", "No"])
            payment       = st.selectbox("Payment Method", [
                "Electronic check", "Mailed check",
                "Bank transfer (automatic)", "Credit card (automatic)"])
            monthly_charges = st.number_input("Monthly Charges ($)", 0.0, 200.0, 70.0, step=0.5)
            total_charges   = st.number_input("Total Charges ($)", 0.0, 10000.0,
                float(monthly_charges * tenure) if tenure > 0 else 70.0, step=1.0)

        submitted = st.form_submit_button("Predict Churn Probability", use_container_width=True)

    if submitted:
        payload = {
            "gender": gender, "SeniorCitizen": 1 if senior == "Yes" else 0,
            "Partner": partner, "Dependents": dependents, "tenure": tenure,
            "PhoneService": phone, "MultipleLines": multi_lines,
            "InternetService": internet, "OnlineSecurity": online_sec,
            "OnlineBackup": online_bkp, "DeviceProtection": device_prot,
            "TechSupport": tech_support, "StreamingTV": streaming_tv,
            "StreamingMovies": streaming_mov, "Contract": contract,
            "PaperlessBilling": paperless, "PaymentMethod": payment,
            "MonthlyCharges": monthly_charges, "TotalCharges": total_charges
        }

        with st.spinner("Running prediction..."):
            try:
                response = requests.post(f"{API_URL}/predict", json=payload, timeout=10)
                result   = response.json()

                prob     = result["churn_probability"]
                prob_pct = result["churn_probability_pct"]
                risk     = result["risk_level"]
                rec      = result["recommendation"]

                st.markdown('<div class="section-title">Prediction Result</div>', unsafe_allow_html=True)
                res_col, gauge_col = st.columns([1, 1])

                with res_col:
                    risk_class = {"High":"risk-high","Medium":"risk-medium","Low":"risk-low"}[risk]
                    risk_color = {"High":BRAND["danger"],"Medium":BRAND["warning"],"Low":BRAND["primary"]}[risk]
                    st.markdown(f"""
                    <div class="{risk_class}">
                        <div class="risk-title" style="color:{risk_color}">{risk} Risk</div>
                        <div class="risk-prob"  style="color:{risk_color}">{prob_pct}</div>
                        <div style="font-size:14px;color:#555;">Churn Probability</div>
                        <div class="risk-rec">{rec}</div>
                    </div>""", unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("**Input Summary**")
                    summary = pd.DataFrame({
                        "Field": ["Contract","Tenure","Internet","Tech Support","Payment","Monthly Charge"],
                        "Value": [contract, f"{tenure} months", internet, tech_support, payment, f"${monthly_charges}"]
                    })
                    st.dataframe(summary, use_container_width=True, hide_index=True)

                with gauge_col:
                    fig_gauge = go.Figure(go.Indicator(
                        mode="gauge+number+delta",
                        value=round(prob * 100, 1),
                        number={"suffix": "%", "font": {"size": 36, "color": BRAND["text"]}},
                        delta={"reference": 26.5, "increasing": {"color": BRAND["danger"]}, "decreasing": {"color": BRAND["primary"]}},
                        gauge={
                            "axis": {"range": [0, 100], "tickwidth": 1},
                            "bar": {"color": risk_color, "thickness": 0.3},
                            "bgcolor": "white",
                            "steps": [
                                {"range": [0,  40], "color": "#e8f5ee"},
                                {"range": [40, 70], "color": "#fef9e7"},
                                {"range": [70,100], "color": "#fdecea"},
                            ],
                            "threshold": {"line": {"color": BRAND["dark"], "width": 3}, "thickness": 0.75, "value": 26.5}
                        }
                    ))
                    fig_gauge.update_layout(height=320, paper_bgcolor="white",
                        font=dict(family="Inter", color=BRAND["text"]),
                        margin=dict(t=30, b=10, l=20, r=20),
                        annotations=[dict(text="Avg churn: 26.5%", x=0.5, y=0.15,
                            showarrow=False, font=dict(size=11, color=BRAND["muted"]))])
                    st.plotly_chart(fig_gauge, use_container_width=True)

            except Exception as e:
                st.error(f"Prediction failed: {e}")