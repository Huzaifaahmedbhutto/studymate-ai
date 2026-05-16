import streamlit as st
import requests
import json
import time
import re
import random

st.set_page_config(
    page_title="StudyMate AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: #060918 !important;
    color: #e8eaf6 !important;
    font-family: 'Inter', sans-serif !important;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0d1030; }
::-webkit-scrollbar-thumb { background: linear-gradient(#6c63ff, #48cae4); border-radius: 10px; }

.main .block-container { padding: 1.5rem 2rem !important; max-width: 1300px; }

/* ── HERO ── */
.hero {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    border: 1px solid rgba(108,99,255,0.3);
    border-radius: 24px;
    padding: 3rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
    text-align: center;
}
.hero::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at 20% 50%, rgba(108,99,255,0.2) 0%, transparent 60%),
                radial-gradient(ellipse at 80% 50%, rgba(72,202,228,0.2) 0%, transparent 60%);
    pointer-events: none;
}
.hero-badge {
    display: inline-block;
    background: rgba(108,99,255,0.2);
    border: 1px solid rgba(108,99,255,0.4);
    border-radius: 20px;
    padding: 0.3rem 1rem;
    font-size: 0.78rem;
    font-weight: 600;
    color: #a89cff;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.hero-title {
    font-size: 3rem;
    font-weight: 900;
    background: linear-gradient(135deg, #fff 0%, #a89cff 40%, #48cae4 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1.5px;
    line-height: 1.1;
    margin-bottom: 0.8rem;
}
.hero-sub {
    font-size: 1.05rem;
    color: #8892b0;
    font-weight: 400;
    max-width: 500px;
    margin: 0 auto 1.5rem;
    line-height: 1.6;
}
.hero-stats {
    display: flex;
    justify-content: center;
    gap: 2rem;
    flex-wrap: wrap;
}
.hero-stat {
    text-align: center;
}
.hero-stat-num {
    font-size: 1.4rem;
    font-weight: 800;
    color: #6c63ff;
}
.hero-stat-label {
    font-size: 0.75rem;
    color: #8892b0;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* ── FEATURE CARDS (mode buttons) ── */
.mode-card-active {
    background: linear-gradient(135deg, #6c63ff, #48cae4) !important;
    color: white !important;
    border: none !important;
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 30px rgba(108,99,255,0.4) !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #6c63ff, #48cae4) !important;
    color: #fff !important; border: none !important;
    border-radius: 12px !important; padding: 0.7rem 1rem !important;
    font-size: 0.85rem !important; font-weight: 700 !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.3s ease !important;
    white-space: nowrap !important; width: 100% !important;
    letter-spacing: 0.3px !important;
}
.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 30px rgba(108,99,255,0.5) !important;
    filter: brightness(1.1) !important;
}
.stButton > button:active { transform: translateY(-1px) !important; }

.stDownloadButton > button {
    background: transparent !important;
    border: 2px solid rgba(108,99,255,0.5) !important;
    color: #a89cff !important; border-radius: 12px !important;
    font-weight: 600 !important; transition: all 0.3s !important;
}
.stDownloadButton > button:hover {
    background: rgba(108,99,255,0.15) !important;
    border-color: #6c63ff !important;
}

/* ── INPUTS ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div,
.stNumberInput > div > div > input {
    background: #0d1030 !important;
    border: 1.5px solid rgba(108,99,255,0.2) !important;
    border-radius: 12px !important; color: #e8eaf6 !important;
    font-family: 'Inter', sans-serif !important; font-size: 0.95rem !important;
    transition: all 0.2s !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #6c63ff !important;
    box-shadow: 0 0 0 4px rgba(108,99,255,0.15) !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label,
.stSlider label, .stRadio label, .stNumberInput label, .stFileUploader label {
    color: #a89cff !important; font-weight: 600 !important; font-size: 0.85rem !important;
    text-transform: uppercase !important; letter-spacing: 0.5px !important;
}

/* ── CARDS ── */
.glass-card {
    background: rgba(13,16,48,0.8);
    border: 1px solid rgba(108,99,255,0.2);
    border-radius: 20px; padding: 2rem; margin-bottom: 1.5rem;
    backdrop-filter: blur(10px);
}
.section-title {
    font-size: 1.4rem; font-weight: 800;
    background: linear-gradient(135deg, #fff, #a89cff);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin-bottom: 1.5rem;
    display: flex; align-items: center; gap: 0.5rem;
}

/* ── RESULT BOX ── */
.result-box {
    background: linear-gradient(135deg, #0d1030, #0a0d2e);
    border: 1px solid rgba(108,99,255,0.3);
    border-left: 5px solid #6c63ff;
    border-radius: 16px; padding: 2rem; margin-top: 1.5rem;
    line-height: 1.9; color: #c8cde8; font-size: 0.96rem;
    box-shadow: 0 20px 60px rgba(108,99,255,0.1);
}

/* ── CHAT ── */
.chat-container { display: flex; flex-direction: column; gap: 1.2rem; padding: 1rem 0; }
.msg-user-wrap { display: flex; justify-content: flex-end; align-items: flex-end; gap: 0.5rem; }
.msg-ai-wrap   { display: flex; justify-content: flex-start; align-items: flex-end; gap: 0.5rem; }
.msg-avatar-user {
    width: 32px; height: 32px; border-radius: 50%;
    background: linear-gradient(135deg, #6c63ff, #48cae4);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.9rem; flex-shrink: 0;
}
.msg-avatar-ai {
    width: 32px; height: 32px; border-radius: 50%;
    background: linear-gradient(135deg, #302b63, #0f0c29);
    border: 1px solid rgba(108,99,255,0.4);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.9rem; flex-shrink: 0;
}
.msg-bubble-user {
    background: linear-gradient(135deg, #6c63ff, #5a52e0);
    border-radius: 20px 20px 6px 20px;
    padding: 0.9rem 1.3rem; max-width: 72%;
    color: #fff; font-size: 0.93rem; line-height: 1.6;
    box-shadow: 0 8px 25px rgba(108,99,255,0.3);
}
.msg-bubble-ai {
    background: #0d1030; border: 1px solid rgba(108,99,255,0.2);
    border-radius: 20px 20px 20px 6px;
    padding: 0.9rem 1.3rem; max-width: 78%;
    color: #c8cde8; font-size: 0.93rem; line-height: 1.7;
    box-shadow: 0 8px 25px rgba(0,0,0,0.3);
}
.msg-time { font-size: 0.68rem; color: #4a5080; margin-top: 0.2rem; }

/* ── QUIZ ── */
.quiz-card {
    background: #0d1030; border: 1px solid rgba(108,99,255,0.2);
    border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem;
    transition: border-color 0.2s;
}
.quiz-card:hover { border-color: rgba(108,99,255,0.5); }
.quiz-num { font-size: 0.7rem; color: #6c63ff; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; }
.quiz-q   { font-size: 1.05rem; font-weight: 700; color: #e8eaf6; margin: 0.5rem 0 1rem; }

/* ── SCORE ── */
.score-box {
    background: linear-gradient(135deg, #0f0c29, #302b63);
    border: 2px solid #6c63ff; border-radius: 20px;
    padding: 2rem; text-align: center; margin: 1.5rem 0;
    box-shadow: 0 20px 60px rgba(108,99,255,0.3);
}
.score-emoji { font-size: 3rem; margin-bottom: 0.5rem; }
.score-num   { font-size: 2.5rem; font-weight: 900; color: #fff; }
.score-pct   { font-size: 1.1rem; color: #a89cff; font-weight: 600; }
.score-grade { font-size: 0.9rem; color: #48cae4; margin-top: 0.3rem; }

/* ── PROGRESS ── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #6c63ff, #48cae4) !important;
    border-radius: 10px !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #070a1a 0%, #0d1030 100%) !important;
    border-right: 1px solid rgba(108,99,255,0.2) !important;
}
[data-testid="stSidebar"] .stMarkdown h2 { color: #a89cff !important; }

/* ── RADIO ── */
.stRadio > div { gap: 0.5rem !important; flex-wrap: wrap !important; }
.stRadio > div > label {
    background: #0d1030 !important; border: 1.5px solid rgba(108,99,255,0.2) !important;
    border-radius: 10px !important; padding: 0.5rem 1rem !important;
    color: #c8cde8 !important; transition: all 0.2s !important; font-weight: 500 !important;
}
.stRadio > div > label:hover { border-color: #6c63ff !important; }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] { background: transparent !important; gap: 0.5rem !important; }
.stTabs [data-baseweb="tab"] {
    background: #0d1030 !important; border: 1px solid rgba(108,99,255,0.2) !important;
    border-radius: 10px !important; color: #8892b0 !important; font-weight: 600 !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #6c63ff, #302b63) !important;
    border-color: #6c63ff !important; color: #fff !important;
}

/* ── INFO / ALERT ── */
.stAlert { background: rgba(108,99,255,0.1) !important; border: 1px solid rgba(108,99,255,0.3) !important; border-radius: 12px !important; }
hr { border-color: rgba(108,99,255,0.15) !important; }

/* ── METRIC ── */
[data-testid="stMetricValue"] { color: #6c63ff !important; font-weight: 800 !important; font-size: 1.8rem !important; }
[data-testid="stMetricLabel"] { color: #8892b0 !important; font-size: 0.8rem !important; }

/* ── TIP CARD ── */
.tip-card {
    background: linear-gradient(135deg, rgba(108,99,255,0.1), rgba(72,202,228,0.05));
    border: 1px solid rgba(108,99,255,0.25); border-radius: 14px;
    padding: 1rem 1.2rem; margin: 1rem 0;
    font-size: 0.88rem; color: #a89cff;
}
.tip-card strong { color: #6c63ff; }

/* ── FLASHCARD ── */
.flashcard {
    background: linear-gradient(135deg, #0f0c29, #1a1645);
    border: 2px solid rgba(108,99,255,0.4); border-radius: 20px;
    padding: 3rem 2rem; text-align: center; min-height: 200px;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    cursor: pointer; transition: all 0.3s ease;
    box-shadow: 0 15px 40px rgba(108,99,255,0.2);
}
.flashcard:hover { transform: translateY(-5px); box-shadow: 0 25px 60px rgba(108,99,255,0.3); }
.flashcard-q { font-size: 1.2rem; font-weight: 700; color: #e8eaf6; }
.flashcard-a { font-size: 1rem; color: #48cae4; margin-top: 1rem; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# ── Session State ─────────────────────────────────────────────
def init():
    defaults = {
        "chat_history": [],
        "explain_history": [],
        "quiz_questions": [], "quiz_answers": {}, "quiz_submitted": False, "quiz_score": 0,
        "mode": "explain",
        "last_explain": None, "last_explain_topic": "",
        "last_summary": None,
        "last_plan": None,
        "flashcards": [],
        "fc_index": 0, "fc_show_answer": False,
        "total_queries": 0,
        "streak": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
init()

# ── API ───────────────────────────────────────────────────────
MODELS = [
    "openrouter/auto",
    "deepseek/deepseek-chat-v3-0324:free",
    "meta-llama/llama-3.2-3b-instruct:free",
    "qwen/qwen-2.5-7b-instruct:free",
]

def ask_ai(messages, api_key, max_tokens=2000):
    if not api_key:
        st.error("⚠️ Service unavailable. Please contact admin.")
        return None
    for model in MODELS:
        try:
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json",
                         "HTTP-Referer": "https://studymate-ai.streamlit.app", "X-Title": "StudyMate AI"},
                json={"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": 0.75},
                timeout=45
            )
            data = r.json()
            if r.status_code == 200:
                st.session_state.total_queries += 1
                return data["choices"][0]["message"]["content"]
            elif r.status_code == 429:
                time.sleep(1); continue
        except Exception:
            continue
    st.error("❌ Could not get a response. Please try again.")
    return None

def read_pdf(f):
    try:
        import io
        try:
            import pypdf
            r = pypdf.PdfReader(io.BytesIO(f.read()))
            return "\n".join(p.extract_text() or "" for p in r.pages)
        except ImportError:
            pass
        try:
            import PyPDF2
            r = PyPDF2.PdfReader(io.BytesIO(f.read()))
            return "\n".join(p.extract_text() or "" for p in r.pages)
        except ImportError:
            return "PDF library not available."
    except Exception as e:
        return f"Could not read PDF: {e}"

# ── API Key ───────────────────────────────────────────────────
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
except Exception:
    api_key = None

# ── STUDY TIPS ────────────────────────────────────────────────
TIPS = [
    "🧠 **Spaced Repetition** — Review material after 1 day, 3 days, 1 week, and 1 month for long-term memory.",
    "⏱️ **Pomodoro Technique** — Study for 25 minutes, take a 5-minute break. Repeat 4 times, then take a long break.",
    "✍️ **Active Recall** — Instead of re-reading, close the book and write down everything you remember.",
    "🎯 **Feynman Technique** — Explain a concept in simple terms as if teaching a child. Gaps = what to study more.",
    "🌙 **Sleep & Memory** — Your brain consolidates memories during sleep. Don't skip it before exams!",
    "📝 **Mind Mapping** — Draw visual connections between concepts. Great for complex topics.",
    "🔇 **Eliminate Distractions** — Put your phone in another room while studying. Focus time is sacred.",
]

# ── SIDEBAR ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚀 StudyMate AI")
    st.markdown("---")

    if api_key:
        st.markdown("""
        <div style='background:linear-gradient(135deg,rgba(108,99,255,0.15),rgba(72,202,228,0.1));
        border:1px solid rgba(108,99,255,0.3);border-radius:12px;padding:0.8rem;text-align:center;'>
        <span style='color:#48cae4;font-weight:700;font-size:0.85rem;'>⚡ AI Connected</span><br>
        <span style='color:#8892b0;font-size:0.75rem;'>Ready to help you study</span>
        </div>""", unsafe_allow_html=True)
    else:
        st.error("⚠️ Service unavailable.")

    st.markdown("---")
    st.markdown("### 📊 Your Progress")
    c1, c2 = st.columns(2)
    c1.metric("Queries", st.session_state.total_queries)
    c2.metric("Chat", len(st.session_state.chat_history) // 2)

    if st.session_state.quiz_score > 0:
        st.metric("Best Quiz", f"{st.session_state.quiz_score} pts")

    st.markdown("---")
    st.markdown("### 💡 Study Tip")
    st.markdown(f"""<div class='tip-card'>{random.choice(TIPS)}</div>""", unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
    with col2:
        if st.button("🔄 Reset All"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

    st.markdown("---")
    st.markdown("<p style='font-size:0.75rem;color:#4a5080;text-align:center;'>Built by <b style='color:#6c63ff;'>Huzaifa</b> · Powered by OpenRouter AI</p>", unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <div class="hero-badge">✦ AI-Powered Study Assistant</div>
    <div class="hero-title">Study Smarter.<br>Not Harder.</div>
    <div class="hero-sub">Your personal AI tutor — available 24/7, powered by advanced language models.</div>
    <div class="hero-stats">
        <div class="hero-stat">
            <div class="hero-stat-num">{st.session_state.total_queries}</div>
            <div class="hero-stat-label">Queries Made</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-num">5</div>
            <div class="hero-stat-label">AI Tools</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-num">∞</div>
            <div class="hero-stat-label">Topics Covered</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-num">Free</div>
            <div class="hero-stat-label">Always</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── MODE BUTTONS ─────────────────────────────────────────────
MODES = {
    "explain":   ("💡", "Explain"),
    "summarize": ("📝", "Summarize"),
    "quiz":      ("❓", "Quiz"),
    "flashcard": ("🃏", "Flashcards"),
    "plan":      ("📅", "Study Plan"),
    "chat":      ("💬", "AI Chat"),
}
cols = st.columns(len(MODES))
for col, (key, (icon, label)) in zip(cols, MODES.items()):
    with col:
        if st.button(f"{icon} {label}", key=f"mode_{key}"):
            st.session_state.mode = key
            st.rerun()

st.markdown("---")
mode = st.session_state.mode

# ══════════════════════════════════════════════════════════════
#  💡  EXPLAIN
# ══════════════════════════════════════════════════════════════
if mode == "explain":
    st.markdown('<div class="section-title">💡 Topic Explainer</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        subject = st.selectbox("Subject", ["Computer Science", "Mathematics", "Physics",
            "Chemistry", "Biology", "History", "English", "Networking",
            "Software Engineering", "Economics", "Psychology", "Other"])
        topic = st.text_input("What do you want to learn?",
            placeholder="e.g. Binary Search Trees, Quantum Mechanics, French Revolution...",
            value=st.session_state.last_explain_topic)
    with col2:
        level = st.select_slider("Depth", ["Basic", "Intermediate", "Advanced", "Expert"])
        lang  = st.selectbox("Response Language", ["English", "Simple English", "Urdu"])

    with st.expander("📎 Attach Reference Material (Optional)"):
        pdf_file = st.file_uploader("Upload PDF", type=["pdf"], key="explain_pdf")
        extra_context = st.text_area("Or paste extra context:", height=80, placeholder="Paste any additional notes or context here...")

    c1, c2, c3 = st.columns([2, 2, 3])
    with c1:
        generate = st.button("✨ Explain Now", key="btn_explain")
    with c2:
        if st.session_state.last_explain:
            if st.button("✏️ Modify Request", key="btn_re_explain"):
                st.session_state.last_explain = None
                st.rerun()

    if generate:
        if not topic.strip() and not pdf_file:
            st.warning("Please enter a topic.")
        else:
            context = extra_context
            if pdf_file:
                with st.spinner("Reading PDF..."):
                    context += "\n" + read_pdf(pdf_file)[:4000]
            with st.spinner("🤖 Generating explanation..."):
                messages = [
                    {"role": "system", "content": (
                        f"You are StudyMate, an expert AI tutor. Respond in {lang}. Depth: {level}. "
                        "Format your response beautifully with: "
                        "**🔍 Definition** — clear one-liner. "
                        "**📖 Explanation** — detailed with real-world analogies and examples. "
                        "**⚡ Key Points** — 4-6 bullet points (most important facts). "
                        "**🎯 Exam Tips** — what examiners look for, common mistakes to avoid. "
                        "**❓ Practice Question** — one question with hint. "
                        "Be thorough, engaging, and use formatting to make it visually clear."
                    )},
                    {"role": "user", "content": f"Explain '{topic}' from {subject} at {level} level." +
                     (f"\n\nAdditional context:\n{context}" if context.strip() else "")}
                ]
                result = ask_ai(messages, api_key, 2500)
            if result:
                st.session_state.last_explain = result
                st.session_state.last_explain_topic = topic
                st.session_state.explain_history.append({"topic": topic, "subject": subject, "result": result})

    if st.session_state.last_explain:
        st.markdown(f'<div class="result-box">{st.session_state.last_explain}</div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button("📥 Download Notes", st.session_state.last_explain,
                               file_name=f"{st.session_state.last_explain_topic}_notes.txt")
        with c2:
            if st.button("🃏 Make Flashcards", key="make_fc"):
                st.session_state.mode = "flashcard"
                st.session_state["pending_fc_topic"] = st.session_state.last_explain_topic
                st.rerun()
        with c3:
            if st.button("❓ Quiz Me On This", key="quiz_this"):
                st.session_state.mode = "quiz"
                st.session_state["pending_quiz_topic"] = st.session_state.last_explain_topic
                st.rerun()

    if len(st.session_state.explain_history) > 1:
        with st.expander(f"📚 History ({len(st.session_state.explain_history)} topics studied)"):
            for item in reversed(st.session_state.explain_history[:-1]):
                st.markdown(f"**{item['subject']} · {item['topic']}**")
                st.markdown(item['result'][:200] + "...")
                st.markdown("---")

# ══════════════════════════════════════════════════════════════
#  📝  SUMMARIZE
# ══════════════════════════════════════════════════════════════
elif mode == "summarize":
    st.markdown('<div class="section-title">📝 Smart Summarizer</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["✏️ Paste Text", "📄 Upload PDF"])
    with tab1:
        notes = st.text_area("Your Notes / Textbook Content", height=250,
                             placeholder="Paste any text here — lecture notes, textbook chapters, articles...")
    with tab2:
        pdf_up = st.file_uploader("Upload PDF", type=["pdf"], key="sum_pdf")
        notes_from_pdf = ""
        if pdf_up:
            with st.spinner("Extracting text..."):
                notes_from_pdf = read_pdf(pdf_up)
            st.success(f"✅ {len(notes_from_pdf):,} characters extracted from PDF!")

    col1, col2, col3 = st.columns(3)
    with col1:
        length = st.selectbox("Summary Style", ["Quick (5 Key Points)", "Standard (10 Points)",
                                                 "Detailed (Full Notes)", "One-liner Summary"])
    with col2:
        focus  = st.selectbox("Focus On", ["Key Concepts", "Exam Preparation", "Definitions & Terms",
                                            "Timeline / Process", "Complete Overview"])
    with col3:
        lang2  = st.selectbox("Language", ["English", "Simple English", "Urdu"])

    c1, c2 = st.columns([2, 2])
    with c1:
        if st.button("⚡ Summarize Now", key="btn_sum"):
            raw = notes or notes_from_pdf
            if not raw.strip():
                st.warning("Please paste notes or upload a PDF.")
            else:
                with st.spinner("🤖 Summarizing your content..."):
                    messages = [
                        {"role": "system", "content": (
                            f"You are StudyMate, an expert AI study assistant. Respond in {lang2}. "
                            f"Create a {length} summary focusing on {focus}. "
                            "Use: **bold headings**, bullet points, numbered lists where needed. "
                            "Highlight key terms. End with '🎯 Key Takeaways' section. "
                            "Make it visually scannable and exam-ready."
                        )},
                        {"role": "user", "content": f"Summarize this content:\n\n{raw[:7000]}"}
                    ]
                    result = ask_ai(messages, api_key, 2500)
                if result:
                    st.session_state.last_summary = result
    with c2:
        if st.session_state.last_summary:
            if st.button("✏️ Re-summarize with Different Settings", key="btn_re_sum"):
                st.session_state.last_summary = None
                st.rerun()

    if st.session_state.last_summary:
        st.markdown(f'<div class="result-box">{st.session_state.last_summary}</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.download_button("📥 Download Summary", st.session_state.last_summary, file_name="summary.txt")
        with c2:
            if st.button("❓ Quiz Me On This Summary", key="quiz_summary"):
                st.session_state.mode = "quiz"
                st.rerun()

# ══════════════════════════════════════════════════════════════
#  ❓  QUIZ
# ══════════════════════════════════════════════════════════════
elif mode == "quiz":
    st.markdown('<div class="section-title">❓ Quiz Generator</div>', unsafe_allow_html=True)

    pending = st.session_state.pop("pending_quiz_topic", None)

    col1, col2 = st.columns(2)
    with col1:
        quiz_topic = st.text_input("Quiz Topic", value=pending or "",
                                   placeholder="e.g. Data Structures, French Revolution, Thermodynamics...")
        num_q = st.slider("Number of Questions", 3, 20, 7)
    with col2:
        difficulty = st.select_slider("Difficulty Level", ["Easy", "Medium", "Hard", "Expert"])
        q_type = st.selectbox("Question Format", ["Multiple Choice (MCQs)", "True / False",
                                                   "Short Answer", "Fill in the Blank", "Mixed (All Types)"])

    if st.button("🚀 Generate Quiz", key="btn_quiz_gen"):
        if not quiz_topic.strip():
            st.warning("Please enter a topic.")
        else:
            with st.spinner("🤖 Building your quiz..."):
                messages = [
                    {"role": "system", "content": (
                        "You are an expert quiz generator. Return ONLY a valid JSON array. "
                        "No explanation, no markdown, no extra text — just the JSON array. "
                        'Format: [{"q":"Question","options":["A) opt","B) opt","C) opt","D) opt"],"answer":"A","explanation":"Why A is correct"}] '
                        "True/False: options=['True','False'], answer='True' or 'False'. "
                        "Short Answer / Fill in Blank: options=[], answer='expected answer'. "
                        "Make questions challenging, clear, and educational."
                    )},
                    {"role": "user", "content": f"Generate {num_q} {q_type} questions on '{quiz_topic}' at {difficulty} level."}
                ]
                raw = ask_ai(messages, api_key, 3500)

            if raw:
                try:
                    clean = re.sub(r"```json|```", "", raw).strip()
                    questions = json.loads(clean)
                    st.session_state.quiz_questions = questions
                    st.session_state.quiz_answers   = {}
                    st.session_state.quiz_submitted  = False
                    st.rerun()
                except Exception:
                    st.markdown(f'<div class="result-box">{raw}</div>', unsafe_allow_html=True)

    if st.session_state.quiz_questions:
        qs    = st.session_state.quiz_questions
        total = len(qs)
        answered = len([v for v in st.session_state.quiz_answers.values() if v])

        st.markdown(f"**Progress: {answered}/{total} answered**")
        st.progress(answered / total if total > 0 else 0)
        st.markdown("")

        for i, q in enumerate(qs):
            with st.container():
                st.markdown(f'<div class="quiz-num">Question {i+1} of {total} · {difficulty}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="quiz-q">{q.get("q","")}</div>', unsafe_allow_html=True)
                opts = q.get("options", [])
                key  = f"q_{i}"
                if opts:
                    chosen = st.radio("", opts, key=key, index=None, horizontal=len(opts) == 2)
                    if chosen is not None:
                        letter = chosen.split(")")[0].strip() if ")" in chosen else chosen
                        st.session_state.quiz_answers[i] = letter
                else:
                    ans = st.text_input("Your answer:", key=key, placeholder="Type your answer...")
                    st.session_state.quiz_answers[i] = ans
                st.markdown("---")

        if not st.session_state.quiz_submitted:
            c1, c2 = st.columns([1, 3])
            with c1:
                if st.button("✅ Submit Quiz", key="btn_submit"):
                    score = 0
                    for i, q in enumerate(qs):
                        correct = str(q.get("answer","")).strip().upper()
                        given   = str(st.session_state.quiz_answers.get(i,"")).strip().upper()
                        if given and (given == correct or given in correct or correct in given):
                            score += 1
                    st.session_state.quiz_score    = max(st.session_state.quiz_score, score)
                    st.session_state.quiz_submitted = True
                    st.rerun()

        if st.session_state.quiz_submitted:
            score = sum(
                1 for i, q in enumerate(qs)
                if str(st.session_state.quiz_answers.get(i,"")).strip().upper() in
                   str(q.get("answer","")).strip().upper() or
                   str(q.get("answer","")).strip().upper() in
                   str(st.session_state.quiz_answers.get(i,"")).strip().upper()
            )
            pct   = int(score / total * 100) if total else 0
            emoji = "🏆" if pct >= 90 else "🎉" if pct >= 75 else "💪" if pct >= 60 else "📚"
            grade = "Outstanding!" if pct >= 90 else "Great Job!" if pct >= 75 else "Good Effort!" if pct >= 60 else "Keep Practicing!"

            st.markdown(f"""
            <div class="score-box">
                <div class="score-emoji">{emoji}</div>
                <div class="score-num">{score} / {total}</div>
                <div class="score-pct">{pct}%</div>
                <div class="score-grade">{grade}</div>
            </div>""", unsafe_allow_html=True)

            with st.expander("📋 Detailed Answer Review"):
                for i, q in enumerate(qs):
                    correct = q.get("answer","")
                    given   = st.session_state.quiz_answers.get(i,"")
                    explain = q.get("explanation","")
                    is_right = str(given).strip().upper() in str(correct).strip().upper() or \
                               str(correct).strip().upper() in str(given).strip().upper()
                    icon = "✅" if is_right else "❌"
                    st.markdown(f"**{icon} Q{i+1}:** {q.get('q','')}")
                    st.markdown(f"&nbsp;&nbsp;Your answer: `{given}` &nbsp;|&nbsp; Correct: `{correct}`")
                    if explain: st.info(f"💡 {explain}")
                    st.markdown("---")

            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("🔄 Try Again", key="btn_retry"):
                    st.session_state.quiz_answers   = {}
                    st.session_state.quiz_submitted  = False
                    st.rerun()
            with c2:
                if st.button("🆕 New Quiz", key="btn_new_quiz"):
                    st.session_state.quiz_questions = []
                    st.session_state.quiz_answers   = {}
                    st.session_state.quiz_submitted  = False
                    st.rerun()
            with c3:
                if st.button("💬 Discuss with AI", key="discuss_quiz"):
                    st.session_state.mode = "chat"
                    st.session_state.chat_history.append({"role": "user",
                        "content": f"I scored {score}/{total} ({pct}%) on a '{quiz_topic}' quiz at {difficulty} level. Help me understand what I got wrong and how to improve."})
                    st.rerun()

# ══════════════════════════════════════════════════════════════
#  🃏  FLASHCARDS
# ══════════════════════════════════════════════════════════════
elif mode == "flashcard":
    st.markdown('<div class="section-title">🃏 AI Flashcards</div>', unsafe_allow_html=True)

    pending_fc = st.session_state.pop("pending_fc_topic", None)

    col1, col2 = st.columns([3, 1])
    with col1:
        fc_topic = st.text_input("Topic for Flashcards", value=pending_fc or "",
                                  placeholder="e.g. Network Protocols, Cell Biology, World War II dates...")
    with col2:
        fc_count = st.number_input("Number of Cards", 5, 30, 10)

    if st.button("🃏 Generate Flashcards", key="btn_fc_gen"):
        if not fc_topic.strip():
            st.warning("Please enter a topic.")
        else:
            with st.spinner("🤖 Creating your flashcards..."):
                messages = [
                    {"role": "system", "content": (
                        "You are a flashcard generator. Return ONLY a JSON array. "
                        'Format: [{"q":"Question or term","a":"Answer or definition"}] '
                        "Make questions concise, answers clear and memorable. No extra text."
                    )},
                    {"role": "user", "content": f"Create {fc_count} flashcards for '{fc_topic}'."}
                ]
                raw = ask_ai(messages, api_key, 2000)
            if raw:
                try:
                    clean = re.sub(r"```json|```", "", raw).strip()
                    cards = json.loads(clean)
                    st.session_state.flashcards    = cards
                    st.session_state.fc_index      = 0
                    st.session_state.fc_show_answer = False
                    st.rerun()
                except Exception:
                    st.error("Could not parse flashcards. Please try again.")

    if st.session_state.flashcards:
        cards   = st.session_state.flashcards
        idx     = st.session_state.fc_index
        total   = len(cards)
        card    = cards[idx]
        show_a  = st.session_state.fc_show_answer

        st.markdown(f"**Card {idx+1} of {total}**")
        st.progress((idx + 1) / total)
        st.markdown("")

        if not show_a:
            st.markdown(f"""
            <div class="flashcard">
                <div style='font-size:0.75rem;color:#6c63ff;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:0.5rem;'>QUESTION</div>
                <div class="flashcard-q">{card['q']}</div>
                <div style='font-size:0.8rem;color:#4a5080;margin-top:1.5rem;'>Click "Show Answer" to reveal</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="flashcard">
                <div style='font-size:0.75rem;color:#48cae4;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:0.5rem;'>ANSWER</div>
                <div class="flashcard-q">{card['q']}</div>
                <div class="flashcard-a">{card['a']}</div>
            </div>""", unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("👁️ Show Answer" if not show_a else "🙈 Hide Answer", key="fc_flip"):
                st.session_state.fc_show_answer = not show_a
                st.rerun()
        with c2:
            if st.button("⬅️ Previous", key="fc_prev", disabled=idx == 0):
                st.session_state.fc_index      -= 1
                st.session_state.fc_show_answer = False
                st.rerun()
        with c3:
            if st.button("Next ➡️", key="fc_next", disabled=idx == total - 1):
                st.session_state.fc_index      += 1
                st.session_state.fc_show_answer = False
                st.rerun()
        with c4:
            if st.button("🔀 Shuffle", key="fc_shuffle"):
                random.shuffle(st.session_state.flashcards)
                st.session_state.fc_index      = 0
                st.session_state.fc_show_answer = False
                st.rerun()

# ══════════════════════════════════════════════════════════════
#  📅  STUDY PLAN
# ══════════════════════════════════════════════════════════════
elif mode == "plan":
    st.markdown('<div class="section-title">📅 Smart Study Planner</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        exam_sub = st.text_input("Subject / Exam Name", placeholder="e.g. Data Structures Final, Physics Midterm")
        days     = st.number_input("Days until exam", min_value=1, max_value=365, value=7)
    with col2:
        hours = st.number_input("Daily study hours available", min_value=1, max_value=20, value=3)
        weak  = st.text_input("Weak areas to focus on (optional)", placeholder="e.g. Recursion, Thermodynamics...")

    col3, col4 = st.columns(2)
    with col3:
        style = st.selectbox("Study Style", ["Balanced & Steady", "Intensive (Exam Crunch Mode)",
                                              "Relaxed & Gradual", "Weekend-Heavy"])
    with col4:
        goal = st.selectbox("Your Target", ["Pass the exam", "Score 60%+", "Score 75%+",
                                             "Score 90%+", "Perfect score"])

    c1, c2 = st.columns([2, 2])
    with c1:
        if st.button("🗓️ Generate My Plan", key="btn_plan"):
            if not exam_sub.strip():
                st.warning("Please enter a subject name.")
            else:
                with st.spinner("🤖 Creating your personalized study plan..."):
                    messages = [
                        {"role": "system", "content": (
                            "You are StudyMate, an expert academic study planner. "
                            "Create a detailed, realistic day-by-day study schedule. "
                            "Format with clear **Day X** headings, specific topics per session, "
                            "time allocation per topic, revision checkpoints, practice test days, "
                            "and daily motivational tips. "
                            "Include a **📋 Overview** section at the top with the full strategy. "
                            "End with **🎯 Success Tips** section. Make it professional and motivating."
                        )},
                        {"role": "user", "content": (
                            f"Create a complete {days}-day study plan for '{exam_sub}'. "
                            f"Available time: {hours} hours/day. Style: {style}. "
                            f"Target: {goal}. Weak areas: {weak or 'none specified'}. "
                            "Be specific with topics, times, and tips."
                        )}
                    ]
                    result = ask_ai(messages, api_key, 3500)
                if result:
                    st.session_state.last_plan = result
    with c2:
        if st.session_state.last_plan:
            if st.button("✏️ Adjust Plan", key="btn_re_plan"):
                st.session_state.last_plan = None
                st.rerun()

    if st.session_state.last_plan:
        st.markdown(f'<div class="result-box">{st.session_state.last_plan}</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.download_button("📥 Download Study Plan", st.session_state.last_plan, file_name="study_plan.txt")
        with c2:
            if st.button("💬 Discuss Plan with AI", key="discuss_plan"):
                st.session_state.mode = "chat"
                st.session_state.chat_history.append({"role": "user",
                    "content": f"I have a {days}-day study plan for {exam_sub}. Can you give me additional tips and strategies to make the most of it?"})
                st.rerun()

# ══════════════════════════════════════════════════════════════
#  💬  AI CHAT
# ══════════════════════════════════════════════════════════════
elif mode == "chat":
    st.markdown('<div class="section-title">💬 AI Study Assistant</div>', unsafe_allow_html=True)
    st.caption("Full conversation memory — ask anything, follow up, go deep on any topic.")

    if not st.session_state.chat_history:
        st.markdown("""
        <div style='text-align:center;padding:3rem;'>
            <div style='font-size:3rem;margin-bottom:1rem;'>🤖</div>
            <div style='font-size:1.1rem;font-weight:700;color:#a89cff;margin-bottom:0.5rem;'>Hi! I'm StudyMate AI</div>
            <div style='color:#8892b0;font-size:0.9rem;'>Ask me to explain a topic, quiz you, help with homework,<br>review your answers, or anything study-related.</div>
        </div>
        """, unsafe_allow_html=True)

        # Quick start suggestions
        suggestions = [
            "Explain the OSI model in simple terms",
            "Quiz me on Python basics",
            "Help me understand recursion",
            "What's the difference between RAM and ROM?",
        ]
        st.markdown("**Quick Start:**")
        cols = st.columns(2)
        for i, s in enumerate(suggestions):
            with cols[i % 2]:
                if st.button(s, key=f"suggest_{i}"):
                    st.session_state.chat_history.append({"role": "user", "content": s})
                    st.rerun()
    else:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="msg-user-wrap">
                    <div>
                        <div style='text-align:right;font-size:0.7rem;color:#6c63ff;font-weight:700;margin-bottom:0.3rem;'>You</div>
                        <div class="msg-bubble-user">{msg["content"]}</div>
                    </div>
                    <div class="msg-avatar-user">👤</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="msg-ai-wrap">
                    <div class="msg-avatar-ai">🎓</div>
                    <div>
                        <div style='font-size:0.7rem;color:#48cae4;font-weight:700;margin-bottom:0.3rem;'>StudyMate AI</div>
                        <div class="msg-bubble-ai">{msg["content"]}</div>
                    </div>
                </div>""", unsafe_allow_html=True)

    user_msg = st.chat_input("Ask anything — explain, quiz, summarize, compare, help with assignments...")

    if user_msg:
        st.session_state.chat_history.append({"role": "user", "content": user_msg})
        messages = [
            {"role": "system", "content": (
                "You are StudyMate, an expert AI study assistant for university students. "
                "You have full memory of the conversation — use it for context-aware responses. "
                "Be thorough, accurate, engaging and encouraging. Use formatting where helpful. "
                "If explaining concepts, use real examples. If quizzed, generate proper questions. "
                "Adapt your depth based on the student's apparent level. Always be supportive."
            )}
        ] + st.session_state.chat_history

        with st.spinner("🤖 Thinking..."):
            reply = ask_ai(messages, api_key, 2000)
        if reply:
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

# ── FOOTER ────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<p style='text-align:center;color:#4a5080;font-size:0.8rem;'>
    <span style='color:#6c63ff;font-weight:700;'>StudyMate AI</span> &nbsp;·&nbsp;
    Built with ❤️ by <span style='color:#6c63ff;'>Huzaifa</span> &nbsp;·&nbsp;
    Powered by OpenRouter AI &nbsp;·&nbsp;
    <span style='color:#48cae4;'>Free forever for students 🎓</span>
</p>""", unsafe_allow_html=True)
