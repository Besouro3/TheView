import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "datos")
ARCHIVO_EJEMPLO = os.path.join(DATA_DIR, "ventas_ejemplo.csv")


def datos_ejemplo() -> pd.DataFrame:
    if not os.path.exists(ARCHIVO_EJEMPLO):
        from datos.generar_datos import generar
        generar()
    return pd.read_csv(ARCHIVO_EJEMPLO, parse_dates=["fecha"])


def datos_archivo(archivo) -> pd.DataFrame:
    nombre = archivo.name.lower()
    if nombre.endswith(".xlsx") or nombre.endswith(".xls"):
        return pd.read_excel(archivo)
    return pd.read_csv(archivo)


def datos_base_datos(tipo: str, host: str, puerto: str, usuario: str,
                     clave: str, base: str, tabla: str) -> pd.DataFrame:
    import sqlalchemy
    if tipo == "MySQL":
        url = f"mysql+pymysql://{usuario}:{clave}@{host}:{puerto}/{base}"
    else:
        url = f"postgresql+psycopg2://{usuario}:{clave}@{host}:{puerto}/{base}"
    engine = sqlalchemy.create_engine(url)
    return pd.read_sql(f"SELECT * FROM {tabla}", engine)


_PATRONES_VALOR = ("monto", "venta", "total", "valor", "precio", "ingreso", "ingresos", "revenue", "amount", "price")
_PATRONES_GRUPO = ("sector", "zona", "categoria", "category", "area", "producto", "product", "equipo", "canal")
_PATRONES_REGION = ("region", "zona", "pais", "país", "area", "continente", "country", "territorio")
_PATRONES_FECHA = ("fecha", "date", "dia", "mes", "fecha_venta")


def _coincide(col: str, patrones) -> bool:
    c = col.lower().strip()
    return any(p in c for p in patrones)


def detectar_columnas(df: pd.DataFrame) -> dict:
    numericas = df.select_dtypes(include=["number"]).columns.tolist()
    textos = df.select_dtypes(include=["object", "category"]).columns.tolist()
    fechas = [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])]

    col_valor = next((c for c in numericas if _coincide(c, _PATRONES_VALOR)), numericas[0] if numericas else None)
    col_region = next((c for c in textos if _coincide(c, _PATRONES_REGION)), None)
    col_grupo = next((c for c in textos if _coincide(c, _PATRONES_GRUPO)),
                     next((c for c in textos if c != col_region and df[c].nunique() <= 12), None))
    col_fecha = next((c for c in fechas if _coincide(c, _PATRONES_FECHA)), fechas[0] if fechas else None)

    return {
        "valor": col_valor,
        "grupo": col_grupo,
        "region": col_region,
        "fecha": col_fecha,
        "numericas": numericas,
        "textos": textos,
    }
