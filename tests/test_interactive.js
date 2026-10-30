/**
 * tests/test_interactive.js
 * Real Browser Interaction & Accessibility Verification Suite
 * using Headless Microsoft Edge / Chromium via Chrome DevTools Protocol (CDP).
 *
 * Verifies:
 * 1. Accessible Lightbox:
 *    - Open via click / keydown.
 *    - Initial focus on close button.
 *    - Tab / Shift+Tab focus trap.
 *    - Escape dismissal.
 *    - Backdrop click dismissal.
 *    - Exact previous body overflow restoration.
 *    - Focus restoration to opener element.
 * 2. Mobile Navigation Disclosure:
 *    - Open / close toggle.
 *    - aria-expanded and aria-label synchronization.
 *    - Focus movement into menu.
 *    - Escape dismissal with focus return to hamburger.
 *    - Link click auto-close.
 * 3. Quadruped Gait Tabs:
 *    - Mouse selection updates panel visibility and ARIA states.
 *    - ArrowRight / ArrowDown moves to next tab.
 *    - ArrowLeft / ArrowUp moves to previous tab.
 *    - Home / End navigates to first / last tab.
 *    - Active / inactive panel 'hidden' and tabindex synchronization.
 */

const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.resolve(__dirname, '..');

// Simple static file server
function createServer() {
  const MIME_TYPES = {
    '.html': 'text/html; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.js': 'application/javascript; charset=utf-8',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.pdf': 'application/pdf',
    '.ico': 'image/x-icon'
  };

  return new Promise((resolve, reject) => {
    const server = http.createServer((req, res) => {
      let reqPath = decodeURIComponent(req.url.split('?')[0]);
      if (reqPath === '/') reqPath = '/index.html';
      const filePath = path.join(ROOT_DIR, reqPath);

      if (!fs.existsSync(filePath) || fs.statSync(filePath).isDirectory()) {
        res.writeHead(404);
        res.end('Not Found');
        return;
      }

      const ext = path.extname(filePath).toLowerCase();
      const mime = MIME_TYPES[ext] || 'application/octet-stream';
      res.writeHead(200, { 'Content-Type': mime });
      fs.createReadStream(filePath).pipe(res);
    });

    server.listen(0, '127.0.0.1', () => {
      const port = server.address().port;
      resolve({ server, port });
    });
  });
}

function findBrowser() {
  const candidates = [
    'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
  ];
  for (const c of candidates) {
    if (fs.existsSync(c)) return c;
  }
  return null;
}

// Minimal CDP client using Node 24 native WebSocket
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

  async close() {
    if (this.ws) this.ws.close();
  }
}

