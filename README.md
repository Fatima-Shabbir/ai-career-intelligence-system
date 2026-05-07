# 🧠 AI Career Intelligence System

An AI-powered job recommendation system that uses **Natural Language Processing (NLP)** and **Semantic Search** to match user skills with relevant job roles.

Instead of simple keyword matching, this system understands the **meaning of text using transformer-based embeddings** and performs intelligent job recommendations.

---


## 📌 Features

- 🧠 AI-powered semantic job matching
- 📄 Resume / skill-based input system
- ⚡ Fast similarity search using FAISS
- 🎯 Accurate job recommendations (not keyword-based)
- 📊 Match score for each recommendation
- 💻 Clean interactive Streamlit UI

---

## 🧠 How It Works

1. User enters skills or resume text  
2. Text is converted into AI embeddings (Sentence-BERT)  
3. Job descriptions are also converted into embeddings  
4. FAISS finds the most similar job vectors  
5. System returns ranked job recommendations  

---

## 🛠️ Tech Stack

- Python 🐍
- Streamlit 🎨
- SentenceTransformers 🤖
- FAISS (Facebook AI Similarity Search) ⚡
- Pandas 📊

---

## 🧠 AI Concepts Used

- Natural Language Processing (NLP)
- Transformer-based embeddings
- Semantic similarity
- Vector search (ANN)
- Information retrieval systems




## 🚀 Future Improvements

- Resume PDF upload support
- ChatGPT-style career assistant
- Skill gap analysis
- Job roadmap generator
- Deployment on cloud (Render / HuggingFace)

---

## 🎯 Real-World Use Cases

- Job portals (like LinkedIn style systems)
- Recruitment platforms
- Career guidance systems
- HR automation tools



## 👨‍💻 Author

**Fatima Shabbir**  
AI/ML Enthusiast | Python Developer  

## 📁 Project Structure
ai_career_ai/
│
├── app.py
├── data/
│ └── jobs.csv
│
├── model/
│ └── recommender.py
│
├── assets/
│ └── style.css
