# 📰 Text Summarizer using Streamlit  

> A simple web-based AI project that summarizes long news articles or blog posts into concise 3-sentence summaries using Natural Language Processing (NLP) and Transformer models.

---

## 📖 Table of Contents
- [Project Overview](#project-overview)
- [Objective](#objective)
- [Tech Stack](#tech-stack)
- [Setup Instructions](#setup-instructions)
- [Step-by-Step Development Log (with-Failures)](#step-by-step-development-log-with-failures)
- [How It Works](#how-it-works)
- [Example Output](#example-output)
- [Author](#author)

---

## 🚀 Project Overview
This project is a **Streamlit web app** that summarizes any online article or blog post into 3 short, meaningful sentences.  
It uses **Hugging Face’s BART model** (`facebook/bart-large-cnn`) to perform **abstractive summarization**, meaning the model **understands** and **rewrites** content in a natural, human-like way.  

Users can simply enter a **URL** or **paste article text** into the app, click “Summarize,” and get an instant short summary.

---

## 🎯 Objective
The goal was to:
- Build a user-friendly web app that performs summarization.  
- Learn how to integrate transformer models with Streamlit.  
- Handle real-world news articles (long text, HTML cleaning, etc.).  

---

## 🧠 Tech Stack
| Component | Description |
|------------|-------------|
| **Language** | Python |
| **Frontend** | Streamlit |
| **Libraries** | `transformers`, `torch`, `requests`, `beautifulsoup4`, `streamlit` |
| **Model Used** | `facebook/bart-large-cnn` |
| **Interface** | Streamlit Web UI |

---

## ⚙️ Setup Instructions

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
## 🧩 Step-by-Step Development Log (with Failures)
🧾 Step 1: First Attempt — Basic Summarization

I started by testing a single block of text with:
```bash
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
print(summarizer(ARTICLE, max_length=130, min_length=30, do_sample=False))
```


✅ It worked perfectly for small articles.

❌ But when I tried summarizing real news websites, I got:
```bash
IndexError: index out of range in self
```


➜ Reason: The text was too long (BART can only handle ~1024 tokens).
