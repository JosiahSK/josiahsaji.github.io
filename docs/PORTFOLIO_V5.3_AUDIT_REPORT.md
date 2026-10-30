# Portfolio V5.3 Engineering Audit & Hardening Report

**Release Identification:** Portfolio V5.3 (Production Hardening & Max-Depth Audit)  
**Baseline Commit:** `6ae094ac656bfdef9d21b4c200658143ff88f45b` (Portfolio V5.2.1)  
**Feature Branch:** `feature/portfolio-v5.3-deep-engineering-audit`  
**Target Production Branch:** `main`  
**Audit Date:** 2026-10-30  
**Live Production URL:** [https://josiahsk.github.io/josiahsaji.github.io/](https://josiahsk.github.io/josiahsaji.github.io/)  
**Central Claims Register:** [PORTFOLIO_CLAIMS_REGISTER.md](PORTFOLIO_CLAIMS_REGISTER.md)  
**Screenshot Visual Register:** [screenshots/v5.3/README.md](screenshots/v5.3/README.md)

---

## 1. Executive Summary & Deficiencies Resolved

This release executes a max-depth forensic audit, technical grounding pass, real browser keyboard test expansion, responsive overflow remediation, and production hardening of Josiah Saji's robotics portfolio.

### Key Root-Cause Issues Discovered & Corrected:
1. **Quadruped Controller Frequency Discrepancy (P0 Accuracy):**
   - *Discovery:* `index.html` contained the residual claim `validated in Gazebo Classic & RViz2 with synchronized 100 Hz ros2_control trajectory execution`. In the actual robotics workspace (`controllers.yaml`), `controller_manager.update_rate: 200` and `joint_trajectory_controller.state_publish_rate: 100.0`, while `locomotion_controller_node.py` runs a 100 Hz timer loop.
   - *Resolution:* Disambiguated all frequencies across `index.html` and `quadruped-locomotion.html`. Accurately documented that the 100 Hz rate represents the master locomotion controller timer loop streaming trajectory commands to a 200 Hz `ros2_control` controller manager with 100 Hz state publication.
2. **SVG Element `.click()` Browser DOM TypeError (P0 Accessibility):**
   - *Discovery:* When activating diagram triggers via real Enter/Space keyboard input, `<svg class="zoomable-figure">` triggers threw an unhandled runtime error: `TypeError: el.click is not a function`. Unlike `HTMLElement` (`<img>`), `SVGSVGElement` does not inherit `HTMLElement.prototype.click()`.
   - *Resolution:* Refactored lightbox trigger activation into a direct `triggerZoom()` function bound to both click and keydown, eliminating `el.click()` across all case studies.
3. **SVG Lightbox Modal DOM ID Collisions (P1 DOM Integrity):**
   - *Discovery:* Cloned SVGs appended to `diagramModalBody` duplicated all internal `<defs>` IDs (`linearGradient`, `marker`, `clipPath`), creating duplicate element IDs in the DOM during modal presentation.
   - *Resolution:* Implemented dynamic namespace rewriting prefixing all clone IDs (`modal-clone-*`) and remapping internal `url(#...)` and `href="#..."` references, ensuring zero duplicate IDs and 100% visual fidelity.
4. **Mobile Navigation Anchor Focus Drop (P1 Navigation):**
   - *Discovery:* Closing the mobile navigation drawer toggled `display: none`, causing browser focus to drop to `document.body` instead of advancing to target section landmarks.
   - *Resolution:* Added smooth programmatic focus transfer to destination section IDs (`tabindex="-1"`) with natural sequential tab resumption.
5. **Contact Form Unconfigured Fallback Reload Bug (P1 Form UX):**
   - *Discovery:* When Formspree was unconfigured, pressing Enter inside form input fields triggered default form submission (reloading the page with query parameters) because only button `click` was handled.
   - *Resolution:* Attached `handleMailtoFallback` to the form's `submit` event, properly handling both Enter key submission and button clicks without page reload.
6. **Mobile Horizontal Scroll Overflow (P1 Layout):**
   - *Discovery:* At 375px and 390px viewports on `tilling-robot.html`, `.metrics-grid` with `font-size: 1.8rem` metric values forced `.metric-card` to expand beyond container width, causing 18px of horizontal body overflow.
   - *Resolution:* Added responsive mobile grid rules (`repeat(2, 1fr)` at &le;600px with `clamp()` font scaling and word breaking), eliminating all page-level overflow across all viewports.
7. **Test Harness Vulnerabilities & Race Conditions (P1 Test Infra):**
   - *Discovery:* Test static server was vulnerable to path traversal (`/../`, `%2e%2e%2f`), used a fixed debugging port (`9223`), and created temporary profiles within the repository workspace.
   - *Resolution:* Implemented strict path containment checks, rejection of directory traversal (403), ephemeral port discovery via `DevToolsActivePort`, and isolated profiles in `os.tmpdir()`.

---

## 2. Complete Repository File Inventory

| File Path | Component / Purpose | Audit Findings | Actions Applied in V5.3 |
| :--- | :--- | :--- | :--- |
| `index.html` | Homepage & Robotics Showcase | Residual "100 Hz ros2_control" claim in line 472 | Rewrote line 472 to specify 100 Hz controller loop and 200 Hz controller manager; verified schema.org Person JSON-LD |
| `quadruped-locomotion.html` | Quadruped Case Study | Architecture SVG lacked 200 Hz manager label; specs table listed only 100 Hz | Added 200 Hz manager / 100 Hz state pub to SVG & specs table; fixed SVG clone ID collision; added TechArticle JSON-LD |
| `esp32-microros-robot.html` | ESP32 micro-ROS Case Study | SVG `.click()` error on Enter key; missing JSON-LD | Fixed trigger keydown to call `triggerZoom()`; namespace SVG clone IDs; added TechArticle JSON-LD; responsive metrics grid |
| `tilling-robot.html` | Tilling Robot Case Study | Outdated "and demo video" meta description; mobile metrics grid horizontal overflow; SVG `.click()` error | Updated meta description; added responsive mobile CSS to `.metrics-grid`; fixed triggerZoom; added TechArticle JSON-LD |
| `ros2-mobile-robot.html` | ROS 2 AMR Case Study | SVG `.click()` error on Enter key; missing JSON-LD | Fixed trigger keydown to call `triggerZoom()`; namespace SVG clone IDs; added TechArticle JSON-LD |
| `404.html` | Custom Error Route | Missing in previous releases | Created industrial-styled 404 page with navigation landmarks and back-to-home actions |
| `robots.txt` | Crawler Directive | Missing in previous releases | Created robots.txt with sitemap declaration |
| `sitemap.xml` | Search Engine Sitemap | Missing in previous releases | Created sitemap.xml with all 5 canonical production URLs |
| `styles.css` | Design System Stylesheet | Table responsive wrappers verified | Verified responsive rules, typography tokens, contrast ratios |
| `script.js` | Core Interactions & Logic | Contact form Enter reload bug; mobile menu anchor focus drop; hamburger Enter key | Bound `handleMailtoFallback` to form submit; added target section focus transfer; added hamburger Enter keydown |
| `assets/resume/resume.pdf` | Single-Page ATS Résumé | Audited for single-page constraint & text stream | Verified 134.8 KB, 3,751 characters, single page, 100% parseable by ATS text extractors |
| `tests/test_links.py` | Static DOM & Claim Suite | Needed V5.3 checks for 200 Hz manager and new pages | Updated checks to validate 6 HTML files, 200 Hz manager claims, disallowed patterns, and 22 positive assertions |
| `tests/test_interactive.js` | CDP Real Browser Test Suite | Fixed port 9223, local profile, lack of real Tab key | Upgraded to port 0, DevToolsActivePort, isolated temp profile, path traversal rejection, real CDP Tab/Shift+Tab |
| `tests/run_all_tests.py` | Unified Test Runner | Missing unified entry point | Created unified orchestrator executing compilation, syntax, static DOM, CDP browser tests, and screenshots |
| `scripts/capture_screenshots.py` | Screenshot Automation | 13 captures previously | Expanded to 26 captures (10 homepage viewports, 4 per case study) into `docs/screenshots/v5.3/` |
| `docs/PORTFOLIO_CLAIMS_REGISTER.md` | Central Claims Reference | New required deliverable | Created central traceability table mapping every claim to source code or configuration |
| `docs/screenshots/v5.3/README.md` | Screenshot Register | New required deliverable | Created detailed capture log and dimension verification register |

---

## 3. Technical Accuracy & Grounding Register

Every numerical frequency, sensor specification, and architectural configuration has been traced to physical or simulation configuration evidence:

1. **Locomotion Controller Frequency:**  
   - Source: `locomotion_controller_node.py` lines 38-40: `self.dt = 0.01`, timer loop period = 10 ms &rarr; **100 Hz**.
2. **Controller Manager Rate:**  
   - Source: `src/quadruped_description/config/controllers.yaml` line 3: `controller_manager: ros__parameters: update_rate: 200` &rarr; **200 Hz**.
3. **Joint State Broadcaster Rate:**  
   - Source: `src/quadruped_description/config/controllers.yaml` line 34: `joint_trajectory_controller: ros__parameters: state_publish_rate: 100.0` &rarr; **100 Hz**.
4. **IMU Sensor Simulation Rate:**  
   - Source: `src/quadruped_description/urdf/quadruped.urdf.xacro`: IMU gazebo sensor plugin &rarr; **200 Hz**.
5. **Mobile Robot Transform Publish Period:**  
   - Source: `mapper_params_online_async.yaml`: `transform_publish_period: 0.02` &rarr; **50 Hz** (1 / 0.02 s).
6. **Mobile Robot SLAM Boundary:**  
   - Source: `mapper_params_online_async.yaml`: `max_laser_range: 8.0 m` &rarr; Configured software noise cutoff, not physical hardware limit.
7. **RPLIDAR Revision Disambiguation:**  
   - Sourced from Slamtec A1M8 Datasheet v2.4 (LD108): A1M8-R4: 0.15–6.0 m; A1M8-R5: 0.15–12.0 m on white targets (90% reflectance). Physical unit revision remains designated as `UNVERIFIED`.
8. **ESP32 Firmware Specifications:**  
   - Source: `src/main.cpp`: LEDC PWM 1 kHz @ 8-bit resolution; motor pins GPIO 25, 26, 27, 14; watchdog timeout 500 ms; 2S Li-ion (7.4 V) with LM2596 buck converter (5.0 V logic).
9. **Agricultural Tilling Robot:**  
   - Square-tube steel chassis, 12V LiFePO4 battery pack, two-stroke cultivator engine, GPS NMEA waypoint guidance; submitted to Young Innovators Programme (YIP) 7.0.

---

## 4. Accessibility & Interactive Browser Verification

All interactive behaviors were tested directly in headless Microsoft Edge via Chrome DevTools Protocol (`tests/test_interactive.js`):

| Widget / Component | Test Action | Expected Behavior | Observed Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Quadruped Tabs** | Real ArrowRight key | Focus shifts to next tab; panel activates | Roving tabindex shifts to "0"; panel `hidden` removed | **PASS** |
| **Quadruped Tabs** | Real ArrowRight at end | Wraps focus to Tab 1 | Wrap confirmed | **PASS** |
| **Quadruped Tabs** | Real ArrowLeft at start | Wraps backward to Tab 3 | Wrap confirmed | **PASS** |
| **Quadruped Tabs** | Real Home / End keys | Jumps to first / last tab | Jumps confirmed | **PASS** |
| **Diagram Lightbox** | Real Enter on trigger | Opens modal with initial focus on close button | Close button focused; body overflow locked | **PASS** |
| **Diagram Lightbox** | Real Tab & Shift+Tab | Focus cycling trapped strictly within modal | Focus trapped; zero escape to document body | **PASS** |
| **Diagram Lightbox** | SVG Clone ID Check | Clone IDs namespaced (`modal-clone-*`) | Zero duplicate element IDs in document | **PASS** |
| **Diagram Lightbox** | Real Escape key | Closes modal and restores focus | Modal closed; focus returned to opener element | **PASS** |
| **Diagram Lightbox** | Overflow Restoration | Restores pre-existing `body.style.overflow` | Verified with pre-set non-empty `'clip'` value | **PASS** |
| **Mobile Navigation** | Real Enter on toggle | Toggles menu drawer open | `aria-expanded="true"`; focus on first link | **PASS** |
| **Mobile Navigation** | Real Tab key | Advances naturally through links | Natural document tab flow confirmed | **PASS** |
| **Mobile Navigation** | Real Escape key | Closes drawer and returns focus | Focus returned to hamburger button | **PASS** |
| **Mobile Navigation** | Anchor link click | Closes drawer & shifts focus to section | Focus transferred to `#projects` (`tabindex="-1"`) | **PASS** |
| **Contact Form** | Enter in text input | Triggers mailto fallback without page reload | Verified fallback execution without query reload | **PASS** |

---

## 5. Viewport Matrix & Visual Inspection

- **Screen Resolution Matrix:** 26 raster screenshots captured across 10 viewports on the homepage and 4 viewports across each of the 4 case studies.
- **Image Header & Dimension Integrity:** All 26 images verified with PIL `im.verify()` and `im.load()`. Exact pixel dimensions confirmed with zero scaling skew.
- **Horizontal Overflow Remediation:** Runtime DOM query `document.documentElement.scrollWidth <= window.innerWidth` verified across 60 document/viewport combinations with zero overflows.

---

## 6. Performance, SEO & Security Audit

- **Structured Data (JSON-LD):** Verified Person schema on `index.html` and TechArticle schema across all 4 case-study pages.
- **Sitemap & Search Directives:** Implemented `robots.txt` and `sitemap.xml` with absolute production URLs.
- **Custom Error Route:** Created `404.html` matching design system typography and color palette.
- **Security & Traversal:** Hardened local static test server against directory traversal (`../` and `%2e%2e%2f` rejected with 403 Forbidden). Verified safe textContent DOM manipulation and secure `rel="noopener noreferrer"` external links.
