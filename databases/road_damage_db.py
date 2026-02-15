import mysql.connector
import streamlit as st
import os

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        port=3306
    )

def insert_road_damage(data):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO road_damage_logs
    (image_id, image_url, timestamp, city,area, latitude, longitude,
     camera_source, weather, road_type, resolution, annotated)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(query, data)
    conn.commit()
    conn.close()
