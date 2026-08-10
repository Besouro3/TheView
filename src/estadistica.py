import numpy as np
import pandas as pd


def resumen_estadistico(df: pd.DataFrame, col: str) -> dict:
    s = df[col].dropna().astype(float)
    q1, q2, q3 = s.quantile([0.25, 0.5, 0.75])
    return {
        "registros": int(s.count()),
        "media": float(s.mean()),
        "mediana": float(q2),
        "desviacion": float(s.std()),
        "minimo": float(s.min()),
        "q1": float(q1),
        "q3": float(q3),
        "maximo": float(s.max()),
        "iqr": float(q3 - q1),
    }


def detectar_outliers(df: pd.DataFrame, col: str) -> pd.DataFrame:
    s = df[col].dropna().astype(float)
    q1, q3 = s.quantile([0.25, 0.75])
    iqr = q3 - q1
    lim_inf, lim_sup = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return df[(df[col] < lim_inf) | (df[col] > lim_sup)]


def correlacion(x: pd.Series, y: pd.Series) -> float:
    datos = pd.concat([x, y], axis=1).dropna()
    if len(datos) < 3:
        return 0.0
    return float(np.corrcoef(datos[x.name], datos[y.name])[0, 1])
