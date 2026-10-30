import os
import subprocess
import tempfile

def generate_resume_pdf():
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Josiah Saji — Robotics Engineer Resume</title>
<style>
  @page {
    size: letter;
    margin: 0.45in 0.5in 0.45in 0.5in;
  }
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }
  body {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    color: #1e293b;
    background: #ffffff;
    font-size: 9.5pt;
    line-height: 1.35;
  }
  .header {
    border-bottom: 2px solid #0f172a;
    padding-bottom: 8px;
    margin-bottom: 10px;
  }
  .name {
    font-size: 20pt;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #0f172a;
    text-transform: uppercase;
  }
  .role-title {
    font-size: 10.5pt;
    font-weight: 700;
    color: #0284c7;
    margin-top: 1px;
    margin-bottom: 4px;
  }
  .contact-bar {
    font-size: 8.5pt;
    color: #475569;
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
  }
  .contact-bar a {
    color: #0284c7;
    text-decoration: none;
  }
  .section {
    margin-bottom: 10px;
  }
  .section-title {
    font-size: 10pt;
    font-weight: 800;
    color: #0f172a;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    border-bottom: 1px solid #cbd5e1;
    padding-bottom: 2px;
    margin-bottom: 6px;
  }
  .item {
    margin-bottom: 6px;
  }
  .item:last-child {
    margin-bottom: 0;
  }
  .item-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
  }
  .item-title {
    font-weight: 700;
    font-size: 9.5pt;
    color: #0f172a;
  }
  .item-subtitle {
    font-weight: 600;
    font-size: 9pt;
    color: #475569;
  }
  .item-date {
    font-size: 8.5pt;
    font-weight: 600;
    color: #64748b;
  }
  ul {
    list-style-type: disc;
    margin-left: 16px;
    margin-top: 2px;
  }
  li {
    font-size: 8.8pt;
    color: #334155;
    margin-bottom: 2px;
    line-height: 1.3;
  }
  li strong {
    color: #0f172a;
  }
  .skills-grid {
    display: grid;
    grid-template-columns: 140px 1fr;
    row-gap: 3px;
    font-size: 8.8pt;
  }
  .skills-cat {
    font-weight: 700;
    color: #0f172a;
  }
  .skills-list {
    color: #334155;
  }
</style>
</head>
<body>

<div class="header">
  <div class="name">Josiah Saji</div>
  <div class="role-title">Robotics &amp; ROS 2 Engineer</div>
  <div class="contact-bar">
    <span>📍 Kerala, India</span>
    <span>✉️ <a href="mailto:josiahsaji2k03@gmail.com">josiahsaji2k03@gmail.com</a></span>
    <span>🌐 <a href="https://josiahsk.github.io/josiahsaji.github.io/">josiahsk.github.io</a></span>
    <span>💼 <a href="https://linkedin.com/in/josiah-saji-aa5080232/">linkedin.com/in/josiah-saji</a></span>
    <span>🐙 <a href="https://github.com/JosiahSK">github.com/JosiahSK</a></span>
  </div>
</div>

<div class="section">
  <div class="section-title">Professional Summary</div>
  <p style="font-size: 8.8pt; color: #334155; line-height: 1.35;">
    Robotics Engineer specializing in ROS 2 (Jazzy/Humble), autonomous mobile robots (SLAM, Nav2), embedded firmware (ESP32, FreeRTOS, micro-ROS), and multi-DOF robot kinematics. Proven track record transitioning autonomous systems from mathematical formulation and dynamic simulation (Gazebo, RViz2) to real hardware prototypes.
  </p>
</div>

<div class="section">
  <div class="section-title">Work Experience</div>
  <div class="item">
    <div class="item-header">
      <span class="item-title">Robotics Engineer</span>
      <span class="item-date">Jan 2026 – Present</span>
    </div>
    <div class="item-subtitle">Evolve Robotics · Kerala, India</div>
    <ul>
      <li>Contributing to ROS 2 mobile robot software integration, URDF/Xacro kinematic modeling, and system bringup launch systems.</li>
      <li>Configuring autonomous navigation pipelines, sensor parameters, and Gazebo simulation environments.</li>
      <li>Developing microcontroller firmware and hardware-in-the-loop test routines for mobile robotics platforms.</li>
    </ul>
  </div>
  <div class="item" style="margin-top: 5px;">
    <div class="item-header">
      <span class="item-title">Secretary — Robotics Society</span>
      <span class="item-date">2024 – 2025</span>
    </div>
    <div class="item-subtitle">Saintgits College of Engineering · Kottayam, Kerala</div>
    <ul>
      <li>Organized and facilitated hands-on technical workshops in ROS 2, micro-ROS, and microcontroller programming for undergraduate engineering students.</li>
      <li>Coordinated hardware procurement, prototyping components, and student technical mentorship.</li>
    </ul>
  </div>
</div>

