import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src import cargador, estadistica, graficos, insights

df = cargador.datos_ejemplo()
meta = cargador.detectar_columnas(df)
print("Meta:", meta)
print("Filas:", len(df))

valor, grupo, region, fecha = meta["valor"], meta["grupo"], meta["region"], meta["fecha"]
assert all([valor, grupo, region, fecha]), "Detección incompleta"

graficos.grafico_barras(df, grupo, valor)
graficos.grafico_lineas(df, fecha, valor)
graficos.grafico_pie(df, grupo, valor)
graficos.grafico_calor(df, region, grupo, valor)
graficos.grafico_box(df, grupo, valor)
graficos.grafico_histograma(df, valor)
graficos.grafico_dispersion(df, "unidades", valor)
print("Graficos OK")

for nombre, fn, args in [
    ("barras", insights.leer_barras, (df, grupo, valor)),
    ("lineas", insights.leer_lineas, (df, fecha, valor)),
    ("pie", insights.leer_pie, (df, grupo, valor)),
    ("calor", insights.leer_calor, (df, region, grupo, valor)),
    ("box", insights.leer_box, (df, grupo, valor)),
    ("hist", insights.leer_histograma, (df, valor)),
    ("disp", insights.leer_dispersion, (df, "unidades", valor)),
]:
    frases, recos = fn(*args)
    print(f"[{nombre}] frases={len(frases)} recos={len(recos)}")
    for f in frases:
        print("   -", f)

resumen = estadistica.resumen_estadistico(df, valor)
print("Resumen:", {k: round(v, 2) if isinstance(v, float) else v for k, v in resumen.items()})
out = estadistica.detectar_outliers(df, valor)
print("Outliers:", len(out))
print("SMOKE_OK")
