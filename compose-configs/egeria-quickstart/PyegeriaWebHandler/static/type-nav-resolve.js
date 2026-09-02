/* type-nav-resolve.js — plain vanilla JS, no React/JSX. Loadable from any page
 * via a bare <script src="/static/type-nav-resolve.js"> tag (React-based SPAs
 * and the plain-vanilla demo-portal.html alike).
 *
 * Single resolver for "which UI destination shows Egeria type X", backed by
 * static/type-nav-map.json. Replaces the three former hand-duplicated tables
 * (TYPE_TO_NAV in tech-catalog.html, EGERIA_EXPLORER_NAV in
 * egeria-shared-ui.js, PORTAL_EXPLORER_NAV in demo-portal.html) — see
 * design-docs/type-system-audit.md.
 *
 * Usage:
 *   loadTypeNavMap().then(function() {
 *     var nav = resolveTypeNav(item.typeName, item.superTypeNames);
 *     // nav is one of the JSON's entry objects (e.g. {explorerHash, kind} or
 *     // {catalogSection, catalogTab, explorerHash}), or null/undefined.
 *   });
 * Call sites that run before the fetch resolves (very unlikely in practice —
 * the map is tiny and same-origin) just see resolveTypeNav return null until
 * loadTypeNavMap()'s promise settles; every consumer here awaits it once in
 * an existing pre-render bootstrap effect, not per-lookup.
 */
(function (global) {
  'use strict';

  var _map = null;
  var _loadPromise = null;

  function loadTypeNavMap() {
    if (_loadPromise) return _loadPromise;
    _loadPromise = fetch('/static/type-nav-map.json')
      .then(function (r) { return r.ok ? r.json() : {}; })
      .then(function (data) { _map = data || {}; return _map; })
      .catch(function () { _map = {}; return _map; });
    return _loadPromise;
  }

  // Exact key match, then walk superTypeNames for the first ancestor present
  // in the map — same lookup order as the old resolveElementNav()/TYPE_TO_NAV
  // inline lookups. Keys starting with "_" are documentation, never real
  // type names, so they can never accidentally match a superTypeNames walk.
  function resolveTypeNav(typeName, superTypeNames) {
    if (!_map) return null;
    var nav = typeName ? _map[typeName] : null;
    if (!nav) {
      var supers = superTypeNames || [];
      for (var i = 0; i < supers.length; i++) {
        if (supers[i] && supers[i].charAt(0) !== '_' && _map[supers[i]]) { nav = _map[supers[i]]; break; }
      }
    }
    return nav || null;
  }

  global.loadTypeNavMap = loadTypeNavMap;
  global.resolveTypeNav = resolveTypeNav;
  // Kick off the fetch immediately on script load — same-origin, tiny file,
  // so by the time any first render/click happens it's almost always already
  // resolved; callers that want to guarantee it's ready can still await
  // loadTypeNavMap() explicitly (e.g. inside an existing pre-render effect).
  loadTypeNavMap();
})(window);
