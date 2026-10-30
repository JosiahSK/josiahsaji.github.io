/* ======================================
   Josiah Saji Portfolio - script.js
   ====================================== */

// ---- HERO CANVAS (starfield + grid + particle network) -----------------
try {
  (function initCanvas() {
    var canvas = document.getElementById('heroCanvas');
    if (!canvas) return;
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    var ctx = canvas.getContext('2d');

    // ── dimensions ──────────────────────────────────────────────────────
    var W, H;

    // ── particle network (existing) ──────────────────────────────────────
    var particles = [];
    var PARTICLE_COUNT = 55;

    // ── starfield ────────────────────────────────────────────────────────
    var stars = [];
    var STAR_COUNT = 190;

    // ── parallax ─────────────────────────────────────────────────────────
    var mouseX = 0, mouseY = 0;
    var parallaxX = 0, parallaxY = 0;
    var MAX_SHIFT = 12; // px

    // ── shooting stars ───────────────────────────────────────────────────
    var shooters = [];
    var nextShooterAt = 0; // timestamp

    // ── RAF handle for cleanup ────────────────────────────────────────────
    var rafId = null;

    // ────────────────────────────────────────────────────────────────────
    function resize() {
      W = canvas.width  = window.innerWidth;
      H = canvas.height = window.innerHeight;
    }

    // ── particle network helpers ─────────────────────────────────────────
    function makeParticle() {
      return {
        x: Math.random() * W,
        y: Math.random() * H,
        r: Math.random() * 1.5 + 0.5,
        vx: (Math.random() - 0.5) * 0.4,
        vy: (Math.random() - 0.5) * 0.4,
        alpha: Math.random() * 0.5 + 0.1,
        color: Math.random() > 0.5 ? '124,58,237' : '6,182,212'
      };
    }
    function resetParticle(p) {
      p.x = Math.random() * W;
      p.y = Math.random() * H;
    }
    function initParticles() {
      particles = [];
      for (var i = 0; i < PARTICLE_COUNT; i++) particles.push(makeParticle());
    }

    // ── star helpers ─────────────────────────────────────────────────────
    function makeStar() {
      var base = Math.random() * 0.5 + 0.08; // 0.08 – 0.58
      return {
        x: Math.random() * W,
        y: Math.random() * H,
        r: Math.random() * 1.5 + 0.5,        // 0.5 – 2 px
        baseOpacity: base,
        twinkleOffset: Math.random() * Math.PI * 2,
        twinkleSpeed:  Math.random() * 0.008 + 0.003, // slow sine
        depth: Math.random()                  // 0-1 for parallax depth
      };
    }
    function initStars() {
      stars = [];
      for (var i = 0; i < STAR_COUNT; i++) stars.push(makeStar());
    }

    // ── shooting star helpers ─────────────────────────────────────────────
    function spawnShooter() {
      // Start from a random point along the top/left edges, streak diagonally
      var startX = Math.random() * W * 1.2 - W * 0.1;
      var startY = Math.random() * H * 0.4;
      var angle  = (Math.random() * 30 + 20) * Math.PI / 180; // 20-50°
      var length = Math.random() * 90 + 70;                    // 70-160 px
      shooters.push({
        x: startX, y: startY,
        dx: Math.cos(angle),
        dy: Math.sin(angle),
        length: length,
        speed: Math.random() * 4 + 5,   // px per frame
        life: 0,                          // 0 → 1
        lifeRate: 1 / (Math.random() * 18 + 22) // total frame duration ≈ 22-40 frames
      });
    }
    function scheduleNextShooter(now) {
      // fire next one in 3–6 seconds
      nextShooterAt = now + 3000 + Math.random() * 3000;
    }

    // ── draw helpers ─────────────────────────────────────────────────────
    function drawGrid() {
      var step = 50;
      ctx.strokeStyle = 'rgba(124,58,237,0.06)';
      ctx.lineWidth = 1;
      for (var x = 0; x < W; x += step) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
      }
      for (var y = 0; y < H; y += step) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
      }
    }

    function drawConnections() {
      var DIST = 120;
      for (var i = 0; i < particles.length; i++) {
        for (var j = i + 1; j < particles.length; j++) {
          var dx   = particles[i].x - particles[j].x;
          var dy   = particles[i].y - particles[j].y;
          var dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < DIST) {
            var alpha = (1 - dist / DIST) * 0.15;
            ctx.strokeStyle = 'rgba(124,58,237,' + alpha + ')';
            ctx.lineWidth = 0.8;
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.stroke();
          }
        }
      }
    }

    function drawStars(tick) {
      var px = parallaxX, py = parallaxY;
      for (var i = 0; i < stars.length; i++) {
        var s = stars[i];
        // Twinkle: sine wave on opacity
        var opacity = s.baseOpacity * (0.35 + 0.65 *
          (0.5 + 0.5 * Math.sin(tick * s.twinkleSpeed + s.twinkleOffset)));
        // Parallax offset — deeper stars shift more
        var ox = px * s.depth * MAX_SHIFT;
        var oy = py * s.depth * MAX_SHIFT;
        ctx.beginPath();
        ctx.arc(s.x + ox, s.y + oy, s.r, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(220,230,255,' + opacity + ')';
        ctx.fill();
      }
    }

    function drawShooters() {
      for (var i = shooters.length - 1; i >= 0; i--) {
        var sh = shooters[i];
        sh.life += sh.lifeRate;
        sh.x += sh.dx * sh.speed;
        sh.y += sh.dy * sh.speed;

        // fade: in during first 30%, out during last 30%
        var fade;
        if (sh.life < 0.3)      fade = sh.life / 0.3;
        else if (sh.life > 0.7) fade = (1 - sh.life) / 0.3;
        else                     fade = 1;
        fade = Math.max(0, Math.min(1, fade));

        var tailX = sh.x - sh.dx * sh.length;
        var tailY = sh.y - sh.dy * sh.length;

        var grad = ctx.createLinearGradient(tailX, tailY, sh.x, sh.y);
        grad.addColorStop(0, 'rgba(255,255,255,0)');
        grad.addColorStop(0.6, 'rgba(180,200,255,' + (fade * 0.35) + ')');
        grad.addColorStop(1,   'rgba(255,255,255,' + (fade * 0.9) + ')');

        ctx.beginPath();
        ctx.moveTo(tailX, tailY);
        ctx.lineTo(sh.x, sh.y);
        ctx.strokeStyle = grad;
        ctx.lineWidth = 1.5;
        ctx.stroke();

        // draw a small bright dot at the head
        ctx.beginPath();
        ctx.arc(sh.x, sh.y, 1.8, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(255,255,255,' + (fade * 0.9) + ')';
        ctx.fill();

        if (sh.life >= 1) shooters.splice(i, 1);
      }
    }

    // ── main animation loop ───────────────────────────────────────────────
    var tick = 0;
    function animate(now) {
      try {
        tick++;

        // ── ease parallax toward mouse target ──
        var targetX = (mouseX / W) - 0.5;  // -0.5 to 0.5
        var targetY = (mouseY / H) - 0.5;
        parallaxX += (targetX - parallaxX) * 0.05;
        parallaxY += (targetY - parallaxY) * 0.05;

        // ── clear ──
        ctx.clearRect(0, 0, W, H);

        // ── grid (subtle, stays fixed) ──
        drawGrid();

        // ── centre radial glow ──
        var grad = ctx.createRadialGradient(W/2, H/2, 0, W/2, H/2, Math.max(W,H)*0.7);
        grad.addColorStop(0, 'rgba(124,58,237,0.06)');
        grad.addColorStop(1, 'rgba(8,11,18,0)');
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, W, H);

        // ── stars (twinkle + parallax) ──
        drawStars(tick);

        // ── particle network ──
        drawConnections();
        for (var i = 0; i < particles.length; i++) {
          var p = particles[i];
          p.x += p.vx; p.y += p.vy;
          if (p.x < 0 || p.x > W || p.y < 0 || p.y > H) resetParticle(p);
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
          ctx.fillStyle = 'rgba(' + p.color + ',' + p.alpha + ')';
          ctx.fill();
        }

        // ── shooting stars ──
        if (now && now >= nextShooterAt) {
          spawnShooter();
          scheduleNextShooter(now);
        }
        drawShooters();

      } catch(e) {}
      rafId = requestAnimationFrame(animate);
    }

    // ── mouse tracking ────────────────────────────────────────────────────
    window.addEventListener('mousemove', function(e) {
      mouseX = e.clientX;
      mouseY = e.clientY;
    });

    // ── resize ────────────────────────────────────────────────────────────
    window.addEventListener('resize', function() {
      resize();
      initParticles();
      initStars();
    });

    // ── cleanup on page hide (memory safety) ─────────────────────────────
    document.addEventListener('visibilitychange', function() {
      if (document.hidden) {
        cancelAnimationFrame(rafId);
      } else {
        scheduleNextShooter(performance.now());
        rafId = requestAnimationFrame(animate);
      }
    });

    // ── boot ─────────────────────────────────────────────────────────────
    resize();
    initParticles();
    initStars();
    scheduleNextShooter(performance.now());
    rafId = requestAnimationFrame(animate);
  })();
} catch(e) {}


