/* ExKnowledge site search — builds index from page list, searches in-browser */
(function() {
  const PAGES = [
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
  ];

  // Resolve base URL (works from / or /pages/)
  const base = location.pathname.includes('/pages/') ? '../' : '';
  let index = null;

  async function buildIndex() {
    if (index) return index;
    index = [];
    const fetches = PAGES.map(async (p) => {
      try {
        const res = await fetch(base + p.url);
        if (!res.ok) return;
        const html = await res.text();
        const doc = new DOMParser().parseFromString(html, 'text/html');
        const body = doc.querySelector('.content-body');
        if (!body) return;
        // Extract sections by h2/h3
        const sections = [];
        let current = { heading: p.title, text: '', anchor: '' };
        for (const node of body.children) {
          if (node.tagName === 'H1') continue;
          if (node.tagName === 'H2' || node.tagName === 'H3') {
            if (current.text.trim()) sections.push({ ...current });
            current = { heading: node.textContent.trim(), text: '', anchor: node.id || '' };
          } else {
            current.text += ' ' + node.textContent;
          }
        }
        if (current.text.trim()) sections.push(current);
        for (const s of sections) {
          index.push({
            page: p.title,
            url: base + p.url + (s.anchor ? '#' + s.anchor : ''),
            heading: s.heading,
            text: s.text.replace(/\s+/g, ' ').trim().toLowerCase(),
            display: s.text.replace(/\s+/g, ' ').trim()
          });
        }
      } catch (e) { /* skip */ }
    });
    await Promise.all(fetches);
    return index;
  }

  function search(query) {
    if (!index) return [];
    const terms = query.toLowerCase().split(/\s+/).filter(t => t.length > 1);
    if (!terms.length) return [];
    const results = [];
    for (const entry of index) {
      const haystack = (entry.heading + ' ' + entry.text).toLowerCase();
      let score = 0;
      let matched = 0;
      for (const t of terms) {
        if (haystack.includes(t)) {
          matched++;
          // Heading match worth more
          if (entry.heading.toLowerCase().includes(t)) score += 10;
          // Count occurrences in text
          let idx = -1;
          while ((idx = haystack.indexOf(t, idx + 1)) !== -1) score++;
        }
      }
      if (matched === terms.length) {
        results.push({ ...entry, score });
      }
    }
    results.sort((a, b) => b.score - a.score);
    return results.slice(0, 15);
  }

  function getSnippet(text, query, maxLen) {
    maxLen = maxLen || 160;
    const terms = query.toLowerCase().split(/\s+/).filter(t => t.length > 1);
    const lower = text.toLowerCase();
    let bestPos = 0;
    for (const t of terms) {
      const i = lower.indexOf(t);
      if (i >= 0) { bestPos = i; break; }
    }
    let start = Math.max(0, bestPos - 40);
    let snippet = (start > 0 ? '…' : '') + text.slice(start, start + maxLen);
    if (start + maxLen < text.length) snippet += '…';
    // Bold matching terms
    for (const t of terms) {
      snippet = snippet.replace(new RegExp('(' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi'), '<mark>$1</mark>');
    }
    return snippet;
  }

  // Inject search UI
  function init() {
    // Add search toggle to nav
    const navLinks = document.querySelector('.nav-links');
    if (!navLinks) return;
    const li = document.createElement('li');
    li.innerHTML = '<a href="#" class="search-toggle" aria-label="Search">🔍</a>';
    navLinks.appendChild(li);

    // Search overlay
    const overlay = document.createElement('div');
    overlay.className = 'search-overlay';
    overlay.innerHTML = `
      <div class="search-box">
        <input type="text" class="search-input" placeholder="Search all topics…" autocomplete="off" autofocus>
        <button class="search-close" aria-label="Close">✕</button>
        <div class="search-results"></div>
      </div>
    `;
    document.body.appendChild(overlay);

    const input = overlay.querySelector('.search-input');
    const resultsDiv = overlay.querySelector('.search-results');
    const closeBtn = overlay.querySelector('.search-close');
    const toggle = li.querySelector('.search-toggle');

    function open() {
      overlay.classList.add('open');
      input.value = '';
      resultsDiv.innerHTML = '<p class="search-hint">Start typing to search across all topics…</p>';
      setTimeout(() => input.focus(), 100);
      buildIndex();
    }
    function close() {
      overlay.classList.remove('open');
    }

    toggle.addEventListener('click', (e) => { e.preventDefault(); open(); });
    closeBtn.addEventListener('click', close);
    overlay.addEventListener('click', (e) => { if (e.target === overlay) close(); });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') close();
      if ((e.key === 'k' || e.key === 'K') && (e.metaKey || e.ctrlKey)) { e.preventDefault(); open(); }
    });

    let debounce;
    input.addEventListener('input', () => {
      clearTimeout(debounce);
      debounce = setTimeout(async () => {
        await buildIndex();
        const q = input.value.trim();
        if (q.length < 2) {
          resultsDiv.innerHTML = '<p class="search-hint">Start typing to search across all topics…</p>';
          return;
        }
        const results = search(q);
        if (!results.length) {
          resultsDiv.innerHTML = '<p class="search-hint">No results found.</p>';
          return;
        }
        resultsDiv.innerHTML = results.map(r =>
          `<a href="${r.url}" class="search-result">
            <span class="search-result-page">${r.page}</span>
            <span class="search-result-heading">${r.heading}</span>
            <span class="search-result-snippet">${getSnippet(r.display, q)}</span>
          </a>`
        ).join('');
      }, 200);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
