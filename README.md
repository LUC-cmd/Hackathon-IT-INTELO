# MemBridge — Memory MCP Challenge

**Équipe : [LUC-cmd](https://github.com/LUC-cmd)** · **Hackathon INTELO2026 · Lomé**

> Serveur MCP de mémoire partagée — réduit les tokens **sans amnésie**.

## Résultats mesurés (benchmark)

| Métrique | Résultat |
|----------|----------|
| **Économie tokens** | **79,5 %** |
| **Questions pièges** | **10/10** |
| **Tests CI** | **16/16** |
| **Outils MCP** | **11** (4 obligatoires + 7 bonus) |
| Mode naïf | 22 381 tokens |
| MemBridge | 4 580 tokens |

## Démo live (présentation jury)

```powershell
cd memory-mcp-challenge
.\scripts\start-demo.ps1
```

Puis ouvrir : **http://localhost:8765** → cliquer **▶ Tour démo auto**

| Page | URL |
|------|-----|
| Dashboard + Console MCP | http://localhost:8765 |
| Battle naïf vs MemBridge | http://localhost:8765/battle |
| Pitch slides | http://localhost:8765/pitch |

**Repo GitHub :** https://github.com/LUC-cmd/Hackathon-IT-INTELO

---

# Memory MCP Challenge — FINALE

**Hackathon INTELO2026** — Serveur MCP de mémoire avec benchmark chiffré tokens/qualité.

> Construisez un serveur MCP qui prouve qu'on peut réduire drastiquement les tokens d'un agent conversationnel **sans le rendre amnésique**.

## Finale — règles importantes

Le squelette fourni **ne suffit pas** pour merger une PR :

| Job CI | Passent avec le squelette ? |
|--------|----------------------------|
| `lint` + `smoke` | Oui |
| `regression` | **Non** — paraphrases, bruit, compression |
| `finale-eval` | **Non** — tests cachés (dépôt privé) |

Les tests cachés ne sont **pas dans ce dépôt**. Même avec l'IA, il faut une vraie recherche sémantique et une vraie compression.

## Contexte

| Mode | Comportement | Coût tokens |
|------|-------------|-------------|
| **Naïf** | Renvoie tout l'historique à chaque tour | Croissance quadratique |
| **Mémoire MCP** | Stocke, recherche, résume | Quasi plat |

## Structure

```
memory-mcp-challenge/
├── src/memory_mcp/     # Serveur MCP + 4 outils
├── benchmark/          # Harnais naïf vs mémoire
├── demo/               # Agent de démo (stub)
├── dashboard/          # Visualisation benchmark
├── tests/
│   ├── test_smoke.py       # API OK
│   └── test_regression.py  # Barre finale (dur)
└── .github/workflows/  # CI multi-niveaux
```

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -e ".[dev]"
```

## Utilisation

```bash
# Tests fumée (doivent passer)
pytest tests/test_smoke.py -v

# Tests régression (doivent passer pour merger)
PYTHONPATH=src:. pytest tests/test_regression.py tests/test_storage.py tests/test_tools.py -v

# Benchmark
python -m benchmark.harness

# Serveur MCP
memory-mcp
```

## Les 4 outils MCP

| Outil | Description |
|-------|-------------|
| `memory_store(content, tags)` | Stocke un fragment de mémoire |
| `memory_search(query, top_k)` | Recherche **sémantique** (paraphrases !) |
| `memory_summarize(session)` | Résumé **compressé** conservant les faits |
| `memory_stats()` | Tokens consommés |

## Critères de merge (PR)

1. **Régression** : paraphrases top-1, isolation sessions, compression ≤ 25 %, économie ≥ 60 % sur 50 tours
2. **Finale cachée** : économie ≥ 70 %, seed dynamique, anti-hardcoding

## Organisateurs

Voir [ADMIN.md](ADMIN.md) pour configurer le dépôt privé et les secrets CI.

## Pitch

Voir [PITCH.md](PITCH.md).
