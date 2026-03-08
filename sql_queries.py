import streamlit as st
import pandas as pd
from utils.db_connection import get_connection

st.set_page_config(page_title="SQL Analytics", layout="wide")

st.title("📊 Cricbuzz Advanced SQL Analytics Dashboard")

# -------------------------------
# Database Connection
# -------------------------------

@st.cache_resource
def get_db():
    return get_connection()

conn = get_db()


# -------------------------------
# SQL Query Dictionary
# -------------------------------

SQL_QUERIES = {

"Basic Analysis": {

"Q1 Players representing India": """
SELECT DISTINCT 
    p.player_name AS full_name,
    p.playing_role,
    p.batting_style,
    p.bowling_style
FROM players p
JOIN batsmen b
ON p.player_id = b.batsman_id
WHERE b.team = 'India';
""",

"Q2 Matches played in last 7 days": """
SELECT 
    m.match_desc,
    m.team1,
    m.team2,
    v.ground AS venue_name,
    v.city,
    m.match_date
FROM matches m
LEFT JOIN venue v
ON m.venue = v.ground
WHERE m.match_date >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY m.match_date DESC;
""",

"Q3 Top 10 ODI run scorers": """
SELECT 
    player_name,
    runs AS total_runs,
    batting_avg,
    centuries
FROM odi_batting_stats
ORDER BY runs DESC
LIMIT 10;
""",

"Q4 Large capacity venues": """
SELECT 
    ground AS venue_name,
    city,
    country,
    capacity
FROM venue
WHERE capacity > 25000
ORDER BY capacity DESC
LIMIT 10;
""",

"Q5 Matches won by each team": """
SELECT 
    team_name,
    total_wins
FROM team_wins
ORDER BY total_wins DESC;
""",

"Q6 Players per role": """
SELECT 
    playing_role,
    COUNT(*) AS player_count
FROM players
GROUP BY playing_role
ORDER BY player_count DESC;
""",

"Q7 Highest score in each format": """
SELECT 
    format,
    highest_score
FROM format_wise_highest_scores
ORDER BY highest_score DESC;
""",

"Q8 Series started in 2024": """
SELECT 
    series_name,
    host_country,
    match_types AS match_type,
    start_date,
    total_matches
FROM matches_2024
WHERE EXTRACT(YEAR FROM start_date) = 2024;
"""
},

# -------------------------------
# Intermediate Analytics
# -------------------------------

"Intermediate Analytics": {

"Q9 All-rounders >1000 runs and >50 wickets": """
SELECT 
    p.player_name,
    a.total_runs,
    a.total_wickets,
    a.cricket_format
FROM all_rounder_stats a
JOIN players p
ON p.player_id = a.player_id
WHERE a.total_runs > 1000
AND a.total_wickets > 50;
""",

"Q10 Last 20 completed matches": """
SELECT 
    match_desc,
    team1,
    team2,
    match_winner AS winning_team,
    CASE
        WHEN win_margin_runs > 0 THEN win_margin_runs
        ELSE win_margin_wickets
    END AS victory_margin,
    CASE
        WHEN win_margin_runs > 0 THEN 'Runs'
        ELSE 'Wickets'
    END AS victory_type,
    venue
FROM matches
WHERE match_winner IS NOT NULL
ORDER BY match_date DESC
LIMIT 20;
""",

"Q11 Player performance across formats": """
SELECT 
    player_name,
    SUM(CASE WHEN format = 'Test' THEN runs ELSE 0 END) AS test_runs,
    SUM(CASE WHEN format = 'ODI' THEN runs ELSE 0 END) AS odi_runs,
    SUM(CASE WHEN format = 'T20I' THEN runs ELSE 0 END) AS t20_runs,
    AVG(batting_average) AS overall_batting_average
FROM player_batting_stats
GROUP BY player_name
HAVING COUNT(DISTINCT format) >= 2;
""",

"Q13 100+ partnerships": """
SELECT 
    match_id,
    innings_id,
    bat1_name,
    bat2_name,
    total_runs
FROM partnerships
WHERE total_runs >= 100
ORDER BY total_runs DESC;
""",

"Q14 Bowling performance by venue": """
SELECT
    b.bowler_id,
    b.bowler_name,
    m.venue,
    COUNT(DISTINCT b.match_id) AS matches_played,
    ROUND(AVG(b.economy)::numeric,2) AS avg_economy,
    SUM(b.wickets) AS total_wickets
FROM bowlers b
JOIN matches m
ON b.match_id = m.match_id
WHERE b.overs >= 4
GROUP BY b.bowler_id, b.bowler_name, m.venue
HAVING COUNT(DISTINCT b.match_id) >= 3
ORDER BY total_wickets DESC;
"""
},

# -------------------------------
# Advanced SQL Analytics
# -------------------------------

"Advanced SQL Analytics": {

"Q16 Player yearly performance": """
WITH match_runs AS (
    SELECT
        b.batsman_id,
        b.batsman_name,
        b.match_id,
        EXTRACT(YEAR FROM m.match_date) AS year,
        SUM(b.runs) AS runs_in_match,
        AVG(b.strike_rate) AS strike_rate
    FROM batsmen b
    JOIN matches m
        ON b.match_id = m.match_id
    WHERE EXTRACT(YEAR FROM m.match_date) >= 2020
    GROUP BY
        b.batsman_id,
        b.batsman_name,
        b.match_id,
        EXTRACT(YEAR FROM m.match_date)
)
SELECT
    batsman_id,
    batsman_name,
    year,
    COUNT(match_id) AS matches_played,
    ROUND(AVG(runs_in_match)::numeric,2) AS avg_runs,
    ROUND(AVG(strike_rate)::numeric,2) AS avg_strike_rate
FROM match_runs
GROUP BY
    batsman_id,
    batsman_name,
    year
HAVING COUNT(match_id) >= 5
ORDER BY year DESC, avg_runs DESC;
""",

"Q18 Most economical bowlers": """
WITH bowler_stats AS (
SELECT
    bowler_id,
    bowler_name,
    COUNT(DISTINCT match_id) AS matches_played,
    SUM(overs) AS total_overs,
    SUM(runs) AS total_runs,
    SUM(wickets) AS total_wickets
FROM bowlers
GROUP BY bowler_id,bowler_name
)
SELECT
    bowler_id,
    bowler_name,
    matches_played,
    total_wickets,
    ROUND((total_runs / total_overs)::numeric,2) AS economy_rate
FROM bowler_stats
WHERE matches_played >= 10
AND (total_overs / matches_played) >= 2
ORDER BY economy_rate ASC;
""",

"Q19 Most consistent batsmen": """
SELECT
    batsman_id,
    batsman_name,
    COUNT(*) AS innings_played,
    ROUND(AVG(runs)::numeric,2) AS avg_runs,
    ROUND(STDDEV(runs)::numeric,2) AS consistency
FROM batsmen b
JOIN matches m
ON b.match_id = m.match_id
WHERE balls >= 10
AND EXTRACT(YEAR FROM m.match_date) >= 2022
GROUP BY batsman_id,batsman_name
HAVING COUNT(*) >= 5
ORDER BY consistency ASC;
"""
}}


# -------------------------------
# Sidebar Navigation
# -------------------------------

category = st.sidebar.selectbox(
"Select Query Category",
list(SQL_QUERIES.keys())
)

query_name = st.sidebar.selectbox(
"Select Analysis Question",
list(SQL_QUERIES[category].keys())
)

query = SQL_QUERIES[category][query_name]


# -------------------------------
# Execute Query
# -------------------------------

if st.button("Run SQL Analysis"):

    try:

        df = pd.read_sql(query, conn)

        st.subheader("📈 Query Result")

        st.dataframe(
            df,
            use_container_width=True
        )

        st.success(f"{len(df)} rows returned")

    except Exception as e:

        st.error("Query execution failed")
        st.exception(e)


# -------------------------------
# Show SQL Query
# -------------------------------

with st.expander("View SQL Query"):
    st.code(query, language="sql")