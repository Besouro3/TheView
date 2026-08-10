import os
import sys

import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src import cargador, estadistica, graficos, insights
from src.ui import (PALETAS, RED, TEAL, cabecera, formatear_dinero,
                    formatear_monto_corto, inyectar_css, inyectar_tema, kpi,
                    mostrar_grafico, mostrar_lectura, mostrar_recomendaciones,
                    mostrar_tabla, tarjeta_kpi)

st.set_page_config(page_title="The View", layout="wide")


def _guardar_df(df, meta=None) -> None:
    st.session_state["df"] = df
    st.session_state["meta"] = meta or cargador.detectar_columnas(df)


def _limpiar_todo() -> None:
    fuente = st.session_state.get("fuente", "ejemplo")
    for k in ["df", "meta", "filtro_sector", "filtro_region", "filtro_rango",
              "sel_valor", "sel_grupo", "sel_region", "sel_fecha",
              "col_valor", "col_grupo", "col_region", "col_fecha",
              "comp_a", "comp_b", "disp_x", "disp_y", "archivo_subido"]:
        st.session_state.pop(k, None)
    st.session_state["fuente_cargada"] = fuente
    st.rerun()


def _aplicar_filtros(df: pd.DataFrame, meta: dict):
    filtrado = df.copy()
    if meta.get("grupo") and st.session_state.get("filtro_sector"):
        filtrado = filtrado[filtrado[meta["grupo"]].isin(st.session_state["filtro_sector"])]
    if meta.get("region") and st.session_state.get("filtro_region"):
        filtrado = filtrado[filtrado[meta["region"]].isin(st.session_state["filtro_region"])]
    if meta.get("fecha"):
        rango = st.session_state.get("filtro_rango")
        if rango:
            col = pd.to_datetime(filtrado[meta["fecha"]])
            filtrado = filtrado[(col.dt.date >= rango[0]) & (col.dt.date <= rango[1])]
    return filtrado


def _sidebar(fuente: str):
    with st.sidebar:
        st.header("Fuente de datos")
        fuente = st.radio(
            "¿De dónde leo la información?",
            ["Datos de ejemplo", "Subir archivo (CSV/Excel)", "Base de datos"],
            label_visibility="collapsed",
            key="fuente_opcion",
        )
        if fuente == "Datos de ejemplo":
            st.session_state["fuente"] = "ejemplo"
            if st.session_state.get("fuente_cargada") != "ejemplo":
                try:
                    _guardar_df(cargador.datos_ejemplo())
                    st.session_state["fuente_cargada"] = "ejemplo"
                except Exception as e:
                    st.error(f"No se pudieron cargar los datos de ejemplo: {e}")
        elif fuente == "Subir archivo (CSV/Excel)":
            st.session_state["fuente"] = "archivo"
            archivo = st.file_uploader("CSV o Excel", type=["csv", "xlsx", "xls"], key="archivo_subido")
            if archivo is not None:
                try:
                    _guardar_df(cargador.datos_archivo(archivo))
                    st.session_state["fuente_cargada"] = "archivo"
                except Exception as e:
                    st.error(f"No se pudo leer el archivo: {e}")
        else:
            st.session_state["fuente"] = "bd"
            with st.form("form_bd"):
                tipo = st.selectbox("Motor", ["MySQL", "PostgreSQL"])
                host = st.text_input("Host", value="localhost")
                puerto = st.text_input("Puerto", value="3306" if tipo == "MySQL" else "5432")
                usuario = st.text_input("Usuario")
                clave = st.text_input("Contraseña", type="password")
                base = st.text_input("Base de datos")
                tabla = st.text_input("Tabla")
                conectado = st.form_submit_button("Conectar")
            if conectado:
                try:
                    df = cargador.datos_base_datos(tipo, host, puerto, usuario, clave, base, tabla)
                    st.session_state["df"] = df
                    st.session_state["meta"] = cargador.detectar_columnas(df)
                    st.session_state["fuente_cargada"] = "bd"
                    st.success("Conectado")
                except Exception as e:
                    st.error(f"Error de conexión: {e}")

        if st.session_state.get("df") is not None:
            st.divider()
            if st.button("🗑️ Limpiar todo", use_container_width=True,
                         help="Borra los datos, los filtros y las selecciones para empezar de nuevo."):
                _limpiar_todo()

        if st.session_state.get("df") is None:
            st.info("Carga los datos para comenzar.")
            if st.button("Usar datos de ejemplo", use_container_width=True):
                try:
                    _guardar_df(cargador.datos_ejemplo())
                    st.session_state["fuente_cargada"] = "ejemplo"
                    st.rerun()
                except Exception as e:
                    st.error(f"No se pudieron cargar los datos de ejemplo: {e}")
            return


