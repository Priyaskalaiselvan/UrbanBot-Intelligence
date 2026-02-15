import streamlit as st

st.set_page_config(page_title="About Me", layout="wide")

# ---------- style ----------
st.markdown("""
<style>
.card {
    background: #f8fafc;
    padding: 22px;
    border-radius: 16px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.10);
    margin-bottom: 18px;
    border: 1px solid #e5e7eb;
}
h1, h2, h3 {
    color: #0284c7;
}
</style>
""", unsafe_allow_html=True)

# ---------- Title ----------
st.title("👩‍💻 About Me")

# ---------- Profile ----------
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown("## Priya — Data Scientist")

st.write("""
I am a motivated and continuously learning Data Science professional with a strong foundation in Information Technology.  
I completed my **B.Tech in Information Technology** from **Veltech Multitech College**.

With a long-standing interest in coding and analytical problem solving, I further strengthened my technical expertise through a structured **Data Science program at HCL GUVI**.

I enjoy working on practical data-driven solutions and continuously upgrading my technical and analytical skills.
""")

st.markdown('</div>', unsafe_allow_html=True)

# ---------- Skills ----------
st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("🧠 Core Skills")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
**Programming**
- Python
- SQL


""")

with c2:
    st.markdown("""
**Data Science**
- Machine Learning
- Data Analysis
- Problem Solving


""")

with c3:
    st.markdown("""
**Tools**
- Streamlit
- Pandas & NumPy
- Jupyter / Colab
""")

st.markdown('</div>', unsafe_allow_html=True)

# ---------- Projects ----------
# ---------- Projects ----------
st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("📂 Academic & Course Projects")

projects = [
    ("UrbanBot — Smart City AI Dashboard",
     "Integrated AI dashboard with forecasting, monitoring, and citizen analytics modules."),

    ("Police Secure Check — Traffic Stop Analytics Dashboard",
     "Data-driven dashboard analyzing violations, demographics, and arrest trends."),

    ("Agricultural Data Analysis & Visualization",
     "Exploratory analysis of crop production and yield trends across India."),

    ("Employee Attrition Prediction",
     "ML model to identify employees at risk of leaving organizations."),

    ("Multiple Disease Prediction System",
     "Predicts Kidney, Liver, and Parkinson diseases using ML models."),

    ("Smart Conversational Partner — Sentiment Analysis",
     "NLP-based system to classify sentiment from user text.")
]

for title, desc in projects:
    st.markdown(f"**{title}**")
    st.caption(desc)

st.markdown('</div>', unsafe_allow_html=True)


# ---------- Learning Focus ----------
st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("📚 Professional Focus")

st.write("""
I chose the IT field driven by my strong interest in coding and technology.  
I actively focus on continuous learning, hands-on experimentation, and applying modern data science techniques to real-world problems.

I am committed to growing as a data professional through practical projects and ongoing skill development.
""")

st.markdown('</div>', unsafe_allow_html=True)

# ---------- Career Direction ----------
st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("🎯 Career Direction")

st.write("""
Seeking opportunities in **Data Science and Analytics** where I can contribute analytical skills, continue learning, and build impactful data-driven solutions.
""")

st.markdown('</div>', unsafe_allow_html=True)
