/* ExKnowledge forms: one sender, field-level validation, sending/success/failure states.
   Every form posts to Web3Forms (JSON API) and is delivered to the site inbox (FormSubmit until its 2026-09-30 outage).
   Form actions in HTML are "#": the address never appears in the markup.
   Usage:
     <form data-exk-form data-subject="…" data-success="…"> … </form>   (generic)
     onsubmit="submitPopup(event)" / submitQuestion / submitNewsletter  (topic-page CTAs)
   See DESIGN.md → Forms. */
(function () {
  // The inbox address is not in the page: the Web3Forms access key (public by design) maps to it.
  var W3F_KEY = '930572e9-b94e-4d18-9c2b-25999a09ef0f';
  var ENDPOINT = 'https://api.web3forms.com/submit';
  var TIMEOUT_MS = 15000;
  var PDF = '/downloads/atex-iecex-pocket-guide.pdf';
  var LANG = (document.documentElement.getAttribute('lang') || 'en').slice(0, 2);
  if (LANG === 'nb' || LANG === 'nn') LANG = 'no';
  var M = {
    en: { sending: 'Sending…', required: 'Please fill in this field.', email: 'Please enter a valid email address, like name@company.com.', fail: 'Could not send. Check your connection and try again.', ok: 'Thanks, we received it.' },
    de: { sending: 'Wird gesendet…', required: 'Bitte füllen Sie dieses Feld aus.', email: 'Bitte geben Sie eine gültige E-Mail-Adresse ein, z. B. name@firma.de.', fail: 'Senden fehlgeschlagen. Bitte prüfen Sie Ihre Verbindung und versuchen Sie es erneut.', ok: 'Danke, wir haben es erhalten.' },
    no: { sending: 'Sender…', required: 'Fyll ut dette feltet.', email: 'Skriv inn en gyldig e-postadresse, for eksempel navn@firma.no.', fail: 'Kunne ikke sende. Sjekk tilkoblingen og prøv igjen.', ok: 'Takk, vi har mottatt det.' },
    da: { sending: 'Sender…', required: 'Udfyld dette felt.', email: 'Indtast en gyldig e-mailadresse, fx navn@firma.dk.', fail: 'Kunne ikke sende. Tjek forbindelsen, og prøv igen.', ok: 'Tak, vi har modtaget det.' },
    sv: { sending: 'Skickar…', required: 'Fyll i det här fältet.', email: 'Ange en giltig e-postadress, till exempel namn@foretag.se.', fail: 'Det gick inte att skicka. Kontrollera anslutningen och försök igen.', ok: 'Tack, vi har tagit emot det.' },
    fi: { sending: 'Lähetetään…', required: 'Täytä tämä kenttä.', email: 'Anna kelvollinen sähköpostiosoite, esim. nimi@yritys.fi.', fail: 'Lähetys epäonnistui. Tarkista yhteys ja yritä uudelleen.', ok: 'Kiitos, vastaanotimme sen.' },
    es: { sending: 'Enviando…', required: 'Rellene este campo.', email: 'Introduzca un correo válido, por ejemplo nombre@empresa.com.', fail: 'No se pudo enviar. Compruebe su conexión e inténtelo de nuevo.', ok: 'Gracias, lo hemos recibido.' },
    nl: { sending: 'Verzenden…', required: 'Vul dit veld in.', email: 'Vul een geldig e-mailadres in, bijvoorbeeld naam@bedrijf.nl.', fail: 'Verzenden mislukt. Controleer uw verbinding en probeer het opnieuw.', ok: 'Bedankt, we hebben het ontvangen.' },
    pt: { sending: 'A enviar…', required: 'Preencha este campo.', email: 'Introduza um e-mail válido, por exemplo nome@empresa.pt.', fail: 'Não foi possível enviar. Verifique a ligação e tente novamente.', ok: 'Obrigado, recebemos.' },
    it: { sending: 'Invio…', required: 'Compila questo campo.', email: 'Inserisci un indirizzo email valido, ad esempio nome@azienda.it.', fail: 'Invio non riuscito. Controlla la connessione e riprova.', ok: 'Grazie, lo abbiamo ricevuto.' },
    ar: { sending: 'جارٍ الإرسال…', required: 'يرجى ملء هذا الحقل.', email: 'يرجى إدخال بريد إلكتروني صالح، مثل name@company.com.', fail: 'تعذّر الإرسال. تحقّق من الاتصال وحاول مرة أخرى.', ok: 'شكرًا، لقد استلمناه.' }
  };
  var T = M[LANG] || M.en;
  var uid = 0;

  /* ---------- Field validation ---------- */
  function fieldError(field) {
    if (field.disabled || field.type === 'hidden' || field.type === 'submit' || field.type === 'button') return '';
    var v = (field.value || '').trim();
    if (field.required && !v && field.type !== 'checkbox') return T.required;
    if (field.type === 'checkbox' && field.required && !field.checked) return T.required;
    if (v && field.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) return T.email;
    return '';
  }
  function showError(field, msg) {
    var id = field.getAttribute('data-err-id');
    var el = id && document.getElementById(id);
    if (!msg) {
      field.removeAttribute('aria-invalid');
      if (el) el.hidden = true;
      return;
    }
    if (!el) {
      id = 'exk-err-' + (++uid);
      el = document.createElement('p');
      el.className = 'field-error';
      el.id = id;
      field.setAttribute('data-err-id', id);
      var anchor = field.closest('.cta-row, .footer-nl-form, .cta-form') === field.form ? field.form : field;
      if (anchor === field.form) anchor.parentNode.insertBefore(el, anchor.nextSibling); else field.insertAdjacentElement('afterend', el);
      var d = field.getAttribute('aria-describedby');
      field.setAttribute('aria-describedby', (d ? d + ' ' : '') + id);
    }
    el.textContent = msg;
    el.hidden = false;
    field.setAttribute('aria-invalid', 'true');
  }
  function validate(form) {
    var firstBad = null;
    [].forEach.call(form.elements, function (f) {
      if (!f.name && f.type !== 'email') return;
      var msg = fieldError(f);
      showError(f, msg);
      if (msg && !firstBad) firstBad = f;
    });
    if (firstBad) firstBad.focus();
    return !firstBad;
  }
  function wire(form) {
    if (form.__exk) return;
    form.__exk = true;
    form.noValidate = true;
    form.addEventListener('input', function (e) {
      if (e.target.getAttribute('aria-invalid') === 'true') showError(e.target, fieldError(e.target));
    });
    form.addEventListener('focusout', function (e) {
      if (e.target.value && e.target.form === form) showError(e.target, fieldError(e.target));
    });
  }

  /* ---------- Status message ---------- */
  function statusFor(form, id) {
    var el = id ? document.getElementById(id) : form.nextElementSibling;
    if (!el || !(el.classList.contains('form-status') || el.classList.contains('cta-ok') || id)) {
      el = document.createElement('p');
      el.className = 'form-status';
      form.parentNode.insertBefore(el, form.nextSibling);
    }
    el.classList.add('form-status');
    el.setAttribute('role', 'status');
    el.setAttribute('aria-live', 'polite');
    if (!el.dataset.ok) el.dataset.ok = el.textContent.trim() || form.getAttribute('data-success') || T.ok;
    return el;
  }
  function setStatus(el, kind, text) {
    el.classList.remove('form-status--ok', 'form-status--error');
    el.classList.add(kind === 'ok' ? 'form-status--ok' : 'form-status--error');
    el.setAttribute('role', kind === 'ok' ? 'status' : 'alert');
    el.textContent = text;
    el.hidden = false;
    el.style.display = 'block';
  }

  /* ---------- Sending ---------- */
  function collect(form, extra) {
    var data = {};
    [].forEach.call(form.elements, function (f) {
      if (!f.name || f.disabled || f.type === 'submit' || f.name.charAt(0) === '_') return;   // no service-specific hidden fields
      if ((f.type === 'checkbox' || f.type === 'radio') && !f.checked) return;
      data[f.name] = f.value;
    });
    data.access_key = W3F_KEY;
    data.from_name = 'exknowledge.com';
    data.page = location.href;
    for (var k in extra) data[k] = extra[k];
    if (data._subject) { data.subject = data._subject; delete data._subject; }
    return data;
  }
  function send(form, opts) {
    opts = opts || {};
    wire(form);
    var status = statusFor(form, opts.statusId);
    if (!validate(form)) return Promise.resolve(false);
    var btn = form.querySelector('[type=submit]');
    var label = btn ? btn.innerHTML : '';
    if (btn) { btn.disabled = true; btn.setAttribute('aria-busy', 'true'); btn.textContent = T.sending; }
    form.setAttribute('aria-busy', 'true');
    status.hidden = true;
    var subject = opts.subject || form.getAttribute('data-subject') || (form.querySelector('[name=_subject]') || {}).value || 'ExKnowledge form';
    var ctrl = window.AbortController ? new AbortController() : null;
    var timer = ctrl ? setTimeout(function () { ctrl.abort(); }, TIMEOUT_MS) : null;   // never hang on 'Sending…'
    return fetch(ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(collect(form, Object.assign({ _subject: subject }, opts.extra || {}))),
      signal: ctrl ? ctrl.signal : undefined
    }).then(function (r) { clearTimeout(timer); return r.json(); }).then(function (j) {
      if (!j || String(j.success) !== 'true') throw new Error((j && (j.message || (j.body && j.body.message))) || 'send failed');
      if (btn) { btn.innerHTML = label; btn.disabled = false; btn.removeAttribute('aria-busy'); }
      form.removeAttribute('aria-busy');
      setStatus(status, 'ok', status.dataset.ok);
      if (opts.hideOnSuccess !== false) form.hidden = true;
      if (opts.onSuccess) opts.onSuccess();
      return true;
    }).catch(function (err) {
      clearTimeout(timer); if (window.console) console.warn('Form not sent:', err && err.message);
      if (btn) { btn.innerHTML = label; btn.disabled = false; btn.removeAttribute('aria-busy'); }
      form.removeAttribute('aria-busy');
      setStatus(status, 'error', T.fail);
      if (opts.onFailure) opts.onFailure();
      return false;
    });
  }
  function download() {
    var a = document.createElement('a');
    a.href = PDF; a.download = 'ATEX-IECEx-Pocket-Guide-ExKnowledge.pdf';
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
  }
  window.EXK = window.EXK || {};
  window.EXK.sendForm = send;
  window.EXK.downloadGuide = download;

  /* ---------- Topic-page CTAs (inline onsubmit handlers) ---------- */
  window.submitNewsletter = function (e) {
    e.preventDefault();
    send(e.target, { subject: 'ExKnowledge newsletter signup', statusId: 'nlOk', onSuccess: function () { try { localStorage.setItem('exk_nl', '1'); } catch (x) { } } });
  };
  window.submitQuestion = function (e) {
    e.preventDefault();
    var f = e.target;
    send(f, { subject: 'ExKnowledge question from ' + ((f.email && f.email.value) || 'a reader'), statusId: 'askOk' });
  };
  window.submitPopup = function (e) {
    e.preventDefault();
    send(e.target, {
      subject: 'ExKnowledge cheat sheet PDF request', statusId: 'popupOk',
      onSuccess: function () {
        try { localStorage.setItem('exk_popup', '1'); } catch (x) { }
        download();
        setTimeout(hidePopup, 4000);
      }
    });
  };

  /* ---------- Scroll popup ---------- */
  var popup;
  function hidePopup() {
    if (!popup) return;
    popup.classList.remove('visible');
    popup.setAttribute('inert', '');
    popup.setAttribute('aria-hidden', 'true');
    if (window.EXK.closeDialog) window.EXK.closeDialog(popup);
  }
  window.dismissPopup = function () {
    hidePopup();
    try { localStorage.setItem('exk_popup', '1'); } catch (x) { }
  };
  function consentOpen() {
    var b = document.getElementById('hag-consent-banner');
    return !!(b && b.offsetParent !== null);
  }
  function showPopup() {
    if (consentOpen()) { setTimeout(showPopup, 1500); return; }
    popup.removeAttribute('inert');
    popup.removeAttribute('aria-hidden');
    popup.classList.add('visible');
    if (window.EXK.openDialog) window.EXK.openDialog(popup, { focus: false, modal: false, onClose: window.dismissPopup });
  }
  function initPopup() {
    popup = document.getElementById('scrollPopup');
    if (!popup) return;
    popup.setAttribute('role', 'dialog');
    popup.setAttribute('aria-labelledby', 'scrollPopupTitle');
    var h = popup.querySelector('h4, h2, h3'); if (h) h.id = 'scrollPopupTitle';
    var input = popup.querySelector('input[type=email]');
    if (input && !input.getAttribute('aria-label')) input.setAttribute('aria-label', 'Email address');
    popup.setAttribute('inert', '');
    popup.setAttribute('aria-hidden', 'true');
    var seen = false;
    try { seen = !!localStorage.getItem('exk_popup'); } catch (x) { }
    if (seen) return;
    var triggered = false;
    window.addEventListener('scroll', function () {
      if (triggered) return;
      if ((window.scrollY + window.innerHeight) / document.documentElement.scrollHeight > 0.6) {
        triggered = true;
        setTimeout(showPopup, 800);
      }
    }, { passive: true });
  }

  function init() {
    document.querySelectorAll('form[data-exk-form], #popupForm, #nlForm, form[onsubmit*="submitQuestion"]').forEach(wire);
    document.querySelectorAll('form[data-exk-form]').forEach(function (f) {
      f.addEventListener('submit', function (e) {
        e.preventDefault();
        var cb = f.getAttribute('data-on-success');
        send(f, { onSuccess: cb && window[cb] ? window[cb] : null, hideOnSuccess: f.getAttribute('data-keep') === null });
      });
    });
    initPopup();
    var subscribed = false;
    try { subscribed = !!localStorage.getItem('exk_nl'); } catch (x) { }
    var nlf = document.getElementById('nlForm');
    if (subscribed && nlf) {
      nlf.hidden = true;
      var ok = document.getElementById('nlOk');
      if (ok) { ok.classList.add('form-status', 'form-status--ok'); ok.style.display = 'block'; }
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
