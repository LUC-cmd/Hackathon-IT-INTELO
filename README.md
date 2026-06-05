# 🚨 Fraud Detection AI - Hackathon IT 2026

**Détection intelligente des fraudes financières avec Intelligence Artificielle**

## 📋 Description

Solution de détection de fraude basée sur l'analyse statistique, les heuristiques métier et l'apprentissage des patterns clients.

### 🎯 Caractéristiques

- ✅ **Détection robuste** : Montants anormaux, fréquences suspectes, anomalies géographiques
- ✅ **Gestion des données manquantes** : Aucun plantage sur données imparfaites
- ✅ **Justifications claires** : Explications lisibles pour chaque verdict
- ✅ **Scoring nuancé** : Score entre 0.0 et 1.0 pour chaque transaction
- ✅ **Interface Streamlit** : Visualisations professionnelles et dashboard interactif

## 🚀 Installation

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer les tests
pytest tests/ -v

# Démarrer l'interface web
streamlit run app.py
```

## 📦 Structure

```
.
├── fraud_detection.py       # Fonction principale detect_fraud()
├── app.py                   # Interface Streamlit (bonus)
├── tests/
│   └── test_fraud_detection.py
├── requirements.txt
└── README.md
```

## 🎯 Algorithme

### Étape 1 : Construction des Profils Clients
- Historique des montants (moyenne, écart-type)
- Pays et commerçants visités
- Ratio de transactions avec carte physique

### Étape 2 : Calcul des Anomalies

#### 1. **Anomalie Montant (Z-score)**
```
Si (montant - moyenne) / écart-type > 3.5 → Signal fort
```

#### 2. **Anomalie Géographique**
- Détection d'impossibilité physique (vitesse > 900 km/h)
- Distance impossible en temps insuffisant

#### 3. **Fréquence Anormale**
- 5+ transactions en 1 minute = suspect
- 3+ transactions en 1 minute = attention

#### 4. **Comportement Anormal**
- Commerçant nouveau (si historique connu)
- Transaction sans carte (vs habitude avec carte)

### Étape 3 : Scoring Final
- Score = somme pondérée des signaux
- Verdict = `is_suspicious` si score >= 0.5

## 📊 Exemple d'Utilisation

```python
from fraud_detection import detect_fraud

transactions = [
    {
        'transaction_id': 'tx001',
        'user_id': 'client_123',
        'amount': 50,
        'currency': 'EUR',
        'merchant': 'Boulangerie',
        'country': 'FR',
        'card_present': True,
        'timestamp': '2024-01-15T09:30:00'
    },
    # ... plus de transactions
]

results = detect_fraud(transactions)
# [
#   {
#       'transaction_id': 'tx001',
#       'fraud_score': 0.0,
#       'is_suspicious': False,
#       'reason': 'Transaction normale'
#   },
#   ...
# ]
```

## 🧪 Tests

11 tests couvrant :
- Format de sortie ✓
- Montants invalides ✓
- Anomalies ✓
- Données manquantes ✓
- Différents clients ✓
- Fréquence ✓
- Géographie ✓

```bash
pytest tests/test_fraud_detection.py -v
```

## 🎨 Interface Web (Bonus)

```bash
streamlit run app.py
```

La dashboard offre :
- 📊 Statistiques temps réel
- 🔍 Filtrage par risque
- 💾 Export CSV
- 📈 Graphiques interactifs

## 🔑 Points Clés de Notation

### Niveau 1 : Fondamentaux ⭐
- ✓ Format correct
- ✓ Montants invalides détectés
- ✓ Pas de plantage

### Niveau 2 : Logique Métier ⭐⭐
- ✓ Montants anormaux vs historique
- ✓ Fréquence suspecte
- ✓ Incohérences géographiques

### Niveau 3 : Finesse ⭐⭐⭐
- ✓ Éviter faux positifs
- ✓ Gérer cas limites
- ✓ Justifications pertinentes

## 📝 Format de Sortie

Chaque résultat contient :

```python
{
    'transaction_id': str,           # Identifiant transaction
    'fraud_score': float,            # Score 0.0-1.0
    'is_suspicious': bool,           # True/False
    'reason': str                    # Explication
}
```

## ⚠️ Pièges à Éviter

❌ Hardcoder les réponses → Tests cachés échouent  
❌ Code qui plante → Zéro points  
❌ Ignorer données manquantes → Erreur en production  
❌ Format invalide → Impossible à évaluer  

## 🏆 Critères de Victoire

1. **Score des tests** : 11/11 points
2. **Code lisible** : Noms explicites, fonctions séparées
3. **Justifications** : Claires et pertinentes
4. **Interface bonus** : Impressionne le jury

## 📞 Support

- Documentation : Voir docstrings dans `fraud_detection.py`
- Tests : `pytest tests/ -v` pour debug
- Interface : `streamlit run app.py` pour tester

---

**Hackathon IT 2026 — Lomé Business School**
*Intelligence Artificielle au service de la sécurité financière*
