import pandas as pd
import os

def process_finance_data():
    os.makedirs('data/processed', exist_ok=True)
    
    # Process Ops Data
    try:
        ops = pd.read_csv('data/raw/raw_ops_data.csv')
        # Crucial: Create the CM2 column the app expects
        ops['CM2_Net_Cash'] = ops['Revenue'] - ops['COGS'] - ops['Logistics_Cost'] - ops['Waste_Loss']
        ops.to_csv('data/processed/daily_cash_forecast.csv', index=False)
        
        # Process AP Data
        ap = pd.read_csv('data/raw/raw_ap_data.csv')
        ap.to_csv('data/processed/cleaned_ap.csv', index=False)
        
        print("✅ Pipeline Success: daily_cash_forecast.csv and cleaned_ap.csv created.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    process_finance_data()