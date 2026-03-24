import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

def generate_data():
    raw_path = Path(__file__).parent.parent / "data" / "raw"
    raw_path.mkdir(parents=True, exist_ok=True)

    # 1. Accounts Payable (The Bills)
    vendors = ['REWE Group', 'Vattenfall', 'Coca-Cola Europacific', 'Tier Mobility', 'Meta Ads']
    hubs = ['BER_Mitte_01', 'BER_PBerg_02', 'BER_Neukoelln_03', 'HAM_Altona_01']
    
    ap_data = {
        'Vendor': [np.random.choice(vendors) for _ in range(150)],
        'Amount_EUR': [np.random.randint(500, 25000) for _ in range(150)],
        'Invoice_Date': [datetime.now() - timedelta(days=np.random.randint(0, 30)) for _ in range(150)],
        'Hub_ID': [np.random.choice(hubs) for _ in range(150)],
        'Category': ['Inventory', 'Utilities', 'Inventory', 'Logistics', 'Marketing'] * 30
    }
    df_ap = pd.DataFrame(ap_data)
    df_ap['Due_Date'] = df_ap['Invoice_Date'] + timedelta(days=14) # Default German terms
    df_ap.to_csv(raw_path / "erp_export_ap.csv", index=False)

    # 2. Daily Ops (Sales & Waste)
    dates = [datetime.now() + timedelta(days=i) for i in range(91)]
    ops_data = {
        'Date': dates,
        'Projected_Rev': [np.random.randint(90000, 150000) for _ in range(91)],
        'Variable_COGS': [np.random.randint(50000, 70000) for _ in range(91)],
        'Rider_Labor': [np.random.randint(20000, 30000) for _ in range(91)],
        'Waste_Loss': [np.random.randint(2000, 5000) for _ in range(91)]
    }
    pd.DataFrame(ops_data).to_csv(raw_path / "ops_projections.csv", index=False)
    print(f"✅ Mock data generated in {raw_path}")

if __name__ == "__main__":
    generate_data()