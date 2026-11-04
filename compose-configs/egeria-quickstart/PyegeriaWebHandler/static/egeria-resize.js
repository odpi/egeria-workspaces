/* SPDX-License-Identifier: Apache-2.0
 * Copyright Contributors to the ODPi Egeria project.
 *
 * egeria-resize.js — user-resizable widths for every portal page (owner rule:
 * "all column/window widths should be user changeable"). Plain JS, no React,
 * so it works on the React SPAs and the plain-DOM pages alike. Load it with a
 * <script> on any page; it needs nothing else.
 *
 * It inserts NO elements: everything is done with document-level pointer
 * listeners that look at where the pointer is, so React-rendered markup is
 * never disturbed (React only diffs the style keys it set itself).
 *
 *   1. Table columns — every <table> with header cells. Drag a header cell's
 *      right edge; double-click that edge to reset the table's widths.
 *      Opt out with data-no-col-resize on the table or an ancestor.
 *   2. Layout grids — elements matching the selectors a page registers with
 *      EgeriaResize.grids('.g-2, .detail-grid'). Drag the gap between two
 *      columns; double-click it to reset. A grid that has collapsed to one
 *      column (responsive breakpoint) is left alone.
 *   3. Edge panes — elements matching EgeriaResize.edges('.drawer', 'left'):
 *      drag the given edge (e.g. a right-hand drawer's left edge).
 *
 * Widths are remembered per page in localStorage (keys start
 * "egeria-resize:"), and reapplied when the element (re)appears.
 */
(function () {
  'use strict';
  if (window.EgeriaResize) return;

  var EDGE = 6;          // px either side of a boundary that grabs it
  var MIN_COL = 40;      // narrowest table column
  var MIN_PANE = 160;    // narrowest grid column / pane
  var PREFIX = 'egeria-resize:' + location.pathname + ':';

  var gridSelectors = [];
  var edgeSpecs = [];    // { selector, side }

  function load(key) {
    try { return JSON.parse(localStorage.getItem(PREFIX + key) || 'null'); } catch (e) { return null; }
  }
  function save(key, val) {
    try {
      if (val == null) localStorage.removeItem(PREFIX + key);
      else localStorage.setItem(PREFIX + key, JSON.stringify(val));
    } catch (e) {}
  }

  /* ── Tables ───────────────────────────────────────────────────────────── */

  function headerRow(table) {
    var row = table.tHead && table.tHead.rows[table.tHead.rows.length - 1];
    if (!row) {
      var first = table.rows && table.rows[0];
      if (first && first.cells.length && first.cells[0].tagName === 'TH') row = first;
    }
    return row && row.cells.length > 1 ? row : null;
  }

  function tableKey(row) {
    var names = [];
    for (var i = 0; i < row.cells.length; i++) names.push((row.cells[i].textContent || '').trim().slice(0, 24));
    return 'table:' + names.join('|');
  }

  function tableOptedOut(table) {
    return !!table.closest('[data-no-col-resize]');
  }

  function freezeTable(table, row) {
    var widths = [];
    for (var i = 0; i < row.cells.length; i++) widths.push(Math.round(row.cells[i].getBoundingClientRect().width));
    applyTableWidths(table, row, widths);
    return widths;
  }

  function applyTableWidths(table, row, widths) {
    if (!widths || widths.length !== row.cells.length) return false;
    var total = 0;
    for (var i = 0; i < widths.length; i++) {
      row.cells[i].style.width = widths[i] + 'px';
      row.cells[i].style.boxSizing = 'border-box';
      total += widths[i];
    }
    table.style.tableLayout = 'fixed';
    table.style.width = total + 'px';
    table.style.minWidth = '';
    table.setAttribute('data-egeria-resized', '1');
    return true;
  }

  function resetTable(table, row) {
    for (var i = 0; i < row.cells.length; i++) { row.cells[i].style.width = ''; }
    table.style.tableLayout = '';
    table.style.width = '';
    table.removeAttribute('data-egeria-resized');
    save(tableKey(row), null);
  }

  // The header cell whose right edge is under the pointer, if any.
  function tableEdgeAt(e) {
    var cell = e.target && e.target.closest && e.target.closest('th, td');
    if (!cell) return null;
    var row = cell.parentElement;
    var table = cell.closest('table');
    if (!table || tableOptedOut(table)) return null;
    var hrow = headerRow(table);
    if (!hrow || hrow !== row) return null;
    var r = cell.getBoundingClientRect();
    var idx = cell.cellIndex;
    if (e.clientX >= r.right - EDGE && e.clientX <= r.right + EDGE && idx < row.cells.length) {
      return { table: table, row: row, idx: idx };
    }
    if (e.clientX <= r.left + EDGE && idx > 0) return { table: table, row: row, idx: idx - 1 };
    return null;
  }

  /* ── Grids ────────────────────────────────────────────────────────────── */

  function gridColumns(el) {
    var cs = getComputedStyle(el);
    if (cs.display !== 'grid' && cs.display !== 'inline-grid') return null;
    var cols = cs.gridTemplateColumns.split(' ').map(parseFloat).filter(function (n) { return !isNaN(n); });
    if (cols.length < 2) return null;
    return { cols: cols, gap: parseFloat(cs.columnGap) || 0, left: el.getBoundingClientRect().left + parseFloat(cs.paddingLeft || 0) };
  }

  function gridKey(el) {
    var sel = el.getAttribute('data-resize-key');
    if (sel) return 'grid:' + sel;
    for (var s = 0; s < gridSelectors.length; s++) {
      var all = document.querySelectorAll(gridSelectors[s]);
      for (var i = 0; i < all.length; i++) if (all[i] === el) return 'grid:' + gridSelectors[s] + '#' + i;
    }
    return null;
  }

  function matchesAny(el, selectors) {
    for (var i = 0; i < selectors.length; i++) { try { if (el.matches(selectors[i])) return true; } catch (e) {} }
    return false;
  }

  // The gap (between column i and i+1) under the pointer, for a registered grid.
  function gridGapAt(e) {
    if (!gridSelectors.length) return null;
    var el = e.target;
    // The gap belongs to the grid container itself, but tolerate a direct child edge.
    if (!el || !el.matches) return null;
    if (!matchesAny(el, gridSelectors)) {
      el = el.parentElement;
      if (!el || !matchesAny(el, gridSelectors)) return null;
    }
    var g = gridColumns(el);
    if (!g) return null;
    var x = g.left;
    for (var i = 0; i < g.cols.length - 1; i++) {
      x += g.cols[i];
      if (e.clientX >= x - EDGE && e.clientX <= x + g.gap + EDGE) return { el: el, idx: i, g: g };
      x += g.gap;
    }
    return null;
  }

  function applyGrid(el, fracs) {
    if (!fracs) return;
    if (!('__egOrigCols' in el)) el.__egOrigCols = el.style.gridTemplateColumns;
    el.style.gridTemplateColumns = fracs.map(function (f) { return 'minmax(0, ' + f.toFixed(4) + 'fr)'; }).join(' ');
  }

  function unapplyGrid(el) {
    if ('__egOrigCols' in el) el.style.gridTemplateColumns = el.__egOrigCols;
  }

  // Apply saved fractions only while the page's own layout (its CSS, media
  // queries and inline style) gives the grid the same number of columns, so a
  // responsive collapse to fewer columns still happens on narrow windows.
  function syncGrid(el) {
    var k = gridKey(el), fr = k && load(k);
    unapplyGrid(el);
    if (!fr) return;
    var natural = gridColumns(el);
    if (natural && natural.cols.length === fr.length) applyGrid(el, fr);
  }

  /* ── Edge panes ───────────────────────────────────────────────────────── */

  function edgeAt(e) {
    for (var i = 0; i < edgeSpecs.length; i++) {
      var spec = edgeSpecs[i];
      var els = document.querySelectorAll(spec.selector);
      for (var j = 0; j < els.length; j++) {
        var r = els[j].getBoundingClientRect();
        if (!r.width || e.clientY < r.top || e.clientY > r.bottom) continue;
        var x = spec.side === 'left' ? r.left : r.right;
        if (Math.abs(e.clientX - x) <= EDGE) return { el: els[j], spec: spec, key: 'edge:' + spec.selector + '#' + j };
      }
    }
    return null;
  }

  /* ── Pointer handling ─────────────────────────────────────────────────── */

  var hoverEl = null;
  function setHover(el) {
    if (hoverEl === el) return;
    if (hoverEl) hoverEl.style.cursor = hoverEl.__egPrevCursor || '';
    hoverEl = el;
    if (el) { el.__egPrevCursor = el.style.cursor; el.style.cursor = 'col-resize'; }
  }

  var drag = null;

  function hit(e) {
    var t = tableEdgeAt(e);
    if (t) return { kind: 'table', t: t, hoverEl: t.row.cells[t.idx] };
    var g = gridGapAt(e);
    if (g) return { kind: 'grid', g: g, hoverEl: g.el };
    var p = edgeAt(e);
    if (p) return { kind: 'edge', p: p, hoverEl: p.el };
    return null;
  }

  document.addEventListener('mousemove', function (e) {
    if (drag) { drag.move(e); return; }
    var h = hit(e);
    setHover(h ? h.hoverEl : null);
  }, true);

  document.addEventListener('mousedown', function (e) {
    if (e.button !== 0) return;
    var h = hit(e);
    if (!h) return;
    e.preventDefault();
    e.stopPropagation();
    var startX = e.clientX;
    if (h.kind === 'table') {
      var t = h.t, widths = freezeTable(t.table, t.row), start = widths[t.idx];
      drag = { move: function (ev) {
        widths[t.idx] = Math.max(MIN_COL, Math.round(start + ev.clientX - startX));
        applyTableWidths(t.table, t.row, widths);
      }, done: function () { save(tableKey(t.row), widths); } };
    } else if (h.kind === 'grid') {
      var g = h.g, cols = g.g.cols.slice(), a = cols[g.idx], b = cols[g.idx + 1], total = 0;
      cols.forEach(function (c) { total += c; });
      drag = { move: function (ev) {
        var d = ev.clientX - startX;
        d = Math.max(MIN_PANE - a, Math.min(b - MIN_PANE, d));
        cols[g.idx] = a + d; cols[g.idx + 1] = b - d;
        applyGrid(g.el, cols.map(function (c) { return c / total * cols.length; }));
      }, done: function () {
        var k = gridKey(g.el);
        if (k) save(k, cols.map(function (c) { return c / total * cols.length; }));
      } };
    } else {
      var p = h.p, w0 = p.el.getBoundingClientRect().width;
      drag = { move: function (ev) {
        var d = ev.clientX - startX;
        var w = p.spec.side === 'left' ? w0 - d : w0 + d;
        w = Math.max(MIN_PANE, Math.min(window.innerWidth - 40, w));
        p.el.style.width = Math.round(w) + 'px';
        p.el.style.maxWidth = 'none';
      }, done: function () { save(p.key, Math.round(p.el.getBoundingClientRect().width)); } };
    }
    document.body.style.userSelect = 'none';
  }, true);

  document.addEventListener('mouseup', function () {
    if (!drag) return;
    drag.done();
    drag = null;
    document.body.style.userSelect = '';
  }, true);

  // Double-click a boundary to reset to the page's own layout.
  document.addEventListener('dblclick', function (e) {
    var h = hit(e);
    if (!h) return;
    e.preventDefault();
    if (h.kind === 'table') resetTable(h.t.table, h.t.row);
    else if (h.kind === 'grid') { var k = gridKey(h.g.el); if (k) save(k, null); unapplyGrid(h.g.el); }
    else { h.p.el.style.width = ''; h.p.el.style.maxWidth = ''; save(h.p.key, null); }
  }, true);

  /* ── Reapply saved widths as elements (re)appear ──────────────────────── */

  var pending = false;
  function restoreAll() {
    pending = false;
    var tables = document.querySelectorAll('table:not([data-egeria-resized])');
    for (var i = 0; i < tables.length; i++) {
      if (tableOptedOut(tables[i])) continue;
      var row = headerRow(tables[i]);
      if (!row) continue;
      var saved = load(tableKey(row));
      if (saved) applyTableWidths(tables[i], row, saved);
    }
    gridSelectors.forEach(function (sel) {
      var els = document.querySelectorAll(sel);
      for (var j = 0; j < els.length; j++) { if (!els[j].__egSynced) { els[j].__egSynced = true; syncGrid(els[j]); } }
    });
    edgeSpecs.forEach(function (spec) {
      var els = document.querySelectorAll(spec.selector);
      for (var j = 0; j < els.length; j++) {
        if (els[j].style.width) continue;
        var w = load('edge:' + spec.selector + '#' + j);
        if (w) { els[j].style.width = Math.min(w, window.innerWidth - 40) + 'px'; els[j].style.maxWidth = 'none'; }
      }
    });
  }
  function schedule() { if (!pending) { pending = true; setTimeout(restoreAll, 120); } }

  function start() {
    restoreAll();
    if (window.MutationObserver) new MutationObserver(schedule).observe(document.body, { childList: true, subtree: true });
    var rt = null;
    window.addEventListener('resize', function () {
      clearTimeout(rt);
      rt = setTimeout(function () {
        gridSelectors.forEach(function (sel) { document.querySelectorAll(sel).forEach(syncGrid); });
      }, 150);
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();

  window.EgeriaResize = {
    grids: function (selectors) {
      String(selectors).split(',').map(function (s) { return s.trim(); }).filter(Boolean).forEach(function (s) {
        if (gridSelectors.indexOf(s) === -1) gridSelectors.push(s);
      });
      schedule();
    },
    edges: function (selector, side) { edgeSpecs.push({ selector: selector, side: side === 'right' ? 'right' : 'left' }); schedule(); },
    reset: function () {
      try { Object.keys(localStorage).forEach(function (k) { if (k.indexOf(PREFIX) === 0) localStorage.removeItem(k); }); } catch (e) {}
    },
  };
})();
