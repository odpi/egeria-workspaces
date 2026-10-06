/* SPDX-License-Identifier: Apache-2.0
 * Copyright Contributors to the ODPi Egeria project.
 *
 * app-bar.js — the one header bar every portal app shares.
 *
 * Layout (same on every page, React or plain-JS):
 *
 *   [⌂ Portal] | [icon] Title  subtitle   [page's own controls ...]   [page extras] [identity] [☾ Dark]
 *
 * The Portal link is ALWAYS first and ALWAYS shown — it never depends on
 * whether a persona is chosen or the user is logged in. Identity ("🎭 persona",
 * "👤 user", or "🎭 Choose persona") and the light/dark toggle are always last.
 * The "💬 Feedback" button floats bottom-right (draggable; position shared
 * with the React FeedbackButton via the same localStorage key).
 *
 * No framework dependency. Load it in <head> (synchronously) so the saved theme
 * is applied before first paint:
 *
 *     <script src="/static/app-bar.js?v=..."></script>
 *
 * Plain-JS pages then declare the bar and let this script fill it in:
 *
 *     <header class="eg-appbar" data-icon="📊" data-title="Egeria Overview"
 *             data-subtitle="Catalog Health" data-feedback="overview">
 *       <div class="eg-appbar-middle"> ...tabs / search / filters... </div>
 *       <div class="eg-appbar-extras"> ...page buttons (Export, Run…) ... </div>
 *     </header>
 *
 *   data-identity="none"   suppresses the identity badge (admin pages show their own)
 *   data-feedback="<page>" also mounts the floating feedback button for that page id
 *   data-portal="none"     only for the Portal itself
 *   <span class="eg-app-title" id=..>  declare the title yourself if page script rewrites it
 *
 * React SPAs use AppHeader / ThemeToggle / useEgeriaTheme from
 * egeria-shared-ui.js, which render the same classes and call into
 * window.EgeriaAppBar for theme state.
 *
 * Theme: one key ('egeria-theme' = 'dark' | 'light'), one mechanism (the
 * `light` class on <html>; each page defines its palette under :root.light).
 * Changing it fires a window 'egeria-theme-change' event and syncs other open
 * tabs via the 'storage' event.
 */
