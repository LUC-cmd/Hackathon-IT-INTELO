import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import csv
import json
from datetime import datetime
from fraud_detection import detect_fraud, load_transactions

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
]


def load_csv_simple(file_obj):
    """Load CSV without pandas."""
    try:
        content = file_obj.read().decode('utf-8')
        reader = csv.DictReader(content.splitlines())
        transactions = []
        for row in reader:
            # Convert amount to float
            if 'amount' in row:
                try:
                    row['amount'] = float(row['amount'])
                except:
                    pass
            transactions.append(row)
        return transactions
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return []


def render_interface():
    st.set_page_config(
        page_title="ShieldAI — Fraud Detection",
        page_icon="🛡️",
        layout="wide",
    )

    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        padding: 1.5rem 2rem; border-radius: 12px; margin-bottom: 1.5rem;
        border: 1px solid #4a4a8a;
    }
    .main-header h1 { color: #fff; margin: 0; font-size: 2rem; }
    .main-header p { color: #a0a0d0; margin: 0.3rem 0 0 0; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="main-header">
        <h1>🛡️ ShieldAI — Fraud Command Center</h1>
        <p>Multi-signal fraud detection · Adaptive client profiles · Real-time explainability</p>
    </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        source = st.radio(
            "Data source",
            ["Demo scenario", "sample_data.csv", "CSV upload"],
        )
        uploaded = st.file_uploader("CSV File", type=["csv"]) if source == "CSV upload" else None
        threshold = st.slider("Alert threshold", 0.3, 0.9, 0.5, 0.05)
        st.markdown("---")
        st.markdown("**Detected signals**")
        st.markdown("""
        - Amount (Z-score + IQR)
        - Geographic impossibility
        - Frequency anomaly
        - Duplicates & missing fields
        - Currency & card behavior
        """)

    # Load data
    transactions = None
    if source == "Demo scenario":
        transactions = DEMO_TRANSACTIONS
    elif source == "sample_data.csv":
        transactions = load_transactions("sample_data.csv")
    elif source == "CSV upload" and uploaded:
        transactions = load_csv_simple(uploaded)

    if transactions is None or not transactions:
        st.warning("No transactions loaded. Please select a data source.")
        return

    # Detect fraud
    results = detect_fraud(transactions)

    # Merge results with transactions
    merged = []
    for tx, res in zip(transactions, results):
        row = dict(tx)
        row.update(res)
        row['is_suspicious'] = res['fraud_score'] >= threshold
        merged.append(row)

    # Display metrics
    total = len(merged)
    frauds = sum(1 for r in merged if r['is_suspicious'])
    high = sum(1 for r in merged if r['fraud_score'] > 0.7)
    avg_score = sum(r['fraud_score'] for r in merged) / total if total > 0 else 0
    unique_users = len(set(r.get('user_id', '') for r in merged))

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Transactions", total)
    col2.metric("🚨 Alerts", frauds, f"{frauds/total*100:.1f}%" if total > 0 else "0%")
    col3.metric("Critical (>0.7)", high)
    col4.metric("Avg Score", f"{avg_score:.3f}")
    col5.metric("Clients", unique_users)

    # Filter transactions
    st.markdown("---")
    st.subheader("Transactions")
    filter_type = st.selectbox("Filter", ["All", "Suspicious", "Score > 0.7", "Normal"])

    filtered = merged
    if filter_type == "Suspicious":
        filtered = [r for r in merged if r['is_suspicious']]
    elif filter_type == "Score > 0.7":
        filtered = [r for r in merged if r['fraud_score'] > 0.7]
    elif filter_type == "Normal":
        filtered = [r for r in merged if not r['is_suspicious']]

    # Display table using columns
    if filtered:
        st.write(f"Showing {len(filtered)} transaction(s)")
        for tx in sorted(filtered, key=lambda x: x['fraud_score'], reverse=True)[:20]:
            col1, col2, col3, col4 = st.columns([1, 1, 1, 3])
            col1.write(f"**{tx['transaction_id']}**")
            col2.write(f"{tx['fraud_score']:.3f}")
            col3.write("🚨 ALERT" if tx['is_suspicious'] else "✓ OK")
            col4.write(tx['reason'][:80] if 'reason' in tx else "")
    else:
        st.info("No transactions match the filter.")

    # Score distribution
    st.markdown("---")
    st.subheader("Score Distribution")
    scores = [r['fraud_score'] for r in merged]
    if scores:
        fig = go.Figure(data=[go.Histogram(x=scores, nbinsx=20, marker_color='indianred')])
        fig.update_layout(
            title="Distribution of fraud scores",
            xaxis_title="Fraud Score",
            yaxis_title="Count",
            height=300,
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    # Top alerts
    st.markdown("---")
    st.subheader("Top Alerts")
    suspicious = [r for r in merged if r['is_suspicious']]
    if suspicious:
        top_5 = sorted(suspicious, key=lambda x: x['fraud_score'], reverse=True)[:5]
        for tx in top_5:
            st.warning(
                f"**{tx['transaction_id']}** (Client: {tx.get('user_id', '?')}) - "
                f"Score: {tx['fraud_score']:.3f}\n{tx['reason'][:150]}"
            )
    else:
        st.success("No alerts. All transactions look normal!")

    # Export
    st.markdown("---")
    csv_output = "transaction_id,fraud_score,is_suspicious,reason\n"
    for r in results:
        csv_output += f"{r['transaction_id']},{r['fraud_score']},{r['is_suspicious']},\"{r['reason']}\"\n"

    st.download_button(
        "📥 Export results CSV",
        csv_output,
        "fraud_results.csv",
        "text/csv"
    )

    st.caption("ShieldAI · Hackathon IT 2026 · Powered by fraud_detection.py")


if __name__ == "__main__":
    render_interface()
