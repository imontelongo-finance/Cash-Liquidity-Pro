import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import os, sys, subprocess

# --- DATA SELF-HEALING ---
def initialize_data():
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    # If files are missing, run the full pipeline
    if not os.path.exists('data/processed/daily_cash_forecast.csv'):
        subprocess.run([sys.executable, "scripts/generate_mock_data.py"], check=True)
        subprocess.run([sys.executable, "scripts/process_data.py"], check=True)

initialize_data()

# --- CONFIG & LOAD ---
st.set_page_config(page_title="Flink Strategic Finance", layout="wide")
DATA_PATH = Path(__file__).parent / "data" / "processed"

@st.cache_data
def load_data():
    ap = pd.read_csv(DATA_PATH / "cleaned_ap.csv", parse_dates=['Due_Date'])
    ops = pd.read_csv(DATA_PATH / "daily_cash_forecast.csv", parse_dates=['Date'])
    return ap, ops

try:
    df_ap, df_ops = load_data()
except Exception as e:
    st.error(f"⚠️ Data Load Failed: {e}")
    st.stop()

# --- SIDEBAR & CALCULATIONS ---
st.sidebar.header("🕹️ Strategic Levers")
starting_cash = st.sidebar.number_input("Starting Capital (€)", value=100000000)
dpo_ext = st.sidebar.slider("Vendor Payment Extension (Days)", 0, 30, 0)
eff_gain = st.sidebar.slider("Waste Reduction Goal (%)", 0, 50, 10) / 100

# Calculation Engine
df_ap['Adj_Due_Date'] = df_ap['Due_Date'] + pd.to_timedelta(dpo_ext, unit='d')
df_ops['Adj_Cash_In'] = df_ops['CM2_Net_Cash'] + (df_ops['Waste_Loss'] * eff_gain)

# 13-Week Forecast Logic
weekly_cash = []
curr_bal = starting_cash
today = pd.Timestamp.now().normalize()

for i in range(13):
    start, end = today + pd.Timedelta(weeks=i), today + pd.Timedelta(weeks=i+1)
    inc = df_ops[(df_ops['Date'] >= start) & (df_ops['Date'] < end)]['Adj_Cash_In'].sum()
    out = df_ap[(df_ap['Adj_Due_Date'] >= start) & (df_ap['Adj_Due_Date'] < end)]['Amount_EUR'].sum()
    curr_bal += (inc - out)
    weekly_cash.append({'Week': f"W{i+1}", 'Balance': curr_bal})

# --- DASHBOARD ---
st.title("🏙️ Berlin Hub: Liquidity & Path to Profitability")
c1, c2, c3 = st.columns(3)
c1.metric("Ending Cash (Q2)", f"€{curr_bal/1e6:.1f}M")
c2.metric("Avg. Weekly CM2", f"€{df_ops['CM2_Net_Cash'].mean()*7/1e3:.1f}k")
c3.metric("Runway Status", "HEALTHY", delta="Stable")

st.plotly_chart(px.line(pd.DataFrame(weekly_cash), x='Week', y='Balance', title="13-Week Liquidity Projection"), use_container_width=True)
st.plotly_chart(px.pie(df_ap, values='Amount_EUR', names='Category', title="Cash Drain by Category", hole=0.4), use_container_width=True)