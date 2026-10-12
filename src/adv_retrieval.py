"""Hybrid retrieval: BM25 + dense -> Reciprocal Rank Fusion -> cross-encoder rerank.

Models load lazily. If the cross-encoder cannot be loaded (offline, etc.) the
retriever degrades gracefully to the fused ranking and says so.
"""
import re
from collections import defaultdict

import numpy as np
from rank_bm25 import BM25Okapi

_TOKEN = re.compile(r"[A-Za-z0-9_]+(?:[.\-:/][A-Za-z0-9_]+)*")


def tokenize(text: str) -> list[str]:
    """Keeps IPs/domains/URIs whole AND adds their parts, so exact IOC queries hit."""
    toks = []
    for t in _TOKEN.findall(text.lower()):
        toks.append(t)
        parts = re.split(r"[.\-:/]", t)
        if len(parts) > 1:
            toks.extend(p for p in parts if len(p) > 1)
    return toks


def rrf(rankings: list[list[int]], k: int = 60) -> dict[int, float]:
    scores: dict[int, float] = defaultdict(float)
    for ranking in rankings:
        for rank, idx in enumerate(ranking):
            scores[idx] += 1.0 / (k + rank + 1)
    return scores


class AdvancedRetriever:
    def __init__(self, chunks, embedding_model, reranker_model=None, embedder=None, reranker=None):
        self.chunks = chunks
        self.bm25 = BM25Okapi([tokenize(c["text"]) for c in chunks])
        if embedder is None:
            from sentence_transformers import SentenceTransformer
            embedder = SentenceTransformer(embedding_model)
        self.embedder = embedder
        self.emb = self.embedder.encode([c["text"] for c in chunks], normalize_embeddings=True,
                                        show_progress_bar=False)
        self.reranker = reranker
        if reranker is None and reranker_model:
            try:
                from sentence_transformers import CrossEncoder
                self.reranker = CrossEncoder(reranker_model)
            except Exception as exc:                         # offline / missing model
                print(f"[warn] reranker unavailable ({exc}); using fused ranking only.")

    def _rank_one(self, query, bm25_k, dense_k):
        bm = np.asarray(self.bm25.get_scores(tokenize(query)))
        q = self.embedder.encode([query], normalize_embeddings=True, show_progress_bar=False)[0]
        de = self.emb @ q
        return list(np.argsort(-bm)[:bm25_k]), list(np.argsort(-de)[:dense_k])

    def retrieve(self, queries: list[str], rerank_query: str, bm25_k=15, dense_k=15,
                 rrf_k=60, top_k=6, max_chars=3500):
        rankings = []
        for q in queries:                       # multi-query: each sub-query votes in RRF
            b, d = self._rank_one(q, bm25_k, dense_k)
            rankings += [b, d]
        fused = rrf(rankings, rrf_k)
        cand = sorted(fused, key=fused.get, reverse=True)[:max(top_k * 3, 12)]

        if self.reranker is not None:
            ce = self.reranker.predict([(rerank_query, self.chunks[i]["text"]) for i in cand])
            order = [i for _, i in sorted(zip(ce, cand), key=lambda x: -x[0])]
            score = {i: float(s) for s, i in zip(ce, cand)}
        else:
            order, score = cand, {i: fused[i] for i in cand}

        out, used = [], 0
        for i in order[:top_k]:
            ln = len(self.chunks[i]["text"])
            if used + ln > max_chars and out:
                break
            out.append({"chunk": self.chunks[i], "score": score[i], "rrf": fused[i]})
            used += ln
        return out
