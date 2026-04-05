"""
streamlit_app.py
================
Customer Churn Analysis — Interactive Dashboard
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

# ── Brand colours (extracted from logo) ──────────────────────────────────────
# Logo: dark forest green (#0d3b2e) + bright lime green (#5cdb5c)
# Professional Data Analyst palette built around these anchors

BRAND = {
    "dark":       "#0d3b2e",   # logo dark green — sidebar, header
    "primary":    "#1a7f5a",   # mid green — primary accents
    "accent":     "#4eca7f",   # bright green — highlights, KPI borders
    "danger":     "#c0392b",   # professional red — high churn
    "warning":    "#d68910",   # amber — medium risk
    "neutral":    "#2e86ab",   # slate blue — neutral metrics
    "bg":         "#f4f6f4",   # very light green-tinted white — main bg
    "surface":    "#ffffff",   # pure white — cards
    "border":     "#dde8e4",   # light green-grey — borders
    "text":       "#0d1f1a",   # near black — headings
    "text_light": "#5a7168",   # muted — captions
}

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Customer Churn Analytics | Tharun Kumar",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Force sidebar always open ─────────────────────────────────────────────────
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

# ── Full CSS ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif !important;
    background-color: {BRAND['bg']} !important;
}}

.block-container {{
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
}}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {{
    background-color: {BRAND['dark']} !important;
}}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown span,
section[data-testid="stSidebar"] caption,
section[data-testid="stSidebar"] small {{
    color: #a8c4b8 !important;
}}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {{
    color: #ffffff !important;
}}
section[data-testid="stSidebar"] label {{
    color: #a8c4b8 !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}}
section[data-testid="stSidebar"] hr {{
    border-color: #1f5c45 !important;
}}

/* ── Page header ── */
.page-header {{
    background: linear-gradient(135deg, {BRAND['dark']} 0%, #1a5c42 100%);
    border-radius: 12px;
    padding: 24px 30px;
    margin-bottom: 22px;
    border-left: 5px solid {BRAND['accent']};
}}
.page-header-title {{
    font-size: 22px; font-weight: 700;
    color: #ffffff; letter-spacing: -0.02em; margin: 0;
}}
.page-header-sub {{
    font-size: 13px; color: #a8c4b8; margin-top: 4px;
}}
.page-header-meta {{
    font-size: 12px; color: {BRAND['accent']}; margin-top: 8px; font-weight: 500;
}}

/* ── KPI Cards ── */
.kpi-card {{
    background: {BRAND['surface']};
    border-radius: 10px;
    padding: 18px 20px;
    border: 1px solid {BRAND['border']};
    border-top: 3px solid {BRAND['border']};
    box-shadow: 0 1px 4px rgba(13,59,46,0.07);
}}
.kpi-card.danger  {{ border-top-color: {BRAND['danger']}; }}
.kpi-card.warning {{ border-top-color: {BRAND['warning']}; }}
.kpi-card.neutral {{ border-top-color: {BRAND['neutral']}; }}
.kpi-card.primary {{ border-top-color: {BRAND['primary']}; }}

.kpi-label {{
    font-size: 10px; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase;
    color: {BRAND['text_light']}; margin-bottom: 8px;
}}
.kpi-value {{
    font-size: 28px; font-weight: 700;
    color: {BRAND['text']}; line-height: 1; letter-spacing: -0.02em;
}}
.kpi-sub {{ font-size: 12px; color: {BRAND['text_light']}; margin-top: 5px; }}
.kpi-badge {{
    display: inline-block; padding: 2px 8px; border-radius: 4px;
    font-size: 11px; font-weight: 600; margin-top: 8px;
}}
.kpi-badge.r {{ background: #fdecea; color: {BRAND['danger']}; }}
.kpi-badge.a {{ background: #fef9e7; color: {BRAND['warning']}; }}
.kpi-badge.b {{ background: #e8f4fd; color: {BRAND['neutral']}; }}
.kpi-badge.g {{ background: #e8f5ee; color: {BRAND['primary']}; }}

/* ── Section title ── */
.section-title {{
    font-size: 15px; font-weight: 700; color: {BRAND['text']};
    margin: 26px 0 12px 0;
    padding-bottom: 8px;
    border-bottom: 2px solid {BRAND['border']};
    letter-spacing: -0.01em;
}}

/* ── Insight banner ── */
.insight-banner {{
    background: #f0f7f4;
    border: 1px solid {BRAND['border']};
    border-left: 3px solid {BRAND['primary']};
    border-radius: 0 6px 6px 0;
    padding: 8px 14px;
    font-size: 12px; color: {BRAND['text']};
    margin: 4px 0 12px 0; line-height: 1.5;
}}

/* ── Sidebar logo area ── */
.sidebar-logo-area {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 4px 0 8px 0;
}}
.sidebar-title {{
    font-size: 15px;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.2;
}}
.sidebar-sub {{
    font-size: 11px;
    color: #a8c4b8;
    margin-top: 2px;
}}

#MainMenu, footer, header {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)


# ── Load data ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    for p in ["data/churn.db", "../data/churn.db"]:
        if os.path.exists(p):
            conn = sqlite3.connect(p)
            df = pd.read_sql("SELECT * FROM customers", conn)
            conn.close()
            return df
    for p in ["data/cleaned/telco_churn_cleaned.csv",
              "../data/cleaned/telco_churn_cleaned.csv"]:
        if os.path.exists(p):
            return pd.read_csv(p)
    st.error("Data not found. Run: python src/setup_database.py")
    st.stop()

df_raw = load_data()
df_raw["Churn"] = pd.to_numeric(df_raw["Churn"], errors="coerce").fillna(0).astype(int)

# ── Plotly chart theme ───────────────────────────────────────────────────────
CHART = dict(
    plot_bgcolor=BRAND["surface"],
    paper_bgcolor=BRAND["surface"],
    font=dict(family="Inter", color=BRAND["text"], size=11),
    title_font=dict(family="Inter", size=13, color=BRAND["text"]),
    margin=dict(t=42, b=24, l=10, r=10),
    xaxis=dict(gridcolor="#eef2f0", linecolor=BRAND["border"], tickfont=dict(size=11)),
    yaxis=dict(gridcolor="#eef2f0", linecolor=BRAND["border"], tickfont=dict(size=11)),
    legend=dict(bgcolor=BRAND["surface"], bordercolor=BRAND["border"], borderwidth=1),
    hoverlabel=dict(bgcolor="white", bordercolor=BRAND["border"],
                    font=dict(family="Inter", size=12))
)
CHART_NO_AX = {k: v for k, v in CHART.items() if k not in ("xaxis", "yaxis")}

def risk_color(value, max_val):
    pct = value / max_val if max_val else 0
    if pct >= 0.70: return BRAND["danger"]
    if pct >= 0.40: return BRAND["warning"]
    return BRAND["primary"]

def bar_colors(values):
    mx = max(values) if values else 1
    return [risk_color(v, mx) for v in values]


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:

    # Logo + title
    logo_paths = ["app/logo.png", "logo.png", "../app/logo.png"]
    logo_found = next((p for p in logo_paths if os.path.exists(p)), None)

    col_logo, col_title = st.columns([1, 2.5])
    with col_logo:
        if logo_found:
            st.image(logo_found, width=56)
        else:
            st.markdown("**[Logo]**")
    with col_title:
        st.markdown("""
        <div class="sidebar-title">Churn Analytics</div>
        <div class="sidebar-sub">Tharun Kumar Srinivasan</div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("**FILTERS**")

    # ── Contract Type ──
    contract_options = sorted(df_raw["Contract"].dropna().unique().tolist())
    sel_contract = st.multiselect(
        "Contract Type",
        options=contract_options,
        default=contract_options,
        placeholder="Select contract types..."
    )
    if not sel_contract:
        sel_contract = contract_options

    # ── Internet Service ──
    internet_options = sorted(df_raw["InternetService"].dropna().unique().tolist())
    sel_internet = st.multiselect(
        "Internet Service",
        options=internet_options,
        default=internet_options,
        placeholder="Select internet service..."
    )
    if not sel_internet:
        sel_internet = internet_options

    # ── Payment Method ──
    payment_options = sorted(df_raw["PaymentMethod"].dropna().unique().tolist())
    sel_payment = st.multiselect(
        "Payment Method",
        options=payment_options,
        default=payment_options,
        placeholder="Select payment methods..."
    )
    if not sel_payment:
        sel_payment = payment_options

    # ── Tenure slider ──
    t_min = int(df_raw["tenure"].min())
    t_max = int(df_raw["tenure"].max())
    sel_tenure = st.slider("Tenure Range (months)", t_min, t_max, (t_min, t_max))

    # ── Customer type ──
    sel_senior = st.selectbox("Customer Type", ["All", "Senior Citizen", "Non-Senior"])

    # ── Churn status ──
    sel_churn = st.selectbox("Churn Status", ["All", "Churned", "Retained"])

    st.divider()
    st.caption("Dataset: Telco Customer Churn")
    st.caption(f"Total records: {len(df_raw):,}")
    st.caption("github.com/Tharun-Design")


