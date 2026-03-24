import pandas as pd
import os

def process_finance_data():
    os.makedirs('data/processed', exist_ok=True)
    try:
        ops = pd.read_csv('data/raw/raw_ops_data.csv')
        # Create the specific column app.py is looking for
        ops['CM2_Net_Cash'] = ops['Revenue'] - ops['COGS'] - ops['Logistics_Cost'] - ops['Waste_Loss']
        ops.to_csv('data/processed/daily_cash_forecast.csv', index=False)
        
        ap = pd.read_csv('data/raw/raw_ap_data.csv')
        ap.to_csv('data/processed/cleaned_ap.csv', index=False)
        print("✅ Success: daily_cash_forecast.csv now contains 'CM2_Net_Cash'.")
    except Exception as e:
        print(f"❌ Processing Error: {e}")

if __name__ == "__main__":
    process_finance_data()