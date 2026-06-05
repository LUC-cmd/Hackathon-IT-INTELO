#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple - Valide le systeme sans emojis (Windows compatible)
"""

import sys
import time
from datetime import datetime, timedelta

# Importer la fonction
from fraud_detection import detect_fraud

print("\n" + "="*70)
print("TEST COMPLET - FRAUD DETECTION SYSTEM")
print("="*70 + "\n")

# ============================================================================
# TEST 1: Transaction normale
# ============================================================================
print("[TEST 1] Transaction normale")
txs = [
    {'transaction_id': 'tx001', 'user_id': 'u001', 'amount': 50,
     'currency': 'EUR', 'merchant': 'Boulangerie', 'country': 'FR',
     'card_present': True, 'timestamp': '2024-01-15T09:30:00'},
]
result = detect_fraud(txs)
test_1 = (len(result) == 1 and result[0]['fraud_score'] < 0.5 and
          not result[0]['is_suspicious'])
status_1 = "PASS" if test_1 else "FAIL"
print(f"  [{status_1}] Score: {result[0]['fraud_score']:.3f} (should be <0.5)\n")

# ============================================================================
# TEST 2: Montant invalide
# ============================================================================
print("[TEST 2] Montant invalide (negative/zero)")
txs = [
    {'transaction_id': 'tx001', 'user_id': 'u001', 'amount': -100,
     'currency': 'EUR', 'merchant': 'Shop', 'country': 'FR', 'card_present': True},
]
result = detect_fraud(txs)
test_2 = (result[0]['fraud_score'] == 1.0 and result[0]['is_suspicious'])
status_2 = "PASS" if test_2 else "FAIL"
print(f"  [{status_2}] Score: {result[0]['fraud_score']:.3f} (should be 1.0)\n")

# ============================================================================
# TEST 3: Montant anormal (Z-score)
# ============================================================================
print("[TEST 3] Montant anormal (Z-score)")
txs = [
    {'transaction_id': 'tx1', 'user_id': 'u1', 'amount': 50, 'currency': 'EUR',
     'merchant': 'Shop', 'country': 'FR', 'timestamp': '2024-01-01T10:00:00'},
    {'transaction_id': 'tx2', 'user_id': 'u1', 'amount': 52, 'currency': 'EUR',
     'merchant': 'Shop', 'country': 'FR', 'timestamp': '2024-01-02T10:00:00'},
    {'transaction_id': 'tx3', 'user_id': 'u1', 'amount': 5000, 'currency': 'EUR',
     'merchant': 'Luxury', 'country': 'FR', 'timestamp': '2024-01-03T10:00:00'},
]
result = detect_fraud(txs)
test_3 = result[2]['fraud_score'] > 0.3
status_3 = "PASS" if test_3 else "FAIL"
print(f"  [{status_3}] TX3 Score: {result[2]['fraud_score']:.3f} (should be >0.3)\n")

# ============================================================================
# TEST 4: Donnees manquantes
# ============================================================================
print("[TEST 4] Donnees manquantes")
txs = [
    {'transaction_id': 'tx1', 'user_id': 'u1', 'amount': 100, 'currency': 'EUR'},
    {'transaction_id': 'tx2', 'amount': 100, 'currency': 'EUR'},
]
result = detect_fraud(txs)
test_4 = len(result) >= 1
status_4 = "PASS" if test_4 else "FAIL"
print(f"  [{status_4}] Results: {len(result)} transactions processed\n")

# ============================================================================
# TEST 5: Frequence anormale
# ============================================================================
print("[TEST 5] Frequence anormale (burst)")
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
test_5 = suspicious > 0
status_5 = "PASS" if test_5 else "FAIL"
print(f"  [{status_5}] Suspicious: {suspicious} (should be >0)\n")

# ============================================================================
# TEST 6: Format sortie
# ============================================================================
print("[TEST 6] Format sortie (4 champs)")
txs = [{'transaction_id': 'tx1', 'user_id': 'u1', 'amount': 100,
        'currency': 'EUR', 'merchant': 'Shop', 'country': 'FR', 'card_present': True}]
result = detect_fraud(txs)
test_6 = (all(k in result[0] for k in
            ['transaction_id', 'fraud_score', 'is_suspicious', 'reason']) and
            isinstance(result[0]['fraud_score'], (int, float)) and
            0.0 <= result[0]['fraud_score'] <= 1.0 and
            isinstance(result[0]['is_suspicious'], bool))
status_6 = "PASS" if test_6 else "FAIL"
print(f"  [{status_6}] Format correct: transaction_id, fraud_score, is_suspicious, reason\n")

# ============================================================================
# TEST 7: Geographie impossible
# ============================================================================
print("[TEST 7] Geographie impossible (France -> Japan en 30min)")
txs = [
    {'transaction_id': 'tx1', 'user_id': 'u1', 'amount': 100, 'currency': 'EUR',
     'merchant': 'Shop', 'country': 'FR', 'timestamp': '2024-01-15T08:00:00'},
    {'transaction_id': 'tx2', 'user_id': 'u1', 'amount': 100, 'currency': 'EUR',
     'merchant': 'Shop', 'country': 'JP', 'timestamp': '2024-01-15T08:30:00'},
]
result = detect_fraud(txs)
test_7 = result[1]['fraud_score'] > 0.5
status_7 = "PASS" if test_7 else "FAIL"
print(f"  [{status_7}] TX2 Score: {result[1]['fraud_score']:.3f} (should be >0.5)\n")

# ============================================================================
# TEST 8: Performance
# ============================================================================
print("[TEST 8] Performance (100 transactions)")
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

start = time.time()
results = detect_fraud(transactions)
elapsed = time.time() - start
speed = len(results) / elapsed if elapsed > 0 else 0
test_8 = elapsed < 5
status_8 = "PASS" if test_8 else "FAIL"
print(f"  [{status_8}] Time: {elapsed:.2f}s, Speed: {speed:.0f} tx/sec\n")

# ============================================================================
# RESULTAT FINAL
# ============================================================================
all_tests = [test_1, test_2, test_3, test_4, test_5, test_6, test_7, test_8]
passed = sum(all_tests)
total = len(all_tests)

print("="*70)
print(f"RESULTS: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
print("="*70 + "\n")

if passed == total:
    print("SUCCESS! All tests passed!")
    print("The system is READY FOR SUBMISSION!")
    print("\nNext step: Run the dashboard")
    print("  streamlit run app.py")
else:
    print(f"WARNING: {total - passed} test(s) failed")
    print("Please check the errors above")

sys.exit(0 if passed == total else 1)