def _filtros_sidebar(meta: dict, df: pd.DataFrame):
    with st.sidebar:
        st.divider()
        st.header("Filtros")
        if meta.get("grupo") and len(df[meta["grupo"]].dropna().unique()) <= 40:
            opciones = sorted(df[meta["grupo"]].dropna().unique())
            st.multiselect(f"Filtrar {meta['grupo']}", opciones, key="filtro_sector")
        if meta.get("region"):
            opciones = sorted(df[meta["region"]].dropna().unique())
            st.multiselect(f"Filtrar {meta['region']}", opciones, key="filtro_region")
        if meta.get("fecha"):
            col_fecha = pd.to_datetime(df[meta["fecha"]])
            minimo, maximo = col_fecha.min().date(), col_fecha.max().date()
            if minimo != maximo:
                st.date_input(
                    "Rango de fechas", value=(minimo, maximo), min_value=minimo,
                    max_value=maximo, key="filtro_rango",
                )

        st.divider()
        st.header("Columnas detectadas")
        col_valor = st.selectbox(
            "Columna de valor (dinero)",
            meta["numericas"] or [], index=meta["numericas"].index(meta["valor"]) if meta["valor"] in meta["numericas"] else 0,
            key="sel_valor",
        )
        col_grupo = st.selectbox(
            "Columna de grupo",
            ["—"] + meta["textos"], index=0,
            key="sel_grupo",
        )
        col_region = st.selectbox(
            "Columna de zona/región",
            ["—"] + meta["textos"], index=0,
            key="sel_region",
        )
        col_fecha = st.selectbox(
            "Columna de fecha",
            ["—"] + [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])],
            index=0, key="sel_fecha",
        )
        st.session_state["col_valor"] = col_valor
        st.session_state["col_grupo"] = None if col_grupo == "—" else col_grupo
        st.session_state["col_region"] = None if col_region == "—" else col_region
        st.session_state["col_fecha"] = None if col_fecha == "—" else col_fecha


def _meta_efectiva(meta: dict) -> dict:
    return {
        "valor": st.session_state.get("col_valor") or meta.get("valor"),
        "grupo": st.session_state.get("col_grupo") or meta.get("grupo"),
        "region": st.session_state.get("col_region") or meta.get("region"),
        "fecha": st.session_state.get("col_fecha") or meta.get("fecha"),
    }


def _mensual(df, fecha, valor):
    serie = df.copy()
    serie["_mes"] = serie[fecha].dt.to_period("M").astype(str)
    return serie.groupby("_mes", as_index=False)[valor].sum().sort_values("_mes")


def _delta_reciente(df, fecha, valor):
    if not fecha:
        return None
    g = _mensual(df, fecha, valor)
    if len(g) < 6:
        return None
    prev = g[valor].iloc[-6:-3].sum()
    rec = g[valor].iloc[-3:].sum()
    if prev <= 0:
        return None
    return (rec - prev) / prev * 100


def _spark_mensual(df, fecha, valor):
    if not fecha:
        return None
    g = _mensual(df, fecha, valor).tail(6)
    vals = g[valor].tolist()
    if not vals or max(vals) <= 0:
        return None
    mx = max(vals)
    return [int(v / mx * 44) for v in vals]


