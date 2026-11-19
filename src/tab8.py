"""Capítulo 7 (aportación del top 25): genera el HTML con las cifras calculadas aquí.

Todas las cifras derivadas salen de las constantes de abajo, para poder revisarlas.
build.py sustituye el marcador {{TAB8}} del body.html por el resultado de html().
"""


def n(x, d=0):
    """Formato español: miles con punto, decimales con coma."""
    s = f"{x:,.{d}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def tag(k):
    return f'<span class="tag t-{k}">{k}</span>'


# ---- Supuestos y reglas ------------------------------------------------------
BAI, NETO = 8020, 6220                # Inditex, ejercicio 2025 (M€)
IMPUESTO_INDITEX = BAI - NETO         # inferido por diferencia
TIPO_EMPRESA = IMPUESTO_INDITEX / BAI
IRPF_AHORRO = 0.30                    # tramo de más de 300.000 €
EXENCION = 0.05 * 0.25                # 95% exento, 5% al 25%
MARGINAL_MADRID = 0.45

# Por cada 100 € de beneficio antes de impuestos
is_emp = 100 * TIPO_EMPRESA
neto = 100 - is_emp
irpf_a = neto * IRPF_AHORRO
tot_a = is_emp + irpf_a
queda_a = 100 - tot_a
is_hold = neto * EXENCION
tot_b = is_emp + is_hold
queda_b = 100 - tot_b

# ---- Dividendos conocidos o estimados (M€ brutos al año) ----------------------
MERCADONA_DIV = 346                   # dividendo total de Mercadona por 2025
ROIG_DIV = 187                        # cifra que da Forbes España para Roig (54% del total)
HERRERO_DIV = MERCADONA_DIV * 0.29    # Herrecha: 29%, sin ajustar por autocartera
PEREZ_DIV = 41.61 * 2.4
FERROVIAL_DIV = 1000                  # previsión de dividendos de Ferrovial en 2026
DELPINO_DIV = 0.223 * FERROVIAL_DIV
MARIA_DIV = 0.0852 * FERROVIAL_DIV    # 8,52% tras la venta de junio de 2026
ESC = [
    # nombre, dividendo, B aplicable, procedencia, etiquetas
    ("Amancio Ortega", 3234, True, "Inditex 2026, vía Pontegadea Inversiones y Partler 2006", ["prensa"]),
    ("Sandra Ortega", 275, True, "Inditex (5,053%) vía Rosp Corunna, 2026 (más de 275 M€)", ["prensa"]),
    ("Juan Roig", ROIG_DIV, True, "Dividendo que cita Forbes España para 2025; Mercadona repartió 346 M€ en total. Vía Finop", ["prensa"]),
    ("Juan Carlos Escotet", 185, True, "Abanca, dividendos con cargo a los resultados de 2024, junto a su family office", ["prensa"]),
    ("Rafael del Pino", DELPINO_DIV, False, "22,3% de los 1.000 M€ que Ferrovial prevé repartir en 2026; parte se cobra en acciones. Holding en Luxemburgo", ["prensa", "estimado"]),
    ("Hortensia Herrero", HERRERO_DIV, True, "29% de los 346 M€ de Mercadona por 2025, vía Herrecha Inversiones; las fuentes dan entre el 27,7% y el 30%", ["prensa", "estimado"]),
    ("Florentino Pérez", PEREZ_DIV, True, "41,61 M de acciones de ACS × 2,4 € anunciados por acción; parte se cobra en acciones", ["prensa", "estimado"]),
    ("María del Pino", MARIA_DIV, False, "8,52% de los 1.000 M€ que Ferrovial prevé repartir en 2026; parte se cobra en acciones. Tiene parte vía Menosmares y parte a título personal en notificaciones antiguas, así que no modelo la holding", ["prensa", "estimado"]),
    ("Familia Daurella (Sol y Carmen)", 177, True, "Dividendos de 2025 de la familia vía Cobega, según ESdiario; un titular de Forbes habla de 160 M€ de Olive Partners. Es de toda la familia, no solo de ellas", ["prensa"]),
    ("Familia Puig", 178, True, "Dividendo de 2026 de Puig; incluye miembros de la familia fuera de Exea", ["prensa"]),
]
# Puestos del top 25 con un dividendo atribuible a la persona o a su familia
CON_DIVIDENDO = {1, 2, 3, 4, 5, 6, 7, 9, 11, 20, 23}
assert len(CON_DIVIDENDO) == 11
ORTEGA_A = 3234 * IRPF_AHORRO

# SICAV mayores por patrimonio hasta septiembre de 2026 (M€)
SICAV = [
    ("Gesprisa (Palatchi)", 1797),
    ("Torrenova (Banca March)", 1308),
    ("Chart (Del Pino)", 958),
    ("Turqueta (Del Pino)", 908),
    ("Allocation (Del Pino)", 895),
    ("Lluc Valores (Banca March)", 720),
    ("Fomento de Ahorros", 718),
    ("Soixa", 650),
    ("Morinvest (Koplowitz)", 627),
    ("Bellver (Banca March)", 613),
]
SICAV_DELPINO = 958 + 908 + 895
assert SICAV_DELPINO == 2761
SICAV_TOP25 = 1797 + SICAV_DELPINO + 627
GESPRISA_SOBRE_FORTUNA = 1797 / 2900 * 100
ITSGF_2023, ITSGF_2025 = 623.6, 19

SUELDO_PEREZ, SUELDO_ROIG = 9.14, 12.0
IRPF_PEREZ = SUELDO_PEREZ * MARGINAL_MADRID
IRPF_ROIG = SUELDO_ROIG * 0.54

