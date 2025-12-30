import os
import fitz
import spacy
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

nlp = spacy.load("en_core_web_sm")


model = SentenceTransformer('all-MiniLM-L6-v2')


skills_list = [
    "python", "data analysis", "machine learning", "flask", "django",
    "excel", "sql", "power bi", "pandas", "numpy"
]


resume_chunks = []
chunk_embeddings = None
index = None

def get_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        page_text = page.get_text()
        page_text = page_text.replace("\n", " ").replace("-", " ").lower()
        text += page_text + " "
    return text

def get_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read().lower()

def find_skills(text):
    text = text.lower()
    skills_found = []
    for skill in skills_list:
        if skill.lower() in text:
            skills_found.append(skill)
    return skills_found

def extract_details(text):
    qualifications = "Bachelor's in Computer Science"
    experience = "2 years as Data Analyst"
    age = "25"
    hobbies = "Reading, Traveling"
    projects = "Data Visualization Project, Machine Learning Project"
    return qualifications, experience, age, hobbies, projects

def analyze_resume(file_path):
    global resume_chunks, chunk_embeddings, index

    ext = os.path.splitext(file_path)[1].lower()

    if ext == '.pdf':
        text = get_text_from_pdf(file_path)
    elif ext == '.txt':
        text = get_text_from_txt(file_path)
    else:
        return {"error": "Only PDF or TXT files are supported."}

    if not text.strip():
        return {"error": "No text found in resume!"}

  
    qualifications, experience, age, hobbies, projects = extract_details(text)

    
    skills = find_skills(text)
    matched_skills = ', '.join(skills)

    
    resume_chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    chunk_embeddings = model.encode(resume_chunks)
    dim = chunk_embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(chunk_embeddings))

    return {
        "name": "Candidate",
        "qualifications": qualifications,
        "experience": experience,
        "age": age,
        "skills": skills,
        "matched_skills": matched_skills,
        "hobbies": hobbies,
        "projects": projects,
        "matched_role": "Data Analyst" if "data analysis" in skills else "Tech Role"
    }


def rag_query(question):
    global resume_chunks, chunk_embeddings, index
    if index is None or len(resume_chunks) == 0:
        return "Please upload a resume first."

    q_emb = model.encode([question])
    D, I = index.search(np.array(q_emb), k=2)
    answer_chunks = [resume_chunks[i] for i in I[0]]
    return " ".join(answer_chunks)
