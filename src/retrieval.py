import re
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


def tokenize(text: str) -> set[str]:
    return set(
        re.findall(
            r"[a-zA-Z0-9_/-]+",
            text.lower()
        )
    )


class HybridRetriever:

    def __init__(
        self,
        chunks: list[dict],
        model_name: str
    ):
        self.chunks = chunks

        self.embedder = SentenceTransformer(
            model_name
        )

        self.embeddings = self.embedder.encode(
            [chunk["text"] for chunk in chunks],
            normalize_embeddings=True,
            show_progress_bar=False
        )

    def retrieve(
        self,
        query: str,
        dense_top_k: int = 8,
        final_top_k: int = 10
    ):

        query_embedding = self.embedder.encode(
            [query],
            normalize_embeddings=True,
            show_progress_bar=False
        )

        dense_scores = cosine_similarity(
            query_embedding,
            self.embeddings
        )[0]

        query_terms = tokenize(query)

        scored = []

        for index, chunk in enumerate(self.chunks):

            chunk_terms = tokenize(
                chunk["text"]
            )

            keyword_score = (
                len(query_terms & chunk_terms)
                / max(len(query_terms), 1)
            )

            dense_score = float(
                dense_scores[index]
            )

            combined_score = (
                0.7 * dense_score
                + 0.3 * keyword_score
            )

            scored.append({
                "chunk": chunk,
                "dense_score": dense_score,
                "keyword_score": keyword_score,
                "combined_score": combined_score
            })

        scored.sort(
            key=lambda item: item["combined_score"],
            reverse=True
        )

        return scored[:final_top_k]