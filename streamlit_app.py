import random
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Autumn Mind", page_icon="🍂", layout="centered")

BASE = Path(__file__).parent
MODEL_FILES = [BASE / "Machine learning on the go.pkl",
               BASE / "Machine_learning_on_the_go.pkl"]


@st.cache_resource
def load_model():
    for f in MODEL_FILES:
        if f.exists():
            return joblib.load(f)
    raise FileNotFoundError(
        "Model .pkl file not found next to streamlit_app.py")


model = load_model()

QUOTES = [
    "Even the trees let go of what no longer serves them, and they bloom again.",
    "Healing is not a straight line. Be gentle with your pace.",
    "A hard day is just a day. Tomorrow arrives with fresh light.",
    "You are allowed to rest. Rest is part of growing.",
    "Small steps still move you forward.",
    "Hope is quiet, but it never really leaves.",
]
SECONDS_PER_QUOTE = 8
TOTAL = SECONDS_PER_QUOTE * len(QUOTES)

# ---------- Falling leaves ----------
random.seed(7)
leaves_html = ""
for i in range(22):
    left = random.randint(0, 100)
    size = random.randint(18, 38)
    fall = random.randint(9, 18)
    delay = round(random.uniform(0, 14), 1)
    sway = random.choice(["sway1", "sway2"])
    emoji = random.choice(["🍁", "🍂", "🍂", "🍁", "🍃"])
    leaves_html += (
        f'<div class="leaf" style="left:{left}vw;font-size:{size}px;'
        f'animation:fall {fall}s linear {delay}s infinite, {sway} {fall/3:.1f}s ease-in-out {delay}s infinite;">{emoji}</div>'
    )

# ---------- Rotating quotes ----------
quotes_html = ""
for i, q in enumerate(QUOTES):
    quotes_html += (
        f'<div class="quote" style="animation:quotefade {TOTAL}s linear {i * SECONDS_PER_QUOTE}s infinite;">'
        f'“{q}”</div>'
    )

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;1,500&family=Nunito:wght@400;600;700&display=swap');

