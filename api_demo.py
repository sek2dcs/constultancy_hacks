import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime

# page config
st.set_page_config(
    page_title="Consultancy Hacks Dashboard",
    layout="wide"
)

# getting api data
@st.cache_data()
def fetch_live_raw_data():
    """pulling live carbon data from UK site"""
    # endpoint pulls data from today only via /date 
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
    """pulling historical carbon data from Jan 1 2024"""
    url = "https://api.carbonintensity.org.uk/intensity/date/2024-01-01"
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



# dashboard setup 
st.title("Consultancy Hacks API Demo")
st.markdown("---")

# hard coding fake metric numbers
st.subheader("(Fake) Metric Numbers")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Quarterly Value", 
        value="$100k"
    )
with col2:
    st.metric(
        label="Monthly Value", 
        value="$10k"
    )
with col3:
    st.metric(
        label="Weekly Value", 
        value="$50k"
    )
with col4:
    st.metric(
        label="Annual Value", 
        value="$1M"
    )

st.markdown("<br><br>", unsafe_allow_html=True)


tab1, tab2, tab3 = st.tabs(["What is an API?", "Live Data Example", "Historical Data Example"])

with tab1: 
    st.markdown("### What is an API?")

with tab2:
    st.markdown("#### Pulling live data via API endpoint")
    st.markdown("This page shows the functionalities of pulling in live data from an API endpoint. Each time the dashboard refreshes, another pull is made to the API key to obtain live data.")
    
    live_df = fetch_live_raw_data()
    
    if not live_df.empty:
        fig_live = px.line(
            live_df, 
            x='Timestamp', 
            y='Raw Intensity (gCO2/kWh)'
        )
        fig_live.update_layout(
            xaxis_title="Time",
            yaxis_title="Intensity (gCO2/kWh)"
          
        )
        st.plotly_chart(fig_live, use_container_width=True)
        
        with st.expander("View Raw Data Table"):
            st.dataframe(live_df, use_container_width=True)
    else:
        st.warning("Data not pulling")


with tab3:
    st.markdown("#### Pulling historical/stagnant data via API endpoint")
    st.markdown("This page shows the functionalities of pulling in historical/stagnant data via a sepcific API endpoint that filters for data that was collected on Jan 1 2024. Each time the dashboard refreshes, another pull is made to the API key to obtain historical/stagnant data.")
    
    stagnant_df = fetch_stagnant_raw_data()
    
    if not stagnant_df.empty:
        fig_stagnant = px.area(
            stagnant_df, 
            x='Timestamp', 
            y='Intensity (gCO2/kWh)'
        )
        fig_stagnant.update_layout(
            xaxis_title="Time",
            yaxis_title="Intensity (gCO2/kWh)"
        )
        st.plotly_chart(fig_stagnant, use_container_width=True)
        
        with st.expander("View Raw Data Table"):
            st.dataframe(stagnant_df, use_container_width=True)
    else:
        st.warning("Data not pulling")