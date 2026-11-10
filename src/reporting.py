"""Plain-text reports (tables) built from the stored evaluation results. No LLM calls.

  qa_evaluation_rag.txt / qa_evaluation_no_rag.txt   per incident + model: question | reference answer | answer from the report | metrics
  rag_vs_no_rag.txt                                  per incident + model: the same LLM with and without retrieval, side by side
  model_comparison.txt                               per incident: all models (and conditions) compared on every metric
Layout on disk:  results/<incident>/<model>/{advanced_postmortem.md, advanced_run_report.json, no_rag_postmortem.md, ...}
"""
import json
import re
import textwrap
from datetime import datetime
from pathlib import Path

METRICS = [
    ("answer_precision", "Answer precision", "Entities (IPs, domains, hosts, URLs, times) in the report's answers that also occur in the reference / all entities it gave"),
    ("answer_recall", "Answer recall", "Reference answer items found in the report's answers / all reference items"),
    ("answer_f1", "Answer F1", "Harmonic mean of answer precision and recall"),
    ("question_recall", "Question recall", "Mean over questions of reference items found anywhere in the report"),
    ("faithfulness", "Faithfulness", "Claims whose facts are in the evidence AND in the chunks they cite / all claims"),
    ("grounding_rate", "Grounding rate", "Claims whose entities and numbers all exist in the evidence"),
    ("citation_precision", "Citation precision", "Cited claims that are actually supported by the chunks they cite"),
    ("citation_rate", "Citation rate", "Cited claims / all claims"),
    ("hallucination_rate", "Hallucination rate", "Entities in the report that are absent from the evidence / all entities (lower is better)"),
    ("unsupported_number_count", "Unsupported numbers", "Numbers in the report that are absent from the evidence (lower is better)"),
    ("placeholder_count", "Placeholders", "'[insert ...]' placeholders left in the report (lower is better)"),
]
LOWER_BETTER = {"hallucination_rate", "unsupported_number_count", "placeholder_count"}


