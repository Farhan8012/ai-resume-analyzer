import streamlit as st
from utils.auth import authenticate, save_user, save_history, get_user_history
import pandas as pd
from utils.report_generator import generate_pdf_report
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

    # --- SIDEBAR INPUTS ---
    with st.sidebar:
        st.title("🎛️ Settings")
        mode = st.radio("Analysis Mode", ["Single Resume", "Compare (A/B Test)"])
        st.divider()
        
        # JD Input (Common for both modes)
        st.header("1. Job Description")
        job_description = st.text_area("Paste JD here...", height=200)
        st.divider()

        # Resume Inputs
        st.header("2. Upload Resume(s)")
        if mode == "Single Resume":
            resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
            resume_b = None # Not used in this mode
        else:
            resume_file = st.file_uploader("Upload Resume A (PDF)", type=["pdf"], key="res_a")
            resume_b = st.file_uploader("Upload Resume B (PDF)", type=["pdf"], key="res_b")

        st.divider()
        analyze_button = st.button("🔍 Analyze")

    # --- LOGIC HANDLING ---
    if mode == "Single Resume":
        # ================= SINGLE MODE (Your Old Dashboard) =================
        tab1, tab2 = st.tabs(["📊 Analysis", "📈 History"])
        
        with tab1:
            st.title("🚀 Single Resume Analysis")
            
            if analyze_button:
                if resume_file and job_description:
                    with st.spinner("Processing..."):
                        # Extract & Analyze
                        raw_text = extract_text_from_pdf(resume_file)
                        cleaned_text = clean_text(raw_text)
                        sections = extract_sections(cleaned_text)
                        resume_skills = extract_skills_from_text(cleaned_text)
                        jd_text = job_description.lower()
                        jd_skills = extract_skills_from_text(jd_text)
                        match_pct, matched, missing = match_skills(resume_skills, jd_skills)
                        sem_score = calculate_semantic_match(cleaned_text, jd_text)
                        
                        # Checks
                        exp_text = sections.get("experience", "")
                        weak_bullets = find_weak_bullets(exp_text)
                        unquantified = find_unquantified_bullets(exp_text)
                        skills_no_ev = skills_without_evidence(resume_skills, exp_text)

                        # Save to State
                        st.session_state.analysis_results = {
                            "match_percentage": match_pct,
                            "semantic_score": sem_score,
                            "matched_skills": matched,
                            "missing_skills": missing,
                            "resume_skills": resume_skills,
                            "jd_skills": jd_skills,
                            "cleaned_text": cleaned_text,
                            "jd_text": jd_text,
                            "weak_bullets": weak_bullets,
                            "unquantified": unquantified,
                            "skills_no_evidence": skills_no_ev
                        }
                        st.session_state.analysis_done = True
                        st.session_state.mode = "single" # Track which mode we ran

                        # Save History
                        uid = st.session_state.get('user_email', st.session_state.user_name)
                        save_history(uid, match_pct, sem_score, missing)
                        st.toast("✅ Analysis saved!")
                else:
                    st.error("⚠️ Please upload a resume and paste a JD.")

            # Display Single Results
            if st.session_state.analysis_done and st.session_state.get("mode") == "single":
                res = st.session_state.analysis_results
                
                # Metrics
                col1, col2 = st.columns(2)
                with col1:
                    fig = plot_gauge_chart(res["match_percentage"])
                    st.plotly_chart(fig, use_container_width=True)
                with col2:
                    st.metric("Semantic Score", f"{res['semantic_score']}%")
                
                # AI Advice
                st.divider()
                st.subheader("🤖 AI Advice")
                if st.button("✨ Get Advice"):
                    with st.spinner("Thinking..."):
                        advice = get_ai_feedback(res['cleaned_text'], res['jd_text'], res['missing_skills'])
                        st.session_state.ai_advice = advice
                        st.markdown(advice)

                # PDF Download (Your Day 12 Feature)
                st.divider()
                st.subheader("📄 Download Report")
                if st.button("Prepare PDF"):
                    advice_text = st.session_state.get("ai_advice", "No AI advice generated.")
                    pdf_data = generate_pdf_report(st.session_state.user_name, res['match_percentage'], res['semantic_score'], res['missing_skills'], advice_text)
                    st.download_button("⬇️ Download PDF", pdf_data, "report.pdf", "application/pdf")

        # History Tab (Same as before)
        with tab2:
            st.header("📈 History")
            uid = st.session_state.get('user_email', st.session_state.user_name)
            hist = get_user_history(uid)
            if hist:
                st.line_chart(pd.DataFrame(hist).set_index("date")[["match_score", "semantic_score"]])

    else:
        # ================= COMPARE MODE (NEW!) =================
        st.title("⚔️ Resume Battle Mode (A vs B)")
        
        if analyze_button:
            if resume_file and resume_b and job_description:
                with st.spinner("Analyzing Both Resumes..."):
                    # Process A
                    text_a = clean_text(extract_text_from_pdf(resume_file))
                    skills_a = extract_skills_from_text(text_a)
                    jd_clean = job_description.lower()
                    jd_skills = extract_skills_from_text(jd_clean)
                    match_a, _, _ = match_skills(skills_a, jd_skills)
                    sem_a = calculate_semantic_match(text_a, jd_clean)

                    # Process B
                    text_b = clean_text(extract_text_from_pdf(resume_b))
                    skills_b = extract_skills_from_text(text_b)
                    match_b, _, _ = match_skills(skills_b, jd_skills)
                    sem_b = calculate_semantic_match(text_b, jd_clean)

                    # Save Comparison Results
                    st.session_state.compare_results = {
                        "match_a": match_a, "sem_a": sem_a,
                        "match_b": match_b, "sem_b": sem_b
                    }
                    st.session_state.compare_done = True
                    st.session_state.mode = "compare"
            else:
                st.error("⚠️ Please upload BOTH resumes and a JD.")

        # Display Comparison
        if st.session_state.get("compare_done") and st.session_state.get("mode") == "compare":
            res = st.session_state.compare_results
            
            # 1. The Winner Banner
            winner = "Resume A" if (res['match_a'] + res['sem_a']) > (res['match_b'] + res['sem_b']) else "Resume B"
            st.success(f"🏆 The Winner is: **{winner}**")

            # 2. Side-by-Side Metrics
            c1, c2 = st.columns(2)
            with c1:
                st.info("📄 Resume A")
                st.metric("ATS Match", f"{res['match_a']}%")
                st.metric("Semantic Match", f"{res['sem_a']}%")
            with c2:
                st.info("📄 Resume B")
                st.metric("ATS Match", f"{res['match_b']}%")
                st.metric("Semantic Match", f"{res['sem_b']}%")

            # 3. Comparison Chart
            from utils.visualizer import plot_comparison
            st.divider()
            st.subheader("📊 Head-to-Head Comparison")
            fig = plot_comparison(res['match_a'], res['match_b'], res['sem_a'], res['sem_b'])
            st.plotly_chart(fig, use_container_width=True)
            
# --- 3. THE CONTROLLER ---
if st.session_state.logged_in:
    main_dashboard()
else:
    login_page()