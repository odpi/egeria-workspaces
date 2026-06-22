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

/* ── Glossary tree (shared by Egeria Explorer + Tech Catalog) ────────────────
 * One twistie-tree implementation for both SPAs. GlossaryTreeNode lazy-loads
 * its child folders + terms via the injected fetchJson(path) -> Promise<json>,
 * via the injected fetchJson(path) wrapper (both SPAs now use the shared
 * token-aware egeriaFetch). onSelect(obj, isFolder) fires on row click.
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
    onClick: function() { setOpen(true); setSubmitted(false); },
    title: 'Share your feedback',
    style: { position: 'fixed', bottom: 20, right: 20, zIndex: 900, background: 'var(--accent)', color: '#fff',
             border: 'none', borderRadius: 20, padding: '7px 15px', fontSize: 12, fontWeight: 600,
             cursor: 'pointer', boxShadow: '0 2px 8px rgba(0,0,0,0.3)', letterSpacing: '0.02em' }
  }, '💬 Feedback');

  if (!open) return floatingBtn;

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
               display: 'flex', alignItems: 'flex-end', justifyContent: 'flex-end', padding: 24 }
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
  var fields = [['Qualified Name', folder.qualifiedName],['GUID', folder.guid],['Type', folder.typeName],['Status', folder.status],['Description', folder.description]].filter(function(r){return r[1]&&String(r[1]).trim();});
  var sHdr = { fontSize: 11, fontWeight: 700, letterSpacing: '0.07em', textTransform: 'uppercase', color: 'var(--accent)', marginBottom: 8, marginTop: 20 };
  var cardStyle = { background: 'var(--card)', border: '1px solid var(--border)', borderRadius: 6, padding: '10px 14px', marginBottom: 8 };
  return React.createElement('div', { style: { padding: '20px 24px', overflowY: 'auto', height: '100%' } },
    React.createElement('div', { style: { display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4 } },
      React.createElement('div', { style: { fontSize: 18, fontWeight: 700, color: 'var(--text)' } }, folder.displayName || folder.qualifiedName),
      React.createElement('span', { style: _glsBadge }, 'Folder')
    ),
    folder.description && React.createElement('p', { style: { fontSize: 13, lineHeight: 1.6, marginBottom: 16, color: 'var(--muted)' } }, folder.description),
    fields.length > 0 && React.createElement('div', null,
      React.createElement('div', { style: sHdr }, 'Properties'),
      React.createElement('table', { style: { width: '100%', borderCollapse: 'collapse', fontSize: 12 } },
        React.createElement('tbody', null,
          fields.map(function(r) {
            var mono = r[0] === 'Qualified Name' || r[0] === 'GUID';
            return React.createElement('tr', { key: r[0], style: { borderTop: '1px solid var(--border)' } },
              React.createElement('td', { style: { padding: '5px 12px 5px 0', color: 'var(--dim)', width: 140, verticalAlign: 'top', whiteSpace: 'nowrap' } }, r[0]),
              React.createElement('td', { style: { padding: '5px 0', color: 'var(--text)', wordBreak: 'break-all', fontFamily: mono ? 'ui-monospace,monospace' : 'inherit', fontSize: mono ? 11 : 12 } }, String(r[1])));
          })
        )
      )
    ),
    (folder.classifications || []).length > 0 && React.createElement('div', null,
      React.createElement('div', { style: sHdr }, 'Classifications'),
      folder.classifications.map(function(c) {
        return React.createElement('div', { key: c.typeName, style: Object.assign({}, cardStyle, { borderLeft: '3px solid var(--classif)' }) },
          React.createElement('div', { style: { fontSize: 12, fontWeight: 600, color: 'var(--classif)', marginBottom: Object.keys(c.properties || {}).length ? 4 : 0 } }, c.typeName),
          Object.entries(c.properties || {}).map(function(e) {
            return React.createElement('div', { key: e[0], style: { fontSize: 11, color: 'var(--muted)' } },
              e[0] + ': ', React.createElement('span', { style: { color: 'var(--text)' } }, String(e[1])));
          })
        );
      })
    ),
    // A CollectionFolder is a Collection — surface its context/anchored graphs.
    React.createElement(MermaidSection, { guid: folder.guid })
  );
}

function GlossaryDetail({ glossary }) {
  if (!glossary) return null;
  var sHdr   = { fontSize: 11, fontWeight: 700, letterSpacing: '0.07em', textTransform: 'uppercase', color: 'var(--accent)', marginBottom: 8, marginTop: 20 };
  var cardStyle = { background: 'var(--card)', border: '1px solid var(--border)', borderRadius: 6, padding: '10px 14px', marginBottom: 8 };
  var fields = [['Qualified Name', glossary.qualifiedName],['GUID', glossary.guid],['Language', glossary.language],['Usage', glossary.usage],['Status', glossary.status]].filter(function(r){return r[1];});
  return React.createElement('div', { style: { padding: '20px 24px', overflowY: 'auto', height: '100%' } },
    React.createElement('div', { style: { display: 'flex', alignItems: 'center', gap: 10, marginBottom: 8 } },
      React.createElement('h2', { style: { fontSize: 18, fontWeight: 700, margin: 0, color: 'var(--text)', flex: 1 } }, glossary.displayName || glossary.qualifiedName || glossary.guid),
      React.createElement('span', { style: _glsBadge }, 'Glossary')
    ),
    glossary.description && React.createElement('p', { style: { fontSize: 13, color: 'var(--muted)', lineHeight: 1.6, margin: '0 0 16px' } }, glossary.description),
    fields.length > 0 && React.createElement('div', null,
      React.createElement('div', { style: sHdr }, 'Properties'),
      React.createElement('table', { style: { width: '100%', borderCollapse: 'collapse', fontSize: 12 } },
        React.createElement('tbody', null,
          fields.map(function(r) {
            var mono = r[0] === 'Qualified Name' || r[0] === 'GUID';
            return React.createElement('tr', { key: r[0], style: { borderTop: '1px solid var(--border)' } },
              React.createElement('td', { style: { padding: '5px 12px 5px 0', color: 'var(--dim)', width: 140, verticalAlign: 'top', whiteSpace: 'nowrap' } }, r[0]),
              React.createElement('td', { style: { padding: '5px 0', color: 'var(--text)', wordBreak: 'break-all', fontFamily: mono ? 'ui-monospace,monospace' : 'inherit', fontSize: mono ? 11 : 12 } }, String(r[1])));
          })
        )
      )
    ),
    (glossary.classifications || []).length > 0 && React.createElement('div', null,
      React.createElement('div', { style: sHdr }, 'Classifications'),
      glossary.classifications.map(function(c) {
        return React.createElement('div', { key: c.typeName, style: Object.assign({}, cardStyle, { borderLeft: '3px solid var(--classif)' }) },
          React.createElement('div', { style: { fontSize: 12, fontWeight: 600, color: 'var(--classif)', marginBottom: Object.keys(c.properties || {}).length ? 4 : 0 } }, c.typeName),
          Object.entries(c.properties || {}).map(function(e) {
            return React.createElement('div', { key: e[0], style: { fontSize: 11, color: 'var(--muted)' } },
              e[0] + ': ', React.createElement('span', { style: { color: 'var(--text)' } }, String(e[1])));
          })
        );
      })
    ),
    React.createElement(MermaidSection, { guid: glossary.guid })
  );
}

function GlossaryTermDetail({ term, onNavigateToTerm, onNavigateToDataDesign, onNavigateToElement, isElementLinkable }) {
  if (!term) return null;
  var sHdr   = { fontSize: 11, fontWeight: 700, letterSpacing: '0.07em', textTransform: 'uppercase', color: 'var(--accent)', marginBottom: 8, marginTop: 20 };
  var fields = [['Qualified Name', term.qualifiedName],['GUID', term.guid],['Abbreviation', term.abbreviation],['Summary', term.summary],['Examples', term.examples],['Usage', term.usage],['Status', term.status],['Content Status', term.contentStatus],['Activity Status', term.activityStatus]].filter(function(r){return r[1]&&String(r[1]).trim();});
  var folderList = term.folders || [];
  var relGroups  = Object.entries(term.relationships || {}).filter(function(e) { return e[1].length > 0; });
  var relBtnStyle = { fontSize: 11, padding: '2px 8px', borderRadius: 4, border: '1px solid rgba(96,165,250,.4)', background: 'rgba(96,165,250,.08)', color: 'var(--accent)', cursor: 'pointer' };
  var ddBtnStyle  = { fontSize: 11, padding: '2px 8px', borderRadius: 4, border: '1px solid rgba(94,234,212,.4)', background: 'rgba(94,234,212,.1)', color: '#5eead4', cursor: 'pointer' };
  var DD_TYPES = { DataField: true, DataStructure: true, DataSpec: true, DataGrain: true, DataClass: true };
  return React.createElement('div', { style: { padding: '20px 24px', overflowY: 'auto', height: '100%' } },
    React.createElement('div', { style: { display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4, flexWrap: 'wrap' } },
      React.createElement('div', { style: { fontSize: 18, fontWeight: 700, color: 'var(--text)' } }, term.displayName),
      term.isTemplateSubstitute && React.createElement('span', { style: Object.assign({}, _glsBadge, { background: 'rgba(245,158,11,.15)', color: '#fbbf24', border: '0.5px solid rgba(245,158,11,.4)' }) }, 'Template Substitute'),
      !term.isTemplateSubstitute && term.isSourcedFromTemplate && React.createElement('span', { style: Object.assign({}, _glsBadge, { background: 'rgba(245,158,11,.08)', color: '#fbbf24', border: '0.5px solid rgba(245,158,11,.25)' }) }, 'From Template'),
      React.createElement('div', { style: { marginLeft: 'auto' } }, React.createElement(EgeriaFeedbackWidget, { guid: term.guid }))
    ),
    folderList.length > 0 && React.createElement('div', { style: { display: 'flex', flexWrap: 'wrap', gap: 4, marginBottom: 8, marginTop: 6 } },
      React.createElement('span', { style: { fontSize: 11, color: 'var(--dim)', marginRight: 4 } }, 'Folders:'),
      folderList.map(function(f) { return React.createElement('span', { key: f.guid, style: Object.assign({}, _glsBadge, { background: 'rgba(99,102,241,.1)', color: '#818cf8', border: '0.5px solid rgba(99,102,241,.25)' }) }, f.displayName || f.guid); })
    ),
    term.description && React.createElement('div', { style: { fontSize: 13, marginBottom: 16, color: 'var(--text)' } }, renderMd(term.description)),
    React.createElement(MermaidSection, { guid: term.guid }),
    fields.length > 0 && React.createElement('div', null,
      React.createElement('div', { style: sHdr }, 'Properties'),
      React.createElement('table', { style: { width: '100%', borderCollapse: 'collapse', fontSize: 12 } },
        React.createElement('tbody', null,
          fields.map(function(r) {
            var mono = r[0] === 'Qualified Name' || r[0] === 'GUID';
            return React.createElement('tr', { key: r[0], style: { borderTop: '1px solid var(--border)' } },
              React.createElement('td', { style: { padding: '5px 12px 5px 0', color: 'var(--dim)', width: 140, verticalAlign: 'top', whiteSpace: 'nowrap' } }, r[0]),
              React.createElement('td', { style: { padding: '5px 0', color: 'var(--text)', wordBreak: 'break-all', fontFamily: mono ? 'ui-monospace,monospace' : 'inherit', fontSize: mono ? 11 : 12 } }, mono ? r[1] : renderMd(r[1])));
          })
        )
      )
    ),
    (term.classifications || []).length > 0 && React.createElement('div', null,
      React.createElement('div', { style: sHdr }, 'Classifications'),
      term.classifications.map(function(c) {
        var cardStyle = { background: 'var(--card)', border: '1px solid var(--border)', borderRadius: 6, padding: '10px 14px', marginBottom: 8 };
        return React.createElement('div', { key: c.typeName, style: Object.assign({}, cardStyle, { borderLeft: '3px solid var(--classif)' }) },
          React.createElement('div', { style: { fontSize: 12, fontWeight: 600, color: 'var(--classif)', marginBottom: Object.keys(c.properties || {}).length ? 4 : 0 } }, c.typeName),
          Object.entries(c.properties || {}).map(function(e) {
            return React.createElement('div', { key: e[0], style: { fontSize: 11, color: 'var(--muted)' } },
              e[0] + ': ', React.createElement('span', { style: { color: 'var(--text)' } }, String(e[1])));
          })
        );
      })
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
var EGERIA_EXPLORER_NAV = {
  SolutionComponent:     { hash: 'solution-architect', kind: 'components' },
  SolutionBlueprint:     { hash: 'solution-architect', kind: 'blueprints' },
  InformationSupplyChain:{ hash: 'isc' },
  ActorRole:             { hash: 'actors', kind: 'roles' },
  ActorProfile:          { hash: 'actors', kind: 'profiles' },
  UserIdentity:          { hash: 'actors', kind: 'identities' },
  Location:              { hash: 'locations' },
  Community:             { hash: 'communities' },
  GovernanceDefinition:  { hash: 'governance' },
  ReferenceDataValue:    { hash: 'reference-data' },
  DataSpec:              { hash: 'data-design', kind: 'specs' },
  DataStructure:         { hash: 'data-design', kind: 'structures' },
  DataField:             { hash: 'data-design', kind: 'fields' },
  DataGrain:             { hash: 'data-design', kind: 'grains' },
  DataClass:             { hash: 'data-design', kind: 'classes' },
  CollectionFolder:      { hash: 'digital-products' },
  DigitalProduct:        { hash: 'digital-products' },
  Collection:            { hash: 'digital-products' },
  GlossaryTerm:          { hash: 'glossary' },
  Glossary:              { hash: 'glossary' },
  GlossaryCategory:      { hash: 'glossary' },
};

function resolveExplorerNav(item) {
  if (!item) return null;
  var nav = item.typeName ? EGERIA_EXPLORER_NAV[item.typeName] : null;
  if (!nav) {
    var supers = item.superTypeNames || item.superTypes || [];
    for (var i = 0; i < supers.length; i++) { nav = EGERIA_EXPLORER_NAV[supers[i]]; if (nav) break; }
  }
  return nav || null;
}

function isElementLinkable(item) { return !!resolveExplorerNav(item); }

function crossAppNavigate(item, explicitNav) {
  var nav = explicitNav || resolveExplorerNav(item);
  if (!nav || !item || !item.guid) return false;
  var url = '/egeria-explorer?guid=' + encodeURIComponent(item.guid)
          + (nav.kind ? '&kind=' + encodeURIComponent(nav.kind) : '')
          + '#' + nav.hash;
  window.open(url, '_blank');
  return true;
}

/* ── Collapsible — a foldable titled section. ─────────────────────────────── */
function Collapsible({ title, defaultOpen, count, children }) {
  var _o = React.useState(defaultOpen !== false), open = _o[0], setOpen = _o[1];
  return React.createElement('div', { style: { borderTop: '1px solid var(--border)' } },
    React.createElement('div', {
      onClick: function() { setOpen(!open); },
      style: { display: 'flex', alignItems: 'center', gap: 6, padding: '8px 4px', cursor: 'pointer', userSelect: 'none', fontSize: 11, fontWeight: 700, letterSpacing: '0.05em', textTransform: 'uppercase', color: 'var(--accent)' }
    },
      React.createElement('span', { style: { width: 12, display: 'inline-block', color: 'var(--muted)' } }, open ? '▾' : '▸'),
      title,
      (count != null) && React.createElement('span', { style: { color: 'var(--dim)', fontWeight: 600 } }, '(' + count + ')')
    ),
    open && React.createElement('div', { style: { padding: '2px 4px 12px 18px' } }, children)
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
  var item = { guid: hdr.guid || element.guid, typeName: type.typeName, superTypeNames: type.superTypeNames || [] };

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
  return React.createElement('div', null,
    isElementLinkable(item) && React.createElement('button', {
      onClick: function() { if (onCrossLink) onCrossLink(item); else crossAppNavigate(item); },
      style: { fontSize: 11, padding: '2px 8px', borderRadius: 4, border: '1px solid rgba(96,165,250,.4)', background: 'rgba(96,165,250,.08)', color: 'var(--accent)', cursor: 'pointer', marginBottom: 8 }
    }, 'Open in Egeria Explorer ↗'),
    React.createElement('table', { style: { width: '100%', borderCollapse: 'collapse' } },
      React.createElement('tbody', null,
        rows.map(function(r, i) {
          return React.createElement('tr', { key: i },
            React.createElement('td', { style: th }, r[0]),
            React.createElement('td', { style: td }, r[1]));
        })
      )
    )
  );
}
