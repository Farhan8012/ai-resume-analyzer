import plotly.graph_objects as go

def plot_gauge_chart(score):
    """
    Creates a professional gauge chart for the Resume Score.
    """
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "ATS Score", 'font': {'size': 24}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#00ff41"}, # Hacker Green
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': "#ff4b4b"},  # Red (Low)
                {'range': [50, 75], 'color': "#ffa500"}, # Orange (Medium)
                {'range': [75, 100], 'color': "#21c354"} # Green (High)
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", # Transparent background
        font={'color': "white", 'family': "Arial"},
        height=300,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig

def plot_skills_gap(resume_skills, jd_skills):
    """
    Creates a Venn-style bar chart comparing Resume Skills vs JD Skills.
    """
    # 1. Logic
    matched = resume_skills.intersection(jd_skills)
    missing = jd_skills - resume_skills
    extra = resume_skills - jd_skills # Skills you have that the job didn't ask for
    
    # 2. Prepare Data
    categories = ['Matched', 'Missing', 'Extra Qualities']
    values = [len(matched), len(missing), len(extra)]
    colors = ['#21c354', '#ff4b4b', '#3498db'] # Green, Red, Blue
    
    # 3. Create Chart
    fig = go.Figure(data=[go.Bar(
        x=categories,
        y=values,
        marker_color=colors,
        text=values,
        textposition='auto',
    )])
    
    fig.update_layout(
        title="Skill Gap Analysis",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white"},
        height=300,
        yaxis=dict(showgrid=False) # Clean look
    )
    
    return fig