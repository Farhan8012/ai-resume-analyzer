SKILL_SYNONYMS = {
    "nlp": ["natural language processing", "text processing"],
    "ml": ["machine learning", "predictive modeling"],
    "ai": ["artificial intelligence", "generative ai"],
    "dl": ["deep learning", "neural networks"],
    "cv": ["computer vision"],
    "git": ["github", "gitlab", "version control"],
    "docker": ["containerization", "kubernetes", "k8s"],
    "aws": ["amazon web services", "ec2", "lambda", "s3"],
    "azure": ["microsoft azure"],
    "gcp": ["google cloud platform"],
    "sql": ["mysql", "postgresql", "postgres", "no-sql", "mongodb"],
    "react": ["reactjs", "react.js"],
    "node": ["nodejs", "node.js", "expressjs"],
    "vue": ["vuejs", "vue.js"],
    "angular": ["angularjs"],
    "python": ["python3", "pandas", "numpy", "scikit-learn", "sklearn"],
    "java": ["springboot", "spring boot", "jvm"],
    "js": ["javascript", "es6", "typescript", "ts"],
    "html": ["html5"],
    "css": ["css3", "tailwind", "bootstrap"]
}

def normalize_skills(skills: set) -> set:
    """
    Standardizes skills (e.g., 'ReactJS' -> 'react') using the synonym dictionary.
    """
    normalized = set()
    for skill in skills:
        skill = skill.lower().strip()
        
        # Check if skill is a known synonym
        mapped = False
        for main_skill, aliases in SKILL_SYNONYMS.items():
            if skill == main_skill or skill in aliases:
                normalized.add(main_skill)
                mapped = True
                break
        
        # If no synonym found, keep original if it's in our main list
        if not mapped:
             # Clean up common variations like "python 3" -> "python" is handled by the synonym map, 
             # but here we just add the raw skill if it matches the keyword list logic later
            normalized.add(skill)
            
    return normalized

SKILL_KEYWORDS = [
    # Programming Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust", "php", "ruby", "swift", "kotlin", "scala", "r", "dart",
    
    # Web Development (Frontend/Backend)
    "html", "css", "react", "angular", "vue", "next.js", "node.js", "django", "flask", "fastapi", "spring boot", "asp.net", "graphql", "rest api",
    
    # Data Science & AI
    "machine learning", "deep learning", "nlp", "computer vision", "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy", "matplotlib", "seaborn", "opencv", "hugging face", "llm", "langchain",
    
    # Databases
    "sql", "mysql", "postgresql", "mongodb", "redis", "firebase", "elasticsearch", "cassandra", "oracle", "snowflake",
    
    # DevOps & Cloud
    "git", "docker", "kubernetes", "aws", "azure", "gcp", "linux", "bash", "jenkins", "circleci", "terraform", "ansible", "prometheus", "grafana",
    
    # Tools & Others
    "jira", "agile", "scrum", "excel", "power bi", "tableau", "figma", "selenium", "cypress", "junit", "postman"
]

def extract_skills_from_text(text: str) -> set:
    """
    Scans text for skills from our expanded SKILL_KEYWORDS list.
    """
    text = text.lower()
    found_skills = set()

    # 1. Direct Keyword Search
    for skill in SKILL_KEYWORDS:
        # We add spaces around the skill to avoid partial matches (e.g., "go" in "google")
        # Regex is safer, but for now, simple string check with padding works for 90% cases
        pattern = f" {skill} " 
        if pattern in f" {text} ": # Pad text too
            found_skills.add(skill)
            
    # 2. Check Synonyms specifically (in case user wrote 'ReactJS' which isn't in main list but is in synonyms)
    for main, aliases in SKILL_SYNONYMS.items():
        for alias in aliases:
            if f" {alias} " in f" {text} ":
                found_skills.add(main)

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



skill_resources = {
    "python": "https://www.learnpython.org/",
    "sql": "https://www.w3schools.com/sql/",
    "machine learning": "https://www.coursera.org/learn/machine-learning",
    "deep learning": "https://www.fast.ai/",
    "nlp": "https://www.kaggle.com/learn/natural-language-processing",
    "git": "https://git-scm.com/doc",
    "docker": "https://docker-curriculum.com/",
    "aws": "https://aws.amazon.com/getting-started/",
    "react": "https://react.dev/learn",
    "node.js": "https://nodejs.org/en/learn",
    "kubernetes": "https://kubernetes.io/docs/tutorials/kubernetes-basics/",
    "terraform": "https://developer.hashicorp.com/terraform/tutorials",
    "java": "https://www.codecademy.com/learn/learn-java"
}

def get_learning_link(skill):
    """Returns a learning link for a missing skill."""
    return skill_resources.get(skill.lower())