def _pestania_resumen(df: pd.DataFrame, meta: dict):
    st.subheader("Resumen ejecutivo")
    valor = meta.get("valor")
    if not valor:
        st.warning("No se detectó una columna de valor numérico.")
        return
    total = df[valor].sum()
    registros = len(df)
    prom = df[valor].mean()

    mejor_g, mejor_pct = None, None
    peor_g, peor_pct = None, None
    if meta.get("grupo"):
        agg = df.groupby(meta["grupo"])[valor].sum().sort_values(ascending=False)
        total_g = agg.sum()
        if total_g > 0:
            mejor_g, mejor_pct = agg.index[0], agg.iloc[0] / total_g * 100
            peor_g, peor_pct = agg.index[-1], agg.iloc[-1] / total_g * 100

    delta = _delta_reciente(df, meta.get("fecha"), valor)
    spark = _spark_mensual(df, meta.get("fecha"), valor)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(tarjeta_kpi(
            "Ventas totales", formatear_monto_corto(total), icono="trending_up",
            sub=f"{registros:,} registros",
            delta=f"{'+' if (delta or 0) >= 0 else ''}{delta:.1f}%" if delta is not None else None,
            delta_sube=(delta or 0) >= 0,
        ), unsafe_allow_html=True)
    with c2:
        st.markdown(tarjeta_kpi(
            "Mejor", str(mejor_g or "—"), icono="star", icono_clase="star",
            valor_sm=True,
            bar=mejor_pct if mejor_pct is not None else None,
            bar_color="var(--tertiary)",
            bar_label=f"{mejor_pct:.0f}% de participación" if mejor_pct is not None else "",
        ), unsafe_allow_html=True)
    with c3:
        st.markdown(tarjeta_kpi(
            "Peor", str(peor_g or "—"), icono="warning", icono_clase="warn",
            valor_sm=True,
            bar=peor_pct if peor_pct is not None else None,
            bar_color="var(--error)",
            bar_label=f"{peor_pct:.0f}% de participación" if peor_pct is not None else "",
        ), unsafe_allow_html=True)
    with c4:
        st.markdown(tarjeta_kpi(
            "Promedio por operación", formatear_monto_corto(prom), icono="show_chart",
            spark=spark,
        ), unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1])
    with c1:
        if meta.get("grupo"):
            mostrar_grafico(graficos.grafico_barras(df, meta["grupo"], valor))
            mostrar_lectura(insights.leer_barras(df, meta["grupo"], valor)[0])
    with c2:
        if meta.get("fecha"):
            mostrar_grafico(graficos.grafico_lineas(df, meta["fecha"], valor))
            mostrar_lectura(insights.leer_lineas(df, meta["fecha"], valor)[0])
        else:
            mostrar_grafico(graficos.grafico_pie(df, meta["grupo"], valor))
            mostrar_lectura(insights.leer_pie(df, meta["grupo"], valor)[0])


def _pestania_graficos(df: pd.DataFrame, meta: dict):
    st.subheader("Gráficos")
    valor = meta.get("valor")
    if not valor:
        st.warning("No se detectó una columna de valor numérico.")
        return
    tipo = st.selectbox(
        "Tipo de gráfico",
        ["Barras por grupo", "Evolución temporal", "Distribución (pastel)",
         "Mapa de calor", "Cajas (box plot)", "Histograma", "Dispersión"],
    )
    if tipo == "Barras por grupo" and meta.get("grupo"):
        mostrar_grafico(graficos.grafico_barras(df, meta["grupo"], valor))
        mostrar_lectura(insights.leer_barras(df, meta["grupo"], valor)[0])
        mostrar_recomendaciones(insights.leer_barras(df, meta["grupo"], valor)[1])
    elif tipo == "Evolución temporal" and meta.get("fecha"):
        mostrar_grafico(graficos.grafico_lineas(df, meta["fecha"], valor))
        mostrar_lectura(insights.leer_lineas(df, meta["fecha"], valor)[0])
        mostrar_recomendaciones(insights.leer_lineas(df, meta["fecha"], valor)[1])
    elif tipo == "Distribución (pastel)" and meta.get("grupo"):
        mostrar_grafico(graficos.grafico_pie(df, meta["grupo"], valor))
        mostrar_lectura(insights.leer_pie(df, meta["grupo"], valor)[0])
        mostrar_recomendaciones(insights.leer_pie(df, meta["grupo"], valor)[1])
    elif tipo == "Mapa de calor" and meta.get("region") and meta.get("grupo"):
        mostrar_grafico(graficos.grafico_calor(df, meta["region"], meta["grupo"], valor))
        mostrar_lectura(insights.leer_calor(df, meta["region"], meta["grupo"], valor)[0])
        mostrar_recomendaciones(insights.leer_calor(df, meta["region"], meta["grupo"], valor)[1])
    elif tipo == "Cajas (box plot)" and meta.get("grupo"):
        mostrar_grafico(graficos.grafico_box(df, meta["grupo"], valor))
        mostrar_lectura(insights.leer_box(df, meta["grupo"], valor)[0])
        mostrar_recomendaciones(insights.leer_box(df, meta["grupo"], valor)[1])
    elif tipo == "Histograma":
        mostrar_grafico(graficos.grafico_histograma(df, valor))
        mostrar_lectura(insights.leer_histograma(df, valor)[0])
        mostrar_recomendaciones(insights.leer_histograma(df, valor)[1])
    elif tipo == "Dispersión":
        numericas = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
        if len(numericas) >= 2:
            x = st.selectbox("Eje X", numericas, index=0, key="disp_x")
            y = st.selectbox("Eje Y", numericas, index=min(1, len(numericas) - 1), key="disp_y")
            mostrar_grafico(graficos.grafico_dispersion(df, x, y))
            mostrar_lectura(insights.leer_dispersion(df, x, y)[0])
            mostrar_recomendaciones(insights.leer_dispersion(df, x, y)[1])


