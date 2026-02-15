import mysql.connector
import streamlit as st
import os
from databases.db_connect import get_connection


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        port=3306
    )
def insert_accident_log(data):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO accident_logs
    (accident_id,
     timestamp,
     image_url,
     city,
     area,
     latitude,
     longitude,
     severity,
     emergency_alert_sent)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(query, data)
    conn.commit()
    conn.close()
