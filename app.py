import streamlit as st
import pandas as pd
import numpy as np
from fraud_detection import detect_fraud, load_transactions
import io

def render_interface():
    st.set_page_config(page_title="Fraud Detector AI", layout="wide", initial_sidebar_state="expanded")

    st.title("🚨 Fraud Detection AI Dashboard")
    st.markdown("*Détection intelligente des fraudes financières en temps réel*")

    with st.sidebar:
        st.header("⚙️ Configuration")
        upload_option = st.radio("Source de données", ["📤 Uploader un CSV", "📝 Données de test"])

    # Chargement des données
    if upload_option == "📤 Uploader un CSV":
        uploaded_file = st.file_uploader("Sélectionne un fichier CSV", type=['csv'])
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                transactions = df.to_dict('records')
            except Exception as e:
                st.error(f"❌ Erreur : {e}")
                return
        else:
            st.info("👈 Upload un CSV pour commencer")
            return
    else:
        transactions = [
            {'transaction_id': 'tx001', 'user_id': 'u001', 'amount': 50, 'currency': 'EUR', 'merchant': 'Boulangerie', 'country': 'FR', 'card_present': True, 'timestamp': '2024-01-15T09:30:00'},
            {'transaction_id': 'tx002', 'user_id': 'u001', 'amount': 150, 'currency': 'EUR', 'merchant': 'Restaurant', 'country': 'FR', 'card_present': False, 'timestamp': '2024-01-15T12:45:00'},
            {'transaction_id': 'tx003', 'user_id': 'u001', 'amount': 5000, 'currency': 'EUR', 'merchant': 'Electronique', 'country': 'JP', 'card_present': False, 'timestamp': '2024-01-15T13:00:00'},
            {'transaction_id': 'tx004', 'user_id': 'u002', 'amount': 75, 'currency': 'EUR', 'merchant': 'Supermarché', 'country': 'FR', 'card_present': True, 'timestamp': '2024-01-15T14:20:00'},
            {'transaction_id': 'tx005', 'user_id': 'u002', 'amount': 80, 'currency': 'EUR', 'merchant': 'Pharmacie', 'country': 'FR', 'card_present': True, 'timestamp': '2024-01-15T14:25:00'},
            {'transaction_id': 'tx006', 'user_id': 'u003', 'amount': -100, 'currency': 'EUR', 'merchant': 'Inconnu', 'country': 'US', 'card_present': False, 'timestamp': '2024-01-15T15:00:00'},
        ]

    # Détection
    if not transactions:
        st.error("❌ Aucune transaction à analyser")
        return

    st.info(f"📊 Analyse en cours... ({len(transactions)} transactions)")
    results = detect_fraud(transactions)

    # Création du dataframe résultat
    results_df = pd.DataFrame(results)

    # Statistiques
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total", len(results_df), "transactions")
    with col2:
        suspicious = sum(results_df['is_suspicious'])
        st.metric("🚨 Fraudes", suspicious, f"{suspicious/len(results_df)*100:.1f}%")
    with col3:
        high_risk = sum(results_df['fraud_score'] > 0.7)
        st.metric("⚠️ Haut Risque", high_risk, f"score > 0.7")
    with col4:
        avg_score = results_df['fraud_score'].mean()
        st.metric("📈 Score Moyen", f"{avg_score:.3f}", "")

    # Visualisations
    st.subheader("📊 Analyse Détaillée")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Distribution des Scores de Fraude**")
        fig_data = results_df['fraud_score'].value_counts().sort_index()
        st.bar_chart(results_df['fraud_score'].hist(bins=20, edgecolor='black'))

    with col2:
        st.markdown("**Répartition Risque/Normal**")
        risk_counts = results_df['is_suspicious'].value_counts()
        labels = ["✅ Normal", "🚨 Fraude"]
        colors = ["#2ecc71", "#e74c3c"]
        st.write(risk_counts)

    # Tableau détaillé
    st.subheader("🔍 Détails des Transactions")

    filter_option = st.selectbox(
        "Filtrer par :",
        ["Toutes", "Fraudes seulement", "Score > 0.5", "Score > 0.7"]
    )

    if filter_option == "Fraudes seulement":
        display_df = results_df[results_df['is_suspicious']]
    elif filter_option == "Score > 0.5":
        display_df = results_df[results_df['fraud_score'] > 0.5]
    elif filter_option == "Score > 0.7":
        display_df = results_df[results_df['fraud_score'] > 0.7]
    else:
        display_df = results_df

    # Format pour affichage
    display_df_formatted = display_df.copy()
    display_df_formatted['fraud_score'] = display_df_formatted['fraud_score'].apply(lambda x: f"{x:.3f}")
    display_df_formatted['is_suspicious'] = display_df_formatted['is_suspicious'].apply(lambda x: "🚨 OUI" if x else "✅ NON")

    st.dataframe(display_df_formatted, use_container_width=True, height=400)

    # Export
    st.subheader("💾 Export")
    csv = results_df.to_csv(index=False)
    st.download_button(
        label="📥 Télécharger résultats CSV",
        data=csv,
        file_name="fraud_detection_results.csv",
        mime="text/csv"
    )

    # Footer
    st.divider()
    st.markdown("---")
    st.markdown("🤖 *Powered by Advanced Fraud Detection AI | Hackathon IT 2026*")

if __name__ == "__main__":
    render_interface()
