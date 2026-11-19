"""Bloque «Dentro de las cotizaciones» de la pestaña 1: por régimen, quién las paga y autónomos.

Las cifras derivadas salen de las constantes de abajo. build.py sustituye {{COTIZ}} en body.html.
"""
from tab8 import n, tag, tr

# ---- Cotizaciones de 2025 (M€), nota del Ministerio de Inclusión de 31-3-2026 -------------
TOTAL = 176918
OCUPADOS = 167042
REG_GENERAL = 136484
ESPECIALES = 12609                      # Autónomos + Mar + Minería del Carbón, juntos
DESEMPLEADOS = 9876
OTROS = OCUPADOS - REG_GENERAL - ESPECIALES   # inferido por resta
assert REG_GENERAL + ESPECIALES + OTROS + DESEMPLEADOS == TOTAL
assert OCUPADOS + DESEMPLEADOS == TOTAL

# ---- Tipos legales 2026, Régimen General, contrato indefinido (Orden PJC/297/2026) --------
TIPOS = [
    # concepto, empresa, trabajador
    ("Contingencias comunes", 23.60, 4.70),
    ("Desempleo (contrato indefinido)", 5.50, 1.55),
    ("Fondo de Garantía Salarial", 0.20, 0.00),
    ("Formación profesional", 0.60, 0.10),
    ("Mecanismo de Equidad Intergeneracional (MEI)", 0.75, 0.15),
]
T_EMP = sum(e for _, e, _ in TIPOS)
T_TRA = sum(t for _, _, t in TIPOS)
T_TOT = T_EMP + T_TRA
P_EMP = T_EMP / T_TOT * 100
P_TRA = 100 - P_EMP
assert round(T_EMP, 2) == 30.65 and round(T_TRA, 2) == 6.50

# ---- Eurostat (ESSPROS) vía Eustat, 2023, % de los ingresos de protección social ----------
ES_EMPLEADORES, ES_PERSONAS = 42.9, 11.5
UE_EMPLEADORES, UE_PERSONAS = 35.1, 21.0
ES_P_EMP = ES_EMPLEADORES / (ES_EMPLEADORES + ES_PERSONAS) * 100
UE_P_EMP = UE_EMPLEADORES / (UE_EMPLEADORES + UE_PERSONAS) * 100

# ---- Autónomos ---------------------------------------------------------------------------------
AFIL_AUT = 3_425_767                    # RETA y SETA, diciembre de 2025
AFIL_TOT = 21_844_414                   # afiliados medios, diciembre de 2025
AFIL_RG = 18_350_000                    # Régimen General, diciembre de 2025 (18,35 M)
RETA_ENE_AGO, TOT_ENE_AGO = 8064, 117248
BASE_MINIMA_N, BASE_MINIMA_TOT = 818_367, 3_448_635   # 31-3-2026
TIPO_RETA = 0.315
BASE_MIN, BASE_MAX = 653.59, 5101.20
P_AFIL = AFIL_AUT / AFIL_TOT * 100
P_COT_ESP = ESPECIALES / TOTAL * 100
P_RETA = RETA_ENE_AGO / TOT_ENE_AGO * 100
P_BASE_MIN = BASE_MINIMA_N / BASE_MINIMA_TOT * 100
POR_AUT = ESPECIALES * 1e6 / AFIL_AUT
POR_RG = REG_GENERAL * 1e6 / AFIL_RG
CUOTA_MIN = BASE_MIN * TIPO_RETA
CUOTA_MAX = BASE_MAX * TIPO_RETA
TOPE_ANUAL = BASE_MAX * 12


def pct(v, d=1):
    return n(v, d) + "%"


def stack(segs, aria):
    """segs: lista de (clase, ancho %, etiqueta con valor)."""
    bar = "".join(f'<i class="{c}" style="--w:{w:.1f}%"></i>' for c, w, _ in segs)
    vals = "".join(f'<span><b class="k{c[1:]}"></b>{t}</span>' for c, _, t in segs)
    return f'<div class="stackbar" role="img" aria-label="{aria}">{bar}</div>\n    <p class="vals">{vals}</p>'


