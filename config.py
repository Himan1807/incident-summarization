from dataclasses import dataclass

@dataclass
class Settings:
    ollama_url: str = "http://localhost:11434/api/generate"
    ollama_model: str = "llama3.1:8b-instruct-q4_K_M"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    chunk_size: int = 450
    chunk_overlap: int = 80
    dense_top_k: int = 8
    final_top_k: int = 10
    max_context_chars: int = 16000
    temperature: float = 0.1
    timeout_seconds: int = 900


@dataclass
class AdvancedSettings:
    """Settings for the advanced RAG pipeline (CPU-friendly defaults)."""
    # Models
    ollama_url: str = "http://localhost:11434/api/generate"
    ollama_model: str = "llama3.1:8b-instruct-q4_K_M"   # try "llama3.2:3b" for ~2-3x speed on CPU
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"  # 22M params, fine on CPU
    temperature: float = 0.1
    timeout_seconds: int = 1800
    num_ctx: int = 4096            # per-section prompts are small; keeps RAM/latency low
    num_predict: int = 450         # max tokens generated per section

    # Chunking (item-level, structure aware)
    items_per_chunk: int = 4

    # Retrieval
    bm25_top_k: int = 15
    dense_top_k: int = 15
    rrf_k: int = 60
    rerank_top_k: int = 6          # chunks kept per section after reranking
    max_context_chars: int = 3500  # per section

    # Raw-log enrichment (first/last seen timestamps for IOCs)
    enable_enrichment: bool = True
