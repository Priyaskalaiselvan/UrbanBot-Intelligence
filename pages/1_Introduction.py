import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="UrbanBot Introduction",
    page_icon="🏙️",
    layout="wide"
)

# ---------------- CSS STYLE ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #e0e7ff, #dbeafe, #c7d2fe);
}

.title {
    font-size: 44px;
    font-weight: 900;
    color: #4338ca;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #475569;
    font-size: 18px;
    margin-bottom: 35px;
}

.card {
    background: rgba(255,255,255,0.55);
    backdrop-filter: blur(14px);
    border-radius: 22px;
    padding: 28px;
    box-shadow: 0 18px 35px rgba(0,0,0,0.18);
    margin-bottom: 20px;
}

.section-title {
    font-size: 22px;
    font-weight: 800;
    color: #1e293b;
    margin-bottom: 10px;
}

.arch-box {
    background: #0f172a;
    color: #e5e7eb;
    border-radius: 16px;
    padding: 20px;
    font-family: monospace;
    font-size: 14px;
    line-height: 1.6;
}

.stButton>button {
    background: linear-gradient(to right, #4f46e5, #22d3ee);
    color: white;
    font-weight: 700;
    border-radius: 30px;
    padding: 12px 28px;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="title">🏙️ UrbanBot Intelligence</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">AI-Powered Smart City Monitoring & Intelligence System</div>',
    unsafe_allow_html=True
)

# ---------------- OVERVIEW ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🔍 Project Overview</div>', unsafe_allow_html=True)
st.write("""
UrbanBot is an AI-driven smart city monitoring platform that analyzes urban
conditions such as traffic congestion, crowd density, accident severity,
air quality, infrastructure damage, and citizen complaints through a unified dashboard.

It converts live and recorded inputs into structured intelligence to support
faster and more accurate decision-making.
""")
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- PROBLEM + SOLUTION ----------------
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚠️ Problem Statement</div>', unsafe_allow_html=True)
    st.write("""
Urban monitoring systems are usually separated and reactive.
Traffic, safety, pollution, and complaints are tracked independently,
causing delayed response and poor coordination.
There is no single intelligent view of city risk indicators.
""")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💡 Our Solution</div>', unsafe_allow_html=True)
    st.write("""
UrbanBot integrates AI models, computer vision, and database logging
into one smart dashboard that detects events, assigns severity levels,
and displays real-time insights for action.
""")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- OBJECTIVES ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🎯 Objectives</div>', unsafe_allow_html=True)
st.markdown("""
- Real-time urban monitoring  
- Traffic & crowd detection  
- Accident and risk identification  
- AQI tracking  
- Complaint & alert logging  
- Unified intelligence dashboard  
- Faster operational response  
""")
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- TOOLS ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🛠 Tools & Technologies</div>', unsafe_allow_html=True)
st.markdown("""
**Technologies**
- Python
- Machine Learning
- Computer Vision
- AI detection models

**System Stack**
- Streamlit UI
- SQL database
- Detection pipelines
- Real-time logging modules
""")
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- IMPACT + USE CASES ----------------
col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🌍 Impact</div>', unsafe_allow_html=True)
    st.markdown("""
- Faster emergency response  
- Better traffic control  
- Safer crowd handling  
- Pollution awareness  
- Data-driven governance  
""")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🏙 Use Cases</div>', unsafe_allow_html=True)
    st.markdown("""
- Smart city control rooms  
- Traffic departments  
- Event monitoring teams  
- Municipal bodies  
- Environmental units  
""")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- REALTIME + FUTURE ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">⏱ Real-Time Monitoring Value</div>', unsafe_allow_html=True)
st.write("""
UrbanBot continuously updates predictions and logs from incoming data,
allowing live visibility of congestion, density, incidents, and alerts —
supporting proactive rather than delayed action.
""")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🚀 Future Enhancements</div>', unsafe_allow_html=True)
st.markdown("""
- Multi-camera live feeds  
- Predictive congestion forecasting  
- IoT sensor integration  
- Automated alert notifications  
- Map-based visualization  
""")
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- ARCHITECTURE ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🧠 Project Architecture</div>', unsafe_allow_html=True)

st.markdown('<div class="arch-box">', unsafe_allow_html=True)
st.text("""
Data Sources
  ↓
Cameras / Images / Sensor Inputs / User Reports
  ↓
AI Processing Layer
  • Traffic Detection Model
  • Crowd Density Model
  • Accident Detection
  • AQI Prediction
  • Road Damage Detection
  ↓
Analysis & Classification
  • Severity Levels
  • Density Levels
  • Congestion Scores
  ↓
Database Layer (SQL Logging)
  • Traffic Logs
  • Crowd Logs
  • Alerts
  • Complaints
  ↓
UrbanBot Intelligence Dashboard
  • Monitoring Tables
  • Alerts Panel
  • Admin AI Assistant
""")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- NAV BUTTON ----------------
st.markdown("<br>", unsafe_allow_html=True)

if st.button("🚦 Enter UrbanBot Dashboard"):
    st.switch_page("main.py")
