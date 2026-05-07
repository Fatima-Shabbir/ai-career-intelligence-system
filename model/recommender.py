import pandas as pd
import faiss
import numpy as np
from model.embedder import Embedder

class CareerRecommender:

    def __init__(self, csv_path):

        self.df = pd.read_csv(csv_path)

        # merge text fields (VERY IMPORTANT)
        self.df["text"] = (
            self.df["job_title"] + " " +
            self.df["description"] + " " +
            self.df["skills"]
        )

        self.embedder = Embedder()

        # create embeddings
        self.embeddings = self.embedder.encode(self.df["text"].tolist())

        # FAISS index
        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(np.array(self.embeddings))

    def recommend(self, user_input, top_k=5):

        query_vec = self.embedder.encode([user_input])

        scores, indices = self.index.search(np.array(query_vec), top_k)

        results = []

        for score, idx in zip(scores[0], indices[0]):

            results.append({
                "job": self.df.iloc[idx]["job_title"],
                "category": self.df.iloc[idx]["category"],
                "score": round(float(score), 3),
                "skills": self.df.iloc[idx]["skills"],
                "level": self.df.iloc[idx]["experience_level"]
            })

        return results