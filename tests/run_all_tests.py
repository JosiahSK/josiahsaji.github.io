#!/usr/bin/env python3
"""
tests/run_all_tests.py
Unified Comprehensive Engineering Test Suite for Josiah Saji's Robotics Portfolio
(Antigravity Release V5.3.1).

Runs in deterministic sequence:
1. Python bytecode compilation (scripts & tests)
2. JavaScript syntax checks (script.js & test_interactive.js)
3. DOM structure, links, assets, heading hierarchy, normalized claims & claims register (tests/test_links.py)
4. ATS machine-readability & factual integrity audit (scripts/verify_resume.py, integrated in test_links.py)
5. Headless browser interaction & WAI-ARIA accessibility (node tests/test_interactive.js)
6. Multi-viewport screenshot generation & dimension verification (scripts/capture_screenshots.py)
7. Optional live GitHub Pages endpoint verification (pass --live)

Provides structured execution tracking, command logging, exact return codes, and a summary diagnostic table.
"""

import os
import sys
import time
import subprocess

class StepResult:
    def __init__(self, step_number, name, command, cwd):
        self.step_number = step_number
        self.name = name
        self.command = command
        self.cwd = cwd
        self.status = "PENDING"
        self.duration = 0.0
        self.exit_code = None
        self.error_message = None

def run_step(step_record):
    print("\n" + "=" * 80)
    print(f"STEP {step_record.step_number}: {step_record.name}")
    print(f"COMMAND: {' '.join(step_record.command)}")
    print(f"DIRECTORY: {step_record.cwd}")
    print("=" * 80)

    start_t = time.time()
    try:
        res = subprocess.run(step_record.command, cwd=step_record.cwd)
        step_record.duration = time.time() - start_t
        step_record.exit_code = res.returncode

        if res.returncode == 0:
            step_record.status = "PASS"
            print(f"\n[PASS] {step_record.name} completed successfully in {step_record.duration:.2f}s.")
            return True
        else:
            step_record.status = "FAIL"
            step_record.error_message = f"Process returned non-zero exit code {res.returncode}"
            print(f"\n[FAIL] {step_record.name} failed with exit code {res.returncode} ({step_record.duration:.2f}s).", file=sys.stderr)
            return False
    except Exception as e:
        step_record.duration = time.time() - start_t
        step_record.status = "ERROR"
        step_record.exit_code = -1
        step_record.error_message = str(e)
        print(f"\n[ERROR] Exception executing {step_record.name}: {e}", file=sys.stderr)
        return False

def print_summary_table(step_records, total_time):
    print("\n" + "#" * 80)
    print("UNIFIED TEST EXECUTION SUMMARY (PORTFOLIO V5.3.2)")
    print("#" * 80)
    print(f"{'#':<3} | {'Step Name':<44} | {'Status':<6} | {'Time':<7} | {'Code':<5}")
    print("-" * 80)

    all_passed = True
    for s in step_records:
        code_str = str(s.exit_code) if s.exit_code is not None else "-"
        status_display = f"[{s.status}]"
        print(f"{s.step_number:<3} | {s.name:<44} | {status_display:<6} | {s.duration:>5.2f}s | {code_str:>5}")
        if s.status != "PASS" and s.status != "SKIPPED":
            all_passed = False

    print("-" * 80)
    passed_count = sum(1 for s in step_records if s.status == "PASS")
    total_count = len(step_records)
    print(f"Total Steps: {total_count} | Passed: {passed_count} | Failed/Error: {total_count - passed_count} | Wall-clock: {total_time:.2f}s")

    if not all_passed:
        print("\nFAILURE DIAGNOSTICS:")
        for s in step_records:
            if s.status not in ("PASS", "SKIPPED"):
                print(f"  - Step {s.step_number} ({s.name}): {s.error_message} (exit {s.exit_code})")
                print(f"    Command was: {' '.join(s.command)}")
    print("#" * 80 + "\n")
    return all_passed

def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    check_live = "--live" in sys.argv
    skip_screens = "--skip-screenshots" in sys.argv

    print("*" * 80)
    print("PORTFOLIO V5.3.2 — UNIFIED FORENSIC QUALITY, ACCESSIBILITY & PRODUCTION TEST RUNNER")
    print(f"Target Repository Root: {repo_root}")
    print("*" * 80)

    raw_steps = [
        ("Python Bytecode Compilation", [sys.executable, "-m", "compileall", "scripts", "tests"]),
        ("JavaScript Syntax Validation", ["node", "--check", "script.js"]),
        ("Test Harness Syntax Validation", ["node", "--check", "tests/test_interactive.js"]),
        ("Claim Normalization & Fixture Regression Suite", [sys.executable, "tests/test_claim_normalization.py"]),
        ("Static DOM, Links, Alt & Claim Integrity", [sys.executable, "tests/test_links.py"]),
        ("Real Browser Accessibility & Interactive CDP", ["node", "tests/test_interactive.js"]),
    ]

    if not skip_screens:
        raw_steps.append(("Multi-Viewport Screenshot Capture & Dimension Audit", [sys.executable, "scripts/capture_screenshots.py"]))

    if check_live:
        raw_steps.append(("Live Production Endpoint Verification", [sys.executable, "tests/test_links.py", "--live"]))

    step_records = []
    for idx, (name, cmd) in enumerate(raw_steps, 1):
        step_records.append(StepResult(idx, name, cmd, repo_root))

    overall_start = time.time()
    aborted = False

    for record in step_records:
        ok = run_step(record)
        if not ok:
            aborted = True
            print(f"\n[ABORT] Pipeline halted due to failure in step: {record.name}", file=sys.stderr)
            break

    total_time = time.time() - overall_start
    all_ok = print_summary_table(step_records, total_time)

    if not all_ok or aborted:
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()
