import itertools

import pandas as pd
import streamlit as st

TEAL = "#0F4C81"
AMBER = "#F59E0B"
GREEN = "#006C47"
RED = "#BA1A1A"

PALETAS = {
    "Esmeralda": {
        "claro": {
            "bg": "#F7F9F4", "surface": "#F7F9F4", "surface-lowest": "#FFFFFF",
            "surface-container": "#EFF2EC", "surface-container-high": "#E7ECE4",
            "surface-container-highest": "#DFE5DC", "outline": "#6F7972",
            "outline-variant": "#C2CCC4", "on-surface": "#1A1C1A", "on-surface-variant": "#444C46",
            "primary": "#005C43", "primary-container": "#007F5F", "on-primary": "#FFFFFF",
            "secondary": "#00796B", "secondary-container": "#9FEEDC", "on-secondary-container": "#00564A",
            "tertiary": "#2E7D32", "tertiary-container": "#005C43", "on-tertiary-container": "#7CF2B0",
            "error": "#BA1A1A", "error-container": "#FFDAD6", "on-error-container": "#93000A",
            "card-shadow": "0 4px 20px rgba(0,124,95,0.08)", "acento": "#007F5F",
        },
        "oscuro": {
            "bg": "#0E1512", "surface": "#0E1512", "surface-lowest": "#141C18",
            "surface-container": "#1A2420", "surface-container-high": "#202B26",
            "surface-container-highest": "#26332D", "outline": "#8FA096",
            "outline-variant": "#3D4A44", "on-surface": "#E2ECE6", "on-surface-variant": "#B6C4BC",
            "primary": "#7EE8B0", "primary-container": "#005C43", "on-primary": "#00392A",
            "secondary": "#6FE3B0", "secondary-container": "#00564A", "on-secondary-container": "#9FEEDC",
            "tertiary": "#7CF2B0", "tertiary-container": "#00452F", "on-tertiary-container": "#B9FDD8",
            "error": "#FFB4AB", "error-container": "#93000A", "on-error-container": "#FFDAD6",
            "card-shadow": "0 4px 20px rgba(0,0,0,0.4)", "acento": "#7EE8B0",
        },
    },
    "Teal": {
        "claro": {
            "bg": "#F3FAFA", "surface": "#F3FAFA", "surface-lowest": "#FFFFFF",
            "surface-container": "#E9F2F2", "surface-container-high": "#DFECEC",
            "surface-container-highest": "#D4E4E4", "outline": "#647D7D",
            "outline-variant": "#B9CCCC", "on-surface": "#16201F", "on-surface-variant": "#3E4E4D",
            "primary": "#006B6B", "primary-container": "#0E9494", "on-primary": "#FFFFFF",
            "secondary": "#00796B", "secondary-container": "#A7EFEA", "on-secondary-container": "#005B50",
            "tertiary": "#00897B", "tertiary-container": "#0E7490", "on-tertiary-container": "#7DF2EC",
            "error": "#BA1A1A", "error-container": "#FFDAD6", "on-error-container": "#93000A",
            "card-shadow": "0 4px 20px rgba(14,148,148,0.10)", "acento": "#0E9494",
        },
        "oscuro": {
            "bg": "#0C1414", "surface": "#0C1414", "surface-lowest": "#12201E",
            "surface-container": "#172726", "surface-container-high": "#1D2F2D",
            "surface-container-highest": "#233735", "outline": "#8CA6A5",
            "outline-variant": "#3C4F4E", "on-surface": "#E0ECEA", "on-surface-variant": "#B4C8C6",
            "primary": "#5EEAD4", "primary-container": "#006B6B", "on-primary": "#00363A",
            "secondary": "#6FE3C0", "secondary-container": "#005B50", "on-secondary-container": "#A7EFEA",
            "tertiary": "#7DF2EC", "tertiary-container": "#0E7490", "on-tertiary-container": "#B5FBF7",
            "error": "#FFB4AB", "error-container": "#93000A", "on-error-container": "#FFDAD6",
            "card-shadow": "0 4px 20px rgba(0,0,0,0.4)", "acento": "#5EEAD4",
        },
    },
    "Índigo": {
        "claro": {
            "bg": "#F8F7FC", "surface": "#F8F7FC", "surface-lowest": "#FFFFFF",
            "surface-container": "#EFEDF7", "surface-container-high": "#E6E3F2",
            "surface-container-highest": "#DCD8EC", "outline": "#757A8C",
            "outline-variant": "#C4C3D6", "on-surface": "#1B1B21", "on-surface-variant": "#454653",
            "primary": "#4338CA", "primary-container": "#4F46E5", "on-primary": "#FFFFFF",
            "secondary": "#7C3AED", "secondary-container": "#C7BFF9", "on-secondary-container": "#4C1D95",
            "tertiary": "#6D28D9", "tertiary-container": "#7B61FF", "on-tertiary-container": "#E2DBFF",
            "error": "#BA1A1A", "error-container": "#FFDAD6", "on-error-container": "#93000A",
            "card-shadow": "0 4px 20px rgba(79,70,229,0.10)", "acento": "#4F46E5",
        },
        "oscuro": {
            "bg": "#121117", "surface": "#121117", "surface-lowest": "#1A1921",
            "surface-container": "#211F29", "surface-container-high": "#28252F",
            "surface-container-highest": "#2F2C37", "outline": "#9799A8",
            "outline-variant": "#4A4957", "on-surface": "#EBEAF2", "on-surface-variant": "#C1C0CD",
            "primary": "#A5B4FC", "primary-container": "#4338CA", "on-primary": "#1E1B5E",
            "secondary": "#C7BFF9", "secondary-container": "#4C1D95", "on-secondary-container": "#D5CEFF",
            "tertiary": "#B7ACFF", "tertiary-container": "#6D28D9", "on-tertiary-container": "#EAE6FF",
            "error": "#FFB4AB", "error-container": "#93000A", "on-error-container": "#FFDAD6",
            "card-shadow": "0 4px 20px rgba(0,0,0,0.4)", "acento": "#A5B4FC",
        },
    },
    "Coral": {
        "claro": {
            "bg": "#FBF6F2", "surface": "#FBF6F2", "surface-lowest": "#FFFFFF",
            "surface-container": "#F4EAE3", "surface-container-high": "#EEE0D6",
            "surface-container-highest": "#E7D6CA", "outline": "#85746C",
            "outline-variant": "#D2C1B8", "on-surface": "#211A16", "on-surface-variant": "#52453E",
            "primary": "#C2410C", "primary-container": "#E8722A", "on-primary": "#FFFFFF",
            "secondary": "#E85D75", "secondary-container": "#FFD9DE", "on-secondary-container": "#A01832",
            "tertiary": "#B45309", "tertiary-container": "#F59E0B", "on-tertiary-container": "#7A3B00",
            "error": "#BA1A1A", "error-container": "#FFDAD6", "on-error-container": "#93000A",
            "card-shadow": "0 4px 20px rgba(232,114,42,0.10)", "acento": "#E8722A",
        },
        "oscuro": {
            "bg": "#180F0A", "surface": "#180F0A", "surface-lowest": "#221711",
            "surface-container": "#2B1D15", "surface-container-high": "#332318",
            "surface-container-highest": "#3B2A1D", "outline": "#A49184",
            "outline-variant": "#57473E", "on-surface": "#F1E5DC", "on-surface-variant": "#CDBEB4",
            "primary": "#FDBA74", "primary-container": "#C2410C", "on-primary": "#4A1C00",
            "secondary": "#FFB4BF", "secondary-container": "#A01832", "on-secondary-container": "#FFD9DE",
            "tertiary": "#FFB84D", "tertiary-container": "#B45309", "on-tertiary-container": "#FFE1B5",
            "error": "#FFB4AB", "error-container": "#93000A", "on-error-container": "#FFDAD6",
            "card-shadow": "0 4px 20px rgba(0,0,0,0.45)", "acento": "#FDBA74",
        },
    },
}


