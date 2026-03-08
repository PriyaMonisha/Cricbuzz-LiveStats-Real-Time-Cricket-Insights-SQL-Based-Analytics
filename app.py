import streamlit as st
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Cricbuzz Live Stats", layout="wide")

# Refresh whole app every 60 seconds
st_autorefresh(interval=60000, key="apprefresh")

st.title("🏏 Cricbuzz Live Stats Dashboard")

st.write("""
Welcome to the **Cricket Analytics Dashboard**

Use the sidebar to explore:

• Live Matches  
• Top Player Statistics  
• SQL Analytics Queries  
• Player CRUD Operations
""")