.stApp {
    background: linear-gradient(160deg, #fff3e0 0%, #ffd9a8 40%, #f6a86b 75%, #c8643a 100%);
    background-attachment: fixed;
}
html, body, [class*="css"], .stApp label, .stApp p {
    font-family: 'Nunito', sans-serif;
}
.stApp, .stApp label, .stApp p, .stApp li { color: #4a2512; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { position: relative; z-index: 3; padding-top: 2rem; max-width: 820px; }

.hero { text-align: center; margin-bottom: 1.2rem; }
.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 3rem; color: #7a2e0e; margin: 0;
}
.hero p { font-size: 1.1rem; color: #8a4b2a; margin-top: .3rem; }

/* translucent glass card for the form */
div[data-testid="stForm"] {
    background: rgba(255, 248, 238, 0.55);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(160, 70, 20, 0.25);
    border-radius: 22px;
    padding: 1.6rem 1.6rem 1rem 1.6rem;
    box-shadow: 0 10px 35px rgba(120, 50, 10, 0.18);
}
div[data-baseweb="select"] > div, .stNumberInput input, .stTextInput input {
    background: rgba(255,255,255,0.75) !important;
    border-radius: 12px !important;
    color: #4a2512 !important;
}
.stFormSubmitButton button {
    width: 100%;
    background: linear-gradient(90deg, #d2561f, #f08a24);
    color: white; font-weight: 700; font-size: 1.1rem;
    border: none; border-radius: 14px; padding: .7rem 0;
    box-shadow: 0 6px 18px rgba(200, 80, 20, .4);
    transition: transform .15s;
}
.stFormSubmitButton button:hover { transform: translateY(-2px) scale(1.01); color: white; }
.stFormSubmitButton button p { color: white !important; }

.section-title {
    font-family: 'Playfair Display', serif; font-size: 1.25rem;
    color: #8f3a12; margin: .6rem 0 .2rem 0;
}

.result-card {
    margin-top: 1.4rem; text-align: center;
    background: rgba(255, 250, 242, 0.8);
    border: 1px solid rgba(160, 70, 20, 0.3);
    border-radius: 24px; padding: 1.6rem;
    box-shadow: 0 12px 40px rgba(120, 50, 10, 0.25);
}
.result-score { font-family: 'Playfair Display', serif; font-size: 4.2rem; color: #b5441a; line-height: 1; }
.result-label { font-size: 1.3rem; font-weight: 700; margin-top: .3rem; }
.result-note { font-size: .85rem; opacity: .75; margin-top: .8rem; }

/* falling leaves */
.leaf { position: fixed; top: -60px; z-index: 4; pointer-events: none; user-select: none; opacity: .9; }
@keyframes fall { from { top: -60px; } to { top: 105vh; } }
@keyframes sway1 { 0%,100% { transform: translateX(0) rotate(0deg); } 50% { transform: translateX(70px) rotate(200deg); } }
@keyframes sway2 { 0%,100% { transform: translateX(0) rotate(0deg); } 50% { transform: translateX(-70px) rotate(-200deg); } }

/* rotating quotes, sitting behind the content */
.quote-wrap { position: fixed; inset: 0; z-index: 1; display: flex; align-items: center; justify-content: center; pointer-events: none; }
.quote {
    position: absolute; width: min(80vw, 760px); text-align: center;
    font-family: 'Playfair Display', serif; font-style: italic;
    font-size: clamp(1.6rem, 4vw, 2.8rem); color: rgba(122, 46, 14, 0.5);
    opacity: 0;
}
@keyframes quotefade {
    0% { opacity: 0; transform: translateY(12px); }
    3% { opacity: 1; transform: translateY(0); }
    13% { opacity: 1; transform: translateY(0); }
    16.6% { opacity: 0; transform: translateY(-12px); }
    100% { opacity: 0; }
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)
st.markdown(
    f'<div class="quote-wrap">{quotes_html}</div>{leaves_html}', unsafe_allow_html=True)

# ---------- Header ----------
st.markdown(
    '<div class="hero"><h1>🍁 Autumn Mind</h1>'
    "<p>Tell us about your daily routine and social media habits.<br>We will estimate your mental health score.</p></div>",
    unsafe_allow_html=True,
)

# ---------- Form ----------
with st.form("predict_form"):
    st.markdown('<div class="section-title">About you</div>',
                unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    age = c1.number_input("Age", min_value=1, max_value=100, value=20, step=1)
    gender = c2.selectbox("Gender", ["Male", "Female"])

    c3, c4 = st.columns(2)
    academic_level = c3.selectbox(
        "Academic level", ["High School", "Undergraduate", "Graduate"])
    country_choice = c4.selectbox(
        "Country",
        ["India", "USA", "Canada", "Australia", "UK",
            "Germany", "Mexico", "Turkey", "France", "Other…"],
    )
    country = country_choice
    if country_choice == "Other…":
        country = st.text_input("Type your country", value="Pakistan")

    st.markdown('<div class="section-title">Social media habits</div>',
                unsafe_allow_html=True)
    c5, c6 = st.columns(2)
    platform = c5.selectbox(
        "Most used platform",
        ["Instagram", "Facebook", "TikTok", "YouTube", "Snapchat", "Twitter", "WhatsApp",
         "LinkedIn", "WeChat", "LINE", "KakaoTalk", "VKontakte"],
    )
    purpose = c6.selectbox("Main purpose of use", [
                           "Entertainment", "Networking", "Education", "News"])
    usage = st.slider("Average daily usage (hours)", 0, 24, 4)
    unlocks = st.slider("Phone unlocks per day", 0, 300, 60)

    st.markdown('<div class="section-title">Daily life</div>',
                unsafe_allow_html=True)
    c7, c8, c9 = st.columns(3)
    study = c7.slider("Study hours", 0, 24, 3)
    activity = c8.slider("Physical activity hours", 0, 24, 1)
    sleep = c9.slider("Sleep hours", 0, 24, 7)
    stress = st.select_slider("Stress level", options=[
                              "Low", "Medium", "High", "Very High"], value="Medium")

    submitted = st.form_submit_button("🍂 Reveal my score")

# ---------- Prediction ----------
if submitted:
    input_row = pd.DataFrame([{
        "Age": int(age),
        "Gender": gender,
        "Country": country,
        "Academic_Level": academic_level,
        "Most_Used_Platform": platform,
        "Purpose_Of_Use": purpose,
        "Avg_Daily_Usage_Hours": int(usage),
        "Daily_Unlocks": int(unlocks),
        "Study_Hours": int(study),
        "Physical_Activity_Hours": int(activity),
        "Sleep_Hours_Per_Night": int(sleep),
        "Stress_Level": stress,
    }])
    try:
        with st.spinner("Gathering the leaves..."):
            score = round(float(model.predict(input_row)[0]), 2)
        if score >= 7.5:
            label, msg = "Flourishing 🌳", "You seem to be in a good place. Keep nurturing your habits."
        elif score >= 6:
            label, msg = "Steady 🍁", "Doing okay. Small tweaks to sleep or screen time can help."
        else:
            label, msg = "Needs some care 🍂", "Be kind to yourself. More rest and a little less scrolling can help."
        st.markdown(
            f'<div class="result-card"><div class="result-score">{score:.2f}</div>'
            f'<div class="result-label">{label}</div><div>{msg}</div>'
            f'<div class="result-note">This is a model estimate, not a medical diagnosis. '
            f"If you are struggling, please talk to someone you trust or a professional.</div></div>",
            unsafe_allow_html=True,
        )
        st.progress(min(max(score / 10, 0.0), 1.0))
    except Exception as e:
        st.error(f"Something went wrong: {e}")
