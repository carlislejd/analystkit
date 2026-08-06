"""Plotly theme management — the core of AnalystKit.

apply_theme() is the main entry point. It brands any Plotly figure with
Bitwise styling: colors, fonts, grid, legend, and — crucially — font sizes
that scale automatically with the chart dimensions so you never have to
fiddle with point sizes when switching between a 825px sidebar chart and
a 1800px full-width hero.
"""

import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from .colors import (
    STYLE_DEFAULTS, CHART_COLORS, SIZE_PRESETS, MARGIN_PRESETS,
    FONT_FAMILIES, FONT_SIZES, COLOR_HIERARCHY, BITWISE_COLORS,
    compute_font_sizes, compute_font_scale,
)


# ─────────────────────────────────────────────
# Internal helpers
# ─────────────────────────────────────────────

def _calculate_axis_buffer(values):
    """Calculate axis range with a small buffer so the tallest bar / highest
    point isn't clipped by the plot boundary."""
    if not values:
        return None
    data = np.array(values)
    data = data[np.isfinite(data)]
    if len(data) == 0:
        return None

    data_min = float(np.min(data))
    data_max = float(np.max(data))
    data_range = data_max - data_min

    buffer = max(data_range * 0.02, abs(data_max) * 0.005)
    return (data_min, data_max + buffer)


def _apply_axis_buffers(fig):
    """Buffer the value-axis so max data points aren't clipped.

    For horizontal bar charts → buffers x-axis.
    For everything else → buffers y-axis.
    """
    is_horizontal_bar = any(
        getattr(t, 'type', None) == 'bar' and getattr(t, 'orientation', None) == 'h'
        for t in fig.data
    )

    if is_horizontal_bar:
        vals = []
        for t in fig.data:
            if hasattr(t, 'x') and t.x is not None:
                try:
                    arr = np.array(t.x, dtype=float)
                except (TypeError, ValueError):
                    continue
                vals.extend(arr[np.isfinite(arr)].tolist())
        rng = _calculate_axis_buffer(vals)
        if rng:
            fig.update_xaxes(range=list(rng))
    else:
        vals = []
        for t in fig.data:
            if hasattr(t, 'y') and t.y is not None:
                try:
                    arr = np.array(t.y, dtype=float)
                except (TypeError, ValueError):
                    continue
                vals.extend(arr[np.isfinite(arr)].tolist())
        rng = _calculate_axis_buffer(vals)
        if rng:
            fig.update_yaxes(range=list(rng))


def _scaled_tick_len(width: int, height: int) -> int:
    """Scale tick-mark length proportionally to chart size."""
    scale = compute_font_scale(width, height)
    return max(6, round(19 * scale))


# ─────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────

