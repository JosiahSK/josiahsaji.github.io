#!/usr/bin/env python3
"""
tests/test_claim_normalization.py
Automated Regression Test Suite for HTML Entity Normalization and Prohibited Claims Detection.

Verifies that the normalization pipeline:
1. Correctly unescapes HTML entities (&mu;, &micro;, &#956;, &#x3BC;, &#181;, etc.).
2. Normalizes Unicode representations (NFKC, U+03BC, U+00B5).
3. Handles all forms of dash (en-dash, em-dash, hyphen).
4. Detects unevidenced microsecond IK timing across body text, metadata, SVGs, and attributes.
5. Reliably passes valid, verified technical terminology.
"""

import os
import re
import sys
import html
import unicodedata

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

def normalize_content(content):
    """
    Robust multi-stage text normalization pipeline:
    1. Unescapes HTML entities (&mu;, &#956;, etc.)
    2. NFKC Unicode normalization
    3. Canonicalizes micro symbols (U+03BC, U+00B5 -> µ)
    4. Normalizes dashes (–, —, − -> -)
    5. Normalizes whitespace
    6. Canonicalizes microseconds ([uµ]\s*s -> µs, microseconds -> µs)
    """
    if not content:
        return ""
    # 1. Unescape HTML named & numeric entities
    text = html.unescape(content)
    # 2. NFKC Unicode decomposition/composition
    text = unicodedata.normalize('NFKC', text)
    # 3. Canonicalize micro symbol
    text = text.replace('\u03bc', 'µ').replace('\u00b5', 'µ')
    # 4. Standardize dashes to standard ASCII hyphen
    text = re.sub(r'[\u2013\u2014\u2212]', '-', text)
    # 5. Standardize whitespace
    text = re.sub(r'\s+', ' ', text)
    # 6. Standardize microsecond notation
    text = re.sub(r'\b(?:microseconds?)\b', 'µs', text, flags=re.IGNORECASE)
    text = re.sub(r'[uµ]\s*s\b', 'µs', text, flags=re.IGNORECASE)
    return text

# Core prohibited IK timing regex pattern
PROHIBITED_IK_PATTERN = re.compile(
    r'(?:'
    r'~?\s*25(?:\.\d+)?\s*µs|'
    r'25\s*-\s*26\s*µs|'
    r'sub\s*-\s*(?:10|30)\s*µs|'
    r'<\s*(?:10|30)\s*µs|'
    r'~?\s*\d+(?:\.\d+)?\s*µs\s*python'
    r')',
    re.IGNORECASE
)

# Core prohibited tilling robot claim patterns
PROHIBITED_TILLING_PATTERNS = [
    (re.compile(r'(?:design target:\s*)?~?\s*15\s*cm\s*(?:depth|furrow)', re.IGNORECASE), "15cm depth/furrow claim"),
    (re.compile(r'24\s*v(?:\s*-\s*class)?\s*dc\s*geared\s*motor', re.IGNORECASE), "24V DC geared motor claim"),
    (re.compile(r'2\.4\s*ghz\s*(?:manual\s*)?(?:remote\s*)?override', re.IGNORECASE), "2.4 GHz override claim"),
    (re.compile(r'(?:fail-safe\s*)?rf\s*remote\s*teleoperation', re.IGNORECASE), "RF remote teleoperation claim"),
    (re.compile(r'teleop\s*failsafe\s*cutoff', re.IGNORECASE), "teleop failsafe cutoff claim"),
    (re.compile(r'gps\s*heading\s*drift\s*at\s*low\s*crawl\s*speeds', re.IGNORECASE), "GPS heading drift at low crawl speeds claim"),
    (re.compile(r'0\.3\s*[-–—]\s*0\.6\s*m/s', re.IGNORECASE), "0.3-0.6 m/s heading speed correlation claim"),
]

def find_prohibited_tilling_claims(raw_text):
    """Normalize text and return list of tilling violations."""
    norm = normalize_content(raw_text)
    matches = []
    for pat, desc in PROHIBITED_TILLING_PATTERNS:
        found = pat.findall(norm)
        if found:
            matches.extend(found)
    return matches