# ── Apply filters ─────────────────────────────────────────────────────────────
df = df_raw.copy()
df = df[df["Contract"].isin(sel_contract)]
df = df[df["InternetService"].isin(sel_internet)]
df = df[df["PaymentMethod"].isin(sel_payment)]
df = df[df["tenure"].between(sel_tenure[0], sel_tenure[1])]
if sel_senior == "Senior Citizen":  df = df[df["SeniorCitizen"] == 1]
elif sel_senior == "Non-Senior":    df = df[df["SeniorCitizen"] == 0]
if sel_churn == "Churned":   df = df[df["Churn"] == 1]
elif sel_churn == "Retained": df = df[df["Churn"] == 0]

if len(df) == 0:
    st.warning("No data matches the current filters. Please adjust your selection.")
    st.stop()

# ── KPIs ───────────────────────────────────────────────────────────────────────
total       = len(df)
churned     = int(df["Churn"].sum())
retained    = total - churned
churn_rate  = round(churned / total * 100, 1) if total > 0 else 0
ret_rate    = round(retained / total * 100, 1) if total > 0 else 0
rev_risk    = round(df[df["Churn"] == 1]["MonthlyCharges"].sum(), 0)
rev_safe    = round(df[df["Churn"] == 0]["MonthlyCharges"].sum(), 0)
avg_ch      = round(df[df["Churn"] == 1]["MonthlyCharges"].mean(), 2) if churned > 0 else 0
avg_re      = round(df[df["Churn"] == 0]["MonthlyCharges"].mean(), 2) if retained > 0 else 0
charge_diff = round(avg_ch - avg_re, 2)

