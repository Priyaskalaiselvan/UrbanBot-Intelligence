import streamlit as st
import uuid
import cv2
import numpy as np
from datetime import datetime
from ultralytics import YOLO

from databases.traffic_detection_db import insert_traffic_log
from utils.email_alert import send_alert_email
from databases.alerts_db import insert_system_alert
from utils.s3_uploader import upload_image_to_s3
from utils.model_loader import ensure_model


st.set_page_config(page_title="Traffic Detection", layout="wide")

# ---------- theme ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #ecfeff, #eef2ff);
}
.card {
    background: white;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
.title {
    font-size: 32px;
    font-weight: 700;
    color: #0f172a;
}
.subtitle {
    font-size: 18px;
    color: #334155;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🚦 Traffic Detection Dashboard</div>', unsafe_allow_html=True)

# ---------- city + area coords ----------
CITY_AREA_DATA = {
    "Chennai": {
        "T Nagar": (13.0418, 80.2337),
        "Anna Nagar": (13.0850, 80.2101)
    },
    "Coimbatore": {
        "Gandhipuram": (11.0183, 76.9725),
        "RS Puram": (11.0089, 76.9510)
    },
    "Madurai": {
        "Anna Nagar": (9.9391, 78.1384),
        "KK Nagar": (9.9173, 78.1192)
    },
    "Tiruchirappalli": {
        "Srirangam": (10.8623, 78.6932),
        "Thillai Nagar": (10.8186, 78.6828)
    },
    "Salem": {
        "Fairlands": (11.6643, 78.1460),
        "Hasthampatti": (11.6710, 78.1348)
    }
}

left, right = st.columns([1,1])

# ================= LEFT =================
with left:
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">📍 Traffic Input</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        city = st.selectbox("City", list(CITY_AREA_DATA.keys()))

    with c2:
        area = st.selectbox("Area", list(CITY_AREA_DATA[city].keys()))

    # ✅ coordinates lookup
    lat, lon = CITY_AREA_DATA[city][area]

    # ---- coordinate row ----
    c3, c4 = st.columns(2)

    with c3:
        st.caption("Latitude")
        st.code(f"{lat:.6f}")

    with c4:
        st.caption("Longitude")
        st.code(f"{lon:.6f}")

    uploaded = st.file_uploader("Upload Traffic Image", type=["jpg","jpeg","png"])
    detect_btn = st.button("🚦 Detect Traffic")

    st.markdown('</div>', unsafe_allow_html=True)

# ================= RIGHT =================
with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">🧠 Detection Result</div>', unsafe_allow_html=True)

    if uploaded and detect_btn:

        lat, lon = CITY_AREA_DATA[city][area]

        with st.spinner("Loading model and detecting vehicles..."):
            ensure_model(
                "models/traffic_best.pt",
                "models/traffic_best.pt"
            )

            model = YOLO("models/traffic_best.pt")


        file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)

        results = model(img)[0]
        boxes = results.boxes

        count = 0

        if boxes is not None and len(boxes) > 0:

            for box in boxes:
                x1,y1,x2,y2 = map(int, box.xyxy[0])
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,200,0),3)
                count += 1

        st.image(img, channels="BGR", width=500)
      

        # after drawing bounding boxes
        cv2.imwrite("temp.jpg", img)

        image_url = upload_image_to_s3(
        local_path="temp.jpg",
        category="traffic"
        )


        # -------- congestion logic --------
        if count < 10:
            congestion = "low"
        elif count < 25:
            congestion = "medium"
        else:
            congestion = "high"

        #st.success(f"Vehicle Count: {count}")
        st.info(f"Congestion Level: {congestion}")

        # -------- peak hour --------
        h = datetime.now().hour
        is_peak = (8 <= h <= 11) or (17 <= h <= 20)

        # -------- DB LOG --------
        data = (
            datetime.now(),
            city,
            area,
            lat,
            lon,
            count,
            congestion,
            is_peak,
            image_url
        )

        insert_traffic_log(data)

        # -------- EMAIL ALERT (only for high) --------
        if congestion == "high":

            subject = "🚨 UrbanBot Traffic Congestion Alert"

            body = f"""Heavy traffic detected!

                 Time: {datetime.now()}
                 City: {city}
                 Area: {area}
                 Coordinates: {lat}, {lon}

                 Vehicle Count: {count}
                 Congestion Level: {congestion}

                 Traffic intervention recommended."""

            email_result = send_alert_email(subject, body)
            email_ok = (email_result == True)

            insert_system_alert(
                alert_type="traffic",
                location=f"{city}-{area}",
                severity="high",
                message=subject,
                email_sent=email_ok
            )

            if email_ok:
                st.error("🚨 High congestion — Alert email sent")
            else:
                st.warning(f"Email failed: {email_result}")

        st.success("✅ Traffic log stored in database")

        st.info(f"""
        **Logged Metadata**
        - City: {city}
        - Area: {area}
        - Coordinates: ({lat}, {lon})
        - Vehicle Count: {count}
        - Congestion: {congestion}
        - Peak Hour: {is_peak}
        """)

    else:
        st.write("Upload an image and click **Detect Traffic**.")

    st.markdown('</div>', unsafe_allow_html=True)