def _pestania_insights(df: pd.DataFrame, meta: dict):
    st.subheader("Insights y recomendaciones")
    st.caption("Todas las lecturas automáticas del tablero reunidas en un solo lugar.")
    valor = meta.get("valor")
    if not valor:
        st.warning("No se detectó una columna de valor numérico.")
        return

    bloques = []
    if meta.get("grupo"):
        f, r = insights.leer_barras(df, meta["grupo"], valor)
        bloques.append(("Mejores y peores por grupo", f, r))
        f, r = insights.leer_pie(df, meta["grupo"], valor)
        bloques.append(("Concentración por grupo", f, r))
    if meta.get("fecha"):
        f, r = insights.leer_lineas(df, meta["fecha"], valor)
        bloques.append(("Tendencia temporal", f, r))
    if meta.get("region") and meta.get("grupo"):
        f, r = insights.leer_calor(df, meta["region"], meta["grupo"], valor)
        bloques.append(("Análisis por zona", f, r))
    if meta.get("grupo"):
        f, r = insights.leer_box(df, meta["grupo"], valor)
        bloques.append(("Dispersión y atípicos", f, r))
    f, r = insights.leer_histograma(df, valor)
    bloques.append(("Forma de la distribución", f, r))

    for titulo, frases, recos in bloques:
        with st.expander(titulo, expanded=True):
            mostrar_lectura(frases)
            mostrar_recomendaciones(recos)


def _pestania_comparar(df: pd.DataFrame, meta: dict):
    st.subheader("Comparar")
    valor = meta.get("valor")
    if not valor or not meta.get("grupo"):
        st.warning("Se necesita una columna de grupo para comparar.")
        return
    grupos = sorted(df[meta["grupo"]].dropna().unique())
    c = st.columns(2)
    g1 = c[0].selectbox("Grupo A", grupos, key="comp_a")
    g2 = c[1].selectbox("Grupo B", grupos, index=min(1, len(grupos) - 1), key="comp_b")
    if g1 == g2:
        st.warning("Elige dos grupos distintos.")
        return
    d1, d2 = df[df[meta["grupo"]] == g1], df[df[meta["grupo"]] == g2]
    t1, t2 = d1[valor].sum(), d2[valor].sum()
    if t2 != 0:
        dif = (t1 - t2) / t2 * 100
        kpi(f"Grupo A: {g1}", formatear_dinero(t1), f"vs {g2}: {dif:+.1f}%", TEAL if dif >= 0 else RED)
        kpi(f"Grupo B: {g2}", formatear_dinero(t2), f"{len(d1):,} vs {len(d2):,} registros", TEAL)
    cc = st.columns(2)
    with cc[0]:
        mostrar_grafico(graficos.grafico_lineas(d1, meta["fecha"], valor) if meta.get("fecha") else graficos.grafico_histograma(d1, valor))
    with cc[1]:
        mostrar_grafico(graficos.grafico_lineas(d2, meta["fecha"], valor) if meta.get("fecha") else graficos.grafico_histograma(d2, valor))
    mostrar_grafico(graficos.grafico_pie(pd.concat([d1, d2]), meta["grupo"], valor))


