# `datos/generar_datos.py` — Datos de ejemplo

## Concepto

Genera el CSV `datos/ventas_ejemplo.csv` con ventas sintéticas pero **realistas**, con tendencia y dispersión controladas. Se usa por defecto en el dashboard (vía `src/cargador.datos_ejemplo`, que lo genera automáticamente si falta).

## Datos

- **Rango de fechas**: `2025-01-01` a `2026-07-31` (19 meses).
- **Registros**: ~6000 filas (seed fija `random.Random(42)`, así siempre sale el mismo dataset).
- **Columnas**: `fecha`, `sector`, `region`, `producto`, `unidades`, `monto`.

## Modelo de generación

Cada fila se construye multiplicando factores:

```
monto = 7500 × peso_sector × peso_region × peso_producto × tendencia_region × ruido(0.78–1.22)
unidades = max(1, redondeo(monto / precio_producto))
```

| Diccionario | Contenido |
|---|---|
| `SECTORES` | 5 sectores con peso 0.9–1.6. |
| `REGIONES` | 5 regiones con `(multiplicador, pendiente_tendencia)`. La pendiente hace que la región crezca (positiva) o decaiga (negativa) a lo largo del período. |
| `PRODUCTOS` | 5 productos con `(peso, precio_unitario)`. |

La **tendencia** es lineal: `1 + pendiente × (mes_actual / meses_totales)`, lo que crea crecimiento o caída progresiva por región. El ruido multiplicativo da variabilidad sin estropear la tendencia.

## Función

### `generar() -> None`
Genera el DataFrame, lo ordena por fecha y lo guarda en `OUT` (`datos/ventas_ejemplo.csv`). Imprime cuántas filas escribió.

- Ejecutable directo: `python datos/generar_datos.py`.

## Notas

- Las fechas se limitan al día 28 para evitar meses sin el día elegido.
- Para **regenerar** el CSV con otros números, cambia la seed (línea `rng = random.Random(42)`) o los parámetros y vuelve a ejecutar el script.