// ---- NAVBAR ------------------------------------------------------------
try {
  (function initNav() {
    var navbar = document.getElementById('navbar');
    var hamburger = document.getElementById('hamburger');
    var mobileMenu = document.getElementById('mobileMenu');
    if (!navbar || !hamburger || !mobileMenu) return;

    hamburger.setAttribute('aria-expanded', 'false');
    hamburger.setAttribute('aria-controls', 'mobileMenu');

    window.addEventListener('scroll', function() {
      if (window.scrollY > 50) {
        navbar.style.background = 'rgba(8,11,18,0.95)';
        navbar.style.boxShadow = '0 4px 30px rgba(0,0,0,0.4)';
      } else {
        navbar.style.background = 'rgba(8,11,18,0.8)';
        navbar.style.boxShadow = 'none';
      }
    });

    function openMobileMenu() {
      mobileMenu.classList.add('open');
      hamburger.setAttribute('aria-expanded', 'true');
      hamburger.setAttribute('aria-label', 'Close menu');
      var firstLink = mobileMenu.querySelector('.mobile-link');
      if (firstLink && typeof firstLink.focus === 'function') {
        firstLink.focus();
      }
    }

    function closeMobileMenu(returnFocus) {
      if (!mobileMenu.classList.contains('open')) return;
      mobileMenu.classList.remove('open');
      hamburger.setAttribute('aria-expanded', 'false');
      hamburger.setAttribute('aria-label', 'Open menu');
      if (returnFocus !== false && typeof hamburger.focus === 'function') {
        hamburger.focus();
      }
    }

    hamburger.addEventListener('click', function() {
      if (mobileMenu.classList.contains('open')) {
        closeMobileMenu(true);
      } else {
        openMobileMenu();
      }
    });

    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && mobileMenu.classList.contains('open')) {
        e.preventDefault();
        closeMobileMenu(true);
      }
    });

    // Navigation disclosure: clicking any navigation link closes the menu
    var mobileLinks = mobileMenu.querySelectorAll('.mobile-link');
    for (var i = 0; i < mobileLinks.length; i++) {
      mobileLinks[i].addEventListener('click', function() {
        closeMobileMenu(false);
      });
    }

    var sections = document.querySelectorAll('section[id]');
    var navLinks = document.querySelectorAll('.nav-links a');

    if (typeof IntersectionObserver !== 'undefined') {
      var navObserver = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
          if (entry.isIntersecting) {
            navLinks.forEach(function(l) { l.classList.remove('active'); });
            var active = document.querySelector('.nav-links a[href="#' + entry.target.id + '"]');
            if (active) active.classList.add('active');
          }
        });
      }, { threshold: 0.4 });
      sections.forEach(function(s) { navObserver.observe(s); });
    }
  })();
} catch(e) {}


