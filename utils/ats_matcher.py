SKILL_SYNONYMS = {
    "nlp": ["natural language processing"],
    "ml": ["machine learning"],
    "ai": ["artificial intelligence"],
    "git": ["github"],
    "docker": ["containers"],
    "sql": ["mysql", "postgresql"],
    "python": ["python3"]
}

def normalize_skills(skills: set) -> set:
    normalized = set()

    for skill in skills:
        skill = skill.lower()
        normalized.add(skill)

        # map synonyms → main skill
        for main_skill, aliases in SKILL_SYNONYMS.items():
            if skill == main_skill or skill in aliases:
                normalized.add(main_skill)

    return normalized

SKILL_KEYWORDS = [
    "python", "java", "c++", "sql", "machine learning", "deep learning",
    "data structures", "algorithms", "nlp", "streamlit", "git", "github",
    "tensorflow", "pytorch", "mysql"
]

def extract_skills_from_text(text: str) -> set:
    text = text.lower()
    found_skills = set()

    for skill in SKILL_KEYWORDS:
        if skill in text:
            found_skills.add(skill)

    return found_skills


def match_skills(resume_skills, jd_skills):
    if not jd_skills:
        return 0, set(), set()

    resume_set = normalize_skills(resume_skills)
    jd_set = normalize_skills(jd_skills)

    matched = resume_set.intersection(jd_set)
    missing = jd_set - matched

    match_percentage = round((len(matched) / len(jd_set)) * 100)
    return match_percentage, matched, missing


    

WEAK_ACTION_WORDS = [
    "worked on",
    "helped",
    "responsible for",
    "assisted",
    "participated",
    "involved in"
]

def find_weak_bullets(experience_text):
    weak_lines = []

    for line in experience_text.split("\n"):
        line_lower = line.lower()
        for word in WEAK_ACTION_WORDS:
            if word in line_lower:
                weak_lines.append(line.strip())
                break

    return weak_lines

import re

def find_unquantified_bullets(experience_text):
    unquantified = []

    for line in experience_text.split("\n"):
        if len(line.strip()) < 5:
            continue

        # Check if line has any number
        if not re.search(r"\d", line):
            unquantified.append(line.strip())

    return unquantified

def skills_without_evidence(skills, experience_text):
    experience_text = experience_text.lower()
    missing = []

    for skill in skills:
        skill_lower = skill.lower()

        # Direct mention
        if skill_lower in experience_text:
            continue

        # Common action patterns
        patterns = [
            f"using {skill_lower}",
            f"with {skill_lower}",
            f"built using {skill_lower}",
            f"developed using {skill_lower}",
            f"implemented using {skill_lower}"
        ]

        if any(p in experience_text for p in patterns):
            continue

        missing.append(skill)

    return missing


SUGGESTION_TEMPLATES = {
    "python": "Built backend features using Python for real-world data processing",
    "sql": "Designed and queried relational databases using SQL",
    "nlp": "Applied NLP techniques for text cleaning and analysis",
    "machine learning": "Trained and evaluated machine learning models on structured data",
    "git": "Used Git for version control and collaborative development",
    "github": "Managed project repositories and pull requests on GitHub",
    "streamlit": "Developed interactive web applications using Streamlit",
    "data structures": "Implemented efficient data structures to optimize performance",
    "algorithms": "Designed algorithms with time and space complexity considerations"
}
