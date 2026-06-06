"""Implémentation des outils MCP : store, search, summarize, stats + bonus."""

from __future__ import annotations

from memory_mcp.stats import count_tokens, get_stats
from memory_mcp.storage import MemoryStore
from memory_mcp.summarize import build_summary


class MemoryTools:
    def __init__(self, store: MemoryStore | None = None) -> None:
        self.store = store or MemoryStore()
        self._session_digest: dict[str, str] = {}

    def memory_store(
        self,
        content: str,
        tags: list[str] | None = None,
        session: str = "default",
        turn: int = 0,
        metadata: dict | None = None,
    ) -> dict:
        stats = get_stats()
        stats.store_calls += 1
        stats.add_input(count_tokens(content))

        memory_id = self.store.store(
            content=content, tags=tags, session=session, turn=turn, metadata=metadata
        )
        entries = self.store.list_session(session)
        self._session_digest[session] = build_summary(entries, max_chars=320)
        return {"id": memory_id, "stored": True, "tags": tags or [], "metadata": metadata or {}}

    def memory_search(self, query: str, top_k: int = 5, session: str | None = None) -> dict:
        stats = get_stats()
        stats.search_calls += 1
        stats.add_input(count_tokens(query))

        hits = self.store.search(query=query, top_k=top_k, session=session)
        results = [
            {
                "id": h.id,
                "content": h.content,
                "tags": h.tags,
                "turn": h.turn,
                "score": round(h.score, 6),
                "metadata": h.metadata or {},
            }
            for h in hits
        ]
        stats.add_output(count_tokens(str(results)))
        return {"results": results, "count": len(results)}

    def memory_summarize(self, session: str = "default", max_chars: int = 500) -> dict:
        stats = get_stats()
        stats.summarize_calls += 1

        entries = self.store.list_session(session)
        if not entries:
            return {"summary": "", "source_turns": 0, "compressed_chars": 0}

        digest = self._session_digest.get(session, "")
        if not digest:
            digest = build_summary(entries, max_chars=max_chars)
            self._session_digest[session] = digest

        summary = digest[:max_chars]
        if len(summary) > max_chars:
            summary = summary[: max_chars - 3] + "..."

        stats.add_input(count_tokens("".join(e.content for e in entries)))
        stats.add_output(count_tokens(summary))
        return {
            "summary": summary,
            "source_turns": len(entries),
            "compressed_chars": len(summary),
        }

    def memory_stats(self) -> dict:
        return get_stats().to_dict()

    # --- Bonus hackathon (différenciation jury) ---

    def memory_forget(
        self, session: str, query: str | None = None, tag: str | None = None, top_k: int = 5
    ) -> dict:
        """Oubli intelligent : purge souvenirs obsolètes ou redondants."""
        if query:
            hits = self.store.search(query=query, top_k=top_k, session=session)
            ids = [h.id for h in hits if "fact" not in h.tags]
        else:
            entries = self.store.list_session(session)
            ids = [e.id for e in entries if tag and tag in e.tags]
        removed = self.store.delete_by_ids(ids, session=session)
        self._session_digest.pop(session, None)
        return {"removed": removed, "session": session}

    def memory_locate(
        self,
        session: str,
        latitude: float,
        longitude: float,
        label: str = "",
        turn: int = 0,
    ) -> dict:
        """Mémorise un contexte géographique (support terrain, livraison, incident)."""
        content = f"Localisation {label or 'point'} : {latitude:.5f}, {longitude:.5f}"
        return self.memory_store(
            content=content,
            tags=["geo", "location"],
            session=session,
            turn=turn,
            metadata={"lat": latitude, "lon": longitude, "label": label},
        )

    def memory_transcribe(
        self,
        session: str,
        transcript: str,
        source: str = "audio",
        language: str = "fr",
        turn: int = 0,
    ) -> dict:
        """Stocke une transcription audio/vidéo dans la mémoire partagée."""
        prefix = {"audio": "🎙️", "video": "🎬", "call": "📞"}.get(source, "📝")
        content = f"{prefix} Transcription ({language}) : {transcript}"
        return self.memory_store(
            content=content,
            tags=["transcript", source, language],
            session=session,
            turn=turn,
            metadata={"source": source, "language": language},
        )

    def memory_translate(self, text: str, target_lang: str = "en") -> dict:
        """Traduction légère FR↔EN pour agents multilingues (offline, sans API)."""
        pairs = {
            ("bonjour", "en"): "hello",
            ("cliente premium", "en"): "premium customer",
            ("facture", "en"): "invoice",
            ("contrat", "en"): "contract",
            ("bug mobile", "en"): "mobile bug",
            ("email de contact", "en"): "contact email",
            ("hello", "fr"): "bonjour",
            ("premium customer", "fr"): "cliente premium",
            ("invoice", "fr"): "facture",
            ("contract", "fr"): "contrat",
            ("mobile bug", "fr"): "bug mobile",
            ("contact email", "fr"): "email de contact",
        }
        lower = text.lower()
        translated = text
        for (src, lang), dst in pairs.items():
            if lang == target_lang and src in lower:
                translated = translated.replace(src, dst).replace(src.title(), dst.title())
        return {"original": text, "translated": translated, "target_lang": target_lang}

    def memory_share(self, from_session: str, to_session: str, query: str, top_k: int = 3) -> dict:
        """Mémoire partagée : un agent lit les souvenirs d'un autre agent."""
        hits = self.store.search(query=query, top_k=top_k, session=from_session)
        shared = []
        for hit in hits:
            memory_id = self.store.store(
                content=hit.content,
                tags=[*hit.tags, "shared", f"from-{from_session}"],
                session=to_session,
                turn=hit.turn,
                metadata={"shared_from": from_session, "original_id": hit.id},
            )
            shared.append({"id": memory_id, "content": hit.content, "score": hit.score})
        return {"from": from_session, "to": to_session, "shared": shared, "count": len(shared)}

    def memory_timeline(self, session: str = "default") -> dict:
        """Chronologie visuelle des souvenirs (fait, géo, média, message)."""
        entries = self.store.list_session(session)

        def _type(tags: list[str]) -> str:
            if "fact" in tags:
                return "fact"
            if "geo" in tags or "location" in tags:
                return "geo"
            if any(t in tags for t in ("audio", "video", "call", "transcript", "vision", "image")):
                return "media"
            return "message"

        events = [
            {
                "turn": e.turn,
                "type": _type(e.tags),
                "preview": e.content[:80],
                "tags": e.tags,
            }
            for e in entries
        ]
        return {"session": session, "events": events, "count": len(events)}
