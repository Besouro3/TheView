import math

import numpy as np
import pandas as pd

from src.ui import formatear_dinero


def _pct(parte: float, total: float) -> float:
    return (parte / total * 100) if total else 0.0


def _top_bottom(df: pd.DataFrame, grupo: str, valor: str):
    agg = df.groupby(grupo, as_index=False)[valor].sum().sort_values(valor, ascending=False)
    return agg, agg.iloc[0], agg.iloc[-1]


def leer_barras(df: pd.DataFrame, grupo: str, valor: str):
    agg, top, bottom = _top_bottom(df, grupo, valor)
    total = agg[valor].sum()
    n = len(agg)
    frases, recos = [], []
    if n < 1:
        return frases, recos
    pct_top = _pct(top[valor], total)
    frases.append(
        f"**{top[grupo]}** lidera con **{formatear_dinero(top[valor])}**, "
        f"el **{pct_top:.0f}%** de las ventas totales ({formatear_dinero(total)})."
    )
    if n >= 2:
        brecha = _pct(top[valor] - bottom[valor], bottom[valor])
        pct_bottom = _pct(bottom[valor], total)
        frases.append(
            f"En el último puesto está **{bottom[grupo]}** con {formatear_dinero(bottom[valor])} "
            f"({pct_bottom:.0f}% del total), un **{brecha:.0f}%** por debajo del líder."
        )
        if pct_top >= 40:
            recos.append(
                f"**{top[grupo]}** concentra el {pct_top:.0f}% del negocio. "
                "Si ese segmento se cae, cae todo: prioriza diversificar."
            )
    prom = total / n if n else 0
    debiles = agg[agg[valor] < prom * 0.6]
    if len(debiles):
        nombres = ", ".join(f"**{g}**" for g in debiles[grupo].head(3))
        recos.append(
            f"{nombres} rinde(n) por debajo del 60% del promedio. "
            "Revisa inventario, precios o demanda en esos segmentos."
        )
    return frases, recos


def leer_lineas(df: pd.DataFrame, fecha: str, valor: str):
    serie = df.copy()
    serie["_mes"] = serie[fecha].dt.to_period("M").astype(str)
    agg = serie.groupby("_mes", as_index=False)[valor].sum().sort_values("_mes")
    frases, recos = [], []
    mom = 0.0
    n = len(agg)
    if n < 2:
        return frases, recos
    primero, ultimo = agg[valor].iloc[0], agg[valor].iloc[-1]
    variacion = _pct(ultimo - primero, primero)
    direccion = "suben" if variacion >= 0 else "bajan"
    frases.append(
        f"Entre **{agg['_mes'].iloc[0]}** y **{agg['_mes'].iloc[-1]}**, las ventas "
        f"**{direccion}** un **{abs(variacion):.1f}%** "
        f"({formatear_dinero(primero)} → {formatear_dinero(ultimo)})."
    )
    mit = n // 2
    if mit >= 1:
        mitad1, mitad2 = agg[valor].iloc[:mit].sum(), agg[valor].iloc[mit:].sum()
        if mitad1 > 0:
            comp = _pct(mitad2 - mitad1, mitad1)
            frases.append(
                f"La segunda mitad del período acumula **{'+' if comp >= 0 else ''}{comp:.1f}%** "
                f"más que la primera ({formatear_dinero(mitad2)} vs {formatear_dinero(mitad1)})."
            )
    if n >= 4:
        recientes, previos = agg[valor].iloc[-3:].sum(), agg[valor].iloc[-6:-3].sum()
        if previos > 0:
            mom = _pct(recientes - previos, previos)
            frases.append(
                f"El ritmo reciente (últimos 3 meses) va **{mom:+.1f}%** "
                "respecto a los 3 meses anteriores."
            )
    mes_max = agg.loc[agg[valor].idxmax(), "_mes"]
    mes_min = agg.loc[agg[valor].idxmin(), "_mes"]
    frases.append(f"El mejor mes fue **{mes_max}**; el más flojo, **{mes_min}**.")
    if variacion < 0:
        recos.append(
            "La tendencia general es negativa. Compara los últimos 3 meses contra los 3 anteriores "
            "para distinguir una estacionalidad normal de un problema estructural."
        )
    elif variacion > 20:
        recos.append(
            "Crecimiento fuerte en el período. Identifica qué lo impulsó "
            "(campaña, producto, temporada) para repetirlo."
        )
    if mom < -10:
        recos.append(
            f"El ritmo reciente se está enfriando ({mom:.1f}%): no asumas que el crecimiento sigue; "
            "actúa antes de que se revierta la tendencia."
        )
    return frases, recos


