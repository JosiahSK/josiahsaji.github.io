# PORTFOLIO V5.3.3 FINAL TECHNICAL EVIDENCE CORRECTION AUDIT REPORT
## Hardware Truth · Source Accuracy · Claim Traceability · Safety Terminology · Release Integrity

**Repository:** `JosiahSK/josiahsaji.github.io`
**Production Baseline Commit:** `5dcede2d5f630cf26211a36d494d61b8d8c49a1f`
**Target Release:** Portfolio V5.3.3
**Audit Date:** 2026-10-30
**Status:** ALL REQUIRED GATES PASSED — PRODUCTION READY

---

## 1. Executive Purpose & Governance Principles

Portfolio V5.3.3 is a strict, evidence-driven precision release dedicated to reconciling technical statements with the actual contents of inspected robotics repositories, configuration files, and project test logs.

### Non-Negotiable Governance Rules Applied:
1. **Never Invent Evidence:** If hardware, tests, records, documents, or measurements do not exist in the inspected source code or project documentation, they are never fabricated.
2. **Qualify or Purge Unsupported Claims:** When evidence does not substantiate a specific quantitative or architectural claim, the statement is either strictly qualified or removed entirely.
3. **Preserve Verified Engineering Achievements:** Valid achievements (e.g., closed-form analytical quadruped IK, micro-ROS UDP architecture, 2WD differential drive SLAM navigation, custom welded tilling chassis fabrication, and 2-stroke engine integration) are preserved with exact technical grounding.
4. **Distinguish Project Records from Independent Certification:** Subsystem testing tables in `docs/testing.md` are documented as project-maintained prototype records, not independently certified laboratory experiments.
5. **Enforce Hard CI Gating:** Setup steps in continuous integration workflows must not use `continue-on-error: true`. Failures must block the quality gate.

---

## 2. Forensic Evidence Discrepancy & Remediation Matrix

