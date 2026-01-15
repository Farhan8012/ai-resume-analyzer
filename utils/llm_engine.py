import google.generativeai as genai
import streamlit as st

def get_ai_feedback(resume_text, job_description, missing_skills):
    """
    Sends the resume and JD to Google Gemini and gets personalized improvement advice.
    """
    try:
        # 1. Access the API Key from secrets.toml
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # 2. Use the Generic "Latest" model (Confirmed available in your list)
        model = genai.GenerativeModel('gemini-flash-latest')

        # 3. Create the Prompt
        prompt = f"""
        Act as a Senior Technical Recruiter and Career Coach. 
        I am applying for a job but my ATS score is low. Help me improve it.

        ---
        MY RESUME TEXT:
        {resume_text[:3000]} 

        JOB DESCRIPTION:
        {job_description[:3000]}
        
        MISSING SKILLS:
        {', '.join(missing_skills)}
        ---

        YOUR TASK:
        1. **Gap Analysis:** Briefly explain why my resume isn't a 100% match.
        2. **Rewrite Strategy:** Provide 3 specific bullet points I should add to my "Experience" section that incorporate the missing skills ({', '.join(missing_skills)}) naturally.
        3. **Summary Upgrade:** Write a new 2-sentence "Professional Summary" that targets this specific job.

        Output Format: Use bold headings and bullet points. Keep it encouraging but direct.
        """

        # 4. Get the Response
        with st.spinner("🤖 Consulting with AI Recruiter..."):
            response = model.generate_content(prompt)
            return response.text

    except Exception as e:
        return f"Error connecting to AI: {str(e)}"