/* SPDX-License-Identifier: Apache-2.0
 * Copyright Contributors to the ODPi Egeria project.
 *
 * report-spec-source.js: one badge saying where the report spec a run used came from, for the
 * plain-JS pages that run specs (local-dashboards.html, governance-metrics.html). Same four
 * sources, words and colours as Egeria Explorer's Report Specs view (type-explorer.html,
 * RsSourceBadge / _RS_SOURCE_TAG), so it reads as one system.
 *
 * Input: the `specSource` field POST /api/report-specs/execute adds to a run's result
 * ({source, sourceLabel, shadows, shadowedBy}). No specSource, or an unknown source: no badge
 * at all (never a guessed tier).
 *
 *   EgeriaSpecSource.badgeHtml(result.specSource)  -> '<span …>held in Egeria</span>…' or ''
 *   EgeriaSpecSource.blockHtml(result)             -> the badge in a small line, or ''
 */
(function (root) {
  var WORDS = {
    builtin: 'pyegeria built-in',
    egeria:  'held in Egeria',
    local:   'Portal (local)',
    user:    'user spec file',
  };
  var COLORS = { builtin: '#94a3b8', egeria: '#34d399', local: '#60a5fa', user: '#c084fc' };

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function badgeHtml(ss) {
    if (!ss || typeof ss !== 'object' || !WORDS[ss.source]) return '';
    var color = COLORS[ss.source];
    var html = '<span class="eg-spec-source" title="Source: where this report spec definition came from"'
      + ' style="display:inline-block;font-size:.68rem;font-weight:600;padding:1px 7px;border-radius:20px;'
      + 'border:1px solid ' + color + ';color:' + color + ';background:transparent">'
      + esc(ss.sourceLabel || WORDS[ss.source]) + '</span>';
    if (ss.shadows && WORDS[ss.shadows]) {
      html += ' <span class="eg-spec-shadow" style="font-size:.68rem;color:var(--muted,#94a3b8)">'
        + 'shadows the ' + esc(ss.shadows) + ' copy</span>';
    } else if (ss.shadowedBy && WORDS[ss.shadowedBy]) {
      html += ' <span class="eg-spec-shadow" style="font-size:.68rem;color:var(--muted,#94a3b8)">'
        + 'shadowed by the ' + esc(ss.shadowedBy) + ' copy</span>';
    }
    return html;
  }

  function blockHtml(result) {
    var ss = result && typeof result === 'object' ? result.specSource : null;
    var b = badgeHtml(ss);
    return b ? '<div class="eg-spec-source-line" style="margin-top:6px">' + b + '</div>' : '';
  }

  var api = { WORDS: WORDS, COLORS: COLORS, badgeHtml: badgeHtml, blockHtml: blockHtml };
  root.EgeriaSpecSource = api;
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
})(typeof window !== 'undefined' ? window : this);
