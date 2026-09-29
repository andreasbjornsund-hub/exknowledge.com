/* ExKnowledge site search: builds an index from the content pages and searches in the browser.
   States: idle hint, loading, results, no results, unavailable (with retry). */
(function () {
  var PAGES = [
    // Core knowledge base
    { url: 'pages/fundamentals.html', title: 'Fundamentals of Explosion Protection' },
    { url: 'pages/zone-classification.html', title: 'Zone Classification' },
    { url: 'pages/gas-groups.html', title: 'Gas Groups & Dust Groups' },
    { url: 'pages/temperature-classes.html', title: 'Temperature Classes' },
    { url: 'pages/protection-methods.html', title: 'Protection Methods' },
    { url: 'pages/epl.html', title: 'Equipment Protection Levels (EPL)' },
    { url: 'pages/ex-markings.html', title: 'Ex Markings' },
    { url: 'pages/standards.html', title: 'Standards & Directives' },
    { url: 'pages/certification.html', title: 'Certification Process' },
    { url: 'pages/installation-inspection.html', title: 'Installation & Inspection' },
    { url: 'pages/atex-equipment-categories.html', title: 'ATEX Equipment Categories' },
    { url: 'pages/cheat-sheet.html', title: 'Cheat Sheet' },
    { url: 'pages/faq.html', title: 'FAQ' },
    // In-depth guides
    { url: 'pages/atex-vs-iecex.html', title: 'ATEX vs IECEx' },
    { url: 'pages/explosion-proof-vs-intrinsically-safe.html', title: 'Explosion Proof vs Intrinsically Safe' },
    { url: 'pages/how-to-read-atex-nameplate.html', title: 'How to Read an ATEX Nameplate' },
    { url: 'pages/atex-directive.html', title: 'ATEX Directive 2014/34/EU' },
    { url: 'pages/hazardous-area-classification.html', title: 'Hazardous Area Classification' },
    { url: 'pages/dust-explosion-protection.html', title: 'Dust Explosion Protection' },
    { url: 'pages/atex-for-beginners.html', title: 'ATEX for Beginners' },
    { url: 'pages/compex-certification.html', title: 'CompEx Certification Guide' },
    { url: 'pages/hydrogen-explosion-protection.html', title: 'Hydrogen Explosion Protection' },
    { url: 'pages/cable-glands-hazardous-areas.html', title: 'Cable Glands for Hazardous Areas' },
    { url: 'pages/ex-equipment-selection-guide.html', title: 'Ex Equipment Selection Guide' },
    { url: 'pages/dsear-regulations-uk.html', title: 'DSEAR Regulations (UK)' },
    { url: 'pages/nec-500-vs-atex-iec.html', title: 'NEC 500 vs ATEX / IEC' },
    { url: 'pages/nr10-inmetro-brazil.html', title: 'NR-10 and INMETRO (Brazil)' },
    // Blog posts
    { url: 'blog/2026-03-hydrogen-safety.html', title: 'Blog: Hydrogen Safety' },
    { url: 'blog/gas-group-iic-hydrogen-acetylene.html', title: 'Blog: Gas Group IIC, Hydrogen and Acetylene' },
    // Applications, certification by country, tools (2026-09)
    { url: 'pages/atex-applications.html', title: "Does It Need ATEX Zoning? Hazardous Areas by Application" },
    { url: 'pages/atex-battery-rooms.html', title: "Battery rooms and battery energy storage: do they need ATEX zoning?" },
    { url: 'pages/atex-ev-charging.html', title: "EV charging and hazardous areas: petrol stations, car parks and ATEX" },
    { url: 'pages/atex-hydrogen-electrolysers.html', title: "Hydrogen electrolysers: ATEX zoning and hazardous area classification" },
    { url: 'pages/atex-co2.html', title: "Does CO2 need an ATEX zone?" },
    { url: 'pages/atex-spray-booths.html', title: "Spray Booth ATEX Zones: EN 16985, DSEAR and NFPA 33" },
    { url: 'pages/atex-grain-silos-flour-mills.html', title: "Do Grain Silos, Flour Mills and Feed Mills Need ATEX Zoning?" },
    { url: 'pages/atex-biogas-plants.html', title: "Do Biogas and Anaerobic Digestion Plants Need ATEX Zoning?" },
    { url: 'pages/atex-distilleries.html', title: "Do Distilleries Need ATEX Zoning? Whisky, Gin and Ethanol Plants" },
    { url: 'pages/ex-certification-schemes.html', title: "Ex Certification by Country: ATEX, IECEx, UKCA and More" },
    { url: 'pages/ukca-ex-certification.html', title: "UKCA Ex (UKEX) Certification for Hazardous Area Equipment" },
    { url: 'pages/eac-ex-certification.html', title: "EAC Ex Certification for the Eurasian Economic Union (TR CU 012/2011)" },
    { url: 'pages/india-peso-ex-certification.html', title: "India: PESO Approval for Ex Equipment in Hazardous Areas" },
    { url: 'pages/china-ccc-ex-certification.html', title: "China CCC Ex Certification for Explosion-Protected Equipment" },
    { url: 'pages/korea-kcs-ex-certification.html', title: "South Korea KCs Ex Certification for Explosion-Protected Equipment" },
    { url: 'pages/japan-jpex-ex-certification.html', title: "Japan Ex Certification (JPEx): Type Examination Rules" },
    { url: 'pages/intrinsic-safety-calculator.html', title: "Intrinsic Safety Loop Calculator" },
    { url: 'blog/2026-09.html', title: 'Blog: September 2026' },
    { url: 'blog/2026-07.html', title: 'Blog: July 2026' },
    { url: 'blog/2026-03.html', title: 'Blog: March 2026' },
    { url: 'blog/2026-02.html', title: 'Blog: February 2026' },
    { url: 'blog/2026-01.html', title: 'Blog: January 2026' },
    { url: 'blog/2025-12.html', title: 'Blog: December 2025' },
    { url: 'blog/2025-11.html', title: 'Blog: November 2025' }
  ];

  var LANG = (document.documentElement.getAttribute('lang') || 'en').slice(0, 2);
  if (LANG === 'nb' || LANG === 'nn') LANG = 'no';
  var S = {
    en: { hint: 'Search across {n} pages…', loading: 'Loading the search index…', none: 'No results found. Try a shorter or different term.', fail: 'Search is unavailable right now.', retry: 'Try again', placeholder: 'Search all topics and guides…', label: 'Search', close: 'Close search' },
    de: { hint: 'Suche in {n} Seiten…', loading: 'Suchindex wird geladen…', none: 'Keine Treffer. Versuchen Sie einen kürzeren oder anderen Begriff.', fail: 'Die Suche ist gerade nicht verfügbar.', retry: 'Erneut versuchen', placeholder: 'Alle Themen und Leitfäden durchsuchen…', label: 'Suche', close: 'Suche schließen' },
    no: { hint: 'Søk i {n} sider…', loading: 'Laster søkeindeksen…', none: 'Ingen treff. Prøv et kortere eller annet ord.', fail: 'Søket er ikke tilgjengelig akkurat nå.', retry: 'Prøv igjen', placeholder: 'Søk i alle emner og guider…', label: 'Søk', close: 'Lukk søk' },
    da: { hint: 'Søg i {n} sider…', loading: 'Indlæser søgeindekset…', none: 'Ingen resultater. Prøv et kortere eller andet ord.', fail: 'Søgningen er ikke tilgængelig lige nu.', retry: 'Prøv igen', placeholder: 'Søg i alle emner og guides…', label: 'Søg', close: 'Luk søgning' },
    sv: { hint: 'Sök bland {n} sidor…', loading: 'Laddar sökindexet…', none: 'Inga träffar. Prova ett kortare eller annat ord.', fail: 'Sökningen är inte tillgänglig just nu.', retry: 'Försök igen', placeholder: 'Sök bland alla ämnen och guider…', label: 'Sök', close: 'Stäng sökning' },
    fi: { hint: 'Hae {n} sivulta…', loading: 'Ladataan hakemistoa…', none: 'Ei tuloksia. Kokeile lyhyempää tai eri hakusanaa.', fail: 'Haku ei ole juuri nyt käytettävissä.', retry: 'Yritä uudelleen', placeholder: 'Hae kaikista aiheista ja oppaista…', label: 'Haku', close: 'Sulje haku' },
    es: { hint: 'Buscar en {n} páginas…', loading: 'Cargando el índice de búsqueda…', none: 'Sin resultados. Pruebe un término más corto o distinto.', fail: 'La búsqueda no está disponible ahora.', retry: 'Reintentar', placeholder: 'Buscar en todos los temas y guías…', label: 'Buscar', close: 'Cerrar búsqueda' },
    nl: { hint: 'Zoek in {n} pagina’s…', loading: 'Zoekindex laden…', none: 'Geen resultaten. Probeer een korter of ander woord.', fail: 'Zoeken is nu niet beschikbaar.', retry: 'Opnieuw proberen', placeholder: 'Zoek in alle onderwerpen en gidsen…', label: 'Zoeken', close: 'Zoeken sluiten' },
    pt: { hint: 'Pesquisar em {n} páginas…', loading: 'A carregar o índice de pesquisa…', none: 'Sem resultados. Tente um termo mais curto ou diferente.', fail: 'A pesquisa não está disponível agora.', retry: 'Tentar novamente', placeholder: 'Pesquisar todos os temas e guias…', label: 'Pesquisar', close: 'Fechar pesquisa' },
    it: { hint: 'Cerca in {n} pagine…', loading: 'Caricamento dell’indice di ricerca…', none: 'Nessun risultato. Prova un termine più breve o diverso.', fail: 'La ricerca non è disponibile al momento.', retry: 'Riprova', placeholder: 'Cerca in tutti gli argomenti e le guide…', label: 'Cerca', close: 'Chiudi ricerca' },
    ar: { hint: 'ابحث في {n} صفحة…', loading: 'جارٍ تحميل فهرس البحث…', none: 'لا توجد نتائج. جرّب كلمة أقصر أو مختلفة.', fail: 'البحث غير متاح الآن.', retry: 'حاول مرة أخرى', placeholder: 'ابحث في جميع المواضيع والأدلة…', label: 'بحث', close: 'إغلاق البحث' }
  };
  var T = S[LANG] || S.en;

  var langCodes = ['ar', 'da', 'de', 'es', 'fi', 'it', 'nl', 'no', 'pt', 'sv'];
  var first = location.pathname.split('/').filter(Boolean)[0];
  var langPrefix = langCodes.indexOf(first) !== -1 ? first + '/' : '';

  // state: 'idle' | 'loading' | 'ready' | 'failed'
  var state = 'idle', index = [], listeners = [];

  function notify() { listeners.forEach(function (fn) { fn(state); }); }
  function onState(fn) { listeners.push(fn); }

  function buildIndex() {
    if (state === 'loading' || state === 'ready') return;
    state = 'loading'; index = []; notify();
    var pending = PAGES.length, ok = 0;
    PAGES.forEach(function (p) {
      var url = langPrefix + p.url;
      fetch('/' + url).then(function (res) {
        if (!res.ok && langPrefix) { url = p.url; return fetch('/' + p.url); }
        return res;
      }).then(function (res) {
        if (!res || !res.ok) throw new Error('http');
        return res.text();
      }).then(function (html) {
        ok++;
        var doc = new DOMParser().parseFromString(html, 'text/html');
        var body = doc.querySelector('.content-body') || doc.querySelector('article') || doc.querySelector('main');
        if (!body) return;
        var sections = [], cur = { heading: p.title, text: '', anchor: '' };
        [].forEach.call(body.children, function (node) {
          if (node.tagName === 'H1') return;
          if (node.tagName === 'H2' || node.tagName === 'H3') {
            if (cur.text.trim()) sections.push(cur);
            cur = { heading: node.textContent.trim(), text: '', anchor: node.id || '' };
          } else {
            cur.text += ' ' + node.textContent;
          }
        });
        if (cur.text.trim()) sections.push(cur);
        var title = (doc.querySelector('h1') || {}).textContent || p.title;
        sections.forEach(function (s) {
          var clean = s.text.replace(/\s+/g, ' ').trim();
          index.push({ page: title.trim(), url: '/' + url + (s.anchor ? '#' + s.anchor : ''), heading: s.heading, text: clean.toLowerCase(), display: clean });
        });
      }).catch(function () { }).then(function () {
        pending--;
        if (pending === 0) { state = ok ? 'ready' : 'failed'; notify(); }
      });
    });
  }

  function search(query) {
    var terms = query.toLowerCase().split(/\s+/).filter(function (t) { return t.length > 1; });
    if (!terms.length) return [];
    var results = [];
    index.forEach(function (e) {
      var hay = (e.heading + ' ' + e.text).toLowerCase(), score = 0, matched = 0;
      terms.forEach(function (t) {
        if (hay.indexOf(t) !== -1) {
          matched++;
          if (e.heading.toLowerCase().indexOf(t) !== -1) score += 10;
          if (e.page.toLowerCase().indexOf(t) !== -1) score += 6;
          var i = -1; while ((i = hay.indexOf(t, i + 1)) !== -1) score++;
        }
      });
      if (matched === terms.length) results.push({ page: e.page, url: e.url, heading: e.heading, display: e.display, score: score });
    });
    results.sort(function (a, b) { return b.score - a.score; });
    return results.slice(0, 12);
  }

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function snippet(text, query) {
    var terms = query.toLowerCase().split(/\s+/).filter(function (t) { return t.length > 1; });
    var lower = text.toLowerCase(), pos = 0;
    for (var i = 0; i < terms.length; i++) { var p = lower.indexOf(terms[i]); if (p >= 0) { pos = p; break; } }
    var start = Math.max(0, pos - 40);
    var s = esc((start > 0 ? '…' : '') + text.slice(start, start + 140) + (start + 140 < text.length ? '…' : ''));
    terms.forEach(function (t) { s = s.replace(new RegExp('(' + esc(t).replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi'), '<mark>$1</mark>'); });
    return s;
  }

  // Renders the current state into a results container. kind: 'hero' | 'overlay'
  function render(box, q, kind) {
    var itemCls = kind === 'hero' ? 'hero-search-result' : 'search-result';
    if (state === 'loading' || state === 'idle') {
      box.innerHTML = '<p class="search-state" role="status"><span class="spinner" aria-hidden="true"></span>' + T.loading + '</p>';
      return;
    }
    if (state === 'failed') {
      box.innerHTML = '<p class="search-state search-state--error" role="alert">' + T.fail + ' <button type="button" class="btn btn--ghost btn--sm search-retry">' + T.retry + '</button></p>';
      box.querySelector('.search-retry').addEventListener('click', function () { state = 'idle'; buildIndex(); });
      return;
    }
    if (q.length < 2) { box.innerHTML = kind === 'overlay' ? '<p class="search-state">' + T.hint.replace('{n}', PAGES.length) + '</p>' : ''; return; }
    var results = search(q);
    if (!results.length) { box.innerHTML = '<p class="search-state" role="status">' + T.none + '</p>'; return; }
    box.innerHTML = results.map(function (r) {
      return kind === 'hero'
        ? '<a class="' + itemCls + '" href="' + r.url + '"><strong>' + esc(r.page) + '</strong><em class="search-result-heading">' + esc(r.heading) + '</em><span>' + snippet(r.display, q) + '</span></a>'
        : '<a class="' + itemCls + '" href="' + r.url + '"><span class="search-result-page">' + esc(r.page) + '</span><span class="search-result-heading">' + esc(r.heading) + '</span><span class="search-result-snippet">' + snippet(r.display, q) + '</span></a>';
    }).join('');
  }

  /* ---------- Hero search (home pages) ---------- */
  function initHero() {
    var input = document.getElementById('heroSearch');
    if (!input) return;
    var wrap = input.parentElement;
    var box = document.createElement('div');
    box.className = 'hero-search-results';
    box.id = 'heroSearchResults';
    box.setAttribute('aria-live', 'polite');
    wrap.appendChild(box);
    input.setAttribute('aria-controls', box.id);
    input.setAttribute('aria-label', input.getAttribute('placeholder') || T.label);
    var btn = wrap.querySelector('.hero-search-btn');
    if (btn) { btn.type = 'button'; var ic = btn.querySelector('.ph'); if (ic) ic.setAttribute('aria-hidden', 'true'); }

    function show() {
      var q = input.value.trim();
      if (q.length < 2 && state === 'ready') { box.classList.remove('open'); return; }
      render(box, q, 'hero');
      box.classList.toggle('open', !!box.innerHTML);
    }
    function go() {
      var q = input.value.trim();
      if (q.length < 2) { input.focus(); return; }
      buildIndex();
      if (state === 'ready') { var a = box.querySelector('a'); if (a) { window.location = a.href; return; } }
      show();
    }
    onState(function () { if (input.value.trim().length >= 2 || state === 'failed') show(); });
    input.addEventListener('focus', buildIndex, { once: true });
    var t;
    input.addEventListener('input', function () { clearTimeout(t); t = setTimeout(function () { buildIndex(); show(); }, 150); });
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { e.preventDefault(); go(); }
      if (e.key === 'Escape') { box.classList.remove('open'); }
    });
    if (btn) btn.addEventListener('click', go);
    document.addEventListener('click', function (e) { if (!wrap.contains(e.target)) box.classList.remove('open'); });
  }

  /* ---------- Overlay search (nav button, Ctrl/Cmd+K) ---------- */
  function initOverlay() {
    var navLinks = document.querySelector('.nav-links');
    // Only on pages that use the shared stylesheet (the certificate scanner has its own)
    if (!navLinks || !document.querySelector('link[href*="/css/style.css"]')) return;
    var li = document.createElement('li');
    li.className = 'nav-search';
    li.innerHTML = '<button type="button" class="search-toggle" aria-label="' + T.label + '" aria-haspopup="dialog"><i class="ph ph-magnifying-glass" aria-hidden="true"></i><span class="nav-search-label">' + T.label + '</span></button>';
    navLinks.appendChild(li);
    var toggle = li.querySelector('.search-toggle');

    var overlay = document.createElement('div');
    overlay.className = 'search-overlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-label', T.label);
    overlay.innerHTML =
      '<div class="search-box">' +
      '<input type="search" class="search-input" placeholder="' + T.placeholder + '" aria-label="' + T.placeholder + '" autocomplete="off">' +
      '<button type="button" class="search-close" aria-label="' + T.close + '">✕</button>' +
      '<div class="search-results" aria-live="polite"></div>' +
      '</div>';
    document.body.appendChild(overlay);
    var input = overlay.querySelector('.search-input');
    var box = overlay.querySelector('.search-results');

    function open() {
      overlay.classList.add('open');
      document.documentElement.classList.add('has-modal');
      input.value = '';
      buildIndex();
      render(box, '', 'overlay');
      if (window.EXK && EXK.openDialog) EXK.openDialog(overlay, { returnFocus: toggle, initialFocus: input, onClose: close });
      else setTimeout(function () { input.focus(); }, 30);
    }
    function close() {
      if (!overlay.classList.contains('open')) return;
      overlay.classList.remove('open');
      document.documentElement.classList.remove('has-modal');
      if (window.EXK && EXK.closeDialog) EXK.closeDialog(overlay); else toggle.focus();
    }
    toggle.addEventListener('click', open);
    overlay.querySelector('.search-close').addEventListener('click', close);
    overlay.addEventListener('click', function (e) { if (e.target === overlay) close(); });
    document.addEventListener('keydown', function (e) {
      if ((e.key === 'k' || e.key === 'K') && (e.metaKey || e.ctrlKey)) { e.preventDefault(); open(); }
      if (e.key === 'Escape' && overlay.classList.contains('open') && !(window.EXK && EXK.openDialog)) close();
    });
    onState(function () { if (overlay.classList.contains('open')) render(box, input.value.trim(), 'overlay'); });
    var t;
    input.addEventListener('input', function () { clearTimeout(t); t = setTimeout(function () { render(box, input.value.trim(), 'overlay'); }, 150); });
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { var a = box.querySelector('a'); if (a) window.location = a.href; }
    });
  }

  function init() { initHero(); initOverlay(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
