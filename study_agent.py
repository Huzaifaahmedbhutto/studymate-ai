import streamlit as st
import requests
import json
import time
import re

st.set_page_config(
    page_title="StudyMate AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, .stApp { background: #0a0e1a !important; color: #e2e8f0 !important; font-family: 'Space Grotesk', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0d1220; }
::-webkit-scrollbar-thumb { background: #2d6a4f; border-radius: 3px; }
.main .block-container { padding: 2rem 2.5rem !important; max-width: 1200px; }

.hero-header {
    background: linear-gradient(135deg, #0d2137 0%, #0a1628 40%, #0d2137 100%);
    border: 1px solid rgba(45,106,79,0.3); border-radius: 20px;
    padding: 2.5rem 3rem; margin-bottom: 2rem; position: relative; overflow: hidden;
}
.hero-header::before {
    content: ''; position: absolute; top: -50%; right: -10%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(45,106,79,0.15) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-size: 2.4rem; font-weight: 700;
    background: linear-gradient(135deg, #52b788, #95d5b2, #52b788);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin-bottom: 0.4rem; letter-spacing: -0.5px;
}
.hero-subtitle { font-size: 1rem; color: #74c69d; font-weight: 400; opacity: 0.85; }

.section-title { font-size: 1.3rem; font-weight: 700; color: #52b788; margin-bottom: 1.2rem; display: flex; align-items: center; gap: 0.5rem; }

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    background: #0a1628 !important; border: 1px solid rgba(82,183,136,0.25) !important;
    border-radius: 10px !important; color: #e2e8f0 !important;
    font-family: 'Space Grotesk', sans-serif !important; font-size: 0.95rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #52b788 !important; box-shadow: 0 0 0 3px rgba(82,183,136,0.15) !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label,
.stSlider label, .stRadio label, .stFileUploader label {
    color: #95d5b2 !important; font-weight: 600 !important; font-size: 0.9rem !important;
}
.stRadio > div { gap: 0.5rem !important; }
.stRadio > div > label {
    background: #0a1628 !important; border: 1px solid rgba(82,183,136,0.2) !important;
    border-radius: 10px !important; padding: 0.5rem 1rem !important; color: #e2e8f0 !important; transition: all 0.2s !important;
}
.stRadio > div > label:hover { border-color: #52b788 !important; background: rgba(82,183,136,0.08) !important; }

.stButton > button {
    background: linear-gradient(135deg, #2d6a4f, #52b788) !important;
    color: #fff !important; border: none !important; border-radius: 10px !important;
    padding: 0.65rem 0.8rem !important; font-size: 0.82rem !important; font-weight: 600 !important;
    font-family: 'Space Grotesk', sans-serif !important; cursor: pointer !important;
    transition: all 0.3s ease !important; white-space: nowrap !important; width: 100% !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important; box-shadow: 0 8px 25px rgba(82,183,136,0.4) !important;
    background: linear-gradient(135deg, #52b788, #74c69d) !important;
}
.stDownloadButton > button {
    background: transparent !important; border: 1px solid rgba(82,183,136,0.4) !important;
    color: #74c69d !important; border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important; font-weight: 600 !important; transition: all 0.3s !important;
}
.stDownloadButton > button:hover { background: rgba(82,183,136,0.1) !important; border-color: #52b788 !important; }

.result-box {
    background: #071020; border: 1px solid rgba(82,183,136,0.25);
    border-left: 4px solid #52b788; border-radius: 12px;
    padding: 1.8rem; margin-top: 1.2rem; line-height: 1.8; font-size: 0.95rem; color: #d1fae5;
}

.chat-message-user {
    background: rgba(82,183,136,0.1); border: 1px solid rgba(82,183,136,0.2);
    border-radius: 14px 14px 4px 14px; padding: 1rem 1.2rem;
    margin: 0.5rem 0 0.5rem 3rem; font-size: 0.92rem; color: #e2e8f0;
}
.chat-message-ai {
    background: #0d1a2e; border: 1px solid rgba(82,183,136,0.15);
    border-radius: 14px 14px 14px 4px; padding: 1rem 1.2rem;
    margin: 0.5rem 3rem 0.5rem 0; font-size: 0.92rem; color: #d1fae5; line-height: 1.7;
}
.chat-label-user { font-size: 0.75rem; color: #52b788; font-weight: 700; text-align: right; margin-right: 0.5rem; }
.chat-label-ai { font-size: 0.75rem; color: #74c69d; font-weight: 700; margin-left: 0.5rem; }

.quiz-question-num { font-size: 0.75rem; color: #52b788; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.4rem; }
.quiz-question-text { font-size: 1rem; font-weight: 600; color: #e2e8f0; margin-bottom: 0.8rem; }

.score-badge {
    background: linear-gradient(135deg, #2d6a4f, #1b4332); border: 1px solid #52b788;
    border-radius: 12px; padding: 1.2rem 2rem; text-align: center;
    font-size: 1.5rem; font-weight: 700; color: #95d5b2; margin: 1rem 0;
}

[data-testid="stSidebar"] { background: #07111e !important; border-right: 1px solid rgba(82,183,136,0.15) !important; }
[data-testid="stSidebar"] .stMarkdown h2, [data-testid="stSidebar"] .stMarkdown h3 { color: #52b788 !important; }

.stSlider > div > div > div > div { background: linear-gradient(90deg, #2d6a4f, #52b788) !important; }
.stAlert { background: rgba(82,183,136,0.08) !important; border: 1px solid rgba(82,183,136,0.25) !important; border-radius: 10px !important; color: #95d5b2 !important; }
hr { border-color: rgba(82,183,136,0.15) !important; }

.stTabs [data-baseweb="tab-list"] { background: transparent !important; gap: 0.5rem !important; }
.stTabs [data-baseweb="tab"] {
    background: #0d1a2e !important; border: 1px solid rgba(82,183,136,0.2) !important;
    border-radius: 10px !important; color: #74c69d !important;
    font-family: 'Space Grotesk', sans-serif !important; font-weight: 600 !important; padding: 0.5rem 1.2rem !important;
}
.stTabs [aria-selected="true"] { background: linear-gradient(135deg, #2d6a4f, #1b4332) !important; border-color: #52b788 !important; color: #d1fae5 !important; }

[data-testid="stMetricValue"] { color: #52b788 !important; font-family: 'Space Grotesk', sans-serif !important; font-weight: 700 !important; }
[data-testid="stMetricLabel"] { color: #74c69d !important; }
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE ─────────────────────────────────────────────
def init_session():
    defaults = {
        "chat_history": [],
        "quiz_questions": [],
        "quiz_answers": {},
        "quiz_submitted": False,
        "quiz_score": 0,
        "mode": "explain",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()

# ─── GROQ API ──────────────────────────────────────────────────
GROQ_MODELS = [
    "openrouter/free",
    "meta-llama/llama-3.2-3b-instruct:free",
    "meta-llama/llama-3.2-1b-instruct:free",
]

def ask_groq(prompt: str, system: str, api_key: str, max_tokens: int = 2000) -> str | None:
    if not api_key:
        st.error("⚠️ Please enter your OpenRouter API key in the sidebar.")
        return None

    for model in GROQ_MODELS:
        try:
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
            r = requests.post(url, headers=headers, json=payload, timeout=40)
            data = r.json()

            if r.status_code == 200:
                return data["choices"][0]["message"]["content"]
            elif r.status_code == 429:
                st.warning(f"⏳ {model} is busy — trying next model...")
                time.sleep(2)
                continue
            else:
                err = data.get("error", {}).get("message", "Unknown error")
                st.warning(f"⚠️ {model}: {err}")
                continue
        except Exception as e:
            continue

    st.error("❌ No models available. Please check your API key.")
    return None

# ─── PDF EXTRACTOR ─────────────────────────────────────────────
def extract_pdf_text(uploaded_file) -> str:
    try:
        import io
        try:
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(uploaded_file.read()))
            return "\n".join(p.extract_text() or "" for p in reader.pages)
        except ImportError:
            pass
        try:
            import PyPDF2
            reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
            return "\n".join(p.extract_text() or "" for p in reader.pages)
        except ImportError:
            pass
        return "PDF library not found. Please add pypdf to requirements.txt."
    except Exception as e:
        return f"Could not read PDF: {e}"

# ─── SIDEBAR ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 StudyMate AI")
    st.markdown("---")
    api_key = st.text_input(
        "🔑 OpenRouter API Key",
        type="password",
        placeholder="sk-or-...",
        help="Free key: openrouter.ai"
    )
    if api_key:
        st.success("✅ Connected")
    else:
        st.info("Get your free key at openrouter.ai")

    st.markdown("---")
    st.markdown("### 📊 Session Stats")
    c1, c2 = st.columns(2)
    c1.metric("Messages", len(st.session_state.chat_history))
    c2.metric("Quiz Score", str(st.session_state.quiz_score))

    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<p style='font-size:0.78rem; color:#52b788;'>Built by <b>Huzaifa</b> 🚀<br/>Powered by OpenRouter AI</p>",
        unsafe_allow_html=True,
    )

# ─── HERO ──────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <div class="hero-title">🎓 StudyMate AI</div>
    <div class="hero-subtitle">Your intelligent study companion — powered by AI, built for students.</div>
</div>
""", unsafe_allow_html=True)

# ─── MODE BUTTONS ──────────────────────────────────────────────
MODES = {
    "explain":   ("💡", "Explain"),
    "summarize": ("📝", "Summarize"),
    "quiz":      ("❓", "Quiz"),
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
#  💡  TOPIC EXPLAIN
# ══════════════════════════════════════════════════════════════
if mode == "explain":
    st.markdown('<div class="section-title">💡 Topic Explainer</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        subject = st.selectbox("Subject", [
            "Computer Science", "Mathematics", "Physics", "Chemistry",
            "Biology", "History", "English", "Networking", "Software Engineering", "Other"
        ])
        topic = st.text_input("Enter Topic", placeholder="e.g. Newton's Laws, Network Topology, OOP Concepts")
    with col2:
        level = st.select_slider("Level", ["Beginner", "Intermediate", "Advanced"])
        lang  = st.selectbox("Language", ["English", "Simple English", "Urdu"])

    with st.expander("📄 Upload Reference Material (Optional)"):
        pdf_file = st.file_uploader("Upload PDF", type=["pdf"], key="explain_pdf")

    if st.button("✨ Generate Explanation", key="btn_explain"):
        if not topic and not pdf_file:
            st.warning("Please enter a topic or upload a PDF.")
        else:
            context = ""
            if pdf_file:
                with st.spinner("Reading PDF..."):
                    context = extract_pdf_text(pdf_file)[:4000]

            with st.spinner("Generating explanation..."):
                system = (
                    f"You are StudyMate, a friendly AI study assistant for university students. "
                    f"Always respond in {lang}. "
                    f"Structure: 1) Simple definition 2) Easy explanation with example "
                    f"3) Key points bullet form 4) One common exam question. Be encouraging."
                )
                query = f"Explain '{topic}' from {subject} at {level} level."
                if context:
                    query += f"\n\nReference:\n{context}"
                result = ask_groq(query, system, api_key, 2000)

            if result:
                st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)
                st.download_button("📥 Download", result, file_name=f"{topic}_notes.txt", key="dl_explain")

# ══════════════════════════════════════════════════════════════
#  📝  NOTES SUMMARIZE
# ══════════════════════════════════════════════════════════════
elif mode == "summarize":
    st.markdown('<div class="section-title">📝 Smart Summarizer</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["✏️ Paste Text", "📄 Upload PDF"])
    with tab1:
        notes = st.text_area("Your Notes", height=220, placeholder="Paste your study notes here...")
    with tab2:
        pdf_up = st.file_uploader("Upload PDF", type=["pdf"], key="sum_pdf")
        notes_from_pdf = ""
        if pdf_up:
            with st.spinner("Extracting text from PDF..."):
                notes_from_pdf = extract_pdf_text(pdf_up)
            st.success(f"✅ PDF loaded successfully!")

    col1, col2, col3 = st.columns(3)
    with col1:
        length = st.selectbox("Length", ["Brief (5 Key Points)", "Standard (10 Points)", "Comprehensive"])
    with col2:
        lang2 = st.selectbox("Language", ["English", "Simple English", "Urdu"], key="lang_sum")
    with col3:
        focus = st.selectbox("Focus", ["Key Concepts", "Exam Preparation", "Definitions & Terms", "Complete Overview"])

    if st.button("📝 Summarize", key="btn_sum"):
        raw = notes or notes_from_pdf
        if not raw.strip():
            st.warning("Please paste notes or upload a PDF.")
        else:
            with st.spinner("Summarizing your notes..."):
                system = (
                    f"You are StudyMate for university students. "
                    f"Summarize in {lang2}. Focus on {focus}. "
                    f"Use clear headings, bullet points, bold keywords. Make it exam-ready."
                )
                result = ask_groq(f"Summarize in '{length}' format:\n\n{raw[:5000]}", system, api_key, 2000)
            if result:
                st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)
                st.download_button("📥 Download Summary", result, file_name="summary.txt", key="dl_sum")

# ══════════════════════════════════════════════════════════════
#  ❓  QUIZ MODE
# ══════════════════════════════════════════════════════════════
elif mode == "quiz":
    st.markdown('<div class="section-title">❓ Quiz Generator</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        quiz_topic = st.text_input("Quiz Topic", placeholder="e.g. Object-Oriented Programming, Networking Basics")
        num_q      = st.slider("Number of Questions", 3, 10, 5)
    with col2:
        difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])
        q_type     = st.selectbox("Type", ["MCQs", "True/False", "Short Answer", "Mix of All"])

    if st.button("🎯 Generate Quiz", key="btn_quiz_gen"):
        if not quiz_topic:
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Generating your quiz..."):
                system = (
                    "You are StudyMate quiz generator. "
                    "Generate quiz in STRICT JSON format only — no extra text, no markdown. "
                    'Return array: [{"q":"Question","options":["A) ...","B) ...","C) ...","D) ..."],"answer":"A","explanation":"..."}] '
                    "For True/False: options=['True','False'], answer='True' or 'False'. "
                    "For Short Answer: options=[], answer='short text'."
                )
                query = f"Generate {num_q} {q_type} on '{quiz_topic}' at {difficulty} level."
                raw = ask_groq(query, system, api_key, 2000)

            if raw:
                try:
                    clean = re.sub(r"```json|```", "", raw).strip()
                    questions = json.loads(clean)
                    st.session_state.quiz_questions = questions
                    st.session_state.quiz_answers   = {}
                    st.session_state.quiz_submitted  = False
                    st.session_state.quiz_score      = 0
                    st.rerun()
                except Exception:
                    st.markdown(f'<div class="result-box">{raw}</div>', unsafe_allow_html=True)
                    st.download_button("📥 Download Quiz", raw, file_name=f"{quiz_topic}_quiz.txt")

    if st.session_state.quiz_questions:
        st.markdown("---")
        qs = st.session_state.quiz_questions

        for i, q in enumerate(qs):
            st.markdown(f'<div class="quiz-question-num">Question {i+1} of {len(qs)}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="quiz-question-text">{q.get("q","")}</div>', unsafe_allow_html=True)
            opts = q.get("options", [])
            key  = f"q_{i}"
            if opts:
                chosen = st.radio("Select your answer:", opts, key=key, index=None)
                if chosen is not None:
                    st.session_state.quiz_answers[i] = chosen.split(")")[0].strip() if ")" in chosen else chosen
            else:
                ans = st.text_input("Your Answer:", key=key)
                st.session_state.quiz_answers[i] = ans
            st.markdown("---")

        if not st.session_state.quiz_submitted:
            if st.button("✅ Submit Answers", key="btn_submit"):
                score = 0
                for i, q in enumerate(qs):
                    correct = str(q.get("answer","")).strip().upper()
                    given   = str(st.session_state.quiz_answers.get(i,"")).strip().upper()
                    if given and (given == correct or given in correct or correct in given):
                        score += 1
                st.session_state.quiz_score    = score
                st.session_state.quiz_submitted = True
                st.rerun()

        if st.session_state.quiz_submitted:
            total = len(qs)
            score = st.session_state.quiz_score
            pct   = int(score / total * 100)
            emoji = "🏆" if pct >= 80 else "💪" if pct >= 50 else "📖"
            st.markdown(f'<div class="score-badge">{emoji} Score: {score}/{total} | {pct}%</div>', unsafe_allow_html=True)

            with st.expander("📋 View Answer Key"):
                for i, q in enumerate(qs):
                    correct  = q.get("answer","")
                    given    = st.session_state.quiz_answers.get(i,"")
                    explain  = q.get("explanation","")
                    is_right = str(given).strip().upper() in str(correct).strip().upper() or \
                               str(correct).strip().upper() in str(given).strip().upper()
                    icon = "✅" if is_right else "❌"
                    st.markdown(f"**{icon} Q{i+1}:** {q.get('q','')}")
                    st.markdown(f"&nbsp;&nbsp;Your answer: `{given}` &nbsp;|&nbsp; Correct: `{correct}`")
                    if explain:
                        st.markdown(f"&nbsp;&nbsp;💡 _{explain}_")
                    st.markdown("---")

            if st.button("🔄 New Quiz", key="btn_new_quiz"):
                st.session_state.quiz_questions = []
                st.session_state.quiz_answers   = {}
                st.session_state.quiz_submitted  = False
                st.rerun()

# ══════════════════════════════════════════════════════════════
#  📅  STUDY PLAN
# ══════════════════════════════════════════════════════════════
elif mode == "plan":
    st.markdown('<div class="section-title">📅 Study Planner</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        exam_sub = st.text_input("Subject / Exam Name", placeholder="e.g. Software Engineering Final Exam")
        days     = st.slider("Days until exam", 1, 60, 7)
    with col2:
        hours = st.slider("Daily study hours", 1, 12, 3)
        weak  = st.text_input("Weak Topics (optional)", placeholder="e.g. UML Diagrams, Sorting Algorithms")

    style = st.radio("Study Style", ["Balanced", "Intensive (Exam Mode)", "Relaxed"], horizontal=True)

    if st.button("📅 Generate Study Plan", key="btn_plan"):
        if not exam_sub:
            st.warning("Please enter a subject.")
        else:
            with st.spinner("Creating your personalized study plan..."):
                system = (
                    "You are StudyMate study planner for university students. "
                    "Create a realistic day-by-day study plan in English. "
                    "Include daily topics, time allocation, revision days, tips. "
                    "Use clear Day-wise headings and bullets. Be practical."
                )
                query = (
                    f"Create {days}-day {style} study plan for '{exam_sub}'. "
                    f"Daily time: {hours} hours. Weak topics: {weak or 'none'}."
                )
                result = ask_groq(query, system, api_key, 2500)
            if result:
                st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)
                st.download_button("📥 Download Plan", result, file_name="study_plan.txt", key="dl_plan")

# ══════════════════════════════════════════════════════════════
#  💬  AI CHAT
# ══════════════════════════════════════════════════════════════
elif mode == "chat":
    st.markdown('<div class="section-title">💬 AI Study Assistant</div>', unsafe_allow_html=True)
    st.caption("Your AI-powered study assistant. Ask any question and get instant, detailed answers.")

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-label-user">You</div><div class="chat-message-user">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-label-ai">🎓 StudyMate</div><div class="chat-message-ai">{msg["content"]}</div>', unsafe_allow_html=True)

    user_msg = st.chat_input("Ask a study question...")
    if user_msg:
        st.session_state.chat_history.append({"role": "user", "content": user_msg})
        history_ctx = "\n".join(
            f"{'User' if m['role']=='user' else 'Assistant'}: {m['content']}"
            for m in st.session_state.chat_history[-6:]
        )
        system = (
            "You are StudyMate, a friendly AI study assistant for university students. "
            "Respond in clear English. Be helpful, concise, and encouraging."
        )
        with st.spinner("Thinking..."):
            reply = ask_groq(
                f"Conversation:\n{history_ctx}\n\nAnswer the user's latest message.",
                system, api_key, 1500
            )
        if reply:
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

# ─── FOOTER ────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#2d6a4f; font-size:0.8rem;'>"
    "StudyMate AI &nbsp;·&nbsp; Built by Huzaifa &nbsp;·&nbsp; Powered by OpenRouter AI"
    "</p>",
    unsafe_allow_html=True
)
