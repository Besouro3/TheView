import numpy as np
import pandas as pd
import plotly.graph_objects as go

_OSCURO = True


def set_tema(oscuro: bool) -> None:
    global _OSCURO
    _OSCURO = oscuro


def _acento() -> str:
    return "#A0C9FF" if _OSCURO else "#0F4C81"


def _texto() -> str:
    return "#E6EBEF" if _OSCURO else "#181C1E"


def _grid() -> str:
    return "rgba(148,163,184,0.22)" if _OSCURO else "rgba(24,28,30,0.08)"


def _colores() -> list:
    return (["#A0C9FF", "#65DCA4", "#48D7F9", "#FFB4AB", "#B7C1C9",
             "#8AB4F8", "#81C995", "#F9ABA0"]
            if _OSCURO else
            ["#0F4C81", "#006C47", "#003945", "#BA1A1A", "#005262",
             "#2D6197", "#38761D", "#E8710A"])


def _layout(fig, titulo: str, eje_x: str = "", eje_y: str = "") -> None:
    fig.update_layout(
        title={"text": titulo, "x": 0.5, "xanchor": "center", "font": {"size": 15, "family": "Manrope"}},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": _texto(), "family": "Inter"},
        margin=dict(l=50, r=20, t=55, b=40),
        xaxis_title=eje_x,
        yaxis_title=eje_y,
        legend={"orientation": "h", "y": 1.12},
    )
    fig.update_xaxes(gridcolor=_grid())
    fig.update_yaxes(gridcolor=_grid())


def grafico_barras(df: pd.DataFrame, grupo: str, valor: str) -> go.Figure:
    agg = df.groupby(grupo, as_index=False)[valor].sum().sort_values(valor, ascending=False)
    fig = go.Figure(go.Bar(
        x=agg[valor], y=agg[grupo], orientation="h",
        marker_color=_acento(), text=[f"${v:,.0f}" for v in agg[valor]], textposition="outside",
        textfont={"color": _texto()},
    ))
    _layout(fig, f"Ventas por {grupo}", eje_x="Total")
    return fig


def grafico_lineas(df: pd.DataFrame, fecha: str, valor: str) -> go.Figure:
    serie = df.copy()
    serie["_mes"] = serie[fecha].dt.to_period("M").astype(str)
    agg = serie.groupby("_mes", as_index=False)[valor].sum()
    fig = go.Figure(go.Scatter(
        x=agg["_mes"], y=agg[valor], mode="lines+markers",
        line={"color": _acento(), "width": 3}, marker={"size": 6, "color": _acento()},
        fill="tozeroy", fillcolor="rgba(15,76,129,0.08)",
    ))
    _layout(fig, "Evolución mensual", eje_x="Mes", eje_y="Total")
    return fig


def grafico_pie(df: pd.DataFrame, grupo: str, valor: str) -> go.Figure:
    agg = df.groupby(grupo, as_index=False)[valor].sum().sort_values(valor, ascending=False)
    fig = go.Figure(go.Pie(
        labels=agg[grupo], values=agg[valor], hole=0.45,
        marker={"colors": _colores()},
        textinfo="label+percent", textposition="auto",
        textfont={"size": 12},
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={"color": _texto(), "family": "Inter"},
                      showlegend=False, margin=dict(l=10, r=10, t=30, b=10))
    return fig


def grafico_calor(df: pd.DataFrame, fila: str, col: str, valor: str) -> go.Figure:
    pivot = df.pivot_table(index=fila, columns=col, values=valor, aggfunc="sum", fill_value=0)
    texto = [[_formato_corto(v) for v in fila_valores] for fila_valores in pivot.values]
    escala = ([[0, "#1F2C38"], [0.5, "#0F4C81"], [1, "#48D7F9"]]
              if _OSCURO else
              [[0, "#E2ECF7"], [0.5, "#0F4C81"], [1, "#006C47"]])
    fig = go.Figure(go.Heatmap(
        z=pivot.values, x=pivot.columns.tolist(), y=pivot.index.tolist(),
        text=texto, texttemplate="%{text}",
        colorscale=escala,
        colorbar={"title": "Total"},
    ))
    _layout(fig, f"Mapa de calor: {fila} × {col}", eje_x=col, eje_y=fila)
    return fig


def grafico_box(df: pd.DataFrame, grupo: str, valor: str) -> go.Figure:
    colores = _colores()
    fig = go.Figure()
    for i, g in enumerate(sorted(df[grupo].dropna().unique())):
        fig.add_trace(go.Box(
            y=df[df[grupo] == g][valor], name=str(g),
            marker_color=colores[i % len(colores)],
        ))
    _layout(fig, f"Distribución por {grupo}", eje_y=valor)
    return fig


def grafico_histograma(df: pd.DataFrame, valor: str) -> go.Figure:
    fig = go.Figure(go.Histogram(
        x=df[valor], nbinsx=24, marker_color=_acento(),
        marker_line={"color": "rgba(0,0,0,0)", "width": 1},
    ))
    _layout(fig, f"Histograma de {valor}", eje_x=valor, eje_y="Frecuencia")
    return fig


def grafico_dispersion(df: pd.DataFrame, x: str, y: str) -> go.Figure:
    datos = df[[x, y]].dropna().astype(float)
    xv, yv = datos[x], datos[y]
    fig = go.Figure(go.Scatter(
        x=xv, y=yv, mode="markers",
        marker={"color": _acento(), "opacity": 0.55, "size": 7},
    ))
    if len(datos) >= 3:
        coef = np.polyfit(xv, yv, 1)
        xline = np.linspace(xv.min(), xv.max(), 50)
        fig.add_trace(go.Scatter(
            x=xline, y=np.polyval(coef, xline), mode="lines",
            line={"color": "#F59E0B", "width": 2, "dash": "dash"},
            name="Tendencia",
        ))
    _layout(fig, f"Relación entre {x} y {y}", eje_x=x, eje_y=y)
    return fig


def _formato_corto(v) -> str:
    if v >= 1_000_000:
        return f"${v / 1_000_000:.1f}M"
    if v >= 1_000:
        return f"${v / 1_000:.0f}k"
    return f"${v:,.0f}"