def leer_pie(df: pd.DataFrame, grupo: str, valor: str):
    agg, top, _ = _top_bottom(df, grupo, valor)
    total = agg[valor].sum()
    frases, recos = [], []
    if len(agg) < 1 or total <= 0:
        return frases, recos
    pct_top = _pct(top[valor], total)
    frases.append(f"**{top[grupo]}** es el segmento dominante: **{pct_top:.0f}%** del total.")
    if len(agg) >= 2:
        segundo = agg.iloc[1]
        pct_seg = _pct(segundo[valor], total)
        frases.append(f"Le sigue **{segundo[grupo]}** con **{pct_seg:.0f}%**.")
        pct_top2 = pct_top + pct_seg
        if pct_top2 >= 50:
            frases.append(f"Entre ambos concentran el **{pct_top2:.0f}%** de las ventas.")
            recos.append(
                f"**{top[grupo]}** y **{segundo[grupo]}** suman más de la mitad del negocio: "
                "son tu prioridad de abastecimiento y promoción."
            )
        elif pct_top < 30:
            recos.append(
                "El mercado está muy repartido y nadie domina: "
                "diferenciarte puede darte una ventaja real."
            )
    return frases, recos


def leer_calor(df: pd.DataFrame, fila: str, col: str, valor: str):
    pivot = df.pivot_table(index=fila, columns=col, values=valor, aggfunc="sum", fill_value=0)
    frases, recos = [], []
    if not pivot.size or pivot.values.sum() <= 0:
        return frases, recos
    idx_max = np.unravel_index(np.argmax(pivot.values), pivot.shape)
    idx_min = np.unravel_index(np.argmin(pivot.values), pivot.shape)
    total = pivot.values.sum()
    mejor, peor = pivot.values[idx_max], pivot.values[idx_min]
    frases.append(
        f"La combinación más fuerte es **{pivot.index[idx_max[0]]} × {pivot.columns[idx_max[1]]}** "
        f"({formatear_dinero(mejor)}, **{_pct(mejor, total):.0f}%** del total); "
        f"la más débil, **{pivot.index[idx_min[0]]} × {pivot.columns[idx_min[1]]}** "
        f"({formatear_dinero(peor)}, {_pct(peor, total):.0f}%)."
    )
    totales_fila = pivot.sum(axis=1)
    prom_fila = totales_fila.mean()
    if prom_fila > 0:
        mas_alta, mas_baja = totales_fila.idxmax(), totales_fila.idxmin()
        brecha = _pct(totales_fila.max() - totales_fila.min(), totales_fila.min())
        frases.append(
            f"En zonas, **{mas_alta}** lidera y **{mas_baja}** queda un **{brecha:.0f}%** por debajo de la líder."
        )
        ratio = _pct(totales_fila.min(), prom_fila)
        if ratio < 70:
            recos.append(
                f"**{mas_baja}** rinde muy por debajo del promedio. "
                "Revisa cobertura comercial, precios o demanda ahí antes de invertir más."
            )
    return frases, recos


