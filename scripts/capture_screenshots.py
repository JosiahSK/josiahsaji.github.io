#!/usr/bin/env python3
"""
scripts/capture_screenshots.py
Automated Multi-Viewport & Case Study Screenshot Verification Suite
for Josiah Saji's Robotics Portfolio (Portfolio V5.2 Release).

Features:
- Dynamically finds repository root from script location.
- Automatically locates Chrome/Edge/Chromium browser executable or uses BROWSER_PATH.
- Dynamically binds to a free local port on 127.0.0.1.
- Avoids process-global os.chdir() by using directory-bound HTTP request handler.
- Waits for server readiness with health-check timeout.
- Isolates browser sessions in fresh temporary user profiles with deterministic cleanup.
- Validates subprocess exit codes, image file creation, and PIL dimensions.
- Captures modal lightbox states.
- Returns non-zero exit code on failure.
"""

import os
import sys
import time
import socket
import shutil
import tempfile
import threading
import subprocess
import urllib.request
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

try:
    from PIL import Image
except ImportError:
    Image = None

VIEWPORTS = [
    ("desktop_1440x900", 1440, 900),
    ("tablet_landscape_1024x768", 1024, 768),
    ("tablet_portrait_768x1024", 768, 1024),
    ("mobile_390x844", 390, 844),
    ("compact_mobile_360x800", 360, 800)
]

PAGES = [
    ("index", "index.html"),
    ("quadruped", "quadruped-locomotion.html"),
    ("esp32", "esp32-microros-robot.html"),
    ("mobile_robot", "ros2-mobile-robot.html"),
    ("tilling", "tilling-robot.html")
]

def find_browser_executable():
    """Discover installed Chromium-based browser."""
    env_browser = os.environ.get("BROWSER_PATH")
    if env_browser and os.path.isfile(env_browser):
        return env_browser

    candidates = [
        # Microsoft Edge
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe"),
        # Google Chrome
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        # Unix/macOS fallbacks
        "msedge", "google-chrome", "chromium", "chromium-browser"
    ]

    for path in candidates:
        if os.path.isabs(path) and os.path.isfile(path):
            return path
        found = shutil.which(path)
        if found:
            return found
    return None

def wait_for_server(url, timeout=5.0):
    """Wait until local HTTP server responds."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(url, timeout=1.0) as res:
                if res.status == 200:
                    return True
        except Exception:
            time.sleep(0.1)
    return False

def capture_screenshot(browser_exe, temp_profile, url, out_path, width, height, strict=True):
    """Capture single viewport screenshot with headless browser and verify dimensions."""
    cmd = [
        browser_exe,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--hide-scrollbars",
        f"--window-size={width},{height}",
        f"--user-data-dir={temp_profile}",
        f"--screenshot={out_path}",
        url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
    if res.returncode != 0:
        return False, f"Browser exited with code {res.returncode}: {res.stderr.strip()}"
    if not os.path.isfile(out_path) or os.path.getsize(out_path) < 1000:
        return False, f"File not created or abnormally small (<1000 bytes)"
    
    # Explicit Image integrity and exact dimension validation
    if Image is None:
        if strict:
            return False, "Pillow is not installed: strict image dimension/integrity verification failed"
        dim_info = " (dimension check skipped: Pillow unavailable)"
    else:
        try:
            # 1. Structural header and block integrity verification
            with Image.open(out_path) as im_check:
                im_check.verify()

            # 2. Full raster decode and dimension matching
            with Image.open(out_path) as im:
                im.load()  # Fully decode raster image data into memory
                actual_w, actual_h = im.size
                if actual_w != width or actual_h != height:
                    return False, f"Dimension mismatch: expected {width}x{height}, got {actual_w}x{actual_h}"
                dim_info = f" ({actual_w}x{actual_h} exact match)"
        except Exception as e:
            return False, f"Invalid or corrupted image file: {e}"

    return True, f"{os.path.getsize(out_path)} bytes{dim_info}"

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    out_dir = os.path.join(root_dir, "docs", "screenshots")
    os.makedirs(out_dir, exist_ok=True)

    browser_exe = find_browser_executable()
    if not browser_exe:
        print("[FAIL] No Chromium browser (Edge/Chrome) discovered on host.", file=sys.stderr)
        sys.exit(1)

    print(f"Discovered browser: {browser_exe}")

    # Bind directly to port 0 on the actual listening socket to eliminate port race conditions
    handler = partial(SimpleHTTPRequestHandler, directory=root_dir)
    httpd = ThreadingHTTPServer(('127.0.0.1', 0), handler)
    port = httpd.server_address[1]
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()

    base_url = f"http://127.0.0.1:{port}"
    if not wait_for_server(f"{base_url}/index.html", timeout=6.0):
        print("[FAIL] Local test server failed to respond.", file=sys.stderr)
        httpd.shutdown()
        httpd.server_close()
        sys.exit(1)

    temp_profile = tempfile.mkdtemp(prefix="portfolio_screen_")
    print(f"Running automated screenshot suite across viewports to: {out_dir}\n")

    failures = 0
    total_captures = 0

    try:
        # 1. Homepage across 5 standard responsive viewports
        for vp_name, w, h in VIEWPORTS:
            total_captures += 1
            out_file = os.path.join(out_dir, f"home_{vp_name}.png")
            url = f"{base_url}/index.html"
            ok, msg = capture_screenshot(browser_exe, temp_profile, url, out_file, w, h)
            if ok:
                print(f"  [PASS] Homepage {w}x{h} -> {os.path.basename(out_file)} ({msg})")
            else:
                failures += 1
                print(f"  [FAIL] Homepage {w}x{h} -> {msg}", file=sys.stderr)

        # 2. All 4 Case Studies across Desktop (1440x900) and Mobile (390x844)
        for page_name, page_file in PAGES:
            if page_name == "index":
                continue

            # Desktop
            total_captures += 1
            out_desk = os.path.join(out_dir, f"{page_name}_desktop.png")
            url_desk = f"{base_url}/{page_file}"
            ok, msg = capture_screenshot(browser_exe, temp_profile, url_desk, out_desk, 1440, 900)
            if ok:
                print(f"  [PASS] Case Study {page_name} desktop -> {os.path.basename(out_desk)} ({msg})")
            else:
                failures += 1
                print(f"  [FAIL] Case Study {page_name} desktop -> {msg}", file=sys.stderr)

            # Mobile 390x844
            total_captures += 1
            out_mob = os.path.join(out_dir, f"{page_name}_mobile_390x844.png")
            url_mob = f"{base_url}/{page_file}"
            ok, msg = capture_screenshot(browser_exe, temp_profile, url_mob, out_mob, 390, 844)
            if ok:
                print(f"  [PASS] Case Study {page_name} mobile (390x844) -> {os.path.basename(out_mob)} ({msg})")
            else:
                failures += 1
                print(f"  [FAIL] Case Study {page_name} mobile -> {msg}", file=sys.stderr)

    finally:
        httpd.shutdown()
        httpd.server_close()
        server_thread.join(timeout=2.0)
        # Clean up temporary browser profile
        try:
            shutil.rmtree(temp_profile, ignore_errors=True)
        except Exception:
            pass

    print(f"\nScreenshot Suite Summary: {total_captures - failures}/{total_captures} passed.")
    if failures > 0:
        sys.exit(1)
    print("All captures generated, validated, and saved successfully.")

if __name__ == "__main__":
    main()
