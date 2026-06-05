"""
Moteurs de Détection de Fraude Avancés
Système bancaire professionnel avec 5 moteurs indépendants
"""

from datetime import datetime, timedelta
from collections import defaultdict
import math

class FraudDNAEngine:
    """ADN Financier - Profil comportemental unique du client"""

    def __init__(self):
        self.dna_profiles = {}

    def build_dna(self, transactions, user_id):
        """Construit le profil DNA d'un utilisateur"""
        user_txs = [t for t in transactions if t.get('user_id') == user_id]

        if not user_txs:
            return None

        amounts = []
        countries = defaultdict(int)
        merchants = defaultdict(int)
        hours = defaultdict(int)

        for tx in user_txs:
            amt = tx.get('amount')
            if amt and amt > 0:
                amounts.append(amt)

            country = str(tx.get('country', '')).upper()
            if country:
                countries[country] += 1

            merchant = str(tx.get('merchant', '')).lower()
            if merchant:
                merchants[merchant] += 1

            ts = tx.get('timestamp')
            if ts:
                try:
                    dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                    hours[dt.hour] += 1
                except:
                    pass

        mean_amount = sum(amounts) / len(amounts) if amounts else 0
        median_amount = sorted(amounts)[len(amounts)//2] if amounts else 0

        return {
            'amount_mean': mean_amount,
            'amount_median': median_amount,
            'amount_min': min(amounts) if amounts else 0,
            'amount_max': max(amounts) if amounts else 0,
            'countries': dict(countries),
            'merchants': dict(merchants),
            'active_hours': dict(hours),
            'tx_count': len(user_txs),
        }

    def calculate_dna_match(self, tx, dna):
        """Calcule le % de similarité avec le DNA (0-100)"""
        if not dna or dna['tx_count'] < 2:
            return 50  # Neutral si pas d'historique

        score = 0
        factors = 0

        # Match montant
        amount = tx.get('amount', 0)
        if amount and amount > 0:
            mean = dna['amount_mean']
            if mean > 0:
                ratio = min(amount, mean) / max(amount, mean)
                score += ratio * 25  # 25 points max
            factors += 1

        # Match pays
        country = str(tx.get('country', '')).upper()
        if country and country in dna['countries']:
            score += 25  # 25 points si pays connu
        factors += 1

        # Match commerçant
        merchant = str(tx.get('merchant', '')).lower()
        if merchant and merchant in dna['merchants']:
            score += 25  # 25 points si commerçant connu
        factors += 1

        # Match horaire
        ts = tx.get('timestamp')
        if ts:
            try:
                dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                if dt.hour in dna['active_hours']:
                    score += 25  # 25 points si heure habituelle
                factors += 1
            except:
                pass

        return int((score / (factors * 25) * 100)) if factors > 0 else 50


class TrustScoreEngine:
    """Score de Confiance - Basé sur historique et cohérence"""

    def calculate_trust_score(self, transactions, user_id):
        """Calcule 0-100 basé sur fiabilité historique"""
        user_txs = [t for t in transactions if t.get('user_id') == user_id]

        if not user_txs:
            return 50  # Nouveau client = neutre

        score = 50

        # Facteur 1: Ancienneté
        if len(user_txs) > 50:
            score += 20
        elif len(user_txs) > 20:
            score += 10
        elif len(user_txs) < 3:
            score -= 15

        # Facteur 2: Cohérence comportementale
        amounts = [t.get('amount', 0) for t in user_txs if t.get('amount', 0) > 0]
        if amounts:
            mean = sum(amounts) / len(amounts)
            variance = sum((x - mean) ** 2 for x in amounts) / len(amounts)
            std = math.sqrt(variance)

            # Coefficient de variation
            cv = (std / mean) if mean > 0 else 1
            if cv < 0.3:
                score += 15  # Très cohérent
            elif cv < 0.8:
                score += 5
            elif cv > 2:
                score -= 10  # Très volatil

        # Facteur 3: Pas d'incidents (pas de montants anormaux)
        abnormal = sum(1 for t in user_txs
                      if t.get('amount', 0) and t.get('amount') > mean * 5)
        if abnormal == 0 and len(user_txs) > 5:
            score += 15

        return max(0, min(100, score))


class CardTestDetectionEngine:
    """Détection des tests de carte bancaire"""

    def detect_card_testing(self, transactions, user_id):
        """Détecte 0.50€, 1€, etc suivis d'achat important"""
        user_txs = sorted(
            [t for t in transactions if t.get('user_id') == user_id],
            key=lambda x: x.get('timestamp', ''),
        )

        if len(user_txs) < 2:
            return None

        # Pattern: petits montants (< 2€) suivis de gros montant
        test_amounts = [0.50, 0.75, 1.0, 1.50, 2.0]

        for i in range(len(user_txs) - 2):
            curr = user_txs[i].get('amount', 0)
            if curr and curr in test_amounts or (0 < curr < 2):
                # Vérifier les 2-3 transactions suivantes
                test_count = 1
                for j in range(i + 1, min(i + 4, len(user_txs))):
                    next_amt = user_txs[j].get('amount', 0)
                    if next_amt and (next_amt in test_amounts or (0 < next_amt < 2)):
                        test_count += 1

                # Puis gros montant après tests
                if test_count >= 2 and i + test_count < len(user_txs):
                    final_amt = user_txs[i + test_count].get('amount', 0)
                    if final_amt and final_amt > 100:
                        return {
                            'detected': True,
                            'test_count': test_count,
                            'test_amounts': [user_txs[i + k].get('amount') for k in range(test_count)],
                            'final_amount': final_amt,
                            'risk': 0.8
                        }

        return None


class TravelDetectionEngine:
    """Détection de voyages et impossibilités physiques"""

    DISTANCE_MATRIX = {
        'FR': (48.8566, 2.3522), 'US': (37.7749, -122.4194), 'GB': (51.5074, -0.1278),
        'DE': (52.5200, 13.4050), 'IT': (41.9028, 12.4964), 'ES': (40.4168, -3.7038),
        'BF': (12.3714, -1.5197), 'CI': (6.8276, -5.2893), 'SN': (14.7167, -17.4674),
        'ML': (12.6392, -8.0029), 'NE': (13.5116, 2.1257), 'TG': (6.1256, 1.2317),
        'BE': (50.8503, 4.3517), 'NL': (52.3676, 4.9041), 'CH': (46.9479, 7.4474),
        'AT': (48.2082, 16.3738), 'PL': (52.2297, 21.0122), 'SE': (59.3293, 18.0686),
        'JP': (35.6762, 139.6503), 'CN': (39.9042, 116.4074), 'IN': (28.6139, 77.2090),
        'BR': (-23.5505, -46.6333), 'MX': (19.4326, -99.1332), 'AU': (-33.8688, 151.2093),
    }

    @staticmethod
    def distance(c1, c2):
        if c1 not in TravelDetectionEngine.DISTANCE_MATRIX or c2 not in TravelDetectionEngine.DISTANCE_MATRIX:
            return 0
        lat1, lon1 = TravelDetectionEngine.DISTANCE_MATRIX[c1]
        lat2, lon2 = TravelDetectionEngine.DISTANCE_MATRIX[c2]
        return math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2) * 111

    def detect_travel_pattern(self, transactions, user_id):
        """Détecte voyage ou impossibilité"""
        user_txs = sorted(
            [t for t in transactions if t.get('user_id') == user_id],
            key=lambda x: x.get('timestamp', ''),
        )

        results = []
        for i in range(len(user_txs) - 1):
            c1 = str(user_txs[i].get('country', '')).upper()
            c2 = str(user_txs[i + 1].get('country', '')).upper()

            if not c1 or not c2 or c1 == c2:
                continue

            t1 = user_txs[i].get('timestamp')
            t2 = user_txs[i + 1].get('timestamp')

            if not t1 or not t2:
                continue

            try:
                dt1 = datetime.fromisoformat(t1.replace('Z', '+00:00'))
                dt2 = datetime.fromisoformat(t2.replace('Z', '+00:00'))
                hours = (dt2 - dt1).total_seconds() / 3600
            except:
                continue

            if hours <= 0:
                continue

            distance = self.distance(c1, c2)
            speed = distance / hours if hours > 0 else 0

            # Légitime voyage (8h+ pour distances longues)
            if hours > 8 and distance > 1000:
                continue

            results.append({
                'from': c1,
                'to': c2,
                'distance_km': distance,
                'hours': hours,
                'speed_kmh': speed,
                'risk': 0.95 if speed > 900 else (0.60 if speed > 500 else 0.30)
            })

        return results


