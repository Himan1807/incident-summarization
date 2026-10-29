"""Offline smoke test (no Ollama, no model downloads): runs the advanced pipeline on every scenario with stand-in models.
Usage: python tests/smoke_all_scenarios.py   -> prints per-scenario context recall; fails loudly on any crash."""
import sys, re, json, argparse, io, contextlib, numpy as np
ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT)); __import__("os").chdir(ROOT)
from pathlib import Path
from src.pipeline_adv import run
from src.evaluate import atom_in

class FakeEmb:
    def encode(self, texts, **k):
        out=[]
        for t in texts:
            v=np.zeros(512)
            for w in re.findall(r"[\w.\-]+", t.lower()): v[hash(w)%512]+=1
            out.append(v/(np.linalg.norm(v)+1e-9))
        return np.array(out)

def echo_llm(prompt, n=450):
    ev = prompt.split("EVIDENCE:")[-1].split("Write the section now")[0] if "EVIDENCE:" in prompt else ""
    ids = re.findall(r"^\[([^\]\s]+#\d+)\]\n(.*?)(?=\n\[|\Z)", ev, re.S|re.M)
    lines=[]
    for cid, body in ids:
        for l in body.strip().splitlines(): lines.append(f"- {l} [{cid}]")
    if not ids: lines=["- Not established from the available artifacts."]
    return "\n".join(lines), False

root=ROOT/"dataset"/"paper_dataset"; rows=[]
for sc in sorted(p.name for p in root.iterdir() if p.is_dir()):
    a=argparse.Namespace(input=str(root/sc/"rag_input.json"), model=None, dry_run=False, strict=False, no_enrich=False, sections=None)
    buf=io.StringIO()
    with contextlib.redirect_stdout(buf):
        run(a, embedder=FakeEmb(), reranker=None, llm=echo_llm)
    rep=json.load(open(ROOT/"results"/sc/"advanced_run_report.json"))
    ev=rep["evaluation"]
    flagged=sum(rep["verification_totals"].values()) if rep["verification_totals"] else 0
    rows.append((sc, ev["question_recall"], ev["answerable_entity_recall"], ev["overall_entity_recall"], ev["hallucination_rate"], flagged))
    print(f"{sc:14s} qrec={ev['question_recall']} ans={ev['answerable_entity_recall']} overall={ev['overall_entity_recall']} halluc={ev['hallucination_rate']} flagged={flagged} unsupp={ev['unsupported_entities'][:3]}")
n=len(rows); print("MEAN qrec %.3f ans %.3f overall %.3f"%(sum(r[1] for r in rows)/n, sum(r[2] for r in rows)/n, sum(r[3] for r in rows)/n))
