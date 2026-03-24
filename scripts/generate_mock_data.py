import pandas as pd
import numpy as np
from datetime import timedelta
from pathlib import Path

def generate_data():
    raw_path = Path(__file__).parent.parent / "data" / "raw"
    raw_path.mkdir(parents=True, exist_ok=True)

    # 1. Accounts Payable
    vendors = ['REWE Group', 'Vattenfall', 'Coca-Cola Europacific', 'Tier Mobility', 'Meta Ads']
    ap_data = {
        'Vendor': [np.random.choice(vendors) for _ in range(150)],
        'Amount_EUR': [np.random.randint(500, 25000) for _ in range(150)],
        'Invoice_Date': [pd.Timestamp.now().normalize() - timedelta(days=np.random.randint(0, 30)) for _ in range(150)],
        'Category': ['Inventory', 'Utilities', 'Inventory', 'Logistics', 'Marketing'] * 30
    }
    df_ap = pd.DataFrame(ap_data)
    df_ap['Due_Date'] = df_ap['Invoice_Date'] + timedelta(days=14)
    df_ap.to_csv(raw_path / "raw_ap_data.csv", index=False)

    # 2. Daily Ops - Using pd.Timestamp for consistency with app.py
    today = pd.Timestamp.now().normalize()
    dates = [today + timedelta(days=i) for i in range(91)]
    ops_data = {
        'Date': dates,
        'Revenue': [np.random.randint(90000, 150000) for _ in range(91)],
        'COGS': [np.random.randint(50000, 70000) for _ in range(91)],
        'Logistics_Cost': [np.random.randint(20000, 30000) for _ in range(91)],
        'Waste_Loss': [np.random.randint(2000, 5000) for _ in range(91)]
    }
    pd.DataFrame(ops_data).to_csv(raw_path / "raw_ops_data.csv", index=False)
    print("✅ Mock data generated successfully.")

if __name__ == "__main__":
    generate_data()