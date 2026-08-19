import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

# Supabase Client Initialization
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    st.error("Missing SUPABASE_URL or SUPABASE_KEY in environment variables. Please configure your .env file.")
    st.stop()

supabase = create_client(supabase_url, supabase_key)

st.title("🌡️ Temperature Dashboard")

# Fetch temperature telemetry from Supabase
try:
    res = supabase.table("temperature").select("*").order("id", desc=False).execute()
    df = pd.DataFrame(res.data)

    if not df.empty and "temp" in df.columns:
        col1, col2, col3 = st.columns(3)
        col1.metric("Current", f"{df['temp'].iloc[-1]} °C")
        col2.metric("Max", f"{df['temp'].max()} °C")
        col3.metric("Min", f"{df['temp'].min()} °C")

        st.subheader("Temperature Trend")
        st.line_chart(df["temp"])
    else:
        st.info("No temperature data available yet. Run send_temp.py to insert readings.")
except Exception as e:
    st.error(f"Error fetching data from Supabase: {e}")
