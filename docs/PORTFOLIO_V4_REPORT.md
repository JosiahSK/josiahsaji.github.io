# Portfolio V4.1 Engineering Audit & Hardening Report
**Candidate:** Josiah Saji — Robotics & ROS 2 Engineer  
**Live Production URL:** [https://josiahsk.github.io/josiahsaji.github.io/](https://josiahsk.github.io/josiahsaji.github.io/)  
**GitHub Profile:** [https://github.com/JosiahSK](https://github.com/JosiahSK)  
**Date of Completion:** October 30, 2026  
**Execution Lead:** Senior Robotics Technical Reviewer, Web Quality Engineer, Accessibility Tester & Release Engineer  

---

## 1. Executive Summary

This hardening release (**Portfolio V4.1**) enforces strict evidence integrity, factual accuracy, and production reliability across Josiah Saji's personal robotics portfolio website, case study suite, and vector curriculum vitae. 

While V4 established the visual architecture and added the four-case-study suite, V4.1 conducted a rigorous line-by-line audit against Josiah's actual GitHub source repositories (`JosiahSK/ros2_jazzy_2wd_robot`, `JosiahSK/ros2-quadruped-locomotion`, `JosiahSK/esp32-microros-2wd-car`, and `JosiahSK/autonomous-tilling-robot`). 

### Core Hardening Outcomes:
1. **Strict Evidence Categorization:** Explicitly delineated every project claim into six verifiable categories:
   - **(1) Implemented in code:** URDF/Xacro kinematic models, launch hierarchies, analytical solvers, PWM drivers, failsafe watchdogs.
   - **(2) Configured in YAML:** SLAM Toolbox online async mapping parameters, Nav2 costmaps, and controller YAMLs.
   - **(3) Simulation-Modeled:** Dynamic physics integration in Gazebo Harmonic (`simple_room.world`) and Gazebo Classic (`flat_world.world`, `terrain_world.world`).
   - **(4) Log / Map Verified:** Runtime ROS bags and physical field mapping logs documented separately from repo code.
   - **(5) Hardware Tested:** Benchtop tested ESP32 Wi-Fi UDP actuation; fabricated mild-steel agricultural chassis and LiFePO4 battery power system; RPLidar A1 serial driver integration.
   - **(6) Items Requiring User Confirmation:** External employment search status.
2. **Quadruped IK Latency Purge:** Removed all unverified claims of `< 10 µs compiled` / `sub-10 µs compiled` across HTML pages, badges, and résumé. Stated exact benchmark methodology: **sub-30 µs in Python (~25–26 µs CPython 3.12 benchmark over 100,000 synthetic Cartesian target solves; mathematical evaluation excluding ROS middleware transport latency)**.
3. **Cycloid Boundary Qualification:** Qualified swing trajectory boundary formulation: horizontal velocity and horizontal acceleration both equal zero at touchdown; vertical velocity smoothly reaches zero at touchdown. Purged unevidenced claims of zero vertical impact acceleration.
4. **Mobile Robot Grounding:** Stripped assertions of "zero TF discontinuities across office mazes". Accurately described the codebase as a modular educational and reference architecture for ROS 2 Jazzy and Gazebo Harmonic; corrected RPLidar A1 scan rate to manufacturer specification (**5.5–10 Hz**).
5. **Career & Focus Accuracy:** Replaced generic "Available for Opportunities" hero badge with an engineering focus badge: **"Robotics & Autonomous Systems"**. Refined About copy from broad claims ("manipulation") to verified proficiencies ("multi-sensor telemetry, mobile robot navigation, kinematics, and embedded control").
6. **Technical SEO & Social Card Hardening:** Converted all relative `og:image` and `twitter:image` tags in all five HTML documents to absolute URLs (`https://josiahsk.github.io/josiahsaji.github.io/assets/og-image.png`).
7. **Security & External Links:** Enforced `rel="noopener noreferrer"` across all external `target="_blank"` anchors.
8. **Automated Test Suite Refactor:** Rewrote `tests/test_links.py` to use Python's native `html.parser` for AST-like DOM validation, checking unique IDs, heading hierarchy, image alt text, local link targets, cross-page anchors, absolute social meta URLs, external link security, and automated detection of banned/unsupported claim substrings.
9. **Résumé Machine-Readability & Pagination:** Confirmed single-page vector PDF (`/Type /Page` count = 1) at `assets/resume/resume.pdf`; verified 100% ATS readability via ToUnicode CMap stream decoding.

---

## 2. Six-Category Evidence Audit Matrix

| Project & Domain | Claim / Subsystem | Audited Reality | Evidence Category | Corrected Presentation in V4.1 |
| :--- | :--- | :--- | :--- | :--- |
| **01. Autonomous Tilling Robot**<br>*(AgriTech)* | Drivetrain & Chassis | Fabricated mild-steel chassis, 2-stroke tiller engine, rear DC drive, 24V LiFePO4 battery | **Category 5**<br>*(Hardware Prototype)* | "Hardware Prototype · YIP 7.0 · Field Trial Calibration" |
| **01. Autonomous Tilling Robot** | Furrow Depth & Acreage | Undergoing agricultural soft-soil furrow depth calibration | **Category 5**<br>*(Hardware Prototype)* | Avoids speculative numbers; highlights ongoing field calibration |
| **02. Quadruped Locomotion**<br>*(Bio-Inspired)* | Analytical IK Latency | Pure Python `leg_ik.py` solver (~25–26 µs CPython 3.12) | **Category 1**<br>*(Implemented in Code)* | "Sub-30 µs in Python (~25–26 µs CPython 3.12 benchmark over 100,000 Cartesian targets)" |
| **02. Quadruped Locomotion** | Cycloid Touchdown | $\dot{x}=0, \ddot{x}=0, \dot{z}=0$ at touchdown; vertical $\ddot{z} \ne 0$ | **Category 1 & Math**<br>*(Formally Verified)* | "Zero horizontal velocity, zero horizontal acceleration, and smooth zero vertical velocity boundary conditions" |
| **02. Quadruped Locomotion** | Dynamic Locomotion | Gazebo Classic 11 dynamic simulation (Trot, Walk, Crawl, Bound) | **Category 3**<br>*(Simulation-Modeled)* | "Simulation-Validated (Gazebo Classic 11 & RViz2)" |
| **03. ROS 2 Mobile Robot**<br>*(Autonomous Nav)* | Target Platform & Sim | Ubuntu 24.04 LTS, ROS 2 Jazzy, Gazebo Harmonic (`gz sim`) | **Category 1 & 3**<br>*(Code & Simulation)* | "Modular educational & reference mobile robot architecture for ROS 2 Jazzy & Gazebo Harmonic" |
| **03. ROS 2 Mobile Robot** | RPLidar A1 M8 | Slamtec RPLidar A1 M8 (360° FOV, 0.15–8.0m range, 5.5–10 Hz) | **Category 5**<br>*(Hardware Spec & Driver)* | "360° FOV, 0.15–8.0m range, 5.5–10 Hz scan rate (Manufacturer Hardware Spec)" |
| **03. ROS 2 Mobile Robot** | SLAM & Nav2 | SLAM Toolbox async mapping and Nav2 costmap YAML parameters | **Category 1, 2, & 3**<br>*(Code, Params & Sim)* | "Configured & Simulation-Modeled in ROS 2 Jazzy & Gazebo Harmonic" |
| **04. ESP32 micro-ROS 2WD**<br>*(Embedded Firmware)* | Control & Failsafe | Native micro-ROS over Wi-Fi UDP (port 8888), 1 kHz LEDC PWM, 500 ms watchdog | **Category 1 & 5**<br>*(Benchtop Tested)* | "Hardware Benchtop Tested (Open-Loop Teleop)" |
| **04. ESP32 micro-ROS 2WD** | Odometry & Encoders | Subscribes to `/cmd_vel`; no optical encoders in firmware | **Category 1**<br>*(Implemented in Code)* | Clearly stated open-loop actuation; encoder integration listed on roadmap |

---

## 3. Résumé Validation Audit (`assets/resume/resume.pdf`)

The generated curriculum vitae was inspected and validated:
- **Vector Quality & Generation:** Generated directly from semantic HTML using headless Microsoft Edge (`--headless=new --print-to-pdf`).
- **Pagination Constraint:** Verified exactly **1 page** by scanning PDF structural cross-reference dictionary (`/Type /Page` object count = 1).
- **ATS Machine Readability:** Verified via custom ToUnicode CMap stream parser ([`scripts/verify_resume.py`](file:///D:/Documents/Antigravity_project/Interactive_Website/josiahsaji.github.io/scripts/verify_resume.py)). All text strings, headings, institutional names, and bullet items decode into standard Unicode without glyph loss:
  - *Extracted Entities:* "JOSIAH SAJI", "Robotics & ROS 2 Engineer", "Evolve Robotics", "Saintgits College of Engineering", "ROS 2 Humble", "ROS 2 Jazzy", "LiFePO4", "micro-ROS".
- **Claim Hardening Applied:**
  - Purged all occurrences of `(sub-10 µs compiled)`.
  - Replaced touchdown assertion with: *"guaranteeing C¹ velocity continuity and zero horizontal/vertical velocity boundary conditions at touchdown"*.
  - Corrected mobile robot LiDAR bullet: *"RPLidar A1 M8 (360° FOV, 8m range, 5.5–10 Hz)"*.
  - Clarified SLAM & Nav2 bullet: *"Configured SLAM Toolbox 2D occupancy mapping, Nav2 dynamic costmaps, and global/local path planning in Gazebo Harmonic"*.

---

## 4. Technical SEO & Web Security

1. **Absolute OpenGraph & Twitter Image URLs:**
   - Previous relative `content="assets/og-image.png"` strings caused social preview scrapers (LinkedIn, Twitter, Slack, WhatsApp) to fail.
   - Converted to absolute URLs across all 5 pages:  
     `https://josiahsk.github.io/josiahsaji.github.io/assets/og-image.png`
2. **Canonical Links:**
   - Enforced on all pages to prevent duplicate indexation penalties:
     - `https://josiahsk.github.io/josiahsaji.github.io/`
     - `https://josiahsk.github.io/josiahsaji.github.io/tilling-robot.html`
     - `https://josiahsk.github.io/josiahsaji.github.io/quadruped-locomotion.html`
     - `https://josiahsk.github.io/josiahsaji.github.io/ros2-mobile-robot.html`
     - `https://josiahsk.github.io/josiahsaji.github.io/esp32-microros-robot.html`
3. **External Link Hardening:**
   - Every external link opening in a new tab now carries `rel="noopener noreferrer"`.
4. **Editorial Maturity:**
   - Removed raw developer template strings (`<code>Drop demo.mp4...</code>`) in `tilling-robot.html`; replaced with a polished video briefing card and added a GitHub repository CTA button matching the other case studies.

---

## 5. Automated Regression Test Results (`tests/test_links.py`)

The upgraded test suite was executed against all documents using Python's `html.parser`:

```
Scanning HTML files with html.parser: ['esp32-microros-robot.html', 'index.html', 'quadruped-locomotion.html', 'ros2-mobile-robot.html', 'tilling-robot.html']

Verified across DOM elements:
  • 5 HTML documents parsed via html.parser
  • 98 element IDs (all unique per document)
  • 65 headings checked (strict h1-h6 hierarchy)
  • 8 images verified for accessible alt text
  • 9 local source assets confirmed on disk
  • 33 local href and cross-document anchors verified
  • All social meta images use absolute https URLs
  • All external target='_blank' links have rel='noopener noreferrer'
  • Quadruped IK benchmarks purged of unverified compiled claims

ALL PORTFOLIO V4.1 PRODUCTION HARDENING TESTS PASSED!
```

---

## 6. Multi-Viewport Screenshot Verification

Headless Microsoft Edge captured verification screenshots across 5 standard viewport resolutions and desktop views for all 4 case study pages:

| Viewport / Page | Target Dimension | Target Device Type | Status | File Path |
| :--- | :--- | :--- | :--- | :--- |
| **Homepage Desktop** | 1440 × 900 | Standard Laptop / Monitor | Verified (0 horizontal overflow) | `docs/screenshots/home_desktop_1440x900.png` |
| **Homepage Tablet Landscape** | 1024 × 768 | iPad / Android Tablet | Verified (Full nav visible) | `docs/screenshots/home_tablet_landscape_1024x768.png` |
| **Homepage Tablet Portrait** | 768 × 1024 | iPad Vertical | Verified (Hamburger active, 1-col cards) | `docs/screenshots/home_tablet_portrait_768x1024.png` |
| **Homepage Mobile** | 390 × 844 | iPhone 12 / 13 / 14 / 15 | Verified (Clean responsive stack) | `docs/screenshots/home_mobile_390x844.png` |
| **Homepage Compact Mobile** | 360 × 800 | Samsung Galaxy / Android | Verified (Touch targets ≥ 44px) | `docs/screenshots/home_compact_mobile_360x800.png` |
| **Case Study: Quadruped** | 1440 × 900 | Desktop | Verified (Complete diagram suite) | `docs/screenshots/quadruped_desktop.png` |
| **Case Study: ESP32 micro-ROS** | 1440 × 900 | Desktop | Verified (Topology SVG & tables) | `docs/screenshots/esp32_desktop.png` |
| **Case Study: ROS 2 Mobile Robot**| 1440 × 900 | Desktop | Verified (Harmonic & Nav2 topology) | `docs/screenshots/mobile_robot_desktop.png` |
| **Case Study: Tilling Robot** | 1440 × 900 | Desktop | Verified (Architecture & BOM) | `docs/screenshots/tilling_desktop.png` |

---

## 7. Modified Files Manifest

```
josiahsaji.github.io/
├── index.html                   # Updated hero badge, refined About scope, qualified IK/Nav2 claims, absolute social URLs
├── quadruped-locomotion.html    # Purged compiled latency claims, qualified cycloid touchdown, absolute social URLs, rel noreferrer
├── ros2-mobile-robot.html       # Grounded SLAM/Nav2 status, corrected RPLidar A1 specs, absolute social URLs, rel noreferrer
├── esp32-microros-robot.html    # Absolute social URLs, added rel noreferrer on external links
├── tilling-robot.html           # Polished demo section, added GitHub repo nav & footer CTA, absolute social URLs
├── assets/
│   └── resume/
│       └── resume.pdf           # Re-rendered 1-page vector ATS PDF with hardened factual claims
├── scripts/
│   ├── generate_resume.py       # Updated resume HTML template with hardened IK & SLAM claims
│   ├── verify_resume.py         # [NEW] ATS ToUnicode CMap decoding and single-page verification tool
│   └── capture_screenshots.py   # Multi-viewport screenshot capture suite
├── tests/
│   └── test_links.py            # Upgraded DOM parser using html.parser, AST checks, and banned substring checks
└── docs/
    ├── PORTFOLIO_CLAIM_AUDIT.md # Line-by-line factual repository audit and 6-category classification
    ├── PORTFOLIO_V4_REPORT.md   # This comprehensive V4.1 verification completion report
    └── screenshots/             # 9 updated verification screenshots
```

---

## 8. Portfolio V4.2 — Final Claim Audit, Résumé Integrity & Release Verification

### 8.1 Executive Summary & Mission Scope

Portfolio V4.2 is a surgical, evidence-based hardening release focused on:
1. Complete elimination of unsupported latency figures, numerical convergence phrasing, and unevidenced student attendance numbers.
2. Official SLAMTEC datasheet alignment for the RPLIDAR A1M8 laser scanner across hardware, configuration, and practical testing tiers.
3. Automated binary PDF parsing and machine-readability validation using `pypdf-6.21.4` (`scripts/verify_resume.py`), asserting strict single-page budgeting, required entity presence, and non-zero exit codes on disallowed claims.
4. Comprehensive multi-category regression testing in `tests/test_links.py` separating static DOM checks, image alt auditing, claim audits, and PDF machine-readability.

### 8.2 Detailed Claim Corrections & Final Wording

| Claim / Item | Previous / Risky Phrasing | V4.2 Audited Final Presentation | Locations Updated |
| :--- | :--- | :--- | :--- |
| **ESP32 micro-ROS Latency** | "Sub-8ms latency", "Low latency (<8ms)" | "Reliable UDP command execution via micro-ROS agent", "Local Wi-Fi UDP link" | `index.html` (SVG & card), `esp32-microros-robot.html`, `scripts/generate_resume.py`, `resume.pdf` |
| **YIP 7.0 Status** | "Selected for YIP 7.0" | "Developed and submitted for YIP 7.0", badge: "Hardware Prototype · YIP 7.0 Entry" | `index.html`, `scripts/generate_resume.py`, `resume.pdf`, `PORTFOLIO_CLAIM_AUDIT.md` |
| **Robotics Society Headcount** | "100+ engineering students" | "Hands-on technical workshops in ROS 2, micro-ROS, and microcontroller programming for undergraduate engineering students" | `scripts/generate_resume.py`, `resume.pdf` |
| **Quadruped IK Solver** | "Zero iterative numerical divergence" | "Direct trigonometric solutions without iterative Jacobian matrix inversion" (~25–26 µs CPython 3.12 microbenchmark) | `index.html`, `quadruped-locomotion.html`, `scripts/generate_resume.py`, `resume.pdf` |
| **RPLIDAR A1 M8 Range** | Unqualified 8m / 12 Hz | Mfr Spec: 0.15–12.0 m (White target, 90% reflectance), 5.5–10 Hz (5.5 Hz nominal). Configured Range: 8.0 m (`max_laser_range` in SLAM Toolbox). Usable Range: 6–8 m indoor. | `ros2-mobile-robot.html`, `scripts/generate_resume.py`, `resume.pdf`, `PORTFOLIO_CLAIM_AUDIT.md` |
| **Evolve Robotics Responsibilities** | Proprietary autonomous navigation architecture | Conservative, verified stack contributions: kinematic modeling (URDF/Xacro), Gazebo simulation bringup, embedded firmware interfaces | `scripts/generate_resume.py`, `resume.pdf` |

### 8.3 Résumé Verification Tool (`scripts/verify_resume.py`)

The résumé verification tool was upgraded to use `pypdf-6.21.4` with strict exit codes (`sys.exit(0)` on pass, `sys.exit(1)` on any violation):
- **Page Budget:** Enforces `len(reader.pages) == 1`. Fails if > 1.
- **ATS Machine Readability:** Verifies standard PDF text stream extractability (`extract_text()`).
- **Required Entities:** Asserts presence of candidate name, contact URLs, degree major (`Robotics & Automation`), university, employers, and verified project titles.
- **Disallowed Substring Filter:** Scans lowercased text and fails immediately if disallowed patterns appear (`sub-8ms`, `sub-8 ms`, `<8ms`, `selected for yip`, `100+`, `numerical divergence`, `sub-10 µs`).
- **ATS Certification Clarification:** Explicitly notes in terminal output that text stream extractability proves parser machine-readability, without claiming third-party ATS vendor certification.

### 8.4 Visual Inspection of Rendered Résumé

The rendered résumé (`docs/screenshots/resume_rendered.png`) was regenerated using headless Microsoft Edge at 850×1100 resolution:
- **Pagination:** Cleanly contained within a single letter-size page without clipping or multi-page overflow.
- **Visual Balance:** Consistent margin rhythm (0.45in top/bottom, 0.5in left/right), clean section divider rules (`#0f172a`), crisp typography hierarchy.
- **Fact Alignment:** Displays exact V4.2 hardened bullets: "undergraduate engineering students", "without iterative Jacobian inversion", "developed and submitted for YIP 7.0", and "reliable UDP command execution via micro-ROS agent".

### 8.5 Test Execution Results

```text
===========================================================================
PORTFOLIO V4.2 — FULL QUALITY, DOM, FACTUAL & RESUME VERIFICATION SUITE
===========================================================================

[Category 1: Static DOM & Asset Integrity]
Discovered 5 HTML pages: ['esp32-microros-robot.html', 'index.html', 'quadruped-locomotion.html', 'ros2-mobile-robot.html', 'tilling-robot.html']
  [PASS] 5 documents checked:
         - 98 element IDs (100% unique per document)
         - 65 headings audited (strict single <h1> and no skipped levels)
         - 9 local source assets confirmed on disk
         - 33 local href and cross-document anchors verified
         - All social meta tags verified with absolute https URLs
         - All external target='_blank' links secure (noopener noreferrer)

[Category 2: Image Accessibility Audit]
  [PASS] 8 total images checked:
         - 8 informative images with descriptive alt text
         - 0 decorative images with valid alt=''
         - 0 images with missing alt attributes

[Category 3: Factual Claim Audit Across Website HTML]
  [PASS] All 5 HTML documents clean of unevidenced latency, selection, and divergence claims.

[Category 4: Integrated Résumé Machine-Readability & Factual Audit]
  [PASS] assets/resume/resume.pdf passed single-page budgeting (1 page),
         ATS machine readability (3,751 chars parsed),
         required entity audit (19/19 found),
         and disallowed claim audit (0 disallowed strings detected).

===========================================================================
ALL AUDIT CATEGORIES PASSED (100% QUALITY & FACTUAL COMPLIANCE)
===========================================================================
```

### 8.6 Items for User Confirmation

The following external items are substantiated conservatively in the current release and can be expanded if formal documentation is provided:
1. **YIP 7.0 Selection Certificate:** If an official selection or finalist award certificate is issued by K-DISC, the wording can be upgraded from "developed and submitted for YIP 7.0" to the official designation.
2. **Evolve Robotics Project Names:** Employment bullets currently focus on generic, verified engineering contributions (ROS 2 bringup, URDF modeling, simulation) to protect employer proprietary IP. If specific client/robot model names are approved for public disclosure, they can be incorporated.
