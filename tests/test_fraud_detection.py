import pytest
from fraud_detection import detect_fraud
from datetime import datetime, timedelta

def test_empty_transactions():
    """Test avec liste vide"""
    result = detect_fraud([])
    assert result == []

def test_invalid_amount():
    """Montants invalides détectés"""
    txs = [
        {'transaction_id': 'tx1', 'user_id': 'u1', 'amount': -100, 'currency': 'EUR', 'merchant': 'Shop'},
        {'transaction_id': 'tx2', 'user_id': 'u1', 'amount': 0, 'currency': 'EUR', 'merchant': 'Shop'},
        {'transaction_id': 'tx3', 'user_id': 'u1', 'amount': None, 'currency': 'EUR', 'merchant': 'Shop'},
    ]
    result = detect_fraud(txs)
    assert len(result) == 3
    assert all(r['is_suspicious'] for r in result)
    assert all(r['fraud_score'] == 1.0 for r in result)

def test_normal_transaction():
    """Transaction normale"""
    txs = [
        {'transaction_id': 'tx1', 'user_id': 'u1', 'amount': 50, 'currency': 'EUR', 'merchant': 'Shop'},
    ]
    result = detect_fraud(txs)
    assert len(result) == 1
    assert not result[0]['is_suspicious']
    assert result[0]['fraud_score'] < 0.5

def test_anomalous_amount():
    """Détection d'un montant anormal"""
    txs = [
        {'transaction_id': 'tx1', 'user_id': 'u1', 'amount': 50, 'currency': 'EUR', 'merchant': 'Shop'},
        {'transaction_id': 'tx2', 'user_id': 'u1', 'amount': 55, 'currency': 'EUR', 'merchant': 'Shop'},
        {'transaction_id': 'tx3', 'user_id': 'u1', 'amount': 52, 'currency': 'EUR', 'merchant': 'Shop'},
        {'transaction_id': 'tx4', 'user_id': 'u1', 'amount': 5000, 'currency': 'EUR', 'merchant': 'Luxury'},
    ]
    result = detect_fraud(txs)
    assert len(result) == 4
    assert result[3]['fraud_score'] > 0.3

def test_different_users():
    """Transactions de différents clients"""
    txs = [
        {'transaction_id': 'tx1', 'user_id': 'u1', 'amount': 100, 'currency': 'EUR', 'merchant': 'A'},
        {'transaction_id': 'tx2', 'user_id': 'u2', 'amount': 100, 'currency': 'EUR', 'merchant': 'B'},
    ]
    result = detect_fraud(txs)
    assert len(result) == 2

def test_missing_fields():
    """Gestion des champs manquants"""
    txs = [
        {'transaction_id': 'tx1', 'user_id': 'u1', 'amount': 100, 'currency': 'EUR'},
        {'transaction_id': 'tx2', 'amount': 100, 'currency': 'EUR'},
        {'transaction_id': 'tx3', 'user_id': 'u1', 'currency': 'EUR'},
    ]
    result = detect_fraud(txs)
    assert len(result) == 3
    assert all('transaction_id' in r for r in result)
    assert all('fraud_score' in r for r in result)
    assert all('is_suspicious' in r for r in result)
    assert all('reason' in r for r in result)

def test_output_format():
    """Format de sortie correct"""
    txs = [
        {'transaction_id': 'tx1', 'user_id': 'u1', 'amount': 100, 'currency': 'EUR', 'merchant': 'Shop'},
    ]
    result = detect_fraud(txs)
    assert len(result) == 1
    r = result[0]
    assert 'transaction_id' in r
    assert 'fraud_score' in r
    assert 'is_suspicious' in r
    assert 'reason' in r
    assert isinstance(r['fraud_score'], float)
    assert 0.0 <= r['fraud_score'] <= 1.0
    assert isinstance(r['is_suspicious'], bool)
    assert isinstance(r['reason'], str)

def test_high_frequency():
    """Détection de fréquence anormale"""
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

def test_geographical_anomaly():
    """Détection d'anomalie géographique"""
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

def test_no_hardcoding():
    """Les résultats ne sont pas en dur"""
    txs1 = [
        {'transaction_id': 'tx1', 'user_id': 'u1', 'amount': 100, 'currency': 'EUR', 'merchant': 'A'},
    ]
    txs2 = [
        {'transaction_id': 'tx1', 'user_id': 'u1', 'amount': 500, 'currency': 'EUR', 'merchant': 'A'},
    ]
    result1 = detect_fraud(txs1)
    result2 = detect_fraud(txs2)
    assert result1[0]['fraud_score'] != result2[0]['fraud_score']
    assert result1[0]['is_suspicious'] != result2[0]['is_suspicious']

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
