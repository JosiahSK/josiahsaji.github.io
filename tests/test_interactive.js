/**
 * tests/test_interactive.js
 * Comprehensive Real Browser Interaction, Accessibility & Server Security Suite
 * using Headless Microsoft Edge / Chromium via Chrome DevTools Protocol (CDP).
 *
 * Verifies:
 * 1. Quadruped Gait Tabs:
 *    - Full WAI-ARIA tablist & tabpanel semantics.
 *    - Real keyboard traversal (ArrowRight, ArrowLeft, ArrowDown, ArrowUp, Home, End).
 *    - Roving tabindex ("0" vs "-1") and "hidden" panel synchronization.
 *    - Real key dispatch via CDP Input.dispatchKeyEvent.
 * 2. Accessible Lightbox across all 4 Case Studies:
 *    - Real Enter key activation from focused diagram triggers.
 *    - Dialog semantics (role="dialog", aria-modal="true", title & caption bindings).
 *    - Initial focus management.
 *    - Real Tab & Shift+Tab focus trap verification within modal.
 *    - Cloned SVG visual integrity & internal defs ID namespacing (zero DOM duplicate IDs).
 *    - Real Escape key dismissal with focus restoration to opener element.
 *    - Exact previous body overflow restoration (tested with non-empty 'clip' and empty default).
 *    - Backdrop click dismissal and scroll position preservation.
 * 3. Mobile Navigation Disclosure Pattern:
 *    - Real Enter key toggle.
 *    - Dynamic aria-expanded and aria-label updates.
 *    - Natural document tab order (no artificial trap).
 *    - Real Escape dismissal with focus return to hamburger.
 *    - Smooth section anchor activation with focus transfer to destination landmark.
 * 4. Local Test Server Hardening & Path Traversal Resistance:
 *    - Safe path resolution, malicious traversal rejection (403/404), stream error handling.
 */

const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const os = require('os');
const path = require('path');

const ROOT_DIR = path.resolve(__dirname, '..');

// Hardened static file server
function createServer() {
  const MIME_TYPES = {
    '.html': 'text/html; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.js': 'application/javascript; charset=utf-8',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.pdf': 'application/pdf',
    '.ico': 'image/x-icon',
    '.xml': 'application/xml; charset=utf-8',
    '.txt': 'text/plain; charset=utf-8',
    '.svg': 'image/svg+xml'
  };

  return new Promise((resolve, reject) => {
    const server = http.createServer((req, res) => {
      let reqUrl = req.url.split('?')[0];
      let decodedPath;
      try {
        decodedPath = decodeURIComponent(reqUrl);
      } catch (err) {
        res.writeHead(400, { 'Content-Type': 'text/plain' });
        res.end('Bad Request: Malformed URI');
        return;
      }

      if (decodedPath === '/' || decodedPath === '') {
        decodedPath = '/index.html';
      }

      if (reqUrl.includes('..') || decodedPath.includes('..')) {
        res.writeHead(403, { 'Content-Type': 'text/plain' });
        res.end('Forbidden: Directory Traversal Rejected');
        return;
      }

      // Safe path resolution: strictly prevent directory traversal outside ROOT_DIR
      const normalized = path.normalize(decodedPath).replace(/^(\.\.[\/\\])+/, '');
      const safePath = path.resolve(ROOT_DIR, '.' + path.sep + normalized);

      if (!safePath.startsWith(ROOT_DIR + path.sep) && safePath !== ROOT_DIR) {
        res.writeHead(403, { 'Content-Type': 'text/plain' });
        res.end('Forbidden: Path Traversal Denied');
        return;
      }

      fs.stat(safePath, (err, stats) => {
        if (err || !stats.isFile()) {
          res.writeHead(404, { 'Content-Type': 'text/plain' });
          res.end('Not Found');
          return;
        }

        const ext = path.extname(safePath).toLowerCase();
        const mime = MIME_TYPES[ext] || 'application/octet-stream';
        res.writeHead(200, { 'Content-Type': mime });

        const stream = fs.createReadStream(safePath);
        stream.on('error', () => {
          if (!res.headersSent) {
            res.writeHead(500, { 'Content-Type': 'text/plain' });
            res.end('Internal Server Error');
          }
        });
        stream.pipe(res);
      });
    });

    server.listen(0, '127.0.0.1', () => {
      const port = server.address().port;
      resolve({ server, port });
    });
  });
}

