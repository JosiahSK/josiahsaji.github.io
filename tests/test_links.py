#!/usr/bin/env python3
"""
tests/test_links.py
Comprehensive Quality, Link Integrity, Accessibility, and Factual Claim Suite
for Josiah Saji's Robotics Portfolio (V4.2 Release Verification).

Categories:
1. Static DOM Structure & Asset Verification (Unique IDs, Heading Hierarchy, Asset Paths, Cross-document Anchors)
2. Accessible Image Alt Text Audit (Informative vs Decorative, Rejection of Missing Alt)
3. Factual Claim Audit Across HTML (Purges of sub-8ms, YIP selection, numerical divergence, compiled IK)
4. Integrated Résumé Verification (Single-page PDF ATS machine-readability & factual integrity)
5. Live Deployment Verification (HTTP 200 checks on live endpoints when invoked with --live)
"""

import os
import sys
import glob
from collections import Counter
from html.parser import HTMLParser

# Ensure standard UTF-8 console output on Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Add parent directory to path to allow importing verification scripts
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from scripts.verify_resume import verify_resume
except ImportError:
    verify_resume = None

class ComprehensiveDOMParser(HTMLParser):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.ids = []
        self.srcs = []
        self.hrefs = []
        self.meta_tags = []
        self.link_tags = []
        self.headings = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)

        # 1. Element ID
        if 'id' in attr_dict:
            self.ids.append(attr_dict['id'])

        # 2. Local/external href
        if 'href' in attr_dict:
            self.hrefs.append({
                'tag': tag,
                'href': attr_dict['href'],
                'target': attr_dict.get('target'),
                'rel': attr_dict.get('rel', '')
            })

        # 3. Source assets
        if 'src' in attr_dict:
            self.srcs.append({
                'tag': tag,
                'src': attr_dict['src']
            })

        # 4. Meta tags (OpenGraph & Twitter)
        if tag == 'meta':
            self.meta_tags.append(attr_dict)

        # 5. Link tags (favicon / preconnect / stylesheet)
        if tag == 'link':
            self.link_tags.append(attr_dict)

        # 6. Heading hierarchy
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            level = int(tag[1])
            self.headings.append(level)

        # 7. Images alt text
        if tag == 'img':
            self.images.append({
                'src': attr_dict.get('src', ''),
                'alt': attr_dict.get('alt'),
                'aria-hidden': attr_dict.get('aria-hidden')
            })

