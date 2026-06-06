# MemBridge — Démarrage Rapide 🚀

**Prêt? Voici comment lancer le projet en 2 minutes:**

---

## 1️⃣ Installation (30 secondes)

```bash
cd memory-mcp-challenge
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -e ".[dev]"
pip install reportlab  # Pour PDF export
```

---

## 2️⃣ Lancer le serveur (30 secondes)

```bash
python -m demo.web_server
```

Output attendu:
```
INFO:     Uvicorn running on http://0.0.0.0:8765
```

Ouvrir: **http://localhost:8765** 🎨

---

## 3️⃣ Démo Interactive (5-7 minutes)

### Étape 1: Benchmark (2 min)
1. Cliquer **"Lancer benchmark"**
2. Attendre ~30-60 secondes
3. Voir les résultats:
   - Graphe token par tour (rouge vs vert)
   - Économie: **-70%** ✓
   - Qualité: **8/10** ✓

### Étape 2: Multi-modal (1-2 min)
1. **Audio**: Cliquer zone audio → parler → "→ Mémoire"
2. **Géo**: Cliquer "Activer GPS" → voir carte
3. **Caméra**: Cliquer "Caméra" → "Capture → mémoire"

### Étape 3: Vérifier Verdict (30 sec)
1. Scroller jusqu'à **"Verdict jury"**
2. Voir les insights auto-générés
3. **Hackathon Gagnant?** ✓

---

## 📥 Exports Premium

- **JSON**: `Cliquer "JSON"` → télécharge rapport brut
- **PDF**: `Cliquer "PDF"` → rapport professionnel formaté

---

## ⚙️ Configuration Avancée

### Changer le nombre de tours
```python
# demo/web_server.py ligne 65
report = run_benchmark(turn_count=100)  # Default: 50
```

### Seed session de démo
```bash
# Utilise des faits prédéfinis (pour démo reproductible)
SESSION = "live-demo"
_seed_trap_session(tools, SESSION)
```

### Changer le port
```bash
python -m demo.web_server --port 9000
```

---

## 🔥 Checklist Avant Démo Jury

- [ ] Serveur lancé: `python -m demo.web_server`
- [ ] Dashboard charge: http://localhost:8765
- [ ] Benchmark produit rapport en 30-60s
- [ ] Audio mic fonctionne (dite quelque chose)
- [ ] GPS accepté (browser ask → autoriser)
- [ ] Caméra fonctionnel
- [ ] Verdict jury visible + insights affichées
- [ ] PDF export génère un fichier
- [ ] FR/EN toggle change la langue

---

## 🐛 Troubleshooting Rapide

| Problème | Solution |
|----------|----------|
| `ModuleNotFoundError: No module named 'memory_mcp'` | `pip install -e ".[dev]"` dans le venv |
| Benchmark très lent | Normal (50 tours = 30-60s). Pendant ce temps, expliquer concept. |
| Pas de micro/GPS | Browser demande permission. Accepter dans fenêtre popup. |
| PDF ne génère pas | `pip install reportlab` |
| Port 8765 déjà utilisé | `python -m demo.web_server --port 9000` |
| Design pas coloré | C'est normal! Palette organique (Rust/Moss), pas colorée volontairement. |

---

## 📊 Résultats Attendus

Après benchmark (50 tours):
- ✓ Tokens naïf: ~12,500
- ✓ Tokens MemBridge: ~3,750
- ✓ **Économie: -70%**
- ✓ Qualité: **8/10 pièges réussis**
- ✓ Verdict: **HACKATHON GAGNANT** 🏆

---

## 📚 Documentation Complète

- **DEMO_GUIDE.md** → Script 5-7 min pour le jury
- **IMPROVEMENTS.md** → Toutes les améliorations apportées
- **README.md** → Documentation technique

---

## 🎬 Lancer la Présentation (PPT)

```bash
# Ouvrir le pitch en navigateur
http://localhost:8765/pitch
```

---

**Prêt? Bonne chance! 🚀**
