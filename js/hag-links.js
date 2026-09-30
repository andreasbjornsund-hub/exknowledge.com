/* HAG network link tracking: one GA4 event per click on a link that leaves the site.
   link_type: xshielder | network | competitor | external; placement: content | menu | footer.
   Installed by scripts/hag_link_policy.py (2026-09-30). */
(function () {
  var NETWORK = ["exknowledge.com", "explosionproofradios.com", "explosionprooftablets.com", "hazardousareaguide.com",
                 "intrinsicallysafeheadsets.com", "intrinsicallysafephones.com"];
  var COMPETITORS = ["xciel.com", "atexxo.com", "ecom-ex.com", "pepperl-fuchs.com", "isafe-mobile.com", "bartec.com",
                     "bartec.de", "aegex.com", "conquest-ex.com", "getac.com", "zebra.com", "pixavi.com", "atex-shop.de",
                     "atexshop.com", "intrinsicallysafestore.com", "sonimtech.com", "cyrus.com", "cyrus-technology.de",
                     "smart-ex.com", "tabex.com", "ruggedexphones.com"];
  var here = location.hostname.replace(/^www\./, "");
  function is(host, list) {
    for (var i = 0; i < list.length; i++) {
      if (host === list[i] || host.slice(-(list[i].length + 1)) === "." + list[i]) return true;
    }
    return false;
  }
  function type(host) {
    if (is(host, ["xshielder.com"])) return "xshielder";
    if (host === here) return "internal";
    if (NETWORK.indexOf(host) > -1) return "network";
    if (is(host, COMPETITORS)) return "competitor";
    return "external";
  }
  document.addEventListener("click", function (e) {
    var a = e.target && e.target.closest ? e.target.closest("a[href]") : null;
    if (!a) return;
    var u;
    try { u = new URL(a.href, location.href); } catch (err) { return; }
    if (u.protocol !== "http:" && u.protocol !== "https:") return;
    var host = u.hostname.replace(/^www\./, "");
    var t = type(host);
    if (t === "internal") return;
    var placement = a.closest("footer") ? "footer" : (a.closest("header, nav") ? "menu" : "content");
    if (typeof window.gtag === "function") {
      window.gtag("event", "network_link_click", {
        link_url: u.href, link_domain: host, link_type: t, placement: placement,
        page_path: location.pathname, transport_type: "beacon"
      });
    }
  }, true);
})();
