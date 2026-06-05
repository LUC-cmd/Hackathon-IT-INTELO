"""
Détecteur de Fraude Bancaire - Version Premium
Système complet avec 5 moteurs avancés et scoring multi-critères
"""

from datetime import datetime, timedelta
from collections import defaultdict
import math
from fraud_engines import (
    FraudDNAEngine, TrustScoreEngine, CardTestDetectionEngine,
    TravelDetectionEngine, BehaviorAnomalyEngine
)

def is_empty(value):
    """Vérifie si une valeur est vide"""
    return value is None or value == "" or str(value).strip() == ""

def parse_timestamp(ts):
    """Parse un timestamp ISO 8601"""
    if is_empty(ts):
        return None
    try:
        ts_str = str(ts).strip()
        return datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
    except:
        return None

def mean(values):
    """Calcule la moyenne"""
    if not values:
        return 0
    return sum(values) / len(values)

def std_dev(values, mean_val=None):
    """Calcule l'écart-type"""
    if len(values) < 2:
        return 0
    if mean_val is None:
        mean_val = mean(values)
    variance = sum((x - mean_val) ** 2 for x in values) / len(values)
    return math.sqrt(variance)

def detect_fraud(transactions):
    """
    Détecteur de fraude premium avec 5 moteurs avancés
    """
    results = []

    if not transactions:
        return results

    # Initialiser les moteurs
    dna_engine = FraudDNAEngine()
    trust_engine = TrustScoreEngine()
    card_test_engine = CardTestDetectionEngine()
    travel_engine = TravelDetectionEngine()
    behavior_engine = BehaviorAnomalyEngine()

    # Normaliser et parser les transactions
    valid_txs = []
    for tx in transactions:
        try:
            amount_raw = tx.get('amount', '')
            amount = None
            if not is_empty(amount_raw):
                try:
                    amount = float(amount_raw)
                except:
                    pass

            user_id = str(tx.get('user_id', 'unknown')).strip()
            timestamp = parse_timestamp(tx.get('timestamp'))
            country = str(tx.get('country', '')).strip().upper()
            merchant = str(tx.get('merchant', '')).strip().lower()
            card_present = str(tx.get('card_present', 'false')).lower() in ['true', '1', 'yes']

            valid_txs.append({
                'tx': tx, 'amount': amount, 'user_id': user_id, 'timestamp': timestamp,
                'country': country, 'merchant': merchant, 'card_present': card_present
            })
        except:
            continue

    # Phase 1: Calculer les profils clients
    user_dnas = {}
    user_trust_scores = {}

    users = set(tx['user_id'] for tx in valid_txs)
    for user_id in users:
        user_dnas[user_id] = dna_engine.build_dna(transactions, user_id)
        user_trust_scores[user_id] = trust_engine.calculate_trust_score(transactions, user_id)

    # Phase 2: Détecter les patterns globaux
    card_test_results = {}
    travel_results = {}
    for user_id in users:
        card_test_results[user_id] = card_test_engine.detect_card_testing(transactions, user_id)
        travel_results[user_id] = travel_engine.detect_travel_pattern(transactions, user_id)

    # Phase 3: Évaluer chaque transaction
    for idx, valid_tx in enumerate(valid_txs):
        tx = valid_tx['tx']
        tx_id = str(tx.get('transaction_id', 'unknown'))
        amount = valid_tx['amount']
        user_id = valid_tx['user_id']
        timestamp = valid_tx['timestamp']
        country = valid_tx['country']
        merchant = valid_tx['merchant']
        card_present = valid_tx['card_present']

        fraud_score = 0.0
        reasons = []
        details = {}

        # ===== MOTEUR 1: Validation Basique =====
        if amount is None or amount <= 0:
            fraud_score = 1.0
            reasons.append("Montant invalide (nul ou negatif)")
        else:
            # ===== MOTEUR 2: DNA Matching =====
            dna = user_dnas.get(user_id)
            if dna:
                dna_match = dna_engine.calculate_dna_match(valid_tx, dna)
                details['dna_match'] = dna_match
                if dna_match < 30:
                    fraud_score += 0.20
                    reasons.append(f"DNA Match: {dna_match}% (anormal)")
                elif dna_match < 50:
                    fraud_score += 0.10
                    reasons.append(f"DNA Match: {dna_match}% (inhabituel)")
                else:
                    reasons.append(f"DNA Match: {dna_match}% (normal)")

            # ===== MOTEUR 3: Trust Score =====
            trust = user_trust_scores.get(user_id, 50)
            details['trust_score'] = trust
            if trust < 30:
                fraud_score += 0.15
                reasons.append(f"Trust Score bas: {trust}/100")

            # ===== MOTEUR 4: Anomalies Comportementales =====
            anomalies = behavior_engine.detect_anomalies(transactions, user_id, valid_tx)
            for anom in anomalies:
                fraud_score += anom['risk']
                if anom['type'] == 'unusual_hour':
                    reasons.append(f"Horaire inhabituel: {anom['hour']}h")
                elif anom['type'] == 'burst':
                    reasons.append(f"Burst: {anom['count']} tx en 5min")

            # ===== MOTEUR 5: Détection Voyage =====
            travels = travel_results.get(user_id, [])
            for travel in travels:
                if timestamp:
                    fraud_score += travel['risk']
                    if travel['risk'] > 0.90:
                        reasons.append(f"IMPOSSIBLE: {travel['from']}→{travel['to']} {travel['speed_kmh']:.0f}km/h")
                    else:
                        reasons.append(f"Voyage rapide: {travel['distance_km']:.0f}km en {travel['hours']:.1f}h")

            # ===== MOTEUR 6: Card Testing =====
            card_test = card_test_results.get(user_id)
            if card_test and card_test['detected']:
                fraud_score += card_test['risk']
                reasons.append(f"Card testing: {card_test['test_count']} tests detectes")

            # ===== MOTEUR 7: Anomalies Montant (Z-score) =====
            prior_amounts = []
            for i in range(idx):
                if valid_txs[i]['user_id'] == user_id and valid_txs[i]['amount'] and valid_txs[i]['amount'] > 0:
                    prior_amounts.append(valid_txs[i]['amount'])

            if prior_amounts and amount > 0:
                m = mean(prior_amounts)
                s = std_dev(prior_amounts, m)
                if s > 0:
                    z_score = (amount - m) / s
                    details['z_score'] = z_score
                    if z_score > 4:
                        fraud_score += 0.30
                        reasons.append(f"Z-score extreme: {z_score:.1f}σ ({amount:.2f} vs {m:.2f}±{s:.2f})")
                    elif z_score > 2.5:
                        fraud_score += 0.15
                        reasons.append(f"Montant anormal: +{z_score:.1f}σ")

        # Clipping score
        fraud_score = max(0.0, min(1.0, fraud_score))
        details['fraud_score'] = fraud_score

        # Verdict
        is_suspicious = fraud_score >= 0.50

        # Si aucune raison: normal
        if not reasons:
            reasons.append("Transaction normale")
            is_suspicious = False
            fraud_score = 0.0

        reason = " | ".join(reasons)

        results.append({
            'transaction_id': tx_id,
            'fraud_score': round(fraud_score, 3),
            'is_suspicious': is_suspicious,
            'reason': reason,
            'details': details,
        })

    return results


if __name__ == "__main__":
    print("Fraud Detection V2 Ready - Advanced Premium System")
