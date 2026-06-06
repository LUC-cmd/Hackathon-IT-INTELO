"""Agent de démo MemBridge — conversation longue + questions pièges + bonus."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from memory_mcp.stats import reset_stats
from memory_mcp.tools import MemoryTools
from memory_mcp.validation import top1_contains

ROOT = Path(__file__).parent.parent
CONVERSATION = ROOT / "benchmark" / "conversation.json"
TRAPS = ROOT / "benchmark" / "trap_questions.json"


def _extend_conversation(base: list[dict], target: int = 50) -> list[dict]:
    turns = list(base)
    n = len(turns) + 1
    roles = ("user", "assistant")
    while len(turns) < target:
        role = roles[(n - 1) % 2]
        turns.append(
            {
                "turn": n,
                "role": role,
                "content": f"Échange {n} — suivi dossier TechCorp, tour {n}.",
            }
        )
        n += 1
    return turns


def run_demo(session: str = "demo", turns_count: int = 50) -> dict:
    """Joue une conversation complète et évalue les questions pièges."""
    reset_stats()
    tools = MemoryTools()
    base = json.loads(CONVERSATION.read_text(encoding="utf-8"))
    turns = _extend_conversation(base, target=turns_count)

    print(f"\n{'=' * 60}")
    print(f"  MemBridge LIVE DEMO — session: {session}")
    print(f"{'=' * 60}\n")

    for turn in turns:
        tag = "fact" if turn["turn"] <= 10 else turn["role"]
        tools.memory_store(
            content=f"{turn['role']}: {turn['content']}",
            tags=[tag],
            session=session,
            turn=turn["turn"],
        )
        if turn["turn"] % 10 == 0:
            print(f"  ✓ Tour {turn['turn']}/{turns_count} stocké")

    # Bonus : géolocalisation + transcription
    tools.memory_locate(session, 6.1319, 1.2228, label="Lomé — siège TechCorp", turn=51)
    tools.memory_transcribe(
        session,
        "Cliente confirme l'écart de facturation et le bug iOS du 12 février.",
        source="call",
        language="fr",
        turn=52,
    )

    summary = tools.memory_summarize(session=session)
    stats = tools.memory_stats()

    traps = json.loads(TRAPS.read_text(encoding="utf-8"))
    passed = 0
    print(f"\n{'─' * 60}")
    print("  QUESTIONS PIÈGES")
    print(f"{'─' * 60}")
    for trap in traps[:5]:
        result = tools.memory_search(trap["query"], top_k=1, session=session)
        ok = top1_contains(trap["expected"], result["results"])
        passed += int(ok)
        icon = "✓" if ok else "✗"
        score = result["results"][0]["score"] if result["results"] else 0
        print(f"  {icon} [{score:.3f}] {trap['query']}")
        print(f"      → attendu: {trap['expected']}")

    print(f"\n{'─' * 60}")
    print(f"  RÉSUMÉ ({summary['compressed_chars']} chars / {summary['source_turns']} tours)")
    print(f"{'─' * 60}")
    print(f"  {summary['summary'][:300]}...")
    print(f"\n  Qualité pièges : {passed}/5")
    print(f"  Stats tokens   : {json.dumps(stats, indent=2)}")

    return {"summary": summary, "stats": stats, "traps_passed": passed}


def run_llm_demo() -> None:
    """Optionnel : branchement OpenAI si OPENAI_API_KEY est défini."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("\n  ℹ OPENAI_API_KEY non défini — démo locale uniquement.")
        return
    try:
        import httpx

        tools = MemoryTools()
        summary = tools.memory_summarize(session="demo")
        context = summary["summary"]
        prompt = (
            f"Contexte mémoire compressé:\n{context}\n\n"
            "Question: Quel est le contrat de Marie Dupont?"
        )
        resp = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 100,
            },
            timeout=30,
        )
        answer = resp.json()["choices"][0]["message"]["content"]
        print(f"\n  🤖 Réponse LLM (via mémoire compressée) : {answer}")
    except Exception as exc:
        print(f"\n  ⚠ Appel LLM échoué : {exc}")


def main() -> None:
    run_demo()
    if "--llm" in sys.argv:
        run_llm_demo()


if __name__ == "__main__":
    main()
