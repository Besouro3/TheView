import itertools

import pandas as pd
import streamlit as st

TEAL = "#0F4C81"
AMBER = "#F59E0B"
GREEN = "#006C47"
RED = "#BA1A1A"

_TEMA_CLARO = """
:root{
  --bg:#f7fafc; --surface:#f7fafc; --surface-lowest:#ffffff;
  --surface-container:#ebeef0; --surface-container-high:#e5e9eb; --surface-container-highest:#e0e3e5;
  --outline:#727780; --outline-variant:#c2c7d1;
  --on-surface:#181c1e; --on-surface-variant:#42474f;
  --primary:#00355f; --primary-container:#0f4c81; --on-primary:#ffffff;
  --secondary:#006c47; --secondary-container:#82f9be; --on-secondary-container:#00734c;
  --tertiary:#003945; --tertiary-container:#005262; --on-tertiary-container:#35caec;
  --error:#ba1a1a; --error-container:#ffdad6; --on-error-container:#93000a;
  --card-shadow: 0 4px 20px rgba(15,76,129,0.06);
}
"""

_TEMA_OSCURO = """
:root{
  --bg:#0f141a; --surface:#0f141a; --surface-lowest:#161d24;
  --surface-container:#1a222b; --surface-container-high:#202933; --surface-container-highest:#26313c;
  --outline:#8d99a3; --outline-variant:#3a434d;
  --on-surface:#e6ebef; --on-surface-variant:#b7c1c9;
  --primary:#a0c9ff; --primary-container:#0f4c81; --on-primary:#0a3556;
  --secondary:#65dca4; --secondary-container:#00734c; --on-secondary-container:#82f9be;
  --tertiary:#48d7f9; --tertiary-container:#005262; --on-tertiary-container:#afecff;
  --error:#ffb4ab; --error-container:#93000a; --on-error-container:#ffdad6;
  --card-shadow: 0 4px 20px rgba(0,0,0,0.35);
}
"""

_TEMA_SISTEMA = _TEMA_OSCURO + """
@media (prefers-color-scheme: light){ :root{"""
_TEMA_SISTEMA += _TEMA_CLARO.replace(":root{", "").replace("}", "}")
_TEMA_SISTEMA += "} }"


def inyectar_tema(modo: str) -> None:
    bloque = {"Oscuro": _TEMA_OSCURO, "Claro": _TEMA_CLARO, "Sistema": _TEMA_SISTEMA}.get(modo, _TEMA_OSCURO)
    st.markdown(f"<style>{bloque}</style>", unsafe_allow_html=True)


_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Manrope:wght@600;700;800&family=JetBrains+Mono:wght@500&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL@20..48,100..700,0..1&display=swap');

:root{
  --bg:#f7fafc; --surface:#f7fafc; --surface-lowest:#ffffff;
  --surface-container:#ebeef0; --surface-container-high:#e5e9eb; --surface-container-highest:#e0e3e5;
  --outline:#727780; --outline-variant:#c2c7d1;
  --on-surface:#181c1e; --on-surface-variant:#42474f;
  --primary:#00355f; --primary-container:#0f4c81; --on-primary:#ffffff;
  --secondary:#006c47; --secondary-container:#82f9be; --on-secondary-container:#00734c;
  --tertiary:#003945; --tertiary-container:#005262; --on-tertiary-container:#35caec;
  --error:#ba1a1a; --error-container:#ffdad6; --on-error-container:#93000a;
  --card-shadow: 0 4px 20px rgba(15,76,129,0.06);
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
[data-testid="stHeader"]{ background:transparent; }
[data-testid="stSidebar"]{ background:var(--surface-container); border-right:1px solid var(--outline-variant); }
[data-testid="stSidebar"] .block-container{ max-width:100%; }
h1,h2,h3,h4{ font-family:var(--font-head); color:var(--on-surface); }
p, li{ color:var(--on-surface); }

.theview-header{ display:flex; align-items:center; justify-content:space-between; gap:12px;
  border-bottom:1px solid var(--outline-variant); padding-bottom:16px; margin-bottom:8px; }
.theview-brand{ display:flex; align-items:center; gap:12px; }
.theview-logo{ width:36px; height:36px; border-radius:999px; background:var(--primary-container);
  color:#ffffff; display:flex; align-items:center; justify-content:center;
  font-family:var(--font-head); font-weight:800; font-size:14px; }
.theview-title{ font-family:var(--font-head); font-size:24px; font-weight:800;
  color:var(--primary); letter-spacing:-0.01em; margin:0; }
.theview-chip{ display:flex; align-items:center; gap:8px; border:1px solid var(--outline-variant);
  background:var(--surface-lowest); border-radius:999px; padding:8px 14px;
  font-family:var(--font-label); font-size:12px; color:var(--on-surface-variant); }
.theview-chip .material-symbols-outlined{ font-size:16px; color:var(--outline); }

.kpi-card{ background:var(--surface-container-lowest); border:1px solid var(--outline-variant);
  border-radius:0.5rem; box-shadow:var(--card-shadow); padding:18px 20px; min-height:148px;
  display:flex; flex-direction:column; justify-content:space-between;
  transition:box-shadow .2s ease, transform .2s ease; }
.kpi-card:hover{ box-shadow:var(--card-shadow), 0 8px 28px rgba(15,76,129,0.10); }
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
            chip = (f'<div class="theview-chip">'
                    f'<span class="material-symbols-outlined">calendar_month</span>'
                    f'<span>{rango}</span></div>')
    st.markdown(
        f'<div class="theview-header">'
        f'<div class="theview-brand">'
        f'<div class="theview-logo">TV</div>'
        f'<h1 class="theview-title">The View</h1>'
        f'</div>{chip}</div>',
        unsafe_allow_html=True,
    )


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
