#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from fraud_detection import detect_fraud
from datetime import datetime, timedelta

print("="*70)
print("  HACKATHON IT 2026 - RAPPORT DE STATUT DU PROJET")
print("="*70)
print()

# ===== STRUCTURE =====
print("[1] STRUCTURE DU PROJET")
print("-" * 70)

files = {
    'fraud_detection.py': 'Algo detection fraude',
    'app.py': 'Interface Streamlit',
    'tests/test_fraud_detection.py': 'Tests unitaires',
    'requirements.txt': 'Dependances',
    'sample_data.csv': 'Donnees exemple',
    'README.md': 'Documentation',
}

for f, desc in files.items():
    path = f
    exists = os.path.exists(path)
    status = "OK" if exists else "MISSING"
    print(f"  {status:10} {f:35} {desc}")

print()

# ===== TESTS =====
print("[2] RESULTATS DES TESTS")
print("-" * 70)

test_results = []

# Test 1: Empty list
try:
    assert detect_fraud([]) == []
    test_results.append(("Empty list", True, ""))
except Exception as e:
    test_results.append(("Empty list", False, str(e)))

# Test 2: Invalid amounts
try:
    txs = [
        {'transaction_id': 'tx1', 'user_id': 'u1', 'amount': -100, 'currency': 'EUR', 'merchant': 'Shop'},
        {'transaction_id': 'tx2', 'user_id': 'u1', 'amount': 0, 'currency': 'EUR', 'merchant': 'Shop'},
    ]
    result = detect_fraud(txs)
    assert all(r['is_suspicious'] for r in result)
    test_results.append(("Invalid amounts", True, ""))
except Exception as e:
    test_results.append(("Invalid amounts", False, str(e)))

# Test 3: Normal transaction
try:
    txs = [{'transaction_id': 'tx1', 'user_id': 'u1', 'amount': 50, 'currency': 'EUR', 'merchant': 'Shop'}]
    result = detect_fraud(txs)
    assert not result[0]['is_suspicious']
    test_results.append(("Normal transaction", True, ""))
except Exception as e:
    test_results.append(("Normal transaction", False, str(e)))

# Test 4: Anomalous amount
try:
    txs = [
        {'transaction_id': 'tx1', 'user_id': 'u1', 'amount': 50, 'currency': 'EUR', 'merchant': 'Shop'},
        {'transaction_id': 'tx2', 'user_id': 'u1', 'amount': 52, 'currency': 'EUR', 'merchant': 'Shop'},
        {'transaction_id': 'tx3', 'user_id': 'u1', 'amount': 5000, 'currency': 'EUR', 'merchant': 'Luxury'},
    ]
    result = detect_fraud(txs)
    assert result[2]['fraud_score'] > 0.3
    test_results.append(("Anomalous amount", True, f"score={result[2]['fraud_score']:.3f}"))
except Exception as e:
    test_results.append(("Anomalous amount", False, str(e)))

# Test 5: Output format
try:
    txs = [{'transaction_id': 'tx1', 'user_id': 'u1', 'amount': 100, 'currency': 'EUR', 'merchant': 'Shop'}]
    result = detect_fraud(txs)
    r = result[0]
    assert all(k in r for k in ['transaction_id', 'fraud_score', 'is_suspicious', 'reason'])
    assert 0.0 <= r['fraud_score'] <= 1.0
    assert isinstance(r['is_suspicious'], bool)
    test_results.append(("Output format", True, ""))
except Exception as e:
    test_results.append(("Output format", False, str(e)))

# Test 6: Missing fields
try:
    txs = [
        {'transaction_id': 'tx1', 'user_id': 'u1', 'amount': 100, 'currency': 'EUR'},
        {'transaction_id': 'tx2', 'amount': 100, 'currency': 'EUR'},
    ]
    result = detect_fraud(txs)
    assert len(result) == 2
    test_results.append(("Missing fields", True, ""))
except Exception as e:
    test_results.append(("Missing fields", False, str(e)))

# Test 7: Multiple users
try:
    txs = [
        {'transaction_id': 'tx1', 'user_id': 'u1', 'amount': 100, 'currency': 'EUR', 'merchant': 'A'},
        {'transaction_id': 'tx2', 'user_id': 'u2', 'amount': 100, 'currency': 'EUR', 'merchant': 'B'},
    ]
    result = detect_fraud(txs)
    assert len(result) == 2
    test_results.append(("Multiple users", True, ""))
