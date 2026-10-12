"""Evaluation against reference_qa.json (evaluation-only file).

Metrics (all deterministic, CPU-cheap):
  * answerable_entity_recall : reference-answer entities that EXIST in the evidence and appear in the report
  * overall_entity_recall    : same, over all reference entities (includes facts missing from the evidence)
  * hallucination_rate       : share of entities in the report not found in the evidence
  * placeholder_count        : '[insert ...]' style placeholders
  * citation_rate            : share of non-empty bullet/sentence lines that carry a valid evidence citation
"""
import json
import re
from pathlib import Path

from src.verify import extract_entities, verify_text, CITE_RE, PLACEHOLDER_RE


def evaluate_report(report: str, qa_path: str, corpus_lower: str, valid_ids: set[str]) -> dict:
    qa = json.loads(Path(qa_path).read_text(encoding="utf-8"))["qa"]
    rep_l = report.lower()
    rows, ans_hit, ans_tot, all_hit, all_tot = [], 0, 0, 0, 0
    for item in qa:
        ents = extract_entities(item["answer"])
        # answers like 'Not determined' have no entity: check the report does not claim them
        if not ents:
            rows.append({"question": item["question"], "type": "abstain", "entities": [], "found": []})
            continue
        found = [e for e in ents if e.lower() in rep_l]
        answerable = [e for e in ents if e.lower() in corpus_lower]
        ans_tot += len(answerable); ans_hit += len([e for e in answerable if e in found])
        all_tot += len(ents); all_hit += len(found)
        rows.append({"question": item["question"], "type": "entity", "entities": sorted(ents),
                     "answerable_from_evidence": sorted(answerable), "found_in_report": sorted(found)})
    v = verify_text(report, corpus_lower, valid_ids)
    lines = [l for l in report.splitlines() if len(l.strip()) > 25 and not l.strip().startswith("#")]
    cited = [l for l in lines if any(c in valid_ids for c in CITE_RE.findall(l))]
    return {
        "answerable_entity_recall": round(ans_hit / ans_tot, 3) if ans_tot else None,
        "overall_entity_recall": round(all_hit / all_tot, 3) if all_tot else None,
        "hallucination_rate": round(len(v["unsupported_entities"]) / max(len(v["entities"]), 1), 3),
        "unsupported_entities": v["unsupported_entities"],
        "placeholder_count": len(PLACEHOLDER_RE.findall(report)),
        "citation_rate": round(len(cited) / max(len(lines), 1), 3),
        "per_question": rows,
    }
