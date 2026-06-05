import streamlit as st
import csv
from fraud_detection import detect_fraud, load_transactions

DEMO_TRANSACTIONS = [
    {'transaction_id': 'tx001', 'user_id': 'u001', 'amount': 50, 'currency': 'EUR',
     'merchant': 'Boulangerie', 'country': 'FR', 'card_present': True,
     'timestamp': '2024-01-15T09:30:00'},
    {'transaction_id': 'tx002', 'user_id': 'u001', 'amount': 55, 'currency': 'EUR',
     'merchant': 'Cafe', 'country': 'FR', 'card_present': True,
     'timestamp': '2024-01-15T10:00:00'},
    {'transaction_id': 'tx003', 'user_id': 'u001', 'amount': 52, 'currency': 'EUR',
     'merchant': 'Supermarche', 'country': 'FR', 'card_present': True,
     'timestamp': '2024-01-15T11:00:00'},
    {'transaction_id': 'tx004', 'user_id': 'u001', 'amount': 5000, 'currency': 'EUR',
     'merchant': 'Electronique', 'country': 'JP', 'card_present': False,
     'timestamp': '2024-01-15T13:00:00'},
    {'transaction_id': 'tx005', 'user_id': 'u002', 'amount': 75, 'currency': 'EUR',
     'merchant': 'Supermarche', 'country': 'FR', 'card_present': True,
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


def main():
    st.set_page_config(page_title="ShieldAI Fraud Detection", page_icon="[shield]", layout="wide")

    st.title("ShieldAI - Fraud Detection System")
    st.markdown("Multi-signal fraud detection | Adaptive client profiles | Real-time explainability")
    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.markdown("### Configuration")
        source = st.radio("Data source", ["Demo scenario", "sample_data.csv", "CSV upload"])
        uploaded = st.file_uploader("CSV File", type=["csv"]) if source == "CSV upload" else None
        threshold = st.slider("Alert threshold", 0.3, 0.9, 0.5, 0.05)
        st.markdown("---")
        st.markdown("**Detected signals:**")
        st.markdown("- Amount (Z-score + IQR)\n- Geographic impossibility\n- Frequency anomaly\n- Duplicates & missing fields")

    # Load data
    transactions = None
    if source == "Demo scenario":
        transactions = DEMO_TRANSACTIONS
    elif source == "sample_data.csv":
        transactions = load_transactions("sample_data.csv")
    elif source == "CSV upload" and uploaded:
        transactions = load_csv_simple(uploaded)

    if not transactions:
        st.warning("No transactions loaded. Select a data source in the sidebar.")
        return

    # Detect fraud
    results = detect_fraud(transactions)

    # Metrics
    total = len(results)
    frauds = sum(1 for r in results if r['fraud_score'] >= threshold)
    high = sum(1 for r in results if r['fraud_score'] > 0.7)
    avg_score = sum(r['fraud_score'] for r in results) / total if total > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Transactions", total)
    col2.metric("Alerts", frauds)
    col3.metric("Critical (>0.7)", high)
    col4.metric("Avg Score", f"{avg_score:.3f}")

    st.markdown("---")

    # Filter
    st.subheader("Transactions")
    filter_type = st.selectbox("Filter by", ["All", "Suspicious", "Score > 0.7", "Normal"])

    filtered = results
    if filter_type == "Suspicious":
        filtered = [r for r in results if r['fraud_score'] >= threshold]
    elif filter_type == "Score > 0.7":
        filtered = [r for r in results if r['fraud_score'] > 0.7]
    elif filter_type == "Normal":
        filtered = [r for r in results if r['fraud_score'] < threshold]

    # Display table
    if filtered:
        st.write(f"**{len(filtered)} transaction(s) found**")
        for tx in sorted(filtered, key=lambda x: x['fraud_score'], reverse=True)[:50]:
            status = "[ALERT]" if tx['fraud_score'] >= threshold else "[OK]"
            st.write(f"**{tx['transaction_id']}** {status} Score: {tx['fraud_score']:.3f}")
            st.write(f"  Reason: {tx['reason'][:120]}")
            st.write("")
    else:
        st.info("No transactions match the filter.")

    st.markdown("---")

    # Top alerts
    st.subheader("Priority Alerts")
    suspicious = [r for r in results if r['fraud_score'] >= threshold]
    if suspicious:
        top_5 = sorted(suspicious, key=lambda x: x['fraud_score'], reverse=True)[:5]
        for i, tx in enumerate(top_5, 1):
            st.warning(f"#{i} {tx['transaction_id']} - Score {tx['fraud_score']:.3f}\n{tx['reason'][:150]}")
    else:
        st.success("No alerts. All transactions look normal!")

    st.markdown("---")

    # Export
    csv_output = "transaction_id,fraud_score,is_suspicious,reason\n"
    for r in results:
        is_suspicious = r['fraud_score'] >= threshold
        csv_output += f"{r['transaction_id']},{r['fraud_score']},{is_suspicious},\"{r['reason']}\"\n"

    st.download_button("Download CSV Results", csv_output, "fraud_results.csv", "text/csv")

    st.caption("ShieldAI | Hackathon IT 2026 | Powered by fraud_detection.py")


if __name__ == "__main__":
    main()
