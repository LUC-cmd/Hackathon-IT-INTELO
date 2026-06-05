import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from fraud_detection import detect_fraud, load_transactions
from insights import (
    merge_results,
    client_risk_profiles,
    fraud_pattern_summary,
    top_alerts,
    explain_transaction,
    score_distribution,
    country_risk_heatmap,
)

DEMO_TRANSACTIONS = [
    {'transaction_id': 'tx001', 'user_id': 'u001', 'amount': 50, 'currency': 'EUR',
     'merchant': 'Boulangerie', 'country': 'FR', 'card_present': True,
     'timestamp': '2024-01-15T09:30:00'},
    {'transaction_id': 'tx002', 'user_id': 'u001', 'amount': 55, 'currency': 'EUR',
     'merchant': 'Café', 'country': 'FR', 'card_present': True,
     'timestamp': '2024-01-15T10:00:00'},
    {'transaction_id': 'tx003', 'user_id': 'u001', 'amount': 52, 'currency': 'EUR',
     'merchant': 'Supermarché', 'country': 'FR', 'card_present': True,
     'timestamp': '2024-01-15T11:00:00'},
    {'transaction_id': 'tx004', 'user_id': 'u001', 'amount': 5000, 'currency': 'EUR',
     'merchant': 'Electronique', 'country': 'JP', 'card_present': False,
     'timestamp': '2024-01-15T13:00:00'},
    {'transaction_id': 'tx005', 'user_id': 'u002', 'amount': 75, 'currency': 'EUR',
     'merchant': 'Supermarché', 'country': 'FR', 'card_present': True,
     'timestamp': '2024-01-15T14:20:00'},
    {'transaction_id': 'tx006', 'user_id': 'u002', 'amount': 80, 'currency': 'EUR',
     'merchant': 'Pharmacie', 'country': 'FR', 'card_present': True,
     'timestamp': '2024-01-15T14:25:00'},
    {'transaction_id': 'tx007', 'user_id': 'u003', 'amount': -100, 'currency': 'EUR',
     'merchant': 'Inconnu', 'country': 'US', 'card_present': False,
     'timestamp': '2024-01-15T15:00:00'},
    {'transaction_id': 'tx008', 'user_id': 'u004', 'amount': 120, 'currency': 'EUR',
     'merchant': 'Shop', 'country': 'FR', 'card_present': True,
     'timestamp': '2024-01-15T16:00:00'},
    {'transaction_id': 'tx008', 'user_id': 'u004', 'amount': 120, 'currency': 'EUR',
     'merchant': 'Shop', 'country': 'FR', 'card_present': True,
     'timestamp': '2024-01-15T16:00:00'},
]