(function () {
  if (window.EgeriaAppBar) return;

  var THEME_KEY = 'egeria-theme';
  var FEEDBACK_POS_KEY = 'egeria-feedback-btn-pos';   // shared with FeedbackButton (egeria-shared-ui.js)
  var PICK_PERSONA_URL = '/portal?pick-persona=1';

  // ── Theme ────────────────────────────────────────────────────────────────
  function readTheme() {
    try { return localStorage.getItem(THEME_KEY) === 'light' ? 'light' : 'dark'; } catch (e) { return 'dark'; }
  }
  var theme = readTheme();
  function applyTheme() {
    document.documentElement.classList.toggle('light', theme === 'light');
    var btns = document.querySelectorAll('.eg-theme-btn[data-eg-vanilla]');
    for (var i = 0; i < btns.length; i++) paintThemeBtn(btns[i]);
  }
  function setTheme(t) {
    t = t === 'light' ? 'light' : 'dark';
    if (t === theme) return;
    theme = t;
    try { localStorage.setItem(THEME_KEY, t); } catch (e) {}
    applyTheme();
    window.dispatchEvent(new CustomEvent('egeria-theme-change', { detail: { theme: t } }));
  }
  function onThemeChange(fn) {
    function h(e) { fn(e.detail.theme); }
    window.addEventListener('egeria-theme-change', h);
    return function () { window.removeEventListener('egeria-theme-change', h); };
  }
  window.addEventListener('storage', function (e) {
    if (e.key !== THEME_KEY) return;
    var t = readTheme();
    if (t === theme) return;
    theme = t;
    applyTheme();
    window.dispatchEvent(new CustomEvent('egeria-theme-change', { detail: { theme: t } }));
  });
  applyTheme();   // before first paint — this script is loaded in <head>

  function themeLabel(t) { return t === 'light' ? '☾ Dark' : '☀ Light'; }
  function themeTitle(t) { return t === 'light' ? 'Switch to dark mode' : 'Switch to light mode'; }
  function paintThemeBtn(b) { b.textContent = themeLabel(theme); b.title = themeTitle(theme); }

  // ── Styles ───────────────────────────────────────────────────────────────
  // Only the shared vars every portal palette defines (--text, --muted,
  // --border, --accent, --bg, --card) plus --panel where a page has one.
  var CSS = [
    '.eg-appbar { display:flex; align-items:center; gap:10px; flex-wrap:nowrap; min-height:46px; box-sizing:border-box;',
    '  padding:6px 16px; background:var(--panel, var(--card)); color:var(--text); border-bottom:1px solid var(--border);',
    '  flex-shrink:0; font-family:inherit; font-size:13px; line-height:1.3; position:relative; z-index:20; }',
    '.eg-appbar.eg-sticky { position:sticky; top:0; }',
    '.eg-appbar a.eg-portal { display:inline-flex; align-items:center; gap:5px; padding:3px 10px; border-radius:6px;',
    '  border:1px solid var(--border); color:var(--muted); text-decoration:none; font-size:12px; font-weight:600;',
    '  white-space:nowrap; flex-shrink:0; }',
    '.eg-appbar a.eg-portal:hover { color:var(--text); border-color:var(--accent); }',
    '.eg-appbar .eg-sep { width:1px; height:18px; background:var(--border); flex-shrink:0; }',
    '.eg-appbar .eg-app { display:flex; align-items:center; gap:7px; flex-shrink:0; min-width:0; }',
    '.eg-appbar .eg-app-icon { font-size:17px; line-height:1; }',
    '.eg-appbar .eg-app-icon img { height:20px; width:auto; display:block; }',
    '.eg-appbar .eg-app-title { font-size:15px; font-weight:700; white-space:nowrap; color:var(--text); }',
    '.eg-appbar .eg-app-sub { font-size:11px; color:var(--muted); white-space:nowrap; }',
    '.eg-appbar .eg-appbar-middle { display:flex; align-items:center; gap:8px; flex:1 1 auto; min-width:0; flex-wrap:wrap; }',
    // Wide screens: page controls wrap inside the middle slot, so Portal/title stay
    // left and identity/theme stay right. Phones: let the whole bar wrap.
    '@media (max-width: 720px) { .eg-appbar { flex-wrap:wrap; } }',
    '.eg-appbar .eg-appbar-right, .eg-appbar .eg-appbar-extras { display:flex; align-items:center; gap:8px; margin-left:auto; flex-shrink:0; }',
    '.eg-appbar .eg-appbar-right .eg-appbar-extras { margin-left:0; }',
    '.eg-appbar .eg-id { font-size:12px; padding:2px 10px; border-radius:12px; white-space:nowrap; text-decoration:none;',
    '  border:1px solid var(--border); color:var(--text); max-width:240px; overflow:hidden; text-overflow:ellipsis; }',
    '.eg-appbar .eg-id-persona { color:var(--accent); border-color:var(--accent); }',
    '.eg-appbar .eg-id-user { color:#34d399; border-color:rgba(52,211,153,.45); }',
    '.eg-appbar .eg-id-choose { color:var(--accent); border-style:dashed; border-color:var(--accent); }',
    '.eg-appbar a.eg-id:hover { background:rgba(127,127,127,.12); }',
    '.eg-appbar .eg-forlineage { display:flex; align-items:center; gap:5px; font-size:11px; color:var(--muted); cursor:pointer;',
    '  user-select:none; white-space:nowrap; padding:2px 8px; border:1px solid var(--border); border-radius:12px; }',
    '.eg-appbar .eg-forlineage input { cursor:pointer; accent-color:var(--accent); margin:0; }',
    '.eg-theme-btn { background:transparent; border:1px solid var(--border); color:var(--muted); border-radius:20px;',
    '  padding:3px 12px; cursor:pointer; font-size:12px; font-family:inherit; white-space:nowrap; }',
    '.eg-theme-btn:hover { color:var(--text); border-color:var(--accent); }',
    // floating feedback (plain-JS pages; React pages use FeedbackButton)
    '.eg-fb-btn { position:fixed; z-index:900; background:var(--accent); color:#fff; border:none; border-radius:20px;',
    '  padding:7px 15px; font-size:12px; font-weight:600; cursor:grab; box-shadow:0 2px 8px rgba(0,0,0,.3);',
    '  letter-spacing:.02em; touch-action:none; user-select:none; font-family:inherit; }',
    '.eg-fb-ovl { position:fixed; inset:0; z-index:1000; background:rgba(0,0,0,.45); display:none; padding:24px; }',
    '.eg-fb-ovl.open { display:flex; }',
    '.eg-fb-panel { background:var(--card); color:var(--text); border:1px solid var(--border); border-radius:12px;',
    '  padding:22px 26px; width:340px; box-shadow:0 8px 32px rgba(0,0,0,.3); font-size:13px; }',
    '.eg-fb-panel h4 { font-size:14px; font-weight:700; margin:0 0 4px; }',
    '.eg-fb-page { font-size:11px; color:var(--muted); margin-bottom:12px; }',
    '.eg-fb-page code { color:var(--text); font-family:ui-monospace,monospace; font-size:10px; }',
    '.eg-fb-stars { display:flex; gap:3px; margin-bottom:10px; }',
    '.eg-fb-stars span { font-size:26px; cursor:pointer; color:var(--muted); line-height:1; }',
    '.eg-fb-stars span.on { color:#f59e0b; }',
    '.eg-fb-inp { width:100%; box-sizing:border-box; background:var(--bg); border:1px solid var(--border); border-radius:6px;',
    '  padding:7px 9px; color:var(--text); font-size:12px; font-family:inherit; outline:none; margin-bottom:8px; display:block; }',
    'textarea.eg-fb-inp { resize:vertical; }',
    '.eg-fb-chk { display:flex; align-items:center; gap:6px; font-size:12px; color:var(--muted); margin-bottom:6px; }',
    '.eg-fb-actions { display:flex; gap:8px; justify-content:flex-end; margin-top:8px; }',
    '.eg-fb-actions button { padding:6px 14px; border-radius:6px; font-size:12px; cursor:pointer; font-family:inherit; }',
    '.eg-fb-cancel { border:1px solid var(--border); background:transparent; color:var(--text); }',
    '.eg-fb-send { border:none; background:var(--accent); color:#fff; font-weight:600; }',
    '.eg-fb-send:disabled { opacity:.45; cursor:default; }',
    '.eg-fb-thanks { text-align:center; padding:16px 0; color:var(--accent); font-size:15px; font-weight:600; }',
  ].join('\n');
  function injectCss() {
    if (document.getElementById('eg-appbar-css')) return;
    var s = document.createElement('style');
    s.id = 'eg-appbar-css';
    s.textContent = CSS;
    (document.head || document.documentElement).appendChild(s);
  }
  injectCss();

  // ── Identity ─────────────────────────────────────────────────────────────
  // Same rules as the React SPAs: server-managed auth → the signed-in user;
  // otherwise the persona this browser picked under the CURRENT portal account
  // (read-only here — loadOwnedPersona in egeria-shared-ui.js owns clearing a
  // mismatched one); otherwise a "Choose persona" link.
  var meP = null;
  function authMe() {
    if (!meP) {
      meP = fetch('/api/auth/me', { credentials: 'same-origin' })
        .then(function (r) { return r.ok ? r.json() : null; })
        .catch(function () { return null; });
    }
    return meP;
  }
  function storedPersona(ownerId) {
    try {
      var raw = localStorage.getItem('egeria-persona');
      if (!raw) return null;
      var p = JSON.parse(raw);
      return p && p.ownerId === (ownerId || null) ? p : null;
    } catch (e) { return null; }
  }
  function identityFor(input) {
    // input: { activePersona, authUser, srvManaged }  (React pages pass their own state)
    input = input || {};
    if (input.activePersona) {
      var p = input.activePersona;
      return { kind: 'persona', label: p.display_name || p.id, title: (p.coco_title ? p.coco_title + ' — ' : '') + 'Switch persona at the Portal' };
    }
    if (input.authUser) {
      var u = input.authUser;
      return { kind: 'user', label: u.displayName || u.display_name || u.userId || u.id, title: u.userId || u.id || '' };
    }
    if (input.srvManaged) return null;
    return { kind: 'choose', label: 'Choose persona', title: 'Pick a Coco persona at the Portal' };
  }
  function autoIdentity() {
    return authMe().then(function (me) {
      if (!me) return null;
      if (me.server_managed_auth) {
        return me.authenticated ? identityFor({ authUser: { displayName: me.display_name, userId: me.id } }) : null;
      }
      return identityFor({ activePersona: storedPersona(me.id) });
    });
  }
  function identityEl(id) {
    if (!id) return null;
    var interactive = id.kind !== 'user';
    var el = document.createElement(interactive ? 'a' : 'span');
    el.className = 'eg-id eg-id-' + id.kind;
    if (interactive) el.href = PICK_PERSONA_URL;
    el.title = id.title || '';
    el.textContent = (id.kind === 'user' ? '👤 ' : '🎭 ') + id.label;
    return el;
  }

  // ── Plain-JS bar ─────────────────────────────────────────────────────────
  function mount(bar) {
    if (!bar || bar.getAttribute('data-eg-mounted')) return;
    bar.setAttribute('data-eg-mounted', '1');
    var ds = bar.dataset;
    var middle = bar.querySelector(':scope > .eg-appbar-middle');
    var extras = bar.querySelector(':scope > .eg-appbar-extras');
    // A page whose own script rewrites the title (e.g. the org name) declares the
    // title element itself, so it exists — with its id — before this runs.
    var ownTitle = bar.querySelector(':scope > .eg-app-title');
    // anything else the page put directly in the bar goes to the middle slot
    var loose = [];
    for (var i = 0; i < bar.childNodes.length; i++) {
      var n = bar.childNodes[i];
      if (n !== middle && n !== extras && n !== ownTitle) loose.push(n);
    }
    if (!middle) { middle = document.createElement('div'); middle.className = 'eg-appbar-middle'; }
    loose.forEach(function (n) { middle.appendChild(n); });

    var frag = document.createDocumentFragment();
    if (ds.portal !== 'none') {
      var a = document.createElement('a');
      a.className = 'eg-portal'; a.href = '/portal'; a.title = 'Back to the Portal';
      a.textContent = '⌂ Portal';
      frag.appendChild(a);
      var sep = document.createElement('span'); sep.className = 'eg-sep';
      frag.appendChild(sep);
    }
    var app = document.createElement('div'); app.className = 'eg-app';
    if (ds.logo) {
      var ic = document.createElement('span'); ic.className = 'eg-app-icon';
      var img = document.createElement('img'); img.src = ds.logo; img.alt = '';
      ic.appendChild(img); app.appendChild(ic);
    } else if (ds.icon) {
      var ic2 = document.createElement('span'); ic2.className = 'eg-app-icon'; ic2.textContent = ds.icon;
      app.appendChild(ic2);
    }
    var t = ownTitle;
    if (!t) { t = document.createElement('span'); t.className = 'eg-app-title'; t.textContent = ds.title || document.title; }
    app.appendChild(t);
    if (ds.subtitle) {
      var sub = document.createElement('span'); sub.className = 'eg-app-sub'; sub.textContent = ds.subtitle;
      app.appendChild(sub);
    }
    frag.appendChild(app);
    frag.appendChild(middle);

    var right = document.createElement('div'); right.className = 'eg-appbar-right';
    if (extras) right.appendChild(extras);
    var idSlot = document.createElement('span'); idSlot.className = 'eg-id-slot';
    right.appendChild(idSlot);
    var tb = document.createElement('button');
    tb.className = 'eg-theme-btn'; tb.setAttribute('data-eg-vanilla', '1');
    wireThemeButton(tb);
    right.appendChild(tb);
    frag.appendChild(right);

    bar.textContent = '';
    bar.appendChild(frag);

    if (ds.identity !== 'none') {
      autoIdentity().then(function (id) {
        if (bar.getAttribute('data-eg-identity-set')) return;   // page called setIdentity first
        renderIdentity(bar, id);
      });
    }
    if (ds.feedback) mountFeedback({ page: ds.feedback });
  }
  function renderIdentity(bar, id) {
    var slot = bar.querySelector('.eg-id-slot');
    if (!slot) return;
    slot.textContent = '';
    var el = identityEl(id);
    if (el) slot.appendChild(el);
  }
  // Pages that know better (e.g. the Overview knows which Egeria user its data
  // was actually queried as) can override the automatic badge.
  function setIdentity(id) {
    var bars = document.querySelectorAll('.eg-appbar[data-eg-mounted]');
    for (var i = 0; i < bars.length; i++) {
      bars[i].setAttribute('data-eg-identity-set', '1');
      renderIdentity(bars[i], id);
    }
  }
  // A page that keeps its own header (the Portal) can still drop in the shared
  // toggle: <button class="eg-theme-btn" data-eg-vanilla></button>
  function wireThemeButton(b) {
    if (b.getAttribute('data-eg-wired')) return;
    b.setAttribute('data-eg-wired', '1');
    b.type = 'button';
    b.addEventListener('click', function () { setTheme(theme === 'light' ? 'dark' : 'light'); });
    paintThemeBtn(b);
  }
  function mountAll() {
    var bars = document.querySelectorAll('header.eg-appbar[data-title], header.eg-appbar[data-logo]');
    for (var i = 0; i < bars.length; i++) mount(bars[i]);
    var btns = document.querySelectorAll('.eg-theme-btn[data-eg-vanilla]');
    for (var j = 0; j < btns.length; j++) wireThemeButton(btns[j]);
  }

  // ── Floating feedback (plain-JS pages) ───────────────────────────────────
  // Same /api/demo-feedback contract & field shape as FeedbackButton in
  // egeria-shared-ui.js, so entries land in the same store.
  function sessionId() {
    try {
      var id = sessionStorage.getItem('_egeria_session_id');
      if (!id) {
        id = (window.crypto && crypto.randomUUID) ? crypto.randomUUID() : Date.now().toString(36) + Math.random().toString(36).substr(2);
        sessionStorage.setItem('_egeria_session_id', id);
      }
      return id;
    } catch (e) { return 'anon-' + Date.now(); }
  }
  var feedbackMounted = false;
  function mountFeedback(opts) {
    if (feedbackMounted) return;
    feedbackMounted = true;
    var page = (opts && opts.page) || location.pathname.replace(/^\//, '') || 'page';

    var pos = { right: 20, bottom: 20 };
    try { var raw = localStorage.getItem(FEEDBACK_POS_KEY); if (raw) { var p = JSON.parse(raw); if (typeof p.right === 'number' && typeof p.bottom === 'number') pos = p; } } catch (e) {}

    var btn = document.createElement('button');
    btn.type = 'button'; btn.className = 'eg-fb-btn'; btn.title = 'Share your feedback — drag to move';
    btn.textContent = '💬 Feedback';
    function place() {
      pos.right = Math.min(Math.max(pos.right, 4), Math.max(4, window.innerWidth - btn.offsetWidth - 4));
      pos.bottom = Math.min(Math.max(pos.bottom, 4), Math.max(4, window.innerHeight - btn.offsetHeight - 4));
      btn.style.right = pos.right + 'px'; btn.style.bottom = pos.bottom + 'px';
    }

    var ovl = document.createElement('div'); ovl.className = 'eg-fb-ovl';
    ovl.innerHTML =
      '<div class="eg-fb-panel">' +
        '<div class="eg-fb-form">' +
          '<h4>Share your feedback</h4>' +
          '<div class="eg-fb-page">Page: <code></code></div>' +
          '<div class="eg-fb-stars">' + [1, 2, 3, 4, 5].map(function (n) { return '<span data-n="' + n + '">☆</span>'; }).join('') + '</div>' +
          '<select class="eg-fb-inp eg-fb-category"><option value="">Category (optional)</option>' +
            '<option value="bug">Bug</option><option value="confusing">Confusing</option>' +
            '<option value="suggestion">Suggestion</option><option value="praise">Praise</option></select>' +
          '<textarea class="eg-fb-inp eg-fb-comment" rows="3" placeholder="What\'s on your mind?"></textarea>' +
          '<input class="eg-fb-inp eg-fb-email" type="email" placeholder="Email for follow-up (optional)">' +
          '<label class="eg-fb-chk"><input type="checkbox" class="eg-fb-wants"> I\'d like a response</label>' +
          '<label class="eg-fb-chk"><input type="checkbox" class="eg-fb-consent"> OK to contact me about this feedback</label>' +
          '<div class="eg-fb-actions"><button type="button" class="eg-fb-cancel">Cancel</button>' +
            '<button type="button" class="eg-fb-send" disabled>Send</button></div>' +
        '</div>' +
        '<div class="eg-fb-thanks" style="display:none">✓ Thank you for your feedback!</div>' +
      '</div>';
    function q(sel) { return ovl.querySelector(sel); }
    q('.eg-fb-page code').textContent = page;
    var form = q('.eg-fb-form'), thanks = q('.eg-fb-thanks'), stars = q('.eg-fb-stars'),
        comment = q('.eg-fb-comment'), email = q('.eg-fb-email'), category = q('.eg-fb-category'),
        wants = q('.eg-fb-wants'), consent = q('.eg-fb-consent'), sendBtn = q('.eg-fb-send');
    var rating = 0, hover = 0;
    function paintStars() {
      var n = hover || rating;
      Array.prototype.forEach.call(stars.children, function (s) {
        var on = Number(s.dataset.n) <= n;
        s.textContent = on ? '★' : '☆';
        s.classList.toggle('on', on);
      });
    }
    function updateSend() { sendBtn.disabled = !(rating > 0 || comment.value.trim().length > 0); }
    Array.prototype.forEach.call(stars.children, function (s) {
      s.addEventListener('click', function () { rating = Number(s.dataset.n); paintStars(); updateSend(); });
      s.addEventListener('mouseenter', function () { hover = Number(s.dataset.n); paintStars(); });
      s.addEventListener('mouseleave', function () { hover = 0; paintStars(); });
    });
    comment.addEventListener('input', updateSend);
    function reset() {
      rating = 0; hover = 0; paintStars();
      comment.value = ''; email.value = ''; category.value = '';
      wants.checked = false; consent.checked = false; updateSend();
      form.style.display = ''; thanks.style.display = 'none';
    }
    function open() {
      // open the panel on whichever side of the screen the button sits
      ovl.style.alignItems = pos.bottom > window.innerHeight / 2 ? 'flex-start' : 'flex-end';
      ovl.style.justifyContent = pos.right > window.innerWidth / 2 ? 'flex-start' : 'flex-end';
      ovl.classList.add('open');
    }
    function close() { ovl.classList.remove('open'); reset(); }
    q('.eg-fb-cancel').addEventListener('click', close);
    ovl.addEventListener('click', function (e) { if (e.target === ovl) close(); });
    sendBtn.addEventListener('click', function () {
      if (sendBtn.disabled) return;
      sendBtn.disabled = true; sendBtn.textContent = 'Sending…';
      authMe().then(function (me) {
        var env = !me ? null : me.demo_mode ? 'quickstart-demo' : me.server_managed_auth ? 'freshstart' : 'quickstart-local';
        var persona = me && (me.server_managed_auth ? me.id : (storedPersona(me.id) || {}).id);
        return fetch('/api/demo-feedback', {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            session_id: sessionId(),
            page: page,
            rating: rating || null,
            category: category.value || null,
            message: comment.value.trim() || null,
            email: email.value.trim() || null,
            wants_response: wants.checked,
            consent_to_contact: consent.checked,
            persona: persona || null,
            env: env,
            viewport: window.innerWidth + 'x' + window.innerHeight,
            locale: navigator.language || null,
          }),
        });
      }).then(function () {
        form.style.display = 'none'; thanks.style.display = '';
        setTimeout(close, 2000);
      }).catch(function () {
        updateSend();
      }).then(function () { sendBtn.textContent = 'Send'; });
    });

    // drag (document-level listeners — same reasoning as FeedbackButton)
    var drag = null, justDragged = false;
    function move(x, y) {
      if (!drag) return;
      var dx = x - drag.x, dy = y - drag.y;
      if (!drag.moved && Math.abs(dx) <= 3 && Math.abs(dy) <= 3) return;
      drag.moved = true;
      pos = { right: drag.right - dx, bottom: drag.bottom - dy };
      place();
    }
    function onMove(e) { move(e.clientX, e.clientY); }
    function onTouchMove(e) { if (e.touches && e.touches[0]) move(e.touches[0].clientX, e.touches[0].clientY); }
    function end() {
      document.removeEventListener('mousemove', onMove);
      document.removeEventListener('mouseup', end);
      document.removeEventListener('touchmove', onTouchMove);
      document.removeEventListener('touchend', end);
      btn.style.cursor = 'grab';
      if (drag && drag.moved) {
        justDragged = true;
        try { localStorage.setItem(FEEDBACK_POS_KEY, JSON.stringify(pos)); } catch (e) {}
      }
      drag = null;
    }
    function begin(x, y) {
      drag = { x: x, y: y, right: pos.right, bottom: pos.bottom, moved: false };
      btn.style.cursor = 'grabbing';
      document.addEventListener('mousemove', onMove);
      document.addEventListener('mouseup', end);
      document.addEventListener('touchmove', onTouchMove, { passive: false });
      document.addEventListener('touchend', end);
    }
    btn.addEventListener('mousedown', function (e) { if (e.button !== 0) return; e.preventDefault(); begin(e.clientX, e.clientY); });
    btn.addEventListener('touchstart', function (e) { if (e.touches && e.touches[0]) begin(e.touches[0].clientX, e.touches[0].clientY); });
    btn.addEventListener('click', function () {
      if (justDragged) { justDragged = false; return; }
      open();
    });

    document.body.appendChild(btn);
    document.body.appendChild(ovl);
    place();
    window.addEventListener('resize', place);
  }

  window.EgeriaAppBar = {
    getTheme: function () { return theme; },
    setTheme: setTheme,
    toggleTheme: function () { setTheme(theme === 'light' ? 'dark' : 'light'); },
    onThemeChange: onThemeChange,
    themeLabel: themeLabel,
    themeTitle: themeTitle,
    identityFor: identityFor,
    setIdentity: setIdentity,
    mount: mount,
    mountFeedback: mountFeedback,
    PICK_PERSONA_URL: PICK_PERSONA_URL,
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mountAll);
  else mountAll();
})();
