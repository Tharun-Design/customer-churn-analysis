"""
data_cleaning.py
================
Reusable data cleaning functions for the Telco Customer Churn dataset.
Run this script directly to generate the cleaned dataset:
    python src/data_cleaning.py
"""

import pandas as pd
import numpy as np
import os

# ── Paths ──────────────────────────────────────────────────────────────────
RAW_PATH     = "data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv"
CLEANED_PATH = "data/cleaned/telco_churn_cleaned.csv"


# ── Step 1: Load ───────────────────────────────────────────────────────────
def load_data(path: str = RAW_PATH) -> pd.DataFrame:
    """Load the raw CSV and do a quick sanity check."""
    df = pd.read_csv(path)
    print(f"✅ Loaded dataset: {df.shape[0]:,} rows × {df.shape[1]} columns")
    return df


# ── Step 2: Inspect ────────────────────────────────────────────────────────
def inspect_data(df: pd.DataFrame) -> None:
    """Print a structured summary — useful to keep as a reference."""
    print("\n── Column dtypes ──────────────────────────")
    print(df.dtypes)

    print("\n── Missing values ─────────────────────────")
    missing = df.isnull().sum()
    print(missing[missing > 0] if missing.sum() > 0 else "No missing values found ✅")

    print("\n── Duplicates ─────────────────────────────")
    print(f"Duplicate rows: {df.duplicated().sum()}")

    print("\n── Target distribution ────────────────────")
    print(df["Churn"].value_counts(normalize=True).mul(100).round(2).astype(str) + " %")


# ── Step 3: Fix TotalCharges ───────────────────────────────────────────────
def fix_total_charges(df: pd.DataFrame) -> pd.DataFrame:
    """
    TotalCharges is loaded as object due to whitespace entries.
    Convert to float; rows with whitespace → NaN → fill with 0
    (new customers with 0 tenure have no charges yet).
    """
    df = df.copy()
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    n_nulls = df["TotalCharges"].isnull().sum()
    if n_nulls > 0:
        print(f"  ⚠️  {n_nulls} TotalCharges nulls filled with 0 (new customers)")
        df["TotalCharges"] = df["TotalCharges"].fillna(0)

    return df


# ── Step 4: Encode target ──────────────────────────────────────────────────
def encode_target(df: pd.DataFrame) -> pd.DataFrame:
    """Convert Churn Yes/No → 1/0 for easy analysis."""
    df = df.copy()
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})
    print("  ✅ Churn encoded: Yes → 1, No → 0")
    return df


# ── Step 5: Clean binary Yes/No columns ───────────────────────────────────
def clean_binary_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Several service columns use 'No internet service' or 'No phone service'
    which are effectively 'No'. Standardise them to 'No'.
    """
    df = df.copy()
    cols_to_fix = [
        "OnlineSecurity", "OnlineBackup", "DeviceProtection",
        "TechSupport", "StreamingTV", "StreamingMovies", "MultipleLines"
    ]
    for col in cols_to_fix:
        if col in df.columns:
            df[col] = df[col].replace(
                {"No internet service": "No", "No phone service": "No"}
            )
    print(f"  ✅ Standardised {len(cols_to_fix)} binary service columns")
    return df


# ── Step 6: Drop unused columns ───────────────────────────────────────────
def drop_unused(df: pd.DataFrame) -> pd.DataFrame:
    """Drop customerID — it's an identifier, not a feature."""
    df = df.copy()
    df.drop(columns=["customerID"], inplace=True, errors="ignore")
    print("  ✅ Dropped customerID column")
    return df


# ── Step 7: Feature engineering ───────────────────────────────────────────
def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add derived features that improve business analysis:
    - tenure_group: bucket tenure into readable segments
    - avg_monthly_spend: TotalCharges / tenure (spend rate)
    - num_services: how many add-on services the customer uses
    """
    df = df.copy()

    # Tenure buckets
    bins   = [0, 12, 24, 48, 72]
    labels = ["0-12 months", "12-24 months", "24-48 months", "48-72 months"]
    df["tenure_group"] = pd.cut(df["tenure"], bins=bins, labels=labels, include_lowest=True)

    # Average monthly spend rate
    df["avg_monthly_spend"] = df.apply(
        lambda r: round(r["TotalCharges"] / r["tenure"], 2) if r["tenure"] > 0 else r["MonthlyCharges"],
        axis=1
    )

    # Count of add-on services
    service_cols = [
        "PhoneService", "MultipleLines", "InternetService",
        "OnlineSecurity", "OnlineBackup", "DeviceProtection",
        "TechSupport", "StreamingTV", "StreamingMovies"
    ]
    df["num_services"] = df[service_cols].apply(
        lambda row: sum(1 for v in row if v not in ["No", "No internet service", "No phone service"]),
        axis=1
    )

    print("  ✅ Added: tenure_group, avg_monthly_spend, num_services")
    return df


# ── Step 8: Save ───────────────────────────────────────────────────────────
def save_cleaned(df: pd.DataFrame, path: str = CLEANED_PATH) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"\n💾 Cleaned dataset saved → {path}")
    print(f"   Final shape: {df.shape[0]:,} rows × {df.shape[1]} columns")


# ── Main pipeline ──────────────────────────────────────────────────────────
def clean_pipeline(raw_path: str = RAW_PATH, save_path: str = CLEANED_PATH) -> pd.DataFrame:
    """Run the full cleaning pipeline end-to-end."""
    print("=" * 50)
    print("  TELCO CHURN — DATA CLEANING PIPELINE")
    print("=" * 50)

    df = load_data(raw_path)
    inspect_data(df)

    print("\n── Cleaning steps ─────────────────────────")
    df = fix_total_charges(df)
    df = encode_target(df)
    df = clean_binary_columns(df)
    df = drop_unused(df)
    df = feature_engineering(df)

    save_cleaned(df, save_path)
    return df


# ── Entry point ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    clean_pipeline()
