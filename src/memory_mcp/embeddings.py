"""Embeddings sémantiques multilingues (fastembed ONNX — léger, offline, CI-friendly)."""

from __future__ import annotations

import json
import math
import os
from functools import lru_cache

MODEL_NAME = os.environ.get(
    "MEMBRIDGE_EMBED_MODEL",
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
)


@lru_cache(maxsize=1)
def _get_model():
    from fastembed import TextEmbedding

    return TextEmbedding(model_name=MODEL_NAME)


def embed_text(text: str) -> list[float]:
    """Vecteur dense normalisé pour une phrase."""
    text = text.strip()
    if not text:
        return []
    model = _get_model()
    vector = next(model.embed([text]))
    return _normalize(vector.tolist())


def embed_batch(texts: list[str]) -> list[list[float]]:
    model = _get_model()
    cleaned = [t.strip() for t in texts]
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
        # Compat ancien format bag-of-words — score nul en pratique
        return []
    return data
