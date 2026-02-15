import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import streamlit as st
import os




SENDER_EMAIL = os.getenv("EMAIL_SENDER")
SENDER_PASS = os.getenv("EMAIL_PASSWORD")
RECEIVER_EMAIL = os.getenv("EMAIL_RECEIVER")

def send_alert_email(subject,body):
  
  msg = MIMEMultipart()
  msg['From'] = SENDER_EMAIL
  msg['To'] = RECEIVER_EMAIL
  msg['Subject'] = subject
  msg.attach(MIMEText(body,'plain'))

  try:
    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login(SENDER_EMAIL, SENDER_PASS)
    server.sendmail(SENDER_EMAIL,RECEIVER_EMAIL,msg.as_string())
    server.quit()
    return True
    

  except Exception as e:
    return str(e) 



