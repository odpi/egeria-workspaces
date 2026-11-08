/* egeria-not-measured.js — plain vanilla JS, no React/JSX. Loadable from any
 * page via a bare <script src="/static/egeria-not-measured.js"> tag.
 *
 * One renderer for the report-spec results (POST /api/report-specs/execute)
 * that say "we did not get this number", so no page shows such a result as
 * an answer: a 0, a blank cell, an empty chart, "No results" or raw JSON.
 *
 * pyegeria's exec_report_spec returns two such shapes:
 *
 *   1. {kind:"absent", content, absence:{state, sentence, reason, ...},
 *       detail?, unmeasured?, envelope?}
 *      The value is not established or does not apply (ISSUE-171, already
 *      in pyegeria 6.2.26), or a scalar/chart result holds a count that was
 *      not measured (odpi/egeria-python #555). The chart is withheld on
 *      purpose. Render the headline, the sentence and any lower bound —
 *      never a KPI number, never an empty chart.
 *
 *   2. {kind:"json"|"empty", ..., unmeasured:[{count, reason, at_least}]}
 *      (#555) A table/dict result whose unmeasured cells are null. Show
 *      those cells as "not measured" (never blank or 0) and list each note
 *      under the result.
 *
 * Results without these keys (all other pyegeria output) are untouched:
 * every helper here answers false / "" / [] for them, so callers keep their
 * old rendering byte-for-byte.
 */
