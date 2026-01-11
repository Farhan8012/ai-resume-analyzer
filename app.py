import streamlit as st
from utils.pdf_reader import extract_text_from_pdf
from utils.text_cleaner import clean_text
from utils.section_extractor import extract_sections

st.set_page_config(page_title="AI Resume Analyzer")
st.title("AI Resume Analyzer")

resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description")

if st.button("Analyze Resume"):
    if resume_file is not None:
        # 1. Extract text
        raw_text = extract_text_from_pdf(resume_file)

        # 🔍 DEBUG: show raw extracted text
        st.subheader("DEBUG: Raw Extracted Text")
        st.text(raw_text[:2000])

        # 2. Clean text
        cleaned_text = clean_text(raw_text)

        # 3. Extract sections
        sections = extract_sections(raw_text)

        sections["skills"] = clean_text(sections["skills"])
        sections["education"] = clean_text(sections["education"])
        sections["experience"] = clean_text(sections["experience"])

        # 4. Display sections
        st.subheader("Extracted Resume Sections")

        st.write("### Skills")
        st.write(sections.get("skills", "Not found"))

        st.write("### Education")
        st.write(sections.get("education", "Not found"))

        st.write("### Experience")
        st.write(sections.get("experience", "Not found"))

        # 🔍 DEBUG cleaned text
        st.subheader("DEBUG: Cleaned Resume Text")
        st.text(cleaned_text[:2000])



        
