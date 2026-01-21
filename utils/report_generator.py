from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO
import re  # <--- NEW: Added Regex library

def generate_pdf_report(name, match_score, semantic_score, missing_skills, ai_advice):
    """
    Generates a professional PDF report using ReportLab.
    Returns the raw bytes of the PDF file.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # --- CUSTOM STYLES ---
    title_style = styles['Title']
    title_style.textColor = colors.HexColor("#00C896")  # Our Mint Green
    
    header_style = ParagraphStyle(
        'Header',
        parent=styles['Heading2'],
        textColor=colors.HexColor("#262730"),
        spaceAfter=12
    )
    
    normal_style = styles['Normal']
    normal_style.spaceAfter = 10

    # --- 1. TITLE ---
    story.append(Paragraph(f"AI Resume Analysis Report", title_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Generated for: <b>{name}</b>", normal_style))
    story.append(Spacer(1, 20))

    # --- 2. SCORES TABLE ---
    data = [
        ["ATS Match Score", "Semantic Match (AI)"],
        [f"{match_score}%", f"{semantic_score}%"]
    ]
    
    t = Table(data, colWidths=[200, 200])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor("#0E1117")), # Dark Header
        ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 14),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor("#00C896")), # Green Scores
    ]))
    story.append(t)
    story.append(Spacer(1, 20))

    # --- 3. MISSING SKILLS ---
    story.append(Paragraph("Missing Skills Detected:", header_style))
    if missing_skills:
        skills_text = ", ".join([skill.title() for skill in missing_skills])
        story.append(Paragraph(skills_text, normal_style))
    else:
        story.append(Paragraph("None! Your resume matched all keywords.", normal_style))
    story.append(Spacer(1, 20))

    # --- 4. AI ADVICE ---
    story.append(Paragraph("AI Career Consultant Advice:", header_style))
    
    # --- CLEANUP LOGIC (FIXED) ---
    # 1. Replace newlines with break tags
    clean_advice = ai_advice.replace("\n", "<br />")
    
    # 2. Use Regex to replace **bold** with <b>bold</b> (Handles pairs correctly)
    clean_advice = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', clean_advice)
    
    # 3. Remove single asterisks (bullets) to prevent formatting errors
    clean_advice = clean_advice.replace("* ", "&bull; ")
    
    try:
        story.append(Paragraph(clean_advice, normal_style))
    except:
        # Fallback: If formatting still fails, strip all HTML and just show plain text
        clean_advice = re.sub('<[^<]+?>', '', clean_advice)
        story.append(Paragraph(clean_advice, normal_style))

    # --- BUILD PDF ---
    doc.build(story)
    buffer.seek(0)
    return buffer