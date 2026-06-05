# 🧪 Guide Complet de Test - Hackathon IT 2026

## ✅ Avant de soumettre, valide TOUT avec ce guide

---

## 1️⃣ INSTALLATION & DEPENDENCIES

### Étape 1: Vérifier Python
```bash
python --version
# Expected: Python 3.8+
```

### Étape 2: Installer les dépendances
```bash
pip install -r requirements.txt
# Should install: pytest, streamlit, pandas, plotly
```

### Étape 3: Vérifier l'installation
```bash
pip list | grep -E "pytest|streamlit|pandas|plotly"
# Devrait montrer toutes les 4 librairies
```

---

## 2️⃣ TEST DE LA FONCTION PRINCIPALE

### Test Direct (Python)

**Copie ce code dans un fichier `test_manual.py` :**

```python
from fraud_detection import detect_fraud

# TEST 1: Transaction normale
print("TEST 1: Transaction normale")
txs = [
    {'transaction_id': 'tx001', 'user_id': 'u001', 'amount': 50, 
     'currency': 'EUR', 'merchant': 'Boulangerie', 'country': 'FR', 
     'card_present': True, 'timestamp': '2024-01-15T09:30:00'},
]
result = detect_fraud(txs)
print(f"  Score: {result[0]['fraud_score']} (should be ~0.0)")
print(f"  Suspicious: {result[0]['is_suspicious']} (should be False)")
print(f"  Status: {'✅ PASS' if result[0]['fraud_score'] < 0.5 else '❌ FAIL'}\n")

# TEST 2: Montant invalide
print("TEST 2: Montant invalide (≤0)")
txs = [
    {'transaction_id': 'tx001', 'user_id': 'u001', 'amount': -100,
     'currency': 'EUR', 'merchant': 'Shop', 'country': 'FR', 'card_present': True},
]
result = detect_fraud(txs)
print(f"  Score: {result[0]['fraud_score']} (should be 1.0)")
print(f"  Suspicious: {result[0]['is_suspicious']} (should be True)")
print(f"  Status: {'✅ PASS' if result[0]['fraud_score'] == 1.0 else '❌ FAIL'}\n")

# TEST 3: Montant anormal (Z-score)
print("TEST 3: Montant anormal vs historique")
txs = [
    {'transaction_id': 'tx1', 'user_id': 'u1', 'amount': 50, 'currency': 'EUR', 'merchant': 'Shop', 'country': 'FR', 'timestamp': '2024-01-01T10:00:00'},
    {'transaction_id': 'tx2', 'user_id': 'u1', 'amount': 52, 'currency': 'EUR', 'merchant': 'Shop', 'country': 'FR', 'timestamp': '2024-01-02T10:00:00'},
    {'transaction_id': 'tx3', 'user_id': 'u1', 'amount': 5000, 'currency': 'EUR', 'merchant': 'Luxury', 'country': 'FR', 'timestamp': '2024-01-03T10:00:00'},
]
result = detect_fraud(txs)
print(f"  TX3 Score: {result[2]['fraud_score']} (should be > 0.3)")
print(f"  Status: {'✅ PASS' if result[2]['fraud_score'] > 0.3 else '❌ FAIL'}\n")

# TEST 4: Données manquantes
print("TEST 4: Données manquantes")
txs = [
    {'transaction_id': 'tx1', 'user_id': 'u1', 'amount': 100, 'currency': 'EUR'},  # manque merchant, country
    {'transaction_id': 'tx2', 'amount': 100, 'currency': 'EUR'},  # manque user_id
]
result = detect_fraud(txs)
print(f"  Results: {len(result)} transactions traitées")
print(f"  Status: {'✅ PASS' if len(result) >= 1 else '❌ FAIL'}\n")

# TEST 5: Fréquence anormale
print("TEST 5: Fréquence anormale")
from datetime import datetime, timedelta
base_time = datetime(2024, 1, 15, 10, 0, 0)
txs = []
for i in range(6):
    txs.append({
        'transaction_id': f'tx{i}',
        'user_id': 'u1',
        'amount': 50,
        'currency': 'EUR',
        'merchant': 'Shop',
        'country': 'FR',
        'timestamp': (base_time + timedelta(seconds=i*10)).isoformat(),
    })
result = detect_fraud(txs)
suspicious = sum(1 for r in result if r['is_suspicious'])
print(f"  Suspicious transactions: {suspicious} (should be > 0)")
print(f"  Status: {'✅ PASS' if suspicious > 0 else '❌ FAIL'}\n")

print("\n" + "="*60)
print("EXECUTION COMPLETE")
print("="*60)
```

**Exécute le test:**
```bash
python test_manual.py
```

