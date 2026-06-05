from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Any, Optional, Set
import math
import csv

# Seuils calibrés pour limiter les faux positifs (niveau 3)
THRESHOLD_SUSPICIOUS = 0.5
Z_SCORE_STRONG = 3.5
Z_SCORE_MODERATE = 2.5
IQR_MULTIPLIER = 1.5
MIN_HISTORY_FOR_IQR = 4
MIN_HISTORY_FOR_MERCHANT = 5
MAX_TRAVEL_SPEED_KMH = 900
GEO_FAST_HOURS = 2
GEO_FAST_DISTANCE_KM = 500
FREQ_CRITICAL = 5
FREQ_ELEVATED = 3
FREQ_WINDOW_SEC = 60


def load_transactions(csv_path: str) -> List[Dict[str, Any]]:
    """Charge les transactions depuis un fichier CSV."""
    try:
        transactions = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                transactions.append(row)
        return transactions
    except Exception as e:
        print(f"Erreur lors du chargement : {e}")
        return []


def is_empty(value: Any) -> bool:
    """Vérifie si une valeur est vide ou absente."""
    if value is None:
        return True
    if isinstance(value, float) and math.isnan(value):
        return True
    return str(value).strip() == ""


def parse_timestamp(ts: Any) -> Optional[datetime]:
    """Parse un timestamp ISO 8601 avec gestion des valeurs vides."""
    if is_empty(ts):
        return None
    try:
        if isinstance(ts, datetime):
            return ts.replace(tzinfo=None) if ts.tzinfo else ts
        ts_str = str(ts).strip()
        parsed = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
        return parsed.replace(tzinfo=None) if parsed.tzinfo else parsed
    except (ValueError, TypeError):
        return None


def parse_amount(raw: Any) -> Optional[float]:
    """Convertit un montant en float ou None si invalide."""
    if is_empty(raw):
        return None
    try:
        return float(raw)
    except (ValueError, TypeError):
        return None


def parse_card_present(raw: Any) -> bool:
    """Interprète card_present depuis plusieurs formats."""
    if isinstance(raw, bool):
        return raw
    if is_empty(raw):
        return False
    return str(raw).strip().lower() in ('true', '1', 'yes', 'oui', 'vrai')


