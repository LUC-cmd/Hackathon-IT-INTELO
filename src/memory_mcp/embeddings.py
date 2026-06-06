"""Embeddings sémantiques multilingues (fastembed ONNX — léger, offline, CI-friendly)."""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
from functools import lru_cache

MODEL_NAME = os.environ.get(
    "MEMBRIDGE_EMBED_MODEL",
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
)
_FALLBACK_DIM = 384


@lru_cache(maxsize=1)
def _get_model():
    try:
        from fastembed import TextEmbedding

        return TextEmbedding(model_name=MODEL_NAME)
    except Exception:
        return None


def _hash_embed(text: str) -> list[float]:
    """Fallback déterministe si fastembed indisponible (rate-limit CI)."""
    tokens = re.findall(r"\w+", text.lower())
    vec = [0.0] * _FALLBACK_DIM
    for token in tokens:
        digest = hashlib.sha256(token.encode()).digest()
        for i in range(0, len(digest), 2):
            idx = int.from_bytes(digest[i : i + 2], "big") % _FALLBACK_DIM
            vec[idx] += 1.0
    return _normalize(vec)


def embed_text(text: str) -> list[float]:
    """Vecteur dense normalisé pour une phrase."""
    text = text.strip()
    if not text:
        return []
    model = _get_model()
    if model is None:
        return _hash_embed(text)
    vector = next(model.embed([text]))
    return _normalize(vector.tolist())


def embed_batch(texts: list[str]) -> list[list[float]]:
    model = _get_model()
    cleaned = [t.strip() for t in texts]
    if model is None:
        return [_hash_embed(t) for t in cleaned]
    return [_normalize(v.tolist()) for v in model.embed(cleaned)]


def _normalize(vec: list[float]) -> list[float]:
    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [x / norm for x in vec]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    return sum(x * y for x, y in zip(a, b, strict=True))


def serialize_embedding(vec: list[float]) -> str:
    return json.dumps(vec)


def deserialize_embedding(raw: str) -> list[float]:
    data = json.loads(raw)
    if isinstance(data, dict):
        return []
    return data