// ---- SCROLL REVEAL -----------------------------------------------------
try {
  (function initReveal() {
    var reveals = document.querySelectorAll('.reveal');

    var heroReveals = document.querySelectorAll('#hero .reveal');
    for (var i = 0; i < heroReveals.length; i++) {
      heroReveals[i].classList.add('visible');
    }

    if (typeof IntersectionObserver !== 'undefined') {
      var observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.05, rootMargin: '0px 0px -10px 0px' });

      for (var i = 0; i < reveals.length; i++) {
        observer.observe(reveals[i]);
      }
    } else {
      for (var i = 0; i < reveals.length; i++) {
        reveals[i].classList.add('visible');
      }
    }

    setTimeout(function() {
      var hidden = document.querySelectorAll('.reveal:not(.visible)');
      for (var i = 0; i < hidden.length; i++) {
        hidden[i].classList.add('visible');
      }
    }, 1500);
  })();
} catch(e) {
  var reveals = document.querySelectorAll('.reveal');
  for (var i = 0; i < reveals.length; i++) {
    reveals[i].classList.add('visible');
  }
}


// ---- SKILL BARS (removed — skills are now pill tags) ------------------
// Skill bars replaced with grouped pill layout; no JS required.


// ---- CONTACT FORM (Formspree) ------------------------------------------
// To activate: set data-form-id="xyzabc" on the <form id="contactForm"> element.
// Get a free form ID at formspree.io → New Form.
try {
  (function initForm() {
    var form = document.getElementById('contactForm');
    var note = document.getElementById('formNote');
    var btn  = document.getElementById('formSubmit');
    if (!form) return;

    var formId = form.getAttribute('data-form-id') || '';
    var formConfigured = formId && formId.length > 4;

    if (!formConfigured) {
      // Show a graceful setup state — form is visible but submitting directs to email
      if (btn) {
        btn.textContent = 'Send via Email →';
        btn.addEventListener('click', function(e) {
          e.preventDefault();
          var name    = (document.getElementById('formName')    || {}).value || '';
          var subject = (document.getElementById('formSubject') || {}).value || 'Portfolio contact';
          var message = (document.getElementById('formMessage') || {}).value || '';
          var mailto  = 'mailto:josiahsaji2k03@gmail.com'
            + '?subject=' + encodeURIComponent(subject || 'Portfolio contact from ' + name)
            + '&body='    + encodeURIComponent(message);
          window.location.href = mailto;
        });
      }
      if (note) {
        note.textContent = 'Or email me directly: josiahsaji2k03@gmail.com';
        note.style.color = 'var(--text-dim)';
      }
      return;
    }

    var submitted = false;

    form.addEventListener('submit', function(e) {
      e.preventDefault();
      if (submitted) return; // prevent double-submit

      // Client-side validation
      var name    = (document.getElementById('formName')    || {}).value || '';
      var email   = (document.getElementById('formEmail')   || {}).value || '';
      var message = (document.getElementById('formMessage') || {}).value || '';
      var emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

      if (!name.trim()) {
        if (note) { note.textContent = 'Please enter your name.'; note.style.color = '#ef4444'; }
        document.getElementById('formName').focus();
        return;
      }
      if (!emailRe.test(email.trim())) {
        if (note) { note.textContent = 'Please enter a valid email address.'; note.style.color = '#ef4444'; }
        document.getElementById('formEmail').focus();
        return;
      }
      if (!message.trim()) {
        if (note) { note.textContent = 'Please enter a message.'; note.style.color = '#ef4444'; }
        document.getElementById('formMessage').focus();
        return;
      }

      btn.textContent = 'Sending\u2026';
      btn.disabled = true;
      if (note) { note.textContent = ''; note.style.color = ''; }

      fetch('https://formspree.io/f/' + formId, {
        method: 'POST',
        body: new FormData(form),
        headers: { 'Accept': 'application/json' }
      })
      .then(function(res) {
        if (res.ok) {
          submitted = true;
          if (note) { note.textContent = '\u2713 Message sent! I will get back to you soon.'; note.style.color = '#22c55e'; }
          form.reset();
        } else {
          return res.json().then(function(data) {
            throw new Error((data.errors || []).map(function(e) { return e.message; }).join(', ') || 'Submission failed.');
          });
        }
      })
      .catch(function(err) {
        if (note) {
          note.textContent = 'Could not send \u2014 ' + err.message + ' Try emailing me directly at josiahsaji2k03@gmail.com';
          note.style.color = '#ef4444';
        }
      })
      ['finally'](function() {
        if (!submitted) {
          btn.textContent = 'Send Message \u2192';
          btn.disabled = false;
        }
      });
    });
  })();
} catch(e) {}


