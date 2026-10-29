# Portfolio V4 Engineering Master Plan: World-Class Robotics Portfolio

**Document:** `docs/PORTFOLIO_V4_PLAN.md`  
**Author:** Lead Engineering & Design Architect  
**Date:** October 2026  
**Target Repository:** `D:\Documents\Antigravity_project\Interactive_Website\josiahsaji.github.io`  
**Production Site:** `https://josiahsk.github.io/josiahsaji.github.io/`  
**GitHub Profile:** `https://github.com/JosiahSK`  

---

## 1. Executive Vision & Objectives

Transform Josiah Saji's robotics portfolio from a promising project showcase into a **tier-one, production-grade engineering portfolio** calibrated for technical recruiters, robotics lab directors, autonomous vehicle teams, and embedded systems leads.

The site must deliver:
1. **Immediate Clarity:** Within 5 seconds, communicate who Josiah is (Robotics Engineer at Evolve Robotics, B.Tech Robotics & Automation 2025, Saintgits College), his core technical competencies (ROS 2, embedded systems, micro-ROS, mobile robot SLAM, robot kinematics, hardware integration), and direct paths to verified project evidence.
2. **Authentic Technical Credibility:** Distinguish rigorously between physical hardware testing, simulation-only validation, and planned roadmap items. Ground every quantitative metric in verified repository commits.
3. **Engineering-Editorial Aesthetic:** Replace generic AI templates, empty developer placeholders ("Drop images here", "demo coming soon"), and noisy decorative gradients with a refined, high-contrast, industrial dark theme featuring clean technical SVGs, real diagrams, structured specs, and clear hierarchy.
4. **First-Class Usability & Responsiveness:** Fluid layouts tested across 1440×900, 1024×768, 768×1024, 390×844, and 360×800.
5. **Accessibility & Maintainability:** Full WCAG 2.2 AA orientation (keyboard navigation, high contrast, focus-visible indicators, reduced-motion compliance) with a clean vanilla HTML5/CSS3/ES6 codebase deployable seamlessly to GitHub Pages.

---

## 2. Baseline Audit & Key Deficiencies Identified

### A. Developer Artifacts & Unfinished Placeholders
- **Homepage Project Carousels:** Projects 01 (Tilling Robot), 03 (ROS 2 Mobile Robot), and 04 (ESP32 micro-ROS) display empty carousel tracks with developer instructional placeholders: `"Drop images in assets/projects/..."`.
- **Video Placeholders:** All four project cards display empty video slots with `"Demo coming soon — drop demo.mp4 in assets/projects/.../videos/"`. On a professional portfolio, these appear as broken/incomplete scaffolding rather than finished work.
- **Visuals:** Project 02 (Quadruped Locomotion) now has 4 genuine technical diagrams. Projects 01, 03, and 04 require dedicated, accurate technical visuals (such as system architectures and wiring/kinematic diagrams) instead of empty boxes.

### B. Project Portfolio Architecture & Case Study Consistency
- Three projects currently have dedicated case-study pages:
  - `quadruped-locomotion.html` (ROS 2 12-DOF Quadruped)
  - `esp32-microros-robot.html` (ESP32 micro-ROS 2WD Car)
  - `tilling-robot.html` (Autonomous Tilling Robot)
- Project 03 on the homepage (`ros2_jazzy_2wd_robot`) does not have a dedicated case study page, only linking to GitHub. We should either create a clean, comprehensive case study or elevate the card with rich technical architecture diagrams and clear navigation.
- Ensure all case studies follow a unified, rigorous 9-stage engineering case-study architecture.

### C. Design Token & Visual System Refinements
- Centralize design tokens in `styles.css`: background `#080b12`, surface `#0f1523`, elevated `#161f33`, borders `#1e293b` / `rgba(124, 58, 237, 0.25)`, typography (Inter for body, Poppins for bold structural headers, JetBrains Mono for telemetry, data, code, and badges).
- Eliminate distracting neon glow overlays (`.project-glow`) and oversized decorative elements in favor of crisp technical borders, structured metadata badges, and high-legibility typographic hierarchy.

---

