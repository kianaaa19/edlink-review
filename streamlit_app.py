import streamlit as st
import re

# =============================================================
# STYLE (Royal Blue Premium)
# =============================================================
st.set_page_config(page_title="Edlink Review Classifier", layout="centered")

st.markdown("""
<style>
body { background-color: #1A3D7C; }

.main .block-container {
    background-color: #F9FAFB;
    padding: 2rem 3rem;
    border-radius: 18px;
    box-shadow: 0 0 20px rgba(255, 255, 255, 0.15);
}

.result-card {
    background-color: white;
    padding: 1rem 1.5rem;
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.12);
    margin-bottom: 1rem;
    border-left: 6px solid #1A3D7C;
}

h2 {
    color: #1A3D7C !important;
    font-weight: 800 !important;
}

label {
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

# =============================================================
# MATCH ENGINE
# =============================================================
def match_keywords(text, keywords):
    score = 0
    for kw in keywords:
        if kw in text.lower():
            score += 1
    return score

# =============================================================
# TOPIC CATEGORIES
# =============================================================
topics = {
    "Akses kelas dan materi": ["kelas", "materi", "akses", "dibuka", "hilang"],
    "Notifikasi tidak muncul": ["notifikasi", "notif", "tidak muncul"],
    "Upload tugas": ["upload", "unggah", "tugas", "gagal upload"],
    "Login atau SSO": ["login", "masuk", "tidak bisa login"],
    "Navigasi aplikasi": ["menu", "navigasi", "bingung"],
    "Fitur tidak lengkap": ["fitur", "kurang fitur"],
    "Video conference bermasalah": ["video", "meeting", "vc"],
    "Bug atau error aplikasi": ["error", "bug", "force close", "crash"],
    "Masalah performa atau lemot": ["lemot", "lag", "loading"],
    "Tampilan atau UI membingungkan": ["tampilan", "ui", "interface", "desain"]
}

# =============================================================
# ICT LITERACY CLASSIFIER
# =============================================================
def classify_ict(text):
    t = text.lower()

    low_kw = ["ga ngerti", "bingung", "cara pakai", "susah", "nggak ngerti"]
    med_kw = ["agak susah", "kadang bingung"]
    high_kw = ["mudah digunakan", "gampang", "simple", "langsung paham"]
    tech_kw = ["error", "bug", "lemot", "crash", "server", "tidak bisa"]

    if any(k in t for k in low_kw):
        return "Low ICT literacy"
    if any(k in t for k in med_kw):
        return "Medium ICT literacy"
    if any(k in t for k in high_kw):
        return "High ICT literacy"
    if any(k in t for k in tech_kw):
        return "Technical issue (not ICT literacy)"

    return "Medium ICT literacy"

# =============================================================
# EMOTION CLASSIFIER
# =============================================================
emotion_lex = {
    "frustration": ["kesal", "frustasi", "frustrasi"],
    "confusion": ["bingung", "tidak paham", "ga ngerti"],
    "annoyance": ["mengganggu", "nyebelin"],
    "overwhelmed": ["kewalahan", "capek"],
    "stress": ["stress", "stres", "pusing"],
    "satisfaction": ["bagus", "mantap", "puas", "oke"],
    "neutral": []
}

def classify_emotion(text):
    t = text.lower()
    scores = {emo: match_keywords(t, kws) for emo, kws in emotion_lex.items()}
    best = max(scores, key=scores.get)
    return best

# =============================================================
# SENTIMENT FROM RATING
# =============================================================
def rating_to_sentiment(r):
    if r >= 4: return "Positive"
    elif r == 3: return "Neutral"
    return "Negative"

# =============================================================
# EMOJI
# =============================================================
emoji_map = {
    "frustration": "😠",
    "confusion": "😕",
    "annoyance": "😒",
    "overwhelmed": "🥵",
    "stress": "😣",
    "satisfaction": "😊",
    "neutral": "😐"
}

sentiment_emoji = {
    "Positive": "👍",
    "Neutral": "😐",
    "Negative": "👎"
}

# =============================================================
# UI HEADER
# =============================================================
st.title("📘 Edlink Review Classification App")
st.write("Masukkan ulasan untuk mendeteksi **Topik**, **ICT Literacy**, **Emotion**, dan **Sentimen**.")

text = st.text_area("📝 Masukkan Ulasan:", height=180)
rating = st.selectbox("⭐ Rating (1–5):", [1,2,3,4,5])

# =============================================================
# RUN
# =============================================================
if st.button("🔍 Klasifikasi Review"):
    if not text.strip():
        st.warning("Masukkan ulasan terlebih dahulu.")
    else:
        with st.spinner("⏳ Menganalisis ulasan..."):

            # Topic
            topic_scores = {label: match_keywords(text, kws) for label, kws in topics.items()}
            topic = max(topic_scores, key=topic_scores.get)

            ict = classify_ict(text)
            emotion = classify_emotion(text)
            sentiment = rating_to_sentiment(rating)

        # =============================================================
        # OUTPUT — NICE CARDS
        # =============================================================
        st.subheader("📊 Hasil Analisis")

        st.markdown(f"""
        <div class="result-card">
            <h4>🎯 Topik Masalah</h4>
            <p><b>{topic}</b></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-card">
            <h4>💻 ICT Literacy</h4>
            <p><b>{ict}</b></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-card">
            <h4>😶‍🌫️ Emotion</h4>
            <p><b>{emoji_map[emotion]} {emotion.title()}</b></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-card">
            <h4>📈 Sentiment</h4>
            <p><b>{sentiment_emoji[sentiment]} {sentiment}</b></p>
        </div>
        """, unsafe_allow_html=True)