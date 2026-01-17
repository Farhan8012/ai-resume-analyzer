import streamlit as st
from utils.pdf_reader import extract_text_from_pdf
from utils.text_cleaner import clean_text
from utils.section_extractor import extract_sections
from utils.ats_matcher import match_skills, extract_skills_from_text, get_learning_link, find_weak_bullets, find_unquantified_bullets, skills_without_evidence, SUGGESTION_TEMPLATES
from utils.semantic_matcher import calculate_semantic_match
from utils.visualizer import plot_gauge_chart, plot_skills_gap
from utils.llm_engine import get_ai_feedback

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Resume Analyzer", page_icon="🚀", layout="wide")

# --- LOAD CUSTOM CSS ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

try:
    local_css("style.css")
except FileNotFoundError:
    st.warning("⚠️ Style file not found. Please ensure 'style.css' is in the main folder.")

# --- TITLE ---
st.title("🚀 AI Resume Analyzer (Pro Dashboard)")
st.markdown("### Optimize your resume for ATS & Semantic Search")

# --- SIDEBAR (INPUTS) ---
with st.sidebar:
    st.header("1. Upload Resume")
    resume_file = st.file_uploader("Upload PDF", type=["pdf"])
    
    st.divider()
    
    st.header("2. Job Description")
    job_description = st.text_area("Paste JD here...", height=300)
    
    st.divider()
    
    analyze_button = st.button("🔍 Analyze Resume")

# --- SESSION STATE ---
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
    st.session_state.analysis_results = {}

# --- MAIN LOGIC ---
if analyze_button:
    if resume_file is not None and job_description:
        with st.spinner("Processing..."):
            # A. Extract & Clean
            raw_text = extract_text_from_pdf(resume_file)
            cleaned_text = clean_text(raw_text)
            sections = extract_sections(cleaned_text)
            
            # B. Match Skills (Strict)
            resume_skills = extract_skills_from_text(cleaned_text)
            jd_text = job_description.lower()
            jd_skills = extract_skills_from_text(jd_text)
            match_percentage, matched_skills, missing_skills = match_skills(resume_skills, jd_skills)
            
            # C. Semantic Match (AI)
            semantic_score = calculate_semantic_match(cleaned_text, jd_text)
            
            # D. Quality Checks
            experience_text = sections.get("experience", "")
            weak_bullets = find_weak_bullets(experience_text)
            unquantified = find_unquantified_bullets(experience_text)
            skills_no_evidence = skills_without_evidence(resume_skills, experience_text)

            # SAVE RESULTS
            st.session_state.analysis_results = {
                "match_percentage": match_percentage,
                "semantic_score": semantic_score,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "resume_skills": resume_skills,
                "jd_skills": jd_skills,
                "cleaned_text": cleaned_text,
                "jd_text": jd_text,
                "weak_bullets": weak_bullets,
                "unquantified": unquantified,
                "skills_no_evidence": skills_no_evidence,
                "sections": sections
            }
            st.session_state.analysis_done = True
            
    else:
        st.sidebar.error("⚠️ Please upload a resume and paste a JD.")

# --- DISPLAY RESULTS (Main Area) ---
if st.session_state.analysis_done:
    res = st.session_state.analysis_results
    
    # 1. Match Score Analysis
    st.subheader("Match Score Analysis")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        fig = plot_gauge_chart(res["match_percentage"])
        st.plotly_chart(fig, use_container_width=True)
        st.caption("**Strict Match:** Based on exact keywords found.")

    with col2:
        st.write("## ") 
        st.metric(label="Semantic Match (AI)", value=f"{res['semantic_score']}%", delta="Smart Context")
        st.caption("**Semantic Match:** Based on meaning & relevance.")

    # Feedback based on score
    if res['semantic_score'] > res['match_percentage'] + 15:
        st.info("💡 **Insight:** Your resume is contextually relevant, but missing specific keywords. Add the skills below.")
    elif res['match_percentage'] > res['semantic_score'] + 15:
        st.warning("⚠️ **Warning:** You have the keywords, but the context is weak. Ensure your bullet points support your skills.")

    st.divider()

    # 2. Skills Breakdown
    c1, c2 = st.columns(2)
    with c1:
        st.write("✅ **Matched Skills**")
        st.write(res['matched_skills'] if res['matched_skills'] else "None")
    with c2:
        st.write("❌ **Missing Skills**")
        if res['missing_skills']:
            for skill in res['missing_skills']:
                link = get_learning_link(skill)
                if link:
                    st.markdown(f"• **{skill}** ([Learn Here]({link}))")
                else:
                    st.write(f"• {skill}")
        else:
            st.write("None")

    st.divider()

    # 3. Gap Analysis Chart
    st.subheader("Visual Skill Gap Analysis")
    gap_fig = plot_skills_gap(res['resume_skills'], res['jd_skills'])
    st.plotly_chart(gap_fig, use_container_width=True)

    st.divider()

    # 4. Resume Quality Checks
    st.subheader("Resume Quality Checks")
    
    if not res['weak_bullets'] and not res['unquantified'] and not res['skills_no_evidence']:
         st.success("🎉 Incredible! Your resume bullets are strong, quantified, and backed by evidence.")
    else:
        if res['weak_bullets']:
            st.write("⚠️ **Weak Action Verbs**")
            for line in res['weak_bullets']:
                st.text(f"• {line}")
        
        if res['unquantified']:
            st.write("⚠️ **Bullets Without Numbers**")
            for line in res['unquantified']:
                st.text(f"• {line}")

        if res['skills_no_evidence']:
            st.write("⚠️ **Skills Listed but Not Demonstrated**")
            for skill in res['skills_no_evidence']:
                st.write(f"• **{skill.title()}** (Found in Skills, but not in Experience)")
                suggestion = SUGGESTION_TEMPLATES.get(skill.lower())
                if suggestion:
                    st.caption(f"   💡 Try: *{suggestion}*")

    st.divider()

    # 5. Generative AI Section
    st.subheader("🤖 AI Career Consultant")
    
    if st.button("✨ Generate Improvement Plan (Powered by Gemini)"):
        if not res['missing_skills']:
            st.success("You have all the required skills! The AI recommends applying immediately.")
        else:
            with st.spinner("Analyzing with Gemini..."):
                ai_advice = get_ai_feedback(res['cleaned_text'], res['jd_text'], res['missing_skills'])
                st.markdown("### 💡 Tailored Advice")
                st.markdown(ai_advice)

    st.divider()

    # Debug Section
    with st.expander("View Extracted Sections"):
        st.write("### Skills")
        st.write(res['sections'].get("skills", "Not found"))
        st.write("### Experience")
        st.write(res['sections'].get("experience", "Not found"))

# --- PLACEHOLDER (If no analysis yet) ---
else:
    st.info("👈 Upload your resume and job description in the sidebar to start!")