## 3. Detailed Implementation Phases

### Phase 1: Homepage Visuals & Project Card Architecture
1. **Project 01 (Autonomous Tilling Robot):**
   - Replace empty carousel placeholder with an authentic technical architecture and sensor integration diagram card.
   - Cleanly remove empty video placeholder in favor of a clean "Validation & Field Status" block.
2. **Project 02 (Quadruped Locomotion Framework):**
   - Retain the 4 authentic diagrams in the carousel with enhanced captions and thumbnail navigation.
   - Streamline the card to highlight the 100 Hz control loop, closed-form analytical IK, and Gazebo Classic dynamic simulation.
3. **Project 03 (ROS 2 Jazzy 2WD Autonomous Robot & SLAM):**
   - Sourced from `JosiahSK/ros2_jazzy_2wd_robot`.
   - Feature an accurate technical diagram depicting the RPLidar A1, TF2 transform tree (`base_footprint -> base_link -> laser_frame / wheel_links`), Gazebo Harmonic simulation, and SLAM Toolbox mapping pipeline.
4. **Project 04 (ESP32 micro-ROS Differential Drive Robot):**
   - Embed an authentic hardware/network architecture visual illustrating the Micro XRCE-DDS UDP transport, 1 kHz LEDC PWM, and differential mixer.

### Phase 2: Design System & Styling Unification
- Unify CSS tokens across `styles.css` and all case-study pages (`quadruped-locomotion.html`, `esp32-microros-robot.html`, `tilling-robot.html`).
- Ensure navigation bar, footer, and section headers share identical height, padding, blur, border, and typography tokens.
- Refine button states with explicit `:focus-visible` and hover elevations.

### Phase 3: Case Study Deep Dives
- Review all three case studies to ensure strict compliance with `docs/PORTFOLIO_CLAIM_AUDIT.md`.
- Ensure technical tables, SVGs, code excerpts, and callout boxes resize flawlessly on mobile (360px–800px).
- Add full case study for ROS 2 Jazzy 2WD Mobile Robot (`ros2-mobile-robot.html`) to complete the 4-quadrant robotics showcase (Legged, Agricultural, Microcontroller/Embedded, Autonomous Navigation/SLAM).

### Phase 4: Automated Testing & Browser Verification
- Extend `tests/test_links.py` to:
  - Check for duplicate IDs across all HTML documents.
  - Verify semantic heading hierarchies (single `<h1>` per page, logical `<h2>`/`<h3>` nesting).
  - Verify all `<figure>` images and SVGs have valid `alt` attributes or `aria-label`s.
  - Test internal anchor resolution and cross-page fragment validation.
- Execute headless Edge browser screenshot suite across viewports:
  - 1440 × 900 (Desktop)
  - 1024 × 768 (Laptop)
  - 768 × 1024 (Tablet)
  - 390 × 844 (Mobile)
  - 360 × 800 (Narrow Mobile)
- Confirm zero horizontal scroll, zero visual collisions, and clean text readability.

### Phase 5: Deployment & Release Verification
- Stage all verified files, review git diff, commit with structured message.
- Push to `origin main` and monitor GitHub Actions deployment run.
- Perform live HTTP 200 ping verification across all endpoints and media assets.
- Generate comprehensive completion report in `docs/PORTFOLIO_V4_REPORT.md`.

---

## 4. Acceptance Criteria Checklist

- [ ] Zero placeholder boxes ("Drop images here", "demo coming soon") visible on production site.
- [ ] Every featured project possesses authentic visual evidence (diagrams, technical schematics, or simulation plots).
- [ ] Technical claims are 100% verified against code repositories.
- [ ] 4 full case study pages or dedicated deep dives representing the major robotics domains.
- [ ] Responsive layout verified at 1440px, 1024px, 768px, 390px, and 360px without horizontal scroll.
- [ ] Full WCAG 2.2 AA orientation (keyboard navigation, focus states, high contrast, reduced motion).
- [ ] `tests/test_links.py` regression suite passes with 0 errors.
- [ ] GitHub Actions Pages deployment passes and all live URLs return HTTP 200.
