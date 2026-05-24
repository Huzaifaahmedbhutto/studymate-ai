import streamlit as st
import requests
import json
import time
import re
import random
from datetime import datetime, date
from io import BytesIO

st.set_page_config(
    page_title="StudyMate AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════
#  CSS — NATURE GREEN THEME + DARK/LIGHT MODE
# ═══════════════════════════════════════════════════════════════
def get_css(dark_mode=True):
    if dark_mode:
        bg        = "#060f0a"
        bg2       = "#0a1a10"
        bg3       = "#0d2118"
        card      = "#0f2318"
        border    = "rgba(82,183,136,0.2)"
        border2   = "rgba(82,183,136,0.4)"
        text      = "#d8f3dc"
        text2     = "#95d5b2"
        text3     = "#74c69d"
        muted     = "#4a7c6f"
        sidebar   = "#060f0a"
        input_bg  = "#0a1a10"
        bubble_ai = "#0f2318"
        result_bg = "#071410"
    else:
        bg        = "#f0faf4"
        bg2       = "#e8f5ee"
        bg3       = "#d8ede0"
        card      = "#ffffff"
        border    = "rgba(45,106,79,0.2)"
        border2   = "rgba(45,106,79,0.5)"
        text      = "#1b4332"
        text2     = "#2d6a4f"
        text3     = "#40916c"
        muted     = "#74c69d"
        sidebar   = "#e8f5ee"
        input_bg  = "#ffffff"
        bubble_ai = "#f0faf4"
        result_bg = "#ffffff"

    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap');

*, *::before, *::after {{ box-sizing: border-box; }}
html, body, .stApp {{ background: {bg} !important; color: {text} !important; font-family: 'Inter', sans-serif !important; }}
#MainMenu, footer, header {{ visibility: hidden; }}
.stDeployButton {{ display: none; }}
::-webkit-scrollbar {{ width: 5px; }}
::-webkit-scrollbar-thumb {{ background: linear-gradient(#52b788, #2d6a4f); border-radius: 10px; }}
.main .block-container {{ padding: 1.5rem 2rem !important; max-width: 1300px; }}

/* HERO */
.hero {{
    background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 40%, #40916c 100%);
    border: 1px solid {border2}; border-radius: 24px;
    padding: 3rem; margin-bottom: 1.5rem;
    position: relative; overflow: hidden; text-align: center;
}}
.hero::before {{
    content: ''; position: absolute; inset: 0;
    background: radial-gradient(ellipse at 20% 50%, rgba(116,198,157,0.3) 0%, transparent 60%),
                radial-gradient(ellipse at 80% 50%, rgba(82,183,136,0.2) 0%, transparent 60%);
    pointer-events: none;
}}
.hero::after {{
    content: '🌿'; position: absolute; top: 1rem; right: 2rem;
    font-size: 4rem; opacity: 0.15; transform: rotate(20deg);
}}
.hero-badge {{
    display: inline-block; background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.3); border-radius: 20px;
    padding: 0.3rem 1rem; font-size: 0.78rem; font-weight: 700;
    color: #d8f3dc; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 1rem;
}}
.hero-title {{
    font-size: 3rem; font-weight: 900;
    background: linear-gradient(135deg, #ffffff 0%, #d8f3dc 50%, #b7e4c7 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; letter-spacing: -1.5px; line-height: 1.1; margin-bottom: 0.8rem;
}}
.hero-sub {{ font-size: 1rem; color: #b7e4c7; max-width: 500px; margin: 0 auto 1.5rem; line-height: 1.6; }}
.hero-stats {{ display: flex; justify-content: center; gap: 2.5rem; flex-wrap: wrap; }}
.hero-stat-num {{ font-size: 1.5rem; font-weight: 800; color: #ffffff; }}
.hero-stat-label {{ font-size: 0.72rem; color: #95d5b2; text-transform: uppercase; letter-spacing: 1px; }}

/* STREAK BANNER */
.streak-banner {{
    background: linear-gradient(135deg, #1b4332, #2d6a4f);
    border: 1px solid {border2}; border-radius: 14px;
    padding: 0.8rem 1.2rem; margin-bottom: 1.2rem;
    display: flex; align-items: center; gap: 0.8rem;
    font-size: 0.9rem; color: {text2}; font-weight: 600;
}}

/* BUTTONS */
.stButton > button {{
    background: linear-gradient(135deg, #2d6a4f, #52b788) !important;
    color: #fff !important; border: none !important; border-radius: 12px !important;
    padding: 0.7rem 1rem !important; font-size: 0.85rem !important;
    font-weight: 700 !important; font-family: 'Inter', sans-serif !important;
    transition: all 0.3s ease !important; white-space: nowrap !important; width: 100% !important;
}}
.stButton > button:hover {{
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 30px rgba(82,183,136,0.4) !important;
    filter: brightness(1.1) !important;
}}
.stDownloadButton > button {{
    background: transparent !important;
    border: 2px solid {border2} !important; color: {text3} !important;
    border-radius: 12px !important; font-weight: 600 !important; transition: all 0.3s !important;
}}
.stDownloadButton > button:hover {{ background: rgba(82,183,136,0.1) !important; }}

/* INPUTS */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div,
.stNumberInput > div > div > input {{
    background: {input_bg} !important; border: 1.5px solid {border} !important;
    border-radius: 12px !important; color: {text} !important;
    font-family: 'Inter', sans-serif !important; transition: all 0.2s !important;
}}
.stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {{
    border-color: #52b788 !important; box-shadow: 0 0 0 4px rgba(82,183,136,0.15) !important;
}}
.stTextInput label, .stTextArea label, .stSelectbox label,
.stSlider label, .stRadio label, .stNumberInput label, .stFileUploader label {{
    color: {text2} !important; font-weight: 600 !important;
    font-size: 0.83rem !important; text-transform: uppercase !important; letter-spacing: 0.5px !important;
}}

/* CARDS */
.result-box {{
    background: {result_bg}; border: 1px solid {border};
    border-left: 5px solid #52b788; border-radius: 16px;
    padding: 2rem; margin-top: 1.5rem; line-height: 1.9;
    color: {text}; box-shadow: 0 10px 40px rgba(82,183,136,0.1);
}}
.section-title {{
    font-size: 1.4rem; font-weight: 800; color: {text2};
    margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.5rem;
}}
.glass-card {{
    background: {card}; border: 1px solid {border};
    border-radius: 20px; padding: 1.5rem; margin-bottom: 1rem;
    box-shadow: 0 4px 20px rgba(82,183,136,0.08);
}}

/* CHAT */
.msg-user-wrap {{ display: flex; justify-content: flex-end; gap: 0.5rem; margin: 0.8rem 0; }}
.msg-ai-wrap   {{ display: flex; justify-content: flex-start; gap: 0.5rem; margin: 0.8rem 0; }}
.msg-avatar {{ width: 34px; height: 34px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1rem; flex-shrink: 0; }}
.msg-avatar-user {{ background: linear-gradient(135deg, #2d6a4f, #52b788); }}
.msg-avatar-ai   {{ background: {bg3}; border: 1px solid {border}; }}
.msg-bubble-user {{
    background: linear-gradient(135deg, #2d6a4f, #40916c);
    border-radius: 20px 20px 6px 20px; padding: 0.9rem 1.3rem; max-width: 72%;
    color: #fff; font-size: 0.93rem; line-height: 1.6;
    box-shadow: 0 6px 20px rgba(45,106,79,0.35);
}}
.msg-bubble-ai {{
    background: {bubble_ai}; border: 1px solid {border};
    border-radius: 20px 20px 20px 6px; padding: 0.9rem 1.3rem; max-width: 78%;
    color: {text}; font-size: 0.93rem; line-height: 1.7;
}}
.msg-name {{ font-size: 0.7rem; font-weight: 700; margin-bottom: 0.3rem; }}

/* QUIZ */
.quiz-card {{
    background: {card}; border: 1px solid {border};
    border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem;
    transition: border-color 0.2s, box-shadow 0.2s;
}}
.quiz-card:hover {{ border-color: {border2}; box-shadow: 0 8px 25px rgba(82,183,136,0.15); }}
.quiz-num {{ font-size: 0.7rem; color: #52b788; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; }}
.quiz-q   {{ font-size: 1.05rem; font-weight: 700; color: {text}; margin: 0.5rem 0 1rem; }}

/* SCORE */
.score-box {{
    background: linear-gradient(135deg, #1b4332, #2d6a4f);
    border: 2px solid #52b788; border-radius: 20px;
    padding: 2.5rem; text-align: center; margin: 1.5rem 0;
    box-shadow: 0 20px 60px rgba(82,183,136,0.3);
}}
.score-emoji {{ font-size: 3.5rem; margin-bottom: 0.5rem; }}
.score-num   {{ font-size: 2.8rem; font-weight: 900; color: #fff; }}
.score-pct   {{ font-size: 1.1rem; color: #95d5b2; font-weight: 600; }}
.score-grade {{ font-size: 0.9rem; color: #b7e4c7; margin-top: 0.3rem; }}

/* POMODORO */
.pomo-timer {{
    background: linear-gradient(135deg, #1b4332, #2d6a4f);
    border: 2px solid #52b788; border-radius: 50%;
    width: 220px; height: 220px; margin: 1.5rem auto;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    box-shadow: 0 0 60px rgba(82,183,136,0.4), inset 0 0 30px rgba(82,183,136,0.1);
}}
.pomo-time {{ font-size: 3rem; font-weight: 900; color: #fff; font-family: 'JetBrains Mono', monospace; }}
.pomo-label {{ font-size: 0.8rem; color: #95d5b2; text-transform: uppercase; letter-spacing: 2px; }}

/* FLASHCARD */
.flashcard {{
    background: linear-gradient(135deg, {bg3}, {bg2});
    border: 2px solid {border2}; border-radius: 24px;
    padding: 3rem 2rem; text-align: center; min-height: 220px;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    cursor: pointer; transition: all 0.3s ease;
    box-shadow: 0 15px 40px rgba(82,183,136,0.2);
}}
.flashcard:hover {{ transform: translateY(-5px); box-shadow: 0 25px 60px rgba(82,183,136,0.3); }}
.flashcard-q {{ font-size: 1.2rem; font-weight: 700; color: {text}; }}
.flashcard-a {{ font-size: 1rem; color: #52b788; margin-top: 1rem; line-height: 1.6; }}

/* VOCAB */
.vocab-card {{
    background: {card}; border: 1px solid {border};
    border-left: 4px solid #52b788; border-radius: 12px;
    padding: 1rem 1.2rem; margin-bottom: 0.8rem;
}}
.vocab-word {{ font-size: 1.1rem; font-weight: 800; color: {text2}; }}
.vocab-type {{ font-size: 0.75rem; color: {muted}; font-style: italic; }}
.vocab-def  {{ font-size: 0.9rem; color: {text}; margin-top: 0.3rem; line-height: 1.5; }}
.vocab-ex   {{ font-size: 0.83rem; color: {text3}; margin-top: 0.3rem; font-style: italic; }}

/* DASHBOARD */
.dash-card {{
    background: {card}; border: 1px solid {border}; border-radius: 16px;
    padding: 1.5rem; text-align: center;
    box-shadow: 0 4px 20px rgba(82,183,136,0.08);
}}
.dash-num   {{ font-size: 2.2rem; font-weight: 900; color: #52b788; }}
.dash-label {{ font-size: 0.78rem; color: {muted}; text-transform: uppercase; letter-spacing: 1px; }}

/* PROGRESS */
.stProgress > div > div > div > div {{
    background: linear-gradient(90deg, #2d6a4f, #52b788, #74c69d) !important;
    border-radius: 10px !important;
}}

/* SIDEBAR */
[data-testid="stSidebar"] {{
    background: {sidebar} !important;
    border-right: 1px solid {border} !important;
}}

/* RADIO */
.stRadio > div {{ gap: 0.5rem !important; flex-wrap: wrap !important; }}
.stRadio > div > label {{
    background: {input_bg} !important; border: 1.5px solid {border} !important;
    border-radius: 10px !important; padding: 0.5rem 1rem !important;
    color: {text} !important; transition: all 0.2s !important; font-weight: 500 !important;
}}
.stRadio > div > label:hover {{ border-color: #52b788 !important; }}

/* TABS */
.stTabs [data-baseweb="tab-list"] {{ background: transparent !important; gap: 0.5rem !important; }}
.stTabs [data-baseweb="tab"] {{
    background: {input_bg} !important; border: 1px solid {border} !important;
    border-radius: 10px !important; color: {muted} !important; font-weight: 600 !important;
}}
.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, #2d6a4f, #1b4332) !important;
    border-color: #52b788 !important; color: #fff !important;
}}

.stAlert {{ background: rgba(82,183,136,0.08) !important; border: 1px solid {border} !important; border-radius: 12px !important; }}
hr {{ border-color: {border} !important; }}
[data-testid="stMetricValue"] {{ color: #52b788 !important; font-weight: 800 !important; }}
[data-testid="stMetricLabel"] {{ color: {muted} !important; }}

/* TIP */
.tip-card {{
    background: rgba(82,183,136,0.08); border: 1px solid {border};
    border-radius: 12px; padding: 0.8rem 1rem; margin: 0.5rem 0;
    font-size: 0.85rem; color: {text2}; line-height: 1.5;
}}
</style>"""

# ── Init ──────────────────────────────────────────────────────
def init():
    today_str = str(date.today())
    defaults = {
        "dark_mode": True,
        "language": "English",
        "mode": "explain",
        "chat_history": [],
        "explain_history": [],
        "last_explain": None, "last_explain_topic": "", "last_explain_subject": "",
        "last_summary": None,
        "last_plan": None,
        "quiz_questions": [], "quiz_answers": {}, "quiz_submitted": False, "quiz_score": 0,
        "best_quiz": 0,
        "flashcards": [], "fc_index": 0, "fc_show_answer": False,
        "vocab_list": [],
        # Pomodoro
        "pomo_mode": "study",
        "pomo_running": False,
        "pomo_start": None,
        "pomo_elapsed": 0,
        "pomo_sessions": 0,
        "pomo_study_mins": 25,
        "pomo_break_mins": 5,
        # Stats
        "total_queries": 0,
        "total_quizzes": 0,
        "topics_studied": 0,
        "flashcards_reviewed": 0,
        # Streak
        "streak_days": 0,
        "last_active": today_str,
        "streak_history": [today_str],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # Update streak
    today = date.today()
    last  = date.fromisoformat(st.session_state.last_active)
    delta = (today - last).days
    if delta == 1:
        st.session_state.streak_days  += 1
        st.session_state.last_active   = today_str
        if today_str not in st.session_state.streak_history:
            st.session_state.streak_history.append(today_str)
    elif delta > 1:
        st.session_state.streak_days  = 1
        st.session_state.last_active   = today_str
    # delta == 0 → same day, no change

init()

# Apply CSS
st.markdown(get_css(st.session_state.dark_mode), unsafe_allow_html=True)

# ── API ───────────────────────────────────────────────────────
MODELS = [
    "openrouter/auto",
    "deepseek/deepseek-chat-v3-0324:free",
    "meta-llama/llama-3.2-3b-instruct:free",
    "qwen/qwen-2.5-7b-instruct:free",
]

try:
    API_KEY = st.secrets["OPENROUTER_API_KEY"]
except Exception:
    API_KEY = None

def ask_ai(messages, max_tokens=2500):
    if not API_KEY:
        st.error("⚠️ Service unavailable. Please contact admin.")
        return None
    for model in MODELS:
        try:
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://studymateai.academy",
                    "X-Title": "StudyMate AI"
                },
                json={"model": model, "messages": messages,
                      "max_tokens": max_tokens, "temperature": 0.75},
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
    st.error("❌ Could not get response. Please try again.")
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
        return f"Error reading PDF: {e}"

# ── Language prompts ──────────────────────────────────────────
LANG = st.session_state.language
LANG_MAP = {
    "English":                    "Respond in clear, professional English.",
    "Simple English":             "Respond in very simple English. Short sentences, basic vocabulary. Explain like to a 15-year-old.",
    "Urdu (اردو)":               "اردو میں جواب دیں۔ واضح اور سادہ اردو استعمال کریں۔",
    "Roman Urdu":                 "Roman Urdu mein jawab dein. Easy aur friendly andaaz mein likhein.",
    "Arabic (العربية)":           "أجب باللغة العربية الواضحة والسهلة.",
    "Hindi (हिन्दी)":            "हिंदी में जवाब दें। सरल और स्पष्ट भाषा का उपयोग करें।",
    "Bengali (বাংলা)":           "বাংলায় উত্তর দিন। সহজ ও স্পষ্ট ভাষা ব্যবহার করুন।",
    "French (Français)":          "Répondez en français clair et professionnel.",
    "Spanish (Español)":          "Responde en español claro y profesional.",
    "Portuguese (Português)":     "Responda em português claro e profissional.",
    "German (Deutsch)":           "Antworte auf klarem, professionellem Deutsch.",
    "Turkish (Türkçe)":           "Açık ve profesyonel Türkçe ile yanıt verin.",
    "Malay (Bahasa Melayu)":      "Jawab dalam Bahasa Melayu yang jelas dan mudah difahami.",
    "Indonesian (Bahasa Indonesia)": "Jawab dalam Bahasa Indonesia yang jelas dan profesional.",
    "Swahili (Kiswahili)":        "Jibu kwa Kiswahili wazi na rahisi kuelewa.",
    "Hausa":                      "Ka amsa da Hausa mai sauƙi da bayyananne.",
    "Yoruba":                     "Dahun ni Yorùbá tó ṣe kedere àti tó rọrùn.",
    "Amharic (አማርኛ)":           "በግልጽ እና ቀላል አማርኛ ይመልሱ።",
    "Persian/Farsi (فارسی)":     "به فارسی واضح و ساده پاسخ دهید.",
    "Pashto (پښتو)":             "د پښتو ژبې په واضح او اسانه بڼه ځواب ورکړئ.",
    "Sindhi (سنڌي)":             "واضح ۽ سادي سنڌيءَ ۾ جواب ڏيو.",
    "Punjabi (ਪੰਜਾਬੀ)":         "ਸਾਫ਼ ਅਤੇ ਆਸਾਨ ਪੰਜਾਬੀ ਵਿੱਚ ਜਵਾਬ ਦਿਓ।",
    "Tamil (தமிழ்)":             "தெளிவான மற்றும் எளிய தமிழில் பதிலளிக்கவும்.",
    "Chinese (中文)":             "请用清晰、专业的中文回答。",
    "Japanese (日本語)":          "明確でわかりやすい日本語で答えてください。",
    "Korean (한국어)":            "명확하고 전문적인 한국어로 답변해 주세요.",
    "Russian (Русский)":          "Отвечайте на чётком и профессиональном русском языке.",
    "Italian (Italiano)":         "Rispondi in italiano chiaro e professionale.",
    "Dutch (Nederlands)":         "Antwoord in duidelijk en professioneel Nederlands.",
    "Swedish (Svenska)":          "Svara på tydlig och professionell svenska.",
}
LANG_INSTRUCTION = LANG_MAP.get(LANG, f"Respond in {LANG}. Be clear and professional.")

# ── TIPS ─────────────────────────────────────────────────────
TIPS = [
    "🧠 **Spaced Repetition** — Review after 1 day, 3 days, 1 week for long-term memory.",
    "⏱️ **Pomodoro** — 25 min study + 5 min break = maximum focus!",
    "✍️ **Active Recall** — Close the book and write what you remember.",
    "🎯 **Feynman Technique** — Explain it simply. Gaps = what to study more.",
    "🌙 **Sleep** — Your brain consolidates memories during sleep. Don't skip it!",
    "📝 **Mind Maps** — Draw visual connections between concepts.",
    "🔇 **No Distractions** — Phone in another room while studying.",
    "🎵 **Lo-fi Music** — Instrumental music can boost focus and reduce stress.",
]

# ══════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    # Dark/Light toggle
    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.markdown("## 🌿 StudyMate AI")
    with col_b:
        if st.button("🌙" if st.session_state.dark_mode else "☀️", key="theme_toggle"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    st.markdown("---")

    # Connection status
    if API_KEY:
        st.markdown("""<div style='background:rgba(82,183,136,0.12);border:1px solid rgba(82,183,136,0.3);
        border-radius:10px;padding:0.7rem;text-align:center;'>
        <span style='color:#52b788;font-weight:700;'>⚡ AI Connected</span><br>
        <span style='font-size:0.75rem;opacity:0.7;'>Ready to help you study</span></div>""",
        unsafe_allow_html=True)
    else:
        st.error("⚠️ Service unavailable.")

    st.markdown("---")

    # Language selector
    LANGUAGES = [
        "English", "Simple English",
        "Urdu (اردو)", "Roman Urdu",
        "Arabic (العربية)", "Hindi (हिन्दी)", "Bengali (বাংলা)",
        "French (Français)", "Spanish (Español)", "Portuguese (Português)",
        "German (Deutsch)", "Turkish (Türkçe)", "Malay (Bahasa Melayu)",
        "Indonesian (Bahasa Indonesia)", "Swahili (Kiswahili)",
        "Hausa", "Yoruba", "Amharic (አማርኛ)",
        "Persian/Farsi (فارسی)", "Pashto (پښتو)", "Sindhi (سنڌي)",
        "Punjabi (ਪੰਜਾਬੀ)", "Tamil (தமிழ்)", "Chinese (中文)",
        "Japanese (日本語)", "Korean (한국어)", "Russian (Русский)",
        "Italian (Italiano)", "Dutch (Nederlands)", "Swedish (Svenska)",
    ]
    curr_idx = LANGUAGES.index(st.session_state.language) if st.session_state.language in LANGUAGES else 0
    st.session_state.language = st.selectbox("🌍 Response Language", LANGUAGES, index=curr_idx)

    st.markdown("---")

    # Streak
    streak = st.session_state.streak_days
    fire   = "🔥" * min(streak, 5) if streak > 0 else "❄️"
    st.markdown(f"""<div style='background:rgba(82,183,136,0.1);border:1px solid rgba(82,183,136,0.25);
    border-radius:12px;padding:0.8rem;text-align:center;margin-bottom:0.5rem;'>
    <div style='font-size:1.5rem;'>{fire}</div>
    <div style='font-weight:800;font-size:1.2rem;color:#52b788;'>{streak} Day Streak</div>
    <div style='font-size:0.72rem;opacity:0.6;'>Keep studying daily!</div></div>""",
    unsafe_allow_html=True)

    # Stats
    st.markdown("### 📊 Your Stats")
    c1, c2 = st.columns(2)
    c1.metric("Queries",  st.session_state.total_queries)
    c2.metric("Quizzes",  st.session_state.total_quizzes)
    c1.metric("Topics",   st.session_state.topics_studied)
    c2.metric("Best Quiz",f"{st.session_state.best_quiz}pts")

    st.markdown("---")

    # Tip
    st.markdown("### 💡 Study Tip")
    st.markdown(f"<div class='tip-card'>{random.choice(TIPS)}</div>", unsafe_allow_html=True)

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
    with c2:
        if st.button("🔄 Reset All"):
            keys_keep = {"dark_mode","language","streak_days","last_active","streak_history","best_quiz"}
            for k in list(st.session_state.keys()):
                if k not in keys_keep:
                    del st.session_state[k]
            st.rerun()

    st.markdown("---")
    st.markdown("<p style='font-size:0.73rem;opacity:0.5;text-align:center;'>Built with ❤️ by <b>Huzaifa</b><br/>Powered by OpenRouter AI</p>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="hero">
    <div class="hero-badge">✦ AI-Powered Learning Platform</div>
    <div class="hero-title">Study Smarter.<br>Grow Every Day.</div>
    <div class="hero-sub">Your personal AI tutor — available 24/7, supporting {LANG}.</div>
    <div class="hero-stats">
        <div class="hero-stat"><div class="hero-stat-num">{st.session_state.total_queries}</div><div class="hero-stat-label">Queries</div></div>
        <div class="hero-stat"><div class="hero-stat-num">{st.session_state.streak_days}🔥</div><div class="hero-stat-label">Day Streak</div></div>
        <div class="hero-stat"><div class="hero-stat-num">7</div><div class="hero-stat-label">AI Tools</div></div>
        <div class="hero-stat"><div class="hero-stat-num">∞</div><div class="hero-stat-label">Topics</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── MODE BUTTONS ─────────────────────────────────────────────
MODES = {
    "explain":   ("💡", "Explain"),
    "summarize": ("📝", "Summarize"),
    "quiz":      ("❓", "Quiz"),
    "flashcard": ("🃏", "Flashcards"),
    "vocab":     ("📖", "Vocabulary"),
    "plan":      ("📅", "Study Plan"),
    "pomodoro":  ("⏱️", "Pomodoro"),
    "dashboard": ("📊", "Dashboard"),
    "chat":      ("💬", "AI Chat"),
}
cols = st.columns(len(MODES))
for col, (key, (icon, label)) in zip(cols, MODES.items()):
    with col:
        if st.button(f"{icon}\n{label}", key=f"mode_{key}"):
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
        subject = st.selectbox("Subject", ["Computer Science","Mathematics","Physics","Chemistry",
            "Biology","History","English","Networking","Software Engineering",
            "Economics","Psychology","Statistics","Accounting","Law","Other"])
        topic = st.text_input("What do you want to learn?",
            placeholder="e.g. Binary Search Trees, Newton's Laws, French Revolution...",
            value=st.session_state.last_explain_topic)
    with col2:
        level = st.select_slider("Depth Level", ["Basic","Intermediate","Advanced","Expert"])
        explain_style = st.selectbox("Explanation Style", [
            "Structured (Headings & Bullets)",
            "Story-based (Narrative)",
            "Example-heavy",
            "Compare & Contrast",
        ])

    with st.expander("📎 Attach Reference Material (Optional)"):
        pdf_file     = st.file_uploader("Upload PDF", type=["pdf"], key="explain_pdf")
        extra_context= st.text_area("Or paste extra context:", height=80,
                                    placeholder="Any additional notes or context...")

    c1, c2, c3 = st.columns([2, 2, 3])
    with c1:
        generate = st.button("✨ Explain Now", key="btn_explain")
    with c2:
        if st.session_state.last_explain:
            if st.button("✏️ Edit Request", key="btn_re_explain"):
                st.session_state.last_explain = None
                st.rerun()

    if generate:
        if not topic.strip() and not pdf_file:
            st.warning("Please enter a topic.")
        else:
            context = extra_context or ""
            if pdf_file:
                with st.spinner("Reading PDF..."):
                    context += "\n" + read_pdf(pdf_file)[:4000]
            with st.spinner("🌿 Generating explanation..."):
                style_prompt = {
                    "Structured (Headings & Bullets)": "Use clear headings and bullet points.",
                    "Story-based (Narrative)": "Explain as an engaging story or narrative.",
                    "Example-heavy": "Use many real-world examples and analogies.",
                    "Compare & Contrast": "Compare with related concepts to explain differences.",
                }.get(explain_style, "")
                messages = [
                    {"role":"system","content":(
                        f"You are StudyMate, an expert AI tutor. {LANG_INSTRUCTION} Level: {level}. "
                        f"{style_prompt} "
                        "Format: **🔍 Definition** | **📖 Explanation** | **⚡ Key Points** (bullets) | "
                        "**🎯 Exam Tips** | **❓ Practice Question** with hint. Be thorough and engaging."
                    )},
                    {"role":"user","content":f"Explain '{topic}' from {subject} at {level} level." +
                     (f"\n\nContext:\n{context}" if context.strip() else "")}
                ]
                result = ask_ai(messages, 2500)
            if result:
                st.session_state.last_explain = result
                st.session_state.last_explain_topic   = topic
                st.session_state.last_explain_subject = subject
                st.session_state.explain_history.append({"topic":topic,"subject":subject,"result":result})
                st.session_state.topics_studied += 1

    if st.session_state.last_explain:
        st.markdown(f'<div class="result-box">{st.session_state.last_explain}</div>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.download_button("📥 Download (.txt)", st.session_state.last_explain,
                               file_name=f"{st.session_state.last_explain_topic}_notes.txt")
        with c2:
            # HTML export for print-as-PDF
            html_export = f"""<!DOCTYPE html><html><head><meta charset='UTF-8'>
            <style>body{{font-family:Georgia,serif;max-width:800px;margin:40px auto;line-height:1.8;color:#1b4332;}}
            h1{{color:#2d6a4f;}}pre{{white-space:pre-wrap;}}</style></head><body>
            <h1>📚 {st.session_state.last_explain_topic}</h1>
            <h3>{st.session_state.last_explain_subject}</h3><hr>
            <pre>{st.session_state.last_explain}</pre>
            <footer style='margin-top:40px;color:#74c69d;font-size:0.85rem;'>Generated by StudyMate AI</footer>
            </body></html>"""
            st.download_button("🖨️ Export (HTML/PDF)", html_export,
                               file_name=f"{st.session_state.last_explain_topic}.html",
                               mime="text/html")
        with c3:
            if st.button("🃏 Make Flashcards", key="make_fc"):
                st.session_state.mode = "flashcard"
                st.session_state["pending_fc_topic"] = st.session_state.last_explain_topic
                st.rerun()
        with c4:
            if st.button("❓ Quiz Me", key="quiz_this"):
                st.session_state.mode = "quiz"
                st.session_state["pending_quiz_topic"] = st.session_state.last_explain_topic
                st.rerun()

    if len(st.session_state.explain_history) > 1:
        with st.expander(f"📚 History ({len(st.session_state.explain_history)} topics)"):
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
        notes = st.text_area("Your Notes / Content", height=250,
                             placeholder="Paste lecture notes, textbook chapters, articles, anything...")
    with tab2:
        pdf_up = st.file_uploader("Upload PDF", type=["pdf"], key="sum_pdf")
        notes_from_pdf = ""
        if pdf_up:
            with st.spinner("Extracting text..."):
                notes_from_pdf = read_pdf(pdf_up)
            st.success(f"✅ {len(notes_from_pdf):,} characters extracted!")

    col1, col2, col3 = st.columns(3)
    with col1:
        length = st.selectbox("Style", ["Quick (5 Key Points)","Standard (10 Points)",
                                         "Detailed (Full Notes)","One-liner TL;DR"])
    with col2:
        focus  = st.selectbox("Focus", ["Key Concepts","Exam Preparation",
                                         "Definitions & Terms","Timeline / Process","Complete Overview"])
    with col3:
        output_format = st.selectbox("Format", ["Bullet Points","Numbered List",
                                                  "Mind Map Text","Table Format","Paragraph"])

    c1, c2 = st.columns([2, 2])
    with c1:
        if st.button("⚡ Summarize Now", key="btn_sum"):
            raw = notes or notes_from_pdf
            if not raw.strip():
                st.warning("Please paste notes or upload a PDF.")
            else:
                with st.spinner("🌿 Summarizing..."):
                    messages = [
                        {"role":"system","content":(
                            f"You are StudyMate expert summarizer. {LANG_INSTRUCTION} "
                            f"Create a {length} summary focusing on {focus}. "
                            f"Use {output_format} format. Bold key terms. "
                            "End with '🎯 Key Takeaways' (3 most important points). Make it exam-ready."
                        )},
                        {"role":"user","content":f"Summarize:\n\n{raw[:8000]}"}
                    ]
                    result = ask_ai(messages, 2500)
                if result:
                    st.session_state.last_summary = result
    with c2:
        if st.session_state.last_summary:
            if st.button("✏️ Re-summarize", key="btn_re_sum"):
                st.session_state.last_summary = None
                st.rerun()

    if st.session_state.last_summary:
        st.markdown(f'<div class="result-box">{st.session_state.last_summary}</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button("📥 Download", st.session_state.last_summary, file_name="summary.txt")
        with c2:
            html_sum = f"<html><body style='font-family:Georgia;max-width:800px;margin:40px auto;line-height:1.8;'><h1>Summary</h1><pre>{st.session_state.last_summary}</pre></body></html>"
            st.download_button("🖨️ Export HTML", html_sum, file_name="summary.html", mime="text/html")
        with c3:
            if st.button("❓ Quiz On This", key="quiz_summary"):
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
        quiz_topic = st.text_input("Topic", value=pending or "",
                                   placeholder="Any topic — no limits!")
        num_q      = st.number_input("Number of Questions (unlimited)", min_value=1, max_value=10000, value=10, step=1)
    with col2:
        difficulty = st.select_slider("Difficulty", ["Very Easy","Easy","Medium","Hard","Expert","Mixed"])
        q_type     = st.selectbox("Format", ["Multiple Choice","True/False","Short Answer",
                                              "Fill in the Blank","Mixed (All Types)"])

    if st.button("🚀 Generate Quiz", key="btn_quiz_gen"):
        if not quiz_topic.strip():
            st.warning("Please enter a topic.")
        else:
            with st.spinner("🌿 Building quiz..."):
                messages = [
                    {"role":"system","content":(
                        "You are an expert quiz generator. Return ONLY a valid JSON array, nothing else. "
                        'Format: [{"q":"Question","options":["A) ...","B) ...","C) ...","D) ..."],"answer":"A","explanation":"Why"}] '
                        "True/False: options=['True','False']. Short/Fill: options=[], answer='text'. "
                        f"{LANG_INSTRUCTION}"
                    )},
                    {"role":"user","content":f"Generate {num_q} {q_type} questions on '{quiz_topic}' at {difficulty} level."}
                ]
                raw = ask_ai(messages, 4000)
            if raw:
                try:
                    clean     = re.sub(r"```json|```","",raw).strip()
                    questions = json.loads(clean)
                    st.session_state.quiz_questions  = questions
                    st.session_state.quiz_answers    = {}
                    st.session_state.quiz_submitted   = False
                    st.session_state.total_quizzes   += 1
                    st.rerun()
                except Exception:
                    st.markdown(f'<div class="result-box">{raw}</div>', unsafe_allow_html=True)

    if st.session_state.quiz_questions:
        qs      = st.session_state.quiz_questions
        total   = len(qs)
        answered= len([v for v in st.session_state.quiz_answers.values() if v])
        st.progress(answered/total if total else 0, text=f"{answered}/{total} answered")
        st.markdown("")

        for i, q in enumerate(qs):
            st.markdown(f'<div class="quiz-num">Question {i+1} of {total} · {difficulty}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="quiz-q">{q.get("q","")}</div>', unsafe_allow_html=True)
            opts = q.get("options",[])
            key  = f"q_{i}"
            if opts:
                chosen = st.radio("", opts, key=key, index=None, horizontal=len(opts)==2)
                if chosen:
                    st.session_state.quiz_answers[i] = chosen.split(")")[0].strip() if ")" in chosen else chosen
            else:
                ans = st.text_input("Answer:", key=key, placeholder="Type your answer...")
                st.session_state.quiz_answers[i] = ans
            st.markdown("---")

        if not st.session_state.quiz_submitted:
            if st.button("✅ Submit Quiz", key="btn_submit"):
                score = sum(
                    1 for i, q in enumerate(qs)
                    if str(st.session_state.quiz_answers.get(i,"")).strip().upper()
                    in str(q.get("answer","")).strip().upper()
                    or str(q.get("answer","")).strip().upper()
                    in str(st.session_state.quiz_answers.get(i,"")).strip().upper()
                )
                st.session_state.quiz_score      = score
                st.session_state.best_quiz       = max(st.session_state.best_quiz, score)
                st.session_state.quiz_submitted   = True
                st.rerun()

        if st.session_state.quiz_submitted:
            score = st.session_state.quiz_score
            pct   = int(score/total*100) if total else 0
            emoji = "🏆" if pct>=90 else "🎉" if pct>=75 else "💪" if pct>=60 else "📚"
            grade = "Outstanding!" if pct>=90 else "Great Job!" if pct>=75 else "Good Effort!" if pct>=60 else "Keep Practicing!"
            st.markdown(f"""<div class="score-box">
                <div class="score-emoji">{emoji}</div>
                <div class="score-num">{score} / {total}</div>
                <div class="score-pct">{pct}%</div>
                <div class="score-grade">{grade}</div>
            </div>""", unsafe_allow_html=True)

            with st.expander("📋 Answer Review"):
                for i, q in enumerate(qs):
                    correct  = q.get("answer","")
                    given    = st.session_state.quiz_answers.get(i,"")
                    explain  = q.get("explanation","")
                    is_right = str(given).strip().upper() in str(correct).strip().upper() or \
                               str(correct).strip().upper() in str(given).strip().upper()
                    st.markdown(f"{'✅' if is_right else '❌'} **Q{i+1}:** {q.get('q','')}")
                    st.markdown(f"Your: `{given}` | Correct: `{correct}`")
                    if explain: st.info(f"💡 {explain}")
                    st.markdown("---")

            c1,c2,c3 = st.columns(3)
            with c1:
                if st.button("🔄 Try Again"):
                    st.session_state.quiz_answers  = {}
                    st.session_state.quiz_submitted = False
                    st.rerun()
            with c2:
                if st.button("🆕 New Quiz"):
                    st.session_state.quiz_questions = []
                    st.session_state.quiz_answers   = {}
                    st.session_state.quiz_submitted  = False
                    st.rerun()
            with c3:
                if st.button("💬 Discuss with AI"):
                    st.session_state.mode = "chat"
                    st.session_state.chat_history.append({"role":"user",
                        "content":f"I scored {score}/{total} ({pct}%) on '{quiz_topic}'. Help me understand what I got wrong."})
                    st.rerun()

# ══════════════════════════════════════════════════════════════
#  🃏  FLASHCARDS
# ══════════════════════════════════════════════════════════════
elif mode == "flashcard":
    st.markdown('<div class="section-title">🃏 AI Flashcards</div>', unsafe_allow_html=True)
    pending_fc = st.session_state.pop("pending_fc_topic", None)

    col1, col2 = st.columns([3,1])
    with col1:
        fc_topic = st.text_input("Topic", value=pending_fc or "",
                                  placeholder="Any topic — unlimited cards!")
    with col2:
        fc_count = st.number_input("Cards", 5, 50, 15)

    if st.button("🃏 Generate Flashcards"):
        if not fc_topic.strip():
            st.warning("Enter a topic.")
        else:
            with st.spinner("🌿 Creating flashcards..."):
                messages = [
                    {"role":"system","content":(
                        f"You are a flashcard generator. {LANG_INSTRUCTION} Return ONLY JSON array. "
                        'Format: [{{"q":"Term or question","a":"Definition or answer"}}] No extra text.'
                    )},
                    {"role":"user","content":f"Create {fc_count} flashcards for '{fc_topic}'."}
                ]
                raw = ask_ai(messages, 3000)
            if raw:
                try:
                    clean = re.sub(r"```json|```","",raw).strip()
                    cards = json.loads(clean)
                    st.session_state.flashcards     = cards
                    st.session_state.fc_index       = 0
                    st.session_state.fc_show_answer = False
                    st.rerun()
                except Exception:
                    st.error("Could not parse flashcards. Please try again.")

    if st.session_state.flashcards:
        cards  = st.session_state.flashcards
        idx    = st.session_state.fc_index
        total  = len(cards)
        card   = cards[idx]
        show_a = st.session_state.fc_show_answer

        st.markdown(f"**Card {idx+1} of {total}**")
        st.progress((idx+1)/total)
        st.markdown("")

        if not show_a:
            st.markdown(f"""<div class="flashcard">
                <div style='font-size:0.72rem;color:#52b788;font-weight:800;letter-spacing:2px;text-transform:uppercase;margin-bottom:0.8rem;'>QUESTION</div>
                <div class="flashcard-q">{card['q']}</div>
                <div style='font-size:0.8rem;opacity:0.5;margin-top:1.5rem;'>👆 Click "Show Answer"</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="flashcard">
                <div style='font-size:0.72rem;color:#74c69d;font-weight:800;letter-spacing:2px;text-transform:uppercase;margin-bottom:0.8rem;'>ANSWER</div>
                <div class="flashcard-q">{card['q']}</div>
                <div class="flashcard-a">✅ {card['a']}</div>
            </div>""", unsafe_allow_html=True)

        c1,c2,c3,c4,c5 = st.columns(5)
        with c1:
            if st.button("👁️ " + ("Hide" if show_a else "Show Answer")):
                st.session_state.fc_show_answer = not show_a
                st.session_state.flashcards_reviewed += 1
                st.rerun()
        with c2:
            if st.button("⬅️ Prev", disabled=idx==0):
                st.session_state.fc_index -= 1
                st.session_state.fc_show_answer = False
                st.rerun()
        with c3:
            if st.button("Next ➡️", disabled=idx==total-1):
                st.session_state.fc_index += 1
                st.session_state.fc_show_answer = False
                st.rerun()
        with c4:
            if st.button("🔀 Shuffle"):
                random.shuffle(st.session_state.flashcards)
                st.session_state.fc_index = 0
                st.session_state.fc_show_answer = False
                st.rerun()
        with c5:
            if st.button("🔁 Restart"):
                st.session_state.fc_index = 0
                st.session_state.fc_show_answer = False
                st.rerun()

        # Export flashcards
        fc_text = "\n\n".join([f"Q: {c['q']}\nA: {c['a']}" for c in cards])
        st.download_button("📥 Download Flashcards", fc_text, file_name="flashcards.txt")

# ══════════════════════════════════════════════════════════════
#  📖  VOCABULARY BUILDER
# ══════════════════════════════════════════════════════════════
elif mode == "vocab":
    st.markdown('<div class="section-title">📖 Vocabulary Builder</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        vocab_topic = st.text_input("Topic / Subject", placeholder="e.g. Biology, Computer Science, Law...")
    with col2:
        vocab_count = st.slider("Number of Words", 5, 30, 10)
    with col3:
        vocab_level = st.selectbox("Level", ["Beginner","Intermediate","Advanced","Academic","Technical"])

    if st.button("📖 Generate Vocabulary List"):
        if not vocab_topic.strip():
            st.warning("Enter a topic.")
        else:
            with st.spinner("🌿 Building vocabulary list..."):
                messages = [
                    {"role":"system","content":(
                        f"You are a vocabulary expert. {LANG_INSTRUCTION} Return ONLY JSON array. "
                        'Format: [{"word":"term","type":"noun/verb/adj","definition":"clear definition","example":"example sentence","mnemonic":"memory trick"}] '
                        "Make definitions clear and examples relevant to the topic."
                    )},
                    {"role":"user","content":f"Give {vocab_count} important {vocab_level} vocabulary words for '{vocab_topic}'."}
                ]
                raw = ask_ai(messages, 3000)
            if raw:
                try:
                    clean = re.sub(r"```json|```","",raw).strip()
                    vocab = json.loads(clean)
                    st.session_state.vocab_list = vocab
                    st.rerun()
                except Exception:
                    st.error("Could not parse vocabulary. Please try again.")

    if st.session_state.vocab_list:
        # Search filter
        search = st.text_input("🔍 Search words...", placeholder="Filter vocabulary...")
        st.markdown("---")

        filtered = [v for v in st.session_state.vocab_list
                    if not search or search.lower() in v.get("word","").lower()
                    or search.lower() in v.get("definition","").lower()]

        for v in filtered:
            st.markdown(f"""<div class="vocab-card">
                <div class="vocab-word">{v.get('word','')}</div>
                <div class="vocab-type">{v.get('type','')}</div>
                <div class="vocab-def">📖 {v.get('definition','')}</div>
                <div class="vocab-ex">💬 "{v.get('example','')}"</div>
                {'<div class="vocab-ex">🧠 ' + v.get('mnemonic','') + '</div>' if v.get('mnemonic') else ''}
            </div>""", unsafe_allow_html=True)

        vocab_text = "\n\n".join([
            f"{v.get('word','')} ({v.get('type','')})\nDef: {v.get('definition','')}\nEx: {v.get('example','')}"
            for v in st.session_state.vocab_list
        ])
        st.download_button("📥 Download Vocabulary", vocab_text, file_name="vocabulary.txt")

# ══════════════════════════════════════════════════════════════
#  📅  STUDY PLAN
# ══════════════════════════════════════════════════════════════
elif mode == "plan":
    st.markdown('<div class="section-title">📅 Smart Study Planner</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        exam_sub = st.text_input("Subject / Exam", placeholder="e.g. Data Structures Final, Physics Midterm")
        days     = st.number_input("Days until exam", 1, 365, 7)
    with col2:
        hours = st.number_input("Daily study hours", 1, 20, 3)
        weak  = st.text_input("Weak areas (optional)", placeholder="e.g. Recursion, Thermodynamics...")

    col3, col4 = st.columns(2)
    with col3:
        style = st.selectbox("Style", ["Balanced & Steady","Intensive (Crunch Mode)",
                                        "Relaxed & Gradual","Weekend-Heavy","Morning-Focused"])
    with col4:
        goal = st.selectbox("Target", ["Pass the exam","Score 60%+","Score 75%+","Score 90%+","Perfect score"])

    extra_prefs = st.text_area("Any special preferences? (optional)",
                                placeholder="e.g. I learn better with examples, prefer short sessions, need revision days...",
                                height=80)

    c1, c2 = st.columns([2,2])
    with c1:
        if st.button("🗓️ Generate My Plan"):
            if not exam_sub.strip():
                st.warning("Enter a subject name.")
            else:
                with st.spinner("🌿 Creating personalized study plan..."):
                    messages = [
                        {"role":"system","content":(
                            f"You are StudyMate expert study planner. {LANG_INSTRUCTION} "
                            "Create a detailed, realistic day-by-day schedule. "
                            "Include: **📋 Strategy Overview**, specific topics per day with time slots, "
                            "revision checkpoints, practice test days, **🎯 Daily Tips**, **✅ Success Tips**. "
                            "Make it professional, motivating, and actionable."
                        )},
                        {"role":"user","content":(
                            f"Create a {days}-day {style} study plan for '{exam_sub}'. "
                            f"Daily time: {hours} hrs. Target: {goal}. "
                            f"Weak areas: {weak or 'none'}. Preferences: {extra_prefs or 'none'}."
                        )}
                    ]
                    result = ask_ai(messages, 4000)
                if result:
                    st.session_state.last_plan = result
    with c2:
        if st.session_state.last_plan:
            if st.button("✏️ Adjust Plan"):
                st.session_state.last_plan = None
                st.rerun()

    if st.session_state.last_plan:
        st.markdown(f'<div class="result-box">{st.session_state.last_plan}</div>', unsafe_allow_html=True)
        c1,c2,c3 = st.columns(3)
        with c1:
            st.download_button("📥 Download Plan", st.session_state.last_plan, file_name="study_plan.txt")
        with c2:
            html_plan = f"<html><body style='font-family:Georgia;max-width:800px;margin:40px auto;line-height:1.8;'><h1>📅 Study Plan: {exam_sub}</h1><pre>{st.session_state.last_plan}</pre><footer style='color:gray;'>StudyMate AI</footer></body></html>"
            st.download_button("🖨️ Export HTML", html_plan, file_name="study_plan.html", mime="text/html")
        with c3:
            if st.button("💬 Discuss with AI"):
                st.session_state.mode = "chat"
                st.session_state.chat_history.append({"role":"user",
                    "content":f"I have a {days}-day plan for {exam_sub}. Give me extra tips to maximize my study efficiency."})
                st.rerun()

# ══════════════════════════════════════════════════════════════
#  ⏱️  POMODORO TIMER
# ══════════════════════════════════════════════════════════════
elif mode == "pomodoro":
    st.markdown('<div class="section-title">⏱️ Pomodoro Focus Timer</div>', unsafe_allow_html=True)
    st.caption("Stay focused with timed study sessions. Customize your intervals.")

    col1, col2, col3 = st.columns(3)
    with col1:
        study_mins = st.number_input("Study Duration (min)", 1, 120,
                                     st.session_state.pomo_study_mins)
        st.session_state.pomo_study_mins = study_mins
    with col2:
        break_mins = st.number_input("Short Break (min)", 1, 30,
                                     st.session_state.pomo_break_mins)
        st.session_state.pomo_break_mins = break_mins
    with col3:
        long_break = st.number_input("Long Break (min)", 5, 60, 15)

    st.markdown("---")

    # Timer display
    pomo_mode = st.session_state.pomo_mode
    total_secs = (study_mins if pomo_mode == "study" else break_mins) * 60
    elapsed    = st.session_state.pomo_elapsed

    if st.session_state.pomo_running and st.session_state.pomo_start:
        elapsed = int(time.time() - st.session_state.pomo_start)
        st.session_state.pomo_elapsed = elapsed
        if elapsed >= total_secs:
            st.session_state.pomo_running = False
            st.session_state.pomo_elapsed = 0
            if pomo_mode == "study":
                st.session_state.pomo_sessions += 1
                st.session_state.pomo_mode = "break"
                st.success(f"🎉 Session complete! Take a {break_mins}-min break. Sessions: {st.session_state.pomo_sessions}")
            else:
                st.session_state.pomo_mode = "study"
                st.info("🌿 Break over! Ready to focus again.")
            st.rerun()

    remaining  = max(0, total_secs - elapsed)
    mins_left  = remaining // 60
    secs_left  = remaining % 60
    pct        = 1 - (remaining / total_secs) if total_secs > 0 else 0

    mode_label = "🌿 Focus Session" if pomo_mode == "study" else "☕ Break Time"
    mode_color = "#52b788" if pomo_mode == "study" else "#74c69d"

    st.markdown(f"""<div class="pomo-timer">
        <div class="pomo-time">{mins_left:02d}:{secs_left:02d}</div>
        <div class="pomo-label">{mode_label}</div>
    </div>""", unsafe_allow_html=True)

    st.progress(pct)
    st.markdown(f"**Sessions completed today: {st.session_state.pomo_sessions}** 🏆")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if not st.session_state.pomo_running:
            if st.button("▶️ Start"):
                st.session_state.pomo_running = True
                st.session_state.pomo_start   = time.time() - st.session_state.pomo_elapsed
                st.rerun()
        else:
            if st.button("⏸️ Pause"):
                st.session_state.pomo_running = False
                st.rerun()
    with c2:
        if st.button("⏹️ Reset"):
            st.session_state.pomo_running = False
            st.session_state.pomo_elapsed = 0
            st.session_state.pomo_start   = None
            st.rerun()
    with c3:
        if st.button("⏭️ Skip"):
            st.session_state.pomo_running = False
            st.session_state.pomo_elapsed = 0
            st.session_state.pomo_mode    = "break" if pomo_mode=="study" else "study"
            st.rerun()
    with c4:
        if st.button("🔄 Auto-refresh"):
            if st.session_state.pomo_running:
                st.rerun()

    st.markdown("---")
    st.info("💡 **Tip:** Use Pomodoro + Explain/Quiz together for maximum learning efficiency!")

    if st.session_state.pomo_running:
        time.sleep(1)
        st.rerun()

# ══════════════════════════════════════════════════════════════
#  📊  DASHBOARD
# ══════════════════════════════════════════════════════════════
elif mode == "dashboard":
    st.markdown('<div class="section-title">📊 Your Learning Dashboard</div>', unsafe_allow_html=True)

    # Main stats
    c1,c2,c3,c4,c5 = st.columns(5)
    stats = [
        ("🔥 Day Streak",     st.session_state.streak_days),
        ("📝 Total Queries",  st.session_state.total_queries),
        ("📚 Topics Studied", st.session_state.topics_studied),
        ("❓ Quizzes Taken",  st.session_state.total_quizzes),
        ("🏆 Best Quiz Score",st.session_state.best_quiz),
    ]
    for col, (label, val) in zip([c1,c2,c3,c4,c5], stats):
        with col:
            st.markdown(f"""<div class="dash-card">
                <div class="dash-num">{val}</div>
                <div class="dash-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🔥 Streak Calendar")
        history = st.session_state.streak_history[-14:]
        cols = st.columns(7)
        day_names = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        for i, d in enumerate(day_names):
            cols[i].markdown(f"<div style='text-align:center;font-size:0.7rem;color:#74c69d;font-weight:700;'>{d}</div>", unsafe_allow_html=True)
        for i in range(14):
            col_idx = i % 7
            day_offset = 13 - i
            check_date = str(date.fromordinal(date.today().toordinal() - day_offset))
            active = check_date in history
            color = "#52b788" if active else "rgba(82,183,136,0.1)"
            cols[col_idx].markdown(
                f"<div style='background:{color};border-radius:6px;height:30px;margin:2px;border:1px solid rgba(82,183,136,0.2);'></div>",
                unsafe_allow_html=True)

    with col2:
        st.markdown("#### 📚 Topics Studied")
        if st.session_state.explain_history:
            for item in reversed(st.session_state.explain_history[-8:]):
                st.markdown(f"""<div style='background:rgba(82,183,136,0.08);border:1px solid rgba(82,183,136,0.2);
                border-radius:10px;padding:0.5rem 0.8rem;margin:0.3rem 0;font-size:0.85rem;'>
                📗 <b>{item['topic']}</b> <span style='opacity:0.5;font-size:0.75rem;'>· {item['subject']}</span></div>""",
                unsafe_allow_html=True)
        else:
            st.info("Start studying to see your topic history here!")

    st.markdown("---")

    # Pomodoro sessions
    st.markdown("#### ⏱️ Pomodoro Sessions Today")
    sessions = st.session_state.pomo_sessions
    pomo_bar = "🟢" * sessions + "⚪" * max(0, 8-sessions)
    st.markdown(f"**{pomo_bar}** — {sessions} sessions ({sessions * st.session_state.pomo_study_mins} minutes focused)")

    st.markdown("---")

    # Motivational message
    if st.session_state.total_queries == 0:
        msg = "👋 Welcome! Start exploring the tools above to begin your learning journey."
    elif st.session_state.streak_days >= 7:
        msg = f"🏆 Incredible! {st.session_state.streak_days} days in a row! You're unstoppable!"
    elif st.session_state.streak_days >= 3:
        msg = f"🔥 {st.session_state.streak_days}-day streak! Keep the momentum going!"
    elif st.session_state.topics_studied >= 10:
        msg = f"📚 Amazing! You've studied {st.session_state.topics_studied} topics. Knowledge is power!"
    else:
        msg = "🌱 Great start! Consistency is key. Come back every day to build your streak!"

    st.markdown(f"""<div style='background:linear-gradient(135deg,#1b4332,#2d6a4f);
    border:1px solid rgba(82,183,136,0.4);border-radius:16px;padding:1.5rem;text-align:center;'>
    <div style='font-size:1.1rem;font-weight:700;color:#fff;'>{msg}</div></div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  💬  AI CHAT
# ══════════════════════════════════════════════════════════════
elif mode == "chat":
    st.markdown('<div class="section-title">💬 AI Study Assistant</div>', unsafe_allow_html=True)
    st.caption("Full conversation memory — ask anything, follow up, go as deep as you want.")

    if not st.session_state.chat_history:
        st.markdown("""<div style='text-align:center;padding:3rem;'>
            <div style='font-size:3rem;margin-bottom:1rem;'>🌿</div>
            <div style='font-size:1.1rem;font-weight:700;color:#52b788;margin-bottom:0.5rem;'>Hi! I'm StudyMate AI</div>
            <div style='opacity:0.6;font-size:0.9rem;'>Ask me to explain topics, quiz you, help with homework,<br>compare concepts, or anything study-related. No limits!</div>
        </div>""", unsafe_allow_html=True)

        suggestions = [
            "Explain the OSI model simply",
            "Quiz me on Python basics",
            "What's the difference between RAM and ROM?",
            "Help me with recursion — I don't get it",
            "Give me 5 tips to study more effectively",
            "Explain OOP with real examples",
        ]
        st.markdown("**💡 Quick Start:**")
        c1, c2 = st.columns(2)
        for i, s in enumerate(suggestions):
            with (c1 if i%2==0 else c2):
                if st.button(s, key=f"suggest_{i}"):
                    st.session_state.chat_history.append({"role":"user","content":s})
                    st.rerun()
    else:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"""<div class="msg-user-wrap">
                    <div><div class="msg-name" style='text-align:right;color:#52b788;'>You</div>
                    <div class="msg-bubble-user">{msg["content"]}</div></div>
                    <div class="msg-avatar msg-avatar-user">👤</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div class="msg-ai-wrap">
                    <div class="msg-avatar msg-avatar-ai">🌿</div>
                    <div><div class="msg-name" style='color:#74c69d;'>StudyMate AI</div>
                    <div class="msg-bubble-ai">{msg["content"]}</div></div>
                </div>""", unsafe_allow_html=True)

    user_msg = st.chat_input("Ask anything — no limits, no restrictions...")
    if user_msg:
        st.session_state.chat_history.append({"role":"user","content":user_msg})
        messages = [
            {"role":"system","content":(
                f"You are StudyMate, an expert AI study assistant. {LANG_INSTRUCTION} "
                "You have full memory of the conversation — use it for context. "
                "Be thorough, accurate, and encouraging. Use formatting when helpful. "
                "Adapt depth to the student's level. Never refuse to help with academic topics."
            )}
        ] + st.session_state.chat_history
        with st.spinner("🌿 Thinking..."):
            reply = ask_ai(messages, 2500)
        if reply:
            st.session_state.chat_history.append({"role":"assistant","content":reply})
            st.rerun()

# ── FOOTER ────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""<p style='text-align:center;opacity:0.4;font-size:0.8rem;'>
    <span style='color:#52b788;font-weight:700;'>StudyMate AI</span> &nbsp;·&nbsp;
    Built with ❤️ by <b>Huzaifa</b> &nbsp;·&nbsp;
    Powered by OpenRouter AI &nbsp;·&nbsp;
    Free forever for students 🎓
</p>""", unsafe_allow_html=True)
