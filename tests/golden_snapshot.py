"""Golden-output snapshot of the advanced pipeline (no Ollama, no model downloads, no network).

For every incident in dataset/paper_dataset it runs src.pipeline_adv twice with the stand-in embedder and no reranker:
  1) --dry-run            -> chunk IDs + texts, every retrieval call (queries -> retrieved IDs) and the retrieved IDs per section
  2) full run, echo LLM   -> the exact prompt (context text) of every LLM call, advanced_postmortem.md,
                             advanced_run_report.json (with its evaluation; timings zeroed) and the text reports it writes
and compares the result with tests/golden/<incident>/. The echo LLM repeats the evidence lines it is given and answers each
investigation question with one evidence line (every 4th question abstains), so all answer statuses are scored.
The snapshot is machine-independent (Windows, macOS, Linux): ties in retrieval scores are broken the same way everywhere,
paths and line endings are normalised, and no real embedder or cross-encoder is loaded.

Usage:
  python tests/golden_snapshot.py            # compare with tests/golden/ ; exit 1 and list the differences if anything changed
  python tests/golden_snapshot.py --update   # (re)write tests/golden/ (only for the Phase 0 baseline or an approved change)
  python tests/golden_snapshot.py --only koi_stealer,easy_123
"""
import sys, os, re, json, io, zlib, argparse, contextlib, difflib, shutil, tempfile
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); os.chdir(ROOT)
sys.modules["sentence_transformers"] = None      # never load a real embedder or cross-encoder: same fused ranking on every machine

_argsort = np.argsort                            # Tied scores come out in a machine-dependent order with numpy's default
def _portable_argsort(a, *args, **kw):           # sort, so the snapshot sorts on scores rounded to 9 decimals with a stable
    kw.pop("kind", None)                         # sort: same ranking on Windows, macOS and Linux. Test-only; src/ unchanged.
    return _argsort(np.round(np.asarray(a, dtype=float), 9), *args, kind="stable", **kw)
np.argsort = _portable_argsort
if hasattr(sys.stdout, "reconfigure"):           # Windows consoles (cp1252) cannot print every character in a diff
    sys.stdout.reconfigure(errors="replace")

import src.pipeline_adv as pa                    # noqa: E402
sys.path.insert(0, str(ROOT / "tests"))
from fakes import HashEmb                        # noqa: E402  same stand-in embedder as the other offline tests

GOLDEN = ROOT / "tests" / "golden"
DATA = ROOT / "dataset" / "paper_dataset"
REPORT_FILES = ("advanced_postmortem.md", "qa_evaluation_rag.txt", "model_comparison.txt")


def echo_llm(calls):                              # smoke_all_scenarios.py's echo LLM + numbered Q&A answers; records every prompt
    def f(prompt, n=450):
        calls.append({"num_predict": n, "prompt": prompt})
        ev = prompt.split("EVIDENCE:")[-1].split("Write the section now")[0] if "EVIDENCE:" in prompt else ""
        ids = re.findall(r"^\[([^\]\s]+#\d+)\]\n(.*?)(?=\n\[|\Z)", ev, re.S | re.M)
        pairs = [(cid, l) for cid, body in ids for l in body.strip().splitlines()]
        if "\nQUESTIONS:\n" in prompt:            # Q&A section: one numbered answer per question, every 4th one abstains,
            qs = re.findall(r"^(\d+)\.", prompt.split("\nQUESTIONS:\n")[1].split("\nVALID EVIDENCE IDS")[0], re.M)
            out = [f"{n}. Not established from the available artifacts." if (i % 4 == 3 or not pairs)   # so the golden covers
                   else f"{n}. {pairs[i % len(pairs)][1]} [{pairs[i % len(pairs)][0]}]" for i, n in enumerate(qs)]  # CORRECT/PARTIAL/
            return "\n".join(out), False                                          # WRONG/ABSTAINED scoring
        lines = [f"- {l} [{cid}]" for cid, l in pairs]
        return ("\n".join(lines) if ids else "- Not established from the available artifacts."), False
    return f


def recording_retriever(base, log):               # wraps AdvancedRetriever without changing what it returns
    class Rec(base):
        def __init__(self, chunks, *a, **k):
            log["chunks"] = [{"id": c["id"], "text": c["text"]} for c in chunks]
            super().__init__(chunks, *a, **k)

        def retrieve(self, queries, rerank_query, *a, **k):
            hits = super().retrieve(queries, rerank_query, *a, **k)
            log["retrievals"].append({"queries": list(queries), "rerank_query": rerank_query,
                                      "ids": [h["chunk"]["id"] for h in hits]})
            return hits
    return Rec


def _args(sc, out, dry):
    return argparse.Namespace(input=str(DATA / sc / "rag_input.json"), model="golden", results_dir=str(out), dry_run=dry,
                              strict=False, annotate=False, no_enrich=False, sections=None, no_postprocess=False,
                              llm_timeline=False)