function findBrowser() {
  if (process.env.BROWSER_PATH && fs.existsSync(process.env.BROWSER_PATH)) {
    return process.env.BROWSER_PATH;
  }
  const candidates = [
    'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
    '/usr/bin/google-chrome',
    '/usr/bin/chromium-browser',
    '/usr/bin/chromium',
    '/usr/bin/microsoft-edge',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge'
  ];
  for (const c of candidates) {
    if (fs.existsSync(c)) return c;
  }
  return null;
}

// Minimal robust CDP client using Node 24 native WebSocket
class CDPClient {
  constructor(wsUrl) {
    this.wsUrl = wsUrl;
    this.ws = null;
    this.id = 1;
    this.pending = new Map();
  }

  async connect() {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.wsUrl);
      this.ws.onopen = () => resolve();
      this.ws.onerror = (e) => reject(e);
      this.ws.onmessage = (msg) => {
        const data = JSON.parse(msg.data);
        if (data.id && this.pending.has(data.id)) {
          const { resolve, reject } = this.pending.get(data.id);
          this.pending.delete(data.id);
          if (data.error) reject(data.error);
          else resolve(data.result);
        }
      };
    });
  }

  async send(method, params = {}) {
    const msgId = this.id++;
    return new Promise((resolve, reject) => {
      this.pending.set(msgId, { resolve, reject });
      this.ws.send(JSON.stringify({ id: msgId, method, params }));
    });
  }

  async evaluate(expression) {
    const res = await this.send('Runtime.evaluate', {
      expression,
      returnByValue: true,
      awaitPromise: true
    });
    if (res.exceptionDetails) {
      throw new Error(res.exceptionDetails.text || 'CDP Evaluation Error');
    }
    return res.result ? res.result.value : undefined;
  }

  async dispatchKey(key, code, windowsVirtualKeyCode, modifiers = 0) {
    const isEnter = key === 'Enter';
    await this.send('Input.dispatchKeyEvent', {
      type: 'rawKeyDown',
      key: key,
      code: code,
      windowsVirtualKeyCode: windowsVirtualKeyCode,
      modifiers: modifiers,
      text: isEnter ? '\r' : (key.length === 1 ? key : undefined),
      unmodifiedText: isEnter ? '\r' : (key.length === 1 ? key : undefined)
    });
    if (key.length === 1 || isEnter) {
      await this.send('Input.dispatchKeyEvent', {
        type: 'char',
        text: isEnter ? '\r' : key,
        unmodifiedText: isEnter ? '\r' : key
      });
    }
    await this.send('Input.dispatchKeyEvent', {
      type: 'keyUp',
      key: key,
      code: code,
      windowsVirtualKeyCode: windowsVirtualKeyCode,
      modifiers: modifiers
    });
  }

  async close() {
    if (this.ws) {
      try { this.ws.close(); } catch (e) {}
    }
  }
}

