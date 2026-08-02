import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

st.title("🌡️ Temperature Dashboard")

# Fetch temperature telemetry from Supabase
res = supabase.table("temperature").select("*").order("id", desc=False).execute()
df = pd.DataFrame(res.data)

if not df.empty:
    col1, col2, col3 = st.columns(3)
    col1.metric("Current", f"{df['temp'].iloc[-1]} °C")
    col2.metric("Max", f"{df['temp'].max()} °C")
    col3.metric("Min", f"{df['temp'].min()} °C")

    st.subheader("Temperature Trend")
    st.line_chart(df["temp"])
else:
    st.info("No temperature data available yet.")