class BehaviorAnomalyEngine:
    """Détection des anomalies comportementales (horaires, fréquence)"""

    def detect_anomalies(self, transactions, user_id, current_tx):
        """Détecte horaires inhabituels et fréquence"""
        user_txs = [t for t in transactions if t.get('user_id') == user_id]

        anomalies = []

        # Anomalie 1: Horaire inhabituel
        ct = current_tx.get('timestamp')
        if ct:
            try:
                curr_hour = datetime.fromisoformat(ct.replace('Z', '+00:00')).hour
                hours = defaultdict(int)
                for t in user_txs:
                    ts = t.get('timestamp')
                    if ts:
                        try:
                            h = datetime.fromisoformat(ts.replace('Z', '+00:00')).hour
                            hours[h] += 1
                        except:
                            pass

                if hours and curr_hour not in hours and hours:
                    anomalies.append({
                        'type': 'unusual_hour',
                        'hour': curr_hour,
                        'usual_hours': list(hours.keys()),
                        'risk': 0.15
                    })
            except:
                pass

        # Anomalie 2: Burst de transactions
        if ct:
            try:
                curr_time = datetime.fromisoformat(ct.replace('Z', '+00:00'))
                recent = sum(1 for t in user_txs
                           if t.get('timestamp') and
                           (datetime.fromisoformat(t['timestamp'].replace('Z', '+00:00')) - curr_time).total_seconds() < 300)

                if recent >= 4:
                    anomalies.append({
                        'type': 'burst',
                        'count': recent,
                        'window_seconds': 300,
                        'risk': 0.40
                    })
            except:
                pass

        return anomalies