def _pestania_estadistica(df: pd.DataFrame, meta: dict):
    st.subheader("Estadística")
    valor = meta.get("valor")
    if not valor:
        st.warning("No se detectó una columna de valor numérico.")
        return
    resumen = estadistica.resumen_estadistico(df, valor)
    filas = [
        ("Registros", f"{resumen['registros']:,}"),
        ("Media", formatear_dinero(resumen["media"])),
        ("Mediana", formatear_dinero(resumen["mediana"])),
        ("Desviación estándar", formatear_dinero(resumen["desviacion"])),
        ("Mínimo", formatear_dinero(resumen["minimo"])),
        ("Cuartil 1", formatear_dinero(resumen["q1"])),
        ("Cuartil 3", formatear_dinero(resumen["q3"])),
        ("Máximo", formatear_dinero(resumen["maximo"])),
    ]
    c = st.columns(4)
    for i, (label, val) in enumerate(filas):
        with c[i % 4]:
            kpi(label, val, "", "#E2E8F0")

    outliers = estadistica.detectar_outliers(df, valor)
    cc = st.columns(2)
    with cc[0]:
        if meta.get("grupo"):
            mostrar_grafico(graficos.grafico_box(df, meta["grupo"], valor))
    with cc[1]:
        mostrar_grafico(graficos.grafico_histograma(df, valor))
        if len(outliers):
            st.error(f"{len(outliers):,} valores atípicos detectados (método 1.5×IQR).")
        else:
            st.success("Sin valores atípicos detectados.")

    if len(outliers):
        st.subheader("Registros atípicos")
        mostrar_tabla(outliers.head(100))


def _pestania_explorador(df: pd.DataFrame):
    st.subheader("Explorador")
    st.caption("Arrastra columnas para crear tus propios gráficos en segundos.")
    try:
        from pygwalker.api.streamlit import StreamlitRenderer
        if "renderer" not in st.session_state:
            st.session_state["renderer"] = StreamlitRenderer(df, spec_io_mode="rw")
        st.session_state["renderer"].explorer()
    except Exception as e:
        st.warning(f"No se pudo cargar el Explorador ({e}). Usa las pestañas de gráficos.")


def main() -> None:
    if st.session_state.get("tema") not in ("Oscuro", "Sistema"):
        st.session_state["tema"] = "Oscuro"
    modo = st.session_state.get("tema", "Oscuro")
    paleta = st.session_state.get("paleta", "Esmeralda")
    inyectar_css()
    inyectar_tema(modo, paleta)
    datos_paleta = PALETAS.get(paleta) or PALETAS["Esmeralda"]
    graficos.set_tema(modo != "Claro", datos_paleta["oscuro" if modo != "Claro" else "claro"]["acento"])

    _sidebar(st.session_state.get("fuente", "ejemplo"))
    df = st.session_state.get("df")
    if df is None:
        cabecera(None, None)
        return
    meta = cargador.detectar_columnas(df)
    _filtros_sidebar(meta, df)
    df_filtrado = _aplicar_filtros(df, meta)
    meta_ef = _meta_efectiva(meta)

    if df_filtrado.empty:
        cabecera(df, meta)
        st.warning("Los filtros dejaron el tablero sin datos. Quita algún filtro.")
        return

    cabecera(df_filtrado, meta_ef)

    t1, t2, t3, t4, t5, t6 = st.tabs(
        ["Resumen", "Gráficos", "Insights", "Comparar", "Estadística", "Explorador"]
    )
    with t1:
        _pestania_resumen(df_filtrado, meta_ef)
    with t2:
        _pestania_graficos(df_filtrado, meta_ef)
    with t3:
        _pestania_insights(df_filtrado, meta_ef)
    with t4:
        _pestania_comparar(df_filtrado, meta_ef)
    with t5:
        _pestania_estadistica(df_filtrado, meta_ef)
    with t6:
        _pestania_explorador(df_filtrado)


if __name__ == "__main__":
    main()
