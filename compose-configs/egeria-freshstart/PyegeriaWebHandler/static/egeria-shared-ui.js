/* SPDX-License-Identifier: Apache-2.0
 * Copyright Contributors to the ODPi Egeria project.
 *
 * egeria-shared-ui.js — shared presentational components used by both SPAs
 * (Egeria Explorer + Tech Catalog). Loaded via <script> AFTER React/ReactDOM and
 * BEFORE each SPA's app script, so these are plain globals referenced by name.
 * Scope: robust clipboard + the mermaid diagram family + useResizable.
 * Depends on host globals: React, window.mermaid; CSS: .mermaid-wrap;
 * CSS vars: --accent --border --panel --muted --dim. No fetch / CredContext.
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

/* ── Glossary tree (shared by Egeria Explorer + Tech Catalog) ────────────────
 * One twistie-tree implementation for both SPAs. GlossaryTreeNode lazy-loads
 * its child folders + terms via the injected fetchJson(path) -> Promise<json>,
 * so each SPA supplies its own auth wrapper (Explorer: fetch+credAppend;
 * Catalog: fetchWithToken). onSelect(obj, isFolder) fires on row click.
 * Depends on host CSS classes .tree-item / .badge / .type-name and CSS vars
 * --accent --muted --dim. */
function GlossaryTermRow({ term, depth, selected, onSelect }) {
  return React.createElement("div", {
    className: "tree-item" + (selected === term.guid ? " sel" : ""),
    style: { paddingLeft: 8 + depth * 16 },
    onClick: function() { onSelect(term, false); }, title: term.qualifiedName || term.guid,
  },
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
function GlossaryTreeNode({ folder, depth, selected, onSelect, showTemplates, fetchJson }) {
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
      React.createElement("span", { onClick: function(e) { e.stopPropagation(); toggle(); }, style: { width: 14, textAlign: 'center', flexShrink: 0, color: expanded ? 'var(--accent)' : 'var(--muted)', fontSize: 10, fontWeight: 700 } }, expanded ? '▼' : '▶'),
      React.createElement("span", { style: { fontSize: 12, flexShrink: 0 }, onClick: function(e) { e.stopPropagation(); toggle(); } }, "📁"),
      React.createElement("span", { className: "type-name", style: { flex: 1 }, onClick: function() { onSelect(folder, true); } }, folder.displayName || folder.qualifiedName || folder.guid)
    ),
    expanded && loading && React.createElement("div", { style: { paddingLeft: pad + 20, fontSize: 11, color: 'var(--dim)', padding: '2px 0' } }, "Loading…"),
    expanded && children && React.createElement(React.Fragment, null,
      children.folders.map(function(cf) { return React.createElement(GlossaryTreeNode, { key: cf.guid, folder: cf, depth: depth + 1, selected: selected, onSelect: onSelect, showTemplates: showTemplates, fetchJson: fetchJson }); }),
      subTerms.map(function(t) { return React.createElement(GlossaryTermRow, { key: t.guid, term: t, depth: depth + 1, selected: selected, onSelect: onSelect }); })
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
