import streamlit as st
import re

# =============================================================
# SIMPLE TEXT MATCHING ENGINE (NO PIPELINE)
# =============================================================

def match_keywords(text, keywords):
    score = 0
    for kw in keywords:
        if kw in text.lower():
            score += 1
    return score

# =============================================================
# TOPIC DEFINITIONS
# =============================================================
topics = {
    "Akses kelas dan materi": ["kelas", "materi", "ga bisa akses", "tidak bisa dibuka", "kelas hilang"],
    "Notifikasi tidak muncul": ["notifikasi", "notif", "ga muncul", "tidak muncul"],
    "Upload tugas": ["upload", "unggah", "tugas", "gagal upload"],
    "Login atau SSO": ["login", "sso", "gabisa masuk", "tidak bisa login"],
    "Navigasi aplikasi": ["menu", "navigasi", "bingung", "tidak tahu dimana"],
    "Fitur tidak lengkap": ["fitur", "kurang fitur", "fitur tidak ada"],
    "Video conference bermasalah": ["video", "zoom", "meeting", "vc", "voice"],
    "Bug atau error aplikasi": ["error", "bug", "force close", "crash"],
    "Masalah performa atau lemot": ["lemot", "lag", "loading", "lambat", "macet"],
    "Tampilan atau UI membingungkan": ["tampilan", "ui", "desain", "susah dilihat"]
}

# =============================================================
# ICT Literacy Classifier
# =============================================================
def classify_ict(text):
    t = text.lower()

    low_kw = ["ga ngerti", "gak ngerti", "nggak ngerti", "bingung", "cara pakai", "susah", "ga bisa pakai"]
    med_kw = ["agak susah", "kadang bingung", "sering bingung"]
    high_kw = ["mudah digunakan", "gampang", "simple", "langsung paham"]
    tech_kw = ["error", "bug", "lemot", "crash", "server", "gagal", "tidak bisa dibuka"]

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
# Emotion classifier (lexicon-based)
# =============================================================
emotion_lex = {
    "frustration": ["kesal", "frustasi", "frustrasi", "nyesek", "nyebelin"],
    "confusion": ["bingung", "tidak paham", "ga ngerti"],
    "annoyance": ["ganggu", "mengganggu", "nyebelin"],
    "overwhelmed": ["kewalahan", "overwhelmed", "capek"],
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
# Sentiment (from rating)
# =============================================================
def rating_to_sentiment(r):
    if r >= 4:
        return "Positive"
    elif r == 3:
        return "Neutral"
    return "Negative"

# =============================================================
# Streamlit UI
# =============================================================
st.set_page_config(page_title="Edlink Review Classifier", layout="centered")

st.markdown("""
<style>
body { background-color: #1A3D7C; }
.main .block-container {
    background-color: #FFFFFF;
    padding: 2rem;
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)

st.title("Edlink Review Classification App")
st.write("Masukkan ulasan untuk mendeteksi **Topik**, **ICT Literacy**, **Emotion**, dan **Sentimen** tanpa model besar.")

text = st.text_area("Masukkan Ulasan:", height=200)
rating = st.selectbox("Rating (1–5):", [1,2,3,4,5])

if st.button("Klasifikasi Review"):
    if not text.strip():
        st.warning("Masukkan ulasan terlebih dahulu.")
    else:
        with st.spinner("Menganalisis..."):

            # TOPIC
            topic_scores = {label: match_keywords(text, kws) for label, kws in topics.items()}
            topic = max(topic_scores, key=topic_scores.get)

            ict = classify_ict(text)
            emotion = classify_emotion(text)
            sentiment = rating_to_sentiment(rating)

        st.subheader("Hasil Analisis")
        st.write(f"**Topik:** {topic}")
        st.write(f"**ICT Literacy:** {ict}")
        st.write(f"**Emotion:** {emotion}")
        st.write(f"**Sentiment:** {sentiment}")