// ---- IMAGE CAROUSELS ---------------------------------------------------
try {
  (function initCarousels() {
    var carousels = document.querySelectorAll('[data-carousel]');
    for (var ci = 0; ci < carousels.length; ci++) {
      (function(carousel) {
        var track       = carousel.querySelector('.carousel-track');
        var items       = track ? track.querySelectorAll('figure') : [];
        var placeholder = carousel.querySelector('.carousel-placeholder');
        var prevBtn     = carousel.querySelector('.carousel-prev');
        var nextBtn     = carousel.querySelector('.carousel-next');

        carousel.setAttribute('role', 'region');
        carousel.setAttribute('aria-roledescription', 'carousel');
        carousel.setAttribute('aria-label', 'Project Media Showcase');

        if (!items.length) {
          // No images — show placeholder, hide arrow buttons
          if (placeholder) placeholder.style.display = 'flex';
          if (prevBtn) prevBtn.style.display = 'none';
          if (nextBtn) nextBtn.style.display = 'none';
          return;
        }

        // Has images — hide placeholder, show arrows
        if (placeholder) placeholder.style.display = 'none';
        if (prevBtn) prevBtn.style.display = '';
        if (nextBtn) nextBtn.style.display = '';

        // Graceful broken image handler to prevent layout shift
        var imgs = track ? track.querySelectorAll('img') : [];
        for (var mi = 0; mi < imgs.length; mi++) {
          (function(img) {
            img.addEventListener('error', function() {
              this.style.display = 'none';
              var fig = this.closest('figure');
              if (fig && !fig.querySelector('.media-err-notice')) {
                var errNotice = document.createElement('div');
                errNotice.className = 'media-err-notice';
                errNotice.style.cssText = 'padding:32px 16px;text-align:center;color:var(--text-dim);font-family:var(--font-mono);font-size:0.75rem;background:var(--surface2);';
                errNotice.innerHTML = '<span>⚙️</span><p style="margin-top:6px;">Media pending verification</p><code style="color:var(--accent2);">' + (img.getAttribute('src') || '') + '</code>';
                fig.insertBefore(errNotice, fig.firstChild);
              }
            });
          })(imgs[mi]);
        }

        var current = 0;
        var total   = items.length;

        function goTo(idx) {
          current = (idx + total) % total;
          if (track) track.style.transform = 'translateX(-' + (current * 100) + '%)';
          for (var i = 0; i < items.length; i++) {
            items[i].setAttribute('aria-hidden', String(i !== current));
          }
        }

        if (prevBtn) {
          prevBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            goTo(current - 1);
          });
        }
        if (nextBtn) {
          nextBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            goTo(current + 1);
          });
        }

        // Touch / swipe
        var swipeStartX = 0;
        if (track) {
          track.addEventListener('touchstart', function(e) {
            swipeStartX = e.touches[0].clientX;
          }, { passive: true });
          track.addEventListener('touchend', function(e) {
            var diff = swipeStartX - e.changedTouches[0].clientX;
            if (Math.abs(diff) > 50) goTo(diff > 0 ? current + 1 : current - 1);
          }, { passive: true });
        }

        // Keyboard navigation when carousel is focused
        carousel.setAttribute('tabindex', '0');
        carousel.addEventListener('keydown', function(e) {
          if (e.key === 'ArrowLeft') { e.preventDefault(); goTo(current - 1); }
          if (e.key === 'ArrowRight') { e.preventDefault(); goTo(current + 1); }
        });

        goTo(0);
      })(carousels[ci]);
    }
  })();
} catch(e) {}


