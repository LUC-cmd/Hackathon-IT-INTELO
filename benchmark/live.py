"""Benchmark live tour-par-tour — SSE pour démo jury."""

from __future__ import annotations

import json
from collections.abc import Iterator

from benchmark.harness import CONVERSATION_PATH, generate_long_conversation, load_json
from benchmark.naive import build_naive_context
from benchmark.scoring import per_turn_context_tokens
from memory_mcp.stats import reset_stats
from memory_mcp.tools import MemoryTools


def stream_benchmark(turn_count: int = 50) -> Iterator[str]:
    """Génère des événements SSE tour par tour."""
    base = load_json(CONVERSATION_PATH)
    turns = generate_long_conversation(base, target_turns=turn_count)

    reset_stats()
    tools = MemoryTools()
    history: list[dict] = []
    naive_cumul = 0
    memory_cumul = 0
    savings = 0.0

    yield _evt("start", {"turns": turn_count, "message": "Benchmark live démarré"})

    for turn in turns:
        role = turn["role"]
        content = turn["content"]
        history.append({"role": role, "content": content})

        _, naive_tok = build_naive_context(history)
        naive_cumul += naive_tok

        tools.memory_store(
            content=f"{role}: {content}",
            tags=[role, f"turn-{turn['turn']}"],
            session="live-stream",
            turn=turn["turn"],
        )
        mem_tok = per_turn_context_tokens(tools, "live-stream", content)
        memory_cumul += mem_tok
        savings = round(100 * (1 - memory_cumul / max(naive_cumul, 1)), 1)

        yield _evt(
            "turn",
            {
                "turn": turn["turn"],
                "naive_turn": naive_tok,
                "memory_turn": mem_tok,
                "naive_cumul": naive_cumul,
                "memory_cumul": memory_cumul,
                "savings_pct": savings,
            },
        )

    yield _evt(
        "done",
        {
            "naive_cumul": naive_cumul,
            "memory_cumul": memory_cumul,
            "savings_pct": savings,
        },
    )


def _evt(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"
