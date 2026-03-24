import pandas as pd
import numpy as np
from datetime import timedelta
from pathlib import Path

def generate_data():
    raw_path = Path(__file__).parent.parent / "data" / "raw"
    raw_path.mkdir(parents=True, exist_ok=True)

    # Define Hubs once to ensure consistency across AP and Ops
    hubs = ['Mitte', 'Prenzlauer Berg', 'Neukölln', 'Kreuzberg']

    # 1. Accounts Payable with expanded vendors
    vendors = ['REWE Group', 'Vattenfall', 'Coca-Cola Europacific', 'Tier Mobility', 'Meta Ads', 'Cloudflare', 'Personio']
    ap_data = {
        'Vendor': [np.random.choice(vendors) for _ in range(200)],
        'Amount_EUR': [np.random.randint(500, 35000) for _ in range(200)],
        'Invoice_Date': [pd.Timestamp.now().normalize() - timedelta(days=np.random.randint(0, 45)) for _ in range(200)],
        'Hub_Location': [np.random.choice(hubs) for _ in range(200)], # ADDED: Links expenses to specific hubs
        'Category': ['Inventory', 'Utilities', 'Inventory', 'Logistics', 'Marketing', 'SaaS', 'HR'] * 28 + ['HR'] * 4
    }
    df_ap = pd.DataFrame(ap_data)
    df_ap['Due_Date'] = df_ap['Invoice_Date'] + timedelta(days=14)
    df_ap.to_csv(raw_path / "raw_ap_data.csv", index=False)

    # 2. Daily Ops with Hub Locations (Berlin Focus)
    today = pd.Timestamp.now().normalize()
    dates = [today + timedelta(days=i) for i in range(91)]
    
    ops_list = []
    for hub in hubs:
        hub_data = {
            'Date': dates,
            'Hub_Location': hub,
            'Revenue': [np.random.randint(25000, 45000) for _ in range(91)],
            'COGS': [np.random.randint(12000, 18000) for _ in range(91)],
            'Logistics_Cost': [np.random.randint(5000, 9000) for _ in range(91)],
            'Waste_Loss': [np.random.randint(500, 1500) for _ in range(91)]
        }
        ops_list.append(pd.DataFrame(hub_data))
    
    pd.concat(ops_list).to_csv(raw_path / "raw_ops_data.csv", index=False)
    print("✅ Enhanced Mock Data Generated.")

if __name__ == "__main__":
    generate_data()