# PORTFOLIO TECHNICAL CLAIMS & HARDWARE SPECIFICATIONS REGISTER

**Version:** V5.3 (Production Baseline)  
**Author / Subject:** Josiah Saji — Robotics & Embedded Systems Engineer  
**Repository:** [https://github.com/JosiahSK/josiahsaji.github.io](https://github.com/JosiahSK/josiahsaji.github.io)  
**Audited Baseline Commit:** `6ae094ac656bfdef9d21b4c200658143ff88f45b`  
**Maintenance Policy:** Every technical metric, frequency, hardware rating, or performance claim presented across the public portfolio website, diagrams, and résumé must map directly to an entry in this register.

---

## 1. Classification & Status Taxonomy

- **VERIFIED FROM SOURCE CODE:** Derived directly from inspected operational Python, C++, or script source files in the robotics codebase.
- **VERIFIED FROM CONFIGURATION:** Explicitly parameterized in audited ROS 2 / firmware configuration files (`controllers.yaml`, `mapper_params_online_async.yaml`, etc.).
- **DATASHEET SPECIFICATION:** Sourced from authoritative manufacturer technical datasheets (Slamtec, Espressif, etc.).
- **ILLUSTRATIVE:** Conceptual diagram or UI visual representation explicitly marked as non-telemetry / non-as-built.
- **UNVERIFIED:** Claim inspected and determined to lack empirical test logs; strictly designated as unverified or removed from numerical claims.
- **REMOVED:** Historical claim permanently purged from public pages due to absence of rigorous experimental measurement.

---

## 2. Central Technical Claims Register Table

| Claim ID | Portfolio Statement | Page / Section | Source Evidence | Verification Method | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CLM-QUAD-01** | `100 Hz Locomotion Controller Loop` | `index.html` (Hero stats, Project card) & `quadruped-locomotion.html` (Telemetry & Architecture) | `locomotion_controller_node.py:38-40`: `self.dt = 0.01`, `self.create_timer(self.dt, self.control_loop)` | Static source inspection & timer callback trace | **VERIFIED FROM SOURCE CODE** |
| **CLM-QUAD-02** | `200 Hz ros2_control Controller Manager Update` | `quadruped-locomotion.html` (Arch diagram & Tech specs table) & `index.html` (Quadruped description) | `src/quadruped_description/config/controllers.yaml:1-3`: `controller_manager: ros__parameters: update_rate: 200` | Configuration inspection | **VERIFIED FROM CONFIGURATION** |
| **CLM-QUAD-03** | `100 Hz Joint State Publication Rate` | `quadruped-locomotion.html` (Tech specs table & Architecture diagram) | `src/quadruped_description/config/controllers.yaml:34`: `joint_trajectory_controller: ros__parameters: state_publish_rate: 100.0` | Configuration inspection | **VERIFIED FROM CONFIGURATION** |
| **CLM-QUAD-04** | `200 Hz Gazebo IMU Sensor Publication` | `quadruped-locomotion.html` (System architecture diagram & sensor specs) | `src/quadruped_description/urdf/quadruped.urdf.xacro`: IMU gazebo sensor plugin configured to 200 Hz | URDF / Xacro inspection | **VERIFIED FROM CONFIGURATION** |
| **CLM-QUAD-05** | `12-DOF Analytical Inverse Kinematics` (3-DOF per leg: Hip Roll, Thigh Pitch, Knee Pitch) | `index.html` & `quadruped-locomotion.html` (Kinematics derivation) | `quadruped_kinematics.py` & `leg.xacro`: 4 symmetric legs &times; 3 active revolute joints per leg | Mathematical derivation & URDF geometric verification | **VERIFIED FROM SOURCE CODE** |
| **CLM-QUAD-06** | `Sub-30 µs / 25–26 µs IK Execution Time across 100,000 targets` | Historically present in V5.1; removed in V5.2.1 | `JosiahSK/ros2-quadruped-locomotion`: Repository contains only `ik_test_node.py` (geometric verification on 2 poses), zero timing instrumentation | Automated regex regression check (`tests/test_links.py`) | **REMOVED** |
| **CLM-QUAD-07** | `Physics Engine: Gazebo Classic 11 (ODE physics, 1 ms time step)` | `quadruped-locomotion.html` (Tech specs table) | `src/quadruped_gazebo/worlds/flat_world.world`: `<max_step_size>0.001</max_step_size>` | World file configuration inspection | **VERIFIED FROM CONFIGURATION** |
| **CLM-QUAD-08** | `Gait Patterns: Trot, Walk, Crawl, Bound` | `quadruped-locomotion.html` (Gait generator section & interactive tabs) | `src/quadruped_gait/quadruped_gait/gait_generator.py`: Explicit gait phase matrix definitions | Source code inspection | **VERIFIED FROM SOURCE CODE** |
| **CLM-AMR-01** | `RPLIDAR A1 Physical Hardware Revision` | `ros2-mobile-robot.html` (Hardware specifications & callout) | Repository hardware manifests do not record the physical sensor revision mark | Explicitly qualified on website and résumé | **UNVERIFIED** |
| **CLM-AMR-02** | `RPLIDAR A1M8-R4 Datasheet Range: 0.15–6.0 m` | `ros2-mobile-robot.html` (Datasheet callout) | Slamtec A1M8 Datasheet v2.4 (LD108) Table 2-1: 0.15–6.0 m | Datasheet citation & URL verification | **DATASHEET SPECIFICATION** |
| **CLM-AMR-03** | `RPLIDAR A1M8-R5 Datasheet Range: 0.15–12.0 m on white targets` | `ros2-mobile-robot.html` (Datasheet callout) | Slamtec A1M8 Datasheet v2.4 (LD108) Table 2-1: 0.15–12.0 m (90% reflectance) | Datasheet citation & URL verification | **DATASHEET SPECIFICATION** |
| **CLM-AMR-04** | `SLAM Toolbox 8.0 m Range Limit` | `index.html` & `ros2-mobile-robot.html` | `mapper_params_online_async.yaml: max_laser_range: 8.0` | Sourced from config; explicitly described as software mapping parameter, not physical sensor limit | **VERIFIED FROM CONFIGURATION** |
| **CLM-AMR-05** | `SLAM Toolbox 50 Hz map → odom transform publish rate` | `ros2-mobile-robot.html` (Architecture diagram & specs table) | `mapper_params_online_async.yaml: transform_publish_period: 0.02` (1 / 0.02 s = 50 Hz) | Configuration inspection | **VERIFIED FROM CONFIGURATION** |
| **CLM-AMR-06** | `6–8 m In-Lab Usable Range Claim` | Audited in V4.2.1; removed | Absence of recorded repeatable range measurement logs under standardized lab conditions | Purged from HTML, résumé, and tests | **REMOVED** |
| **CLM-AMR-07** | `Mobile Robot Kinematic Geometry: r = 0.065 m, L = 0.22 m` | `ros2-mobile-robot.html` (Differential drive equations) | `src/diff_drive_description/urdf/robot.urdf.xacro` wheel separation and radius properties | URDF inspection & forward kinematic validation | **VERIFIED FROM CONFIGURATION** |
| **CLM-ESP-01** | `ESP32-WROOM-32 DevKit V1 (Xtensa dual-core @ 240 MHz)` | `esp32-microros-robot.html` (Specs table & hardware diagram) | Espressif ESP32-WROOM-32 Datasheet & platformio.ini board definition | Datasheet & PlatformIO configuration | **DATASHEET SPECIFICATION** |
| **CLM-ESP-02** | `LEDC Hardware PWM at 1 kHz, 8-bit resolution (0–255)` | `esp32-microros-robot.html` (PWM configuration) | `src/main.cpp`: `ledcSetup(0, 1000, 8)` | Firmware source code inspection | **VERIFIED FROM SOURCE CODE** |
| **CLM-ESP-03** | `4-Pin Motor Control: GPIO 25, 26, 27, 14` | `esp32-microros-robot.html` (Pinout callout & diagram) | `src/main.cpp`: `#define M1A 25`, `#define M1B 26`, `#define M2A 27`, `#define M2B 14` | Firmware source code inspection | **VERIFIED FROM SOURCE CODE** |
| **CLM-ESP-04** | `Local Failsafe Watchdog: 500 ms timeout` | `esp32-microros-robot.html` (Watchdog architecture) | `src/main.cpp`: `if (millis() - lastCmdTime > 500) stopMotors();` | Firmware source code inspection | **VERIFIED FROM SOURCE CODE** |
| **CLM-ESP-05** | `Sub-8ms Wireless Communication Latency` | Audited in V4.1; removed | No round-trip ping / XRCE-DDS latency benchmark script present in repository | Purged from HTML, résumé, and tests | **REMOVED** |
| **CLM-ESP-06** | `Power Subsystem: 2S Li-ion (7.4 V) + LM2596 Buck Converter (5.0 V)` | `esp32-microros-robot.html` (Power architecture) | Hardware wiring manifest & BOM: separate logic rail from motor power bus | Hardware manifest inspection | **VERIFIED FROM CONFIGURATION** |
| **CLM-TILL-01** | `Agricultural Tilling Robot: YIP 7.0 Submission` | `tilling-robot.html` (Hero badge & project overview) | Young Innovators Programme (YIP) 7.0 submission documentation | Institutional submission record | **VERIFIED** |
| **CLM-TILL-02** | `YIP 7.0 Official Selection / Award Claim` | Audited in V4.1; removed | Replaced with verified submission status; official final selection unconfirmed | Purged from HTML, résumé, and tests | **REMOVED** |
| **CLM-TILL-03** | `Power Subsystem: 12V LiFePO4 Battery Pack` | `tilling-robot.html` (Powertrain & BOM) | Project bill of materials & battery specification documentation | Hardware manifest inspection | **VERIFIED FROM CONFIGURATION** |
| **CLM-TILL-04** | `100+ Engineering Students Trained Claim` | Audited in V4.1; removed | Historical leadership description revised to documented Robotics Society workshop sessions | Purged from HTML, résumé, and tests | **REMOVED** |
| **CLM-UI-01** | `Interactive Robot Schematic (Hero SVG)` | `index.html` (Hero visual stage) | SVG elements with coordinate grid, range rings, and animated radar sweep; explicitly captioned as interactive schematic | DOM & visual inspection; non-live telemetry notice present | **ILLUSTRATIVE** |

---

## 3. Discrepancy & External Source Register

1. **Quadruped Public GitHub README Inconsistency:**  
   The external repository `JosiahSK/ros2-quadruped-locomotion` historical README references "100 Hz ros2_control" and "sub-10 µs analytical IK". The repository's actual configuration file (`controllers.yaml`) sets `controller_manager.update_rate: 200` and `state_publish_rate: 100.0`, while `locomotion_controller_node.py` runs a 100 Hz timer loop. Furthermore, the repository lacks any latency measurement benchmark code. The portfolio strictly decouples from the external README's imprecise phrasing, presenting the verified 200 Hz manager / 100 Hz timer distinction and deterministic closed-form mathematics without fabricated latency numbers.

2. **RPLIDAR Hardware Revision Tracking:**  
   The physical unit revision is not stamped in repository manifests. The portfolio therefore explicitly avoids claiming R5 capabilities (12 m) for the physical hardware, noting that A1M8-R4 is rated to 6.0 m while A1M8-R5 is rated to 12.0 m on white targets, with the software mapping stack bounding range to 8.0 m.
