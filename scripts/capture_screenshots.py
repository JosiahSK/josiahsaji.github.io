import os
import time
import subprocess
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
import tempfile

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

def run_server(port, root_dir):
    os.chdir(root_dir)
    handler = SimpleHTTPRequestHandler
    httpd = HTTPServer(('127.0.0.1', port), handler)
    httpd.serve_forever()

def capture_all():
    root_dir = r"D:\Documents\Antigravity_project\Interactive_Website\josiahsaji.github.io"
    out_dir = os.path.join(root_dir, "docs", "screenshots")
    os.makedirs(out_dir, exist_ok=True)
    
    port = 8089
    server_thread = threading.Thread(target=run_server, args=(port, root_dir), daemon=True)
    server_thread.start()
    time.sleep(1) # Allow server to bind
    
    edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    temp_profile = os.path.join(tempfile.gettempdir(), "edge_screen_profile")
    
    print(f"Starting viewport verification captures to {out_dir}...")
    
    # Capture homepage across all 5 viewports
    for name, w, h in VIEWPORTS:
        out_file = os.path.join(out_dir, f"home_{name}.png")
        url = f"http://127.0.0.1:{port}/index.html"
        cmd = [
            edge_exe,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            f"--window-size={w},{h}",
            f"--user-data-dir={temp_profile}",
            f"--screenshot={out_file}",
            url
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if os.path.exists(out_file) and os.path.getsize(out_file) > 1000:
            print(f"  [OK] Captured homepage ({w}x{h}) -> {os.path.basename(out_file)} ({os.path.getsize(out_file)} bytes)")
        else:
            print(f"  [FAIL] Failed to capture {name}")
            
    # Capture desktop view of all 4 case study pages
    for page_name, page_file in PAGES:
        if page_name == "index":
            continue
        out_file = os.path.join(out_dir, f"{page_name}_desktop.png")
        url = f"http://127.0.0.1:{port}/{page_file}"
        cmd = [
            edge_exe,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--window-size=1440,900",
            f"--user-data-dir={temp_profile}",
            f"--screenshot={out_file}",
            url
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if os.path.exists(out_file) and os.path.getsize(out_file) > 1000:
            print(f"  [OK] Captured case study {page_name} -> {os.path.basename(out_file)} ({os.path.getsize(out_file)} bytes)")
            
    print("Screenshot capture suite finished successfully.")

if __name__ == "__main__":
    capture_all()
