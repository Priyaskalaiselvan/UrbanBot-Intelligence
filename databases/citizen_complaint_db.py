import mysql.connector
import os

import mysql.connector
import streamlit as st

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        port=3306
    )

# ---------- Insert a new complaint ----------
def insert_complaint(city,area, category, text, lat, lon, dept, priority):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO citizen_complaints
    (city,area, category, complaint_text, latitude, longitude, department, priority)
    VALUES (%s,%s, %s, %s, %s, %s, %s, %s)
    """

    values = (city, area,category, text, lat, lon, dept, priority)
    cursor.execute(query, values)

    conn.commit()
    conn.close()

# ---------- Fetch latest complaints for live log ----------
def fetch_complaints(limit=10):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT complaint_id, city, area,category, priority, complaint_text, timestamp
        FROM citizen_complaints
        ORDER BY timestamp DESC
        LIMIT %s
    """

    cursor.execute(query, (limit,))
    rows = cursor.fetchall()

    conn.close()
    return rows
