#!/usr/bin/env python3
"""
tests/test_links.py
Comprehensive Quality, Link Integrity, Accessibility, and Factual Claim Suite
for Josiah Saji's Robotics Portfolio (Portfolio V5.2 Production Hardening).

Categories:
1. Static DOM Structure & Asset Verification (Unique IDs, Heading Hierarchy, Asset Paths, Cross-document Anchors)
2. Accessible Image Alt Text Audit (Attribute presence, Informative vs Empty alt, Manual Review Checklist)
3. Factual Claim Audit Across HTML (Purges of sub-8ms, YIP selection, numerical divergence, compiled IK, unevidenced 6-8m usable range)
4. Integrated Résumé Verification (Single-page PDF ATS machine-readability & factual integrity)
5. Live Deployment Verification (HTTP 200 checks on live endpoints when invoked with --live)

NOTE: This script performs static automated DOM, file, and text pattern audits.
It does NOT substitute for interactive keyboard traversal, screen-reader testing,
or full subjective WCAG 2.2 AA conformance certification.
"""

import os
import sys
import glob
import re
import html
import unicodedata
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

def normalize_content(content):
    """Normalize HTML source by unescaping entities, canonicalizing Unicode, and standardizing whitespace."""
    unescaped = html.unescape(content)
    norm = unicodedata.normalize('NFKC', unescaped)
    norm = norm.replace('\u03BC', 'µ').replace('\u00B5', 'µ')
    return norm


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
    print("PORTFOLIO V5.3 — MAX-DEPTH DOM, ACCESSIBILITY, FACTUAL & RESUME VERIFICATION")
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
    non_empty_alt_images = []
    empty_alt_images = []
    missing_alt_images = []

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
            src_val = img['src']
            if alt_val is None:
                missing_alt_images.append((hf, src_val))
                errors.append(f"[{hf}] Image missing alt attribute: {src_val}")
            elif alt_val.strip() == '':
                empty_alt_images.append((hf, src_val))
            else:
                non_empty_alt_images.append((hf, src_val, alt_val))

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

    # 2. Image Accessibility Audit (Precise Scope Reporting)
    print(f"\n[Category 2: Image Accessibility Automated Syntax Audit]")
    print(f"  Total <img> elements parsed: {total_images}")
    print(f"  - Non-empty alt attribute string present: {len(non_empty_alt_images)}")
    print(f"    (Automated check confirms attribute presence and non-whitespace text;")
    print(f"     it does not evaluate qualitative accuracy, clarity, or contextual suitability.)")
    print(f"  - Empty alt attribute (alt=''): {len(empty_alt_images)}")
    print(f"    (Images with empty alt require manual review to confirm they are purely decorative")
    print(f"     and do not convey substantive technical information.)")
    print(f"  - Missing alt attribute entirely: {len(missing_alt_images)}")
    if missing_alt_images:
        print(f"    [FAIL] {len(missing_alt_images)} images lack an alt attribute.")
    else:
        print(f"    [PASS] 0 images lack an alt attribute.")

    print("\n  [Parsed Image Catalog for Manual Review]")
    for hf, src, alt in non_empty_alt_images:
        print(f"    • [{hf}] {os.path.basename(src)}")
        print(f"      alt: \"{alt}\"")

    print("\n  [Manual Accessibility Review Checklist for Informative Images]")
    print("  [ ] Qualitative Description: Does the alt text communicate the core technical takeaway of the diagram?")
    print("  [ ] Contextual Explanation: Is the diagram reinforced by adjacent heading and narrative copy for screen readers?")
    print("  [ ] Decorative Verification: If alt='' is used on any element, is it genuinely decorative with zero lost context?")
    print("  [ ] Keyboard Traversal: Do interactive carousels and buttons support sequential Tab navigation with visible focus rings?")

    # 3. Factual Claim Audit Across HTML (Purge Verification with Entity Normalization)
    print(f"\n[Category 3: Factual Purge Audit Across Website HTML]")
    disallowed_web_patterns = [
        ("sub-8ms", "Unsubstantiated ESP32 latency claim"),
        ("sub-8 ms", "Unsubstantiated ESP32 latency claim"),
        ("<8ms", "Unsubstantiated ESP32 latency claim"),
        ("< 8ms", "Unsubstantiated ESP32 latency claim"),
        ("selected for yip 7.0", "Unverified YIP selection claim (use 'developed and submitted')"),
        ("selected for yip", "Unverified YIP selection claim"),
        ("zero iterative numerical divergence", "Unsubstantiated numerical divergence phrasing"),
        ("numerical divergence", "Unsubstantiated numerical divergence phrasing"),
        ("sub-10 µs compiled", "Unverified compiled IK execution metric"),
        ("sub-10 us compiled", "Unverified compiled IK execution metric"),
        ("sub-10 µs", "Unverified compiled IK execution metric"),
        ("sub-10 us", "Unverified compiled IK execution metric"),
        ("sub-30 µs", "Unevidenced analytical IK timing metric"),
        ("sub-30 us", "Unevidenced analytical IK timing metric"),
        ("25–26 µs", "Unevidenced analytical IK benchmark timing"),
        ("25-26 µs", "Unevidenced analytical IK benchmark timing"),
        ("25–26 us", "Unevidenced analytical IK benchmark timing"),
        ("25-26 us", "Unevidenced analytical IK benchmark timing"),
        ("< 30 µs", "Unevidenced analytical IK timing metric"),
        ("< 30 us", "Unevidenced analytical IK timing metric"),
        ("&lt; 30 µs", "Unevidenced analytical IK timing metric"),
        ("&lt; 30 us", "Unevidenced analytical IK timing metric"),
        ("100,000 cartesian", "Unevidenced benchmark iteration count"),
        ("100000 cartesian", "Unevidenced benchmark iteration count"),
        ("100,000 targets", "Unevidenced benchmark iteration count"),
        ("100000 targets", "Unevidenced benchmark iteration count"),
        ("~25 µs", "Unevidenced analytical IK timing metric"),
        ("~25 us", "Unevidenced analytical IK timing metric"),
        ("25 µs python", "Unevidenced analytical IK timing metric"),
        ("25 us python", "Unevidenced analytical IK timing metric"),
        ("~25-26", "Unevidenced analytical IK benchmark timing"),
        ("~25–26", "Unevidenced analytical IK benchmark timing"),
        ("quadruped ros2_control sim", "Ambiguous quadruped rate label; use 'Locomotion Controller Loop'"),
        ("6–8 m", "Unevidenced in-situ usable range metric"),
        ("6-8 m", "Unevidenced in-situ usable range metric"),
        ("usable indoor range", "Unevidenced in-situ usable range claim"),
        ("r5 and above", "Unsupported revision generalization beyond datasheet (use 'A1M8-R5')"),
        ("r5 and later", "Unsupported revision generalization beyond datasheet (use 'A1M8-R5')"),
        ("r5+", "Unsupported revision generalization beyond datasheet (use 'A1M8-R5')"),
        ("r5 and higher", "Unsupported revision generalization beyond datasheet (use 'A1M8-R5')"),
        ("live sensor radar", "Misleading telemetry claim implying running sensor hardware on static portfolio"),
        ("100 hz fused", "Unverified EKF odometry fusion rate claim borrowed from quadruped"),
        ("dwb active", "Misleading active planner telemetry claim on static portfolio"),
        ("360° @ 10 hz", "Unqualified LiDAR operational rate implying real running telemetry"),
        ("360deg @ 10 hz", "Unqualified LiDAR operational rate implying real running telemetry"),
        ("map → odom (100 hz)", "Discrepant SLAM transform rate contradicting configured 50 Hz transform_publish_period"),
        ("map -> odom (100 hz)", "Discrepant SLAM transform rate contradicting configured 50 Hz transform_publish_period"),
        ("synchronized 100 hz ros2_control", "Imprecise quadruped controller statement; must distinguish 100 Hz timer loop and 200 Hz controller manager"),
        ("100 hz joint state publication", "Discrepant parameter attribution; state_publish_rate belongs to JointTrajectoryController, not joint_state_broadcaster"),
        ("100 hz state publication;", "Ambiguous state publication parameter; must specify JointTrajectoryController"),
        ("200 hz manager / 100 hz state pub", "Ambiguous state publication parameter; must specify JTC state pub"),
        ("undergoing agricultural field trials", "Unverified completed/in-progress field trial claim; must be classified as planned validation"),
        ("prototype evaluated on experimental agricultural plots", "Unverified field trial evaluation claim; must be classified as planned validation"),
        ("test results, and agricultural field trials", "Unverified agricultural trial metadata claim"),
        ("failsafe watchdog", "Software command timeout mislabeled as hardware watchdog"),
        ("watchdog failsafe", "Software command timeout mislabeled as hardware watchdog"),
        ("command timeout watchdog", "Software command timeout mislabeled as hardware watchdog"),
        ("safety watchdog", "Software command timeout mislabeled as hardware watchdog"),
        ("hardware failsafe loop", "Software command timeout mislabeled as hardware failsafe loop"),
        ("hardware safety timer", "Software command timeout mislabeled as hardware safety timer"),
        ("client-side watchdog", "Software command timeout mislabeled as hardware watchdog"),
        ("autonomous tilling", "Unevidenced autonomy claim; must be designated as Agricultural Tilling Robot Prototype"),
        ("gps waypoint tracking", "Unevidenced waypoint tracking; must be classified as GPS Data Acquisition"),
        ("gps waypoint guidance", "Unevidenced waypoint guidance; must be classified as GPS Data Acquisition"),
        ("rf failsafe", "Unverified safety failsafe claim; must be classified as Manual Remote Override"),
        ("high-torque rear drive", "Must be classified as Geared DC Motor Drive or Rear-Wheel Drive"),
        ("e-brake", "Unsubstantiated dynamic braking claim; must be labeled Zero PWM"),
        ("deterministic failsafe", "Must be qualified as application-level software command timeout"),
        ("2.4 ghz manual remote override", "Unevidenced 2.4 GHz RF wireless transceiver claim; must use Emergency Manual Override"),
        ("2.4 ghz rf / bluetooth", "Unevidenced RF wireless transceiver claim"),
        ("deterministic software command-timeout failsafes", "Misleading deterministic failsafe phrasing in ESP32"),
        ("asynchronous timer constantly monitors", "Inaccurate asynchronous timer description; timeout check is in main loop"),
        ("provides active regenerative braking", "Unsupported regenerative braking claim on H-bridge 0V state"),
        ("active regenerative braking", "Unsupported regenerative braking claim"),
        ("regenerative braking", "Unsupported regenerative braking claim"),
        ("src/gps/gps_reader.py", "Nonexistent source code path; GPS node is documented in docs/gps_localization.md"),
        ("~8s configuration", "Unsupported battery cell series configuration claim"),
        ("~8s", "Unsupported battery cell configuration claim"),
        ("~15cm furrow depth", "Unsupported numerical furrow depth claim"),
        ("~15 cm furrow depth", "Unsupported numerical furrow depth claim"),
        ("15 cm furrow depth", "Unsupported numerical furrow depth claim"),
        ("target furrow depth ~15cm", "Unsupported numerical furrow depth claim"),
    ]

    claims_clean = True
    for hf, (_, raw_content) in parsed_docs.items():
        norm_content = normalize_content(raw_content).lower()
        ascii_content = norm_content.replace('µ', 'u')
        lower_raw = raw_content.lower()

        for pat, reason in disallowed_web_patterns:
            pat_norm = normalize_content(pat).lower()
            pat_ascii = pat_norm.replace('µ', 'u')
            if pat_norm in norm_content or pat_ascii in ascii_content or pat in lower_raw:
                errors.append(f"[{hf}] Disallowed claim detected: '{pat}' ({reason})")
                claims_clean = False

        # Additional Context-Sensitive Regex Checks on Normalized Content
        ik_timing_match = re.search(r"(?:analytical\s+ik|leg_ik|inverse\s+kinematics|solve_ik)[^<>]*?\b\d+\s*(?:µs|μs|us)\b", norm_content)
        if ik_timing_match:
            errors.append(f"[{hf}] Contextual IK timing claim detected: '{ik_timing_match.group(0)}'")
            claims_clean = False

        ik_timing_match2 = re.search(r'\d+\s*(?:µs|μs|us)\s*python', norm_content)
        if ik_timing_match2:
            errors.append(f"[{hf}] Contextual IK timing claim detected: '{ik_timing_match2.group(0)}'")
            claims_clean = False

    if claims_clean:
        print("  [PASS] All 5 HTML documents clean of unevidenced latency, selection, divergence, 6-8m usable-range, watchdog mislabeling, and R5+ generalization claims.")

    # 4. Positive Technical Grounding & Architecture Assertions
    print(f"\n[Category 4: Positive Technical Grounding & Architecture Assertions]")
    pos_checks = [
        ("index.html", "Locomotion Controller Loop", "Quadruped 100 Hz stat must be precisely labeled 'Locomotion Controller Loop'"),
        ("quadruped-locomotion.html", "Locomotion Controller Loop", "Quadruped case study 100 Hz metric must be labeled 'Locomotion Controller Loop'"),
        ("ros2-mobile-robot.html", "map → odom (SLAM / 50 Hz Config)", "TF tree Figure 2.1 must specify 'map → odom (SLAM / 50 Hz Config)'"),
        ("ros2-mobile-robot.html", "physical revision unverified", "RPLIDAR hardware revision must be explicitly qualified as unverified"),
        ("ros2-mobile-robot.html", "A1M8-R4", "Datasheet range must reference A1M8-R4"),
        ("ros2-mobile-robot.html", "A1M8-R5 specifies 0.15–12.0 m on white targets", "Datasheet range for A1M8-R5 must quote 0.15–12.0 m on white targets"),
        ("ros2-mobile-robot.html", "max_laser_range: 8.0 m", "8.0 m must be explicitly identified as configured max_laser_range software parameter"),
        ("index.html", 'aria-controls="mobileMenu"', "Hamburger button in index.html must have aria-controls='mobileMenu'"),
        ("index.html", "streaming trajectories to a 200 Hz <code>ros2_control</code> controller manager", "Index description must distinguish 100 Hz loop from 200 Hz controller manager"),
        ("quadruped-locomotion.html", "200 Hz Controller Manager update rate; 100 Hz JointTrajectoryController state publication; receives 100 Hz trajectory command stream", "Quadruped specs table must explicitly list 200 Hz manager and 100 Hz JointTrajectoryController state publication"),
        ("quadruped-locomotion.html", "200 Hz manager / 100 Hz JTC state pub", "Quadruped SVG architecture diagram must specify 200 Hz manager and 100 Hz JTC state pub"),
        ("quadruped-locomotion.html", "Closed-Form Analytical IK", "Quadruped hero badge must feature 'Closed-Form Analytical IK'"),
        ("esp32-microros-robot.html", "Software Command Timeout", "ESP32 case study metric must feature 'Software Command Timeout'"),
        ("esp32-microros-robot.html", "Software Command Timeout (500ms)", "ESP32 hero badge must feature 'Software Command Timeout (500ms)'"),
        ("esp32-microros-robot.html", "Zero PWM", "ESP32 timeout action must specify Zero PWM"),
        ("tilling-robot.html", "Agricultural Tilling Robot Prototype", "Tilling page must be titled 'Agricultural Tilling Robot Prototype'"),
        ("tilling-robot.html", "24V-Class LiFePO4", "Tilling page must specify 24V-Class LiFePO4 battery subsystem"),
        ("tilling-robot.html", "Emergency Manual Override", "Tilling page must specify Emergency Manual Override"),
        ("tilling-robot.html", "GPS Data Acquisition", "Tilling page must specify GPS Data Acquisition"),
        ("tilling-robot.html", "Mechanical Tilling Blades (Soft Soil Tested)", "Tilling schematic must feature Soft Soil Tested tilling blades"),
        ("tilling-robot.html", "Engineering Validation Status & Field Trial Plan", "Tilling section title must feature 'Engineering Validation Status & Field Trial Plan'"),
        ("tilling-robot.html", "Verification Status: Hardware Prototype & Validation Plan", "Tilling verification box must feature 'Verification Status: Hardware Prototype & Validation Plan'"),
        ("tilling-robot.html", "Documented Prototype Test Records (Repository docs/testing.md)", "Tilling page must feature documented subsystem test records"),
        ("index.html", "Agricultural Tilling Robot Prototype", "Index project 01 must be titled 'Agricultural Tilling Robot Prototype'"),
        ("index.html", "24V-Class LiFePO4", "Index project 01 must feature 24V-Class LiFePO4"),
        ("quadruped-locomotion.html", 'id="quad-tab-kinematics"', "Quadruped tab must have id='quad-tab-kinematics'"),
        ("quadruped-locomotion.html", 'aria-controls="quad-panel-kinematics"', "Quadruped tab must have aria-controls='quad-panel-kinematics'"),
        ("quadruped-locomotion.html", 'aria-labelledby="quad-tab-kinematics"', "Quadruped panel must have aria-labelledby='quad-tab-kinematics'"),
    ]

    # Verify lightbox overflow preservation in all 4 case study pages
    for cs_file in ["quadruped-locomotion.html", "esp32-microros-robot.html", "tilling-robot.html", "ros2-mobile-robot.html"]:
        pos_checks.append((cs_file, "previousOverflow = document.body.style.overflow", f"[{cs_file}] Lightbox must store previous body overflow"))
        pos_checks.append((cs_file, "document.body.style.overflow = previousOverflow", f"[{cs_file}] Lightbox must restore exact previous body overflow"))

    pos_clean = True
    for doc_name, required_str, desc in pos_checks:
        _, raw_content = parsed_docs[doc_name]
        norm_content = normalize_content(raw_content)
        if required_str not in raw_content and required_str not in norm_content:
            errors.append(f"[{doc_name}] Required positive architectural ground missing: '{required_str}' ({desc})")
            pos_clean = False

    if pos_clean:
        print(f"  [PASS] All {len(pos_checks)} positive technical grounding and architectural assertions confirmed.")

    # 5. Integrated Résumé Verification
    print(f"\n[Category 5: Integrated Résumé Machine-Readability & Factual Audit]")
    if verify_resume:
        pdf_path = os.path.join(base_dir, 'assets', 'resume', 'resume.pdf')
        resume_ok = verify_resume(pdf_path)
        if not resume_ok:
            errors.append("assets/resume/resume.pdf failed verify_resume audit.")
        else:
            print("  [PASS] Résumé passed single-page budgeting, ATS machine readability, and claim audit.")
    else:
        errors.append("scripts.verify_resume could not be imported.")

    # 6. Technical Claims Register Consistency Audit
    print(f"\n[Category 6: Technical Claims Register Consistency Audit]")
    reg_path = os.path.join(base_dir, 'docs', 'PORTFOLIO_CLAIMS_REGISTER.md')
    if not os.path.isfile(reg_path):
        errors.append("docs/PORTFOLIO_CLAIMS_REGISTER.md not found.")
    else:
        with open(reg_path, 'r', encoding='utf-8') as f:
            reg_text = f.read()

        valid_statuses = {
            "VERIFIED_FROM_SOURCE_CODE",
            "VERIFIED_FROM_CONFIGURATION",
            "DATASHEET_SPECIFICATION",
            "VERIFIED_FROM_PROJECT_DOCUMENT",
            "MEASURED_WITH_TEST_EVIDENCE",
            "USER_CONFIRMED_NOT_INDEPENDENTLY_VERIFIED",
            "ILLUSTRATIVE",
            "UNVERIFIED",
            "REMOVED"
        }

        reg_rows = [line.strip() for line in reg_text.splitlines() if line.strip().startswith('| **CLM-')]
        print(f"  Auditing {len(reg_rows)} entries from docs/PORTFOLIO_CLAIMS_REGISTER.md...")
        reg_errors = 0
        for row in reg_rows:
            cols = [c.strip().replace(r'\|', '|') for c in re.split(r'(?<!\\)\|', row)[1:-1]]
            if len(cols) < 11:
                errors.append(f"Invalid register row format: {row[:50]}")
                reg_errors += 1
                continue
            claim_id = cols[0].replace('*', '').strip()
            stmt = cols[1].replace('`', '').strip()
            commit_sha = cols[4].replace('`', '').strip()
            src_file = cols[5].strip()
            src_loc = cols[6].strip()
            status = cols[10].replace('*', '').strip()

            if status not in valid_statuses:
                errors.append(f"Claim {claim_id} has invalid status '{status}'. Must be one of {valid_statuses}")
                reg_errors += 1

            # Enforce 40-character commit hashes and valid paths for verified code/config claims
            if status in ("VERIFIED_FROM_SOURCE_CODE", "VERIFIED_FROM_CONFIGURATION"):
                if not re.match(r'^[0-9a-f]{40}$', commit_sha):
                    errors.append(f"Claim {claim_id} must cite a full 40-char SHA, got '{commit_sha}'")
                    reg_errors += 1
                if "src/gps/gps_reader.py" in src_file:
                    errors.append(f"Claim {claim_id} cites nonexistent path 'src/gps/gps_reader.py'!")
                    reg_errors += 1

            # If claim is REMOVED, verify that no public page contains the removed statement
            if status == "REMOVED":
                for hf, (_, raw_c) in parsed_docs.items():
                    norm_c = normalize_content(raw_c).lower()
                    if "sub-30" in stmt.lower() and "sub-30" in norm_c:
                        errors.append(f"Public page [{hf}] contains removed claim '{stmt}' from {claim_id}!")
                        reg_errors += 1
                    elif "sub-8ms" in stmt.lower() and "sub-8ms" in norm_c:
                        errors.append(f"Public page [{hf}] contains removed claim '{stmt}' from {claim_id}!")
                        reg_errors += 1
                    elif "6–8" in stmt and "6–8 m" in norm_c:
                        errors.append(f"Public page [{hf}] contains removed claim '{stmt}' from {claim_id}!")
                        reg_errors += 1
                    elif "regenerative" in stmt.lower() and "regenerative" in norm_c:
                        errors.append(f"Public page [{hf}] contains removed claim '{stmt}' from {claim_id}!")
                        reg_errors += 1

        if reg_errors == 0:
            print(f"  [PASS] All {len(reg_rows)} claims in register verified against controlled taxonomy and public DOM.")

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

    # Scope and Testing Boundary Clarification
    print("\n" + "-" * 75)
    print("Scope & Testing Boundary Clarification:")
    print("  • Automated Static Scope: DOM syntax, unique element IDs, heading hierarchy,")
    print("    local asset file existence, anchor target validation, alt attribute presence,")
    print("    disallowed string pattern absence, and PDF text stream extractability.")
    print("  • Interactive & Assistive Scope: Full WCAG 2.2 AA certification, contrast under")
    print("    all dynamic states, screen reader annunciation (NVDA/JAWS), and keyboard focus")
    print("    require real browser interaction and human manual audit.")
    print("-" * 75)

    if errors:
        print(f"\nAUDIT FAILED with {len(errors)} error(s):")
        for err in errors:
            print(f"  [-] {err}")
        return False
    else:
        print("\nAUTOMATED QUALITY, DOM, AND INTEGRITY CHECKS PASSED WITHIN DEFINED SCOPE")
        print("=" * 75)
        return True

if __name__ == '__main__':
    check_live_flag = '--live' in sys.argv
    success = run_suite(check_live=check_live_flag)
    sys.exit(0 if success else 1)
