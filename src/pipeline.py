import argparse
import json

from config import Settings
from src.ingestion import load_incident, artifact_to_documents
from src.chunking import chunk_documents
from src.retrieval import HybridRetriever
from src.generation import build_prompt, generate_postmortem


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)

    args = parser.parse_args()

    settings = Settings()

    incident = load_incident(
        args.input
    )

    documents = artifact_to_documents(
        incident
    )

    chunks = chunk_documents(
        documents,
        chunk_size=settings.chunk_size,
        overlap=settings.chunk_overlap
    )

    if not chunks:
        raise ValueError(
            "No usable incident artifacts were found."
        )

    retriever = HybridRetriever(
        chunks,
        settings.embedding_model
    )

    # Single generic postmortem query
    query = (
        "Create a complete incident postmortem including "
        "impact, timeline, detection, investigation, "
        "root cause, resolution, and preventive actions."
    )

    results = retriever.retrieve(
        query,
        dense_top_k=settings.dense_top_k,
        final_top_k=settings.final_top_k
    )

    # Build context from retrieved chunks
    context_parts = []
    total_chars = 0

    for item in results:

        chunk = item["chunk"]

        block = (
            f'[Artifact: '
            f'{chunk["metadata"]["artifact_type"]}; '
            f'ID: {chunk["id"]}; '
            f'Score: '
            f'{item["combined_score"]:.3f}]\n'
            f'{chunk["text"]}\n'
        )

        if (
            total_chars + len(block)
            > settings.max_context_chars
        ):
            break

        context_parts.append(block)
        total_chars += len(block)

    context = "\n".join(
        context_parts
    )

    # Generate postmortem
    prompt = build_prompt(
        context
    )

    output = generate_postmortem(
        prompt,
        settings.ollama_url,
        settings.ollama_model,
        settings.temperature,
        settings.timeout_seconds
    )

    print(
        "\n===== GENERATED POSTMORTEM =====\n"
    )

    print(output)


if __name__ == "__main__":
    main()