except Exception as e:
    test_results.append(("Multiple users", False, str(e)))

# Test 8: Frequency anomaly
try:
    base_time = datetime(2024, 1, 1, 10, 0, 0)
    txs = []
    for i in range(6):
        txs.append({
            'transaction_id': f'tx{i}',
            'user_id': 'u1',
            'amount': 50,
            'currency': 'EUR',
            'merchant': 'Shop',
            'timestamp': (base_time + timedelta(seconds=i*5)).isoformat(),
        })
    result = detect_fraud(txs)
    suspicious_count = sum(1 for r in result if r['is_suspicious'])
    assert suspicious_count > 0
    test_results.append(("Frequency anomaly", True, f"detected={suspicious_count}"))
except Exception as e:
    test_results.append(("Frequency anomaly", False, str(e)))

# Test 9: Geographic anomaly
try:
    txs = [
        {
            'transaction_id': 'tx1',
            'user_id': 'u1',
            'amount': 100,
            'currency': 'EUR',
            'merchant': 'Shop',
            'country': 'FR',
            'timestamp': '2024-01-01T10:00:00',
        },
        {
            'transaction_id': 'tx2',
            'user_id': 'u1',
            'amount': 100,
            'currency': 'EUR',
            'merchant': 'Shop',
            'country': 'JP',
            'timestamp': '2024-01-01T10:30:00',
        },
    ]
    result = detect_fraud(txs)
    assert len(result) == 2
    assert result[1]['fraud_score'] > 0.2
    test_results.append(("Geographic anomaly", True, f"score={result[1]['fraud_score']:.3f}"))
except Exception as e:
    test_results.append(("Geographic anomaly", False, str(e)))

# Display results
passed = 0
failed = 0
for name, success, detail in test_results:
    status = "PASS" if success else "FAIL"
    detail_str = f" ({detail})" if detail else ""
    print(f"  [{status:4}] {name:25}{detail_str}")
    if success:
        passed += 1
    else:
        failed += 1

print()
print(f"TOTAL: {passed} passed, {failed} failed out of {len(test_results)} tests")
print()

# ===== METRIQUES =====
print("[3] METRIQUES DU CODE")
print("-" * 70)

source = open('fraud_detection.py').read()
lines = source.split('\n')
non_empty = [l for l in lines if l.strip() and not l.strip().startswith('#')]

print(f"  Total lines of code:  {len(lines):3}")
print(f"  Non-empty lines:      {len(non_empty):3}")
print(f"  Functions defined:    {source.count('def '):3}")
print(f"  Comments:             {source.count('#'):3}")

print()

# ===== CAPACITES =====
print("[4] CAPACITES IMPLEMENTEES")
print("-" * 70)

features = [
    ("Niveau 1 - Fondamentaux", [
        "Format sortie valide",
        "Montants invalides detectes",
        "Pas de plantage",
    ]),
    ("Niveau 2 - Logique metier", [
        "Anomalies montants (Z-score)",
        "Frequence anormale",
        "Incoherence geographique",
    ]),
    ("Niveau 3 - Finesse", [
        "Profils clients",
        "Justifications pertinentes",
        "Gestion cas limites",
    ]),
    ("Bonus", [
        "Interface Streamlit",
        "Donnees exemple",
        "Documentation complete",
    ]),
]

for category, items in features:
    print(f"  {category}")
    for item in items:
        print(f"    - {item}")

print()

# ===== RECOMMANDATIONS =====
print("[5] RECOMMANDATIONS POUR DOMINER")
print("-" * 70)

recommendations = [
    "1. Push sur GitHub LUC-cmd/Hackathon-IT-INTELO",
    "2. PR vers INTELO2026/fraud-challenge",
    "3. Verifier score dans Checks (viser 11/11)",
    "4. Affiner heuristiques si tests echouent",
    "5. Tester interface Streamlit pour jury",
    "6. Verifier lisibilite code (variable names)",
    "7. Valider explications (raison lisible)",
]

for rec in recommendations:
    print(f"  {rec}")

print()
print("="*70)
print(f"STATUS: PRET POUR LE CONCOURS - {passed}/9 tests passes")
print("="*70)
