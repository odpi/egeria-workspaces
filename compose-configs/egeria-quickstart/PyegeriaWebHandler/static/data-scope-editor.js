/* SPDX-License-Identifier: Apache-2.0
 * Copyright Contributors to the ODPi Egeria project.
 *
 * Data scope editor and view, shared by The Catalog (a resource's DataScope) and the
 * Resource Locator (a Data Lens). Both draw their fields from the dimension groups
 * that /api/data-scope/dimensions reads from Egeria's type definitions, so a dimension
 * Egeria adds later shows up here with no change.
 *
 * Group shapes: timeRange (start/end dates, UTC), bound (min/max numbers), map
 * (name/value pairs), field (one value). A group marked readOnly (additionalProperties,
 * which Egeria's lineage service writes) is shown, never edited.
 *
 *   DataScopeEditor({ groups, scope, busy, error, saveLabel, onSave(values), onCancel, onClear })
 *   DataScopeView({ groups, scope })           — what a scope records, "not recorded" when absent
 *   dataScopeValues(groups, scope)             — form values from stored properties
 *   dataScopeFetchDimensions(type, creds)      — cached GET of the groups
 *   dataScopeDateText(iso, role)               — a stored time as the form shows it (UTC)
 *   dataScopePeriodText(start, end)            — a period for a chip: "2026", "2026-03", or from → to
 *
 * Dates are typed, not picked (PO-35, 2026-11-17): a date-and-time picker filled in the time of
 * day when only a date was chosen, so "2026" saved 09:04 → 09:05. A year, month or day now
 * means the whole of it; the server turns a start into its first instant and an end into its
 * last (…23:59:59.999Z). A time can still be typed (yyyy-mm-dd hh:mm, UTC).
 */
