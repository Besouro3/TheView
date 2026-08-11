# `src/cargador.py` — Carga de datos

## Concepto

Este módulo se encarga de **traer los datos** al dashboard desde tres fuentes (archivo de ejemplo, archivo subido por el usuario o base de datos) y de **descubrir el rol** de cada columna del DataFrame. Es la puerta de entrada: nada se analiza hasta que este módulo entrega un `DataFrame` y su "meta" (qué columna es el valor, cuál el grupo, etc.).

Es un módulo **puro**: no importa `streamlit`, solo `pandas` y `os`. Esto permite probarlo por separado.

## Constantes

| Constante | Valor | Descripción |
|---|---|---|
| `DATA_DIR` | `<raíz>/datos` | Ruta calculada con `__file__`, así funciona aunque cambie el directorio de trabajo. |
| `ARCHIVO_EJEMPLO` | `<raíz>/datos/ventas_ejemplo.csv` | Ruta del CSV de ejemplo. |

## Funciones

### `datos_ejemplo() -> pd.DataFrame`
Carga el CSV de ejemplo. Si no existe, lo genera con `datos.generar_datos.generar()` y luego lo lee.

- **Retorna**: `DataFrame` con la columna `fecha` parseada como fecha (`parse_dates=["fecha"]`).

### `datos_archivo(archivo) -> pd.DataFrame`
Lee un archivo subido por el usuario.

- **Parámetros**: `archivo` — objeto *UploadedFile* de Streamlit.
- **Comportamiento**: según la extensión usa `pd.read_excel` (`.xlsx`/`.xls`) o `pd.read_csv`.

### `datos_base_datos(tipo, host, puerto, usuario, clave, base, tabla) -> pd.DataFrame`
Conecta a una base de datos y lee una tabla completa.

- **Parámetros**: `tipo` (`"MySQL"` o `"PostgreSQL"`), credenciales y nombre de tabla.
- **Comportamiento**: construye la URL con SQLAlchemy (`mysql+pymysql://` o `postgresql+psycopg2://`) y ejecuta `SELECT * FROM tabla`.
- **Nota**: la importación de `sqlalchemy` es perezosa (dentro de la función) para no pagar el costo de importarla si no se usa.

### `detectar_columnas(df: pd.DataFrame) -> dict`
Detecta automáticamente qué columna cumple cada rol.

- **Retorna** un diccionario con:

| Clave | Significado | Criterio |
|---|---|---|
| `valor` | Columna numérica principal (dinero) | Primera numérica que coincide con `_PATRONES_VALOR`, si no, la primera numérica. |
| `grupo` | Columna de agrupación (sector, producto…) | Primera de texto que coincide con `_PATRONES_GRUPO`; si no, la primera de texto con ≤ 12 valores únicos que no sea región. |
| `region` | Columna de zona/región | Primera de texto que coincide con `_PATRONES_REGION`. |
| `fecha` | Columna de fecha | Primera fecha que coincide con `_PATRONES_FECHA`, si no, la primera fecha. |
| `numericas` | Lista | Todas las columnas numéricas. |
| `textos` | Lista | Todas las columnas de tipo `object`/`category`. |

## Patrones de coincidencia

El módulo busca subcadenas (case-insensitive) en el nombre de la columna:

```python
_PATRONES_VALOR  = ("monto", "venta", "total", "valor", "precio", "ingreso", "revenue", "amount", "price")
_PATRONES_GRUPO  = ("sector", "zona", "categoria", "category", "area", "producto", "product", "equipo", "canal")
_PATRONES_REGION = ("region", "zona", "pais", "país", "area", "continente", "country", "territorio")
_PATRONES_FECHA  = ("fecha", "date", "dia", "mes", "fecha_venta")
```

## Funciones internas

### `_coincide(col, patrones) -> bool`
Devuelve `True` si el nombre de la columna (en minúsculas, sin espacios) contiene alguno de los patrones.

## Ejemplo de uso

```python
from src import cargador

df = cargador.datos_ejemplo()
meta = cargador.detectar_columnas(df)
# meta["valor"] -> "monto", meta["grupo"] -> "sector",
# meta["region"] -> "region", meta["fecha"] -> "fecha"
```

## Para añadir nuevas fuentes o columnas

- Para **otra fuente de datos**: añade una función que devuelva un `DataFrame` (p. ej. `datos_api(...)`).
- Para que **se detecten otras columnas** como valor/grupo/región/fecha: amplía las tuplas `_PATRONES_*`.
