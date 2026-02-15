import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from databases.aqi_db import insert_aqi_log
from datetime import datetime



# ---------- load models ----------
def load_models():

    rf_model = joblib.load("models/aqi_calculation.pkl")
    cols = joblib.load("models/aqi_calc_columns.pkl")

    arima_models = {
        "Chennai": joblib.load("models/chennai_arima.pkl"),
        "Bengaluru": joblib.load("models/bangalore_arima.pkl"),
        "Delhi": joblib.load("models/delhi_arima.pkl"),
        "Jaipur": joblib.load("models/jaipur_arima.pkl"),
    }

    return rf_model, cols, arima_models



# ---------- rules ----------
def aqi_category(aqi):

    if aqi <= 50:
        return "Good"

    elif aqi <= 200:
        return "Moderate"

    elif aqi <= 400:
        return "Poor"

    else:
        return "Severe"
    
def aqi_badge(cat):
    return {
        "Good": "GOOD 🟢",
        "Moderate": "MODERATE 🟡",
        "Poor": "POOR 🟠",
        "Severe": "SEVERE 🔴"
    }.get(cat, cat)

def aqi_color_style(val):
    if val <= 50:
        return "color: green; font-weight:700"
    elif val <= 100:
        return "color: goldenrod; font-weight:700"
    elif val <= 200:
        return "color: orange; font-weight:700"
    else:
        return "color: red; font-weight:700"


def health_message(cat):
    return {
        "Good": "Air quality is good",
        "Moderate": "Sensitive people should reduce outdoor activity",
        "Poor": "Breathing discomfort likely — limit exposure",
        "Severe": "Health alert — stay indoors"
    }[cat]

CITY_COORDS = {
    "Chennai": (13.0827, 80.2707),
    "Bengaluru": (12.9716, 77.5946),
    "Delhi": (28.6139, 77.2090),
    "Jaipur": (26.9124, 75.7873)
}


# ---------- page ----------
def show_aqi_page():

    st.header("🌍 AQI Intelligence Module")

    rf_model, model_cols, arima_models = load_models()
    if rf_model is None:
        return

    # -----------------------
    # Predictor Section
    # -----------------------
    

    st.subheader("Location Details")

    col1, col2 = st.columns(2)

    with col1:
        city = st.selectbox("City", list(CITY_COORDS.keys()))
        default_lat, default_lon = CITY_COORDS[city]

        station = st.text_input(
             "Monitoring Station",
               value="UrbanBot Predictor"
        )

    with col2:
        latitude = st.number_input( "Latitude",value=default_lat,format="%.6f")
        
        longitude = st.number_input("Longitude",value=default_lon,format="%.6f")

        
    st.subheader("AQI Predictor")

    c1, c2 = st.columns(2)

    with c1:
        pm25 = st.number_input("PM2.5", 0.0, 1000.0, 80.0)
        pm10 = st.number_input("PM10", 0.0, 1000.0, 120.0)
        no = st.number_input("NO", 0.0, 500.0, 20.0)
        no2 = st.number_input("NO2", 0.0, 500.0, 40.0)

    with c2:
        nox = st.number_input("NOx", 0.0, 500.0, 60.0)
        co = st.number_input("CO", 0.0, 50.0, 1.0)
        so2 = st.number_input("SO2", 0.0, 500.0, 10.0)
        o3 = st.number_input("O3", 0.0, 500.0, 30.0)

    if st.button("Predict AQI"):

        df = pd.DataFrame(
            [[pm25, pm10, no, no2, nox, co, so2, o3]],
            columns=model_cols
        )

        pred = rf_model.predict(df)[0]
        cat = aqi_category(pred)

        st.metric("Predicted AQI", round(pred,1))

        data = (
           datetime.now(),
           city,
           station,
           latitude,
           longitude,
           pm25,
           pm10,
           co,
           no2,
           so2,
           o3,
           int(pred),
           cat
        )

        try:
            insert_aqi_log(data)
            st.success("AQI log saved ✅")

        except Exception as e:
            st.error(f"AQI DB insert failed: {e}")
        # 🎨 color badge
        color_map = {
            "Good": "#2ecc71",
            
            "Moderate": "#f39c12",
            "Poor": "#e74c3c",
           
           "Severe": "#8e44ad"
        }

        st.markdown(
                f"""
                <div style="
                    display:inline-block;
                    padding:8px 18px;
                    border-radius:20px;
                    background:{color_map[cat]};
                    color:white;
                    font-weight:bold;
                    font-size:18px;">
                    {cat}
                </div>
                """,
                unsafe_allow_html=True
        )

       


        st.caption(health_message(cat))

    # -----------------------
    # Forecast Section
    # -----------------------
    st.subheader("AQI Forecast")
    
    st.markdown("""
       <style>
       .aqi-card {
           background: #f8fafc;
           padding: 18px;
           border-radius: 14px;
           box-shadow: 0 6px 18px rgba(0,0,0,0.08);
           border: 1px solid #e5e7eb;
           margin-bottom: 12px;
        }
        </style>
    """, unsafe_allow_html=True)

    city = st.selectbox("Select City", list(arima_models.keys()))
    days = st.slider("Forecast Days", 1, 14, 5)

    if st.button("Run Forecast"):
        model = arima_models[city]
        fc = model.get_forecast(steps=days)
        mean = fc.predicted_mean

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="aqi-card">', unsafe_allow_html=True)

            st.subheader("Forecast Table")

            forecast_df = mean.to_frame(name="AQI")
            forecast_df["AQI"] = forecast_df["AQI"].round(2)
            forecast_df["AQI_Level"] = forecast_df["AQI"].apply(
                lambda x: aqi_badge(aqi_category(x))
            )
            forecast_df.index = forecast_df.index.date
           # forecast_df = forecast_df.reset_index(drop=True)

            styled_df = (
                 forecast_df.style
                 .map(aqi_color_style, subset=["AQI"])
                 .set_properties(**{
                    "color": "#111827",
                    "font-size": "14px"
                 })
            )

            st.dataframe(styled_df, width="stretch")

            st.markdown('</div>', unsafe_allow_html=True)


        with col2:
            st.markdown('<div class="aqi-card">', unsafe_allow_html=True)

            st.subheader("AQI Trend")

            fig, ax = plt.subplots(figsize=(6,3))
            ax.plot(mean.index, mean.values, marker="o")
            ax.set_title("AQI Forecast Trend")
            ax.set_xlabel("Date")
            ax.set_ylabel("AQI")
            ax.tick_params(axis="x", rotation=45)

            st.pyplot(fig)

    st.markdown('</div>', unsafe_allow_html=True)



# 🔥 REQUIRED for switch_page navigation
show_aqi_page()

