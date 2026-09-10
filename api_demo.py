import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="ESG Strategic Advisory Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# DATA FETCHING FUNCTIONS (RAW API DATA)
# ==========================================
@st.cache_data(ttl=300)
def fetch_live_raw_data():
    """Pulls today's raw half-hourly carbon intensity data from the UK National Grid."""
    # Using the /date endpoint without a specific date defaults to today
    url = "https://api.carbonintensity.org.uk/intensity/date"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()['data']
        df = pd.DataFrame([
            {'Timestamp': d['from'], 'Raw Intensity (gCO2/kWh)': d['intensity']['actual']} 
            for d in data if d['intensity']['actual'] is not None
        ])
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        return df
    except Exception:
        return pd.DataFrame(columns=['Timestamp', 'Raw Intensity (gCO2/kWh)'])

@st.cache_data
def fetch_stagnant_raw_data():
    """Pulls a fixed, stagnant day of raw data from the API (e.g., Oct 1, 2023)."""
    url = "https://api.carbonintensity.org.uk/intensity/date/2023-10-01"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()['data']
        df = pd.DataFrame([
            {'Timestamp': d['from'], 'Raw Intensity (gCO2/kWh)': d['intensity']['actual']} 
            for d in data
        ])
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        return df
    except Exception:
        return pd.DataFrame(columns=['Timestamp', 'Raw Intensity (gCO2/kWh)'])

# ==========================================
# DASHBOARD UI & FAKE METRICS
# ==========================================
st.title("📊 ESG & Grid Operations Summary")
st.markdown("---")

# FAKE STAKEHOLDER METRICS (Hardcoded for presentation)
st.subheader("Executive KPIs")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Quarterly OpEx Savings", 
        value="$1.24M", 
        delta="12.5% vs Target",
        delta_color="normal"
    )
with col2:
    st.metric(
        label="Carbon Tax Exposure", 
        value="$450K", 
        delta="-$50K YoY (Risk Reduced)",
        delta_color="inverse"
    )
with col3:
    st.metric(
        label="Grid Optimization Alpha", 
        value="94.2%", 
        delta="+1.4% WoW"
    )
with col4:
    st.metric(
        label="Regulatory Compliance Score", 
        value="98/100", 
        delta="Tier 1 Certified",
        delta_color="normal"
    )

st.markdown("<br><br>", unsafe_allow_html=True)

# TABS FOR RAW DATA VISUALIZATION
tab1, tab2 = st.tabs(["🟢 Live Raw Data (Today)", "📁 Stagnant Raw Data (Baseline)"])

# ------------------------------------------
# TAB 1: LIVE RAW DATA
# ------------------------------------------
with tab1:
    st.markdown("#### Today's Raw Carbon Intensity")
    st.markdown("Visualizing the raw JSON payload retrieved directly from the live API endpoint.")
    
    live_df = fetch_live_raw_data()
    
    if not live_df.empty:
        fig_live = px.line(
            live_df, 
            x='Timestamp', 
            y='Raw Intensity (gCO2/kWh)',
            markers=True,
            line_shape='spline',
            color_discrete_sequence=['#1f77b4']
        )
        fig_live.update_layout(
            xaxis_title="Time",
            yaxis_title="Raw Intensity (gCO2/kWh)",
            hovermode="x unified"
        )
        st.plotly_chart(fig_live, use_container_width=True)
        
        with st.expander("View Raw Data Table"):
            st.dataframe(live_df, use_container_width=True)
    else:
        st.warning("Awaiting live data or API is currently unreachable.")

# ------------------------------------------
# TAB 2: STAGNANT RAW DATA
# ------------------------------------------
with tab2:
    st.markdown("#### Historical Baseline (October 1, 2023)")
    st.markdown("Visualizing the raw JSON payload retrieved from a fixed historical API endpoint.")
    
    stagnant_df = fetch_stagnant_raw_data()
    
    if not stagnant_df.empty:
        fig_stagnant = px.area(
            stagnant_df, 
            x='Timestamp', 
            y='Raw Intensity (gCO2/kWh)',
            color_discrete_sequence=['#ff7f0e']
        )
        fig_stagnant.update_layout(
            xaxis_title="Time",
            yaxis_title="Raw Intensity (gCO2/kWh)",
            hovermode="x unified"
        )
        st.plotly_chart(fig_stagnant, use_container_width=True)
        
        with st.expander("View Raw Data Table"):
            st.dataframe(stagnant_df, use_container_width=True)
    else:
        st.warning("Awaiting stagnant data or API is currently unreachable.")