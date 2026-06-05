#!/usr/bin/env python3
"""
ShieldAI ULTRA Dashboard - Flask Web Application
Serves pure HTML (no Jinja2) for Python 3.14 compatibility
"""

from flask import Flask, jsonify, request, send_file, Response
from fraud_detection import detect_fraud
import io
import csv
import os

app = Flask(__name__)

DEMO_TRANSACTIONS = [
    {'transaction_id': 'tx001', 'user_id': 'u001', 'amount': 50, 'currency': 'EUR',
     'merchant': 'Boulangerie', 'country': 'FR', 'card_present': True, 'timestamp': '2024-01-15T09:30:00'},
    {'transaction_id': 'tx002', 'user_id': 'u001', 'amount': 55, 'currency': 'EUR',
     'merchant': 'Cafe', 'country': 'FR', 'card_present': True, 'timestamp': '2024-01-15T10:00:00'},
    {'transaction_id': 'tx003', 'user_id': 'u001', 'amount': 52, 'currency': 'EUR',
     'merchant': 'Supermarche', 'country': 'FR', 'card_present': True, 'timestamp': '2024-01-15T11:00:00'},
    {'transaction_id': 'tx004', 'user_id': 'u001', 'amount': 5000, 'currency': 'EUR',
     'merchant': 'Electronique', 'country': 'JP', 'card_present': False, 'timestamp': '2024-01-15T13:00:00'},
    {'transaction_id': 'tx005', 'user_id': 'u002', 'amount': 75, 'currency': 'EUR',
     'merchant': 'Supermarche', 'country': 'FR', 'card_present': True, 'timestamp': '2024-01-15T14:20:00'},
    {'transaction_id': 'tx006', 'user_id': 'u002', 'amount': 80, 'currency': 'EUR',
     'merchant': 'Pharmacie', 'country': 'FR', 'card_present': True, 'timestamp': '2024-01-15T14:25:00'},
    {'transaction_id': 'tx007', 'user_id': 'u003', 'amount': -100, 'currency': 'EUR',
     'merchant': 'Inconnu', 'country': 'US', 'card_present': False, 'timestamp': '2024-01-15T15:00:00'},
    {'transaction_id': 'tx008', 'user_id': 'u004', 'amount': 120, 'currency': 'EUR',
     'merchant': 'Shop', 'country': 'FR', 'card_present': True, 'timestamp': '2024-01-15T16:00:00'},
]

current_results = None
current_transactions = None


def process_data():
    global current_results, current_transactions
    current_transactions = DEMO_TRANSACTIONS
    current_results = detect_fraud(DEMO_TRANSACTIONS)


def get_api_data(threshold=0.5):
    if current_results is None:
        process_data()

    results = current_results
    transactions = current_transactions
    total = len(results)
    alerts = sum(1 for r in results if r['fraud_score'] >= threshold)
    critical = sum(1 for r in results if r['fraud_score'] > 0.7)
    avg_score = sum(r['fraud_score'] for r in results) / total if total > 0 else 0

    score_buckets = {'0-0.2': 0, '0.2-0.4': 0, '0.4-0.6': 0, '0.6-0.8': 0, '0.8-1.0': 0}
    for r in results:
        s = r['fraud_score']
        if s < 0.2: score_buckets['0-0.2'] += 1
        elif s < 0.4: score_buckets['0.2-0.4'] += 1
        elif s < 0.6: score_buckets['0.4-0.6'] += 1
        elif s < 0.8: score_buckets['0.6-0.8'] += 1
        else: score_buckets['0.8-1.0'] += 1

    country_scores = {}
    for tx, res in zip(transactions, results):
        c = tx.get('country', 'Unknown')
        if c not in country_scores:
            country_scores[c] = {'total': 0, 'sum': 0, 'alerts': 0}
        country_scores[c]['total'] += 1
        country_scores[c]['sum'] += res['fraud_score']
        if res['fraud_score'] >= threshold:
            country_scores[c]['alerts'] += 1

    country_data = [{'country': k, 'avg_score': v['sum']/v['total'], 'alerts': v['alerts'], 'total': v['total']}
                    for k, v in country_scores.items()]

    top_alerts = sorted(
        [{'id': r['transaction_id'], 'score': r['fraud_score'], 'reason': r['reason']}
         for r in results if r['fraud_score'] >= threshold],
        key=lambda x: x['score'], reverse=True)[:5]

    recent = [{'id': r['transaction_id'], 'score': r['fraud_score'],
               'status': 'ALERT' if r['fraud_score'] >= threshold else 'OK',
               'reason': r['reason'][:80]}
              for r in sorted(results, key=lambda x: x['fraud_score'], reverse=True)]

    return {
        'metrics': {'total': total, 'alerts': alerts, 'critical': critical,
                    'avg_score': avg_score, 'alert_rate': f"{alerts/total*100:.1f}%" if total else "0%"},
        'score_distribution': score_buckets,
        'country_data': country_data,
        'top_alerts': top_alerts,
        'recent_transactions': recent
    }


@app.route('/')
def index():
    process_data()
    # Read HTML file and serve it directly (no Jinja2 template rendering)
    html_path = os.path.join(os.path.dirname(__file__), 'templates', 'dashboard_ultra.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    return Response(html, mimetype='text/html')


@app.route('/static/css/<filename>')
def serve_css(filename):
    css_path = os.path.join(os.path.dirname(__file__), 'static', 'css', filename)
    with open(css_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return Response(content, mimetype='text/css')


@app.route('/static/js/<filename>')
def serve_js(filename):
    js_path = os.path.join(os.path.dirname(__file__), 'static', 'js', filename)
    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return Response(content, mimetype='application/javascript')


@app.route('/api/data')
def get_data():
    threshold = float(request.args.get('threshold', 0.5))
    data = get_api_data(threshold)
    return jsonify(data)


@app.route('/api/transactions')
def get_transactions():
    if current_results is None:
        process_data()
    filter_type = request.args.get('filter', 'all')
    threshold = float(request.args.get('threshold', 0.5))
    txs = []
    for r in current_results:
        score = r['fraud_score']
        if filter_type == 'alert' and score < threshold: continue
        if filter_type == 'critical' and score <= 0.7: continue
        if filter_type == 'safe' and score >= threshold: continue
        txs.append({'id': r['transaction_id'], 'score': score,
                    'is_suspicious': score >= threshold, 'reason': r['reason']})
    return jsonify({'transactions': txs})


@app.route('/api/export')
def export_csv():
    if current_results is None:
        process_data()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['transaction_id', 'fraud_score', 'is_suspicious', 'reason'])
    for r in current_results:
        writer.writerow([r['transaction_id'], r['fraud_score'], r['is_suspicious'], r['reason']])
    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode()),
                     mimetype='text/csv', as_attachment=True,
                     download_name='fraud_results.csv')


if __name__ == '__main__':
    print("[*] Starting ShieldAI ULTRA Dashboard...")
    print("[*] Open: http://localhost:5000")
    app.run(debug=False, port=5000)
