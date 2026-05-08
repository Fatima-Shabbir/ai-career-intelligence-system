# 🧠 AI Career Intelligence System

An AI-powered career recommendation system that matches user skills or resumes with the most relevant job roles using **semantic search (Sentence Transformers + FAISS),NLP**.

---

## 🚀 Live Features

- 📄 Upload Resume (PDF)
- ✍️ Manual Skill Input
- 🧠 AI Skill Extraction from Resume
- 🔍 Semantic Job Matching (not keyword-based)
- ⚡ FAISS Vector Search for fast recommendations
- 📊 Match Score Visualization
- ❌ Skill Gap Analysis
- 🎯 Interactive Streamlit Dashboard

---

## 🧠 How It Works

1. User uploads resume or enters skills  
2. Resume text is extracted (PDF parsing)  
3. Important skills are extracted using NLP  
4. Skills are converted into embeddings using Sentence Transformers  
5. FAISS finds the most similar job roles  
6. Results are ranked and displayed with match scores  

---

## 🏗️ Tech Stack

- Python  
- Streamlit (Frontend UI)  
- Sentence Transformers (NLP Embeddings)  
- FAISS (Vector Similarity Search)  
- Pandas (Data Handling)  
- Plotly (Visualization)  
- pdfplumber (Resume parsing)

---

## 🧠 AI Concepts Used

- Semantic Search  
- Vector Embeddings  
- Cosine Similarity  
- Information Retrieval  
- NLP-based Skill Extraction  

---
## Future Improvements
- LLM-based career coach
- Real job API integration
- Resume scoring system
- Login + user profiles
- Personalized learning roadmap

---

## 🎯 Real-World Use Cases

- Job portals (like LinkedIn style systems)
- Recruitment platforms
- Career guidance systems
- HR automation tools

## 📁 Project Structure

```text
model/
   embedder.py
   recommender.py

utils/
   resume_parser.py
   skill_extractor.py

data/
   jobs.csv

app.py
style.css

---

## 👨‍💻 Author

**Fatima Shabbir**  
AI/ML Enthusiast | Python Developer  


