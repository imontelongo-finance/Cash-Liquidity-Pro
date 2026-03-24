import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import os
import subprocess

# Check if data exists; if not, run the generation script
if not os.path.exists('data/processed/processed_data.csv'):
    subprocess.run(["python", "scripts/generate_mock_data.py"])
    subprocess.run(["python", "scripts/process_data.py"])
# --- CONFIG ---
st.set_page_config(page_title="Flink Strategic Finance", layout="wide")
DATA_PATH = Path(__file__).parent / "data" / "processed"

# --- SIDEBAR: EXECUTIVE LEVERS ---
st.sidebar.header("🕹️ Strategic Levers")
starting_cash = st.sidebar.number_input("Starting Capital (€)", value=100000000)
dpo_extension = st.sidebar.slider("Vendor Payment Extension (Days)", 0, 30, 0)
efficiency_gain = st.sidebar.slider("Waste Reduction Goal (%)", 0, 50, 10) / 100

# --- LOAD DATA ---
@st.cache_data
def load_forecast():
    ap = pd.read_csv(DATA_PATH / "cleaned_ap.csv", parse_dates=['Due_Date'])
    ops = pd.read_csv(DATA_PATH / "daily_cash_forecast.csv", parse_dates=['Date'])
    return ap, ops

try:
    df_ap, df_ops = load_forecast()
except:
    st.error("⚠️ Data not found. Please run 'python scripts/generate_mock_data.py' first.")
    st.stop()

# --- CALCULATION ENGINE ---
df_ap['Adj_Due_Date'] = df_ap['Due_Date'] + pd.to_timedelta(dpo_extension, unit='d')
# Reduce waste based on lever
df_ops['Adj_Cash_In'] = df_ops['CM2_Net_Cash'] + (df_ops['Waste_Loss'] * efficiency_gain)

# 13-Week Aggregate
weekly_cash = []
current_balance = starting_cash

for i in range(13):
    start = pd.Timestamp.now().normalize() + pd.Timedelta(weeks=i)
    end = start + pd.Timedelta(weeks=1)
    
    inc = df_ops[(df_ops['Date'] >= start) & (df_ops['Date'] < end)]['Adj_Cash_In'].sum()
    out = df_ap[(df_ap['Adj_Due_Date'] >= start) & (df_ap['Adj_Due_Date'] < df_ap['Adj_Due_Date'])]['Amount_EUR'].sum()
    
    current_balance += (inc - out)
    weekly_cash.append({'Week': f"W{i+1}", 'Balance': current_balance})

df_final = pd.DataFrame(weekly_cash)

# --- VISUALS ---
st.title("🏙️ Berlin Hub: Liquidity & Path to Profitability")

c1, c2, c3 = st.columns(3)
c1.metric("Ending Cash (Q2)", f"€{current_balance/1e6:.1f}M")
c2.metric("Avg. Weekly CM2", f"€{df_ops['CM2_Net_Cash'].mean()*7/1e3:.1f}k")
c3.metric("Runway Status", "HEALTHY", delta="Stable")

st.plotly_chart(px.line(df_final, x='Week', y='Balance', title="13-Week Liquidity Projection", markers=True), use_container_width=True)

st.subheader("📦 Cash Drain by Category")
st.plotly_chart(px.pie(df_ap, values='Amount_EUR', names='Category', hole=0.4), use_container_width=True)