def _declaraciones(d: dict) -> str:
    return "".join(f"--{k}:{v};" for k, v in d.items())


def _vars_css(d: dict) -> str:
    return f":root{{{_declaraciones(d)}}}"


def inyectar_tema(modo: str, paleta: str) -> None:
    datos = PALETAS.get(paleta) or PALETAS["Esmeralda"]
    if modo == "Claro":
        bloque = _vars_css(datos["claro"])
    elif modo == "Sistema":
        bloque = (_vars_css(datos["oscuro"])
                  + "@media (prefers-color-scheme: light){:root{"
                  + _declaraciones(datos["claro"]) + "}}")
    else:
        bloque = _vars_css(datos["oscuro"])
    st.markdown(f"<style>{bloque}</style>", unsafe_allow_html=True)


_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Manrope:wght@600;700;800&family=JetBrains+Mono:wght@500&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL@20..48,100..700,0..1&display=swap');

:root{
  --bg:#F7F9F4; --surface:#F7F9F4; --surface-lowest:#FFFFFF;
  --surface-container:#EFF2EC; --surface-container-high:#E7ECE4; --surface-container-highest:#DFE5DC;
  --outline:#6F7972; --outline-variant:#C2CCC4;
  --on-surface:#1A1C1A; --on-surface-variant:#444C46;
  --primary:#005C43; --primary-container:#007F5F; --on-primary:#FFFFFF;
  --secondary:#00796B; --secondary-container:#9FEEDC; --on-secondary-container:#00564A;
  --tertiary:#2E7D32; --tertiary-container:#005C43; --on-tertiary-container:#7CF2B0;
  --error:#BA1A1A; --error-container:#FFDAD6; --on-error-container:#93000A;
  --card-shadow: 0 4px 20px rgba(0,124,95,0.08);
  --font-body:'Inter',sans-serif; --font-head:'Manrope',sans-serif; --font-label:'JetBrains Mono',monospace;
}

