#!/usr/bin/env python
"""Verification pre-demo — ensures all components work."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

def check_imports() -> bool:
    """Check critical imports work."""
    print("Checking imports...")
    try:
        from memory_mcp.tools import MemoryTools
        from benchmark.harness import run_benchmark
        from benchmark.insights import generate_insights
        from demo.export_pdf import generate_pdf_report
        print("  [OK] All imports")
        return True
    except ImportError as e:
        print(f"  [FAIL] Import error: {e}")
        return False


def check_files() -> bool:
    """Check all critical files exist."""
    print("Checking files...")
    files_to_check = [
        "dashboard/index.html",
        "dashboard/app.js",
        "dashboard/styles.css",
        "src/memory_mcp/server.py",
        "benchmark/conversation.json",
        "benchmark/trap_questions.json",
        "demo/web_server.py",
        "demo/export_pdf.py",
    ]

    all_ok = True
    for file in files_to_check:
        path = ROOT / file
        if path.exists():
            print(f"  [OK] {file}")
        else:
            print(f"  [FAIL] {file} MISSING")
            all_ok = False

    return all_ok


def check_endpoints() -> bool:
    """Check that endpoints are declared."""
    print("Checking endpoints...")
    web_server = ROOT / "demo" / "web_server.py"
    content = web_server.read_text()

    endpoints = [
        "/api/benchmark",
        "/api/report",
        "/api/memory",
        "/api/search",
        "/api/transcribe",
        "/api/locate",
        "/api/vision",
        "/api/stats",
        "/api/export/pdf",
    ]

    all_ok = True
    for endpoint in endpoints:
        if f'"{endpoint}"' in content or f"'{endpoint}'" in content:
            print(f"  [OK] {endpoint}")
        else:
            print(f"  [FAIL] {endpoint} NOT FOUND")
            all_ok = False

    return all_ok


def main() -> int:
    """Run all checks."""
    print("\n" + "="*50)
    print("MemBridge - Pre-Demo Verification")
    print("="*50 + "\n")

    checks = [
        ("Imports", check_imports),
        ("Files", check_files),
        ("Endpoints", check_endpoints),
    ]

    results = []
    for name, check in checks:
        try:
            result = check()
            results.append((name, result))
        except Exception as e:
            print(f"[ERROR] {name} failed: {e}\n")
            results.append((name, False))

    print("\n" + "="*50)
    print("Summary")
    print("="*50)
    for name, result in results:
        status = "OK" if result else "FAIL"
        print(f"[{status}] {name}")

    all_passed = all(result for _, result in results)
    if all_passed:
        print("\nAll checks passed! Ready for demo.\n")
        return 0
    else:
        print("\nSome checks failed. Fix before demo.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
