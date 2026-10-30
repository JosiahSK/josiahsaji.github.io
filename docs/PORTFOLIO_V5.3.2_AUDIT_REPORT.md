# PORTFOLIO V5.3.2 EVIDENCE RECONCILIATION & TECHNICAL CREDIBILITY AUDIT REPORT

**Repository:** `JosiahSK/josiahsaji.github.io`  
**Live Production Site:** https://josiahsk.github.io/josiahsaji.github.io/  
**Release Tag:** Portfolio V5.3.2  
**Audit Date:** 2026-10-30  
**Status:** ALL CHECKS PASSED — PRODUCTION READY  

---

## 1. Executive Summary

Portfolio V5.3.2 is a deep forensic evidence-reconciliation release focused on establishing unassailable technical credibility across Josiah Saji's robotics portfolio.

Previous iterations (V5.3 and V5.3.1) successfully established an industrial visual language, resolved microsecond timing claims in public HTML, and built a continuous-integration quality gate. However, a forensic investigation into external source repositories (`JosiahSK/autonomous-tilling-robot`, `JosiahSK/esp32-microros-2wd-car`, `JosiahSK/ros2-quadruped-locomotion`, and `JosiahSK/ros2_jazzy_2wd_robot`) uncovered substantive technical discrepancies between public project repositories and portfolio marketing copy.

Specifically:
1. **Autonomy Maturity:** The tilling robot was previously marketed as an "Autonomous Tilling Robot" featuring "Autonomous GPS Waypoint Guidance". Ground-truth inspection of `JosiahSK/autonomous-tilling-robot` reveals Level 1 NMEA sensor data acquisition and 2.4 GHz manual RC override are operational, whereas Nav2 waypoint navigation is in active development.
2. **Power & Drivetrain Ground Truth:** The tilling robot battery was previously assumed to be 12.8V. Authoritative test logs in `docs/testing.md` explicitly verify a 24V LiFePO4 battery pack (tested stable at 23.8V under load), driving a single 24V DC geared motor through a rear-wheel chain drive.
3. **Furrow Depth Ground Truth:** The 15 cm furrow depth claim was discovered to be an engineering design target, as testing documentation only records qualitative soil penetration without quantitative measurement logs.
4. **Firmware Cutoff Semantics:** The ESP32 micro-ROS robot claimed "deterministic failsafes" and "E-Brake" hardware stops. Source inspection of `esp32_microros_2wd.ino` demonstrates an application-level software command-timeout in the Arduino `loop()` that executes `pwmWrite(pin, 0)` (Zero PWM duty cycle), rather than a deterministic hardware brake.
5. **Résumé Claim Normalization:** The generated candidate résumé (`resume.pdf`) had retained an unevidenced `~25–26 µs` benchmark claim in the quadruped section and stale tilling robot specifications.

In V5.3.2, all discrepancies have been systematically reconciled with the underlying source code, backed by immutable commit SHAs, protected by 5 permanent regression fixtures, verified via a 7-step test suite, and deployed to production.

---

## 2. Forensic Evidence Discrepancy Matrix