.material-symbols-outlined{
  font-family:'Material Symbols Outlined'; font-weight:normal; font-style:normal;
  font-size:20px; line-height:1; letter-spacing:normal; text-transform:none;
  display:inline-block; white-space:nowrap; word-wrap:normal; direction:ltr;
  font-variation-settings:'FILL' 0,'wght' 400,'GRAD' 0,'opsz' 20;
}

html, body, .stApp{ background:var(--bg); color:var(--on-surface); font-family:var(--font-body); }
.block-container{ padding-top:1.25rem; max-width:1200px; }
[data-testid="stHeader"]{ display:none !important; }
footer{ visibility:hidden; }
[data-testid="stSidebar"]{ background:var(--surface-container); border-right:1px solid var(--outline-variant); }
[data-testid="stSidebar"] .block-container{ max-width:100%; }
h1,h2,h3,h4{ font-family:var(--font-head); color:var(--on-surface); }
p, li{ color:var(--on-surface); }

.theview-brand{ display:flex; align-items:center; gap:12px; }
.theview-logo{ width:36px; height:36px; border-radius:999px; background:var(--primary-container);
  color:#ffffff; display:flex; align-items:center; justify-content:center;
  font-family:var(--font-head); font-weight:800; font-size:14px; }
.theview-title{ font-family:var(--font-head); font-size:24px; font-weight:800;
  color:var(--primary); letter-spacing:-0.01em; margin:0; }
.theview-chip{ display:flex; align-items:center; gap:8px; border:1px solid var(--outline-variant);
  background:var(--surface-lowest); border-radius:999px; padding:8px 14px;
  font-family:var(--font-label); font-size:12px; color:var(--on-surface-variant);
  margin-left:auto; }
.theview-chip .material-symbols-outlined{ font-size:16px; color:var(--outline); }
.theview-divider{ border-bottom:1px solid var(--outline-variant); margin-bottom:8px; }
.menu-titulo{ font-family:var(--font-label); font-size:10px; letter-spacing:0.12em;
  text-transform:uppercase; color:var(--on-surface-variant); margin-bottom:2px; }

