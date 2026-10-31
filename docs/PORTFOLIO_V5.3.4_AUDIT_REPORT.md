# ANTIGRAVITY V5.3.4 — RESIDUAL CLAIM PURGE, EVIDENCE RECONCILIATION & FINAL RELEASE AUDIT REPORT

**Release:** Antigravity V5.3.4  
**Audit Date:** 2026-10-31  
**Project:** Josiah Saji — Robotics Engineering Portfolio  
**Repository:** [https://github.com/JosiahSK/josiahsaji.github.io](https://github.com/JosiahSK/josiahsaji.github.io)  
**Production Baseline Commit:** `b24cb452bd1818f3e47e2f5b99fd6935acdd31e1` (V5.3.3)  
**Feature Branch:** `feature/portfolio-v5.3.4-residual-claim-audit`  
**Live Production URL:** [https://josiahsk.github.io/josiahsaji.github.io/](https://josiahsk.github.io/josiahsaji.github.io/)  

---

## 1. Executive Summary & Release Purpose

Antigravity V5.3.4 is a focused technical accuracy, evidence-governance, and test-hardening release. It preserves the established dark industrial visual identity, typography, color accents, layout, animations, and responsive behavior while eliminating all remaining unevidenced claims regarding the agricultural tilling robot prototype, reconciling claims-register status counts with mathematical precision, correcting previous reporting misattributions, and hardening the automated test harness with dedicated regression fixtures.

### Key Corrections in V5.3.4
1. **Homepage Tilling Schematic SVG (`index.html`):** Purged obsolete strings from the technical schematic (`Design Target: ~15cm Depth` &rarr; `Soft-Soil Blade Evaluation`, `24V LiFePO4 Battery` &rarr; `24V-Class LiFePO4 Battery`, `24V DC Geared Motor` &rarr; `24V DC Motor`, and `2.4 GHz Manual Override` &rarr; `Mechanical Emergency Override`).
2. **Case Study Wireless Claims Purge (`tilling-robot.html`):** Replaced `Fail-safe RF remote teleoperation protocol` with verified capabilities (`Documented ROS 2 node architecture · GPS NMEA data acquisition · LiDAR obstacle detection`) and removed `teleop failsafe cutoff` from the embedded controller BOM note.
3. **GPS Challenge Grounding (`tilling-robot.html`):** Retitled Challenge 02 to `GPS Coordinate Drift`. Purged unsupported claims regarding speed-correlated heading degradation at 0.3–0.6 m/s. Maintained forward driving (0.3 m/s) and GPS logging (~3 m drift) as separate documented prototype test records.
4. **Challenge Sections Rewritten as Design Considerations:** Audited Challenge 01 (Power Architecture & Subsystem Isolation) and Challenge 03 (Traction Management in Agricultural Soil), eliminating unevidenced failure narratives (in-rush resets, TVS diodes, Kerala mud counter-torque, cleated tyre fixes, gear ratio adjustments) and framing them strictly as engineering design considerations and qualitative evaluations.
5. **Purge of Unverified Mechanical/Electrical Assertions:** Removed or qualified claims regarding cleated mud tires, front stabilizer caster, heavy-duty shaft coupling, extruded heat sink, ceramic patch antenna details, and fixed buck converter quantities.
6. **YIP 7.0 Claim ID & Classification Discrepancy Fix:** Corrected previous reporting confusion: `CLM-TILL-01` is the author-confirmed YIP 7.0 submission (`USER_CONFIRMED_NOT_INDEPENDENTLY_VERIFIED`), while `CLM-TILL-08` is the mechanical Emergency Manual Override Lever (`VERIFIED_FROM_PROJECT_DOCUMENT`).
7. **Drivetrain & Steering Language Discipline:** Purged the word `geared` when referencing the tilling robot drive motor and eliminated all `Ackermann` / `Ackermann-style` claims in favor of documented `servo steering` or `front steering servo`.
8. **Mathematical Claims Register Reconciliation:** Recomputed exact status totals programmatically directly from parsed register rows, eliminating conflicting legacy counts.
9. **Regression Test Suite Hardening:** Added explicit negative pattern checks, contextual page validators, and dedicated regression test fixtures (`prohibited_tilling_claims.html` and `valid_tilling_claims.html`) to `tests/test_links.py` and `tests/test_claim_normalization.py`.
10. **Multi-Viewport Visual Verification:** Generated fresh 26-screenshot suite in `docs/screenshots/v5.3.4/` validating desktop, tablet, and mobile layouts.

---

## 2. Authoritative Evidence Reconciliation: Agricultural Tilling Robot

All corrections were reconciled against the authoritative source repository:
- **Repository:** [`JosiahSK/autonomous-tilling-robot`](https://github.com/JosiahSK/autonomous-tilling-robot)
- **Immutable Commit SHA:** `19fe9cc2f644f2947d716eead1e7bef3d797993c`
- **Inspected Files:** `README.md`, `docs/future_work.md`, `docs/gps_localization.md`, `docs/obstacle_avoidance.md`, `docs/software_architecture.md`, `docs/system_architecture.md`, `docs/testing.md`, `docs/throttle_control.md`.
- **Physical Repository Tree:** Contains documentation and code snippets; contains no executable `src/` directory, mechanical CAD models, PCB layout packages, or dimensioned fabrication drawings.

| Subsystem | Source Evidence Reference | Established Ground Truth | Purged / Prohibited Phrasing |
| :--- | :--- | :--- | :--- |
| **Battery Subsystem** | `README.md:37`, `docs/testing.md:12` | 24V-class LiFePO4 battery system; stable at 23.8V under operational load. | "24V nominal (~8S configuration)", cell capacity, internal BMS specs |
| **Drivetrain Motor** | `README.md:42-43`, `docs/system_architecture.md:39` | Single 24V DC drive motor (BOM Qty: 1) driving rear axle via chain transmission. | "24V DC Geared Motor", "dual geared motors", "differential-drive torque control" |
| **Steering Subsystem** | `docs/system_architecture.md:40` | Front steering servo; direction control via servo. | "Ackermann steering geometry", "Ackermann-style linkage" |
| **Emergency Takeover** | `docs/throttle_control.md:5-8` | Mechanical emergency throttle takeover lever on throttle cable mechanism. | "2.4 GHz Manual Override", "RF remote teleoperation", "wireless signal-loss cutoff" |
| **GPS Localization** | `docs/gps_localization.md:16-40`, `docs/testing.md:20, 22` | Documented ROS 2 GPS node code sample and architecture. Forward driving: stable at 0.3 m/s; GPS logging: ~3 m drift observed (separate test records). | `src/gps/gps_reader.py`, "GPS heading drift at crawl speeds (0.3–0.6 m/s)", tested EKF improvement |
| **Tilling Blades** | `docs/testing.md:24` | Front rototiller blades evaluated as effective on soft soil. | "Design Target: ~15cm Depth", "~15 cm Furrow Depth", measured trenching metrics |
| **Obstacle Stop** | `docs/testing.md:21`, `docs/obstacle_avoidance.md:22-37` | Obstacle stop at 50 cm recorded in prototype test notes. | Independent safety certification, dynamic obstacle swerving |
| **Chassis / Frame** | `README.md:88`, `docs/testing.md` | Welded mild-steel frame prototype fabricated and bench-tested. | High-traction cleated wheels, front stabilizer caster, heavy-duty shaft coupling |

---

## 3. Detailed Audit of Page Modifications

### 3.1 Homepage Schematic (`index.html`)
The technical schematic for Project 01 (Agricultural Tilling Robot Prototype) in `index.html` was corrected to align with ground truth:
- **Line 359:** `<text ...>Design Target: ~15cm Depth</text>` &rarr; `<text ...>Soft-Soil Blade Evaluation</text>`
- **Line 365:** `<text ...>24V LiFePO4 Battery</text>` &rarr; `<text ...>24V-Class LiFePO4 Battery</text>`
- **Line 373:** `<text ...>24V DC Geared Motor</text>` &rarr; `<text ...>24V DC Motor</text>`
- **Line 375:** `<text ...>2.4 GHz Manual Override</text>` &rarr; `<text ...>Mechanical Emergency Override</text>`

### 3.2 Tilling Case Study (`tilling-robot.html`)
The case study page underwent a thorough claim purge and qualification:
1. **Illustrative Schematic & Overview:**
   - Replaced `Cleated Mud Tires` with `Rear Drive Wheels`.
   - Replaced `Rear Chain Drive &middot; Front Rototiller Counter-Torque` with `Rear Chain Drive &middot; Front Tilling Implement`.
   - In system overview narrative, updated `ceramic patch antenna GPS module` to `NEO-6M GPS receiver for field data acquisition` and clarified power delivery with step-down logic regulation.
2. **Architecture SVG & Signal Paths:**
   - Replaced `Rear cleated agricultural drive wheels` with `• Rear drive axle &amp; wheels`.
   - Replaced `24V Power bus with flyback suppression` with `24V Power bus to motor driver`.
   - Updated legend text to remove unevidenced claims of inductive transient isolation and ignition noise suppression, stating: `Buck converters step 24V-class LiFePO4 battery power down to 5V/3.3V logic rails sharing common system ground.`
3. **Subsystem Summary Cards:**
   - Mechanical: Replaced `High-traction cleated drive wheels · Front stabilizer caster · Heavy-duty shaft coupling to rotary tiller drum` with `Welded mild steel chassis · Rear chain drive transmission · Front steering servo · Two-stroke engine tilling mechanism`.
   - Software: Replaced `Fail-safe RF remote teleoperation protocol` with `Documented ROS 2 node architecture · GPS NMEA data acquisition · LiDAR obstacle detection · Embedded motor drive loop`.
4. **Bill of Materials Table:**
   - Motor driver note: Replaced `with extruded heat sink` with `PWM speed and directional control for 24V DC drive motor`.
   - Embedded controller note: Removed `teleop failsafe cutoff`, updated to `Executes motor PWM, sensor polling, and throttle servo actuation`.
   - GPS module: Replaced `NEO-6M GPS Receiver (Ceramic Patch Antenna)` with `NEO-6M GPS Receiver`.
   - Buck converter quantity: Changed from fixed `2` to `Subsystem` (note: `Steps 24V LiFePO4 down for subsystem logic and sensor rails with common ground`).
5. **Challenges & Solutions Reframing:**
   - **Challenge 01:** Retitled to `Power Architecture & Subsystem Isolation`. Eliminated unevidenced failure narrative (in-rush current causing 5V bus resets, addition of TVS diodes and filter capacitors). Framed as an engineering design consideration: powering a 24V DC motor alongside digital computing logic using independent step-down buck regulators and common ground.
   - **Challenge 02:** Retitled to `GPS Coordinate Drift`. Removed unevidenced claims of noisy heading at 0.3–0.6 m/s crawl speeds causing erratic steering. Accurately documented prototype test record of ~3 m coordinate drift in standalone GPS logging, maintaining 0.3 m/s forward driving as a separate test record, with EKF fusion designated as planned future work.
   - **Challenge 03:** Retitled to `Traction Management in Agricultural Soil`. Removed unevidenced narrative of Kerala soil counter-torque pushing the robot backward, loss of grip, shifting chassis mass, aggressive cleated tires, and adjusted gear ratios. Framed as a design consideration regarding rotational tine resistance, highlighting qualitative soft-soil testing with quantitative traction evaluation planned for future trials.

---

## 4. Reconciliation of Claims Register Status Distribution

The status distribution in `docs/PORTFOLIO_CLAIMS_REGISTER.md` was programmatically audited using regex parsing on unescaped pipes (`(?<!\\)\|`). The register comprises exactly 34 rows, distributed as follows:

| Classification Status | Count | Verified / Governance Description |
| :--- | :---: | :--- |
| `VERIFIED_FROM_SOURCE_CODE` | 8 | Code-level verification in repository source (IK, timers, loop rates) |
| `VERIFIED_FROM_CONFIGURATION` | 7 | Formally verified configuration files (`controllers.yaml`, Xacro, world) |
| `VERIFIED_FROM_PROJECT_DOCUMENT` | 5 | Established from formal repository documentation, BOM, and specs |
| `MEASURED_WITH_TEST_EVIDENCE` | 2 | Repeatable test records (`testing.md`: soft-soil blade, 50cm obstacle stop) |
| `DATASHEET_SPECIFICATION` | 3 | Manufacturer published specifications (A1M8-R4, A1M8-R5, ESP32) |
| `USER_CONFIRMED_NOT_INDEPENDENTLY_VERIFIED` | 1 | Author-asserted project submission without public third-party receipt (`CLM-TILL-01`) |
| `ILLUSTRATIVE` | 1 | Conceptual / interactive UI schematic (`CLM-UI-01`) |
| `UNVERIFIED` | 1 | Hardware revision unconfirmed from code (`CLM-AMR-01`) |
| `REMOVED` | 6 | Historical unevidenced claims permanently purged from public pages |
| **Total Registered Entries** | **34** | **100% Accounted For** |

### Reconciliation of Legacy Reporting Errors
- In previous V5.3.3 handover notes, a legacy breakdown (`25 verified from code, 6 from documents, 3 user-confirmed`) was erroneously referenced. That breakdown did not reflect the actual 34 rows of the register.
- In previous handover documentation, `CLM-TILL-08` was mistakenly labeled as the YIP submission claim. The actual register correctly designates:
  - **`CLM-TILL-01`:** `Agricultural Tilling Robot Prototype: YIP 7.0 Innovation Programme Submission` (`USER_CONFIRMED_NOT_INDEPENDENTLY_VERIFIED`).
  - **`CLM-TILL-08`:** `Emergency Manual Override Lever (Throttle Takeover Mechanism)` (`VERIFIED_FROM_PROJECT_DOCUMENT`).
This audit report confirms and locks this taxonomy alignment.

---

## 5. Local vs. CI Test Reporting Boundaries

To prevent ambiguity, testing boundaries are strictly partitioned:

| Test Scope | Local Test Runner (`tests/run_all_tests.py`) | GitHub Actions CI (`.github/workflows/quality-gate.yml`) |
| :--- | :---: | :---: |
| Python Bytecode Compilation | **EXECUTED & PASSED** | **EXECUTED & PASSED** |
| JavaScript Syntax Checks (`script.js`, `test_interactive.js`) | **EXECUTED & PASSED** | **EXECUTED & PASSED** |
| Claim Normalization & Regression Fixtures | **EXECUTED & PASSED** | **EXECUTED & PASSED** |
| Static DOM, Links, Alt Text & Claims Integrity | **EXECUTED & PASSED** | **EXECUTED & PASSED** |
| ATS Machine-Readability & Résumé Factual Integrity | **EXECUTED & PASSED** | **EXECUTED & PASSED** (via `test_links.py`) |
| Real Browser Interaction & CDP Accessibility (`test_interactive.js`) | **EXECUTED & PASSED** (75/75) | Not run in CI (avoids headless browser setup instability) |
| Multi-Viewport Screenshot Suite (`capture_screenshots.py`) | **EXECUTED & PASSED** (26/26) | Not run in CI (avoids GPU/display raster rendering differences) |
| Live Production HTTP 200 Verification | **EXECUTED & PASSED** (7/7) | Executed locally post-deployment |

---

## 6. Comprehensive Test Results

### 6.1 Compilation & Static Analysis
- `python -m compileall scripts tests`: **PASS** (100% clean compilation across all Python scripts and test suites).
- `node --check script.js`: **PASS** (Zero syntax errors).
- `node --check tests/test_interactive.js`: **PASS** (Zero syntax errors).

### 6.2 Claim Normalization & Fixture Test Suite (`tests/test_claim_normalization.py`)
- **Unit Test 1 (Entity & Normalization Pipeline):** 35 test cases evaluated. Verified detection of unevidenced IK timing (various Unicode entities, dashes, microseconds) and verified detection of prohibited tilling claims (`Design Target: ~15cm Depth`, `~15cm depth`, `24V DC Geared Motor`, `2.4 GHz Manual Override`, `Fail-safe RF remote teleoperation protocol`, `teleop failsafe cutoff`, `GPS Heading Drift at Low Crawl Speeds`, `0.3–0.6 m/s`). Confirmed that valid technical strings (`Soft-Soil Blade Evaluation`, `24V-Class LiFePO4 Battery`, `24V DC Motor`, `Mechanical Emergency Override`, `2.4 GHz Wi-Fi`, `GPS Coordinate Drift`) pass cleanly without false positives.
- **Unit Test 2 (Permanent Regression Fixtures):** 7 HTML fixture files evaluated:
  - `prohibited_ik_timing.html`: Detected violations (14 matches) &mdash; **PASS**
  - `prohibited_ik_metadata.html`: Detected violations (2 matches) &mdash; **PASS**
  - `prohibited_ik_svg.html`: Detected violations (3 matches) &mdash; **PASS**
  - `prohibited_ik_attributes.html`: Detected violations (3 matches) &mdash; **PASS**
  - `valid_ik_terminology.html`: Clean (0 matches) &mdash; **PASS**
  - `prohibited_tilling_claims.html`: Detected violations (7 matches) &mdash; **PASS**
  - `valid_tilling_claims.html`: Clean (0 matches) &mdash; **PASS**

### 6.3 Static DOM, Links, Alt Text & Factual Audit (`tests/test_links.py`)
- **Category 1 (Static DOM & Asset Integrity):** 6 documents checked (`404.html`, `esp32-microros-robot.html`, `index.html`, `quadruped-locomotion.html`, `ros2-mobile-robot.html`, `tilling-robot.html`). 143 unique element IDs, 67 audited headings (strict single `<h1>`, zero skipped levels), 12 local assets on disk, 43 local anchors verified, absolute HTTPS social meta tags, secure `target="_blank"` attributes &mdash; **PASS**.
- **Category 2 (Image Accessibility):** 11 informative `<img>` tags parsed, 100% present substantive alt descriptions &mdash; **PASS**.
- **Category 3 (Factual Purge Audit Across HTML):** All 6 HTML pages clean of all prohibited pattern strings &mdash; **PASS**.
- **Category 4 (Positive Technical Grounding Assertions):** All 42 positive assertions confirmed across all pages &mdash; **PASS**.
- **Category 5 (Résumé Factual & ATS Integrity):** Verified `assets/resume/resume.pdf` (137,651 bytes, 3,743 characters, 1 page, ATS parseable, zero disallowed strings, confirmed entities) &mdash; **PASS**.
- **Category 6 (Claims Register Consistency):** Audited 34 entries from `docs/PORTFOLIO_CLAIMS_REGISTER.md` against public DOM and controlled taxonomy &mdash; **PASS**.

### 6.4 Real Browser Interaction & CDP Accessibility (`tests/test_interactive.js`)
- Executed in headless Chromium (`msedge.exe` on port 53806):
  - **Suite 1:** Local server security & path traversal resistance (7 tests) &mdash; **PASS**
  - **Suite 2:** Quadruped tabs keyboard traversal, roving tabindex, ARIA states (16 tests) &mdash; **PASS**
  - **Suite 3:** Accessible lightbox modal behavior across all 4 case study pages (focus trap, Escape key, body overflow restore, zero duplicate IDs) (40 tests) &mdash; **PASS**
  - **Suite 4:** Mobile navigation disclosure pattern, keyboard focus advancement, drawer close (12 tests) &mdash; **PASS**
- **Total Interaction Tests:** **75 Passed, 0 Failed**.

### 6.5 Multi-Viewport Screenshot Matrix (`scripts/capture_screenshots.py`)
- Generated 26 screenshots into `docs/screenshots/v5.3.4/`:
  - 10 Homepage Viewports (1440&times;900 Desktop down to 320&times;700 Small Mobile).
  - 16 Case Study Viewports (4 viewports for each of the 4 case studies: Desktop 1440&times;900, Tablet 1024&times;768, Mobile 390&times;844, Compact Mobile 360&times;800).
- 100% dimension verification confirmed by Pillow raster inspection.
- Screenshot catalog published in `docs/screenshots/v5.3.4/README.md`.

---

## 7. Résumé Integrity Audit

- **File:** [`assets/resume/resume.pdf`](file:///D:/Documents/Antigravity_project/Interactive_Website/josiahsaji.github.io/assets/resume/resume.pdf)
- **Size:** 137,651 bytes (134.4 KB)
- **Page Count:** 1 page (strictly maintained single-page geometry)
- **Extracted Text:** 3,743 characters
- **ATS Parseability:** 100% machine-readable text stream without OCR artifacts
- **Negative Pattern Checks:** Verified absence of `15cm`, `15 cm`, `ackermann`, `geared motor`, `2.4 ghz`, `watchdog`, `regenerative`, `e-brake`, `deterministic failsafe`, `~8s`, `selected for yip`, `100+ students`, `sub-30 µs`, `25–26 µs`.

---

## 8. Final Release Decision & Quality Verdict

```
================================================================================
                    FINAL RELEASE VERIFICATION VERDICT
================================================================================
  RELEASE VERSION:    V5.3.4 (Residual Claim Purge & Final Release Audit)
  PRODUCTION BASELINE: b24cb452bd1818f3e47e2f5b99fd6935acdd31e1
  VERIFICATION STATUS: PRODUCTION READY — ALL V5.3.4 REQUIRED GATES PASSED
================================================================================
```