| ID | Component / Area | Defective Statement / Assumption | Ground-Truth Evidence Discovered | Remediated Production Grounding | Authoritative Source File & Line |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CORR-01** | **Tilling Battery Voltage** | "24V nominal (~8S configuration)" | `docs/testing.md:12` records `LiFePO4 under load \| PASS - stable at 23.8V`. `README.md:37` specifies `24V LiFePO4 battery`. The specific cell count (e.g., 8S) or nominal stack topology is not documented. | **24V-Class LiFePO4 Battery System**<br>Project test documentation records a 23.8V reading under operational load. Cell configuration is not inferred. | `autonomous-tilling-robot`<br>`README.md:37`<br>`docs/testing.md:12` |
| **CORR-02** | **Tilling Drivetrain & Motor Count** | BOM Qty: 2 motors; "24V DC Geared Motors"; "differential drive torque profiles" | `README.md:42-43` specifies `Rear-wheel drive (24V DC motor)` and `Chain transmission`. `docs/system_architecture.md:39` specifies `Drive motor \| L298N` (singular) and `Steering \| Servo`. `docs/testing.md:20` logs forward driving at 0.3 m/s. | **Single 24V DC Motor & Chain Drive**<br>BOM Qty: 1. Rear-wheel chain drive transmission with front steering axle. Differential drive references removed. | `autonomous-tilling-robot`<br>`README.md:42-43`<br>`docs/system_architecture.md:39` |
| **CORR-03** | **Remote Control Subsystem** | "2.4 GHz Manual Remote Override", "2.4 GHz RF / Bluetooth Transceiver", "teleop failsafe signal-loss cutoff" | `docs/throttle_control.md:8` documents `Manual override lever for emergency takeover` on the throttle rack. No 2.4 GHz RF/Bluetooth receiver is documented or installed in the repository. | **Emergency Manual Override Lever**<br>Mechanical throttle takeover lever providing immediate manual engine control. 2.4 GHz RF claims purged from BOM, diagrams, and badges. | `autonomous-tilling-robot`<br>`docs/throttle_control.md:8` |
| **CORR-04** | **GPS Source Classification & Drift Correlation** | Cited nonexistent file `src/gps/gps_reader.py`; claimed ~3 m drift measured during 0.3 m/s crawl | No `src/` directory exists. `docs/gps_localization.md:16-40` contains a ROS 2 node code sample and architecture specification. In `docs/testing.md`, Line 20 (`Forward driving: stable at 0.3 m/s`) and Line 22 (`GPS logging: approx 3 m drift observed`) are separate tests. | **GPS NMEA Data Acquisition Node Architecture**<br>Documented architecture and code sample (`docs/gps_localization.md:16-40`). Forward driving (0.3 m/s) and GPS drift (~3 m) reported as separate documented test notes. | `autonomous-tilling-robot`<br>`docs/gps_localization.md:16-40`<br>`docs/testing.md:20, 22` |
| **CORR-05** | **Furrow Depth Claim** | "Design Target: ~15cm Furrow Depth" / "15 cm Furrow Depth" | `docs/testing.md:24` records `Tilling blade \| Done \| Effective on soft soil`. No dimensioned drawings, calculations, or field measurement logs document a 15 cm target. | **Tilling Blade Soft Soil Evaluation**<br>Documented as tested effective on soft soil (`docs/testing.md:24`). Numerical 15 cm furrow depth claim purged from public marketing copy. | `autonomous-tilling-robot`<br>`docs/testing.md:24` |
| **CORR-06** | **YIP 7.0 Submission Status** | Cited `README.md:1` as proof of institutional verification | `README.md:1-3, 110-111` lists project title and author affiliation (Robotics Society — Saintgits College). Project was developed by author as a submission to YIP 7.0, but no institutional certificate or receipt PDF is hosted in the git repository. | **USER_CONFIRMED_NOT_INDEPENDENTLY_VERIFIED**<br>Classified as author project submission without implying selection, finalist status, or awards. | `autonomous-tilling-robot`<br>`README.md:1-3, 110-111` |
| **CORR-07** | **ESP32 Timeout Terminology** | "Deterministic software command-timeout failsafes", "asynchronous timer constantly monitors packet freshness", "deadline timer" | In `esp32_microros_2wd.ino:144-150`, `loop()` calls `rclc_executor_spin_some()` then checks `millis() - lastCmdTime > CMD_TIMEOUT_MS -> stopMotors()`. This is an application-level sequential check in the Arduino main loop, not an asynchronous hardware timer. | **Application-Level Software Command Timeout Check**<br>When command age exceeds 500 ms in the main loop, firmware calls `stopMotors()` to command zero PWM duty cycle on all 4 motor pins. | `esp32-microros-2wd-car`<br>`firmware/.../esp32_microros_2wd.ino:144-150` |
| **CORR-08** | **ESP32 Braking Semantics** | "provides active regenerative braking on 0V" | `stopMotors()` calls `pwmWrite(pin, 0)` on all 4 pins. H-bridge stopping physics (coasting vs dynamic brake) depend on the physical driver module (e.g. L298N high-Z coast vs DRV8833). Firmware commands zero PWM; it does not provide active regenerative braking. | **Zero PWM Commanded to Motor Pins**<br>Commanded stop sets both direction PWM channels to zero. Regenerative and dynamic braking claims purged. | `esp32-microros-2wd-car`<br>`firmware/.../esp32_microros_2wd.ino:68-70, 79-82` |
| **CORR-09** | **CI Setup Policy** | `.github/workflows/quality-gate.yml` contained `continue-on-error: true` on Python setup | Python setup failure silently allowed later steps to execute without valid Python runtime environment. | **Strict CI Quality Gate**<br>Removed `continue-on-error: true` and cleaned up unused pip cache key. Any setup failure now halts CI immediately. | `.github/workflows/quality-gate.yml:24-28` |

