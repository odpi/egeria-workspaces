/* diagram-viewer.js — standalone copy of openDiagramViewer() for the pages that
 * do not load static/egeria-shared-ui.js (it needs React at load time):
 * local-dashboards.html and governance-metrics.html. The React pages get the
 * same function from egeria-shared-ui.js — keep the two in step.
 */
/* ── Diagram pop-up viewer (pan + zoom) ───────────────────────────────────────
 *   openDiagramViewer(svgMarkup, title, opts)   opts: { dark: bool }
 * Full-window overlay for any rendered SVG (Mermaid, Vega exports, ...).
 *   drag = pan · wheel / pinch = zoom at the pointer · double-click = fit
 *   + / − / 0 (fit) / 1 (100%) keys · Esc closes
 * Plain DOM, no React, so non-React pages can call it too.
 * diagramExpandButton(getSvg, title, opts) builds the matching "⤢ Expand" button. */
function openDiagramViewer(svgMarkup, title, opts) {
  if (!svgMarkup) return;
  opts = opts || {};
  var old = document.getElementById('egeria-diagram-viewer');
  if (old) old.remove();

  var overlay = document.createElement('div');
  overlay.id = 'egeria-diagram-viewer';
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-label', title || 'Diagram');
  overlay.style.cssText = 'position:fixed;inset:0;z-index:100000;display:flex;flex-direction:column;background:rgba(6,10,18,.94);font-family:inherit;';

  var bar = document.createElement('div');
  bar.style.cssText = 'display:flex;align-items:center;gap:6px;padding:8px 12px;color:#e2e8f0;font-size:13px;flex:0 0 auto;';
  var ttl = document.createElement('div');
  ttl.textContent = title || 'Diagram';
  ttl.style.cssText = 'font-weight:600;margin-right:auto;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;';
  var hint = document.createElement('div');
  hint.textContent = 'drag to pan · scroll to zoom · double-click to fit';
  hint.style.cssText = 'font-size:11px;opacity:.6;margin-right:10px;white-space:nowrap;';
  var pct = document.createElement('div');
  pct.style.cssText = 'min-width:44px;text-align:right;font-size:11px;opacity:.8;font-variant-numeric:tabular-nums;';
  function btn(label, tip, fn) {
    var b = document.createElement('button');
    b.type = 'button'; b.textContent = label; b.title = tip;
    b.style.cssText = 'min-width:30px;font-size:13px;padding:3px 9px;border-radius:4px;border:1px solid #334155;background:#0f172a;color:#e2e8f0;cursor:pointer;';
    b.addEventListener('click', fn);
    return b;
  }
  bar.appendChild(ttl); bar.appendChild(hint); bar.appendChild(pct);

  var stage = document.createElement('div');
  stage.style.cssText = 'position:relative;flex:1 1 auto;overflow:hidden;cursor:grab;touch-action:none;margin:0 12px 12px;border-radius:6px;background:' + (opts.dark ? '#0b111c' : '#ffffff') + ';';
  var content = document.createElement('div');
  content.style.cssText = 'position:absolute;left:0;top:0;transform-origin:0 0;will-change:transform;';
  content.innerHTML = svgMarkup;
  stage.appendChild(content);

  // Give the SVG a fixed natural size: Mermaid emits width="100%" plus a
  // max-width style, which would pin it to the stage width and defeat zoom.
  var svg = content.querySelector('svg');
  var natW = 800, natH = 600;
  if (svg) {
    var vb = (svg.getAttribute('viewBox') || '').split(/[\s,]+/).map(Number);
    if (vb.length === 4 && vb[2] > 0 && vb[3] > 0) { natW = vb[2]; natH = vb[3]; }
    else {
      var bb = svg.getBoundingClientRect();
      if (bb.width > 0 && bb.height > 0) { natW = bb.width; natH = bb.height; }
    }
    svg.style.maxWidth = 'none';
    svg.removeAttribute('width'); svg.removeAttribute('height');
    svg.setAttribute('width', natW); svg.setAttribute('height', natH);
  }

  var s = { k: 1, x: 0, y: 0 };
  var K_MIN = 0.02, K_MAX = 40;
  function apply() {
    content.style.transform = 'translate(' + s.x + 'px,' + s.y + 'px) scale(' + s.k + ')';
    pct.textContent = Math.round(s.k * 100) + '%';
  }
  function fit() {
    var w = stage.clientWidth, h = stage.clientHeight;
    var k = Math.min(w / natW, h / natH) * 0.95;
    s.k = Math.max(K_MIN, Math.min(k, 3));
    s.x = (w - natW * s.k) / 2; s.y = (h - natH * s.k) / 2;
    apply();
  }
  function zoomAt(factor, cx, cy) {
    var k2 = Math.max(K_MIN, Math.min(K_MAX, s.k * factor));
    var f = k2 / s.k;
    s.x = cx - (cx - s.x) * f; s.y = cy - (cy - s.y) * f; s.k = k2;
    apply();
  }
  function zoomCentre(factor) { zoomAt(factor, stage.clientWidth / 2, stage.clientHeight / 2); }
  function actual() {
    var cx = stage.clientWidth / 2, cy = stage.clientHeight / 2;
    zoomAt(1 / s.k, cx, cy);
  }

  bar.appendChild(btn('−', 'Zoom out (-)', function() { zoomCentre(1 / 1.3); }));
  bar.appendChild(btn('+', 'Zoom in (+)', function() { zoomCentre(1.3); }));
  bar.appendChild(btn('Fit', 'Fit to window (0)', fit));
  bar.appendChild(btn('100%', 'Actual size (1)', actual));
  var closeBtn = btn('✕ Close', 'Close (Esc)', close);
  closeBtn.style.marginLeft = '8px';
  bar.appendChild(closeBtn);

  stage.addEventListener('wheel', function(e) {
    e.preventDefault();
    var r = stage.getBoundingClientRect();
    var d = e.deltaMode === 1 ? e.deltaY * 16 : e.deltaY;
    zoomAt(Math.exp(-d * (e.ctrlKey ? 0.01 : 0.0015)), e.clientX - r.left, e.clientY - r.top);
  }, { passive: false });

  var drag = null;
  stage.addEventListener('pointerdown', function(e) {
    if (e.button !== 0) return;
    drag = { x: e.clientX, y: e.clientY, ox: s.x, oy: s.y };
    stage.setPointerCapture(e.pointerId);
    stage.style.cursor = 'grabbing';
  });
  stage.addEventListener('pointermove', function(e) {
    if (!drag) return;
    s.x = drag.ox + (e.clientX - drag.x); s.y = drag.oy + (e.clientY - drag.y);
    apply();
  });
  function endDrag() { drag = null; stage.style.cursor = 'grab'; }
  stage.addEventListener('pointerup', endDrag);
  stage.addEventListener('pointercancel', endDrag);
  stage.addEventListener('dblclick', fit);

  function onKey(e) {
    if (e.key === 'Escape') { e.preventDefault(); close(); }
    else if (e.key === '+' || e.key === '=') zoomCentre(1.3);
    else if (e.key === '-' || e.key === '_') zoomCentre(1 / 1.3);
    else if (e.key === '0') fit();
    else if (e.key === '1') actual();
  }
  function onResize() { fit(); }
  function close() {
    document.removeEventListener('keydown', onKey, true);
    window.removeEventListener('resize', onResize);
    overlay.remove();
    if (prevFocus && prevFocus.focus) { try { prevFocus.focus(); } catch (e) {} }
  }
  var prevFocus = document.activeElement;
  document.addEventListener('keydown', onKey, true);
  window.addEventListener('resize', onResize);

  overlay.appendChild(bar); overlay.appendChild(stage);
  document.body.appendChild(overlay);
  fit();
  closeBtn.focus();
}

/* egeriaAttachExpand(container, title): once a Mermaid/Vega chart has rendered an
 * <svg> into `container`, add a "⤢ Expand" button to its top-right corner that
 * opens the pan/zoom viewer. Safe to call again after a re-render. */
function egeriaAttachExpand(container, title) {
  if (!container || !container.querySelector('svg')) return;
  var old = container.querySelector(':scope > .egeria-expand-btn');
  if (old) old.remove();
  if (getComputedStyle(container).position === 'static') container.style.position = 'relative';
  var b = document.createElement('button');
  b.type = 'button';
  b.className = 'egeria-expand-btn';
  b.textContent = '\u2922 Expand';
  b.title = 'Open larger, with pan and zoom';
  b.style.cssText = 'position:absolute;top:4px;right:4px;z-index:2;font-size:10px;padding:2px 8px;border-radius:4px;border:1px solid var(--border);background:var(--panel);color:var(--accent);cursor:pointer;opacity:.9;';
  b.addEventListener('click', function(e) {
    e.stopPropagation();
    var svg = container.querySelector('svg');
    if (svg) openDiagramViewer(svg.outerHTML, title, { dark: !document.documentElement.classList.contains('light') });
  });
  container.appendChild(b);
}
