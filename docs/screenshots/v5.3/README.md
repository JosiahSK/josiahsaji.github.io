# PORTFOLIO V5.3 SCREENSHOT VERIFICATION REGISTER

**Release Version:** Portfolio V5.3  
**Capture Date:** 2026-10-30  
**Test Engine:** Microsoft Edge (Headless Chromium)  
**Host Platform:** Windows 10/11 x64  
**Validation Method:** Automated ephemeral local server binding, PIL header verification (`im.verify()`), full raster pixel decoding (`im.load()`), and exact pixel dimension assertion (`im.size == (w, h)`).

---

## 1. Viewport Matrix & Visual Test Inventory

| Page | Viewport Description | Target Dimensions | Capture File | Byte Size | Verification Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Homepage** | Desktop (Widescreen) | 1440 &times; 900 | `home_desktop_1440x900.png` | ~290 KB | **PASS (Exact Match)** |
| **Homepage** | Standard Laptop | 1366 &times; 768 | `home_laptop_1366x768.png` | ~275 KB | **PASS (Exact Match)** |
| **Homepage** | Compact Laptop | 1280 &times; 800 | `home_laptop_1280x800.png` | ~265 KB | **PASS (Exact Match)** |
| **Homepage** | Tablet Landscape | 1024 &times; 768 | `home_tablet_landscape_1024x768.png` | ~248 KB | **PASS (Exact Match)** |
| **Homepage** | Tablet Portrait | 768 &times; 1024 | `home_tablet_portrait_768x1024.png` | ~181 KB | **PASS (Exact Match)** |
| **Homepage** | Mobile Flagship | 390 &times; 844 | `home_mobile_390x844.png` | ~62 KB | **PASS (Exact Match)** |
| **Homepage** | Compact Mobile | 375 &times; 812 | `home_mobile_375x812.png` | ~58 KB | **PASS (Exact Match)** |
| **Homepage** | Compact Android | 360 &times; 800 | `home_compact_mobile_360x800.png` | ~51 KB | **PASS (Exact Match)** |
| **Homepage** | Ultra-Small Mobile | 320 &times; 700 | `home_small_mobile_320x700.png` | ~44 KB | **PASS (Exact Match)** |
| **Homepage** | Landscape Mobile | 844 &times; 390 | `home_mobile_landscape_844x390.png` | ~85 KB | **PASS (Exact Match)** |
| **Quadruped** | Desktop | 1440 &times; 900 | `quadruped_desktop_1440x900.png` | ~380 KB | **PASS (Exact Match)** |
| **Quadruped** | Tablet Landscape | 1024 &times; 768 | `quadruped_tablet_1024x768.png` | ~310 KB | **PASS (Exact Match)** |
| **Quadruped** | Mobile Flagship | 390 &times; 844 | `quadruped_mobile_390x844.png` | ~182 KB | **PASS (Exact Match)** |
| **Quadruped** | Compact Android | 360 &times; 800 | `quadruped_compact_mobile_360x800.png` | ~165 KB | **PASS (Exact Match)** |
| **ESP32 micro-ROS** | Desktop | 1440 &times; 900 | `esp32_desktop_1440x900.png` | ~425 KB | **PASS (Exact Match)** |
| **ESP32 micro-ROS** | Tablet Landscape | 1024 &times; 768 | `esp32_tablet_1024x768.png` | ~340 KB | **PASS (Exact Match)** |
| **ESP32 micro-ROS** | Mobile Flagship | 390 &times; 844 | `esp32_mobile_390x844.png` | ~195 KB | **PASS (Exact Match)** |
| **ESP32 micro-ROS** | Compact Android | 360 &times; 800 | `esp32_compact_mobile_360x800.png` | ~178 KB | **PASS (Exact Match)** |
| **ROS 2 AMR** | Desktop | 1440 &times; 900 | `mobile_robot_desktop_1440x900.png` | ~415 KB | **PASS (Exact Match)** |
| **ROS 2 AMR** | Tablet Landscape | 1024 &times; 768 | `mobile_robot_tablet_1024x768.png` | ~335 KB | **PASS (Exact Match)** |
| **ROS 2 AMR** | Mobile Flagship | 390 &times; 844 | `mobile_robot_mobile_390x844.png` | ~191 KB | **PASS (Exact Match)** |
| **ROS 2 AMR** | Compact Android | 360 &times; 800 | `mobile_robot_compact_mobile_360x800.png` | ~172 KB | **PASS (Exact Match)** |
| **Tilling Robot** | Desktop | 1440 &times; 900 | `tilling_desktop_1440x900.png` | ~375 KB | **PASS (Exact Match)** |
| **Tilling Robot** | Tablet Landscape | 1024 &times; 768 | `tilling_tablet_1024x768.png` | ~305 KB | **PASS (Exact Match)** |
| **Tilling Robot** | Mobile Flagship | 390 &times; 844 | `tilling_mobile_390x844.png` | ~174 KB | **PASS (Exact Match)** |
| **Tilling Robot** | Compact Android | 360 &times; 800 | `tilling_compact_mobile_360x800.png` | ~158 KB | **PASS (Exact Match)** |

---

## 2. Visual Observations & Quality Analysis

1. **Horizontal Viewport Fit:**  
   Runtime DOM scroll calculations confirmed `document.documentElement.scrollWidth <= window.innerWidth` across all 60 combinations of 6 HTML documents and 10 viewports. The prior horizontal overflow bug on `tilling-robot.html` caused by unconstrained metric card widths was resolved by responsive media queries (`repeat(2, 1fr)` on mobile and `clamp()` typography).

2. **Diagram Scalability:**  
   Technical SVG architecture and schematic diagrams scale with high fidelity from 1440px desktop displays down to 320px compact screens via responsive SVG viewBox attributes (`0 0 520 340` and `0 0 980 440`).

3. **Typography & Readability:**  
   Headings use Space Grotesk with fluid clamping; technical tables and telemetry labels use JetBrains Mono; body copy uses Inter with line-height &ge; 1.6.

4. **Testing Scope Distinction:**  
   Automated screenshots validate static layout rendering, component wrapping, and exact raster dimensions. Dynamic interactive states (modal focus trapping, roving tabindex, keyboard disclosure) are validated separately via the Chrome DevTools Protocol test suite (`tests/test_interactive.js`).
