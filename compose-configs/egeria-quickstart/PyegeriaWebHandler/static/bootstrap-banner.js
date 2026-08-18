/* SPDX-License-Identifier: Apache-2.0
 * Copyright Contributors to the ODPi Egeria project.
 *
 * bootstrap-banner.js — self-initializing "Reinitializing Portal" banner.
 * No framework dependency (plain DOM) so it works identically on React SPAs
 * (type-explorer.html, egeria-overview.html, ...) and plain-JS pages
 * (local-dashboards.html, governance-metrics.html). Polls
 * GET /api/bootstrap/status (bootstrap_monitor_handler.py) and shows/hides a
 * fixed-position banner while `reinitializing` is true — the repository was
 * reset and Dr.Egeria bootstrap docs are being re-run automatically, so some
 * data may be briefly missing or slow to load.
 *
 * Include with a single <script src="/static/bootstrap-banner.js?v=..."></script>
 * tag — nothing else to wire up per page.
 */
(function () {
  var POLL_MS = 4000;
  var el = null;

  function ensureBanner() {
    if (el) return el;
    el = document.createElement('div');
    el.id = '_bootstrap-banner';
    el.style.cssText = [
      'position:fixed', 'top:0', 'left:0', 'right:0', 'z-index:99999',
      'background:#f5b74e', 'color:#1a1a2e', 'font-family:system-ui,-apple-system,sans-serif',
      'font-size:.82rem', 'font-weight:600', 'text-align:center',
      'padding:7px 14px', 'display:none', 'box-shadow:0 2px 8px rgba(0,0,0,.25)',
    ].join(';');
    document.body.appendChild(el);
    return el;
  }

  function poll() {
    fetch('/api/bootstrap/status')
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) {
        var banner = ensureBanner();
        if (d && d.reinitializing) {
          banner.textContent = '🔄 ' + (d.message || 'Reinitializing Portal — some data may be missing or slow');
          banner.style.display = 'block';
        } else {
          banner.style.display = 'none';
        }
      })
      .catch(function () { /* status endpoint unreachable — leave banner as-is, don't spam errors */ });
    setTimeout(poll, POLL_MS);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', poll);
  } else {
    poll();
  }
})();