def find_prohibited_claims(raw_text):
    """Normalize text and return list of matches."""
    norm = normalize_content(raw_text)
    # Also check lowercased ASCII version
    ascii_norm = norm.replace('µ', 'u')
    matches = PROHIBITED_IK_PATTERN.findall(norm)
    return matches

def test_unit_normalization():
    print("[Unit Test 1: Entity & Unicode Normalization Pipeline]")
    test_cases = [
        ("~25 µs", True),
        ("~25 μs", True),
        ("~25 us", True),
        ("~25 microseconds", True),
        ("~25 &mu;s", True),
        ("~25 &micro;s", True),
        ("~25 &#956;s", True),
        ("~25 &#x3BC;s", True),
        ("~25 &#181;s", True),
        ("25–26 µs", True),
        ("25-26 µs", True),
        ("sub-30 µs", True),
        ("<30 µs", True),
        ("&lt;30 µs", True),
        ("25.5 µs", True),
        ("Closed-Form Analytical IK", False),
        ("Direct trigonometric equations", False),
        ("200 Hz Controller Manager", False),
        ("Design Target: ~15cm Depth", True),
        ("~15cm depth", True),
        ("24V DC Geared Motor", True),
        ("2.4 GHz Manual Override", True),
        ("Fail-safe RF remote teleoperation protocol", True),
        ("teleop failsafe cutoff", True),
        ("GPS Heading Drift at Low Crawl Speeds", True),
        ("0.3–0.6 m/s", True),
        ("0.3-0.6 m/s", True),
        ("Soft-Soil Blade Evaluation", False),
        ("24V-Class LiFePO4 Battery", False),
        ("24V DC Motor", False),
        ("Mechanical Emergency Override", False),
        ("2.4 GHz Wi-Fi", False),
        ("GPS Coordinate Drift", False),
        ("Forward driving: stable at 0.3 m/s", False),
        ("GPS logging: ~3 m drift observed", False),

    ]

    failed = 0
    for sample, should_match in test_cases:
        matches = find_prohibited_claims(sample) + find_prohibited_tilling_claims(sample)
        matched = len(matches) > 0
        if matched == should_match:
            print(f"  [PASS] '{sample}' -> matched={matched} (expected {should_match})")
        else:
            print(f"  [FAIL] '{sample}' -> matched={matched} (expected {should_match})", file=sys.stderr)
            failed += 1

    return failed == 0

def test_fixture_files():
    print("\n[Unit Test 2: Fixture Files Permanent Regression Suite]")
    fixtures_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "claims")
    if not os.path.isdir(fixtures_dir):
        print(f"  [FAIL] Fixtures directory not found: {fixtures_dir}", file=sys.stderr)
        return False

    fixture_expectations = {
        "prohibited_ik_timing.html": True,
        "prohibited_ik_metadata.html": True,
        "prohibited_ik_svg.html": True,
        "prohibited_ik_attributes.html": True,
        "valid_ik_terminology.html": False,
        "prohibited_tilling_claims.html": True,
        "valid_tilling_claims.html": False,
    }

    all_passed = True
    for fname, should_contain_violations in fixture_expectations.items():
        fpath = os.path.join(fixtures_dir, fname)
        if not os.path.isfile(fpath):
            print(f"  [FAIL] Fixture file missing: {fname}", file=sys.stderr)
            all_passed = False
            continue

        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        matches = find_prohibited_claims(content) + find_prohibited_tilling_claims(content)
        has_violations = len(matches) > 0

        if has_violations == should_contain_violations:
            status = "detected violations" if has_violations else "clean (no violations)"
            print(f"  [PASS] {fname}: {status} as expected ({len(matches)} matches)")
        else:
            print(f"  [FAIL] {fname}: has_violations={has_violations}, expected={should_contain_violations}", file=sys.stderr)
            all_passed = False

    return all_passed

def main():
    print("=" * 78)
    print("PORTFOLIO V5.3.2 — CLAIM NORMALIZATION & REGRESSION TEST HARNESS")
    print("=" * 78)

    t1_ok = test_unit_normalization()
    t2_ok = test_fixture_files()

    if t1_ok and t2_ok:
        print("\n[PASS] All claim normalization and fixture tests passed successfully.")
        sys.exit(0)
    else:
        print("\n[FAIL] One or more normalization tests failed.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