def apply_theme(
    fig,
    size_preset: str = 'full',
    margin_preset: str = 'minimal',
    width: int = None,
    height: int = None,
    auto_colors: bool = True,
):
    """Apply the Bitwise brand theme to *any* Plotly figure.

    This is the primary entry point for AnalystKit. It handles:

    • Dimensions — via ``size_preset`` or explicit ``width``/``height``.
    • Font scaling — all font sizes adjust automatically to the chosen
      dimensions so text looks proportional at every aspect ratio.
    • Grid & axes — horizontal gridlines on the y-axis, no vertical grid,
      clean zero-line styling.
    • Legend — horizontal, top-right, transparent background, circle markers.
    • Colors — when ``auto_colors=True`` (default) and traces don't already
      have explicit colors, the Bitwise palette is applied using the
      curated hierarchy.

    Args:
        fig: Any ``plotly.graph_objects.Figure``.
        size_preset: A key from ``SIZE_PRESETS`` (e.g. 'full', '18:9', '1:1').
            Ignored when ``width``/``height`` are given explicitly.
        margin_preset: A key from ``MARGIN_PRESETS`` ('minimal', 'standard', 'wide').
        width: Explicit width in pixels. Overrides ``size_preset``.
        height: Explicit height in pixels. Overrides ``size_preset``.
        auto_colors: When True, apply Bitwise palette automatically to
            traces that don't already have colors set.

    Returns:
        The same figure, mutated in-place (also returned for chaining).
    """

    # --- Resolve dimensions ---------------------------------------------------
    if width is None or height is None:
        size = SIZE_PRESETS.get(size_preset, SIZE_PRESETS['full'])
        width = width or size['width']
        height = height or size['height']

    margin = MARGIN_PRESETS.get(margin_preset, MARGIN_PRESETS['minimal'])

    # --- Compute scaled font sizes --------------------------------------------
    fonts = compute_font_sizes(width, height)
    tick_len = _scaled_tick_len(width, height)

    # --- Layout ---------------------------------------------------------------
    fig.update_layout(
        width=width,
        height=height,
        plot_bgcolor=CHART_COLORS['background'],
        paper_bgcolor=CHART_COLORS['background'],
        font=dict(
            family=FONT_FAMILIES['primary'],
            size=fonts['axis'],
            color=CHART_COLORS['text'],
        ),
        title_font=dict(
            family=FONT_FAMILIES['title'],
            size=fonts['title'],
            color=CHART_COLORS['text'],
        ),
        margin=margin,
    )

    # --- X-axis ---------------------------------------------------------------
    fig.update_xaxes(
        showgrid=STYLE_DEFAULTS['xaxis']['showgrid'],
        zeroline=STYLE_DEFAULTS['xaxis']['zeroline'],
        showline=STYLE_DEFAULTS['xaxis']['showline'],
        title=None,
        tickangle=0,
        ticklen=tick_len,
        tickwidth=1,
        tickcolor=CHART_COLORS['grid_dark'],
        tickfont=dict(
            family=FONT_FAMILIES['primary'],
            size=fonts['axis'],
            color=CHART_COLORS['text'],
        ),
    )

    # --- Y-axis ---------------------------------------------------------------
    fig.update_yaxes(
        showgrid=STYLE_DEFAULTS['yaxis']['showgrid'],
        gridwidth=STYLE_DEFAULTS['yaxis']['gridwidth'],
        gridcolor=STYLE_DEFAULTS['yaxis']['gridcolor'],
        zeroline=STYLE_DEFAULTS['yaxis']['zeroline'],
        zerolinewidth=STYLE_DEFAULTS['yaxis']['zerolinewidth'],
        zerolinecolor=STYLE_DEFAULTS['yaxis']['zerolinecolor'],
        showline=STYLE_DEFAULTS['yaxis']['showline'],
        title=None,
        ticklen=tick_len,
        tickwidth=1,
        tickcolor=CHART_COLORS['grid_dark'],
        tickfont=dict(
            family=FONT_FAMILIES['axis'],
            size=fonts['axis'],
            color=CHART_COLORS['text'],
        ),
    )

    # --- Axis buffers ---------------------------------------------------------
    _apply_axis_buffers(fig)

    # --- Legend ----------------------------------------------------------------
    fig.update_layout(
        legend=dict(
            borderwidth=0,
            bgcolor='rgba(0,0,0,0)',
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1,
            title=None,
            traceorder='normal',
            font=dict(
                family=FONT_FAMILIES['primary'],
                size=fonts['legend'],
                color=CHART_COLORS['text'],
            ),
        ),
    )

    # --- Auto-color traces ----------------------------------------------------
    if auto_colors:
        _auto_apply_colors(fig)

    return fig


def _auto_apply_colors(fig):
    """Apply Bitwise color hierarchy to traces that lack explicit colors."""
    traces = [t for t in fig.data if t.name and t.showlegend is not False]
    n = len(traces) if traces else len(fig.data)
    if n == 0:
        return

    colors = get_color_palette(n)

    for i, trace in enumerate(fig.data):
        color = colors[i % len(colors)]
        trace_type = getattr(trace, 'type', '')

        # Only apply if no explicit color is already set
        has_color = False
        if hasattr(trace, 'marker') and trace.marker and getattr(trace.marker, 'color', None):
            has_color = True
        if hasattr(trace, 'line') and trace.line and getattr(trace.line, 'color', None):
            has_color = True

        if has_color:
            continue

        if trace_type == 'bar':
            trace.update(marker_color=color)
        elif trace_type in ('scatter', 'scattergl'):
            trace.update(marker_color=color, line_color=color)
        elif trace_type == 'pie':
            # Pie charts get the full palette as a sequence
            if not getattr(trace.marker, 'colors', None):
                trace.update(marker_colors=colors[:len(trace.labels or [])])
        elif trace_type in ('heatmap', 'contour'):
            pass  # Heatmaps use colorscale, not individual colors
        else:
            # Generic fallback — try marker then line
            try:
                trace.update(marker_color=color)
            except Exception:
                pass
            try:
                trace.update(line_color=color)
            except Exception:
                pass


def get_color_palette(n_colors: int):
    """Get N colors from the Bitwise brand palette.

    For 1–11 colors, returns the curated hierarchy subset.
    For >11, cycles through the full palette.

    Args:
        n_colors: Number of distinct colors needed.

    Returns:
        List of hex color strings.
    """
    if n_colors <= 0:
        return []
    if n_colors <= 11:
        return COLOR_HIERARCHY.get(n_colors, BITWISE_COLORS[:n_colors])
    import itertools
    return list(itertools.islice(itertools.cycle(BITWISE_COLORS), n_colors))
