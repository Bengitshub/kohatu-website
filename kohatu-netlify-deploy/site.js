/* Kohatu MC — shared behaviour for all pages */
(function () {
  'use strict';

  // sticky nav shading
  var nav = document.getElementById('nav');
  if (nav) {
    var onScroll = function () { nav.classList.toggle('scrolled', window.scrollY > 24); };
    addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // mobile menu
  var toggle = document.querySelector('.nav-toggle');
  var links = document.getElementById('nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      toggle.setAttribute('aria-expanded', links.classList.toggle('open'));
    });
    links.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { links.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); }
    });
  }

  // event filters (rides grid)
  var chips = document.querySelectorAll('.chip');
  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      chips.forEach(function (c) { c.setAttribute('aria-pressed', 'false'); });
      chip.setAttribute('aria-pressed', 'true');
      var f = chip.dataset.filter;
      document.querySelectorAll('.event-card').forEach(function (card) {
        card.style.display = (f === 'all' || card.dataset.cat === f) ? '' : 'none';
      });
    });
  });

  // scroll reveals
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { threshold: 0.12 });
    document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
  }

  // dialogs: [data-open="dialog-id"] opens, [data-close] closes, backdrop click closes
  document.querySelectorAll('[data-open]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var d = document.getElementById(btn.dataset.open);
      if (d) d.showModal();
    });
  });
  document.querySelectorAll('dialog').forEach(function (d) {
    d.addEventListener('click', function (e) { if (e.target === d) d.close(); });
    d.querySelectorAll('[data-close]').forEach(function (b) {
      b.addEventListener('click', function () { d.close(); });
    });
  });

  // DEMO ONLY: intercept forms so no data is collected. Remove at go-live.
  document.querySelectorAll('form.js-demo-form').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      form.reset();
      var d = document.getElementById(form.dataset.dialog);
      if (d) d.showModal();
    });
  });

  // lite YouTube embeds: load the iframe only on click
  document.querySelectorAll('.yt-lite').forEach(function (el) {
    el.addEventListener('click', function () {
      var id = el.dataset.id;
      var iframe = document.createElement('iframe');
      iframe.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0';
      iframe.title = el.dataset.title || 'Video';
      iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
      iframe.allowFullscreen = true;
      el.replaceChildren(iframe);
      el.classList.add('playing');
    }, { once: true });
  });

  // concept-preview bar dismiss
  var bar = document.getElementById('concept-bar');
  var barX = document.getElementById('concept-bar-close');
  if (bar && barX) barX.addEventListener('click', function () { bar.remove(); });

  var yr = document.getElementById('yr');
  if (yr) yr.textContent = new Date().getFullYear();
})();
