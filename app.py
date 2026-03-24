import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# --- CONFIG ---
st.set_page_config(page_title="Strategic Finance Tower", layout="wide")
DATA_PATH = Path(__file__).parent / "data" / "processed"

@st.cache_data
def load_data():
    ap = pd.read_csv(DATA_PATH / "cleaned_ap.csv", parse_dates=['Due_Date'])
    ops = pd.read_csv(DATA_PATH / "daily_cash_forecast.csv", parse_dates=['Date'])
    return ap, ops

df_ap, df_ops = load_data()
today = pd.Timestamp.now().normalize()

# --- SIDEBAR: LEVERS & FILTERS ---
st.sidebar.header("🕹️ Strategic Levers")
starting_cash = st.sidebar.number_input("Starting Cash (€)", value=10000000)
dpo_ext = st.sidebar.slider("DPO Extension (Days)", 0, 30, 0)
eff_gain = st.sidebar.slider("Waste Efficiency Gain (%)", 0, 50, 10) / 100

st.sidebar.markdown("---")
hubs = df_ops['Hub_Location'].unique()
hub_filter = st.sidebar.multiselect("Filter by Berlin Hub", options=hubs, default=hubs)

# --- CALCULATION ENGINE ---
f_ops = df_ops[df_ops['Hub_Location'].isin(hub_filter)].copy()
f_ap = df_ap[df_ap['Hub_Location'].isin(hub_filter)].copy()

f_ap['Adj_Due_Date'] = f_ap['Due_Date'] + pd.to_timedelta(dpo_ext, unit='d')
f_ops['Adj_Cash_In'] = f_ops['CM2_Net_Cash'] + (f_ops['Waste_Loss'] * eff_gain)

weekly_data = []
curr_bal = starting_cash

for i in range(13):
    start, end = today + pd.Timedelta(weeks=i), today + pd.Timedelta(weeks=i+1)
    inc = f_ops[(f_ops['Date'] >= start) & (f_ops['Date'] < end)]['Adj_Cash_In'].sum()
    out = f_ap[(f_ap['Adj_Due_Date'] >= start) & (f_ap['Adj_Due_Date'] < end)]['Amount_EUR'].sum()
    net_change = inc - out
    curr_bal += net_change
    weekly_data.append({'Week': f"W{i+1}", 'Inflow': inc, 'Outflow': out, 'Net': net_change, 'Balance': curr_bal})

df_cf = pd.DataFrame(weekly_data)

# --- STRATEGIC METRICS ---
avg_weekly_burn = -df_cf['Net'].mean()
if avg_weekly_burn > 0:
    runway = f"{curr_bal / avg_weekly_burn:.1f} Wks"
else:
    runway = "Self-Sustaining"

baseline_out = f_ap[(f_ap['Due_Date'] >= today) & (f_ap['Due_Date'] < today + pd.Timedelta(weeks=13))]['Amount_EUR'].sum()
current_out = f_ap[(f_ap['Adj_Due_Date'] >= today) & (f_ap['Adj_Due_Date'] < today + pd.Timedelta(weeks=13))]['Amount_EUR'].sum()
cash_unlocked = baseline_out - current_out

# --- UI LAYOUT ---
st.title("🏙️ Berlin Hub: Cash Liquidity")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Projected Liquidity", f"€{curr_bal:,.0f}")
m2.metric("Net Weekly Burn/Gen", f"€{df_cf['Net'].mean():,.0f}")
m3.metric("Cash Runway", runway)
m4.metric("WC Cash Unlocked", f"€{cash_unlocked:,.0f}")

tab1, tab2 = st.tabs(["📈 Liquidity Projection", "📊 Operational Drill-Down"])

with tab1:
    st.plotly_chart(px.line(df_cf, x='Week', y='Balance', title="13-Week Cash Forecast (Direct Method)"), use_container_width=True)
    st.subheader("📑 Indirect Cash Flow Summary (Weekly)")
    st.table(df_cf.set_index('Week').style.format("€{:,.0f}"))

with tab2:
    col_a, col_b = st.columns(2)
    with col_a:
        st.plotly_chart(px.bar(f_ops.groupby('Hub_Location')['CM2_Net_Cash'].sum().reset_index(), 
                               x='Hub_Location', y='CM2_Net_Cash', title="Margin by District"), use_container_width=True)
    with col_b:
        st.plotly_chart(px.pie(f_ap, values='Amount_EUR', names='Category', title="Expense Categories"), use_container_width=True)