def model_tag(model: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", model)


def fmt(v) -> str:
    if v is None:
        return "-"
    if isinstance(v, float):
        return f"{v:.3f}"
    return str(v)


def _wrap(text, width):
    return textwrap.wrap(str(text), width=width, break_long_words=True, replace_whitespace=True) or [""]


def render_table(headers, rows, widths, title=None) -> str:
    sep = "+" + "+".join("-" * (w + 2) for w in widths) + "+"

    def row_lines(cells):
        wrapped = [_wrap(c, w) for c, w in zip(cells, widths)]
        height = max(len(x) for x in wrapped)
        return ["| " + " | ".join((wrapped[j][i] if i < len(wrapped[j]) else "").ljust(widths[j]) for j in range(len(widths))) + " |"
                for i in range(height)]

    out = [title] if title else []
    out += [sep] + row_lines(headers) + [sep]
    for r in rows:
        out += row_lines(r) + [sep]
    return "\n".join(out)


def _found(q):
    if q.get("answer_text") is None:
        return "-"
    return f"{len(q.get('atoms_found_in_answer', []))}/{len(q['atoms'])}"


def _prec(q):
    pred = q.get("predicted_entities") or []
    return f"{len(q.get('correct_entities', []))}/{len(pred)}" if pred else "-"


def status_counts(ev) -> dict:
    c = {"CORRECT": 0, "PARTIAL": 0, "WRONG": 0, "ABSTAINED": 0, "NO ANSWER": 0}
    for q in ev["per_question"]:
        if q.get("type") != "abstain":
            c[q.get("status", "NO ANSWER")] += 1
    return c


def _qs(ev):
    return [q for q in ev["per_question"] if q.get("type") != "abstain"]


def _header(scenario, model, condition, info):
    lines = ["=" * 100, f"INCIDENT : {scenario}", f"MODEL    : {model}", f"CONDITION: {condition}"]
    if info.get("seconds") is not None:
        lines.append(f"RUN TIME : {info['seconds'] / 60:.1f} min of LLM generation")
    if info.get("report"):
        lines.append(f"REPORT   : {info['report']}")
    lines += [f"CREATED  : {datetime.now().isoformat(timespec='seconds')}", "=" * 100]
    return "\n".join(lines)


def metrics_table(ev) -> str:
    rows = [[label, fmt(ev.get(key)), meaning] for key, label, meaning in METRICS]
    sc = status_counts(ev)
    rows += [["Questions correct / partial / wrong / abstained / unanswered",
              f"{sc['CORRECT']} / {sc['PARTIAL']} / {sc['WRONG']} / {sc['ABSTAINED']} / {sc['NO ANSWER']}", "Per-question status in the table above"],
             ["Claims (cited / total)", f"{ev.get('claims', 0) - ev.get('uncited_lines', 0)} / {ev.get('claims', 0)}",
              "Claim lines counted by the verifier; hedged assessments are excluded"]]
    return render_table(["Metric", "Value", "Meaning"], rows, [44, 12, 70])


def write_qa_evaluation(path: Path, scenario: str, model: str, condition: str, ev: dict, info: dict) -> str:
    rows = [[q.get("id"), q["question"], q.get("reference_answer", ""), q.get("answer_text") or "(no answer in the report)",
             _found(q), _prec(q), ", ".join(q.get("wrong_entities", [])) or "-", q.get("status", "NO ANSWER")] for q in _qs(ev)]
    text = "\n".join([
        _header(scenario, model, condition, info), "",
        "A. QUESTION-BY-QUESTION EVALUATION",
        "   Found = reference items present in the report's answer; Prec. = correct entities / entities the answer gave;",
        "   Wrong items = entities in the answer that are not in the reference answer.", "",
        render_table(["#", "Question", "Reference answer", "Answer from the report", "Found", "Prec.", "Wrong items", "Status"],
                     rows, [3, 32, 26, 34, 5, 5, 16, 9]), "",
        "B. METRICS", "", metrics_table(ev), "",
        "Status: CORRECT = every reference item found and nothing wrong; PARTIAL = some items found or wrong items present;",
        "        WRONG = answer given but no reference item found; ABSTAINED = the report says 'Not established from the available artifacts';",
        "        NO ANSWER = the report has no answer for that question.", ""])
    Path(path).write_text(text, encoding="utf-8")
    return text


def write_rag_vs_norag(path: Path, scenario: str, model: str, rag: dict, norag: dict, rag_info: dict, norag_info: dict) -> str:
    mrows = []
    for key, label, _ in METRICS:
        a, b = norag.get(key), rag.get(key)
        if isinstance(a, int) and isinstance(b, int):
            delta = f"{b - a:+d}"
        else:
            delta = f"{b - a:+.3f}" if isinstance(a, (int, float)) and isinstance(b, (int, float)) else "-"
        mrows.append([label + (" (lower is better)" if key in LOWER_BETTER else ""), fmt(a), fmt(b), delta])
    sn, sr = status_counts(norag), status_counts(rag)
    mrows.append(["Questions CORRECT", sn["CORRECT"], sr["CORRECT"], f"{sr['CORRECT'] - sn['CORRECT']:+d}"])
    mrows.append(["Questions PARTIAL", sn["PARTIAL"], sr["PARTIAL"], f"{sr['PARTIAL'] - sn['PARTIAL']:+d}"])
    mrows.append(["Questions WRONG", sn["WRONG"], sr["WRONG"], f"{sr['WRONG'] - sn['WRONG']:+d}"])
    mrows.append(["Questions ABSTAINED / unanswered", f"{sn['ABSTAINED']} / {sn['NO ANSWER']}", f"{sr['ABSTAINED']} / {sr['NO ANSWER']}", "-"])
    if norag_info.get("seconds") is not None and rag_info.get("seconds") is not None:
        mrows.append(["LLM generation time (min)", f"{norag_info['seconds'] / 60:.1f}", f"{rag_info['seconds'] / 60:.1f}", "-"])
    nq = {q["id"]: q for q in _qs(norag)}
    prow = []
    for q in _qs(rag):
        n = nq.get(q["id"], {})
        prow.append([q["id"], q["question"], q.get("reference_answer", ""), n.get("answer_text") or "(no answer)",
                     q.get("answer_text") or "(no answer)", n.get("status", "NO ANSWER"), q.get("status", "NO ANSWER")])
    text = "\n".join([
        _header(scenario, model, "No RAG vs RAG (same LLM, same section plan, same questions)", {}), "",
        "NO RAG : the LLM receives only the incident context (network description and the questions). It has NO logs, alerts or query results.",
        "         Output is formatted (titles/preambles removed) but not verified, de-duplicated or given citations.",
        "RAG    : the advanced pipeline (hybrid retrieval, reranking, section-wise generation with citations, verification).",
        "Hallucination, grounding and number checks are always measured against the REAL evidence of the incident.", "",
        "A. METRICS", "",
        render_table(["Metric", "No RAG", "RAG", "RAG - No RAG"], mrows, [52, 14, 14, 14]), "",
        "B. ANSWERS PER QUESTION", "",
        render_table(["#", "Question", "Reference answer", "No RAG answer", "RAG answer", "No RAG", "RAG"],
                     prow, [3, 28, 24, 30, 30, 9, 9]), "",
        "Faithfulness and citation metrics are 0 / '-' for No RAG by construction: without retrieved chunks it cannot cite evidence.", ""])
    Path(path).write_text(text, encoding="utf-8")
    return text


SHORT = {"CORRECT": "OK", "PARTIAL": "PART", "WRONG": "WRONG", "ABSTAINED": "ABST", "NO ANSWER": "NONE"}


def write_model_comparison(path: Path, scenario: str, entries: list[dict]) -> str:
    """entries: [{label, model, condition, ev, seconds}]"""
    cols = [("answer_precision", "Ans-P"), ("answer_recall", "Ans-R"), ("answer_f1", "Ans-F1"), ("question_recall", "Q-recall"),
            ("faithfulness", "Faithful"), ("grounding_rate", "Ground."), ("citation_precision", "CitePrec"), ("citation_rate", "CiteRate"),
            ("hallucination_rate", "Halluc."), ("unsupported_number_count", "BadNum")]
    ids = [f"R{i}" for i in range(1, len(entries) + 1)]
    mrows = [[i, e["label"]] + [fmt(e["ev"].get(k)) for k, _ in cols] + [f"{e['seconds'] / 60:.1f}" if e.get("seconds") is not None else "-"]
             for i, e in zip(ids, entries)]
    base = entries[0]["ev"]
    qrows = []
    for q in _qs(base):
        row = [q["id"], q["question"], q.get("reference_answer", "")]
        for e in entries:
            m = next((x for x in _qs(e["ev"]) if x["id"] == q["id"]), None)
            row.append(SHORT[m["status"]] if m else "-")
        qrows.append(row)
    best = [(e["ev"].get("answer_f1") or 0.0, e["label"]) for e in entries]
    best.sort(reverse=True)
    lines = ["=" * 100, f"INCIDENT: {scenario}   -   comparison of {len(entries)} run(s) (models and conditions)",
             f"CREATED : {datetime.now().isoformat(timespec='seconds')}", "=" * 100, "",
             "Runs:  " + "   ".join(f"{i} = {e['label']}" for i, e in zip(ids, entries)), "",
             "A. METRICS PER RUN (higher is better except Halluc. and BadNum)", "",
             render_table(["Run", "Model / condition"] + [n for _, n in cols] + ["Min"], mrows,
                          [4, 34] + [8] * len(cols) + [6]), "",
             "B. ANSWER STATUS PER QUESTION  (OK = correct, PART = partial, WRONG, ABST = 'Not established', NONE = no answer in the report)", "",
             render_table(["#", "Question", "Reference answer"] + ids, qrows, [3, 40, 30] + [6] * len(ids)), "",
             f"Best answer F1: {best[0][1]} ({best[0][0]:.3f})", "",
             "Metric definitions: see METRICS.md. 'no RAG' rows have no retrieved evidence, so their faithfulness and citation metrics are 0 or '-'.", ""]
    text = "\n".join(lines)
    Path(path).write_text(text, encoding="utf-8")
    return text


def _load(p: Path):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def refresh_reports(scenario: str, results_dir: str = "results") -> list[str]:
    """(Re)build every text report of one incident from the stored run reports. Returns the written paths."""
    root = Path(results_dir) / scenario
    written, entries = [], []
    for mdir in sorted(p for p in root.iterdir() if p.is_dir()) if root.exists() else []:
        rag, nor = _load(mdir / "advanced_run_report.json"), _load(mdir / "no_rag_run_report.json")
        rag_ev = (rag or {}).get("evaluation")
        nor_ev = (nor or {}).get("evaluation")
        model = (rag or nor or {}).get("model", mdir.name)
        rag_info = {"seconds": (rag or {}).get("seconds_total"), "report": str(mdir / "advanced_postmortem.md")}
        nor_info = {"seconds": (nor or {}).get("seconds_total"), "report": str(mdir / "no_rag_postmortem.md")}
        if rag_ev:
            write_qa_evaluation(mdir / "qa_evaluation_rag.txt", scenario, model, "RAG (advanced pipeline)", rag_ev, rag_info)
            written.append(str(mdir / "qa_evaluation_rag.txt"))
            entries.append({"label": f"{model} (RAG)", "model": model, "condition": "rag", "ev": rag_ev, "seconds": rag_info["seconds"]})
        if nor_ev:
            write_qa_evaluation(mdir / "qa_evaluation_no_rag.txt", scenario, model, "No RAG (LLM without retrieval)", nor_ev, nor_info)
            written.append(str(mdir / "qa_evaluation_no_rag.txt"))
            entries.append({"label": f"{model} (no RAG)", "model": model, "condition": "no_rag", "ev": nor_ev, "seconds": nor_info["seconds"]})
        if rag_ev and nor_ev:
            write_rag_vs_norag(mdir / "rag_vs_no_rag.txt", scenario, model, rag_ev, nor_ev, rag_info, nor_info)
            written.append(str(mdir / "rag_vs_no_rag.txt"))
    if entries:
        write_model_comparison(root / "model_comparison.txt", scenario, entries)
        written.append(str(root / "model_comparison.txt"))
    return written


def write_overall_summary(results_dir: str = "results") -> str | None:
    """results/summary.txt: every incident x model x condition, plus the mean per model and condition."""
    root = Path(results_dir)
    cols = [("answer_f1", "Ans-F1"), ("answer_precision", "Ans-P"), ("answer_recall", "Ans-R"), ("question_recall", "Q-recall"),
            ("faithfulness", "Faithful"), ("grounding_rate", "Ground."), ("hallucination_rate", "Halluc.")]
    rows, acc = [], {}
    for sdir in sorted(p for p in root.iterdir() if p.is_dir()) if root.exists() else []:
        for mdir in sorted(p for p in sdir.iterdir() if p.is_dir()):
            for fname, cond in (("advanced_run_report.json", "RAG"), ("no_rag_run_report.json", "no RAG")):
                rep = _load(mdir / fname)
                ev = (rep or {}).get("evaluation")
                if not ev:
                    continue
                model = rep.get("model", mdir.name)
                rows.append([sdir.name, model, cond] + [fmt(ev.get(k)) for k, _ in cols])
                for k, _ in cols:
                    if isinstance(ev.get(k), (int, float)):
                        acc.setdefault((model, cond, k), []).append(ev[k])
    if not rows:
        return None
    means = []
    for (model, cond) in sorted({(m, c) for m, c, _ in acc}):
        means.append(["MEAN", model, cond] + [fmt(sum(acc[(model, cond, k)]) / len(acc[(model, cond, k)])) if (model, cond, k) in acc else "-"
                                              for k, _ in cols])
    text = "\n".join(["=" * 100, "ALL INCIDENTS - every model and condition", f"CREATED: {datetime.now().isoformat(timespec='seconds')}", "=" * 100, "",
                      render_table(["Incident", "Model", "Condition"] + [n for _, n in cols], rows + means, [14, 28, 9] + [8] * len(cols)), ""])
    (root / "summary.txt").write_text(text, encoding="utf-8")
    return str(root / "summary.txt")


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Rebuild all text reports from stored results (no LLM needed).")
    ap.add_argument("--scenarios", default=None, help="comma-separated; default: every incident found in the results folder")
    ap.add_argument("--results", default="results")
    a = ap.parse_args()
    names = a.scenarios.split(",") if a.scenarios else sorted(p.name for p in Path(a.results).iterdir() if p.is_dir())
    for sc in names:
        for w in refresh_reports(sc, a.results):
            print("wrote", w)
    w = write_overall_summary(a.results)
    if w:
        print("wrote", w)


if __name__ == "__main__":
    main()