# ---- Top 25 de Forbes España 2026 (M€) ----------------------------------------
TOP = [
    (1, "Amancio Ortega", 125200, "Inditex, vía Pontegadea Inversiones (50,01%) y Partler 2006 (9,284%).", "Dividendos de 3.234 M€ en 2026. Pontegadea Inversiones ganó 2.518 M€ en 2025. No tiene cargo ejecutivo remunerado en Inditex.", ["prensa"]),
    (2, "Sandra Ortega", 11500, "Rosp Corunna.", "Beneficio de 307 M€ en 2025, casi todo de dividendos de Inditex; lo reinvierte todo.", ["prensa"]),
    (3, "Juan Roig", 9800, "Finop (50,66% de Mercadona).", "Dividendos de 187 M€ y sueldo de 12 M€ brutos en 2025, según Forbes España.", ["prensa"]),
    (4, "Juan Carlos Escotet", 8100, "Abanca y su family office.", "Unos 185 M€ de dividendos con cargo a 2024. En 2026 el banco paga más impuesto porque usa menos créditos fiscales.", ["prensa"]),
    (5, "Rafael del Pino", 7800, "Rijn Capital SARL (Luxemburgo): 22,3% de Ferrovial.", "Ferrovial prevé 1.000 M€ de dividendos en 2026. Rijn salió de Países Bajos en 2024, tras una inspección neerlandesa.", ["prensa"]),
    (6, "Hortensia Herrero", 5550, "Herrecha Inversiones: en torno al 29% de Mercadona; con Roig, el 80%.", "Con el 29% de los 346 M€ repartidos, le tocarían unos 100 M€ de dividendo por 2025. No encontré su cifra publicada.", ["prensa", "estimado"]),
    (7, "Florentino Pérez", 4900, "Rosán Inversiones: 15,015% de ACS.", "Unos 100 M€ de dividendos al 2,4 € por acción. Sueldo de ACS de 9,14 M€ en 2025.", ["prensa", "estimado"]),
    (8, "Tomás Olivo", 4900, "General de Galerías Comerciales (socimi).", "Controla el 99,58% de la socimi, según MarketScreener. No encontré dividendos.", ["prensa"]),
    (9, "María del Pino", 4200, "Menosmares (Ferrovial).", "Tiene el 8,52% de Ferrovial tras vender 860.000 acciones en junio de 2026. En el último año vendió 10,2 M de acciones por unos 484 M€, vía Casa Grande de Cartagena y Menosmares.", ["prensa"]),
    (10, "Miguel Fluxà", 4100, "Sayglo Holding, matriz de Iberostar.", "Iberostar gestionó 5.100 M€ de ingresos en 2025 y dice ser 100% familiar. No encontré beneficio ni impuestos.", ["prensa"]),
    (11, "Sol Daurella", 3500, "Cobega; Olive Partners.", "La familia recibió 177 M€ de dividendos en 2025 vía Cobega, según ESdiario; un titular de Forbes habla de 160 M€ de Olive Partners. Es de toda la familia, no solo de Sol.", ["prensa"]),
    (12, "Daniel Maté", 3500, "Glencore (en torno al 3%).", "Vive en Suiza según Forbes (vía Wikipedia): su IRPF español probablemente no aplica.", ["prensa", "inferido"]),
    (13, "Carlos March", 3300, "Corporación Financiera Alba (retirada de bolsa en 2025) y Banca March.", "Banca March ganó 239,2 M€ en 2024. Alba y Banca March son 100% familiares, con cuatro accionistas (los hermanos March Delgado), así que no hay dividendo público.", ["prensa"]),
    (14, "Juan Abelló", 3100, "Torreal.", "Sin dato público consultado.", []),
    (15, "Juan March", 3100, "Familia March: Alba y Banca March.", "Ver Carlos March.", ["prensa"]),
    (16, "Alberto Palatchi", 2900, "Galma Capital; SICAV Gesprisa Inversiones.", "Vendió Pronovias en 2017 por 550 M€ y se quedó el 10%. Galma Capital ganó 161 M€ en 2025. Controla la mayor SICAV de España (ver sección 7).", ["prensa"]),
    (17, "José María Serra Farré", 2900, "Inocsa y Grupo Catalana Occidente (Occidente).", "Occidente repartió 639 M€ en 2025, 558 M€ de ellos extraordinarios. Inocsa dice que no los reparte entre sus accionistas.", ["oficial", "prensa"]),
    (18, "Leopoldo del Pino", 2600, "Siemprelara (Ferrovial).", "Siemprelara tenía el 4,2% de Ferrovial en el informe anual de 2022; no verifiqué cuánto tiene hoy.", ["oficial"]),
    (19, "Fernando Roig", 2400, "Pamesa.", "Sin dato público consultado.", []),
    (20, "Manuel Puig", 2100, "Exea, holding de la familia Puig; Puig Brands.", "La familia ingresó más de 178 M€ de dividendos en 2026.", ["prensa"]),
    (21, "Familia Luengo (SAMCA)", 2100, "SAMCA.", "Sin dato público consultado.", []),
    (22, "Alicia Koplowitz", 1900, "Omega Capital; SICAV Morinvest.", "Es la inversora de control de Morinvest, con 627 M€ de patrimonio hasta septiembre de 2026 (ver sección 7). No encontré dividendos.", ["prensa"]),
    (23, "Carmen Daurella", 1900, "Cobega.", "Ver Sol Daurella: el dividendo es de toda la familia.", ["prensa"]),
    (24, "Manuel Lao", 1900, "Nortia Capital.", "Vendió Cirsa a Blackstone en 2018 por entre 2.200 y 2.400 M€, según la fuente. Hoy invierte vía Nortia: 8,5% de Merlin, y vendió el 5,12% de Sacyr por 150,8 M€ en diciembre de 2025. No encontré dividendos.", ["prensa"]),
    (25, "Joaquín del Pino", 1800, "Familia Del Pino (Ferrovial).", "Una noticia, sin fecha clara, le atribuye el 2,53% de Ferrovial; no lo verifiqué.", ["prensa"]),
]
TOTAL_LISTA = 300500
SUMA_TOP25 = sum(t[2] for t in TOP)
assert SUMA_TOP25 == 225050, SUMA_TOP25


