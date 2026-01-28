import streamlit as st
from utils.auth import authenticate, save_user, save_history, get_user_history
import pandas as pd
from utils.report_generator import generate_pdf_report
from utils.pdf_reader import extract_text_from_pdf
from utils.text_cleaner import clean_text
from utils.section_extractor import extract_sections
from utils.ats_matcher import match_skills, extract_skills_from_text, get_learning_link, find_weak_bullets, find_unquantified_bullets, skills_without_evidence, SUGGESTION_TEMPLATES
from utils.semantic_matcher import calculate_semantic_match
from utils.visualizer import plot_gauge_chart, plot_skills_gap, plot_comparison
from utils.llm_engine import get_ai_feedback
from utils.csv_export import convert_df_to_csv
import requests
from streamlit_lottie import st_lottie
import time

def check_rate_limit():
    """
    Prevents users from spamming the Analyze button.
    Enforces a 10-second cooldown.
    """
    if "last_call" not in st.session_state:
        st.session_state.last_call = 0
    
    current_time = time.time()
    # Check if less than 10 seconds have passed since last click
    if current_time - st.session_state.last_call < 10: 
        wait_time = 10 - int(current_time - st.session_state.last_call)
        st.warning(f"⏳ Please wait {wait_time} seconds before analyzing again.")
        st.stop() # <--- Kills the process immediately
    else:
        # Update the last call time
        st.session_state.last_call = current_time

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def ui_footer():
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: grey; font-size: 14px;">
            Built with ❤️ by <b>Farhan Ansari</b> | Powered by <b>Google Gemini</b> & <b>Streamlit</b>
        </div>
        """, unsafe_allow_html=True
    )

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
    # Load the animation (A cool AI robot)
    lottie_ai = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_V9t630.json")

    st.title("🚀 AI Resume Analyzer")
    
    # Create two columns
    col1, col2 = st.columns([1, 2]) # Left is smaller (animation), Right is wider (login)

    with col1:
        # Display animation
        if lottie_ai:
            st_lottie(lottie_ai, height=250, key="ai_anim")
    
    with col2:
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
                    st.session_state.user_email = email # Store email for history
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
        st.title("🎛️ Controls")
        
        # --- NEW: ADVANCED SETTINGS ---
        with st.expander("⚙️ Scoring Settings", expanded=False):
            st.caption("Customize how the AI ranks candidates.")
            
            # 1. Weighted Scoring
            st.write("⚖️ **Score Weighting**")
            ats_weight = st.slider("ATS Keyword Importance (%)", 0, 100, 70)
            sem_weight = 100 - ats_weight
            st.write(f"🤖 Semantic Importance: **{sem_weight}%**")
            
            # 2. Threshold
            st.write("🚫 **Strict Mode**")
            cutoff_score = st.number_input("Minimum Passing Score", 0, 100, 50)
        
        st.divider()
        
        # Standard Inputs
        mode = st.radio("Analysis Mode", ["Single Resume", "Compare (A/B Test)", "Bulk Analysis (HR Mode)"])
        
        st.header("1. Job Description")
        job_description = st.text_area("Paste JD here...", height=200)
        
        st.header("2. Upload Resume(s)")
        
        if mode == "Single Resume":
            resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
            resume_b = None
            uploaded_files = None
            
        elif mode == "Compare (A/B Test)":
            resume_file = st.file_uploader("Upload Resume A (PDF)", type=["pdf"], key="res_a")
            resume_b = st.file_uploader("Upload Resume B (PDF)", type=["pdf"], key="res_b")
            uploaded_files = None
            
        else: # Bulk Mode
            resume_file = None
            resume_b = None
            uploaded_files = st.file_uploader("Upload Candidates (PDF)", type=["pdf"], accept_multiple_files=True)

        st.divider()
        analyze_button = st.button("🔍 Analyze")

   # --- LOGIC HANDLING ---
    if mode == "Single Resume":
        # ================= SINGLE MODE =================
        tab1, tab2 = st.tabs(["📊 Analysis", "📈 History"])
        
        with tab1:
            st.title("🚀 Single Resume Analysis")
            
            if analyze_button:
                check_rate_limit()
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
                        st.session_state.mode = "single"

                        # Save History
                        uid = st.session_state.get('user_email', st.session_state.user_name)
                        save_history(uid, match_pct, sem_score, missing)
                        st.toast("✅ Analysis saved!")
                else:
                    st.error("⚠️ Please upload a resume and paste a JD.")

            # Display Single Results
            if st.session_state.analysis_done and st.session_state.get("mode") == "single":
                res = st.session_state.analysis_results
                
                col1, col2 = st.columns(2)
                with col1:
                    fig = plot_gauge_chart(res["match_percentage"])
                    st.plotly_chart(fig, use_container_width=True)
                with col2:
                    st.metric("Semantic Score", f"{res['semantic_score']}%")
                
                st.divider()
                st.subheader("🤖 AI Advice")
                if st.button("✨ Get Advice"):
                    with st.spinner("Thinking..."):
                        advice = get_ai_feedback(res['cleaned_text'], res['jd_text'], res['missing_skills'])
                        st.session_state.ai_advice = advice
                        st.markdown(advice)

                st.divider()
                st.subheader("📄 Download Report")
                if st.button("Prepare PDF"):
                    advice_text = st.session_state.get("ai_advice", "No AI advice generated.")
                    pdf_data = generate_pdf_report(st.session_state.user_name, res['match_percentage'], res['semantic_score'], res['missing_skills'], advice_text)
                    st.download_button("⬇️ Download PDF", pdf_data, "report.pdf", "application/pdf")

        with tab2:
            st.header("📈 History")
            uid = st.session_state.get('user_email', st.session_state.user_name)
            hist = get_user_history(uid)
            if hist:
                st.line_chart(pd.DataFrame(hist).set_index("date")[["match_score", "semantic_score"]])

    elif mode == "Compare (A/B Test)":
        # ================= COMPARE MODE =================
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

                    st.session_state.compare_results = {
                        "match_a": match_a, "sem_a": sem_a,
                        "match_b": match_b, "sem_b": sem_b
                    }
                    st.session_state.compare_done = True
                    st.session_state.mode = "compare"
            else:
                st.error("⚠️ Please upload BOTH resumes and a JD.")

        if st.session_state.get("compare_done") and st.session_state.get("mode") == "compare":
            res = st.session_state.compare_results
            winner = "Resume A" if (res['match_a'] + res['sem_a']) > (res['match_b'] + res['sem_b']) else "Resume B"
            st.success(f"🏆 The Winner is: **{winner}**")

            c1, c2 = st.columns(2)
            with c1:
                st.info("📄 Resume A")
                st.metric("ATS Match", f"{res['match_a']}%")
            with c2:
                st.info("📄 Resume B")
                st.metric("ATS Match", f"{res['match_b']}%")

            fig = plot_comparison(res['match_a'], res['match_b'], res['sem_a'], res['sem_b'])
            st.plotly_chart(fig, use_container_width=True)

    else:
        # ================= BULK MODE (HR) =================
        st.title("📊 Bulk Resume Screening (HR Mode)")
        from utils.csv_export import convert_df_to_csv
        import time

        # Initialize Session State for Bulk Data if not exists
        if "bulk_results" not in st.session_state:
            st.session_state.bulk_results = []

        # --- PHASE 1: HEAVY LIFTING (Run AI Only When Button Clicked) ---
        if analyze_button:
            check_rate_limit()
            if uploaded_files and job_description:
                
                # Clear previous results
                st.session_state.bulk_results = []
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                total_files = len(uploaded_files)
                
                # Run Analysis Loop
                for i, file in enumerate(uploaded_files):
                    status_text.text(f"Analyzing candidate {i+1} of {total_files}: {file.name}...")
                    progress_bar.progress((i + 1) / total_files)
                    
                    # 1. Extraction & AI
                    text = clean_text(extract_text_from_pdf(file))
                    skills = extract_skills_from_text(text)
                    jd_clean = job_description.lower()
                    jd_skills = extract_skills_from_text(jd_clean)
                    match_pct, _, missing = match_skills(skills, jd_skills)
                    sem_score = calculate_semantic_match(text, jd_clean)
                    
                    # Store RAW data in Session State (Not the final score yet)
                    st.session_state.bulk_results.append({
                        "Candidate Name": file.name,
                        "ATS Match": match_pct,
                        "Semantic Match": sem_score,
                        "Missing Skills": list(missing) # Store as list
                    })
                    time.sleep(0.5) # Be nice to API

                st.success("✅ Analysis Complete!")
                st.rerun() # Force refresh to show results immediately
            else:
                st.error("⚠️ Please upload candidates and a JD.")

        # --- PHASE 2: LIGHT MATH (Run Every Time Slider Moves) ---
        if st.session_state.bulk_results:
            
            # 1. Get Settings from Sidebar
            # (These variables ats_weight, sem_weight, cutoff_score are already defined in your sidebar code)
            
            final_display_list = []
            
            # 2. Recalculate Scores INSTANTLY
            for candidate in st.session_state.bulk_results:
                final_score = (candidate["ATS Match"] * (ats_weight / 100)) + (candidate["Semantic Match"] * (sem_weight / 100))
                status = "✅ Pass" if final_score >= cutoff_score else "❌ Reject"
                
                final_display_list.append({
                    "Candidate Name": candidate["Candidate Name"],
                    "Status": status,
                    "Final Score": round(final_score, 1),
                    "ATS Match": candidate["ATS Match"],
                    "Semantic Match": candidate["Semantic Match"],
                    "Missing Skills": ", ".join(candidate["Missing Skills"][:5])
                })
            
            # 3. Display Leaderboard
            df = pd.DataFrame(final_display_list)
            df = df.sort_values(by="Final Score", ascending=False)
            
            st.subheader("🏆 Candidate Leaderboard")
            
            def highlight_status(val):
                color = '#d4edda' if val == "✅ Pass" else '#f8d7da'
                return f'background-color: {color}; color: black'

            st.dataframe(
                df.style.map(highlight_status, subset=['Status'])
                        .format({"Final Score": "{:.1f}", "ATS Match": "{:.1f}", "Semantic Match": "{:.1f}"}),
                use_container_width=True
            )
            
            # CSV Download
            csv = convert_df_to_csv(df)
            st.download_button("⬇️ Download CSV", csv, "HR_Report.csv", "text/csv")

        else:
            st.error("⚠️ Please upload candidates and a JD.")
                
# --- 3. THE CONTROLLER (WITH SAFETY NET) ---
if __name__ == "__main__":
    try:
        if st.session_state.logged_in:
            main_dashboard()
            ui_footer() # <--- Show footer in dashboard
        else:
            login_page()
            ui_footer() # <--- Show footer in login
            
    except Exception as e:
        # If ANYTHING crashes, we catch it here
        st.error("⚠️ An unexpected error occurred. Please refresh the page.")
        # Optionally print the error to console for you (the developer) to see
        print(f"CRASH LOG: {e}")