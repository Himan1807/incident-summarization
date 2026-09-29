# Updated Pilot Dataset for the Incident RAG Pipeline

This version reorganizes the supplied security-traffic dataset for the project RAG pipeline while preserving the original raw/derived evidence.

## What was changed

1. Added `rag_input.json` for each scenario.
   - Uses an explicit `artifacts` list.
   - Each artifact has an ID, type, subtype, source, content, and metadata.
   - Capture timestamps are retained in metadata.
2. Added `starter_input.json` for immediate compatibility with the current `incident_rag_starter`.
   - Network evidence is placed under `logs`.
   - `alerts` and `communications` are intentionally empty.
   - The incident description is placed under `investigation_notes`.
3. Preserved the original `conn.log.json`, `dns.log.json`, `http.log.json`, `tls.log.json`, `chunks.json`, `meta.json`, `reference_qa.json`, and PCAP files unchanged.
4. Kept `reference_qa.json` separate from generation input. It must be used only for evaluation, never supplied to the LLM during generation.
5. No missing alerts, chats, usernames, root causes, or other facts were fabricated.

## Important limitation

The supplied pilot is **network-telemetry-only**. It does not contain genuine communication/chat records or validated Suricata/IDS alert artifacts. Therefore those source types are not invented in this update.

For the final project dataset, add real incident-description/ticker records, alerts, and communication records when those artifacts are available. The RAG pipeline should then ingest them as separate artifact types.

## Recommended usage

- Use `starter_input.json` to run the current starter code without changing its ingestion schema.
- Use `rag_input.json` as the canonical dataset format for the next version of the project pipeline, where ingestion is artifact-generic.

## Evaluation separation

`reference_qa.json` contains reference answers and evidence notes. It is evaluation-only and must not be passed into the generation pipeline.
