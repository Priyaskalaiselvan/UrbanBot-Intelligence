from streamlit_autorefresh import st_autorefresh
import streamlit as st
import pandas as pd
import mysql.connector
import os

st_autorefresh(interval=60000, key="datarefresh")  # refresh every 60 sec



st.set_page_config(layout="wide")

# ---------- DB CONNECT ----------

def get_conn():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        port=3306
    )

# ---------- LOAD DATA ----------
def load_table(name):
    conn = get_conn()
    df = pd.read_sql(f"SELECT * FROM {name}", conn)
    conn.close()
    return df

traffic_df = load_table("traffic_logs")
acc_df = load_table("accident_logs")
crowd_df = load_table("crowd_density_logs")
complaints_df = load_table("citizen_complaints")
alerts_df = load_table("system_alerts")
aqi_df = load_table("aqi_logs")
pothole_df = load_table("road_damage_logs")

# ---------- HEADER ----------

st.title("🏙️ Smart City Intelligence Dashboard")
st.markdown(
    "<p style='font-size:16px; color:gray;'>AI-Powered Real-Time Urban Monitoring</p>",
    unsafe_allow_html=True
)

st.markdown("### 📊 Live City Metrics Overview")


today = pd.Timestamp.today().date()

traffic_today = len(traffic_df[traffic_df.timestamp.dt.date == today])
accidents_today = len(acc_df[acc_df.timestamp.dt.date == today])

crowd_high_count = len(
    crowd_df[
        (crowd_df.timestamp.dt.date == today) &
        (crowd_df.density_level == "High")
    ]
)

complaints_today = len(complaints_df[complaints_df.timestamp.dt.date == today])
alerts_today = len(alerts_df[alerts_df.timestamp.dt.date == today])



def metric_card(title, value, accent):
    st.markdown(f"""
    <div style="
        background:white;
        padding:14px 16px;
        border-radius:12px;
        border-left:6px solid {accent};
        box-shadow:0 2px 6px rgba(0,0,0,0.08);
    ">
        <div style="font-size:13px; color:#555; font-weight:600;">
            {title}
        </div>
        <div style="font-size:22px; font-weight:700; margin-top:4px;">
            {value}
        </div>
    </div>
    """, unsafe_allow_html=True)


col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    metric_card("🚗 Traffic Today", traffic_today, "#3b82f6")

with col2:
    metric_card("💥 Accidents", accidents_today, "#ef4444")

with col3:
    metric_card("👥 Crowd Zones", crowd_high_count, "#8b5cf6")

with col4:
    metric_card("📝 Complaints", complaints_today, "#f59e0b")

with col5:
    metric_card("🚨 Alerts", alerts_today, "#374151")


# ---------- METRIC CARDS ----------
c1,c2,c3,c4 = st.columns(4)


st.markdown("### 📈 Daily City Trends")
def panel_start():
    st.markdown("""
        <div style="
            background:white;
            padding:14px;
            border-radius:12px;
            box-shadow:0 2px 6px rgba(0,0,0,0.08);
        ">
    """, unsafe_allow_html=True)

def panel_end():
    st.markdown("</div>", unsafe_allow_html=True)

traffic_daily = (
    traffic_df
    .groupby(traffic_df["timestamp"].dt.date)
    .size()
)

accident_daily = (
    acc_df
    .groupby(acc_df["timestamp"].dt.date)
    .size()
)

complaints_daily = (
    complaints_df
    .groupby(complaints_df["timestamp"].dt.date)
    .size()
)

aqi_daily = (
    aqi_df
    .groupby(aqi_df["timestamp"].dt.date)["aqi"]
    .mean()
)

colA, colB,col3 = st.columns(3)

with colA:
    panel_start()
    st.markdown("**🚗 Traffic Events Trend**")
    st.line_chart(traffic_daily)
    panel_end()

with colB:
    panel_start()
    st.markdown("**💥 Accident Trend**")
    st.line_chart(accident_daily)
    panel_end()

colC, colD,col3 = st.columns(3)

with colC:
    panel_start()
    st.markdown("**🌫 AQI Trend**")
    st.line_chart(aqi_daily)
    panel_end()
with colD:
    panel_start()
    st.markdown("**📝 Complaint Trend**")
    st.line_chart(complaints_daily)
    panel_end()

st.markdown("### 📋 Records Viewer")
st.markdown("""
<style>
[data-testid="stDataFrame"] {
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

record_type = st.selectbox(
    "Select Record Type",
    [
        "Traffic Records",
        "Accident Records",
        "Crowd Records",
        "Complaint Records",
        "Alert Records",
        "AQI Records"
    ]
)

if record_type == "Traffic Records":

    df = traffic_df[[
        "timestamp", "city", "area", "congestion_level"
    ]].copy()

    df = df.rename(columns={
        "timestamp": "Time",
        "city": "City",
        "area": "Area",
        "congestion_level": "Congestion"
    })

    st.dataframe(
        df.sort_values("Time", ascending=False),
        height=320,
        width="stretch"
    )

elif record_type == "Crowd Records":

    df = crowd_df[[
        "timestamp", "city", "area", "density_level"
    ]].copy()

    df.columns = ["Time","City","Area","Density"]

    st.dataframe(df.sort_values("Time", ascending=False),
                 height=320,
                 width="stretch")

elif record_type == "Accident Records":

    df = acc_df[[
        "timestamp", "city", "area", "severity"
    ]].copy()

    df.columns = ["Time","City","Area","Severity"]

    st.dataframe(df.sort_values("Time", ascending=False),
                 height=320,
                 width="stretch")
    
elif record_type == "Complaint Records":

    df = complaints_df[[
        "timestamp","city","area","department","priority"
    ]].copy()

    df.columns = ["Time","City","Area","Department","Priority"]

    st.dataframe(df.sort_values("Time", ascending=False),
                 height=320,
                 width="stretch")

elif record_type == "Alert Records":

    df = alerts_df[[
        "timestamp","location","message","severity"
    ]].copy()

    df.columns = ["Time","Location","Message","Severity"]

    st.dataframe(df.sort_values("Time", ascending=False),
                 height=320,
                 width="stretch")

elif record_type == "AQI Records":

    df = aqi_df[[
        "timestamp","city","aqi","aqi_category"
    ]].copy()

    df.columns = ["Time","City","AQI","AQI_Category"]

    st.dataframe(df.sort_values("Time", ascending=False),
                 height=320,
                 width="stretch")


