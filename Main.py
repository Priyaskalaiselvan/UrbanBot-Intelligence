import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="UrbanBot Intelligence",
    page_icon="🏙️",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
/* Balanced soft-dark background */
.stApp {
    background: linear-gradient(135deg, #e0e7ff, #dbeafe, #c7d2fe);
}

/* Container spacing */
.block-container {
    padding-top: 3rem;
    padding-bottom: 2rem;
}

/* Header */
.title {
    font-size: 46px;
    font-weight: 800;
    color: #4338ca;
    text-align: center;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    color: #475569;
    font-size: 18px;
    margin-bottom: 45px;
}

/* Glass cards */
.card {
    background: rgba(255,255,255,0.55);
    backdrop-filter: blur(14px);
    border-radius: 22px;
    padding: 30px;
    text-align: center;
    box-shadow: 0 18px 35px rgba(0,0,0,0.18);
    transition: 0.35s;
}

.card:hover {
    transform: translateY(-10px) scale(1.03);
}

/* Icons */
.icon {
    font-size: 52px;
    margin-bottom: 12px;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(to right, #4f46e5, #22d3ee);
    color: white;
    font-weight: 700;
    border-radius: 30px;
    padding: 10px 25px;
    border: none;
}

.stButton>button:hover {
    background: linear-gradient(to right, #22d3ee, #4f46e5);
}

/* Color accents */
.traffic { border-top: 5px solid #22c55e; }
.accident { border-top: 5px solid #ef4444; }
.infra { border-top: 5px solid #f97316; }
.crowd { border-top: 5px solid #ec4899; }
.aqi { border-top: 5px solid #0ea5e9; }
.complaint { border-top: 5px solid #a855f7; }
.chatbot { border-top: 5px solid #14b8a6; }
.dashboard { border-top: 5px solid #06b6d4; }
           
</style>
""", unsafe_allow_html=True)



# ---------------- HEADER ----------------
st.markdown('<div class="title">UrbanBot Intelligence</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">AI-Powered Smart City Analytics Platform</div>',
    unsafe_allow_html=True
)
if st.button("📘 Project Introduction"):
    st.switch_page("pages/1_Introduction.py")


# ---------------- GRID ----------------
row1 = st.columns(4)
row2 = st.columns(4)

with row1[0]:
    st.markdown('<div class="card traffic">', unsafe_allow_html=True)
    st.markdown('<div class="icon">🚦</div>', unsafe_allow_html=True)
    st.markdown("### Traffic Congestion")
    if st.button("Open", key="traffic"):
        st.switch_page("pages/2_Traffic.py")
    st.markdown('</div>', unsafe_allow_html=True)

with row1[1]:
    st.markdown('<div class="card accident">', unsafe_allow_html=True)
    st.markdown('<div class="icon">🚑</div>', unsafe_allow_html=True)
    st.markdown("### Accident Detection")
    if st.button("Open", key="accident"):
        st.switch_page("pages/4_Accident.py")
    st.markdown('</div>', unsafe_allow_html=True)

with row1[2]:
    st.markdown('<div class="card infra">', unsafe_allow_html=True)
    st.markdown('<div class="icon">🛣</div>', unsafe_allow_html=True)
    st.markdown("### Infrastructure")
    if st.button("Open", key="infra"):
        st.switch_page("pages/5_Road_Damage.py")
    st.markdown('</div>', unsafe_allow_html=True)

with row1[3]:
    st.markdown('<div class="card crowd">', unsafe_allow_html=True)
    st.markdown('<div class="icon">👥</div>', unsafe_allow_html=True)
    st.markdown("### Crowd Detection")
    if st.button("Open", key="crowd"):
        st.switch_page("pages/3_Crowd_Density.py")
    st.markdown('</div>', unsafe_allow_html=True)

with row2[0]:
    st.markdown('<div class="card aqi">', unsafe_allow_html=True)
    st.markdown('<div class="icon">🌫</div>', unsafe_allow_html=True)
    st.markdown("### Air Quality")
    if st.button("Open", key="aqi"):
        st.switch_page("pages/6_Air_Quality.py")
    st.markdown('</div>', unsafe_allow_html=True)

with row2[1]:
    st.markdown('<div class="card complaint">', unsafe_allow_html=True)
    st.markdown('<div class="icon">🗣</div>', unsafe_allow_html=True)
    st.markdown("### Citizen Complaints")
    if st.button("Open", key="complaint"):
        st.switch_page("pages/7_Citizen_Complaints.py")
    st.markdown('</div>', unsafe_allow_html=True)

with row2[2]:
    st.markdown('<div class="card chatbot">', unsafe_allow_html=True)
    st.markdown('<div class="icon">🤖</div>', unsafe_allow_html=True)
    st.markdown("### Admin AI Assistant")
    if st.button("Open", key="chatbot"):
        st.switch_page("pages/8_Chatbot.py")
    st.markdown('</div>', unsafe_allow_html=True)

with row2[3]:
    st.markdown('<div class="card dashboard">', unsafe_allow_html=True)
    st.markdown('<div class="icon">📊</div>', unsafe_allow_html=True)
    st.markdown("### Monitoring Dashboard")
    if st.button("Open", key="monitor"):
        st.switch_page("pages/9_Dashboard.py")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown(
    "<center><small style='color:#e0e7ff;'>UrbanBot Intelligence © 2026</small></center>",
    unsafe_allow_html=True
)


