from typing import List, Dict, Tuple
import os, json, glob
import numpy as np
from .providers import HuggingFaceProvider
from .monitor import log_usage
from .config import OPENAI_EMBED_MODEL

def _chunk_text(text: str, chunk_size=1200, overlap=200) -> List[str]:
    chunks, i = [], 0
    while i < len(text):
        chunks.append(text[i:i+chunk_size])
        i += chunk_size - overlap
    return chunks

class SimpleDocStore:
    def _init_(self, index_dir="data/index", embed_model: str = OPENAI_EMBED_MODEL):
        self.index_dir = index_dir
        os.makedirs(self.index_dir, exist_ok=True)
        self.meta_path = os.path.join(self.index_dir, "meta.json")
        self.vec_path = os.path.join(self.index_dir, "vectors.npy")
        self.embed_model = embed_model
        self._provider = HuggingFaceProvider()

def ingest_folder(self, folder: str) -> int:
    texts: List[str] = []
    metas: List[Dict] = []
    # دعم اسم بديل ingest()
    def ingest(self, folder: str) -> int:
        return self.ingest_folder(folder)

    folder = os.path.abspath(folder)  # ثبّتي المسار
    for root, _, files in os.walk(folder):
        for fname in files:
            lower = fname.lower()
            if not (lower.endswith(".txt") or lower.endswith(".md")):
                continue
            path = os.path.join(root, fname)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    raw = f.read()
            except Exception as e:
                # تجاهلي أي ملف مش قابل للقراءة
                continue
            for j, ch in enumerate(_chunk_text(raw)):
                texts.append(ch)
                metas.append({"source": path, "chunk": j})

    if not texts:
        raise RuntimeError(f"لم يتم العثور على نصوص .txt/.md داخل: {folder}")

    vecs = self._provider.embed(texts)  # ndarray [N, D]
    np.save(self.vec_path, vecs)
    with open(self.meta_path, "w", encoding="utf-8") as f:
        json.dump({"texts": texts, "metas": metas}, f, ensure_ascii=False)
    return len(texts)

    def _load(self) -> Tuple[np.ndarray, Dict]:
        if not (os.path.exists(self.vec_path) and os.path.exists(self.meta_path)):
            raise RuntimeError("لا يوجد فهرس. شغّلي ingest أولًا.")
        vecs = np.load(self.vec_path)
        with open(self.meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
        return vecs, meta

    def search(self, query: str, k: int = 5):
        vecs, meta = self._load()
        qv = self._provider.embed([query], model=self.embed_model)[0]
        sims = (vecs @ qv) / ((np.linalg.norm(vecs, axis=1)*(np.linalg.norm(qv)+1e-9))+1e-9)
        idxs = np.argsort(-sims)[:k]
        out = []
        for i in idxs:
            i = int(i)
            out.append({"text": meta["texts"][i], "meta": meta["metas"][i], "score": float(sims[i])})
        return out