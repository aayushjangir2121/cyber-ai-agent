import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import datetime

# ── Load API key ──────────────────────────────────────────────
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Cyber AI Agent — Aayush Jangir",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS + Matrix Rain ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600&family=Syne:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    background-color: #010801 !important;
    color: #c8e6c8 !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* ── MATRIX CANVAS ── */
#matrix-canvas {
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    z-index: 0;
    pointer-events: none;
    opacity: 0.18;
}

/* ── make streamlit content sit above canvas ── */
.stApp > div { position: relative; z-index: 1; }
[data-testid="stAppViewContainer"] { background: transparent !important; }
[data-testid="stHeader"] { background: transparent !important; }
section[data-testid="stSidebar"] { z-index: 999 !important; }

/* ── HEADER ── */
.header-wrap {
    display: flex; align-items: center;
    justify-content: space-between;
    padding: 18px 0 20px 0;
    border-bottom: 1px solid rgba(0,255,70,0.12);
    margin-bottom: 28px;
    backdrop-filter: blur(2px);
}
.header-left { display: flex; align-items: center; gap: 16px; }
.logo-box {
    width: 48px; height: 48px; border-radius: 12px;
    background: linear-gradient(135deg, #00ff44, #00cc88);
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
    box-shadow: 0 0 28px rgba(0,255,70,0.55);
}
.app-title {
    font-family: 'Syne', sans-serif;
    font-size: 21px; font-weight: 800;
    color: #00ff44; letter-spacing: 2px;
    text-shadow: 0 0 20px rgba(0,255,70,0.7), 0 0 40px rgba(0,255,70,0.3);
}
.app-sub {
    font-size: 10px; color: rgba(0,255,70,0.4);
    letter-spacing: 1px; margin-top: 2px;
    font-family: 'JetBrains Mono', monospace;
}
.owner-block { text-align: right; }
.owner-name {
    font-family: 'Syne', sans-serif;
    font-size: 15px; font-weight: 700;
    color: #00ff44;
    text-shadow: 0 0 12px rgba(0,255,70,0.5);
    letter-spacing: 1px;
}
.owner-title {
    font-size: 10px; color: rgba(0,255,70,0.45);
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.8px; margin-top: 3px;
}
.badge-row { display: flex; gap: 7px; margin-top: 8px; justify-content: flex-end; }
.sev-tag {
    padding: 3px 9px; border-radius: 4px;
    font-size: 10px; font-family: 'JetBrains Mono', monospace;
    border: 1px solid rgba(0,255,70,0.12);
    color: rgba(0,255,70,0.35);
}

/* ── WELCOME CARD ── */
.welcome-card {
    background: rgba(0,255,70,0.025);
    border: 1px solid rgba(0,255,70,0.1);
    border-radius: 18px;
    padding: 32px;
    margin: 10px 0 24px 0;
    text-align: center;
    backdrop-filter: blur(8px);
}
.welcome-title {
    font-family: 'Syne', sans-serif;
    font-size: 20px; font-weight: 800;
    color: #00ff44; letter-spacing: 1px;
    margin-bottom: 8px;
    text-shadow: 0 0 16px rgba(0,255,70,0.6);
}
.welcome-sub {
    font-size: 12px; color: rgba(0,255,70,0.5);
    line-height: 2; font-family: 'JetBrains Mono', monospace;
}
.caps-row {
    display: flex; gap: 10px; justify-content: center;
    flex-wrap: wrap; margin-top: 18px;
}
.cap-chip {
    padding: 6px 14px; border-radius: 20px;
    border: 1px solid rgba(0,255,70,0.2);
    background: rgba(0,255,70,0.05);
    color: rgba(0,255,70,0.65);
    font-size: 11px; font-family: 'JetBrains Mono', monospace;
}

/* ── CHAT BUBBLES ── */
.chat-row-user {
    display: flex; justify-content: flex-end;
    align-items: flex-end; gap: 10px;
    margin: 14px 0; animation: fadeUp 0.3s ease-out;
}
.chat-row-bot {
    display: flex; justify-content: flex-start;
    align-items: flex-end; gap: 10px;
    margin: 14px 0; animation: fadeUp 0.3s ease-out;
}
.avatar-bot {
    width: 34px; height: 34px; border-radius: 10px; flex-shrink: 0;
    background: linear-gradient(135deg, #00ff44, #00cc88);
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; box-shadow: 0 0 14px rgba(0,255,70,0.45);
    margin-bottom: 2px;
}
.avatar-user {
    width: 34px; height: 34px; border-radius: 10px; flex-shrink: 0;
    background: rgba(0,255,70,0.1);
    border: 1px solid rgba(0,255,70,0.25);
    display: flex; align-items: center; justify-content: center;
    font-size: 15px; margin-bottom: 2px;
}
.bubble-user {
    max-width: 70%;
    background: linear-gradient(135deg, #00ff44, #00cc66);
    color: #010801;
    padding: 12px 16px;
    border-radius: 18px 18px 4px 18px;
    font-family: 'Syne', sans-serif;
    font-size: 14px; font-weight: 500; line-height: 1.65;
    box-shadow: 0 4px 20px rgba(0,255,70,0.22);
}
.bubble-bot {
    max-width: 75%;
    background: rgba(0,20,0,0.7);
    border: 1px solid rgba(0,255,70,0.13);
    color: #b8e0b8;
    padding: 14px 18px;
    border-radius: 18px 18px 18px 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12.5px; line-height: 1.9;
    box-shadow: 0 2px 16px rgba(0,0,0,0.5);
    white-space: pre-wrap; word-break: break-word;
    backdrop-filter: blur(6px);
}
.msg-meta {
    font-size: 10px; color: rgba(0,255,70,0.25);
    font-family: 'JetBrains Mono', monospace;
    margin-top: 4px; padding: 0 4px; text-align: right;
}
.msg-meta-left {
    font-size: 10px; color: rgba(0,255,70,0.25);
    font-family: 'JetBrains Mono', monospace;
    margin-top: 4px; padding: 0 4px;
}

/* ── INPUT ── */
.stTextArea textarea {
    background: rgba(0,20,0,0.7) !important;
    border: 1px solid rgba(0,255,70,0.18) !important;
    border-radius: 14px !important;
    color: #b8e0b8 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important; line-height: 1.7 !important;
    backdrop-filter: blur(8px) !important;
}
.stTextArea textarea:focus {
    border-color: rgba(0,255,70,0.45) !important;
    box-shadow: 0 0 0 2px rgba(0,255,70,0.08) !important;
}
.stTextArea textarea::placeholder { color: rgba(0,255,70,0.2) !important; }

/* ── BUTTON ── */
.stButton > button {
    background: rgba(0,255,70,0.08) !important;
    border: 1px solid rgba(0,255,70,0.25) !important;
    color: #00ff44 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important; font-weight: 600 !important;
    border-radius: 12px !important; letter-spacing: 1px !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #00ff44, #00cc66) !important;
    color: #010801 !important;
    box-shadow: 0 0 22px rgba(0,255,70,0.45) !important;
    border-color: transparent !important;
}

/* ── FILE UPLOADER ── */
[data-testid="stFileUploader"] {
    border: 1px dashed rgba(0,200,255,0.2) !important;
    border-radius: 12px !important;
    background: rgba(0,10,0,0.5) !important;
    backdrop-filter: blur(6px) !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: rgba(1,8,1,0.97) !important;
    border-right: 1px solid rgba(0,255,70,0.08) !important;
}

/* ── DIVIDER ── */
.chat-divider {
    border: none; border-top: 1px solid rgba(0,255,70,0.07); margin: 8px 0;
}

/* ── FOOTER ── */
.cyber-footer {
    text-align: center; font-size: 10px;
    color: rgba(0,255,70,0.18);
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.8px; margin-top: 8px; padding-bottom: 4px;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(0,255,70,0.18); border-radius: 10px; }
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }
</style>

<!-- ── MATRIX CANVAS ── -->
<canvas id="matrix-canvas"></canvas>
<script>
(function() {
    const canvas = document.getElementById('matrix-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    canvas.width  = window.innerWidth;
    canvas.height = window.innerHeight;
    window.addEventListener('resize', () => {
        canvas.width  = window.innerWidth;
        canvas.height = window.innerHeight;
        columns = Math.floor(canvas.width / fontSize);
        drops = Array(columns).fill(1);
    });

    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()_+[]{}|;:<>?/\\~`アイウエオカキクケコサシスセソタチツテトナニヌネノ';
    const fontSize = 13;
    let columns = Math.floor(canvas.width / fontSize);
    let drops = Array(columns).fill(1);

    function draw() {
        ctx.fillStyle = 'rgba(1, 8, 1, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        for (let i = 0; i < drops.length; i++) {
            const char = chars[Math.floor(Math.random() * chars.length)];
            // Head of stream — bright white-green
            if (drops[i] * fontSize < canvas.height * 0.05 || Math.random() > 0.97) {
                ctx.fillStyle = '#ccffcc';
            } else {
                // Random shade of green
                const g = Math.floor(180 + Math.random() * 75);
                ctx.fillStyle = `rgb(0, ${g}, 30)`;
            }
            ctx.font = fontSize + 'px JetBrains Mono, monospace';
            ctx.fillText(char, i * fontSize, drops[i] * fontSize);

            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }
    }
    setInterval(draw, 45);
})();
</script>
""", unsafe_allow_html=True)

# ── System Prompt ─────────────────────────────────────────────
SYSTEM_PROMPT = """You are Cyber AI Agent — an elite cybersecurity code reviewer and penetration tester, built by Aayush Jangir (Cyber Security Analyst).

When reviewing code, ALWAYS use this exact format:

## 🔍 Vulnerabilities Found
For EACH vulnerability:
- **[SEVERITY] Vulnerability Name** (🔴 CRITICAL / 🟠 HIGH / 🟡 MEDIUM / 🟢 LOW)
- **📍 Location:** Exact line number(s) and the vulnerable code snippet
- **💀 Why Dangerous:** Brief explanation of the risk

## 💥 Exploit Demos
For each vulnerability, provide a real-world PoC:
- Exact payload or attack an attacker would use
- What the impact would be (data leaked, account bypass, RCE, etc.)

## ✅ Fixed Code
Secure version with inline comments explaining each fix.

## 📊 Security Score
X/10 — one line verdict.

RULES:
- Always quote the exact vulnerable line with line number
- Exploit demos are educational — label them clearly
- For general cybersecurity questions, answer as an expert
- Always respond in English only."""

# ── Session state ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ── API key check ─────────────────────────────────────────────
if not GROQ_API_KEY or GROQ_API_KEY == "apni_key_yahan_paste_karo":
    st.markdown("""
    <div style="background:rgba(255,50,50,0.07);border:1px solid rgba(255,50,50,0.35);
    border-radius:14px;padding:20px;margin:30px auto;max-width:520px;text-align:center;">
    <div style="font-size:28px;margin-bottom:10px;">⚠️</div>
    <div style="color:#ff7777;font-family:'Syne',sans-serif;font-size:15px;font-weight:700;margin-bottom:8px;">
    API Key Missing</div>
    <div style="color:rgba(255,120,120,0.75);font-family:'JetBrains Mono',monospace;font-size:12px;line-height:2;">
    .env file mein apni Groq key daalo:<br>
    <span style="background:rgba(0,0,0,0.5);padding:4px 12px;border-radius:6px;
    color:#00ff44;display:inline-block;margin:6px 0;">GROQ_API_KEY=gsk_xxxxxxxx</span><br>
    Phir restart: <span style="color:#00ccff;">streamlit run cybersentinel.py</span>
    </div></div>
    """, unsafe_allow_html=True)
    st.stop()

# ── HEADER ───────────────────────────────────────────────────
st.markdown(f"""
<div class="header-wrap">
  <div class="header-left">
    <div class="logo-box">🛡️</div>
    <div>
      <div class="app-title">CYBER AI AGENT</div>
      <div class="app-sub">● SECURITY CODE REVIEWER — POWERED BY GROQ</div>
    </div>
  </div>
  <div class="owner-block">
    <div class="owner-name">⚡ Aayush Jangir</div>
    <div class="owner-title">CYBER SECURITY ANALYST</div>
    <div class="badge-row">
      <span class="sev-tag">🔴 CRITICAL</span>
      <span class="sev-tag">🟠 HIGH</span>
      <span class="sev-tag">🟡 MED</span>
      <span class="sev-tag">🟢 LOW</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="font-family:'Syne',sans-serif;font-size:14px;font-weight:700;
    color:#00ff44;letter-spacing:1px;padding:8px 0 16px 0;">⚙️ Settings</div>
    """, unsafe_allow_html=True)
    model = st.selectbox("Model", [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768",
        "gemma2-9b-it",
    ], index=0)
    st.markdown("---")
    st.markdown("""
    <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:600;
    color:#00ff44;margin-bottom:10px;">🎯 Detects</div>
    <div style="font-size:11px;color:rgba(0,255,70,0.55);line-height:2.3;
    font-family:'JetBrains Mono',monospace;">
    🔴 SQL Injection<br>🔴 Command Injection<br>
    🟠 XSS<br>🟠 IDOR<br>🟠 Broken Auth<br>
    🟡 CSRF<br>🟡 Hardcoded Secrets<br>🟢 Info Disclosure
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center;padding:8px 0;">
    <div style="font-family:'Syne',sans-serif;font-size:14px;font-weight:700;
    color:#00ff44;text-shadow:0 0 10px rgba(0,255,70,0.5);">Aayush Jangir</div>
    <div style="font-size:10px;color:rgba(0,255,70,0.4);font-family:'JetBrains Mono',monospace;
    margin-top:4px;letter-spacing:1px;">CYBER SECURITY ANALYST</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.rerun()

# ── CHAT AREA ─────────────────────────────────────────────────
with st.container():
    if not st.session_state.messages:
        st.markdown("""
        <div class="welcome-card">
          <div class="welcome-title">🛡️ Cyber AI Agent Online</div>
          <div class="welcome-sub">
            Paste your code or upload a source file.<br>
            I'll find every vulnerability — with exact location & exploit demo.
          </div>
          <div class="caps-row">
            <span class="cap-chip">📍 Exact Line Numbers</span>
            <span class="cap-chip">💥 Exploit PoC</span>
            <span class="cap-chip">✅ Fixed Code</span>
            <span class="cap-chip">📊 Security Score</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.messages:
            time_str = msg.get("time", "")
            content  = msg["content"].replace("<", "&lt;").replace(">", "&gt;")
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="chat-row-user">
                  <div>
                    <div class="bubble-user">{content}</div>
                    <div class="msg-meta">{time_str} &nbsp; You</div>
                  </div>
                  <div class="avatar-user">👤</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-row-bot">
                  <div class="avatar-bot">🛡️</div>
                  <div>
                    <div class="bubble-bot">{content}</div>
                    <div class="msg-meta-left">Cyber AI Agent &nbsp;·&nbsp; {time_str}</div>
                  </div>
                </div>""", unsafe_allow_html=True)

# ── FILE UPLOAD ───────────────────────────────────────────────
st.markdown("<hr class='chat-divider'>", unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "📁 Upload source file for full scan",
    type=["py","js","ts","php","java","c","cpp","cs","go","rb","html","sql","sh","txt","json","xml","yaml","yml","env"],
    label_visibility="visible",
)

# ── INPUT ROW ─────────────────────────────────────────────────
col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_area(
        "input", placeholder="Paste code or ask a security question...",
        height=110, label_visibility="collapsed",
    )
with col2:
    st.markdown("<div style='height:36px'></div>", unsafe_allow_html=True)
    send = st.button("▶ SCAN", use_container_width=True)

st.markdown("""
<div class="cyber-footer">
  OWASP TOP 10 &nbsp;•&nbsp; CVE DETECTION &nbsp;•&nbsp; EXPLOIT PoC &nbsp;•&nbsp; SECURE CODE GEN
  &nbsp;&nbsp;|&nbsp;&nbsp; Built by
  <span style="color:rgba(0,255,70,0.45);font-family:'Syne',sans-serif;font-weight:600;">
  Aayush Jangir</span>
  <span style="color:rgba(0,255,70,0.25);"> — Cyber Security Analyst</span>
</div>
""", unsafe_allow_html=True)

# ── HANDLE SEND ───────────────────────────────────────────────
prompt       = None
current_time = datetime.datetime.now().strftime("%H:%M")

if send:
    if uploaded_file:
        try:
            file_content = uploaded_file.read().decode("utf-8", errors="ignore")
            prompt = f"Please perform a full security audit of this file: {uploaded_file.name}\n\n```\n{file_content}\n```"
        except Exception as e:
            st.error(f"Could not read file: {e}")
    elif user_input.strip():
        prompt = user_input.strip()
    else:
        st.warning("Please enter some code or a question first!")

if prompt:
    st.session_state.messages.append({"role": "user",  "content": prompt,  "time": current_time})
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    with st.spinner("🔍 Scanning for vulnerabilities..."):
        try:
            client   = Groq(api_key=GROQ_API_KEY)
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.chat_history,
                temperature=0.2,
                max_tokens=2048,
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = f"⚠️ Error: {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": reply, "time": current_time})
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.rerun()