**Résultat attendu:**
```
TEST 1: Transaction normale
  Score: 0.0 (should be ~0.0)
  Suspicious: False (should be False)
  Status: ✅ PASS

TEST 2: Montant invalide (≤0)
  Score: 1.0 (should be 1.0)
  Suspicious: True (should be True)
  Status: ✅ PASS

TEST 3: Montant anormal vs historique
  TX3 Score: 0.35 (should be > 0.3)
  Status: ✅ PASS

TEST 4: Données manquantes
  Results: 1+ transactions traitées
  Status: ✅ PASS

TEST 5: Fréquence anormale
  Suspicious transactions: 6 (should be > 0)
  Status: ✅ PASS
```

---

## 3️⃣ TEST AVEC PYTEST

### Exécuter les tests existants
```bash
pytest tests/test_fraud_detection.py -v
```

**Résultat attendu:**
```
tests/test_fraud_detection.py::test_empty_transactions PASSED
tests/test_fraud_detection.py::test_invalid_amount PASSED
tests/test_fraud_detection.py::test_normal_transaction PASSED
tests/test_fraud_detection.py::test_anomalous_amount PASSED
tests/test_fraud_detection.py::test_output_format PASSED
tests/test_fraud_detection.py::test_missing_fields PASSED
tests/test_fraud_detection.py::test_multiple_users PASSED
tests/test_fraud_detection.py::test_high_frequency PASSED
tests/test_fraud_detection.py::test_geographical_anomaly PASSED

========================= 9 passed in X.XXs =========================
```

---

## 4️⃣ TEST DU CSV AVEC DONNEES REELLES

### Charger et tester sample_data.csv
```python
from fraud_detection import detect_fraud, load_transactions
import pandas as pd

# Charger le CSV
transactions = load_transactions('sample_data.csv')
print(f"Transactions chargées: {len(transactions)}")

# Exécuter la détection
results = detect_fraud(transactions)
print(f"Résultats obtenus: {len(results)}")

# Afficher résultats
for r in results:
    print(f"TX: {r['transaction_id']:6} | Score: {r['fraud_score']:.3f} | Suspicious: {r['is_suspicious']} | Reason: {r['reason'][:60]}...")

# Résumé
suspicious_count = sum(1 for r in results if r['is_suspicious'])
print(f"\nRésumé:")
print(f"  Total: {len(results)}")
print(f"  Suspectes: {suspicious_count}")
print(f"  Taux: {suspicious_count/len(results)*100:.1f}%")
```

---

## 5️⃣ TEST DU DASHBOARD STREAMLIT

### Lancer le dashboard
```bash
streamlit run app.py
```

**Attendu:**
- ✅ Interface s'ouvre dans le navigateur (http://localhost:8501)
- ✅ Vous pouvez sélectionner "Démo scénario complet"
- ✅ Les transactions s'affichent dans un tableau
- ✅ Les graphiques se chargent
- ✅ Vous pouvez filtrer par risque
- ✅ Vous pouvez télécharger les résultats

### Tester les fonctionnalités:
1. **Mode Démo:**
   - Cliquez sur "Démo scénario complet"
   - Vérifiez que les données s'affichent
   
2. **Filtrage:**
   - Sélectionnez "Suspectes"
   - Vérifiez que seules les transactions suspectes s'affichent
   
3. **Graphiques:**
   - Vérifiez que le graphique de distribution s'affiche
   - Vérifiez que les KPIs se mettent à jour
   
4. **Export:**
   - Cliquez sur "Télécharger résultats CSV"
   - Vérifiez que le fichier se télécharge

---

## 6️⃣ TEST DU DASHBOARD PREMIUM

### Lancer le dashboard premium
```bash
streamlit run app_premium.py
```

**Attendu:**
- ✅ Interface "ShieldAI — Fraud Command Center" s'affiche
- ✅ 5 onglets visibles (Commande, Transactions, Clients, Intel, Simulateur)
- ✅ KPIs affichés (Transactions, Alertes, Critiques, Score moyen, Clients)
- ✅ Graphiques Plotly interactifs
- ✅ Design professionnel (couleurs, styling)

### Tester chaque onglet:
1. **Centre de commande:**
   - KPIs visible
   - Graphiques chargés
   - Alertes affichées
   
2. **Transactions:**
   - Tableau des transactions
   - Filtrage fonctionnel
   - Détails affichés
   
3. **Profils clients:**
   - Analyse par client
   - Risque identifié
   
4. **Intelligence fraude:**
   - Patterns détectés
   - Statistiques affichées
   
5. **Simulateur:**
   - Vous pouvez modifier le seuil d'alerte
   - Les résultats se mettent à jour

---

## 7️⃣ CHECKLIST FINALE DE VALIDATION

### ✅ Fonctionnalité Core
- [ ] `detect_fraud()` accepte une liste de transactions
- [ ] Output contient 4 champs: transaction_id, fraud_score, is_suspicious, reason
- [ ] fraud_score est entre 0.0 et 1.0
- [ ] is_suspicious est un booléen
- [ ] Pas de plantage sur données malformées

