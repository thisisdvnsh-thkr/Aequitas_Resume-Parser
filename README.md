# Aequitas — AI Resume Auditor
### Python • NLP • Streamlit • Scikit-learn

![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![NLP](https://img.shields.io/badge/NLP-Scikit--learn-F7931E?style=flat&logo=scikitlearn&logoColor=white)
![Status](https://img.shields.io/badge/Status-Live-brightgreen?style=flat)

An intelligent and fair AI system for resume screening — analyses resumes against job descriptions using NLP to provide match scores and skill gap analysis, with a strong focus on reducing hiring bias.

🔗 **[Launch Live App](https://aequitas-by-thisisdvnsh-thkr.streamlit.app)**

---

## 📌 Problem Statement

Traditional resume screening relies on simple keyword matching, which introduces bias based on phrasing, formatting, gender and background — rather than actual skills and competency.

**Aequitas** solves this by using **Cosine Similarity** and **NLP techniques** to calculate a match percentage purely based on technical skills and content, removing human and keyword-based bias from the initial screening process.

---

## ✨ Key Features

- 📄 **Multi-Format Support** — Accepts PDF and DOCX files for both resumes and job descriptions
- 🔍 **Intelligent Parsing** — Extracts and cleans text using Regex and Tokenization
- 📊 **Compatibility Score** — Calculates match percentage (0–100%) using vector similarity
- ✅ **Matched Skills** — Shows skills present in both resume and job description
- ❌ **Missing Skills** — Highlights critical skills absent from the resume
- ⚖️ **Bias Reduction** — Focuses purely on technical skills and content, ignoring demographic signals

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | Python 3.10 |
| NLP & ML | Scikit-learn (Cosine Similarity, CountVectorizer) |
| PDF Parsing | pdfminer.six |
| DOCX Parsing | docx2txt |
| Text Processing | Regex, Tokenization |

---

## 🔄 How It Works

```
Resume (PDF/DOCX) ──┐
                    ├──► Text Extraction & Cleaning
JD (PDF/DOCX) ─────┘         │
                              ▼
                    NLP Processing
                    (Tokenization + Regex)
                              │
                              ▼
                    Cosine Similarity
                    (CountVectorizer)
                              │
                              ▼
                    Match Score (0–100%)
                    + Skill Gap Analysis
```

---

## 📊 Output

- **Match Score** — Percentage compatibility between resume and job description
- **Matched Skills** — Common technical keywords found in both documents
- **Missing Skills** — Skills present in JD but missing from resume
- **Bias-free Analysis** — No demographic, formatting or keyword-phrasing bias

---

## 🚀 Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/thisisdvnsh-thkr/aequitas-fair-hiring-nlp.git
cd aequitas-fair-hiring-nlp
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
├── .devcontainer/     # Dev container config
├── images/            # UI screenshots
├── app.py             # Main Streamlit application
├── requirements.txt   # Python dependencies
├── runtime.txt        # Python version spec
└── README.md
```

---

## 👥 Contributors

**Devansh Thakur** — Project Lead & Developer  
[LinkedIn](https://linkedin.com/in/devansh-thakur) • [GitHub](https://github.com/thisisdvnsh-thkr)

**Arpit Upadhyay** — Contributor  
[GitHub](https://github.com/Arpit7088)

---

*Built with Python & Streamlit*
