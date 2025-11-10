import streamlit as st
import sqlite3
import pandas as pd

st.title(" Login History")

# Connect to the correct database
conn = sqlite3.connect("login_times.db")
c = conn.cursor()

# Create table if it doesn't exist (safe fallback)
c.execute('''
    CREATE TABLE IF NOT EXISTS logins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        status TEXT,
        timestamp TEXT
    )
''')
conn.commit()

# Fetch login/logout data
try:
    c.execute("SELECT name, status, timestamp FROM logins ORDER BY timestamp DESC")
    data = c.fetchall()
    if data:
        df = pd.DataFrame(data, columns=["Name", "Status", "Time"])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No login history found.")
except sqlite3.OperationalError as e:
    st.error(f"Database Error: {e}")
finally:
    conn.close()