// ---- PROJECT CARDS (clean industrial hover handled via CSS) -----------



// ---- NAV ACTIVE STYLE --------------------------------------------------
try {
  var s = document.createElement('style');
  s.textContent = '.nav-links a.active{color:#fff!important}.nav-links a.active::after{transform:scaleX(1)!important}';
  document.head.appendChild(s);
} catch(e) {}


// ---- RESUME AVAILABILITY CHECK -----------------------------------------
// Shows resume download buttons only if the PDF actually exists (avoids 404 downloads).
try {
  (function checkResume() {
    var resumePath = 'assets/resume/resume.pdf';
    fetch(resumePath, { method: 'HEAD' })
      .then(function(res) {
        if (res.ok) {
          var ids = ['heroResume', 'navResumeBtn', 'mobileResumeBtn'];
          ids.forEach(function(id) {
            var el = document.getElementById(id);
            if (el) el.style.display = '';
          });
        }
        // If 404, buttons stay hidden — no broken download link presented to visitor
      })
      .catch(function() { /* network error: leave buttons hidden */ });
  })();
} catch(e) {}


// ---- HERO STAGE INTERACTIVE TELEMETRY -----------------------------------
try {
  (function initHeroStage() {
    var stage = document.getElementById('heroStage');
    if (!stage) return;

    var chips = stage.querySelectorAll('.telem-chip');
    var sweepBeam = document.getElementById('radarSweepBeam');
    var pointCloud = document.getElementById('pointCloudGroup');
    var robotChassis = document.getElementById('robotChassis');

    chips.forEach(function(chip) {
      chip.setAttribute('tabindex', '0');
      chip.setAttribute('role', 'button');
      chip.setAttribute('aria-pressed', chip.classList.contains('active') ? 'true' : 'false');

      function activate() {
        chips.forEach(function(c) {
          c.classList.remove('active');
          c.setAttribute('aria-pressed', 'false');
        });
        chip.classList.add('active');
        chip.setAttribute('aria-pressed', 'true');

        if (chip.id === 'telemLidar') {
          if (sweepBeam) sweepBeam.style.filter = 'drop-shadow(0 0 8px #00d4ff)';
          if (pointCloud) pointCloud.style.opacity = '1';
        } else if (chip.id === 'telemOdom') {
          if (robotChassis) robotChassis.style.filter = 'drop-shadow(0 0 10px #8b5cf6)';
        } else if (chip.id === 'telemSlam') {
          if (pointCloud) pointCloud.style.opacity = '1';
        } else if (chip.id === 'telemNav') {
          if (robotChassis) robotChassis.style.filter = 'drop-shadow(0 0 10px #00d4ff)';
        }
      }

      chip.addEventListener('click', activate);
      chip.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          activate();
        }
      });
    });
  })();
} catch(e) {}


