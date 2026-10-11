(function () {
  var d = document;
  d.documentElement.classList.add('js');

  d.querySelectorAll('[data-i]').forEach(function (el) {
    var name = el.getAttribute('data-i');
    el.outerHTML = '<span class="i icon icon-' + name + '" aria-hidden="true"></span>';
  });
  d.querySelectorAll('a[target="_blank"]').forEach(function (a) {
    a.insertAdjacentHTML('beforeend', '<span class="sr"> (nouvel onglet)</span>');
  });
  d.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
  var backButton = d.querySelector('[data-back]');
  if (backButton && window.history.length > 1) {
    backButton.hidden = false;
    backButton.addEventListener('click', function () {
      window.history.back();
    });
  }
  var pathNode = d.querySelector('[data-path]');
  if (pathNode) {
    pathNode.textContent = location.pathname;
    pathNode.parentNode.hidden = false;
  }
  if (d.querySelector('base')) {
    d.querySelectorAll('a[href^="#"]').forEach(function (a) {
      a.setAttribute('href', location.pathname + location.search + a.getAttribute('href'));
    });
  }
  var btn = d.querySelector('.toggle'), menu = d.getElementById('menu');
  if (btn && menu) {
    btn.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }
})();
