/* Catboing — scripts propios (vanilla, sin librerías) */
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function initReveal() {
    var els = document.querySelectorAll('.cb-reveal:not(.cb-visible)');
    if (!els.length) return;
    if (reduce || !('IntersectionObserver' in window)) {
      els.forEach(function (el) { el.classList.add('cb-visible'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('cb-visible'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    els.forEach(function (el) { io.observe(el); });
  }

  function initParallax() {
    var imgs = document.querySelectorAll('[data-cb-parallax]');
    if (!imgs.length || reduce) return;
    var ticking = false;
    function update() {
      imgs.forEach(function (wrap) {
        var img = wrap.querySelector('img');
        if (!img) return;
        var k = parseFloat(wrap.getAttribute('data-cb-parallax')) || 0;
        var r = wrap.getBoundingClientRect();
        if (r.bottom < 0 || r.top > window.innerHeight) return;
        img.style.transform = 'translate3d(0,' + (r.top * -k / 100).toFixed(1) + 'px,0) scale(1.08)';
      });
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { window.requestAnimationFrame(update); ticking = true; }
    }, { passive: true });
    update();
  }

  function formatMoney(cents, format) {
    var value = (cents / 100).toFixed(2);
    var parts = value.split('.');
    var comma = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.') + ',' + parts[1];
    var dot = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',') + '.' + parts[1];
    var noDec = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    return (format || '${{amount}}')
      .replace(/\{\{\s*amount_with_comma_separator\s*\}\}/, comma)
      .replace(/\{\{\s*amount_no_decimals\s*\}\}/, noDec)
      .replace(/\{\{\s*amount_no_decimals_with_comma_separator\s*\}\}/, parts[0])
      .replace(/\{\{\s*amount\s*\}\}/, dot);
  }

  function initProducto() {
    document.querySelectorAll('[data-cb-producto]').forEach(function (root) {
      // Galería
      var main = root.querySelector('[data-cb-main-img]');
      var thumbs = root.querySelectorAll('[data-cb-thumb]');
      function showThumb(t) {
        if (!t || !main) return;
        thumbs.forEach(function (x) { x.setAttribute('aria-current', 'false'); });
        t.setAttribute('aria-current', 'true');
        main.style.opacity = '0';
        setTimeout(function () {
          main.src = t.getAttribute('data-src');
          if (t.getAttribute('data-srcset')) main.srcset = t.getAttribute('data-srcset');
          main.alt = t.getAttribute('data-alt') || '';
          main.style.opacity = '1';
        }, 160);
      }
      thumbs.forEach(function (t) { t.addEventListener('click', function () { showThumb(t); }); });

      // Cantidad
      var qty = root.querySelector('[data-cb-qty]');
      root.querySelectorAll('[data-cb-qty-btn]').forEach(function (b) {
        b.addEventListener('click', function () {
          var v = parseInt(qty.value, 10) || 1;
          v += parseInt(b.getAttribute('data-cb-qty-btn'), 10);
          qty.value = Math.max(1, v);
        });
      });

      // Variantes
      var dataEl = root.querySelector('[data-cb-variants]');
      if (!dataEl) return;
      var variants = JSON.parse(dataEl.textContent);
      var moneyFormat = root.getAttribute('data-money-format');
      var idInput = root.querySelector('input[name="id"]');
      var btns = document.querySelectorAll('[data-cb-add]');
      var priceNow = document.querySelectorAll('[data-cb-price]');
      var priceOld = document.querySelectorAll('[data-cb-compare]');
      var addLabel = root.getAttribute('data-add-label');
      var soldLabel = root.getAttribute('data-sold-label');
      var fieldsets = root.querySelectorAll('[data-cb-option]');
      if (!fieldsets.length) return;

      function selected() {
        return Array.prototype.map.call(fieldsets, function (fs) {
          var c = fs.querySelector('input:checked');
          return c ? c.value : null;
        });
      }
      function update() {
        var opts = selected();
        var v = variants.find(function (x) {
          return x.options.every(function (o, i) { return o === opts[i]; });
        });
        btns.forEach(function (b) {
          b.disabled = !v || !v.available;
          var lbl = b.querySelector('[data-cb-add-label]');
          if (lbl) lbl.textContent = (v && v.available) ? addLabel : soldLabel;
        });
        if (!v) return;
        idInput.value = v.id;
        priceNow.forEach(function (p) { p.textContent = formatMoney(v.price, moneyFormat); });
        priceOld.forEach(function (p) {
          var show = v.compare_at_price && v.compare_at_price > v.price;
          p.textContent = show ? formatMoney(v.compare_at_price, moneyFormat) : '';
          p.hidden = !show;
        });
        if (v.featured_media_id) {
          var t = root.querySelector('[data-cb-thumb][data-media-id="' + v.featured_media_id + '"]');
          if (t) showThumb(t);
        }
        var url = new URL(window.location.href);
        url.searchParams.set('variant', v.id);
        window.history.replaceState({}, '', url.toString());
      }
      fieldsets.forEach(function (fs) { fs.addEventListener('change', update); });
    });
  }

  function initStickyAtc() {
    var bar = document.querySelector('[data-cb-sticky]');
    var zone = document.querySelector('[data-cb-buy-zone]');
    var mainBtn = zone && zone.querySelector('form [data-cb-add]');
    if (!bar || !mainBtn) return;
    // Se muestra solo cuando el botón principal ya ha quedado por encima de la pantalla.
    // (Comprobación en cada scroll: un IntersectionObserver no avisa si se salta el botón de golpe)
    var ticking = false;
    function check() {
      // Visible siempre que el botón principal no esté en pantalla (ni antes de llegar a él ni después)
      var r = mainBtn.getBoundingClientRect();
      bar.classList.toggle('cb-mostrar', r.bottom < 0 || r.top > window.innerHeight);
      ticking = false;
    }
    if (!bar.dataset.cbScroll) {
      bar.dataset.cbScroll = '1';
      window.addEventListener('scroll', function () {
        if (!ticking) { ticking = true; window.requestAnimationFrame(check); }
      }, { passive: true });
    }
    check();
    var stickyBtn = bar.querySelector('[data-cb-sticky-submit]');
    if (stickyBtn && !stickyBtn.dataset.cbBound) {
      stickyBtn.dataset.cbBound = '1';
      stickyBtn.addEventListener('click', function (ev) { ev.preventDefault(); mainBtn.click(); });
    }
  }

  function init() {
    initReveal();
    initParallax();
    initProducto();
    initStickyAtc();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
  document.addEventListener('shopify:section:load', function () { initReveal(); initProducto(); initStickyAtc(); });
})();