def tags(ks):
    return " ".join(tag(k) for k in ks)


def tr(cells, labels):
    tds = "".join(f'<td data-l="{l}">{c}</td>' for c, l in zip(cells, labels))
    return f"<tr>{tds}</tr>"


def bars(items, aria, hi_last=True):
    top = max(v for _, v, _ in items)
    out = [f'<ul class="bars" aria-label="{aria}">']
    for i, (lab, v, txt) in enumerate(items):
        cls = ' class="hi"' if hi_last and i == len(items) - 1 else ""
        out.append(f'<li{cls}><span>{lab}</span><span class="bar"><i style="--w:{v / top * 100:.1f}%"></i></span><span class="v">{txt}</span></li>')
    out.append("</ul>")
    return "\n    ".join(out)


def html():
    # --- escenarios
    esc_rows = []
    for nom, div, b_ok, origen, tg in ESC:
        a = div * IRPF_AHORRO
        b = f"{n(div * EXENCION, 1)}" if b_ok else "no se modela"
        esc_rows.append(tr(
            [f"<strong>{nom}</strong>", n(div, 0 if div >= 100 else 1), n(a, 1) + f" {tag('estimado')}", b + (f" {tag('estimado')}" if b_ok else ""), f"{origen} {tags(tg)}"],
            ["Persona", "Dividendo bruto al año (M€)", "Como persona física, 30% (M€)", "Vía holding, 1,25% (M€)", "De dónde sale el dividendo"]))
    esc_bars = bars([(nom, div, n(div, 0)) for nom, div, _, _, _ in ESC], "Dividendos brutos anuales conocidos o estimados, en millones de euros", hi_last=False)

    top_rows = []
    for r, nom, fort, veh, dato, tg in TOP:
        top_rows.append(tr([f"{r} · <strong>{nom}</strong>", n(fort), veh, f"{dato} {tags(tg)}".strip()],
                           ["Nombre", "Fortuna (M€)", "Vehículo", "Lo que se sabe"]))

    stats_itsgf = bars([("2023", ITSGF_2023, n(ITSGF_2023, 1)), ("2024", 37, "≈37"), ("2025", ITSGF_2025, "≈19")],
                       "Recaudación del Impuesto de Solidaridad de las Grandes Fortunas en millones de euros")
    stats_patr = bars([("2013", 471, "471"), ("2023", 865, "865"), ("2024", 1023, "1.023")],
                      "Declarantes del Impuesto sobre el Patrimonio con más de 30 millones de euros")
    stats_irpf = bars([("2007", 10580, "10.580"), ("2023", 14738, "14.738"), ("2024", 18829, "18.829")],
                      "Declarantes del IRPF con más de 601.000 euros")

    stats_sicav = bars([(nom, v, n(v)) for nom, v in SICAV], "Patrimonio de las diez mayores SICAV de España hasta septiembre de 2026, en millones de euros", hi_last=False)

    return f'''<section class="panel chapter" id="tab-aportacion">
  <div class="tab-head">
    <p class="eyebrow"><span class="chnum" aria-hidden="true">07</span>Cuánto aportan los 25 mayores patrimonios</p>
    <h2>Su IRPF personal es secreto. Lo que sí se mide es lo que pagan sus empresas y cuánto cambia la factura según cobren.</h2>
    <p class="sub">Hacienda no publica lo que paga cada contribuyente (artículo 95 de la Ley General Tributaria), así que no hay una cifra pública del IRPF de Ortega, Roig o Del Pino. Este capítulo hace tres cosas: cuenta lo que pagan las empresas que controlan, calcula con las reglas oficiales cuánto tributaría un dividendo según lo cobre una persona o una holding, y sitúa a los más ricos en las estadísticas agregadas de Hacienda. <strong>Ninguna cifra de aquí es el IRPF real de una persona.</strong></p>
  </div>

  <h3 class="lead">1. Lo que pagan las empresas antes de repartir un euro</h3>
  <p class="prose">El primer impuesto sobre el beneficio lo paga la empresa. Esto es lo que encontré de tres de los grupos del top 25.</p>
  <div class="tbl-wrap">
    <table class="plain stack">
      <thead><tr><th>Grupo y dueño</th><th>Beneficio antes de impuestos</th><th>Impuesto</th><th>Beneficio neto</th><th>Dividendos</th></tr></thead>
      <tbody>
        {tr(["<strong>Inditex</strong> (Ortega)", f"{n(BAI)} M€ {tag('prensa')}", f"≈{n(IMPUESTO_INDITEX)} M€, el {n(TIPO_EMPRESA * 100, 1)}% {tag('inferido')}", f"{n(NETO)} M€ {tag('prensa')}", f"5.454 M€; a Amancio Ortega, 3.234 M€ {tag('prensa')}"], ["Grupo y dueño", "Beneficio antes de impuestos", "Impuesto", "Beneficio neto", "Dividendos"])}
        {tr(["<strong>Mercadona</strong> (Roig, Herrero)", "No consultado", f"690 M€ entre impuesto de sociedades y otros impuestos; tipo efectivo del 22,8% {tag('prensa')}", f"1.729 M€ {tag('prensa')}", f"346 M€, el 20% del beneficio {tag('prensa')}"], ["Grupo y dueño", "Beneficio antes de impuestos", "Impuesto", "Beneficio neto", "Dividendos"])}
        {tr(["<strong>Abanca</strong> (Escotet)", f"500,7 M€ en el primer semestre de 2026 {tag('prensa')}", f"114,7 M€ en ese semestre, frente a 55,9 M€ un año antes {tag('prensa')}", f"386 M€ en el semestre; 902,4 M€ en 2025 {tag('prensa')}", f"≈185 M€ a Escotet y su family office, por los resultados de 2024 {tag('prensa')}"], ["Grupo y dueño", "Beneficio antes de impuestos", "Impuesto", "Beneficio neto", "Dividendos"])}
      </tbody>
    </table>
  </div>
  <ul class="notes">
    <li>Inditex: el impuesto es la diferencia entre el beneficio antes de impuestos y el neto, así que incluye cualquier otro ajuste. Un diario añade que Inditex suma unos 10.000 M€ en impuestos de todo tipo, 2.600 M€ de ellos en España, sin precisar qué cuenta {tag('prensa')}.</li>
    <li>Mercadona: de los 690 M€, el desglose en España que da otro medio es 469 M€ de impuesto de sociedades y 202 M€ de otros impuestos, que suman 671 M€ {tag('prensa')}. Además, Mercadona estima su aportación total, con impuestos soportados y recaudados, en 3.383 M€ {tag('prensa')}.</li>
    <li>Abanca: el impuesto sube porque usa menos créditos fiscales de procesos de integración ya concluidos {tag('prensa')}.</li>
  </ul>

  <h3 class="lead">2. De cada 100 € de beneficio antes de impuestos, ¿cuánto llega a Hacienda?</h3>
  <p class="prose">Con el tipo de impuesto de sociedades que implica Inditex ({n(TIPO_EMPRESA * 100, 1)}%) y las reglas oficiales. Es un ejemplo, no un caso real.</p>
  <div class="sb-row">
    <p class="cap">El dueño cobra el dividendo como persona física</p>
    <div class="stackbar" role="img" aria-label="De 100 euros: {n(is_emp, 1)} de impuesto de sociedades, {n(irpf_a, 1)} de IRPF, {n(queda_a, 1)} se queda el dueño"><i class="s1" style="--w:{is_emp:.1f}%"></i><i class="s2" style="--w:{irpf_a:.1f}%"></i><i class="s3" style="--w:{queda_a:.1f}%"></i></div>
    <p class="vals"><span><b class="k1"></b>Impuesto de sociedades {n(is_emp, 1)}</span><span><b class="k2"></b>IRPF del ahorro {n(irpf_a, 1)}</span><span><b class="k3"></b>Se queda el dueño {n(queda_a, 1)}</span></p>
    <p class="tot">Hacienda recibe {n(tot_a, 1)} de cada 100 € {tag('estimado')}</p>
  </div>
  <div class="sb-row">
    <p class="cap">El dividendo entra en una holding con exención del 95%</p>
    <div class="stackbar" role="img" aria-label="De 100 euros: {n(is_emp, 1)} de impuesto de sociedades, {n(is_hold, 1)} de impuesto de la holding, {n(queda_b, 1)} queda en la holding"><i class="s1" style="--w:{is_emp:.1f}%"></i><i class="s2" style="--w:{is_hold:.2f}%"></i><i class="s3" style="--w:{queda_b:.1f}%"></i></div>
    <p class="vals"><span><b class="k1"></b>Impuesto de sociedades {n(is_emp, 1)}</span><span><b class="k2"></b>Impuesto de la holding {n(is_hold, 1)}</span><span><b class="k3"></b>Queda en la holding {n(queda_b, 1)}</span></p>
    <p class="tot">Hacienda recibe {n(tot_b, 1)} de cada 100 € {tag('estimado')}</p>
  </div>
  <p class="prose">La diferencia no es un agujero sin más: en el segundo caso el dinero sigue dentro de la sociedad y no está a disposición personal. Si el dueño lo reparte, tributa; si lo reinvierte, no. Y si fallece con las acciones, la ganancia acumulada no tributa en su IRPF {tag('oficial')}.</p>
  <ul class="notes">
    <li>Impuesto de sociedades de la empresa: el {n(TIPO_EMPRESA * 100, 1)}% que implican las cuentas de Inditex {tag('inferido')}.</li>
    <li>IRPF del ahorro: 19% hasta 6.000 €, luego 21%, 23%, 27% y 30% por encima de 300.000 €. Para cantidades grandes, el 30% {tag('oficial')}.</li>
    <li>Holding con al menos un 5% de la participada: el 95% del dividendo queda exento y el resto paga el 25%, un 1,25% efectivo {tag('oficial')}. No comprobé los requisitos holding por holding {tag('estimado')}.</li>
  </ul>

  <h3 class="lead">3. Los 25 mayores patrimonios y lo que se sabe de cada uno</h3>
  <p class="prose">Las fortunas son la estimación de mercado de Forbes España 2026 {tag('prensa')}, no un patrimonio fiscal. Los 25 suman {n(SUMA_TOP25)} M€, el {n(SUMA_TOP25 / TOTAL_LISTA * 100, 1)}% de los unos {n(TOTAL_LISTA)} M€ de la lista de 100. Ortega solo, el {n(125200 / TOTAL_LISTA * 100, 1)}%. De {len(CON_DIVIDENDO)} de los 25 hay un dividendo atribuible a la persona o a su familia; de los otros {25 - len(CON_DIVIDENDO)}, no.</p>
  <div class="tbl-wrap">
    <table class="plain stack">
      <thead><tr><th>Nombre</th><th>Fortuna (M€)</th><th>Vehículo</th><th>Lo que se sabe</th></tr></thead>
      <tbody>
        {chr(10).join("        " + r for r in top_rows).strip()}
      </tbody>
    </table>
  </div>

  <h3 class="lead">4. Escenarios por persona: persona física frente a holding</h3>
  <p class="prose"><strong>No es lo que pagan.</strong> Es lo que saldría de aplicar las reglas oficiales al dividendo conocido, en dos situaciones hipotéticas. En el primer caso la persona cobraría todo; en el segundo, el dividendo se queda en una holding con exención del 95%. Solo están los {len(ESC)} casos con un dividendo atribuible a la persona o a su familia.</p>
  <div class="tbl-wrap">
    <table class="plain stack">
      <thead><tr><th>Persona</th><th>Dividendo bruto al año (M€)</th><th>Como persona física, 30% (M€)</th><th>Vía holding, 1,25% (M€)</th><th>De dónde sale el dividendo</th></tr></thead>
      <tbody>
        {chr(10).join("        " + r for r in esc_rows).strip()}
      </tbody>
    </table>
  </div>
  <p class="prose">Dividendo bruto anual conocido o estimado, en millones de euros:</p>
  {esc_bars}
  <p class="prose">Solo el dividendo de 2026 de Amancio Ortega, de tributar como persona física al 30%, daría unos {n(ORTEGA_A)} M€ {tag('estimado')}. Es más que todo el Impuesto de Solidaridad de las Grandes Fortunas de 2023 ({n(ITSGF_2023, 1)} M€) {tag('oficial')} y unas {n(ORTEGA_A / ITSGF_2025)} veces el de 2025 (≈{ITSGF_2025} M€) {tag('oficial')}. Comparan un impuesto sobre la renta hipotético con un impuesto sobre el patrimonio: sirven para ver órdenes de magnitud, no como argumento a favor de ninguno de los dos.</p>

  <h3 class="lead">5. Lo que sí tributa a tipo pleno: los sueldos</h3>
  <div class="tbl-wrap">
    <table class="plain stack">
      <thead><tr><th>Persona</th><th>Retribución</th><th>IRPF aproximado</th><th>Frente al dividendo de su holding</th></tr></thead>
      <tbody>
        {tr(["<strong>Florentino Pérez</strong>", f"{n(SUELDO_PEREZ, 2)} M€ en ACS, 2025 {tag('prensa')}", f"≈{n(IRPF_PEREZ, 1)} M€, al 45% marginal de Madrid, sin deducciones y sin verificar su residencia {tag('estimado')}", f"≈{n(PEREZ_DIV)} M€ de dividendos {tag('estimado')}"], ["Persona", "Retribución", "IRPF aproximado", "Frente al dividendo de su holding"])}
        {tr(["<strong>Juan Roig</strong>", f"12 M€ brutos en 2025 {tag('prensa')}", f"≈{n(IRPF_ROIG, 1)} M€: pagó el 54% de su retribución, según la prensa {tag('prensa')} {tag('estimado')}", f"{n(ROIG_DIV)} M€ de dividendos {tag('prensa')}"], ["Persona", "Retribución", "IRPF aproximado", "Frente al dividendo de su holding"])}
      </tbody>
    </table>
  </div>
  <p class="prose">El tipo marginal máximo del IRPF general va del 45% en Madrid al 54% en la Comunitat Valenciana {tag('oficial')}. Es la parte de su renta de la que hay indicios de tributación plena; el resto depende de si reparten dividendos.</p>

  <h3 class="lead">6. Los más ricos dentro de las estadísticas de Hacienda</h3>
  <p class="prose">Recaudación del Impuesto de Solidaridad de las Grandes Fortunas, en millones de euros {tag('oficial')}:</p>
  {stats_itsgf}
  <p class="prose">En 2023 lo pagaron 12.010 declarantes con una cuota media de 52.000 €, y Madrid aportó 555 de los 623,6 M€ {tag('oficial')}. Sumado al Impuesto sobre el Patrimonio, 2023 dejó 1.868 M€ {tag('oficial')}. No he encontrado la explicación oficial de la caída de 2024 y 2025, y no la doy.</p>
  <p class="prose">Declarantes del Impuesto sobre el Patrimonio con más de 30 M€ {tag('prensa')}:</p>
  {stats_patr}
  <p class="prose">En 2024 hubo 227.424 declarantes de Patrimonio, 185.031 de ellos con cuota {tag('prensa')}.</p>
  <p class="prose">Declarantes del IRPF con más de 601.000 € {tag('prensa')}:</p>
  {stats_irpf}
  <p class="prose">Son el 0,08% de las 24.628.279 declaraciones de 2024 {tag('prensa')}.</p>
  <h3 class="lead">Qué ve la estadística y qué no</h3>
  <ul class="notes">
    <li>El IRPF solo ve lo que llega a la persona. Lo que una holding retiene no aparece en la declaración del dueño {tag('inferido')}.</li>
    <li>Los 100 de Forbes serían como mucho una décima parte de los 1.023 declarantes de Patrimonio con más de 30 M€ {tag('inferido')}. Es un máximo: Maté vive en Suiza, y no confirmé si la estadística incluye País Vasco y Navarra.</li>
    <li>Forbes valora a precio de mercado; el Patrimonio usa valores fiscales y tiene exenciones, como la de la empresa familiar {tag('oficial')}. Por eso ni las fortunas de Forbes ni la base del impuesto son comparables.</li>
  </ul>

  <h3 class="lead">7. Las mayores SICAV y de quién son</h3>
  <p class="prose">La SICAV es la vía con impuesto reducido que sigue abierta a los grandes patrimonios (capítulo 6). Patrimonio de las diez mayores hasta septiembre de 2026, en millones de euros {tag('prensa')}:</p>
  {stats_sicav}
  <p class="prose">Tres de las diez son de la familia Del Pino y suman {n(SICAV_DELPINO)} M€, más que la mayor, la de Palatchi (1.797 M€) {tag('prensa')}. Sumando las de Del Pino, Palatchi y Koplowitz, las SICAV que la prensa asocia a gente del top 25 tienen {n(SICAV_TOP25)} M€ de patrimonio {tag('inferido')}.</p>
  <ul class="notes">
    <li>Es el patrimonio de la sociedad, no el del dueño: una SICAV necesita al menos 100 accionistas para seguir pagando el 1% {tag('oficial')}. No sé qué parte de cada una es de la familia que la controla. Gesprisa equivale al {n(GESPRISA_SOBRE_FORTUNA)}% de la fortuna que Forbes atribuye a Palatchi (2.900 M€), pero eso es una comparación de órdenes de magnitud {tag('inferido')}.</li>
    <li>Banca March gestiona otras tres (Torrenova, Lluc Valores y Bellver). Un medio las atribuye a la familia March, pero Bellver tiene 2.818 partícipes, así que no las sumo {tag('prensa')}.</li>
  </ul>

  <h3 class="lead">Veredicto</h3>
  <div class="tbl-wrap">
    <table class="plain verdict">
      <thead><tr><th>Lo que se dice</th><th>Veredicto</th><th>Qué hay detrás</th></tr></thead>
      <tbody>
        <tr>
          <td>«Los más ricos no contribuyen»</td>
          <td><strong>Depende de qué se cuente. De su IRPF personal no hay datos; de lo que pagan sus empresas, sí.</strong></td>
          <td>Inditex paga unos {n(IMPUESTO_INDITEX)} M€ de impuesto sobre beneficios {tag('inferido')} y Mercadona estima 3.383 M€ de aportación total {tag('prensa')}. Sus sueldos tributan a tipo pleno {tag('estimado')}. En el otro lado, el Impuesto de Solidaridad de las Grandes Fortunas dejó unos 19 M€ en 2025 {tag('oficial')} y, si un dueño deja el dividendo en una holding, por cada 100 € de beneficio Hacienda recibe unos {n(tot_b)} en lugar de unos {n(tot_a)} {tag('estimado')}.</td>
        </tr>
        <tr>
          <td>«Sus empresas ya pagan mucho»</td>
          <td><strong>Cierto, pero es otra pregunta: el impuesto de sociedades no es el IRPF del dueño.</strong></td>
          <td>Lo paga la empresa tenga un dueño rico o accionistas dispersos. Cómo se reparte su carga entre accionistas, trabajadores y clientes es un debate abierto entre economistas, y esta página no tiene datos para zanjarlo.</td>
        </tr>
      </tbody>
    </table>
  </div>

  <h3 class="lead">Qué significa para la pregunta de fondo</h3>
  <p class="prose">Este capítulo no contrasta si subir impuestos a los ricos lo paga la clase media. Aporta dos hechos: el impuesto específico sobre grandes fortunas recauda hoy poco, y buena parte del beneficio de los mayores grupos ya tributa en la empresa antes de llegar al dueño. También da un ejemplo de que las estructuras se mueven: Rijn Capital pasó de Países Bajos a Luxemburgo en 2024, después de que Hacienda neerlandesa abriera una inspección {tag('prensa')}. Eso no prueba que se mueva por impuestos, y no dice nada de qué pasaría con la clase media.</p>

  <h3 class="lead">Lo que no sé</h3>
  <ul class="list">
    <li>El IRPF real de cualquiera de ellos. Es secreto y no figura en ninguna fuente.</li>
    <li>Cuánto de los dividendos de cada holding llega a la persona. Ortega, Sandra Ortega, Florentino Pérez y los Serra reinvierten o retienen según la prensa, pero no sé cuánto sale en sueldos o préstamos.</li>
    <li>De {25 - len(CON_DIVIDENDO)} de los 25 no encontré un dividendo atribuible a la persona: Olivo, Fluxà, Maté, los March, Abelló, Palatchi, Serra, Leopoldo y Joaquín del Pino, Fernando Roig, Luengo, Koplowitz y Lao. De Abelló, Fernando Roig y Luengo no encontré nada útil.</li>
    <li>Fuentes que no cuadran: el desglose de impuestos de Mercadona (690 frente a 671 M€) y los resultados del grupo de Ortega, que ya señalé en el capítulo 6.</li>
    <li>Daurella: 177 M€ según ESdiario frente a 160 M€ en un titular de Forbes. No sé si son años o niveles distintos, y el dinero es de toda la familia, no de Sol.</li>
    <li>Mercadona: los 187 M€ de Roig son el 54% de los 346 M€, no el 50,66% de su participación, y no sé por qué. La parte de Hortensia Herrero (29%) está calculada sobre el total, sin ese ajuste, y las fuentes dan entre el 27,7% y el 30%.</li>
    <li>Del Pino: la participación de María (8,52%) es la de junio de 2026, pero la de Leopoldo (4,2%, informe de 2022) y la de Joaquín (2,53%, sin fecha clara) son antiguas, y por eso no las modelo.</li>
    <li>Residencia fiscal de Pérez y de los Del Pino, y si el 30% de IRPF del ahorro aplica a cada uno según su comunidad.</li>
    <li>El dividendo de Escotet es de resultados de 2024; los de 2025 serían menores, porque Abanca ganó menos.</li>
    <li>Los dividendos de Ferrovial y ACS pueden cobrarse en acciones, lo que aplaza el IRPF. No sé qué eligió cada uno.</li>
  </ul>

  <h3 class="lead">Fuentes de este capítulo</h3>
  <ul class="src-cols">
    <li><a href="https://sede.agenciatributaria.gob.es/Sede/estadisticas/recaudacion-tributaria/informe-anual/ejercicio-2025/6-otros-impuestos.html">AEAT, informe anual de recaudación 2025: otros impuestos</a> {tag('oficial')}</li>
    <li><a href="https://www.hacienda.gob.es/GabineteMinistro/notas%20prensa/2023/s.e.hacienda/20-09-23-np-impuesto-grandes-fortunas.pdf">Hacienda, nota sobre el ITSGF de 2023</a> {tag('oficial')}</li>
    <li><a href="https://valenciaplaza.com/impuesto-solidaridad-grandes-fortunas-recauda-200000-euros-comunitat">Valencia Plaza sobre el ITSGF de 2023, con el dato de Madrid</a> {tag('prensa')}</li>
    <li><a href="https://www.bankinter.com/blog/economia/distribucion-impuesto-patrimonio">Bankinter sobre la estadística de Patrimonio de 2024</a> {tag('prensa')}</li>
    <li><a href="https://www.xataka.com/empresas-y-economia/hacienda-ha-detectado-fenomeno-inedito-2013-se-ha-duplicado-numero-espanoles-30-millones-euros">Xataka sobre los contribuyentes de más de 30 M€</a> {tag('prensa')}</li>
    <li><a href="https://www.bolsamania.com/noticias_amp/economia/economia--los-contribuyentes-ricos-con-patrimonio-superior-a-30-millones-se-multiplican-casi-por-dos-en-una-decada--20818296.html">Europa Press (Bolsamanía): 865 declarantes en 2023</a> {tag('prensa')}</li>
    <li><a href="https://forbes.es/?p=969876">Forbes España sobre los 18.829 declarantes de más de 601.000 €</a> {tag('prensa')}</li>
    <li><a href="https://forbes.es/?p=753425">Forbes España (Europa Press): 14.738 en 2023</a> {tag('prensa')}</li>
    <li><a href="https://www.estrategiasdeinversion.com/actualidad/noticias/bolsa-espana/inditex-beneficio-record-de-6220-millones-y-eleva-n-897733">Estrategias de Inversión: resultados de Inditex de 2025</a> {tag('prensa')}</li>
    <li><a href="https://www.elespanol.com/quincemil/economia/empresas/20260311/amancio-ortega-recibira-millones-dividendos-inditex-elevar-retribucion/1003744164811_0.html">El Español: dividendos de Inditex a Ortega</a> {tag('prensa')}</li>
    <li><a href="https://www.eldiario.es/economia/inditex-logra-beneficio-record-gana-6-220-millones-ingresos-rozan-40-000_1_13056951.html">elDiario.es sobre los impuestos de Inditex</a> {tag('prensa')}</li>
    <li><a href="https://forbes.es/?p=986792">Forbes España sobre Rosp Corunna</a> {tag('prensa')}</li>
    <li><a href="https://www.merca2.es/2026/07/24/holding-sandra-ortega-beneficio-307-millones-2423050/">Merca2 sobre el holding de Sandra Ortega</a> {tag('prensa')}</li>
    <li><a href="https://www.eldiario.es/comunitat-valenciana/economia/mercadona-gano-1-729-millones-euros-2025-alcanzo-28-5-cuota-mercado-alcanzar-41-500-milloones_1_13054918.html">elDiario.es sobre los resultados de Mercadona</a> {tag('prensa')}</li>
    <li><a href="https://www.merca2.es/2026/03/20/juan-roig-presume-mercadona-2360812/">Merca2 sobre la aportación fiscal de Mercadona</a> {tag('prensa')}</li>
    <li><a href="https://forbes.es/?p=676176">Forbes España sobre el sueldo de Roig y su 50,66% de Mercadona</a> {tag('prensa')}</li>
    <li><a href="https://forbes.es/economia/906818/juan-roig-invierte-220-millones-de-su-sueldo-y-dividendos-en-la-economia-espanola/">Forbes España: 187 M€ de dividendos y 12 M€ de sueldo de Roig en 2025</a> {tag('prensa')}</li>
    <li><a href="https://www.eldebate.com/espana/comunidad-valenciana/20260116/hortensia-herrero-vicepresidenta-mercadona-sale-accionario-proveedor-mobiliario-inditex_374956.html">El Debate sobre Herrecha y el 29% de Mercadona de Hortensia Herrero</a> {tag('prensa')}</li>
    <li><a href="https://roams.es/actualidad/finanzas/abanca-record-negocio-pese-ganar-menos/">Roams sobre Abanca en el primer semestre de 2026</a> {tag('prensa')}</li>
    <li><a href="https://theobjective.com/economia/banca/2026-01-28/abanca-beneficios-2025-clientes/">The Objective sobre el beneficio de Abanca en 2025</a> {tag('prensa')}</li>
    <li><a href="https://metropolitano.gal/enfoque/escotet-y-su-family-office-cobran-185-millones-en-dividendos-de-abanca-de-los-resultados-de-2024">Metropolitano sobre los dividendos de Escotet</a> {tag('prensa')}</li>
    <li><a href="https://blarkad.com/ticker/FER/ownership">Declaración SEC 13G/A de Rijn Capital sobre Ferrovial</a> {tag('oficial')}</li>
    <li><a href="https://forbes.es/?p=903256">Forbes España: Ferrovial prevé 1.000 M€ de dividendos en 2026</a> {tag('prensa')}</li>
    <li><a href="https://www.merca2.es/2026/06/15/ferrovial-dividendo-flexible-400-millones-2397553/">Merca2 sobre el dividendo flexible de Ferrovial</a> {tag('prensa')}</li>
    <li><a href="https://www.eldiario.es/economia/rafael-pino-saca-ahora-paises-bajos-patrimonial-controla-21-ferrovial_1_11346476.html">elDiario.es sobre Rijn Capital y Luxemburgo</a> {tag('prensa')}</li>
    <li><a href="https://www.merca2.es/2026/06/18/maria-del-pino-vende-acciones-ferrovial-2400660/">Merca2 sobre las ventas de acciones de María del Pino</a> {tag('prensa')}</li>
    <li><a href="https://informeanualintegrado2022.ferrovial.com/wp-content/uploads/sites/8/2023/02/ferrovial-informe-anual-integrado-2022-ferrovial-en-bolsa.pdf">Ferrovial, informe anual de 2022: accionistas significativos</a> {tag('oficial')}</li>
    <li><a href="https://www.vozpopuli.com/espana/ferrovial-rafael_del_pino-cnmv-leopoldo_del_pino-siemprelara_0_880112031.html">Vozpópuli sobre las participaciones de los hermanos Del Pino</a> {tag('prensa')}</li>
    <li><a href="https://www.finect.com/usuario/eduardogarcia/articulos/el-dividendo-de-acs-crece-un-20-florentino-perez-anuncia-el-pago-de-24-euros-por-accion">Finect sobre el dividendo de ACS de 2,4 € por acción</a> {tag('prensa')}</li>
    <li><a href="https://finantresnoticias.com/empresas/florentino-perez-sube-15-por-ciento-en-acs-debe-vigilar-pequeno-inversor/">Finanzas Noticias: Florentino Pérez al 15,015% de ACS</a> {tag('prensa')}</li>
    <li><a href="https://fashionunited.es/noticias/empresas/los-puig-ingresan-mas-de-178-millones-de-euros-en-dividendos-del-grupo/2026061549675">FashionUnited sobre el dividendo de los Puig</a> {tag('prensa')}</li>
    <li><a href="https://thecorner.eu/?p=123334">The Corner sobre el dividendo de Occidente e Inocsa</a> {tag('prensa')}</li>
    <li><a href="https://www.gco.com/doc/cat/gco/-2025-informe-situacio-financera-i-solvencia---gco/2025_sfcr_gco.pdf">Grupo Catalana Occidente, informe de solvencia 2025</a> {tag('oficial')}</li>
    <li><a href="https://forbes.es/etiqueta/coca-cola-europacific-partners/">Forbes España, etiqueta de Coca-Cola Europacific (titular sobre Olive Partners)</a> {tag('prensa')}</li>
    <li><a href="https://www.esdiario.com/chismografo/251111/171985/ortega-thyssen-koplowitz-100-mujeres-ricas-espana-suman-56-000-m-euros.html">ESdiario: 177 M€ de dividendos de la familia Daurella</a> {tag('prensa')}</li>
    <li><a href="https://en.wikipedia.org/wiki/Daniel_Mat%C3%A9">Wikipedia sobre Daniel Maté, citando a Forbes</a> {tag('prensa')}</li>
    <li><a href="https://www.paxnews.com/news/hotel/iberostar-group-reports-14-cent-revenue-growth-plans-1b-investment-through-2028">PaxNews sobre los resultados de Iberostar de 2025</a> {tag('prensa')}</li>
    <li><a href="https://forbes.es/nombramientos/805744/carlos-march-deja-la-presidencia-de-alba-y-es-sustituido-por-juan-march-de-la-lastra/">Forbes España sobre Alba y los March</a> {tag('prensa')}</li>
    <li><a href="https://asest.es/story/familia-march-inversiones-en-startups/">Asest sobre la propiedad de Banca March y sus SICAV</a> {tag('prensa')}</li>
    <li><a href="https://www.democrata.es/economia/la-sicav-del-fundador-de-pronovias-se-acerca-a-los-1-800-millones-y-sigue-lider-por-patrimonio-hasta-septiembre/">Demócrata (Europa Press): ranking de SICAV hasta septiembre de 2026</a> {tag('prensa')}</li>
    <li><a href="https://forbes.es/?p=132638">Forbes España sobre Palatchi, Pronovias y su SICAV</a> {tag('prensa')}</li>
    <li><a href="https://www.vozpopuli.com/dolcevita/asi-es-alberto-palatchi-fundador-de-pronovias-sus-dos-matrimonios-e-hijos-sus-negocios-su-fortuna-y-su-exclusiva-casa.html">Vozpópuli sobre Galma Capital, de Palatchi</a> {tag('prensa')}</li>
    <li><a href="https://www.vozpopuli.com/economia/empresas/bestinver-alicia_koplowitz-endesa_0_638336187.html">Vozpópuli sobre Morinvest, la SICAV de Koplowitz</a> {tag('prensa')}</li>
    <li><a href="https://es.marketscreener.com/insider/TOMAS-OLIVO-LOPEZ-A28OB8/">MarketScreener sobre Tomás Olivo</a> {tag('prensa')}</li>
    <li><a href="https://www.gamblinginsider.com/es/?p=105786">Gambling Insider sobre Manuel Lao y Merlin</a> {tag('prensa')}</li>
    <li><a href="https://en.ara.cat/economy/manuel-lao-sells-5-12-of-sacyr-for-150-8-million-euros_1_5587799.html">Ara sobre la venta del 5,12% de Sacyr por Lao</a> {tag('prensa')}</li>
    <li><a href="https://inforcapital.com/news/blackstone-vende-el-36-de-su-participaci%C3%B3n-en-cirsa-alantra-colidera-la-operaci%C3%B3n/">Inforcapital sobre la compra de Cirsa por Blackstone en 2018</a> {tag('prensa')}</li>
    <li><a href="https://travelbulletin.co.uk/news/2026-a-key-iberostar-anniversary-new-properties-and-sustainable-strides">Travel Bulletin sobre Iberostar</a> {tag('prensa')}</li>
  </ul>
</section>
'''


