#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 SCRIPT DE TEST COMPLET - Hackathon IT 2026
Valide TOUT le système en une seule exécution
"""

import sys
import time
from datetime import datetime, timedelta
from fraud_detection import detect_fraud, load_transactions

def print_section(title):
    """Affiche un titre de section"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def print_result(test_name, passed, details=""):
    """Affiche le résultat d'un test"""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"  {status} | {test_name:40} {details}")

# ============================================================================
# TEST 1: INSTALLATION & IMPORTS
# ============================================================================
print_section("1️⃣ VÉRIFICATION INSTALLATION")

try:
    import pandas
    print_result("pandas", True)
except ImportError:
    print_result("pandas", False, "- Install: pip install pandas")
    sys.exit(1)

try:
    import streamlit as st
    print_result("streamlit", True)
except ImportError:
    print_result("streamlit", False, "- Install: pip install streamlit")
    sys.exit(1)

try:
    import plotly.express as px
    print_result("plotly", True)
except ImportError:
    print_result("plotly", False, "- Install: pip install plotly")
    sys.exit(1)

try:
    import pytest
    print_result("pytest", True)
except ImportError:
    print_result("pytest", False, "- Install: pip install pytest")
    sys.exit(1)

# ============================================================================
# TEST 2: FONCTION CORE
# ============================================================================
print_section("2️⃣ TEST DE LA FONCTION detect_fraud()")

# Test 2.1: Liste vide
result = detect_fraud([])
test_2_1 = len(result) == 0
print_result("Empty list", test_2_1, f"({len(result)} résultats)")

# Test 2.2: Transaction normale
txs = [
    {'transaction_id': 'tx001', 'user_id': 'u001', 'amount': 50,
     'currency': 'EUR', 'merchant': 'Boulangerie', 'country': 'FR',
     'card_present': True, 'timestamp': '2024-01-15T09:30:00'},
]
result = detect_fraud(txs)
test_2_2 = (len(result) == 1 and
            result[0]['fraud_score'] < 0.5 and
            not result[0]['is_suspicious'])
print_result("Normal transaction", test_2_2, f"(score={result[0]['fraud_score']:.3f})")

# Test 2.3: Montant invalide
txs = [
    {'transaction_id': 'tx001', 'user_id': 'u001', 'amount': -100,
     'currency': 'EUR', 'merchant': 'Shop', 'country': 'FR', 'card_present': True},
]
result = detect_fraud(txs)
test_2_3 = (result[0]['fraud_score'] == 1.0 and result[0]['is_suspicious'])
print_result("Invalid amount (≤0)", test_2_3, f"(score={result[0]['fraud_score']:.3f})")

# Test 2.4: Montant anormal (Z-score)
txs = [
    {'transaction_id': 'tx1', 'user_id': 'u1', 'amount': 50, 'currency': 'EUR',
     'merchant': 'Shop', 'country': 'FR', 'timestamp': '2024-01-01T10:00:00'},
    {'transaction_id': 'tx2', 'user_id': 'u1', 'amount': 52, 'currency': 'EUR',
     'merchant': 'Shop', 'country': 'FR', 'timestamp': '2024-01-02T10:00:00'},
    {'transaction_id': 'tx3', 'user_id': 'u1', 'amount': 5000, 'currency': 'EUR',
     'merchant': 'Luxury', 'country': 'FR', 'timestamp': '2024-01-03T10:00:00'},
]
result = detect_fraud(txs)
test_2_4 = result[2]['fraud_score'] > 0.3
print_result("Anomalous amount (Z-score)", test_2_4, f"(score={result[2]['fraud_score']:.3f})")

# Test 2.5: Données manquantes
txs = [
    {'transaction_id': 'tx1', 'user_id': 'u1', 'amount': 100, 'currency': 'EUR'},
    {'transaction_id': 'tx2', 'amount': 100, 'currency': 'EUR'},
]
result = detect_fraud(txs)
test_2_5 = len(result) >= 1
print_result("Missing fields", test_2_5, f"({len(result)} résultats)")

# Test 2.6: Fréquence anormale
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
test_2_6 = suspicious > 0
print_result("Frequency anomaly", test_2_6, f"({suspicious} suspectes)")

# Test 2.7: Format sortie
txs = [{'transaction_id': 'tx1', 'user_id': 'u1', 'amount': 100,
        'currency': 'EUR', 'merchant': 'Shop', 'country': 'FR', 'card_present': True}]
result = detect_fraud(txs)
test_2_7 = (all(k in result[0] for k in
            ['transaction_id', 'fraud_score', 'is_suspicious', 'reason']) and
            isinstance(result[0]['fraud_score'], (int, float)) and
            0.0 <= result[0]['fraud_score'] <= 1.0 and
            isinstance(result[0]['is_suspicious'], bool))
print_result("Output format (4 fields)", test_2_7, "✅ Correct")

