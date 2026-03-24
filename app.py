import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# --- CONFIG ---
st.set_page_config(page_title="Flink Strategic Finance Tower", layout="wide")
DATA_PATH = Path(__file__).parent / "data" / "processed"

@st.cache_data
def load_data():
    ap = pd.read_csv(DATA_PATH / "cleaned_ap.csv", parse_dates=['Due_Date'])
    ops = pd.read_csv(DATA_PATH / "daily_cash_forecast.csv", parse_dates=['Date'])
    return ap, ops

df_ap, df_ops = load_data()

# --- SIDEBAR: LEVERS & DRILL-DOWN ---
st.sidebar.header("🕹️ Strategic Levers")
starting_cash = st.sidebar.number_input("Starting Cash (€)", value=10000000)
dpo_ext = st.sidebar.slider("DPO Extension (Days)", 0, 30, 0)
eff_gain = st.sidebar.slider("Waste Efficiency Gain (%)", 0, 50, 10) / 100

st.sidebar.markdown("---")
hub_filter = st.sidebar.multiselect("Filter by Hub", options=df_ops['Hub_Location'].unique(), default=df_ops['Hub_Location'].unique())

# --- FILTERING ---
filtered_ops = df_ops[df_ops['Hub_Location'].isin(hub_filter)]

# --- CALCULATION ENGINE ---
df_ap['Adj_Due_Date'] = df_ap['Due_Date'] + pd.to_timedelta(dpo_ext, unit='d')
filtered_ops['Adj_Cash_In'] = filtered_ops['CM2_Net_Cash'] + (filtered_ops['Waste_Loss'] * eff_gain)

# 13-Week Forecast Logic
weekly_data = []
curr_bal = starting_cash
today = pd.Timestamp.now().normalize()

for i in range(13):
    start, end = today + pd.Timedelta(weeks=i), today + pd.Timedelta(weeks=i+1)
    
    # Cash Flow Components
    inc = filtered_ops[(filtered_ops['Date'] >= start) & (filtered_ops['Date'] < end)]['Adj_Cash_In'].sum()
    out = df_ap[(df_ap['Adj_Due_Date'] >= start) & (df_ap['Adj_Due_Date'] < end)]['Amount_EUR'].sum()
    net_change = inc - out
    curr_bal += net_change
    
    weekly_data.append({
        'Week': f"W{i+1}",
        'Inflow (Ops)': inc,
        'Outflow (AP)': out,
        'Net Cash Flow': net_change,
        'Ending Balance': curr_bal
    })

df_cf = pd.DataFrame(weekly_data)

# --- DASHBOARD VISUALS ---
st.title("🏙️ Berlin Hub: Strategic Finance Tower")

# Key Metrics
c1, c2, c3, c4 = st.columns(4)
c1.metric("Projected Liquidity", f"€{curr_bal/1e6:.2f}M")
c2.metric("Net Burn/Gen (Avg)", f"€{df_cf['Net Cash Flow'].mean()/1e3:.1f}k")
c3.metric("Efficiency Impact", f"€{(filtered_ops['Waste_Loss'].sum() * eff_gain)/1e3:.1f}k")
c4.metric("Active Hubs", len(hub_filter))

# Charts
tab1, tab2 = st.tabs(["📈 Liquidity Projection", "📊 Operational Drill-Down"])

with tab1:
    st.plotly_chart(px.line(df_cf, x='Week', y='Ending Balance', title="13-Week Cash Runway"), use_container_width=True)
    
    st.subheader("📑 Indirect Cash Flow Summary (Weekly)")
    st.table(df_cf.set_index('Week').style.format("€{:,.0f}"))

with tab2:
    col_a, col_b = st.columns(2)
    with col_a:
        st.plotly_chart(px.bar(filtered_ops.groupby('Hub_Location')['CM2_Net_Cash'].sum().reset_index(), 
                               x='Hub_Location', y='CM2_Net_Cash', title="CM2 Contribution by Hub"), use_container_width=True)
    with col_b:
        st.plotly_chart(px.pie(df_ap, values='Amount_EUR', names='Category', title="Expense Distribution (Working Capital)"), use_container_width=True)