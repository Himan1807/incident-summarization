from typing import Any

def chunk_documents(
    documents: list[dict[str, Any]],
    chunk_size: int = 450,
    overlap: int = 80
) -> list[dict[str, Any]]:
    chunks = []

    for document in documents:
        words = document["text"].split()
        start = 0
        chunk_id = 0

        while start < len(words):
            end = min(start + chunk_size, len(words))
            chunk_text = " ".join(words[start:end]).strip()

            if chunk_text:
                chunks.append({
                    "id": f'{document["metadata"]["artifact_type"]}-{document["metadata"]["artifact_index"]}-{chunk_id}',
                    "text": chunk_text,
                    "metadata": document["metadata"]
                })

            if end == len(words):
                break

            start = max(end - overlap, start + 1)
            chunk_id += 1

    return chunks