def html():
    s_reg = stack([
        ("s1", REG_GENERAL / TOTAL * 100, f"Régimen General {n(REG_GENERAL)} M€ ({pct(REG_GENERAL / TOTAL * 100)})"),
        ("s2", ESPECIALES / TOTAL * 100, f"Autónomos, Mar y Minería {n(ESPECIALES)} ({pct(P_COT_ESP)})"),
        ("s4", OTROS / TOTAL * 100, f"Otros conceptos de ocupados {n(OTROS)} ({pct(OTROS / TOTAL * 100)})"),
        ("s3", DESEMPLEADOS / TOTAL * 100, f"Desempleados {n(DESEMPLEADOS)} ({pct(DESEMPLEADOS / TOTAL * 100)})"),
    ], f"Reparto de las cotizaciones de 2025 en millones de euros: Régimen General {n(REG_GENERAL)}, autónomos, Mar y Minería {n(ESPECIALES)}, otros conceptos {n(OTROS)}, desempleados {n(DESEMPLEADOS)}")

    def row3(a, b, c):
        return f'<tr><td>{a}</td><td class="num">{b}</td><td class="num">{c}</td></tr>'

    tipo_rows = "\n        ".join(row3(c, f"{n(e, 2)}%", f"{n(t, 2)}%" if t else "0%") for c, e, t in TIPOS)
    tot_row = row3(f"<strong>Suma</strong> {tag('inferido')}", f"<strong>{n(T_EMP, 2)}%</strong>", f"<strong>{n(T_TRA, 2)}%</strong>")
    atep_row = row3("Accidentes de trabajo y enfermedades profesionales", "variable", "0%")

    s_legal = stack([
        ("s1", P_EMP, f"Empresa {pct(P_EMP)}"),
        ("s2", P_TRA, f"Trabajador {pct(P_TRA)}"),
    ], f"De cada 100 euros de cotización de un asalariado indefinido, la empresa paga {n(P_EMP, 1)} y el trabajador {n(P_TRA, 1)}")
    s_es = stack([
        ("s1", ES_P_EMP, f"Empleadores {pct(ES_P_EMP)}"),
        ("s2", 100 - ES_P_EMP, f"Personas protegidas {pct(100 - ES_P_EMP)}"),
    ], f"España 2023: los empleadores aportan el {n(ES_P_EMP, 1)}% de las cotizaciones y las personas protegidas el {n(100 - ES_P_EMP, 1)}%")
    s_ue = stack([
        ("s1", UE_P_EMP, f"Empleadores {pct(UE_P_EMP)}"),
        ("s2", 100 - UE_P_EMP, f"Personas protegidas {pct(100 - UE_P_EMP)}"),
    ], f"UE-27 2023: los empleadores aportan el {n(UE_P_EMP, 1)}% de las cotizaciones y las personas protegidas el {n(100 - UE_P_EMP, 1)}%")

    def tr(cells, _labels):   # tabla sin etiquetas por celda: en móvil cada fila es un bloque
        a, b = cells
        return f"<tr><td><strong>{a}</strong></td><td>{b}</td></tr>"

    L = None
    aut_rows = "\n        ".join([
        tr(["Autónomos afiliados (RETA y SETA), diciembre de 2025", f"{n(AFIL_AUT)} {tag('oficial')}; ≈{pct(P_AFIL)} de los {n(AFIL_TOT)} afiliados {tag('inferido')}"], L),
        tr(["Cotizaciones de Autónomos, Mar y Minería juntos, 2025", f"{n(ESPECIALES)} M€, el {pct(P_COT_ESP)} del total {tag('oficial')}"], L),
        tr(["Solo el RETA, de enero a agosto de 2025", f"{n(RETA_ENE_AGO)} M€ de {n(TOT_ENE_AGO)} M€, el {pct(P_RETA)} {tag('prensa')}"], L),
        tr(["Cotización media por afiliado y año", f"Autónomo ≈{n(round(POR_AUT, -2))} €; Régimen General ≈{n(round(POR_RG, -2))} € (empresa más trabajador) {tag('inferido')}"], L),
        tr(["Autónomos en el tramo más bajo, 31 de marzo de 2026", f"{n(BASE_MINIMA_N)} de {n(BASE_MINIMA_TOT)}, el {pct(P_BASE_MIN)} {tag('prensa')}"], L),
        tr(["Cuota 2026", f"{pct(TIPO_RETA * 100)} de la base, que el autónomo elige según su rendimiento neto en 15 tramos. Con la base mínima ({n(BASE_MIN, 2)} €): ≈{n(CUOTA_MIN, 0)} € al mes; con la máxima ({n(BASE_MAX, 2)} €): ≈{n(CUOTA_MAX, 0)} € al mes {tag('inferido')}"], L),
    ])

    return f'''<div id="cotiz-detalle" style="margin-top:38px">
  <h3 class="lead">Dentro de las cotizaciones: quién las paga y cuánto aportan los autónomos</h3>
  <p class="prose">Los {n(TOTAL)} M€ de cotizaciones de 2025 no salen de un solo bolsillo. Tres cortes: por régimen, por quién las paga según la ley y por lo que aportan los autónomos.</p>

  <h4 class="sublead">1. Por régimen, 2025</h4>
  <div class="sb-row">
    {s_reg}
    <p class="tot">Total: {n(TOTAL)} M€ {tag('oficial')}</p>
  </div>
  <ul class="notes">
    <li>«Otros conceptos» es una resta mía ({n(OCUPADOS)} de ocupados menos {n(REG_GENERAL)} y {n(ESPECIALES)}) {tag('inferido')}. La nota oficial los agrupa sin cifra: accidentes de trabajo y enfermedades profesionales, MEI, cese de actividad y sistemas especiales.</li>
    <li>Parte de lo que pagan los autónomos (el cese de actividad, por ejemplo) puede estar en ese «otros», así que {n(ESPECIALES)} M€ es un suelo {tag('inferido')}.</li>
  </ul>

  <h4 class="sublead">2. ¿Quién las paga? Según la ley, sobre todo la empresa</h4>
  <p class="prose">Tipos de 2026 del Régimen General para un asalariado con contrato indefinido, en % de la base de cotización {tag('oficial')}. En accidentes de trabajo, la prima depende de la actividad y la paga la empresa entera.</p>
  <div class="tbl-wrap">
    <table class="legend">
      <thead><tr><th>Concepto</th><th class="num">Empresa</th><th class="num">Trabajador</th></tr></thead>
      <tbody>
        {tipo_rows}
        {tot_row}
        {atep_row}
      </tbody>
    </table>
  </div>
  <div class="sb-row">
    <p class="cap">De cada 100 € de cotización de un asalariado indefinido (sin contar accidentes de trabajo)</p>
    {s_legal}
    <p class="tot">La empresa paga el {pct(P_EMP)} {tag('inferido')}</p>
  </div>
  <p class="prose">El dato nacional va en la misma dirección. Eurostat reparte los ingresos de la protección social por quién los aporta; quitando la parte pública, queda esto:</p>
  <div class="sb-row">
    <p class="cap">España, 2023</p>
    {s_es}
  </div>
  <div class="sb-row">
    <p class="cap">Unión Europea (27), 2023</p>
    {s_ue}
    <p class="tot">Los empleadores pagan más en España que en la media europea {tag('inferido')}</p>
  </div>
  <ul class="notes">
    <li>Las dos barras de Eurostat son mi cálculo a partir de dos porcentajes oficiales de 2023: empleadores ({n(ES_EMPLEADORES, 1)}% en España, {n(UE_EMPLEADORES, 1)}% en la UE) y personas protegidas ({n(ES_PERSONAS, 1)}% y {n(UE_PERSONAS, 1)}%) {tag('oficial')} {tag('inferido')}. «Personas protegidas» incluye asalariados, autónomos y pensionistas. Eurostat cuenta también contribuciones imputadas de los empleadores, que no son un pago en efectivo.</li>
    <li><strong>Pagar según la ley no es soportar el coste.</strong> Si la empresa descuenta la cotización de lo que ofrece de sueldo, en la práctica la soporta el trabajador; si la sube a los precios, el cliente. Ninguna fuente usada aquí mide esa incidencia en España, así que la web solo muestra quién paga según la ley.</li>
    <li>Contexto: la cuña fiscal de un salario medio (cotizaciones de empresa y trabajador más IRPF) fue el 40,2% del coste laboral bruto en 2023, según la OCDE que cita la prensa {tag('prensa')}.</li>
    <li>Tope: por encima de la base máxima ({n(BASE_MAX, 2)} € al mes, {n(TOPE_ANUAL, 0)} € al año) solo rige una cotización de solidaridad adicional {tag('oficial')}. Los dividendos y las plusvalías no cotizan a la Seguridad Social. Es decir, la carga recae sobre sueldos hasta ese tope, no sobre las rentas del capital {tag('inferido')}.</li>
  </ul>

  <h4 class="sublead">3. Autónomos: pagan todo ellos, pero aportan menos de lo que pesan</h4>
  <div class="tbl-wrap">
    <table class="plain verdict">
      <thead><tr><th>Dato</th><th>Cifra</th></tr></thead>
      <tbody>
        {aut_rows}
      </tbody>
    </table>
  </div>
  <p class="prose">Uno de cada seis afiliados es autónomo y aportan alrededor del 7% de las cotizaciones. En los datos se ve que casi uno de cada cuatro está en el tramo más bajo, y la cotización de un autónomo depende de lo que él declara como rendimiento neto, no de un sueldo bruto.</p>
  <ul class="notes">
    <li>El autónomo paga el tipo completo él solo; en un asalariado se reparte con la empresa (apartado 2). Por eso la cotización media por afiliado no es comparable euro a euro: la del Régimen General incluye la parte que paga la empresa.</li>
    <li>El cociente por afiliado mezcla los afiliados de diciembre con la recaudación de todo el año, y los {n(ESPECIALES)} M€ incluyen Mar y Minería del Carbón. Es un orden de magnitud {tag('inferido')}.</li>
    <li>Las cuotas de 2026 son base por tipo, no una cifra que publique la Seguridad Social tal cual {tag('inferido')}. Quien tiene sociedad o trabaja como autónomo colaborador tiene una base mínima más alta.</li>
    <li>No encontré cuánto paga de IRPF el colectivo de autónomos. Queda anotado en las lagunas de la pestaña 8.</li>
  </ul>
  <p class="src">Fuentes: <a href="https://www.inclusion.gob.es/en/w/el-deficit-de-la-seguridad-social-se-reduce-al-0-4-del-pib-su-nivel-mas-bajo-desde-2011-gracias-al-incremento-de-los-ingresos-por-cotizaciones-sociales">Ministerio de Inclusión, cotizaciones 2025</a> <span class="tag t-oficial">oficial</span>; <a href="https://www.boe.es/boe/dias/2026/03/31/pdfs/BOE-A-2026-7296.pdf">Orden PJC/297/2026 (BOE)</a> <span class="tag t-oficial">oficial</span>; <a href="https://en.eustat.eus/elementos/ele0003500/social-protection-income-indicators-by-country-horizontal-/tbl0003525_i.html">Eustat con datos de Eurostat (ESSPROS)</a> <span class="tag t-oficial">oficial</span>; <a href="https://www.inclusion.gob.es/w/la-seguridad-social-suma-en-2025-medio-mill%C3%B3n-de-afiliados-por-cuarto-a%C3%B1o-consecutivo-y-se-acerca-a-los-21-9-millones-de-ocupados">Ministerio de Inclusión, afiliación de 2025</a> <span class="tag t-oficial">oficial</span>; <a href="https://forbes.es/?p=852671">Forbes España, afiliados</a>, <a href="https://www.eldebate.com/economia/20251015/mei-crece-325-recaudacion-autonomos-baja-01_344273.html">El Debate, RETA</a>, <a href="https://www.holded.com/es/blog/autonomos-cotizan-base-minima">Holded, base mínima</a>, <a href="https://thecorner.eu/news-spain/spain-economy/spain-the-tax-burden-on-employment-continues-to-rise-and-now-stands-at-40-2-5-4-points-above-the-oecd-average/114294/">The Corner, cuña fiscal</a> <span class="tag t-prensa">prensa</span>.</p>
</div>
'''


if __name__ == "__main__":
    print("OTROS", OTROS)
    print("legal empresa %", round(P_EMP, 2), "trabajador", round(P_TRA, 2), "suma", round(T_EMP, 2), round(T_TRA, 2))
    print("ES empleadores %", round(ES_P_EMP, 2), "UE", round(UE_P_EMP, 2))
    print("afil %", round(P_AFIL, 2), "cot esp %", round(P_COT_ESP, 2), "RETA %", round(P_RETA, 2), "base min %", round(P_BASE_MIN, 2))
    print("por aut", round(POR_AUT), "por RG", round(POR_RG))
    print("cuotas", round(CUOTA_MIN, 2), round(CUOTA_MAX, 2), "tope anual", TOPE_ANUAL)
    print("pcts reg", [round(x / TOTAL * 100, 1) for x in (REG_GENERAL, ESPECIALES, OTROS, DESEMPLEADOS)])
