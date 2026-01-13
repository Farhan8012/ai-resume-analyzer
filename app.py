import streamlit as st
from utils.ats_matcher import (
    extract_skills_from_text,
    match_skills,
    find_weak_bullets,
    find_unquantified_bullets,
    skills_without_evidence
)

from utils.ats_matcher import SUGGESTION_TEMPLATES
from utils.pdf_reader import extract_text_from_pdf
from utils.text_cleaner import clean_text
from utils.section_extractor import extract_sections
from utils.semantic_matcher import calculate_semantic_match
st.set_page_config(page_title="AI Resume Analyzer")
st.title("AI Resume Analyzer")

resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
st.subheader("Job Description")
job_description = st.text_area(
    "Paste the job description here",
    height=200
)

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
        sections = extract_sections(cleaned_text)

        resume_sections = sections  # lock extracted resume sections
 
        st.subheader("ATS Match Result")

        # 1. Keyword Match (Strict ATS)
        resume_skills = extract_skills_from_text(cleaned_text)
        jd_text = job_description.lower()
        jd_skills = extract_skills_from_text(jd_text)
        
        # Calculate strict match
        match_percentage, matched_skills, missing_skills = match_skills(resume_skills, jd_skills)

        # 2. Semantic Match (AI Analysis)
        semantic_match = calculate_semantic_match(cleaned_text, jd_text)

        # 3. Display Scores Side-by-Side
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="ATS Keyword Match", value=f"{match_percentage}%", delta="Strict")
        with col2:
            st.metric(label="Semantic Match (AI)", value=f"{semantic_match}%", delta="Smart")

        # 4. Smart Feedback
        if semantic_match > match_percentage + 15:
            st.info("💡 **Insight:** Your resume is contextually relevant to this job, but you are missing specific keywords. Add the missing skills below to pass the automated filters.")
        elif match_percentage > semantic_match + 15:
            st.warning("⚠️ **Warning:** You have the keywords, but the context of your resume doesn't strongly match the job description. Ensure your bullet points support your skills.")

        st.divider() # Adds a nice visual line

        st.write("✅ **Matched Skills**")
        st.write(matched_skills if matched_skills else "None")

        st.write("❌ **Missing Skills**")
        st.write(missing_skills if missing_skills else "None")


        jd_text = job_description.lower()
        jd_skills = extract_skills_from_text(jd_text)

        if job_description.strip():
            match_percentage, matched_skills, missing_skills = match_skills(
                resume_skills,
                jd_skills
            )

            st.metric("ATS Match %", f"{match_percentage}%")

            st.write("✅ Matched Skills")
            st.write(matched_skills if matched_skills else "None")

            st.write("❌ Missing Skills")
            st.write(missing_skills if missing_skills else "None")

            # ✅ Resume Quality Checks (ONLY when JD exists)
            experience_text = resume_sections.get("experience", "")



            st.subheader("DEBUG: Experience Text Used for Evidence Check")
            st.text(experience_text)


            st.subheader("Resume Quality Checks")

            weak_bullets = find_weak_bullets(experience_text)
            unquantified = find_unquantified_bullets(experience_text)
            skills_no_evidence = skills_without_evidence(resume_skills, experience_text)

            st.write("⚠ Weak Experience Bullets")
            st.write(weak_bullets if weak_bullets else "None")

            st.write("⚠ Bullets Without Numbers")
            st.write(unquantified if unquantified else "None")

            st.write("⚠ Skills Without Evidence")

            if skills_no_evidence:
                for skill in skills_no_evidence:
                    st.write(f"• {skill} → Not demonstrated in experience section")

                    suggestion = SUGGESTION_TEMPLATES.get(skill.lower())
                    if suggestion:
                        st.caption(f"💡 Example: {suggestion}")
            else:
                st.write("None")

            

        else:
            st.info("Please paste a Job Description to calculate ATS match.")


        
        
        

        


        # 4. Display sections
        st.subheader("Extracted Resume Sections")

        st.write("### Skills")
        st.write(sections.get("skills", "Not found"))

        st.write("### Education")
        st.write(sections.get("education", "Not found"))

        st.write("### Experience")
        st.write(sections.get("experience", "Not found"))

        st.write("DEBUG JD Skills:", jd_skills)


    



        
