import streamlit as st
import psycopg2
import pandas as pd

secret = "monineha"

DB_CONFIG = {
    "dbname": "cricbuzz",
    "user": "postgres",
    "password": secret,
    "host": "localhost",
    "port": 5432
}

def connect():
    return psycopg2.connect(**DB_CONFIG)


st.title("⚙ Player CRUD Operations")

menu = st.sidebar.selectbox(
    "Choose Operation",
    ["View Players","Add Player","Update Player","Delete Player"]
)

# -----------------------------
# VIEW PLAYERS
# -----------------------------
if menu == "View Players":

    conn = connect()
    df = pd.read_sql("SELECT * FROM players ORDER BY player_id", conn)
    conn.close()

    st.subheader("All Players")
    st.dataframe(df)

# -----------------------------
# ADD PLAYER
# -----------------------------
elif menu == "Add Player":

    st.subheader("Add New Player")

    name = st.text_input("Player Name")
    role = st.text_input("Playing Role")
    batting = st.text_input("Batting Style")
    bowling = st.text_input("Bowling Style")

    if st.button("Add Player"):

        conn = connect()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO players
            (player_name,playing_role,batting_style,bowling_style)
            VALUES (%s,%s,%s,%s)
            """,
            (name,role,batting,bowling)
        )

        conn.commit()
        conn.close()

        st.success("Player added successfully")

# -----------------------------
# UPDATE PLAYER
# -----------------------------
elif menu == "Update Player":

    st.subheader("Update Player")

    player_id = st.number_input("Player ID", step=1)

    new_name = st.text_input("New Player Name")
    new_role = st.text_input("New Role")

    if st.button("Update Player"):

        conn = connect()
        cur = conn.cursor()

        cur.execute(
            """
            UPDATE players
            SET player_name=%s,
                playing_role=%s
            WHERE player_id=%s
            """,
            (new_name,new_role,player_id)
        )

        conn.commit()
        conn.close()

        st.success("Player updated")

# -----------------------------
# DELETE PLAYER
# -----------------------------
elif menu == "Delete Player":

    st.subheader("Delete Player")

    player_id = st.number_input("Player ID to Delete", step=1)

    if st.button("Delete Player"):

        conn = connect()
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM players WHERE player_id=%s",
            (player_id,)
        )

        conn.commit()
        conn.close()

        st.warning("Player deleted")