(function () {
  var h = React.createElement;
  var _dims = {};

  function dataScopeFetchDimensions(type, creds) {
    if (!_dims[type]) {
      _dims[type] = egeriaFetch('/api/data-scope/dimensions?type=' + encodeURIComponent(type), creds)
        .then(function (r) {
          return r.json().catch(function () { return {}; }).then(function (d) {
            if (!r.ok) throw new Error((d && d.detail) || ('HTTP ' + r.status));
            return d.groups;
          });
        })
        .catch(function (e) { delete _dims[type]; throw e; });
    }
    return _dims[type];
  }

  // Egeria returns 0 for bounds never set, so a bound group of zeros holds no value.
  function _boundIsEmpty(g, scope) {
    return g.fields.every(function (f) { var v = scope[f.name]; return v === undefined || v === null || Number(v) === 0; });
  }

  function _pad(n) { return (n < 10 ? '0' : '') + n; }

  // A stored time as the form shows it, in UTC: just the day when it is the first instant of a
  // day (a start) or the last (an end), else the day and time.
  function dataScopeDateText(iso, role) {
    var d = new Date(iso);
    if (iso === undefined || iso === null || iso === '' || isNaN(d)) return iso === undefined || iso === null ? '' : String(iso);
    var day = d.getUTCFullYear() + '-' + _pad(d.getUTCMonth() + 1) + '-' + _pad(d.getUTCDate());
    var h = d.getUTCHours(), m = d.getUTCMinutes(), sec = d.getUTCSeconds(), ms = d.getUTCMilliseconds();
    if (role !== 'end' && !h && !m && !sec && !ms) return day;
    if (role === 'end' && h === 23 && m === 59 && sec === 59) return day;
    return day + ' ' + _pad(h) + ':' + _pad(m);
  }

  // A period for a chip: a whole year or month collapses to "2026" or "2026-03"; else from → to,
  // with "UTC" when a time is shown. An open end is "…".
  function dataScopePeriodText(start, end) {
    var s = start ? dataScopeDateText(start, 'start') : '', e = end ? dataScopeDateText(end, 'end') : '';
    var ms = /^(\d{4})-(\d{2})-01$/.exec(s), me = /^(\d{4})-(\d{2})-(\d{2})$/.exec(e);
    if (ms && me && ms[1] === me[1]) {
      var last = new Date(Date.UTC(+me[1], +me[2], 0)).getUTCDate();
      if (ms[2] === '01' && me[2] === '12' && me[3] === '31') return ms[1];
      if (ms[2] === me[2] && +me[3] === last) return ms[1] + '-' + ms[2];
    }
    var timed = s.indexOf(':') >= 0 || e.indexOf(':') >= 0;
    return (s || '\u2026') + ' \u2192 ' + (e || '\u2026') + (timed ? ' UTC' : '');
  }

  function dataScopeValues(groups, scope) {
    var out = {};
    scope = scope || {};
    groups.forEach(function (g) {
      var emptyBound = g.shape === 'bound' && _boundIsEmpty(g, scope);
      g.fields.forEach(function (f) {
        var v = scope[f.name];
        if (v === undefined || v === null || emptyBound) { out[f.name] = f.kind === 'map' ? {} : ''; return; }
        if (f.kind === 'date') out[f.name] = dataScopeDateText(v, f.role);   // yyyy-mm-dd, or yyyy-mm-dd hh:mm; UTC
        else if (f.kind === 'map') out[f.name] = Object.assign({}, v);
        else out[f.name] = String(v);
      });
    });
    return out;
  }

  function _fmt(f, v) {
    if (f.kind === 'date') { var t = dataScopeDateText(v, f.role); return t.indexOf(':') >= 0 ? t + ' UTC' : t; }
    return String(v);
  }

  var box = { display: 'flex', flexDirection: 'column', gap: 4, marginBottom: 12 };
  var lab = { fontSize: 12, fontWeight: 600, color: 'var(--text)' };
  var hint = { fontSize: 11, color: 'var(--dim)' };
  var inp = { background: 'var(--bg, transparent)', color: 'var(--text)', border: '1px solid var(--border)', borderRadius: 4,
              padding: '4px 6px', fontSize: 12, minWidth: 0, flex: '1 1 160px' };
  var row = { display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' };

  function Tip(text) {
    return text ? h('span', { title: text, tabIndex: 0, 'aria-label': text,
      style: { marginLeft: 4, fontSize: 10, color: 'var(--dim)', border: '1px solid var(--dim)', borderRadius: '50%',
               width: 13, height: 13, display: 'inline-flex', alignItems: 'center', justifyContent: 'center', cursor: 'help' } }, '?') : null;
  }

  function MapRows(props) {
    var f = props.field, value = props.value || {}, set = props.onChange, ro = props.readOnly;
    var keys = Object.keys(value);
    if (ro) {
      if (!keys.length) return h('div', { style: hint }, 'none');
      return h('table', { style: { fontSize: 12, borderCollapse: 'collapse' } }, h('tbody', null, keys.map(function (k) {
        return h('tr', { key: k }, h('td', { style: { color: 'var(--dim)', paddingRight: 10, verticalAlign: 'top' } }, k),
          h('td', { style: { wordBreak: 'break-all' } }, String(value[k])));
      })));
    }
    function put(oldKey, newKey, newVal) {
      var next = {};
      keys.forEach(function (k) { if (k === oldKey) { if (newKey !== null) next[newKey] = newVal; } else next[k] = value[k]; });
      if (oldKey === null) next[newKey] = newVal;
      set(next);
    }
    return h('div', { style: { display: 'flex', flexDirection: 'column', gap: 4 } },
      keys.map(function (k, i) {
        return h('div', { key: i, style: row },
          h('input', { style: inp, value: k, placeholder: 'name', 'aria-label': f.name + ' name',
            onChange: function (e) { put(k, e.target.value, value[k]); } }),
          h('input', { style: inp, value: value[k], placeholder: 'value', 'aria-label': f.name + ' value',
            onChange: function (e) { put(k, k, e.target.value); } }),
          h('button', { type: 'button', onClick: function () { put(k, null); }, title: 'Remove this entry',
            style: { fontSize: 11, background: 'transparent', color: 'var(--dim)', border: '1px solid var(--border)', borderRadius: 4, cursor: 'pointer' } }, '✕'));
      }),
      h('button', { type: 'button', disabled: keys.indexOf('') >= 0, onClick: function () { put(null, '', ''); },
        style: { alignSelf: 'flex-start', fontSize: 11, background: 'transparent', color: 'var(--accent)', border: '1px solid var(--border)', borderRadius: 4, padding: '2px 8px', cursor: 'pointer' } }, '+ add'));
  }

  function Input(props) {
    var f = props.field, v = props.value, set = props.onChange, g = props.group;
    var common = { style: inp, value: v, title: f.help, 'aria-label': f.name, onChange: function (e) { set(e.target.value); } };
    if (f.kind === 'date') return h('input', Object.assign({}, common, { type: 'text', inputMode: 'numeric',
      placeholder: (f.role === 'end' ? 'to' : 'from') + ': yyyy, yyyy-mm or yyyy-mm-dd',
      title: (f.help ? f.help + '\n' : '') + 'UTC. A year or month means all of it: as a start its first day, as an end its last. ' +
        'Add a time (yyyy-mm-dd hh:mm) only when it matters.' }));
    if (f.kind === 'number') return h('input', Object.assign({ type: 'number', step: 'any', min: g.range ? g.range[0] : undefined,
      max: g.range ? g.range[1] : undefined, placeholder: f.role === 'min' ? 'min' : f.role === 'max' ? 'max' : '' }, common));
    if (f.kind === 'boolean') return h('input', { type: 'checkbox', checked: !!v, 'aria-label': f.name, onChange: function (e) { set(e.target.checked); } });
    return h('input', common);
  }

  function DataScopeEditor(props) {
    var groups = props.groups || [];
    var _v = React.useState(function () { return dataScopeValues(groups, props.scope); }), values = _v[0], setValues = _v[1];
    // Reset the form only when the stored scope or the dimensions really change. Pages pass
    // groups.filter(...), a new array on every render, so depending on the array itself reset
    // the form on every re-render: pressing Save put the stored values back (owner, 2026-11-17).
    var resetKey = JSON.stringify(props.scope || null) + '|' + groups.map(function (g) { return g.id; }).join(',');
    React.useEffect(function () { setValues(dataScopeValues(groups, props.scope)); }, [resetKey]);
    function setField(name, val) { var n = Object.assign({}, values); n[name] = val; setValues(n); }
    function submit(e) {
      e.preventDefault();
      var send = {};
      groups.forEach(function (g) { if (!g.readOnly) g.fields.forEach(function (f) { send[f.name] = values[f.name]; }); });
      props.onSave(send);
    }
    return h('form', { onSubmit: submit, className: 'ds-editor' },
      groups.map(function (g) {
        var tips = g.fields.map(function (f) { return f.help; }).filter(Boolean).join(' ');
        return h('div', { key: g.id, style: box },
          h('div', { style: lab }, g.label, Tip(tips), g.shape === 'timeRange' && h('span', { style: Object.assign({ marginLeft: 6 }, hint) }, 'UTC'),
            g.readOnly && h('span', { style: Object.assign({ marginLeft: 6 }, hint) }, 'kept as it is (written by Egeria services)')),
          g.shape === 'map'
            ? h(MapRows, { field: g.fields[0], value: values[g.fields[0].name], readOnly: g.readOnly, onChange: function (m) { setField(g.fields[0].name, m); } })
            : h('div', { style: row }, g.fields.map(function (f, i) {
                return h(React.Fragment, { key: f.name },
                  i > 0 && (g.shape === 'timeRange' || g.shape === 'bound') && h('span', { style: hint }, g.shape === 'timeRange' ? 'to' : '…'),
                  h(Input, { field: f, group: g, value: values[f.name], onChange: function (val) { setField(f.name, val); } }));
              })));
      }),
      props.error && h('div', { role: 'alert', style: { color: 'var(--err, #f87171)', fontSize: 12, marginBottom: 8 } }, props.error),
      h('div', { style: row },
        h('button', { type: 'submit', disabled: props.busy,
          style: { fontSize: 12, padding: '4px 14px', borderRadius: 4, border: '1px solid var(--accent)', background: 'transparent', color: 'var(--accent)', cursor: 'pointer' } },
          props.busy ? 'Saving…' : (props.saveLabel || 'Save')),
        props.onCancel && h('button', { type: 'button', onClick: props.onCancel, disabled: props.busy,
          style: { fontSize: 12, padding: '4px 10px', borderRadius: 4, border: '1px solid var(--border)', background: 'transparent', color: 'var(--dim)', cursor: 'pointer' } }, 'Cancel'),
        props.onClear && h('button', { type: 'button', onClick: props.onClear, disabled: props.busy, title: props.clearTitle || '',
          style: { fontSize: 12, padding: '4px 10px', borderRadius: 4, border: '1px solid var(--border)', background: 'transparent', color: 'var(--dim)', cursor: 'pointer', marginLeft: 'auto' } }, props.clearLabel || 'Clear')));
  }

  function DataScopeView(props) {
    var groups = props.groups || [], scope = props.scope;
    if (!scope) return h('div', { style: hint }, props.absent || 'No data scope recorded.');
    var shown = groups.filter(function (g) {
      if (g.shape === 'bound') return !_boundIsEmpty(g, scope);
      return g.fields.some(function (f) { var v = scope[f.name]; return v !== undefined && v !== null && v !== '' && !(typeof v === 'object' && !Object.keys(v).length); });
    });
    var known = {};
    groups.forEach(function (g) { g.fields.forEach(function (f) { known[f.name] = true; }); });
    var extra = Object.keys(scope).filter(function (k) { return !known[k] && scope[k] !== null && scope[k] !== '' && typeof scope[k] !== 'object'; });
    if (!shown.length && !extra.length) return h('div', { style: hint }, 'A data scope is recorded but holds no dimensions.');
    return h('table', { style: { fontSize: 12, borderCollapse: 'collapse', width: '100%' } }, h('tbody', null,
      shown.map(function (g) {
        var cell;
        if (g.shape === 'map') {
          var m = scope[g.fields[0].name] || {};
          cell = Object.keys(m).map(function (k) { return k + ': ' + m[k]; }).join('\n');
        } else {
          cell = g.fields.map(function (f) { var v = scope[f.name]; return v === undefined || v === null || v === '' ? '…' : _fmt(f, v); })
            .join(g.shape === 'timeRange' ? ' → ' : g.shape === 'bound' ? ' to ' : ', ');
        }
        return h('tr', { key: g.id, style: { borderBottom: '1px solid var(--border)' } },
          h('td', { style: { padding: '4px 10px 4px 0', color: 'var(--dim)', verticalAlign: 'top', whiteSpace: 'nowrap' } }, g.label),
          h('td', { style: { padding: '4px 0', whiteSpace: 'pre-wrap', wordBreak: 'break-word' } }, cell));
      }),
      extra.map(function (k) {
        return h('tr', { key: k }, h('td', { style: { padding: '4px 10px 4px 0', color: 'var(--dim)' } }, k), h('td', null, String(scope[k])));
      })));
  }

  window.DataScopeEditor = DataScopeEditor;
  window.DataScopeView = DataScopeView;
  window.dataScopeValues = dataScopeValues;
  window.dataScopeFetchDimensions = dataScopeFetchDimensions;
  window.dataScopeDateText = dataScopeDateText;
  window.dataScopePeriodText = dataScopePeriodText;
})();
