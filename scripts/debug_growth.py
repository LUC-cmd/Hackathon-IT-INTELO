from benchmark.harness import CONVERSATION_PATH, generate_long_conversation, load_json
from benchmark.scoring import context_growth_factor, per_turn_context_tokens
from memory_mcp.stats import reset_stats
from memory_mcp.tools import MemoryTools

reset_stats()
tools = MemoryTools()
turns = generate_long_conversation(load_json(CONVERSATION_PATH), target_turns=50)
per_turn = []
for turn in turns:
    tools.memory_store(
        f"{turn['role']}: {turn['content']}",
        session="plateau",
        turn=turn["turn"],
    )
    t = per_turn_context_tokens(tools, "plateau", turn["content"])
    per_turn.append(t)
    if turn["turn"] in (1, 10, 25, 40, 50):
        s = tools.memory_summarize(session="plateau")
        print(f"t{turn['turn']}: ctx={t} summary_len={len(s['summary'])}")

print("factor", context_growth_factor(per_turn))
