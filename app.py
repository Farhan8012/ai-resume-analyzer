import streamlit as st
import pdfplumber

st.set_page_config(page_title="AI Resume Analyzer")

st.title("AI Resume Analyzer")

resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description")

def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

if st.button("Analyze Resume"):
    if resume_file is not None:
        resume_text = extract_text_from_pdf(resume_file)
        st.subheader("Extracted Resume Text")
        st.text(resume_text[:3000])  # show limited text
    else:
        st.warning("Please upload a resume PDF.")
