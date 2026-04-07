# 📉 Customer Churn Analysis & Business Dashboard

> **Identifying high-risk customers and actionable retention strategies using data analysis and machine learning**

[![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live%20Demo-red?logo=streamlit)](https://your-streamlit-link-here)


---

## Problem Statement

A telecom company is losing ~26% of its customers every quarter. The business needs to understand **who is churning, why they're churning, and what can be done to retain them** — before losing more revenue.

This project answers three core business questions:
1. Which customer segments have the highest churn rate?
2. What are the strongest drivers of churn?
3. How can the business prioritize retention efforts?

---

## Dataset

| Property | Details |
|---|---|
| Source | [Kaggle – Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) |
| Records | 7,043 customers |
| Features | 21 (demographics, account info, services) |
| Target | `Churn` (Yes/No) |

---

## Tools & Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.13 |
| Data Wrangling | Pandas, NumPy |
| SQL Layer | SQLite, SQLAlchemy |
| Visualization | Matplotlib, Seaborn, Plotly |
| Dashboard | Streamlit |
| ML (Phase 2) | Scikit-learn, XGBoost |

---

## Key Findings

> *(To be updated as analysis progresses)*

- 📌 **Finding 1:** Month-to-month contract customers churn at **3x the rate** of annual plan customers
- 📌 **Finding 2:** Customers in their **first 12 months** are highest risk — 50%+ churn rate
- 📌 **Finding 3:** Fiber optic users without tech support churn at **41%** vs 15% with support
- 📌 **Finding 4:** Electronic check payers churn **2x more** than credit card users

---

## Live Demo

**[View the Dashboard](https://your-streamlit-link-here)**  
*(Deployed on Streamlit Cloud — no setup required)*

---

## Project Architecture

```
customer-churn-analysis/
│
├── data/
│   ├── raw/                  # Original Kaggle dataset (not pushed to GitHub)
│   └── cleaned/              # Processed, analysis-ready data
│
├── notebooks/
│   └── 01_EDA.ipynb          # Full exploratory data analysis
│
├── queries/
│   ├── 01_churn_by_contract.sql
│   ├── 02_churn_by_tenure.sql
│   ├── 03_revenue_at_risk.sql
│   └── ...                   # 8–10 business SQL queries
│
├── src/
│   └── data_cleaning.py      # Reusable cleaning functions
│
├── app/
│   └── streamlit_app.py      # Interactive dashboard
│
├── docs/
│   └── architecture.png      # Architecture diagram
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/your-username/customer-churn-analysis.git
cd customer-churn-analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add the dataset
# Download from Kaggle and place in: data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv

# 4. Run the notebook
jupyter notebook notebooks/01_EDA.ipynb

# 5. Launch the dashboard
streamlit run app/streamlit_app.py
```

---

## Business Impact

This analysis enables the retention team to:
- **Target** the top 20% highest-risk customers with personalized offers
- **Reduce churn** by focusing on the first 12-month customer lifecycle
- **Prioritize** fiber optic customers for tech support upsells

---

## Next Steps (Phase 2 — ML Model)

- [ ] Build a churn prediction model (XGBoost)
- [ ] Add SHAP explainability to identify per-customer risk factors
- [ ] Deploy prediction API with FastAPI

---

## Author

**Tharun Kumar Srinivasan**  
[LinkedIn](https://www.linkedin.com/in/tharunkumarsrini/) · [GitHub](https://github.com/Tharun-Design) ·
