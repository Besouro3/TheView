# The View — Documentación del código

Dashboard de análisis de ventas hecho con **Streamlit**, **Plotly** y **Pandas**. Carga datos (CSV, Excel o base de datos), detecta automáticamente el rol de cada columna y genera gráficos, lecturas automáticas y recomendaciones.

## Índice

| Documento | Contenido |
|---|---|
| [cargador.md](cargador.md) | Carga de datos y detección automática de columnas |
| [estadistica.md](estadistica.md) | Resumen estadístico, outliers y correlación |
| [graficos.md](graficos.md) | Gráficos Plotly y tema de colores |
| [insights.md](insights.md) | Lecturas automáticas y recomendaciones |
| [ui.md](ui.md) | Interfaz: paletas, CSS y componentes visuales |
| [app.md](app.md) | Punto de entrada: flujo, estado y pestañas |
| [datos.md](datos.md) | Generación del CSV de ejemplo |
| [tests.md](tests.md) | Pruebas automáticas |

## Arquitectura en un vistazo

```
TheView/
├── app.py                 # Entrada de Streamlit: orquesta todo
├── requirements.txt       # Dependencias
├── .streamlit/config.toml # Tema base y configuración
├── datos/
│   ├── ventas_ejemplo.csv # Datos de ejemplo
│   └── generar_datos.py   # Script que genera el CSV
├── src/                   # Lógica separada por responsabilidad
│   ├── cargador.py        # Leer datos + detectar columnas
│   ├── estadistica.py     # Métricas y análisis numérico
│   ├── graficos.py        # Construcción de figuras Plotly
│   ├── insights.py        # Textos de lectura y recomendaciones
│   └── ui.py              # CSS, paletas y componentes visuales
├── tests/                 # Pruebas (AppTest + smoke)
└── scripts/
    └── The View.bat       # Lanzador en Windows
```

## Flujo de datos

1. `app.py` arranca y aplica tema/paleta (`src/ui.py`).
2. La barra lateral elige la **fuente**: ejemplo, archivo subido o base de datos (`src/cargador.py`).
3. `cargador.detectar_columnas()` clasifica cada columna como *valor*, *grupo*, *región* o *fecha*.
4. El usuario ajusta filtros y columnas manualmente; se guarda todo en `st.session_state`.
5. Cada pestaña pide sus gráficos a `src/graficos.py` y sus textos a `src/insights.py`, y los pinta con los componentes de `src/ui.py`.

## Principios del diseño

- **Streamlit no importa en `src/`** salvo en `ui.py` (que es la capa de presentación). La lógica de datos y análisis es pura (solo pandas/numpy/plotly) y por eso se puede probar sin lanzar la interfaz.
- **Todo el estado** (datos, filtros, selecciones) vive en `st.session_state`; ninguna función muta datos globales.
- **Cada gráfico tiene su lectura**: `graficos.py` dibuja, `insights.py` explica lo que ve el gráfico y sugiere acciones.
- **El tema visual** se controla por variables CSS (`--primary`, `--bg`, etc.) definidas en `src/ui.py`, así que cambiar de paleta no toca los gráficos.