def mean(values: List[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def std_dev(values: List[float], mean_val: Optional[float] = None) -> float:
    if len(values) < 2:
        return 0.0
    if mean_val is None:
        mean_val = mean(values)
    variance = sum((x - mean_val) ** 2 for x in values) / len(values)
    return math.sqrt(variance)


def iqr_upper_fence(values: List[float]) -> Optional[float]:
    """Borne supérieure IQR — robuste aux outliers pour éviter les faux positifs."""
    if len(values) < MIN_HISTORY_FOR_IQR:
        return None
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    q1 = sorted_vals[n // 4]
    q3 = sorted_vals[(3 * n) // 4]
    iqr = q3 - q1
    if iqr <= 0:
        return None
    return q3 + IQR_MULTIPLIER * iqr


def calculate_distance_km(country1: str, country2: str) -> float:
    """Distance approximative entre deux pays (km)."""
    if is_empty(country1) or is_empty(country2):
        return 0.0

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
        'XOF': (6.1256, 1.2317),
    }

    c1, c2 = country1.upper(), country2.upper()
    if c1 not in country_coords or c2 not in country_coords:
        return 5000.0

    lat1, lon1 = country_coords[c1]
    lat2, lon2 = country_coords[c2]
    return math.sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2) * 111


def _normalize_tx(tx: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Normalise une transaction sans jamais lever d'exception."""
    try:
        return {
            'tx': tx,
            'transaction_id': str(tx.get('transaction_id', '')).strip(),
            'user_id': str(tx.get('user_id', '')).strip(),
            'amount': parse_amount(tx.get('amount')),
            'currency': str(tx.get('currency', '')).strip().upper(),
            'merchant': str(tx.get('merchant', '')).strip().lower(),
            'country': str(tx.get('country', '')).strip().upper(),
            'timestamp': parse_timestamp(tx.get('timestamp')),
            'card_present': parse_card_present(tx.get('card_present')),
        }
    except Exception:
        return None


def _missing_critical_fields(norm: Dict[str, Any]) -> List[str]:
    missing = []
    if is_empty(norm['transaction_id']):
        missing.append('transaction_id')
    if is_empty(norm['user_id']):
        missing.append('user_id')
    if norm['amount'] is None:
        missing.append('amount')
    return missing


def _prior_history(valid_txs: List[Dict], idx: int, user_id: str) -> Dict[str, Any]:
    """Historique client strictement antérieur (index + ordre temporel)."""
    prior_amounts: List[float] = []
    prior_countries: Set[str] = set()
    prior_merchants: Set[str] = set()
    prior_currencies: Set[str] = set()
    prior_card_present = 0
    prior_total = 0
    prior_timestamps: List[datetime] = []

    current_ts = valid_txs[idx]['timestamp']

    for i, other in enumerate(valid_txs):
        if i >= idx or other['user_id'] != user_id:
            continue
        if current_ts and other['timestamp'] and other['timestamp'] >= current_ts:
            continue
        if other['amount'] is not None and other['amount'] > 0:
            prior_amounts.append(other['amount'])
        if other['country']:
            prior_countries.add(other['country'])
        if other['merchant']:
            prior_merchants.add(other['merchant'])
        if other['currency']:
            prior_currencies.add(other['currency'])
        if other['card_present']:
            prior_card_present += 1
        if other['timestamp']:
            prior_timestamps.append(other['timestamp'])
        prior_total += 1

    return {
        'amounts': prior_amounts,
        'countries': prior_countries,
        'merchants': prior_merchants,
        'currencies': prior_currencies,
        'card_present': prior_card_present,
        'total': prior_total,
        'timestamps': prior_timestamps,
    }


def _last_country_before(valid_txs: List[Dict], idx: int, user_id: str, timestamp: datetime):
    last_country = None
    last_time = None
    for i, other in enumerate(valid_txs):
        if i == idx or other['user_id'] != user_id:
            continue
        if not other['timestamp'] or not other['country']:
            continue
        if other['timestamp'] >= timestamp:
            continue
        if last_time is None or other['timestamp'] > last_time:
            last_country = other['country']
            last_time = other['timestamp']
    return last_country, last_time


def _count_nearby(valid_txs: List[Dict], idx: int, user_id: str, timestamp: datetime) -> int:
    return sum(
        1 for j, other in enumerate(valid_txs)
        if other['user_id'] == user_id
        and other['timestamp']
        and abs((other['timestamp'] - timestamp).total_seconds()) < FREQ_WINDOW_SEC
    )


def _is_duplicate(valid_txs: List[Dict], idx: int, norm: Dict[str, Any]) -> bool:
    """Détecte les doublons (même id ou même signature métier)."""
    tx_id = norm['transaction_id']
    seen_ids: Set[str] = set()
    for i, other in enumerate(valid_txs):
        if i >= idx:
            break
        oid = other['transaction_id']
        if oid and oid == tx_id:
            return True
        if oid:
            seen_ids.add(oid)

    for i, other in enumerate(valid_txs):
        if i >= idx:
            break
        if (
            other['user_id'] == norm['user_id']
            and other['amount'] == norm['amount']
            and other['merchant'] == norm['merchant']
            and other['timestamp'] and norm['timestamp']
            and other['timestamp'] == norm['timestamp']
        ):
            return True
    return False


def detect_fraud(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Détecteur de fraude multi-signaux avec profils clients adaptatifs.
    Ne plante jamais, même sur données imparfaites.
    """
    if not transactions:
        return []

    valid_txs: List[Dict[str, Any]] = []
    for tx in transactions:
        norm = _normalize_tx(tx if isinstance(tx, dict) else {})
        if norm is None:
            norm = {
                'tx': tx, 'transaction_id': 'unknown', 'user_id': '', 'amount': None,
                'currency': '', 'merchant': '', 'country': '', 'timestamp': None,
                'card_present': False,
            }
        valid_txs.append(norm)

    results = []
    for idx, norm in enumerate(valid_txs):
        tx_id = norm['transaction_id'] or 'unknown'
        amount = norm['amount']
        user_id = norm['user_id']
        timestamp = norm['timestamp']
        country = norm['country']
        merchant = norm['merchant']
        currency = norm['currency']
        card_present = norm['card_present']

        fraud_score = 0.0
        reasons: List[str] = []

        missing = _missing_critical_fields(norm)
        if missing:
            fraud_score = 1.0
            reasons.append(f"Champ(s) manquant(s) : {', '.join(missing)}")

        elif amount is None or amount <= 0:
            fraud_score = 1.0
            reasons.append("Montant invalide (nul ou négatif)")

        else:
            history = _prior_history(valid_txs, idx, user_id)
            prior_amounts = history['amounts']
            client_mean = mean(prior_amounts)
            client_std = std_dev(prior_amounts, client_mean)

            if _is_duplicate(valid_txs, idx, norm):
                fraud_score += 0.40
                reasons.append("Transaction dupliquée détectée")

            # Anomalie montant : IQR si historique suffisant, sinon Z-score / ratio
            amount_flagged = False
            iqr_fence = iqr_upper_fence(prior_amounts)
            if iqr_fence is not None and amount > iqr_fence:
                excess = (amount - iqr_fence) / max(iqr_fence, 1)
                fraud_score += min(0.40, 0.20 + excess * 0.05)
                reasons.append(
                    f"Montant hors plage habituelle : {amount:.2f} > seuil IQR {iqr_fence:.2f}"
                )
                amount_flagged = True
            elif client_mean > 0 and client_std > 0:
                z_score = (amount - client_mean) / client_std
                if z_score > Z_SCORE_STRONG:
                    fraud_score += 0.35
                    reasons.append(
                        f"Montant anormal : {amount:.2f} vs moyenne "
                        f"{client_mean:.2f}±{client_std:.2f} (z={z_score:.1f})"
                    )
                    amount_flagged = True
                elif z_score > Z_SCORE_MODERATE and len(prior_amounts) >= 3:
                    fraud_score += 0.15
                    reasons.append(f"Montant élevé : {amount:.2f} vs moyenne {client_mean:.2f}")
                    amount_flagged = True
            elif prior_amounts and amount > max(prior_amounts) * 3:
                fraud_score += 0.15
                reasons.append(
                    f"Montant 3× supérieur au maximum historique ({max(prior_amounts):.2f})"
                )
                amount_flagged = True

            # Pas de pénalité commerçant sur première transaction (évite faux positifs)
            if merchant and merchant not in history['merchants']:
                if len(history['merchants']) >= MIN_HISTORY_FOR_MERCHANT and not amount_flagged:
                    fraud_score += 0.05
                    reasons.append(f"Commerçant nouveau : {merchant}")

            # Devise inhabituelle (signal faible, historique requis)
            if currency and history['currencies'] and currency not in history['currencies']:
                if len(history['currencies']) >= 2:
                    fraud_score += 0.08
                    reasons.append(f"Devise inhabituelle : {currency}")

            # Carte absente vs profil
            if history['total'] >= 3:
                card_ratio = history['card_present'] / history['total']
                if not card_present and card_ratio > 0.8:
                    fraud_score += 0.10
                    reasons.append("Paiement sans carte (profil habituellement en magasin)")

            # Géographie impossible (indépendant de l'ordre du CSV)
            if timestamp and country:
                last_country, last_time = _last_country_before(
                    valid_txs, idx, user_id, timestamp
                )
                if last_country and last_country != country and last_time:
                    time_diff_h = (timestamp - last_time).total_seconds() / 3600
                    distance = calculate_distance_km(last_country, country)
                    if time_diff_h > 0 and distance / time_diff_h > MAX_TRAVEL_SPEED_KMH:
                        fraud_score += 0.25
                        reasons.append(
                            f"Déplacement impossible : {last_country}→{country} "
                            f"en {time_diff_h:.1f}h ({distance:.0f} km)"
                        )
                    elif time_diff_h < GEO_FAST_HOURS and distance > GEO_FAST_DISTANCE_KM:
                        fraud_score += 0.15
                        reasons.append(
                            f"Déplacement trop rapide : {distance:.0f} km en {time_diff_h:.1f}h"
                        )

            # Fréquence suspecte
            if timestamp:
                nearby = _count_nearby(valid_txs, idx, user_id, timestamp)
                if nearby >= FREQ_CRITICAL:
                    fraud_score += 0.55
                    reasons.append(
                        f"Fréquence excessive : {nearby} transactions en 1 minute"
                    )
                elif nearby >= FREQ_ELEVATED:
                    fraud_score += 0.15
                    reasons.append(
                        f"Fréquence élevée : {nearby} transactions en 1 minute"
                    )

        fraud_score = max(0.0, min(1.0, fraud_score))
        is_suspicious = fraud_score >= THRESHOLD_SUSPICIOUS

        if not reasons:
            reason = "Transaction normale"
            fraud_score = 0.0
            is_suspicious = False
        else:
            reason = " | ".join(reasons)

        results.append({
            'transaction_id': tx_id,
            'fraud_score': round(fraud_score, 3),
            'is_suspicious': is_suspicious,
            'reason': reason,
        })

    return results


if __name__ == "__main__":
    print("Fraud Detection Module Ready")
