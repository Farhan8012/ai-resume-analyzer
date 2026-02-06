import google.generativeai as genai
import streamlit as st

def generate_study_plan(missing_skills):
    """
    Generates a 5-day crash course for the identified missing skills.
    """
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # Using the Flash model as it's faster for generating long lists
        model = genai.GenerativeModel('gemini-1.5-flash')

        skills_text = ", ".join(missing_skills)

        prompt = f"""
        You are a Senior Technical Mentor.
        The candidate is missing the following skills: {skills_text}.
        
        Create a customized "5-Day Crash Course" to help them learn the basics of these skills efficiently.
        
        STRUCTURE:
        - **Day 1-2: Concepts & Basics** (What is it? Why use it?)
        - **Day 3-4: Hands-on Practice** (Simple exercises or commands)
        - **Day 5: Mini Project Idea** (How to apply it to a resume project)
        - **Recommended Resources:** (Suggest specific official docs, YouTube channels, or free courses).
        
        Keep it concise, actionable, and encouraging.
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Error generating roadmap: {str(e)}"