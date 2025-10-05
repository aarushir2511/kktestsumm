# 📰 Text Summarizer using Streamlit  

> A simple web-based AI project that summarizes long news articles or blog posts into concise 3-sentence summaries using Natural Language Processing (NLP) and Transformer models.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Objective](#objective)
- [Tech Stack](#tech-stack)
- [Setup Instructions](#setup-instructions)
- [Step-by-Step Development Log (with-Failures)](#step-by-step-development-log-with-failures)
- [How It Works](#how-it-works)
- [Example Output](#example-output)
- [Author](#author)

---

## Project Overview
This project is a **Streamlit web app** that summarizes any online article or blog post into 3 short, meaningful sentences.  
It uses **Hugging Face’s BART model** (`facebook/bart-large-cnn`) to perform **abstractive summarization**, meaning the model **understands** and **rewrites** content in a natural, human-like way.  

Users can simply enter a **URL** or **paste article text** into the app, click “Summarize,” and get an instant short summary.

---

## Objective
The goal was to:
- Build a user-friendly web app that performs summarization.  
- Learn how to integrate transformer models with Streamlit.  
- Handle real-world news articles (long text, HTML cleaning, etc.).  

---

## Tech Stack
| Component | Description |
|------------|-------------|
| **Language** | Python |
| **Frontend** | Streamlit |
| **Libraries** | `transformers`, `torch`, `requests`, `beautifulsoup4`, `streamlit` |
| **Model Used** | `facebook/bart-large-cnn` |
| **Interface** | Streamlit Web UI |

---

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/text-summarizer.git
   cd text-summarizer

2. **Install Dependencies**
   ```bash
   pip install streamlit transformers torch requests beautifulsoup4
   
 3.**Run the App**
  ```bash
  streamlit run app.py
  ```


---
## Step-by-Step Development Log (with Failures)
### Step 1: First Attempt — Basic Summarization

 I started by testing a single block of text with:
```bash
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
print(summarizer(ARTICLE, max_length=130, min_length=30, do_sample=False))
```


It worked perfectly for small articles.

But when I tried summarizing real news websites, I got:
```bash
IndexError: index out of range in self
```


➜ Reason: The text was too long (BART can only handle ~1024 tokens).

### Step 2: Research and Debugging

I learned that BART crashes if the input exceeds its token limit.

Tried to reduce article text size using slicing:
```bash
text = text[:3000]
```

 Fixed the error, but the summary missed important details (since only the first part of the article was used).

### Step 3: Final Working Solution — Chunk + Combine

I wrote a chunking function to split long text into smaller pieces:

```bash
def chunk_text(text, max_chunk_size=3000):
    return [text[i:i+max_chunk_size] for i in range(0, len(text), max_chunk_size)]

```
Summarized each chunk separately, then summarized those mini-summaries again.

This method worked for any article length and gave a clean 3-sentence summary.

### Step 4: Added Web Scraping

Used requests + BeautifulSoup to fetch article text from any URL:
```bash
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
text = ' '.join(soup.stripped_strings)
```

Removed unwanted elements (<script>, <style>) before summarizing.

Now I can summarize any live article directly from the internet.

### Step 5: Warning About max_length

I noticed a warning:
```bash
Your max_length is set to 130, but input_length is only 99...
```

Not an error, just a suggestion.

It means the text was short — so I ignored it.

Optional fix: make max_length dynamic based on text length.

---
## How It Works

1. **Fetch Article** → Download and clean article text using BeautifulSoup.

2. **Chunk Text** → Split into 3000-character pieces to fit model’s limit.

3. **Summarize Each Chunk** → Use BART to summarize each piece.

4. **Combine & Re-summarize** → Merge all mini-summaries and summarize them again to produce the final 3-sentence output.
