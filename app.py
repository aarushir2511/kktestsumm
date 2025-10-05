# app.py
import streamlit as st
from transformers import pipeline
import requests
from bs4 import BeautifulSoup

# ✅ Page config must be first Streamlit call
st.set_page_config(page_title="Article Summarizer", page_icon="📰", layout="centered")

# -----------------------------
# 1️⃣ Load summarization model
# -----------------------------
@st.cache_resource
def load_model():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_model()

# -----------------------------
# 2️⃣ Fetch article text
# -----------------------------
def fetch_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for script in soup(["script", "style"]):
        script.extract()
    return ' '.join(soup.stripped_strings)

# -----------------------------
# 3️⃣ Chunking
# -----------------------------
def chunk_text(text, max_chunk_size=3000):
    return [text[i:i+max_chunk_size] for i in range(0, len(text), max_chunk_size)]

# -----------------------------
# 4️⃣ Summarization
# -----------------------------
def summarize_text(text):
    chunks = chunk_text(text)
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
        summaries.append(summary[0]['summary_text'])
    combined_summary = " ".join(summaries)
    final_summary = summarizer(combined_summary, max_length=130, min_length=30, do_sample=False)
    return final_summary[0]['summary_text']

# -----------------------------
# 5️⃣ UI
# -----------------------------
st.title("📰 Article Summarizer with BART")
st.write("Paste a **news/blog article link** below and get an instant AI-generated summary.")

url = st.text_input("Enter Article URL", "")

if st.button("Summarize"):
    if not url.strip():
        st.warning("⚠️ Please enter a valid URL")
    else:
        with st.spinner("Fetching and summarizing article..."):
            try:
                article_text = fetch_article(url)
                if len(article_text) < 500:
                    st.error("❌ Couldn't extract enough content from the URL. Try another link.")
                else:
                    st.subheader("📄 Original Article (first 500 chars)")
                    st.text_area("Article Preview", article_text[:500] + "...", height=200)

                    summary = summarize_text(article_text)
                    st.subheader("🔹 AI Summary")
                    st.success(summary)
            except Exception as e:
                st.error(f"Error: {str(e)}")
