import pandas as pd
from pathlib import Path
import logging

# Setup Paths & Logging
BASE_DIR = Path(__file__).parent.parent
logging.basicConfig(filename=BASE_DIR / "logs/pipeline.log", level=logging.INFO)

def process_all():
    logging.info("Starting Flink Data Pipeline...")
    
    # 1. Load Raw Data
    raw_ap = pd.read_csv(BASE_DIR / "data/raw/erp_export_ap.csv", parse_dates=['Due_Date'])
    raw_ops = pd.read_csv(BASE_DIR / "data/raw/ops_projections.csv", parse_dates=['Date'])
    
    # 2. Engineering Features (Unit Economics)
    # CM2 = Revenue - COGS - Labor - Waste
    raw_ops['CM2_Margin'] = (raw_ops['Projected_Rev'] - raw_ops['Variable_COGS'] - raw_ops['Waste_Loss'] - raw_ops['Rider_Labor']) / raw_ops['Projected_Rev']
    
    # 3. Save to Processed (This is what app.py will read)
    raw_ap.to_csv(BASE_DIR / "data/processed/cleaned_ap.csv", index=False)
    raw_ops.to_csv(BASE_DIR / "data/processed/daily_cash_forecast.csv", index=False)
    
    logging.info("Pipeline Complete: CM2 margins and AP aging processed.")

if __name__ == "__main__":
    process_all()