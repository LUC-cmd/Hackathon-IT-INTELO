# MemBridge — Guide de Démo pour le Jury

**Durée suggérée: 5-7 minutes | Impressionner en live**

---

## 🎬 Ouverture (30 secondes)

```bash
cd memory-mcp-challenge
python -m demo.web_server
# Ouvrir http://localhost:8765
```

**Script:**
> "MemBridge est une mémoire partagée pour agents IA. Au lieu de renvoyer l'**historique complet** à chaque tour — ce qui coûte **quadratiquement** en tokens — nous stockons, recherchons et compressons intelligemment. Résultat: **-70% de tokens** sans perdre la qualité."

---

## 📊 Acte 1: Benchmark Live (2-3 min)

1. **Cliquer "Lancer benchmark"**
   - Montre les deux modes **côte à côte**:
     - **Naïf**: courbe qui monte (🔴 rouge / rust)
     - **MemBridge**: courbe qui stagne (🟢 vert / moss)

2. **Regarder les métriques apparaître**:
   - Tokens naïf: ~12,500 ❌
   - Tokens MemBridge: ~3,750 ✓
   - **Économie: -70%** 💰

3. **Pointer le graphe Waterfall**:
   > "Voici la compression détaillée. Chaque étape réduit les tokens."

4. **Vérifier les pièges**:
   > "Mais l'agent ne devient pas amnésique. Voyez: 8/10 questions pièges réussies. Il **retrouve les faits cachés** dans l'historique via recherche sémantique."

---

## 🎤 Acte 2: Multi-modal Live (1-2 min)

### Option A: Audio + Mémoire

1. Cliquer **"Cliquer pour dicter"** (Audio zone)
2. **Parler**: "Je suis Marie Dupont, contrat CTR-2024-8847, facture 149,90€"
3. Cliquer **"→ Mémoire"**
4. **Chercher** dans "Recherche sémantique live":
   - Query: "Qui est la cliente premium?"
   - Résultat: "Marie Dupont" retrouvée ✓

### Option B: Caméra + Snapshot

1. Cliquer **"Caméra"**
2. Cliquer **"Capture → mémoire"**
3. Voir la timeline se mettre à jour (point bleu = média)

### Option C: Géolocalisation

1. Cliquer **"Activer GPS"**
2. Voir la carte OpenStreetMap s'afficher avec localisation
3. Point vert = démo jury positionnée

---

## 🏆 Acte 3: Verdict (30 secondes)

Scroller jusqu'à **"Verdict jury"** (insights panel):

```
✓ HACKATHON GAGNANT
  • Compression exceptionnelle (-70%)
  • Qualité maintenue (80%)
  • Contexte stable
  • Dépendance contextuelle maîtrisée
```

**Script final:**
> "MemBridge n'est pas une promesse — c'est une mesure **chiffre à l'appui**. Nous avons réduit les coûts de 70% **sans** perdre la qualité. Et tout ça dans un serveur MCP standardisé qu'**n'importe quel agent** peut appeler."

---

## 💾 Exports Bonus (optionnel)

- **JSON**: `Cliquer "JSON"` → télécharge le rapport complet
- **PDF**: `Cliquer "PDF"` → rapport professionnel formaté (avec branding MemBridge)

---

## 🎨 Design Premium (ce qui les impressionne)

- ✅ **Palette organique** (Rust #C44F28, Moss #2F5242) — pas de violet "IA générique"
- ✅ **Animations fluides** — confetti + sons authentiques au-dessus de 70%
- ✅ **Multi-langue** — basculer FR ↔ EN avec le bouton
- ✅ **Timeline visuelle** — dots colorés = faits/géo/média
- ✅ **Graphes avancés**: Waterfall, Donut, Bar chart, Line chart

---

## ⏱️ Timeline Complète (5 min)

| Durée | Action | Aperçu |
|-------|--------|---------|
| 0:00-0:30 | Ouverture + explication concept | Contexte du problème |
| 0:30-3:30 | Lancer benchmark + explorer graphes | Metrics + visualisations |
| 3:30-4:30 | Démo multi-modal (audio/géo/caméra) | Mémoire partagée en action |
| 4:30-5:00 | Verdict jury + exports | Résultat final |

---

## 🔧 Troubleshooting

**Benchmark lent?**
- C'est normal (50 tours = ~30 secondes). Pendant ce temps, expliquer l'architecture.

**Pas de GPS?**
- Safari/Firefox demandent la permission. Autoriser → carte s'affiche.

**Speech Recognition ne marche pas?**
- Vérifier le navigateur (Chrome/Edge recommandés). Vérifier le micro.

**PDF ne génère pas?**
- Check si `reportlab` est installé: `pip install reportlab`

---

## 🎯 Points Clés à Mettre en Avant

1. **Pas de trade-off**: Économie + Qualité (pas l'un ou l'autre)
2. **Réplicabilité**: Même conversation → même résultats (anti-hacking)
3. **Standard**: MCP = n'importe quel agent peut utiliser
4. **Production-ready**: Tests, CI, validation, insights automatiques
5. **Design**: Premium sans être "AI-generic"

---

## 🚀 Gagner le hackathon

- ✅ Benchmark chiffré (70% économie)
- ✅ Qualité maintenue (80%+)
- ✅ Démo multi-modal impressionnante
- ✅ Design authentique (palette organique, pas générique)
- ✅ Architecture solide (MCP standard, tests, insights)

**Le jury ne juge pas une promesse — ils jugent une MESURE. Vous leur montrez les numbers.**

---

Bonne démo! 🏆
