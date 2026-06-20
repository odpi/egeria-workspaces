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
