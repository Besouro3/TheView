# `app.py` — Punto de entrada

## Concepto

Es el archivo que ejecuta Streamlit (`streamlit run app.py`). Orquesta todo: configura la página, inyecta el tema, dibuja la barra lateral (fuente + filtros), aplica los filtros y dibuja las 6 pestañas. Toda la lógica de datos está en `src/`, aquí solo se **coordina**.

Cada vez que el usuario toca algo, Streamlit re-ejecuta `app.py` de arriba a abajo; por eso todo el estado vive en `st.session_state`.

## Flujo de `main()` (app.py:420)

1. Inicializa el tema por defecto (`"Oscuro"`) si no hay uno guardado.
2. Aplica tema y paleta: `inyectar_css()` + `inyectar_tema(modo, paleta)` y `graficos.set_tema(...)` para que los gráficos combinen.
3. Dibuja el sidebar de **fuente de datos** (`_sidebar`).
4. Si no hay datos, muestra la cabecera vacía y termina.
5. Detecta columnas (`cargador.detectar_columnas`), dibuja **filtros** (`_filtros_sidebar`) y aplica filtros (`_aplicar_filtros`).
6. Calcula la **meta efectiva** (columnas elegidas por el usuario con prioridad sobre las detectadas).
7. Si el filtrado queda vacío, avisa y termina.
8. Pinta la cabecera y las **6 pestañas**, pasando siempre el `df` filtrado y la meta efectiva.

## Estado (`st.session_state`)

| Clave | Qué guarda |
|---|---|
| `df` / `meta` | DataFrame cargado y metadatos de columnas. |
| `fuente` / `fuente_cargada` | Fuente elegida / fuente ya cargada (evita recargar). |
| `tema` / `paleta` | Apariencia elegida por el usuario. |
| `filtro_sector`, `filtro_region`, `filtro_rango` | Filtros activos. |
| `sel_valor`, `sel_grupo`, `sel_region`, `sel_fecha` | Selección manual de columnas. |
| `col_valor`, `col_grupo`, `col_region`, `col_fecha` | Valores "efectivos" (señal de qué usar). |
| `comp_a`, `comp_b`, `disp_x`, `disp_y` | Selecciones de Comparar y Dispersión. |
| `archivo_subido` | Archivo subido (widget). |
| `renderer` | Instancia de PyGWalker (pestaña Explorador). |

## Utilidades

### `_guardar_df(df, meta=None) -> None`
Guarda el DataFrame y sus metadatos en el estado.

### `_limpiar_todo() -> None`
Borra datos, filtros y selecciones, restaura la fuente y hace `st.rerun()`.

### `_aplicar_filtros(df, meta) -> pd.DataFrame`
Aplica en orden: filtro de grupo (multiselect), de región y de rango de fechas. Devuelve una copia filtrada.

### `_sidebar(fuente) -> None`
Selector de fuente con `st.radio`: **Datos de ejemplo**, **Subir archivo (CSV/Excel)** o **Base de datos** (formulario con motor MySQL/PostgreSQL). Muestra botón "Limpiar todo" si hay datos y el atajo "Usar datos de ejemplo" si no los hay.

### `_filtros_sidebar(meta, df) -> None`
Filtros multiselect de grupo (si tiene ≤ 40 valores) y región, rango de fechas (`st.date_input`), y la sección "Columnas detectadas" para sobrescribir valor/grupo/región/fecha.

### `_meta_efectiva(meta) -> dict`
Devuelve la meta final dando prioridad a las columnas elegidas por el usuario (`col_*`) sobre las detectadas.

### `_mensual(df, fecha, valor) -> pd.DataFrame`
Agrega `valor` por mes (periodo `M`, como string) ordenado.

### `_delta_reciente(df, fecha, valor) -> float | None`
Variación % de los últimos 3 meses vs los 3 anteriores; `None` si no hay ≥ 6 meses o el previo es ≤ 0.

### `_spark_mensual(df, fecha, valor) -> list[int] | None`
Alturas (0–44) normalizadas de los últimos 6 meses para el spark del KPI.

## Pestañas

Cada pestaña recibe `df_filtrado` y `meta_ef`:

| Pestaña | Función | Contenido |
|---|---|---|
| **Resumen** | `_pestania_resumen` | 4 KPIs (total, mejor, peor, promedio), gráfico de barras + líneas/pastel con sus lecturas. |
| **Gráficos** | `_pestania_graficos` | Selector de tipo (barras, líneas, pastel, calor, box, histograma, dispersión) + lectura y recomendaciones. |
| **Insights** | `_pestania_insights` | Todos los análisis reunidos en acordeones (expander). |
| **Comparar** | `_pestania_comparar` | Dos grupos A/B: KPIs de total, línea/histograma por grupo y pastel conjunto. |
| **Estadística** | `_pestania_estadistica` | 8 métricas (media, mediana, cuartiles…), box+histograma, conteo de atípicos y tabla de atípicos. |
| **Explorador** | `_pestania_explorador` | PyGWalker: interfaz drag-and-drop para gráficos propios (usa el df filtrado). |

## Notas

- `_pestania_explorador` importa `pygwalker` de forma perezosa y envuelve el error con un `st.warning` para que la app nunca se caiga si PyGWalker falla.
- El bloque `if __name__ == "__main__": main()` evita que el código se ejecute al importar `app.py` (lo usan los tests).
- Los gráficos de la pestaña Gráficos también pintan **recomendaciones** (`mostrar_recomendaciones`); en Resumen solo lecturas.
