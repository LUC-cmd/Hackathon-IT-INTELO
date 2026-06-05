#!/usr/bin/env python3
"""
ShieldAI Premium Dashboard Launcher
Opens the beautiful web-based fraud detection dashboard
"""

import os
import sys
import time
import webbrowser
import subprocess
from pathlib import Path

def main():
    print("\n" + "="*60)
    print("  ShieldAI Premium Dashboard")
    print("  Fraud Detection System")
    print("="*60 + "\n")

    # Check if Flask is installed
    try:
        import flask
        print("[OK] Flask is installed")
    except ImportError:
        print("[!] Flask not found. Installing...")
        os.system("pip install flask --quiet")
        print("[OK] Flask installed")

    # Change to app directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    print("[*] Starting server at http://localhost:5000")
    print("[*] Opening dashboard in browser...")
    print("[*] Press Ctrl+C to stop the server\n")

    # Open browser after short delay
    time.sleep(2)
    try:
        webbrowser.open('http://localhost:5000')
        print("[OK] Browser opened!")
    except:
        print("[!] Could not open browser automatically")
        print("    Visit: http://localhost:5000")

    print("\n" + "="*60)
    print("  Features:")
    print("  - Real-time fraud detection")
    print("  - Interactive score distribution chart")
    print("  - Country risk analysis")
    print("  - Priority alerts display")
    print("  - Dynamic threshold adjustment")
    print("  - CSV export functionality")
    print("="*60 + "\n")

    # Start Flask app
    from app_premium_flask import app
    app.run(debug=False, port=5000, use_reloader=False)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[*] Shutting down...")
        print("[OK] Dashboard stopped")
        sys.exit(0)
