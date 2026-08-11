# `tests/` — Pruebas

## Concepto

Dos scripts de validación que corren sin framework (solo `python tests/<archivo>`). Verifican que la app arranca sin excepciones y que la lógica de datos produce los objetos esperados.

## `test_app.py` — Prueba de la interfaz

Usa `streamlit.testing.v1.AppTest` (el runner de pruebas de Streamlit).

1. Carga `app.py` y lo ejecuta con timeout de 120 s.
2. Falla con `AssertionError` si la app lanza alguna excepción (`at.exception`).
3. Recorre cada pestaña, las ejecuta y comprueba que ninguna tenga errores.

### Nota importante
Usa `st.session_state` real; por eso el renderer de PyGWalker (`_pestania_explorador`) se crea durante la prueba y el Explorador se ejecuta como pestaña.

### Cómo correrlo
```bash
python tests/test_app.py
```
Éxito esperado: imprime `APPTEST_OK` y termina con código 0.

## `test_smoke.py` — Prueba de la lógica

Valida la capa de datos sin arrancar la interfaz:

1. Carga los datos de ejemplo y `detectar_columnas`.
2. Comprueba que se detecten las 4 columnas clave (`valor`, `grupo`, `region`, `fecha`).
3. Genera todos los gráficos de `src/graficos.py` (sin errores).
4. Llama a cada `leer_*` de `src/insights.py` y comprueba que devuelva tuplas con frases/recomendaciones.
5. Calcula el resumen estadístico y los outliers.

### Cómo correrlo
```bash
python tests/test_smoke.py
```
Éxito esperado: imprime `SMOKE_OK` y termina con código 0.

## Ruta de raíz en los tests

Ambos tests se ejecutan desde `tests/`, por lo que:

- `test_app.py` calcula la raíz con `Path(__file__).resolve().parent.parent`, cambia a ella con `os.chdir(ROOT)` y abre `ROOT / "app.py"`.
- `test_smoke.py` añade la raíz a `sys.path` para poder `import src`.

Así funcionan sin importar desde qué carpeta se lancen.

## Añadir una prueba nueva

- Para **lógica**: agrega aserciones en `test_smoke.py` o crea otro script que haga `import src.<modulo>` y valide resultados.
- Para **interfaz**: replica el patrón de `test_app.py` con `AppTest.from_file(...)`.
