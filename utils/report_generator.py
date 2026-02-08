from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO

def generate_pdf_report(name, match_score, semantic_score, missing_skills, ai_advice, interview_q=None, study_plan=None, improved_bullets=None):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Custom Styles
    title_style = styles['Title']
    heading_style = styles['Heading2']
    normal_style = styles['Normal']
    
    # --- TITLE SECTION ---
    story.append(Paragraph(f"AI Career Report for {name}", title_style))
    story.append(Spacer(1, 12))
    
    # --- SCORES ---
    story.append(Paragraph("1. Performance Scores", heading_style))
    data = [
        ["Metric", "Score"],
        ["ATS Match", f"{match_score}%"],
        ["Semantic Match", f"{semantic_score}%"]
    ]
    t = Table(data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(t)
    story.append(Spacer(1, 12))

    # --- MISSING SKILLS ---
    story.append(Paragraph("2. Missing Skills", heading_style))
    if missing_skills:
        skills_text = ", ".join(missing_skills)
        story.append(Paragraph(f"<b>Critical Gaps:</b> {skills_text}", normal_style))
    else:
        story.append(Paragraph("No critical skills missing!", normal_style))
    story.append(Spacer(1, 12))

    # --- AI ADVICE ---
    story.append(Paragraph("3. Strategic Advice", heading_style))
    story.append(Paragraph(ai_advice, normal_style))
    story.append(Spacer(1, 12))

    # --- NEW: INTERVIEW PREP ---
    if interview_q:
        story.append(Paragraph("4. Custom Interview Questions", heading_style))
        # Clean up markdown asterisks if present
        clean_q = interview_q.replace("**", "").replace("*", "-")
        story.append(Paragraph(clean_q.replace("\n", "<br/>"), normal_style))
        story.append(Spacer(1, 12))

    # --- NEW: STUDY PLAN ---
    if study_plan:
        story.append(Paragraph("5. 1-Week Study Roadmap", heading_style))
        clean_plan = study_plan.replace("**", "").replace("*", "-")
        story.append(Paragraph(clean_plan.replace("\n", "<br/>"), normal_style))
        story.append(Spacer(1, 12))
        
    # --- NEW: IMPROVED BULLETS ---
    if improved_bullets:
        story.append(Paragraph("6. Resume Improvements", heading_style))
        clean_bullets = improved_bullets.replace("**", "").replace("*", "-")
        story.append(Paragraph(clean_bullets.replace("\n", "<br/>"), normal_style))
        story.append(Spacer(1, 12))

    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer