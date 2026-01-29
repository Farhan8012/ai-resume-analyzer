import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
import pandas as pd
from collections import Counter

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

def plot_comparison(match_a, match_b, semantic_a, semantic_b):
    """Plots a grouped bar chart comparing two resumes."""
    fig = go.Figure()

    # Resume A Bars
    fig.add_trace(go.Bar(
        x=['ATS Match', 'Semantic Match'],
        y=[match_a, semantic_a],
        name='Resume A',
        marker_color='#00C896' # Green
    ))

    # Resume B Bars
    fig.add_trace(go.Bar(
        x=['ATS Match', 'Semantic Match'],
        y=[match_b, semantic_b],
        name='Resume B',
        marker_color='#FF4B4B' # Red/Pink
    ))

    fig.update_layout(
        barmode='group',
        title="Resume A vs. Resume B Score Comparison",
        yaxis_title="Score (%)",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    return fig


def plot_history_trend(history_data):
    """
    Plots the user's ATS and Semantic scores over time.
    """
    if not history_data:
        return None
        
    df = pd.DataFrame(history_data)
    
    # Melt dataframe for multi-line plot
    df_melt = df.melt(id_vars=["date"], value_vars=["match_score", "semantic_score"], 
                      var_name="Score Type", value_name="Score")
    
    fig = px.line(df_melt, x="date", y="Score", color="Score Type", 
                  title="📈 Your Improvement Over Time",
                  color_discrete_map={"match_score": "#00C896", "semantic_score": "#9B51E0"},
                  markers=True)
    
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
    return fig

def plot_top_missing_skills(history_data):
    """
    Finds and plots the most frequently missing skills across all scans.
    """
    if not history_data:
        return None
        
    all_missing = []
    for entry in history_data:
        # missing_skills is stored as a list in the JSON
        all_missing.extend(entry.get("missing_skills", []))
        
    if not all_missing:
        return None
        
    # Count frequency
    counts = Counter(all_missing)
    # Get Top 7
    top_skills = dict(counts.most_common(7))
    
    df = pd.DataFrame(list(top_skills.items()), columns=["Skill", "Count"])
    
    fig = px.bar(df, x="Count", y="Skill", orientation='h',
                 title="⚠️ Most Recurring Missing Skills",
                 color="Count", color_continuous_scale="Reds")
                 
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", 
                      font_color="white", yaxis=dict(autorange="reversed"))
    return fig




