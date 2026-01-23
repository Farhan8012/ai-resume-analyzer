import google.generativeai as genai
import streamlit as st
import os

try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    api_key = os.getenv("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

def get_ai_feedback(resume_text, jd_text, missing_skills):
    """
    Asks Gemini to provide actionable advice on HOW to fill the missing gaps.
    """
    if not api_key:
        return "⚠️ Google API Key not found. Please check your secrets.toml file."

    # Create a focused prompt
    missing_str = ", ".join(missing_skills) if missing_skills else "None"
    
    # --- THIS IS THE NEW DAY 14 PROMPT ---
    prompt = f"""
    Act as a Senior Technical Recruiter and Career Coach. 
    I have a candidate's resume and a job description.
    
    The system has detected these MISSING SKILLS: {missing_str}
    
    Your task:
    1. For the top 3 most important missing skills, suggest a SPECIFIC mini-project or certification to prove them.
       (e.g., if missing 'Docker', suggest "Containerize your existing Python script").
    2. Provide a 'Power Statement' the candidate can add to their resume for each skill once they learn it.
    3. Keep it encouraging but direct.
    
    RESUME CONTENT:
    {resume_text[:2000]}
    
    JOB DESCRIPTION:
    {jd_text[:1000]}
    """
    
    try:
        # --- WE KEEP YOUR WORKING MODEL HERE ---
        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating advice: {str(e)}"