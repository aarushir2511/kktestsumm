# textsumm.py

from transformers import pipeline
import requests
from bs4 import BeautifulSoup

# -----------------------------
# 1️⃣ Load the summarization model
# -----------------------------
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


# -----------------------------
# 2️⃣ Fetch article text from URL
# -----------------------------
def fetch_article(url):
    """Fetch text content from a news/blog article"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Remove scripts, styles, and other irrelevant tags
    for script in soup(["script", "style"]):
        script.extract()
    
    # Join all visible text
    text = ' '.join(soup.stripped_strings)
    return text


# -----------------------------
# 3️⃣ Split text into manageable chunks
# -----------------------------
def chunk_text(text, max_chunk_size=3000):
    """Split text into smaller chunks so model doesn't crash"""
    return [text[i:i+max_chunk_size] for i in range(0, len(text), max_chunk_size)]


# -----------------------------
# 4️⃣ Summarize text using chunking
# -----------------------------
def summarize_text(text):
    """Summarize long text safely using chunks"""
    # Split into chunks
    chunks = chunk_text(text)
    summaries = []

    # Summarize each chunk
    for chunk in chunks:
        summary = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
        summaries.append(summary[0]['summary_text'])
    
    # Combine mini-summaries and summarize again for final summary
    combined_summary = " ".join(summaries)
    final_summary = summarizer(combined_summary, max_length=130, min_length=30, do_sample=False)
    
    return final_summary[0]['summary_text']


# -----------------------------
# 5️⃣ Main program
# -----------------------------
if __name__ == "__main__":
    # Example: replace with any news/blog URL
    url = "https://www.moneycontrol.com/news/india/if-pak-dares-what-is-sir-creek-dispute-and-why-rajnath-singh-is-warning-islamabad-13594985.html"
    
    # Fetch article text
    article_text = fetch_article(url)
    print("Original Article (first 500 chars):\n", article_text[:500], "...\n")
    
    # Summarize
    summary = summarize_text(article_text)
    print("🔹 Summary:\n", summary)
