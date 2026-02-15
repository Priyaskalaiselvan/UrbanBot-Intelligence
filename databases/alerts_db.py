import uuid
from datetime import datetime
import streamlit as st
import mysql.connector
import os


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        port=3306
    )
def insert_system_alert(
    alert_type,
    location,
    severity,
    message,
    email_sent
):

    conn = get_connection()
    cur = conn.cursor()

    query = """
    INSERT INTO system_alerts
    (alert_id, alert_type, timestamp, location,
     severity, message, email_sent, resolved)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """

    data = (
        str(uuid.uuid4()),
        alert_type,
        datetime.now(),
        location,
        severity,
        message,
        email_sent,
        False
    )

    cur.execute(query, data)
    conn.commit()

    cur.close()
    conn.close()
