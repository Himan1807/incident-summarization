"""Offline test of src/prepare_rcaeval.py on a tiny fake RE2-OB case (no download needed).
The fake case has a CPU fault in checkoutservice injected after 12 minutes; the test checks the reference answers, that the
incident name and artifact ids do not reveal the answer, that the injected time is not used for the baseline, and that the
output is deterministic.   Usage: python tests/test_prepare_rcaeval.py"""
import sys, io, json, zipfile, tempfile
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); __import__("os").chdir(ROOT)
from src.prepare_rcaeval import convert, write_report_section

T0, INJ = 1705353846, 1705353846 + 720
SERVICES = ["cartservice", "checkoutservice", "currencyservice", "frontend"]


def fake_zip() -> bytes:
    t = np.arange(T0, T0 + 1441); rng = np.random.default_rng(0); b = io.BytesIO()
    cols = {"time": t}
    for s in SERVICES:
        cols[f"{s}_cpu"] = 1.0 + 0.01 * rng.standard_normal(len(t)); cols[f"{s}_mem"] = 1e7 + 1e4 * rng.standard_normal(len(t))
        cols[f"{s}_latency-90"] = 0.005 + 0.0001 * rng.standard_normal(len(t))
    cols["checkoutservice_cpu"][t >= INJ + 3] += 5.0                            # the fault
    cols["frontend_latency-90"][t >= INJ + 10] += 0.05                          # its downstream symptom
    sm = ",".join(cols) + "\n" + "\n".join(",".join(str(int(cols[c][i])) if c == "time" else f"{cols[c][i]:.6g}" for c in cols) for i in range(len(t)))
    tl = np.arange(T0, T0 + 1441, 15)
    lat = "time,checkoutservice_PlaceOrder,frontendservice_frontend\n" + "\n".join(
        f"{x},{2 if x < INJ else 3},{1 if x < INJ else 9}" for x in tl)
    err = "time,checkoutservice_PlaceOrder,frontendservice_frontend\n" + "\n".join(f"{x},0.0,0.0" for x in tl)
    logs = "time,timestamp,container_name,message,level,req_path,error\n" + "\n".join(
        f"00:00,{(T0 + i) * 10**9},{SERVICES[i % 4]},request {i} served,info,," for i in range(0, 1440, 3))
    pods = "POD,NODE_NAME\n" + "\n".join(f"{s}-abc{i}-x{i}y,gke-node-{i % 2}" for i, s in enumerate(SERVICES))
    with zipfile.ZipFile(b, "w") as z:
        base = "RE2-OB/checkoutservice_cpu/1/"
        for name, text in (("inject_time.txt", str(INJ)), ("simple_metrics.csv", sm), ("tracets_lat.csv", lat), ("tracets_err.csv", err),
                           ("logs.csv", logs), ("pod-node-1.csv", pods), ("pod-node-2.csv", pods)):
            z.writestr(base + name, text)
    return b.getvalue()


def run(out: Path) -> dict:
    z = zipfile.ZipFile(io.BytesIO(fake_zip()))
    rep = convert(z, "checkoutservice_cpu", "re2ob_01", out)
    write_report_section(out, [rep])
    return rep


with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
    rep = run(Path(a)); run(Path(b))
    files = sorted(p.relative_to(a) for p in Path(a).rglob("*") if p.is_file())
    assert files == sorted(p.relative_to(b) for p in Path(b).rglob("*") if p.is_file())
    assert all((Path(a) / f).read_bytes() == (Path(b) / f).read_bytes() for f in files), "output must be deterministic"
    d = Path(a) / "re2ob_01"
    rag = json.loads((d / "rag_input.json").read_text(encoding="utf-8"))
    qa = {i["id"]: i for i in json.loads((d / "reference_qa.json").read_text(encoding="utf-8"))["qa"]}
    answers = {k: v["answer"] for k, v in qa.items()}
    print(json.dumps(answers, indent=1)); print("atoms in evidence:", rep["atoms_in_evidence"], "/", rep["atoms"], rep["atoms_not_in_evidence"])
    assert answers[1] == "checkoutservice" and answers[2] == "checkoutservice-abc1-x1y" and answers[3] == "gke-node-1"
    assert answers[4] == "CPU" and answers[5] == "availability" and answers[6] == "2024-01-15 21:36 UTC"
    assert answers[7] == "checkoutservice_cpu" and answers[8] == "frontendservice_frontend, downstream symptom"
    assert len(rag["investigation_questions"]) == 8
    assert all("checkoutservice" not in x["artifact_id"] and "cpu" not in x["artifact_id"] for x in rag["artifacts"]), "ids must be neutral"
    assert "checkoutservice_cpu" not in json.dumps(rag["metadata"]) + rag["incident_description"]
    facts = [f for x in rag["artifacts"] for f in json.loads(x["content"])["facts"]]
    first = next(f for f in facts if f.startswith("metric anomalies: checkoutservice_cpu"))
    assert "sustained deviation from 2024-01-15 21:36:09 UTC" in first, first
    assert rep["atoms_in_evidence"] == rep["atoms"], rep
    assert "# RCAEval RE2-OB" in (Path(a) / "DATASET_REPORT.md").read_text(encoding="utf-8")
print("OK")
