import google.generativeai as genai
import streamlit as st

def ask_resume_question(resume_text, question):
    """
    Answers a specific question about the resume text.
    """
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # Use the model that works best for you (e.g., gemini-2.5-flash or gemini-1.5-flash)
        model = genai.GenerativeModel('gemini-2.5-flash')

        prompt = f"""
        You are an intelligent assistant helping a recruiter analyze a resume.
        
        RESUME TEXT:
        {resume_text}
        
        USER QUESTION:
        {question}
        
        INSTRUCTIONS:
        1. Answer the question based ONLY on the resume text provided.
        2. If the information is not in the resume, say "I cannot find that information in the resume."
        3. Be concise and professional.
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Error processing question: {str(e)}"