import mysql.connector
import streamlit as st
from datetime import datetime
import os

# -------------------------
# CONNECTION 
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
# INSERT AQI LOG
# -------------------------
def insert_aqi_log(data):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO aqi_logs
    (
        timestamp,
        city,
        monitoring_station,
        latitude,
        longitude,
        pm25,
        pm10,
        co,
        no2,
        so2,
        o3,
        aqi,
        aqi_category
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(query, data)

    conn.commit()
    conn.close()
