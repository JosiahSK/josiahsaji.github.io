#!/usr/bin/env python3
"""
scripts/verify_resume.py
Rigorous verification of assets/resume/resume.pdf for Portfolio V4.2.

Validates:
1. File existence and valid PDF structure.
2. Page budget: Exactly 1 page (fails if > 1).
3. ATS Machine-Readability: Full text extraction using pypdf.
4. Factual Integrity & Required Fields: Essential contact info, education,
   experience, and verified project details.
5. Strict Exclusion: Disallowed / unsubstantiated claims (latency benchmarks without logs,
   unsubstantiated competition selection, unverified student counts, numerical claims).

NOTE: Text extraction verifies parser extractability (ATS machine-readability).
It does not claim proprietary third-party ATS certification.
"""

import os
import sys
import pypdf

# Ensure standard UTF-8 console output on Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

RESUME_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'resume', 'resume.pdf')

REQUIRED_KEYWORDS = [
    # Contact & Identity
    ("Josiah Saji", "Candidate Name"),
    ("josiahsaji2k03@gmail.com", "Email Address"),
    ("linkedin.com/in/josiah-saji", "LinkedIn Profile"),
    ("github.com/JosiahSK", "GitHub Profile"),
    ("josiahsk.github.io", "Portfolio Website"),
    
    # Education
    ("Saintgits College of Engineering", "Undergraduate Institution"),
    ("Robotics & Automation", "Degree Major"),
    ("B.Tech", "Degree Type"),
    
    # Work Experience
    ("Evolve Robotics", "Current Employer"),
    ("Robotics Engineer", "Job Title"),
    ("Robotics Society", "Leadership Role"),
    
    # Projects & Technical Coverage
    ("Quadruped Locomotion", "Project: Quadruped"),
    ("micro-ROS", "Project: micro-ROS 2WD Car"),
    ("Autonomous Mobile Robot", "Project: ROS 2 AMR"),
    ("Autonomous Tilling Robot", "Project: Tilling Robot"),
    ("RPLidar A1", "Hardware: RPLidar A1"),
    ("8m", "Laser mapping range"),
    ("LiFePO4", "Hardware: Battery Chemistry"),
    ("SLAM", "Capability: SLAM"),
    ("Nav2", "Capability: Nav2"),
]

# Disallowed claims that lack rigorous empirical documentation or official certification
DISALLOWED_PATTERNS = [
    ("sub-8ms", "Unsubstantiated ESP32 round-trip latency metric"),
    ("sub-8 ms", "Unsubstantiated ESP32 round-trip latency metric"),
    ("<8ms", "Unsubstantiated ESP32 round-trip latency metric"),
    ("< 8ms", "Unsubstantiated ESP32 round-trip latency metric"),
    ("selected for yip", "Unsubstantiated YIP 7.0 finalist/selection status (use 'developed and submitted')"),
    ("100+ students", "Unsubstantiated workshop attendee headcount"),
    ("100+ engineering", "Unsubstantiated workshop attendee headcount"),
    ("100+", "Unsubstantiated 100+ headcount metric"),
    ("zero iterative numerical divergence", "Unsubstantiated numerical divergence claim (use analytical closed-form IK)"),
    ("numerical divergence", "Unsubstantiated numerical divergence phrasing"),
    ("sub-10 µs", "Unverified compiled IK execution metric"),
    ("sub-10 us", "Unverified compiled IK execution metric"),
    ("< 10 µs", "Unverified compiled IK execution metric"),
    ("< 10 us", "Unverified compiled IK execution metric"),
]

def verify_resume(pdf_path=RESUME_PATH):
    print("=" * 70)
    print("PORTFOLIO V4.2 — RÉSUMÉ INTEGRITY & ATS READABILITY AUDIT")
    print("=" * 70)
    print(f"Target PDF: {pdf_path}")
    
    if not os.path.exists(pdf_path):
        print(f"[-] FAILED: File does not exist at {pdf_path}")
        return False
        
    file_size = os.path.getsize(pdf_path)
    print(f"[+] File exists. Size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    if file_size < 10000:
        print(f"[-] FAILED: File size abnormally small ({file_size} bytes)")
        return False
        
    try:
        reader = pypdf.PdfReader(pdf_path)
    except Exception as e:
        print(f"[-] FAILED to parse PDF with pypdf: {e}")
        return False

    # 1. Page Count Validation
    num_pages = len(reader.pages)
    print(f"[+] Total pages parsed: {num_pages}")
    if num_pages != 1:
        print(f"[-] FAILED: Expected exactly 1 page for single-page robotics résumé, got {num_pages}")
        return False
    print("    [PASS] Single-page layout strictly maintained.")

    # 2. Text Extraction & Machine-Readability
    page = reader.pages[0]
    extracted_text = page.extract_text() or ""
    text_len = len(extracted_text)
    print(f"[+] Extracted text length: {text_len:,} characters")
    if text_len < 1000:
        print(f"[-] FAILED: Extracted text unexpectedly short ({text_len} chars); potential font encoding issue.")
        return False
    print("    [PASS] Text stream is fully parseable by standard PDF text extractors (ATS machine-readable).")

    # 3. Required Fields Verification
    print("\n--- Verifying Required Fields & Verified Entities ---")
    missing_required = []
    text_lower = extracted_text.lower()
    
    for kw, description in REQUIRED_KEYWORDS:
        if kw.lower() in text_lower:
            print(f"    [OK] {description} ('{kw}') found.")
        else:
            print(f"    [MISSING] {description} ('{kw}') NOT found!")
            missing_required.append(f"{description} ('{kw}')")

    if missing_required:
        print(f"\n[-] FAILED: {len(missing_required)} required fields missing from résumé text:")
        for item in missing_required:
            print(f"    - {item}")
        return False
    print("    [PASS] All required identity, education, experience, and project entities confirmed.")

    # 4. Strict Exclusion of Unsubstantiated Claims
    print("\n--- Verifying Absence of Disallowed / Unsubstantiated Claims ---")
    found_disallowed = []
    for pattern, rationale in DISALLOWED_PATTERNS:
        if pattern.lower() in text_lower:
            print(f"    [VIOLATION] Disallowed string '{pattern}' detected! Rationale: {rationale}")
            found_disallowed.append((pattern, rationale))
        else:
            print(f"    [CLEAR] '{pattern}' absent.")

    if found_disallowed:
        print(f"\n[-] FAILED: {len(found_disallowed)} disallowed/unsubstantiated claims detected:")
        for pattern, rationale in found_disallowed:
            print(f"    - '{pattern}': {rationale}")
        return False
    print("    [PASS] All disallowed and unevidenced claims strictly purged.")

    print("\n" + "=" * 70)
    print("RÉSUMÉ INTEGRITY AUDIT: ALL CHECKS PASSED (100%)")
    print("NOTE: Verified machine-readability confirms parser text extractability.")
    print("=" * 70)
    return True

if __name__ == '__main__':
    success = verify_resume()
    sys.exit(0 if success else 1)