if __name__ == "__main__":
    print(f"Inditex: impuesto {IMPUESTO_INDITEX} M€, tipo {TIPO_EMPRESA * 100:.2f}%")
    print(f"Por 100 €: A empresa {is_emp:.2f} + IRPF {irpf_a:.2f} = {tot_a:.2f}, queda {queda_a:.2f}")
    print(f"Por 100 €: B empresa {is_emp:.2f} + holding {is_hold:.2f} = {tot_b:.2f}, queda {queda_b:.2f}")
    print(f"Top 25: {SUMA_TOP25} M€ = {SUMA_TOP25 / TOTAL_LISTA * 100:.1f}% ; Ortega {125200 / TOTAL_LISTA * 100:.1f}%")
    for nom, div, b_ok, *_ in ESC:
        print(f"{nom:22s} div {div:8.1f}  A {div * IRPF_AHORRO:7.1f}  B {div * EXENCION:6.2f}")
    print(f"Ortega A {ORTEGA_A:.1f} vs ITSGF 2023 {ITSGF_2023} y 2025 x{ORTEGA_A / ITSGF_2025:.1f}")
    print(f"Pérez IRPF sueldo {IRPF_PEREZ:.2f}, Roig {IRPF_ROIG:.2f}")
    print(f"Con dividendo atribuible: {len(CON_DIVIDENDO)} de 25; sin él: {25 - len(CON_DIVIDENDO)}")
    print(f"SICAV Del Pino {SICAV_DELPINO}; top 25 identificadas {SICAV_TOP25}; Gesprisa/fortuna {GESPRISA_SOBRE_FORTUNA:.1f}%")
    print(f"Herrero {HERRERO_DIV:.2f}; María {MARIA_DIV:.2f}; Roig/total {ROIG_DIV / MERCADONA_DIV * 100:.1f}%")
