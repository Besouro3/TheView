# `src/estadistica.py` — Estadística

## Concepto

Módulo puro (solo `numpy` y `pandas`) con el cálculo numérico del dashboard: resumen descriptivo, detección de valores atípicos y correlación. No genera gráficos ni texto; entrega números que `app.py` muestra con los componentes de `src/ui.py`.

## Funciones

### `resumen_estadistico(df, col) -> dict`
Calcula el resumen descriptivo de una columna numérica.

- **Parámetros**: `df` — DataFrame; `col` — nombre de la columna.
- **Proceso**: elimina nulos, convierte a `float` y calcula cuantiles.
- **Retorna** un diccionario con:

| Clave | Valor |
|---|---|
| `registros` | Número de valores no nulos (int) |
| `media` | Media aritmética |
| `mediana` | Cuantil 0.5 |
| `desviacion` | Desviación estándar (muestral) |
| `minimo` / `maximo` | Mínimo / máximo |
| `q1` / `q3` | Cuantiles 0.25 / 0.75 |
| `iqr` | Rango intercuartil (`q3 - q1`) |

### `detectar_outliers(df, col) -> pd.DataFrame`
Devuelve las filas consideradas atípicas por el **método 1.5×IQR**.

- **Parámetros**: `df` — DataFrame; `col` — columna numérica.
- **Proceso**: calcula `q1`, `q3`, `iqr`, y marca como atípico todo valor fuera de `[q1 - 1.5*iqr, q3 + 1.5*iqr]`.
- **Retorna**: un `DataFrame` (subconjunto de `df`) con los registros atípicos.

### `correlacion(x: pd.Series, y: pd.Series) -> float`
Coeficiente de correlación de Pearson entre dos series.

- **Parámetros**: `x`, `y` — series pandas.
- **Proceso**: las une y descarta nulos; si quedan menos de 3 filas devuelve `0.0`.
- **Retorna**: `float` entre -1 y 1. Nota: este módulo define la función, pero `app.py` usa la correlación directamente en `src/insights.py` (`leer_dispersion`) para los textos del gráfico de dispersión.

## Ejemplo de uso

```python
from src import estadistica

resumen = estadistica.resumen_estadistico(df, "monto")
outliers = estadistica.detectar_outliers(df, "monto")
r = estadistica.correlacion(df["unidades"], df["monto"])
```