// ---- MAGNETIC BUTTONS --------------------------------------------------
try {
  (function initMagneticButtons() {
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    if (window.innerWidth < 768) return; // desktop only

    var btns = document.querySelectorAll('.btn-primary, .btn-resume');
    btns.forEach(function(btn) {
      btn.addEventListener('mousemove', function(e) {
        var rect = btn.getBoundingClientRect();
        var x = e.clientX - rect.left - rect.width / 2;
        var y = e.clientY - rect.top - rect.height / 2;
        btn.style.transform = 'translate(' + (x * 0.18) + 'px, ' + (y * 0.18) + 'px)';
      });
      btn.addEventListener('mouseleave', function() {
        btn.style.transform = '';
      });
    });
  })();
} catch(e) {}


// ---- REDUCED MOTION SUPPORT --------------------------------------------
// Disable non-essential animations for users who prefer reduced motion.
try {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var rm = document.createElement('style');
    rm.textContent = [
      '.reveal { transition: none !important; opacity: 1 !important; transform: none !important; }',
      '.reveal.visible { transition: none !important; }',
      '.avatar-ring { animation: none !important; }',
      '.badge-dot { animation: none !important; }',
      '.scroll-line { animation: none !important; }',
      '.lidar-sweep-group { animation: none !important; }',
      '#heroCanvas { display: none !important; }',
    ].join('');
    document.head.appendChild(rm);
  }
} catch(e) {}

