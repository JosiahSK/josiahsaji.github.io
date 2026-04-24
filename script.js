/* ======================================
   Josiah Saji Portfolio - script.js
   ====================================== */

// ---- HERO CANVAS -------------------------------------------------------
try {
  (function initCanvas() {
    var canvas = document.getElementById('heroCanvas');
    if (!canvas) return;
    var ctx = canvas.getContext('2d');
    var W, H, particles = [];
    var PARTICLE_COUNT = 55;

    function resize() {
      W = canvas.width = window.innerWidth;
      H = canvas.height = window.innerHeight;
    }

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
          var dx = particles[i].x - particles[j].x;
          var dy = particles[i].y - particles[j].y;
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

    function animate() {
      try {
        ctx.clearRect(0, 0, W, H);
        drawGrid();
        var grad = ctx.createRadialGradient(W/2, H/2, 0, W/2, H/2, Math.max(W,H)*0.7);
        grad.addColorStop(0, 'rgba(124,58,237,0.06)');
        grad.addColorStop(1, 'rgba(8,11,18,0)');
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, W, H);
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
      } catch(e) {}
      requestAnimationFrame(animate);
    }

    window.addEventListener('resize', function() { resize(); initParticles(); });
    resize();
    initParticles();
    animate();
  })();
} catch(e) {}


// ---- NAVBAR ------------------------------------------------------------
try {
  (function initNav() {
    var navbar = document.getElementById('navbar');
    var hamburger = document.getElementById('hamburger');
    var mobileMenu = document.getElementById('mobileMenu');
    if (!navbar || !hamburger || !mobileMenu) return;

    window.addEventListener('scroll', function() {
      if (window.scrollY > 50) {
        navbar.style.background = 'rgba(8,11,18,0.95)';
        navbar.style.boxShadow = '0 4px 30px rgba(0,0,0,0.4)';
      } else {
        navbar.style.background = 'rgba(8,11,18,0.8)';
        navbar.style.boxShadow = 'none';
      }
    });

    hamburger.addEventListener('click', function() {
      mobileMenu.classList.toggle('open');
    });

    var mobileLinks = document.querySelectorAll('.mobile-link');
    for (var i = 0; i < mobileLinks.length; i++) {
      mobileLinks[i].addEventListener('click', function() {
        mobileMenu.classList.remove('open');
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


// ---- SKILL BARS --------------------------------------------------------
try {
  (function initSkillBars() {
    var fills = document.querySelectorAll('.skill-fill');
    if (typeof IntersectionObserver === 'undefined') {
      for (var i = 0; i < fills.length; i++) {
        fills[i].style.width = (fills[i].getAttribute('data-width') || '0') + '%';
      }
      return;
    }
    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.style.width = (entry.target.getAttribute('data-width') || '0') + '%';
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.2 });
    for (var i = 0; i < fills.length; i++) observer.observe(fills[i]);
  })();
} catch(e) {}


// ---- CONTACT FORM ------------------------------------------------------
try {
  (function initForm() {
    var form = document.getElementById('contactForm');
    var note = document.getElementById('formNote');
    if (!form) return;
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      var btn = document.getElementById('formSubmit');
      btn.textContent = 'Sending...';
      btn.disabled = true;
      setTimeout(function() {
        if (note) { note.textContent = 'Message received! I will get back to you soon.'; note.style.color = '#22c55e'; }
        form.reset();
        btn.textContent = 'Send Message';
        btn.disabled = false;
      }, 1400);
    });
  })();
} catch(e) {}


// ---- TILT ON PROJECT CARDS (desktop only) ------------------------------
try {
  if (window.matchMedia('(hover: hover)').matches) {
    var cards = document.querySelectorAll('.project-card');
    for (var i = 0; i < cards.length; i++) {
      (function(card) {
        card.addEventListener('mousemove', function(e) {
          var rect = card.getBoundingClientRect();
          var rotX = (((e.clientY - rect.top) / rect.height) - 0.5) * -10;
          var rotY = (((e.clientX - rect.left) / rect.width) - 0.5) * 10;
          card.style.transform = 'translateY(-8px) perspective(600px) rotateX(' + rotX + 'deg) rotateY(' + rotY + 'deg)';
        });
        card.addEventListener('mouseleave', function() { card.style.transform = ''; });
      })(cards[i]);
    }
  }
} catch(e) {}


// ---- NAV ACTIVE STYLE --------------------------------------------------
try {
  var s = document.createElement('style');
  s.textContent = '.nav-links a.active{color:#fff!important}.nav-links a.active::after{transform:scaleX(1)!important}';
  document.head.appendChild(s);
} catch(e) {}