[data-testid="stPopover"]{ position:fixed; top:0.85rem; right:1.05rem; z-index:1000; }
[data-testid="stPopoverButton"]{
  border:1px solid var(--outline-variant); border-radius:999px;
  width:42px; height:42px; min-width:42px; max-width:42px; padding:0;
  background:var(--surface-lowest); color:var(--on-surface);
  box-shadow:var(--card-shadow); display:flex; align-items:center; justify-content:center;
  font-size:24px; line-height:1; }
[data-testid="stPopoverButton"]:hover{ border-color:var(--primary); color:var(--primary); }
[data-testid="stPopoverButton"] [aria-hidden="true"]{ display:none !important; }

.kpi-card{ background:var(--surface-container-lowest); border:1px solid var(--outline-variant);
  border-radius:0.5rem; box-shadow:var(--card-shadow); padding:18px 20px; min-height:148px;
  display:flex; flex-direction:column; justify-content:space-between;
  transition:box-shadow .2s ease; }
.kpi-card:hover{ box-shadow:var(--card-shadow), 0 8px 28px rgba(0,0,0,0.08); }
.kpi-mini{ min-height:118px; }
.kpi-head{ display:flex; justify-content:space-between; align-items:center; gap:8px; }
.kpi-label{ font-family:var(--font-label); font-size:11px; letter-spacing:0.08em;
  text-transform:uppercase; color:var(--on-surface-variant); }
.kpi-icon{ color:var(--primary-container); }
.kpi-icon.star{ color:var(--tertiary); }
.kpi-icon.warn{ color:var(--error); }
.kpi-value{ font-family:var(--font-head); font-size:26px; font-weight:800;
  color:var(--on-surface); letter-spacing:-0.02em; margin-top:10px; white-space:nowrap; }
.kpi-value-sm{ font-size:20px; white-space:normal; }
.kpi-foot{ display:flex; justify-content:space-between; align-items:center; gap:8px;
  margin-top:14px; padding-top:12px; border-top:1px solid var(--surface-container-high); }
.kpi-sub{ font-family:var(--font-label); font-size:11px; color:var(--outline); }
.kpi-delta{ display:flex; align-items:center; gap:4px; font-family:var(--font-label);
  font-size:11px; font-weight:500; padding:4px 10px; border-radius:999px; }
.kpi-delta.up{ background:color-mix(in srgb, var(--secondary-container) 32%, transparent); color:var(--on-secondary-container); }
.kpi-delta.down{ background:color-mix(in srgb, var(--error-container) 32%, transparent); color:var(--on-error-container); }
.kpi-bar{ height:6px; border-radius:999px; background:var(--surface-container-highest);
  margin-top:14px; overflow:hidden; }
.kpi-bar-fill{ height:100%; border-radius:999px; }
.kpi-bar-label{ font-family:var(--font-label); font-size:11px; text-align:right;
  margin-top:6px; color:var(--outline); }
.kpi-spark{ display:flex; align-items:flex-end; gap:6px; height:44px; margin-top:14px; }
.kpi-spark i{ background:var(--primary-container); border-radius:3px 3px 0 0; opacity:0.8; flex:1; }

.lectura{ background:color-mix(in srgb, var(--tertiary-container) 14%, transparent);
  border-left:3px solid var(--tertiary-container); border-radius:0.5rem; padding:12px 16px; margin-top:10px; }
.lectura .lectura-titulo{ font-family:var(--font-label); font-size:11px; font-weight:500;
  letter-spacing:0.1em; text-transform:uppercase; color:var(--on-tertiary-container); margin-bottom:6px; }
.lectura ul{ margin:0; padding-left:18px; }
.lectura li{ font-size:13px; color:var(--on-surface); margin-bottom:4px; }
.recomendacion{ background:color-mix(in srgb, var(--secondary-container) 14%, transparent);
  border-left:3px solid var(--secondary); border-radius:0.5rem; padding:12px 16px; margin-top:10px; }
.recomendacion .reco-titulo{ font-family:var(--font-label); font-size:11px; font-weight:500;
  letter-spacing:0.1em; text-transform:uppercase; color:var(--on-secondary-container); margin-bottom:6px; }
.recomendacion p{ margin:0; font-size:13px; color:var(--on-surface); }

