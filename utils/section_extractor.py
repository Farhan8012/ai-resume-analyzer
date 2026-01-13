import re

SECTION_KEYWORDS = {
    "skills": [
        "skills", "technical skills", "technologies", "tools", "expertise"
    ],
    "education": [
        "education", "academic", "qualification", "degree"
    ],
    "experience": [
        "experience", "work experience", "employment", "internship", "projects"
    ]
}

def extract_sections(text):
    sections = {
        "skills": "",
        "education": "",
        "experience": ""
    }

    current_section = None
    lines = text.split("\n")

    for line in lines:
        line_strip = line.strip()

        if not line_strip:
            continue

        upper_line = line_strip.upper()

        if upper_line == "SKILLS":
            current_section = "skills"
            continue
        elif upper_line == "EDUCATION":
            current_section = "education"
            continue
        elif upper_line == "EXPERIENCE":
            current_section = "experience"
            continue
        elif upper_line.startswith("PROJECT"):
            current_section = None
            continue
        elif upper_line.startswith("CERTIFICATION"):
            current_section = None
            continue
        elif upper_line.startswith("ACHIEVEMENT"):
            current_section = None
            continue

        if current_section:
            sections[current_section] += line_strip + " "

    return sections