<div class="section">
  <div class="section-title">Key Engineering Projects</div>

  <div class="item">
    <div class="item-header">
      <span class="item-title">ROS 2 Quadruped Locomotion Framework</span>
      <span class="item-date">ROS 2 Humble · C++ / Python · Gazebo</span>
    </div>
    <ul>
      <li>Formulated closed-form analytical 3-DOF leg inverse kinematics providing direct trigonometric solutions without iterative Jacobian inversion.</li>
      <li>Implemented parametric 3D cycloid foot trajectory generator guaranteeing <strong>C¹ velocity continuity</strong> and zero horizontal/vertical velocity boundary conditions at touchdown.</li>
      <li>Validated multi-gait sequencing (Trot, Walk, Crawl, Bound) and IMU active roll/pitch balance loop at 100 Hz in Gazebo.</li>
    </ul>
  </div>

  <div class="item">
    <div class="item-header">
      <span class="item-title">Agricultural Tilling Robot Prototype (AgriTech)</span>
      <span class="item-date">ROS 2 Humble · Raspberry Pi 4B · ESP32 · 24V-Class LiFePO4</span>
    </div>
    <ul>
      <li>Architected hybrid 24V agricultural rover with front 2-stroke engine and rear chain drivetrain; developed for <strong>YIP 7.0</strong>.</li>
      <li>Integrated GPS data acquisition node (NEO-6M), multi-sensor telemetry, and emergency manual throttle override mechanism.</li>
      <li>Engineered custom mild-steel chassis and 24V-class LiFePO4 battery power architecture for high-vibration agricultural environments.</li>
    </ul>
  </div>

  <div class="item">
    <div class="item-header">
      <span class="item-title">ROS 2 Jazzy 2WD Differential Drive Robot</span>
      <span class="item-date">ROS 2 Jazzy · Ubuntu 24.04 · Gazebo Harmonic · Nav2</span>
    </div>
    <ul>
      <li>Developed modular navigation framework for 2WD + dual-castor chassis with RPLidar A1 M8 (360° FOV, 8m configured mapping range, 5.5–10 Hz).</li>
      <li>Configured SLAM Toolbox 2D occupancy mapping, Nav2 dynamic costmaps, and global/local path planning in Gazebo Harmonic.</li>
      <li>Authored multi-module curriculum covering URDF/Xacro, TF2 trees, RViz2, and automated bash installation.</li>
    </ul>
  </div>

  <div class="item">
    <div class="item-header">
      <span class="item-title">ESP32 micro-ROS 2WD Differential Drive</span>
      <span class="item-date">ESP32 · FreeRTOS · micro-ROS (UDP) · C++</span>
    </div>
    <ul>
      <li>Built native micro-ROS node on ESP32 executing command subscriptions over Wi-Fi UDP with micro-ROS agent.</li>
      <li>Implemented 4-pin pure PWM motor driver with static friction deadband cutoff (MIN_PWM = 60) and 1 kHz LEDC switching.</li>
      <li>Integrated 500 ms software command-timeout cutoff setting motor PWM to zero on Wi-Fi packet drop or agent disconnection; benchtop tested.</li>
    </ul>
  </div>
</div>

<div class="section">
  <div class="section-title">Technical Skills</div>
  <div class="skills-grid">
    <div class="skills-cat">Robotics &amp; Autonomy:</div>
    <div class="skills-list">ROS 2 (Jazzy, Humble), micro-ROS, Nav2, SLAM Toolbox, MoveIt 2, ros2_control, TF2</div>

    <div class="skills-cat">Simulation &amp; CAD:</div>
    <div class="skills-list">Gazebo (Harmonic, Classic 11), RViz2, URDF, Xacro, 3D Prototyping (STL/CAD)</div>

    <div class="skills-cat">Embedded &amp; Hardware:</div>
    <div class="skills-list">ESP32, Raspberry Pi, FreeRTOS, RPLidar A1, MPU6050/BNO055 IMU, LiFePO4 BMS, PWM/UART/I2C/SPI</div>

    <div class="skills-cat">Languages &amp; Tools:</div>
    <div class="skills-list">C++, Python, Embedded C, Linux (Ubuntu 24.04/22.04 LTS), Git, Bash, CMake</div>
  </div>
</div>

<div class="section">
  <div class="section-title">Education</div>
  <div class="item">
    <div class="item-header">
      <span class="item-title">Bachelor of Technology (B.Tech) in Robotics &amp; Automation</span>
      <span class="item-date">2021 – 2025</span>
    </div>
    <div class="item-subtitle">Saintgits College of Engineering · APJ Abdul Kalam Technological University, Kerala</div>
  </div>
</div>

</body>
</html>
"""
    temp_dir = tempfile.gettempdir()
    html_path = os.path.join(temp_dir, "josiah_saji_resume.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    pdf_out = r"D:\Documents\Antigravity_project\Interactive_Website\josiahsaji.github.io\assets\resume\resume.pdf"
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

    cmd = [
        edge_path,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        f"--user-data-dir={os.path.join(temp_dir, 'edge_pdf_profile')}",
        f"--print-to-pdf={pdf_out}",
        "--no-pdf-header-footer",
        f"file:///{html_path.replace(os.sep, '/')}"
    ]

    print("Running Edge print-to-pdf...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(f"Edge exited with code: {res.returncode}")
    if os.path.exists(pdf_out):
        print(f"SUCCESS: Generated {pdf_out} (size: {os.path.getsize(pdf_out)} bytes)")
    else:
        print("ERROR: PDF was not generated.")

if __name__ == "__main__":
    generate_resume_pdf()
