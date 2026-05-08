# import os
# import faiss
# import numpy as np
# import pandas as pd

# from model.embedder import Embedder


# class CareerRecommender:

#     def __init__(self, csv_path):

#         self.df = pd.read_csv(csv_path)

#         # Merge text columns
#         # self.df["text"] = (
#         #     self.df["job_title"] + " " +
#         #     self.df["description"] + " " +
#         #     self.df["skills"]
#         # )
#         self.df["text"] = (
#     "Job Title: " + self.df["job_title"].astype(str) + ". " +
#     "Category: " + self.df["category"].astype(str) + ". " +
#     "Skills Required: " + self.df["skills"].astype(str) + ". " +
#     "Job Description: " + self.df["description"].astype(str)
# )
       
#         self.embedder = Embedder()

#         os.makedirs("saved", exist_ok=True)

#         # Load existing index if available
#         if os.path.exists("saved/faiss.index"):

#             self.index = faiss.read_index(
#                 "saved/faiss.index"
#             )

#             self.embeddings = np.load(
#                 "saved/embeddings.npy"
#             )

#         else:

#             self.embeddings = self.embedder.encode(
#                 self.df["text"].tolist()
#             )

#             self.embeddings = np.array(
#                 self.embeddings,
#                 dtype=np.float32
#             )

#             dim = self.embeddings.shape[1]

#             self.index = faiss.IndexFlatIP(dim)

#             self.index.add(self.embeddings)

#             # Save index
#             faiss.write_index(
#                 self.index,
#                 "saved/faiss.index"
#             )

#             np.save(
#                 "saved/embeddings.npy",
#                 self.embeddings
#             )

#     def recommend(self, user_input, top_k=5):

#         query_vec = self.embedder.encode(
#             [user_input]
#         )

#         query_vec = np.array(
#             query_vec,
#             dtype=np.float32
#         )

#         scores, indices = self.index.search(
#             query_vec,
#             top_k
#         )

#         results = []

#         for score, idx in zip(
#             scores[0],
#             indices[0]
#         ):

#             row = self.df.iloc[idx]

#             required_skills = [
#                 s.strip().lower()
#                 for s in row["skills"].split(",")
#             ]

#             user_skills = [
#                 s.strip().lower()
#                 for s in user_input.split(",")
#             ]

#             missing_skills = list(
#                 set(required_skills) - set(user_skills)
#             )

#             results.append({

#                 "job": row["job_title"],

#                 "category": row["category"],

#                 "score": round(
#                     float(score) * 100,
#                     2
#                 ),

#                 "skills": row["skills"],

#                 "level": row["experience_level"],

#                 "missing_skills": missing_skills,

#                 "reason": f"""
# Strong match because your profile
# aligns with {row["job_title"]}
# requirements.
# """
#             })

#         return results




import os
import faiss
import numpy as np
import pandas as pd

from model.embedder import Embedder


class CareerRecommender:

    def __init__(self, csv_path):

        self.df = pd.read_csv(csv_path)

        # ==============================
        # IMPROVED TEXT REPRESENTATION
        # ==============================
        self.df["text"] = (
            "Job Title: " + self.df["job_title"].astype(str) + ". " +
            "Category: " + self.df["category"].astype(str) + ". " +
            "Skills Required: " + self.df["skills"].astype(str) + ". " +
            "Job Description: " + self.df["description"].astype(str)
        )

        self.embedder = Embedder()

        os.makedirs("saved", exist_ok=True)

        # ==============================
        # LOAD OR BUILD FAISS INDEX
        # ==============================
        index_path = "saved/faiss.index"
        emb_path = "saved/embeddings.npy"

        if os.path.exists(index_path) and os.path.exists(emb_path):

            self.index = faiss.read_index(index_path)
            self.embeddings = np.load(emb_path)

        else:

            self.embeddings = self.embedder.encode(self.df["text"].tolist())

            self.embeddings = np.array(self.embeddings).astype("float32")

            dim = self.embeddings.shape[1]

            self.index = faiss.IndexFlatIP(dim)

            self.index.add(self.embeddings)

            faiss.write_index(self.index, index_path)
            np.save(emb_path, self.embeddings)

    # ==============================
    # FIXED RECOMMENDATION ENGINE
    # ==============================
    def recommend(self, user_input, top_k=5):

        # ==============================
        # INPUT NORMALIZATION (IMPORTANT)
        # ==============================
        user_input = user_input.lower()

        if len(user_input.split()) < 3:
            user_input = "skills: " + user_input

        # ==============================
        # QUERY EMBEDDING FIX
        # ==============================
        query_vec = self.embedder.encode([user_input])

        query_vec = np.array(query_vec).astype("float32")

        # ==============================
        # FAISS SEARCH
        # ==============================
        scores, indices = self.index.search(query_vec, top_k)

        results = []

        for score, idx in zip(scores[0], indices[0]):

            row = self.df.iloc[idx]

            # ==============================
            # SKILL PROCESSING (FIXED)
            # ==============================
            required_skills = [
                s.strip().lower()
                for s in str(row["skills"]).split(",")
            ]

            # better skill extraction from full input
            user_skills = [
                s.strip().lower()
                for s in user_input.replace("skills:", "").split(",")
            ]

            missing_skills = list(
                set(required_skills) - set(user_skills)
            )

            results.append({

                "job": row["job_title"],
                "category": row["category"],

                # score normalization
                "score": round(float(score) * 100, 2),

                "skills": row["skills"],
                "level": row["experience_level"],

                "missing_skills": missing_skills,

                "reason": (
                    f"Strong semantic match with {row['job_title']} "
                    f"based on skills and job description similarity."
                )
            })

        return results