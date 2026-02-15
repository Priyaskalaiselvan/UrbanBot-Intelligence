import mysql.connector
import streamlit as st
from datetime import datetime
import os


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        port=3306
    )


def insert_traffic_log(data):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO traffic_logs
    (timestamp,
     city,
     area,
     latitude,
     longitude,
     vehicle_count,
     congestion_level,
     is_peak_hour,
     image_url)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(query, data)
    conn.commit()
    conn.close()