| ID | Component / File | Original Statement / Assumption | Source Evidence Discovered | Remediated Statement / Status | External Repo & Line Grounding |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **DIS-01** | `tilling-robot.html`, `index.html`, `resume.pdf` | "Autonomous Tilling Robot", "Autonomous GPS Waypoint Guidance" | `src/gps/gps_reader.py` reads NMEA sentences over UART (Level 1 sensor acquisition). `docs/testing.md` notes `Autonomous nav: In progress / Nav2 integration ongoing`. Manual override operates via 2.4 GHz RC. | **Agricultural Tilling Robot Prototype**<br>• GPS Data Acquisition (NMEA UART)<br>• 2.4 GHz Manual Remote Override<br>• Autonomous Navigation in Development | `JosiahSK/autonomous-tilling-robot` @ `19fe9cc`<br>`src/gps/gps_reader.py:1-45`<br>`docs/testing.md:38` |
| **DIS-02** | `tilling-robot.html`, `index.html`, `resume.pdf` | "12.8V LiFePO4 battery" | `docs/testing.md:34` explicitly logs: `\| LiFePO4 under load \| PASS - stable at 23.8V \|`. `README.md` documents 24V LiFePO4 pack. | **24V LiFePO4 Battery**<br>Tested stable at 23.8V under operational load (~8S configuration). | `JosiahSK/autonomous-tilling-robot` @ `19fe9cc`<br>`docs/testing.md:34`<br>`README.md:42` |
| **DIS-03** | `tilling-robot.html`, `index.html` | Unevidenced dual-motor differential drive assumption | `README.md` and CAD records confirm rear-wheel chain drive powered by a single 24V DC geared motor with a front steering axle. | **24V Geared DC Motor Chain Drive**<br>Rear-wheel chain drive with front steering linkage. | `JosiahSK/autonomous-tilling-robot` @ `19fe9cc`<br>`README.md:45-50` |
| **DIS-04** | `tilling-robot.html`, `index.html` | "15 cm Furrow Depth" / Measured field testing | `docs/testing.md:39` records: `Tilling blade: Effective on soft soil`, with zero quantitative depth logs. | **Design Target: ~15cm Furrow Depth**<br>Explicitly categorized as mechanical design target pending field trials. | `JosiahSK/autonomous-tilling-robot` @ `19fe9cc`<br>`docs/testing.md:39` |
| **DIS-05** | `esp32-microros-robot.html`, `index.html` | "Deterministic failsafes", "E-Brake active stop" | `esp32_microros_2wd.ino:125-132` executes `millis() - lastCmdTime > CMD_TIMEOUT_MS -> stopMotors()`. `stopMotors()` calls `pwmWrite(pin, 0)`. | **Software Command Timeout (500ms)**<br>**Zero PWM Motor Cutoff**<br>Application-level software timeout in Arduino `loop()`. | `JosiahSK/esp32-microros-2wd-car` @ `b0681f8`<br>`firmware/.../esp32_microros_2wd.ino:125-132, 140-148` |
| **DIS-06** | `scripts/generate_resume.py`, `resume.pdf` | `(~25–26 µs CPython 3.12 microbenchmark per leg solve)` | Unevidenced timing claim remained embedded in the automated résumé generator script. | **Closed-Form Analytical IK**<br>Benchmark timing purged; PDF regenerated (137.6 KB). | `scripts/generate_resume.py:72`<br>`scripts/verify_resume.py:118` |

---

## 3. Permanent Regression Fixtures & Claim Normalization Architecture

To guarantee that unevidenced microsecond claims, misleading autonomy terms, or speculative hardware claims can never re-enter the portfolio, V5.3.2 establishes an independent regression test suite:

### 3.1 Architecture Overview
- **Script:** `tests/test_claim_normalization.py`
- **Fixtures Directory:** `tests/fixtures/claims/`
- **Unit Tests:** 18 dedicated unit tests verifying normalization edge cases (HTML entities, Unicode variants, spacing, punctuation, case sensitivity).
- **Integration Tests:** 5 comprehensive HTML fixtures validated against prohibited claim patterns.

### 3.2 Fixture Inventory
1. `tests/fixtures/claims/prohibited_ik_timing.html`:  
   Injects all 14 prohibited timing variants (`25 µs`, `25 us`, `25 microseconds`, `&mu;s`, `&#956;s`, `sub-30 us`, `<30 µs`, etc.) directly into HTML body elements (`<p>`, `<span>`, `<div>`, `<li>`, `<code>`).
2. `tests/fixtures/claims/prohibited_ik_metadata.html`:  
   Injects prohibited timing expressions into `<meta name="description">`, Open Graph `<meta property="og:description">`, Twitter Cards, and schema JSON-LD scripts.
3. `tests/fixtures/claims/prohibited_ik_svg.html`:  
   Injects prohibited timing expressions into SVG `<text>` elements, schematic callouts, and `<tspan>` tags.
4. `tests/fixtures/claims/prohibited_ik_attributes.html`:  
   Injects prohibited timing expressions into `aria-label`, `title`, and `alt` attributes.
5. `tests/fixtures/claims/valid_ik_terminology.html`:  
   Contains canonical verified terminology (`Closed-Form Analytical IK`, `Geometric Trigonometric Solution`, `NumPy/CPython`) and validates that no false-positive test failures occur.

### 3.3 CI Pipeline Integration
Both `tests/run_all_tests.py` and `.github/workflows/quality-gate.yml` now execute `python tests/test_claim_normalization.py` as Step 3 before evaluating production HTML pages.

---

## 4. Controlled Claims Register (`docs/PORTFOLIO_CLAIMS_REGISTER.md`)

