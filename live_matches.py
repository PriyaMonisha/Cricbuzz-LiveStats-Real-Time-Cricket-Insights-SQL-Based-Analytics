import streamlit as st
import pandas as pd
from utils.db_connection import get_connection

st.title("📡 Live Matches")

conn = get_connection()

query = """
SELECT
match_id,
series_name,
match_format,
team1_name,
team1_runs,
team1_wickets,
team1_overs,
team2_name,
team2_runs,
team2_wickets,
team2_overs,
status,
city
FROM live_matches
ORDER BY start_date DESC
"""

df = pd.read_sql(query, conn)

format_filter = st.selectbox(
    "Select Format",
    ["All"] + sorted(df["match_format"].dropna().unique())
)

if format_filter != "All":
    df = df[df["match_format"] == format_filter]

st.dataframe(df, use_container_width=True)

conn.close()