# Is it default (no filters applied)?
is_default = (
    set(sel_contract) == set(contract_options) and
    set(sel_internet) == set(internet_options) and
    set(sel_payment)  == set(payment_options)  and
    sel_tenure == (t_min, t_max) and
    sel_senior == "All" and sel_churn == "All"
)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="page-header">
    <div class="page-header-title">Customer Churn Analytics Dashboard</div>
    <div class="page-header-sub">
        Telco Customer Retention Intelligence &nbsp;—&nbsp; Tharun Kumar Srinivasan
    </div>
    <div class="page-header-meta">
        {"Showing all 7,043 customers" if is_default else f"Showing {total:,} of {len(df_raw):,} customers (filters active)"}
        &nbsp;|&nbsp; Dataset: Telco Customer Churn (Kaggle)
    </div>
</div>
""", unsafe_allow_html=True)

if not is_default:
    st.info(f"Filters active — {total:,} of {len(df_raw):,} customers in view")


# ══════════════════════════════════════════════════════════════════════════════
# KPI CARDS
# ══════════════════════════════════════════════════════════════════════════════
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"""<div class="kpi-card danger">
        <div class="kpi-label">Churn Rate</div>
        <div class="kpi-value">{churn_rate}%</div>
        <div class="kpi-sub">{churned:,} of {total:,} customers churned</div>
        <span class="kpi-badge r">High Risk</span>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class="kpi-card warning">
        <div class="kpi-label">Revenue at Risk</div>
        <div class="kpi-value">${rev_risk:,.0f}</div>
        <div class="kpi-sub">Monthly revenue from churned customers</div>
        <span class="kpi-badge a">Per Month</span>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class="kpi-card neutral">
        <div class="kpi-label">Avg Charge — Churned</div>
        <div class="kpi-value">${avg_ch}</div>
        <div class="kpi-sub">vs ${avg_re} for retained customers</div>
        <span class="kpi-badge b">+${charge_diff} higher</span>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""<div class="kpi-card primary">
        <div class="kpi-label">Retained Customers</div>
        <div class="kpi-value">{retained:,}</div>
        <div class="kpi-sub">{ret_rate}% retention rate</div>
        <span class="kpi-badge g">Stable</span>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ROW 1 — Contract + Tenure
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">Churn by Customer Segment</div>', unsafe_allow_html=True)
r1c1, r1c2 = st.columns(2)

