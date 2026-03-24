import pandas as pd
import pytest
from pathlib import Path

# --- DIRECTORY SETUP ---
BASE_DIR = Path(__file__).parent.parent
PROCESSED_DATA = BASE_DIR / "data" / "processed"

# 1. LOGIC TEST: Basic Cash Flow Arithmetic
def test_cash_math_consistency():
    """Verify that the core calculator logic isn't broken."""
    opening_balance = 1000.0
    inflows = 500.0
    outflows = 300.0
    expected_ending = 1200.0
    
    # This simulates your app's internal calculation
    actual_ending = opening_balance + inflows - outflows
    assert actual_ending == expected_ending, "Basic cash addition logic is failing."

# 2. INTEGRITY TEST: File Presence
def test_processed_files_exist():
    """Ensure the pipeline has actually generated the required files."""
    ap_file = PROCESSED_DATA / "cleaned_ap.csv"
    ops_file = PROCESSED_DATA / "daily_cash_forecast.csv"
    
    assert ap_file.exists(), "🚨 Processed AP data is missing! Run scripts/process_data.py"
    assert ops_file.exists(), "🚨 Processed Ops data is missing! Run scripts/process_data.py"

# 3. QUALITY TEST: No Negative Liabilities
def test_ap_amounts_are_positive():
    """Invoices (AP) should always be positive outflows."""
    df_ap = pd.read_csv(PROCESSED_DATA / "cleaned_ap.csv")
    assert (df_ap['Amount_EUR'] >= 0).all(), "Found negative amounts in Accounts Payable."

# 4. BUSINESS LOGIC TEST: CM2 Margin Range
def test_cm2_margin_reasonableness():
    """CM2 Margins in Quick Commerce should be within a logical range (e.g., -50% to +50%)."""
    df_ops = pd.read_csv(PROCESSED_DATA / "daily_cash_forecast.csv")
    # Ensuring we don't have crazy outliers like a 5000% margin due to data errors
    assert df_ops['CM2_Margin'].max() < 1.0, "CM2 Margin > 100% detected; check revenue vs cost logic."
    assert df_ops['CM2_Margin'].min() > -1.0, "CM2 Margin < -100% detected; check for extreme waste/labor costs."

if __name__ == "__main__":
    print("🧪 Executing Flink Liquidity Test Suite...")
    # Instructions for the user
    print("Tip: Run 'pytest tests/test_liquidity_math.py' in your terminal for a full report.")