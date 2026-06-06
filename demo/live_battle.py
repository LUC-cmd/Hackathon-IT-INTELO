"""Battle live terminal — démo jury en console animée."""

from __future__ import annotations

import sys
import time

from benchmark.harness import CONVERSATION_PATH, generate_long_conversation, load_json
from benchmark.naive import build_naive_context
from benchmark.scoring import per_turn_context_tokens
from memory_mcp.stats import reset_stats
from memory_mcp.tools import MemoryTools

RUST = "\033[38;5;167m"
MOSS = "\033[38;5;65m"
AMBER = "\033[38;5;172m"
RESET = "\033[0m"
BOLD = "\033[1m"


def bar(value: int, max_val: int, width: int = 30, color: str = RUST) -> str:
    filled = int(width * min(value / max(max_val, 1), 1))
    return f"{color}{'█' * filled}{'░' * (width - filled)}{RESET}"


def run_battle(turn_count: int = 50, delay: float = 0.08) -> None:
    base = load_json(CONVERSATION_PATH)
    turns = generate_long_conversation(base, target_turns=turn_count)
    reset_stats()
    tools = MemoryTools()
    history: list[dict] = []
    naive_cumul = memory_cumul = 0

    print(f"\n{BOLD}═══ MemBridge BATTLE LIVE ═══{RESET}\n")

    for turn in turns:
        history.append({"role": turn["role"], "content": turn["content"]})
        _, naive_tok = build_naive_context(history)
        naive_cumul += naive_tok
        tools.memory_store(
            f"{turn['role']}: {turn['content']}",
            tags=[turn["role"]],
            session="terminal-battle",
            turn=turn["turn"],
        )
        mem_tok = per_turn_context_tokens(tools, "terminal-battle", turn["content"])
        memory_cumul += mem_tok
        savings = round(100 * (1 - memory_cumul / max(naive_cumul, 1)), 1)

        sys.stdout.write("\033[H\033[J")
        hdr = f"{BOLD}Tour {turn['turn']}/{turn_count}{RESET} · {AMBER}{savings}%{RESET}"
        print(f"{hdr}\n")
        print(f"{RUST}NAÏF {naive_cumul:>6}{RESET} {bar(naive_cumul, naive_cumul, color=RUST)}")
        print(f"{MOSS}MCP  {memory_cumul:>6}{RESET} {bar(memory_cumul, naive_cumul, color=MOSS)}")
        print()
        if turn["turn"] == turn_count:
            print(f"{BOLD}{MOSS}✓ VICTOIRE — {savings}% tokens économisés{RESET}")
        sys.stdout.flush()
        time.sleep(delay)


if __name__ == "__main__":
    run_battle()
