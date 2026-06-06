# MemBridge — Guide équipe gagnante

## Démarrage rapide

```powershell
cd memory-mcp-challenge
python -m venv .venv
.\.venv\Scripts\activate
pip install -e ".[dev,demo]"
pytest -v
python -m benchmark.harness
python -m demo.agent
python -m demo.web_server
```

Dashboard : http://localhost:8765

## Ce qui est déjà implémenté

### Core (passe la CI)
- **Embeddings** : `fastembed` + modèle multilingue (paraphrases FR/EN)
- **Résumé intelligent** : extractif, faits tagués + signaux (email, contrat, montants, dates)
- **Benchmark** : 50 tours, économie tokens, questions pièges, `report.json`

### Bonus différenciants (jury)
- `memory_forget` — oubli intelligent
- `memory_locate` — géolocalisation en mémoire
- `memory_transcribe` — audio/vidéo/appels → mémoire
- `memory_translate` — FR↔EN offline
- `memory_timeline` — chronologie visuelle des souvenirs
- Dashboard **style éditorial chaud** (pas de violet IA) :
  - 3 graphiques (ligne, donut, barres pièges)
  - Recherche sémantique live
  - Dictée vocale Web Speech API
  - Caméra + capture → mémoire
  - GPS + carte OpenStreetMap
  - Mode présentation plein écran
  - Sons organiques + confetti

## Scénario démo jury (5 min)

1. `python -m demo.web_server` → ouvrir http://localhost:8765
2. Cliquer **Lancer benchmark** → courbe rouge explose, verte plate
3. Montrer **Questions pièges** 10/10
4. Activer **Géolocalisation** → stockée en mémoire
5. Coller une **transcription appel** → `memory_transcribe`
6. Poser question piège live : *"identité de l'interlocutrice premium"* → Marie Dupont

## Variables d'environnement

```env
OPENAI_API_KEY=sk-...          # optionnel, démo LLM
MEMBRIDGE_EMBED_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

## Checklist avant PR

- [ ] `pytest -v` → tout vert
- [ ] `python -m benchmark.harness` → savings ≥ 70%
- [ ] `ruff check src tests benchmark demo`
- [ ] PR vers `main` depuis `develop`