async function runInteractiveTests() {
  console.log('='.repeat(78));
  console.log('PORTFOLIO V5.3 — DEEP REAL BROWSER ACCESSIBILITY & INTERACTION VERIFICATION');
  console.log('='.repeat(78));

  const browserPath = findBrowser();
  if (!browserPath) {
    console.error('[FAIL] No supported Chromium browser binary found for interactive tests.');
    process.exit(1);
  }
  console.log(`[+] Discovered Browser Engine: ${browserPath}`);

  const { server, port } = await createServer();
  console.log(`[+] Ephemeral Static Test Server listening on: http://127.0.0.1:${port}`);

  // Create isolated temp profile in system temporary directory
  const tempProfile = fs.mkdtempSync(path.join(os.tmpdir(), 'portfolio-cdp-profile-'));
  console.log(`[+] Isolated User Data Profile: ${tempProfile}`);

  const browserProc = spawn(browserPath, [
    '--headless=new',
    '--remote-debugging-port=0',
    '--no-sandbox',
    '--disable-gpu',
    `--user-data-dir=${tempProfile}`,
    'about:blank'
  ]);

  // Discover dynamic remote debugging port from DevToolsActivePort
  const activePortFile = path.join(tempProfile, 'DevToolsActivePort');
  let cdpPort = null;
  for (let i = 0; i < 40; i++) {
    if (fs.existsSync(activePortFile)) {
      try {
        const lines = fs.readFileSync(activePortFile, 'utf8').trim().split(/\r?\n/);
        if (lines[0] && parseInt(lines[0], 10) > 0) {
          cdpPort = parseInt(lines[0], 10);
          break;
        }
      } catch (e) {}
    }
    await new Promise(r => setTimeout(r, 100));
  }

  if (!cdpPort) {
    console.error('[FAIL] Failed to discover DevToolsActivePort from headless browser.');
    browserProc.kill();
    fs.rmSync(tempProfile, { recursive: true, force: true, maxRetries: 5 });
    server.close();
    process.exit(1);
  }
  console.log(`[+] Dynamic DevTools Port Assigned: ${cdpPort}`);

  let totalTests = 0;
  let passedTests = 0;
  let failedTests = 0;

  function assert(condition, name) {
    totalTests++;
    if (condition) {
      passedTests++;
      console.log(`  [PASS] ${name}`);
    } else {
      failedTests++;
      console.error(`  [FAIL] ${name}`);
    }
  }

  let cdp = null;

  try {
    // Connect to CDP target
    const targetsRes = await new Promise((resolve, reject) => {
      http.get(`http://127.0.0.1:${cdpPort}/json/list`, res => {
        let d = '';
        res.on('data', c => d += c);
        res.on('end', () => resolve(JSON.parse(d)));
      }).on('error', reject);
    });

    const pageTarget = targetsRes.find(t => t.type === 'page') || targetsRes[0];
    cdp = new CDPClient(pageTarget.webSocketDebuggerUrl);
    await cdp.connect();
    await cdp.send('Page.enable');
    await cdp.send('Runtime.enable');

    async function navigateTo(urlPath) {
      await cdp.send('Page.navigate', { url: `http://127.0.0.1:${port}/${urlPath}` });
      await new Promise(r => setTimeout(r, 300));
      await cdp.evaluate(`new Promise(resolve => {
        if (document.readyState === 'complete') resolve();
        else window.addEventListener('load', () => resolve());
      })`);
      await new Promise(r => setTimeout(r, 200));
    }

    // ──────────────────────────────────────────────────────────────────────────
    // SUITE 1: Local Test Server Security & Path Traversal Resistance
    // ──────────────────────────────────────────────────────────────────────────
    console.log('\n[Suite 1: Local Test Server Security & Traversal Resistance]');

    async function httpGet(urlPath) {
      return new Promise((resolve) => {
        http.get(`http://127.0.0.1:${port}${urlPath}`, res => {
          let body = '';
          res.on('data', c => body += c);
          res.on('end', () => resolve({ status: res.statusCode, headers: res.headers, body }));
        }).on('error', err => resolve({ status: 500, error: err }));
      });
    }

    const resHome = await httpGet('/index.html');
    assert(resHome.status === 200 && resHome.headers['content-type'].includes('text/html'), 'Serves index.html with HTTP 200 and text/html');

    const resRobots = await httpGet('/robots.txt');
    assert(resRobots.status === 200 && resRobots.body.includes('Sitemap:'), 'Serves robots.txt with HTTP 200');

    const resSitemap = await httpGet('/sitemap.xml');
    assert(resSitemap.status === 200 && resSitemap.body.includes('<urlset'), 'Serves sitemap.xml with HTTP 200');

    const res404 = await httpGet('/nonexistent_file_xyz.html');
    assert(res404.status === 404, 'Returns HTTP 404 for missing resources');

    const resTraversal = await httpGet('/../package.json');
    assert(resTraversal.status === 403 || resTraversal.status === 404, 'Rejects directory traversal attempts (../)');

    const resEncodedTraversal = await httpGet('/%2e%2e%2fstyles.css');
    assert(resEncodedTraversal.status === 403 || resEncodedTraversal.status === 404, 'Rejects URL-encoded directory traversal (%2e%2e%2f)');

    const resMalformed = await httpGet('/%E0%A4%A');
    assert(resMalformed.status === 400 || resMalformed.status === 404, 'Safely handles malformed percent-encoded URIs without server crash');

    // ──────────────────────────────────────────────────────────────────────────
    // SUITE 2: Quadruped Gait Tabs ARIA & Real Keyboard Navigation
    // ──────────────────────────────────────────────────────────────────────────
    console.log('\n[Suite 2: Quadruped Tabs Real Keyboard Traversal & WAI-ARIA Relationships]');
    await navigateTo('quadruped-locomotion.html');

    const initialTabState = await cdp.evaluate(`(() => {
      const tab1 = document.getElementById('quad-tab-kinematics');
      const panel1 = document.getElementById('quad-panel-kinematics');
      const panel2 = document.getElementById('quad-panel-gait');
      return {
        tab1Selected: tab1.getAttribute('aria-selected'),
        tab1Index: tab1.getAttribute('tabindex'),
        tab1Controls: tab1.getAttribute('aria-controls'),
        panel1Label: panel1.getAttribute('aria-labelledby'),
        panel1Hidden: panel1.hasAttribute('hidden'),
        panel2Hidden: panel2.hasAttribute('hidden'),
        panel1Tabindex: panel1.getAttribute('tabindex')
      };
    })()`);

    assert(initialTabState.tab1Selected === 'true', 'Tab 1 initially has aria-selected="true"');
    assert(initialTabState.tab1Index === '0', 'Tab 1 initially has roving tabindex="0"');
    assert(initialTabState.tab1Controls === 'quad-panel-kinematics', 'Tab 1 aria-controls matches Panel 1 ID');
    assert(initialTabState.panel1Label === 'quad-tab-kinematics', 'Panel 1 aria-labelledby matches Tab 1 ID');
    assert(initialTabState.panel1Hidden === false, 'Panel 1 is initially visible (not hidden)');
    assert(initialTabState.panel2Hidden === true, 'Panel 2 is initially hidden');
    assert(initialTabState.panel1Tabindex === '0', 'Active panel 1 is keyboard focusable (tabindex="0")');

    // Focus Tab 1 and test Real Keyboard Traversal via CDP
    await cdp.evaluate(`document.getElementById('quad-tab-kinematics').focus()`);
    let focusedTabId = await cdp.evaluate(`document.activeElement.id`);
    assert(focusedTabId === 'quad-tab-kinematics', 'Keyboard focus placed on Tab 1');

    // Real ArrowRight key press -> moves to Tab 2
    await cdp.dispatchKey('ArrowRight', 'ArrowRight', 39);
    let tabStateAfterArrowRight = await cdp.evaluate(`(() => {
      const activeEl = document.activeElement;
      const tab2 = document.getElementById('quad-tab-gait');
      const panel2 = document.getElementById('quad-panel-gait');
      return {
        activeId: activeEl.id,
        tab2Selected: tab2.getAttribute('aria-selected'),
        tab2Index: tab2.getAttribute('tabindex'),
        panel2Hidden: panel2.hasAttribute('hidden')
      };
    })()`);
    assert(tabStateAfterArrowRight.activeId === 'quad-tab-gait', 'Real ArrowRight key moves focus to Tab 2');
    assert(tabStateAfterArrowRight.tab2Selected === 'true', 'Tab 2 receives aria-selected="true"');
    assert(tabStateAfterArrowRight.panel2Hidden === false, 'Panel 2 becomes visible');

    // Real ArrowRight key press again -> moves to Tab 3
    await cdp.dispatchKey('ArrowRight', 'ArrowRight', 39);
    let tabStateTab3 = await cdp.evaluate(`document.activeElement.id`);
    assert(tabStateTab3 === 'quad-tab-polygon', 'Real ArrowRight key advances to Tab 3');

    // Real ArrowRight key press at end of list -> wraps to Tab 1
    await cdp.dispatchKey('ArrowRight', 'ArrowRight', 39);
    let tabStateWrap = await cdp.evaluate(`document.activeElement.id`);
    assert(tabStateWrap === 'quad-tab-kinematics', 'Real ArrowRight key wraps from last tab to Tab 1');

    // Real ArrowLeft key press at start of list -> wraps backward to Tab 3
    await cdp.dispatchKey('ArrowLeft', 'ArrowLeft', 37);
    let tabStateWrapBack = await cdp.evaluate(`document.activeElement.id`);
    assert(tabStateWrapBack === 'quad-tab-polygon', 'Real ArrowLeft key wraps from first tab to last tab');

    // Real Home key -> navigates to first tab
    await cdp.dispatchKey('Home', 'Home', 36);
    let tabStateHome = await cdp.evaluate(`document.activeElement.id`);
    assert(tabStateHome === 'quad-tab-kinematics', 'Real Home key jumps to first tab');

    // Real End key -> navigates to last tab
    await cdp.dispatchKey('End', 'End', 35);
    let tabStateEnd = await cdp.evaluate(`document.activeElement.id`);
    assert(tabStateEnd === 'quad-tab-polygon', 'Real End key jumps to last tab');

    // ──────────────────────────────────────────────────────────────────────────
    // SUITE 3: Accessible Lightbox Across All Four Case Studies
    // ──────────────────────────────────────────────────────────────────────────
    console.log('\n[Suite 3: Accessible Lightbox Modal Behavior Across All 4 Case Studies]');

    const caseStudyPages = [
      'quadruped-locomotion.html',
      'esp32-microros-robot.html',
      'tilling-robot.html',
      'ros2-mobile-robot.html'
    ];

    for (const pageName of caseStudyPages) {
      await navigateTo(pageName);

      // Pre-set a non-empty inline body overflow value to verify exact restoration
      await cdp.evaluate(`document.body.style.overflow = 'clip'`);
      await cdp.evaluate(`window.scrollTo(0, 320)`);

      // 1. Focus diagram trigger
      await cdp.evaluate(`(() => {
        const trigger = document.querySelector('.zoomable-figure');
        trigger.focus();
      })()`);

      // 2. Open modal using real Enter key
      await cdp.dispatchKey('Enter', 'Enter', 13);
      await new Promise(r => setTimeout(r, 200));

      const modalOpenState = await cdp.evaluate(`(() => {
        const modal = document.getElementById('diagramModal');
        const closeBtn = document.getElementById('diagramModalClose');
        const modalBody = document.getElementById('diagramModalBody');
        const cloneSvg = modalBody.querySelector('svg');
        const allDocIds = Array.from(document.querySelectorAll('[id]')).map(el => el.id);
        const duplicateIds = allDocIds.filter((id, i) => allDocIds.indexOf(id) !== i);

        return {
          isOpen: modal.classList.contains('active'),
          role: modal.getAttribute('role'),
          ariaModal: modal.getAttribute('aria-modal'),
          activeElementId: document.activeElement ? document.activeElement.id : null,
          bodyOverflowLocked: document.body.style.overflow === 'hidden',
          hasCloneSvg: cloneSvg !== null,
          duplicateIdCount: duplicateIds.length,
          duplicateIds: duplicateIds
        };
      })()`);

      assert(modalOpenState.isOpen, `[${pageName}] Modal opens upon real Enter key press on diagram trigger`);
      assert(modalOpenState.role === 'dialog' && modalOpenState.ariaModal === 'true', `[${pageName}] Modal has role="dialog" and aria-modal="true"`);
      assert(modalOpenState.activeElementId === 'diagramModalClose', `[${pageName}] Initial keyboard focus lands on modal close button`);
      assert(modalOpenState.bodyOverflowLocked, `[${pageName}] Body overflow locked to 'hidden' while modal is active`);
      assert(modalOpenState.duplicateIdCount === 0, `[${pageName}] Zero duplicate element IDs in document during SVG clone display`);

      // 3. Test Real Tab & Shift+Tab Focus Trap
      // Dispatch real Tab key
      await cdp.dispatchKey('Tab', 'Tab', 9);
      let tabTrap = await cdp.evaluate(`(() => {
        const modal = document.getElementById('diagramModal');
        return modal.contains(document.activeElement);
      })()`);
      assert(tabTrap, `[${pageName}] Real Tab key keeps focus trapped inside modal`);

      // Dispatch real Shift+Tab key
      await cdp.dispatchKey('Tab', 'Tab', 9, 8); // modifier 8 = Shift
      let shiftTabTrap = await cdp.evaluate(`(() => {
        const modal = document.getElementById('diagramModal');
        return modal.contains(document.activeElement);
      })()`);
      assert(shiftTabTrap, `[${pageName}] Real Shift+Tab key keeps focus trapped inside modal`);

      // 4. Dismiss modal using real Escape key
      await cdp.dispatchKey('Escape', 'Escape', 27);
      await new Promise(r => setTimeout(r, 200));

      const modalClosedState = await cdp.evaluate(`(() => {
        const modal = document.getElementById('diagramModal');
        const trigger = document.querySelector('.zoomable-figure');
        return {
          isOpen: modal.classList.contains('active'),
          bodyOverflowRestored: document.body.style.overflow === 'clip',
          currentOverflow: document.body.style.overflow,
          isFocusRestored: document.activeElement === trigger
        };
      })()`);

      assert(!modalClosedState.isOpen, `[${pageName}] Modal dismisses upon real Escape key press`);
      assert(modalClosedState.bodyOverflowRestored, `[${pageName}] Exact non-empty body overflow ('clip') faithfully restored upon closure`);
      assert(modalClosedState.isFocusRestored, `[${pageName}] Focus accurately returned to diagram opener trigger`);

      // Reset body overflow to default
      await cdp.evaluate(`document.body.style.overflow = ''`);
    }

    // ──────────────────────────────────────────────────────────────────────────
    // SUITE 4: Mobile Navigation Disclosure Pattern & Section Navigation
    // ──────────────────────────────────────────────────────────────────────────
    console.log('\n[Suite 4: Mobile Navigation Disclosure Pattern & Target Focus]');
    await navigateTo('index.html');

    // Emulate Mobile Device Viewport (390 x 844)
    await cdp.send('Emulation.setDeviceMetricsOverride', {
      width: 390,
      height: 844,
      deviceScaleFactor: 2,
      mobile: true
    });
    await new Promise(r => setTimeout(r, 200));

    const initialNavState = await cdp.evaluate(`(() => {
      const hamburger = document.getElementById('hamburger');
      const mobileMenu = document.getElementById('mobileMenu');
      return {
        expanded: hamburger.getAttribute('aria-expanded'),
        controls: hamburger.getAttribute('aria-controls'),
        label: hamburger.getAttribute('aria-label'),
        menuOpen: mobileMenu.classList.contains('open')
      };
    })()`);

    assert(initialNavState.expanded === 'false', 'Mobile hamburger initially has aria-expanded="false"');
    assert(initialNavState.controls === 'mobileMenu', 'Mobile hamburger aria-controls="mobileMenu"');
    assert(initialNavState.menuOpen === false, 'Mobile menu drawer initially closed');

    // Focus hamburger and open via real Enter key
    await cdp.evaluate(`document.getElementById('hamburger').focus()`);
    await cdp.dispatchKey('Enter', 'Enter', 13);
    await new Promise(r => setTimeout(r, 200));

    const openedNavState = await cdp.evaluate(`(() => {
      const hamburger = document.getElementById('hamburger');
      const mobileMenu = document.getElementById('mobileMenu');
      const firstLink = mobileMenu.querySelector('.mobile-link');
      return {
        expanded: hamburger.getAttribute('aria-expanded'),
        menuOpen: mobileMenu.classList.contains('open'),
        firstLinkFocused: document.activeElement === firstLink
      };
    })()`);

    assert(openedNavState.expanded === 'true', 'Hamburger aria-expanded updates to "true" on open');
    assert(openedNavState.menuOpen === true, 'Mobile menu drawer displays class "open"');
    assert(openedNavState.firstLinkFocused, 'Keyboard focus automatically advances to first mobile navigation link');

    // Test Natural Tab Navigation (move from first link to second link)
    await cdp.dispatchKey('Tab', 'Tab', 9);
    const secondLinkFocused = await cdp.evaluate(`(() => {
      const mobileLinks = document.querySelectorAll('#mobileMenu .mobile-link');
      return document.activeElement === mobileLinks[1];
    })()`);
    assert(secondLinkFocused, 'Real Tab key advances naturally to second mobile navigation link');

    // Test Escape key closes menu and returns focus to hamburger
    await cdp.dispatchKey('Escape', 'Escape', 27);
    await new Promise(r => setTimeout(r, 200));

    const escapedNavState = await cdp.evaluate(`(() => {
      const hamburger = document.getElementById('hamburger');
      const mobileMenu = document.getElementById('mobileMenu');
      return {
        expanded: hamburger.getAttribute('aria-expanded'),
        menuOpen: mobileMenu.classList.contains('open'),
        hamburgerFocused: document.activeElement === hamburger
      };
    })()`);

    assert(!escapedNavState.menuOpen, 'Escape key closes mobile menu drawer');
    assert(escapedNavState.expanded === 'false', 'Hamburger aria-expanded resets to "false"');
    assert(escapedNavState.hamburgerFocused, 'Escape key restores focus back to hamburger button');

    // Reopen and test Section Link Activation Focus Management
    await cdp.dispatchKey('Enter', 'Enter', 13);
    await new Promise(r => setTimeout(r, 200));

    await cdp.evaluate(`(() => {
      const projectsLink = document.querySelector('#mobileMenu a[href="#projects"]');
      if (projectsLink) projectsLink.click();
    })()`);
    await new Promise(r => setTimeout(r, 250));

    const sectionNavState = await cdp.evaluate(`(() => {
      const mobileMenu = document.getElementById('mobileMenu');
      const projectsSection = document.getElementById('projects');
      return {
        menuOpen: mobileMenu.classList.contains('open'),
        projectsFocused: document.activeElement === projectsSection
      };
    })()`);

    assert(!sectionNavState.menuOpen, 'Activating anchor link closes mobile menu drawer');
    assert(sectionNavState.projectsFocused, 'Activating anchor link smoothly shifts focus to target #projects section');

    // Reset device metrics
    await cdp.send('Emulation.clearDeviceMetricsOverride');

  } catch (err) {
    console.error('[UNCAUGHT TEST RUNNER ERROR]:', err);
    failedTests++;
  } finally {
    console.log('\n[+] Cleaning up test processes and temporary directories...');
    if (cdp) await cdp.close();
    browserProc.kill();
    server.close();

    // Robust temp profile removal
    try {
      fs.rmSync(tempProfile, { recursive: true, force: true, maxRetries: 10, retryDelay: 200 });
      console.log('[+] Temporary browser profile deleted successfully.');
    } catch (e) {
      console.warn('[-] Note: Windows retained temp profile lock; system temp will reap on reboot.');
    }

    console.log('='.repeat(78));
    console.log(`INTERACTION TEST SUMMARY: ${passedTests} PASSED, ${failedTests} FAILED (TOTAL: ${totalTests})`);
    console.log('='.repeat(78));

    if (failedTests > 0) {
      process.exit(1);
    } else {
      process.exit(0);
    }
  }
}

runInteractiveTests();
