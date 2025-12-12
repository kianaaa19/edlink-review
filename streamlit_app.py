# =============================================================
# IMPORTS (torch harus PALING ATAS agar tidak error di Streamlit Cloud)
# =============================================================
import torch
import streamlit as st
from transformers import pipeline

# =============================================================
# LOAD MODEL (dibungkus fungsi supaya tidak dipre-load sebelum torch)
# =============================================================
@st.cache_resource(show_spinner=True)
def load_zsc_model():
    import torch
    return pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli"
    )

zsc = load_zsc_model()

# =============================================================
# LABEL DEFINITIONS
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
# HELPER FUNCTIONS
# =============================================================
def classify(text, labels):
    result = zsc(text, labels, multi_label=False)
    return result["labels"][0]

def rating_to_sentiment(r):
    if r >= 4: return "Positive"
    elif r == 3: return "Neutral"
    else: return "Negative"

# =============================================================
# STREAMLIT UI
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
st.write("Masukkan teks ulasan untuk mendeteksi **Topik**, **ICT Literacy**, **Emotion**, dan **Sentimen**.")

# INPUT FIELDS
review_text = st.text_area("Masukkan Ulasan:", height=200)
rating = st.selectbox("Pilih Rating (1–5):", [1, 2, 3, 4, 5])

# =============================================================
# RUN CLASSIFICATION
# =============================================================
if st.button("Klasifikasi Review"):
    if not review_text.strip():
        st.warning("Masukkan teks ulasan terlebih dahulu.")
    else:
        with st.spinner("Menganalisis ulasan..."):
            topic = classify(review_text, topic_labels)
            ict = classify(review_text, ict_labels)
            emotion = classify(review_text, emotion_labels)
            sentiment = rating_to_sentiment(rating)

        # OUTPUT
        st.subheader("Hasil Analisis")
        st.write(f"**Topik Masalah:** {topic}")
        st.write(f"**ICT Literacy:** {ict}")
        st.write(f"**Emotion:** {emotion}")
        st.write(f"**Sentiment:** {sentiment}")