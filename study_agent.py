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
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; }
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
    background-clip: text; margin-bottom: 0.4rem;
}
.hero-subtitle { font-size: 1rem; color: #74c69d; opacity: 0.85; }

.section-title { font-size: 1.3rem; font-weight: 700; color: #52b788; margin-bottom: 1.2rem; }

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
.stSlider label, .stRadio label, .stFileUploader label, .stNumberInput label {
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
    padding: 0.65rem 0.8rem !important; font-size: 0.85rem !important; font-weight: 600 !important;
    font-family: 'Space Grotesk', sans-serif !important; cursor: pointer !important;
    transition: all 0.3s ease !important; white-space: nowrap !important; width: 100% !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important; box-shadow: 0 8px 25px rgba(82,183,136,0.4) !important;
}
.stDownloadButton > button {
    background: transparent !important; border: 1px solid rgba(82,183,136,0.4) !important;
    color: #74c69d !important; border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important; font-weight: 600 !important;
}
.stDownloadButton > button:hover { background: rgba(82,183,136,0.1) !important; }

.result-box {
    background: #071020; border: 1px solid rgba(82,183,136,0.25);
    border-left: 4px solid #52b788; border-radius: 12px;
    padding: 1.8rem; margin-top: 1.2rem; line-height: 1.8; color: #d1fae5;
}

/* Chat bubbles */
.chat-wrap { display: flex; flex-direction: column; gap: 1rem; margin-bottom: 1rem; }
.chat-user-row { display: flex; justify-content: flex-end; }
.chat-ai-row   { display: flex; justify-content: flex-start; }
.chat-bubble-user {
    background: linear-gradient(135deg, #2d6a4f, #1b4332);
    border-radius: 18px 18px 4px 18px; padding: 0.9rem 1.2rem;
    max-width: 75%; color: #d1fae5; font-size: 0.93rem; line-height: 1.6;
}
.chat-bubble-ai {
    background: #0d1a2e; border: 1px solid rgba(82,183,136,0.2);
    border-radius: 18px 18px 18px 4px; padding: 0.9rem 1.2rem;
    max-width: 80%; color: #e2e8f0; font-size: 0.93rem; line-height: 1.7;
}
.chat-name-user { font-size: 0.72rem; color: #74c69d; font-weight: 700; text-align: right; margin-bottom: 0.2rem; margin-right: 0.3rem; }
.chat-name-ai   { font-size: 0.72rem; color: #52b788; font-weight: 700; margin-bottom: 0.2rem; margin-left: 0.3rem; }

.quiz-q-num  { font-size: 0.72rem; color: #52b788; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
.quiz-q-text { font-size: 1rem; font-weight: 600; color: #e2e8f0; margin: 0.3rem 0 0.7rem; }

.score-badge {
    background: linear-gradient(135deg, #2d6a4f, #1b4332); border: 1px solid #52b788;
    border-radius: 12px; padding: 1.2rem 2rem; text-align: center;
    font-size: 1.5rem; font-weight: 700; color: #95d5b2; margin: 1rem 0;
}

[data-testid="stSidebar"] { background: #07111e !important; border-right: 1px solid rgba(82,183,136,0.15) !important; }
.stSlider > div > div > div > div { background: linear-gradient(90deg, #2d6a4f, #52b788) !important; }
.stAlert { background: rgba(82,183,136,0.08) !important; border: 1px solid rgba(82,183,136,0.25) !important; border-radius: 10px !important; }
hr { border-color: rgba(82,183,136,0.15) !important; }
.stTabs [data-baseweb="tab-list"] { background: transparent !important; gap: 0.5rem !important; }
.stTabs [data-baseweb="tab"] {
    background: #0d1a2e !important; border: 1px solid rgba(82,183,136,0.2) !important;
    border-radius: 10px !important; color: #74c69d !important; font-weight: 600 !important;
}
.stTabs [aria-selected="true"] { background: linear-gradient(135deg, #2d6a4f, #1b4332) !important; border-color: #52b788 !important; color: #d1fae5 !important; }
[data-testid="stMetricValue"] { color: #52b788 !important; font-weight: 700 !important; }
[data-testid="stMetricLabel"] { color: #74c69d !important; }
.stNumberInput > div > div > input {
    background: #0a1628 !important; border: 1px solid rgba(82,183,136,0.25) !important;
    border-radius: 10px !important; color: #e2e8f0 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session State ──────────────────────────────────────────────
def init():
    defaults = {
        "chat_history": [],       # [{role, content}]
        "explain_history": [],    # past explain results
        "summarize_history": [],  # past summarize results
        "quiz_questions": [],
        "quiz_answers": {},
        "quiz_submitted": False,
        "quiz_score": 0,
        "mode": "explain",
        "last_explain": None,
        "last_summary": None,
        "last_plan": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()

# ── API ────────────────────────────────────────────────────────
MODELS = [
    "openrouter/auto",
    "deepseek/deepseek-chat-v3-0324:free",
    "meta-llama/llama-3.2-3b-instruct:free",
    "qwen/qwen-2.5-7b-instruct:free",
]

def ask_ai(messages: list, api_key: str, max_tokens: int = 2000) -> str | None:
    if not api_key:
        st.error("⚠️ Service unavailable. Please contact admin.")
        return None

    for model in MODELS:
        try:
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": 0.7},
                timeout=45
            )
            data = r.json()
            if r.status_code == 200:
                return data["choices"][0]["message"]["content"]
            elif r.status_code == 429:
                time.sleep(1); continue
            else:
                continue
        except Exception:
            continue

    st.error("❌ Could not get a response. Please try again in a moment.")
    return None

# ── PDF ────────────────────────────────────────────────────────
def read_pdf(f) -> str:
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

# ── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 StudyMate AI")
    st.markdown("---")
    try:
        api_key = st.secrets["OPENROUTER_API_KEY"]
        st.success("✅ Connected")
    except Exception:
        api_key = None
        st.error("⚠️ Service unavailable.")

    st.markdown("---")
    st.markdown("### 📊 Stats")
    c1, c2 = st.columns(2)
    c1.metric("Messages", len(st.session_state.chat_history))
    c2.metric("Quiz Score", str(st.session_state.quiz_score))

    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()
    if st.button("🔄 Reset All"):
        for k in ["chat_history","explain_history","summarize_history",
                  "quiz_questions","quiz_answers","quiz_submitted",
                  "quiz_score","last_explain","last_summary","last_plan"]:
            st.session_state[k] = [] if "history" in k or "questions" in k or "answers" in k else (False if k=="quiz_submitted" else (0 if k=="quiz_score" else None))
        st.rerun()

    st.markdown("---")
    st.markdown("<p style='font-size:0.78rem;color:#52b788;'>Built by <b>Huzaifa</b> 🚀<br/>Powered by OpenRouter AI</p>", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <div class="hero-title">🎓 StudyMate AI</div>
    <div class="hero-subtitle">Your intelligent study companion — powered by AI, built for students.</div>
</div>
""", unsafe_allow_html=True)

# ── Mode Buttons ───────────────────────────────────────────────
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
#  💡  EXPLAIN
# ══════════════════════════════════════════════════════════════
if mode == "explain":
    st.markdown('<div class="section-title">💡 Topic Explainer</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        subject = st.selectbox("Subject", [
            "Computer Science", "Mathematics", "Physics", "Chemistry",
            "Biology", "History", "English", "Networking", "Software Engineering", "Other"
        ])
        topic = st.text_input("Enter Topic", placeholder="e.g. Newton's Laws, Network Topology, OOP Concepts",
                              value=st.session_state.get("last_explain_topic", ""))
    with col2:
        level = st.select_slider("Explanation Level", ["Basic", "Intermediate", "Advanced", "Expert"])
        lang  = st.selectbox("Language", ["English", "Simple English", "Urdu"])

    with st.expander("📄 Upload Reference Material (Optional)"):
        pdf_file = st.file_uploader("Upload PDF", type=["pdf"], key="explain_pdf")

    c1, c2 = st.columns([1, 4])
    with c1:
        generate = st.button("✨ Explain", key="btn_explain")
    with c2:
        if st.session_state.last_explain:
            if st.button("✏️ Edit & Re-generate", key="btn_re_explain"):
                st.session_state.last_explain = None
                st.rerun()

    if generate:
        if not topic and not pdf_file:
            st.warning("Please enter a topic or upload a PDF.")
        else:
            context = ""
            if pdf_file:
                with st.spinner("Reading PDF..."):
                    context = read_pdf(pdf_file)[:4000]

            with st.spinner("Generating explanation..."):
                messages = [
                    {"role": "system", "content": (
                        f"You are StudyMate, a professional AI study assistant. "
                        f"Respond in {lang}. Level: {level}. "
                        f"Structure: 1) Clear definition 2) Detailed explanation with real-world examples "
                        f"3) Key points in bullet form 4) Common exam question with answer tip. "
                        f"Be thorough, accurate, and encouraging."
                    )},
                    {"role": "user", "content": f"Explain '{topic}' from {subject}." + (f"\n\nReference:\n{context}" if context else "")}
                ]
                result = ask_ai(messages, api_key, 2000)

            if result:
                st.session_state.last_explain = result
                st.session_state.last_explain_topic = topic
                st.session_state.explain_history.append({"topic": topic, "result": result})

    # Show result with edit option
    if st.session_state.last_explain:
        st.markdown(f'<div class="result-box">{st.session_state.last_explain}</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.download_button("📥 Download Notes", st.session_state.last_explain,
                               file_name=f"{st.session_state.get('last_explain_topic','topic')}_notes.txt")
        with c2:
            if st.button("🔁 Follow-up Question", key="followup_explain"):
                st.session_state.mode = "chat"
                followup = f"I just read about '{st.session_state.get('last_explain_topic','')}'. Can you give me a quick recap and quiz me on it?"
                st.session_state.chat_history.append({"role": "user", "content": followup})
                st.rerun()

    # Past explanations
    if len(st.session_state.explain_history) > 1:
        with st.expander(f"📚 Past Explanations ({len(st.session_state.explain_history)})"):
            for i, item in enumerate(reversed(st.session_state.explain_history[:-1]), 1):
                st.markdown(f"**{i}. {item['topic']}**")
                st.markdown(item['result'][:300] + "...")
                st.markdown("---")

# ══════════════════════════════════════════════════════════════
#  📝  SUMMARIZE
# ══════════════════════════════════════════════════════════════
elif mode == "summarize":
    st.markdown('<div class="section-title">📝 Smart Summarizer</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["✏️ Paste Text", "📄 Upload PDF"])
    with tab1:
        notes = st.text_area("Your Notes", height=220, placeholder="Paste your study notes, textbook content, or any text here...")
    with tab2:
        pdf_up = st.file_uploader("Upload PDF", type=["pdf"], key="sum_pdf")
        notes_from_pdf = ""
        if pdf_up:
            with st.spinner("Extracting text from PDF..."):
                notes_from_pdf = read_pdf(pdf_up)
            st.success(f"✅ PDF loaded! ({len(notes_from_pdf):,} characters extracted)")

    col1, col2, col3 = st.columns(3)
    with col1:
        length = st.selectbox("Summary Length", ["Brief (5 Key Points)", "Standard (10 Points)", "Comprehensive"])
    with col2:
        lang2 = st.selectbox("Language", ["English", "Simple English", "Urdu"])
    with col3:
        focus = st.selectbox("Focus Area", ["Key Concepts", "Exam Preparation", "Definitions & Terms", "Complete Overview"])

    c1, c2 = st.columns([1, 4])
    with c1:
        summarize = st.button("📝 Summarize", key="btn_sum")
    with c2:
        if st.session_state.last_summary:
            if st.button("✏️ Edit & Re-summarize", key="btn_re_sum"):
                st.session_state.last_summary = None
                st.rerun()

    if summarize:
        raw = notes or notes_from_pdf
        if not raw.strip():
            st.warning("Please paste your notes or upload a PDF.")
        else:
            with st.spinner("Summarizing your content..."):
                messages = [
                    {"role": "system", "content": (
                        f"You are StudyMate, a professional AI study assistant. "
                        f"Summarize in {lang2}. Focus on {focus}. "
                        f"Format: clear headings, bullet points, bold key terms. "
                        f"Length: {length}. Make it concise and exam-ready."
                    )},
                    {"role": "user", "content": f"Summarize this:\n\n{raw[:6000]}"}
                ]
                result = ask_ai(messages, api_key, 2000)

            if result:
                st.session_state.last_summary = result
                st.session_state.summarize_history.append(result)

    if st.session_state.last_summary:
        st.markdown(f'<div class="result-box">{st.session_state.last_summary}</div>', unsafe_allow_html=True)
        st.download_button("📥 Download Summary", st.session_state.last_summary, file_name="summary.txt")

# ══════════════════════════════════════════════════════════════
#  ❓  QUIZ
# ══════════════════════════════════════════════════════════════
elif mode == "quiz":
    st.markdown('<div class="section-title">❓ Quiz Generator</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        quiz_topic  = st.text_input("Quiz Topic", placeholder="e.g. Object-Oriented Programming, World War II, Photosynthesis")
        num_q       = st.slider("Number of Questions", 3, 15, 5)
    with col2:
        difficulty  = st.select_slider("Difficulty", ["Easy", "Medium", "Hard", "Expert"])
        q_type      = st.selectbox("Question Type", ["Multiple Choice (MCQs)", "True / False", "Short Answer", "Mixed (All Types)"])

    if st.button("🎯 Generate Quiz", key="btn_quiz_gen"):
        if not quiz_topic:
            st.warning("Please enter a topic to generate a quiz.")
        else:
            with st.spinner("Building your quiz..."):
                messages = [
                    {"role": "system", "content": (
                        "You are StudyMate quiz generator. "
                        "Generate quiz ONLY as a valid JSON array. No extra text, no markdown. "
                        "Format: [{\"q\":\"Question text\",\"options\":[\"A) ...\",\"B) ...\",\"C) ...\",\"D) ...\"],\"answer\":\"A\",\"explanation\":\"Why A is correct\"}] "
                        "For True/False: options=[\"True\",\"False\"], answer=\"True\" or \"False\". "
                        "For Short Answer: options=[], answer=\"expected answer\". "
                        "Return ONLY the JSON array."
                    )},
                    {"role": "user", "content": f"Generate {num_q} {q_type} questions about '{quiz_topic}' at {difficulty} difficulty level."}
                ]
                raw = ask_ai(messages, api_key, 3000)

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

    # Render Quiz
    if st.session_state.quiz_questions:
        st.markdown("---")
        qs    = st.session_state.quiz_questions
        total = len(qs)

        # Progress bar
        answered = len([v for v in st.session_state.quiz_answers.values() if v])
        st.progress(answered / total, text=f"Progress: {answered}/{total} answered")
        st.markdown("")

        for i, q in enumerate(qs):
            with st.container():
                st.markdown(f'<div class="quiz-q-num">Question {i+1} of {total} · {difficulty}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="quiz-q-text">{q.get("q","")}</div>', unsafe_allow_html=True)
                opts = q.get("options", [])
                key  = f"q_{i}"
                if opts:
                    chosen = st.radio("Select your answer:", opts, key=key, index=None)
                    if chosen is not None:
                        letter = chosen.split(")")[0].strip() if ")" in chosen else chosen
                        st.session_state.quiz_answers[i] = letter
                else:
                    ans = st.text_input("Your answer:", key=key, placeholder="Type your answer here...")
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
                    st.session_state.quiz_score    = score
                    st.session_state.quiz_submitted = True
                    st.rerun()

        if st.session_state.quiz_submitted:
            score = st.session_state.quiz_score
            pct   = int(score / total * 100)
            emoji = "🏆" if pct >= 80 else "💪" if pct >= 60 else "📖"
            grade = "Excellent!" if pct >= 80 else "Good job!" if pct >= 60 else "Keep practicing!"

            st.markdown(f'<div class="score-badge">{emoji} {score}/{total} · {pct}% · {grade}</div>', unsafe_allow_html=True)

            with st.expander("📋 View Detailed Answer Key"):
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
                        st.info(f"💡 {explain}")
                    st.markdown("---")

            c1, c2 = st.columns(2)
            with c1:
                if st.button("🔄 New Quiz", key="btn_new_quiz"):
                    st.session_state.quiz_questions = []
                    st.session_state.quiz_answers   = {}
                    st.session_state.quiz_submitted  = False
                    st.rerun()
            with c2:
                if st.button("💬 Discuss Results with AI", key="discuss_quiz"):
                    st.session_state.mode = "chat"
                    msg = f"I just scored {score}/{total} ({pct}%) on a {quiz_topic} quiz at {difficulty} level. Can you help me understand the topics I got wrong and give me tips to improve?"
                    st.session_state.chat_history.append({"role": "user", "content": msg})
                    st.rerun()

# ══════════════════════════════════════════════════════════════
#  📅  STUDY PLAN
# ══════════════════════════════════════════════════════════════
elif mode == "plan":
    st.markdown('<div class="section-title">📅 Study Planner</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        exam_sub = st.text_input("Subject / Exam Name", placeholder="e.g. Software Engineering Final Exam")
        days     = st.number_input("Days until exam", min_value=1, max_value=365, value=7, step=1)
    with col2:
        hours = st.number_input("Daily study hours", min_value=1, max_value=24, value=3, step=1)
        weak  = st.text_input("Weak Topics (optional)", placeholder="e.g. UML Diagrams, Sorting Algorithms")

    col3, col4 = st.columns(2)
    with col3:
        style = st.selectbox("Study Style", ["Balanced", "Intensive (Exam Mode)", "Relaxed", "Weekend-Heavy"])
    with col4:
        goal = st.selectbox("Your Goal", ["Pass the exam", "Score above 70%", "Score above 85%", "Get full marks"])

    c1, c2 = st.columns([1, 4])
    with c1:
        plan_btn = st.button("📅 Generate Plan", key="btn_plan")
    with c2:
        if st.session_state.last_plan:
            if st.button("✏️ Edit & Regenerate", key="btn_re_plan"):
                st.session_state.last_plan = None
                st.rerun()

    if plan_btn:
        if not exam_sub:
            st.warning("Please enter a subject name.")
        else:
            with st.spinner("Creating your personalized study plan..."):
                messages = [
                    {"role": "system", "content": (
                        "You are StudyMate, a professional AI study planner for university students. "
                        "Create a detailed, realistic day-by-day study plan in English. "
                        "Include: specific topics per day, time slots, revision days, practice tests, and motivational tips. "
                        "Use clear Day headings and bullet points. Be practical and encouraging. "
                        "Make it look like a professional study schedule."
                    )},
                    {"role": "user", "content": (
                        f"Create a complete {days}-day {style} study plan for '{exam_sub}'. "
                        f"Daily available time: {hours} hours. "
                        f"Goal: {goal}. "
                        f"Weak areas to focus on: {weak or 'not specified'}. "
                        f"Make it detailed, realistic, and motivating."
                    )}
                ]
                result = ask_ai(messages, api_key, 3000)

            if result:
                st.session_state.last_plan = result

    if st.session_state.last_plan:
        st.markdown(f'<div class="result-box">{st.session_state.last_plan}</div>', unsafe_allow_html=True)
        st.download_button("📥 Download Study Plan", st.session_state.last_plan, file_name="study_plan.txt")

# ══════════════════════════════════════════════════════════════
#  💬  AI CHAT  (full context-aware conversation)
# ══════════════════════════════════════════════════════════════
elif mode == "chat":
    st.markdown('<div class="section-title">💬 AI Study Assistant</div>', unsafe_allow_html=True)
    st.caption("Ask anything — your full conversation history is used for context-aware answers.")

    # Render conversation
    if st.session_state.chat_history:
        st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(
                    f'<div class="chat-user-row"><div>'
                    f'<div class="chat-name-user">You</div>'
                    f'<div class="chat-bubble-user">{msg["content"]}</div>'
                    f'</div></div>', unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div class="chat-ai-row"><div>'
                    f'<div class="chat-name-ai">🎓 StudyMate AI</div>'
                    f'<div class="chat-bubble-ai">{msg["content"]}</div>'
                    f'</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("👋 Hello! Ask me anything — explain a topic, help with homework, quiz you, or discuss your study plan.")

    # Input
    user_msg = st.chat_input("Ask a study question, request an explanation, or say anything...")

    if user_msg:
        st.session_state.chat_history.append({"role": "user", "content": user_msg})

        # Build full message list with system prompt + all history
        messages = [
            {"role": "system", "content": (
                "You are StudyMate, a professional and friendly AI study assistant for university students. "
                "You have full memory of the conversation. Use past messages for context. "
                "Respond in clear, helpful English. Be detailed, accurate, and encouraging. "
                "If asked about a topic, explain it clearly with examples. "
                "If asked to quiz, generate questions. If asked to summarize, do so concisely. "
                "Always maintain conversation context from previous messages."
            )}
        ] + st.session_state.chat_history

        with st.spinner("Thinking..."):
            reply = ask_ai(messages, api_key, 2000)

        if reply:
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

# ── Footer ──────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#2d6a4f;font-size:0.8rem;'>"
    "StudyMate AI &nbsp;·&nbsp; Built by Huzaifa &nbsp;·&nbsp; Powered by OpenRouter AI"
    "</p>", unsafe_allow_html=True
)
