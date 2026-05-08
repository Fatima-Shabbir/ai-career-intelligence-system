import os
import faiss
import numpy as np
import pandas as pd

from model.embedder import Embedder


class CareerRecommender:

    def __init__(self, csv_path):

        self.df = pd.read_csv(csv_path)

        # -----------------------------
        # CLEAN DATA
        # -----------------------------
        self.df.dropna(inplace=True)

        self.df.drop_duplicates(
            subset=["job_title", "skills"],
            inplace=True
        )

        # normalize skills
        self.df["skills"] = (
            self.df["skills"]
            .astype(str)
            .str.lower()
            .str.replace("/", ",")
            .str.replace("|", ",")
        )

        # -----------------------------
        # BETTER TEXT FOR EMBEDDINGS
        # -----------------------------
        self.df["text"] = (
            "Job: " +
            self.df["job_title"].astype(str)
            + ". Skills: " +
            self.df["skills"].astype(str)
            + ". Category: " +
            self.df["category"].astype(str)
        )

        self.embedder = Embedder()

        os.makedirs("saved", exist_ok=True)

        index_path = "saved/faiss.index"
        emb_path = "saved/embeddings.npy"

        # -----------------------------
        # LOAD OR CREATE INDEX
        # -----------------------------
        if os.path.exists(index_path):

            self.index = faiss.read_index(index_path)

            self.embeddings = np.load(emb_path)

        else:

            self.embeddings = self.embedder.encode(
                self.df["text"].tolist()
            )

            self.embeddings = np.array(
                self.embeddings,
                dtype=np.float32
            )

            dim = self.embeddings.shape[1]

            self.index = faiss.IndexFlatIP(dim)

            self.index.add(self.embeddings)

            faiss.write_index(
                self.index,
                index_path
            )

            np.save(
                emb_path,
                self.embeddings
            )

    # ---------------------------------
    # RECOMMEND FUNCTION
    # ---------------------------------
    def recommend(self, user_input, top_k=5):

        # normalize input
        user_input = user_input.lower()

        # better semantic query
        query_text = (
            f"Candidate with skills in {user_input}"
        )

        query_vec = self.embedder.encode(
            [query_text]
        )

        query_vec = np.array(
            query_vec,
            dtype=np.float32
        )

        # search more results for reranking
        scores, indices = self.index.search(
            query_vec,
            20
        )

        results = []

        user_skills = [

            s.strip().lower()

            for s in user_input.split(",")
        ]

        for score, idx in zip(
            scores[0],
            indices[0]
        ):

            row = self.df.iloc[idx]

            required_skills = [

                s.strip().lower()

                for s in str(
                    row["skills"]
                ).split(",")
            ]

            # -----------------------------
            # HYBRID SCORING
            # -----------------------------
            overlap = len(
                set(user_skills) &
                set(required_skills)
            )

            overlap_score = (
                overlap /
                max(len(required_skills), 1)
            )

            semantic_score = float(score)

            final_score = (
                semantic_score * 0.7 +
                overlap_score * 0.3
            )

            final_score = round(
                final_score * 100,
                2
            )

            missing_skills = list(
                set(required_skills) -
                set(user_skills)
            )

            results.append({

                "job":
                row["job_title"],

                "category":
                row["category"],

                "score":
                final_score,

                "skills":
                row["skills"],

                "level":
                row["experience_level"],

                "missing_skills":
                missing_skills,

                "reason":
                f"Strong semantic and skill match for {row['job_title']}."
            })

        # sort by final score
        results = sorted(
            results,
            key=lambda x: x["score"],
            reverse=True
        )

        return results[:top_k]