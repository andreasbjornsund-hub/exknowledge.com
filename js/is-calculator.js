/* Intrinsic safety loop calculator (entity concept), exknowledge.com.
   Checks one field device + cable against one associated apparatus per IEC 60079-14 / IEC 60079-25:
   Uo<=Ui, Io<=Ii, Po<=Pi, Ci+Cc<=Co, Li+Lc<=Lo (or cable L/R <= Lo/Ro when Li is negligible),
   with the mixed-circuit rule (Li and Ci both > 1 % of Lo and Co -> use 50 % of Lo and Co; halved Co capped
   at 600 nF for IIC and 1 uF for IIB). Inputs are kept in the URL so a result can be shared. */
(function () {
  var form = document.getElementById('isCalc');
  if (!form) return;
  var out = document.getElementById('isResult');
  var F = ['group', 'uo', 'io', 'po', 'co', 'lo', 'loro', 'ui', 'ii', 'pi', 'ci', 'li', 'len', 'cc', 'lc', 'lr'];

  function num(id) {
    var v = form.elements[id].value.trim().replace(',', '.');
    return v === '' ? null : Number(v);
  }
  function fmt(x, unit) {
    if (x === null || !isFinite(x)) return '–';
    var a = Math.abs(x), d = a >= 100 ? 0 : a >= 10 ? 1 : a >= 1 ? 2 : 3;
    var t = x.toFixed(d);
    if (t.indexOf('.') >= 0) t = t.replace(/0+$/, '').replace(/\.$/, '');   // trim decimals only, never "100" -> "1"
    return t + (unit ?' ' + unit : '');
  }
  function row(label, left, op, right, ok, note) {
    var cls = ok === null ? 'na' : ok ? 'ok' : 'fail';
    var txt = ok === null ? 'Not checked' : ok ? 'Pass' : 'Fail';
    return '<tr class="is-' + cls + '"><th scope="row">' + label + '</th><td>' + left + '</td><td>' + op + '</td><td>' + right +
      '</td><td><span class="is-badge is-badge--' + cls + '">' + txt + '</span>' + (note ? '<br><small>' + note + '</small>' : '') + '</td></tr>';
  }

  function calc() {
    var g = form.elements.group.value;
    var uo = num('uo'), io = num('io'), po = num('po'), co = num('co'), lo = num('lo'), loro = num('loro');
    var ui = num('ui'), ii = num('ii'), pi = num('pi'), ci = num('ci'), li = num('li');
    var len = num('len'), ccKm = num('cc'), lcKm = num('lc'), lr = num('lr');
    var need = [uo, io, co, lo, ui, ii, ci, li, len];
    if (need.some(function (x) { return x === null || isNaN(x) || x < 0; })) {
      out.innerHTML = '<p class="is-hint">Enter at least Uo, Io, Co and Lo, Ui, Ii, Ci and Li, and the cable length. Po and Pi are checked when both are given.</p>';
      return;
    }
    ccKm = ccKm === null ? 200 : ccKm; lcKm = lcKm === null ? 1 : lcKm;
    var cc = ccKm * len / 1000 / 1000;          // nF/km * m -> uF
    var lc = lcKm * len / 1000;                  // mH/km * m -> mH
    var ciUF = ci / 1000, liMH = li / 1000;      // nF -> uF, uH -> mH
    var mixed = ciUF > 0.01 * co && liMH > 0.01 * lo;
    var coEff = co, loEff = lo, capNote = '';
    if (mixed) {
      coEff = co / 2; loEff = lo / 2;
      var cap = g === 'IIC' ? 0.6 : g === 'IIB' ? 1 : null;
      if (cap !== null && coEff > cap) { coEff = cap; capNote = ' (halved value capped at ' + fmt(cap * 1000, 'nF') + ' for ' + g + ')'; }
    }
    var cTot = ciUF + cc, lTot = liMH + lc;
    var okU = uo <= ui, okI = io <= ii;
    var okP = (po === null || pi === null) ? null : po <= pi;
    var okC = cTot <= coEff;
    var okL = lTot <= loEff, lNote = '';
    if (!okL && loro !== null && lr !== null && li === 0 && !mixed) {
      okL = lr <= loro;
      lNote = 'Inductance checked with the L/R method: cable L/R ' + fmt(lr, 'µH/Ω') + ' vs Lo/Ro ' + fmt(loro, 'µH/Ω') + '.';
    }
    var all = okU && okI && okC && okL && okP !== false;
    var maxLenC = ccKm > 0 ? (coEff - ciUF) * 1e6 / ccKm : Infinity;       // m
    var maxLenL = lcKm > 0 ? (loEff - liMH) * 1000 / lcKm : Infinity;      // m
    var maxLen = Math.max(0, Math.min(maxLenC, maxLenL));

    var h = '<p class="is-verdict ' + (all ? 'is-verdict--ok' : 'is-verdict--fail') + '" role="status">' +
      (all ? 'The loop meets the entity parameters' + (okP === null ? ' (power not checked)' : '') + '.'
           : 'The loop does not meet the entity parameters. See the failed checks below.') + '</p>';
    if (mixed) h += '<p class="callout">Mixed circuit: the field device has both Ci (' + fmt(ci, 'nF') + ') and Li (' + fmt(li, 'µH') +
      ') above 1 % of Co and Lo, so 50 % of Co and Lo is used' + capNote + ': Co ' + fmt(coEff, 'µF') + ', Lo ' + fmt(loEff, 'mH') + '.</p>';
    h += '<div class="table-wrap"><table class="is-table"><thead><tr><th scope="col">Check</th><th scope="col">Associated apparatus</th><th scope="col"></th><th scope="col">Field device + cable</th><th scope="col">Result</th></tr></thead><tbody>' +
      row('Voltage', 'Uo ' + fmt(uo, 'V'), '≤', 'Ui ' + fmt(ui, 'V'), okU) +
      row('Current', 'Io ' + fmt(io, 'mA'), '≤', 'Ii ' + fmt(ii, 'mA'), okI) +
      row('Power', 'Po ' + fmt(po, 'mW'), '≤', 'Pi ' + fmt(pi, 'mW'), okP, okP === null ? 'Enter Po and Pi to check power.' : '') +
      row('Capacitance', 'Co ' + fmt(coEff, 'µF'), '≥', 'Ci + Cc = ' + fmt(ciUF, 'µF') + ' + ' + fmt(cc, 'µF') + ' = ' + fmt(cTot, 'µF'), okC) +
      row('Inductance', 'Lo ' + fmt(loEff, 'mH'), '≥', 'Li + Lc = ' + fmt(liMH, 'mH') + ' + ' + fmt(lc, 'mH') + ' = ' + fmt(lTot, 'mH'), okL, lNote) +
      '</tbody></table></div>';
    h += '<p>Cable: ' + fmt(len, 'm') + ' at ' + fmt(ccKm, 'nF/km') + ' and ' + fmt(lcKm, 'mH/km') + '. ' +
      (isFinite(maxLen) ? 'With these cable values, capacitance and inductance allow up to about <strong>' + fmt(maxLen, 'm') + '</strong> of cable.' : '') + '</p>';
    out.innerHTML = h;
  }

  function toUrl() {
    var q = new URLSearchParams();
    F.forEach(function (k) { var v = form.elements[k].value.trim(); if (v !== '') q.set(k, v); });
    history.replaceState(null, '', location.pathname + '?' + q.toString() + location.hash);
  }
  var q = new URLSearchParams(location.search);
  F.forEach(function (k) { if (q.has(k)) form.elements[k].value = q.get(k); });
  form.addEventListener('input', function () { calc(); toUrl(); });
  form.addEventListener('submit', function (e) { e.preventDefault(); calc(); toUrl(); });
  var ex = document.getElementById('isExample');
  if (ex) ex.addEventListener('click', function () {
    var v = { group: 'IIC', uo: '28', io: '93', po: '650', co: '0.083', lo: '4.2', loro: '', ui: '30', ii: '100', pi: '750', ci: '5', li: '10', len: '200', cc: '200', lc: '1', lr: '' };
    F.forEach(function (k) { form.elements[k].value = v[k]; });
    calc(); toUrl();
  });
  var pr = document.getElementById('isPrint');
  if (pr) pr.addEventListener('click', function () { window.print(); });
  calc();
})();
