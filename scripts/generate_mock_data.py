import pandas as pd
import numpy as np
from datetime import timedelta
from pathlib import Path

def generate_data():
    raw_path = Path(__file__).parent.parent / "data" / "raw"
    raw_path.mkdir(parents=True, exist_ok=True)

    # 1. Define Hubs for Berlin
    hubs = ['Mitte', 'Prenzlauer Berg', 'Neukölln', 'Kreuzberg']

    # 2. Accounts Payable: Increased range to populate the full 13-week forecast
    vendors = ['REWE Group', 'Vattenfall', 'Coca-Cola Europacific', 'Tier Mobility', 'Meta Ads', 'Cloudflare', 'Personio']
    
    # Generate 300 invoices spread across the past and future
    ap_data = {
        'Vendor': [np.random.choice(vendors) for _ in range(300)],
        'Amount_EUR': [np.random.randint(1000, 45000) for _ in range(300)],
        # Invoices dated from 45 days ago to 45 days in the future
        'Invoice_Date': [pd.Timestamp.now().normalize() + timedelta(days=np.random.randint(-45, 45)) for _ in range(300)],
        'Hub_Location': [np.random.choice(hubs) for _ in range(300)],
        'Category': ['Inventory', 'Utilities', 'Inventory', 'Logistics', 'Marketing', 'SaaS', 'HR'] * 42 + ['HR'] * 6
    }
    
    df_ap = pd.DataFrame(ap_data)
    # Varying payment terms (14 to 60 days) ensures outflows across the 13-week window
    terms = [14, 30, 45, 60]
    df_ap['Due_Date'] = df_ap['Invoice_Date'] + pd.to_timedelta(np.random.choice(terms, 300), unit='d')
    df_ap.to_csv(raw_path / "raw_ap_data.csv", index=False)

    # 3. Daily Ops: Hub-specific revenue and costs
    today = pd.Timestamp.now().normalize()
    dates = [today + timedelta(days=i) for i in range(91)]
    
    ops_list = []
    for hub in hubs:
        hub_data = {
            'Date': dates,
            'Hub_Location': hub,
            'Revenue': [np.random.randint(30000, 50000) for _ in range(91)],
            'COGS': [np.random.randint(15000, 20000) for _ in range(91)],
            'Logistics_Cost': [np.random.randint(6000, 10000) for _ in range(91)],
            'Waste_Loss': [np.random.randint(800, 2000) for _ in range(91)]
        }
        ops_list.append(pd.DataFrame(hub_data))
    
    pd.concat(ops_list).to_csv(raw_path / "raw_ops_data.csv", index=False)
    print("✅ Success: Enhanced Mock Data generated with full 13-week AP coverage.")

if __name__ == "__main__":
    generate_data()