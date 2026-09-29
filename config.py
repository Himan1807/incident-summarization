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