---

## 3. Discrepancy Reconciliation Analysis

### 3.1 Tilling Power Subsystem Ground Truth
The portfolio previously concluded that `docs/testing.md:12` (`LiFePO4 under load | PASS - stable at 23.8V`) established a "24V nominal (~8S) battery configuration". In LiFePO4 chemistry, an 8-cell series configuration has a nominal voltage of $8 \times 3.2\text{ V} = 25.6\text{ V}$ and a maximum charging threshold of $8 \times 3.65\text{ V} = 29.2\text{ V}$. An under-load terminal voltage of 23.8V is consistent with an operating 24V-class pack, but does not identify the specific cell count, BMS cutoff voltage, or capacity without manufacturer cell datasheets. The description has been reconciled to **24V-Class LiFePO4 Battery System**, accurately noting that project test documentation records 23.8V under operational load.

### 3.2 Propulsion Motor Count & Transmission
The project README explicitly states:
```text
Rear-wheel drive (24V DC motor)
Chain transmission
```
And `docs/system_architecture.md:39` specifies:
```text
Drive motor | L298N | Forward / backward / stop
```
Earlier portfolio copy listed "24V DC Geared Motors & Chain Drive" with a BOM quantity of 2, and referenced "differential drive torque profiles". In V5.3.3, the BOM quantity has been corrected to **1**, the description reconciled to **24V DC Motor & Chain Drive**, and differential-drive torque control references removed.

### 3.3 Emergency Throttle Override vs. 2.4 GHz RF
The claims register previously cited `docs/throttle_control.md:8` for a 2.4 GHz remote override. The actual source line states:
```text
- Manual override lever for emergency takeover
```
This specifies a mechanical lever on the engine throttle mechanism, not a wireless radio receiver. All references to 2.4 GHz RF transceivers, teleoperation links, and automatic RF signal-loss failsafes have been purged from BOM tables, SVG schematics, badges, and résumé, retaining the mechanical emergency override lever.

### 3.4 GPS Architecture vs. Executable Code
`JosiahSK/autonomous-tilling-robot` contains architectural documentation and code samples, but no executable Python files in a `src/` tree. `docs/gps_localization.md:16-40` describes a `GPSNode` parsing NMEA 0183 `$GPRMC` sentences. The portfolio now classifies this as a documented ROS 2 node architecture and NMEA coordinate acquisition rather than an executable source file. Furthermore, the field test records of forward driving (0.3 m/s on line 20) and GPS logging (~3 m drift on line 22) are maintained as separate documented test records rather than a combined simultaneous performance metric.

### 3.5 Furrow Depth Ground Truth
`docs/testing.md:24` records:
```text
Tilling blade | Done | Effective on soft soil
```
There are no engineering calculations, drawings, or measurement logs establishing a 15 cm depth. The unevidenced 15 cm numerical claim has been removed from all public copy, accurately highlighting the documented soft-soil tilling blade test.

### 3.6 ESP32 Firmware Execution Model
In `firmware/esp32_microros_2wd/esp32_microros_2wd.ino`:
```cpp
void loop() {
    rclc_executor_spin_some(&executor, RCL_MS_TO_NS(10));

    if (millis() - lastCmdTime > CMD_TIMEOUT_MS) {
        stopMotors();
    }
}
```
This timeout check executes sequentially within the single-threaded Arduino `loop()` following the micro-ROS executor spin. It is an application-level command-age check, not a hardware watchdog timer or asynchronous FreeRTOS software timer. `stopMotors()` calls `pwmWrite(pin, 0)` on all four channels. This sets the PWM duty cycle to zero; it does not constitute active regenerative braking. The portfolio now uses **500 ms Application-Level Software Command-Timeout Check** and **Zero PWM Commanded to Motor Pins**.

---

## 4. Candidate Résumé Synchronization

