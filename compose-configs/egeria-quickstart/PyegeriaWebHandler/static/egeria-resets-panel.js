/* SPDX-License-Identifier: Apache-2.0
 * Copyright Contributors to the ODPi Egeria project.
 *
 * egeria-resets-panel.js — the read-only "Last Egeria reset" block in Admin → Data Initialization
 * (local-admin.html, demo-admin.html). Data: GET /api/admin/egeria-resets, written by the host-only
 * CLI bin/egeria-upgrade-reset. There is deliberately no action here: resetting Egeria needs the
 * host's Docker and the Postgres superuser, which the Portal must not have.
 *
 * Absence is said, never blank: "No reset recorded by egeria-upgrade-reset." for none, and
 * "Reset history not read: <reason>" when the table could not be read.
 *
 *   EgeriaResetsPanel.load(elementId)
 */
(function (global) {
  'use strict';

  function esc(s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }
  function short(d) { return d ? esc(String(d).replace(/^sha256:/, '').slice(0, 12)) : '—'; }
  function bytes(n) {
    if (n == null) return '—';
    var u = ['B', 'KB', 'MB', 'GB'], i = 0, v = Number(n);
    while (v >= 1024 && i < u.length - 1) { v /= 1024; i++; }
    return v.toFixed(i ? 1 : 0) + ' ' + u[i];
  }
  function parse(v) {
    if (v == null) return null;
    if (typeof v === 'string') { try { return JSON.parse(v); } catch (e) { return null; } }
    return v;
  }

  function verifyLine(verify) {
    var v = parse(verify);
    if (!v || !v.checks) return 'not run';
    var c = { PASS: 0, FAIL: 0, 'NOT MEASURED': 0, CHANGED: 0 };
    v.checks.forEach(function (x) { c[x.verdict] = (c[x.verdict] || 0) + 1; });
    return c.PASS + ' pass, ' + c.FAIL + ' fail, ' + c['NOT MEASURED'] + ' not measured'
      + (c.CHANGED ? ', ' + c.CHANGED + ' changed (review)' : '')
      + (v.failed && v.failed.length ? ' (failed: ' + esc(v.failed.join(', ')) + ')' : '');
  }
  function healLine(heal) {
    var h = parse(heal);
    if (!h || !h.families) return 'not run';
    var names = Object.keys(h.families);
    var missing = h.missing || [];
    return names.length + ' batches checked' + (missing.length ? ', still missing: ' + esc(missing.join(', ')) : ', all present')
      + (h.logErrorCount ? '; ' + h.logErrorCount + ' log errors' : '');
  }

  function rowHtml(r, latest) {
    var outcomeColor = r.outcome === 'completed' ? 'var(--ok,#4ade80)' : 'var(--amber,#f5b74e)';
    return '<div class="er-card"' + (latest ? '' : ' style="opacity:.85"') + '>'
      + '<div style="display:flex;flex-wrap:wrap;gap:0.4rem 1rem;align-items:baseline">'
      + '<b>' + esc(r.started_at) + '</b>'
      + '<span style="color:' + outcomeColor + '">' + esc(r.outcome) + '</span>'
      + '<span class="er-note">by ' + esc(r.operator || '?') + ' on ' + esc(r.host || '?') + '</span></div>'
      + '<div class="er-note" style="margin-top:0.3rem;overflow-wrap:anywhere">'
      + 'Image ' + short(r.old_digest) + ' → ' + short(r.new_digest)
      + (r.database ? ' · database <code>' + esc(r.database) + '</code> cleared' : ' · metadata store kept')
      + (r.backup_path ? ' · backup ' + esc(r.backup_path) + ' (' + bytes(r.backup_bytes) + ', sha256 ' + short(r.backup_sha256) + ')' : '')
      + '<br>Heal: ' + healLine(r.heal) + ' · Verify: ' + verifyLine(r.verify) + '</div></div>';
  }

  function render(el, data) {
    if (!data || data.state === 'not read') {
      el.innerHTML = '<div class="er-card er-note">Reset history not read: ' + esc(data && data.reason || 'no answer') + '</div>';
      return;
    }
    if (data.state === 'none' || !data.rows || !data.rows.length) {
      el.innerHTML = '<div class="er-card er-note">' + esc(data.message || 'No reset recorded by egeria-upgrade-reset.') + '</div>';
      return;
    }
    var html = rowHtml(data.rows[0], true);
    if (data.rows.length > 1) {
      html += '<details><summary class="er-note" style="cursor:pointer">Earlier resets (' + (data.rows.length - 1) + ')</summary>'
        + data.rows.slice(1).map(function (r) { return rowHtml(r, false); }).join('') + '</details>';
    }
    el.innerHTML = html;
  }

  function injectStyles() {
    if (typeof document === 'undefined' || document.getElementById('egeria-resets-styles')) return;
    var el = document.createElement('style');
    el.id = 'egeria-resets-styles';
    el.textContent = '.er-card{background:var(--card,var(--bg));border:1px solid var(--border);border-radius:8px;'
      + 'padding:0.6rem 0.8rem;margin-bottom:0.5rem;font-size:0.82rem}'
      + '.er-note{color:var(--muted,var(--dim,#8b93a7));font-size:0.76rem;line-height:1.5}';
    (document.head || document.documentElement).appendChild(el);
  }

  function load(id) {
    injectStyles();
    var el = document.getElementById(id);
    if (!el) return;
    el.innerHTML = '<div class="er-card er-note">Loading…</div>';
    fetch('/api/admin/egeria-resets').then(function (r) {
      if (r.status === 403) return { state: 'not read', reason: 'administrators only' };
      return r.json();
    }).then(function (d) { render(el, d); })
      .catch(function (e) { render(el, { state: 'not read', reason: String(e) }); });
  }

  var api = { load: load, render: render, esc: esc };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  global.EgeriaResetsPanel = api;
})(typeof window !== 'undefined' ? window : this);