def _zero_timings(o):
    if isinstance(o, dict):
        return {k: (0 if k in ("seconds", "seconds_total") else _zero_timings(v)) for k, v in o.items()}
    if isinstance(o, list):
        return [_zero_timings(v) for v in o]
    return o


def _dump(o):
    return json.dumps(o, indent=1, ensure_ascii=False, sort_keys=True) + "\n"


def snapshot(sc, tmp):
    """Returns {relative file name: text} for one incident."""
    files, orig = {}, pa.AdvancedRetriever
    try:
        # 1) dry run: retrieval only
        log = {"chunks": [], "retrievals": []}
        pa.AdvancedRetriever = recording_retriever(orig, log)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            pa.run(_args(sc, tmp, True), embedder=HashEmb(), reranker=None, llm=echo_llm([]))
        stdout = [l for l in buf.getvalue().splitlines() if not l.startswith("[warn]")]
        files["chunks.json"] = _dump(log["chunks"])
        files["dry_run.json"] = _dump({"stdout": stdout, "retrievals": log["retrievals"]})
        # 2) full run with the echo LLM
        log = {"chunks": [], "retrievals": []}; calls = []
        pa.AdvancedRetriever = recording_retriever(orig, log)
        with contextlib.redirect_stdout(io.StringIO()):
            pa.run(_args(sc, tmp, False), embedder=HashEmb(), reranker=None, llm=echo_llm(calls))
        files["full_run.json"] = _dump({"retrievals": log["retrievals"], "llm_calls": calls})
        out = Path(tmp) / sc
        rep = json.loads((out / "golden" / "advanced_run_report.json").read_text(encoding="utf-8"))
        files["advanced_run_report.json"] = _dump(_zero_timings(rep))
        for name in REPORT_FILES:
            p = next((q for q in (out / "golden" / name, out / name) if q.exists()), None)
            if p is not None:
                text = p.read_text(encoding="utf-8").replace(str(tmp), "<results>")
                text = re.sub(r"<results>\S*", lambda m: m.group(0).replace("\\", "/"), text)   # Windows path separators
                files[name] = re.sub(r"^(CREATED\s*:\s*)\S+", r"\1<timestamp>", text, flags=re.M)
    finally:
        pa.AdvancedRetriever = orig
    return files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--update", action="store_true", help="rewrite tests/golden/ instead of comparing")
    ap.add_argument("--only", default=None, help="comma-separated incident names")
    a = ap.parse_args()
    scenarios = sorted(p.name for p in DATA.iterdir() if (p / "rag_input.json").exists())
    if a.only:
        scenarios = [s for s in scenarios if s in set(a.only.split(","))]
    tmp = Path(tempfile.mkdtemp(prefix="golden_"))
    changed, n_files = [], 0
    try:
        for sc in scenarios:
            files = snapshot(sc, tmp)
            gdir = GOLDEN / sc
            if a.update:
                shutil.rmtree(gdir, ignore_errors=True); gdir.mkdir(parents=True, exist_ok=True)
                for name, text in files.items():
                    (gdir / name).write_text(text, encoding="utf-8", newline="\n")
                n_files += len(files); print(f"[golden] wrote {sc} ({len(files)} files)")
                continue
            have = {p.name for p in gdir.glob("*")} if gdir.exists() else set()
            for name in sorted(have | set(files)):
                old = (gdir / name).read_text(encoding="utf-8") if name in have else None
                new = files.get(name)
                n_files += 1
                if old != new:
                    changed.append((sc, name, old, new))
            print(f"[golden] {sc}: {'DIFF' if any(c[0] == sc for c in changed) else 'same'}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if a.update:
        print(f"[golden] baseline written: {len(scenarios)} incidents, {n_files} files in {GOLDEN.relative_to(ROOT)}")
        return 0
    if not a.only:                                # an incident that disappeared from the dataset is a difference too
        for gdir in sorted(p for p in GOLDEN.iterdir() if p.is_dir() and p.name not in set(scenarios)):
            changed.append((gdir.name, "(whole incident)", "", None))
    for sc, name, old, new in changed:
        print(f"\n--- {sc}/{name}: " + ("missing in golden" if old is None else "missing in new run" if new is None else "changed"))
        if old is not None and new is not None:
            d = list(difflib.unified_diff(old.splitlines(), new.splitlines(), "golden", "now", lineterm="", n=1))
            print("\n".join(d[:40]) + (f"\n... ({len(d) - 40} more diff lines)" if len(d) > 40 else ""))
    print(f"\n[golden] {len(scenarios)} incidents, {n_files} files compared, {len(changed)} differ")
    if changed:
        print("FAIL"); return 1
    print("OK"); return 0


if __name__ == "__main__":
    sys.exit(main())
