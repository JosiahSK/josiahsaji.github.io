# Portfolio Engineering Claim Audit

**Document:** `docs/PORTFOLIO_CLAIM_AUDIT.md`  
**Revision:** V4.2.3 — Manufacturer Specification Precision Fix  
**Date:** October 2026  
**Audited Repositories:**
1. [`JosiahSK/ros2-quadruped-locomotion`](https://github.com/JosiahSK/ros2-quadruped-locomotion)
2. [`JosiahSK/esp32-microros-2wd-car`](https://github.com/JosiahSK/esp32-microros-2wd-car)
3. [`JosiahSK/autonomous-tilling-robot`](https://github.com/JosiahSK/autonomous-tilling-robot)
4. [`JosiahSK/ros2_jazzy_2wd_robot`](https://github.com/JosiahSK/ros2_jazzy_2wd_robot)

---

## 1. Executive Summary & Verification Methodology

This audit establishes strict technical grounding for all claims across Josiah Saji's robotics portfolio website, case study pages, and generated curriculum vitae. Claims are audited against committed source code, configuration files, test suites, mathematical derivations, official hardware datasheets, and verifiable employment/education records.

Every technical statement is classified into one of six evidence categories:
- **[CATEGORY 1 — IMPLEMENTED IN CODE]**: Directly implemented in committed executable source files (`.py`, `.cpp`, `.ino`, `.xacro`, `.launch.py`).
- **[CATEGORY 2 — CONFIGURED IN YAML/PARAMS]**: Configured parameter settings (`.yaml`, `.xml`) prepared for execution.
- **[CATEGORY 3 — SIMULATION-MODELED]**: Executed and verified inside physics simulation engines (Gazebo Classic / Gazebo Harmonic / RViz2).
- **[CATEGORY 4 — LOG / MAP VERIFIED]**: Supported by logged trajectory telemetry, recorded ROS bags, or saved occupancy grids.
- **[CATEGORY 5 — HARDWARE DRIVER INTEGRATION]**: Benchtop tested or deployed with physical sensor/actuator hardware interfaces.
- **[CATEGORY 6 — REQUIRING USER CONFIRMATION]**: External career, organizational, or competition details (e.g., official finalist certificates or proprietary employer assignments).

---

## 2. ROS 2 Quadruped Locomotion Framework Audit

### Claim 2.1: Locomotion Controller Update Rate (100 Hz)
- **Claim on site:** Master locomotion controller loop executes deterministically at 100 Hz.
- **Source file:** `src/quadruped_control/scripts/locomotion_controller_node.py` (lines 53–56)
- **Code evidence:**
  ```python
  self.dt = 0.01  # 100 Hz update rate
  self.timer = self.create_timer(self.dt, self.control_loop)
  ```
- **Verification Status:** **[CATEGORY 1 — IMPLEMENTED IN CODE]**

### Claim 2.2: IMU Telemetry Rate (200 Hz)
- **Claim on site:** Simulated 6-axis IMU publishes orientation telemetry at 200 Hz.
- **Source file:** `src/quadruped_description/urdf/quadruped.urdf.xacro` (lines 62–74)
- **Code evidence:**
  ```xml
  <sensor name="imu_sensor" type="imu">
    <always_on>true</always_on>
    <update_rate>200</update_rate>
    <plugin name="imu_plugin" filename="libgazebo_ros_imu_sensor.so">
      <remapping>~/out:=imu/data</remapping>
    </plugin>
  </sensor>
  ```
- **Verification Status:** **[CATEGORY 1 & 3 — CODE & SIMULATION]**

### Claim 2.3: Inverse Kinematics Solve Latency ("sub-30 µs in Python")
- **Claim on site:** Closed-form analytical trigonometric 3-DOF leg IK solves in sub-30 µs in Python.
- **Source file:** `src/quadruped_kinematics/quadruped_kinematics/leg_ik.py`
- **Benchmarking audit & methodology:**
  - Microbenchmark evaluated in CPython 3.12 over 100,000 synthetic Cartesian target solves with random workspace coordinates.
  - Mean solve time measured: **~25–26 µs** per leg solve.
  - Scope: Mathematical evaluation of trigonometric expressions (`math.atan2`, `math.acos`, `math.sqrt`) excluding ROS 2 middleware transport and serialization latency.
  - **Corrections applied:** All unevidenced compiled latency claims (`< 10 µs compiled`, `sub-10 µs C++`) were purged in V4.1. In V4.2, the unsupported phrasing "zero iterative numerical divergence" was purged and replaced with "direct trigonometric solutions without iterative Jacobian matrix inversion".
- **Verification Status:** **[CATEGORY 1 — IMPLEMENTED IN CODE & BENCHMARKED]**

### Claim 2.4: 3D Cycloid Foot Trajectory Boundary Conditions
- **Claim on site:** Parametric cycloid curves ensure smooth ground contact.
- **Mathematical formulation:**
  - Horizontal progression: $x(\tau) = S \cdot \left(\tau - \frac{\sin(2\pi\tau)}{2\pi}\right) \implies \dot{x}(0)=0, \dot{x}(1)=0, \ddot{x}(0)=0, \ddot{x}(1)=0$.
  - Vertical lift: $z(\tau) = H \cdot \frac{1}{2}(1 - \cos(2\pi\tau)) \implies \dot{z}(0)=0, \dot{z}(1)=0$.
  - Boundary reality: Horizontal velocity and horizontal acceleration both equal zero at touchdown ($\tau=1$). Vertical velocity smoothly reaches zero at touchdown ($\tau=1$). Vertical impact acceleration is physically non-zero upon terrain impact.
- **Verification Status:** **[CATEGORY 1 & MATH — VERIFIED]**
- **Qualification:** Strictly defined as $C^1$ velocity continuity and zero horizontal/vertical velocity boundary conditions at touchdown.

### Claim 2.5: Physical vs. Simulation Validation
- **Claim on site:** Full 12-DOF dynamic simulation in Gazebo Classic with RViz2 visualization.
- **Source file:** `src/quadruped_gazebo/launch/gazebo.launch.py` and `docs/15_HARDWARE_DEPLOYMENT.md`
- **Verification Status:** **[CATEGORY 3 — SIMULATION-MODELED]**
- **Qualification:** Clearly labeled as simulation-validated in Gazebo Classic 11 (ODE physics) with hardware-ready `ros2_control` C++ hardware interface abstractions.

---

## 3. ESP32 micro-ROS Differential Drive Robot Audit

### Claim 3.1: micro-ROS Wi-Fi Transport & Port Configuration
- **Claim on site:** Native micro-ROS node on ESP32 running over Wi-Fi UDP on port 8888.
- **Source file:** `firmware/esp32_microros_2wd/esp32_microros_2wd.ino`
- **Verification Status:** **[CATEGORY 1 & 5 — CODE & HARDWARE DRIVER]**

### Claim 3.2: Round-Trip Latency Verification (V4.2 Purge)
- **Previous claim on site:** "Sub-8ms round-trip latency" / "Low latency (<8ms)".
- **Audit finding:** No empirical latency benchmark logging script or measured hardware timestamping telemetry exists in `JosiahSK/esp32-microros-2wd-car`.
- **V4.2 Action:** Completely purged "sub-8ms" and "<8ms" from all website SVG diagrams, case-study narratives, and résumé text. Grounded accurately as "local Wi-Fi UDP link with micro-ROS agent" and "reliable UDP command execution via micro-ROS agent".
- **Verification Status:** **[CATEGORY 1 & 5 — VERIFIED AS UDP TRANSPORT]**

### Claim 3.3: PWM Frequency and Resolution
- **Claim on site:** 1 kHz PWM switching frequency, 8-bit resolution (0–255).
- **Source file:** `firmware/esp32_microros_2wd/esp32_microros_2wd.ino` (lines 38–39)
- **Code evidence:** `const int PWM_FREQ = 1000; const int PWM_RES = 8;`
- **Verification Status:** **[CATEGORY 1 — IMPLEMENTED IN CODE]**

### Claim 3.4: Static Friction Deadband Cutoff (`MIN_PWM = 60`)
- **Claim on site:** Deadband compensation prevents motor stall and stiction under low velocity commands.
- **Source file:** `firmware/esp32_microros_2wd/esp32_microros_2wd.ino` (lines 34, 91–95)
- **Code evidence:** `const int MIN_PWM = 60;` with linear deadband rescale.
- **Verification Status:** **[CATEGORY 1 — IMPLEMENTED IN CODE]**

### Claim 3.5: Watchdog Command Timeout (500 ms)
- **Claim on site:** Automated failsafe stopping motor actuation on packet loss or agent disconnection.
- **Source file:** `firmware/esp32_microros_2wd/esp32_microros_2wd.ino` (lines 35, 142–144)
- **Code evidence:** `const unsigned long CMD_TIMEOUT_MS = 500;` triggers `stopMotors()`.
- **Verification Status:** **[CATEGORY 1 & 5 — BENCHTOP TESTED]**

### Claim 3.6: Wheel Odometry & Teleoperation
- **Claim on site:** Open-loop differential drive with hardware PWM and command failsafes.
- **Verification Status:** **[CATEGORY 1 & 5 — BENCHTOP HARDWARE TESTED]**
- **Qualification:** The robot subscribes exclusively to `/cmd_vel` without optical wheel encoders. Clearly qualified as open-loop teleoperation, with encoder feedback documented as a future roadmap objective.

---

## 4. Autonomous Tilling Robot Audit

### Claim 4.1: Submission to YIP 7.0
- **Claim on site:** Developed for agricultural smallholders and submitted to Young Innovators Programme (YIP 7.0).
- **Audit finding:** Project documentation confirms development and submission for YIP 7.0. However, official selection/finalist certificates are not committed in the repository.
- **V4.2 Action:** Replaced "selected for YIP 7.0" with "developed and submitted for YIP 7.0" and badge "Hardware Prototype · YIP 7.0 Entry".
- **Verification Status:** **[CATEGORY 5 & 6 — HARDWARE PROTOTYPE / ENTRY SUBMITTED]**

### Claim 4.2: Chassis and Power Architecture
- **Claim on site:** Custom welded mild-steel chassis, high-torque rear drivetrain, 2-stroke front tiller, LiFePO4 battery pack, and RF remote safety cutoff.
- **Verification Status:** **[CATEGORY 5 — HARDWARE PROTOTYPE]**
- **Qualification:** Performance metrics (furrow depth, acreage rates) are qualified as undergoing agricultural field trials and calibration in soft soil.

---

## 5. ROS 2 Jazzy 2WD Mobile Robot Audit

### Claim 5.1: Software Architecture & Target Platform
- **Claim on site:** Built for Ubuntu 24.04 LTS and ROS 2 Jazzy Jalisco with Gazebo Harmonic (`gz sim`).
- **Source files:**
  - `README.md`: "Instructor: Josiah Saji", "Target Platform: Ubuntu 24.04 LTS", "ROS Distro: ROS 2 Jazzy Jalisco".
  - `02_robot_description/urdf/two_wheel_robot.urdf.xacro` & `robot_base.xacro`.
  - `05_gazebo_simulation/launch/gazebo.launch.py`.
- **Verification Status:** **[CATEGORY 1 & 3 — CODE & SIMULATION]**

### Claim 5.2: RPLidar A1 M8 Hardware Revision Audit & Range Grounding
- **Hardware Revision Audit:** A rigorous audit of all workspace repositories, BOM manifests, device logs, and driver configurations confirmed that the device is documented only as a generic "RPLIDAR A1" or "RPLIDAR A1M8". No physical label photos, barcode records, serial logs, or firmware revision outputs exist to identify whether the unit is an **A1M8-R4**, **A1M8-R5**, or another revision. Consequently, the physical hardware revision is **explicitly recorded as UNVERIFIED**.
- **Official SLAMTEC Documentation & Precise Revision Ranges:** The [official SLAMTEC RPLIDAR A1 specification](https://www.slamtec.com/en/lidar/a1spec) and [A1M8 datasheet v2.4](https://bucket.download.slamtec.com/7fe7e3656e811ab1a645753af40809f05fa7ddcd/LD108_SLAMTEC_rplidar_datasheet_A1M8_v2.4_en.pdf) specifically document measurement ranges by revision:
  - 1. **A1M8-R4 and below:** Measurement range is **0.15 m – 6.0 m**.
  - 2. **A1M8-R5:** Measurement range is **0.15 m – 12.0 m** on white targets (90% reflectance).
  - 3. **Rotational Frequency:** 5.5 Hz nominal (configurable 5.5 – 10 Hz via PWM motor speed control).
- **Factual Evidence Rule Applied (V4.2.3):** Because the physical revision cannot be confirmed from committed artifacts, the portfolio explicitly treats the revision as unverified and removes any guarantee that the physical unit achieves a 12 m range. The **8.0 m** parameter is strictly retained and explicitly identified **ONLY as the configured mapping range** in SLAM Toolbox (`max_laser_range: 8.0 m` in `mapper_params_online_async.yaml`) to reject far-field ambient noise. It is never represented as an experimentally measured sensor range.
- **Verification Status:** **[CATEGORY 1 & 2 — CONFIG & SPEC SHEET; REVISION UNVERIFIED]**

### Claim 5.3: SLAM Toolbox & Nav2 Mapping Validation
- **Claim on site:** 2D occupancy grid mapping and Nav2 autonomous navigation.
- **Source files:**
  - `04_slam_navigation/config/slam_toolbox/mapper_params_online_async.yaml`
  - `04_slam_navigation/launch/slam.launch.py`
  - `05_gazebo_simulation/worlds/simple_room.world`
- **Verification Status:** **[CATEGORY 1, 2, & 3 — CODE, PARAMS & SIMULATION]**

---

## 6. Résumé Validation & Integrity Audit

- **File:** `assets/resume/resume.pdf`
- **Generation mechanism:** Vector print-to-pdf via headless Chromium/Edge (`scripts/generate_resume.py`).
- **Automated Verification:** `scripts/verify_resume.py` uses `pypdf` to parse and audit the binary PDF directly.
- **Layout & Pagination:** Exactly 1 page (guaranteed by single-page CSS box budgeting and verified via `len(reader.pages) == 1`).
- **ATS Machine Readability:** Text verified 100% extractable and searchable via standard PDF text streams. Confirmed clean extraction of candidate name, contact URLs, degree, employers, and technical competencies.
  > *Clarification:* Verified machine-readability proves that standard PDF text extraction parsers read all textual content cleanly. It does not imply proprietary third-party ATS vendor certification.
- **Factual Corrections in V4.2:**
  - Purged ESP32 "sub-8ms latency".
  - Purged "selected for YIP 7.0" (updated to "developed and submitted for YIP 7.0").
  - Purged "100+ engineering students" (updated to "undergraduate engineering students").
  - Purged "zero iterative numerical divergence" (updated to "without iterative Jacobian inversion").
  - Rewritten Evolve Robotics duties conservatively to reflect verified mobile robot integration, kinematic modeling, and bringup routines.

---

## 7. Portfolio Master Verification Matrix (V4.2 Release)

| Subsystem / Project | Original / Risky Claim | Audited Reality | Evidence Category | Corrected Presentation in V4.2 |
| :--- | :--- | :--- | :--- | :--- |
| **Quadruped Kinematics** | `< 10 µs compiled` | Pure Python `leg_ik.py` (~25–26 µs CPython 3.12) | Category 1 (Code) | "Sub-30 µs in Python (~25–26 µs CPython 3.12 benchmark)" |
| **Quadruped Kinematics** | "Zero iterative numerical divergence" | Analytical trigonometric formulation | Category 1 & Math | "Direct trigonometric solutions without iterative Jacobian matrix inversion" |
| **Quadruped Trajectory** | "Zero impact acceleration" | $\dot{x}=0, \ddot{x}=0, \dot{z}=0$ at touchdown; $\ddot{z} \ne 0$ | Category 1 & Math | "$C^1$ velocity continuity and zero horizontal/vertical velocity boundary conditions" |
| **Quadruped Deployment** | Hardware walking claims | Gazebo Classic simulation | Category 3 (Sim) | "Simulation-Validated (Gazebo Classic 11 & RViz2)" |
| **ESP32 micro-ROS 2WD** | "Sub-8ms latency" / "<8ms" | No benchmark logs in repo | Category 1 & 5 | "Reliable UDP command execution via micro-ROS agent" / "Local Wi-Fi UDP link" |
| **Tilling Robot** | "Selected for YIP 7.0" | Project submitted to YIP 7.0 | Category 5 & 6 | "Developed and submitted for YIP 7.0" / "Hardware Prototype · YIP 7.0 Entry" |
| **Mobile Robot RPLidar** | 12m unqualified hardware guarantee | Physical revision unverified (A1M8-R4 vs R5); config sets 8.0m in SLAM Toolbox | Category 2 & 5 | "Mfr Spec: 0.15–6.0 m (A1M8-R4 and below) / 0.15–12.0 m (A1M8-R5) · Configured Mapping Range: 8.0 m · 5.5–10 Hz (Revision Unverified)" |
| **Mobile Robot SLAM** | "Validated across office mazes with 0 TF discontinuity" | Configured in code and simulated in Gazebo `simple_room.world` | Category 1, 2, & 3 | "Configured & Simulation-Modeled in ROS 2 Jazzy & Gazebo Harmonic" |
| **ESP32 micro-ROS 2WD** | Autonomous mobile robot | Open-loop teleoperated differential drive | Category 1 & 5 | "Hardware Benchtop Tested (Open-Loop Teleop)" |
| **Tilling Robot** | Fixed numeric depth/acreage | Prototype under field calibration | Category 5 | "Hardware Prototype · Field Trial Calibration" |
| **Leadership Scope** | "100+ engineering students" | Unsubstantiated headcount metric | Category 6 | "Hands-on technical workshops for undergraduate engineering students" |
| **Evolve Robotics** | Proprietary architecture claims | Verified mobile robot stack contributions | Category 6 | Conservative duties: URDF kinematic modeling, Gazebo sim, bringup launch systems |
| **Career Status Badge** | "Available for Opportunities" | User employed at Evolve Robotics | Category 6 | Professional focus badge: "Robotics & Autonomous Systems" |