.stButton>button, .stDownloadButton>button{
  background:var(--primary); color:var(--on-primary); border:none; border-radius:0.5rem;
  font-family:var(--font-label); font-size:11px; font-weight:500; letter-spacing:0.06em;
  text-transform:uppercase; padding:0.55rem 1rem; }
.stButton>button:hover{ background:var(--primary-container); color:#ffffff; border:none; }
button[kind="secondary"], .stButton>button[kind="secondary"]{
  background:transparent; border:1px solid var(--outline-variant); color:var(--primary); }
button[kind="secondary"]:hover, .stButton>button[kind="secondary"]:hover{ border:1px solid var(--primary); }

.stTabs [data-baseweb="tab-list"]{ gap:4px; border-bottom:1px solid var(--outline-variant); }
.stTabs [data-baseweb="tab"]{ font-family:var(--font-label); font-size:11px; letter-spacing:0.06em;
  text-transform:uppercase; color:var(--on-surface-variant); padding:12px 14px; }
.stTabs [aria-selected="true"]{ color:var(--primary); font-weight:600; border-bottom:2px solid var(--primary); }
.stTabs [data-baseweb="tab-highlight"]{ background:var(--primary); }

[data-testid="stExpander"]{ border:1px solid var(--outline-variant); border-radius:0.5rem;
  background:var(--surface-container-lowest); overflow:hidden; }
[data-testid="stExpander"] summary{ font-family:var(--font-label); font-size:11px;
  letter-spacing:0.06em; text-transform:uppercase; color:var(--on-surface); }

[data-testid="stRadio"] label, [data-testid="stMultiSelect"] label,
[data-testid="stSelectbox"] label, [data-testid="stDateInput"] label{
  font-family:var(--font-label); font-size:11px; letter-spacing:0.04em; color:var(--on-surface-variant); }
[data-baseweb="select"] > div{ background:var(--surface-container-lowest);
  border:1px solid var(--outline-variant); color:var(--on-surface); border-radius:0.5rem; }
[data-testid="stDataFrame"]{ border:1px solid var(--outline-variant); border-radius:0.5rem; }
.stAlert{ border-radius:0.5rem; }
.stAppDeployButton{ display:none !important; }
</style>
"""


def inyectar_css() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)


_MESES_ES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]


def formatear_dinero(valor: float) -> str:
    entero = int(round(valor))
    signo = "-" if entero < 0 else ""
    digitos = str(abs(entero))
    buffer = []
    for i, ch in enumerate(digitos):
        if i > 0 and (len(digitos) - i) % 3 == 0:
            buffer.append(".")
        buffer.append(ch)
    return f"{signo}${''.join(buffer)}"


def formatear_monto_corto(valor: float) -> str:
    if abs(valor) >= 1_000_000:
        return f"${valor / 1_000_000:,.1f}M"
    if abs(valor) >= 1_000:
        return f"${valor / 1_000:,.0f}k"
    return formatear_dinero(valor)


def fecha_es(fecha) -> str:
    return f"{fecha.day:02d} {_MESES_ES[fecha.month - 1]} {fecha.year}"


def tarjeta_kpi(label, valor, icono=None, icono_clase="", sub="", delta=None,
                delta_sube=True, bar=None, bar_color=None, bar_label="", spark=None,
                valor_sm=False, color=None) -> str:
    head_icon = f'<span class="material-symbols-outlined kpi-icon {icono_clase}">{icono}</span>' if icono else ""
    value_style = f"color:{color};" if color else ""
    cls = "kpi-value kpi-value-sm" if valor_sm else "kpi-value"
    delta_html = ""
    if delta is not None:
        d = "up" if delta_sube else "down"
        ico = "trending_up" if delta_sube else "trending_down"
        delta_html = (f'<span class="kpi-delta {d}">'
                      f'<span class="material-symbols-outlined" style="font-size:14px">{ico}</span>{delta}</span>')
    bar_html = ""
    if bar is not None:
        bc = bar_color or "var(--primary-container)"
        bar_html = (f'<div class="kpi-bar"><div class="kpi-bar-fill" '
                    f'style="width:{min(bar, 100):.0f}%;background:{bc}"></div></div>'
                    f'<div class="kpi-bar-label">{bar_label}</div>')
    spark_html = ""
    if spark:
        barras = "".join(f'<i style="height:{max(h, 8)}px"></i>' for h in spark)
        spark_html = f'<div class="kpi-spark">{barras}</div>'
    foot = (f'<div class="kpi-foot"><span class="kpi-sub">{sub}</span>{delta_html}</div>'
            if sub or delta_html else "")
    return (f'<div class="kpi-card">'
            f'<div class="kpi-head"><span class="kpi-label">{label}</span>{head_icon}</div>'
            f'<div class="{cls}" style="{value_style}">{valor}</div>'
            f'{bar_html}{spark_html}{foot}'
            f'</div>')


def kpi(label: str, valor: str, sub: str = "", color: str = "") -> None:
    value_style = f"color:{color};" if color else ""
    st.markdown(
        f'<div class="kpi-card kpi-mini">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value" style="{value_style}">{valor}</div>'
        f'<div class="kpi-sub">{sub}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def cabecera(df, meta) -> None:
    chip = ""
    if df is not None and meta and meta.get("fecha"):
        col = pd.to_datetime(df[meta["fecha"]])
        if len(col):
            rango = f"{fecha_es(col.min().date())} - {fecha_es(col.max().date())}"
            chip = (f'<span class="theview-chip">'
                    f'<span class="material-symbols-outlined">calendar_month</span>'
                    f'<span>{rango}</span></span>')
    marca = (f'<div class="theview-brand">'
             f'<div class="theview-logo">TV</div>'
             f'<h1 class="theview-title">The View</h1>'
             f'{chip}</div>')

    izq, der = st.columns([5, 1], vertical_alignment="center")
    with izq:
        st.markdown(marca, unsafe_allow_html=True)
    with der:
        with st.popover("⋮", help="Ajustes de apariencia"):
            st.markdown('<div class="menu-titulo">APARIENCIA</div>', unsafe_allow_html=True)
            st.radio("Tema", ["Oscuro", "Sistema"], key="tema", label_visibility="collapsed")
            st.markdown('<div class="menu-titulo">PALETA DE COLORES</div>', unsafe_allow_html=True)
            st.radio("Paleta", list(PALETAS.keys()), key="paleta", label_visibility="collapsed")
            st.divider()
            st.caption("The View · v1.0 · dashboard con lectura automática y recomendaciones")
    st.markdown('<div class="theview-divider"></div>', unsafe_allow_html=True)


def mostrar_lectura(frases) -> None:
    if not frases:
        return
    items = "".join(f"<li>{f}</li>" for f in frases)
    st.markdown(
        f"""
        <div class="lectura">
          <div class="lectura-titulo">LECTURA AUTOMÁTICA</div>
          <ul>{items}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def mostrar_recomendaciones(frases) -> None:
    if not frases:
        return
    parrafos = "".join(f"<p>{f}</p>" for f in frases)
    st.markdown(
        f"""
        <div class="recomendacion">
          <div class="reco-titulo">RECOMENDACIÓN</div>
          {parrafos}
        </div>
        """,
        unsafe_allow_html=True,
    )


_SEED = itertools.count()


def _clave_grafico(fig) -> str:
    titulo = fig.layout.title.text if fig.layout.title else ""
    return f"plot_{next(_SEED)}_{titulo}"


def mostrar_grafico(fig) -> None:
    clave = _clave_grafico(fig)
    try:
        st.plotly_chart(fig, width="stretch", key=clave)
    except Exception:
        try:
            st.plotly_chart(fig, use_container_width=True, key=clave)
        except Exception:
            st.plotly_chart(fig, key=clave)


def mostrar_tabla(df) -> None:
    clave = f"tabla_{next(_SEED)}"
    try:
        st.dataframe(df, width="stretch", height=380, key=clave)
    except Exception:
        try:
            st.dataframe(df, use_container_width=True, key=clave)
        except Exception:
            st.dataframe(df, key=clave)
