import pandas as pd
import re

# ==========================================
# LOAD SKILLS FROM DATASET
# ==========================================

df = pd.read_csv("data/jobs.csv")

all_skills = []

for skills in df["skills"]:

    split_skills = str(skills).split(",")

    for skill in split_skills:

        cleaned = skill.strip().lower()

        if cleaned:
            all_skills.append(cleaned)

# ==========================================
# EXTRA SCIENTIFIC / TECHNICAL SKILLS
# ==========================================

EXTRA_SKILLS = [

    "ftir",
    "h-nmr",
    "tga",
    "xrd",
    "lsv",
    "cv",
    "ca",

    "electrochemical impedance spectroscopy",

    "nova software",
    "chem draw",
    "cosmo-rs",
    "jmp",

    "data analysis",

    "aspen hysys",
    "origin lab",

    "ms office",
    "ms outlook",
    "ms word",
    "ms powerpoint",
    "ms excel",
    "ms visio",

    "endnote"
]

# ==========================================
# MERGE SKILLS
# ==========================================

SKILLS_DB = list(set(all_skills + EXTRA_SKILLS))

# ==========================================
# SKILL EXTRACTION
# ==========================================

def extract_skills(text):

    text = text.lower()

    # CLEAN TEXT
    text = re.sub(r'[^a-zA-Z0-9\-\+ ]', ' ', text)

    found_skills = set()

    # ======================================
    # REGEX MATCHING
    # ======================================

    for skill in SKILLS_DB:

        pattern = r'\b' + re.escape(skill.lower()) + r'\b'

        if re.search(pattern, text):
            found_skills.add(skill)

    return sorted(list(found_skills))