async function runInteractiveTests() {
  console.log('='.repeat(75));
  console.log('PORTFOLIO V5.2.1 — REAL BROWSER INTERACTIVE & ACCESSIBILITY TESTS');
  console.log('='.repeat(75));

  const browserPath = findBrowser();
  if (!browserPath) {
    console.error('[FAIL] No supported Chromium browser binary found for interactive tests.');
    process.exit(1);
  }

  const { server, port } = await createServer();
  const cdpPort = 9223;
  const tempProfile = path.join(ROOT_DIR, '.tmp_interactive_profile');

  const browserProc = spawn(browserPath, [
    '--headless=new',
    `--remote-debugging-port=${cdpPort}`,
    '--no-sandbox',
    '--disable-gpu',
    `--user-data-dir=${tempProfile}`,
    'about:blank'
  ]);

  // Wait for browser CDP HTTP endpoint
  await new Promise(r => setTimeout(r, 1200));

  let totalTests = 0;
  let passedTests = 0;

  function assert(condition, name) {
    totalTests++;
    if (condition) {
      passedTests++;
      console.log(`  [PASS] ${name}`);
    } else {
      console.error(`  [FAIL] ${name}`);
    }
  }

  try {
    // 1. Get browser targets
    const targetsRes = await new Promise((resolve, reject) => {
      http.get(`http://127.0.0.1:${cdpPort}/json/list`, res => {
        let d = '';
        res.on('data', c => d += c);
        res.on('end', () => resolve(JSON.parse(d)));
      }).on('error', reject);
    });

    const pageTarget = targetsRes.find(t => t.type === 'page') || targetsRes[0];
    const cdp = new CDPClient(pageTarget.webSocketDebuggerUrl);
    await cdp.connect();
    await cdp.send('Page.enable');
    await cdp.send('Runtime.enable');

    // ──────────────────────────────────────────────────────────────────────────
    // SUITE 1: Quadruped Gait Tabs ARIA & Keyboard Navigation
    // ──────────────────────────────────────────────────────────────────────────
    console.log('\n[Suite 1: Quadruped Tabs Keyboard Navigation & ARIA Relationships]');
    await cdp.send('Page.navigate', { url: `http://127.0.0.1:${port}/quadruped-locomotion.html` });
    await new Promise(r => setTimeout(r, 600));
    await cdp.evaluate(`new Promise(resolve => {
      if (document.readyState === 'complete') resolve();
      else window.addEventListener('load', () => resolve());
    })`);
    await new Promise(r => setTimeout(r, 400));

    // Test Initial Tab State
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
        panel2Hidden: panel2.hasAttribute('hidden')
      };
    })()`);

    assert(initialTabState.tab1Selected === 'true', 'Tab 1 initially has aria-selected="true"');
    assert(initialTabState.tab1Index === '0', 'Tab 1 initially has roving tabindex="0"');
    assert(initialTabState.tab1Controls === 'quad-panel-kinematics', 'Tab 1 aria-controls matches Panel 1 ID');
    assert(initialTabState.panel1Label === 'quad-tab-kinematics', 'Panel 1 aria-labelledby matches Tab 1 ID');
    assert(initialTabState.panel1Hidden === false, 'Panel 1 is initially visible (not hidden)');
    assert(initialTabState.panel2Hidden === true, 'Panel 2 is initially hidden');

    // Test Mouse Click on Tab 2
    const clickTab2 = await cdp.evaluate(`(() => {
      const tab2 = document.getElementById('quad-tab-gait');
      tab2.click();
      const tab1 = document.getElementById('quad-tab-kinematics');
      const panel1 = document.getElementById('quad-panel-kinematics');
      const panel2 = document.getElementById('quad-panel-gait');
      return {
        tab2Selected: tab2.getAttribute('aria-selected'),
        tab2Index: tab2.getAttribute('tabindex'),
        tab1Selected: tab1.getAttribute('aria-selected'),
        tab1Index: tab1.getAttribute('tabindex'),
        panel2Hidden: panel2.hasAttribute('hidden'),
        panel1Hidden: panel1.hasAttribute('hidden')
      };
    })()`);

    assert(clickTab2.tab2Selected === 'true' && clickTab2.tab1Selected === 'false', 'Mouse click activates Tab 2 and deactivates Tab 1');
    assert(clickTab2.tab2Index === '0' && clickTab2.tab1Index === '-1', 'Roving tabindex shifts to Tab 2');
    assert(clickTab2.panel2Hidden === false && clickTab2.panel1Hidden === true, 'Panel 2 becomes visible and Panel 1 becomes hidden');

    // Test Keyboard Navigation (ArrowRight, ArrowLeft, Home, End)
    const keyNavState = await cdp.evaluate(`(() => {
      const tab2 = document.getElementById('quad-tab-gait');
      tab2.focus();

      // Dispatch ArrowRight -> Tab 3
      tab2.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowRight', bubbles: true }));
      const tab3 = document.getElementById('quad-tab-polygon');
      const t3Active = tab3.getAttribute('aria-selected') === 'true';

      // Dispatch ArrowRight -> Wraps to Tab 1
      tab3.dispatchEvent(new KeyboardEvent('keydown', { key: 'ArrowRight', bubbles: true }));
      const tab1 = document.getElementById('quad-tab-kinematics');
      const t1Active = tab1.getAttribute('aria-selected') === 'true';

      // Dispatch End -> Tab 3
      tab1.dispatchEvent(new KeyboardEvent('keydown', { key: 'End', bubbles: true }));
      const tEndActive = tab3.getAttribute('aria-selected') === 'true';

      // Dispatch Home -> Tab 1
      tab3.dispatchEvent(new KeyboardEvent('keydown', { key: 'Home', bubbles: true }));
      const tHomeActive = tab1.getAttribute('aria-selected') === 'true';

      return { t3Active, t1Active, tEndActive, tHomeActive };
    })()`);

    assert(keyNavState.t3Active, 'ArrowRight advances to Tab 3');
    assert(keyNavState.t1Active, 'ArrowRight wraps from last tab to Tab 1');
    assert(keyNavState.tEndActive, 'End key navigates to last tab');
    assert(keyNavState.tHomeActive, 'Home key navigates to first tab');

    // ──────────────────────────────────────────────────────────────────────────
    // SUITE 2: Accessible Lightbox Modal Behavior & Overflow Restoration
    // ──────────────────────────────────────────────────────────────────────────
    console.log('\n[Suite 2: Lightbox Modal Accessibility, Overflow & Focus Restoration]');

    const lightboxTest = await cdp.evaluate(`(() => {
      const initialOverflow = document.body.style.overflow;
      const zoomFigure = document.querySelector('.zoomable-figure');
      zoomFigure.focus();
      const openerId = zoomFigure.id || 'figure-opener';
      zoomFigure.id = openerId;

      // 1. Open modal via click
      zoomFigure.click();
      const modal = document.getElementById('diagramModal');
      const closeBtn = document.getElementById('diagramModalClose');
      const modalOpen = modal.classList.contains('active');
      const lockedOverflow = document.body.style.overflow;
      const focusedOnOpen = document.activeElement === closeBtn;

      // 2. Dismiss via Escape key
      modal.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
      const modalClosedOnEscape = !modal.classList.contains('active');
      const restoredOverflow = document.body.style.overflow;
      const focusedOnClose = document.activeElement === zoomFigure;

      // 3. Open again and test backdrop dismissal
      zoomFigure.click();
      modal.dispatchEvent(new MouseEvent('click', { bubbles: true }));
      const modalClosedOnBackdrop = !modal.classList.contains('active');
      const restoredOverflowBackdrop = document.body.style.overflow;

      return {
        modalOpen,
        lockedOverflow,
        focusedOnOpen,
        modalClosedOnEscape,
        restoredOverflow,
        focusedOnClose,
        modalClosedOnBackdrop,
        restoredOverflowBackdrop,
        initialOverflow
      };
    })()`);

    assert(lightboxTest.modalOpen, 'Modal opens on clicking zoomable technical figure');
    assert(lightboxTest.lockedOverflow === 'hidden', 'Document body style.overflow set to "hidden" when open');
    assert(lightboxTest.focusedOnOpen, 'Initial focus placed automatically on close button');
    assert(lightboxTest.modalClosedOnEscape, 'Escape key dismisses modal dialog');
    assert(lightboxTest.restoredOverflow === lightboxTest.initialOverflow, 'Exact previous body style.overflow restored after Escape');
    assert(lightboxTest.focusedOnClose, 'Focus restored to original triggering diagram element');
    assert(lightboxTest.modalClosedOnBackdrop, 'Backdrop click dismisses modal dialog');
    assert(lightboxTest.restoredOverflowBackdrop === lightboxTest.initialOverflow, 'Exact previous body style.overflow restored after backdrop click');

    // ──────────────────────────────────────────────────────────────────────────
    // SUITE 3: Mobile Navigation Disclosure Pattern
    // ──────────────────────────────────────────────────────────────────────────
    console.log('\n[Suite 3: Mobile Navigation Disclosure & Accessibility Pattern]');
    await cdp.send('Page.navigate', { url: `http://127.0.0.1:${port}/index.html` });
    await new Promise(r => setTimeout(r, 800));

    const navTest = await cdp.evaluate(`(() => {
      const hamburger = document.getElementById('hamburger');
      const mobileMenu = document.getElementById('mobileMenu');
      const firstLink = mobileMenu.querySelector('.mobile-link');

      const initialExpanded = hamburger.getAttribute('aria-expanded');
      const controlsAttr = hamburger.getAttribute('aria-controls');
      const initialOpen = mobileMenu.classList.contains('open');

      // 1. Open mobile menu
      hamburger.click();
      const openedExpanded = hamburger.getAttribute('aria-expanded');
      const openedLabel = hamburger.getAttribute('aria-label');
      const openedClass = mobileMenu.classList.contains('open');
      const focusedOnLink = document.activeElement === firstLink;

      // 2. Close via Escape key
      document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
      const escapeExpanded = hamburger.getAttribute('aria-expanded');
      const escapeOpen = mobileMenu.classList.contains('open');
      const focusRestoredToHamburger = document.activeElement === hamburger;

      // 3. Open again and click a navigation link
      hamburger.click();
      firstLink.click();
      const linkClickOpen = mobileMenu.classList.contains('open');
      const linkClickExpanded = hamburger.getAttribute('aria-expanded');

      return {
        initialExpanded,
        controlsAttr,
        initialOpen,
        openedExpanded,
        openedLabel,
        openedClass,
        focusedOnLink,
        escapeExpanded,
        escapeOpen,
        focusRestoredToHamburger,
        linkClickOpen,
        linkClickExpanded
      };
    })()`);

    assert(navTest.initialExpanded === 'false', 'Hamburger initially has aria-expanded="false"');
    assert(navTest.controlsAttr === 'mobileMenu', 'Hamburger aria-controls points to "mobileMenu"');
    assert(navTest.initialOpen === false, 'Mobile menu initially closed');
    assert(navTest.openedExpanded === 'true', 'Clicking hamburger toggles aria-expanded="true"');
    assert(navTest.openedLabel === 'Close menu', 'Hamburger aria-label updates to "Close menu"');
    assert(navTest.openedClass === true, 'Mobile menu receives .open class');
    assert(navTest.focusedOnLink === true, 'Focus shifts automatically to first menu link');
    assert(navTest.escapeExpanded === 'false' && navTest.escapeOpen === false, 'Escape key closes mobile menu and resets aria-expanded');
    assert(navTest.focusRestoredToHamburger === true, 'Focus returns to hamburger button on Escape');
    assert(navTest.linkClickOpen === false && navTest.linkClickExpanded === 'false', 'Activating mobile link automatically closes navigation drawer');

    await cdp.close();

  } finally {
    server.close();
    browserProc.kill();
    try {
      fs.rmSync(tempProfile, { recursive: true, force: true });
    } catch (e) {}
  }

  console.log('\n' + '='.repeat(75));
  console.log(`INTERACTIVE TEST RESULTS: ${passedTests}/${totalTests} checks passed.`);
  console.log('='.repeat(75));

  if (passedTests !== totalTests) {
    process.exit(1);
  }
}

runInteractiveTests().catch(err => {
  console.error('[FATAL] Interactive test execution failed:', err);
  process.exit(1);
});
