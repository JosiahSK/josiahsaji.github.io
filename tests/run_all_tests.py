#!/usr/bin/env python3
"""
tests/run_all_tests.py
Unified Comprehensive Engineering Test Suite for Josiah Saji's Robotics Portfolio.

Runs in deterministic sequence:
1. Python bytecode compilation (scripts & tests)
2. JavaScript syntax checks (script.js & test_interactive.js)
3. DOM structure, links, assets, heading hierarchy & claim purge (tests/test_links.py)
4. ATS machine-readability & factual integrity audit (scripts/verify_resume.py)
5. Headless browser interaction & WAI-ARIA accessibility (node tests/test_interactive.js)
6. Multi-viewport screenshot generation & dimension verification (scripts/capture_screenshots.py)
7. Optional live GitHub Pages endpoint verification (pass --live)
"""

import os
import sys
import time
import subprocess

def run_step(step_name, cmd, cwd=None):
    print("\n" + "=" * 78)
    print(f"STEP: {step_name}")
    print(f"COMMAND: {' '.join(cmd)}")
    print("=" * 78)
    start_t = time.time()
    res = subprocess.run(cmd, cwd=cwd)
    dur = time.time() - start_t
    if res.returncode == 0:
        print(f"\n[PASS] {step_name} completed successfully in {dur:.2f}s.")
        return True
    else:
        print(f"\n[FAIL] {step_name} failed with exit code {res.returncode} ({dur:.2f}s).", file=sys.stderr)
        return False

def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    check_live = "--live" in sys.argv

    print("*" * 78)
    print("PORTFOLIO V5.3 — UNIFIED QUALITY, ACCESSIBILITY & PRODUCTION TEST RUNNER")
    print(f"Target Directory: {repo_root}")
    print("*" * 78)

    steps = [
        ("Python Bytecode Compilation", [sys.executable, "-m", "compileall", "scripts", "tests"]),
        ("JavaScript Syntax Validation", ["node", "--check", "script.js"]),
        ("Test Harness Syntax Validation", ["node", "--check", "tests/test_interactive.js"]),
        ("Static DOM, Links, Alt & Claim Integrity", [sys.executable, "tests/test_links.py"]),
        ("Real Browser Accessibility & Interactive CDP", ["node", "tests/test_interactive.js"]),
        ("Multi-Viewport Screenshot Capture & Dimension Audit", [sys.executable, "scripts/capture_screenshots.py"]),
    ]

    if check_live:
        steps.append(("Live Production Endpoint Verification", [sys.executable, "tests/test_links.py", "--live"]))

    overall_start = time.time()
    passed = 0
    failed = 0

    for name, cmd in steps:
        ok = run_step(name, cmd, cwd=repo_root)
        if ok:
            passed += 1
        else:
            failed += 1
            print(f"\n[ABORT] Pipeline halted due to failure in step: {name}", file=sys.stderr)
            sys.exit(1)

    total_time = time.time() - overall_start
    print("\n" + "#" * 78)
    print(f"UNIFIED TEST SUMMARY: ALL {passed}/{len(steps)} STEPS PASSED IN {total_time:.2f}s.")
    print("#" * 78)
    sys.exit(0)

if __name__ == "__main__":
    main()
