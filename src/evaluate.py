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
Also: unsupported_number_count, placeholder_count.
"""
import json
import re
from pathlib import Path

from src.verify import extract_entities, verify_text, claim_stats, norm_ts, strip_cites, Evidence

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
        if ln.strip().startswith("---") or ln.strip().lower().startswith(("verification note", "_verification")):
            break                                          # the closing note is not part of any answer
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
        row = {"id": item.get("id"), "question": item["question"], "reference_answer": item.get("answer", ""),
               "atoms": atoms, "answerable_from_evidence": answerable,
               "found_in_report": found, "missing_from_evidence": [a for a in atoms if a not in answerable],
               "answer_text": None, "status": "NO ANSWER"}
        pred = blocks.get(item.get("id"))
        if pred is not None:                                   # answer-level precision / recall
            pl = _prep(pred)
            pf = [a for a in atoms if atom_in(a, pl)]
            pents = {e for e in extract_entities(pred)}
            ref_blob = " ".join(_prep(a) for a in atoms)
            ref_blob = re.sub(r"\s+utc\b", "", ref_blob)
            ok = {e for e in pents if e.lower() in ref_blob}
            p_match += len(ok); p_pred += len(pents); r_hit += len(pf); r_tot += len(atoms)
            wrong = sorted(pents - ok)
            abstained = "not established" in pred.lower()
            status = ("CORRECT" if (len(pf) == len(atoms) and not wrong) else "PARTIAL" if pf
                      else "ABSTAINED" if abstained else "WRONG")
            row.update(answer_text=re.sub(r"\s+([.,;:])", r"\1", re.sub(r"\s+", " ", strip_cites(pred))).strip(), predicted_entities=sorted(pents),
                       correct_entities=sorted(ok), atoms_found_in_answer=pf, wrong_entities=wrong, status=status,
                       precision=(round(len(ok) / len(pents), 3) if pents else None), recall=round(len(pf) / len(atoms), 3))
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
        "claims": cs["claims"], "assessment_lines": cs["assessments"],
        "hallucination_rate": round(len(v["unsupported_entities"]) / max(len(v["entities"]), 1), 3),
        "unsupported_entities": v["unsupported_entities"],
        "unsupported_number_count": len(v["unsupported_numbers"]),
        "unsupported_numbers": v["unsupported_numbers"],
        "placeholder_count": len(v["placeholders"]),
        "per_question": rows,
    }


# ---------------------------------------------------------------------------------------------------------------- RQ4
UNANSWERABLE_HEADING = "Additional Investigation Questions"


def unanswerable_blocks(text: str) -> dict[int, str]:
    """{N: answer} from the lines 'U<N>. ...' (or 'N. ...') of the Additional Investigation Questions section text."""
    blocks, cur = {}, None
    for ln in (text or "").splitlines():
        if ln.strip().startswith("---") or ln.strip().lower().startswith(("verification note", "_verification")):
            break
        n = re.match(r"^\s{0,3}U?(\d+)[.)]\s*(.*)$", ln, re.I)
        if n:
            cur = int(n.group(1)); blocks[cur] = n.group(2)
        elif cur is not None and ln.strip():
            blocks[cur] += " " + ln.strip()
    return blocks


def classify_unanswerable(answer: str | None, question: str, absent_type: str) -> tuple[str, list[str]]:
    """ABSTAINED: says the information is not established (the evaluator's ABSTAINED test) and gives no value of the asked type.
    INVENTED : gives a value of the asked type (pattern from src.check_unanswerable), or any entity / number (verify.extract_entities /
               numbers_in) without abstaining. Values that already occur in the question do not count.
    OTHER    : an answer without a specific value and without the abstention phrase (e.g. 'unknown').  NO ANSWER: no answer line."""
    from src.check_unanswerable import ABSENT_TYPES
    from src.verify import numbers_in
    if answer is None or not strip_cites(answer).strip():
        return "NO ANSWER", []
    a = re.sub(r"\s+", " ", strip_cites(answer)).strip()
    asked = sorted(set(m.group(0) for m in ABSENT_TYPES[absent_type].finditer(a)))
    q_l = question.lower()
    other = sorted(v for v in (extract_entities(a) | numbers_in(a)) if v.lower() not in q_l)
    abstains = "not established" in a.lower()
    if asked or (other and not abstains):
        return "INVENTED", asked or other
    return ("ABSTAINED" if abstains else "OTHER"), []


def evaluate_unanswerable(raw_text: str, final_text: str, questions: list[dict], real_eval: dict | None = None) -> dict:
    """RQ4 scores for one report. raw_text = the model's section after formatting, before the fact-check; final_text = the section as
    published (after the fact-check). real_eval = evaluate_report() of the same report, for over-abstention on answerable questions."""
    raw_b, fin_b = unanswerable_blocks(raw_text), unanswerable_blocks(final_text)
    rows = []
    for i, q in enumerate(questions, 1):
        rs, rv = classify_unanswerable(raw_b.get(i), q["question"], q["absent_type"])
        fs, fv = classify_unanswerable(fin_b.get(i), q["question"], q["absent_type"])
        rows.append({"id": q["id"], "question": q["question"], "absent_type": q["absent_type"],
                     "raw_answer": raw_b.get(i), "raw_status": rs, "raw_values": rv,
                     "final_answer": fin_b.get(i), "final_status": fs, "final_values": fv,
                     "removed_by_fact_check": rs == "INVENTED" and fs != "INVENTED"})
    n = len(rows)
    rate = lambda k, key="raw_status": round(sum(r[key] == k for r in rows) / n, 3) if n else None
    out = {"questions": n, "correct_abstention_rate": rate("ABSTAINED"), "invention_rate": rate("INVENTED"),
           "invention_rate_after_fact_check": rate("INVENTED", "final_status"),
           "invented_removed_by_fact_check": sum(r["removed_by_fact_check"] for r in rows),
           "other_rate": rate("OTHER"), "no_answer_rate": rate("NO ANSWER"), "per_question": rows}
    if real_eval:                                          # control: abstentions on the real questions
        real = [r for r in real_eval.get("per_question", []) if r.get("atoms")]
        answerable = [r for r in real if set(r["atoms"]) <= set(r.get("answerable_from_evidence", []))]
        out["answerable_questions"] = len(answerable)
        out["over_abstention_rate"] = round(sum(r["status"] == "ABSTAINED" for r in answerable) / len(answerable), 3) if answerable else None
        out["over_abstention_rate_all_questions"] = round(sum(r["status"] == "ABSTAINED" for r in real) / len(real), 3) if real else None
    return out
