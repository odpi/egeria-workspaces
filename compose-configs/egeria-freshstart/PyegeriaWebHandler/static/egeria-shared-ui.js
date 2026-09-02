/* SPDX-License-Identifier: Apache-2.0
 * Copyright Contributors to the ODPi Egeria project.
 *
 * egeria-shared-ui.js — shared presentational components used by both SPAs
 * (Egeria Explorer + Tech Catalog). Loaded via <script> AFTER React/ReactDOM and
 * BEFORE each SPA's app script, so these are plain globals referenced by name.
 * Scope: robust clipboard + the mermaid diagram family + useResizable +
 *        markdown renderer + glossary tree + Egeria Feedback widgets.
 * Depends on host globals: React, window.mermaid; CSS: .mermaid-wrap;
 * CSS vars: --accent --border --panel --muted --dim --md-code-bg.
 * Feedback widgets use bare fetch() against /api/egeria-feedback/* (cookie auth).
 * Extracted verbatim from type-explorer.html (canonical) — keep in sync there.
 */

var _MERMAID_FIELD_LABELS = {
  mermaidGraph:                          'Context Diagram',
  iscImplementationMermaidGraph:         'ISC Implementation',
  informationSupplyChainMermaidGraph:    'Supply Chain Graph',
  edgeMermaidGraph:                      'Asset Edge Graph',
  anchorMermaidGraph:                    'Anchored Graph',
  specificationMermaidGraph:             'Specification Graph',
  solutionBlueprintMermaidGraph:         'Blueprint Graph',
  solutionSubcomponentMermaidGraph:      'Subcomponent Graph',
  actionMermaidGraph:                    'Action Graph',
  localLineageGraph:                     'Local Lineage',
  fieldLevelLineageGraph:                'Field-Level Lineage',
  governanceActionProcessMermaidGraph:   'Governance Action Process',
  organizationTreeMermaidGraph:          'Organization Tree',
  collectionMermaidMindMap:              'Collection Mind Map',
  zoneProfileMermaidPieChart:            'Zone Profile',
  zoneProfileAnchoredMermaidPieChart:    'Zone Anchored Profile',
  zoneProfileAllPieChart:                'Zone All Assets',
  userAccountTypeProfileMermaidPieChart: 'Account Type Profile',
  userAccountStatusMermaidPieChart:      'Account Status',
};

var _MERMAID_SECTION_FIELDS = new Set(['mermaidGraph', 'anchorMermaidGraph']);

function _execCopyFallback(text) {
  try {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.position = 'fixed';
    ta.style.top = '-9999px';
    ta.style.left = '-9999px';
    document.body.appendChild(ta);
    ta.select();
    ta.setSelectionRange(0, ta.value.length);
    var ok = document.execCommand('copy');
    document.body.removeChild(ta);
    return ok;
  } catch (e) { return false; }
}

function copyToClipboard(text) {
  if (navigator.clipboard && window.isSecureContext) {
    return navigator.clipboard.writeText(text)
      .then(function() { return true; })
      .catch(function() { return _execCopyFallback(text); });
  }
  return Promise.resolve(_execCopyFallback(text));
}

function _isMermaidKey(k) {
  var kl = k.toLowerCase();
  return kl.indexOf('mermaid') !== -1 || /(?:graph|mindmap|piechart|chart)$/i.test(k);
}

function _mermaidLabel(k) {
  return _MERMAID_FIELD_LABELS[k]
    || k.replace(/Mermaid/g, '').replace(/([a-z0-9])([A-Z])/g, '$1 $2').replace(/\s+/g, ' ').trim()
        .replace(/^./, function(c) { return c.toUpperCase(); });
}

function MermaidDiagram({ code }) {
  const ref = React.useRef(null);
  const [errMsg, setErrMsg] = React.useState('');
  const [copyState, setCopyState] = React.useState('');  // '' | 'ok' | 'fail'

  React.useEffect(function() {
    if (!code) return;
    setErrMsg('');
    if (ref.current) ref.current.innerHTML = '';

    function doRender() {
      try { window.mermaid.initialize({ startOnLoad: false, theme: 'default', securityLevel: 'loose' }); } catch(_) {}
      var id = 'mmd' + Math.random().toString(36).slice(2);
      window.mermaid.render(id, code)
        .then(function(result) {
          if (ref.current) ref.current.innerHTML = result.svg || '';
        })
        .catch(function(err) {
          console.warn('Mermaid render failed:', err);
          setErrMsg(String(err));
        });
    }

    if (window.mermaid && window.mermaid.render) {
      doRender();
    } else {
      var attempts = 0;
      var timer = setInterval(function() {
        if (window.mermaid && window.mermaid.render) {
          clearInterval(timer); doRender();
        } else if (++attempts > 40) {
          clearInterval(timer);
          setErrMsg('Mermaid library not loaded — CDN may be unreachable');
        }
      }, 150);
      return function() { clearInterval(timer); };
    }
  }, [code]);

  var copyBtn = code && React.createElement('button', {
    onClick: function(e) {
      e.stopPropagation();
      Promise.resolve(copyToClipboard(code)).then(function(ok) {
        setCopyState(ok ? 'ok' : 'fail');
        setTimeout(function() { setCopyState(''); }, 2000);
      });
    },
    title: copyState === 'fail' ? 'Copy needs https:// or localhost' : 'Copy Mermaid source to clipboard',
    style: { position: 'absolute', top: 4, right: 4, zIndex: 2, fontSize: 10, padding: '2px 8px',
             borderRadius: 4, border: '1px solid var(--border)', background: 'var(--panel)',
             color: copyState === 'ok' ? '#34d399' : copyState === 'fail' ? '#f87171' : 'var(--accent)', cursor: 'pointer', opacity: 0.9 }
  }, copyState === 'ok' ? '✓ Copied' : copyState === 'fail' ? '✕ Copy failed' : '⧉ Copy source');

  return React.createElement('div', { style: { position: 'relative' } },
    copyBtn,
    errMsg
      ? React.createElement('div', null,
          React.createElement('div', { style: { fontSize: 11, color: '#f87171', padding: '4px 0 6px' } }, '⚠ ' + errMsg),
          React.createElement('pre', { style: { fontSize: 11, color: 'var(--muted)', background: 'rgba(255,255,255,.04)', padding: '8px 12px', borderRadius: 4, overflowX: 'auto', whiteSpace: 'pre-wrap', margin: 0, border: '1px solid var(--border)' } }, code)
        )
      : React.createElement('div', { ref: ref, className: 'mermaid-wrap' })
  );
}

function DiagramPanelFromData({ code, label }) {
  const [visible, setVisible] = React.useState(false);
  if (!code) return null;
  var btnStyle = { fontSize: 12, padding: '3px 10px', borderRadius: 4, border: '1px solid var(--border)', background: 'rgba(96,165,250,.08)', color: 'var(--accent)', cursor: 'pointer' };
  return React.createElement('div', { style: { margin: '4px 0' } },
    React.createElement('button', { onClick: function() { setVisible(function(v) { return !v; }); }, style: btnStyle },
      visible ? ('▦ Hide ' + label) : ('▦ Show ' + label)
    ),
    visible && React.createElement(MermaidDiagram, { code: code })
  );
}

function AvailableMermaidDiagrams({ data, skip }) {
  if (!data) return null;
  var skipSet = skip || _MERMAID_SECTION_FIELDS;
  var panels = [];
  Object.keys(data).forEach(function(k) {
    if (skipSet.has(k)) return;
    var code = data[k];
    if (typeof code !== 'string' || !code.trim() || code.toLowerCase().indexOf('no ') === 0) return;
    if (!_isMermaidKey(k)) return;
    panels.push(React.createElement(DiagramPanelFromData, { key: k, code: code, label: _mermaidLabel(k) }));
  });
  if (panels.length === 0) return null;
  return React.createElement('div', { style: { margin: '8px 0' } }, panels);
}

function useResizable(initialPx, min, max) {
  min = (min === undefined) ? 100 : min;
  max = (max === undefined) ? 900 : max;
  const [width, setWidth] = React.useState(initialPx);
  const widthRef = React.useRef(width);
  widthRef.current = width;
  const onMouseDown = React.useCallback(function(e) {
    e.preventDefault();
    var startX = e.clientX;
    var startW = widthRef.current;
    function onMove(mv) {
      setWidth(Math.max(min, Math.min(max, startW + mv.clientX - startX)));
    }
    function onUp() {
      document.removeEventListener('mousemove', onMove);
      document.removeEventListener('mouseup', onUp);
    }
    document.addEventListener('mousemove', onMove);
    document.addEventListener('mouseup', onUp);
  }, [min, max]);
  return [width, onMouseDown];
}

// Per-column sibling of useResizable, for drag-to-resize <table> columns (e.g.
// report/DictResultView output). Keyed by column key rather than a single
// scalar so an arbitrary number of columns can be resized independently.
// initialWidths: { [colKey]: px }. Returns [widths, onColMouseDown(colKey)] —
// call onColMouseDown(key) from a column's resize-handle onMouseDown.
function useResizableColumns(initialWidths, min, max) {
  min = (min === undefined) ? 60 : min;
  max = (max === undefined) ? 800 : max;
  const [widths, setWidths] = React.useState(initialWidths);
  const widthsRef = React.useRef(widths);
  widthsRef.current = widths;
  const onColMouseDown = React.useCallback(function(colKey) {
    return function(e) {
      e.preventDefault();
      e.stopPropagation();
      var startX = e.clientX;
      var startW = widthsRef.current[colKey];
      // No stored width yet (first drag on this column) — fall back to the <th>'s
      // actual rendered width so the drag starts from where the column visually is,
      // instead of leaving startW undefined (undefined + delta = NaN, which React
      // silently drops as an invalid style.width — the handle would then appear to
      // do nothing at all).
      if (startW === undefined || startW === null) {
        var thEl = e.currentTarget && e.currentTarget.parentElement;
        startW = thEl ? thEl.offsetWidth : 150;
      }
      function onMove(mv) {
        var next = Math.max(min, Math.min(max, startW + mv.clientX - startX));
        setWidths(function(prev) { return Object.assign({}, prev, { [colKey]: next }); });
      }
      function onUp() {
        document.removeEventListener('mousemove', onMove);
        document.removeEventListener('mouseup', onUp);
      }
      document.addEventListener('mousemove', onMove);
      document.addEventListener('mouseup', onUp);
    };
  }, [min, max]);
  return [widths, onColMouseDown];
}

// Thin drag handle for a resizable <th> — absolutely positioned strip on the
// column's right edge, cursor: col-resize. Same visual language as
// ResizeDivider below, but sized/positioned to sit inline inside a <th>
// rather than as a sibling flex divider.
function ColResizeHandle({ onMouseDown }) {
  return React.createElement('div', {
    onMouseDown: onMouseDown,
    style: {
      position: 'absolute', top: 0, right: 0, bottom: 0, width: 6,
      cursor: 'col-resize', userSelect: 'none', zIndex: 1,
    },
  });
}

/* ── Glossary tree (shared by Egeria Explorer + Tech Catalog) ────────────────
 * One twistie-tree implementation for both SPAs. GlossaryTreeNode lazy-loads
 * its child folders + terms via the injected fetchJson(path) -> Promise<json>,
 * via the injected fetchJson(path) wrapper (both SPAs now use the shared
 * token-aware egeriaFetch). onSelect(obj, isFolder) fires on row click.
 * Depends on host CSS classes .tree-item / .badge / .type-name and CSS vars
 * --accent --muted --dim. */
function GlossaryTermRow({ term, depth, selected, onSelect, selection }) {
  return React.createElement("div", {
    className: "tree-item" + (selected === term.guid ? " sel" : ""),
    style: { paddingLeft: 8 + depth * 16 },
    onClick: function() { onSelect(term, false); }, title: term.qualifiedName || term.guid,
  },
    selection && term.guid && React.createElement("input", {
      type: "checkbox", checked: selection.isSelected(term.guid), style: { flexShrink: 0, cursor: 'pointer' },
      onClick: function(e) { e.stopPropagation(); },
      onChange: function() { selection.toggle({ guid: term.guid, displayName: term.displayName, typeName: term.typeName }); },
    }),
    React.createElement("span", { style: { width: 14, display: 'inline-block', flexShrink: 0 } }),
    React.createElement("div", { style: { flex: 1, minWidth: 0 } },
      React.createElement("div", { className: "type-name" }, term.displayName || term.qualifiedName || term.guid),
      term.qualifiedName && React.createElement("div", { style: { fontSize: 10, color: 'var(--dim)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' } }, term.qualifiedName)
    ),
    term.isTemplateSubstitute && React.createElement("span", { className: "badge", style: { fontSize: 9, background: 'rgba(245,158,11,.12)', color: '#fbbf24', border: '0.5px solid rgba(245,158,11,.35)', flexShrink: 0 } }, "template")
  );
}

// A folder node in the glossary tree — expanding the twistie lazily loads its
// child folders + terms (consistent with the Collections / Digital Products trees).
function GlossaryTreeNode({ folder, depth, selected, onSelect, showTemplates, fetchJson, selection }) {
  const [expanded, setExpanded] = React.useState(false);
  const [children, setChildren] = React.useState(null); // null = unfetched; {folders, terms}
  const [loading, setLoading] = React.useState(false);
  function toggle() {
    var next = !expanded;
    setExpanded(next);
    if (next && children === null && !loading) {
      setLoading(true);
      Promise.all([
        Promise.resolve(fetchJson('/api/glossary/' + encodeURIComponent(folder.guid) + '/folders')).catch(function() { return {}; }),
        Promise.resolve(fetchJson('/api/glossary/' + encodeURIComponent(folder.guid) + '/terms')).catch(function() { return {}; }),
      ]).then(function(res) { setChildren({ folders: (res[0] || {}).folders || [], terms: (res[1] || {}).terms || [] }); setLoading(false); })
        .catch(function() { setChildren({ folders: [], terms: [] }); setLoading(false); });
    }
  }
  var pad = 8 + depth * 16;
  var subTerms = children ? (showTemplates ? children.terms : children.terms.filter(function(t) { return !t.isTemplateSubstitute; })) : [];
  return React.createElement(React.Fragment, null,
    React.createElement("div", {
      className: "tree-item" + (selected === folder.guid ? " sel" : ""),
      style: { display: 'flex', alignItems: 'center', gap: 6, paddingLeft: pad, cursor: 'pointer' },
      title: folder.description || folder.qualifiedName,
    },
      React.createElement(FoldTriangle, { open: expanded, onClick: function(e) { e.stopPropagation(); toggle(); }, size: 12, style: { width: 14, textAlign: 'center' } }),
      React.createElement("span", { style: { fontSize: 12, flexShrink: 0 }, onClick: function(e) { e.stopPropagation(); toggle(); } }, "📁"),
      React.createElement("span", { className: "type-name", style: { flex: 1 }, onClick: function() { onSelect(folder, true); } }, folder.displayName || folder.qualifiedName || folder.guid)
    ),
    expanded && loading && React.createElement("div", { style: { paddingLeft: pad + 20, fontSize: 11, color: 'var(--dim)', padding: '2px 0' } }, "Loading…"),
    expanded && children && React.createElement(React.Fragment, null,
      children.folders.map(function(cf) { return React.createElement(GlossaryTreeNode, { key: cf.guid, folder: cf, depth: depth + 1, selected: selected, onSelect: onSelect, showTemplates: showTemplates, fetchJson: fetchJson, selection: selection }); }),
      subTerms.map(function(t) { return React.createElement(GlossaryTermRow, { key: t.guid, term: t, depth: depth + 1, selected: selected, onSelect: onSelect, selection: selection }); })
    )
  );
}

/* ── Markdown renderer (shared by Egeria Explorer + Tech Catalog) ────────────
 * renderMd(text) -> React element(s): splits on fenced ```mermaid blocks
 * (rendering each via the shared MermaidDiagram) and renders the rest as a
 * small markdown subset (headings, bold/italic/code, bullet/numbered lists,
 * GitHub-style tables). Inline-code background uses the --md-code-bg CSS var so
 * it adapts to each host SPA's light/dark theme. Depends on host globals React,
 * MermaidDiagram and CSS vars --accent --border --muted --md-code-bg. */