The candidate résumé (`assets/resume/resume.pdf`) was regenerated and audited using `scripts/verify_resume.py`:
- **File Size:** 137,651 bytes (134.4 KB).
- **Page Budget:** Exactly 1 page (single-page layout strictly maintained).
- **ATS Extractability:** 3,743 characters parsed cleanly by `pypdf`.
- **Negative Assurances (100% Clear):**
  * `watchdog` — CLEAR
  * `regenerative` — CLEAR
  * `e-brake` — CLEAR
  * `deterministic failsafe` — CLEAR
  * `2.4 ghz` — CLEAR
  * `~8s` / `8s configuration` — CLEAR
  * `15cm` / `15 cm` — CLEAR
  * `25–26 µs` / `sub-30 µs` / `<30 µs` — CLEAR
  * `selected for yip` — CLEAR
  * `100+ students` — CLEAR

---

## 5. Controlled Claims Register Audit (`docs/PORTFOLIO_CLAIMS_REGISTER.md`)

- **Total Audited Entries:** 34 entries.
- **Controlled Status Distribution:**
  * `VERIFIED_FROM_SOURCE_CODE`: 8
  * `VERIFIED_FROM_CONFIGURATION`: 6
  * `VERIFIED_FROM_PROJECT_DOCUMENT`: 7
  * `MEASURED_WITH_TEST_EVIDENCE`: 2
  * `DATASHEET_SPECIFICATION`: 4
  * `USER_CONFIRMED_NOT_INDEPENDENTLY_VERIFIED`: 1
  * `ILLUSTRATIVE`: 1
  * `UNVERIFIED`: 1
  * `REMOVED`: 4
- **Automated Consistency Validation:** Validated via regex table parser handling escaped pipes (`\|`), asserting 40-character commit hashes for verified code/config claims, and confirming zero occurrences of removed claims in public HTML.

---

## 6. Multi-Viewport Screenshot Suite (V5.3.3)

Automated capture and PIL dimension assertion completed across 26 viewports:
- **Matrix:** 10 homepage viewports (1440×900 down to 320×700) + 16 case study viewports (4 per page).
- **Validation:** 26/26 captures verified (`im.size == (w, h)` and `im.load()` bitmap decompression).
- **Catalog:** Full audit catalog committed to `docs/screenshots/v5.3.3/README.md`.

---

## 7. Unified Test Suite Execution

| Step # | Test Name | Command | Duration | Exit Code | Result |
| :---: | :--- | :--- | :---: | :---: | :---: |
| 1 | Python Bytecode Compilation | `python -m compileall scripts tests` | 0.15s | 0 | **PASS** |
| 2 | JavaScript Syntax Validation | `node --check script.js` | 0.08s | 0 | **PASS** |
| 3 | Test Harness Syntax Validation | `node --check tests/test_interactive.js` | 0.08s | 0 | **PASS** |
| 4 | Claim Normalization & Regression Suite | `python tests/test_claim_normalization.py` | 0.10s | 0 | **PASS** (18/18 unit, 5/5 fixtures) |
| 5 | Static DOM, Links, Alt & Claim Integrity | `python tests/test_links.py` | 1.12s | 0 | **PASS** (43 links, 36 positive assertions, 34 register claims) |
| 6 | Real Browser Accessibility & Interactive CDP | `node tests/test_interactive.js` | 9.85s | 0 | **PASS** (75/75 assertions) |
| 7 | Multi-Viewport Screenshot Capture & Dimension Audit | `python scripts/capture_screenshots.py` | ~25s | 0 | **PASS** (26/26 viewports) |

---

## 8. Final Release Decision

```text
PRODUCTION READY — ALL V5.3.3 REQUIRED GATES PASSED
```
Every public claim across the Josiah Saji Robotics Portfolio is now traceable to verified source code, documented project specifications, or official component datasheets, with all speculative, ungrounded, or misattributed statements permanently corrected.
