import mysql.connector
from datetime import datetime
import streamlit as st
import os

# -------------------------
# DB CONFIG — change to yours
# -------------------------
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        port=3306
    )


# -------------------------
# Insert Crowd Log
# -------------------------
def insert_crowd_log(data):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO crowd_density_logs
    (timestamp,
     city,
     area,
     latitude,
     longitude,
     predicted_count,
     density_level,
     image_url)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(query, data)
    conn.commit()
    conn.close()

