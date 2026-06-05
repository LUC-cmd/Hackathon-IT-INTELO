import streamlit as st
import pandas as pd
import numpy as np
from fraud_detection_v2 import detect_fraud
from datetime import datetime, timedelta
import math

def render_interface():
    st.set_page_config(
        page_title="Fraud Detection - Enterprise",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Header professionnel
    col1, col2 = st.columns([0.7, 0.3])
    with col1:
        st.title("🚨 Fraud Detection AI - Enterprise")
        st.markdown("*Système bancaire intelligent de détection de fraude en temps réel*")
    with col2:
        st.metric("Status", "🟢 ONLINE", "Prêt")

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        mode = st.radio("Mode", ["Demo", "Upload CSV"])

        if mode == "Demo":
            transactions = generate_sample_data()
        else:
            uploaded = st.file_uploader("Charge CSV", type=['csv'])
            if uploaded:
                try:
                    df = pd.read_csv(uploaded)
                    transactions = df.to_dict('records')
                except:
                    st.error("Erreur chargement")
                    return
            else:
                st.info("Charge un CSV pour démarrer")
                return

    if not transactions:
        return

    st.divider()

    # LANCER DETECTION
    results = detect_fraud(transactions)
    results_df = pd.DataFrame(results)

    # ===== SECTION 1: KPIs =====
    st.subheader("📊 KPIs Clés")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Transactions",
            len(results_df),
            "analysées"
        )

    with col2:
        suspicious = sum(results_df['is_suspicious'])
        pct = (suspicious / len(results_df) * 100) if results_df.shape[0] > 0 else 0
        st.metric(
            "🚨 Fraudes",
            suspicious,
            f"{pct:.1f}%"
        )

    with col3:
        high_risk = sum(results_df['fraud_score'] > 0.7)
        st.metric(
            "⚠️ Haut Risque",
            high_risk,
            "score > 0.7"
        )

    with col4:
        total_amount = sum(t.get('amount', 0) for t in transactions if t.get('amount', 0) > 0)
        st.metric(
            "💰 Total",
            f"€{total_amount:,.0f}",
            "transactions"
        )

    with col5:
        avg_score = results_df['fraud_score'].mean()
        st.metric(
            "📈 Risque Moyen",
            f"{avg_score:.3f}",
            "0.0-1.0"
        )

    st.divider()

    # ===== SECTION 2: Analyse Détaillée =====
    st.subheader("📈 Analyse Détaillée")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Distribution des Scores**")
        fig_hist = st.bar_chart(
            results_df['fraud_score'].astype(float).hist(bins=20).value_counts()
        )

    with col2:
        st.markdown("**Répartition Risque**")
        risk_dist = pd.Series({
            'Faible (0-0.3)': sum(results_df['fraud_score'] < 0.3),
            'Moyen (0.3-0.6)': sum((results_df['fraud_score'] >= 0.3) & (results_df['fraud_score'] < 0.6)),
            'Haut (0.6-0.8)': sum((results_df['fraud_score'] >= 0.6) & (results_df['fraud_score'] < 0.8)),
            'Critique (>0.8)': sum(results_df['fraud_score'] >= 0.8),
        })
        st.bar_chart(risk_dist)

    with col3:
        st.markdown("**Verdict**")
        verdict = pd.Series({
            '✅ Légitime': sum(~results_df['is_suspicious']),
            '🚨 Suspect': sum(results_df['is_suspicious']),
        })
        st.bar_chart(verdict)

    st.divider()

    # ===== SECTION 3: Tableau Détaillé =====
    st.subheader("🔍 Transactions Détaillées")

    filter_col = st.selectbox(
        "Filtrer par risque",
        ["Toutes", "Suspectes", "Score > 0.5", "Score > 0.7", "Score > 0.8"]
    )

    if filter_col == "Suspectes":
        display_df = results_df[results_df['is_suspicious']]
    elif filter_col == "Score > 0.5":
        display_df = results_df[results_df['fraud_score'] > 0.5]
    elif filter_col == "Score > 0.7":
        display_df = results_df[results_df['fraud_score'] > 0.7]
    elif filter_col == "Score > 0.8":
        display_df = results_df[results_df['fraud_score'] > 0.8]
    else:
        display_df = results_df

    # Format pour affichage
    display_data = display_df.copy()
    display_data['fraud_score'] = display_data['fraud_score'].apply(lambda x: f"{x:.3f}")
    display_data['is_suspicious'] = display_data['is_suspicious'].apply(lambda x: "🚨 OUI" if x else "✅ NON")

    st.dataframe(
        display_data[['transaction_id', 'fraud_score', 'is_suspicious', 'reason']],
        use_container_width=True,
        height=400
    )

    # ===== SECTION 4: Détails Avancés =====
    if st.checkbox("Afficher détails avancés"):
        st.subheader("🔬 Détails Moteurs")

        suspicious_txs = results_df[results_df['is_suspicious']]
        if len(suspicious_txs) > 0:
            for idx, row in suspicious_txs.head(5).iterrows():
                with st.expander(f"Transaction {row['transaction_id']} (Score: {row['fraud_score']:.3f})"):
                    st.write(f"**Raison:** {row['reason']}")
                    if 'details' in row and isinstance(row['details'], dict):
                        for key, val in row['details'].items():
                            st.write(f"- {key}: {val}")

    st.divider()

    # ===== SECTION 5: Export & Stats =====
    col1, col2 = st.columns(2)

    with col1:
        csv = results_df.to_csv(index=False)
        st.download_button(
            "📥 Export CSV",
            data=csv,
            file_name=f"fraud_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

    with col2:
        st.info(f"📊 Rapport généré à {datetime.now().strftime('%H:%M:%S')}")

    # Footer
    st.divider()
    st.markdown(
        "---\n"
        "🤖 **Fraud Detection AI v2.0** | "
        "*Moteurs avancés: DNA, Trust, Card Testing, Travel, Behavior*\n"
        "Hackathon IT 2026 - Lomé Business School"
    )


def generate_sample_data():
    """Génère des données de démo réalistes"""
    return [
        {
            'transaction_id': 'tx001', 'user_id': 'u001', 'amount': 50, 'currency': 'EUR',
            'merchant': 'Boulangerie', 'country': 'FR', 'card_present': True,
            'timestamp': '2024-01-15T09:30:00'
        },
        {
            'transaction_id': 'tx002', 'user_id': 'u001', 'amount': 150, 'currency': 'EUR',
            'merchant': 'Restaurant', 'country': 'FR', 'card_present': False,
            'timestamp': '2024-01-15T12:45:00'
        },
        {
            'transaction_id': 'tx003', 'user_id': 'u001', 'amount': 5000, 'currency': 'EUR',
            'merchant': 'Electronique', 'country': 'JP', 'card_present': False,
            'timestamp': '2024-01-15T13:00:00'
        },
        {
            'transaction_id': 'tx004', 'user_id': 'u002', 'amount': 75, 'currency': 'EUR',
            'merchant': 'Supermarche', 'country': 'FR', 'card_present': True,
            'timestamp': '2024-01-15T14:20:00'
        },
        {
            'transaction_id': 'tx005', 'user_id': 'u002', 'amount': 1.00, 'currency': 'EUR',
            'merchant': 'Inconnu', 'country': 'FR', 'card_present': False,
            'timestamp': '2024-01-15T14:25:00'
        },
        {
            'transaction_id': 'tx006', 'user_id': 'u002', 'amount': 0.75, 'currency': 'EUR',
            'merchant': 'Inconnu2', 'country': 'FR', 'card_present': False,
            'timestamp': '2024-01-15T14:26:00'
        },
        {
            'transaction_id': 'tx007', 'user_id': 'u002', 'amount': 3000, 'currency': 'EUR',
            'merchant': 'Electronique', 'country': 'FR', 'card_present': False,
            'timestamp': '2024-01-15T14:27:00'
        },
        {
            'transaction_id': 'tx008', 'user_id': 'u003', 'amount': 100, 'currency': 'EUR',
            'merchant': 'Hotel', 'country': 'FR', 'card_present': True,
            'timestamp': '2024-01-15T15:00:00'
        },
        {
            'transaction_id': 'tx009', 'user_id': 'u003', 'amount': 100, 'currency': 'USD',
            'merchant': 'Restaurant', 'country': 'US', 'card_present': False,
            'timestamp': '2024-01-15T15:30:00'
        },
        {
            'transaction_id': 'tx010', 'user_id': 'u004', 'amount': -100, 'currency': 'EUR',
            'merchant': 'Refund', 'country': 'FR', 'card_present': False,
            'timestamp': '2024-01-15T16:00:00'
        },
    ]


if __name__ == "__main__":
    render_interface()
