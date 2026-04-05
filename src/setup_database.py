"""
setup_database.py
=================
Loads the cleaned Telco Churn CSV into a local SQLite database.
Run this ONCE before running any SQL queries:

    python src/setup_database.py

This creates:  data/churn.db  (SQLite database file)
Table name:    customers
"""

import sqlite3
import pandas as pd
import os

DB_PATH  = "data/churn.db"
CSV_PATH = "data/cleaned/telco_churn_cleaned.csv"

def setup_database():
    # ── Load cleaned CSV ───────────────────────────────────────────────────
    if not os.path.exists(CSV_PATH):
        print(f"❌ Cleaned CSV not found at: {CSV_PATH}")
        print("   Run: python src/data_cleaning.py  first!")
        return

    df = pd.read_csv(CSV_PATH)
    print(f"✅ Loaded cleaned data: {df.shape[0]:,} rows × {df.shape[1]} columns")

    # ── Write to SQLite ────────────────────────────────────────────────────
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("customers", conn, if_exists="replace", index=False)
    conn.close()

    print(f"✅ Database created: {DB_PATH}")
    print(f"   Table: customers ({df.shape[0]:,} rows)")
    print("\n── Columns available ──────────────────────")
    for col in df.columns:
        print(f"   • {col}")

    print("\n🎯 Ready! Now open: notebooks/02_SQL_Analysis.ipynb")

if __name__ == "__main__":
    setup_database()
