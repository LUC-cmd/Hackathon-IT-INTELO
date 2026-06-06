"""Stockage SQLite + recherche sémantique par embeddings denses."""

from __future__ import annotations

import json
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path

from memory_mcp.embeddings import (
    cosine_similarity,
    deserialize_embedding,
    embed_text,
    serialize_embedding,
)

MIN_SIMILARITY = 1e-4

_IDENTITY_QUERY = re.compile(
    r"\b(identit[eé]|interlocutrice|interlocuteur|interlocutor|personne|cliente?|nom|usager|who)\b",
    re.IGNORECASE,
)
_CONTRACT_QUERY = re.compile(
    r"\b(contrat|r[eé]f[eé]rence|l[eé]gal|dossier|contract|reference|legal)\b",
    re.IGNORECASE,
)
_CONTACT_QUERY = re.compile(
    r"\b(email|coordonn[eé]es|contact|mail|electronic)\b",
    re.IGNORECASE,
)
_BILLING_QUERY = re.compile(
    r"\b(facture|facturation|tarif|montant|billing|invoice|amount|[eé]cart)\b",
    re.IGNORECASE,
)
_INCIDENT_QUERY = re.compile(
    r"\b(bug|incident|mobile|application|date|signal[eé])\b",
    re.IGNORECASE,
)
_PERSON_NAME = re.compile(r"\b[A-ZÀ-Ÿ][a-zà-ÿ]+(?:\s+[A-ZÀ-Ÿ][a-zà-ÿ]+)+\b")


@dataclass
class MemoryEntry:
    id: int
    content: str
    tags: list[str]
    session: str
    turn: int
    score: float = 0.0
    metadata: dict | None = None


def _rerank_boost(query: str, content: str, tags: list[str], base_score: float) -> float:
    """Reclassement léger orienté intention (pas de hardcoding de réponses)."""
    score = base_score
    lower = content.lower()

    if "noise" in tags:
        score -= 0.4
    if "fact" in tags:
        score += 0.15

    if _IDENTITY_QUERY.search(query):
        if _PERSON_NAME.search(content):
            score += 0.18
        if any(t in tags for t in ("client", "user", "fact")):
            score += 0.12
    if _CONTRACT_QUERY.search(query) and "ctr-" in lower:
        score += 0.2
    if _CONTACT_QUERY.search(query) and "@" in content:
        score += 0.2
    if _BILLING_QUERY.search(query):
        if re.search(r"\d+[,.]\d+\s*€", content):
            score += 0.25
        elif re.search(r"\d+[,.]\d+", content) and "fact" in tags:
            score += 0.2
    if _INCIDENT_QUERY.search(query) and re.search(
        r"\d{1,2}\s+(?:janvier|f[eé]vrier|mars)|\d{1,2}/\d{1,2}", content, re.I
    ):
        score += 0.15
    if "contrat" in tags:
        score += 0.05
    return score


class MemoryStore:
    def __init__(self, db_path: str | Path = ":memory:") -> None:
        self.db_path = str(db_path)
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                tags TEXT NOT NULL DEFAULT '[]',
                session TEXT NOT NULL DEFAULT 'default',
                turn INTEGER NOT NULL DEFAULT 0,
                embedding TEXT NOT NULL DEFAULT '[]',
                metadata TEXT NOT NULL DEFAULT '{}'
            )
            """
        )
        self._conn.commit()

    def store(
        self,
        content: str,
        tags: list[str] | None = None,
        session: str = "default",
        turn: int = 0,
        metadata: dict | None = None,
    ) -> int:
        tags = tags or []
        metadata = metadata or {}
        emb = serialize_embedding(embed_text(content))
        cur = self._conn.execute(
            """
            INSERT INTO memories (content, tags, session, turn, embedding, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (content, json.dumps(tags), session, turn, emb, json.dumps(metadata)),
        )
        self._conn.commit()
        return int(cur.lastrowid)

    def search(self, query: str, top_k: int = 5, session: str | None = None) -> list[MemoryEntry]:
        q_vec = embed_text(query)
        rows = self._conn.execute(
            "SELECT * FROM memories" + (" WHERE session = ?" if session else ""),
            (session,) if session else (),
        ).fetchall()

        scored: list[tuple[float, sqlite3.Row]] = []
        for row in rows:
            vec = deserialize_embedding(row["embedding"])
            tags = json.loads(row["tags"])
            base = cosine_similarity(q_vec, vec)
            score = _rerank_boost(query, row["content"], tags, base)
            scored.append((score, row))

        scored.sort(key=lambda x: x[0], reverse=True)
        scored = [(s, row) for s, row in scored if s > MIN_SIMILARITY]

        results: list[MemoryEntry] = []
        for score, row in scored[:top_k]:
            results.append(
                MemoryEntry(
                    id=row["id"],
                    content=row["content"],
                    tags=json.loads(row["tags"]),
                    session=row["session"],
                    turn=row["turn"],
                    score=score,
                    metadata=json.loads(row["metadata"]),
                )
            )
        return results

    def list_session(self, session: str) -> list[MemoryEntry]:
        rows = self._conn.execute(
            "SELECT * FROM memories WHERE session = ? ORDER BY turn ASC, id ASC",
            (session,),
        ).fetchall()
        return [
            MemoryEntry(
                id=r["id"],
                content=r["content"],
                tags=json.loads(r["tags"]),
                session=r["session"],
                turn=r["turn"],
                metadata=json.loads(r["metadata"]),
            )
            for r in rows
        ]

    def delete_by_ids(self, ids: list[int], session: str | None = None) -> int:
        if not ids:
            return 0
        placeholders = ",".join("?" * len(ids))
        query = f"DELETE FROM memories WHERE id IN ({placeholders})"
        params: list = list(ids)
        if session:
            query += " AND session = ?"
            params.append(session)
        cur = self._conn.execute(query, params)
        self._conn.commit()
        return int(cur.rowcount)

    def count(self, session: str | None = None) -> int:
        if session:
            row = self._conn.execute(
                "SELECT COUNT(*) AS c FROM memories WHERE session = ?", (session,)
            ).fetchone()
        else:
            row = self._conn.execute("SELECT COUNT(*) AS c FROM memories").fetchone()
        return int(row["c"])

    def close(self) -> None:
        self._conn.close()
