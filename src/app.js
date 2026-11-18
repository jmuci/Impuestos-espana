(function () {
  'use strict';

  /* ---------- formato: es-ES, con punto de millares también en 4 cifras ---------- */
  function group(s) { return s.replace(/\B(?=(\d{3})+(?!\d))/g, '.'); }
  function fmtInt(n) { var r = Math.round(n); return (r < 0 ? '−' : '') + group(String(Math.abs(r))); }
  function fmtD(n, d) { var p = Math.abs(n).toFixed(d).split('.'); return (n < 0 && +Math.abs(n).toFixed(d) !== 0 ? '−' : '') + group(p[0]) + (p[1] ? ',' + p[1] : ''); }
  function fmtM(m, d) { return (d ? fmtD(m, d) : fmtInt(m)) + ' M€'; }
  function eur(n) { return fmtInt(n) + ' €'; }
  function pct(p, d) { return fmtD(p, d == null ? 1 : d) + '%'; }
  function roundTo(n, s) { return Math.round(n / s) * s; }

  /* ---------- datos (del paquete de datos; fuentes en las pestañas y en la 6) ---------- */
  var SRC = [
    { key: 'ss',   label: 'Cotizaciones a la Seguridad Social', value: 176918, color: 'c-ss' },
    { key: 'irpf', label: 'IRPF (impuesto sobre la renta)',      value: 142466, color: 'c-irpf' },
    { key: 'iva',  label: 'IVA',                                 value: 99532,  color: 'c-iva' },
    { key: 'is',   label: 'Impuesto sobre Sociedades',           value: 42266,  color: 'c-is' },
    { key: 'ied',  label: 'Impuestos Especiales',                value: 23083,  color: 'c-ied' },
    { key: 'oth',  label: 'Otros impuestos y tasas',             value: 18009,  color: 'c-oth' }
  ];
  var AEAT_TOTAL = 325356, COMBINED = 502274;

  var BR_LABELS = ['Negativa o cero', '0–1.500 €', '1.500–6.000 €', '6.000–12.000 €', '12.000–21.000 €', '21.000–30.000 €', '30.000–60.000 €', '60.000–150.000 €', '150.000–601.000 €', 'Más de 601.000 €'];
  var BR_FILERS = [1531620, 1689995, 3194543, 2226016, 4040146, 4566506, 5796268, 1369675, 194681, 18829];
  var BR_FPCT = [6.22, 6.86, 12.97, 9.04, 16.40, 18.54, 23.54, 5.56, 0.79, 0.08];
  var BR_BASE_EUR = [-584067734, 340934861, 10572136405, 17731654833, 66324001210, 109744014414, 223384600037, 100743046546, 33077781456, 13016775624];
  var BR_BPCT = [-0.10, 0.06, 1.84, 3.09, 11.55, 19.11, 38.89, 17.54, 5.76, 2.27];
  var IRPF_FILERS = 24628279, IRPF_BASE_EUR = 574350877653, IRPF_CUOTA_EUR = 133444424540;

  var MAD = [
    { key: 'm0', label: 'Menos de 6.000 €',  color: 's2', f: 19.45, t: null },
    { key: 'm1', label: '6.000–12.000 €',    color: 's3', f: 7.37,  t: 0.26 },
    { key: 'm2', label: '12.000–21.000 €',   color: 's4', f: 14.40, t: 3.08 },
    { key: 'm3', label: '21.000–30.000 €',   color: 's5', f: 18.48, t: 8.43 },
    { key: 'm4', label: '30.000–60.000 €',   color: 's6', f: 28.84, t: 29.80 },
    { key: 'm5', label: '60.000–150.000 €',  color: 's7', f: 9.55,  t: 27.77 },
    { key: 'm6', label: '150.000–601.000 €', color: 's8', f: 1.70,  t: 16.97 },
    { key: 'm7', label: 'Más de 601.000 €',  color: 's9', f: 0.20,  t: null }
  ];
  var IEF_TOP = 53.96;

  var REG = [
    ['mad', 'Madrid', 33594, 7113886, 'c-irpf'],
    ['cat', 'Cataluña', 31374, 8124126, 'c-ss'],
    ['and', 'Andalucía', 23420, 8676713, 'c-iva'],
    ['val', 'Comunitat Valenciana', 16622, 5425182, 'c-is'],
    ['gal', 'Galicia', 8274, 2714741, 'g1'],
    ['cyl', 'Castilla y León', 7874, 2401221, 'g2'],
    ['clm', 'Castilla-La Mancha', 5687, 2126378, 'g3'],
    ['bal', 'Baleares', 4952, 1249844, 'g1'],
    ['ara', 'Aragón', 4884, 1364621, 'g2'],
    ['mur', 'Murcia', 4299, 1586989, 'g3'],
    ['cnr', 'Canarias', 3462, 2258866, 'g1'],
    ['ast', 'Asturias', 3295, 1015128, 'g2'],
    ['ext', 'Extremadura', 2637, 1053345, 'g3'],
    ['can', 'Cantabria', 2061, 593623, 'g1'],
    ['rio', 'La Rioja', 1075, 326803, 'g2']
  ];
  var REG_TOTAL_SRC = 153509;
  var AVG15 = REG.reduce(function (s, r) { return s + r[2]; }, 0) * 1e6 / REG.reduce(function (s, r) { return s + r[3]; }, 0);

  /* Territorios forales, cierre 2025 (M€). Las cifras del País Vasco salen al euro de la nota oficial. */
  var NAV_TOTAL = 5865.7;
  var NAV_OTH_IND = Math.round((NAV_TOTAL - (2195.9 + 1972.7 + 622.7 + 541.2 + 207.2 + 138.4 + 33.4)) * 10) / 10;   // por diferencia
  var FORAL = {
    pv: {
      name: 'País Vasco', pop: 2242343, popApprox: false, total: 20324.5,
      growth: '+11% sobre 2024 (2024 lastrado por devoluciones a mutualistas)',
      pieSub: 'Recaudación de las tres Diputaciones Forales (Álava, Bizkaia y Gipuzkoa), cierre 2025.',
      items: [
        { key: 'irpf', label: 'IRPF', value: 7960.502, color: 'c-irpf', type: 'oficial' },
        { key: 'iva',  label: 'IVA (incluye ajustes con el Estado)', value: 7790.258, color: 'c-iva', type: 'oficial' },
        { key: 'ied',  label: 'Impuestos Especiales (incluye ajustes)', value: 1590.785, color: 'c-ied', type: 'oficial' },
        { key: 'is',   label: 'Sociedades', value: 1438.397, color: 'c-is', type: 'oficial' },
        { key: 'oth',  label: 'Resto: Patrimonio, Sucesiones, ITP-AJD, No Residentes, tasas…', value: 1544.560, color: 'c-oth', type: 'oficial' }
      ],
      eq: { irpf: 7960.502, iva: 7790.258, ied: 1590.785, rest: 1544.560 },
      flow: 1464.7, flowDec: 1,
      flowStat: 'Cupo al Estado, 2025', flowSmall: 'provisional · 7,2% de lo recaudado',
      flowLabel: 'Cupo al Estado 2025 (provisional)',
      keepLabel: 'Se queda en el País Vasco (sanidad, educación, policía, ayuntamientos…)',
      flowSub: 'El cupo provisional de 2025 frente a lo que se queda en el territorio.',
      seriesTitle: 'Cupo al Estado, por año (M€)',
      series: [
        ['2023', '1.676,0', 'definitivo', 'oficial'],
        ['2024', '1.735,6', 'definitivo (provisional: 1.562,0)', 'oficial'],
        ['2025', '1.464,7', 'provisional', 'oficial'],
        ['2025, liquidación prevista', '≈1.700 o ≈1.407', 'dos previsiones de prensa incompatibles', 'prensa'],
        ['2026', '1.590', 'provisional, proyecto de presupuestos', 'prensa']
      ],
      seriesNote: 'Las Diputaciones transfirieron 13.770,6 M€ al Gobierno Vasco en 2025: es un reparto interno vasco, que no hay que confundir con el cupo. El «líquido a pagar» que difunde Hacienda es neto de compensaciones.'
    },
    nav: {
      name: 'Navarra', pop: 683900, popApprox: true, total: NAV_TOTAL,
      growth: '+8% sobre 2024 (5.433 M€)',
      pieSub: 'Recaudación líquida de la Hacienda Foral de Navarra, cierre 2025.',
      items: [
        { key: 'irpf', label: 'IRPF', value: 2195.9, color: 'c-irpf', type: 'oficial' },
        { key: 'iva',  label: 'IVA (gestión directa 655,5 + ajuste con el Estado 1.317,2)', value: 1972.7, color: 'c-iva', type: 'oficial' },
        { key: 'ied',  label: 'Impuestos Especiales (gestión directa 506,5 + ajustes 116,2)', value: 622.7, color: 'c-ied', type: 'oficial' },
        { key: 'is',   label: 'Sociedades', value: 541.2, color: 'c-is', type: 'oficial' },
        { key: 'od',   label: 'Otros directos: Patrimonio, Sucesiones, No Residentes, Grandes Fortunas', value: 207.2, color: 'g1', type: 'inferido' },
        { key: 'oi',   label: 'Otros indirectos: ITP-AJD, primas de seguros…', value: NAV_OTH_IND, color: 'g2', type: 'inferido' },
        { key: 'ret',  label: 'Ajuste con el Estado por retenciones', value: 138.4, color: 's6', type: 'oficial' },
        { key: 'fee',  label: 'Tasas y otros ingresos', value: 33.4, color: 'g3', type: 'oficial' }
      ],
      eq: { irpf: 2195.9, iva: 1972.7, ied: 622.7, rest: 207.2 + NAV_OTH_IND },
      flow: 874, flowDec: 0,
      flowStat: 'Aportación al Estado, 2025', flowSmall: 'presupuestada · 14,9% de lo recaudado',
      flowLabel: 'Aportación al Estado 2025 (presupuestada)',
      keepLabel: 'Se queda en Navarra (sanidad, educación, policía, ayuntamientos…)',
      flowSub: 'La aportación presupuestada de 2025 frente a lo que se queda en el territorio. Con la previsión de 777,9 M€ sería el 13,3%.',
      seriesTitle: 'Aportación de Navarra al Estado, por año (M€)',
      series: [
        ['2020, año base del quinquenio 2020-24', '510,2 (neta de ajuste por retenciones: 431,3)', 'definitivo', 'oficial'],
        ['2024', '777,9 (neta: 653,4)', 'provisional', 'oficial'],
        ['2024, ejecución presupuestaria', '832,2', 'puede incluir regularizaciones', 'prensa'],
        ['2025', '874 presupuestados (previsión: 777,9)', 'provisional', 'oficial'],
        ['2026', '932 presupuestados', 'provisional', 'oficial']
      ],
      seriesNote: 'El acuerdo del quinquenio 2025-2029 sigue sin cerrarse, según la AIReF (julio de 2026); por eso las aportaciones de 2025 son provisionales.'
    }
  };

  /* Capacidad «equivalente a régimen común»: 50% IRPF + 50% IVA + 58% Especiales + r × resto (r entre 0,6 y 0,8). Sin Sociedades. */
  function eqCap(T, r) { return 0.5 * T.eq.irpf + 0.5 * T.eq.iva + 0.58 * T.eq.ied + r * T.eq.rest; }
  function eqPc(T, r) { return eqCap(T, r) * 1e6 / T.pop; }

  var CLAIM = 10000;           // cifra del partido, M€
  var IRPF_AEAT = 142466;      // M€

  /* ---------- utilidades ---------- */
  var NS = 'http://www.w3.org/2000/svg';
  function svgEl(tag, attrs) { var e = document.createElementNS(NS, tag); for (var k in attrs) e.setAttribute(k, attrs[k]); return e; }
  function h(tag, attrs) {
    var e = document.createElement(tag);
    if (attrs) for (var k in attrs) {
      if (k === 'class') e.className = attrs[k];
      else if (k === 'text') e.textContent = attrs[k];
      else e.setAttribute(k, attrs[k]);
    }
    for (var i = 2; i < arguments.length; i++) {
      var c = arguments[i];
      if (c == null) continue;
      if (Array.isArray(c)) c.forEach(function (x) { if (x != null) e.append(x.nodeType ? x : document.createTextNode(x)); });
      else e.append(c.nodeType ? c : document.createTextNode(c));
    }
    return e;
  }
  function $(s) { return document.querySelector(s); }
  function cssVar(name) { return getComputedStyle(document.documentElement).getPropertyValue('--' + name).trim(); }
  function textOn(colorName) {
    var c = cssVar(colorName), m = /^#([0-9a-f]{6})$/i.exec(c);
    if (!m) return '#fff';
    var n = parseInt(m[1], 16), r = (n >> 16) & 255, g = (n >> 8) & 255, b = n & 255;
    var L = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255;
    return L > 0.58 ? '#12161c' : '#ffffff';
  }
  var TAGS = { oficial: 'oficial', prensa: 'prensa', academica: 'académica', estimado: 'estimado', inferido: 'inferido', partido: 'cifra del partido' };
  function tag(t) { return h('span', { class: 'tag t-' + t }, TAGS[t] || t); }

  /* selección compartida por los gráficos y tablas de una vista */
  function makeGroup() {
    var subs = [], pinned = null;
    var api = {
      add: function (fn) { subs.push(fn); fn(pinned); },
      show: function (k) { subs.forEach(function (fn) { fn(k); }); },
      enter: function (k) { api.show(k); },
      leave: function () { api.show(pinned); },
      click: function (k) { pinned = pinned === k ? null : k; api.show(pinned); },
      bindRows: function (root) {
        var rows = root.querySelectorAll('tr[data-key]');
        rows.forEach(function (tr) {
          var k = tr.getAttribute('data-key');
          tr.tabIndex = 0;
          tr.addEventListener('pointerenter', function () { api.enter(k); });
          tr.addEventListener('pointerleave', function () { api.leave(); });
          tr.addEventListener('click', function () { api.click(k); });
          tr.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); api.click(k); } });
        });
        api.add(function (k) { rows.forEach(function (tr) { tr.classList.toggle('on', tr.getAttribute('data-key') === k); }); });
      }
    };
    return api;
  }

  /* gráfico circular: items = [{key,label,value,color,text}], o = {aria,totalMain,totalSub,grp} */
  function makePie(host, items, o) {
    host.textContent = '';
    var vis = items.filter(function (i) { return i.value > 0; });
    var sum = vis.reduce(function (s, i) { return s + i.value; }, 0);
    var wrap = h('div', { class: 'pie' });
    var readout = h('div', { class: 'readout', 'aria-live': 'polite' });
    var svg = svgEl('svg', { viewBox: '0 0 320 320', role: 'group', 'aria-label': o.aria });
    var cx = 160, cy = 160, r = 146, a = -Math.PI / 2, nodes = {};
    vis.forEach(function (it) {
      var f = it.value / sum, b = a + f * 2 * Math.PI, mid = (a + b) / 2, d;
      if (f > 0.9999) d = 'M ' + cx + ' ' + (cy - r) + ' A ' + r + ' ' + r + ' 0 1 1 ' + (cx - 0.01) + ' ' + (cy - r) + ' Z';
      else {
        var x1 = cx + r * Math.cos(a), y1 = cy + r * Math.sin(a), x2 = cx + r * Math.cos(b), y2 = cy + r * Math.sin(b);
        d = 'M ' + cx + ' ' + cy + ' L ' + x1.toFixed(2) + ' ' + y1.toFixed(2) + ' A ' + r + ' ' + r + ' 0 ' + (f > 0.5 ? 1 : 0) + ' 1 ' + x2.toFixed(2) + ' ' + y2.toFixed(2) + ' Z';
      }
      var g = svgEl('g', { class: 'sg' });
      g.style.setProperty('--dx', (Math.cos(mid) * 7).toFixed(1) + 'px');
      g.style.setProperty('--dy', (Math.sin(mid) * 7).toFixed(1) + 'px');
      var p = svgEl('path', { d: d, tabindex: '0', role: 'img', 'aria-label': it.label + ': ' + it.text });
      p.style.fill = 'var(--' + it.color + ')';
      g.append(p);
      if (f >= 0.07) {
        var t = svgEl('text', { x: (cx + 0.64 * r * Math.cos(mid)).toFixed(1), y: (cy + 0.64 * r * Math.sin(mid) + 4).toFixed(1), 'text-anchor': 'middle', 'class': 'slice-label' });
        t.textContent = pct(f * 100);
        t.style.fill = textOn(it.color);
        g.append(t);
      }
      p.addEventListener('pointerenter', function () { o.grp.enter(it.key); });
      p.addEventListener('pointerleave', function () { o.grp.leave(); });
      p.addEventListener('focus', function () { o.grp.enter(it.key); });
      p.addEventListener('blur', function () { o.grp.leave(); });
      p.addEventListener('click', function () { o.grp.click(it.key); });
      p.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); o.grp.click(it.key); } });
      svg.append(g);
      nodes[it.key] = { g: g, it: it };
      a = b;
    });
    wrap.append(svg);
    host.append(readout, wrap);
    o.grp.add(function (k) {
      var n = k != null ? nodes[k] : null;
      Object.keys(nodes).forEach(function (kk) { nodes[kk].g.classList.toggle('on', n && kk === k); });
      wrap.classList.toggle('has-active', !!n);
      readout.textContent = '';
      if (n) {
        var sw = h('span', { class: 'r-sw' }); sw.style.background = 'var(--' + n.it.color + ')';
        readout.append(h('div', { class: 'r-main' }, n.it.text), h('div', { class: 'r-sub' }, sw, n.it.label));
      } else {
        readout.append(h('div', { class: 'r-main' }, o.totalMain), h('div', { class: 'r-sub' }, o.totalSub));
      }
    });
  }

  /* leyenda / tabla de datos; cols = [{h, get(item), num}]; get puede devolver texto, un nodo o {na} */
  function makeTable(items, cols, foot) {
    var t = h('table', { class: 'legend' });
    var tr = h('tr');
    cols.forEach(function (c) { tr.append(h('th', { class: c.num ? 'num' : '', scope: 'col' }, c.h)); });
    t.append(h('thead', null, tr));
    var tb = h('tbody');
    items.forEach(function (it) {
      var row = h('tr', { 'data-key': it.key });
      cols.forEach(function (c, ci) {
        var td = h('td', { class: c.num ? 'num' : '' });
        if (ci === 0) {
          var sw = h('span', { class: 'sw' + (it.value > 0 ? '' : ' none') });
          if (it.value > 0) sw.style.background = 'var(--' + it.color + ')';
          td.append(sw);
        }
        var v = c.get(it);
        if (v && v.nodeType) td.append(v);
        else if (v && v.na) td.append(h('span', { class: 'na' }, v.na));
        else td.append(v == null ? '' : String(v));
        row.append(td);
      });
      tb.append(row);
    });
    t.append(tb);
    if (foot) {
      var fr = h('tr');
      foot.forEach(function (c, i) { fr.append(h('td', { class: cols[i].num ? 'num' : '' }, c)); });
      t.append(h('tfoot', null, fr));
    }
    return t;
  }

  /* tabla simple sin selección: heads = [texto], rows = [[celda…]] */
  function plainTable(heads, rows) {
    var t = h('table', { class: 'plain' });
    var tr = h('tr');
    heads.forEach(function (x) { tr.append(h('th', { scope: 'col' }, x)); });
    t.append(h('thead', null, tr));
    var tb = h('tbody');
    rows.forEach(function (r) {
      var row = h('tr');
      r.forEach(function (c) { row.append(h('td', null, c)); });
      tb.append(row);
    });
    t.append(tb);
    return h('div', { class: 'tbl-wrap' }, t);
  }

  function stat(label, value, small) {
    return h('div', { class: 'stat' }, h('dt', null, label), h('dd', null, value, small ? h('small', null, small) : null));
  }

  var state = { rev: 'all', br: 'nat', rg: 'off', fo: 'pv', erosion: 0, rule: 'none' };

  /* ---------- pestaña 1 ---------- */
  function renderRevenue() {
    var all = state.rev === 'all';
    var items = SRC.filter(function (s) { return all || s.key !== 'ss'; }).map(function (s) { return Object.assign({}, s); });
    var total = all ? COMBINED : AEAT_TOTAL;
    items.forEach(function (i) { i.text = fmtM(i.value) + ' · ' + pct(i.value / total * 100); });
    $('#rev-finding').textContent = all
      ? 'La Seguridad Social y el IRPF aportan el 64% de los 502.274 M€ que recauda España.'
      : 'El IRPF y el IVA suman el 74% de los 325.356 M€ en impuestos.';
    var host = $('#rev-card'); host.textContent = '';
    var pieHost = h('div'), tblHost = h('div', { class: 'tbl-wrap' });
    host.append(pieHost, tblHost);
    var grp = makeGroup();
    makePie(pieHost, items, { aria: 'Gráfico circular de los ingresos públicos españoles por fuente, 2025', totalMain: fmtM(total), totalSub: all ? 'Impuestos más Seguridad Social, 2025' : 'Impuestos gestionados por la AEAT, 2025', grp: grp });
    var tbl = makeTable(items, [
      { h: 'Fuente', get: function (i) { return i.label; } },
      { h: 'M€', num: true, get: function (i) { return fmtInt(i.value); } },
      { h: '% del total', num: true, get: function (i) { return pct(i.value / total * 100); } }
    ], ['Total', fmtInt(total), '100%']);
    tblHost.append(tbl);
    grp.bindRows(tblHost);
  }

  /* ---------- pestaña 2 ---------- */
  function renderBrackets() {
    var nat = state.br === 'nat';
    var stats = $('#br-stats'); stats.textContent = '';
    if (nat) {
      stats.append(
        stat('Declarantes del IRPF', fmtD(IRPF_FILERS / 1e6, 1) + ' M', 'territorio de régimen común, declaraciones de 2024'),
        stat('Base liquidable', fmtM(IRPF_BASE_EUR / 1e6), 'base liquidable general'),
        stat('Cuota líquida incrementada', fmtM(IRPF_CUOTA_EUR / 1e6), 'unos 67.900 M€ para el Estado y 65.500 M€ para las comunidades'),
        stat('Declarantes con más de 60.000 €', '6,4%', 'acumulan el 25,6% de la base liquidable')
      );
    } else {
      stats.append(
        stat('Declarantes de Madrid con más de 60.000 €', '11,5%', 'de las declaraciones individuales de Madrid'),
        stat('Su parte del IRPF de Madrid', '≥ 44,7%', 'sin contar el tramo superior, que no se publica'),
        stat('Declarantes de Madrid con menos de 30.000 €', '59,7%', 'pagan al menos el 11,8% del IRPF de Madrid (celda de menos de 6.000 € oculta)'),
        stat('Oculto por secreto estadístico', '13,7%', 'del IRPF de Madrid: menos de 6.000 € y más de 601.000 €')
      );
    }
    var pies = $('#br-pies'); pies.textContent = '';
    var cardA = h('div', { class: 'card' }), cardB = h('div', { class: 'card' });
    var hostA = h('div'), hostB = h('div');
    pies.append(cardA, cardB);
    var grp = makeGroup(), items, tblCols, foot = null;

    if (nat) {
      items = BR_LABELS.map(function (lb, i) {
        return { key: 'b' + i, label: lb, color: 's' + i, value: BR_FILERS[i], filers: BR_FILERS[i], fpct: BR_FPCT[i], base: BR_BASE_EUR[i], bpct: BR_BPCT[i] };
      });
      cardA.append(h('h3', null, 'Parte de los declarantes'), h('p', { class: 'sub' }, 'Cada porción es un tramo de renta anual.'), hostA);
      cardB.append(h('h3', null, 'Parte de la base liquidable'), h('p', { class: 'sub' }, 'Sustituto de la cuota pagada. El tramo negativo no tiene porción.'), hostB);
      var itA = items.map(function (i) { return Object.assign({}, i, { value: i.filers, text: fmtInt(i.filers) + ' declarantes · ' + pct(i.fpct, 2) }); });
      var itB = items.map(function (i) { return Object.assign({}, i, { value: i.base, text: fmtM(i.base / 1e6) + ' · ' + pct(i.bpct, 2) + ' de la base' }); });
      makePie(hostA, itA, { aria: 'Gráfico circular de los declarantes del IRPF por tramo de renta', totalMain: fmtD(IRPF_FILERS / 1e6, 1) + ' M declarantes', totalSub: 'España, régimen común, 2024', grp: grp });
      makePie(hostB, itB, { aria: 'Gráfico circular de la base liquidable del IRPF por tramo de renta', totalMain: fmtM(IRPF_BASE_EUR / 1e6), totalSub: 'Base liquidable, 2024', grp: grp });
      tblCols = [
        { h: 'Tramo (renta)', get: function (i) { return i.label; } },
        { h: 'Declarantes', num: true, get: function (i) { return fmtInt(i.filers); } },
        { h: '% de declarantes', num: true, get: function (i) { return pct(i.fpct, 2); } },
        { h: 'Base liquidable (M€)', num: true, get: function (i) { return fmtInt(i.base / 1e6); } },
        { h: '% de la base', num: true, get: function (i) { return pct(i.bpct, 2); } }
      ];
      foot = ['Total', fmtInt(IRPF_FILERS), '100%', fmtInt(IRPF_BASE_EUR / 1e6), '100%'];
    } else {
      var tSum = MAD.reduce(function (s, m) { return s + (m.t || 0); }, 0);
      var rest = +(100 - tSum).toFixed(2);
      items = MAD.map(function (m) { return { key: m.key, label: m.label, color: m.color, value: m.f, f: m.f, t: m.t }; });
      cardA.append(h('h3', null, 'Madrid: parte de los declarantes'), h('p', { class: 'sub' }, 'Declaraciones individuales por renta anual.'), hostA);
      cardB.append(h('h3', null, 'Madrid: parte de la cuota pagada'), h('p', { class: 'sub' }, 'Cuota líquida incrementada total. En gris, el resto no publicado.'), hostB);
      var mA = items.map(function (i) { return Object.assign({}, i, { value: i.f, text: pct(i.f, 2) + ' de los declarantes' }); });
      var mB = items.filter(function (i) { return i.t != null; }).map(function (i) { return Object.assign({}, i, { value: i.t, text: pct(i.t, 2) + ' del IRPF' }); });
      mB.push({ key: 'mx', label: 'Menos de 6.000 € y más de 601.000 € (no publicado)', color: 'c-oth', value: rest, text: pct(rest, 2) + ' del IRPF, oculto' });
      makePie(hostA, mA, { aria: 'Gráfico circular de los declarantes del IRPF de Madrid por tramo de renta', totalMain: '100%', totalSub: 'Declaraciones individuales de Madrid, 2024', grp: grp });
      makePie(hostB, mB, { aria: 'Gráfico circular del IRPF pagado en Madrid por tramo de renta', totalMain: '100%', totalSub: 'IRPF pagado en Madrid, 2024', grp: grp });
      tblCols = [
        { h: 'Tramo (renta)', get: function (i) { return i.label; } },
        { h: '% de declarantes de Madrid', num: true, get: function (i) { return i.f != null ? pct(i.f, 2) : { na: 'n/d' }; } },
        { h: '% del IRPF de Madrid', num: true, get: function (i) { return i.key === 'mx' ? pct(rest, 2) + ' juntos' : (i.t != null ? pct(i.t, 2) : { na: 'no publicado' }); } }
      ];
      items.push({ key: 'mx', label: 'Resto no publicado (menos de 6.000 € y más de 601.000 €)', color: 'c-oth', value: rest, f: null, t: null });
    }
    var tHost = $('#br-table'); tHost.textContent = '';
    tHost.append(makeTable(items, tblCols, foot));
    grp.bindRows(tHost);

    // decil superior (IEF)
    var ief = $('#ief-card'); ief.textContent = '';
    var pH = h('div'), tH = h('div'), g2 = makeGroup();
    ief.append(pH, tH);
    var iItems = [
      { key: 'top', label: 'El 10% de contribuyentes con más renta', color: 'c-irpf', value: IEF_TOP, text: pct(IEF_TOP, 2) + ' del IRPF' },
      { key: 'rest', label: 'El otro 90%', color: 'c-ss', value: +(100 - IEF_TOP).toFixed(2), text: pct(100 - IEF_TOP, 2) + ' del IRPF' }
    ];
    makePie(pH, iItems, { aria: 'Gráfico circular: parte de la cuota del IRPF que paga el decil superior', totalMain: 'Todo el país', totalSub: 'Parte de la cuota real del IRPF, por decil de renta', grp: g2 });
    tH.append(h('h3', null, 'Todo el país, por deciles'), h('p', { class: 'sub' }, 'El Instituto de Estudios Fiscales calcula que el decil de mayor renta soporta el 53,96% de la cuota real del IRPF. El otro 90% es el resto (100 menos 53,96).'));
    var tb = makeTable(iItems, [
      { h: 'Grupo', get: function (i) { return i.label; } },
      { h: 'Parte del IRPF', num: true, get: function (i) { return pct(i.value, 2); } }
    ]);
    var w = h('div', { class: 'tbl-wrap', style: 'margin-top:12px' }, tb);
    tH.append(w);
    g2.bindRows(w);
  }

  /* ---------- pestaña 3 ---------- */
  function renderRegions() {
    var est = state.rg === 'est';
    var list = REG.map(function (r) { return { key: r[0], label: r[1], cap: r[2], pop: r[3], color: r[4], est: false }; });
    if (est) {
      ['pv', 'nav'].forEach(function (k) {
        var T = FORAL[k];
        list.push({ key: k, label: T.name + ' (estimado)', cap: roundTo(eqCap(T, 0.7), 100), pop: T.pop, color: k === 'pv' ? 'c-pv' : 'c-nav', est: true });
      });
    }
    var capTot = REG_TOTAL_SRC + list.filter(function (i) { return i.est; }).reduce(function (s, i) { return s + i.cap; }, 0);
    var popTot = list.reduce(function (s, i) { return s + i.pop; }, 0);
    var items = list.map(function (i) {
      var pc = i.est ? roundTo(i.cap * 1e6 / i.pop, 50) : i.cap * 1e6 / i.pop;
      return Object.assign({}, i, { pc: pc, idx: pc / AVG15 * 100, capPct: i.cap / capTot * 100, popPct: i.pop / popTot * 100 });
    });
    var mad = items.filter(function (i) { return i.key === 'mad'; })[0];
    $('#rg-finding').textContent = est
      ? 'Con una estimación propia, País Vasco y Navarra quedarían por encima de la media por habitante.'
      : 'Madrid recauda un ' + Math.round(mad.idx - 100) + '% más de impuestos cedidos por habitante que la media autonómica.';

    var pies = $('#rg-pies'); pies.textContent = '';
    var cA = h('div', { class: 'card' }), cB = h('div', { class: 'card' }), hA = h('div'), hB = h('div');
    cA.append(h('h3', null, 'Parte del impuesto recaudado'), h('p', { class: 'sub' }, est ? 'Capacidad tributaria por comunidad: 15 de régimen común (oficial) más País Vasco y Navarra (estimado).' : 'Capacidad tributaria por comunidad, 15 comunidades de régimen común.'), hA);
    cB.append(h('h3', null, 'Euros por habitante'), h('p', { class: 'sub' }, 'El tamaño de la porción son euros por persona; el conjunto no tiene significado.'), hB);
    pies.append(cA, cB);
    var grp = makeGroup();
    var approx = function (i) { return i.est ? '≈' : ''; };
    var itA = items.slice().sort(function (a, b) { return b.cap - a.cap; }).map(function (i) { return Object.assign({}, i, { value: i.cap, text: approx(i) + fmtM(i.cap) + ' · ' + pct(i.capPct) + ' de la capacidad' }); });
    var itB = items.slice().sort(function (a, b) { return b.pc - a.pc; }).map(function (i) { return Object.assign({}, i, { value: i.pc, text: approx(i) + eur(i.pc) + ' por habitante · ' + Math.round(i.idx) + '% de la media' }); });
    makePie(hA, itA, { aria: 'Gráfico circular de la capacidad tributaria por comunidad', totalMain: fmtM(capTot), totalSub: est ? 'Capacidad tributaria, 17 territorios, 2024' : 'Capacidad tributaria, 15 comunidades, 2024', grp: grp });
    makePie(hB, itB, { aria: 'Gráfico circular de la capacidad tributaria por habitante y comunidad', totalMain: eur(AVG15), totalSub: 'Media de las 15 comunidades de régimen común', grp: grp });
    var cols = [
      { h: 'Comunidad', get: function (i) { return i.label; } },
      { h: 'Capacidad (M€)', num: true, get: function (i) { return approx(i) + fmtInt(i.cap); } },
      { h: '% de la capacidad', num: true, get: function (i) { return pct(i.capPct); } },
      { h: 'Habitantes', num: true, get: function (i) { return approx(i) + fmtInt(i.pop); } },
      { h: '% de habitantes', num: true, get: function (i) { return pct(i.popPct); } },
      { h: '€ por habitante', num: true, get: function (i) { return approx(i) + fmtInt(i.pc); } },
      { h: 'Índice (media = 100)', num: true, get: function (i) { return approx(i) + Math.round(i.idx); } }
    ];
    if (est) cols.push({ h: 'Tipo', get: function (i) { return tag(i.est ? 'estimado' : 'oficial'); } });
    var tHost = $('#rg-table'); tHost.textContent = '';
    var foot = [est ? '17 territorios' : '15 comunidades', fmtInt(capTot), '100%', fmtInt(popTot), '100%', est ? '' : fmtInt(AVG15), est ? '' : '100'];
    if (est) foot.push('');
    tHost.append(makeTable(itA, cols, foot));
    grp.bindRows(tHost);
  }

  /* ---------- pestaña 4 ---------- */
  function renderForal() {
    var T = FORAL[state.fo], total = T.total;
    var eqC = eqCap(T, 0.7), eqP = eqPc(T, 0.7);
    var pcLabel = (T.popApprox ? '≈' : '') + eur(total * 1e6 / T.pop);

    var stats = $('#fo-stats'); stats.textContent = '';
    stats.append(
      stat('Recaudación foral, 2025', fmtM(total, 1), T.growth),
      stat('Por habitante', pcLabel, 'bruta: incluye lo que en régimen común es del Estado; no comparable con 3.335 €'),
      stat(T.flowStat, fmtM(T.flow, T.flowDec), T.flowSmall + ' · ≈' + eur(T.flow * 1e6 / T.pop) + ' por habitante'),
      stat('Capacidad equivalente por habitante', '≈' + eur(roundTo(eqP, 50)), 'estimado, ±10% · media de régimen común: ' + eur(AVG15))
    );

    var pies = $('#fo-pies'); pies.textContent = '';
    var cA = h('div', { class: 'card' }), cB = h('div', { class: 'card' }), hA = h('div'), hB = h('div');
    cA.append(h('h3', null, T.name + ': qué se recauda'), h('p', { class: 'sub' }, T.pieSub), hA);
    cB.append(h('h3', null, T.name + ': cuánto va al Estado'), h('p', { class: 'sub' }, T.flowSub), hB);
    pies.append(cA, cB);
    var gA = makeGroup(), gB = makeGroup();

    var itA = T.items.map(function (i) { return Object.assign({}, i, { text: fmtM(i.value, 1) + ' · ' + pct(i.value / total * 100) }); });
    makePie(hA, itA, { aria: 'Gráfico circular de la recaudación foral de ' + T.name + ' por impuesto, 2025', totalMain: fmtM(total, 1), totalSub: 'Recaudación foral bruta, 2025', grp: gA });
    var lgA = h('div', { class: 'tbl-wrap', style: 'margin-top:12px' }, makeTable(itA, [
      { h: 'Impuesto', get: function (i) { return i.label; } },
      { h: 'M€', num: true, get: function (i) { return fmtD(i.value, 1); } },
      { h: '%', num: true, get: function (i) { return pct(i.value / total * 100); } },
      { h: '€/hab.', num: true, get: function (i) { return (T.popApprox ? '≈' : '') + fmtInt(i.value * 1e6 / T.pop); } },
      { h: 'Tipo', get: function (i) { return tag(i.type); } }
    ], ['Total', fmtD(total, 1), '100%', (T.popApprox ? '≈' : '') + fmtInt(total * 1e6 / T.pop), tag('oficial')]));
    cA.append(lgA); gA.bindRows(lgA);

    var keep = +(total - T.flow).toFixed(1);
    var itB = [
      { key: 'flow', label: T.flowLabel, color: 's8', value: T.flow, text: fmtM(T.flow, T.flowDec ? 1 : 0) + ' · ' + pct(T.flow / total * 100), type: 'oficial' },
      { key: 'keep', label: T.keepLabel, color: 's3', value: keep, text: fmtM(keep, 1) + ' · ' + pct(keep / total * 100), type: 'inferido' }
    ];
    makePie(hB, itB, { aria: 'Gráfico circular: parte de la recaudación foral de ' + T.name + ' que va al Estado', totalMain: pct(T.flow / total * 100) + ' al Estado', totalSub: 'Sobre la recaudación foral bruta de 2025', grp: gB });
    var lgB = h('div', { class: 'tbl-wrap', style: 'margin-top:12px' }, makeTable(itB, [
      { h: 'Destino', get: function (i) { return i.label; } },
      { h: 'M€', num: true, get: function (i) { return fmtD(i.value, 1); } },
      { h: '%', num: true, get: function (i) { return pct(i.value / total * 100); } },
      { h: 'Tipo', get: function (i) { return tag(i.type); } }
    ], ['Total', fmtD(total, 1), '100%', '']));
    cB.append(lgB); gB.bindRows(lgB);

    var ser = $('#fo-series'); ser.textContent = '';
    ser.append(h('h3', null, T.seriesTitle), plainTable(['Año', 'Importe (M€)', 'Estado', 'Tipo'], T.series.map(function (r) { return [r[0], r[1], r[2], tag(r[3])]; })), h('p', { class: 'sub', style: 'margin-top:10px' }, T.seriesNote));

    renderForalBrackets();
    renderForalCompare();
  }

  function renderForalBrackets() {
    var host = $('#fo-brackets'); host.textContent = '';
    if (state.fo === 'pv') {
      host.append(h('div', { class: 'card' }, h('h3', null, 'País Vasco: IRPF por tramos'), h('div', { class: 'empty', style: 'margin-top:10px;min-height:120px' }, 'No hay una tabla consolidada del IRPF por tramos para toda la comunidad. Bizkaia publica la suya en Open Data Bizkaia, pero no se pudo descargar; Álava y Gipuzkoa no se han verificado. Es una laguna, no un cero.')));
      return;
    }
    var rows = [
      { key: 'a', label: 'Más de 60.000 € de base', color: 'c-irpf', value: 8.6, f: 8.6, t: 46, tf: 'prensa', tt: 'prensa' },
      { key: 'b', label: '24.000–60.000 € («clases medias»)', color: 'c-ss', value: 37, f: 37, t: 45, tf: 'prensa', tt: 'prensa' },
      { key: 'c', label: 'Menos de 24.000 € (resto)', color: 'c-oth', value: 54.4, f: 54.4, t: 9, tf: 'inferido', tt: 'inferido' }
    ];
    var grp = makeGroup();
    var cA = h('div', { class: 'card' }), cB = h('div', { class: 'card' }), hA = h('div'), hB = h('div');
    cA.append(h('h3', null, 'Navarra: parte de los declarantes'), h('p', { class: 'sub' }, 'IRPF, tramos de base, 2019.'), hA);
    cB.append(h('h3', null, 'Navarra: parte de la cuota'), h('p', { class: 'sub' }, 'Cuota del IRPF por los mismos tramos, 2019.'), hB);
    var itA = rows.map(function (r) { return Object.assign({}, r, { value: r.f, text: (r.key === 'c' ? '≈' : '') + pct(r.f) + ' de los declarantes' }); });
    var itB = rows.map(function (r) { return Object.assign({}, r, { value: r.t, text: '≈' + pct(r.t, 0) + ' de la cuota' }); });
    makePie(hA, itA, { aria: 'Gráfico circular de los declarantes del IRPF de Navarra por tramo de base, 2019', totalMain: '100%', totalSub: 'Declarantes, Navarra, 2019', grp: grp });
    makePie(hB, itB, { aria: 'Gráfico circular de la cuota del IRPF de Navarra por tramo de base, 2019', totalMain: '100%', totalSub: 'Cuota del IRPF, Navarra, 2019', grp: grp });
    var lg = h('div', { class: 'tbl-wrap', style: 'margin-top:12px' }, makeTable(rows, [
      { h: 'Tramo de base', get: function (i) { return i.label; } },
      { h: '% de declarantes', num: true, get: function (i) { return (i.key === 'c' ? '≈' : '') + pct(i.f); } },
      { h: '% de la cuota', num: true, get: function (i) { return '≈' + pct(i.t, 0); } },
      { h: 'Tipo', get: function (i) { return tag(i.tf); } }
    ]));
    cB.append(lg); grp.bindRows(lg);
    host.append(
      h('h3', { style: 'margin:0 0 10px;font:700 20px/1.2 var(--font-display)' }, 'Navarra: IRPF por tramos'),
      h('div', { class: 'pair' }, cA, cB),
      h('ul', { class: 'notes' },
        h('li', null, 'Estadística de la Hacienda Foral recogida por la prensa. El tramo «resto» se deduce por diferencia (100 menos las dos cifras publicadas). Se parte de declarantes y cuota del mismo año (2019).'),
        h('li', null, 'Dentro del tramo de más de 60.000 €: los de más de 120.000 € (1,1–1,2% de los declarantes) pagan el 17–17,7% de la cuota (2019-2020); los de 90.000–120.000 € (1,5%) pagan el 9,3% (2020). En 2026 la prensa sitúa en unas 52.000 las declaraciones de más de 60.000 € y dice que aportan la mayoría del impuesto; en la campaña de 2023 hubo 502.522 contribuyentes.'),
        h('li', null, 'Referencia de régimen común (AEAT, 2023): los 14.738 declarantes de más de 601.000 € (0,06%) aportan el 6,84% de la cuota íntegra estatal.')
      )
    );
  }

  function renderForalCompare() {
    var pv = FORAL.pv, nv = FORAL.nav;
    var rows = [
      ['Recaudación foral bruta, 2025', '20.324,5 M€ (9.064 €/hab.)', '5.865,7 M€ (8.577 €/hab.)', [tag('oficial')]],
      ['Cupo o aportación al Estado, 2025', '1.464,7 M€ provisional (7,2% de lo recaudado; ≈653 €/hab.)', '874 M€ presupuestados (14,9%; ≈1.278 €/hab.)', [tag('oficial')]],
      ['Índice de imputación frente al peso de la población', '6,24% frente a ≈4,6%', '1,60% frente a ≈1,4%', [tag('oficial'), ' (peso de población: cálculo propio)']],
      ['Capacidad tributaria equivalente a régimen común (media: ' + eur(AVG15) + '/hab.)',
        '≈' + eur(roundTo(eqPc(pv, 0.7), 50)) + '/hab. (≈' + Math.round(eqPc(pv, 0.7) / AVG15 * 100) + '% de la media)',
        '≈' + eur(roundTo(eqPc(nv, 0.7), 50)) + '/hab. (≈' + Math.round(eqPc(nv, 0.7) / AVG15 * 100) + '% de la media)',
        [tag('estimado'), ' ±10%']],
      ['Renta relativa, 2022 (España = 100)', '127', '120', [tag('academica'), ' Fedea, 2024']],
      ['Financiación por habitante ajustado (régimen común = 100)', 'cerca del doble de la media', 'más de 1,5 veces la media', [tag('academica'), ' García Díaz, Fedea 2024']],
      ['Exceso de recursos por habitante que no explican las competencias', '29,8%', '28,2%', [tag('academica'), ' Ivie, 2014']],
      ['Balanza fiscal 2014 (positivo = recibe más de lo que aporta; Madrid: −2.979 €/hab., Cataluña: −1.317 €/hab.)', '+1.547 €/hab.', '+179 €/hab.', [tag('oficial'), ' Ministerio de Hacienda, 2014']],
      ['Saldo contributivo de la Seguridad Social, 2022', '−4.269,5 M€ (−1.930 €/hab.)', '−475,0 M€ (−708 €/hab.)', [tag('academica'), ' García Díaz, Fedea 2024']],
      ['Cupo adicional implícito si la base estuviera infravalorada (≈30% en el País Vasco; 15–25% supuesto en Navarra)', '≈2.000 M€ al año', '≈170–285 M€ al año', [tag('estimado')]],
      ['<strong>«Contribución que faltaría»</strong> (cupo adicional más nivelación entre comunidades)', '≈2.700–3.700 M€ al año (≈1.200–1.650 €/hab.)', '≈375–700 M€ al año (≈550–1.000 €/hab.)', [tag('estimado'), ' incertidumbre alta']]
    ];
    rows[rows.length - 1][0] = h('span', null, h('strong', null, '«Contribución que faltaría»'), ' (cupo adicional más nivelación entre comunidades)');
    var host = $('#fo-compare'); host.textContent = '';
    host.append(plainTable(['Indicador', 'País Vasco', 'Navarra', 'Tipo y fuente'], rows));

    var lo = function (T) { return roundTo(eqCap(T, 0.6), 10); }, hi = function (T) { return roundTo(eqCap(T, 0.8), 10); };
    var m = $('#fo-method'); m.textContent = '';
    m.append(
      h('li', null, h('strong', null, 'Capacidad equivalente (estimado, ±10%). '), 'Se aplica a la recaudación foral el reparto del sistema común: 50% del IRPF, 50% del IVA, 58% de los Impuestos Especiales y entre el 60% y el 80% del resto (Patrimonio, Sucesiones, ITP-AJD…); se usa el 70%. No entra Sociedades, que en régimen común no se cede. Sale ≈' + fmtInt(roundTo(eqCap(pv, 0.7), 100)) + ' M€ en el País Vasco (' + fmtInt(lo(pv)) + '–' + fmtInt(hi(pv)) + ' con el 60–80%) y ≈' + fmtInt(roundTo(eqCap(nv, 0.7), 100)) + ' M€ en Navarra (' + fmtInt(lo(nv)) + '–' + fmtInt(hi(nv)) + '). No se incluye el ajuste por retenciones de Navarra (138,4 M€); añadiría unos 70 M€, dentro del margen. Las cifras forales se calculan con normativa foral, no común, y por eso el margen es amplio.'),
      h('li', null, h('strong', null, '«Contribución que faltaría» (estimado, incertidumbre alta). '), 'País Vasco: 32.000 M€ de infravaloración de la base del cupo (De la Fuente, año 2017) × 6,24% ≈ 2.000 M€, más una contribución a la nivelación entre comunidades de 300–750 € por habitante (el rango de lo que aportaron en 2017 Cataluña, Baleares y Madrid) × 2,24 M de habitantes = 0,7–1,7 mil M€. Navarra: infravaloración supuesta del 15–25% sobre una base corregida de 70.757 M€ (2015) × 1,60% = 170–285 M€, más nivelación de 300–600 € por habitante × 0,684 M de habitantes = 205–410 M€. No se suma el déficit de la Seguridad Social, para no duplicar. Los datos de partida son de 2015-2017 y las cifras de De la Fuente no son oficiales.'),
      h('li', null, 'Un artículo de opinión (El Liberal, no académico) cifra el déficit en 3.673 M€ para el País Vasco y 793 M€ para Navarra: el mismo orden de magnitud, con un método menos riguroso. ', tag('prensa'))
    );
  }

  /* ---------- pestaña 5 ---------- */
  function renderScenario() {
    var e = state.erosion / 100, rule = state.rule;
    var collected = CLAIM * (1 - e), shortfall = CLAIM * e;
    var refill = rule === 'none' ? 0 : shortfall;
    var irpfAfter = IRPF_AEAT + refill;
    var surcharge = refill / IRPF_AEAT * 100;
    var perFiler = refill * 1e6 / IRPF_FILERS;
    var topShare = rule === 'prop' ? IEF_TOP : (rule === 'flat' ? 10 : null);

    var sum = $('#scn-summary');
    var parts = [];
    parts.push('Con una erosión del ' + state.erosion + '%, la propuesta recauda ' + fmtM(collected) + ' de los ' + fmtM(CLAIM) + ' que calcula el partido.');
    if (rule === 'none') parts.push(shortfall > 0 ? 'Los ' + fmtM(shortfall) + ' que faltan simplemente no se recaudan.' : 'No falta nada.');
    else if (shortfall > 0) parts.push('Si esos ' + fmtM(shortfall) + ' se cubren con el IRPF ' + (rule === 'prop' ? 'en proporción a lo que cada uno paga hoy' : 'con los mismos euros por declarante') + ', la recaudación del IRPF sube un ' + pct(surcharge) + ', unos ' + eur(perFiler) + ' por declarante de media. El decil de mayor renta asumiría el ' + pct(topShare, 2) + ' de ese importe.');
    else parts.push('No hay hueco que cubrir.');
    sum.textContent = parts.join(' ');

    var st = $('#scn-stats'); st.textContent = '';
    st.append(
      stat('Recaudado con el impuesto al patrimonio', fmtM(collected), pct(collected / COMBINED * 100) + ' sobre los 502.274 M€ actuales'),
      stat('Diferencia respecto a la cifra del partido', fmtM(shortfall), pct(state.erosion, 0) + ' de lo calculado'),
      stat('Variación de la recaudación del IRPF', refill > 0 ? '+' + pct(surcharge) : 'ninguna', refill > 0 ? eur(perFiler) + ' por declarante de media' : 'no se eligió ninguna compensación'),
      stat('Parte del decil superior en la compensación', topShare == null ? 'n/d' : pct(topShare, 1), topShare == null ? 'no se eligió ninguna compensación' : (rule === 'prop' ? 'proporcional al IRPF pagado' : 'cargo igual por declarante'))
    );

    var pies = $('#scn-pies'); pies.textContent = '';
    var cA = h('div', { class: 'card' }), cB = h('div', { class: 'card' }), hA = h('div'), hB = h('div');
    cA.append(h('h3', null, 'Hoy'), h('p', { class: 'sub' }, 'Impuestos más Seguridad Social, 2025.'), hA);
    cB.append(h('h3', null, 'Con la propuesta'), h('p', { class: 'sub' }, 'El impuesto al patrimonio aparece como porción propia.'), hB);
    pies.append(cA, cB);
    var grp = makeGroup();
    var before = SRC.map(function (s) { return Object.assign({}, s, { text: fmtM(s.value) + ' · ' + pct(s.value / COMBINED * 100) }); });
    var afterTotal = COMBINED + collected + refill;
    var after = SRC.map(function (s) {
      var v = s.key === 'irpf' ? irpfAfter : s.value;
      return Object.assign({}, s, { value: v, label: s.key === 'irpf' && refill > 0 ? s.label + ' con compensación' : s.label, text: fmtM(v) + ' · ' + pct(v / afterTotal * 100) });
    });
    after.push({ key: 'wt', label: 'Impuesto al patrimonio (propuesta)', color: 'c-prop', value: collected, text: fmtM(collected) + ' · ' + pct(collected / afterTotal * 100) });
    makePie(hA, before, { aria: 'Gráfico circular de los ingresos de hoy', totalMain: fmtM(COMBINED), totalSub: 'Hoy', grp: grp });
    makePie(hB, after, { aria: 'Gráfico circular de los ingresos con la propuesta de impuesto al patrimonio', totalMain: fmtM(afterTotal), totalSub: 'Con la propuesta', grp: grp });
    var lgA = h('div', { class: 'tbl-wrap', style: 'margin-top:12px' }, makeTable(before, [
      { h: 'Fuente', get: function (i) { return i.label; } },
      { h: 'M€', num: true, get: function (i) { return fmtInt(i.value); } },
      { h: '% del total', num: true, get: function (i) { return pct(i.value / COMBINED * 100); } }
    ], ['Total', fmtInt(COMBINED), '100%']));
    var lgB = h('div', { class: 'tbl-wrap', style: 'margin-top:12px' }, makeTable(after, [
      { h: 'Fuente', get: function (i) { return i.label; } },
      { h: 'M€', num: true, get: function (i) { return fmtInt(i.value); } },
      { h: '% del total', num: true, get: function (i) { return pct(i.value / afterTotal * 100); } }
    ], ['Total', fmtInt(afterTotal), '100%']));
    cA.append(lgA); cB.append(lgB);
    grp.bindRows(lgA); grp.bindRows(lgB);

    var bear = $('#scn-bear'); bear.textContent = '';
    var pH = h('div'), tH = h('div');
    bear.append(pH, tH);
    if (topShare == null) {
      pH.append(h('div', { class: 'empty' }, 'No se eligió ninguna compensación, así que no se modela ningún efecto distributivo.'));
      tH.append(h('h3', null, 'Quién carga con la compensación'), h('p', { class: 'sub' }, 'Elige arriba una regla de compensación por IRPF para ver cómo se reparte el hueco entre el decil superior y el resto.'));
    } else {
      var g3 = makeGroup();
      var bi = [
        { key: 'top', label: 'El 10% de contribuyentes con más renta', color: 'c-irpf', value: topShare, text: pct(topShare, 2) + ' de la compensación' },
        { key: 'rest', label: 'El otro 90%', color: 'c-ss', value: 100 - topShare, text: pct(100 - topShare, 2) + ' de la compensación' }
      ];
      makePie(pH, bi, { aria: 'Gráfico circular: quién carga con la compensación', totalMain: fmtM(refill), totalSub: 'Hueco cubierto con el IRPF', grp: g3 });
      tH.append(h('h3', null, 'Quién carga con la compensación'),
        h('p', { class: 'sub' }, rule === 'prop'
          ? 'La factura de IRPF de todos sube el mismo porcentaje, así que el reparto sigue la distribución actual del IRPF: el decil superior paga el 53,96% (IEF).'
          : 'Todos los declarantes pagan los mismos euros, así que cada décima parte de los declarantes carga con una décima parte.'),
        h('p', { class: 'sub' }, 'El resultado depende de la regla que elijas, no de los datos. Ninguna fuente de aquí mide cómo recaerían el IVA o la Seguridad Social, así que esas reglas no se ofrecen.'));
    }
  }

  function renderWealth() {
    var host = $('#wealth-card'); host.textContent = '';
    var pH = h('div'), tH = h('div', { class: 'tbl-wrap' }), grp = makeGroup();
    host.append(pH, tH);
    var items = [
      { key: 'w10', label: 'El 10% de hogares más ricos', color: 'c-prop', value: 53, q: '53%', e: '52,7%', text: '53% de la riqueza neta' },
      { key: 'w40', label: 'El 40% intermedio', color: 'c-oth', value: 38, q: '38%', e: '39,9%', text: '38% de la riqueza neta (el resto)' },
      { key: 'w50', label: 'El 50% de hogares con menos', color: 'c-ss', value: 9, q: '9%', e: '7,4%', text: '9% de la riqueza neta' }
    ];
    makePie(pH, items, { aria: 'Gráfico circular de la riqueza neta de los hogares por grupo', totalMain: '100%', totalSub: 'Riqueza neta de los hogares españoles, 3T 2025', grp: grp });
    tH.append(h('h3', null, 'Quién tiene la riqueza'), h('p', { class: 'sub' }, 'Banco de España. Las cuotas del 3T 2025 figuran en su página de distribución de la riqueza; la columna de 2022 procede de la Encuesta Financiera de las Familias. La página no nombra la fuente de los datos de 2025. El 40% intermedio es 100 menos las otras dos cuotas publicadas. El 1% superior tenía el 19,4% en 2022.'));
    var t = makeTable(items, [
      { h: 'Grupo', get: function (i) { return i.label; } },
      { h: '3T 2025', num: true, get: function (i) { return i.q; } },
      { h: 'EFF 2022', num: true, get: function (i) { return i.e; } }
    ]);
    var w = h('div', { class: 'tbl-wrap', style: 'margin-top:12px' }, t);
    tH.append(w);
    grp.bindRows(w);
  }

  function renderAll() { renderRevenue(); renderBrackets(); renderRegions(); renderForal(); renderScenario(); renderWealth(); }

  /* ---------- controles ---------- */
  function setSeg(ids, activeId) { ids.forEach(function (id) { $('#' + id).setAttribute('aria-pressed', id === activeId ? 'true' : 'false'); }); }
  function seg(a, b, key, va, vb, fn) {
    $('#' + a).addEventListener('click', function () { state[key] = va; setSeg([a, b], a); fn(); });
    $('#' + b).addEventListener('click', function () { state[key] = vb; setSeg([a, b], b); fn(); });
  }
  seg('rev-all', 'rev-tax', 'rev', 'all', 'tax', renderRevenue);
  seg('br-nat', 'br-mad', 'br', 'nat', 'mad', renderBrackets);
  seg('rg-off', 'rg-est', 'rg', 'off', 'est', renderRegions);
  seg('fo-pv', 'fo-nav', 'fo', 'pv', 'nav', renderForal);

  var slider = $('#erosion'), out = $('#erosion-out'), presets = $('#presets');
  function syncPresets() {
    presets.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', Number(b.getAttribute('data-e')) === state.erosion ? 'true' : 'false'); });
  }
  slider.addEventListener('input', function () { state.erosion = Number(slider.value); out.textContent = state.erosion + '%'; syncPresets(); renderScenario(); });
  presets.addEventListener('click', function (ev) {
    var b = ev.target.closest('button'); if (!b) return;
    state.erosion = Number(b.getAttribute('data-e')); slider.value = String(state.erosion); out.textContent = state.erosion + '%'; syncPresets(); renderScenario();
  });
  document.querySelectorAll('input[name="rule"]').forEach(function (r) {
    r.addEventListener('change', function () { if (r.checked) { state.rule = r.value; renderScenario(); } });
  });

  /* ---------- pestañas, con ruta en el #hash ---------- */
  var TABS = ['ingresos', 'tramos', 'comunidades', 'forales', 'patrimonio', 'ricos', 'evidencia'];
  function showTab(name, focus) {
    if (TABS.indexOf(name) < 0) name = 'ingresos';
    TABS.forEach(function (t) {
      var on = t === name;
      $('#tab-' + t).hidden = !on;
      var b = $('#t-' + t);
      b.setAttribute('aria-selected', on ? 'true' : 'false');
      b.tabIndex = on ? 0 : -1;
    });
    var cur = $('#t-' + name);
    if (cur && cur.scrollIntoView) { try { cur.scrollIntoView({ block: 'nearest', inline: 'center' }); } catch (e) {} }
    if (focus) cur.focus();
  }
  function fromHash() { showTab((location.hash || '').replace('#', '')); }
  document.querySelectorAll('.tab').forEach(function (b, i, all) {
    b.addEventListener('click', function () { var n = b.getAttribute('data-tab'); if (location.hash === '#' + n) showTab(n); else location.hash = n; window.scrollTo(0, 0); });
    b.addEventListener('keydown', function (e) {
      var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
      if (!d) return;
      e.preventDefault();
      var n = all[(i + d + all.length) % all.length].getAttribute('data-tab');
      location.hash = n; showTab(n, true);
    });
  });
  window.addEventListener('hashchange', fromHash);

  renderAll();
  fromHash();
})();
