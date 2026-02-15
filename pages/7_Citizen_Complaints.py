import streamlit as st
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from databases.citizen_complaint_db import insert_complaint, fetch_complaints

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

# ---------- page config ----------
st.set_page_config(page_title="Citizen Complaint AI", layout="wide")


# ---------- custom CSS ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #fff7ed, #ecfeff);
    color: #111827;
}

.card {
    background: #f8fafc;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.10);
    margin-bottom: 15px;
    border: 1px solid #e5e7eb;
}

h1, h2, h3 {
    color: #0284c7;
}

.badge-high {
    color:#dc2626;
    font-weight:bold;
}

.badge-medium {
    color:#d97706;
    font-weight:bold;
}

.badge-low {
    color:#059669;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)




st.title("🗣 Citizen Complaint AI Dashboard")

# ---------- city coordinates ----------
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

dept_map = {
    "road": "Roads Department",
    "water": "Water Board",
    "lighting": "Electricity Board",
    "pollution": "Pollution Control Board",
    "traffic": "Traffic Police"
}

left, right = st.columns([1, 1])

# ================= LEFT : FORM =================
with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📌 Register New Complaint")

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

    

    category = st.selectbox(
        "Category",
        ["road", "water", "lighting", "pollution", "traffic"]
    )

    complaint_text = st.text_area("Complaint Description")

    


    if st.button("🚀 Submit Complaint"):

        if not complaint_text.strip():
            st.warning("Please enter complaint text")
        else:
            polarity = sia.polarity_scores(complaint_text)["compound"]

            if polarity <= -0.5:
                priority = "high"
                st.error("Negative complaint detected → High priority")
            elif polarity < 0.05:
                priority = "medium"
                st.info("Neutral complaint → Medium priority")
            else:
                priority = "low"
                st.success("Positive complaint → Low priority")

            department = dept_map[category]

            insert_complaint(
                city=city,
                area=area,
                category=category,
                text=complaint_text,
                lat=lat,
                lon=lon,
                dept=department,
                priority=priority
            )
            st.success("✅ Complaint stored successfully")
            st.write(f"Assigned Department: **{department}**")
            st.write(f"Priority Level: **{priority.upper()}**")

            
            
            
            

    st.markdown('</div>', unsafe_allow_html=True)

# ================= RIGHT : LIVE LOG =================
with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📡 Live Complaint Logs")

    rows = fetch_complaints()
    rows = list(rows)[:5]


    if not rows:
        st.write("No complaints yet.")
    else:
        for r in rows:
            complaint_id, city,area, category, priority, text, created_at = r

            if priority == "high":
                badge = '<span class="badge-high">🔴 HIGH</span>'
            elif priority == "medium":
                badge = '<span class="badge-medium">🟡 MEDIUM</span>'
            else:
                badge = '<span class="badge-low">🟢 LOW</span>'

            st.markdown(f"""
            <div class="card">
            <b>{category.upper()}</b> | {badge}<br>
            {text}<br>
            <small>{city} • {created_at}</small>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
