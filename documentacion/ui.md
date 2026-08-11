# `src/ui.py` — Interfaz y presentación

## Concepto

Es la **capa de presentación**: define el sistema de temas/paletas, el CSS global, los componentes visuales (tarjetas KPI, lecturas, recomendaciones) y la cabecera. Es el único módulo de `src/` que importa `streamlit` (además de `pandas`).

Todo el estilo se maneja con **variables CSS** (`--primary`, `--bg`, etc.) inyectadas en el documento. Por eso cambiar de paleta solo reemplaza las variables y toda la interfaz se repinta sin tocar los componentes.

## Constantes

| Constante | Valor | Uso |
|---|---|---|
| `TEAL` / `AMBER` / `GREEN` / `RED` | `#0F4C81` / `#F59E0B` / `#006C47` / `#BA1A1A` | Colores puntuales para KPIs (comparar, estadística). |
| `PALETAS` | `dict` | 4 paletas: **Esmeralda, Teal, Índigo, Coral**. Cada una con variantes `claro` y `oscuro`, y cada variante con ~20 variables CSS. |

## Temas

### `inyectar_tema(modo: str, paleta: str) -> None`
Inyecta las variables CSS según modo y paleta.

- **`modo`**: `"Oscuro"` (usa la variante oscura), `"Claro"` (la clara) o `"Sistema"` (oscura por defecto + `@media (prefers-color-scheme: light)` para cambiar sola con el sistema).
- **`paleta`**: clave de `PALETAS`; si no existe, cae a `"Esmeralda"`.
- Aplica con `st.markdown("<style>...</style>", unsafe_allow_html=True)`.

### `inyectar_css() -> None`
Inyecta el bloque CSS completo (`_CSS`): fuentes (Inter, Manrope, JetBrains Mono), iconos Material Symbols, y estilos de todos los componentes (KPIs, pestañas, sidebar, botones, selectbox, etc.). Se llama una vez por render.

## Formato de números y fechas

| Función | Qué hace |
|---|---|
| `formatear_dinero(valor) -> str` | Formato español con puntos: `$1.234.567` (sin decimales). |
| `formatear_monto_corto(valor) -> str` | Versión compacta: `$1.2M`, `$12k`, o `formatear_dinero`. |
| `fecha_es(fecha) -> str` | Fecha en español abreviado: `05 ago 2026`. |

## Componentes visuales

### `tarjeta_kpi(label, valor, icono=None, icono_clase="", sub="", delta=None, delta_sube=True, bar=None, bar_color=None, bar_label="", spark=None, valor_sm=False, color=None) -> str`
Genera el HTML de una tarjeta KPI grande. **Retorna** un string (se pinta con `st.markdown(..., unsafe_allow_html=True)`).

| Parámetro | Uso |
|---|---|
| `label` / `valor` | Texto principal. |
| `icono` | Nombre de icono Material Symbols (p. ej. `"trending_up"`). |
| `sub` | Texto pequeño al pie. |
| `delta` | % de variación; pinta una píldora verde/roja. `delta_sube` decide el color. |
| `bar` | Progreso 0–100; `bar_color` y `bar_label` lo personalizan. |
| `spark` | Lista de alturas (0–44) para un mini gráfico de barras. |
| `valor_sm` | Reduce el tamaño del número. |
| `color` | Color inline del valor. |

### `kpi(label, valor, sub="", color="") -> None`
Tarjeta KPI **mini** (pinta directamente con `st.markdown`). Se usa en Comparar y Estadística.

### `cabecera(df, meta) -> None`
Pinta el encabezado del dashboard: logo "TV", título **The View**, chip con el rango de fechas (si `meta` tiene fecha) y un **popover** de ajustes (⋮) con selector de tema y paleta.

### `mostrar_lectura(frases) -> None`
Pinta el bloque "LECTURA AUTOMÁTICA" (caja con borde izquierdo terciario). Si `frases` está vacío, no pinta nada.

### `mostrar_recomendaciones(frases) -> None`
Pinta el bloque "RECOMENDACIÓN" (caja con borde secundario). Si está vacío, no pinta nada.

### `mostrar_grafico(fig) -> None`
Pinta un gráfico Plotly con `st.plotly_chart`. Usa una clave única por gráfico (contador `_SEED` + título) y degrada de `width="stretch"` a `use_container_width` y luego al modo simple según lo que soporte la versión de Streamlit instalada.

### `mostrar_tabla(df) -> None`
Pinta un `st.dataframe` con clave única y el mismo degradado por compatibilidad de versiones.

## Notas

- Las claves únicas de `mostrar_grafico`/`mostrar_tabla` evitan choques de estado en Streamlit entre renders.
- El `_CSS` también oculta el header, el footer y el botón de deploy de Streamlit para un look de app propia.
