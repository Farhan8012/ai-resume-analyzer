from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_semantic_match(resume_text, jd_text):
    """
    Calculates the semantic similarity between resume and JD using TF-IDF and Cosine Similarity.
    This is an international-standard approach for basic NLP matching.
    """
    if not resume_text.strip() or not jd_text.strip():
        return 0.0

    # 1. Combine texts into a list for the vectorizer
    documents = [resume_text, jd_text]
    
    # 2. Initialize TF-IDF Vectorizer (removes common English stop words)
    vectorizer = TfidfVectorizer(stop_words='english')
    
    try:
        # 3. Transform text into mathematical vectors
        tfidf_matrix = vectorizer.fit_transform(documents)
        
        # 4. Calculate Cosine Similarity (the 'angle' between the two vectors)
        # tfidf_matrix[0:1] is the Resume; tfidf_matrix[1:2] is the JD
        match_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        # 5. Return as a rounded percentage
        return round(float(match_score * 100), 2)
    except Exception:
        # Returns 0 if vectors cannot be compared (e.g., empty or non-informative text)
        return 0.0