### ✅ Niveau 1 - Fondamentaux
- [ ] Montants invalides (≤0) détectés → score 1.0
- [ ] Transactions normales → score < 0.5
- [ ] Champs manquants gérés → pas de crash
- [ ] Format sortie correct

### ✅ Niveau 2 - Métier
- [ ] Montants anormaux détectés (Z-score)
- [ ] Fréquence anormale détectée (5+ en 1h)
- [ ] Géographie impossible détectée

### ✅ Niveau 3 - Finesse
- [ ] Faux positifs réduits (score < 0.5 sur cas normaux)
- [ ] Justifications claires et pertinentes
- [ ] Historique client utilisé correctement

### ✅ Interface
- [ ] app.py fonctionne (`streamlit run app.py`)
- [ ] Données chargées correctement
- [ ] Graphiques affichés
- [ ] Export CSV fonctionne
- [ ] Dashboard premium fonctionne

### ✅ Documentation
- [ ] README.md lisible
- [ ] README_PREMIUM.md complet
- [ ] Fichiers validation présents

### ✅ Git
- [ ] Pas de changements non commités
- [ ] Historique clean (8 commits)
- [ ] Messages de commit explicites

---

## 8️⃣ TEST DE STRESS (Optionnel mais recommandé)

### Générer beaucoup de données
```python
from fraud_detection import detect_fraud
import random
from datetime import datetime, timedelta

# Générer 1000 transactions
transactions = []
base_time = datetime(2024, 1, 1, 0, 0, 0)

for i in range(1000):
    transactions.append({
        'transaction_id': f'tx{i:04d}',
        'user_id': f'u{random.randint(1, 100)}',
        'amount': random.uniform(10, 5000),
        'currency': random.choice(['EUR', 'USD', 'GBP']),
        'merchant': random.choice(['Shop', 'Restaurant', 'Bank', 'Store']),
        'country': random.choice(['FR', 'US', 'GB', 'DE', 'IT']),
        'card_present': random.choice([True, False]),
        'timestamp': (base_time + timedelta(minutes=i)).isoformat(),
    })

# Exécuter la détection
import time
start = time.time()
results = detect_fraud(transactions)
elapsed = time.time() - start

print(f"Transactions traitées: {len(results)}")
print(f"Temps écoulé: {elapsed:.2f} secondes")
print(f"Vitesse: {len(results)/elapsed:.0f} transactions/sec")
print(f"Mémoire ok: {True}")  # Pas d'erreur mémoire

# Vérifier les résultats
suspicious = sum(1 for r in results if r['is_suspicious'])
print(f"Suspectes détectées: {suspicious}")
```

**Résultat attendu:**
```
Transactions traitées: 1000
Temps écoulé: 0.XX secondes
Vitesse: XXXX transactions/sec
Mémoire ok: True
Suspectes détectées: XX
```

---

## 9️⃣ COMMANDES RAPIDES DE TEST

### Test complet en une commande
```bash
# 1. Tests unitaires
pytest tests/ -v

# 2. Test manuel
python test_manual.py

# 3. Test CSV
python -c "
from fraud_detection import detect_fraud, load_transactions
txs = load_transactions('sample_data.csv')
res = detect_fraud(txs)
print(f'✅ {len(res)} transactions traitées')
"

# 4. Test Streamlit (dans un autre terminal)
streamlit run app.py
```

---

## 🔟 SI QUELQUE CHOSE ECHOUE

### Erreur: "ModuleNotFoundError: No module named 'pandas'"
```bash
pip install pandas plotly pytest streamlit
```

### Erreur: "No such file or directory: 'sample_data.csv'"
```bash
# Vérifie que tu es dans le bon répertoire
pwd
# Should be: C:\projets\HACKATHON IT 2026

# Ou charge depuis le bon chemin
txs = load_transactions('./sample_data.csv')
```

### Erreur: "Streamlit port already in use"
```bash
# Utilise un port différent
streamlit run app.py --server.port 8502
```

### Erreur: "TypeError in detect_fraud"
```bash
# Vérifiez que l'input est correct:
# - Liste de dictionnaires
# - Chaque dict a: transaction_id, user_id, amount, currency, merchant, country, card_present, timestamp
```

---

## ✅ RÉSUMÉ FINAL

Si TOUS les tests passent:

```
✅ Tests unitaires: 9/9 PASS
✅ Test manuel: 5/5 PASS
✅ CSV chargé: OK
✅ Dashboard: Fonctionne
✅ Format output: Correct
✅ Git status: Clean
✅ Code quality: Excellent
```

**ALORS TU ES PRET A SOUMETTRE! 🚀**

---

## 📝 Notes importantes

- **Ne change rien** si tous les tests passent
- **Sauvegarde une copie** avant de soumettre
- **Teste localement** avant de pusher
- **Démo le dashboard** pour le jury
- **Explique les scores** en détail

Bonne chance! 🏆