def _inject_css():
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        padding: 1.5rem 2rem; border-radius: 12px; margin-bottom: 1.5rem;
        border: 1px solid #4a4a8a;
    }
    .main-header h1 { color: #fff; margin: 0; font-size: 2rem; }
    .main-header p { color: #a0a0d0; margin: 0.3rem 0 0 0; }
    .alert-card {
        background: #1a1a2e; border-left: 4px solid #e74c3c;
        padding: 0.8rem 1rem; border-radius: 8px; margin: 0.4rem 0;
    }
    .metric-box {
        background: #16213e; padding: 1rem; border-radius: 10px;
        text-align: center; border: 1px solid #0f3460;
    }
    div[data-testid="stMetricValue"] { font-size: 1.8rem; }
    </style>
    """, unsafe_allow_html=True)


def _load_data(source: str, uploaded_file):
    if source == "CSV upload":
        if not uploaded_file:
            return None
        df = pd.read_csv(uploaded_file)
        return df.to_dict('records')
    if source == "sample_data.csv":
        return load_transactions("sample_data.csv")
    return DEMO_TRANSACTIONS


def render_interface():
    st.set_page_config(
        page_title="ShieldAI — Fraud Command Center",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    _inject_css()

    st.markdown("""
    <div class="main-header">
        <h1>🛡️ ShieldAI — Fraud Command Center</h1>
        <p>Détection multi-signaux · Profils clients adaptatifs · Explicabilité en temps réel</p>
    </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/shield.png", width=64)
        st.markdown("### ⚙️ Configuration")
        source = st.radio(
            "Source de données",
            ["Démo scénario complet", "sample_data.csv", "CSV upload"],
        )
        uploaded = st.file_uploader("Fichier CSV", type=["csv"]) if source == "CSV upload" else None
        threshold = st.slider("Seuil d'alerte", 0.3, 0.9, 0.5, 0.05)
        st.markdown("---")
        st.markdown("**Signaux détectés**")
        st.markdown("""
        - Montant (Z-score + IQR)
        - Géographie impossible
        - Fréquence anormale
        - Doublons & champs manquants
        - Devise & comportement carte
        """)
        st.markdown("---")
        st.caption("Hackathon IT 2026 · Lomé Business School")

    transactions = _load_data(source, uploaded)
    if transactions is None:
        st.info("👈 Uploadez un CSV pour commencer")
        return
    if not transactions:
        st.error("Aucune transaction trouvée")
        return

    results = detect_fraud(transactions)
    df = merge_results(transactions, results)
    df['is_suspicious'] = df['fraud_score'] >= threshold

    tab_cmd, tab_tx, tab_clients, tab_intel, tab_sim = st.tabs([
        "🎯 Centre de commande",
        "🔍 Transactions",
        "👤 Profils clients",
        "🧠 Intelligence fraude",
        "⚡ Simulateur live",
    ])

    # ── TAB 1 : Centre de commande ──
    with tab_cmd:
        total = len(df)
        frauds = int(df['is_suspicious'].sum())
        high = int((df['fraud_score'] > 0.7).sum())
        avg = df['fraud_score'].mean()

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Transactions", total)
        c2.metric("🚨 Alertes", frauds, f"{frauds/total*100:.1f}%")
        c3.metric("Critiques (>0.7)", high)
        c4.metric("Score moyen", f"{avg:.3f}")
        c5.metric("Clients", df['user_id'].nunique() if 'user_id' in df.columns else 0)

        col_left, col_right = st.columns([1, 1])
        with col_left:
            st.subheader("🔴 Alertes prioritaires")
            alerts = top_alerts(df)
            if alerts:
                for a in alerts:
                    st.markdown(f"""
                    <div class="alert-card">
                        <strong>{a['id']}</strong> · Client {a['user']} ·
                        Score <strong>{a['score']:.3f}</strong><br>
                        <small>{a['reason'][:120]}</small>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("Aucune alerte active")

        with col_right:
            st.subheader("📊 Distribution des scores")
            dist = score_distribution(df)
            if not dist.empty:
                fig = px.bar(dist, x='bucket', y='count', color='count',
                               color_continuous_scale='Reds', title="Répartition du risque")
                fig.update_layout(showlegend=False, height=350,
                                  plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)

    # ── TAB 2 : Transactions ──
    with tab_tx:
        filt = st.selectbox("Filtrer", ["Toutes", "Suspectes", "Score > 0.7", "Normales"])
        view = df.copy()
        if filt == "Suspectes":
            view = view[view['is_suspicious']]
        elif filt == "Score > 0.7":
            view = view[view['fraud_score'] > 0.7]
        elif filt == "Normales":
            view = view[~view['is_suspicious']]

        st.dataframe(
            view.sort_values('fraud_score', ascending=False),
            use_container_width=True,
            height=400,
        )

        sel_id = st.selectbox(
            "Explicabilité — choisir une transaction",
            df['transaction_id'].tolist(),
        )
        row = df[df['transaction_id'] == sel_id].iloc[0]
        res = next((r for r in results if r['transaction_id'] == sel_id), results[0])

        st.subheader(f"🔎 Explication — {sel_id}")
        bullets = explain_transaction(res)
        for b in bullets:
            st.markdown(f"- {b}")

        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=res['fraud_score'],
            title={'text': "Score de fraude"},
            gauge={
                'axis': {'range': [0, 1]},
                'bar': {'color': '#e74c3c' if res['is_suspicious'] else '#2ecc71'},
                'steps': [
                    {'range': [0, 0.5], 'color': '#1a472a'},
                    {'range': [0.5, 0.75], 'color': '#7d4e00'},
                    {'range': [0.75, 1], 'color': '#4a0e0e'},
                ],
            },
        ))
        gauge.update_layout(height=250)
        st.plotly_chart(gauge, use_container_width=True)

    # ── TAB 3 : Profils clients ──
    with tab_clients:
        profiles = client_risk_profiles(df)
        if profiles.empty:
            st.warning("Pas de profils disponibles")
        else:
            st.subheader("Classement des clients par risque")
            st.dataframe(profiles, use_container_width=True)

            fig = px.scatter(
                profiles, x='transactions', y='max_score',
                size='frauds', color='risk_level',
                hover_name='user_id',
                color_discrete_map={
                    'CRITIQUE': '#e74c3c', 'ÉLEVÉ': '#e67e22',
                    'MODÉRÉ': '#f1c40f', 'FAIBLE': '#2ecc71',
                },
                title="Carte de risque clients",
            )
            fig.update_layout(height=400, plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

    # ── TAB 4 : Intelligence ──
    with tab_intel:
        patterns = fraud_pattern_summary(df)
        st.subheader("Types de fraude détectés")
        pat_df = pd.DataFrame(list(patterns.items()), columns=['Pattern', 'Occurrences'])
        pat_df = pat_df[pat_df['Occurrences'] > 0]
        if not pat_df.empty:
            fig = px.pie(pat_df, values='Occurrences', names='Pattern', hole=0.4,
                         title="Répartition des signaux")
            st.plotly_chart(fig, use_container_width=True)

        geo = country_risk_heatmap(df)
        if not geo.empty:
            st.subheader("Risque par pays")
            fig2 = px.bar(geo, x='country', y='avg_score', color='avg_score',
                          color_continuous_scale='Reds', title="Score moyen par pays")
            st.plotly_chart(fig2, use_container_width=True)

        if 'timestamp' in df.columns and 'fraud_score' in df.columns:
            st.subheader("Timeline des scores")
            tmp = df.copy()
            tmp['timestamp'] = pd.to_datetime(tmp['timestamp'], errors='coerce')
            tmp = tmp.dropna(subset=['timestamp']).sort_values('timestamp')
            if not tmp.empty:
                fig3 = px.scatter(tmp, x='timestamp', y='fraud_score',
                                  color='is_suspicious', hover_data=['transaction_id', 'user_id'],
                                  title="Évolution temporelle du risque")
                st.plotly_chart(fig3, use_container_width=True)

    # ── TAB 5 : Simulateur ──
    with tab_sim:
        st.subheader("⚡ Tester une transaction en direct")
        st.caption("Ajoutez une transaction fictive et voyez le verdict instantanément")

        c1, c2, c3 = st.columns(3)
        sim_id = c1.text_input("ID", "sim_001")
        sim_user = c2.text_input("Client", "u001")
        sim_amount = c3.number_input("Montant", 0.0, 50000.0, 5000.0)
        c4, c5, c6 = st.columns(3)
        sim_country = c4.text_input("Pays", "JP")
        sim_merchant = c5.text_input("Commerçant", "Luxury Store")
        sim_card = c6.checkbox("Carte présente", False)

        if st.button("🚀 Analyser", type="primary"):
            sim_tx = {
                'transaction_id': sim_id,
                'user_id': sim_user,
                'amount': sim_amount,
                'currency': 'EUR',
                'merchant': sim_merchant,
                'country': sim_country,
                'card_present': sim_card,
                'timestamp': '2024-01-15T18:00:00',
            }
            batch = transactions + [sim_tx]
            sim_result = detect_fraud(batch)[-1]

            if sim_result['is_suspicious']:
                st.error(f"🚨 SUSPECT — Score {sim_result['fraud_score']:.3f}")
            else:
                st.success(f"✅ NORMAL — Score {sim_result['fraud_score']:.3f}")
            for b in explain_transaction(sim_result):
                st.markdown(f"- {b}")

    st.divider()
    csv_out = pd.DataFrame(results).to_csv(index=False)
    st.download_button("📥 Exporter résultats CSV", csv_out,
                       "shieldai_fraud_results.csv", "text/csv")
    st.caption("ShieldAI · Hackathon IT 2026 · Lomé Business School")


if __name__ == "__main__":
    render_interface()
