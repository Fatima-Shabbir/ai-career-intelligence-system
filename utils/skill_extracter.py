import re

SKILLS_DB = [

    "python",
    "sql",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "nlp",
    "docker",
    "kubernetes",
    "aws",
    "django",
    "flask",
    "react",
    "javascript",
    "html",
    "css",
    "data analysis",
    "power bi",
    "excel",
    "pandas",
    "numpy",
    "api",
    "linux",
    "git",
    "mongodb",
    "postgresql",
    "opencv",
    "streamlit",
    "fastapi",
    "data science",
    "computer vision",
    "matplotlib",
    "seaborn",
    "scikit-learn",
     "chemistry",
    "thermodynamics",
    "process engineering",
    "taxation",
    "auditing",
    "finance",
    "pharma",
    "biology",
    "geology",
    "research"
]


def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS_DB:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):

            found_skills.append(skill)

    return list(set(found_skills))