import streamlit as st
import uuid
import cv2
import numpy as np
from datetime import datetime
from ultralytics import YOLO
from databases.road_damage_db import insert_road_damage
from utils.s3_uploader import upload_image_to_s3
from utils.model_loader import ensure_model

st.set_page_config(page_title="Road Damage Detection", layout="wide")

# ---------- balanced colourful theme ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #e0f2fe, #f0fdfa);
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

st.markdown('<div class="title">🛣 Road Damage Detection Dashboard</div>', unsafe_allow_html=True)

# ---------- load YOLO once ----------
@st.cache_resource
def load_model():
    ensure_model(
        "models/road_damage_yolo.pt",
        "models/road_damage_yolo.pt"
    )
    return YOLO("models/road_damage_yolo.pt")

model = load_model()

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

left, right = st.columns([1, 1])

# ================= LEFT PANEL =================
with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">📍 Capture Details</div>', unsafe_allow_html=True)

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


    camera_source = st.selectbox("Camera Source", ["Cam1", "Cam2", "Cam3","Cam4"])
    weather = st.selectbox("Weather", ["Sunny", "Cloudy", "Rainy", "Night"])
    road_type = st.selectbox("Road Type", ["Highway", "Urban"])

    uploaded = st.file_uploader("Upload Road Image", type=["jpg", "jpeg", "png"])

    detect_btn = st.button("🔍 Detect Road Damage")
    st.markdown('</div>', unsafe_allow_html=True)

# ================= RIGHT PANEL =================
with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">🧠 Detection Result</div>', unsafe_allow_html=True)

    if uploaded and detect_btn:
        file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)

        results = model(img)[0]
        annotated_img = results.plot()

        st.image(annotated_img, caption="Annotated Detection", channels="BGR",  width="stretch")

        detected_classes = [model.names[int(c)] for c in results.boxes.cls]

        damage_classes = {"pothole", "manhole", "crack"}
        found_damage = [c for c in detected_classes if c in damage_classes]

        if found_damage:
            st.error(f"⚠️ Detected: {', '.join(set(found_damage))}")

            image_id = str(uuid.uuid4())
            cv2.imwrite("temp.jpg", annotated_img)

            image_url = upload_image_to_s3(
            local_path="temp.jpg",
            category="road_damage"
            )

            
            timestamp = datetime.now()
            resolution = f"{img.shape[1]}x{img.shape[0]}"

            data = (
                image_id,
                image_url,
                timestamp,
                city,
                area,
                lat,
                lon,
                camera_source,
                weather,
                road_type,
                resolution,
                True
            )

            insert_road_damage(data)
            st.success("✅ Incident stored in database")

            st.info(f"""
            **Logged Metadata**
            - City: {city}
            - Source: {camera_source}
            - Weather: {weather}
            - Road Type: {road_type}
            - Resolution: {resolution}
            """)

        else:
            st.success("No pothole, manhole or crack detected")

    else:
        st.write("Upload an image and click **Detect Road Damage**.")

    st.markdown('</div>', unsafe_allow_html=True)
