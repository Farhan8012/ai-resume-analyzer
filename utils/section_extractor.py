import re

SECTION_KEYWORDS = {
    "skills": [
        "skills", "technical skills", "technologies", "tools", "expertise", "competencies"
    ],
    "education": [
        "education", "academic", "qualification", "degree", "alma mater"
    ],
    "experience": [
        "experience", "work experience", "employment", "internship", "projects", "work history"
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

        # 1. Check if this line is a Section Header
        found_section = None
        for section_name, keywords in SECTION_KEYWORDS.items():
            if line_strip.lower() in keywords:
                found_section = section_name
                break
        
        # 2. If it is a header, switch the "bucket"
        if found_section:
            current_section = found_section
            continue # Don't add the header itself to the text

        # 3. Stop if we hit other headers we don't care about
        if any(line_strip.upper().startswith(k) for k in ["CERTIFICATION", "ACHIEVEMENT", "LANGUAGES"]):
            current_section = None
            continue

        # 4. Add line to the current bucket
        if current_section:
            sections[current_section] += line_strip + "\n"  

    return sections