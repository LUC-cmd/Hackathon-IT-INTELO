"""Harnais de benchmark : naïf vs MemBridge + qualité + rapport JSON."""

from __future__ import annotations

import json
from pathlib import Path

from benchmark.insights import generate_insights
from benchmark.naive import simulate_naive_conversation
from benchmark.scoring import compression_ratio, context_growth_factor, per_turn_context_tokens
from memory_mcp.stats import reset_stats
from memory_mcp.tools import MemoryTools
from memory_mcp.validation import top1_contains

ROOT = Path(__file__).parent
CONVERSATION_PATH = ROOT / "conversation.json"
TRAP_QUESTIONS_PATH = ROOT / "trap_questions.json"
RESULTS_DIR = ROOT / "results"
REPORT_PATH = RESULTS_DIR / "report.json"

TOKEN_COST_PER_MILLION = 0.15  # € indicatif gpt-4o-mini input


def load_json(path: Path) -> list | dict:
    return json.loads(path.read_text(encoding="utf-8"))


def generate_long_conversation(base_turns: list[dict], target_turns: int = 40) -> list[dict]:
    turns = list(base_turns)
    turn_num = len(turns) + 1
    roles = ("user", "assistant")
    while len(turns) < target_turns:
        role = roles[(turn_num - 1) % 2]
        turns.append(
            {
                "turn": turn_num,
                "role": role,
                "content": f"Échange {turn_num} — précision contextuelle pour le tour {turn_num}.",
            }
        )
        turn_num += 1
    return turns


def _seed_trap_session(tools: MemoryTools, session: str) -> None:
    facts = [
        (1, "user: Bonjour, je suis Marie Dupont, cliente premium chez TechCorp."),
        (3, "user: Mon numéro de contrat est CTR-2024-8847."),
        (5, "user: La facture de mars devrait être 99,90 € mais affiche 149,90 €."),
        (7, "user: Bug mobile signalé le 12 février sur l'application iOS."),
        (9, "user: Email de contact : marie.dupont@email.fr."),
    ]
    for turn, content in facts:
        tools.memory_store(content, tags=["fact"], session=session, turn=turn)
    noise_topics = [
        "météo Paris 18°C vent faible",
        "recette tarte aux pommes sans gluten",
        "match PSG 2-1 fin de saison",
        "taux change EUR USD 1.08",
        "sortie cinéma blockbuster mars",
    ]
    for i in range(25):
        topic = noise_topics[i % len(noise_topics)]
        tools.memory_store(
            f"assistant: hors-sujet tour {i} — {topic} — bruit sémantique {i * 17}",
            tags=["noise"],
            session=session,
            turn=100 + i,
        )


def evaluate_trap_questions(tools: MemoryTools, session: str) -> dict:
    traps = load_json(TRAP_QUESTIONS_PATH)
    passed = 0
    details: list[dict] = []
    for trap in traps:
        result = tools.memory_search(trap["query"], top_k=1, session=session)
        ok = top1_contains(trap["expected"], result["results"])
        if ok:
            passed += 1
        details.append(
            {
                "query": trap["query"],
                "expected": trap["expected"],
                "passed": ok,
                "score": result["results"][0]["score"] if result["results"] else 0,
            }
        )
    total = len(traps)
    return {
        "passed": passed,
        "total": total,
        "score_pct": round(100 * passed / total, 1) if total else 0,
        "details": details,
    }


def simulate_memory_conversation(turns: list[dict], session: str = "benchmark") -> dict:
    reset_stats()
    tools = MemoryTools()
    total_context_tokens = 0
    per_turn: list[int] = []

    for turn in turns:
        role = turn["role"]
        content = turn["content"]
        tools.memory_store(
            content=f"{role}: {content}",
            tags=[role, f"turn-{turn['turn']}"],
            session=session,
            turn=turn["turn"],
        )
        tokens = per_turn_context_tokens(tools, session, content)
        total_context_tokens += tokens
        per_turn.append(tokens)

    stats = tools.memory_stats()
    return {
        "mode": "memory",
        "turns": len(turns),
        "total_tokens": total_context_tokens,
        "per_turn_tokens": per_turn,
        "growth_factor": context_growth_factor(per_turn) if per_turn else 0.0,
        "compression_ratio": compression_ratio(tools, session),
        "stats": stats,
    }


def run_benchmark(turn_count: int = 50) -> dict:
    base = load_json(CONVERSATION_PATH)
    turns = generate_long_conversation(base, target_turns=turn_count)
    naive = simulate_naive_conversation(turns)
    memory = simulate_memory_conversation(turns)

    savings_pct = 0.0
    if naive["total_tokens"] > 0:
        savings_pct = round(100 * (1 - memory["total_tokens"] / naive["total_tokens"]), 1)

    tokens_saved = naive["total_tokens"] - memory["total_tokens"]
    euros_saved = round(tokens_saved * TOKEN_COST_PER_MILLION / 1_000_000, 4)

    reset_stats()
    quality_tools = MemoryTools()
    _seed_trap_session(quality_tools, "quality-eval")
    quality = evaluate_trap_questions(quality_tools, "quality-eval")

    report = {
        "naive": naive,
        "memory": memory,
        "savings_pct": savings_pct,
        "tokens_saved": tokens_saved,
        "euros_saved": euros_saved,
        "quality": quality,
        "turn_count": turn_count,
        "note": "MemBridge — benchmark rejouable pour démo jury",
    }

    # Ajouter insights automatiques
    report["insights"] = generate_insights(report)

    return report


def save_report(report: dict, path: Path = REPORT_PATH) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def main() -> None:
    report = run_benchmark()
    save_report(report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"\n✓ Rapport sauvegardé : {REPORT_PATH}")


if __name__ == "__main__":
    main()