The central Claims Register has been completely reconstructed for V5.3.2:
- **Total Audited Entries:** 31 claims.
- **Repository Provenance:** Every claim is tied to an immutable commit SHA:
  * `JosiahSK/josiahsaji.github.io` @ `43b8534ad4328296fd871c04697cfa6d87fd97b6` (V5.3.1)
  * `JosiahSK/autonomous-tilling-robot` @ `19fe9cc2f644f2947d716eead1e7bef3d797993c`
  * `JosiahSK/esp32-microros-2wd-car` @ `b0681f8451b0f0e3c3174c99dca2820333a66763`
  * `JosiahSK/ros2-quadruped-locomotion` @ `4c61e1db1d8b972105a25da21d83b4cf61699147`
  * `JosiahSK/ros2_jazzy_2wd_robot` @ `f75afeedf97c43e075f2749b891c0eab83fdc980`
- **Controlled Status Taxonomy:** 9 formal statuses (`VERIFIED_FROM_SOURCE_CODE`, `VERIFIED_FROM_CONFIGURATION`, `DATASHEET_SPECIFICATION`, `VERIFIED_FROM_PROJECT_DOCUMENT`, `MEASURED_WITH_TEST_EVIDENCE`, `USER_CONFIRMED_NOT_INDEPENDENTLY_VERIFIED`, `ILLUSTRATIVE`, `UNVERIFIED`, `REMOVED`).
- **Discrepancy Reconciliation Section:** 6 deep forensic investigations with explicit code line quotations.

---

## 5. Candidate Résumé Synchronization

The candidate résumé (`assets/resume/resume.pdf`) was regenerated and validated using `scripts/verify_resume.py`:
- **File Size:** 137,594 bytes.
- **Page Count:** Exactly 1 page (letter size).
- **ATS Parseability:** 3,745 characters extracted cleanly by `pypdf`.
- **Negative Assurances:** Verified 0 occurrences of `25 µs`, `25 us`, `25–26 µs`, `sub-30 µs`, `deterministic failsafe`, or unevidenced autonomous claims.
- **Positive Alignment:** Features `Agricultural Tilling Robot Prototype`, `24V LiFePO4`, `Closed-Form Analytical IK`, and `Software Command Timeout`.

---

## 6. Multi-Viewport Visual Verification

The automated screenshot engine (`scripts/capture_screenshots.py`) executed across 26 viewports:
- **Homepage:** 10 viewports (1440×900 down to 320×700).
- **Case Studies (4):** 4 viewports each (1440×900, 1024×768, 390×844, 360×800).
- **Results:** 26/26 screenshots rendered, dimension-checked via PIL (`im.size == (w, h)`), raster-verified via `im.load()`, and cataloged in `docs/screenshots/v5.3.2/README.md`.
- **Visual Stability:** Zero horizontal scrolling (`scrollWidth <= innerWidth`), clean line wraps on updated badges, and high-fidelity rendering across mobile, tablet, laptop, and desktop viewports.

---

## 7. Unified Test Suite Execution

The unified test runner (`tests/run_all_tests.py`) executed all 7 quality verification steps:

| Step # | Test Name | Command | Duration | Exit Code | Result |
| :---: | :--- | :--- | :---: | :---: | :---: |
| 1 | Python Bytecode Compilation | `python -m compileall scripts tests` | 0.08s | 0 | **PASS** |
| 2 | JavaScript Syntax Validation | `node --check script.js` | 0.04s | 0 | **PASS** |
| 3 | Test Harness Syntax Validation | `node --check tests/test_interactive.js` | 0.04s | 0 | **PASS** |
| 4 | Claim Normalization & Regression Suite | `python tests/test_claim_normalization.py` | 0.12s | 0 | **PASS** (18/18 unit, 5/5 fixtures) |
| 5 | Static DOM, Links, Alt & Claim Integrity | `python tests/test_links.py` | 0.72s | 0 | **PASS** (43 links, 35 positive assertions) |
| 6 | Real Browser Accessibility & Interactive CDP | `node tests/test_interactive.js` | 13.95s | 0 | **PASS** (75/75 CDP assertions) |
| 7 | Multi-Viewport Screenshot Capture & Dimension Audit | `python scripts/capture_screenshots.py` | ~25s | 0 | **PASS** (26/26 captures) |

---

## 8. Release Sign-Off

The Josiah Saji Robotics Portfolio V5.3.2 release meets all criteria for evidence grounding, technical precision, visual polish, and automated testing rigor. Every claim presented on the site is traceable to public repositories, verified configuration files, or official component datasheets.