def leer_box(df: pd.DataFrame, grupo: str, valor: str):
    frases, recos = [], []
    resumen = {}
    for g in sorted(df[grupo].dropna().unique()):
        s = df[df[grupo] == g][valor].dropna().astype(float)
        if len(s) >= 2:
            resumen[g] = s
    if not resumen:
        return frases, recos
    if len(resumen) >= 2:
        por_mediana = sorted(resumen.items(), key=lambda kv: kv[1].median())
        minimo_g, maximo_g = por_mediana[0], por_mediana[-1]
        frases.append(
            f"La operación típica (mediana) vale **{formatear_dinero(maximo_g[1].median())}** "
            f"en **{maximo_g[0]}** frente a **{formatear_dinero(minimo_g[1].median())}** en **{minimo_g[0]}**."
        )
    dispersiones = {g: s.quantile(0.75) - s.quantile(0.25) for g, s in resumen.items()}
    mas_var = max(dispersiones.items(), key=lambda kv: kv[1])
    q1, q3 = resumen[mas_var[0]].quantile([0.25, 0.75])
    iqr = q3 - q1
    s = resumen[mas_var[0]]
    n_out = int(((s < q1 - 1.5 * iqr) | (s > q3 + 1.5 * iqr)).sum())
    frases.append(
        f"**{mas_var[0]}** tiene la mayor variabilidad (rango intercuartil "
        f"{formatear_dinero(iqr)}) y registra **{n_out}** valores atípicos."
    )
    if n_out > 0:
        recos.append(
            f"En **{mas_var[0]}** hay {n_out} registros fuera de lo normal. "
            "Valida si son errores de captura, pedidos grandes o una línea con otro comportamiento."
        )
    return frases, recos


def leer_histograma(df: pd.DataFrame, valor: str):
    from scipy import stats as scipy_stats

    s = df[valor].dropna().astype(float)
    frases, recos = [], []
    if len(s) < 2:
        return frases, recos
    media, mediana = s.mean(), s.median()
    cv = s.std() / media * 100 if media else 0
    frases.append(
        f"Promedio **{formatear_dinero(media)}** con una variabilidad del **{cv:.0f}%** "
        f"(desviación estándar {formatear_dinero(s.std())})."
    )
    skew = float(scipy_stats.skew(s)) if len(s) >= 8 else 0.0
    if not math.isfinite(skew):
        skew = 0.0
    if abs(skew) < 0.5:
        frases.append(
            "La distribución es **bastante simétrica**: la mayoría de operaciones "
            "se agrupa alrededor del promedio."
        )
    elif skew > 0:
        frases.append(
            f"Está **sesgada a la derecha** (asimetría {skew:.1f}): la mayoría de operaciones es menor "
            f"que {formatear_dinero(media)} y unas pocas ventas grandes elevan el promedio."
        )
        recos.append(
            f"Usa la **mediana** ({formatear_dinero(mediana)}) como meta realista; "
            "la media se infla por pocas ventas grandes."
        )
    else:
        frases.append(
            f"Está **sesgada a la izquierda** (asimetría {skew:.1f}): abundan los valores altos "
            "y escasean los bajos."
        )
    return frases, recos


def leer_dispersion(df: pd.DataFrame, x: str, y: str):
    datos = df[[x, y]].dropna().astype(float)
    frases, recos = [], []
    if len(datos) < 3:
        return frases, recos
    r = float(np.corrcoef(datos[x], datos[y])[0, 1])
    fuerza = ("muy fuerte" if abs(r) >= 0.8 else
              ("fuerte" if abs(r) >= 0.6 else
               ("moderada" if abs(r) >= 0.4 else "débil")))
    sentido = "positiva" if r >= 0 else "negativa"
    frases.append(f"Correlación **{fuerza} {sentido}** entre **{x}** y **{y}** (r = {r:.2f}).")
    if abs(r) >= 0.6:
        if r > 0:
            frases.append(
                f"Cuando **{x}** sube, **{y}** sube en la misma dirección: se comportan como un solo factor."
            )
            recos.append(
                f"Como se mueven juntos (r={r:.2f}), puedes usar **{x}** para proyectar **{y}**."
            )
        else:
            frases.append(f"Cuando **{x}** sube, **{y}** baja: son sustitutos o se compensan.")
    elif abs(r) < 0.2:
        recos.append(
            "No hay relación lineal entre ambas variables: no uses una para predecir la otra."
        )
    return frases, recos
