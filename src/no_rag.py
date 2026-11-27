"""'No RAG' condition: the SAME LLM, the SAME section plan and the SAME questions, but WITHOUT retrieved evidence.

The model only sees the incident context (neutral description, network context, query window) and the questions; it has no logs, alerts or
query results. The output is only formatted (preambles / repeated titles removed, unfinished last line dropped); it is NOT verified,
de-duplicated or given citations. It is evaluated against the real evidence with the same evaluator as the RAG report.

python -m src.no_rag --input dataset/paper_dataset/koi_stealer/rag_input.json --model llama3.2:3b
Option: --fair-norag-evidence  score against the same evidence as the RAG run (artifacts + raw-log enrichment); off by default.
        --section-profile auto|security|service_outage  same section plan as the RAG run (default: security for every incident)
"""
import argparse
import json
import time
from pathlib import Path

from config import AdvancedSettings
from src.adv_ingestion import load_artifacts
from src.adv_chunking import chunk_artifacts
from src.adv_generation import call_llm
from src.check_env import preflight
from src.enrichment import build_enrichment
from src.common import incident_header
from src.evaluate import evaluate_report
from src.postprocess import clean_model_output, drop_partial_tail
from src.reporting import model_tag, refresh_reports
from src.sections import build_sections, resolve_profile
from src.verify import make_evidence

NO_RAG_SYSTEM = """You are an incident-response analyst writing ONE section of a postmortem.
You were NOT given any logs, alerts or query results - only the incident context below. Write the section as completely and specifically as you can
(affected host, IP addresses, domains, times, accounts), using the context and your general knowledge. Bullets only, concise, no title, no introduction."""
_NO_RAG_DETAILS = {"security": "(affected host, IP addresses, domains, times, accounts)",
                   "service_outage": "(root-cause service, pod, node, metrics, times, fault type)"}


def _no_rag_system(profile: str) -> str:
    return NO_RAG_SYSTEM if profile == "security" else NO_RAG_SYSTEM.replace(_NO_RAG_DETAILS["security"], _NO_RAG_DETAILS[profile])


def no_rag_prompt(section: dict, header: str, all_sections: list[str], profile: str = "security") -> str:
    length = f"LENGTH: write AT MOST {section['max_bullets']} bullets, one short line each, then stop.\n" if section.get("max_bullets") else ""
    return (f"{_no_rag_system(profile)}\n\nINCIDENT CONTEXT:\n{header}\n\nREPORT STRUCTURE (you write ONLY '{section['name']}'): "
            f"{'; '.join(all_sections)}\n\nSECTION: {section['name']}\nTASK: {section['task']}\n{length}\nWrite the section now (Markdown bullets):")


def no_rag_summary_prompt(header: str, sections_text: str, profile: str = "security") -> str:
    return (f"{_no_rag_system(profile)}\n\nINCIDENT CONTEXT:\n{header}\n\nBelow are the postmortem sections you wrote.\n"
            f"TASK: Write a 4-6 sentence Incident Summary from them. Start directly with the summary.\n\nSECTIONS:\n{sections_text}\n\nIncident Summary:")


def run_no_rag(args, llm=None):
    S = AdvancedSettings()
    if getattr(args, "model", None):
        S.ollama_model = args.model
    if llm is None:
        preflight(S.ollama_model, S.ollama_url, need_llm=True)
    inp = Path(args.input)
    folder = inp.parent
    data = load_artifacts(str(inp))
    meta = data["metadata"]
    scenario = meta.get("scenario", folder.name)
    artifacts = data["artifacts"]
    fair = getattr(args, "fair_norag_evidence", False)
    if fair and S.enable_enrichment and not getattr(args, "no_enrich", False):   # same evaluation evidence as pipeline_adv
        artifacts = artifacts + build_enrichment(artifacts, str(folder), scenario)
    chunks = chunk_artifacts(artifacts, S.items_per_chunk)           # used ONLY to evaluate (real evidence), never shown to the LLM
    header = incident_header(meta, data["description"])
    usage = {}                                           # filled only by hosted models (src/llm_api.py)
    gen = llm or (lambda p, n: call_llm(p, S, n, usage))
    profile = resolve_profile(getattr(args, "section_profile", None), meta)
    sections = build_sections(data.get("questions"), profile)
    names = [s["name"] for s in sections]
    parts, run_log = [], []
    for sec in sections:
        t0 = time.time()
        n_tok = S.num_predict_long if sec.get("long") else S.num_predict
        raw, truncated = gen(no_rag_prompt(sec, header, names, profile), n_tok)
        if truncated:
            raw, _ = drop_partial_tail(raw)
        text = clean_model_output(raw, sec["name"])
        parts.append(f"## {sec['name']}\n\n{text}\n")
        run_log.append({"section": sec["name"], "seconds": round(time.time() - t0, 1), "truncated": truncated})
        print(f"[no-rag] {sec['name']} ({run_log[-1]['seconds']}s)")
    body = "\n".join(parts)
    summ_raw, st = gen(no_rag_summary_prompt(header, body, profile), S.num_predict)
    if st:
        summ_raw, _ = drop_partial_tail(summ_raw)
    summ = clean_model_output(summ_raw, "Incident Summary")
    report = f"# Incident Postmortem (no RAG): {meta.get('title', scenario)}\n\n## Incident Summary\n\n{summ}\n\n{body}"

    out_dir = Path(getattr(args, "results_dir", "results")) / scenario / model_tag(S.ollama_model)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "no_rag_postmortem.md").write_text(report, encoding="utf-8")
    result = {"condition": "no_rag", "model": S.ollama_model, "scenario": scenario,
              "seconds_total": round(sum(e["seconds"] for e in run_log), 1), "run_log": run_log}
    if fair:
        result["evaluation_evidence"] = "same as RAG (artifacts + raw-log enrichment)"
    if getattr(args, "section_profile", None):                 # recorded only when the option is used
        result["section_profile"] = profile
    if usage:                                              # hosted models only
        result["llm_usage"] = dict(usage)
    qa = folder / "reference_qa.json"
    if qa.exists():                                          # evaluation only; answers are never given to the LLM
        ev_text = make_evidence("\n".join(c["text"] for c in chunks), header)
        result["evaluation"] = evaluate_report(report, str(qa), ev_text, {c["id"] for c in chunks}, {c["id"]: c["text"] for c in chunks})
    (out_dir / "no_rag_run_report.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    for w in refresh_reports(scenario, getattr(args, "results_dir", "results")):
        print("[report]", w)
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--model", default=None)
    ap.add_argument("--results-dir", default="results", dest="results_dir")
    ap.add_argument("--fair-norag-evidence", action="store_true", dest="fair_norag_evidence",
                    help="score against the same evidence as the RAG run (adds the raw-log enrichment); off by default")
    ap.add_argument("--section-profile", default=None, choices=["auto", "security", "service_outage"], dest="section_profile",
                    help="section plan (same as the RAG run); default: security for every incident")
    print(run_no_rag(ap.parse_args()))


if __name__ == "__main__":
    main()
