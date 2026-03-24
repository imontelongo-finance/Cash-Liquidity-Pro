import pandas as pd
import os

def process_finance_data():
    os.makedirs('data/processed', exist_ok=True)
    
    try:
        # Load raw data
        ops = pd.read_csv('data/raw/raw_ops_data.csv')
        
        # KEY FIX: Explicitly create the column app.py is looking for
        # CM2 = Revenue - COGS - Logistics - Waste
        ops['CM2_Net_Cash'] = ops['Revenue'] - ops['COGS'] - ops['Logistics_Cost'] - ops['Waste_Loss']
        
        # Save to the path used by app.py
        ops.to_csv('data/processed/daily_cash_forecast.csv', index=False)
        
        # Also ensure AP data is processed/moved
        ap = pd.read_csv('data/raw/raw_ap_data.csv')
        ap.to_csv('data/processed/cleaned_ap.csv', index=False)
        
        print("✅ Success: Columns 'CM2_Net_Cash' and 'Waste_Loss' are now in daily_cash_forecast.csv")
    except Exception as e:
        print(f"❌ Processing Error: {e}")

if __name__ == "__main__":
    process_finance_data()