import streamlit as st
import pandas as pd
import psycopg2

# ---------- DATABASE CONNECTION ----------
secret = "monineha"

DB_CONFIG = {
    "dbname": "cricbuzz",
    "user": "postgres",
    "password": secret,
    "host": "localhost",
    "port": 5432
}

conn = psycopg2.connect(**DB_CONFIG)

st.title("🏏 Cricket Top Statistics")

# ---------- FORMAT SELECTION ----------
format_selected = st.selectbox(
    "Select Cricket Format",
    ["Test", "ODI", "T20"]
)

# ---------- BATSMEN QUERY ----------
batsman_query = f"""
SELECT
    b.batsman_name,
    SUM(b.runs) AS total_runs
FROM batsmen b
JOIN matches m
ON b.match_id = m.match_id
WHERE LOWER(m.match_format) = LOWER('{format_selected}')
GROUP BY b.batsman_name
ORDER BY total_runs DESC
LIMIT 10
"""

# ---------- BOWLERS QUERY ----------
bowler_query = f"""
SELECT
    bo.bowler_name,
    SUM(bo.wickets) AS total_wickets
FROM bowlers bo
JOIN matches m
ON bo.match_id = m.match_id
WHERE LOWER(m.match_format) = LOWER('{format_selected}')
GROUP BY bo.bowler_name
ORDER BY total_wickets DESC
LIMIT 10
"""

# ---------- FETCH DATA ----------
batsman_df = pd.read_sql(batsman_query, conn)
bowler_df = pd.read_sql(bowler_query, conn)

# ---------- BATSMEN SECTION ----------
st.subheader(f"Top Batsmen - {format_selected}")

if batsman_df.empty:
    st.warning("No batsman data available.")
else:
    st.dataframe(batsman_df)
    st.bar_chart(batsman_df.set_index("batsman_name"))

# ---------- BOWLERS SECTION ----------
st.subheader(f"Top Bowlers - {format_selected}")

if bowler_df.empty:
    st.warning("No bowler data available.")
else:
    st.dataframe(bowler_df)
    st.bar_chart(bowler_df.set_index("bowler_name"))

conn.close()