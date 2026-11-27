"""Offline test of hosted models (src/llm_api.py) against a fake OpenAI-compatible server on localhost (no internet, no key).
Checks the request (model id, one user message = the prompt, temperature, max_tokens = the token cap, bearer key), the retry on
HTTP 429, finish_reason 'length' -> hit_token_cap, removal of <think> blocks, usage accounting in the run JSON, the results folder
name, the pre-flight check and the error messages.   Usage: python tests/test_llm_api.py"""
import sys, io, os, re, json, argparse, contextlib, tempfile, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tests")); os.chdir(ROOT)
sys.modules["sentence_transformers"] = None
from fakes import HashEmb
from src.llm_api import split_model, check_api, call_api
from src.pipeline_adv import run

SEEN, STATE = [], {"429_sent": False}


class Fake(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        SEEN.append({"path": self.path, "auth": self.headers.get("Authorization"), "body": body})
        if body["model"] == "no-such/model":
            return self._send(404, {"error": "model not found"})
        if not STATE["429_sent"]:
            STATE["429_sent"] = True
            return self._send(429, {"error": "rate limited"}, {"Retry-After": "0"})
        prompt = body["messages"][0]["content"]
        sec = re.search(r"SECTION: (.+)\n", prompt)
        name = sec.group(1).strip() if sec else "summary"
        text = ("1. Not established from the available artifacts.\n2. Not established from the available artifacts."
                if "Questions" in name else "- Not established from the available artifacts.")
        self._send(200, {"choices": [{"message": {"role": "assistant", "content": f"<think>private reasoning</think>\n{text}"},
                                      "finish_reason": "length" if name.startswith("Detection") else "stop"}],
                         "usage": {"prompt_tokens": len(prompt) // 4, "completion_tokens": 12, "estimated_cost": 0.0001}})

    def _send(self, code, obj, headers=None):
        data = json.dumps(obj).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(data)))
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers(); self.wfile.write(data)


srv = ThreadingHTTPServer(("127.0.0.1", 0), Fake); threading.Thread(target=srv.serve_forever, daemon=True).start()
os.environ.update(DEEPINFRA_BASE_URL=f"http://127.0.0.1:{srv.server_port}", DEEPINFRA_API_KEY="test-key",
                  NO_PROXY="127.0.0.1,localhost", no_proxy="127.0.0.1,localhost")
MODEL = "deepinfra:test-org/test-model"

assert split_model("llama3.2:3b") == (None, "llama3.2:3b") and split_model(MODEL) == ("deepinfra", "test-org/test-model")
assert split_model("qwen2.5:7b-instruct")[0] is None
with tempfile.TemporaryDirectory() as tmp:
    a = argparse.Namespace(input="dataset/paper_dataset/koi_stealer/rag_input.json", model=MODEL, results_dir=tmp, dry_run=False, strict=False,
                           annotate=False, no_enrich=False, sections=None, no_postprocess=False, llm_timeline=False)
    with contextlib.redirect_stdout(io.StringIO()):
        report = run(a, embedder=HashEmb(), reranker=None)        # real call_llm -> call_api path (no llm= stand-in)
    out = Path(tmp) / "koi_stealer" / "deepinfra_test-org_test-model"
    j = json.loads((out / "advanced_run_report.json").read_text(encoding="utf-8"))
    u = j["llm_usage"]; calls = [s for s in SEEN if s["body"]["model"] == "test-org/test-model"]
    print("folder:", out.name, "| usage:", u, "| requests:", len(calls))
    assert u["provider"] == "deepinfra" and u["calls"] == len(calls) - 1 and u["retries"] == 1      # one 429 was retried
    assert u["prompt_tokens"] > 1000 and u["completion_tokens"] == 12 * u["calls"] and abs(u["estimated_cost_usd"] - 0.0001 * u["calls"]) < 1e-9
    assert all(c["auth"] == "Bearer test-key" and c["path"] == "/chat/completions" for c in calls)
    assert all(len(c["body"]["messages"]) == 1 and c["body"]["messages"][0]["role"] == "user" and c["body"]["temperature"] == 0.1 for c in calls)
    assert {c["body"]["max_tokens"] for c in calls} == {600, 900}, "max_tokens = num_predict / num_predict_long"
    assert "<think>" not in report and "private reasoning" not in report
    det = next(e for e in j["run_log"] if e["section"].startswith("Detection"))
    assert det["truncated"] is True and next(e for e in j["run_log"] if e["section"].startswith("Affected"))["truncated"] is False
    assert "evaluation" in j
    # no-RAG through the API (its package pre-flight is skipped here: this test needs no sentence-transformers)
    import src.no_rag as nr
    nr.preflight = lambda *x, **k: None
    n0 = len(SEEN)
    with contextlib.redirect_stdout(io.StringIO()):
        nr.run_no_rag(argparse.Namespace(input=a.input, model=MODEL, results_dir=tmp))
    nj = json.loads((out / "no_rag_run_report.json").read_text(encoding="utf-8"))
    print("no-RAG usage:", nj["llm_usage"])
    assert nj["llm_usage"]["calls"] == len(SEEN) - n0 and "evaluation" in nj and "<think>" not in (out / "no_rag_postmortem.md").read_text(encoding="utf-8")
# pre-flight and error messages (no key is ever printed)
assert check_api(MODEL) == []
os.environ.pop("DEEPINFRA_API_KEY")
msg = check_api(MODEL)[0]; print("missing key ->", msg)
assert "DEEPINFRA_API_KEY" in msg
os.environ["DEEPINFRA_API_KEY"] = "test-key"
try:
    call_api("x", "deepinfra:no-such/model", 0.1, 10, 5, retries=0); raise AssertionError("must fail")
except RuntimeError as exc:
    print("unknown model ->", str(exc)[:110]); assert "deepinfra.com/models" in str(exc) and "test-key" not in str(exc)
srv.shutdown()
print("OK")
