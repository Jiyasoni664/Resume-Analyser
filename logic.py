import os
import fitz  # PyMuPDF
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Define known skills
skills_list = [
    "python", "data analysis", "machine learning", "flask", "django",
    "excel", "sql", "power bi", "pandas", "numpy"
]

# Extract text from PDF
def get_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Extract text from TXT
def get_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

# Find matching skills
def find_skills(text):
    text = text.lower()
    skills_found = []
    for skill in skills_list:
        if skill in text:
            skills_found.append(skill)
    return skills_found

# Extract qualifications, experience, and other details
def extract_details(text):
    # Placeholder logic for extracting details from the resume
    qualifications = "Bachelor's in Computer Science"  # Extract from text
    experience = "2 years as Data Analyst"  # Extract from text
    age = "25"  # Extract from text (use date of birth, etc.)
    hobbies = "Reading, Traveling"  # Extract from text
    projects = "Data Visualization Project, Machine Learning Project"  # Extract from text

    return qualifications, experience, age, hobbies, projects

# Analyze the resume
def analyze_resume(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == '.pdf':
        text = get_text_from_pdf(file_path)
    elif ext == '.txt':
        text = get_text_from_txt(file_path)
    else:
        return {"error": "Only PDF or TXT files are supported."}

    if not text.strip():
        return {"error": "No text found in resume!"}

    # Extract additional details
    qualifications, experience, age, hobbies, projects = extract_details(text)

    # Find skills
    skills = find_skills(text)
    matched_skills = ', '.join(skills)
    score = len(skills) * 10

    # Return the complete analysis result
    return {
        "name": "Candidate",  # This can be extracted from the resume text if available
        "qualifications": qualifications,
        "experience": experience,
        "age": age,
        "skills": skills,
        "matched_skills": matched_skills,
        "hobbies": hobbies,
        "projects": projects,
        "matched_role": "Data Analyst" if "data analysis" in skills else "Tech Role"
    }