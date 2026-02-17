import streamlit as st
import mysql.connector
from langchain_groq import ChatGroq
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from decimal import Decimal
import os
# ---------------- PAGE ----------------
st.set_page_config(layout="wide", page_title="UrbanBot AI")

# ---------------- STYLE ----------------
st.markdown("""
<style>

.chat-header {
    font-size: 30px;
    font-weight: 900;
    color: #2563eb;
}

.chat-sub {
    color:#64748b;
    margin-bottom:12px;
}

/* column boxes */
.panel-box {
    border:2px solid #e5e7eb;
    border-radius:16px;
    padding:14px;
    background:white;
    box-shadow:0 6px 18px rgba(0,0,0,0.06);
    height:78vh;
    overflow:auto;
}

/* chat bubbles */
.msg-row { display:flex; margin:8px 0; }

.msg-user {
    margin-left:auto;
    background:#2563eb;
    color:white;
    padding:10px 14px;
    border-radius:14px 14px 4px 14px;
    max-width:75%;
}

.msg-bot {
    margin-right:auto;
    background:#f1f5f9;
    padding:10px 14px;
    border-radius:14px 14px 14px 4px;
    max-width:75%;
}

/* badges */
.agent-badge {
    font-size:11px;
    font-weight:700;
    padding:3px 8px;
    border-radius:999px;
    display:inline-block;
    margin-bottom:6px;
}

.badge-db { background:#dcfce7; color:#166534; }
.badge-report { background:#dbeafe; color:#1e40af; }
.badge-email { background:#fef3c7; color:#92400e; }
.badge-llm { background:#ede9fe; color:#5b21b6; }

/* right info box */
.info-box {
 background:linear-gradient(135deg,#e0f2ff,#f3e8ff);
 border-radius:14px;
 padding:14px;
 border:2px solid #d0d7ff;
}
            [data-testid="column"] > div {
    border:2px solid #e5e7eb;
    border-radius:16px;
    padding:14px;
    background:white;
    box-shadow:0 6px 18px rgba(0,0,0,0.06);
}


</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="chat-header">🤖 UrbanBot AI Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="chat-sub">Multi-Agent City Intelligence Assistant</div>', unsafe_allow_html=True)

# ---------------- LLM ----------------
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

# ---------------- DB ----------------
def sql(query, params=None):
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        port=3306
    )

    cur = conn.cursor()
    cur.execute(query, params or ())

    rows = cur.fetchall()
    cols = [c[0] for c in cur.description] if cur.description else []

    conn.close()
    return rows, cols


# ---------------- EMAIL ----------------
def send_email_tool(subject, body):
    msg = MIMEMultipart()
    msg["From"] = os.getenv("EMAIL_SENDER")
    msg["To"] = os.getenv("EMAIL_RECEIVER")
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))
        s.send_message(msg)

def email_agent(report_text, user_request):
    subject = "UrbanBot Report"
    send_email_tool(subject, report_text)
    return "📧 Email agent sent the report."

# ---------------- SCHEMA AUTO ----------------
@st.cache_data
def get_tables():
    rows, _ = sql("SHOW TABLES")
    return [r[0] for r in rows]


@st.cache_data
def get_columns(t):
    rows, _ = sql(f"SHOW COLUMNS FROM {t}")
    return [r[0] for r in rows]


@st.cache_data
def build_schema():
    return {t: get_columns(t) for t in get_tables()}

def clean_sql(s):
    p = s.lower().find("select")
    if p == -1: return None
    s = s[p:]
    if any(b in s.lower() for b in ["drop","delete","update","insert"]):
        return None
    return s


@st.cache_data

def build_schema_text():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        port=3306
    )

    cur = conn.cursor()

    cur.execute("SHOW TABLES")
    tables = [t[0] for t in cur.fetchall()]

    lines = []

    for t in tables:
        cur.execute(f"SHOW COLUMNS FROM {t}")
        cols = [c[0] for c in cur.fetchall()]
        lines.append(f"{t}: {', '.join(cols)}")

    conn.close()
    return "\n".join(lines)  

# ==============================
# SQL SAFETY FILTER
# ==============================

def clean_sql(s):
    s_low = s.lower()
    p = s_low.find("select")
    if p == -1:
        return None

    s = s[p:]

    banned = ["delete", "update", "drop", "insert", "alter"]
    if any(b in s.lower() for b in banned):
        return None

    if "limit" not in s.lower():
        s += " LIMIT 100"

    return s

# ==============================
# VALUE FORMATTER
# ==============================

def safe_val(x):
    if isinstance(x, Decimal):
        x = float(x)
    if isinstance(x, float):
        return round(x, 2)
    return x


# ==============================
# RESULT FORMATTER
# ==============================

def format_result(rows, cols, title):

    if not rows:
        return "No records found."

    # single scalar
    if len(rows) == 1 and len(rows[0]) == 1:
        return f"**Total:** {rows[0][0]}"

    lines = []

    for row in rows:
        vals = [safe_val(v) for v in row]

        label = str(vals[0])

        metrics = []
        for c, v in zip(cols[1:], vals[1:]):
            nice = c.replace("_", " ")
            metrics.append(f"{nice} {v}")

        line = ", ".join(metrics)
        lines.append(f"- {label}: {line}")

    block = "\n".join(lines)

    return f"""
### {title}

{block}
"""


# ==============================
# TITLE DETECTOR
# ==============================

def detect_title(question):

    q = question.lower()

    if "accident" in q:
        return "🚨 Accident Insight"
    if "traffic" in q:
        return "🚗 Traffic Insight"
    if "aqi" in q:
        return "🌫 AQI Insight"
    if "crowd" in q:
        return "👥 Crowd Insight"
    if "complaint" in q:
        return "📣 Complaint Insight"
    if "alert" in q:
        return "📬 Alert Insight"
    if "damage" in q:
        return "🛣 Road Damage Insight"

    return "📊 Data Insight"

# ==============================
# DATABASE AGENT (FINAL)
# ==============================

def database_agent(question):

    schema_text = build_schema_text()

    prompt = f"""
    You are an Urban City Database Agent.

    Use ONLY this MySQL schema:

    {schema_text}

    Rules:
    - SELECT queries only
    - Every table has a column named timestamp
    - Use timestamp for date filtering
    - Prefer grouped insights instead of single COUNT
    - Use GROUP BY city or category when useful
    - LIMIT 100
    - Return ONLY SQL

    Date rules:
    today → DATE(timestamp)=CURDATE()
    yesterday → DATE(timestamp)=CURDATE()-INTERVAL 1 DAY
    last week → timestamp >= CURDATE()-INTERVAL 7 DAY

    Question:
    {question}
    """

    raw_sql = llm.invoke(prompt).content.strip()
    query = clean_sql(raw_sql)

    if not query:
        return "⚠️ Unsafe query blocked.", raw_sql, None

    try:
        rows, cols = sql(query)
    except Exception as e:
        return f"DB error: {e}", query, None

    title = detect_title(question)
    answer = format_result(rows, cols, title)

    return answer, query, rows
# ---------------- REPORTS ----------------
def accident_summary():

    r,_ = sql("SELECT COUNT(*) FROM accident_logs")
    total = r[0][0]

    rows,_ = sql("""
        SELECT severity, COUNT(*)
        FROM accident_logs
        GROUP BY severity
    """)

    return total, rows


def traffic_summary():

    r,_ = sql("SELECT COUNT(*) FROM traffic_logs")
    total = r[0][0]

    rows,_ = sql("""
        SELECT congestion_level, COUNT(*)
        FROM traffic_logs
        GROUP BY congestion_level
    """)

    return total, rows

def complaint_summary():

    r,_ = sql("SELECT COUNT(*) FROM citizen_complaints")
    total = r[0][0]

    rows,_ = sql("""
        SELECT category, COUNT(*)
        FROM citizen_complaints
        GROUP BY category
    """)

    return total, rows


def crowd_summary():

    r,_ = sql("SELECT COUNT(*) FROM crowd_density_logs")
    total = r[0][0]

    rows,_ = sql("""
        SELECT density_level, COUNT(*)
        FROM crowd_density_logs
        GROUP BY density_level
    """)

    return total, rows


def aqi_summary():

    r,_ = sql("SELECT COUNT(*) FROM aqi_logs")
    total = r[0][0]

    rows,_ = sql("""
        SELECT aqi_category, COUNT(*)
        FROM aqi_logs
        GROUP BY aqi_category
    """)

    return total, rows


def alerts_summary():

    r,_ = sql("SELECT COUNT(*) FROM system_alerts")
    total = r[0][0]

    rows,_ = sql("""
        SELECT alert_type, COUNT(*)
        FROM system_alerts
        GROUP BY alert_type
    """)

    return total, rows



# ---------------- BADGE ----------------
def badge(tag):
    m = {
        "db":"badge-db",
        "report":"badge-report",
        "email":"badge-email",
        "llm":"badge-llm"
    }
    return f'<span class="agent-badge {m.get(tag,"badge-llm")}">{tag.upper()} AGENT</span>'

# ---------------- CHAT STATE ----------------
if "chat" not in st.session_state:
    st.session_state.chat = [{
        "role":"assistant",
        "text":"Hello 👋 I’m UrbanBot AI. Ask me reports or insights.",
        "agent":"llm"
    }]
    # upgrade old chat records
for m in st.session_state.chat:
    if "agent" not in m and m["role"] == "assistant":
        m["agent"] = "llm"


# ---------------- LAYOUT ----------------
left, right = st.columns([2,1])

# ===== RIGHT PANEL =====
with right:
  

    st.markdown("""
    <div class="info-box">
    🟢 Database Connected<br>
    ⚡ Agents Active<br><br>
    Ask about:<br>
    🚗 Traffic<br>
    🚨 Accidents<br>
    📣 Complaints<br>
    👥 Crowd<br>
    🌫 AQI<br>
    📬 Alerts
    </div>
    """, unsafe_allow_html=True)

    if st.button("🧹 Clear Chat"):
        st.session_state.chat = st.session_state.chat[:1]
        st.rerun()

    

# ===== LEFT CHAT PANEL =====
with left:
    

    for m in st.session_state.chat:
        if m["role"] == "user":
            st.markdown(f'<div class="msg-row"><div class="msg-user">{m["text"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="msg-row"><div class="msg-bot">{badge(m.get("agent","llm"))}<br>{m["text"]}</div></div>',unsafe_allow_html=True)

   

# ---------------- INPUT ----------------
user = st.chat_input("Ask UrbanBot…")

if user:

    st.session_state.chat.append({"role":"user","text":user})
    u = user.lower()

    agent = "llm"

    if "send" in u and "email" in u:
        last = next((m["text"] for m in reversed(st.session_state.chat) if m["role"]=="assistant"), None)
        reply = email_agent(last,user) if last else "No report yet."
        agent="email"

    elif "accident" in u and "report" in u:
        t, s = accident_summary()

        lines = "\n".join([f"- {a}: {b}" for a,b in s])

        reply = f"""
### 🚨 Accident Report

**Total:** {t}

**Category Breakdown:**

{lines}
"""
        agent = "report"


    elif "traffic" in u and "report" in u:
        t, s = traffic_summary()

        lines = "\n".join([f"- {a}: {b}" for a,b in s])

        reply = f"""
### 🚗 Traffic Report

**Total:** {t}

**Category Breakdown:**

{lines}
"""
        agent = "report"


    elif "complaint" in u and "report" in u:
        t, s = complaint_summary()

        lines = "\n".join([f"- {a}: {b}" for a,b in s])

        reply = f"""
### 📣 Complaint Report

**Total:** {t}

**Category Breakdown:**

{lines}
"""
        agent = "report"


    elif "crowd" in u and "report" in u:
        t, s = crowd_summary()
        lines = "\n".join([f"- {a}: {b}" for a,b in s])

        reply = f"""
### 👥 Crowd Density Report

**Total Records:** {t}

**Density Breakdown:**

{lines}
"""
        agent = "report"

    elif "aqi" in u and "report" in u:
        t, s = aqi_summary()
        lines = "\n".join([f"- {a}: {b}" for a,b in s])

        reply = f"""
### 🌫 AQI Report

**Total Records:** {t}

**AQI Status Breakdown:**

{lines}
"""
        agent = "report"

    elif "alert" in u and "report" in u:
        t, s = alerts_summary()
        lines = "\n".join([f"- {a}: {b}" for a,b in s])

        reply = f"""
### 📬 Alerts Report

**Total Alerts:** {t}

**Alert Type Breakdown:**

{lines}
"""
        agent = "report"


    elif any(k in u for k in ["how many","count","today","yesterday","week"]):
        reply, sql_used, rows = database_agent(user)
        agent = "db"


    else:
        reply = llm.invoke(user).content

    st.session_state.chat.append({"role":"assistant","text":reply,"agent":agent})
    st.rerun()

# ---------------- SIDEBAR ----------------
st.sidebar.success("UrbanBot AI Online")
