"""Evaluation against reference_qa.json (evaluation-only file). Uses the same extraction rules as verify.py.

Reference answers are split into ATOMS (one IP / domain / host / user / time / label each). An atom is found when it appears in the
text (case-insensitive, defang-insensitive; URLs need host AND file name; times match at minute level; 'C2 server' /
'legitimate service' labels accept common synonyms).

ANSWER-LEVEL (Q&A section 'Answers to Investigation Questions', answer N compared with reference answer N):
  answer_precision  predicted entities (IPs, domains, hosts, URLs, times) that occur in the reference answer / all predicted entities
  answer_recall     reference atoms found in the predicted answer / all reference atoms
  answer_f1         harmonic mean (micro-averaged over all questions)
REPORT-LEVEL (whole report):
  question_recall          mean over questions of (atoms found anywhere in the report / atoms)   <- paper-style recall
  answerable_entity_recall atoms that exist in the evidence and appear in the report
  overall_entity_recall    all atoms found / all atoms
  hallucination_rate       report entities not in the evidence / all report entities
CLAIM-LEVEL:
  faithfulness       claims whose facts are in the evidence AND in the chunks they cite / all claims
  grounding_rate     claims whose facts are in the evidence (any report, cited or not)
  citation_precision cited claims actually supported by the chunks they cite
  citation_rate      cited claims / all claims
Also: unsupported_number_count, placeholder_count.
"""
import json
import re
from pathlib import Path

from src.verify import extract_entities, verify_text, claim_stats, norm_ts, Evidence

SYNONYMS = {"c2 server": ["c2", "command-and-control", "command and control", "c&c"],
            "legitimate service": ["legitimate", "benign"]}
QA_HEADING = "answers to investigation questions"


def _prep(t: str) -> str:
    return norm_ts(t).lower()


def atom_in(atom: str, text_lower: str) -> bool:
    a = _prep(atom).strip()
    a = re.sub(r"\s+utc$", "", a)
    if a in SYNONYMS:
        return any(s in text_lower for s in SYNONYMS[a])
    if a in text_lower:
        return True
    if "://" in a:
        rest = a.split("://", 1)[1]
        host, _, path = rest.partition("/")
        base = path.rstrip("/").split("/")[-1]
        return host.split(":")[0] in text_lower and (not base or base in text_lower)
    return False


def _atoms(item: dict) -> list[str]:
    if item.get("atoms"):
        return [a["text"] if isinstance(a, dict) else a for a in item["atoms"]]
    return sorted(extract_entities(item["answer"]))


def answer_blocks(report: str) -> dict[int, str]:
    """Extract {N: text} from the 'Answers to Investigation Questions' section (lines starting 'N.')."""
    m = re.search(r"^##\s*" + QA_HEADING + r".*?$(.*?)(?=^##\s|\Z)", report, re.S | re.M | re.I)
    if not m:
        return {}
    blocks, cur = {}, None
    for ln in m.group(1).splitlines():
        n = re.match(r"^\s{0,3}(\d+)[.)]\s*(.*)$", ln)
        if n:
            cur = int(n.group(1)); blocks[cur] = n.group(2)
        elif cur is not None:
            blocks[cur] += " " + ln.strip()
    return blocks


def evaluate_report(report: str, qa_path: str, ev: Evidence, valid_ids: set[str], chunk_text: dict | None = None) -> dict:
    qa = json.loads(Path(qa_path).read_text(encoding="utf-8"))["qa"]
    rep_l = _prep(report)
    blocks = answer_blocks(report)
    rows, ans_hit, ans_tot, all_hit, all_tot, q_scores, q_correct = [], 0, 0, 0, 0, [], 0
    p_match = p_pred = r_hit = r_tot = 0
    for item in qa:
        atoms = _atoms(item)
        if not atoms:
            rows.append({"question": item["question"], "type": "abstain"}); continue
        found = [a for a in atoms if atom_in(a, rep_l)]
        answerable = [a for a in atoms if atom_in(a, ev.text)]
        ans_tot += len(answerable); ans_hit += len([a for a in answerable if a in found])
        all_tot += len(atoms); all_hit += len(found)
        q_scores.append(len(found) / len(atoms)); q_correct += bool(found)
        row = {"question": item["question"], "atoms": atoms, "answerable_from_evidence": answerable,
               "found_in_report": found, "missing_from_evidence": [a for a in atoms if a not in answerable]}
        pred = blocks.get(item.get("id"))
        if pred is not None:                                   # answer-level precision / recall
            pl = _prep(pred)
            pf = [a for a in atoms if atom_in(a, pl)]
            pents = {e for e in extract_entities(pred)}
            ref_blob = " ".join(_prep(a) for a in atoms)
            ref_blob = re.sub(r"\s+utc\b", "", ref_blob)
            ok = {e for e in pents if e.lower() in ref_blob}
            p_match += len(ok); p_pred += len(pents); r_hit += len(pf); r_tot += len(atoms)
            row.update(predicted_entities=sorted(pents), correct_entities=sorted(ok), atoms_found_in_answer=pf,
                       wrong_entities=sorted(pents - ok))
        rows.append(row)
    prec = round(p_match / p_pred, 3) if p_pred else None
    rec = round(r_hit / r_tot, 3) if blocks and r_tot else None
    f1 = round(2 * prec * rec / (prec + rec), 3) if prec and rec else (0.0 if prec is not None and rec is not None else None)
    v = verify_text(report, ev, valid_ids)
    cs = claim_stats(report, ev, valid_ids, chunk_text)
    return {
        "answer_precision": prec, "answer_recall": rec, "answer_f1": f1,
        "question_recall": round(sum(q_scores) / len(q_scores), 3) if q_scores else None,
        "questions_correct": f"{q_correct}/{len(q_scores)}",
        "answerable_entity_recall": round(ans_hit / ans_tot, 3) if ans_tot else None,
        "overall_entity_recall": round(all_hit / all_tot, 3) if all_tot else None,
        "faithfulness": cs["faithfulness"], "grounding_rate": cs["grounding_rate"],
        "citation_precision": cs["citation_precision"],
        "citation_rate": round(cs["cited_claims"] / cs["claims"], 3) if cs["claims"] else None,
        "claims": cs["claims"], "uncited_lines": cs["uncited_claims"],
        "hallucination_rate": round(len(v["unsupported_entities"]) / max(len(v["entities"]), 1), 3),
        "unsupported_entities": v["unsupported_entities"],
        "unsupported_number_count": len(v["unsupported_numbers"]),
        "unsupported_numbers": v["unsupported_numbers"],
        "placeholder_count": len(v["placeholders"]),
        "per_question": rows,
    }