with r1c1:
    g = df.groupby("Contract")["Churn"].agg(Churned="sum", Total="count").reset_index()
    g["Churn Rate (%)"] = (g["Churned"] / g["Total"] * 100).round(1)
    g = g.sort_values("Churn Rate (%)", ascending=False)
    fig = go.Figure(go.Bar(
        x=g["Contract"], y=g["Churn Rate (%)"],
        marker_color=bar_colors(g["Churn Rate (%)"].tolist()),
        marker_line_color="white", marker_line_width=1.5,
        text=[f"{v}%" for v in g["Churn Rate (%)"]],
        textposition="outside", textfont=dict(size=12, color=BRAND["text"]),
        hovertemplate="<b>%{x}</b><br>Churn Rate: %{y}%<extra></extra>"
    ))
    fig.update_layout(title="Churn Rate by Contract Type", **CHART)
    fig.update_yaxes(title="Churn Rate (%)", range=[0, 55])
    fig.update_xaxes(title="Contract Type")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="insight-banner">Month-to-month customers churn at 3x the rate of annual plan customers. Incentivising annual contract upgrades is the highest-impact retention lever available.</div>', unsafe_allow_html=True)

with r1c2:
    if "tenure_group" in df.columns and df["tenure_group"].notna().any():
        g2 = df.groupby("tenure_group")["Churn"].agg(Churned="sum", Total="count").reset_index()
        g2.columns = ["Tenure Group", "Churned", "Total"]
        g2["Churn Rate (%)"] = (g2["Churned"] / g2["Total"] * 100).round(1)
        fig2 = go.Figure(go.Bar(
            x=g2["Tenure Group"], y=g2["Churn Rate (%)"],
            marker_color=bar_colors(g2["Churn Rate (%)"].tolist()),
            marker_line_color="white", marker_line_width=1.5,
            text=[f"{v}%" for v in g2["Churn Rate (%)"]],
            textposition="outside", textfont=dict(size=12, color=BRAND["text"]),
            hovertemplate="<b>%{x}</b><br>Churn Rate: %{y}%<extra></extra>"
        ))
        fig2.update_layout(title="Churn Rate by Tenure Group", **CHART)
        fig2.update_yaxes(title="Churn Rate (%)", range=[0, 62])
        fig2.update_xaxes(title="Tenure Group")
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('<div class="insight-banner">Nearly 1 in 2 customers leaves within the first 12 months. A structured onboarding programme targeting this window is the most critical intervention point.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ROW 2 — Payment + Internet + Tech Support
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">Churn by Service and Payment</div>', unsafe_allow_html=True)
r2c1, r2c2 = st.columns(2)

with r2c1:
    g3 = df.groupby("PaymentMethod")["Churn"].agg(Churned="sum", Total="count").reset_index()
    g3.columns = ["Payment Method", "Churned", "Total"]
    g3["Churn Rate (%)"] = (g3["Churned"] / g3["Total"] * 100).round(1)
    g3 = g3.sort_values("Churn Rate (%)", ascending=True)
    fig3 = go.Figure(go.Bar(
        x=g3["Churn Rate (%)"], y=g3["Payment Method"], orientation="h",
        marker_color=bar_colors(g3["Churn Rate (%)"].tolist()),
        marker_line_color="white", marker_line_width=1.5,
        text=[f"{v}%" for v in g3["Churn Rate (%)"]],
        textposition="outside", textfont=dict(size=12, color=BRAND["text"]),
        hovertemplate="<b>%{y}</b><br>Churn Rate: %{x}%<extra></extra>"
    ))
    fig3.update_layout(title="Churn Rate by Payment Method", **CHART)
    fig3.update_xaxes(title="Churn Rate (%)", range=[0, 58])
    fig3.update_yaxes(title="")
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('<div class="insight-banner">Electronic check users churn at nearly 3x the rate of auto-pay customers. A modest incentive to switch to automatic payment could produce a significant reduction in churn.</div>', unsafe_allow_html=True)

with r2c2:
    g4 = df.groupby(["InternetService", "TechSupport"])["Churn"].agg(Churned="sum", Total="count").reset_index()
    g4.columns = ["Internet Service", "Tech Support", "Churned", "Total"]
    g4["Churn Rate (%)"] = (g4["Churned"] / g4["Total"] * 100).round(1)
    fig4 = px.bar(g4, x="Internet Service", y="Churn Rate (%)",
                  color="Tech Support", barmode="group",
                  color_discrete_map={"Yes": BRAND["primary"], "No": BRAND["danger"]},
                  text="Churn Rate (%)")
    fig4.update_traces(texttemplate="%{text}%", textposition="outside",
                       textfont=dict(size=11),
                       marker_line_color="white", marker_line_width=1.5)
    fig4.update_layout(title="Churn Rate: Internet Service + Tech Support", **CHART)
    fig4.update_yaxes(range=[0, 58], title="Churn Rate (%)")
    fig4.update_xaxes(title="Internet Service")
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('<div class="insight-banner">Tech Support reduces churn for Fiber Optic customers by more than half. Proactive upsell of Tech Support to fiber customers is a high-ROI retention action.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ROW 3 — Revenue
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">Revenue Analysis</div>', unsafe_allow_html=True)
r3c1, r3c2 = st.columns(2)

with r3c1:
    total_rev = rev_safe + rev_risk
    fig5 = go.Figure(go.Pie(
        labels=["Revenue Retained", "Revenue at Risk"],
        values=[rev_safe, rev_risk], hole=0.62,
        marker=dict(colors=[BRAND["primary"], BRAND["danger"]],
                    line=dict(color="white", width=3)),
        textinfo="percent+label", textfont=dict(size=12),
        pull=[0, 0.04],
        hovertemplate="<b>%{label}</b><br>$%{value:,.0f}/mo (%{percent})<extra></extra>"
    ))
    fig5.update_layout(
        title="Monthly Revenue Split",
        annotations=[dict(
            text=f"<b>${total_rev:,.0f}</b><br>Total/mo",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color=BRAND["text"])
        )],
        **CHART_NO_AX
    )
    st.plotly_chart(fig5, use_container_width=True)

with r3c2:
    fig6 = go.Figure()
    fig6.add_trace(go.Histogram(
        x=df[df["Churn"] == 0]["MonthlyCharges"],
        name="Retained", marker_color=BRAND["primary"], opacity=0.75, nbinsx=35,
        hovertemplate="Charge: $%{x:.0f}<br>Count: %{y}<extra>Retained</extra>"
    ))
    fig6.add_trace(go.Histogram(
        x=df[df["Churn"] == 1]["MonthlyCharges"],
        name="Churned", marker_color=BRAND["danger"], opacity=0.75, nbinsx=35,
        hovertemplate="Charge: $%{x:.0f}<br>Count: %{y}<extra>Churned</extra>"
    ))
    fig6.update_layout(barmode="overlay",
                       title="Monthly Charges Distribution — Churned vs Retained", **CHART)
    fig6.update_xaxes(title="Monthly Charges ($)")
    fig6.update_yaxes(title="Customer Count")
    st.plotly_chart(fig6, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# ROW 4 — Services + Retention Hit List
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">High-Risk Segment Analysis</div>', unsafe_allow_html=True)
r4c1, r4c2 = st.columns(2)

with r4c1:
    if "num_services" in df.columns:
        g5 = df.groupby("num_services")["Churn"].agg(mean="mean", count="count").reset_index()
        g5.columns = ["Num Services", "Churn Rate", "Customers"]
        g5["Churn Rate (%)"] = (g5["Churn Rate"] * 100).round(1)
        fig7 = go.Figure()
        fig7.add_trace(go.Bar(
            x=g5["Num Services"], y=g5["Churn Rate (%)"],
            marker_color=BRAND["warning"],
            marker_line_color="white", marker_line_width=1.5,
            name="Churn Rate (%)",
            text=[f"{v}%" for v in g5["Churn Rate (%)"]],
            textposition="outside", textfont=dict(size=11, color=BRAND["text"]),
            hovertemplate="Services: %{x}<br>Churn Rate: %{y}%<extra></extra>"
        ))
        fig7.add_trace(go.Scatter(
            x=g5["Num Services"], y=g5["Customers"],
            mode="lines+markers", name="Total Customers", yaxis="y2",
            line=dict(color=BRAND["dark"], width=2),
            marker=dict(size=6, color=BRAND["dark"]),
            hovertemplate="Services: %{x}<br>Customers: %{y:,}<extra></extra>"
        ))
        fig7.update_layout(
            title="Churn Rate by Number of Services",
            yaxis=dict(title="Churn Rate (%)", gridcolor="#eef2f0", linecolor=BRAND["border"]),
            yaxis2=dict(title="Total Customers", overlaying="y", side="right",
                        gridcolor="#eef2f0"),
            xaxis=dict(title="Number of Services", dtick=1, gridcolor="#eef2f0"),
            **CHART_NO_AX
        )
        st.plotly_chart(fig7, use_container_width=True)
        st.markdown('<div class="insight-banner">Customers subscribed to more services churn significantly less. Cross-selling additional services during onboarding increases stickiness and lifetime value.</div>', unsafe_allow_html=True)

with r4c2:
    st.markdown("**Retention Priority List**")
    st.caption("Highest-risk customer segments ranked by churn rate")
    rdf = df.groupby(["Contract", "PaymentMethod"]).agg(
        Customers=("Churn", "count"), Churned=("Churn", "sum")).reset_index()
    rdf["Churn Rate (%)"] = (rdf["Churned"] / rdf["Customers"] * 100).round(1)
    rev_map = (df[df["Churn"] == 1]
               .groupby(["Contract", "PaymentMethod"])["MonthlyCharges"]
               .sum().reset_index())
    rev_map.columns = ["Contract", "PaymentMethod", "Revenue at Risk ($)"]
    rdf = rdf.merge(rev_map, on=["Contract", "PaymentMethod"], how="left").fillna(0)
    rdf["Revenue at Risk ($)"] = rdf["Revenue at Risk ($)"].round(0).astype(int)
    rdf = (rdf[rdf["Customers"] > 5]
           .sort_values("Churn Rate (%)", ascending=False)
           .head(10).reset_index(drop=True))
    st.dataframe(
        rdf[["Contract", "PaymentMethod", "Customers", "Churn Rate (%)", "Revenue at Risk ($)"]],
        use_container_width=True, hide_index=True,
        column_config={
            "Churn Rate (%)": st.column_config.ProgressColumn(
                "Churn Rate (%)", min_value=0, max_value=100, format="%.1f%%"),
            "Revenue at Risk ($)": st.column_config.NumberColumn(
                "Revenue at Risk ($)", format="$%d"),
            "Customers": st.column_config.NumberColumn("Customers", format="%d")
        }
    )
    st.caption("These segments should be prioritised in retention campaigns.")


# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
fc1, fc2, fc3 = st.columns(3)
with fc1: st.caption("Dataset: Telco Customer Churn — Kaggle (7,043 records)")
with fc2: st.caption("Stack: Python · Streamlit · Plotly · SQLite · Pandas")
with fc3: st.caption("Author: Tharun Kumar Srinivasan — github.com/Tharun-Design")