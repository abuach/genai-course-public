// Theme toggle (remembered per browser) and nav highlighting. No tracking.
(function () {
  var root = document.documentElement, btn = document.querySelector('.theme');
  try { var saved = localStorage.getItem('cs238-theme'); if (saved) root.setAttribute('data-theme', saved); } catch (e) {}
  if (btn) btn.addEventListener('click', function () {
    var dark = root.getAttribute('data-theme') === 'dark' ||
      (!root.getAttribute('data-theme') && window.matchMedia('(prefers-color-scheme: dark)').matches);
    var next = dark ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('cs238-theme', next); } catch (e) {}
  });
  var links = Array.prototype.slice.call(document.querySelectorAll('.nav ul a'));
  var sections = links.map(function (a) { return document.querySelector(a.getAttribute('href')); });
  function highlight() {
    var y = window.scrollY + 90, current = null;
    sections.forEach(function (s, i) { if (s && s.offsetTop <= y) current = i; });
    links.forEach(function (a, i) { a.classList.toggle('active', i === current); });
  }
  window.addEventListener('scroll', highlight, { passive: true }); highlight();
})();