function _renderMdHtml(rawText) {
  if (!rawText || !rawText.trim()) return '';
  const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const inlineMarkup = s => s
    .replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*([^*\n]+?)\*/g, '<em>$1</em>')
    .replace(/`([^`\n]+)`/g, '<code style="background:var(--md-code-bg);padding:1px 4px;border-radius:3px;font-size:.9em">$1</code>');

  const lines = rawText.split('\n');
  const parts = [];
  let i = 0;
  while (i < lines.length) {
    // Detect markdown table: current line has pipes, next is separator row
    if (i + 1 < lines.length && /^\|.+\|/.test(lines[i]) && /^\|[\s\-:|]+\|/.test(lines[i + 1])) {
      const tlines = [];
      while (i < lines.length && /^\|/.test(lines[i].trim())) { tlines.push(lines[i]); i++; }
      const headers = tlines[0].split('|').slice(1, -1).map(h => h.trim());
      const seps    = tlines[1].split('|').slice(1, -1).map(s => s.trim());
      const aligns  = seps.map(s => s.startsWith(':') && s.endsWith(':') ? 'center' : s.endsWith(':') ? 'right' : 'left');
      const rows    = tlines.slice(2).map(r => r.split('|').slice(1, -1).map(c => c.trim()));
      let t = '<div style="overflow-x:auto;margin:8px 0"><table style="border-collapse:collapse;font-size:12px"><thead><tr>';
      headers.forEach(function(h, j) { t += '<th style="text-align:' + (aligns[j]||'left') + ';padding:5px 8px;border:1px solid var(--border);color:var(--muted);white-space:nowrap">' + inlineMarkup(esc(h)) + '</th>'; });
      t += '</tr></thead><tbody>';
      rows.forEach(function(row) {
        t += '<tr>';
        headers.forEach(function(_, j) { t += '<td style="text-align:' + (aligns[j]||'left') + ';padding:5px 8px;border:1px solid var(--border)">' + inlineMarkup(esc(row[j] || '')) + '</td>'; });
        t += '</tr>';
      });
      t += '</tbody></table></div>';
      parts.push(t);
    } else {
      // Accumulate non-table lines until a table starts
      const nonTable = [];
      while (i < lines.length && !(i + 1 < lines.length && /^\|.+\|/.test(lines[i]) && /^\|[\s\-:|]+\|/.test(lines[i + 1]))) {
        nonTable.push(lines[i]); i++;
      }
      if (nonTable.length > 0) {
        parts.push(inlineMarkup(esc(nonTable.join('\n')))
          .replace(/^### (.+)$/gm, '<b style="font-size:12px;display:block;margin:8px 0 2px;color:var(--accent)">$1</b>')
          .replace(/^## (.+)$/gm,  '<b style="font-size:13px;display:block;margin:10px 0 2px;color:var(--accent)">$1</b>')
          .replace(/^# (.+)$/gm,   '<b style="font-size:14px;display:block;margin:12px 0 4px;color:var(--accent)">$1</b>')
          .replace(/^[-*] (.+)$/gm, '<span style="display:block;padding-left:12px">• $1</span>')
          .replace(/^(\d+)\. (.+)$/gm, '<span style="display:block;padding-left:12px">$1. $2</span>')
          .replace(/\n\n/g, '<br><br>')
          .replace(/\n/g, '<br>'));
      }
    }
  }
  return parts.join('');
}

function renderMd(text) {
  if (!text || !text.trim()) return null;
  // Split on fenced mermaid code blocks
  const segs = [];
  const re = /```mermaid\n([\s\S]*?)```/g;
  let last = 0, m;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) segs.push({ type: 'md', src: text.slice(last, m.index) });
    segs.push({ type: 'mermaid', code: m[1].trim() });
    last = m.index + m[0].length;
  }
  if (last < text.length) segs.push({ type: 'md', src: text.slice(last) });
  if (segs.length === 0) return null;
  const els = segs.map(function(seg, i) {
    if (seg.type === 'mermaid') return React.createElement(MermaidDiagram, { key: i, code: seg.code });
    const html = _renderMdHtml(seg.src);
    if (!html) return null;
    return React.createElement('div', { key: i, dangerouslySetInnerHTML: { __html: html }, style: { lineHeight: 1.6, wordBreak: 'break-word' } });
  }).filter(Boolean);
  if (els.length === 0) return null;
  if (els.length === 1) return els[0];
  return React.createElement('div', null, ...els);
}

/* ResizeDivider — drag handle for resizable side panes (shared by both SPAs).
 * Uses the .col-divider CSS class (defined identically in both SPAs: a 5px
 * hit area with a 1px ::after line that turns --accent on hover). Pair with
 * useResizable for the width state. */
function ResizeDivider({ onMouseDown }) {
  return React.createElement('div', { className: 'col-divider', onMouseDown: onMouseDown });
}

/* ── Token-aware fetch (shared by Egeria Explorer + Tech Catalog) ────────────
 * egeriaFetch passes url/server/user_id as (non-secret) query params and the
 * Egeria bearer token as the X-Egeria-Token header — never user_pwd in the URL.
 * On HTTP 401 it refreshes the token once via the callback an App registers in
 * _tokenRefresher.refresh, then retries. Each SPA registers its own refresher. */
var _tokenRefresher = { refresh: null };

function egeriaFetch(url, creds, opts) {
  var _isRetry = !!(opts && opts._isRetry);
  var headers = Object.assign({}, (opts && opts.headers) || {});
  var queryUrl = url;
  if (creds) {
    var p = new URLSearchParams();
    if (creds.url)    p.set('url',     creds.url);
    if (creds.server) p.set('server',  creds.server);
    if (creds.userId) p.set('user_id', creds.userId);
    if (creds.token)  headers['X-Egeria-Token'] = creds.token;
    var qs = p.toString();
    if (qs) queryUrl = url + (url.indexOf('?') === -1 ? '?' : '&') + qs;
  }
  var mergedOpts = Object.assign({}, opts || {});
  delete mergedOpts._isRetry;
  mergedOpts.headers = headers;
  return fetch(queryUrl, mergedOpts).then(function(r) {
    if (r.status === 401 && !_isRetry && _tokenRefresher.refresh && creds && creds.userId) {
      return _tokenRefresher.refresh(creds).then(function(newCreds) {
        return egeriaFetch(url, newCreds, Object.assign({}, opts || {}, { _isRetry: true }));
      }).catch(function() { return r; });
    }
    return r;
  });
}

/* ──────────────────────────────────────────────────────────────────────────
 * Catalog search — shared by tech-catalog.html's SearchView and type-explorer
 * .html's ExplorerSearchView in quickstart. Ported here (2026-08-15, follow-up
 * to the bulk-action sync) because type-explorer.html's ExplorerSearchView
 * reference implementation already depends on it — porting the bulk-select
 * pattern for that view without this hook leaves `useCatalogSearch`/
 * `CATALOG_SEARCH_CATEGORY_ICONS`/`highlightHtml` as dangling references
 * (a runtime ReferenceError, invisible to `node --check`'s syntax-only pass).
 * freshstart's tech-catalog.html SearchView was NOT rewired onto this hook —
 * it still uses its own local q/data/err/loading/facets/selTypes state, and
 * its own local `highlightHtml`/`_hlEscape`/`SEARCH_CATEGORY_ICONS` (different
 * name from CATALOG_SEARCH_CATEGORY_ICONS below, so no collision there). Its
 * page-level `<script>` loads after this shared file and its own `highlightHtml`
 * plain-function declaration simply overwrites this one in the shared global
 * scope — harmless, since both implementations are identical; only
 * type-explorer.html's ExplorerSearchView actually depends on the shared one.
 * ────────────────────────────────────────────────────────────────────────── */

var CATALOG_SEARCH_CATEGORY_ICONS = {
  'glossary':       '📖',
  'tech-types':     '🔧',
  'data-assets':    '🗄️',
  'infrastructure': '🖧',
  'apis':           '🔗',
  'processes':      '⚙️',
  'projects':       '📁',
  'surveys':        '🔍',
  'valid-values':   '✅',
  'other':          '📦',
};

function _catalogSearchHlEscape(s) { return s.replace(/[&<>"]/g, function(c) { return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
// Wraps query-term matches in <mark>; safe against regex-special characters
// in the query itself (escaped before building the RegExp) and against HTML
// injection from the source text (escaped before highlighting).
function highlightHtml(text, q) {
  if (!text) return '';
  var safe = _catalogSearchHlEscape(text);
  if (!q || q.length < 2) return safe;
  try {
    var re = new RegExp('(' + q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi');
    return safe.replace(re, '<mark style="background:rgba(251,191,36,.35);color:inherit;border-radius:2px;padding:0 1px">$1</mark>');
  } catch (e) { return safe; }
}

// Result-list section headers group by real typeName, not categoryId --
// categoryId/categoryLabel (_TYPE_CATEGORY in catalog_search_handler.py) only
// curates ~40 of several hundred real Egeria types, so grouping the visible
// list by it means most headings read as the generic "Other" bucket even
// when a search was scoped to one exact, known type (e.g. selecting the
// PersonRole facet still headed the list "Other"). Regrouping by typeName
// here matches the same "trust the real result, not the curated bucket"
// principle typeFacets already uses. categoryId is kept per-type only for
// picking a (harmless, decorative) icon.
function groupCatalogSearchItemsByType(groups) {
  var byType = {};
  (groups || []).forEach(function(g) {
    g.items.forEach(function(it) {
      var key = it.typeName || '(unknown)';
      if (!byType[key]) byType[key] = { typeName: key, categoryId: it.categoryId, items: [] };
      byType[key].items.push(it);
    });
  });
  return Object.values(byType).sort(function(a, b) {
    return b.items.length - a.items.length || a.typeName.localeCompare(b.typeName);
  });
}

// The search state machine itself: debounced free-text query, server-side
// type-facet scoping (re-searches rather than filtering client-side — see
// the comment this carried at each original call site, kept below), loading/
// error/result state. `onReset`, if given, fires at the start of every fresh
// query (not on a facet-toggle re-search) — Catalog uses it to clear a stale
// bulk-selection from a previous, now-invisible result set; Explorer has no
// selection concept and omits it.
function useCatalogSearch(creds, initialQuery, onReset) {
  var _q = React.useState(initialQuery || ''), q = _q[0], setQ = _q[1];
  var _data = React.useState(null), data = _data[0], setData = _data[1];
  var _err = React.useState(null), err = _err[0], setErr = _err[1];
  var _loading = React.useState(false), loading = _loading[0], setLoading = _loading[1];
  var _baseFacets = React.useState(null), baseFacets = _baseFacets[0], setBaseFacets = _baseFacets[1];
  var _selTypes = React.useState([]), selTypes = _selTypes[0], setSelTypes = _selTypes[1];
  var timer = React.useRef(null);

  function doSearch(query, typeList) {
    var trimmed = (query || '').trim();
    if (!trimmed || trimmed === '*') { setData(null); setErr(null); return; }
    setLoading(true); setErr(null);
    var url = '/api/catalog/search?q=' + encodeURIComponent(trimmed) + '&page_size=200';
    (typeList || []).forEach(function(t) { url += '&types=' + encodeURIComponent(t); });
    egeriaFetch(url, creds)
      .then(function(r) { return r.ok ? r.json() : r.json().then(function(e) { throw new Error(e.detail || r.status); }); })
      .then(function(j) {
        setData(j); setLoading(false);
        if (!typeList || !typeList.length) setBaseFacets(j.typeFacets || []);
        if (j.typeFilterDropped) setSelTypes([]); // server couldn't apply it — don't show a filter that isn't real
      })
      .catch(function(e) { setErr(e.message || String(e)); setLoading(false); });
  }

  function handleInput(e) {
    var val = e.target.value;
    setQ(val);
    setSelTypes([]); setBaseFacets(null);
    if (onReset) onReset();
    clearTimeout(timer.current);
    if (val.trim().length >= 2) timer.current = setTimeout(function() { doSearch(val, []); }, 400);
    else setData(null);
  }

  function toggleType(tn) {
    var next = selTypes.indexOf(tn) === -1 ? selTypes.concat([tn]) : selTypes.filter(function(t) { return t !== tn; });
    setSelTypes(next);
    doSearch(q, next);
  }

  React.useEffect(function() {
    if (initialQuery && initialQuery.trim().length >= 2) doSearch(initialQuery, []);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  var hasResults = data && data.total > 0;
  var facets = baseFacets || [];
  var typeGroups = hasResults ? groupCatalogSearchItemsByType(data.groups) : [];

  return {
    q: q, setQ: setQ, data: data, err: err, loading: loading,
    facets: facets, selTypes: selTypes, hasResults: hasResults, typeGroups: typeGroups,
    handleInput: handleInput, toggleType: toggleType, doSearch: doSearch,
  };
}

/* ──────────────────────────────────────────────────────────────────────────
 * Type-graph helpers (subset ported from quickstart's egeria-shared-ui.js,
 * 2026-08-15) — only the pieces AddToCollectionModal below needs to walk the
 * /api/types subtype tree (e.g. Collection → SubjectArea, DigitalProduct…).
 * type-explorer.html keeps its own local getChain/getAllProps/getSubs (not
 * yet promoted to this shared file here, unlike quickstart's SHARE-3 — out of
 * scope for this port), so only getSubs/getAllSubs/useTypeGraph are added
 * here to avoid a wider, unrelated refactor.
 * ────────────────────────────────────────────────────────────────────────── */

// Direct subtypes only (one level). See getAllSubs below for the full
// transitive tree.
function getSubs(name, entities) {
  return Object.keys(entities).filter(function(n) {
    var t = entities[n];
    return t && t.supertype === name;
  });
}

// Transitive subtypes — needed wherever the direct children aren't enough
// (e.g. Collection's subtype tree is multi-level: Agreement, DigitalProduct,
// SubjectArea, … each have their own children too).
function getAllSubs(name, entities) {
  var direct = getSubs(name, entities);
  var all = direct.slice();
  direct.forEach(function(n) {
    all = all.concat(getAllSubs(n, entities));
  });
  return all;
}

// Fetches /api/types once per mount and returns just the `entities` map (what
// getSubs/getAllSubs operate on) — pass the same `creds` shape already
// threaded through other egeriaFetch call sites. Returns null while loading,
// {} on error (callers treat both as "nothing to show yet" rather than
// needing a separate error state for what's usually a background lookup
// feeding a picker, not the screen's primary content).
function useTypeGraph(creds) {
  var state = React.useState(null);
  var entities = state[0], setEntities = state[1];
  React.useEffect(function() {
    egeriaFetch('/api/types', creds).then(function(r) {
      return r.ok ? r.json() : Promise.reject(new Error('HTTP ' + r.status));
    }).then(function(data) {
      setEntities((data && data.entities) || {});
    }).catch(function() {
      setEntities({});
    });
    // Mount-once by design — see quickstart's egeria-shared-ui.js for the
    // full rationale (a picker inside a short-lived modal doesn't need this
    // to react to creds changing mid-lifetime).
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  return entities;
}

/* ──────────────────────────────────────────────────────────────────────────
 * Bulk selection — shared by any screen that renders a list of elements and
 * wants a "select some, then act on them" flow. Ported from quickstart's
 * egeria-shared-ui.js (2026-08-15) — see that file's history for the design
 * rationale (pilot: tech-catalog.html's search results + Add-to-Collection,
 * 2026-08-14).
 * ────────────────────────────────────────────────────────────────────────── */

// selected is a Map<guid, {guid, displayName, typeName}> — stores enough per
// item to render a confirm step without re-fetching, not just a bare guid Set.
function useSelection() {
  var state = React.useState(function() { return new Map(); });
  var selected = state[0], setSelected = state[1];

  var toggle = React.useCallback(function(item) {
    setSelected(function(prev) {
      var next = new Map(prev);
      if (next.has(item.guid)) next.delete(item.guid);
      else next.set(item.guid, item);
      return next;
    });
  }, []);

  // Merges into the existing selection rather than replacing it — a
  // per-group "select all" shouldn't clear selections made in other groups.
  var selectAll = React.useCallback(function(items) {
    setSelected(function(prev) {
      var next = new Map(prev);
      items.forEach(function(i) { next.set(i.guid, i); });
      return next;
    });
  }, []);

  var deselectAll = React.useCallback(function(items) {
    setSelected(function(prev) {
      var next = new Map(prev);
      items.forEach(function(i) { next.delete(i.guid); });
      return next;
    });
  }, []);

  var clear = React.useCallback(function() { setSelected(new Map()); }, []);
  var isSelected = React.useCallback(function(guid) { return selected.has(guid); }, [selected]);

  return {
    selected: selected, toggle: toggle, selectAll: selectAll, deselectAll: deselectAll,
    clear: clear, isSelected: isSelected, count: selected.size,
  };
}

// Presentational only — renders nothing when count is 0. actions:
// [{id, label, onClick}].
function BulkActionBar({ count, onClear, actions }) {
  if (!count) return null;
  var el = React.createElement;
  return el('div', {
    style: {
      display: 'flex', alignItems: 'center', gap: 10, padding: '6px 12px',
      background: 'var(--panel)', border: '1px solid var(--border)', borderRadius: 6,
      marginBottom: 8, fontSize: 12,
    },
  },
    el('span', { style: { fontWeight: 600, color: 'var(--text)' } }, count + ' selected'),
    (actions || []).map(function(a) {
      return el('button', {
        key: a.id, onClick: a.onClick,
        style: {
          fontSize: 11, padding: '3px 10px', borderRadius: 4, border: '1px solid var(--accent)',
          background: 'var(--accent)', color: 'var(--bg)', cursor: 'pointer',
        },
      }, a.label);
    }),
    el('button', {
      onClick: onClear,
      style: {
        fontSize: 11, padding: '3px 10px', borderRadius: 4, border: '1px solid var(--border)',
        background: 'transparent', color: 'var(--dim)', cursor: 'pointer', marginLeft: 'auto',
      },
    }, 'Clear')
  );
}

// Two-step "add these to a collection" flow: pick a Collection subtype (from
// the /api/types graph, via useTypeGraph/getAllSubs above), then pick an
// existing collection of that subtype (GET /api/collections/by-type), then
// confirm (POST /api/collections/{guid}/members). v1 scope: existing
// collections only — no inline "create new collection" yet (BACKLOG.md
// Bulk Actions Phase 2). Modal chrome mirrors EgeriaFeedbackWidget's dialog
// below for visual consistency (same overlay/panel/input styling).
// action: 'add' (default) or 'remove' — remove mode always targets an
// existing collection (no "create new", nothing to remove from a collection
// that doesn't exist yet) and calls DELETE .../members instead of POST
// (BACKLOG.md Bulk Actions, task #19, 2026-08-14).
function AddToCollectionModal({ items, creds, action, onClose, onDone }) {
  // Verb picked inside the modal now, not baked into which BulkActionBar
  // button was clicked (Dan's call, 2026-08-18 -- collapses the bar from a
  // button per verb×kind down to one per kind). `action` still seeds the
  // initial tab so any caller not yet updated to the 1-button pattern keeps
  // working unchanged (e.g. "Remove from Collection…" opens straight to the
  // Remove tab instead of defaulting to Add).
  var verbState = React.useState(action === 'remove' ? 'remove' : 'add');
  var verb = verbState[0], setVerb = verbState[1];
  var isRemove = verb === 'remove';
  var entities = useTypeGraph(creds);
  var subtypeState = React.useState('Collection');
  var subtype = subtypeState[0], setSubtype = subtypeState[1];
  // 'existing' picks a collection via GET /api/collections/by-type; 'new'
  // creates one via POST /api/collections first, then adds to it (BACKLOG.md
  // Bulk Actions Phase 2, 2026-08-14). Remove mode never leaves 'existing'.
  var modeState = React.useState('existing');
  var mode = isRemove ? 'existing' : modeState[0], setMode = modeState[1];
  var colsState = React.useState(null); // null = not yet loaded; [] = loaded, empty
  var collections = colsState[0], setCollections = colsState[1];
  var colsLoadingState = React.useState(false);
  var collectionsLoading = colsLoadingState[0], setCollectionsLoading = colsLoadingState[1];
  var colsErrState = React.useState(null);
  var collectionsError = colsErrState[0], setCollectionsError = colsErrState[1];
  var targetState = React.useState(null);
  var target = targetState[0], setTarget = targetState[1];
  var newNameState = React.useState('');
  var newName = newNameState[0], setNewName = newNameState[1];
  var newDescState = React.useState('');
  var newDescription = newDescState[0], setNewDescription = newDescState[1];
  var submittingState = React.useState(false);
  var submitting = submittingState[0], setSubmitting = submittingState[1];
  var resultState = React.useState(null);
  var result = resultState[0], setResult = resultState[1];
  var resultTargetState = React.useState(null); // the collection actually used, incl. newly-created ones
  var resultTarget = resultTargetState[0], setResultTarget = resultTargetState[1];
  var submitErrState = React.useState(null);
  var submitError = submitErrState[0], setSubmitError = submitErrState[1];

  var subtypeOptions = React.useMemo(function() {
    if (!entities) return ['Collection'];
    return ['Collection'].concat(getAllSubs('Collection', entities).slice().sort());
  }, [entities]);

  React.useEffect(function() {
    if (!subtype || mode !== 'existing') return;
    setCollections(null);
    setCollectionsError(null);
    setTarget(null);
    setCollectionsLoading(true);
    egeriaFetch('/api/collections/by-type?type_name=' + encodeURIComponent(subtype), creds)
      .then(function(r) { return r.ok ? r.json() : Promise.reject(new Error('HTTP ' + r.status)); })
      .then(function(list) { setCollections(list || []); setCollectionsLoading(false); })
      .catch(function(e) { setCollectionsError(e.message || String(e)); setCollectionsLoading(false); });
  }, [subtype, mode]);

  function addMembers(collGuid) {
    return egeriaFetch('/api/collections/' + encodeURIComponent(collGuid) + '/members', creds, {
      method: isRemove ? 'DELETE' : 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ guids: items.map(function(i) { return i.guid; }) }),
    }).then(function(r) { return r.ok ? r.json() : r.json().then(function(e) { throw new Error(e.detail || ('HTTP ' + r.status)); }); });
  }

  function submit() {
    if (submitting) return;
    if (mode === 'existing') {
      if (!target) return;
      setSubmitting(true);
      setSubmitError(null);
      addMembers(target.guid)
        .then(function(res) { setResultTarget(target); setResult(res); setSubmitting(false); if (onDone) onDone(res); })
        .catch(function(e) { setSubmitError(e.message || String(e)); setSubmitting(false); });
    } else {
      if (!newName.trim()) return;
      setSubmitting(true);
      setSubmitError(null);
      egeriaFetch('/api/collections', creds, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type_name: subtype, display_name: newName.trim(), description: newDescription.trim() || null }),
      })
        .then(function(r) { return r.ok ? r.json() : r.json().then(function(e) { throw new Error(e.detail || ('HTTP ' + r.status)); }); })
        .then(function(created) {
          setResultTarget(created);
          return addMembers(created.guid).then(function(res) { setResult(res); setSubmitting(false); if (onDone) onDone(res); });
        })
        .catch(function(e) { setSubmitError(e.message || String(e)); setSubmitting(false); });
    }
  }

  var el = React.createElement;
  var inp = { width: '100%', boxSizing: 'border-box', background: 'var(--bg)', border: '1px solid var(--border)',
              borderRadius: 6, padding: '7px 9px', color: 'var(--text)', fontSize: 12, fontFamily: 'inherit', outline: 'none' };
  function tabBtn(id, label) {
    var active = mode === id;
    return el('button', {
      key: id, onClick: function() { setMode(id); },
      style: { fontSize: 11, padding: '4px 10px', borderRadius: 4, cursor: 'pointer',
               border: '1px solid ' + (active ? 'var(--accent)' : 'var(--border)'),
               background: active ? 'var(--accent)' : 'transparent',
               color: active ? 'var(--bg)' : 'var(--dim)', fontWeight: active ? 700 : 400 },
    }, label);
  }
  var canSubmit = mode === 'existing' ? !!target : newName.trim().length > 0;

  return el('div', {
    onClick: function(e) { if (e.target === e.currentTarget && !submitting) onClose(); },
    style: { position: 'fixed', inset: 0, zIndex: 1000, background: 'rgba(0,0,0,0.45)',
             display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 24 },
  },
    el('div', { style: { background: 'var(--surface,var(--card))', border: '1px solid var(--border)',
        borderRadius: 12, padding: '22px 26px', width: 420, boxShadow: '0 8px 32px rgba(0,0,0,0.3)' } },

      el('div', { style: { fontWeight: 700, fontSize: 14, marginBottom: 4 } }, isRemove ? 'Remove from Collection' : 'Add to Collection'),
      el('div', { style: { fontSize: 11, color: 'var(--muted)', marginBottom: 14 } },
        items.length + ' element' + (items.length === 1 ? '' : 's') + ' selected'),

      !result && el(React.Fragment, null,
        el('div', { style: { display: 'flex', gap: 6, marginBottom: 14 } },
          ['add', 'remove'].map(function(id) {
            var active = verb === id;
            return el('button', {
              key: id, disabled: submitting,
              onClick: function() { setVerb(id); },
              style: { flex: 1, fontSize: 12, padding: '6px 10px', borderRadius: 6, cursor: submitting ? 'default' : 'pointer',
                       border: '1px solid ' + (active ? 'var(--accent)' : 'var(--border)'),
                       background: active ? 'var(--accent)' : 'transparent',
                       color: active ? 'var(--bg)' : 'var(--dim)', fontWeight: active ? 700 : 400 },
            }, id === 'add' ? 'Add' : 'Remove');
          })
        ),
        el('label', { style: { fontSize: 11, color: 'var(--dim)', display: 'block', marginBottom: 3 } }, 'Collection type'),
        el('select', {
          value: subtype, onChange: function(e) { setSubtype(e.target.value); },
          style: Object.assign({}, inp, { marginBottom: 10 }),
        }, subtypeOptions.map(function(t) { return el('option', { key: t, value: t }, t); })),

        !isRemove && el('div', { style: { display: 'flex', gap: 6, marginBottom: 10 } },
          tabBtn('existing', 'Use existing'), tabBtn('new', 'Create new')),

        mode === 'existing' && el(React.Fragment, null,
          el('label', { style: { fontSize: 11, color: 'var(--dim)', display: 'block', marginBottom: 3 } }, 'Collection'),
          collectionsLoading && el('div', { style: { fontSize: 12, color: 'var(--dim)', padding: '6px 0' } }, 'Loading…'),
          collectionsError && el('div', { style: { fontSize: 12, color: '#f87171', padding: '6px 0' } }, 'Error: ' + collectionsError),
          !collectionsLoading && !collectionsError && collections && collections.length === 0 &&
            el('div', { style: { fontSize: 12, color: 'var(--dim)', padding: '6px 0' } },
              'No existing ' + subtype + ' collections found' + (isRemove ? '.' : ' — try "Create new".')),
          !collectionsLoading && !collectionsError && collections && collections.length > 0 &&
            el('select', {
              value: (target && target.guid) || '',
              onChange: function(e) {
                var c = collections.find(function(x) { return x.guid === e.target.value; });
                setTarget(c || null);
              },
              style: Object.assign({}, inp, { marginBottom: 10 }),
            },
              el('option', { value: '' }, '— choose —'),
              collections.map(function(c) {
                return el('option', { key: c.guid, value: c.guid }, c.displayName || c.qualifiedName || c.guid);
              })
            )
        ),

        mode === 'new' && el(React.Fragment, null,
          el('label', { style: { fontSize: 11, color: 'var(--dim)', display: 'block', marginBottom: 3 } }, 'New ' + subtype + ' name'),
          el('input', {
            type: 'text', value: newName, onChange: function(e) { setNewName(e.target.value); },
            placeholder: 'Display name', style: Object.assign({}, inp, { marginBottom: 8 }),
          }),
          el('textarea', {
            value: newDescription, onChange: function(e) { setNewDescription(e.target.value); },
            placeholder: 'Description (optional)', rows: 2,
            style: Object.assign({}, inp, { resize: 'vertical', marginBottom: 10 }),
          })
        ),

        submitError && el('div', { style: { fontSize: 12, color: '#f87171', marginBottom: 8 } }, 'Error: ' + submitError),

        el('div', { style: { display: 'flex', gap: 8, justifyContent: 'flex-end', marginTop: 10 } },
          el('button', {
            onClick: onClose, disabled: submitting,
            style: { fontSize: 12, padding: '6px 14px', borderRadius: 6, border: '1px solid var(--border)',
                     background: 'transparent', color: 'var(--dim)', cursor: submitting ? 'default' : 'pointer' },
          }, 'Cancel'),
          el('button', {
            onClick: submit, disabled: !canSubmit || submitting,
            style: { fontSize: 12, padding: '6px 14px', borderRadius: 6, border: '1px solid var(--accent)',
                     background: (!canSubmit || submitting) ? 'var(--panel)' : 'var(--accent)',
                     color: (!canSubmit || submitting) ? 'var(--dim)' : 'var(--bg)',
                     cursor: (!canSubmit || submitting) ? 'default' : 'pointer' },
          }, submitting ? (mode === 'new' ? 'Creating…' : (isRemove ? 'Removing…' : 'Adding…'))
                        : (mode === 'new' ? 'Create & Add' : (isRemove ? 'Remove' : 'Add')))
        )
      ),

      result && el(React.Fragment, null,
        el('div', { style: { fontSize: 13, marginBottom: 6 } },
          '✓ ', isRemove ? result.removed.length : result.added.length,
          isRemove ? ' removed from ' : ' added to ', (resultTarget && resultTarget.displayName) || subtype, '.'),
        result.failed && result.failed.length > 0 && el('div', { style: { fontSize: 12, color: '#f87171', marginBottom: 10 } },
          result.failed.length + ' failed:',
          el('ul', { style: { margin: '4px 0 0 18px', padding: 0 } },
            result.failed.map(function(f) {
              return el('li', { key: f.guid }, f.guid + ' — ' + f.error);
            })
          )
        ),
        el('div', { style: { display: 'flex', justifyContent: 'flex-end', marginTop: 10 } },
          el('button', {
            onClick: onClose,
            style: { fontSize: 12, padding: '6px 14px', borderRadius: 6, border: '1px solid var(--accent)',
                     background: 'var(--accent)', color: 'var(--bg)', cursor: 'pointer' },
          }, 'Done')
        )
      )
    )
  );
}

// Bulk zone-membership add/remove — same overlay/header/submit/result chrome
// as AddToCollectionModal (deliberately not unified into one shared shell —
// see quickstart's egeria-shared-ui.js history for the rationale). Backend:
// governance_zones_handler.py — POST/DELETE /api/zone-membership/{zone}/
// members. Unlike collection membership (a relationship, pure blind write),
// zone membership is a classification whose zoneMembership property is a
// list the backend read-modifies-writes per element — see that handler's
// module docstring for why.
function ZoneMembershipModal({ items, creds, action, onClose, onDone }) {
  // Verb picked inside the modal (Dan's call, 2026-08-18) -- same pattern as
  // AddToCollectionModal's verb tabs. `action` still seeds the initial tab
  // for backward compatibility with callers not yet on the 1-button pattern.
  var verbState = React.useState(action === 'remove' ? 'remove' : 'add');
  var verb = verbState[0], setVerb = verbState[1];
  var isRemove = verb === 'remove';
  var zonesState = React.useState(null); // null = not yet loaded; [] = loaded, empty
  var zones = zonesState[0], setZones = zonesState[1];
  var zonesLoadingState = React.useState(true);
  var zonesLoading = zonesLoadingState[0], setZonesLoading = zonesLoadingState[1];
  var zonesErrState = React.useState(null);
  var zonesError = zonesErrState[0], setZonesError = zonesErrState[1];
  var targetState = React.useState(null);
  var target = targetState[0], setTarget = targetState[1]; // the picked zone object ({name, displayName, ...})
  var submittingState = React.useState(false);
  var submitting = submittingState[0], setSubmitting = submittingState[1];
  var resultState = React.useState(null);
  var result = resultState[0], setResult = resultState[1];
  var submitErrState = React.useState(null);
  var submitError = submitErrState[0], setSubmitError = submitErrState[1];

  React.useEffect(function() {
    setZonesLoading(true);
    setZonesError(null);
    egeriaFetch('/api/insights/zones', creds)
      .then(function(r) { return r.ok ? r.json() : Promise.reject(new Error('HTTP ' + r.status)); })
      .then(function(data) { setZones((data && data.zones) || []); setZonesLoading(false); })
      .catch(function(e) { setZonesError(e.message || String(e)); setZonesLoading(false); });
  }, []);

  function submit() {
    if (submitting || !target) return;
    setSubmitting(true);
    setSubmitError(null);
    var url = '/api/zone-membership/' + encodeURIComponent(target.name) + '/members';
    egeriaFetch(url, creds, {
      method: isRemove ? 'DELETE' : 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ guids: items.map(function(i) { return i.guid; }) }),
    })
      .then(function(r) { return r.ok ? r.json() : r.json().then(function(e) { throw new Error(e.detail || ('HTTP ' + r.status)); }); })
      .then(function(res) { setResult(res); setSubmitting(false); if (onDone) onDone(res); })
      .catch(function(e) { setSubmitError(e.message || String(e)); setSubmitting(false); });
  }

  var el = React.createElement;
  var inp = { width: '100%', boxSizing: 'border-box', background: 'var(--bg)', border: '1px solid var(--border)',
              borderRadius: 6, padding: '7px 9px', color: 'var(--text)', fontSize: 12, fontFamily: 'inherit', outline: 'none' };

  return el('div', {
    onClick: function(e) { if (e.target === e.currentTarget && !submitting) onClose(); },
    style: { position: 'fixed', inset: 0, zIndex: 1000, background: 'rgba(0,0,0,0.45)',
             display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 24 },
  },
    el('div', { style: { background: 'var(--surface,var(--card))', border: '1px solid var(--border)',
        borderRadius: 12, padding: '22px 26px', width: 420, boxShadow: '0 8px 32px rgba(0,0,0,0.3)' } },

      el('div', { style: { fontWeight: 700, fontSize: 14, marginBottom: 4 } }, isRemove ? 'Remove from Governance Zone' : 'Add to Governance Zone'),
      el('div', { style: { fontSize: 11, color: 'var(--muted)', marginBottom: 14 } },
        items.length + ' element' + (items.length === 1 ? '' : 's') + ' selected'),

      !result && el(React.Fragment, null,
        el('div', { style: { display: 'flex', gap: 6, marginBottom: 14 } },
          ['add', 'remove'].map(function(id) {
            var active = verb === id;
            return el('button', {
              key: id, disabled: submitting,
              onClick: function() { setVerb(id); },
              style: { flex: 1, fontSize: 12, padding: '6px 10px', borderRadius: 6, cursor: submitting ? 'default' : 'pointer',
                       border: '1px solid ' + (active ? 'var(--accent)' : 'var(--border)'),
                       background: active ? 'var(--accent)' : 'transparent',
                       color: active ? 'var(--bg)' : 'var(--dim)', fontWeight: active ? 700 : 400 },
            }, id === 'add' ? 'Add' : 'Remove');
          })
        ),
        el('label', { style: { fontSize: 11, color: 'var(--dim)', display: 'block', marginBottom: 3 } }, 'Governance zone'),
        zonesLoading && el('div', { style: { fontSize: 12, color: 'var(--dim)', padding: '6px 0' } }, 'Loading…'),
        zonesError && el('div', { style: { fontSize: 12, color: '#f87171', padding: '6px 0' } }, 'Error: ' + zonesError),
        !zonesLoading && !zonesError && zones && zones.length === 0 &&
          el('div', { style: { fontSize: 12, color: 'var(--dim)', padding: '6px 0' } }, 'No governance zones defined.'),
        !zonesLoading && !zonesError && zones && zones.length > 0 &&
          el('select', {
            value: (target && target.name) || '',
            onChange: function(e) {
              var z = zones.find(function(x) { return x.name === e.target.value; });
              setTarget(z || null);
            },
            style: Object.assign({}, inp, { marginBottom: 10 }),
          },
            el('option', { value: '' }, '— choose —'),
            zones.map(function(z) {
              return el('option', { key: z.guid || z.name, value: z.name }, (z.displayName || z.name) + ' (' + z.count + ')');
            })
          ),

        submitError && el('div', { style: { fontSize: 12, color: '#f87171', marginBottom: 8 } }, 'Error: ' + submitError),

        el('div', { style: { display: 'flex', gap: 8, justifyContent: 'flex-end', marginTop: 10 } },
          el('button', {
            onClick: onClose, disabled: submitting,
            style: { fontSize: 12, padding: '6px 14px', borderRadius: 6, border: '1px solid var(--border)',
                     background: 'transparent', color: 'var(--dim)', cursor: submitting ? 'default' : 'pointer' },
          }, 'Cancel'),
          el('button', {
            onClick: submit, disabled: !target || submitting,
            style: { fontSize: 12, padding: '6px 14px', borderRadius: 6, border: '1px solid var(--accent)',
                     background: (!target || submitting) ? 'var(--panel)' : 'var(--accent)',
                     color: (!target || submitting) ? 'var(--dim)' : 'var(--bg)',
                     cursor: (!target || submitting) ? 'default' : 'pointer' },
          }, submitting ? (isRemove ? 'Removing…' : 'Adding…') : (isRemove ? 'Remove' : 'Add'))
        )
      ),

      result && el(React.Fragment, null,
        el('div', { style: { fontSize: 13, marginBottom: 6 } },
          '✓ ', isRemove ? result.removed.length : result.added.length,
          isRemove ? ' removed from ' : ' added to ', (target && (target.displayName || target.name)) || 'zone', '.'),
        result.failed && result.failed.length > 0 && el('div', { style: { fontSize: 12, color: '#f87171', marginBottom: 10 } },
          result.failed.length + ' failed:',
          el('ul', { style: { margin: '4px 0 0 18px', padding: 0 } },
            result.failed.map(function(f) {
              return el('li', { key: f.guid }, f.guid + ' — ' + f.error);
            })
          )
        ),
        el('div', { style: { display: 'flex', justifyContent: 'flex-end', marginTop: 10 } },
          el('button', {
            onClick: onClose,
            style: { fontSize: 12, padding: '6px 14px', borderRadius: 6, border: '1px solid var(--accent)',
                     background: 'var(--accent)', color: 'var(--bg)', cursor: 'pointer' },
          }, 'Done')
        )
      )
    )
  );
}

/* ──────────────────────────────────────────────────────────────────────────
 * Egeria Feedback widgets (likes / ratings / comments) — shared by both SPAs.
 * Behaviour-identical extraction from type-explorer.html (canonical). They use
 * bare fetch() against /api/egeria-feedback/* (session/cookie auth, env-agnostic).
 * ────────────────────────────────────────────────────────────────────────── */

// ── EgeriaFeedbackWidget ──────────────────────────────────────────────────────

function EgeriaFeedbackWidget({ guid }) {
  var _dataState       = React.useState(null),  feedbackData = _dataState[0],       setFeedbackData = _dataState[1];
  var _loadState       = React.useState(true),  loading      = _loadState[0],       setLoading      = _loadState[1];
  var _showRateState   = React.useState(false), showRate     = _showRateState[0],   setShowRate     = _showRateState[1];
  var _hoverState      = React.useState(0),     hoverStar    = _hoverState[0],      setHoverStar    = _hoverState[1];
  var _likeLoadState   = React.useState(false), likeLoading  = _likeLoadState[0],   setLikeLoading  = _likeLoadState[1];
  var _rateLoadState   = React.useState(false), rateLoading  = _rateLoadState[0],   setRateLoading  = _rateLoadState[1];

  React.useEffect(function() {
    if (!guid) return;
    setLoading(true);
    fetch('/api/egeria-feedback/' + encodeURIComponent(guid))
      .then(function(r) { return r.ok ? r.json() : null; })
      .then(function(d) { if (d) setFeedbackData(d); setLoading(false); })
      .catch(function() { setLoading(false); });
  }, [guid]);

  function handleLike() {
    if (likeLoading || !feedbackData) return;
    setLikeLoading(true);
    fetch('/api/egeria-feedback/' + encodeURIComponent(guid) + '/like', { method: 'POST' })
      .then(function(r) { return r.ok ? r.json() : null; })
      .then(function(d) { if (d) setFeedbackData(function(p) { return Object.assign({}, p, d); }); })
      .catch(function() {})
      .finally(function() { setLikeLoading(false); });
  }

  function handleStar(n) {
    if (rateLoading || !feedbackData) return;
    setRateLoading(true);
    var sameRating = n === feedbackData.my_rating;
    var url = '/api/egeria-feedback/' + encodeURIComponent(guid) + '/rating';
    var opts = sameRating
      ? { method: 'DELETE' }
      : { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ star_rating: n }) };
    fetch(url, opts)
      .then(function(r) { return r.ok ? r.json() : null; })
      .then(function(d) {
        if (d) setFeedbackData(function(p) { return Object.assign({}, p, d); });
        setShowRate(false); setHoverStar(0);
      })
      .catch(function() {})
      .finally(function() { setRateLoading(false); });
  }

  if (loading || !feedbackData) return null;

  var liked = feedbackData.my_like;
  var likeStyle = {
    cursor: likeLoading ? 'default' : 'pointer',
    color:  liked ? '#f87171' : 'var(--muted)',
    opacity: likeLoading ? 0.5 : 1,
    fontWeight: 600, fontSize: 13, letterSpacing: '0.02em',
  };

  var avgRating = feedbackData.avg_rating;
  var avgStars = avgRating !== null
    ? '★'.repeat(Math.round(avgRating)) + '☆'.repeat(5 - Math.round(avgRating))
    : null;

  var starPicker = showRate
    ? React.createElement('span', { style: { display: 'inline-flex', alignItems: 'center', gap: 1, marginLeft: 4 } },
        [1,2,3,4,5].map(function(n) {
          var active = (hoverStar || feedbackData.my_rating || 0) >= n;
          return React.createElement('span', {
            key: n,
            onClick: function(e) { e.stopPropagation(); handleStar(n); },
            onMouseEnter: function() { setHoverStar(n); },
            onMouseLeave: function() { setHoverStar(0); },
            title: feedbackData.my_rating === n ? 'Remove your rating' : n + ' star' + (n > 1 ? 's' : ''),
            style: {
              fontSize: 16, cursor: rateLoading ? 'default' : 'pointer',
              color: active ? '#f59e0b' : 'var(--dim)',
              opacity: rateLoading ? 0.5 : 1,
            }
          }, active ? '★' : '☆');
        }),
        React.createElement('span', {
          onClick: function(e) { e.stopPropagation(); setShowRate(false); setHoverStar(0); },
          style: { fontSize: 10, color: 'var(--muted)', cursor: 'pointer', marginLeft: 4 }
        }, '✕')
      )
    : null;

  var ratingDisplay = !showRate
    ? React.createElement('span', {
        onClick: function() { setShowRate(true); },
        title: feedbackData.my_rating ? 'Change your rating' : 'Rate this',
        style: { cursor: 'pointer' }
      },
        avgStars
        ? React.createElement(React.Fragment, null,
            React.createElement('span', { style: { color: '#f59e0b', letterSpacing: '0.05em' } }, avgStars),
            feedbackData.ratings_count > 1 && React.createElement('span', { style: { color: 'var(--dim)', fontSize: 10, marginLeft: 3 } }, '(' + feedbackData.ratings_count + ')')
          )
        : React.createElement('span', { style: { color: 'var(--muted)', fontSize: 11 } }, 'Rate ★')
      )
    : null;

  return React.createElement('div', {
    style: { display: 'flex', alignItems: 'center', gap: 8, marginTop: 6, marginBottom: 2, fontSize: 12, userSelect: 'none' }
  },
    React.createElement('span', { onClick: handleLike, title: liked ? 'Unlike' : 'Like', style: likeStyle },
      '♥ ' + feedbackData.likes_count),
    React.createElement('span', { style: { color: 'var(--border)' } }, '|'),
    ratingDisplay,
    starPicker
  );
}

// ── EgeriaCommentsSection ─────────────────────────────────────────────────────

function EgeriaCommentsSection({ guid }) {
  var TYPES = ['STANDARD_COMMENT','QUESTION','ANSWER','SUGGESTION','USAGE_EXPERIENCE','REQUIREMENT','OTHER'];
  var TYPE_COLOR = {
    STANDARD_COMMENT: 'var(--muted)', QUESTION: '#60a5fa', ANSWER: '#34d399',
    SUGGESTION: '#a78bfa', USAGE_EXPERIENCE: '#fbbf24', REQUIREMENT: '#f87171', OTHER: 'var(--dim)'
  };
  var TYPE_LABEL = {
    STANDARD_COMMENT: 'Comment', QUESTION: 'Question', ANSWER: 'Answer',
    SUGGESTION: 'Suggestion', USAGE_EXPERIENCE: 'Usage', REQUIREMENT: 'Requirement', OTHER: 'Other'
  };

  var _cState  = React.useState([]),                 comments    = _cState[0],    setComments    = _cState[1];
  var _lState  = React.useState(true),               loading     = _lState[0],    setLoading     = _lState[1];
  var _tState  = React.useState(''),                 text        = _tState[0],    setText        = _tState[1];
  var _ctState = React.useState('STANDARD_COMMENT'), commentType = _ctState[0],   setCommentType = _ctState[1];
  var _sState  = React.useState(false),              submitting  = _sState[0],    setSubmitting  = _sState[1];
  var _eState  = React.useState(''),                 errMsg      = _eState[0],    setErrMsg      = _eState[1];
  // editing: null | { guid, text, commentType }
  var _edState = React.useState(null),               editing     = _edState[0],   setEditing     = _edState[1];
  var _esState = React.useState(false),              editSaving  = _esState[0],   setEditSaving  = _esState[1];
  var _eeState = React.useState(''),                 editErr     = _eeState[0],   setEditErr     = _eeState[1];

  React.useEffect(function() {
    if (!guid) return;
    setLoading(true);
    fetch('/api/egeria-feedback/' + encodeURIComponent(guid) + '/comments')
      .then(function(r) { return r.ok ? r.json() : []; })
      .then(function(d) { setComments(Array.isArray(d) ? d : []); setLoading(false); })
      .catch(function() { setLoading(false); });
  }, [guid]);

  function handleSubmit() {
    if (!text.trim() || submitting) return;
    setSubmitting(true); setErrMsg('');
    fetch('/api/egeria-feedback/' + encodeURIComponent(guid) + '/comments', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ comment_type: commentType, text: text.trim() })
    })
      .then(function(r) { return r.ok ? r.json() : r.json().then(function(d) { throw new Error(d.detail || 'Error'); }); })
      .then(function(d) { setComments(Array.isArray(d) ? d : []); setText(''); })
      .catch(function(e) { setErrMsg(e.message || 'Failed to post comment'); })
      .finally(function() { setSubmitting(false); });
  }

  function handleDelete(cguid) {
    fetch('/api/egeria-feedback/' + encodeURIComponent(guid) + '/comments/' + encodeURIComponent(cguid), { method: 'DELETE' })
      .then(function(r) { return r.ok ? r.json() : []; })
      .then(function(d) { setComments(Array.isArray(d) ? d : []); if (editing && editing.guid === cguid) setEditing(null); })
      .catch(function() {});
  }

  function startEdit(c) {
    setEditing({ guid: c.guid, text: c.text, commentType: c.commentType || 'STANDARD_COMMENT' });
    setEditErr('');
  }

  function handleEditSave() {
    if (!editing || !editing.text.trim() || editSaving) return;
    setEditSaving(true); setEditErr('');
    fetch('/api/egeria-feedback/' + encodeURIComponent(guid) + '/comments/' + encodeURIComponent(editing.guid), {
      method: 'PUT', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ comment_type: editing.commentType, text: editing.text.trim() })
    })
      .then(function(r) { return r.ok ? r.json() : r.json().then(function(d) { throw new Error(d.detail || 'Error'); }); })
      .then(function(d) { setComments(Array.isArray(d) ? d : []); setEditing(null); })
      .catch(function(e) { setEditErr(e.message || 'Save failed'); })
      .finally(function() { setEditSaving(false); });
  }

  var btnBase = { border: 'none', borderRadius: 4, fontSize: 11, fontWeight: 600, cursor: 'pointer', padding: '3px 10px' };

  function renderComment(c) {
    var col = TYPE_COLOR[c.commentType] || 'var(--muted)';
    var isEditing = editing && editing.guid === c.guid;

    return React.createElement('div', { key: c.guid, style: { borderLeft: '3px solid ' + col, paddingLeft: 10, marginBottom: 12, fontSize: 12 } },
      React.createElement('div', { style: { display: 'flex', alignItems: 'center', gap: 6, marginBottom: 4, flexWrap: 'wrap' } },
        React.createElement('span', { style: { fontSize: 10, fontWeight: 700, color: col, textTransform: 'uppercase' } }, TYPE_LABEL[c.commentType] || c.commentType),
        React.createElement('span', { style: { color: 'var(--dim)', fontSize: 10 } }, c.createdBy || 'unknown'),
        c.createTime && React.createElement('span', { style: { color: 'var(--dim)', fontSize: 10 } }, '· ' + new Date(c.createTime).toLocaleDateString()),
        !isEditing && React.createElement('button', {
          onClick: function() { startEdit(c); },
          title: 'Edit comment',
          style: Object.assign({}, btnBase, { marginLeft: 'auto', background: 'var(--hover)', color: 'var(--muted)' })
        }, 'Edit'),
        !isEditing && React.createElement('button', {
          onClick: function() { handleDelete(c.guid); },
          title: 'Delete comment',
          style: Object.assign({}, btnBase, { background: 'rgba(248,113,113,.1)', color: '#f87171' })
        }, 'Delete')
      ),
      isEditing
        ? React.createElement('div', null,
            React.createElement('div', { style: { marginBottom: 4 } },
              React.createElement('select', {
                value: editing.commentType,
                onChange: function(e) { setEditing(Object.assign({}, editing, { commentType: e.target.value })); },
                style: { background: 'var(--card)', border: '1px solid var(--border)', borderRadius: 4, color: 'var(--text)', fontSize: 11, padding: '3px 6px' }
              },
                TYPES.map(function(t) { return React.createElement('option', { key: t, value: t }, TYPE_LABEL[t]); })
              )
            ),
            React.createElement('textarea', {
              value: editing.text,
              onChange: function(e) { setEditing(Object.assign({}, editing, { text: e.target.value })); },
              onKeyDown: function(e) { if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) handleEditSave(); },
              rows: 3,
              style: { width: '100%', background: 'var(--card)', border: '1px solid var(--accent)', borderRadius: 4, color: 'var(--text)', fontSize: 12, padding: '6px 8px', resize: 'vertical', fontFamily: 'inherit', lineHeight: 1.5, outline: 'none', marginBottom: 4 }
            }),
            React.createElement('div', { style: { display: 'flex', gap: 6 } },
              React.createElement('button', {
                onClick: handleEditSave, disabled: editSaving || !editing.text.trim(),
                style: Object.assign({}, btnBase, { background: 'var(--accent)', color: '#fff', padding: '4px 14px' })
              }, editSaving ? '…' : 'Save'),
              React.createElement('button', {
                onClick: function() { setEditing(null); setEditErr(''); },
                style: Object.assign({}, btnBase, { background: 'var(--hover)', color: 'var(--muted)', padding: '4px 14px' })
              }, 'Cancel')
            ),
            editErr && React.createElement('div', { style: { color: '#f87171', fontSize: 11, marginTop: 4 } }, editErr)
          )
        : React.createElement('div', { style: { color: 'var(--text)', lineHeight: 1.55, whiteSpace: 'pre-wrap', wordBreak: 'break-word' } }, c.text)
    );
  }

  return React.createElement('div', { style: { marginTop: 28, borderTop: '1px solid var(--border)', paddingTop: 16 } },
    React.createElement('div', { style: { fontSize: 11, fontWeight: 700, color: 'var(--dim)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: 10, display: 'flex', alignItems: 'center', gap: 6 } },
      'Comments',
      !loading && React.createElement('span', { style: { background: 'rgba(96,165,250,.12)', color: 'var(--accent)', borderRadius: 8, padding: '0 6px', fontSize: 10, fontWeight: 600 } }, comments.length)
    ),
    loading
      ? React.createElement('div', { style: { fontSize: 12, color: 'var(--dim)', marginBottom: 12 } }, 'Loading…')
      : comments.length === 0
        ? React.createElement('div', { style: { fontSize: 12, color: 'var(--dim)', marginBottom: 12, fontStyle: 'italic' } }, 'No comments yet.')
        : React.createElement('div', { style: { marginBottom: 12 } }, comments.map(renderComment)),
    React.createElement('div', { style: { marginBottom: 6 } },
      React.createElement('select', {
        value: commentType,
        onChange: function(e) { setCommentType(e.target.value); },
        style: { background: 'var(--card)', border: '1px solid var(--border)', borderRadius: 4, color: 'var(--text)', fontSize: 11, padding: '3px 6px', cursor: 'pointer' }
      },
        TYPES.map(function(t) { return React.createElement('option', { key: t, value: t }, TYPE_LABEL[t]); })
      )
    ),
    React.createElement('div', { style: { display: 'flex', gap: 6 } },
      React.createElement('textarea', {
        value: text,
        onChange: function(e) { setText(e.target.value); },
        onKeyDown: function(e) { if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) handleSubmit(); },
        placeholder: 'Write a comment… (Ctrl/Cmd+Enter to post)',
        rows: 3,
        style: { flex: 1, background: 'var(--card)', border: '1px solid var(--border)', borderRadius: 4, color: 'var(--text)', fontSize: 12, padding: '6px 8px', resize: 'vertical', fontFamily: 'inherit', lineHeight: 1.5, outline: 'none' }
      }),
      React.createElement('button', {
        onClick: handleSubmit, disabled: submitting || !text.trim(),
        style: { alignSelf: 'flex-end', padding: '6px 14px', borderRadius: 4, border: 'none', background: (text.trim() && !submitting) ? 'var(--accent)' : 'var(--hover)', color: (text.trim() && !submitting) ? '#fff' : 'var(--dim)', cursor: (text.trim() && !submitting) ? 'pointer' : 'not-allowed', fontSize: 12, fontWeight: 600, flexShrink: 0 }
      }, submitting ? '…' : 'Post')
    ),
    errMsg && React.createElement('div', { style: { color: '#f87171', fontSize: 11, marginTop: 4 } }, errMsg)
  );
}

/* ──────────────────────────────────────────────────────────────────────────
 * Demo "Share your feedback" floating button (per-page feedback → /api/demo-feedback).
 * Canonical = the Egeria Explorer version (the richer superset: category +
 * "want a response"/consent). Shared by both SPAs. The Tech Catalog used to
 * carry a stripped-down copy that prefixed the page with "tech-catalog/"; pass
 * pagePrefix="tech-catalog/" to reproduce that. _SESSION_ID is a per-tab id.
 * ────────────────────────────────────────────────────────────────────────── */

var _SESSION_ID = (function() {
  try {
    var id = sessionStorage.getItem('_egeria_session_id');
    if (!id) {
      id = (crypto.randomUUID ? crypto.randomUUID() : Date.now().toString(36) + Math.random().toString(36).substr(2));
      sessionStorage.setItem('_egeria_session_id', id);
    }
    return id;
  } catch(e) { return 'anon-' + Date.now(); }
})();

// Props: section, persona, demoMode, srvManaged, pagePrefix (optional)
// Draggable position, persisted per-browser (shared localStorage key across
// every portal app, since this component is loaded from one static file and
// the button should stay wherever the user last put it regardless of which
// page they're on — moving it once should mean it's out of the way
// everywhere, not just on the page they moved it on).
var _FEEDBACK_POS_KEY = 'egeria-feedback-btn-pos';
function _loadFeedbackPos() {
  try {
    var raw = localStorage.getItem(_FEEDBACK_POS_KEY);
    if (!raw) return null;
    var p = JSON.parse(raw);
    if (typeof p.right === 'number' && typeof p.bottom === 'number') return p;
  } catch (e) {}
  return null;
}

function FeedbackButton({ section, persona, demoMode, srvManaged, pagePrefix }) {
  var _openState      = React.useState(false), open       = _openState[0],      setOpen       = _openState[1];
  var _rateState      = React.useState(0),     rating     = _rateState[0],      setRating     = _rateState[1];
  var _hoverState     = React.useState(0),     hover      = _hoverState[0],     setHover      = _hoverState[1];
  var _commentState   = React.useState(''),    comment    = _commentState[0],   setComment    = _commentState[1];
  var _emailState     = React.useState(''),    email      = _emailState[0],     setEmail      = _emailState[1];
  var _catState       = React.useState(''),    category   = _catState[0],       setCategory   = _catState[1];
  var _wantsState     = React.useState(false), wantsResp  = _wantsState[0],     setWantsResp  = _wantsState[1];
  var _consentState   = React.useState(false), consent    = _consentState[0],   setConsent    = _consentState[1];
  var _subState       = React.useState(false), submitted  = _subState[0],       setSubmitted  = _subState[1];
  var _submitting     = React.useState(false), submitting = _submitting[0],     setSubmitting = _submitting[1];

  // Draggable floating button — see _FEEDBACK_POS_KEY above. `posRef` is the
  // authoritative current position during a drag (updated synchronously on
  // every pointermove); `pos` state exists only to trigger re-renders for
  // the visible position. Reading posRef.current on pointerup (rather than
  // the `pos` closure) avoids persisting a stale position if React hasn't
  // finished re-rendering yet.
  var _posState = React.useState(function() { return _loadFeedbackPos() || { right: 20, bottom: 20 }; }),
      pos = _posState[0], setPos = _posState[1];
  var _draggingState = React.useState(false), dragging = _draggingState[0], setDragging = _draggingState[1];
  var posRef = React.useRef(pos);
  var btnRef = React.useRef(null);
  var dragRef = React.useRef({ active: false, moved: false, startX: 0, startY: 0, startRight: 0, startBottom: 0 });

  // Document-level mousemove/mouseup listeners (attached on mousedown,
  // removed on mouseup) rather than element-scoped pointer events +
  // setPointerCapture — the capture-based approach didn't reliably track
  // drags that move fast enough for the cursor to leave the small button's
  // own bounds between synthesized move events (confirmed via automated
  // browser testing: the drag fell through to the page's own text
  // selection instead of the button once the pointer left its rect).
  // Document-level listeners keep tracking regardless of what's under the
  // cursor, the standard robust pattern for this kind of drag.
  function onDragMove(e) {
    var d = dragRef.current;
    if (!d.active) return;
    var dx = e.clientX - d.startX, dy = e.clientY - d.startY;
    if (Math.abs(dx) > 3 || Math.abs(dy) > 3) d.moved = true;
    if (!d.moved) return; // stay put until past the click-vs-drag threshold
    var btnW = (btnRef.current && btnRef.current.offsetWidth) || 110;
    var btnH = (btnRef.current && btnRef.current.offsetHeight) || 34;
    var next = {
      right:  Math.min(Math.max(d.startRight - dx, 4), window.innerWidth - btnW - 4),
      bottom: Math.min(Math.max(d.startBottom - dy, 4), window.innerHeight - btnH - 4),
    };
    posRef.current = next;
    setPos(next);
  }
  function onDragEnd() {
    var d = dragRef.current;
    if (!d.active) return;
    d.active = false;
    setDragging(false);
    document.removeEventListener('mousemove', onDragMove);
    document.removeEventListener('mouseup', onDragEnd);
    document.removeEventListener('touchmove', onDragTouchMove);
    document.removeEventListener('touchend', onDragEnd);
    if (d.moved) {
      try { localStorage.setItem(_FEEDBACK_POS_KEY, JSON.stringify(posRef.current)); } catch (err) {}
    }
  }
  function onDragTouchMove(e) {
    if (e.touches && e.touches[0]) onDragMove({ clientX: e.touches[0].clientX, clientY: e.touches[0].clientY });
  }
  function beginDrag(clientX, clientY) {
    dragRef.current = {
      active: true, moved: false, startX: clientX, startY: clientY,
      startRight: posRef.current.right, startBottom: posRef.current.bottom,
    };
    setDragging(true);
    document.addEventListener('mousemove', onDragMove);
    document.addEventListener('mouseup', onDragEnd);
    document.addEventListener('touchmove', onDragTouchMove, { passive: false });
    document.addEventListener('touchend', onDragEnd);
  }
  function onDragMouseDown(e) {
    if (e.button !== 0) return; // left-click only
    e.preventDefault(); // avoid the page's own text-selection drag
    beginDrag(e.clientX, e.clientY);
  }
  function onDragTouchStart(e) {
    if (e.touches && e.touches[0]) beginDrag(e.touches[0].clientX, e.touches[0].clientY);
  }
  function handleButtonClick() {
    // A drag-release fires a click right after on most browsers — suppress
    // just that one so dragging the button doesn't also pop the panel open.
    if (dragRef.current.moved) { dragRef.current.moved = false; return; }
    setOpen(true); setSubmitted(false);
  }

  var env = demoMode ? 'quickstart-demo' : srvManaged ? 'freshstart' : 'quickstart-local';

  function handleClose() {
    setOpen(false); setRating(0); setComment(''); setEmail('');
    setCategory(''); setWantsResp(false); setConsent(false);
    setSubmitted(false); setHover(0);
  }

  function handleSubmit() {
    if (!rating && !comment.trim()) return;
    setSubmitting(true);
    fetch('/api/demo-feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id:         _SESSION_ID,
        page:               (pagePrefix || '') + (section || 'splash'),
        rating:             rating || null,
        category:           category || null,
        message:            comment.trim() || null,
        email:              email.trim() || null,
        wants_response:     wantsResp,
        consent_to_contact: consent,
        persona:            persona || null,
        env:                env,
        viewport:           window.innerWidth + 'x' + window.innerHeight,
        locale:             navigator.language || null,
      }),
    }).then(function() {
      setSubmitted(true);
      setTimeout(handleClose, 2000);
    }).catch(function() {
      setSubmitting(false);
    }).finally(function() {
      setSubmitting(false);
    });
  }

  var floatingBtn = React.createElement('button', {
    ref: btnRef,
    onClick: handleButtonClick,
    onMouseDown: onDragMouseDown,
    onTouchStart: onDragTouchStart,
    title: 'Share your feedback — drag to move',
    style: { position: 'fixed', bottom: pos.bottom, right: pos.right, zIndex: 900, background: 'var(--accent)', color: '#fff',
             border: 'none', borderRadius: 20, padding: '7px 15px', fontSize: 12, fontWeight: 600,
             cursor: dragging ? 'grabbing' : 'grab', boxShadow: '0 2px 8px rgba(0,0,0,0.3)', letterSpacing: '0.02em',
             touchAction: 'none', userSelect: 'none' }
  }, '💬 Feedback');

  if (!open) return floatingBtn;

  // Open the feedback panel near wherever the button currently is, rather
  // than always assuming bottom-right — otherwise a button dragged to the
  // top-left would still pop its panel up on the opposite side of the screen.
  var nearLeft = pos.right > window.innerWidth / 2;
  var nearTop = pos.bottom > window.innerHeight / 2;

  var stars = [1,2,3,4,5].map(function(n) {
    var active = (hover || rating) >= n;
    return React.createElement('span', { key: n,
      onClick: function() { setRating(n); },
      onMouseEnter: function() { setHover(n); }, onMouseLeave: function() { setHover(0); },
      style: { fontSize: 26, cursor: 'pointer', color: active ? '#f59e0b' : 'var(--dim)', lineHeight: 1 }
    }, active ? '★' : '☆');
  });

  var inp = { width: '100%', boxSizing: 'border-box', background: 'var(--bg)', border: '1px solid var(--border)',
              borderRadius: 6, padding: '7px 9px', color: 'var(--text)', fontSize: 12, fontFamily: 'inherit', outline: 'none' };
  var chkRow = { display: 'flex', alignItems: 'center', gap: 6, fontSize: 12, color: 'var(--muted)', marginBottom: 6 };
  var canSubmit = !submitting && (rating > 0 || comment.trim().length > 0);

  return React.createElement(React.Fragment, null, floatingBtn,
    React.createElement('div', {
      onClick: function(e) { if (e.target === e.currentTarget) handleClose(); },
      style: { position: 'fixed', inset: 0, zIndex: 1000, background: 'rgba(0,0,0,0.45)',
               display: 'flex', alignItems: nearTop ? 'flex-start' : 'flex-end',
               justifyContent: nearLeft ? 'flex-start' : 'flex-end', padding: 24 }
    },
      React.createElement('div', { style: { background: 'var(--surface,var(--card))', border: '1px solid var(--border)',
          borderRadius: 12, padding: '22px 26px', width: 360, boxShadow: '0 8px 32px rgba(0,0,0,0.3)' } },
        submitted
          ? React.createElement('div', { style: { textAlign: 'center', padding: '16px 0', color: 'var(--accent)', fontSize: 15, fontWeight: 600 } },
              '✓ Thank you for your feedback!')
          : React.createElement(React.Fragment, null,
              React.createElement('div', { style: { fontWeight: 700, fontSize: 14, marginBottom: 4 } }, 'Share your feedback'),
              React.createElement('div', { style: { fontSize: 11, color: 'var(--muted)', marginBottom: 12 } },
                'Page: ', React.createElement('span', { style: { color: 'var(--text)', fontFamily: 'ui-monospace,monospace', fontSize: 10 } }, (pagePrefix || '') + (section || 'splash'))),
              React.createElement('div', { style: { display: 'flex', gap: 3, marginBottom: 10 } }, ...stars),
              React.createElement('select', { value: category, onChange: function(e) { setCategory(e.target.value); },
                style: Object.assign({}, inp, { marginBottom: 8 }) },
                React.createElement('option', { value: '' }, 'Category (optional)'),
                ['Bug', 'Confusing', 'Suggestion', 'Praise'].map(function(c) {
                  return React.createElement('option', { key: c, value: c.toLowerCase() }, c); })
              ),
              React.createElement('textarea', { placeholder: "What's on your mind?", value: comment,
                onChange: function(e) { setComment(e.target.value); }, rows: 3,
                style: Object.assign({}, inp, { resize: 'vertical', marginBottom: 8 }) }),
              React.createElement('input', { type: 'email', placeholder: 'Email for follow-up (optional)',
                value: email, onChange: function(e) { setEmail(e.target.value); },
                style: Object.assign({}, inp, { marginBottom: 10 }) }),
              React.createElement('div', { style: chkRow },
                React.createElement('input', { type: 'checkbox', checked: wantsResp, onChange: function(e) { setWantsResp(e.target.checked); } }),
                'I\'d like a response'),
              React.createElement('div', { style: Object.assign({}, chkRow, { marginBottom: 14 }) },
                React.createElement('input', { type: 'checkbox', checked: consent, onChange: function(e) { setConsent(e.target.checked); } }),
                'OK to contact me about this feedback'),
              React.createElement('div', { style: { display: 'flex', gap: 8, justifyContent: 'flex-end' } },
                React.createElement('button', { onClick: handleClose, style: { padding: '6px 14px', borderRadius: 6, border: '1px solid var(--border)', background: 'transparent', color: 'var(--text)', cursor: 'pointer', fontSize: 12 } }, 'Cancel'),
                React.createElement('button', { onClick: handleSubmit, disabled: !canSubmit, style: { padding: '6px 14px', borderRadius: 6, border: 'none', background: 'var(--accent)', color: '#fff', cursor: canSubmit ? 'pointer' : 'default', opacity: canSubmit ? 1 : 0.45, fontSize: 12, fontWeight: 600 } },
                  submitting ? 'Sending…' : 'Send')
              )
            )
      )
    )
  );
}

/* ──────────────────────────────────────────────────────────────────────────
 * Credential context — provides Egeria connection params (or a token) to all
 * child components without prop-drilling. Both SPAs wrap their tree in
 * CredContext.Provider value={creds}; shared components read it via useContext
 * and pass it to egeriaFetch. (Was previously Explorer-only; the Tech Catalog
 * prop-drilled instead — unified here so credential handling is identical.)
 * ────────────────────────────────────────────────────────────────────────── */
var CredContext = React.createContext({ url: '', server: '', userId: '', password: '' });

// PersonaContext — the active persona/user ID for the favorites API (null if unknown).
// Set by each SPA's App via PersonaContext.Provider and read by detail panels.
var PersonaContext = React.createContext(null);

/* Single lazy-loading diagram panel. fetchUrl is called on first open; label
 * appears in the header. field: which key to read from the JSON response
 * (default 'mermaidGraph'). Reads creds from CredContext + uses egeriaFetch so
 * the call is token-aware in every auth mode. Canonical = the Explorer version. */
function DiagramPanel({ fetchUrl, label, buttonLabel, field }) {
  const [code, setCode]       = React.useState(null);   // null=unfetched, ''=empty, string=content
  const [loading, setLoading] = React.useState(false);
  const [visible, setVisible] = React.useState(false);
  const creds = React.useContext(CredContext);

  var btnStyle = { fontSize: 12, padding: '3px 10px', borderRadius: 4, border: '1px solid var(--border)', background: 'rgba(96,165,250,.08)', color: 'var(--accent)', cursor: 'pointer' };
  var readField = field || 'mermaidGraph';

  function toggle() {
    if (code === null && !loading) {
      setLoading(true);
      setVisible(true);
      egeriaFetch(fetchUrl, creds)
        .then(function(r) { return r.ok ? r.json() : null; })
        .then(function(data) {
          var val = data && (data.graphs && data.graphs[readField]) ? data.graphs[readField]
                  : data && data[readField] ? data[readField] : '';
          setCode(val); setLoading(false);
        })
        .catch(function() { setCode(''); setLoading(false); });
    } else {
      setVisible(function(v) { return !v; });
    }
  }

  var btnLabel = visible ? ('▦ Hide ' + label) : (code !== null ? ('▦ Show ' + label) : buttonLabel);

  return React.createElement('div', { style: { margin: '4px 0' } },
    React.createElement('button', { onClick: toggle, style: btnStyle }, btnLabel),
    visible && loading && React.createElement('div', { style: { fontSize: 11, color: 'var(--dim)', padding: '6px 0' } }, 'Loading diagram…'),
    visible && !loading && code === '' && React.createElement('div', { style: { fontSize: 11, color: 'var(--dim)', padding: '4px 0' } }, 'No diagram available for this element.'),
    visible && !loading && code && React.createElement(MermaidDiagram, { code: code })
  );
}

/* Context diagram + anchored graph buttons for any element GUID. */
function MermaidSection({ guid }) {
  if (!guid) return null;
  return React.createElement('div', { style: { margin: '8px 0' } },
    React.createElement(DiagramPanel, {
      key: 'ctx:' + guid,
      fetchUrl: '/api/mermaid/' + encodeURIComponent(guid),
      label: 'Context Diagram',
      buttonLabel: '▦ Load Context Diagram'
    }),
    React.createElement(DiagramPanel, {
      key: 'anc:' + guid,
      fetchUrl: '/api/mermaid/' + encodeURIComponent(guid) + '/anchored',
      label: 'Anchored Graph',
      buttonLabel: '▦ Load Anchored Graph'
    })
  );
}

/* Reverse SemanticAssignment lookup for a glossary term: "which physical and
 * logical elements are assigned this term?" — split into two groups server-
 * side (glossary_handler.py's /assigned-elements, backed by semantic_links.py)
 * so a schema column and a Data Design DataField that mean the same thing
 * show up together here, even though they live in different apps/tabs.
 * Click-to-load, same convention as DiagramPanel above. */
function AssignedElementsSection({ termGuid, onNavigateToElement, isElementLinkable }) {
  const [data, setData]       = React.useState(null);
  const [loading, setLoading] = React.useState(false);
  const [visible, setVisible] = React.useState(false);
  const creds = React.useContext(CredContext);
  var btnStyle = { fontSize: 12, padding: '3px 10px', borderRadius: 4, border: '1px solid var(--border)', background: 'rgba(96,165,250,.08)', color: 'var(--accent)', cursor: 'pointer' };

  function toggle() {
    if (data === null && !loading) {
      setLoading(true); setVisible(true);
      egeriaFetch('/api/glossary/term/' + encodeURIComponent(termGuid) + '/assigned-elements', creds)
        .then(function(r) { return r.ok ? r.json() : null; })
        .then(function(j) { setData(j || { physical: [], logical: [], other: [], total: 0 }); setLoading(false); })
        .catch(function() { setData({ physical: [], logical: [], other: [], total: 0 }); setLoading(false); });
    } else {
      setVisible(function(v) { return !v; });
    }
  }

  var btnLabel = visible ? '▦ Hide assigned elements'
               : (data !== null ? '▦ Show assigned elements' : '▦ Where is this used? (physical & logical elements)');

  function renderGroup(title, items) {
    if (!items || !items.length) return null;
    return React.createElement('div', { style: { marginBottom: 10 } },
      React.createElement('div', { style: { fontSize: 11, color: 'var(--muted)', fontWeight: 600, marginBottom: 4 } }, title + ' (' + items.length + ')'),
      items.map(function(el) {
        var linkable = onNavigateToElement && isElementLinkable && isElementLinkable(el);
        return React.createElement('div', { key: el.guid, style: { display: 'flex', alignItems: 'center', gap: 6, padding: '3px 0', borderTop: '1px solid var(--border)' } },
          React.createElement('span', { style: { flex: 1, fontSize: 12, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }, title: el.qualifiedName || el.guid }, el.displayName || el.qualifiedName || el.guid),
          el.typeName && React.createElement('span', { style: { fontSize: 10, color: 'var(--dim)', flexShrink: 0 } }, el.typeName),
          linkable && React.createElement('button', { onClick: function() { onNavigateToElement(el); }, style: { fontSize: 11, padding: '2px 8px', borderRadius: 4, border: '1px solid rgba(96,165,250,.4)', background: 'rgba(96,165,250,.08)', color: 'var(--accent)', cursor: 'pointer' } }, 'View →')
        );
      })
    );
  }

  return React.createElement('div', { style: { margin: '4px 0 12px' } },
    React.createElement('button', { onClick: toggle, style: btnStyle }, btnLabel),
    visible && loading && React.createElement('div', { style: { fontSize: 11, color: 'var(--dim)', padding: '6px 0' } }, 'Looking up assigned elements…'),
    visible && !loading && data && data.total === 0 && React.createElement('div', { style: { fontSize: 11, color: 'var(--dim)', padding: '4px 0' } }, 'No physical or logical elements are assigned this term yet.'),
    visible && !loading && data && data.total > 0 && React.createElement('div', { style: { marginTop: 8 } },
      renderGroup('Physical elements', data.physical),
      renderGroup('Logical elements', data.logical),
      renderGroup('Other', data.other)
    )
  );
}

/* ──────────────────────────────────────────────────────────────────────────
 * Glossary detail panes — shared by both SPAs. Visual design = the Tech
 * Catalog's (Properties / Classifications section headers + cards). The folder
 * pane carries the MermaidSection context graph (previously Explorer-only). The
 * term pane takes optional cross-link callbacks — onNavigateToTerm always;
 * onNavigateToDataDesign / onNavigateToElement render only when the host SPA
 * provides them, plus an injected isElementLinkable(item) predicate (each SPA
 * decides what it can route to). Depends on shared _glsBadge / MermaidSection /
 * renderMd / EgeriaFeedbackWidget / EgeriaCommentsSection; CSS var --classif.
 * ────────────────────────────────────────────────────────────────────────── */
var _glsBadge = { display: 'inline-block', fontSize: 10, fontWeight: 600, padding: '1px 7px', borderRadius: 10, border: '0.5px solid rgba(96,165,250,.3)', background: 'rgba(96,165,250,.1)', color: 'var(--accent)' };

function GlossaryFolderDetail({ folder }) {
  if (!folder) return null;
  var sHdr = { fontSize: 11, fontWeight: 700, letterSpacing: '0.07em', textTransform: 'uppercase', color: 'var(--accent)', marginBottom: 8, marginTop: 20 };
  return React.createElement('div', { style: { padding: '20px 24px', overflowY: 'auto', height: '100%' } },
    React.createElement('div', { style: { display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4 } },
      React.createElement('div', { style: { fontSize: 18, fontWeight: 700, color: 'var(--text)', flex: 1 } }, folder.displayName || folder.qualifiedName),
      React.createElement('span', { style: _glsBadge }, 'Folder'),
      React.createElement(HeaderInfoButton, { header: folder._header }),
      React.createElement(CopyJsonButton, { data: folder })
    ),
    folder.description && React.createElement('p', { style: { fontSize: 13, lineHeight: 1.6, marginBottom: 16, color: 'var(--muted)' } }, folder.description),
    React.createElement('div', null,
      React.createElement('div', { style: sHdr }, 'Properties'),
      React.createElement(GenericPropertiesTable, { item: folder, priority: ['description'] })
    ),
    // Classifications (foldable) + "Copy raw JSON" debug affordance — see
    // GlossaryTermDetail's identical switch for why (Dan's catch, 2026-08-18).
    React.createElement(ClassificationsAndRawJson, { item: folder }),
    // A CollectionFolder is a Collection — surface its context/anchored graphs.
    React.createElement(MermaidSection, { guid: folder.guid })
  );
}

function GlossaryDetail({ glossary }) {
  if (!glossary) return null;
  var sHdr   = { fontSize: 11, fontWeight: 700, letterSpacing: '0.07em', textTransform: 'uppercase', color: 'var(--accent)', marginBottom: 8, marginTop: 20 };
  return React.createElement('div', { style: { padding: '20px 24px', overflowY: 'auto', height: '100%' } },
    React.createElement('div', { style: { display: 'flex', alignItems: 'center', gap: 10, marginBottom: 8 } },
      React.createElement('h2', { style: { fontSize: 18, fontWeight: 700, margin: 0, color: 'var(--text)', flex: 1 } }, glossary.displayName || glossary.qualifiedName || glossary.guid),
      React.createElement('span', { style: _glsBadge }, 'Glossary'),
      React.createElement(HeaderInfoButton, { header: glossary._header }),
      React.createElement(CopyJsonButton, { data: glossary })
    ),
    glossary.description && React.createElement('p', { style: { fontSize: 13, color: 'var(--muted)', lineHeight: 1.6, margin: '0 0 16px' } }, glossary.description),
    React.createElement('div', null,
      React.createElement('div', { style: sHdr }, 'Properties'),
      React.createElement(GenericPropertiesTable, { item: glossary, priority: ['description'] })
    ),
    // Classifications (foldable) + "Copy raw JSON" debug affordance — see
    // GlossaryTermDetail's identical switch for why (Dan's catch, 2026-08-18).
    React.createElement(ClassificationsAndRawJson, { item: glossary }),
    React.createElement(MermaidSection, { guid: glossary.guid })
  );
}

function GlossaryTermDetail({ term, onNavigateToTerm, onNavigateToDataDesign, onNavigateToElement, isElementLinkable }) {
  if (!term) return null;
  var personaId = React.useContext(PersonaContext);
  var sHdr   = { fontSize: 11, fontWeight: 700, letterSpacing: '0.07em', textTransform: 'uppercase', color: 'var(--accent)', marginBottom: 8, marginTop: 20 };
  var folderList = term.folders || [];
  var relGroups  = Object.entries(term.relationships || {}).filter(function(e) { return e[1].length > 0; });
  var relBtnStyle = { fontSize: 11, padding: '2px 8px', borderRadius: 4, border: '1px solid rgba(96,165,250,.4)', background: 'rgba(96,165,250,.08)', color: 'var(--accent)', cursor: 'pointer' };
  var ddBtnStyle  = { fontSize: 11, padding: '2px 8px', borderRadius: 4, border: '1px solid rgba(94,234,212,.4)', background: 'rgba(94,234,212,.1)', color: '#5eead4', cursor: 'pointer' };
  var DD_TYPES = { DataField: true, DataStructure: true, DataSpec: true, DataGrain: true, DataClass: true };
  var termFavUrl = '/egeria-explorer?guid=' + encodeURIComponent(term.guid) + '#glossary';
  return React.createElement('div', { style: { padding: '20px 24px', overflowY: 'auto', height: '100%' } },
    React.createElement('div', { style: { display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4, flexWrap: 'wrap' } },
      React.createElement('div', { style: { fontSize: 18, fontWeight: 700, color: 'var(--text)' } }, term.displayName),
      term.isTemplateSubstitute && React.createElement('span', { style: Object.assign({}, _glsBadge, { background: 'rgba(245,158,11,.15)', color: '#fbbf24', border: '0.5px solid rgba(245,158,11,.4)' }) }, 'Template Substitute'),
      !term.isTemplateSubstitute && term.isSourcedFromTemplate && React.createElement('span', { style: Object.assign({}, _glsBadge, { background: 'rgba(245,158,11,.08)', color: '#fbbf24', border: '0.5px solid rgba(245,158,11,.25)' }) }, 'From Template'),
      React.createElement('div', { style: { marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: 4 } },
        personaId && React.createElement(FavoriteButton, { app: 'type-explorer', section: 'glossary', label: term.displayName || term.qualifiedName, icon: '≡', url: termFavUrl, personaId: personaId }),
        React.createElement(EgeriaFeedbackWidget, { guid: term.guid })
      ),
      React.createElement(HeaderInfoButton, { header: term._header }),
      React.createElement(CopyJsonButton, { data: term })
    ),
    folderList.length > 0 && React.createElement('div', { style: { display: 'flex', flexWrap: 'wrap', gap: 4, marginBottom: 8, marginTop: 6 } },
      React.createElement('span', { style: { fontSize: 11, color: 'var(--dim)', marginRight: 4 } }, 'Folders:'),
      folderList.map(function(f) { return React.createElement('span', { key: f.guid, style: Object.assign({}, _glsBadge, { background: 'rgba(99,102,241,.1)', color: '#818cf8', border: '0.5px solid rgba(99,102,241,.25)' }) }, f.displayName || f.guid); })
    ),
    term.description && React.createElement('div', { style: { fontSize: 13, marginBottom: 16, color: 'var(--text)' } }, renderMd(term.description)),
    React.createElement(MermaidSection, { guid: term.guid }),
    React.createElement('div', null,
      React.createElement('div', { style: sHdr }, 'Properties'),
      React.createElement(GenericPropertiesTable, { item: term, skip: ['description', 'folders', 'isTemplateSubstitute', 'isSourcedFromTemplate'], renderValue: function(key, val) { return renderMd(val); } })
    ),
    // Classifications (foldable) + "Copy raw JSON" debug affordance — was a
    // hand-rolled always-open block here; switched to the shared component
    // both to pick up RawJsonViewer (missing from Glossary entirely until
    // now, Dan's catch 2026-08-18 — BACKLOG.md already flagged this as a
    // known gap since the 2026-07-22 rollout) and because PrimeWord/
    // ClassWord/Modifier classifications only became visible at all once
    // glossary_handler.py's _extract_classifications learned to also read
    // list-valued header keys like glossaryTermKinds, not just individually
    // named ElementClassification keys (see that function's own docstring).
    React.createElement(ClassificationsAndRawJson, { item: term }),
    React.createElement('div', { style: { marginTop: 16, paddingTop: 12, borderTop: '1px solid var(--border)' } },
      React.createElement('div', { style: sHdr }, 'Assigned Elements'),
      React.createElement(AssignedElementsSection, { termGuid: term.guid, onNavigateToElement: onNavigateToElement, isElementLinkable: isElementLinkable })
    ),
    relGroups.length > 0 && React.createElement('div', { style: { marginTop: 16, paddingTop: 12, borderTop: '1px solid var(--border)' } },
      React.createElement('div', { style: sHdr }, 'Relationships'),
      relGroups.map(function(entry) {
        var label = entry[0], items = entry[1];
        return React.createElement('div', { key: label, style: { marginBottom: 12 } },
          React.createElement('div', { style: { fontSize: 11, color: 'var(--muted)', fontWeight: 600, marginBottom: 4 } }, label),
          items.map(function(item) {
            var isDD   = DD_TYPES[item.typeName];
            var isTerm = !item.typeName || item.typeName === 'GlossaryTerm';
            var isGeneric = !isTerm && !isDD && onNavigateToElement && isElementLinkable && isElementLinkable(item);
            return React.createElement('div', { key: item.guid, style: { display: 'flex', alignItems: 'center', gap: 6, padding: '3px 0', borderTop: '1px solid var(--border)' } },
              React.createElement('span', { style: { flex: 1, fontSize: 12, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }, title: item.qualifiedName || item.guid }, item.displayName || item.qualifiedName || item.guid),
              item.typeName && !isTerm && React.createElement('span', { style: { fontSize: 10, color: 'var(--dim)', flexShrink: 0 } }, item.typeName),
              isTerm    && onNavigateToTerm       && React.createElement('button', { onClick: function() { onNavigateToTerm(item.guid); },                       style: relBtnStyle }, 'View →'),
              isDD      && onNavigateToDataDesign && React.createElement('button', { onClick: function() { onNavigateToDataDesign(item.typeName, item.guid); }, style: ddBtnStyle  }, 'View in Data Design →'),
              isGeneric                           && React.createElement('button', { onClick: function() { onNavigateToElement(item); },                         style: relBtnStyle }, 'View →')
            );
          })
        );
      })
    ),
    React.createElement(EgeriaCommentsSection, { guid: term.guid })
  );
}

/* ───────────────────────────────────────────────────────────────────────────
 * Tabular data preview modal (resizable cols, filter, sort, paging). Shared by
 * the Explorer's Digital Products (TabularDataSet) and the Tech Catalog's file
 * Data Assets (TC-13). Caller passes a `fetchUrl` that returns {columns, rows,
 * has_more}; egeriaFetch adds creds/token. `name` is the display label.
 * ─────────────────────────────────────────────────────────────────────────── */
function TabularPreviewModal({ fetchUrl, name, creds, onClose }) {
  var PAGE_SIZE = 100;
  var DEFAULT_COL_W = 150;
  var MIN_COL_W = 40;

  var _pageState     = React.useState(0),    page      = _pageState[0],     setPage      = _pageState[1];
  var _dataState     = React.useState(null), tableData = _dataState[0],     setTableData = _dataState[1];
  var _loadState     = React.useState(true), loading   = _loadState[0],     setLoading   = _loadState[1];
  var _errState      = React.useState(''),   errMsg    = _errState[0],      setErrMsg    = _errState[1];
  var _colWState     = React.useState(null), colWidths = _colWState[0],     setColWidths = _colWState[1];
  var _draggingState = React.useState(false),isDragging= _draggingState[0], setIsDragging= _draggingState[1];
  var dragRef = React.useRef(null); // { colIdx, startX, startW }
  var _filterState = React.useState(''),   filterText = _filterState[0], setFilterText = _filterState[1];
  var _sortState   = React.useState(null), sortState  = _sortState[0],   setSortState  = _sortState[1];

  React.useEffect(function() {
    setLoading(true); setErrMsg(''); setColWidths(null);
    var params = new URLSearchParams({ start_from_row: page * PAGE_SIZE, max_row_count: PAGE_SIZE });
    // egeriaFetch adds url/server/user_id + the X-Egeria-Token header (no password in the URL).
    egeriaFetch(fetchUrl + (fetchUrl.indexOf('?') === -1 ? '?' : '&') + params.toString(), creds)
      .then(function(r) { return r.json(); })
      .then(function(d) {
        setTableData(d);
        setLoading(false);
        if (d && d.columns && d.columns.length) {
          setColWidths(d.columns.map(function() { return DEFAULT_COL_W; }));
        }
      })
      .catch(function(e) { setErrMsg('Failed to load data: ' + e); setLoading(false); });
  }, [fetchUrl, page]);

  var columns = (tableData && tableData.columns) || [];
  var rows    = (tableData && tableData.rows)    || [];
  var hasMore = tableData && tableData.has_more;

  // Client-side filter + sort applied to the current page of rows
  var visRows = rows;
  if (filterText.trim()) {
    var q = filterText.trim().toLowerCase();
    visRows = visRows.filter(function(row) {
      var cells = Array.isArray(row) ? row : columns.map(function(c) { return row[c]; });
      return cells.some(function(cell) { return cell != null && String(cell).toLowerCase().indexOf(q) !== -1; });
    });
  }
  if (sortState) {
    var si = sortState.col, sd = sortState.dir;
    visRows = visRows.slice().sort(function(a, b) {
      var ca = Array.isArray(a) ? a[si] : a[columns[si]];
      var cb = Array.isArray(b) ? b[si] : b[columns[si]];
      var sa = ca == null ? '' : String(ca), sb = cb == null ? '' : String(cb);
      var n = (!isNaN(sa) && !isNaN(sb)) ? Number(sa) - Number(sb) : sa.localeCompare(sb);
      return sd === 'asc' ? n : -n;
    });
  }

  function toggleSort(idx) {
    setSortState(function(prev) {
      if (!prev || prev.col !== idx) return { col: idx, dir: 'asc' };
      if (prev.dir === 'asc') return { col: idx, dir: 'desc' };
      return null;
    });
  }

  var tableWidth = colWidths ? colWidths.reduce(function(s, w) { return s + w; }, 0) : undefined;

  function onResizeMouseDown(e, idx) {
    e.preventDefault();
    var startW = colWidths ? colWidths[idx] : DEFAULT_COL_W;
    dragRef.current = { colIdx: idx, startX: e.clientX, startW: startW };
    setIsDragging(true);

    function onMouseMove(ev) {
      if (!dragRef.current) return;
      var dx = ev.clientX - dragRef.current.startX;
      var newW = Math.max(MIN_COL_W, dragRef.current.startW + dx);
      setColWidths(function(prev) {
        var next = (prev || columns.map(function() { return DEFAULT_COL_W; })).slice();
        next[dragRef.current.colIdx] = newW;
        return next;
      });
    }
    function onMouseUp() {
      dragRef.current = null;
      setIsDragging(false);
      document.removeEventListener('mousemove', onMouseMove);
      document.removeEventListener('mouseup', onMouseUp);
    }
    document.addEventListener('mousemove', onMouseMove);
    document.addEventListener('mouseup', onMouseUp);
  }

  var thBase = { padding: '6px 12px', textAlign: 'left', borderBottom: '2px solid var(--border)',
                 color: 'var(--accent)', fontSize: 11, position: 'relative',
                 overflow: 'hidden', whiteSpace: 'nowrap', userSelect: 'none' };
  var tdBase = { padding: '4px 12px', borderBottom: '1px solid var(--border)',
                 borderRight: '1px dotted var(--border)',
                 overflow: 'hidden', whiteSpace: 'nowrap', textOverflow: 'ellipsis' };
  var handleStyle = { position: 'absolute', right: 0, top: 0, bottom: 0, width: 6,
                      cursor: 'col-resize', zIndex: 1,
                      borderRight: '2px dotted rgba(96,165,250,0.5)', boxSizing: 'border-box' };

  return React.createElement('div', {
    style: { position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.7)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000,
             cursor: isDragging ? 'col-resize' : undefined },
    onClick: function(e) { if (!isDragging && e.target === e.currentTarget) onClose(); }
  },
    React.createElement('div', { style: { background: 'var(--panel)', border: '1px solid var(--border)', borderRadius: 8, width: '90vw', minHeight: '60vh', maxHeight: '88vh', display: 'flex', flexDirection: 'column', overflow: 'hidden' } },
      // Header
      React.createElement('div', { style: { display: 'flex', alignItems: 'center', padding: '12px 20px', borderBottom: '1px solid var(--border)', gap: 12 } },
        React.createElement('div', { style: { flex: 1, fontWeight: 700, fontSize: 15 } }, '📊 Data Preview — ' + (name || 'data')),
        React.createElement('div', { style: { fontSize: 11, color: 'var(--dim)' } }, 'Page ' + (page + 1) + (tableData ? ' · ' + rows.length + ' rows' : '')),
        React.createElement('button', { onClick: onClose, style: { marginLeft: 8, padding: '4px 12px', borderRadius: 4, border: '1px solid var(--border)', background: 'transparent', color: 'var(--text)', cursor: 'pointer' } }, 'Close')
      ),
      // Filter bar
      !loading && columns.length > 0 && React.createElement('div', { style: { padding: '6px 20px', borderBottom: '1px solid var(--border)', display: 'flex', alignItems: 'center', gap: 8 } },
        React.createElement('input', {
          type: 'search', placeholder: 'Filter / search rows…', value: filterText,
          onChange: function(e) { setFilterText(e.target.value); },
          style: { flex: 1, fontSize: 12, padding: '4px 8px', borderRadius: 4, border: '1px solid var(--border)', background: 'var(--bg)', color: 'inherit', outline: 'none' }
        }),
        filterText && React.createElement('button', {
          onClick: function() { setFilterText(''); },
          style: { fontSize: 11, padding: '3px 8px', borderRadius: 4, border: '1px solid var(--border)', background: 'transparent', color: 'var(--dim)', cursor: 'pointer' }
        }, '✕ Clear')
      ),
      // Body
      React.createElement('div', { style: { overflowY: 'auto', overflowX: 'auto', flex: 1 } },
        loading ? React.createElement('div', { style: { padding: 40, textAlign: 'center', color: 'var(--dim)' } }, 'Loading…')
        : errMsg ? React.createElement('div', { style: { padding: 24, color: '#f87171' } }, errMsg)
        : columns.length === 0 ? React.createElement('div', { style: { padding: 24, color: 'var(--dim)' } }, 'No tabular data returned. The data set may be empty or the format unsupported.')
        : React.createElement('table', { style: { tableLayout: 'fixed', borderCollapse: 'collapse', fontSize: 12, width: tableWidth ? tableWidth + 'px' : '100%', minWidth: '100%' } },
            React.createElement('colgroup', null,
              columns.map(function(col, i) {
                return React.createElement('col', { key: col, style: { width: (colWidths ? colWidths[i] : DEFAULT_COL_W) + 'px' } });
              })
            ),
            React.createElement('thead', { style: { position: 'sticky', top: 0, background: 'var(--panel)', zIndex: 2 } },
              React.createElement('tr', null,
                columns.map(function(col, i) {
                  var isSorted = sortState && sortState.col === i;
                  var sortIcon = isSorted ? (sortState.dir === 'asc' ? ' ↑' : ' ↓') : ' ↕';
                  return React.createElement('th', { key: col, style: Object.assign({}, thBase, { cursor: 'pointer' }),
                    onClick: function() { toggleSort(i); }
                  },
                    col + sortIcon,
                    React.createElement('div', {
                      style: handleStyle,
                      onMouseDown: function(e) { e.stopPropagation(); onResizeMouseDown(e, i); },
                      onMouseEnter: function(e) { e.currentTarget.style.borderRight = '2px solid var(--accent)'; },
                      onMouseLeave: function(e) { e.currentTarget.style.borderRight = '2px dotted rgba(96,165,250,0.5)'; },
                    })
                  );
                })
              )
            ),
            React.createElement('tbody', null,
              visRows.length === 0
                ? React.createElement('tr', null, React.createElement('td', { colSpan: columns.length, style: { padding: 24, textAlign: 'center', color: 'var(--dim)' } }, filterText.trim() ? 'No rows match the filter.' : 'No rows returned from the server.'))
                : visRows.map(function(row, i) {
                    var cells = Array.isArray(row) ? row : columns.map(function(c) { return row[c]; });
                    return React.createElement('tr', { key: i, style: { background: i % 2 ? 'rgba(255,255,255,0.02)' : 'transparent' } },
                      cells.map(function(cell, j) {
                        return React.createElement('td', { key: j, style: tdBase }, cell == null ? '' : String(cell));
                      })
                    );
                  })
            )
          )
      ),
      // Footer / paging
      React.createElement('div', { style: { display: 'flex', gap: 8, padding: '10px 20px', borderTop: '1px solid var(--border)', alignItems: 'center' } },
        React.createElement('button', { disabled: page === 0 || loading, onClick: function() { setPage(page - 1); }, style: { padding: '4px 14px', borderRadius: 4, border: '1px solid var(--border)', background: page === 0 ? 'transparent' : 'var(--hover)', color: page === 0 ? 'var(--dim)' : 'var(--text)', cursor: page === 0 ? 'not-allowed' : 'pointer' } }, '← Prev'),
        React.createElement('span', { style: { flex: 1, fontSize: 11, color: 'var(--dim)' } },
          'Rows ' + (page * PAGE_SIZE + 1) + '–' + (page * PAGE_SIZE + rows.length) +
          (filterText.trim() ? ' · ' + visRows.length + ' shown' : '') +
          (colWidths ? ' · drag edges to resize · click header to sort' : '')
        ),
        React.createElement('button', { disabled: !hasMore || loading, onClick: function() { setPage(page + 1); }, style: { padding: '4px 14px', borderRadius: 4, border: '1px solid var(--border)', background: !hasMore ? 'transparent' : 'var(--hover)', color: !hasMore ? 'var(--dim)' : 'var(--text)', cursor: !hasMore ? 'not-allowed' : 'pointer' } }, 'Next →')
      )
    )
  );
}

/* ───────────────────────────────────────────────────────────────────────────
 * Time slider — emits an as_of_time ISO string (or null = "now") for
 * point-in-time / historical queries. Generalised from the Lineage Explorer
 * (LE-3) with inline styles so it carries no CSS-class dependency. Props:
 *   createTime — ISO string for the slider's left bound (default: 30 days ago)
 *   onChange(asOfTimeOrNull) — fired on release; null means "now"
 *   label — optional heading (default "Time Slider")
 * ─────────────────────────────────────────────────────────────────────────── */
function TimeSlider({ createTime, onChange, label }) {
  var nowMs   = Date.now();
  var startMs = createTime ? new Date(createTime).getTime() : (nowMs - 30 * 24 * 3600 * 1000);
  if (isNaN(startMs) || startMs >= nowMs) startMs = nowMs - 30 * 24 * 3600 * 1000;

  var _val = React.useState(nowMs), val = _val[0], setVal = _val[1];
  React.useEffect(function() { setVal(nowMs); }, [createTime]);

  function fmt(ms) {
    return new Date(ms).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });
  }
  function onCommit(ms) {
    var ms2 = parseInt(ms, 10);
    setVal(ms2);
    var isNow = ms2 >= nowMs - 60000; // within 1 min of now = "now"
    onChange(isNow ? null : new Date(ms2).toISOString());
  }

  return React.createElement('div', { style: { background: 'var(--card)', border: '1px solid var(--border)', borderRadius: 8, padding: '14px 18px', marginBottom: 18 } },
    React.createElement('div', { style: { fontSize: 11, fontWeight: 700, letterSpacing: '0.06em', textTransform: 'uppercase', color: 'var(--muted)', marginBottom: 10 } }, label || 'Time Slider'),
    React.createElement('div', { style: { display: 'flex', alignItems: 'center', gap: 10 } },
      React.createElement('input', {
        type: 'range',
        style: { flex: 1, accentColor: 'var(--accent)', cursor: 'pointer' },
        min: String(startMs), max: String(nowMs), value: String(val),
        onChange:   function(e) { setVal(parseInt(e.target.value, 10)); },
        onMouseUp:  function(e) { onCommit(e.target.value); },
        onTouchEnd: function(e) { onCommit(e.target.value); },
        onKeyUp:    function(e) { onCommit(e.target.value); },
      }),
      React.createElement('span', { style: { fontSize: 11, color: 'var(--accent)', whiteSpace: 'nowrap', minWidth: 110, textAlign: 'right' } },
        val >= nowMs - 60000 ? 'Now' : fmt(val))
    ),
    React.createElement('div', { style: { display: 'flex', justifyContent: 'space-between', fontSize: 10, color: 'var(--dim)', marginTop: 4 } },
      React.createElement('span', null, fmt(startMs)),
      React.createElement('span', null, 'Now')
    )
  );
}

/* ───────────────────────────────────────────────────────────────────────────
 * Cross-app navigation resolver (shared). Single source of truth for "which
 * Egeria Explorer panel displays element type X". Used for OUTGOING cross-links
 * from any module (Audit, Catalog, …). resolveExplorerNav walks superTypeNames
 * when there's no exact typeName match; crossAppNavigate opens the deep-link in a
 * new tab (the target views read ?guid/?kind on cold load).
 * ─────────────────────────────────────────────────────────────────────────── */
// Cross-app routing table lives in static/type-nav-map.json now (loaded by
// static/type-nav-resolve.js, which this file's HTML consumers all load
// alongside egeria-shared-ui.js — see design-docs/type-system-audit.md).
// resolveExplorerNav() is kept as a thin wrapper: it used to look up
// EGERIA_EXPLORER_NAV directly; now it delegates to the shared resolver and
// only forwards the hash/kind shape callers here expect.
function resolveExplorerNav(item) {
  if (!item) return null;
  var supers = item.superTypeNames || item.superTypes || [];
  var nav = (typeof resolveTypeNav === 'function') ? resolveTypeNav(item.typeName, supers) : null;
  if (!nav || !nav.explorerHash) return null;
  return { hash: nav.explorerHash, kind: nav.kind };
}

function _isCatalogType(item) {
  // Types displayed in the Tech Catalog (resolves ?guid via its element-nav).
  var st = item.superTypeNames || item.superTypes || [];
  var tn = item.typeName || '';
  return st.indexOf('Asset') !== -1 || tn === 'Endpoint' || tn === 'SoftwareCapability' || st.indexOf('SoftwareCapability') !== -1;
}

/* Unified element-nav: prefer an Explorer panel, else the Tech Catalog. Returns
 * { app, hash?, kind? } or null.
 * Notification/Meeting/ToDo/Review (Action Center) and ValidMetadataValue used
 * to be special-cased here in code; they're now plain entries in
 * static/type-nav-map.json (explorerHash: 'action-center' / 'valid-values')
 * and fall out of the generic resolveExplorerNav() call below — no code path
 * needed for them any more.
 * EngineAction is the one type that still needs an explicit special case: it
 * doesn't route to an Egeria Explorer hash at all (unlike every map entry),
 * it opens the egeria-operations app directly — a genuinely different target
 * app, not just a different hash — and egeria-operations has no per-guid deep
 * link yet, so there's no {hash} to carry even if it were data-driven. Must
 * be checked before the generic Asset-supertype fallback below, which would
 * otherwise route it to Tech Catalog's generic mixed "Actions" tab
 * (metadata_element_type="Action", no per-subtype detail). */
function resolveElementNav(item) {
  if (!item) return null;
  if ((item.typeName || '') === 'EngineAction') return { app: 'egeria-operations' };
  var ex = resolveExplorerNav(item);
  if (ex) return { app: 'egeria-explorer', hash: ex.hash, kind: ex.kind };
  if (_isCatalogType(item)) return { app: 'tech-catalog' };
  return null;
}

function isElementLinkable(item) { return !!resolveElementNav(item); }

/* Open the Egeria Audit tab for an element (INCOMING cross-link target). */
function auditNavigate(guid, tab) {
  if (!guid) return false;
  window.open('/egeria-audit?guid=' + encodeURIComponent(guid) + (tab ? '&tab=' + encodeURIComponent(tab) : '') + '#' + (tab || 'exceptions'), '_blank');
  return true;
}

function crossAppNavigate(item, explicitNav) {
  var nav = explicitNav || resolveElementNav(item);
  if (!nav || !item || !item.guid) return false;
  if (nav.app === 'tech-catalog') {
    window.open('/tech-catalog?guid=' + encodeURIComponent(item.guid), '_blank');
    return true;
  }
  if (nav.app === 'egeria-operations') {
    // No per-guid deep link exists yet in egeria-operations.html (it only
    // reads ?tab=/hash for tab selection) — route to the Engine Actions tab,
    // still a real improvement over falling through to Tech Catalog's
    // generic mixed Actions tab.
    window.open('/egeria-operations?tab=actions#actions', '_blank');
    return true;
  }
  var url = '/egeria-explorer?guid=' + encodeURIComponent(item.guid)
          + (nav.kind ? '&kind=' + encodeURIComponent(nav.kind) : '')
          + '#' + nav.hash;
  window.open(url, '_blank');
  return true;
}

/* ── Collapsible — a foldable titled section. ─────────────────────────────── */
// FoldTriangle — the one canonical fold/expand indicator, standardized across
// every collapsible/expandable affordance in the app: section headers
// (Collapsible, SubPane, Annotations) AND hierarchical tree drill-downs. A
// single glyph rotated via CSS transform/transition gives a real "turning"
// animation instead of an instant character swap. onClick/size/style are
// optional escape hatches for call sites that need the arrow itself
// clickable (independent of a row-level onClick) or a smaller footprint in
// deeply-nested trees; defaults match the section-header look.
function FoldTriangle({ open, onClick, size, style }) {
  return React.createElement('span', {
    onClick: onClick,
    style: Object.assign({
      display: 'inline-block', fontSize: size || 16, lineHeight: 1, flexShrink: 0,
      color: 'var(--accent)', transition: 'transform 0.15s ease',
      transform: open ? 'rotate(90deg)' : 'rotate(0deg)',
    }, style || {})
  }, '▶');
}

function Collapsible({ title, defaultOpen, count, children }) {
  var _o = React.useState(defaultOpen !== false), open = _o[0], setOpen = _o[1];
  return React.createElement('div', { style: { borderTop: '1px solid var(--border)' } },
    React.createElement('div', {
      onClick: function() { setOpen(!open); },
      style: { display: 'flex', alignItems: 'center', gap: 8, padding: '8px 4px', cursor: 'pointer', userSelect: 'none', fontSize: 11, fontWeight: 700, letterSpacing: '0.05em', textTransform: 'uppercase', color: 'var(--accent)' }
    },
      React.createElement(FoldTriangle, { open: open }),
      title,
      (count != null) && React.createElement('span', { style: { color: 'var(--dim)', fontWeight: 600 } }, '(' + count + ')')
    ),
    open && React.createElement('div', { style: { padding: '2px 4px 12px 18px' } }, children)
  );
}

// RawJsonViewer — "Copy raw JSON" debug affordance for advanced users: fetches
// the untransformed Egeria/pyegeria payload for a guid (via the generic
// /api/debug/raw/{guid} endpoint — tech_catalog_handler.py, but reachable from
// any app since all handlers share one FastAPI instance) instead of this
// app's serialized/flattened shape, and copies it straight to the clipboard —
// no inline display, just a copy action with a brief confirmation.
function RawJsonViewer({ guid, creds, depth }) {
  var _s = React.useState('idle'), state = _s[0], setState = _s[1]; // idle | loading | copied | error

  function handleClick() {
    if (state === 'loading') return;
    setState('loading');
    var url = '/api/debug/raw/' + encodeURIComponent(guid) + (depth != null ? '?depth=' + depth : '');
    egeriaFetch(url, creds).then(function(r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    }).then(function(d) {
      var payload = { fetch_method: d.fetch_method, raw: d.raw };
      return navigator.clipboard.writeText(JSON.stringify(payload, null, 2));
    }).then(function() {
      setState('copied');
      setTimeout(function() { setState('idle'); }, 1500);
    }).catch(function() {
      setState('error');
      setTimeout(function() { setState('idle'); }, 2000);
    });
  }

  var label = state === 'loading' ? 'Copying…'
    : state === 'copied' ? '✓ Copied raw JSON'
    : state === 'error' ? 'Copy failed'
    : 'Copy raw JSON (debug)';

  return React.createElement('div', {
    onClick: handleClick,
    style: { borderTop: '1px solid var(--border)', marginTop: 16, padding: '8px 4px', cursor: 'pointer',
             userSelect: 'none', fontSize: 11, fontWeight: 700, letterSpacing: '0.05em', textTransform: 'uppercase',
             color: state === 'copied' ? '#4ade80' : state === 'error' ? '#f87171' : 'var(--dim)',
             display: 'flex', alignItems: 'center', gap: 6 }
  }, '📋', label);
}

// Classifications that are internal infrastructure — never shown in the UI.
// Mirrors common_serialize.py's _SKIP_CLASSIFICATIONS.
var _SKIP_CLASSIFICATIONS = { Anchors: 1, LatestChange: 1, Memento: 1, TemplateSubstitute: 1, SpineObject: 1, SpineAttribute: 1, ObjectIdentifier: 1 };

// _classificationsFromHeader — JS port of common_serialize.py's _classifications():
// each classification is a named key directly on elementHeader (not a
// "classifications" list), with class === "ElementClassification". Converts
// to the [{typeName, properties}] shape ClassificationsAndRawJson expects, for
// call sites (e.g. ElementPropertiesPane) that only have a raw elementHeader.
function _classificationsFromHeader(hdr) {
  if (!hdr || typeof hdr !== 'object') return [];
  var result = [];
  Object.keys(hdr).forEach(function(key) {
    var val = hdr[key];
    if (!val || typeof val !== 'object') return;
    if (val.class !== 'ElementClassification') return;
    var clsName = val.classificationName || (val.type && val.type.typeName) || (key.charAt(0).toUpperCase() + key.slice(1));
    if (!clsName || _SKIP_CLASSIFICATIONS[clsName]) return;
    var flat = {};
    var rawProps = val.classificationProperties || {};
    Object.keys(rawProps).forEach(function(k) {
      if (k === 'class' || k === 'typeName') return;
      var v = rawProps[k];
      if (Array.isArray(v)) flat[k] = v.join(', ');
      else if (v !== null && typeof v !== 'object') flat[k] = String(v);
    });
    result.push({ typeName: clsName, properties: flat });
  });
  return result;
}

// ClassificationsAndRawJson — one shared insertion point for any Detail
// component: the foldable "Classifications" section (only rendered when the
// element actually carries any — closed by default, unlike Relationships,
// since classification data is usually secondary/governance-oriented rather
// than what a reader wants to see first) plus the "Copy raw JSON" debug
// affordance. Mirrors RelationshipSection's role for relationships — pass
// whatever object carries `guid` + `classifications` (the shape every
// _authored_fields(el)-based serializer now produces, common_serialize.py).
function ClassificationsAndRawJson({ item, creds }) {
  var ctxCreds = React.useContext(CredContext);
  var effectiveCreds = creds || ctxCreds;
  if (!item) return null;
  var classifs = item.classifications || [];
  return React.createElement(React.Fragment, null,
    classifs.length > 0 && React.createElement(Collapsible, { title: 'Classifications', count: classifs.length, defaultOpen: false },
      classifs.map(function(c) {
        return React.createElement('div', { key: c.typeName, style: { borderLeft: '3px solid var(--classif)', paddingLeft: 8, marginBottom: 6 } },
          React.createElement('div', { style: { fontSize: 12, fontWeight: 600, color: 'var(--classif)', marginBottom: Object.keys(c.properties || {}).length ? 4 : 0 } }, c.typeName),
          Object.entries(c.properties || {}).map(function(e) {
            return React.createElement('div', { key: e[0], style: { fontSize: 11, color: 'var(--muted)' } },
              e[0] + ': ', React.createElement('span', { style: { color: 'var(--text)' } }, String(e[1])));
          })
        );
      })
    ),
    item.guid && React.createElement(RawJsonViewer, { guid: item.guid, creds: effectiveCreds })
  );
}

/* ── ElementPropertiesPane — render any Egeria element's header + properties
 * generically (used by the Audit detail panes; reusable elsewhere). `element`
 * is a get_element_by_guid JSON dict. Shows a cross-link button when the element
 * type is displayable in the Explorer. onCrossLink(item) overrides the default
 * crossAppNavigate (e.g. to add an audit deep-link). ─────────────────────── */
function ElementPropertiesPane({ element, onCrossLink }) {
  if (!element || typeof element !== 'object') {
    return React.createElement('div', { style: { fontSize: 12, color: 'var(--dim)', padding: '6px 0' } }, 'No details available.');
  }
  var hdr  = element.elementHeader || element;
  var type = (hdr.type || {});
  var vers = (hdr.versions || {});
  var props = element.properties || {};
  var item = { guid: hdr.guid || element.guid, typeName: type.typeName, superTypeNames: type.superTypeNames || [], classifications: _classificationsFromHeader(hdr) };

  var rows = [];
  function push(k, v) { if (v != null && String(v).trim() !== '') rows.push([k, String(v)]); }
  push('GUID', item.guid);
  push('Type', item.typeName);
  push('Created by', vers.createdBy);
  push('Create time', vers.createTime);
  push('Updated by', vers.updatedBy);
  push('Update time', vers.updateTime);
  Object.keys(props).sort().forEach(function(k) {
    if (k === 'class') return;
    var v = props[k];
    if (v != null && typeof v !== 'object') push(k, v);
  });

  var th = { padding: '4px 12px 4px 0', color: 'var(--dim)', verticalAlign: 'top', whiteSpace: 'nowrap', width: 150, fontSize: 12 };
  var td = { padding: '4px 0', color: 'var(--text)', wordBreak: 'break-word', fontSize: 12 };
  var _nav = resolveElementNav(item);
  var _label = _nav && _nav.app === 'tech-catalog' ? 'Open in The Catalog ↗' : 'Open in Egeria Explorer ↗';
  return React.createElement('div', null,
    _nav && React.createElement('button', {
      onClick: function() { if (onCrossLink) onCrossLink(item); else crossAppNavigate(item); },
      style: { fontSize: 11, padding: '2px 8px', borderRadius: 4, border: '1px solid rgba(96,165,250,.4)', background: 'rgba(96,165,250,.08)', color: 'var(--accent)', cursor: 'pointer', marginBottom: 8 }
    }, _label),
    React.createElement('table', { style: { width: '100%', borderCollapse: 'collapse' } },
      React.createElement('tbody', null,
        rows.map(function(r, i) {
          return React.createElement('tr', { key: i },
            React.createElement('td', { style: th }, r[0]),
            React.createElement('td', { style: td }, r[1]));
        })
      )
    ),
    React.createElement(ClassificationsAndRawJson, { item: item })
  );
}

/* ───────────────────────────────────────────────────────────────────────────
 * AuditRelationshipTab — the shared, reusable pane behind the Egeria Audit
 * Exceptions / Certifications / Licenses tabs. Driven by config so the three
 * tabs are one component:
 *   relType    : 'Exception' | 'Certification' | 'License'
 *   columns    : [[label, row => value], …] table columns
 *   actorRoles : ['steward'] | ['certifiedBy','custodian','recipient'] | …
 *   creds      : passed to egeriaFetch
 * Table is sortable + filterable; selecting a row lazy-loads a 3-section foldable
 * detail (end1 element, relationship props + resolved actors, end2 type) using
 * the shared ElementPropertiesPane / Collapsible / crossAppNavigate. Honours a
 * point-in-time TimeSlider (asOfTime threaded into every fetch).
 * ─────────────────────────────────────────────────────────────────────────── */
function _titleCase(s) { return (s || '').replace(/([A-Z])/g, ' $1').replace(/^./, function(c){ return c.toUpperCase(); }).trim(); }

function AuditRelationshipTab({ relType, columns, actorRoles, creds, focusGuid, onClearFocus }) {
  var _rows  = React.useState([]),        rows  = _rows[0],  setRows  = _rows[1];
  var _state = React.useState('loading'), state = _state[0], setState = _state[1];
  var _emsg  = React.useState(''),        errMsg= _emsg[0],  setErrMsg= _emsg[1];
  var _asOf  = React.useState(null),      asOf  = _asOf[0],  setAsOf  = _asOf[1];
  var _filter= React.useState(''),        filter= _filter[0],setFilter= _filter[1];
  var _sort  = React.useState(null),      sort  = _sort[0],  setSort  = _sort[1]; // {col, dir}
  var _sel   = React.useState(null),      sel   = _sel[0],   setSel   = _sel[1];  // selected row
  var _attempt = React.useState(0),       attempt = _attempt[0], setAttempt = _attempt[1];
  var rz = useColumnResize(columns.length, 160);
  var tableRef = React.useRef(null);
  var _th = React.useState(null), tableH = _th[0], setTableH = _th[1];  // detail-split height (px)
  function onSplitDown(e) {
    e.preventDefault();
    var h0 = tableRef.current ? tableRef.current.offsetHeight : 300, y0 = e.clientY;
    function mv(ev){ setTableH(Math.max(80, h0 + (ev.clientY - y0))); }
    function up(){ document.removeEventListener('mousemove', mv); document.removeEventListener('mouseup', up); }
    document.addEventListener('mousemove', mv); document.addEventListener('mouseup', up);
  }

  React.useEffect(function() {
    setState('loading'); setSel(null); setErrMsg('');
    var u = '/api/audit/relationships?type=' + encodeURIComponent(relType) + (asOf ? '&as_of_time=' + encodeURIComponent(asOf) : '');
    egeriaFetch(u, creds)
      .then(function(r) {
        if (r.ok) return r.json();
        var status = r.status;
        return r.json().catch(function(){ return {}; }).then(function(e) {
          var msg = e.detail || '';
          if (status === 401) throw new Error('Your session has expired or credentials are invalid (HTTP 401). Please reconnect.' + (msg ? ' — ' + msg : ''));
          if (status === 403) throw new Error('Your Egeria account does not have permission to view ' + relType.toLowerCase() + ' relationships (HTTP 403).' + (msg ? ' — ' + msg : ''));
          throw new Error('Failed to load (HTTP ' + status + ').' + (msg ? ' ' + msg : ''));
        });
      })
      .then(function(d){ setRows(d.items || []); setState('ready'); })
      .catch(function(e){ setErrMsg(e.message || 'Failed to load.'); setState('error'); });
  }, [relType, asOf, attempt]);

  // incoming cross-link: restrict to relationships touching a focus element
  var vis = rows;
  if (focusGuid) vis = vis.filter(function(r){ return (r.end1 && r.end1.guid === focusGuid) || (r.end2 && r.end2.guid === focusGuid); });
  if (filter.trim()) {
    var q = filter.trim().toLowerCase();
    vis = vis.filter(function(row) {
      return columns.some(function(c){ var v = c[1](row); return v != null && String(v).toLowerCase().indexOf(q) !== -1; });
    });
  }
  if (sort) {
    var gi = columns[sort.col][1], dir = sort.dir;
    vis = vis.slice().sort(function(a, b) {
      var va = gi(a), vb = gi(b); va = va == null ? '' : String(va); vb = vb == null ? '' : String(vb);
      var n = (!isNaN(va) && !isNaN(vb) && va !== '' && vb !== '') ? (Number(va) - Number(vb)) : va.localeCompare(vb);
      return dir === 'asc' ? n : -n;
    });
  }
  function toggleSort(i) {
    setSort(function(p){ if (!p || p.col !== i) return { col: i, dir: 'asc' }; if (p.dir === 'asc') return { col: i, dir: 'desc' }; return null; });
  }

  var th = { textAlign: 'left', padding: '6px 12px', borderBottom: '2px solid var(--border)', color: 'var(--accent)', fontSize: 11, whiteSpace: 'nowrap', position: 'sticky', top: 0, background: 'var(--panel)', cursor: 'pointer', userSelect: 'none', overflow: 'hidden' };
  var td = { padding: '5px 12px', borderBottom: '1px solid var(--border)', fontSize: 12, verticalAlign: 'top', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' };

  var focusBanner = focusGuid && React.createElement('div', { style: { padding: '6px 12px', display: 'flex', alignItems: 'center', gap: 8, fontSize: 12, background: 'rgba(96,165,250,.1)', borderBottom: '1px solid var(--border)', color: 'var(--accent)' } },
    '\uD83D\uDD0E Showing ' + relType.toLowerCase() + 's for the selected element',
    React.createElement('button', { onClick: function(){ if (onClearFocus) onClearFocus(); }, style: { marginLeft: 'auto', fontSize: 11, padding: '2px 8px', borderRadius: 4, border: '1px solid var(--border)', background: 'transparent', color: 'var(--muted)', cursor: 'pointer' } }, 'Clear'));

  var table = React.createElement('div', { ref: tableRef, style: { overflow: 'auto', flex: sel ? (tableH ? '0 0 ' + tableH + 'px' : '0 0 42%') : 1 } },
    React.createElement('table', { style: { borderCollapse: 'collapse', tableLayout: 'fixed', width: rz.tableWidth ? rz.tableWidth + 'px' : '100%', minWidth: '100%' } },
      React.createElement('colgroup', null, columns.map(function(c, i){
        return React.createElement('col', { key: i, style: { width: ((rz.widths && rz.widths[i]) || rz.defaultW) + 'px' } });
      })),
      React.createElement('thead', null, React.createElement('tr', null,
        columns.map(function(c, i){
          var arrow = sort && sort.col === i ? (sort.dir === 'asc' ? ' ↑' : ' ↓') : ' ↕';
          return React.createElement('th', { key: i, style: th, onClick: function(){ toggleSort(i); } }, c[0] + arrow, colResizeHandle(rz.onResizeDown, i));
        })
      )),
      React.createElement('tbody', null, vis.map(function(row, ri){
        var on = sel && sel.relationshipGuid === row.relationshipGuid;
        return React.createElement('tr', { key: row.relationshipGuid || ri,
          onClick: function(){ setSel(on ? null : row); },
          style: { cursor: 'pointer', background: on ? 'rgba(96,165,250,.12)' : (ri % 2 ? 'rgba(255,255,255,0.02)' : 'transparent') } },
          columns.map(function(c, ci){ var v = c[1](row); v = (v == null || v === '') ? '' : String(v);
            return React.createElement('td', { key: ci, style: td, title: v }, v); }));
      }))
    )
  );

  return React.createElement('div', { style: { display: 'flex', flexDirection: 'column', height: '100%', overflow: 'hidden' } },
    React.createElement('div', { style: { padding: '8px 10px', display: 'flex', gap: 10, alignItems: 'flex-start' } },
      React.createElement('div', { style: { flex: '0 0 320px' } }, React.createElement(TimeSlider, { onChange: setAsOf, label: 'As of' })),
      React.createElement('input', { type: 'search', placeholder: 'Filter ' + relType.toLowerCase() + 's…', value: filter,
        onChange: function(e){ setFilter(e.target.value); },
        style: { flex: 1, alignSelf: 'center', fontSize: 12, padding: '5px 9px', borderRadius: 4, border: '1px solid var(--border)', background: 'var(--bg)', color: 'inherit', outline: 'none' } }),
      React.createElement('button', { className: 'btn-sm', style: { alignSelf: 'center' }, onClick: function(){ setAttempt(function(a){ return a + 1; }); } }, '↻ Refresh'),
      React.createElement('span', { title: 'Results are filtered by your governance-zone access rights — elements in zones you cannot access are hidden, so two users may see different counts.',
        style: { alignSelf: 'center', fontSize: 11, color: 'var(--dim)', cursor: 'help', whiteSpace: 'nowrap', border: '1px solid var(--border)', borderRadius: 12, padding: '2px 9px' } }, '🔒 filtered by your access')
    ),
    state === 'loading' ? React.createElement('div', { style: { padding: 24, color: 'var(--muted)', fontSize: 13 } }, 'Loading ' + relType + ' relationships…')
    : state === 'error' ? React.createElement('div', { style: { padding: 24, color: '#f87171', fontSize: 13, lineHeight: 1.6 } }, errMsg || 'Failed to load.')
    : rows.length === 0 ? React.createElement('div', { style: { padding: 24, color: 'var(--muted)', fontSize: 13, lineHeight: 1.6 } },
        React.createElement('div', null, 'No ' + relType.toLowerCase() + 's are visible to you' + (asOf ? ' as of the selected time.' : '.')),
        React.createElement('div', { style: { fontSize: 12, color: 'var(--dim)', marginTop: 6 } }, '🔒 Results are filtered by your governance-zone access rights — there may be ' + relType.toLowerCase() + 's in zones your user cannot access.'))
    : React.createElement(React.Fragment, null,
        focusBanner,
        table,
        sel && React.createElement('div', { onMouseDown: onSplitDown, title: 'Drag to resize', style: { height: 6, flexShrink: 0, cursor: 'row-resize', background: 'var(--border)', borderTop: '1px solid var(--panel)', borderBottom: '1px solid var(--panel)' } }),
        sel && React.createElement('div', { style: { flex: 1, overflow: 'auto', padding: '6px 14px' } },
          React.createElement(AuditDetailPanel, { row: sel, relType: relType, actorRoles: actorRoles, creds: creds, asOf: asOf }))
      )
  );
}

/* The 3-section foldable detail for a selected audit relationship. */
function AuditDetailPanel({ row, relType, actorRoles, creds, asOf }) {
  var _e1 = React.useState({ st: 'idle', el: null }), e1 = _e1[0], setE1 = _e1[1];
  var _e2 = React.useState({ st: 'idle', el: null }), e2 = _e2[0], setE2 = _e2[1];
  var _ac = React.useState({}),                       actors = _ac[0], setActors = _ac[1]; // role -> {st, el}
  var q = asOf ? '&as_of_time=' + encodeURIComponent(asOf) : '';

  React.useEffect(function() {
    setE1({ st: 'loading', el: null }); setE2({ st: 'loading', el: null }); setActors({});
    function _authMsg(status) {
      if (status === 401) return 'Session expired or credentials invalid (HTTP 401).';
      if (status === 403) return 'Not authorized to view this element (HTTP 403).';
      return 'Could not load (HTTP ' + status + ').';
    }
    function load(guid, set) {
      if (!guid) { set({ st: 'none', el: null }); return; }
      egeriaFetch('/api/audit/element/' + encodeURIComponent(guid) + '?_=1' + q, creds)
        .then(function(r) {
          if (r.ok) return r.json().then(function(d){ set({ st: 'ready', el: d }); });
          set({ st: 'error', el: null, msg: _authMsg(r.status) });
        })
        .catch(function(){ set({ st: 'error', el: null, msg: 'Could not load.' }); });
    }
    load(row.end1 && row.end1.guid, setE1);
    load(row.end2 && row.end2.guid, setE2);
    (actorRoles || []).forEach(function(role) {
      var val = row.props[role]; if (!val) return;
      var pname = row.props[role + 'PropertyName']; var tname = row.props[role + 'TypeName'];
      setActors(function(p){ return Object.assign({}, p, { [role]: { st: 'loading', el: null } }); });
      var u = '/api/audit/actor?value=' + encodeURIComponent(val)
            + (pname ? '&property_name=' + encodeURIComponent(pname) : '')
            + (tname ? '&type_name=' + encodeURIComponent(tname) : '') + q;
      egeriaFetch(u, creds)
        .then(function(r) {
          if (r.ok) return r.json().then(function(d){ setActors(function(p){ return Object.assign({}, p, { [role]: { st: 'ready', el: d } }); }); });
          setActors(function(p){ return Object.assign({}, p, { [role]: { st: 'error', el: null, msg: _authMsg(r.status) } }); });
        })
        .catch(function(){ setActors(function(p){ return Object.assign({}, p, { [role]: { st: 'error', el: null, msg: 'Could not load.' } }); }); });
    });
  }, [row.relationshipGuid, asOf]);

  function paneFor(s) {
    if (!s || s.st === 'loading') return React.createElement('div', { style: { fontSize: 12, color: 'var(--dim)' } }, 'Loading…');
    if (s.st === 'error') return React.createElement('div', { style: { fontSize: 12, color: '#f87171' } }, s.msg || 'Could not load.');
    if (s.st === 'none') return React.createElement('div', { style: { fontSize: 12, color: 'var(--dim)' } }, 'Not specified.');
    return React.createElement(ElementPropertiesPane, { element: s.el });
  }

  var propRows = Object.keys(row.props || {}).filter(function(k){ return typeof row.props[k] !== 'object'; }).sort();
  var pth = { padding: '3px 12px 3px 0', color: 'var(--dim)', verticalAlign: 'top', whiteSpace: 'nowrap', width: 160, fontSize: 12 };
  var ptd = { padding: '3px 0', color: 'var(--text)', wordBreak: 'break-word', fontSize: 12 };

  return React.createElement('div', null,
    React.createElement(Collapsible, { title: (row.end1.typeName || 'Affected element'), defaultOpen: true }, paneFor(e1)),
    React.createElement(Collapsible, { title: relType + ' properties & actors', defaultOpen: true },
      React.createElement('table', { style: { width: '100%', borderCollapse: 'collapse', marginBottom: 8 } },
        React.createElement('tbody', null, propRows.map(function(k){
          return React.createElement('tr', { key: k },
            React.createElement('td', { style: pth }, _titleCase(k)),
            React.createElement('td', { style: ptd }, String(row.props[k])));
        }))
      ),
      (actorRoles || []).map(function(role){
        var st = actors[role]; if (!row.props[role]) return null;
        return React.createElement('div', { key: role, style: { marginTop: 6 } },
          React.createElement('div', { style: { fontSize: 11, fontWeight: 700, color: 'var(--muted)', marginBottom: 2 } }, _titleCase(role)),
          paneFor(st));
      })
    ),
    React.createElement(Collapsible, { title: (row.end2.typeName || relType + ' type'), defaultOpen: false }, paneFor(e2))
  );
}

/* ── useColumnResize — shared drag-to-resize for table columns. Returns
 * { widths, onResizeDown(e, i), tableWidth }. Pair with table-layout:fixed + a
 * <colgroup>, and put a colResizeHandle in each <th>. ─────────────────────── */
function useColumnResize(count, defaultW) {
  defaultW = defaultW || 150;
  var _w = React.useState(null), widths = _w[0], setWidths = _w[1];
  var dragRef = React.useRef(null);
  React.useEffect(function() {
    var a = []; for (var i = 0; i < count; i++) a.push(defaultW); setWidths(a);
  }, [count]);
  function onResizeDown(e, idx) {
    e.preventDefault(); e.stopPropagation();
    var startW = (widths && widths[idx]) || defaultW;
    dragRef.current = { idx: idx, startX: e.clientX, startW: startW };
    function mv(ev) {
      if (!dragRef.current) return;
      var dx = ev.clientX - dragRef.current.startX;
      var nw = Math.max(40, dragRef.current.startW + dx);
      setWidths(function(prev){ var n = (prev || []).slice(); n[dragRef.current.idx] = nw; return n; });
    }
    function up() { dragRef.current = null; document.removeEventListener('mousemove', mv); document.removeEventListener('mouseup', up); }
    document.addEventListener('mousemove', mv); document.addEventListener('mouseup', up);
  }
  var tableWidth = widths ? widths.reduce(function(s, w){ return s + w; }, 0) : null;
  return { widths: widths, onResizeDown: onResizeDown, tableWidth: tableWidth, defaultW: defaultW };
}

function colResizeHandle(onResizeDown, idx) {
  // width: 6 is the visible dotted border; the handle's actual mousedown hit
  // target is 12px (right: -3 either side of that line) — 6px was too easy to
  // miss and land on the neighbouring header's text-select/sort-click instead.
  // At 0.45 opacity the line itself was reported as effectively invisible at
  // rest (confirmed present in the DOM with correct geometry, just too faint
  // to notice) — bumped the resting opacity and added a mouseenter/mouseleave
  // brighten. This is a plain function (not a component — called per-column
  // inside a .map() loop, so it can't safely use hooks), hence the imperative
  // style mutation instead of React state for the hover effect.
  return React.createElement('div', {
    onMouseDown: function(e){ onResizeDown(e, idx); },
    onClick: function(e){ e.stopPropagation(); },
    onMouseEnter: function(e){ var line = e.currentTarget.firstChild; if (line) line.style.borderRightColor = 'rgba(96,165,250,0.9)'; },
    onMouseLeave: function(e){ var line = e.currentTarget.firstChild; if (line) line.style.borderRightColor = 'rgba(96,165,250,0.6)'; },
    style: { position: 'absolute', right: -3, top: 0, bottom: 0, width: 12, cursor: 'col-resize', zIndex: 2 }
  },
    React.createElement('div', { style: { position: 'absolute', right: 3, top: 0, bottom: 0, width: 6, borderRight: '2px dotted rgba(96,165,250,0.6)' } })
  );
}

/* ── makeResizableCols — hook-free column resize for plain render-helper
 * functions (e.g. TechTable) that get called directly inside another
 * component's render, often inside a .map() loop — a variable number of
 * calls per render, so they can't safely use useColumnResize's hooks
 * (React requires a fixed hook-call count/order per component). This writes
 * directly to each <col> element's DOM style on drag instead of going
 * through React state, so no hooks are needed at all — safe to call from
 * anywhere, any number of times, per render.
 *
 * Usage: var rz = makeResizableCols(headers.length, initialWidths);
 *   <table style="table-layout:fixed"> + resizableColgroup(rz.refs) +
 *   <th>{h}{colResizeHandle(rz.onResizeDown, i)}</th> (th needs position:relative). ── */
function makeResizableCols(count, initialWidths) {
  var refs = [];
  for (var i = 0; i < count; i++) refs.push(React.createRef());
  function onResizeDown(e, idx) {
    e.preventDefault(); e.stopPropagation();
    var colEl = refs[idx].current;
    var startX = e.clientX;
    var startW = colEl ? colEl.getBoundingClientRect().width : 120;
    function mv(ev) {
      var dx = ev.clientX - startX;
      var nw = Math.max(40, startW + dx);
      if (refs[idx].current) refs[idx].current.style.width = nw + 'px';
    }
    function up() { document.removeEventListener('mousemove', mv); document.removeEventListener('mouseup', up); }
    document.addEventListener('mousemove', mv); document.addEventListener('mouseup', up);
  }
  return { refs: refs, onResizeDown: onResizeDown, initialWidths: initialWidths || [] };
}

function resizableColgroup(rz) {
  return React.createElement('colgroup', null, rz.refs.map(function(ref, i) {
    var w = rz.initialWidths[i];
    return React.createElement('col', { key: i, ref: ref, style: w ? { width: w } : undefined });
  }));
}

/* ── GenericPropertiesTable — shared by Egeria Explorer + Tech Catalog ───────
 * Renders every scalar property of `item` as a label:value row, instead of
 * each Detail component hand-picking a fixed field list. This is what makes
 * a property like `authors` (AuthoredReferenceable) show up automatically,
 * everywhere, without a per-type frontend change — the backend just needs to
 * include it in the item it hands to this component (see common_serialize.py
 * ::_authored_fields, which every *_handler.py serializer now merges in).
 *
 * Props:
 *   item     — the object whose scalar keys become rows
 *   priority — key names to show first, in this order (e.g. ['description'])
 *   skip     — additional key names to exclude beyond _GENERIC_PROPS_SKIP
 *              (header/relationship/classification keys already shown
 *              elsewhere are skipped by default)
 *   extra    — [[label, value], ...] rows appended after the generic ones,
 *              for computed/derived values that aren't plain item keys
 */
var _GENERIC_PROPS_SKIP = new Set([
  'class', 'guid', 'typeName', 'superTypeNames', 'displayName', 'name',
  'classifications', 'relationships', 'hasSchema', 'hasLineage', 'hasAnnotations',
  'createTime', 'updateTime', 'createdBy', 'updatedBy', 'maintainedBy', 'version',
  'description', '_header',
]);
var _GENERIC_PROPS_LABELS = {
  qualifiedName: 'Qualified Name', authors: 'Authors', contentStatus: 'Content Status',
  userDefinedContentStatus: 'User-Defined Content Status', description: 'Description',
  guid: 'GUID',
};
function _titleCaseKey(key) {
  var s = String(key).replace(/([a-z0-9])([A-Z])/g, '$1 $2').replace(/_/g, ' ');
  return s.charAt(0).toUpperCase() + s.slice(1);
}
// A value is "scalar enough" for the generic table if it's a plain string/number/
// boolean, or an array of such (e.g. authors: ['alice','bob']). Plain objects and
// arrays-of-objects are curated relationship/nested-element data already rendered
// by a dedicated section elsewhere (e.g. blueprint.components, project.relationships)
// — showing them here would just stringify to "[object Object]".
function _isScalarForPropsTable(v) {
  if (Array.isArray(v)) return v.every(function(x) { return x === null || typeof x !== 'object'; });
  return typeof v !== 'object';
}
function _genericPropsRows(item, priority, skip) {
  if (!item) return [];
  var skipSet = new Set(_GENERIC_PROPS_SKIP);
  (skip || []).forEach(function(k) { skipSet.add(k); });
  var isEmpty = function(v) { return v === undefined || v === null || (typeof v === 'string' && !v.trim()) || (Array.isArray(v) && v.length === 0); };
  var rows = [], seen = new Set();
  (priority || []).forEach(function(k) {
    if (skipSet.has(k) || seen.has(k) || isEmpty(item[k])) return;
    rows.push([k, item[k]]); seen.add(k);
  });
  Object.keys(item).sort().forEach(function(k) {
    if (skipSet.has(k) || seen.has(k) || _isMermaidKey(k)) return;
    var v = item[k];
    if (isEmpty(v) || !_isScalarForPropsTable(v)) return;
    rows.push([k, v]); seen.add(k);
  });
  return rows;
}
function GenericPropertiesTable({ item, priority, skip, extra, renderValue }) {
  var rows = _genericPropsRows(item, priority, skip);
  (extra || []).forEach(function(r) {
    var v = r[1];
    if (v !== undefined && v !== null && String(v).trim() !== '') rows.push(r);
  });
  if (rows.length === 0) return null;
  var mono = new Set(['qualifiedName', 'guid']);
  var rz = makeResizableCols(2, ['160px', 'auto']);
  return React.createElement('table', { style: { width: '100%', borderCollapse: 'collapse', fontSize: 12, tableLayout: 'fixed' } },
    resizableColgroup(rz),
    React.createElement('tbody', null,
      rows.map(function(r, ri) {
        var key = r[0], val = r[1];
        var label = _GENERIC_PROPS_LABELS[key] || _titleCaseKey(key);
        var isMono = mono.has(key);
        // renderValue lets a caller customize specific rows (e.g. markdown for a
        // long-text field) without every consumer of this shared table needing
        // the same special-casing baked in.
        var raw = Array.isArray(val) ? val.join(', ') : String(val);
        var display = isMono || !renderValue ? raw : renderValue(key, raw);
        return React.createElement('tr', { key: key, style: { borderTop: '1px solid var(--border)' } },
          React.createElement('td', { style: { padding: '5px 12px 5px 0', color: 'var(--dim)', verticalAlign: 'top', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', position: ri === 0 ? 'relative' : 'static' } },
            label, ri === 0 && colResizeHandle(rz.onResizeDown, 0)),
          React.createElement('td', { style: { padding: '5px 0', color: 'var(--text)', wordBreak: 'break-all', fontFamily: isMono ? 'ui-monospace,monospace' : 'inherit', fontSize: isMono ? 11 : 12 } }, display)
        );
      })
    )
  );
}

/* ── HeaderInfoButton — pops up elementHeader metadata (guid, type, status,
 * version, created/updated by+time) common to every element, regardless of
 * type. Mirrors the "Show Context Diagram" toggle-button convention used for
 * mermaid graphs. Drop into any Detail component's header-button row next to
 * CopyJsonButton. `header` is the normalized subset a backend serializer
 * produces via common_serialize.py::_header_summary (or an equivalent
 * frontend-side pick of guid/typeName/status/version/createdBy/etc off the
 * item, for handlers not yet updated to send a dedicated `_header` field). ── */

// Renders a Referenceable's plain additionalProperties Map<String,String>
// (e.g. a ValidMetadataValue's "explanation" note) as its own resizable
// sub-table, instead of it getting flattened into a generic properties
// table's giant "k: v; k2: v2" cell. Ported from quickstart (2026-08-16,
// SHARE-3 drift audit) -- digital_products_handler.py's _serialize_node
// deliberately skips additionalProperties in its flat prop-string builder
// for the same reason (see that file's _extract_props comment) and surfaces
// it as this structured dict instead.
function AdditionalPropertiesTable({ data }) {
  var entries = Object.entries(data || {}).filter(function(e) { return e[1] !== undefined && e[1] !== null && String(e[1]).trim() !== ''; });
  if (entries.length === 0) return null;
  var rz = makeResizableCols(2, ['180px', 'auto']);
  return React.createElement('div', { style: { marginTop: 12 } },
    React.createElement('div', { style: { fontSize: 11, fontWeight: 700, letterSpacing: '0.05em', textTransform: 'uppercase', color: 'var(--dim)', marginBottom: 6 } },
      'Additional Properties (' + entries.length + ')'),
    React.createElement('table', { style: { width: '100%', borderCollapse: 'collapse', fontSize: 12, tableLayout: 'fixed', border: '1px solid var(--border)', borderRadius: 4 } },
      resizableColgroup(rz),
      React.createElement('tbody', null,
        entries.map(function(e, ri) {
          return React.createElement('tr', { key: e[0], style: { borderTop: ri === 0 ? 'none' : '1px solid var(--border)' } },
            React.createElement('td', { style: { padding: '5px 12px', color: 'var(--dim)', verticalAlign: 'top', wordBreak: 'break-word', background: 'var(--panel)', position: ri === 0 ? 'relative' : 'static' } },
              e[0], ri === 0 && colResizeHandle(rz.onResizeDown, 0)),
            React.createElement('td', { style: { padding: '5px 12px', color: 'var(--text)', wordBreak: 'break-word' } }, String(e[1]))
          );
        })
      )
    )
  );
}

function _fmtHeaderDate(iso) {
  if (!iso) return '';
  try { return new Date(iso).toLocaleString(undefined, { dateStyle: 'medium', timeStyle: 'short' }); } catch (e) { return iso; }
}
function HeaderInfoButton({ header }) {
  var _open = React.useState(false), open = _open[0], setOpen = _open[1];
  if (!header) return null;
  var rows = [
    ['GUID', header.guid],
    ['Type', header.typeName],
    ['Status', header.status],
    ['Version', header.version],
    ['Created By', header.createdBy],
    ['Create Time', _fmtHeaderDate(header.createTime)],
    ['Updated By', header.updatedBy],
    ['Update Time', _fmtHeaderDate(header.updateTime)],
    ['Maintained By', Array.isArray(header.maintainedBy) ? header.maintainedBy.join(', ') : header.maintainedBy],
  ].filter(function(r) { return r[1] !== undefined && r[1] !== null && String(r[1]).trim() !== ''; });
  if (rows.length === 0) return null;
  return React.createElement('div', { style: { position: 'relative', display: 'inline-block' } },
    React.createElement('button', {
      onClick: function(e) { e.stopPropagation(); setOpen(function(o) { return !o; }); },
      title: 'Show element header (guid, status, version, created/updated metadata)',
      style: { fontSize: 11, padding: '3px 9px', borderRadius: 4, border: '1px solid var(--border)',
               background: open ? 'rgba(96,165,250,.1)' : 'transparent', color: open ? 'var(--accent)' : 'var(--dim)',
               cursor: 'pointer', whiteSpace: 'nowrap' }
    }, 'ℹ Header'),
    open && React.createElement(React.Fragment, null,
      React.createElement('div', { onClick: function() { setOpen(false); }, style: { position: 'fixed', inset: 0, zIndex: 19 } }),
      React.createElement('div', {
        onClick: function(e) { e.stopPropagation(); },
        style: { position: 'absolute', top: '100%', right: 0, marginTop: 4, zIndex: 20, background: 'var(--card)',
                 border: '1px solid var(--border)', borderRadius: 6, padding: '10px 12px', minWidth: 260,
                 boxShadow: '0 4px 16px rgba(0,0,0,.35)' }
      },
        rows.map(function(r) {
          return React.createElement('div', { key: r[0], style: { display: 'flex', gap: 8, fontSize: 11, padding: '2px 0' } },
            React.createElement('span', { style: { color: 'var(--dim)', minWidth: 100, flexShrink: 0 } }, r[0]),
            React.createElement('span', { style: { color: 'var(--text)', wordBreak: 'break-all' } }, String(r[1]))
          );
        })
      )
    )
  );
}

/* ── Shared sort / filter / pill utilities ───────────────────────────────── */
function applySort(rows, sort, keys) {
  var key = sort.col != null ? keys[sort.col] : null;
  if (!key) return rows;
  return rows.slice().sort(function(a, b) {
    var av = (a[key] == null ? '' : String(a[key])).toLowerCase();
    var bv = (b[key] == null ? '' : String(b[key])).toLowerCase();
    var r = av < bv ? -1 : av > bv ? 1 : 0;
    return sort.dir === 'asc' ? r : -r;
  });
}

function thSortable(sort, setSort, i, h, rzDown, thStyle) {
  var el = React.createElement;
  var isSorted = sort.col === i;
  var indicator = isSorted
    ? el('span', { style:{ fontSize:9, opacity:0.8 } }, sort.dir === 'asc' ? ' ↑' : ' ↓')
    : el('span', { style:{ fontSize:9, opacity:0.2 } }, ' ⇅');
  return el('th', { key:i, style: Object.assign({}, thStyle, { cursor:'pointer', userSelect:'none' }),
    onClick: function(){ setSort(function(s){ return { col:i, dir: s.col===i ? (s.dir==='asc'?'desc':'asc') : 'asc' }; }); } },
    h, indicator, rzDown ? colResizeHandle(rzDown, i) : null);
}

/* simplePillRow: filter pills without colour-coded status maps.
   values    : array of string keys
   labelFn   : key → display string
   fSet      : current Set<string>
   setFSet   : state setter */
// ── CopyJsonButton ────────────────────────────────────────────────────────────
// Small utility button for advanced users: copies the raw JSON payload for any
// property view to the clipboard. Pass the object/array directly as `data`.
function CopyJsonButton({ data, title }) {
  var _s = React.useState('idle'), state = _s[0], setState = _s[1];
  function handleClick(e) {
    e.stopPropagation();
    var text;
    try { text = JSON.stringify(data, null, 2); } catch(_) { setState('fail'); return; }
    copyToClipboard(text).then(function(ok) {
      setState(ok ? 'ok' : 'fail');
      setTimeout(function() { setState('idle'); }, 2000);
    });
  }
  var label = state === 'ok' ? '✓ Copied' : state === 'fail' ? '✕ Failed' : (title || '{ } Copy JSON');
  var color = state === 'ok' ? '#4ade80' : state === 'fail' ? '#f87171' : 'var(--dim)';
  return React.createElement('button', {
    onClick: handleClick,
    title: 'Copy raw JSON payload to clipboard',
    style: {
      fontSize: 11, padding: '3px 9px', borderRadius: 4,
      border: '1px solid var(--border)', background: 'transparent',
      color: color, cursor: 'pointer', whiteSpace: 'nowrap',
      fontFamily: 'ui-monospace,monospace', transition: 'color 0.15s'
    }
  }, label);
}

/*
 * FavoriteButton — toggles a section/element as a portal favorite for the
 * active persona. Backed by /api/favorites (demo mode only — returns null
 * outside demo mode or before a persona is selected).
 *
 * Props: app, section, label, icon, url, personaId, demoMode
 */
function FavoriteButton({ app, section, label, icon, url, personaId, demoMode }) {
  var _stateH = React.useState('loading'), state = _stateH[0], setState = _stateH[1]; // loading | on | off
  var _idH    = React.useState(null),      favId = _idH[0],    setFavId = _idH[1];

  React.useEffect(function() {
    if (!personaId || !section) { setState('off'); return; }
    setState('loading');
    fetch('/api/favorites?persona=' + encodeURIComponent(personaId))
      .then(function(r) { return r.ok ? r.json() : []; })
      .then(function(favs) {
        var match = (favs || []).find(function(f) { return f.url === url; });
        if (match) { setFavId(match.id); setState('on'); }
        else { setFavId(null); setState('off'); }
      })
      .catch(function() { setState('off'); });
  }, [app, section, url, personaId]);

  function toggle(e) {
    e.stopPropagation();
    if (!personaId || state === 'loading') return;
    setState('loading');
    if (favId) {
      fetch('/api/favorites/' + encodeURIComponent(favId) + '?persona=' + encodeURIComponent(personaId), { method: 'DELETE' })
        .then(function(r) { if (r.ok) { setFavId(null); setState('off'); } else { setState('on'); } })
        .catch(function() { setState('on'); });
    } else {
      fetch('/api/favorites?persona=' + encodeURIComponent(personaId), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ app: app, section: section, label: label, icon: icon, url: url }),
      })
        .then(function(r) { return r.ok ? r.json() : Promise.reject(r.status); })
        .then(function(res) { setFavId(res.id); setState('on'); })
        .catch(function() { setState('off'); });
    }
  }

  if (!personaId) return null;

  return React.createElement('button', {
    onClick: toggle,
    disabled: state === 'loading',
    title: state === 'on' ? 'Remove from My Bookmarks' : 'Add to My Bookmarks',
    style: {
      background: 'none', border: 'none', cursor: state === 'loading' ? 'default' : 'pointer',
      fontSize: 16, lineHeight: 1, padding: '2px 6px',
      color: state === 'on' ? '#34d399' : 'var(--muted)',
      opacity: state === 'loading' ? 0.5 : 1,
    },
  }, state === 'on' ? '☑' : '☐');
}

function simplePillRow(values, labelFn, fSet, setFSet) {
  var el = React.createElement;
  return el('div', { style:{ display:'flex', gap:3, flexWrap:'wrap', alignItems:'center' } },
    values.map(function(v){
      var on = fSet.has(v);
      return el('button', { key:v, onClick:function(){ setFSet(function(prev){ var n=new Set(prev); if(n.has(v)) n.delete(v); else n.add(v); return n; }); },
        style:{ fontSize:10, padding:'2px 8px', borderRadius:10, cursor:'pointer', fontWeight: on ? 700 : 400,
                border: on ? '1.5px solid var(--accent)' : '1px solid var(--border)',
                background: on ? 'rgba(96,165,250,.15)' : 'transparent', color: on ? 'var(--accent)' : 'var(--muted)' } }, labelFn(v)); }),
    fSet.size > 0 && el('button', { onClick:function(){ setFSet(new Set()); },
      style:{ fontSize:10, padding:'2px 8px', borderRadius:4, border:'1px solid var(--border)', background:'transparent', color:'var(--dim)', cursor:'pointer' } }, 'clear'));
}
