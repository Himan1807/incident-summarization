"""Stand-ins shared by the offline tests (no Ollama, no model downloads)."""
import re
import zlib

import numpy as np


class HashEmb:
    """Deterministic stand-in for the sentence-transformers embedder: hashed bag of words, 512 dims, L2-normalised."""
    def encode(self, texts, **k):
        out = []
        for t in texts:
            v = np.zeros(512)
            for w in re.findall(r"[\w.\-]+", t.lower()): v[zlib.crc32(w.encode()) % 512] += 1
            out.append(v / (np.linalg.norm(v) + 1e-9))
        return np.array(out)
