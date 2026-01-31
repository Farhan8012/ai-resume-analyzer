import google.generativeai as genai
import streamlit as st

def generate_interview_questions(resume_text, jd_text):
    """
    Generates 5 custom interview questions based on the candidate's specific experience.
    """
    try:
        # Load API Key
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-2.5-flash')

        prompt = f"""
        You are an expert Technical Interviewer. 
        I am going to give you a candidate's Resume and a Job Description.
        
        Your goal is to generate 5 TOUGH, specific interview questions.
        
        RULES:
        1. Do NOT ask generic questions (e.g., "Tell me about yourself").
        2. Ask specific technical questions based on the PROJECTS mentioned in the resume.
        3. If they mention a specific tool (e.g., "React"), ask how they handled a specific problem with it.
        4. Relate the questions to the Job Description requirements.
        
        RESUME TEXT:
        {resume_text[:2000]}
        
        JOB DESCRIPTION:
        {jd_text[:1000]}
        
        OUTPUT FORMAT:
        Return exactly 5 questions, numbered 1 to 5.
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Error generating questions: {str(e)}"