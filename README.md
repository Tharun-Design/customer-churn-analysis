# Customer Churn Analysis & Prediction

**Author:** Tharun Kumar Srinivasan  
**GitHub:** [github.com/Tharun-Design](https://github.com/Tharun-Design)  
**Live Dashboard:** [tharun-design.github.io/customer-churn-analysis/dashboard.html](https://tharun-design.github.io/customer-churn-analysis/dashboard.html)  
**Project Page:** [tharun-design.github.io/customer-churn-analysis](https://tharun-design.github.io/customer-churn-analysis/)  
**LinkedIn:** [linkedin.com/in/tharun-kumar-srinivasan](https://linkedin.com/in/tharun-kumar-srinivasan)

---

## Overview

An end-to-end data science project that analyses customer churn for a telecom company, builds a machine learning prediction model, and serves predictions through a REST API integrated into an interactive web dashboard.

The project covers the complete data science workflow — from raw data exploration and SQL business queries to a tuned XGBoost model deployed via FastAPI, with a fully interactive dashboard built in HTML, CSS, and JavaScript hosted on GitHub Pages.

**Business Problem:** A telecom company loses approximately 26.5% of customers every quarter, representing $139,131 in monthly revenue at risk. This project identifies the drivers of churn, predicts which customers are likely to leave, and provides actionable retention recommendations.

---

## Live Links

| Resource | URL |
|----------|-----|
| Interactive Dashboard | [View Dashboard](https://tharun-design.github.io/customer-churn-analysis/dashboard.html) |
| Project Showcase Page | [View Project Page](https://tharun-design.github.io/customer-churn-analysis/) |
| GitHub Repository | [View Repository](https://github.com/Tharun-Design/customer-churn-analysis) |
| API (local) | `http://localhost:8000/docs` |

---

## Key Results

| Metric | Value |
|--------|-------|
| Overall Churn Rate | 26.5% |
| Monthly Revenue at Risk | $139,131 |
| Best Model | XGBoost (Tuned) |
| Model ROC-AUC | 84.47% |
| Model Recall | 84.76% |
| Models Compared | 5 |
| SQL Business Queries | 10 |

---

## Project Structure

```
customer-churn-analysis/
|
|-- api/
|   |-- main.py                        FastAPI REST API
|   |-- test_api.py                    API test script
|   |-- requirements.txt               API-specific dependencies
|   |-- __init__.py
|
|-- notebooks/
|   |-- 01_EDA.ipynb                   Exploratory data analysis
|   |-- 02_SQL_Analysis.ipynb          SQL business queries
|   |-- 03_ML_Model_Comparison.ipynb   5-model comparison + SHAP
|   |-- 04_Hyperparameter_Tuning.ipynb Tuning + cross validation
|
|-- src/
|   |-- data_cleaning.py               Data cleaning pipeline
|   |-- setup_database.py              Load CSV into SQLite
|
|-- queries/
|   |-- 01_overall_churn_rate.sql
|   |-- 02_churn_by_contract.sql
|   |-- 03_churn_by_tenure.sql
|   |-- 04_revenue_at_risk.sql
|   |-- 05_churn_by_payment.sql
|   |-- 06_churn_by_internet_techsupport.sql
|   |-- 07_high_risk_segments.sql
|   |-- 08_churn_by_num_services.sql
|   |-- 09_churn_by_demographics.sql
|   |-- 10_executive_summary.sql
|
|-- models/
|   |-- final_xgboost_tuned.pkl        Production model
|   |-- imputer.pkl                    Fitted imputer
|   |-- scaler.pkl                     Fitted scaler
|   |-- label_encoders.pkl             Fitted encoders
|   |-- feature_names.pkl              Feature list
|
|-- reports/
|   |-- model_comparison_results.csv
|   |-- tuned_model_results.csv
|   |-- shap_feature_importance.csv
|   |-- best_hyperparameters.csv
|
|-- docs/                              GitHub Pages — live dashboard and project page
|   |-- index.html                     Project showcase page
|   |-- dashboard.html                 Interactive web dashboard (HTML/CSS/JS)
|   |-- model_comparison.png
|   |-- roc_curves.png
|   |-- confusion_matrix.png
|   |-- shap_importance.png
|   |-- shap_beeswarm.png
|   |-- shap_waterfall.png
|   |-- learning_curves.png
|   |-- cross_validation.png
|   |-- tuned_vs_baseline.png
|
|-- data/
|   |-- raw/                           Original dataset (not tracked)
|   |-- cleaned/                       Processed dataset
|
|-- render.yaml                        Render deployment config
|-- requirements.txt
|-- .gitignore
|-- README.md
```

---

## Tech Stack

| Category | Tools |
|----------|-------|
| Language | Python 3.11 |
| Data Wrangling | Pandas, NumPy |
| Database | SQLite, SQLAlchemy |
| Visualisation | Matplotlib, Seaborn, Plotly |
| Machine Learning | Scikit-learn, XGBoost, LightGBM |
| Explainability | SHAP |
| API | FastAPI, Uvicorn, Pydantic |
| Dashboard | HTML, CSS, JavaScript, Chart.js |
| Hosting | GitHub Pages |
| Version Control | Git, GitHub |

---

## Dataset

| Property | Details |
|----------|---------|
| Source | [Kaggle — Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) |
| Records | 7,043 customers |
| Features | 21 (demographics, account info, services) |
| Target | Churn (Yes / No) |

---

## Setup and Installation

### Prerequisites

- Python 3.9 or higher
- Git

### Step 1 — Clone the repository

```bash
git clone https://github.com/Tharun-Design/customer-churn-analysis.git
cd customer-churn-analysis
```

### Step 2 — Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Add the dataset

Download the dataset from [Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) and place it at:

```
data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv
```

### Step 5 — Run the data pipeline

```bash
# Clean the raw data
python src/data_cleaning.py

# Load into SQLite database
python src/setup_database.py
```

---

## Dashboard

The interactive dashboard is built in pure HTML, CSS, and JavaScript using Chart.js. It is hosted on GitHub Pages with no server required.

**Live URL:**
```
https://tharun-design.github.io/customer-churn-analysis/dashboard.html
```

**Features:**
- Sidebar with 5 real-time filters — Contract Type, Internet Service, Payment Method, Churn Status, Senior Citizen
- 4 KPI cards updating dynamically on filter change
- 7 interactive charts — Contract, Tenure, Payment, Internet + Tech Support, Revenue donut, Charges distribution, Services dual-axis
- Retention Priority List table with progress bars
- Business insight banners below each chart

To view locally, simply open `docs/dashboard.html` in any browser. No installation required.

---

## Running the API

```bash
python -m uvicorn api.main:app --reload --port 8000
```

Interactive API documentation is available at `http://localhost:8000/docs`

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check and model status |
| GET | `/model-info` | Model name, features, and performance metrics |
| POST | `/predict` | Single customer churn prediction |
| POST | `/predict-batch` | Batch prediction for up to 100 customers |

### Sample Request

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "gender": "Male",
    "SeniorCitizen": 0,
    "Partner": "No",
    "Dependents": "No",
    "tenure": 2,
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "Fiber optic",
    "OnlineSecurity": "No",
    "OnlineBackup": "No",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "No",
    "StreamingMovies": "No",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 79.85,
    "TotalCharges": 159.70
  }'
```

### Sample Response

```json
{
  "churn_prediction": true,
  "churn_probability": 0.8968,
  "churn_probability_pct": "89.7%",
  "risk_level": "High",
  "recommendation": "Immediate retention action required — high churn risk.",
  "model_used": "XGBoost (Tuned)"
}
```

---

## Notebooks

| Notebook | Description |
|----------|-------------|
| `01_EDA.ipynb` | Data quality checks, distributions, and 10-section exploratory analysis with business insights |
| `02_SQL_Analysis.ipynb` | 10 SQL queries answering business questions on churn by contract, tenure, payment, revenue, and demographics |
| `03_ML_Model_Comparison.ipynb` | Training and comparing Logistic Regression, Random Forest, XGBoost, LightGBM, and SVM — includes SHAP feature importance, beeswarm, and waterfall plots |
| `04_Hyperparameter_Tuning.ipynb` | RandomizedSearchCV tuning of top 3 models, learning curves, and 5-fold cross validation with boxplot stability analysis |

---

## Machine Learning

### Models Compared

| Model | Accuracy | F1 Score | ROC-AUC |
|-------|----------|----------|---------|
| XGBoost (Tuned) | 75.87% | 60.44% | **84.47%** |
| Random Forest (Tuned) | 77.00% | 61.70% | 84.12% |
| Logistic Regression | 73.81% | 61.76% | 83.99% |
| LightGBM (Tuned) | 75.94% | 61.78% | 83.54% |
| SVM | 74.24% | 61.09% | 81.66% |

### Model Selection Rationale

**Primary metric: ROC-AUC**

The retention team contacts a fixed number of customers per month. ROC-AUC measures how accurately the model ranks customers by churn risk, which directly determines campaign ROI.

**Winner: XGBoost (Tuned)**
- Highest ROC-AUC after hyperparameter tuning: 84.47%
- Recall of 84.76% — catches 85 out of every 100 churners before they leave
- Tuning method: RandomizedSearchCV, 30 iterations, 5-fold StratifiedKFold
- Cross-validation stability: 84.76% +/- 1.21% across folds

### Top Churn Drivers (SHAP)

1. Tenure — shorter tenure correlates strongly with higher churn risk
2. Contract type — month-to-month customers are at the highest risk
3. Monthly charges — higher charges increase churn likelihood
4. Internet service — Fiber optic without Tech Support is the highest-risk combination
5. Payment method — electronic check users churn at nearly 3x the rate of auto-pay customers

---

## Key Business Findings

| Segment | Churn Rate | Recommendation |
|---------|------------|----------------|
| Month-to-month contracts | 42.7% | Offer incentives to upgrade to annual plans |
| Customers in first 12 months | 47.4% | Implement structured onboarding programme |
| Fiber optic without Tech Support | 41.0% | Proactive Tech Support upsell campaign |
| Electronic check payment | 45.3% | Discount to switch to automatic payment |
| Customers with 1-2 services | 44.9% | Cross-sell additional services at onboarding |

---

## Running the Tests

Ensure the API is running first, then in a second terminal:

```bash
python api/test_api.py
```

This runs 5 automated tests: health check, model info endpoint, high-risk customer prediction, low-risk customer prediction, and batch prediction.

---

## Project Roadmap

- [x] Week 1 — Data cleaning and exploratory data analysis
- [x] Week 2 — SQL analysis (10 business queries)
- [x] Week 3 — Interactive web dashboard (HTML/CSS/Chart.js)
- [x] Week 4 — GitHub Pages deployment
- [x] Week 5 — ML model comparison (5 models + SHAP explainability)
- [x] Week 6 — Hyperparameter tuning and cross validation
- [x] Week 7 — FastAPI REST API with Swagger documentation
- [x] Week 8 — Complete project with live GitHub Pages dashboard


---

## License

This project is licensed under the MIT License.

---

## Contact

**Tharun Kumar Srinivasan**  
[LinkedIn](https://linkedin.com/in/tharun-kumar-srinivasan) &nbsp;|&nbsp; [GitHub](https://github.com/Tharun-Design)
