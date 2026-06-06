# MemBridge — Notre implémentation INTELO2026

## Résultats mesurés

| Métrique | Valeur |
|---|---|
| Économie tokens | **~79 %** |
| Questions pièges | **10/10** |
| Tests CI | **16/16** |
| Outils MCP | **4 core + 7 bonus** |

## Lancement rapide

```powershell
.\scripts\start-demo.ps1
```

Ou manuellement :

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\activate
pip install -e ".[dev,demo]"
pytest -v
python -m benchmark.harness
python -m demo.web_server
```

- Dashboard : http://localhost:8765
- Pitch jury : http://localhost:8765/pitch

## Outils MCP

### Core (obligatoires)
- `memory_store` · `memory_search` · `memory_summarize` · `memory_stats`

### Bonus (différenciation)
- `memory_forget` — oubli intelligent
- `memory_locate` — géolocalisation
- `memory_transcribe` — audio / vidéo / appels
- `memory_translate` — FR ↔ EN
- `memory_timeline` — chronologie visuelle
- `memory_share` — mémoire partagée multi-agents

## Stack technique

- **Embeddings** : fastembed + paraphrase-multilingual-MiniLM-L12-v2
- **Résumé** : format structuré à slots fixes (CLIENT|CTR|MAIL|EUR|DATE)
- **Stockage** : SQLite + similarité cosinus + reranking par intention
- **Dashboard** : Chart.js, Web Speech API, caméra, GPS

## Démo jury (5 min)

1. Ouvrir `/pitch` — slides + chiffres
2. Dashboard → **Lancer benchmark** — courbes + donut
3. Recherche live : *identité de l'interlocutrice premium*
4. Dictée micro → mémoire
5. Caméra capture + GPS Lomé