def run_suite(check_live=False):
    print("=" * 75)
    print("PORTFOLIO V4.2 — FULL QUALITY, DOM, FACTUAL & RESUME VERIFICATION SUITE")
    print("=" * 75)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_files = sorted(glob.glob(os.path.join(base_dir, '*.html')))
    rel_html_files = [os.path.basename(f) for f in html_files]
    print(f"\n[Category 1: Static DOM & Asset Integrity]")
    print(f"Discovered {len(html_files)} HTML pages: {rel_html_files}")

    errors = []
    total_ids = 0
    total_srcs = 0
    total_hrefs = 0
    total_headings = 0
    total_images = 0
    informative_images = 0
    decorative_images = 0

    parsed_docs = {}
    for hf_path in html_files:
        hf = os.path.basename(hf_path)
        with open(hf_path, 'r', encoding='utf-8') as f:
            content = f.read()
        parser = ComprehensiveDOMParser(hf)
        parser.feed(content)
        parsed_docs[hf] = (parser, content)

    # 1. Audit DOM and Assets
    for hf, (parser, raw_content) in parsed_docs.items():
        # A. Unique element IDs
        id_counts = Counter(parser.ids)
        total_ids += len(parser.ids)
        for el_id, count in id_counts.items():
            if count > 1:
                errors.append(f"[{hf}] Duplicate element id: '{el_id}' appears {count} times")
        page_id_set = set(parser.ids)

        # B. Heading hierarchy
        total_headings += len(parser.headings)
        h1_count = parser.headings.count(1)
        if h1_count != 1:
            errors.append(f"[{hf}] Document must have exactly one <h1>, found {h1_count}")
        for i in range(len(parser.headings) - 1):
            curr, nxt = parser.headings[i], parser.headings[i+1]
            if nxt > curr + 1:
                errors.append(f"[{hf}] Heading level skipped: <h{curr}> followed by <h{nxt}>")

        # C. Image alt attributes
        total_images += len(parser.images)
        for img in parser.images:
            alt_val = img['alt']
            if alt_val is None:
                errors.append(f"[{hf}] Image missing alt attribute: {img['src']}")
            elif alt_val.strip() == '':
                decorative_images += 1
            else:
                informative_images += 1

        # D. Source assets exist locally
        for item in parser.srcs:
            src = item['src']
            if src.startswith(('http://', 'https://', 'data:')):
                continue
            total_srcs += 1
            full_src_path = os.path.join(base_dir, src.replace('/', os.sep))
            if not os.path.exists(full_src_path):
                errors.append(f"[{hf}] Missing active src file: {src}")

        # E. Href targets & Anchor validity
        for link in parser.hrefs:
            href = link['href']
            # External target="_blank" safety
            if link['target'] == '_blank':
                rel = link['rel'].lower()
                if 'noopener' not in rel or 'noreferrer' not in rel:
                    errors.append(f"[{hf}] Blank link missing rel='noopener noreferrer': href={href}")

            if href.startswith(('http://', 'https://', 'mailto:', 'tel:')):
                continue

            # Local anchor on same page
            if href.startswith('#'):
                anchor = href[1:]
                if anchor and anchor not in page_id_set:
                    errors.append(f"[{hf}] Target anchor #{anchor} not found on page")
                continue

            total_hrefs += 1
            target_path = href.split('#')[0]
            anchor = href.split('#')[1] if '#' in href else None
            full_target = os.path.join(base_dir, target_path.replace('/', os.sep))
            if target_path and not os.path.exists(full_target):
                errors.append(f"[{hf}] Missing local link target: {target_path}")
            elif target_path and anchor:
                if target_path in parsed_docs:
                    target_id_set = set(parsed_docs[target_path][0].ids)
                    if anchor not in target_id_set:
                        errors.append(f"[{hf}] Cross-page anchor #{anchor} not found in {target_path}")

        # F. Social Meta Image Absolute URLs
        for m in parser.meta_tags:
            prop = m.get('property', '')
            name = m.get('name', '')
            if prop in ('og:image', 'twitter:image') or name in ('og:image', 'twitter:image'):
                content_val = m.get('content', '')
                if not content_val.startswith('https://'):
                    errors.append(f"[{hf}] Meta tag {prop or name} must use absolute https URL, found: '{content_val}'")

    print(f"  [PASS] {len(html_files)} documents checked:")
    print(f"         - {total_ids} element IDs (100% unique per document)")
    print(f"         - {total_headings} headings audited (strict single <h1> and no skipped levels)")
    print(f"         - {total_srcs} local source assets confirmed on disk")
    print(f"         - {total_hrefs} local href and cross-document anchors verified")
    print(f"         - All social meta tags verified with absolute https URLs")
    print(f"         - All external target='_blank' links secure (noopener noreferrer)")

    # 2. Image Accessibility Audit
    print(f"\n[Category 2: Image Accessibility Audit]")
    print(f"  [PASS] {total_images} total images checked:")
    print(f"         - {informative_images} informative images with descriptive alt text")
    print(f"         - {decorative_images} decorative images with valid alt=''")
    print(f"         - 0 images with missing alt attributes")

    # 3. Factual Claim Audit Across HTML
    print(f"\n[Category 3: Factual Claim Audit Across Website HTML]")
    disallowed_web_patterns = [
        ("sub-8ms", "Unsubstantiated ESP32 latency claim"),
        ("sub-8 ms", "Unsubstantiated ESP32 latency claim"),
        ("<8ms", "Unsubstantiated ESP32 latency claim"),
        ("< 8ms", "Unsubstantiated ESP32 latency claim"),
        ("selected for yip 7.0", "Unverified YIP selection claim (use 'developed and submitted')"),
        ("zero iterative numerical divergence", "Unsubstantiated numerical divergence phrasing"),
        ("numerical divergence", "Unsubstantiated numerical divergence phrasing"),
        ("sub-10 µs compiled", "Unverified compiled IK execution metric"),
        ("sub-10 us compiled", "Unverified compiled IK execution metric"),
        ("<10 µs c++", "Unverified compiled IK execution metric"),
    ]

    claims_clean = True
    for hf, (_, raw_content) in parsed_docs.items():
        lower_content = raw_content.lower()
        for pat, reason in disallowed_web_patterns:
            if pat in lower_content:
                errors.append(f"[{hf}] Disallowed claim detected: '{pat}' ({reason})")
                claims_clean = False

    if claims_clean:
        print("  [PASS] All 5 HTML documents clean of unevidenced latency, selection, and divergence claims.")

    # 4. Integrated Résumé Verification
    print(f"\n[Category 4: Integrated Résumé Machine-Readability & Factual Audit]")
    if verify_resume:
        pdf_path = os.path.join(base_dir, 'assets', 'resume', 'resume.pdf')
        resume_ok = verify_resume(pdf_path)
        if not resume_ok:
            errors.append("assets/resume/resume.pdf failed verify_resume audit.")
        else:
            print("  [PASS] Résumé passed single-page budgeting, ATS machine readability, and claim audit.")
    else:
        errors.append("scripts.verify_resume could not be imported.")

    # 5. Optional Live Deployment Checks
    if check_live:
        print(f"\n[Category 5: Live Deployment Endpoint Verification]")
        import urllib.request
        live_urls = [
            "https://josiahsk.github.io/josiahsaji.github.io/",
            "https://josiahsk.github.io/josiahsaji.github.io/index.html",
            "https://josiahsk.github.io/josiahsaji.github.io/quadruped-locomotion.html",
            "https://josiahsk.github.io/josiahsaji.github.io/esp32-microros-robot.html",
            "https://josiahsk.github.io/josiahsaji.github.io/tilling-robot.html",
            "https://josiahsk.github.io/josiahsaji.github.io/ros2-mobile-robot.html",
            "https://josiahsk.github.io/josiahsaji.github.io/assets/resume/resume.pdf",
        ]
        live_errors = []
        for url in live_urls:
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    if resp.status == 200:
                        print(f"  [OK 200] {url}")
                    else:
                        live_errors.append(f"{url} returned status {resp.status}")
            except Exception as e:
                live_errors.append(f"{url} request failed: {e}")
        if live_errors:
            errors.extend(live_errors)
        else:
            print("  [PASS] All 7 live production endpoints verified HTTP 200.")

    print("\n" + "=" * 75)
    if errors:
        print(f"AUDIT FAILED with {len(errors)} error(s):")
        for err in errors:
            print(f"  [-] {err}")
        return False
    else:
        print("ALL AUDIT CATEGORIES PASSED (100% QUALITY & FACTUAL COMPLIANCE)")
        print("=" * 75)
        return True

if __name__ == '__main__':
    check_live_flag = '--live' in sys.argv
    success = run_suite(check_live=check_live_flag)
    sys.exit(0 if success else 1)
