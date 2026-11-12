/* Test runner for static/egeria-table.js, used by tests/test_egeria_table_js.py.
 *
 * Usage: node egeria_table_harness.js <module path>  (a JSON request on stdin)
 *   {"op": "html", "result": {...}, "link": true|false}  -> {"html": "..."}
 *   {"op": "attach", "result": {...}, "clicks": ["more:0", "sub:0", ...]} -> the toggles' states
 *
 * Node has no DOM (no jsdom in the image or on the host). "attach" builds a
 * deliberately small fake one from the rendered HTML: just the elements that
 * carry data-et-more / data-et-sub / data-et-sub-row, which is all attach()
 * and its click handler touch.
 */
'use strict';
const fs = require('fs');
const T = require(process.argv[2]);
const req = JSON.parse(fs.readFileSync(0, 'utf8'));

const linkBuilder = (el) => (el && el.guid ? '/egeria-explorer?guid=' + encodeURIComponent(el.guid) : null);

function html() {
  if (req.hrefs) return T.renderHtml(req.result, { linkBuilder: (el) => req.hrefs[el.guid] });
  return T.renderHtml(req.result, req.link ? { linkBuilder } : {});
}

class El {
  constructor(tag, attrs) {
    this.tagName = tag.toUpperCase(); this.attrs = Object.assign({}, attrs); this.textContent = attrs.__text || '';
    delete this.attrs.__text; this.parentNode = null; this.previousElementSibling = null; this.nextElementSibling = null;
    const self = this;
    this.classList = {
      toggle(c, on) {
        const set = new Set((self.attrs.class || '').split(/\s+/).filter(Boolean));
        if (on === undefined ? !set.has(c) : on) set.add(c); else set.delete(c);
        self.attrs.class = [...set].join(' ');
      },
    };
  }
  getAttribute(n) { return n in this.attrs ? this.attrs[n] : null; }
  setAttribute(n, v) { this.attrs[n] = String(v); }
  removeAttribute(n) { delete this.attrs[n]; }
}

function attachScenario() {
  const s = html();
  const listeners = [];
  const els = [];
  const root = {
    ownerDocument: null,
    addEventListener: (t, fn) => listeners.push(fn),
    removeEventListener: (t, fn) => { const i = listeners.indexOf(fn); if (i >= 0) listeners.splice(i, 1); },
    querySelectorAll: () => [],
    querySelector: (sel) => {
      const m = /data-et-sub-row="(\d+)"/.exec(sel);
      return els.find((e) => m && e.getAttribute('data-et-sub-row') === m[1]) || null;
    },
  };
  // The clamp box and its "more" button are adjacent siblings in the HTML.
  const more = [];
  const reMore = /<div class="([^"]*et-clamp[^"]*)"[^>]*>[\s\S]*?<\/div><button type="button" class="et-btn" data-et-more aria-expanded="false">more<\/button>/g;
  let m;
  while ((m = reMore.exec(s))) {
    const box = new El('div', { class: m[1] });
    const btn = new El('button', { 'data-et-more': '', 'aria-expanded': 'false', __text: 'more' });
    btn.previousElementSibling = box; box.nextElementSibling = btn; box.parentNode = root; btn.parentNode = root;
    more.push({ box, btn });
  }
  const subs = [];
  const reSub = /<button type="button" class="et-btn" data-et-sub="(\d+)" aria-expanded="false">([^<]*)<\/button>/g;
  while ((m = reSub.exec(s))) {
    const btn = new El('button', { 'data-et-sub': m[1], 'aria-expanded': 'false', __text: m[2] });
    btn.parentNode = root;
    const row = new El('tr', { 'data-et-sub-row': m[1], hidden: '' });
    els.push(row);
    subs.push({ btn, row });
  }
  const off = T.attach(root, {});
  for (const c of req.clicks || []) {
    const [kind, i] = c.split(':');
    const target = kind === 'more' ? more[+i].btn : subs[+i].btn;
    listeners.slice().forEach((fn) => fn({ target }));
  }
  off();
  return {
    listenersLeft: listeners.length,
    more: more.map(({ box, btn }) => ({ open: /\bet-open\b/.test(box.attrs.class), label: btn.textContent, expanded: btn.getAttribute('aria-expanded') })),
    subs: subs.map(({ btn, row }) => ({ hidden: row.getAttribute('hidden') !== null, label: btn.textContent, expanded: btn.getAttribute('aria-expanded') })),
  };
}

try {
  const out = req.op === 'attach' ? attachScenario() : { html: html() };
  process.stdout.write(JSON.stringify(Object.assign({ ok: true }, out)));
} catch (e) {
  process.stdout.write(JSON.stringify({ ok: false, error: String(e && e.stack || e) }));
}