# Test 2.8: Géographie impossible
txs = [
    {'transaction_id': 'tx1', 'user_id': 'u1', 'amount': 100, 'currency': 'EUR',
     'merchant': 'Shop', 'country': 'FR', 'timestamp': '2024-01-15T08:00:00'},
    {'transaction_id': 'tx2', 'user_id': 'u1', 'amount': 100, 'currency': 'EUR',
     'merchant': 'Shop', 'country': 'JP', 'timestamp': '2024-01-15T08:30:00'},
]
result = detect_fraud(txs)
test_2_8 = result[1]['fraud_score'] > 0.5
print_result("Geographic impossibility", test_2_8, f"(score={result[1]['fraud_score']:.3f})")

# ============================================================================
# TEST 3: CHARGEMENT CSV
# ============================================================================
print_section("3️⃣ TEST CHARGEMENT CSV")

try:
    txs = load_transactions('sample_data.csv')
    test_3_1 = len(txs) > 0
    print_result("Load sample_data.csv", test_3_1, f"({len(txs)} transactions)")

    result = detect_fraud(txs)
    test_3_2 = len(result) == len(txs)
    print_result("Process CSV results", test_3_2, f"({len(result)} résultats)")

    suspicious = sum(1 for r in result if r['is_suspicious'])
    print_result("Detect anomalies", suspicious > 0, f"({suspicious} suspectes)")
except Exception as e:
    print_result("Load sample_data.csv", False, f"Error: {str(e)}")

# ============================================================================
# TEST 4: PERFORMANCE
# ============================================================================
print_section("4️⃣ TEST DE PERFORMANCE")

# Générer 100 transactions
import random
transactions = []
base_time = datetime(2024, 1, 1, 0, 0, 0)
for i in range(100):
    transactions.append({
        'transaction_id': f'tx{i:03d}',
        'user_id': f'u{random.randint(1, 20)}',
        'amount': random.uniform(10, 5000),
        'currency': 'EUR',
        'merchant': random.choice(['Shop', 'Restaurant', 'Bank']),
        'country': random.choice(['FR', 'US', 'GB', 'DE']),
        'card_present': random.choice([True, False]),
        'timestamp': (base_time + timedelta(minutes=i)).isoformat(),
    })

# Mesurer le temps
start = time.time()
results = detect_fraud(transactions)
elapsed = time.time() - start

speed = len(results) / elapsed if elapsed > 0 else 0
test_4_1 = elapsed < 5  # Moins de 5 secondes pour 100 transactions
print_result("Process 100 transactions", test_4_1, f"({elapsed:.2f}s, {speed:.0f} tx/sec)")

# ============================================================================
# TEST 5: RÉSUMÉ DES RÉSULTATS
# ============================================================================
print_section("5️⃣ RÉSUMÉ DES RÉSULTATS")

all_tests = [
    test_2_1, test_2_2, test_2_3, test_2_4, test_2_5,
    test_2_6, test_2_7, test_2_8, test_4_1
]
passed = sum(all_tests)
total = len(all_tests)

print(f"  Tests passés: {passed}/{total}")
print(f"  Taux de réussite: {passed/total*100:.0f}%\n")

if passed == total:
    print("  🎉 TOUS LES TESTS PASSENT!")
    print("  ✅ Le système est PRET pour la soumission!\n")
else:
    print(f"  ⚠️  {total - passed} test(s) échoué(s)")
    print("  Vérifie les erreurs ci-dessus\n")

# ============================================================================
# TEST 6: CHECKLIST FINALE
# ============================================================================
print_section("6️⃣ CHECKLIST FINALE")

checklist = [
    ("Format sortie (4 champs)", test_2_7),
    ("Montants invalides détectés", test_2_3),
    ("Données manquantes gérées", test_2_5),
    ("Montants anormaux détectés", test_2_4),
    ("Fréquence détectée", test_2_6),
    ("Géographie impossible détectée", test_2_8),
    ("Performance acceptable", test_4_1),
]

for item, status in checklist:
    print_result(item, status)

# ============================================================================
# TEST 7: PROCHAINES ETAPES
# ============================================================================
print_section("7️⃣ PROCHAINES ETAPES")

print("""
Si tous les tests passent (✅ TOUS LES TESTS PASSENT):

  1. Tester le Dashboard:
     streamlit run app.py

  2. Vérifier les Git commits:
     git log --oneline | head -10
     git status  # Doit afficher "nothing to commit"

  3. Tester avec sample_data.csv:
     streamlit run app.py
     → Charger sample_data.csv
     → Vérifier les résultats

  4. Faire une démo:
     streamlit run app_premium.py
     → Tester tous les onglets
     → Vérifier les graphiques

  5. Prêt pour la soumission:
     git push origin master
     → Créer une PR sur INTELO2026/fraud-challenge

""")

# ============================================================================
# RÉSULTAT FINAL
# ============================================================================
print("="*70)
if passed == total:
    print("  ✅ SUCCES - Tout fonctionne parfaitement!")
    print("  🚀 Vous êtes prêt à soumettre!")
else:
    print(f"  ⚠️  {total - passed} problème(s) trouvé(s)")
    print("  Corrigez les erreurs avant de soumettre")
print("="*70)
print()
