import os
import random

import numpy as np
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(DATA_DIR, "ventas_ejemplo.csv")

SECTORES = {
    "Sector 1": 1.0,
    "Sector 2": 1.3,
    "Sector 3": 0.9,
    "Sector 4": 1.6,
    "Sector 5": 1.2,
}
REGIONES = {
    "África": (1.45, 0.30),
    "Asia": (1.20, 0.12),
    "Europa": (1.00, 0.06),
    "América": (0.82, -0.18),
    "Oceanía": (0.70, 0.02),
}
PRODUCTOS = {
    "Cola Original": (1.00, 4500),
    "Cola Zero": (1.05, 4800),
    "Sprite": (0.85, 3800),
    "Fanta": (0.80, 3500),
    "Agua": (0.70, 2600),
}


def generar() -> None:
    rng = random.Random(42)
    inicio = pd.Timestamp("2025-01-01")
    fin = pd.Timestamp("2026-07-31")
    meses_totales = (fin.year - inicio.year) * 12 + (fin.month - inicio.month)

    filas = []
    for _ in range(6000):
        fecha = pd.Timestamp(
            rng.randint(inicio.year, fin.year),
            rng.randint(1, 12),
            rng.randint(1, 28),
        )
        if not (inicio <= fecha <= fin):
            continue
        sector = rng.choice(list(SECTORES))
        region = rng.choice(list(REGIONES))
        producto = rng.choice(list(PRODUCTOS))
        mult_region, tendencia_region = REGIONES[region]
        indice = (fecha.year - inicio.year) * 12 + (fecha.month - inicio.month)
        tendencia = 1 + tendencia_region * (indice / meses_totales)
        monto = (7500 * SECTORES[sector] * mult_region * PRODUCTOS[producto][0]
                 * tendencia * rng.uniform(0.78, 1.22))
        monto = round(monto / 10) * 10
        unidades = max(1, round(monto / PRODUCTOS[producto][1]))
        filas.append((fecha, sector, region, producto, unidades, monto))

    df = pd.DataFrame(filas, columns=["fecha", "sector", "region", "producto", "unidades", "monto"])
    df = df.sort_values("fecha").reset_index(drop=True)
    df.to_csv(OUT, index=False)
    print(f"Datos generados: {len(df)} filas -> {OUT}")


if __name__ == "__main__":
    generar()
