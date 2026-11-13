/* SPDX-License-Identifier: Apache-2.0
 * Copyright Contributors to the ODPi Egeria project.
 *
 * infra-health-panel.js — the read-only "Shared infrastructure" block in Admin → Data Initialization
 * (local-admin.html, demo-admin.html), beside "Last Egeria reset". Data: GET /api/admin/infra-health.
 *
 * The check itself runs on the HOST (`egeria-upgrade-reset infra-check --record`): the Portal has no
 * Docker socket and must not get one, so this block only shows the latest recorded row.
 *
 * Absence is an answer:
 *   - a row older than staleAfterSeconds (30 min) is greyed, says "last checked <time>: not current",
 *     and shows no green;
 *   - no row: "not checked yet (run `egeria-upgrade-reset infra-check --record` on the host)";
 *   - unreadable: "Shared-infrastructure health not read: <reason>".
 *   - alert email: the recorded run's `alerting` ("not configured (unset: …)" in amber, or configured
 *     with this run's outcome and when mail was last sent); missing is said as "not reported".
 * The Portal's own reachability of the shared ports is a different fact (it says nothing about restart
 * policies) and is shown separately, labelled "reachable from the Portal now".
 *
 *   InfraHealthPanel.load(elementId)
 */
(function (global) {
  'use strict';

  function esc(s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  var COLOURS = { PASS: 'var(--ok,#4ade80)', FAIL: 'var(--err,#f87171)', WARN: 'var(--amber,#f5b74e)' };

  function badge(verdict, stale) {
    var c = stale ? 'var(--muted,#8b93a7)' : (COLOURS[verdict] || 'var(--muted,#8b93a7)');
    return '<span class="ih-badge" style="border-color:' + c + ';color:' + c + '">' + esc(verdict || '?') + '</span>';
  }

  function serviceHtml(s, stale) {
    var name = esc(s.service) + (s.container ? ' <span class="ih-note">(' + esc(s.container) + ')</span>' : '');
    return '<li>' + badge(s.verdict, stale) + ' <b>' + name + '</b>'
      + '<div class="ih-note">' + esc(s.words || '') + '</div></li>';
  }

  function openlineageHtml(ol) {
    if (!ol) return '';
    var text = ol.notRead ? ol.notRead
      : 'latest OpenLineage event ' + (ol.latestAt || 'time not read') + ' (offset ' + ol.offset + ')';
    return '<div class="ih-note" style="margin-top:0.3rem">Info: ' + esc(text) + '</div>';
  }

  // The host's alert email, as the recorded run saw it. Missing means that run did not alert (a manual
  // run without --log, or an infra-check older than alerting): said, not left blank.
  function alertingHtml(a) {
    var text, colour;
    if (!a) {
      text = 'not reported by this check (only the scheduled run, with --log, sends alert email)';
      colour = 'var(--muted,#8b93a7)';
    } else if (a.configured === true) {
      text = 'configured (' + (a.route || 'route not said') + ') · this run: ' + (a.outcome || '?')
        + ' · last sent ' + (a.lastSentAt || 'never');
      colour = 'var(--muted,#8b93a7)';
    } else if (a.configured === false) {
      text = a.unset && a.unset.length ? 'not configured (unset: ' + a.unset.join(', ') + '): nothing is mailed'
        : (a.outcome || 'not configured') + ': nothing is mailed';
      colour = 'var(--amber,#f5b74e)';
    } else {
      text = a.outcome || 'state not said';
      colour = 'var(--muted,#8b93a7)';
    }
    return '<div class="ih-note ih-alerting" style="margin-top:0.3rem;color:' + colour + '">Alert email: '
      + esc(text) + '</div>';
  }

  function reachHtml(r) {
    if (!r || !r.ports) return '';
    return '<div class="ih-card ih-reach"><div><b>' + esc(r.label || 'reachable from the Portal now') + '</b>'
      + ' <span class="ih-note">' + esc(r.checkedAt || '') + ': a TCP connection from the Portal\'s container; '
      + 'it says nothing about restart policies.</span></div><ul class="ih-list">'
      + r.ports.map(function (p) {
        return '<li title="' + esc(p.error || '') + '">' + (p.reachable ? '✓' : '✗') + ' ' + esc(p.name)
          + ' <span class="ih-note">' + esc(p.host) + ':' + esc(p.port) + (p.reachable ? '' : ' (' + esc(p.error) + ')') + '</span></li>';
      }).join('') + '</ul></div>';
  }

  function render(el, data) {
    if (!data || data.state === 'not read') {
      el.innerHTML = '<div class="ih-card ih-note">Shared-infrastructure health not read: '
        + esc(data && data.reason || 'no answer') + '</div>' + reachHtml(data && data.reachability);
      return;
    }
    if (data.state === 'none') {
      el.innerHTML = '<div class="ih-card ih-note">' + esc(data.message) + '</div>' + reachHtml(data.reachability);
      return;
    }
    var res = data.result || {};
    var services = res.services || [];
    var stale = data.stale !== false;          // unknown age is not current either
    var head = stale
      ? '<b>last checked ' + esc(data.checkedAt || 'at an unknown time') + ': not current</b>'
        + ' <span class="ih-note">(older than ' + Math.round((data.staleAfterSeconds || 1800) / 60) + ' minutes; '
        + 'run <code>egeria-upgrade-reset infra-check --record</code> on the host)</span>'
      : '<b>Checked ' + esc(data.checkedAt) + '</b>';
    var counts = res.counts || {};
    var sum = ['PASS', 'FAIL', 'WARN', 'EXPECTED STOPPED', 'NOT MEASURED'].filter(function (v) { return counts[v]; })
      .map(function (v) { return counts[v] + ' ' + v.toLowerCase(); }).join(', ');
    el.innerHTML = '<div class="ih-card' + (stale ? ' ih-stale' : '') + '" data-stale="' + (stale ? 'true' : 'false') + '">'
      + '<div>' + head + ' <span class="ih-note">on ' + esc(data.host || '?') + (sum ? ' · ' + esc(sum) : '') + '</span></div>'
      + (services.length ? '<ul class="ih-list">' + services.map(function (s) { return serviceHtml(s, stale); }).join('') + '</ul>'
        : '<div class="ih-note">The recorded check lists no services.</div>')
      + openlineageHtml(res.openlineage) + alertingHtml(res.alerting) + '</div>' + reachHtml(data.reachability);
  }

  function injectStyles() {
    if (typeof document === 'undefined' || document.getElementById('infra-health-styles')) return;
    var el = document.createElement('style');
    el.id = 'infra-health-styles';
    el.textContent = '.ih-card{background:var(--card,var(--bg));border:1px solid var(--border);border-radius:8px;'
      + 'padding:0.6rem 0.8rem;margin-bottom:0.5rem;font-size:0.82rem;overflow-wrap:anywhere}'
      + '.ih-stale{opacity:.6;filter:grayscale(1)}'
      + '.ih-note{color:var(--muted,var(--dim,#8b93a7));font-size:0.76rem;line-height:1.5}'
      + '.ih-list{list-style:none;margin:0.4rem 0 0;padding:0}.ih-list li{margin:0 0 0.35rem}'
      + '.ih-badge{display:inline-block;border:1px solid;border-radius:4px;padding:0 0.3rem;font-size:0.7rem;'
      + 'font-weight:600;min-width:3.2rem;text-align:center}';
    (document.head || document.documentElement).appendChild(el);
  }

  function load(id) {
    injectStyles();
    var el = document.getElementById(id);
    if (!el) return;
    el.innerHTML = '<div class="ih-card ih-note">Loading…</div>';
    fetch('/api/admin/infra-health').then(function (r) {
      if (r.status === 403) return { state: 'not read', reason: 'administrators only' };
      return r.json();
    }).then(function (d) { render(el, d); })
      .catch(function (e) { render(el, { state: 'not read', reason: String(e) }); });
  }

  var api = { load: load, render: render, esc: esc };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  global.InfraHealthPanel = api;
})(typeof window !== 'undefined' ? window : this);
