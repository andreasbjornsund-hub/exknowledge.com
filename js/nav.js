/* ExKnowledge shared navigation and accessibility helpers.
   Loaded on every page. See DESIGN.md for the behaviour contract. */
(function () {
  var LANG = (document.documentElement.getAttribute('lang') || 'en').slice(0, 2);
  if (LANG === 'nb' || LANG === 'nn') LANG = 'no';
  var I18N = {
    en: { skip: 'Skip to content', menu: 'Menu', close: 'Close', search: 'Search', sending: 'Sending…' },
    de: { skip: 'Zum Inhalt springen', menu: 'Menü', close: 'Schließen', search: 'Suche', sending: 'Wird gesendet…' },
    no: { skip: 'Hopp til innhold', menu: 'Meny', close: 'Lukk', search: 'Søk', sending: 'Sender…' },
    da: { skip: 'Spring til indhold', menu: 'Menu', close: 'Luk', search: 'Søg', sending: 'Sender…' },
    sv: { skip: 'Hoppa till innehåll', menu: 'Meny', close: 'Stäng', search: 'Sök', sending: 'Skickar…' },
    fi: { skip: 'Siirry sisältöön', menu: 'Valikko', close: 'Sulje', search: 'Haku', sending: 'Lähetetään…' },
    es: { skip: 'Saltar al contenido', menu: 'Menú', close: 'Cerrar', search: 'Buscar', sending: 'Enviando…' },
    nl: { skip: 'Naar inhoud', menu: 'Menu', close: 'Sluiten', search: 'Zoeken', sending: 'Verzenden…' },
    pt: { skip: 'Ir para o conteúdo', menu: 'Menu', close: 'Fechar', search: 'Pesquisar', sending: 'A enviar…' },
    it: { skip: 'Vai al contenuto', menu: 'Menu', close: 'Chiudi', search: 'Cerca', sending: 'Invio…' },
    ar: { skip: 'انتقل إلى المحتوى', menu: 'القائمة', close: 'إغلاق', search: 'بحث', sending: 'جارٍ الإرسال…' }
  };
  var T = I18N[LANG] || I18N.en;

  /* ---------- Shared dialog helper: Escape, focus in, focus trap, focus back ---------- */
  var FOCUSABLE = 'a[href], button:not([disabled]), input:not([disabled]):not([type=hidden]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';
  var openDialogs = [];
  function openDialog(el, opts) {
    opts = opts || {};
    var rec = { el: el, onClose: opts.onClose, back: opts.returnFocus || document.activeElement, modal: opts.modal !== false };
    openDialogs.push(rec);
    el.removeAttribute('inert');
    if (opts.focus !== false) {
      var first = opts.initialFocus || el.querySelector('input:not([type=hidden]), textarea, select') || el.querySelector(FOCUSABLE);
      if (first) setTimeout(function () { first.focus(); }, 30);
    }
    return rec;
  }
  function closeDialog(el) {
    for (var i = openDialogs.length - 1; i >= 0; i--) {
      if (openDialogs[i].el === el) {
        var rec = openDialogs.splice(i, 1)[0];
        if (rec.back && rec.back.focus && document.contains(rec.back)) rec.back.focus();
        return;
      }
    }
  }
  document.addEventListener('keydown', function (e) {
    var top = openDialogs[openDialogs.length - 1];
    if (!top) return;
    if (e.key === 'Escape') {
      e.preventDefault();
      if (top.onClose) top.onClose(); else closeDialog(top.el);
      return;
    }
    if (e.key === 'Tab' && top.modal) {
      var items = [].filter.call(top.el.querySelectorAll(FOCUSABLE), function (n) { return n.offsetParent !== null || n === document.activeElement; });
      if (!items.length) return;
      var first = items[0], last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      else if (!top.el.contains(document.activeElement)) { e.preventDefault(); first.focus(); }
    }
  });
  window.EXK = window.EXK || {};
  window.EXK.lang = LANG;
  window.EXK.t = T;
  window.EXK.openDialog = openDialog;
  window.EXK.closeDialog = closeDialog;

  /* ---------- Skip link ---------- */
  function initSkip() {
    var target = document.getElementById('main-content') ||
      document.querySelector('main, .content-page, .hero, .page-hero, body > section, body > div.container');
    if (!target) return;
    if (!target.id) target.id = 'main-content';
    if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1');
    var link = document.querySelector('.skip-link');
    if (!link) {
      link = document.createElement('a');
      link.className = 'skip-link';
      link.textContent = T.skip;
      document.body.insertBefore(link, document.body.firstChild);
    }
    link.setAttribute('href', '#' + target.id);
  }

  /* ---------- Mobile menu ---------- */
  function initMenu() {
    var burger = document.querySelector('.burger');
    var links = document.querySelector('.nav-links');
    if (!burger || !links) return;
    if (!links.id) links.id = 'site-nav';
    if (burger.tagName !== 'BUTTON') { burger.setAttribute('role', 'button'); burger.setAttribute('tabindex', '0'); }
    burger.setAttribute('aria-controls', links.id);
    burger.setAttribute('aria-expanded', 'false');
    if (!burger.getAttribute('aria-label')) burger.setAttribute('aria-label', T.menu);
    var icon = burger.querySelector('.ph-bold, .ph'); if (icon) icon.setAttribute('aria-hidden', 'true');

    function setOpen(open, focusBack) {
      burger.classList.toggle('open', open);
      links.classList.toggle('open', open);
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (icon) { icon.classList.toggle('ph-list', !open); icon.classList.toggle('ph-x', open); }
      if (open) {
        openDialog(links, { returnFocus: burger, modal: false, onClose: function () { setOpen(false, true); } });
      } else {
        closeAllDropdowns();
        for (var i = openDialogs.length - 1; i >= 0; i--) if (openDialogs[i].el === links) openDialogs.splice(i, 1);
        if (focusBack) burger.focus();
      }
    }
    burger.addEventListener('click', function (e) { e.stopPropagation(); setOpen(!links.classList.contains('open')); });
    burger.addEventListener('keydown', function (e) {
      if (burger.tagName !== 'BUTTON' && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); burger.click(); }
    });
    document.addEventListener('click', function (e) {
      if (links.classList.contains('open') && !burger.contains(e.target) && !links.contains(e.target)) setOpen(false);
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 900 && links.classList.contains('open')) setOpen(false);
    });
  }

  /* ---------- Dropdowns (click, keyboard, hover via CSS) ---------- */
  function closeAllDropdowns(except) {
    document.querySelectorAll('.has-dropdown.open').forEach(function (li) {
      if (li === except) return;
      li.classList.remove('open');
      var t = li.querySelector('.dd-toggle, :scope > a');
      if (t) t.setAttribute('aria-expanded', 'false');
    });
  }
  function initDropdowns() {
    document.querySelectorAll('.has-dropdown').forEach(function (li) {
      var trigger = li.querySelector('.dd-toggle') || li.querySelector(':scope > a');
      var menu = li.querySelector('.dropdown');
      if (!trigger || !menu) return;
      if (trigger.tagName === 'A') trigger.setAttribute('role', 'button');
      trigger.setAttribute('aria-haspopup', 'true');
      trigger.setAttribute('aria-expanded', 'false');
      trigger.addEventListener('click', function (e) {
        e.preventDefault();
        var open = !li.classList.contains('open');
        closeAllDropdowns(li);
        li.classList.toggle('open', open);
        trigger.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
      li.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && li.classList.contains('open')) {
          e.stopPropagation();
          li.classList.remove('open');
          trigger.setAttribute('aria-expanded', 'false');
          trigger.focus();
        }
      });
      li.addEventListener('focusout', function (e) {
        if (window.innerWidth > 900 && !li.contains(e.relatedTarget)) {
          li.classList.remove('open');
          trigger.setAttribute('aria-expanded', 'false');
        }
      });
    });
    document.addEventListener('click', function (e) {
      if (!e.target.closest || !e.target.closest('.has-dropdown')) {
        if (window.innerWidth > 900) closeAllDropdowns();
      }
    });
  }

  /* ---------- Language select: short code on small phones ---------- */
  function initLang() {
    var sel = document.querySelector('.lang-select');
    if (!sel || !window.matchMedia) return;
    var mq = window.matchMedia('(max-width: 420px)');
    function codeFor(opt) {
      var m = (opt.value || '').match(/^\/(ar|da|de|es|fi|it|nl|no|pt|sv)\//);
      return m ? m[1].toUpperCase() : 'EN';
    }
    function apply() {
      [].forEach.call(sel.options, function (o) {
        if (!o.dataset.full) o.dataset.full = o.textContent;
        o.textContent = (mq.matches && o.selected) ? codeFor(o) : o.dataset.full;
      });
    }
    apply();
    if (mq.addEventListener) mq.addEventListener('change', apply); else if (mq.addListener) mq.addListener(apply);
    sel.addEventListener('change', apply);
  }

  /* ---------- Video slides: keyboard operable ---------- */
  function initSlides() {
    document.querySelectorAll('.slide[onclick]').forEach(function (s) {
      var h = s.querySelector('h3');
      s.setAttribute('role', 'button');
      s.setAttribute('tabindex', '0');
      s.setAttribute('aria-label', 'Play video: ' + (h ? h.textContent.trim() : ''));
      s.addEventListener('keydown', function (e) {
        if ((e.key === 'Enter' || e.key === ' ') && s.getAttribute('role') === 'button') { e.preventDefault(); s.click(); }
      });
    });
  }

  function init() { initSkip(); initMenu(); initDropdowns(); initLang(); initSlides(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();

function slideVideos(dir) {
  var track = document.getElementById('sliderTrack');
  var slide = track && track.querySelector('.slide');
  if (!slide) return;
  var w = slide.offsetWidth + 16; // width + gap
  track.scrollBy({ left: dir * w * 2, behavior: 'smooth' });
}

function playVideo(el, id) {
  var thumb = el.querySelector('.slide-thumb');
  var title = (el.querySelector('h3') || {}).textContent || 'Video';
  thumb.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1" title="' + title.replace(/"/g, '&quot;') + '" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="position:absolute;top:0;left:0;width:100%;height:100%;border:0"></iframe>';
  el.style.cursor = 'default';
  el.onclick = null;
  el.removeAttribute('onclick');
  el.removeAttribute('role');
  el.removeAttribute('tabindex');
  el.removeAttribute('aria-label');
}
