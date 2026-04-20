"""
main.py
=======
Customer Churn Prediction — FastAPI REST API
Author : Tharun Kumar Srinivasan
GitHub : https://github.com/Tharun-Design

Run locally:
    uvicorn api.main:app --reload --port 8000

Endpoints:
    GET  /              — Health check
    GET  /model-info    — Model metadata
    POST /predict       — Single customer prediction
    POST /predict-batch — Batch prediction
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import List, Optional
import pickle
import numpy as np
import pandas as pd
import os

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Customer Churn Prediction API",
    description="Predicts churn probability for telecom customers using XGBoost.",
    version="1.0.0",
    contact={
        "name": "Tharun Kumar Srinivasan",
        "url":  "https://github.com/Tharun-Design"
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ── Load artifacts ─────────────────────────────────────────────────────────────
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")

def load_artifact(filename):
    path = os.path.join(MODEL_DIR, filename)
    with open(path, "rb") as f:
        return pickle.load(f)

try:
    try:
        model      = load_artifact("final_xgboost_tuned.pkl")
        model_name = "XGBoost (Tuned)"
    except FileNotFoundError:
        files = [f for f in os.listdir(MODEL_DIR) if f.startswith("best_model")]
        model      = load_artifact(files[0])
        model_name = files[0].replace("best_model_", "").replace(".pkl", "")

    imputer       = load_artifact("imputer.pkl")
    feature_names = load_artifact("feature_names.pkl")
    LOADED = True
    print(f"Model loaded : {model_name}")
    print(f"Features     : {len(feature_names)}")

except Exception as e:
    print(f"WARNING: {e}")
    LOADED = False
    model_name    = "Not loaded"
    feature_names = []


# ── Input schema ───────────────────────────────────────────────────────────────
class CustomerInput(BaseModel):
    gender             : str   = Field(..., example="Male",              description="Male or Female")
    SeniorCitizen      : int   = Field(..., example=0,                   description="1 = Senior, 0 = Not")
    Partner            : str   = Field(..., example="Yes",               description="Yes or No")
    Dependents         : str   = Field(..., example="No",                description="Yes or No")
    tenure             : int   = Field(..., example=12,                  description="Months with company (0-72)")
    PhoneService       : str   = Field(..., example="Yes",               description="Yes or No")
    MultipleLines      : str   = Field(..., example="No",                description="Yes, No")
    InternetService    : str   = Field(..., example="Fiber optic",       description="DSL, Fiber optic, No")
    OnlineSecurity     : str   = Field(..., example="No",                description="Yes or No")
    OnlineBackup       : str   = Field(..., example="No",                description="Yes or No")
    DeviceProtection   : str   = Field(..., example="No",                description="Yes or No")
    TechSupport        : str   = Field(..., example="No",                description="Yes or No")
    StreamingTV        : str   = Field(..., example="Yes",               description="Yes or No")
    StreamingMovies    : str   = Field(..., example="Yes",               description="Yes or No")
    Contract           : str   = Field(..., example="Month-to-month",    description="Month-to-month, One year, Two year")
    PaperlessBilling   : str   = Field(..., example="Yes",               description="Yes or No")
    PaymentMethod      : str   = Field(..., example="Electronic check",  description="Payment type")
    MonthlyCharges     : float = Field(..., example=75.50,               description="Monthly bill ($)")
    TotalCharges       : float = Field(..., example=906.0,               description="Total billed ($)")

    @validator("Contract")
    def validate_contract(cls, v):
        valid = ["Month-to-month", "One year", "Two year"]
        if v not in valid:
            raise ValueError(f"Contract must be one of {valid}")
        return v

    @validator("InternetService")
    def validate_internet(cls, v):
        valid = ["DSL", "Fiber optic", "No"]
        if v not in valid:
            raise ValueError(f"InternetService must be one of {valid}")
        return v


# ── Feature engineering ────────────────────────────────────────────────────────
BINARY_MAP = {"Yes": 1, "No": 0, "Male": 1, "Female": 0}

INTERNET_MAP = {"DSL": 0, "Fiber optic": 1, "No": 2}

CONTRACT_MAP = {"Month-to-month": 0, "One year": 1, "Two year": 2}

PAYMENT_MAP = {
    "Bank transfer (automatic)": 0,
    "Credit card (automatic)"  : 1,
    "Electronic check"         : 2,
    "Mailed check"             : 3
}

def encode_customer(data: CustomerInput) -> pd.DataFrame:
    tenure = data.tenure

    service_cols = [
        data.PhoneService, data.MultipleLines, data.InternetService,
        data.OnlineSecurity, data.OnlineBackup, data.DeviceProtection,
        data.TechSupport, data.StreamingTV, data.StreamingMovies
    ]
    num_services = sum(1 for s in service_cols if s not in ["No", "No internet service", "No phone service"])

    avg_monthly = (
        round(data.TotalCharges / tenure, 2) if tenure > 0 else data.MonthlyCharges
    )

    row = {
        "gender"           : 1 if data.gender == "Male" else 0,
        "SeniorCitizen"    : data.SeniorCitizen,
        "Partner"          : BINARY_MAP.get(data.Partner, 0),
        "Dependents"       : BINARY_MAP.get(data.Dependents, 0),
        "tenure"           : tenure,
        "PhoneService"     : BINARY_MAP.get(data.PhoneService, 0),
        "MultipleLines"    : BINARY_MAP.get(data.MultipleLines, 0),
        "InternetService"  : INTERNET_MAP.get(data.InternetService, 0),
        "OnlineSecurity"   : BINARY_MAP.get(data.OnlineSecurity, 0),
        "OnlineBackup"     : BINARY_MAP.get(data.OnlineBackup, 0),
        "DeviceProtection" : BINARY_MAP.get(data.DeviceProtection, 0),
        "TechSupport"      : BINARY_MAP.get(data.TechSupport, 0),
        "StreamingTV"      : BINARY_MAP.get(data.StreamingTV, 0),
        "StreamingMovies"  : BINARY_MAP.get(data.StreamingMovies, 0),
        "Contract"         : CONTRACT_MAP.get(data.Contract, 0),
        "PaperlessBilling" : BINARY_MAP.get(data.PaperlessBilling, 0),
        "PaymentMethod"    : PAYMENT_MAP.get(data.PaymentMethod, 2),
        "MonthlyCharges"   : data.MonthlyCharges,
        "TotalCharges"     : data.TotalCharges,
        "avg_monthly_spend": avg_monthly,
        "num_services"     : num_services,
    }

    df = pd.DataFrame([row])

    # Align with training feature order
    if feature_names:
        for col in feature_names:
            if col not in df.columns:
                df[col] = 0
        df = df[feature_names]

    return df


def make_prediction(df: pd.DataFrame):
    X = imputer.transform(df)
    prob  = float(model.predict_proba(X)[0][1])
    label = int(model.predict(X)[0])

    if prob >= 0.70:
        risk = "High"
    elif prob >= 0.40:
        risk = "Medium"
    else:
        risk = "Low"

    return prob, label, risk


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def health_check():
    return {
        "status"     : "online",
        "api"        : "Customer Churn Prediction API",
        "version"    : "1.0.0",
        "model"      : model_name,
        "model_ready": LOADED,
        "author"     : "Tharun Kumar Srinivasan",
        "github"     : "https://github.com/Tharun-Design"
    }


@app.get("/model-info", tags=["Health"])
def model_info():
    if not LOADED:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {
        "model_name"   : model_name,
        "features"     : feature_names,
        "feature_count": len(feature_names),
        "model_type"   : "XGBoost Classifier",
        "tuning"       : "RandomizedSearchCV (30 iterations, 5-fold CV)",
        "metric"       : "ROC-AUC: 84.47%",
        "week"         : "Week 6 — Hyperparameter Tuning"
    }


@app.post("/predict", tags=["Prediction"])
def predict(customer: CustomerInput):
    if not LOADED:
        raise HTTPException(status_code=503, detail="Model not loaded. Check models/ folder.")

    try:
        df            = encode_customer(customer)
        prob, label, risk = make_prediction(df)

        return {
            "churn_prediction"   : bool(label),
            "churn_probability"  : round(prob, 4),
            "churn_probability_pct": f"{round(prob * 100, 1)}%",
            "risk_level"         : risk,
            "recommendation"     : (
                "Immediate retention action required — high churn risk."
                if risk == "High" else
                "Monitor closely and consider a proactive offer."
                if risk == "Medium" else
                "Customer is stable. No immediate action needed."
            ),
            "model_used"         : model_name
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/predict-batch", tags=["Prediction"])
def predict_batch(customers: List[CustomerInput]):
    if not LOADED:
        raise HTTPException(status_code=503, detail="Model not loaded.")
    if len(customers) > 100:
        raise HTTPException(status_code=400, detail="Max 100 customers per batch.")

    results = []
    for i, customer in enumerate(customers):
        try:
            df            = encode_customer(customer)
            prob, label, risk = make_prediction(df)
            results.append({
                "customer_index"     : i,
                "churn_prediction"   : bool(label),
                "churn_probability"  : round(prob, 4),
                "churn_probability_pct": f"{round(prob * 100, 1)}%",
                "risk_level"         : risk
            })
        except Exception as e:
            results.append({
                "customer_index": i,
                "error"         : str(e)
            })

    high_risk = sum(1 for r in results if r.get("risk_level") == "High")
    med_risk  = sum(1 for r in results if r.get("risk_level") == "Medium")

    return {
        "total_customers"    : len(customers),
        "high_risk_count"    : high_risk,
        "medium_risk_count"  : med_risk,
        "low_risk_count"     : len(customers) - high_risk - med_risk,
        "predictions"        : results
    }
