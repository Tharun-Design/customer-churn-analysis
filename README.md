# Customer Churn Analysis & Prediction

**Author:** Tharun Kumar Srinivasan  
**GitHub:** [github.com/Tharun-Design](https://github.com/Tharun-Design)  
**Live Demo:** [View Dashboard](https://your-streamlit-app.streamlit.app)  
**API Docs:** [View Swagger UI](http://localhost:8000/docs)

---

## Overview

An end-to-end data science project that analyses customer churn for a telecom company, builds a machine learning prediction model, and serves predictions through a REST API integrated into an interactive dashboard.

The project covers the complete data science workflow — from raw data exploration to a deployed, production-ready prediction system.

**Business Problem:** A telecom company loses ~26.5% of customers every quarter, representing $139,131 in monthly revenue at risk. This project identifies the drivers of churn, predicts which customers are likely to leave, and provides actionable retention recommendations.

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
|-- app/
|   |-- streamlit_app.py               Interactive dashboard + ML predictor UI
|   |-- logo.png                       Brand logo
|
|-- api/
|   |-- main.py                        FastAPI REST API
|   |-- test_api.py                    API test script
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
|-- docs/
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
|   |-- cleaned/                       Processed dataset (not tracked)
|
|-- .streamlit/
|   |-- config.toml                    Streamlit theme configuration
|
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
| Dashboard | Streamlit |
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

## Running the Project

### Option A — Dashboard only

```bash
python -m streamlit run app/streamlit_app.py
```

Open your browser at `http://localhost:8501`

### Option B — Dashboard with live ML Predictor

The Churn Predictor tab requires the FastAPI server to be running.
Open two terminals in the project root:

**Terminal 1 — Start the API:**
```bash
python -m uvicorn api.main:app --reload --port 8000
```

**Terminal 2 — Start the Dashboard:**
```bash
python -m streamlit run app/streamlit_app.py
```

Open `http://localhost:8501` and navigate to the Churn Predictor tab in the sidebar.

### Option C — API only

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

### Sample Request — Single Prediction

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

The retention team contacts a fixed number of customers per month. ROC-AUC measures how accurately the model ranks customers by churn risk, which directly determines campaign ROI. A model with high recall but poor ranking is less useful for targeted campaigns than one with a high AUC.

**Winner: XGBoost (Tuned)**
- Highest ROC-AUC after hyperparameter tuning: 84.47%
- Recall of 84.76% — the model catches 85 out of every 100 churners before they leave
- Tuning method: RandomizedSearchCV, 30 iterations, 5-fold StratifiedKFold
- Cross-validation stability: 84.76% +/- 1.21% across folds

### Top Churn Drivers (SHAP)

1. Tenure — shorter tenure correlates strongly with higher churn risk
2. Contract type — month-to-month customers are at the highest risk
3. Monthly charges — higher charges increase churn likelihood
4. Internet service type — Fiber optic without Tech Support is the highest-risk combination
5. Payment method — electronic check users churn at nearly 3x the rate of auto-pay customers

---

## Key Business Findings

| Segment | Churn Rate | Priority Recommendation |
|---------|------------|------------------------|
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

This runs 5 automated tests: health check, model info endpoint, high-risk customer prediction, low-risk customer prediction, and batch prediction with a 2-customer payload.

---


## Contact

**Tharun Kumar Srinivasan**  
[LinkedIn](https://linkedin.com/in/tharun-kumar-srinivasan) &nbsp;|&nbsp; [GitHub](https://github.com/Tharun-Design)