(function (global) {
  'use strict';

  var NULL_TEXT = 'not measured';

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  function isAbsent(result) {
    return !!(result && typeof result === 'object' && result.kind === 'absent');
  }

  // The notes naming each count that was not measured; [] when there are none
  // (every pre-#555 result).
  function notes(result) {
    var u = result && typeof result === 'object' ? result.unmeasured : null;
    if (!Array.isArray(u)) return [];
    return u.filter(function (n) { return n && typeof n === 'object'; });
  }

  function hasUnmeasured(result) { return notes(result).length > 0; }

  // The absence state, from the declared absence first, then the envelope.
  function absenceState(result) {
    if (!result) return '';
    var a = result.absence;
    if (a && a.state) return String(a.state);
    var e = result.envelope;
    if (e && e.state) return String(e.state);
    return result.state ? String(result.state) : '';
  }

  // The headline. "Does not apply" is a different claim from "not measured",
  // so it keeps its own words; everything else that reaches kind:"absent" is
  // a value nobody established.
  function headline(result) {
    var st = absenceState(result);
    if (st === 'not_applicable') return 'Does not apply';
    if (st === 'not_permitted') return 'Not measured — not permitted';
    return 'Not measured';
  }

  // The sentence under the headline: pyegeria's own words.
  function sentence(result) {
    if (!result) return '';
    if (typeof result.content === 'string' && result.content) return result.content;
    var a = result.absence;
    if (a && a.sentence) return String(a.sentence);
    var e = result.envelope;
    if (e && e.reason) return String(e.reason);
    return '';
  }

  // "at least N" for each note that saw a lower bound. One note: "at least
  // 500"; several: "at least 500 (Asset); at least 500 (Process)".
  function atLeastText(result) {
    var bounded = notes(result).filter(function (n) {
      return n.at_least !== null && n.at_least !== undefined && n.at_least !== '';
    });
    if (!bounded.length) return '';
    if (bounded.length === 1) return 'at least ' + bounded[0].at_least;
    return bounded.map(function (n) {
      return 'at least ' + n.at_least + (n.count ? ' (' + n.count + ')' : '');
    }).join('; ');
  }

  function noteLine(n) {
    var count = n.count != null ? String(n.count) : 'a count';
    return n.reason ? count + ': ' + n.reason : count;
  }

  // The footnote listing each note; "" when there are none.
  function footnoteHtml(result) {
    var ns = notes(result);
    if (!ns.length) return '';
    return '<div class="nm-footnote" data-nm="footnote">'
      + '<span class="nm-footnote-head">Not measured' + (ns.length > 1 ? ' (' + ns.length + ' counts)' : '') + ':</span>'
      + '<ul>' + ns.map(function (n) { return '<li>' + esc(noteLine(n)) + '</li>'; }).join('') + '</ul>'
      + '</div>';
  }

  // The whole kind:"absent" block: headline, sentence, lower bound, and the
  // partial result (if any) collapsed. No number in KPI style, no chart.
  function absentHtml(result) {
    var html = '<div class="nm-absent" data-nm="absent">'
      + '<div class="nm-headline">' + esc(headline(result)) + '</div>';
    var s = sentence(result);
    if (s) html += '<div class="nm-sentence">' + esc(s) + '</div>';
    var al = atLeastText(result);
    if (al) html += '<div class="nm-atleast">' + esc(al) + '</div>';
    if (result && result.detail !== undefined && result.detail !== null) {
      html += '<details class="nm-detail"><summary>Partial result</summary><pre>'
        + esc(JSON.stringify(result.detail, nullReplacer, 2)) + '</pre></details>';
    }
    return html + '</div>';
  }

  // JSON.stringify replacer for a result with unmeasured counts: a null is a
  // count that was not measured, so say so instead of printing "null".
  function nullReplacer(_key, value) { return value === null ? NULL_TEXT : value; }

  // How a table cell shows a value. `unmeasured` true: null reads "not
  // measured"; false: exactly the caller's old rendering (blank).
  function cellText(value, unmeasured) {
    if (value === null || value === undefined) return unmeasured && value === null ? NULL_TEXT : '';
    if (typeof value === 'object') return JSON.stringify(value, unmeasured ? nullReplacer : null);
    return String(value);
  }

  // Styles shared by every page; injected once, using each page's own
  // palette variables with fallbacks.
  function injectStyles() {
    if (typeof document === 'undefined' || document.getElementById('egeria-nm-styles')) return;
    var css = ''
      + '.nm-absent{padding:4px 0;}'
      + '.nm-headline{font-size:1.05rem;font-weight:650;color:var(--amber,#f5b74e);letter-spacing:.01em;}'
      + '.nm-sentence{font-size:.8rem;line-height:1.45;color:var(--text,inherit);margin-top:4px;white-space:normal;}'
      + '.nm-atleast{font-size:.76rem;color:var(--muted,var(--dim,#8b93a7));margin-top:4px;font-style:italic;}'
      + '.nm-detail{margin-top:6px;font-size:.74rem;color:var(--muted,var(--dim,#8b93a7));}'
      + '.nm-detail summary{cursor:pointer;}'
      + '.nm-detail pre{white-space:pre-wrap;font-size:.72rem;margin-top:4px;}'
      + '.nm-footnote{font-size:.72rem;color:var(--muted,var(--dim,#8b93a7));margin-top:6px;white-space:normal;font-family:inherit;}'
      + '.nm-footnote-head{font-weight:600;color:var(--amber,#f5b74e);}'
      + '.nm-footnote ul{margin:2px 0 0 16px;padding:0;}'
      + '.nm-cell{font-style:italic;color:var(--amber,#f5b74e);}';
    var el = document.createElement('style');
    el.id = 'egeria-nm-styles';
    el.textContent = css;
    (document.head || document.documentElement).appendChild(el);
  }

  var api = {
    NULL_TEXT: NULL_TEXT,
    isAbsent: isAbsent,
    notes: notes,
    hasUnmeasured: hasUnmeasured,
    headline: headline,
    sentence: sentence,
    atLeastText: atLeastText,
    footnoteHtml: footnoteHtml,
    absentHtml: absentHtml,
    nullReplacer: nullReplacer,
    cellText: cellText,
    injectStyles: injectStyles,
  };

  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  global.EgeriaNotMeasured = api;
  if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', injectStyles);
    else injectStyles();
  }
})(typeof window !== 'undefined' ? window : this);
