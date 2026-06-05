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
    # === CLIENT u001 - Profil normal FR, puis anomalie JP ===
    {'transaction_id': 'tx001', 'user_id': 'u001', 'amount': 48,  'currency': 'EUR', 'merchant': 'Boulangerie Martin', 'country': 'FR', 'card_present': True,  'timestamp': '2024-01-15T08:10:00'},
    {'transaction_id': 'tx002', 'user_id': 'u001', 'amount': 55,  'currency': 'EUR', 'merchant': 'Cafe de la Paix',    'country': 'FR', 'card_present': True,  'timestamp': '2024-01-15T09:00:00'},
    {'transaction_id': 'tx003', 'user_id': 'u001', 'amount': 120, 'currency': 'EUR', 'merchant': 'Carrefour',          'country': 'FR', 'card_present': True,  'timestamp': '2024-01-15T10:30:00'},
    {'transaction_id': 'tx004', 'user_id': 'u001', 'amount': 52,  'currency': 'EUR', 'merchant': 'Boulangerie Martin', 'country': 'FR', 'card_present': True,  'timestamp': '2024-01-15T11:00:00'},
    {'transaction_id': 'tx005', 'user_id': 'u001', 'amount': 9800,'currency': 'EUR', 'merchant': 'Electronics Tokyo',  'country': 'JP', 'card_present': False, 'timestamp': '2024-01-15T13:30:00'},

    # === CLIENT u002 - Burst de frequence suspect ===
    {'transaction_id': 'tx006', 'user_id': 'u002', 'amount': 75,  'currency': 'EUR', 'merchant': 'Supermarche Bio',   'country': 'FR', 'card_present': True,  'timestamp': '2024-01-15T14:00:00'},
    {'transaction_id': 'tx007', 'user_id': 'u002', 'amount': 80,  'currency': 'EUR', 'merchant': 'Pharmacie Centrale','country': 'FR', 'card_present': True,  'timestamp': '2024-01-15T14:00:10'},
    {'transaction_id': 'tx008', 'user_id': 'u002', 'amount': 95,  'currency': 'EUR', 'merchant': 'Station BP',        'country': 'FR', 'card_present': True,  'timestamp': '2024-01-15T14:00:20'},
    {'transaction_id': 'tx009', 'user_id': 'u002', 'amount': 60,  'currency': 'EUR', 'merchant': 'Quick Burger',      'country': 'FR', 'card_present': True,  'timestamp': '2024-01-15T14:00:30'},
    {'transaction_id': 'tx010', 'user_id': 'u002', 'amount': 110, 'currency': 'EUR', 'merchant': 'Decathlon',         'country': 'FR', 'card_present': True,  'timestamp': '2024-01-15T14:00:40'},
    {'transaction_id': 'tx011', 'user_id': 'u002', 'amount': 88,  'currency': 'EUR', 'merchant': 'Zara',              'country': 'FR', 'card_present': True,  'timestamp': '2024-01-15T14:00:50'},

    # === CLIENT u003 - Montant negatif / invalide ===
    {'transaction_id': 'tx012', 'user_id': 'u003', 'amount': 200, 'currency': 'EUR', 'merchant': 'FNAC',              'country': 'FR', 'card_present': True,  'timestamp': '2024-01-15T15:00:00'},
    {'transaction_id': 'tx013', 'user_id': 'u003', 'amount': -500,'currency': 'EUR', 'merchant': 'Inconnu',           'country': 'US', 'card_present': False, 'timestamp': '2024-01-15T15:05:00'},
    {'transaction_id': 'tx014', 'user_id': 'u003', 'amount': 0,   'currency': 'EUR', 'merchant': 'Ghost Merchant',    'country': 'CN', 'card_present': False, 'timestamp': '2024-01-15T15:10:00'},

    # === CLIENT u004 - Profil normal ===
    {'transaction_id': 'tx015', 'user_id': 'u004', 'amount': 35,  'currency': 'EUR', 'merchant': 'Boulangerie Dupont','country': 'FR', 'card_present': True,  'timestamp': '2024-01-15T08:00:00'},
    {'transaction_id': 'tx016', 'user_id': 'u004', 'amount': 42,  'currency': 'EUR', 'merchant': 'Cafe Renard',       'country': 'FR', 'card_present': True,  'timestamp': '2024-01-15T09:30:00'},
    {'transaction_id': 'tx017', 'user_id': 'u004', 'amount': 38,  'currency': 'EUR', 'merchant': 'Boulangerie Dupont','country': 'FR', 'card_present': True,  'timestamp': '2024-01-15T10:00:00'},
    {'transaction_id': 'tx018', 'user_id': 'u004', 'amount': 45,  'currency': 'EUR', 'merchant': 'Monoprix',          'country': 'FR', 'card_present': True,  'timestamp': '2024-01-15T12:00:00'},
    {'transaction_id': 'tx019', 'user_id': 'u004', 'amount': 40,  'currency': 'EUR', 'merchant': 'Boulangerie Dupont','country': 'FR', 'card_present': True,  'timestamp': '2024-01-15T16:00:00'},

    # === CLIENT u005 - Deplacement impossible FR -> BR ===
    {'transaction_id': 'tx020', 'user_id': 'u005', 'amount': 150, 'currency': 'EUR', 'merchant': 'Leclerc',           'country': 'FR', 'card_present': True,  'timestamp': '2024-01-15T09:00:00'},
    {'transaction_id': 'tx021', 'user_id': 'u005', 'amount': 300, 'currency': 'BRL', 'merchant': 'Mercado Livre',     'country': 'BR', 'card_present': False, 'timestamp': '2024-01-15T10:00:00'},
    {'transaction_id': 'tx022', 'user_id': 'u005', 'amount': 180, 'currency': 'EUR', 'merchant': 'Total Energies',    'country': 'FR', 'card_present': True,  'timestamp': '2024-01-15T18:00:00'},

    # === CLIENT u006 - Transactions normales UK ===
    {'transaction_id': 'tx023', 'user_id': 'u006', 'amount': 65,  'currency': 'GBP', 'merchant': 'Tesco',             'country': 'GB', 'card_present': True,  'timestamp': '2024-01-15T10:00:00'},
    {'transaction_id': 'tx024', 'user_id': 'u006', 'amount': 72,  'currency': 'GBP', 'merchant': 'Boots',             'country': 'GB', 'card_present': True,  'timestamp': '2024-01-15T11:00:00'},
    {'transaction_id': 'tx025', 'user_id': 'u006', 'amount': 90,  'currency': 'GBP', 'merchant': 'Marks Spencer',     'country': 'GB', 'card_present': True,  'timestamp': '2024-01-15T14:00:00'},

    # === CLIENT u007 - Gros montant anormal ===
    {'transaction_id': 'tx026', 'user_id': 'u007', 'amount': 30,  'currency': 'EUR', 'merchant': 'Tabac Presse',      'country': 'FR', 'card_present': True,  'timestamp': '2024-01-14T09:00:00'},
    {'transaction_id': 'tx027', 'user_id': 'u007', 'amount': 28,  'currency': 'EUR', 'merchant': 'Tabac Presse',      'country': 'FR', 'card_present': True,  'timestamp': '2024-01-14T10:00:00'},
    {'transaction_id': 'tx028', 'user_id': 'u007', 'amount': 35,  'currency': 'EUR', 'merchant': 'Boulangerie',       'country': 'FR', 'card_present': True,  'timestamp': '2024-01-14T11:00:00'},
    {'transaction_id': 'tx029', 'user_id': 'u007', 'amount': 12500,'currency':'EUR', 'merchant': 'Luxury Watches',    'country': 'AE', 'card_present': False, 'timestamp': '2024-01-15T22:00:00'},

    # === CLIENT u008 - Normal DE ===
    {'transaction_id': 'tx030', 'user_id': 'u008', 'amount': 95,  'currency': 'EUR', 'merchant': 'Rewe',              'country': 'DE', 'card_present': True,  'timestamp': '2024-01-15T08:30:00'},
    {'transaction_id': 'tx031', 'user_id': 'u008', 'amount': 110, 'currency': 'EUR', 'merchant': 'Saturn',            'country': 'DE', 'card_present': True,  'timestamp': '2024-01-15T11:00:00'},
    {'transaction_id': 'tx032', 'user_id': 'u008', 'amount': 88,  'currency': 'EUR', 'merchant': 'DM Drogerie',       'country': 'DE', 'card_present': True,  'timestamp': '2024-01-15T14:00:00'},
    {'transaction_id': 'tx033', 'user_id': 'u008', 'amount': 102, 'currency': 'EUR', 'merchant': 'Kaufland',          'country': 'DE', 'card_present': True,  'timestamp': '2024-01-15T17:00:00'},

    # === CLIENT u009 - Test de carte (0.50->0.75->1.00) ===
    {'transaction_id': 'tx034', 'user_id': 'u009', 'amount': 0.50,'currency': 'EUR', 'merchant': 'Online Test',       'country': 'US', 'card_present': False, 'timestamp': '2024-01-15T03:00:00'},
    {'transaction_id': 'tx035', 'user_id': 'u009', 'amount': 0.75,'currency': 'EUR', 'merchant': 'Online Test',       'country': 'US', 'card_present': False, 'timestamp': '2024-01-15T03:01:00'},
    {'transaction_id': 'tx036', 'user_id': 'u009', 'amount': 1.00,'currency': 'EUR', 'merchant': 'Online Test',       'country': 'US', 'card_present': False, 'timestamp': '2024-01-15T03:02:00'},
    {'transaction_id': 'tx037', 'user_id': 'u009', 'amount': 4500,'currency': 'USD', 'merchant': 'Amazon US',         'country': 'US', 'card_present': False, 'timestamp': '2024-01-15T03:05:00'},

    # === CLIENT u010 - Normal Afrique ===
    {'transaction_id': 'tx038', 'user_id': 'u010', 'amount': 15000,'currency':'XOF', 'merchant': 'Marche Central',    'country': 'TG', 'card_present': True,  'timestamp': '2024-01-15T09:00:00'},
    {'transaction_id': 'tx039', 'user_id': 'u010', 'amount': 8000, 'currency':'XOF', 'merchant': 'Orange Money',      'country': 'TG', 'card_present': True,  'timestamp': '2024-01-15T12:00:00'},
    {'transaction_id': 'tx040', 'user_id': 'u010', 'amount': 12000,'currency':'XOF', 'merchant': 'Station Total',     'country': 'TG', 'card_present': True,  'timestamp': '2024-01-15T15:00:00'},

    # === CLIENT u011 - Deplacement impossible FR->US ===
    {'transaction_id': 'tx041', 'user_id': 'u011', 'amount': 60,  'currency': 'EUR', 'merchant': 'Auchan',            'country': 'FR', 'card_present': True,  'timestamp': '2024-01-15T07:00:00'},
    {'transaction_id': 'tx042', 'user_id': 'u011', 'amount': 350, 'currency': 'USD', 'merchant': 'Best Buy',          'country': 'US', 'card_present': False, 'timestamp': '2024-01-15T08:00:00'},

    # === CLIENT u012 - Normal ES ===
    {'transaction_id': 'tx043', 'user_id': 'u012', 'amount': 55,  'currency': 'EUR', 'merchant': 'Mercadona',         'country': 'ES', 'card_present': True,  'timestamp': '2024-01-15T10:00:00'},
    {'transaction_id': 'tx044', 'user_id': 'u012', 'amount': 40,  'currency': 'EUR', 'merchant': 'El Corte Ingles',   'country': 'ES', 'card_present': True,  'timestamp': '2024-01-15T13:00:00'},
    {'transaction_id': 'tx045', 'user_id': 'u012', 'amount': 70,  'currency': 'EUR', 'merchant': 'Zara ES',           'country': 'ES', 'card_present': True,  'timestamp': '2024-01-15T16:00:00'},

    # === CLIENT u013 - Anomalie devise ===
    {'transaction_id': 'tx046', 'user_id': 'u013', 'amount': 200, 'currency': 'EUR', 'merchant': 'Ikea FR',           'country': 'FR', 'card_present': True,  'timestamp': '2024-01-14T10:00:00'},
    {'transaction_id': 'tx047', 'user_id': 'u013', 'amount': 220, 'currency': 'EUR', 'merchant': 'Darty',             'country': 'FR', 'card_present': True,  'timestamp': '2024-01-14T14:00:00'},
    {'transaction_id': 'tx048', 'user_id': 'u013', 'amount': 7500,'currency': 'USD', 'merchant': 'Crypto Exchange',   'country': 'US', 'card_present': False, 'timestamp': '2024-01-15T02:00:00'},

    # === CLIENT u014 - Normal IT ===
    {'transaction_id': 'tx049', 'user_id': 'u014', 'amount': 85,  'currency': 'EUR', 'merchant': 'Esselunga',         'country': 'IT', 'card_present': True,  'timestamp': '2024-01-15T09:00:00'},
    {'transaction_id': 'tx050', 'user_id': 'u014', 'amount': 120, 'currency': 'EUR', 'merchant': 'Rinascente',        'country': 'IT', 'card_present': True,  'timestamp': '2024-01-15T15:00:00'},
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
