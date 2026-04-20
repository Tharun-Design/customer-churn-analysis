"""
test_api.py
===========
Test the Churn Prediction API
Run with API running: python api/test_api.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def print_result(title, response):
    print(f"\n{'='*55}")
    print(f"{title}")
    print('='*55)
    try:
        print(json.dumps(response.json(), indent=2))
    except Exception:
        print(response.text)

# Test 1: Health check
r = requests.get(f"{BASE_URL}/")
print_result("TEST 1 — Health Check", r)

# Test 2: Model info
r = requests.get(f"{BASE_URL}/model-info")
print_result("TEST 2 — Model Info", r)

# Test 3: High-risk customer
high_risk = {
    "gender": "Male", "SeniorCitizen": 0, "Partner": "No",
    "Dependents": "No", "tenure": 2, "PhoneService": "Yes",
    "MultipleLines": "No", "InternetService": "Fiber optic",
    "OnlineSecurity": "No", "OnlineBackup": "No",
    "DeviceProtection": "No", "TechSupport": "No",
    "StreamingTV": "No", "StreamingMovies": "No",
    "Contract": "Month-to-month", "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 79.85, "TotalCharges": 159.70
}
r = requests.post(f"{BASE_URL}/predict", json=high_risk)
print_result("TEST 3 — High Risk Customer (Month-to-month, Fiber, 2 months)", r)

# Test 4: Low-risk customer
low_risk = {
    "gender": "Female", "SeniorCitizen": 0, "Partner": "Yes",
    "Dependents": "Yes", "tenure": 60, "PhoneService": "Yes",
    "MultipleLines": "Yes", "InternetService": "DSL",
    "OnlineSecurity": "Yes", "OnlineBackup": "Yes",
    "DeviceProtection": "Yes", "TechSupport": "Yes",
    "StreamingTV": "Yes", "StreamingMovies": "Yes",
    "Contract": "Two year", "PaperlessBilling": "No",
    "PaymentMethod": "Credit card (automatic)",
    "MonthlyCharges": 65.40, "TotalCharges": 3924.0
}
r = requests.post(f"{BASE_URL}/predict", json=low_risk)
print_result("TEST 4 — Low Risk Customer (Two year, DSL, 60 months)", r)

# Test 5: Batch prediction
print_result("TEST 5 — Batch Prediction (2 customers)",
    requests.post(f"{BASE_URL}/predict-batch", json=[high_risk, low_risk]))
