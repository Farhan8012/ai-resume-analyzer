# 🚀 AI Resume Analyzer (International Level)

> **A Dual-Engine Resume Analysis Platform built with Python, Streamlit, and NLP.** > *Mimics real-world ATS systems while providing "Semantic" feedback that keywords miss.*


## 🧠 The Problem
Traditional Resume Parsers (ATS) are dumb. They only look for exact keywords.
- If a job asks for **"Machine Learning"** and you write **"ML"**, you get a **0% score**.
- If you copy-paste the Job Description in white text, you get **100%**.

## 💡 The Solution: Dual-Engine Logic
This project fixes that by running **Two Analysis Engines** side-by-side:

| Feature | Engine 1: The "Strict" ATS | Engine 2: The "Smart" AI |
| :--- | :--- | :--- |
| **Technology** | Keyword Matching (Python Set Operations) | Vector Embeddings (TF-IDF + Cosine Similarity) |
| **Logic** | Checks for exact word matches (e.g., "Python", "SQL"). | Checks for *contextual meaning* and relevance. |
| **Goal** | Tells you if you will pass the **Robot**. | Tells you if you are actually **Qualified**. |

---

## ✨ Key Features (Implemented)
- **📄 PDF Parsing:** Extracts text from PDF resumes while preserving structure.
- **🧹 NLP Cleaning:** Removes special characters and formatting noise.
- **🔍 Smart Section Extraction:** Automatically identifies Skills, Education, and Experience sections.
- **📊 Dual Scoring System:** Displays "Keyword Match" vs. "Semantic Match" scores side-by-side.
- **📉 Resume Quality Check:**
    - Flags bullet points that lack **Quantification** (numbers/metrics).
    - Detects skills listed but **not demonstrated** in the Experience section.

---

## 🛠️ Tech Stack
- **Frontend:** Streamlit
- **Backend:** Python
- **NLP & AI:** Scikit-Learn (TF-IDF), NLTK, Regex
- **PDF Processing:** PDFPlumber

---

## 🚀 How to Run Locally

1. **Clone the Repo**
   ```bash
   git clone [https://github.com/Farhan8012/ai-resume-analyzer.git](https://github.com/Farhan8012/ai-resume-analyzer.git)
   cd ai-resume-analyzer### Day 2
- Implemented PDF resume parsing
- Cleaned extracted text using NLP preprocessing
- Extracted structured resume sections (Skills, Education, Experience)

2. install dependencies
   pip install -r requirements.txt

3. run the app
   streamlit run app.py


## 📅 Development Roadmap (Building in Public)

- [x] **Day 1:** Project Setup & PDF Extraction
- [x] **Day 2:** Text Cleaning & Section Segmentation
- [x] **Day 3:** Basic ATS Keyword Matching
- [x] **Day 4:** Resume Quality & Quantification Checks
- [x] **Day 5:** Semantic Matching Engine (TF-IDF & Cosine Similarity) 🧠
- [x] **Day 6:** **Advanced Keywords (100+ Skills) & Interactive Visualizations (Plotly)** 📊
- [x] **Day 5:** Semantic Matching Engine (TF-IDF & Cosine Similarity) 🧠
- [x] **Day 6:** **Advanced Keywords (100+ Skills) & Interactive Visualizations (Plotly)** 📊
- [x] **Day 7:** **Gemini AI Integration (Generative Feedback & Resume Rewriting)** 🤖
- [x] **Day 8:** UI Polish (Themes, Custom Styling, Dark Mode)
- [x] **Day 9:** **Deployment (Hosting on Streamlit Cloud for Free) ☁️ [DONE!]**
- [x] **Day 10:** **User Authentication (Login/Signup Logic)** 🔐
- [x] **Day 11:** History Tracking (Saving Resume Scores Over Time) 📈
- [x] **Day 12:** PDF Report Generation (Downloadable Analysis) 📄
- [x] **Day 13:** Compare Mode (A/B Testing for Resumes) ⚔️
- [x] **Day 14:** Smart Skill Recommendations (Actionable Project Ideas) 🧠
- [x] **Day 15:** UI Polish & Animations (Lottie + Error Handling) ✨
- [x] **Day 16:** Bulk Resume Screening (HR Mode) 📊
- [x] **Day 17:** Customizable Scoring & Thresholds (The Control Panel) 🎛️
- [x] **Day 18:** **Smart Caching (Real-Time Performance Optimization)** ⚡