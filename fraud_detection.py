import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Dict, Any, Tuple

def load_transactions(csv_path: str) -> List[Dict[str, Any]]:
    """Charge les transactions depuis un fichier CSV"""
    try:
        df = pd.read_csv(csv_path)
        return df.to_dict('records')
    except Exception as e:
        print(f"Erreur lors du chargement : {e}")
        return []

def parse_timestamp(ts: Any) -> datetime:
    """Parse un timestamp ISO 8601 avec gestion des valeurs vides"""
    if pd.isna(ts) or ts == "" or ts is None:
        return None
    try:
        if isinstance(ts, datetime):
            return ts
        return pd.to_datetime(ts)
    except:
        return None

def calculate_distance_km(country1: str, country2: str) -> float:
    """Approximation simple de la distance entre deux pays"""
    if not country1 or not country2 or pd.isna(country1) or pd.isna(country2):
        return 0

    country_coords = {
        'FR': (48.8566, 2.3522), 'US': (37.7749, -122.4194), 'GB': (51.5074, -0.1278),
        'DE': (52.5200, 13.4050), 'IT': (41.9028, 12.4964), 'ES': (40.4168, -3.7038),
        'BF': (12.3714, -1.5197), 'CI': (6.8276, -5.2893), 'SN': (14.7167, -17.4674),
        'ML': (12.6392, -8.0029), 'NE': (13.5116, 2.1257), 'TG': (6.1256, 1.2317),
        'BE': (50.8503, 4.3517), 'NL': (52.3676, 4.9041), 'CH': (46.9479, 7.4474),
        'AT': (48.2082, 16.3738), 'PL': (52.2297, 21.0122), 'SE': (59.3293, 18.0686),
        'NO': (59.9139, 10.7522), 'DK': (55.6761, 12.5683), 'FI': (60.1695, 24.9354),
        'JP': (35.6762, 139.6503), 'CN': (39.9042, 116.4074), 'IN': (28.6139, 77.2090),
        'BR': (-23.5505, -46.6333), 'MX': (19.4326, -99.1332), 'CA': (43.6532, -79.3832),
        'AU': (-33.8688, 151.2093), 'KR': (37.5665, 126.9780), 'TH': (13.7563, 100.5018),
    }

    if country1 not in country_coords or country2 not in country_coords:
        return 5000

    lat1, lon1 = country_coords[country1]
    lat2, lon2 = country_coords[country2]

    return np.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2) * 111

