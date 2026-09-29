# Incident RAG Starter

A simple, extensible RAG baseline for incident summarization and automated postmortem generation.

## Initial pipeline
1. Load incident artifacts from JSON.
2. Normalize artifacts into documents.
3. Chunk documents while preserving metadata.
4. Create dense embeddings.
5. Retrieve using dense similarity + keyword overlap.
6. Rerank retrieved chunks using a lightweight scoring function.
7. Generate a structured postmortem with Ollama.

## Setup (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Ensure Ollama is running and a model is available:

```powershell
ollama pull llama3.1:8b-instruct-q4_K_M
```

Run:

```powershell
python -m src.pipeline --input data/raw/sample_incident.json
```

The reference postmortem must not be included in the input artifacts used for generation. It is reserved for evaluation.
"# incident-summarization" 
