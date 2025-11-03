# app.py
import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from heuristic_detector import analyze_dataframe as heuristic_analyze
from ai_analyzer import summarize_with_ai, count_failed_attempts
from dotenv import load_dotenv
import os

# --------------------
# โหลด .env และ OpenAI API Key
# --------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY ไม่ถูกตั้งค่าใน .env")
    st.stop()

st.title("AI Log Analyzer")

# --------------------
# เลือกวันที่
# --------------------
selected_date = st.date_input("เลือกวันที่ต้องการดู log")

# --------------------
# ตั้งค่า API URL
# --------------------
API_URL = "https://login-system-qlon.onrender.com/logs"

# --------------------
# ดึง log จาก API
# --------------------
@st.cache_data(ttl=60)
def fetch_logs():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        logs = response.json()
        df = pd.DataFrame(logs)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception as e:
        st.error(f"ไม่สามารถดึง log จาก API ได้: {e}")
        return pd.DataFrame()  # empty df

df_logs = fetch_logs()

# Filter ตามวันที่
df_selected = df_logs[df_logs['timestamp'].dt.date == selected_date]

st.subheader(f"Log ของวันที่ {selected_date}")
st.dataframe(df_selected)

# Heuristic check

threshold = st.number_input("Heuristic threshold", min_value=1, value=15)

if st.button("Run heuristic check"):
    counts, alerts = heuristic_analyze(df_selected, threshold)
    st.write("Counts per IP:")
    st.write(counts)
    if alerts:
        st.error(f"Possible brute-force detected: {alerts}")
    else:
        st.success("No brute-force detected")


if st.button("Ask AI to summarize"):
    with st.spinner("Sending to AI..."):
        lines = df_selected.apply(
            lambda row: f"{row['timestamp']} {row['username']} {row['ip_address']} {row['status']}\n",
            axis=1
        ).tolist()

        ip_counts = count_failed_attempts(lines)
        summary = summarize_with_ai("".join(lines), ip_counts, api_key=OPENAI_API_KEY)
        st.subheader("AI Summary")
        st.write(summary)

st.markdown("---")
st.info(
    "Logs are fetched from API. "
    "Select a date to view logs for that day only. "
    "Click 'Run heuristic check' to detect brute-force, or 'Ask AI to summarize' for AI analysis."
)

