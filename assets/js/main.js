/*!
 * Mais Vida - Clínica Popular da Família
 * JS do site estático: menu mobile, carrossel do topo, slideshows de fundo,
 * sombra do header e aviso de cookies. Sem dependências externas.
 */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ------------------------------ Menu mobile ----------------------------- */
  var toggle = document.getElementById('nav-toggle');
  var nav = document.getElementById('main-nav');

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
    });

    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        nav.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) {
        nav.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
      }
    });
  }

  /* --------------------------- Sombra do header --------------------------- */
  var header = document.getElementById('site-header');
  if (header) {
    var onScroll = function () {
      header.classList.toggle('is-stuck', window.scrollY > 8);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ------------------------------- Carrossel ------------------------------ */
  var track = document.getElementById('hero-track');

  if (track) {
    var slides = Array.prototype.slice.call(track.querySelectorAll('.slide'));
    var dotsBox = document.getElementById('hero-dots');
    var prev = document.getElementById('hero-prev');
    var next = document.getElementById('hero-next');
    var index = 0;
    var timer = null;
    var DELAY = 5000;

    var dots = slides.map(function (slide, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.setAttribute('role', 'tab');
      b.setAttribute('aria-label', 'Ir para o slide ' + (i + 1));
      b.addEventListener('click', function () {
        go(i);
        restart();
      });
      if (dotsBox) dotsBox.appendChild(b);
      return b;
    });

    function go(i) {
      index = (i + slides.length) % slides.length;
      slides.forEach(function (s, n) {
        s.classList.toggle('is-active', n === index);
        s.setAttribute('aria-hidden', String(n !== index));
      });
      dots.forEach(function (d, n) {
        d.classList.toggle('is-active', n === index);
        d.setAttribute('aria-selected', String(n === index));
      });
    }

    function start() {
      if (reduceMotion || slides.length < 2) return;
      timer = window.setInterval(function () { go(index + 1); }, DELAY);
    }
    function stop() {
      if (timer) { window.clearInterval(timer); timer = null; }
    }
    function restart() { stop(); start(); }

    if (prev) prev.addEventListener('click', function () { go(index - 1); restart(); });
    if (next) next.addEventListener('click', function () { go(index + 1); restart(); });

    track.addEventListener('mouseenter', stop);
    track.addEventListener('mouseleave', start);
    track.addEventListener('focusin', stop);

    document.addEventListener('visibilitychange', function () {
      if (document.hidden) { stop(); } else { restart(); }
    });

    // Navegação por toque (swipe)
    var startX = null;
    track.addEventListener('touchstart', function (e) {
      startX = e.changedTouches[0].clientX;
      stop();
    }, { passive: true });
    track.addEventListener('touchend', function (e) {
      if (startX === null) return;
      var dx = e.changedTouches[0].clientX - startX;
      if (Math.abs(dx) > 45) go(dx < 0 ? index + 1 : index - 1);
      startX = null;
      start();
    }, { passive: true });

    go(0);
    start();
  }

  /* --------------------- Slideshows de fundo (fade) ----------------------- */
  Array.prototype.forEach.call(document.querySelectorAll('[data-slideshow]'), function (box) {
    var images;
    try {
      images = JSON.parse(box.getAttribute('data-images') || '[]');
    } catch (err) {
      images = [];
    }
    if (!images.length) return;

    box.style.backgroundImage = 'url("' + images[0] + '")';
    if (images.length < 2 || reduceMotion) return;

    // Pré-carrega para evitar "piscada" na primeira troca
    images.slice(1).forEach(function (src) { new Image().src = src; });

    var i = 0;
    var interval = parseInt(box.getAttribute('data-interval'), 10) || 5000;
    window.setInterval(function () {
      i = (i + 1) % images.length;
      box.style.backgroundImage = 'url("' + images[i] + '")';
    }, interval);
  });

  /* ------------------------- Avaliações do Google -------------------------- */

  // Data relativa ("há 2 meses"). Sem JS, fica a data absoluta que está no HTML.
  var rtf = null;
  try {
    rtf = new Intl.RelativeTimeFormat('pt-BR', { numeric: 'auto' });
  } catch (err) { rtf = null; }

  if (rtf) {
    Array.prototype.forEach.call(document.querySelectorAll('.review__date[datetime]'), function (el) {
      var d = new Date(el.getAttribute('datetime'));
      if (isNaN(d)) return;
      var dias = Math.round((d - Date.now()) / 86400000);
      var texto;
      if (dias > -30) {
        texto = rtf.format(Math.min(dias, -1), 'day');
      } else if (dias > -365) {
        texto = rtf.format(Math.round(dias / 30), 'month');
      } else {
        texto = rtf.format(Math.round(dias / 365), 'year');
      }
      el.textContent = texto;
    });
  }

  // "Leia mais" só aparece quando o texto realmente foi cortado
  Array.prototype.forEach.call(document.querySelectorAll('.review'), function (card) {
    var texto = card.querySelector('.review__text');
    var botao = card.querySelector('.review__more');
    if (!texto || !botao) return;

    if (texto.scrollHeight - texto.clientHeight > 4) botao.hidden = false;

    botao.addEventListener('click', function () {
      var aberto = texto.classList.toggle('is-expanded');
      botao.textContent = aberto ? 'Esconder' : 'Leia mais';
    });
  });

  /* ---------------------------- Aviso de cookies -------------------------- */
  var bar = document.getElementById('cookie-bar');
  var accept = document.getElementById('cookie-accept');
  var KEY = 'mv_cookie_consent';

  if (bar && accept) {
    var stored = null;
    try { stored = window.localStorage.getItem(KEY); } catch (err) { stored = 'skip'; }

    // display inline garante o sumiço mesmo se um CSS antigo estiver em cache
    function hideBar() {
      bar.hidden = true;
      bar.style.display = 'none';
      document.body.classList.remove('cookie-open');
    }
    function showBar() {
      bar.hidden = false;
      bar.style.display = '';
      document.body.classList.add('cookie-open');
    }

    if (stored) { hideBar(); } else { showBar(); }

    accept.addEventListener('click', function () {
      try { window.localStorage.setItem(KEY, 'accepted'); } catch (err) { /* modo privado */ }
      hideBar();
    });
  }
})();
