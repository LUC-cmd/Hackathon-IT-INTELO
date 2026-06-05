"""Analytics avancés pour la démo jury — profils clients, patterns, explainability."""

from collections import defaultdict
from typing import List, Dict, Any
import pandas as pd


def merge_results(transactions: List[Dict], results: List[Dict]) -> pd.DataFrame:
    """Fusionne entrées et résultats de détection."""
    tx_df = pd.DataFrame(transactions)
    res_df = pd.DataFrame(results)
    if tx_df.empty:
        return res_df
    if 'transaction_id' in tx_df.columns and 'transaction_id' in res_df.columns:
        return tx_df.merge(res_df, on='transaction_id', how='left')
    return pd.concat([tx_df.reset_index(drop=True), res_df.reset_index(drop=True)], axis=1)


def client_risk_profiles(df: pd.DataFrame) -> pd.DataFrame:
    """Score de risque agrégé par client."""
    if df.empty or 'user_id' not in df.columns:
        return pd.DataFrame()

    agg = df.groupby('user_id').agg(
        transactions=('transaction_id', 'count'),
        frauds=('is_suspicious', 'sum'),
        max_score=('fraud_score', 'max'),
        avg_score=('fraud_score', 'mean'),
        total_amount=('amount', lambda s: pd.to_numeric(s, errors='coerce').sum()),
    ).reset_index()

    agg['risk_level'] = agg.apply(_risk_label, axis=1)
    agg['fraud_rate'] = (agg['frauds'] / agg['transactions'] * 100).round(1)
    return agg.sort_values('max_score', ascending=False)


def _risk_label(row) -> str:
    if row['max_score'] >= 0.8 or row['frauds'] >= 2:
        return "CRITIQUE"
    if row['max_score'] >= 0.5 or row['frauds'] >= 1:
        return "ÉLEVÉ"
    if row['avg_score'] >= 0.25:
        return "MODÉRÉ"
    return "FAIBLE"


def fraud_pattern_summary(df: pd.DataFrame) -> Dict[str, int]:
    """Compte les types de signaux détectés dans les raisons."""
    patterns = {
        'Montant invalide': 0,
        'Champ manquant': 0,
        'Montant anormal': 0,
        'Géographie': 0,
        'Fréquence': 0,
        'Doublon': 0,
        'Devise': 0,
        'Carte absente': 0,
        'Commerçant nouveau': 0,
    }
    if df.empty or 'reason' not in df.columns:
        return patterns

    keywords = {
        'Montant invalide': ['Montant invalide', 'nul ou négatif'],
        'Champ manquant': ['manquant'],
        'Montant anormal': ['Montant anormal', 'Montant élevé', 'IQR', '3×'],
        'Géographie': ['impossible', 'rapide', 'Déplacement'],
        'Fréquence': ['Fréquence'],
        'Doublon': ['dupliquée'],
        'Devise': ['Devise inhabituelle'],
        'Carte absente': ['sans carte'],
        'Commerçant nouveau': ['Commerçant nouveau'],
    }

    for reason in df['reason'].astype(str):
        for label, keys in keywords.items():
            if any(k.lower() in reason.lower() for k in keys):
                patterns[label] += 1
    return patterns


def top_alerts(df: pd.DataFrame, limit: int = 5) -> List[Dict[str, Any]]:
    """Alertes prioritaires pour le centre de commande."""
    if df.empty:
        return []
    suspicious = df[df['is_suspicious'] == True].sort_values(  # noqa: E712
        'fraud_score', ascending=False
    ).head(limit)
    alerts = []
    for _, row in suspicious.iterrows():
        alerts.append({
            'id': row.get('transaction_id', '?'),
            'user': row.get('user_id', '?'),
            'score': row.get('fraud_score', 0),
            'reason': row.get('reason', ''),
            'amount': row.get('amount', '?'),
        })
    return alerts


def explain_transaction(result: Dict[str, Any]) -> List[str]:
    """Décompose une raison en bullet points pour l'explicabilité."""
    reason = result.get('reason', '')
    if reason == 'Transaction normale':
        return ["Aucun signal de fraude détecté.", "Profil cohérent avec l'historique client."]
    return [part.strip() for part in reason.split('|') if part.strip()]


def score_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Distribution des scores pour graphiques."""
    if df.empty or 'fraud_score' not in df.columns:
        return pd.DataFrame({'bucket': [], 'count': []})
    bins = [0, 0.1, 0.25, 0.5, 0.75, 1.0]
    labels = ['0-10%', '10-25%', '25-50%', '50-75%', '75-100%']
    df = df.copy()
    df['bucket'] = pd.cut(df['fraud_score'], bins=bins, labels=labels, include_lowest=True)
    return df.groupby('bucket', observed=True).size().reset_index(name='count')


def country_risk_heatmap(df: pd.DataFrame) -> pd.DataFrame:
    """Risque moyen par pays."""
    if df.empty or 'country' not in df.columns:
        return pd.DataFrame()
    tmp = df.copy()
    tmp['country'] = tmp['country'].fillna('?')
    return (
        tmp.groupby('country')
        .agg(avg_score=('fraud_score', 'mean'), count=('transaction_id', 'count'))
        .reset_index()
        .sort_values('avg_score', ascending=False)
    )
