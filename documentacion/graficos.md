# `src/graficos.py` — Gráficos

## Concepto

Construye todas las figuras **Plotly** del dashboard. Cada función recibe un `DataFrame` y devuelve una figura lista para `st.plotly_chart`. El módulo mantiene un **estado global de tema** (claro/oscuro + color acento) que se configura desde `app.py` según la paleta elegida por el usuario, de modo que todos los gráficos se repintan con la misma identidad visual sin cambiar el código de cada figura.

## Estado global

| Variable | Uso |
|---|---|
| `_OSCURO` | `True` → paleta oscura, `False` → clara. Inicial `True`. |
| `_ACENTO` | Color de acento (hex). Si es `None`, se usa el por defecto según tema. |

### `set_tema(oscuro: bool, acento: str = None) -> None`
Actualiza el estado global. Se llama en cada render de `app.py` (app.py:428) con el color de acento de la paleta activa.

## Utilidades internas (color)

| Función | Qué hace |
|---|---|
| `_acento()` | Color acento: el configurado o `#7EE8B0` (oscuro) / `#007F5F` (claro). |
| `_texto()` | Color de texto: `#E2ECE6` (oscuro) / `#1A1C1A` (claro). |
| `_grid()` | Color de las líneas de cuadrícula (con transparencia). |
| `_mezclar(hexc, blanco)` | Aclara un color mezclándolo con blanco (0–1). |
| `_colores()` | Lista de colores para series múltiples: el acento + una paleta por tema. |
| `_escala_calor()` | Escala de dos paradas para heatmaps (acento aclarado → acento). |
| `_layout(fig, titulo, eje_x="", eje_y="")` | Aplica fondo transparente, fuente, títulos y cuadrícula a una figura. |

## Gráficos

| Función | Parámetros | Descripción |
|---|---|---|
| `grafico_barras(df, grupo, valor)` | grupo, valor | Barras horizontales de `valor` sumado por `grupo`, ordenadas de mayor a menor, con etiqueta `$`. |
| `grafico_lineas(df, fecha, valor)` | fecha, valor | Serie mensual (agrupa por `to_period("M")`) con área bajo la línea. |
| `grafico_pie(df, grupo, valor)` | grupo, valor | Pastel/dona (agujero 45%) con porcentajes y paleta de colores. |
| `grafico_calor(df, fila, col, valor)` | fila, col, valor | Tabla pivote (suma de `valor`) como heatmap; celdas con formato corto (`$1.2M`). |
| `grafico_box(df, grupo, valor)` | grupo, valor | Un box plot por valor único de `grupo`, coloreados. |
| `grafico_histograma(df, valor)` | valor | Histograma con 24 barras. |
| `grafico_dispersion(df, x, y)` | x, y | Nube de puntos + recta de regresión (dash naranja) si hay ≥ 3 puntos. |

### `_formato_corto(v) -> str`
Formato compacto para montos: `$1.2M`, `$12k`, `$1,234`.

## Notas de diseño

- Todas las figuras usan **fondo transparente** (`rgba(0,0,0,0)`) para integrarse con el tema CSS de la app.
- El agrupado mensual se repite aquí y en `insights.py`; ambos suman por período `M` para que el gráfico y su lectura coincidan.
- `grafico_dispersion` y `_escala_calor` dependen de `_mezclar` y del acento activo.

## Ejemplo de uso

```python
from src import graficos

graficos.set_tema(oscuro=True, acento="#7EE8B0")
fig = graficos.grafico_lineas(df, "fecha", "monto")
```
