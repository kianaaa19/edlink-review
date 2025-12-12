import streamlit as st
import torch
from transformers import pipeline

# =============================================================
# Load Model Pipeline (Stable for Streamlit Cloud)
# =============================================================
zsc = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

# =============================================================
# Label Definitions
# =============================================================
topic_labels = [
    "Akses kelas dan materi",
    "Notifikasi tidak muncul",
    "Upload tugas",
    "Login atau SSO",
    "Navigasi aplikasi",
    "Fitur tidak lengkap",
    "Video conference bermasalah",
    "Bug atau error aplikasi",
    "Masalah performa atau lemot",
    "Tampilan atau UI membingungkan"
]

ict_labels = [
    "Low ICT literacy",
    "Medium ICT literacy",
    "High ICT literacy",
    "Technical issue (not ICT literacy)"
]

emotion_labels = [
    "frustration",
    "confusion",
    "annoyance",
    "overwhelmed",
    "stress",
    "satisfaction",
    "neutral"
]

# =============================================================
# Utils
# =============================================================
def classify(text, labels):
    result = zsc(text, labels, multi_label=False)
    return result["labels"][0]

def rating_to_sentiment(rating):
    if rating >= 4:
        return "Positive"
    elif rating == 3:
        return "Neutral"
    else:
        return "Negative"

# =============================================================
# Streamlit UI
# =============================================================
st.set_page_config(page_title="Edlink Review Classifier", layout="centered")

st.markdown("""
<style>
body {
    background-color: #1A3D7C;
}
.main .block-container {
    background-color: #FFFFFF;
    padding: 2rem;
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)

st.title("Edlink Review Classification App")
st.write("Masukkan teks ulasan untuk mendeteksi **Topik**, **ICT Literacy**, **Emotion**, dan **Sentimen**.")

# Input for prediction
review_text = st.text_area("Masukkan Ulasan:", height=200)

# Rating for sentiment
rating = st.selectbox("Pilih Rating (1–5):", [1, 2, 3, 4, 5])

# =============================================================
# Run Classification
# =============================================================
if st.button("Klasifikasi Review"):
    if review_text.strip() == "":
        st.warning("Tolong masukkan teks ulasan terlebih dahulu.")
    else:
        with st.spinner("Menganalisis..."):
            topic = classify(review_text, topic_labels)
            ict = classify(review_text, ict_labels)
            emotion = classify(review_text, emotion_labels)
            sentiment = rating_to_sentiment(rating)

        st.subheader("Hasil Analisis")
        st.write(f"**Topik Masalah:** {topic}")
        st.write(f"**Tingkat ICT Literacy:** {ict}")
        st.write(f"**Emotion:** {emotion}")
        st.write(f"**Sentiment:** {sentiment}")