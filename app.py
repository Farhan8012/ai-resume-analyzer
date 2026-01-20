import streamlit as st
from utils.auth import authenticate, save_user, save_history, get_user_history
import pandas as pd
from utils.pdf_reader import extract_text_from_pdf
from utils.text_cleaner import clean_text
from utils.section_extractor import extract_sections
from utils.ats_matcher import match_skills, extract_skills_from_text, get_learning_link, find_weak_bullets, find_unquantified_bullets, skills_without_evidence, SUGGESTION_TEMPLATES
from utils.semantic_matcher import calculate_semantic_match
from utils.visualizer import plot_gauge_chart, plot_skills_gap
from utils.llm_engine import get_ai_feedback

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Resume Analyzer", page_icon="🚀", layout="wide")

# --- CUSTOM CSS ---
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

local_css("style.css")

# --- SESSION STATE ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = {}

# --- 1. LOGIN PAGE FUNCTION ---
def login_page():
    st.title("🚀 AI Resume Analyzer")
    st.subheader("Login to access the Pro Dashboard")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    # LOGIN TAB
    with tab1:
        email = st.text_input("Email Address", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Login"):
            user = authenticate(email, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user_name = user
                st.session_state.user_email = email
                st.success(f"Welcome back, {user}!")
                st.rerun() 
            else:
                st.error("Invalid email or password")

    # SIGN UP TAB
    with tab2:
        new_name = st.text_input("Full Name")
        new_email = st.text_input("Email Address", key="signup_email")
        new_pass = st.text_input("Password", type="password", key="signup_pass")
        
        if st.button("Create Account"):
            if new_name and new_email and new_pass:
                if save_user(new_email, new_pass, new_name):
                    st.success("Account created! Please go to Login tab.")
                else:
                    st.error("User already exists!")
            else:
                st.warning("Please fill all fields.")

# --- 2. MAIN DASHBOARD FUNCTION ---
def main_dashboard():
    # Sidebar Logout
    with st.sidebar:
        st.write(f"👤 **{st.session_state.user_name}**")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_name = ""
            if 'user_email' in st.session_state:
                del st.session_state.user_email
            st.rerun()
        st.divider()

    # --- INPUTS (Sidebar) ---
    with st.sidebar:
        st.header("1. Upload Resume")
        resume_file = st.file_uploader("Upload PDF", type=["pdf"])
        st.divider()
        st.header("2. Job Description")
        job_description = st.text_area("Paste JD here...", height=300)
        st.divider()
        analyze_button = st.button("🔍 Analyze Resume")

    # --- NEW: TABS FOR DASHBOARD ---
    tab1, tab2 = st.tabs(["📊 Current Analysis", "📈 Progress History"])

    # --- TAB 1: CURRENT ANALYSIS (Your Original Logic) ---
    with tab1:
        st.title("🚀 AI Resume Analyzer (Pro Dashboard)")

        if analyze_button:
            if resume_file is not None and job_description:
                with st.spinner("Processing..."):
                    # Processing Logic
                    raw_text = extract_text_from_pdf(resume_file)
                    cleaned_text = clean_text(raw_text)
                    sections = extract_sections(cleaned_text)
                    
                    resume_skills = extract_skills_from_text(cleaned_text)
                    jd_text = job_description.lower()
                    jd_skills = extract_skills_from_text(jd_text)
                    match_percentage, matched_skills, missing_skills = match_skills(resume_skills, jd_skills)
                    semantic_score = calculate_semantic_match(cleaned_text, jd_text)
                    
                    experience_text = sections.get("experience", "")
                    weak_bullets = find_weak_bullets(experience_text)
                    unquantified = find_unquantified_bullets(experience_text)
                    skills_no_evidence = skills_without_evidence(resume_skills, experience_text)

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
                    
                    # --- NEW: SAVE TO HISTORY ---
                    # We use the email (if available) or username as the ID
                    user_id = st.session_state.get('user_email', st.session_state.user_name)
                    save_history(user_id, match_percentage, semantic_score, missing_skills)
                    st.toast("✅ Result saved to history!")
                    
            else:
                st.sidebar.error("⚠️ Please upload a resume and paste a JD.")

        # Display Results
        if st.session_state.analysis_done:
            res = st.session_state.analysis_results
            
            st.subheader("Match Score Analysis")
            col1, col2 = st.columns([1, 1])
            with col1:
                fig = plot_gauge_chart(res["match_percentage"])
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                st.write("## ") 
                st.metric(label="Semantic Match (AI)", value=f"{res['semantic_score']}%", delta="Smart Context")
                
            st.divider()

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

            st.subheader("Visual Skill Gap Analysis")
            gap_fig = plot_skills_gap(res['resume_skills'], res['jd_skills'])
            st.plotly_chart(gap_fig, use_container_width=True)

            st.divider()

            st.subheader("Resume Quality Checks")
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

            st.subheader("🤖 AI Career Consultant")
            if st.button("✨ Generate Improvement Plan (Powered by Gemini)"):
                if not res['missing_skills']:
                    st.success("You have all the required skills!")
                else:
                    with st.spinner("Analyzing with Gemini..."):
                        ai_advice = get_ai_feedback(res['cleaned_text'], res['jd_text'], res['missing_skills'])
                        st.markdown("### 💡 Tailored Advice")
                        st.markdown(ai_advice)

        else:
            st.info("👈 Upload resume to see analysis.")

    # --- NEW: TAB 2 (PROGRESS HISTORY) ---
    with tab2:
        st.header("📈 Your Progress Over Time")
        
        # Get history using email (or username as fallback)
        user_id = st.session_state.get('user_email', st.session_state.user_name)
        history = get_user_history(user_id)
        
        if history:
            # Convert to DataFrame for easy plotting
            df = pd.DataFrame(history)
            
            # Create a line chart
            st.write("### ATS Score vs Semantic Score")
            st.line_chart(df.set_index("date")[["match_score", "semantic_score"]])
            
            # Show the raw data table
            st.write("### Detailed History Log")
            st.dataframe(df)
        else:
            st.info("No history found yet. Analyze a resume to start tracking!")

# --- 3. THE CONTROLLER ---
if st.session_state.logged_in:
    main_dashboard()
else:
    login_page()