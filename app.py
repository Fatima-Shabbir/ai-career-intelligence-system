import streamlit as st
import streamlit.components.v1 as components

import plotly.express as px
import pandas as pd

from model.recommender import CareerRecommender

from utils.resume_parser import extract_text
from utils.skill_extracter import extract_skills


# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(

    page_title="AI Career Intelligence",

    layout="wide",

    page_icon="🧠"
)

# ---------------- LOAD CSS ---------------- #

with open("style.css") as f:

    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ---------------- TITLE ---------------- #

st.markdown(
    """
    <div class="main-title">
        🧠 AI Career Intelligence System
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Resume Parsing + Skill Extraction + AI Recommendations
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- LOAD MODEL ---------------- #

@st.cache_resource
def load_model():

    return CareerRecommender(
        "data/jobs.csv"
    )

model = load_model()

# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.header("⚙️ Settings")

    top_k = st.slider(
        "Top Recommendations",
        1,
        10,
        5
    )

    uploaded_file = st.file_uploader(
        "📄 Upload Resume PDF",
        type=["pdf"]
    )

# ---------------- TEXT INPUT ---------------- #

user_input = st.text_area(

    "Enter Skills Manually",

    height=180,

    placeholder="""
Python, SQL,
Machine Learning,
Docker...
"""
)

# ---------------- RESUME MODE ---------------- #

resume_skills = []

if uploaded_file:

    extracted_text = extract_text(
        uploaded_file
    )

    resume_skills = extract_skills(
        extracted_text
    )

    user_input = ", ".join(
        resume_skills
    )

    st.success(
        "✅ Resume uploaded successfully!"
    )

    st.write("## 🧠 Extracted Skills")

    skill_html = ""

    for skill in resume_skills:

        skill_html += f"""
        <span class="skill-tag">
            {skill}
        </span>
        """

    st.markdown(
        skill_html,
        unsafe_allow_html=True
    )

# ---------------- ANALYZE BUTTON ---------------- #

if st.button("🚀 Analyze Career Match"):

    if not user_input.strip():

        st.warning(
            "Please enter skills or upload a resume."
        )

    else:
    #      user_input = user_input.lower()

    # if len(user_input.split()) < 3:
    #     user_input = "skills: " + user_input

        results = model.recommend(
            user_input,
            top_k
        )

        st.success(
            "✅ AI Analysis Complete"
        )

        # ---------- METRICS ---------- #

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Jobs Found",
            len(results)
        )

        col2.metric(
            "Top Match",
            f"{results[0]['score']}%"
        )

        col3.metric(
            "AI Engine",
            "FAISS + NLP"
        )

        st.write("")

        jobs = []
        scores = []

        # ---------- RESULTS ---------- #

        for r in results:

            jobs.append(r["job"])
            scores.append(r["score"])

            card_html = f"""

            <style>

            .card {{
                background: linear-gradient(
                    135deg,
                    #1e293b,
                    #0f172a
                );

                padding: 25px;

                border-radius: 20px;

                color: white;

                margin-bottom: 20px;

                border: 1px solid #334155;

                font-family: Arial;
            }}

            .title {{
                color: #60a5fa;
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 15px;
            }}

            .text {{
                font-size: 16px;
                margin-bottom: 10px;
            }}

            </style>

            <div class="card">

                <div class="title">
                    💼 {r['job']}
                </div>

                <div class="text">
                    <b>Category:</b>
                    {r['category']}
                </div>

                <div class="text">
                    <b>Experience:</b>
                    {r['level']}
                </div>

                <div class="text">
                    <b>Skills Required:</b><br>
                    {r['skills']}
                </div>

                <div class="text">
                    <b>AI Match Score:</b>
                    {r['score']}%
                </div>

                <div class="text">
                    <b>Why Recommended?</b><br>
                    {r['reason']}
                </div>

            </div>
            """

            components.html(
                card_html,
                height=320
            )

            st.progress(
                int(r["score"])
            )

            # ---------- MISSING SKILLS ---------- #

            if len(r["missing_skills"]) > 0:

                st.write("###  Missing Skills")

                missing_html = ""

                for skill in r["missing_skills"]:

                    missing_html += f"""
                    <span class="skill-tag">
                        {skill}
                    </span>
                    """

                st.markdown(
                    missing_html,
                    unsafe_allow_html=True
                )

        # ---------- CHART ---------- #

        st.write("## 📊 Match Comparison")

        chart_df = pd.DataFrame({

            "Job": jobs,
            "Score": scores

        })

        fig = px.bar(

            chart_df,

            x="Job",

            y="Score",

            text="Score",

            template="plotly_dark"
        )

        fig.update_layout(
            height=500
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )