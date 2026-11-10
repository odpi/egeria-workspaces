/* Test harness for static/egeria-resize.js, run by tests/test_egeria_resize_js.py.
 *
 * Node has no DOM here (no jsdom in the image or on the host), so this is a
 * deliberately small fake one: just what egeria-resize.js touches, plus
 *   - fixed table layout: a column's width is its <col>'s inline width if it
 *     has one, else the header cell's inline width, else 100px — so a test
 *     sees whether a drag actually moves the column a user would see;
 *   - real capture/bubble dispatch (window → document → … → target and back)
 *     honouring stopPropagation, so page handlers that stop events are real.
 *
 * Usage: node egeria_resize_harness.js <path to egeria-resize.js> <scenario>
 * Prints one JSON object: { ok: true, ... } or { ok: false, error }.
 */
'use strict';
const fs = require('fs');
const vm = require('vm');

/* ── Fake DOM ───────────────────────────────────────────────────────────── */

class Style {
  constructor() { this._v = {}; }
}
const STYLE_PROPS = ['width', 'minWidth', 'maxWidth', 'tableLayout', 'boxSizing', 'cursor', 'userSelect', 'gridTemplateColumns'];
STYLE_PROPS.forEach((p) => Object.defineProperty(Style.prototype, p, {
  get() { return this._v[p] || ''; }, set(v) { this._v[p] = v == null ? '' : String(v); },
}));

class Target {
  constructor() { this._l = []; }
  addEventListener(type, fn, opt) { this._l.push({ type, fn, capture: opt === true || !!(opt && opt.capture) }); }
  removeEventListener(type, fn, opt) {
    const cap = opt === true || !!(opt && opt.capture);
    this._l = this._l.filter((l) => !(l.type === type && l.fn === fn && l.capture === cap));
  }
  _fire(ev, capturePhase) {
    for (const l of this._l.slice()) {
      if (l.type !== ev.type) continue;
      if (ev.eventPhase === 2 || l.capture === capturePhase) { ev.currentTarget = this; l.fn.call(this, ev); }
      if (ev._stopped) return;
    }
  }
}

class El extends Target {
  constructor(tag, doc) {
    super();
    this.tagName = tag.toUpperCase(); this.nodeType = 1; this.ownerDocument = doc;
    this.children = []; this.parentElement = null; this.style = new Style(); this._attrs = {}; this._text = '';
  }
  appendChild(c) { if (c.parentElement) c.parentElement.removeChild(c); c.parentElement = this; this.children.push(c); this.ownerDocument._mutated(); return c; }
  removeChild(c) { this.children = this.children.filter((x) => x !== c); c.parentElement = null; this.ownerDocument._mutated(); return c; }
  replaceChildren(...cs) { this.children.slice().forEach((c) => this.removeChild(c)); cs.forEach((c) => this.appendChild(c)); }
  get textContent() { return this._text + this.children.map((c) => c.textContent).join(''); }
  set textContent(v) { this._text = String(v); }
  setAttribute(k, v) { this._attrs[k] = String(v); }
  getAttribute(k) { return k in this._attrs ? this._attrs[k] : null; }
  hasAttribute(k) { return k in this._attrs; }
  removeAttribute(k) { delete this._attrs[k]; }
  _matches(sel) {
    sel = sel.trim();
    const attr = /^\[([\w-]+)\]$/.exec(sel);
    if (attr) return this.hasAttribute(attr[1]);
    return this.tagName === sel.toUpperCase();
  }
  matches(sel) { return sel.split(',').some((s) => this._matches(s)); }
  closest(sel) { for (let e = this; e; e = e.parentElement) if (e.matches && e.matches(sel)) return e; return null; }
  _desc(out) { for (const c of this.children) { out.push(c); c._desc(out); } return out; }
  getElementsByTagName(t) { return t === '*' ? this._desc([]) : this._desc([]).filter((e) => e.tagName === t.toUpperCase()); }
  querySelectorAll(sel) { return this._desc([]).filter((e) => e.matches(sel)); }
  querySelector(sel) { return this.querySelectorAll(sel)[0] || null; }
  // table API
  get tHead() { return this.children.find((c) => c.tagName === 'THEAD') || null; }
  get rows() {
    if (this.tagName === 'TABLE') return this.getElementsByTagName('tr').filter((r) => r.closest('table') === this);
    return this.children.filter((c) => c.tagName === 'TR');
  }
  get cells() { return this.children.filter((c) => c.tagName === 'TH' || c.tagName === 'TD'); }
  get cellIndex() { return this.parentElement ? this.parentElement.cells.indexOf(this) : -1; }
  getBoundingClientRect() { return this.ownerDocument._layout(this); }
}

function makeEnv() {
  const win = new Target();
  const doc = new Target();
  doc.readyState = 'complete';
  doc._mutated = () => {};
  doc.createElement = (t) => new El(t, doc);
  const html = new El('html', doc);
  const body = new El('body', doc);
  html.appendChild(body);
  doc.documentElement = html; doc.body = body;
  doc.querySelectorAll = (s) => html.querySelectorAll(s);
  doc.querySelector = (s) => html.querySelector(s);

  // Layout: tables start at x=0, header rows at y=0..20, body rows below.
  function colWidths(table) {
    const head = table.tHead ? table.tHead.rows[table.tHead.rows.length - 1] : table.rows[0];
    const cols = table.getElementsByTagName('col');
    return head.cells.map((c, i) => parseFloat((cols[i] && cols[i].style.width) || c.style.width) || 100);
  }
  doc._layout = (el) => {
    const cell = el.closest('th, td');
    const table = el.closest('table');
    if (!table) return { left: 0, right: 0, top: 0, bottom: 0, width: 0, height: 0 };
    const w = colWidths(table);
    if (!cell) { const tot = w.reduce((a, b) => a + b, 0); return { left: 0, right: tot, top: 0, bottom: 100, width: tot, height: 100 }; }
    const row = cell.parentElement;
    const y = table.rows.indexOf(row) * 20;
    const i = cell.cellIndex;
    const left = w.slice(0, i).reduce((a, b) => a + b, 0);
    const r = { left, right: left + w[i], top: y, bottom: y + 20, width: w[i], height: 20 };
    if (el !== cell) { r.left = r.right - 9; r.width = 9; }   // a handle at the cell's right edge
    return r;
  };

  win.window = win; win.document = doc;
  win.location = { pathname: '/test-page' };
  const store = {};
  win.localStorage = {
    getItem: (k) => (k in store ? store[k] : null),
    setItem: (k, v) => { store[k] = String(v); },
    removeItem: (k) => { delete store[k]; },
  };
  Object.defineProperty(win.localStorage, '_store', { value: store });
  win.innerWidth = 2000;
  win.getComputedStyle = (el) => {
    let cur = 'auto';
    for (let e = el; e; e = e.parentElement) if (e.style.cursor) { cur = e.style.cursor; break; }
    return { cursor: cur, display: 'block', gridTemplateColumns: '', columnGap: '0', paddingLeft: '0' };
  };
  win.setTimeout = setTimeout; win.clearTimeout = clearTimeout;
  win.Date = Date; win.JSON = JSON; win.Math = Math; win.Object = Object; win.String = String; win.parseFloat = parseFloat; win.parseInt = parseInt; win.isNaN = isNaN;
  // MutationObserver: callbacks run when the test calls env.flush().
  const observers = [];
  win.MutationObserver = class { constructor(cb) { this.cb = cb; observers.push(this); } observe() {} };
  doc._mutated = () => { observers.forEach((o) => o.cb([])); };

  function path(target) { const p = []; for (let e = target; e; e = e.parentElement) p.unshift(e); return [win, doc].concat(p); }
  function dispatch(target, type, init) {
    const ev = Object.assign({ type, target, button: 0, buttons: type === 'mouseup' ? 0 : 1, clientX: 0, clientY: 0, defaultPrevented: false, _stopped: false }, init || {});
    ev.preventDefault = () => { ev.defaultPrevented = true; };
    ev.stopPropagation = () => { ev._stopped = true; };
    const p = path(target);
    ev.eventPhase = 1;
    for (let i = 0; i < p.length - 1 && !ev._stopped; i++) p[i]._fire(ev, true);
    if (!ev._stopped) { ev.eventPhase = 2; target._fire(ev, true); }
    ev.eventPhase = 3;
    for (let i = p.length - 2; i >= 0 && !ev._stopped; i--) p[i]._fire(ev, false);
    return ev;
  }
  return { win, doc, body, dispatch, store, wait: (ms) => new Promise((r) => setTimeout(r, ms)) };
}

function load(env, src) {
  const ctx = vm.createContext(env.win);
  vm.runInContext(src, ctx, { filename: 'egeria-resize.js' });
}

function table(env, labels, opts) {
  opts = opts || {};
  const d = env.doc;
  const t = d.createElement('table');
  if (opts.cols) {
    const cg = d.createElement('colgroup');
    labels.forEach(() => { const c = d.createElement('col'); c.style.width = opts.cols + 'px'; cg.appendChild(c); });
    t.appendChild(cg);
  }
  const thead = d.createElement('thead');
  thead.appendChild(headRow(env, labels));
  t.appendChild(thead);
  const tbody = d.createElement('tbody');
  const tr = d.createElement('tr');
  labels.forEach(() => { const td = d.createElement('td'); td.textContent = 'x'; tr.appendChild(td); });
  tbody.appendChild(tr);
  t.appendChild(tbody);
  return t;
}
function headRow(env, labels) {
  const tr = env.doc.createElement('tr');
  labels.forEach((l) => { const th = env.doc.createElement('th'); th.textContent = l; tr.appendChild(th); });
  return tr;
}
function widthsOf(env, t) {
  const head = t.tHead.rows[0];
  return head.cells.map((c) => env.doc._layout(c).width);
}
// Drag the right edge of header cell i by dx, the way a user does.
function drag(env, t, i, dx, target) {
  const cell = t.tHead.rows[0].cells[i];
  const r = cell.getBoundingClientRect();
  const x = r.right - 2;
  const tg = target || cell;
  env.dispatch(tg, 'mousemove', { clientX: x, clientY: 10, buttons: 0 });
  const down = env.dispatch(tg, 'mousedown', { clientX: x, clientY: 10 });
  env.dispatch(tg, 'mousemove', { clientX: x + dx, clientY: 10 });
  env.dispatch(tg, 'mouseup', { clientX: x + dx, clientY: 10 });
  return down;
}

/* ── Scenarios ──────────────────────────────────────────────────────────── */

const scenarios = {
  async plain_drag(env) {
    const t = env.body.appendChild(table(env, ['Name', 'Type', 'Status']));
    drag(env, t, 0, 60);
    return { widths: widthsOf(env, t), marked: t.hasAttribute('data-egeria-resized'), tableWidth: t.style.width,
             saved: env.store['egeria-resize:/test-page:table:Name|Type|Status'] || null };
  },

  // A page's header handler that stops propagation (bubble phase on the th,
  // and React-style on the root container) must not stop the module's drag.
  async stop_propagation(env) {
    const root = env.body.appendChild(env.doc.createElement('div'));
    const t = root.appendChild(table(env, ['Name', 'Type', 'Status']));
    let pageSaw = 0;
    const th = t.tHead.rows[0].cells[0];
    th.addEventListener('mousedown', (e) => { pageSaw++; e.stopPropagation(); });
    root.addEventListener('mousedown', (e) => { pageSaw++; e.stopPropagation(); }, true);
    root.addEventListener('mousemove', (e) => { e.stopPropagation(); }, true);
    root.addEventListener('mouseup', (e) => { e.stopPropagation(); }, true);
    drag(env, t, 0, 60);
    // An ordinary click elsewhere in the header still reaches the page.
    env.dispatch(th, 'mousedown', { clientX: 20, clientY: 10 });
    env.dispatch(th, 'mouseup', { clientX: 20, clientY: 10 });
    return { widths: widthsOf(env, t), pageSawPlainClick: pageSaw };
  },

  // React replaces the header cells of the same <table> for another view.
  async rerender_new_cells(env) {
    const t = env.body.appendChild(table(env, ['Name', 'Type', 'Status']));
    drag(env, t, 0, 60);
    const before = { widths: widthsOf(env, t), tableWidth: t.style.width };
    t.tHead.replaceChildren(headRow(env, ['Engine', 'Service', 'Description', 'Last Refresh']));
    t.children.find((c) => c.tagName === 'TBODY').replaceChildren(headRowAsBody(env, 4));
    await env.wait(200);   // restoreAll is debounced (120 ms)
    const afterRerender = { widths: widthsOf(env, t), marked: t.hasAttribute('data-egeria-resized'), tableWidth: t.style.width };
    drag(env, t, 1, 50);
    const afterDrag = { widths: widthsOf(env, t), tableWidth: t.style.width };
    // Back to the first view: its saved widths come back.
    t.tHead.replaceChildren(headRow(env, ['Name', 'Type', 'Status']));
    t.children.find((c) => c.tagName === 'TBODY').replaceChildren(headRowAsBody(env, 3));
    await env.wait(200);
    const back = { widths: widthsOf(env, t), tableWidth: t.style.width };
    return { before, afterRerender, afterDrag, back };
  },

  // React keeps the same <th> elements but changes their text (same count).
  async rerender_reused_cells(env) {
    const t = env.body.appendChild(table(env, ['Name', 'Type', 'Status']));
    drag(env, t, 0, 60);
    const cells = t.tHead.rows[0].cells;
    cells[0].textContent = 'Engine'; cells[1].textContent = 'Service'; cells[2].textContent = 'Kind';
    env.doc._mutated();
    await env.wait(200);
    const after = { widths: widthsOf(env, t), marked: t.hasAttribute('data-egeria-resized'), cellWidth0: cells[0].style.width };
    drag(env, t, 2, 30);
    return { after, afterDrag: widthsOf(env, t) };
  },

  // A sort indicator in the header text does not change the saved key.
  async sort_marks(env) {
    const t = env.body.appendChild(table(env, ['Name ↑', 'Type ⇅']));
    drag(env, t, 0, 40);
    return { keys: Object.keys(env.store) };
  },

  // A table with its own resize handles (egeria-shared-ui.js colResizeHandle:
  // React state + <colgroup>) is left to the page.
  async page_owned_handles(env) {
    const t = env.body.appendChild(table(env, ['Name', 'Type', 'Status'], { cols: 150 }));
    let pageDowns = 0;
    t.tHead.rows[0].cells.forEach((th) => {
      const h = env.doc.createElement('div');
      h.style.cursor = 'col-resize';
      h.addEventListener('mousedown', (e) => { pageDowns++; e.stopPropagation(); });
      th.appendChild(h);
    });
    // Saved widths from before the fix must not be re-applied either.
    env.store['egeria-resize:/test-page:table:Name|Type|Status'] = JSON.stringify([300, 100, 100]);
    env.doc._mutated();
    await env.wait(200);
    const restored = t.hasAttribute('data-egeria-resized');
    const handle = t.tHead.rows[0].cells[0].children[0];
    const down = drag(env, t, 0, 60, handle);
    // On the cell's own edge, outside the handle, the module also stays out.
    drag(env, t, 1, 60);
    return { pageDowns, restored, marked: t.hasAttribute('data-egeria-resized'), moduleTookIt: down.defaultPrevented, widths: widthsOf(env, t) };
  },

  // A plain <colgroup> with widths (no handles): the drag must write the
  // <col> widths too, or fixed layout ignores it.
  async colgroup_no_handles(env) {
    const t = env.body.appendChild(table(env, ['Name', 'Type', 'Status'], { cols: 150 }));
    drag(env, t, 0, 60);
    const afterDrag = widthsOf(env, t);
    const ev = env.dispatch(t.tHead.rows[0].cells[0], 'dblclick', { clientX: afterDrag[0] - 2, clientY: 10 });
    return { afterDrag, afterReset: widthsOf(env, t), colWidths: t.getElementsByTagName('col').map((c) => c.style.width), marked: t.hasAttribute('data-egeria-resized'), resetHandled: ev.defaultPrevented };
  },

  // The mouseup never reaches the page (released outside the window): the
  // next mousemove with no button down ends the drag instead of resizing.
  async lost_mouseup(env) {
    const t = env.body.appendChild(table(env, ['Name', 'Type', 'Status']));
    const cell = t.tHead.rows[0].cells[0];
    const x = cell.getBoundingClientRect().right - 2;
    env.dispatch(cell, 'mousedown', { clientX: x, clientY: 10 });
    env.dispatch(cell, 'mousemove', { clientX: x + 40, clientY: 10 });
    env.dispatch(cell, 'mousemove', { clientX: x + 400, clientY: 10, buttons: 0 });
    return { widths: widthsOf(env, t), saved: !!env.store['egeria-resize:/test-page:table:Name|Type|Status'] };
  },
};

function headRowAsBody(env, n) {
  const tr = env.doc.createElement('tr');
  for (let i = 0; i < n; i++) { const td = env.doc.createElement('td'); td.textContent = 'x'; tr.appendChild(td); }
  return tr;
}

(async () => {
  const [src, name] = process.argv.slice(2);
  try {
    const env = makeEnv();
    load(env, fs.readFileSync(src, 'utf8'));
    const out = await scenarios[name](env);
    console.log(JSON.stringify(Object.assign({ ok: true }, out)));
  } catch (e) {
    console.log(JSON.stringify({ ok: false, error: String(e && e.stack || e) }));
  }
})();
