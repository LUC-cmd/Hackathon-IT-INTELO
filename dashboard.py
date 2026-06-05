#!/usr/bin/env python3
"""
Simple HTML dashboard for fraud detection - no external dependencies needed
"""
import csv
from fraud_detection import detect_fraud, load_transactions
from datetime import datetime

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


def generate_html(results, threshold=0.5):
    """Generate HTML report for fraud detection results."""

    total = len(results)
    alerts = sum(1 for r in results if r['fraud_score'] >= threshold)
    critical = sum(1 for r in results if r['fraud_score'] > 0.7)
    avg_score = sum(r['fraud_score'] for r in results) / total if total > 0 else 0

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>ShieldAI - Fraud Detection Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: Arial, sans-serif; background: #0f0c29; color: #fff; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            padding: 30px; border-radius: 10px; margin-bottom: 30px;
            border: 1px solid #4a4a8a;
        }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header p {{ color: #a0a0d0; font-size: 0.95em; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .metric {{ background: #1a1a2e; padding: 20px; border-radius: 10px; border-left: 4px solid #4a9eff; text-align: center; }}
        .metric h3 {{ color: #4a9eff; font-size: 0.9em; margin-bottom: 10px; text-transform: uppercase; }}
        .metric .value {{ font-size: 2em; font-weight: bold; }}
        .metric.alert {{ border-left-color: #e74c3c; }}
        .metric.alert h3 {{ color: #e74c3c; }}
        .metric.critical {{ border-left-color: #c0392b; }}
        .metric.critical h3 {{ color: #c0392b; }}

        .section {{ margin-bottom: 30px; }}
        .section h2 {{ margin-bottom: 15px; padding-bottom: 10px; border-bottom: 2px solid #4a9eff; }}

        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        th {{ background: #16213e; padding: 12px; text-align: left; font-weight: bold; border-bottom: 2px solid #0f3460; }}
        td {{ padding: 12px; border-bottom: 1px solid #16213e; }}
        tr:hover {{ background: #16213e; }}

        .score-high {{ color: #e74c3c; font-weight: bold; }}
        .score-medium {{ color: #f39c12; font-weight: bold; }}
        .score-low {{ color: #27ae60; font-weight: bold; }}
        .reason {{ font-size: 0.9em; color: #bdc3c7; }}

        .alert-box {{ background: #2c1810; border-left: 4px solid #e74c3c; padding: 15px; margin-bottom: 10px; border-radius: 5px; }}
        .alert-box strong {{ color: #e74c3c; }}
        .success-box {{ background: #0d2818; border-left: 4px solid #27ae60; padding: 15px; margin-bottom: 10px; border-radius: 5px; }}

        .footer {{ text-align: center; margin-top: 40px; color: #7f8c8d; font-size: 0.9em; }}
        .timestamp {{ color: #95a5a6; font-size: 0.85em; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>[shield] ShieldAI - Fraud Detection Report</h1>
            <p>Multi-signal fraud detection | Adaptive client profiles | Real-time explainability</p>
            <p class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>

        <div class="metrics">
            <div class="metric">
                <h3>Total Transactions</h3>
                <div class="value">{total}</div>
            </div>
            <div class="metric alert">
                <h3>Alerts</h3>
                <div class="value">{alerts}</div>
                <p style="font-size: 0.8em; margin-top: 5px;">{alerts/total*100:.1f}% alert rate</p>
            </div>
            <div class="metric critical">
                <h3>Critical (>0.7)</h3>
                <div class="value">{critical}</div>
            </div>
            <div class="metric">
                <h3>Average Score</h3>
                <div class="value">{avg_score:.3f}</div>
            </div>
        </div>

        <div class="section">
            <h2>Priority Alerts (Top 10)</h2>
"""

    suspicious = sorted([r for r in results if r['fraud_score'] >= threshold],
                       key=lambda x: x['fraud_score'], reverse=True)[:10]

    if suspicious:
        for rank, tx in enumerate(suspicious, 1):
            score_class = 'score-high' if tx['fraud_score'] >= 0.7 else 'score-medium'
            html += f"""
            <div class="alert-box">
                <strong>#{rank} {tx['transaction_id']}</strong>
                <span class="{score_class}" style="margin-left: 20px;">Score: {tx['fraud_score']:.3f}</span>
                <p class="reason" style="margin-top: 8px;">{tx['reason'][:200]}</p>
            </div>
"""
    else:
        html += '<div class="success-box"><strong>No alerts detected!</strong> All transactions look normal.</div>'

    html += """
        </div>

        <div class="section">
            <h2>All Transactions</h2>
            <table>
                <thead>
                    <tr>
                        <th>Transaction ID</th>
                        <th>Score</th>
                        <th>Status</th>
                        <th>Reason</th>
                    </tr>
                </thead>
                <tbody>
"""

    for tx in sorted(results, key=lambda x: x['fraud_score'], reverse=True):
        if tx['fraud_score'] >= threshold:
            score_class = 'score-high' if tx['fraud_score'] >= 0.7 else 'score-medium'
            status = '[ALERT]'
        else:
            score_class = 'score-low'
            status = '[OK]'

        html += f"""
                    <tr>
                        <td><strong>{tx['transaction_id']}</strong></td>
                        <td><span class="{score_class}">{tx['fraud_score']:.3f}</span></td>
                        <td>{status}</td>
                        <td><span class="reason">{tx['reason'][:80]}</span></td>
                    </tr>
"""

    html += """
                </tbody>
            </table>
        </div>

        <div class="footer">
            <p>ShieldAI | Hackathon IT 2026 | Powered by fraud_detection.py</p>
            <p>System ready for production deployment</p>
        </div>
    </div>
</body>
</html>
"""
    return html


def main():
    print("[*] ShieldAI Fraud Detection Dashboard")
    print("[*] Loading demo transactions...")

    results = detect_fraud(DEMO_TRANSACTIONS)
    html_content = generate_html(results, threshold=0.5)

    # Save HTML file
    with open('fraud_report.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("[OK] HTML report generated: fraud_report.html")
    print("[OK] Opening in browser...")

    import webbrowser
    import os
    webbrowser.open('file://' + os.path.realpath('fraud_report.html'))

    print("[OK] Dashboard opened!")
    print()
    print("Summary:")
    print(f"  Total transactions: {len(results)}")
    print(f"  Alerts: {sum(1 for r in results if r['fraud_score'] >= 0.5)}")
    print(f"  Critical (>0.7): {sum(1 for r in results if r['fraud_score'] > 0.7)}")
    print(f"  Average score: {sum(r['fraud_score'] for r in results) / len(results):.3f}")
    print()
    print("[*] System ready for production submission!")


if __name__ == "__main__":
    main()
