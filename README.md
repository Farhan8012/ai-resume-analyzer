# 🚀 AI Career Coach: The Ultimate Resume Analyzer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://farhan-ai-resume.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-orange?logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

> **A full-stack AI Career Assistant that helps job seekers beat the ATS, rewrite their resumes, and prep for interviews.**

---

## 🌟 Live Demo
👉 **[Click here to use the App](https://farhan-ai-resume.streamlit.app/)** *(Note: Replace this link with your actual Streamlit URL)*

---

## 🧠 What Problem Does This Solve?
Job seekers struggle with:
1.  **ATS Rejection:** "Why did I get rejected instantly?"
2.  **Generic Advice:** "Your resume needs work" (but doesn't say *where*).
3.  **Writer's Block:** Not knowing how to phrase bullet points.

**This tool fixes that by mimicking a Senior Technical Recruiter.** It doesn't just "score" you; it rewrites your text, generates cover letters, and creates a 7-day study plan for your missing skills.

---

## 📸 Screenshots

### 1. The Dashboard (Score & Analysis)
![Dashboard](https://github.com/Farhan8012/ai-resume-analyzer/blob/main/screenshots/dashboard.jpg?raw=true)

### 2. AI Resume Chat (RAG)
![Chat](https://github.com/Farhan8012/ai-resume-analyzer/blob/main/screenshots/chat.jpg?raw=true)

### 3. Study Plan Generator
![Roadmap](https://github.com/Farhan8012/ai-resume-analyzer/blob/main/screenshots/roadmap.jpg?raw=true)

---

## 🛠️ Key Features

| Feature | Description | Tech Stack |
| :--- | :--- | :--- |
| **📊 ATS Scoring** | Calculates a % match based on Keywords & Semantics. | `TF-IDF`, `Cosine Similarity` |
| **✨ AI Rewriter** | Rewrites weak bullet points into "Action-Result" statements. | `Google Gemini 1.5 Flash` |
| **💬 Chat with Resume** | Ask questions like *"Does he know Docker?"* to the PDF. | `RAG (Retrieval Augmented Generation)` |
| **📚 Smart Study Plan** | Generates a 7-day crash course for missing skills. | `Generative AI` |
| **📄 Cover Letter** | Auto-drafts a personalized cover letter for the role. | `Prompt Engineering` |
| **🎙️ Interview Prep** | Generates tough interview questions based on your projects. | `Gemini Pro` |

---

## ⚙️ Installation (Run Locally)

1. **Clone the Repo**
   ```bash
   git clone [https://github.com/Farhan8012/ai-resume-analyzer.git](https://github.com/Farhan8012/ai-resume-analyzer.git)
   cd ai-resume-analyzer

   Install Dependencies


2. pip install -r requirements.txt
Set up Secrets Create a .streamlit/secrets.toml file and add your Google API Key:


3. GOOGLE_API_KEY = "your_api_key_here"


4.Run the App
streamlit run app.py
🤝 Contribution
Built with ❤️ by Farhan Ansari.

Feel free to fork this repo and submit Pull Requests!