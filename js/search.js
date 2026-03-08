/* ExKnowledge site search — builds index from all pages, searches in-browser */
(function() {
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
    // Blog posts
    { url: 'blog/2026-03.html', title: 'Blog: March 2026' },
    { url: 'blog/2026-02.html', title: 'Blog: February 2026' },
    { url: 'blog/2026-01.html', title: 'Blog: January 2026' },
    { url: 'blog/2025-12.html', title: 'Blog: December 2025' },
    { url: 'blog/2025-11.html', title: 'Blog: November 2025' },
  ];

  // Detect language prefix
  var pathParts = location.pathname.split('/').filter(Boolean);
  var langCodes = ['ar','da','de','es','fi','it','nl','no','pt','sv'];
  var langPrefix = '';
  if (pathParts.length > 0 && langCodes.indexOf(pathParts[0]) !== -1) {
    langPrefix = pathParts[0] + '/';
  }

  var index = null;
  var indexBuilding = false;
  var indexCallbacks = [];

  function buildIndex(cb) {
    if (index) { cb(index); return; }
    indexCallbacks.push(cb);
    if (indexBuilding) return;
    indexBuilding = true;
    index = [];

    var urlsToFetch = PAGES.map(function(p) {
      return langPrefix
        ? { title: p.title, url: langPrefix + p.url, fallbackUrl: p.url }
        : { title: p.title, url: p.url, fallbackUrl: null };
    });

    var pending = urlsToFetch.length;
    function done() {
      pending--;
      if (pending <= 0) {
        indexCallbacks.forEach(function(fn) { fn(index); });
        indexCallbacks = [];
      }
    }

    urlsToFetch.forEach(function(p) {
      fetch('/' + p.url).then(function(res) {
        if (!res.ok && p.fallbackUrl) return fetch('/' + p.fallbackUrl);
        return res;
      }).then(function(res) {
        if (!res.ok) { done(); return; }
        return res.text();
      }).then(function(html) {
        if (!html) { done(); return; }
        var doc = new DOMParser().parseFromString(html, 'text/html');
        var body = doc.querySelector('.content-body') || doc.querySelector('article');
        if (!body) { done(); return; }
        var sections = [];
        var current = { heading: p.title, text: '', anchor: '' };
        var children = body.children;
        for (var i = 0; i < children.length; i++) {
          var node = children[i];
          if (node.tagName === 'H1') continue;
          if (node.tagName === 'H2' || node.tagName === 'H3') {
            if (current.text.trim()) sections.push({ heading: current.heading, text: current.text, anchor: current.anchor });
            current = { heading: node.textContent.trim(), text: '', anchor: node.id || '' };
          } else {
            current.text += ' ' + node.textContent;
          }
        }
        if (current.text.trim()) sections.push(current);
        sections.forEach(function(s) {
          index.push({
            page: p.title,
            url: '/' + p.url + (s.anchor ? '#' + s.anchor : ''),
            heading: s.heading,
            text: s.text.replace(/\s+/g, ' ').trim().toLowerCase(),
            display: s.text.replace(/\s+/g, ' ').trim()
          });
        });
        done();
      }).catch(function() { done(); });
    });
  }

  function search(query) {
    if (!index) return [];
    var terms = query.toLowerCase().split(/\s+/).filter(function(t) { return t.length > 1; });
    if (!terms.length) return [];
    var results = [];
    for (var i = 0; i < index.length; i++) {
      var entry = index[i];
      var haystack = (entry.heading + ' ' + entry.text).toLowerCase();
      var score = 0;
      var matched = 0;
      for (var j = 0; j < terms.length; j++) {
        var t = terms[j];
        if (haystack.indexOf(t) !== -1) {
          matched++;
          if (entry.heading.toLowerCase().indexOf(t) !== -1) score += 10;
          var idx = -1;
          while ((idx = haystack.indexOf(t, idx + 1)) !== -1) score++;
        }
      }
      if (matched === terms.length) {
        results.push({ page: entry.page, url: entry.url, heading: entry.heading, display: entry.display, score: score });
      }
    }
    results.sort(function(a, b) { return b.score - a.score; });
    return results.slice(0, 12);
  }

  function getSnippet(text, query, maxLen) {
    maxLen = maxLen || 140;
    var terms = query.toLowerCase().split(/\s+/).filter(function(t) { return t.length > 1; });
    var lower = text.toLowerCase();
    var bestPos = 0;
    for (var i = 0; i < terms.length; i++) {
      var pos = lower.indexOf(terms[i]);
      if (pos >= 0) { bestPos = pos; break; }
    }
    var start = Math.max(0, bestPos - 40);
    var snippet = (start > 0 ? '…' : '') + text.slice(start, start + maxLen);
    if (start + maxLen < text.length) snippet += '…';
    for (var i = 0; i < terms.length; i++) {
      snippet = snippet.replace(new RegExp('(' + terms[i].replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi'), '<mark>$1</mark>');
    }
    return snippet;
  }

  function renderResults(results, query) {
    if (!results.length) return '<div class="hero-search-result"><span>No results found</span></div>';
    return results.map(function(r) {
      var snippet = getSnippet(r.display, query);
      return '<a class="hero-search-result" href="' + r.url + '">' +
        '<strong>' + r.page + '</strong>' +
        '<em style="color:var(--accent);font-size:12px;font-style:normal;display:block;margin-bottom:2px">' + r.heading + '</em>' +
        '<span>' + snippet + '</span></a>';
    }).join('');
  }

  // ========== Hero search (homepage) ==========
  function initHeroSearch() {
    var input = document.getElementById('heroSearch');
    if (!input) return;
    var wrap = input.parentElement;
    var resultsDiv = document.createElement('div');
    resultsDiv.className = 'hero-search-results';
    wrap.appendChild(resultsDiv);

    // Start building index immediately
    buildIndex(function() {});

    var debounce;
    input.addEventListener('input', function() {
      clearTimeout(debounce);
      var self = this;
      debounce = setTimeout(function() {
        buildIndex(function() {
          var q = self.value.trim();
          if (q.length < 2) { resultsDiv.classList.remove('open'); return; }
          var results = search(q);
          resultsDiv.innerHTML = renderResults(results, q);
          resultsDiv.classList.add('open');
        });
      }, 150);
    });

    document.addEventListener('click', function(e) {
      if (!wrap.contains(e.target)) resultsDiv.classList.remove('open');
    });
    input.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') {
        var first = resultsDiv.querySelector('a');
        if (first) window.location = first.href;
      }
    });
  }

  // ========== Nav overlay search (Cmd+K) ==========
  function initOverlaySearch() {
    var navLinks = document.querySelector('.nav-links');
    if (!navLinks) return;
    var li = document.createElement('li');
    li.innerHTML = '<a href="#" class="search-toggle" aria-label="Search"><i class="ph ph-magnifying-glass"></i></a>';
    navLinks.appendChild(li);

    var overlay = document.createElement('div');
    overlay.className = 'search-overlay';
    overlay.innerHTML =
      '<div class="search-box">' +
      '<input type="text" class="search-input" placeholder="Search all topics and guides…" autocomplete="off">' +
      '<button class="search-close" aria-label="Close">✕</button>' +
      '<div class="search-results"></div>' +
      '</div>';
    document.body.appendChild(overlay);

    var input = overlay.querySelector('.search-input');
    var resultsDiv = overlay.querySelector('.search-results');
    var closeBtn = overlay.querySelector('.search-close');
    var toggle = li.querySelector('.search-toggle');

    function open() {
      overlay.classList.add('open');
      input.value = '';
      resultsDiv.innerHTML = '<p class="search-hint">Search across 28 pages…</p>';
      setTimeout(function() { input.focus(); }, 100);
      buildIndex(function() {});
    }
    function close() { overlay.classList.remove('open'); }

    toggle.addEventListener('click', function(e) { e.preventDefault(); open(); });
    closeBtn.addEventListener('click', close);
    overlay.addEventListener('click', function(e) { if (e.target === overlay) close(); });
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') close();
      if ((e.key === 'k' || e.key === 'K') && (e.metaKey || e.ctrlKey)) { e.preventDefault(); open(); }
    });

    var debounce;
    input.addEventListener('input', function() {
      clearTimeout(debounce);
      var self = this;
      debounce = setTimeout(function() {
        buildIndex(function() {
          var q = self.value.trim();
          if (q.length < 2) {
            resultsDiv.innerHTML = '<p class="search-hint">Search across 28 pages…</p>';
            return;
          }
          var results = search(q);
          if (!results.length) {
            resultsDiv.innerHTML = '<p class="search-hint">No results found.</p>';
            return;
          }
          resultsDiv.innerHTML = results.map(function(r) {
            return '<a href="' + r.url + '" class="search-result">' +
              '<span class="search-result-page">' + r.page + '</span>' +
              '<span class="search-result-heading">' + r.heading + '</span>' +
              '<span class="search-result-snippet">' + getSnippet(r.display, q) + '</span></a>';
          }).join('');
        });
      }, 200);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() { initHeroSearch(); initOverlaySearch(); });
  } else {
    initHeroSearch();
    initOverlaySearch();
  }
})();