def detect_fraud(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Détecteur de fraude intelligent basé sur l'historique client et heuristiques métier
    """
    results = []

    if not transactions:
        return results

    # Phase 1 : Construction des profils clients
    client_profiles = defaultdict(lambda: {
        'amounts': [], 'countries': set(), 'merchants': set(),
        'timestamps': [], 'card_present_count': 0, 'total_tx': 0
    })

    valid_txs = []
    for tx in transactions:
        try:
            amount = float(tx.get('amount', 0)) if pd.notna(tx.get('amount')) else None
            user_id = str(tx.get('user_id', 'unknown'))
            timestamp = parse_timestamp(tx.get('timestamp'))
            country = str(tx.get('country', '')).upper() if pd.notna(tx.get('country')) else ''
            merchant = str(tx.get('merchant', '')).lower() if pd.notna(tx.get('merchant')) else ''
            card_present = bool(tx.get('card_present', False))

            valid_txs.append({
                'tx': tx, 'amount': amount, 'user_id': user_id, 'timestamp': timestamp,
                'country': country, 'merchant': merchant, 'card_present': card_present
            })

            if amount and amount > 0:
                client_profiles[user_id]['amounts'].append(amount)
            if country:
                client_profiles[user_id]['countries'].add(country)
            if merchant:
                client_profiles[user_id]['merchants'].add(merchant)
            if timestamp:
                client_profiles[user_id]['timestamps'].append(timestamp)
            if card_present:
                client_profiles[user_id]['card_present_count'] += 1
            client_profiles[user_id]['total_tx'] += 1
        except:
            continue

    # Phase 2 : Calcul des statistiques clients
    client_stats = {}
    for user_id, profile in client_profiles.items():
        amounts = profile['amounts']
        if amounts:
            client_stats[user_id] = {
                'mean': np.mean(amounts),
                'std': np.std(amounts) if len(amounts) > 1 else 0,
                'min': np.min(amounts),
                'max': np.max(amounts),
                'median': np.median(amounts),
                'countries': profile['countries'],
                'merchants': profile['merchants'],
                'card_present_ratio': profile['card_present_count'] / max(1, profile['total_tx']),
            }
        else:
            client_stats[user_id] = {
                'mean': 0, 'std': 0, 'min': 0, 'max': 0, 'median': 0,
                'countries': profile['countries'],
                'merchants': profile['merchants'],
                'card_present_ratio': 0,
            }

    # Phase 3 : Évaluation de chaque transaction
    for valid_tx in valid_txs:
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

        # Détection 1 : Montant invalide
        if amount is None or amount <= 0:
            fraud_score = 1.0
            reasons.append("Montant invalide (nul ou négatif)")
        else:
            stats = client_stats.get(user_id, {})
            mean = stats.get('mean', 0)
            std = stats.get('std', 0)

            # Détection 2 : Anomalie montant (Z-score)
            if mean > 0 and std > 0:
                z_score = (amount - mean) / std
                if z_score > 3.5:
                    fraud_score += 0.35
                    reasons.append(f"Montant anormal : {amount:.2f} vs moyenne {mean:.2f}±{std:.2f} (z={z_score:.1f})")
                elif z_score > 2.5:
                    fraud_score += 0.15
                    reasons.append(f"Montant élevé : {amount:.2f} vs moyenne {mean:.2f}")
            elif amount and mean > 0 and amount > mean * 2:
                fraud_score += 0.15
                reasons.append(f"Montant 2x la moyenne : {amount:.2f} vs {mean:.2f}")

            # Détection 3 : Transaction sans carte physique
            if not card_present and stats.get('card_present_ratio', 0) > 0.8:
                fraud_score += 0.10
                reasons.append("Transaction en ligne (vs habitude carte présente)")

            # Détection 4 : Commerçant nouveau
            if merchant and merchant not in stats.get('merchants', set()):
                if len(stats.get('merchants', set())) > 5:
                    fraud_score += 0.05
                    reasons.append(f"Commerçant nouveau : {merchant}")

            # Détection 5 : Géographie impossible
            if timestamp and country:
                last_tx_country = None
                last_tx_time = None

                for other_tx in valid_txs:
                    if (other_tx['user_id'] == user_id and
                        other_tx['timestamp'] and
                        other_tx['country'] and
                        other_tx['timestamp'] < timestamp):
                        if last_tx_time is None or other_tx['timestamp'] > last_tx_time:
                            last_tx_country = other_tx['country']
                            last_tx_time = other_tx['timestamp']

                if last_tx_country and last_tx_country != country:
                    time_diff = (timestamp - last_tx_time).total_seconds() / 3600
                    distance = calculate_distance_km(last_tx_country, country)

                    if time_diff > 0 and distance / time_diff > 900:
                        fraud_score += 0.25
                        reasons.append(f"Impossible : {last_tx_country} → {country} en {time_diff:.1f}h ({distance:.0f}km)")
                    elif time_diff < 2 and distance > 500:
                        fraud_score += 0.15
                        reasons.append(f"Trop rapide : {distance:.0f}km en {time_diff:.1f}h")

        # Détection 6 : Fréquence suspecte
        if timestamp:
            nearby_txs = sum(1 for other_tx in valid_txs
                            if (other_tx['user_id'] == user_id and
                                other_tx['timestamp'] and
                                abs((other_tx['timestamp'] - timestamp).total_seconds()) < 60))

            if nearby_txs >= 5:
                fraud_score += 0.25
                reasons.append(f"Fréquence excessive : {nearby_txs} transactions en 1 minute")
            elif nearby_txs >= 3:
                fraud_score += 0.10
                reasons.append(f"Fréquence élevée : {nearby_txs} transactions en 1 minute")

        # Clipping du score entre 0 et 1
        fraud_score = max(0.0, min(1.0, fraud_score))

        # Détermination du verdict
        is_suspicious = fraud_score >= 0.5

        # Si aucune raison et score bas : transaction normale
        if not reasons:
            is_suspicious = False
            fraud_score = 0.0
            reason = "Transaction normale"
        else:
            reason = " | ".join(reasons)

        results.append({
            'transaction_id': tx_id,
            'fraud_score': round(fraud_score, 3),
            'is_suspicious': is_suspicious,
            'reason': reason
        })

    return results

if __name__ == "__main__":
    print("Fraud Detection Module Ready")
