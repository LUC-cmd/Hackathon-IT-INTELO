#!/usr/bin/env python3
"""
ShieldAI ULTRA Dashboard Launcher
Advanced fraud detection with stunning visuals
"""

import os
import sys
import time
import webbrowser
from pathlib import Path

def main():
    print("\n" + "="*70)
    print("  ShieldAI ULTRA - Advanced Fraud Detection Command Center")
    print("="*70)
    print("")
    print("  FEATURES:")
    print("  ✨ Advanced 4-Chart System (Timeline, Heatmap, Distribution, Breakdown)")
    print("  🎯 Real-Time KPI Cards with Animations")
    print("  🚨 Intelligent Threat Analysis Engine")
    print("  📊 Geographic Risk Heatmap with Radar Chart")
    print("  🤖 AI-Powered Insights Generator")
    print("  🎨 Cyberpunk Design with Glassmorphism UI")
    print("  ⚡ Dynamic Threshold Control with Live Updates")
    print("  📋 Advanced Transaction Ledger with Filtering")
    print("")
    print("="*70 + "\n")

    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    print("[*] Checking Flask installation...")
    try:
        import flask
        print("[OK] Flask ready\n")
    except ImportError:
        print("[!] Installing Flask...")
        os.system("pip install flask --quiet")
        print("[OK] Flask installed\n")

    print("[*] Starting ULTRA Dashboard at http://localhost:5000")
    print("[*] Opening browser...")
    print("[*] Press Ctrl+C to stop\n")

    time.sleep(1)
    try:
        webbrowser.open('http://localhost:5000')
        print("[OK] Browser opening...\n")
    except:
        print("[!] Manual open: http://localhost:5000\n")

    print("="*70)
    print("  ADVANCED FEATURES:")
    print("  • 4 Advanced Charts (Real-time updates)")
    print("  • AI Insights Panel (Pattern Recognition)")
    print("  • Threat Level Indicator (Dynamic)")
    print("  • Smart Filtering (Multiple Views)")
    print("  • Live Metrics (Real-time)")
    print("  • Sensitivity Control (0.3 - 0.9)")
    print("="*70 + "\n")

    from app_premium_flask import app
    app.run(debug=False, port=5000, use_reloader=False)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[*] Shutting down ULTRA Dashboard...")
        print("[OK] See you next time!")
        sys.exit(0)
