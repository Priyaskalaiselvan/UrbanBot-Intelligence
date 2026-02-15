import streamlit as st
import torch
import cv2
import numpy as np
import torchvision.transforms as T
from datetime import datetime
import uuid
from utils.email_alert import send_alert_email
from databases.alerts_db import insert_system_alert

from databases.crowd_density_db import insert_crowd_log
from utils.s3_uploader import upload_image_to_s3

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Crowd Density", layout="wide")

# ---------------- THEME ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #eef2ff, #ecfdf5);
}
.card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.10);
    margin-bottom: 20px;
}
.title {
    font-size: 32px;
    font-weight: 800;
    color: #0f172a;
}
.subtitle {
    font-size: 18px;
    color: #334155;
    margin-bottom: 10px;
}
.bigcount {
    font-size: 48px;
    font-weight: 800;
    color: #2563eb;
}
.level-low {color:#16a34a;font-weight:700;}
.level-medium {color:#f59e0b;font-weight:700;}
.level-high {color:#ef4444;font-weight:700;}
.level-extreme {color:#7c3aed;font-weight:700;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">👥 Crowd Density Dashboard</div>', unsafe_allow_html=True)

# ---------------- MODEL ----------------
import torch.nn as nn
from torchvision import models

class CrowdNet(nn.Module):
    def __init__(self):
        super().__init__()
        vgg = models.vgg16(weights=None)
        self.frontend = nn.Sequential(*list(vgg.features.children())[:23])
        self.backend = nn.Sequential(
            nn.Conv2d(512,512,3,padding=2,dilation=2), nn.ReLU(),
            nn.Conv2d(512,256,3,padding=2,dilation=2), nn.ReLU(),
            nn.Conv2d(256,128,3,padding=2,dilation=2), nn.ReLU(),
            nn.Conv2d(128,64,3,padding=2,dilation=2), nn.ReLU(),
        )
        self.output_layer = nn.Conv2d(64,1,1)

    def forward(self,x):
        return self.output_layer(self.backend(self.frontend(x)))

@st.cache_resource
def load_model():
    m = CrowdNet()
    m.load_state_dict(torch.load("models/crowd_density_cc50_v1.pth", map_location="cpu"))
    m.eval()
    return m

model = load_model()
transform = T.ToTensor()

# ---------------- CITY COORDS ----------------
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

# ---------------- DENSITY LEVEL ----------------
def density_level(count):
    if count < 50: return "Low"
    elif count < 150: return "Medium"
    elif count < 300: return "High"
    else: return "Extreme"

def crowd_severity(level):
    if level == "Low": return "low"
    if level == "Medium": return "low"
    if level == "High": return "medium"
    return "high"


def level_class(level):
    return {
        "Low":"level-low",
        "Medium":"level-medium",
        "High":"level-high",
        "Extreme":"level-extreme"
    }[level]

# ---------------- PREDICT ----------------
def predict(img):
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h,w = rgb.shape[:2]
    rgb = cv2.resize(rgb,(w-w%8,h-h%8))
    x = transform(rgb).unsqueeze(0)
    with torch.no_grad():
        dmap = model(x).squeeze().numpy()
    return dmap.sum(), dmap

# ---------------- LAYOUT ----------------
left, right = st.columns([1,1])

# ========= LEFT PANEL =========
with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">📍 Crowd Input</div>', unsafe_allow_html=True)

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

    uploaded = st.file_uploader("Upload Crowd Image", type=["jpg","jpeg","png"])
    detect_btn = st.button("👥 Estimate Crowd")

    st.markdown('</div>', unsafe_allow_html=True)


# ========= RIGHT PANEL =========
with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">📊 Crowd Analysis Result</div>', unsafe_allow_html=True)

    if uploaded and detect_btn:

        lat, lon = CITY_AREA_DATA[city][area]

        file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)

        with st.spinner("Analyzing crowd density..."):
            count, dmap = predict(img)

        level = density_level(count)

        st.image(img, channels="BGR", width=500)
        # after drawing bounding boxes
        cv2.imwrite("temp.jpg", img)

        image_url = upload_image_to_s3(
        local_path="temp.jpg",
        category="crowd"
        )

        

        st.markdown(
            f'<div class="{level_class(level)}">Density Level: {level}</div>',
            unsafe_allow_html=True
        )

        # -------- DB SAVE --------
        data = (
          datetime.now(),
          city,
          area,
          lat,
          lon,
          int(count),
          level,
          image_url
        )

        try:
            insert_crowd_log(data)
            st.success("✅ Crowd log stored in database")
        except Exception as e:
            st.error(f"DB Save Failed: {e}")

        # ---------------- EMAIL ALERT ----------------
        if level == "Extreme":
            current_time = datetime.now()

            subject = "🚨 UrbanBot Crowd Density Alert"

            body = f"""Severe crowd density detected!

            Time: {current_time}
            City: {city}
            Coordinates: {lat}, {lon}

            Predicted Crowd Count: {int(count)}
            Density Level: {level}

            Immediate monitoring recommended."""

            email_result = send_alert_email(subject, body)

            email_ok = (email_result == True)

            insert_system_alert(
               alert_type="crowd",
               location=f"{city}-{area}",
               severity=crowd_severity(level),
               message=subject,
               email_sent=email_ok
            )


            if email_result == True:
                st.error("🚨 Severe crowd detected — Alert email sent")
            else:
                st.warning(f"Email failed: {email_result}")


        st.info(f"""
        **Logged Metadata**
        - City: {city}
        - Coordinates: ({lat}, {lon})
        - Crowd Count: {int(count)}
        - Density Level: {level}
        """)

    else:
        st.write("Upload an image and click **Estimate Crowd**.")

    st.markdown('</div>', unsafe_allow_html=True)
