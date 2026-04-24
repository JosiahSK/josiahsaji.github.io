/* ======================================
   Josiah Saji Portfolio – script.js
   ====================================== */

// ── HERO CANVAS (Animated Grid + Particles) ──────────────────────────
(function initCanvas() {
  const canvas = document.getElementById('heroCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let W, H, particles = [];
  const PARTICLE_COUNT = 60;

  function resize() {
    W = canvas.width = canvas.offsetWidth;
    H = canvas.height = canvas.offsetHeight;
  }

  function Particle() {
    this.reset();
  }
  Particle.prototype.reset = function () {
    this.x = Math.random() * W;
    this.y = Math.random() * H;
    this.r = Math.random() * 1.5 + 0.5;
    this.vx = (Math.random() - 0.5) * 0.4;
    this.vy = (Math.random() - 0.5) * 0.4;
    this.alpha = Math.random() * 0.5 + 0.1;
    this.color = Math.random() > 0.5 ? '124,58,237' : '6,182,212';
  };
  Particle.prototype.update = function () {
    this.x += this.vx;
    this.y += this.vy;
    if (this.x < 0 || this.x > W || this.y < 0 || this.y > H) this.reset();
  };

  function initParticles() {
    particles = [];
    for (let i = 0; i < PARTICLE_COUNT; i++) particles.push(new Particle());
  }

  function drawGrid() {
    const step = 50;
    ctx.strokeStyle = 'rgba(124,58,237,0.06)';
    ctx.lineWidth = 1;
    for (let x = 0; x < W; x += step) {
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
    }
    for (let y = 0; y < H; y += step) {
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
    }
  }

  function drawConnections() {
    const CONNECT_DIST = 120;
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < CONNECT_DIST) {
          const alpha = (1 - dist / CONNECT_DIST) * 0.15;
          ctx.strokeStyle = `rgba(124,58,237,${alpha})`;
          ctx.lineWidth = 0.8;
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.stroke();
        }
      }
    }
  }

  function animate() {
    ctx.clearRect(0, 0, W, H);
    drawGrid();

    // Radial gradient overlay
    const grad = ctx.createRadialGradient(W / 2, H / 2, 0, W / 2, H / 2, Math.max(W, H) * 0.7);
    grad.addColorStop(0, 'rgba(124,58,237,0.06)');
    grad.addColorStop(1, 'rgba(8,11,18,0)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, W, H);

    drawConnections();

    particles.forEach(p => {
      p.update();
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${p.color},${p.alpha})`;
      ctx.fill();
    });

    requestAnimationFrame(animate);
  }

  window.addEventListener('resize', () => { resize(); initParticles(); });
  resize();
  initParticles();
  animate();
})();


// ── NAVBAR ────────────────────────────────────────────────────────────
(function initNav() {
  const navbar = document.getElementById('navbar');
  const hamburger = document.getElementById('hamburger');
  const mobileMenu = document.getElementById('mobileMenu');

  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      navbar.style.background = 'rgba(8,11,18,0.95)';
      navbar.style.boxShadow = '0 4px 30px rgba(0,0,0,0.4)';
    } else {
      navbar.style.background = 'rgba(8,11,18,0.8)';
      navbar.style.boxShadow = 'none';
    }
  });

  hamburger.addEventListener('click', () => {
    mobileMenu.classList.toggle('open');
  });

  document.querySelectorAll('.mobile-link').forEach(link => {
    link.addEventListener('click', () => mobileMenu.classList.remove('open'));
  });

  // Active link highlight
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-links a');

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        navLinks.forEach(l => l.classList.remove('active'));
        const active = document.querySelector(`.nav-links a[href="#${entry.target.id}"]`);
        if (active) active.classList.add('active');
      }
    });
  }, { threshold: 0.4 });

  sections.forEach(s => observer.observe(s));
})();


// ── SCROLL REVEAL ────────────────────────────────────────────────────
(function initReveal() {
  const reveals = document.querySelectorAll('.reveal');

  const observer = new IntersectionObserver(entries => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        // Stagger children of the same parent
        setTimeout(() => {
          entry.target.classList.add('visible');
        }, 80);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  reveals.forEach(el => observer.observe(el));
})();


// ── SKILL BARS ────────────────────────────────────────────────────────
(function initSkillBars() {
  const fills = document.querySelectorAll('.skill-fill');

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const width = el.getAttribute('data-width') || '0';
        el.style.width = width + '%';
        observer.unobserve(el);
      }
    });
  }, { threshold: 0.3 });

  fills.forEach(f => observer.observe(f));
})();


// ── CONTACT FORM ──────────────────────────────────────────────────────
(function initForm() {
  const form = document.getElementById('contactForm');
  const note = document.getElementById('formNote');
  if (!form) return;

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    const btn = document.getElementById('formSubmit');
    btn.textContent = 'Sending…';
    btn.disabled = true;

    setTimeout(() => {
      note.textContent = '✓ Message received! I'll get back to you soon.';
      note.style.color = '#22c55e';
      form.reset();
      btn.textContent = 'Send Message →';
      btn.disabled = false;
    }, 1400);
  });
})();


// ── SMOOTH TILT ON PROJECT CARDS ──────────────────────────────────────
(function initTilt() {
  document.querySelectorAll('.project-card').forEach(card => {
    card.addEventListener('mousemove', e => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const cx = rect.width / 2;
      const cy = rect.height / 2;
      const rotX = ((y - cy) / cy) * -6;
      const rotY = ((x - cx) / cx) * 6;
      card.style.transform = `translateY(-8px) perspective(600px) rotateX(${rotX}deg) rotateY(${rotY}deg)`;
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
    });
  });
})();


// ── NAV ACTIVE STYLE ─────────────────────────────────────────────────
const style = document.createElement('style');
style.textContent = `.nav-links a.active { color: #fff !important; }
.nav-links a.active::after { transform: scaleX(1) !important; }`;
document.head.appendChild(style);
