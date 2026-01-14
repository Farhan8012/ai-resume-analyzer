import streamlit as st

from utils.visualizer import plot_gauge_chart, plot_skills_gap
from utils.ats_matcher import (
    extract_skills_from_text,
    get_learning_link,
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

        # 2. Clean text
        cleaned_text = clean_text(raw_text)

        # 3. Extract sections
        sections = extract_sections(cleaned_text)

        # 4. ATS & Semantic Analysis
        st.subheader("ATS Match Result")

        # A. Strict Match
        resume_skills = extract_skills_from_text(cleaned_text)
        jd_text = job_description.lower()
        jd_skills = extract_skills_from_text(jd_text)
        
        match_percentage, matched_skills, missing_skills = match_skills(resume_skills, jd_skills)

        # B. Semantic Match
        semantic_score = calculate_semantic_match(cleaned_text, jd_text)

        
       # C. Display Scores (With Interactive Gauge)
        st.subheader("Match Score Analysis")

        col1, col2 = st.columns([1, 1]) # Equal width columns

        with col1:
            # Display the Gauge Chart for the Strict ATS Score
            fig = plot_gauge_chart(match_percentage)
            st.plotly_chart(fig, use_container_width=True)
            st.caption("**Strict Match:** Based on exact keywords found.")

        with col2:
            # Keep the Metric for the AI Score (clean contrast)
            st.write("## ") # Spacing to align vertically
            st.metric(label="Semantic Match (AI)", value=f"{semantic_score}%", delta="Smart Context")
            st.caption("**Semantic Match:** Based on meaning & relevance.")


        # D. Smart Feedback
        if semantic_score > match_percentage + 15:
            st.info("💡 **Insight:** Your resume is contextually relevant, but missing specific keywords. Add the skills below.")
        elif match_percentage > semantic_score + 15:
            st.warning("⚠️ **Warning:** You have the keywords, but the context is weak. Ensure your bullet points support your skills.")

        st.divider()

        # E. Display Skills (Only Once!)
        c1, c2 = st.columns(2)
        with c1:
            st.write("✅ **Matched Skills**")
            st.write(matched_skills if matched_skills else "None")
        with c2:
            st.write("❌ **Missing Skills**")
            if missing_skills:
                for skill in missing_skills:
                    link = get_learning_link(skill)
                    if link:
                        st.markdown(f"• **{skill}** ([Learn Here]({link}))")
                    else:
                        st.write(f"• {skill}")
            else:
                st.write("None")

        # F. Skill Gap Chart
        st.subheader("Visual Skill Gap Analysis")
        gap_fig = plot_skills_gap(resume_skills, jd_skills)
        st.plotly_chart(gap_fig, use_container_width=True)

        st.divider()

        # 5. Resume Quality Checks
        st.subheader("Resume Quality Checks")
        experience_text = sections.get("experience", "")

        weak_bullets = find_weak_bullets(experience_text)
        unquantified = find_unquantified_bullets(experience_text)
        skills_no_evidence = skills_without_evidence(resume_skills, experience_text)

        if not weak_bullets and not unquantified and not skills_no_evidence:
             st.success("🎉 Incredible! Your resume bullets are strong, quantified, and backed by evidence.")
        else:
            if weak_bullets:
                st.write("⚠️ **Weak Action Verbs (Replace with Power Words)**")
                for line in weak_bullets:
                    st.text(f"• {line}")

            if unquantified:
                st.write("⚠️ **Bullets Without Numbers (Quantify these!)**")
                for line in unquantified:
                    st.text(f"• {line}")

            if skills_no_evidence:
                st.write("⚠️ **Skills Listed but Not Demonstrated**")
                for skill in skills_no_evidence:
                    st.write(f"• **{skill.title()}** (Found in Skills, but not in Experience)")
                    suggestion = SUGGESTION_TEMPLATES.get(skill.lower())
                    if suggestion:
                        st.caption(f"   💡 Try: *{suggestion}*")

        st.divider()

        # 6. Display Raw Sections (For Debugging)
        with st.expander("View Extracted Sections"):
            st.write("### Skills")
            st.write(sections.get("skills", "Not found"))
            st.write("### Education")
            st.write(sections.get("education", "Not found"))
            st.write("### Experience")
            st.write(sections.get("experience", "Not found"))

    



        
