import streamlit as st
from model.recommender import CareerRecommender

st.set_page_config(page_title="AI Career System", layout="wide")

st.title("🧠 AI Career Intelligence System")
st.write("Semantic AI using Sentence Transformers + FAISS")

model = CareerRecommender("data/jobs.csv")

user_input = st.text_area(
    "Enter your skills / resume text",
    placeholder="e.g. I know Python, Machine Learning, Data Analysis, SQL"
)

top_k = st.slider("Top Recommendations", 1, 5, 3)

if st.button("Analyze with AI"):

    results = model.recommend(user_input, top_k)

    st.success("AI Analysis Complete")

    for r in results:

        st.markdown(f"""
        ---
        ### 💼 {r['job']}
        - Category: {r['category']}
        - Match Score: {r['score']}
        - Skills: {r['skills']}
        - Level: {r['level']}
        """)