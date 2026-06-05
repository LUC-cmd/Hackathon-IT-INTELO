#!/usr/bin/env python3
"""
ShieldAI Premium Dashboard - Flask Web Application
Interactive fraud detection dashboard with graphs, real-time filtering, and stunning UI
"""

from flask import Flask, render_template, jsonify, request, send_file
import json
from fraud_detection import detect_fraud, load_transactions
from datetime import datetime
import io
import csv

app = Flask(__name__)

# Demo data
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

# Global data cache
current_results = None
current_transactions = None


def process_data(transactions=None):
    """Process transactions and cache results."""
    global current_results, current_transactions
    if transactions is None:
        transactions = DEMO_TRANSACTIONS
    current_transactions = transactions
    current_results = detect_fraud(transactions)
    return current_results, current_transactions


@app.route('/')
def index():
    """Main dashboard page."""
    process_data()
    return render_template('index.html')


@app.route('/api/data')
def get_data():
    """API endpoint for dashboard data."""
    if current_results is None:
        process_data()

    threshold = float(request.args.get('threshold', 0.5))
    results = current_results
    transactions = current_transactions

    # Calculate metrics
    total = len(results)
    alerts = sum(1 for r in results if r['fraud_score'] >= threshold)
    critical = sum(1 for r in results if r['fraud_score'] > 0.7)
    avg_score = sum(r['fraud_score'] for r in results) / total if total > 0 else 0

    # Score distribution
    score_buckets = {'0-0.2': 0, '0.2-0.4': 0, '0.4-0.6': 0, '0.6-0.8': 0, '0.8-1.0': 0}
    for r in results:
        score = r['fraud_score']
        if score < 0.2:
            score_buckets['0-0.2'] += 1
        elif score < 0.4:
            score_buckets['0.2-0.4'] += 1
        elif score < 0.6:
            score_buckets['0.4-0.6'] += 1
        elif score < 0.8:
            score_buckets['0.6-0.8'] += 1
        else:
            score_buckets['0.8-1.0'] += 1

    # Country distribution
    country_scores = {}
    for tx, res in zip(transactions, results):
        country = tx.get('country', 'Unknown')
        if country not in country_scores:
            country_scores[country] = {'total': 0, 'sum': 0, 'alerts': 0}
        country_scores[country]['total'] += 1
        country_scores[country]['sum'] += res['fraud_score']
        if res['fraud_score'] >= threshold:
            country_scores[country]['alerts'] += 1

    country_data = [
        {
            'country': k,
            'avg_score': v['sum'] / v['total'],
            'alerts': v['alerts'],
            'total': v['total']
        }
        for k, v in country_scores.items()
    ]

    # Top alerts
    top_alerts = sorted(
        [{'id': r['transaction_id'], 'score': r['fraud_score'], 'reason': r['reason']}
         for r in results if r['fraud_score'] >= threshold],
        key=lambda x: x['score'],
        reverse=True
    )[:5]

    # Recent transactions
    recent = [
        {
            'id': r['transaction_id'],
            'score': r['fraud_score'],
            'status': 'ALERT' if r['fraud_score'] >= threshold else 'OK',
            'reason': r['reason'][:80]
        }
        for r in sorted(results, key=lambda x: x['fraud_score'], reverse=True)[:10]
    ]

    return jsonify({
        'metrics': {
            'total': total,
            'alerts': alerts,
            'critical': critical,
            'avg_score': avg_score,
            'alert_rate': f"{alerts/total*100:.1f}%" if total > 0 else "0%"
        },
        'score_distribution': score_buckets,
        'country_data': country_data,
        'top_alerts': top_alerts,
        'recent_transactions': recent
    })


@app.route('/api/transactions')
def get_transactions():
    """Get all transactions with filtering."""
    if current_results is None:
        process_data()

    filter_type = request.args.get('filter', 'all')
    threshold = float(request.args.get('threshold', 0.5))

    results = current_results

    transactions_data = []
    for r in results:
        if filter_type == 'alerts' and r['fraud_score'] < threshold:
            continue
        if filter_type == 'critical' and r['fraud_score'] <= 0.7:
            continue
        if filter_type == 'normal' and r['fraud_score'] >= threshold:
            continue

        transactions_data.append({
            'id': r['transaction_id'],
            'score': r['fraud_score'],
            'is_suspicious': r['fraud_score'] >= threshold,
            'reason': r['reason']
        })

    return jsonify({'transactions': transactions_data})


@app.route('/api/export')
def export_csv():
    """Export results as CSV."""
    if current_results is None:
        process_data()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['transaction_id', 'fraud_score', 'is_suspicious', 'reason'])

    for r in current_results:
        writer.writerow([
            r['transaction_id'],
            r['fraud_score'],
            r['is_suspicious'],
            r['reason']
        ])

    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='fraud_results.csv'
    )


if __name__ == '__main__':
    print("[*] Starting ShieldAI Premium Dashboard...")
    print("[*] Open: http://localhost:5000")
    print("[*] Press Ctrl+C to stop")
    app.run(debug=True, port=5000)
