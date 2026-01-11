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
        line_strip = line.strip().upper()

        if "SKILLS" == line_strip:
            current_section = "skills"
            continue
        elif "EDUCATION" == line_strip:
            current_section = "education"
            continue
        elif "EXPERIENCE" == line_strip:
            current_section = "experience"
            continue

        if current_section and len(line.strip()) > 2:
            sections[current_section] += line.strip() + "\n"

    return sections
