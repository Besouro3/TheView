# `src/insights.py` — Lecturas y recomendaciones

## Concepto

Este módulo convierte los **números en frases**. Cada función recibe los mismos parámetros que el gráfico equivalente de `src/graficos.py` y devuelve **dos listas**: las *lecturas* (qué muestra el gráfico) y las *recomendaciones* (qué hacer). Es la capa de "análisis automático" del dashboard.

Todas las funciones devuelven la tupla `(frases, recomendaciones)`:

| Elemento | Tipo | Contenido |
|---|---|---|
| `frases` | `list[str]` | Lecturas automáticas (Markdown con **negritas**). |
| `recomendaciones` | `list[str]` | Acciones sugeridas. Puede estar vacía. |

Si los datos no alcanzan para un análisis (pocas filas, sin grupos, etc.), devuelven listas vacías en lugar de fallar.

## Funciones por gráfico

| Función | Gráfico equivalente | Qué analiza |
|---|---|---|
| `leer_barras(df, grupo, valor)` | barras | Líder y cola por grupo, % de participación, brecha y grupos por debajo del 60% del promedio. |
| `leer_lineas(df, fecha, valor)` | líneas | Variación total, mitad 1 vs mitad 2, ritmo reciente (últimos 3 vs 3 previos), mejor/peor mes, tendencia. |
| `leer_pie(df, grupo, valor)` | pastel | Segmento dominante, segundo puesto, concentración top-2 y recomendación si está muy repartido. |
| `leer_calor(df, fila, col, valor)` | heatmap | Combinación más fuerte/débil, zona líder/cola y zonas bajo el promedio. |
| `leer_box(df, grupo, valor)` | box plot | Mediana por grupo, grupo más variable (IQR) y conteo de atípicos. |
| `leer_histograma(df, valor)` | histograma | Media, variabilidad (CV), asimetría con `scipy.stats.skew` y cuándo usar la mediana. |
| `leer_dispersion(df, x, y)` | dispersión | Correlación de Pearson, fuerza (muy fuerte/fuerte/moderada/débil) y sentido. |

## Utilidades internas

### `_pct(parte, total) -> float`
Porcentaje `parte/total*100`; devuelve `0.0` si el total es 0.

### `_top_bottom(df, grupo, valor) -> (agg, top, bottom)`
Agrupa por `grupo`, suma `valor` y ordena descendente. Devuelve el DataFrame agregado, la fila del líder y la del último.

## Lógica destacada (para entender las frases)

- **Barras**: el líder con su % del total; la brecha `(top - bottom)/bottom`; recomendación si el líder ≥ 40% del negocio; alerta si hay grupos bajo el 60% del promedio.
- **Líneas**: compara `último vs primero`, `mitad 2 vs mitad 1` y `últimos 3 meses vs 3 anteriores` (`mom`). Recomienda si la tendencia es negativa, si crece > 20%, o si el ritmo reciente baja de -10%.
- **Histograma**: asimetría — si es > 0 (sesgo derecho), recomienda usar la **mediana** como meta realista porque la media la inflan pocas ventas grandes.
- **Dispersión**: si `|r| ≥ 0.6` sugiere usar una variable para proyectar la otra; si `|r| < 0.2` avisa que no hay relación lineal.

## Ejemplo de uso

```python
from src import insights

frases, recomendaciones = insights.leer_barras(df, "sector", "monto")
for f in frases:
    print("-", f)
```

## Para añadir un análisis nuevo

1. Añade la función `leer_*` en este módulo siguiendo la firma `(df, ...) -> (frases, recos)`.
2. Añade el gráfico correspondiente en `src/graficos.py`.
3. Úsala en la pestaña de `app.py` con `mostrar_lectura(frases)` y `mostrar_recomendaciones(recos)` (importadas de `src/ui.py`).
