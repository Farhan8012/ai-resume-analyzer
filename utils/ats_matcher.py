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


def match_skills(resume_skills: set, jd_skills: set):
    if not jd_skills:
        return 0, set(), set()

    matched = resume_skills.intersection(jd_skills)
    missing = jd_skills - resume_skills

    match_percentage = int((len(matched) / len(jd_skills)) * 100)

    return match_percentage, matched, missing
