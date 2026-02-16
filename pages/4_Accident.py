import streamlit as st
import uuid
import cv2
import numpy as np
from datetime import datetime
from ultralytics import YOLO
from databases.accident_detection_db import insert_accident_log
from utils.email_alert import send_alert_email
from databases.alerts_db import insert_system_alert
from utils.s3_uploader import upload_image_to_s3
from utils.model_loader import ensure_model

st.set_page_config(page_title="Accident Detection", layout="wide")

# ---------- theme ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #fff7ed, #ecfeff);
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

st.markdown('<div class="title">🚨 Accident Detection Dashboard</div>', unsafe_allow_html=True)

# ---------- city coords ----------
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
    st.markdown('<div class="subtitle">📍 Incident Input</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        city = st.selectbox("City", list(CITY_AREA_DATA.keys()))

    with c2:
        area = st.selectbox("Area", list(CITY_AREA_DATA[city].keys()))

    lat, lon = CITY_AREA_DATA[city][area]

    c3, c4 = st.columns(2)

    with c3:
        st.caption("Latitude")
        st.code(lat)

    with c4:
        st.caption("Longitude")
        st.code(lon)

    uploaded = st.file_uploader("Upload Accident Image", type=["jpg","jpeg","png"])
    detect_btn = st.button("🚨 Detect Accident")

    st.markdown('</div>', unsafe_allow_html=True)


# ================= RIGHT =================
with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">🧠 Detection Result</div>', unsafe_allow_html=True)

    if uploaded and detect_btn:

        lat, lon = CITY_AREA_DATA[city][area]

        with st.spinner("Loading model and detecting..."):
            ensure_model("models/accident_best.pt","models/accident_best.pt")

            model = YOLO("models/accident_best.pt")

        file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)

        results = model(img)[0]
        boxes = results.boxes

        confidence_max = 0

         # after drawing bounding boxes
        cv2.imwrite("temp.jpg", img)

        image_url = upload_image_to_s3(
        local_path="temp.jpg",
        category="accident"
        )

        if boxes is not None and len(boxes) > 0:

            for box in boxes:
                x1,y1,x2,y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                confidence_max = max(confidence_max, conf)
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,180,0),3)

            st.image(img, channels="BGR", width=500)

            st.error("⚠️ Accident Detected")
            

         


            # -------- auto severity --------
            if confidence_max >= 0.80:
                severity = "high"
            elif confidence_max >= 0.50:
                severity = "medium"
            else:
                severity = "low"

            #Email alert
            current_time = datetime.now()
            subject = "🚨 UrbanBot Accident Alert"
            body = f"""Accident detected!
            Time:{current_time}
            City: {city}
            Coordinates: {lat}, {lon}
            Severity: {severity}
            Confidence: {round(confidence_max,3)}

            Please take immediate action."""

            
            
            email_result = send_alert_email(subject, body)

            email_ok = (email_result == True)

   

            data = (
                str(uuid.uuid4()),
                datetime.now(),
                image_url,
                city,
                area,
                lat,
                lon,
                severity,
                email_ok
            )

            insert_accident_log(data)


            insert_system_alert(
               alert_type="accident",
               location=city,
               severity=severity,
               message=subject,
               email_sent=email_ok
            )


            if email_result == True:
                 st.error("🚨 Accident detected — Alert email sent")
            else:
                st.warning(f"Email failed: {email_result}")


     

            st.success("✅ Accident stored in database")

            st.info(f"""
            **Logged Metadata**
            - City: {city}
            - Coordinates: ({lat}, {lon})
           
            - Severity: {severity}
            """)

        else:
            st.success("No accident detected")

    else:
        st.write("Upload an image and click **Detect Accident**.")

   


    st.markdown('</div>', unsafe_allow_html=True)
