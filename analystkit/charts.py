"""Chart creation helpers and export utilities.

The philosophy: apply_theme() is the engine — it can brand ANY Plotly
figure. The functions here are thin convenience wrappers that handle
common data-munging patterns and call apply_theme() under the hood.

For chart types not covered by a wrapper, build the figure with Plotly
directly and then call ``ak.apply_theme(fig)`` to brand it.
"""

import os
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Union, Callable
from datetime import datetime, timedelta

from .plotly_theme import apply_theme, get_color_palette
from .colors import (
    SIZE_PRESETS, COLOR_HIERARCHY, FONT_SIZES, FONT_FAMILIES,
    compute_font_sizes, compute_font_scale,
)


# ─────────────────────────────────────────────
# Legend helper
# ─────────────────────────────────────────────

def _apply_scatter_legend_markers(fig: go.Figure, marker_size: int = 10) -> go.Figure:
    """Replace all legend symbols with uniform scatter-circle markers.

    This gives a consistent legend appearance across bar, line, area, and
    other chart types — every legend entry is a filled circle.
    """
    traces_to_process = []

    for trace in fig.data:
        if not (trace.name and trace.showlegend is not False):
            continue

        color = None
        if hasattr(trace, 'marker') and trace.marker:
            color = getattr(trace.marker, 'color', None)
        if not color and hasattr(trace, 'line') and trace.line:
            color = getattr(trace.line, 'color', None)
        if not color and hasattr(trace, 'fillcolor'):
            color = trace.fillcolor
        if not color:
            color = COLOR_HIERARCHY[1][0]

        if isinstance(color, (list, np.ndarray)) and len(color) > 0:
            color = color[0] if isinstance(color[0], str) else COLOR_HIERARCHY[1][0]

        traces_to_process.append({
            'trace': trace,
            'name': trace.name,
            'color': color,
            'legendgroup': getattr(trace, 'legendgroup', trace.name),
        })

    for info in traces_to_process:
        info['trace'].showlegend = False
        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode='markers',
            marker=dict(size=marker_size, color=info['color']),
            showlegend=True,
            name=info['name'],
            legendgroup=info['legendgroup'],
            hoverinfo='skip',
        ))

    return fig


# ─────────────────────────────────────────────
# Convenience chart constructors
# ─────────────────────────────────────────────

def create_chart(
    data: Union[pd.DataFrame, List, Dict],
    chart_type: str = "bar",
    x: Optional[str] = None,
    y: Optional[str] = None,
    x_label: str = "",
    y_label: str = "",
    color_column: Optional[str] = None,
    size_preset: str = "full",
    margin_preset: str = "minimal",
    width: int = None,
    height: int = None,
    scatter_legend: bool = True,
    **kwargs,
) -> go.Figure:
    """Create a branded chart from data.

    This is the main convenience wrapper. It builds a Plotly Express figure
    for the requested ``chart_type``, applies the Bitwise theme (with
    automatic font scaling), and returns a ready-to-export figure.

    For chart types not listed here, build the figure with Plotly directly
    and call ``ak.apply_theme(fig)`` instead.

    Args:
        data: DataFrame, list, or dict.
        chart_type: One of 'bar', 'line', 'scatter', 'area', 'pie',
            'histogram', 'box', 'violin', 'funnel', 'treemap', 'sunburst'.
        x: Column name for x-axis (DataFrame) or ignored for simple data.
        y: Column name for y-axis (DataFrame) or ignored for simple data.
        x_label: Optional x-axis title.
        y_label: Optional y-axis title.
        color_column: Column for color grouping.
        size_preset: Size preset key (ignored when width/height given).
        margin_preset: Margin preset key.
        width: Explicit chart width in pixels.
        height: Explicit chart height in pixels.
        scatter_legend: Replace legend symbols with circle markers (default True).
        **kwargs: Passed through to the underlying Plotly Express call.

    Returns:
        A styled ``go.Figure``.
    """
    # Build the base figure
    fig = _build_figure(data, chart_type, x, y, color_column, **kwargs)

    # Hide axis titles by default
    fig.update_xaxes(title=None)
    fig.update_yaxes(title=None)

    # Apply theme (handles fonts, colors, grid, legend)
    fig = apply_theme(
        fig,
        size_preset=size_preset,
        margin_preset=margin_preset,
        width=width,
        height=height,
        auto_colors=True,
    )

    # Scatter-circle legend markers
    if scatter_legend and chart_type not in ('pie', 'treemap', 'sunburst'):
        fig = _apply_scatter_legend_markers(fig)

    # Axis labels (only when explicitly provided)
    if x_label:
        fig.update_xaxes(title_text=x_label)
    if y_label:
        fig.update_yaxes(title_text=y_label)

    return fig


def _build_figure(data, chart_type, x, y, color_column, **kwargs):
    """Dispatch to the right Plotly Express function."""

    # Coerce simple data types into a DataFrame
    if not isinstance(data, pd.DataFrame):
        data = _coerce_to_dataframe(data)
        if x is None:
            x = 'x'
        if y is None:
            y = 'y'

    # Require x/y for DataFrame-based charts (except pie, histogram, etc.)
    needs_xy = chart_type in ('bar', 'line', 'scatter', 'area', 'funnel')
    if needs_xy and not (x and y):
        raise ValueError(f"Both x and y must be specified for '{chart_type}' with DataFrame input")

    px_kwargs = {}
    if color_column:
        px_kwargs['color'] = color_column

    dispatch = {
        'bar': px.bar,
        'line': px.line,
        'scatter': px.scatter,
        'area': px.area,
        'pie': px.pie,
        'histogram': px.histogram,
        'box': px.box,
        'violin': px.violin,
        'funnel': px.funnel,
        'treemap': px.treemap,
        'sunburst': px.sunburst,
    }

    fn = dispatch.get(chart_type)
    if fn is None:
        raise ValueError(
            f"Unsupported chart_type '{chart_type}'. "
            f"Supported: {list(dispatch.keys())}. "
            f"For other types, build the figure with Plotly and call ak.apply_theme()."
        )

    # Pie / treemap / sunburst use 'names' and 'values' instead of x/y
    if chart_type in ('pie', 'treemap', 'sunburst'):
        names_col = kwargs.pop('names', x)
        values_col = kwargs.pop('values', y)
        return fn(data, names=names_col, values=values_col, **px_kwargs, **kwargs)

    if chart_type == 'histogram':
        return fn(data, x=x, **px_kwargs, **kwargs)

    return fn(data, x=x, y=y, **px_kwargs, **kwargs)


def _coerce_to_dataframe(data):
    """Turn a dict or list into a two-column DataFrame with 'x' and 'y'."""
    if isinstance(data, dict):
        return pd.DataFrame({'x': list(data.keys()), 'y': list(data.values())})
    elif isinstance(data, list):
        if data and isinstance(data[0], (list, tuple)) and len(data[0]) == 2:
            return pd.DataFrame(data, columns=['x', 'y'])
        return pd.DataFrame({'x': range(len(data)), 'y': data})
    raise ValueError("Data must be a DataFrame, dict, or list")


# Backward-compatible aliases
def create_bar_chart(data, x=None, y=None, orientation="v", **kwargs):
    """Create a styled bar chart. See ``create_chart`` for full docs."""
    return create_chart(data, chart_type="bar", x=x, y=y, orientation=orientation, **kwargs)


def create_line_chart(data, x=None, y=None, **kwargs):
    """Create a styled line chart. See ``create_chart`` for full docs."""
    return create_chart(data, chart_type="line", x=x, y=y, **kwargs)


# ─────────────────────────────────────────────
# Export
# ─────────────────────────────────────────────

# Supported static image formats (via kaleido)
_KALEIDO_FORMATS = {'svg', 'png', 'jpg', 'jpeg', 'pdf', 'webp', 'eps'}


def export_chart(
    fig: go.Figure,
    filename: str,
    format: str = "svg",
    width: Optional[int] = None,
    height: Optional[int] = None,
    scale: int = 2,
) -> str:
    """Export a chart to a file.

    Supports all Plotly static image formats (svg, png, jpg, jpeg, pdf,
    webp, eps) via kaleido, plus interactive formats (html, json).

    Args:
        fig: Plotly figure to export.
        filename: Output path. Extension is appended if missing.
        format: Export format string.
        width: Override width (default: figure's own width).
        height: Override height (default: figure's own height).
        scale: Scale factor for raster formats (default 2 for retina).

    Returns:
        The final file path written.
    """
    fmt = format.lower().strip('.')
    if not filename.endswith(f".{fmt}"):
        filename = f"{filename}.{fmt}"

    # Ensure parent directory exists
    parent = os.path.dirname(filename)
    if parent:
        os.makedirs(parent, exist_ok=True)

    export_width = width or getattr(fig.layout, 'width', None) or SIZE_PRESETS['full']['width']
    export_height = height or getattr(fig.layout, 'height', None) or SIZE_PRESETS['full']['height']

    if fmt == 'html':
        fig.write_html(filename, include_plotlyjs='cdn')
        return filename

    if fmt == 'json':
        fig.write_json(filename)
        return filename

    if fmt in _KALEIDO_FORMATS:
        try:
            import kaleido  # noqa: F401
        except ImportError:
            raise ImportError(
                "Static image export requires kaleido. "
                "Install with: pip install kaleido"
            )
        try:
            fig.write_image(
                filename,
                width=export_width,
                height=export_height,
                scale=scale,
            )
        except Exception as exc:
            raise RuntimeError(
                "Static image export requires a working Kaleido/Chrome runtime. "
                "Install or repair Kaleido and Chrome, then retry."
            ) from exc
        return filename

    raise ValueError(
        f"Unsupported format '{fmt}'. "
        f"Supported: {sorted(_KALEIDO_FORMATS | {'html', 'json'})}"
    )


def save_chart(
    fig: go.Figure,
    title: str,
    output_dir: str = "design",
    aspect_ratio: str = "18:9",
    formats: Optional[List[str]] = None,
    include_svg: bool = True,
    include_png: bool = True,
    include_1x1: bool = False,
    png_scale: int = 2,
) -> Dict[str, str]:
    """Save a chart in multiple formats with consistent aspect ratios.

    Args:
        fig: Plotly figure to save.
        title: Chart title (used for filename).
        output_dir: Target directory (created if needed).
        aspect_ratio: Size key from SIZE_PRESETS, or a standard ratio
            string ('18:9', '3:1', '1:1', '16:9', '4:3', 'type_a'…'type_f').
        formats: List of format strings to export (e.g. ['svg', 'png', 'html']).
            When provided, ``include_svg`` and ``include_png`` are ignored.
        include_svg: Legacy flag — export SVG (default True).
        include_png: Legacy flag — export PNG (default True).
        include_1x1: Also export 1:1 square versions (default False).
        png_scale: Scale factor for raster formats (default 2).

    Returns:
        Dict mapping format labels to file paths.
    """
    os.makedirs(output_dir, exist_ok=True)
    clean = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
    clean = clean.replace(' ', '_')

    # Resolve dimensions
    dims = SIZE_PRESETS.get(aspect_ratio)
    if dims is None:
        raise ValueError(
            f"Unknown aspect_ratio '{aspect_ratio}'. "
            f"Available: {list(SIZE_PRESETS.keys())}"
        )

    # Determine which formats to export
    if formats:
        fmt_list = [f.lower().strip('.') for f in formats]
    else:
        fmt_list = []
        if include_svg:
            fmt_list.append('svg')
        if include_png:
            fmt_list.append('png')

    saved = {}
    for fmt in fmt_list:
        path = os.path.join(output_dir, f"{clean}.{fmt}")
        try:
            scale = png_scale if fmt in ('png', 'jpg', 'jpeg', 'webp') else 2
            export_chart(fig, path, format=fmt,
                         width=dims['width'], height=dims['height'],
                         scale=scale)
            saved[fmt] = path
        except ImportError:
            print(f"Warning: {fmt.upper()} export failed — kaleido not installed")

    # Optional 1:1 exports
    if include_1x1:
        sq = SIZE_PRESETS['1:1']
        for fmt in fmt_list:
            path = os.path.join(output_dir, f"{clean}_1x1.{fmt}")
            try:
                scale = png_scale if fmt in ('png', 'jpg', 'jpeg', 'webp') else 2
                export_chart(fig, path, format=fmt,
                             width=sq['width'], height=sq['height'],
                             scale=scale)
                saved[f"{fmt}_1x1"] = path
            except ImportError:
                print(f"Warning: 1:1 {fmt.upper()} export failed — kaleido not installed")

    return saved


# ─────────────────────────────────────────────
# Range tick marks (time-series)
# ─────────────────────────────────────────────

def apply_range_tick_marks(
    fig: go.Figure,
    start_date: Union[str, pd.Timestamp, datetime],
    end_date: Union[str, pd.Timestamp, datetime],
    period: str = "quarter",
    label_formatter: Optional[Callable[[int, int], str]] = None,
    ticklen: int = 10,
    label_y_position: float = -0.01,
    label_font_size: Optional[int] = None,
    label_font_family: Optional[str] = None,
    xaxis_id: str = "x",
    include_start_boundary: bool = True,
    include_end_boundary: bool = True,
    **kwargs,
) -> go.Figure:
    """Apply tick marks at period boundaries with labels at midpoints.

    Creates a pattern where tick marks appear at period START/END dates
    and text labels sit at the MIDPOINT of each period (via annotations).
    This is ideal for quarterly or yearly time-series charts.

    Args:
        fig: Plotly figure to modify.
        start_date: Range start.
        end_date: Range end.
        period: 'quarter', 'year', 'month', or 'week'.
        label_formatter: ``fn(year, period_num) -> str``. Defaults vary
            by period type (e.g. "Q1 '23" for quarters).
        ticklen: Tick mark length in pixels.
        label_y_position: Y-position in paper coords (default -0.01).
        label_font_size: Override label size (default: auto-scaled).
        label_font_family: Override label font family.
        xaxis_id: X-axis identifier (default 'x').
        include_start_boundary: Tick at first period start.
        include_end_boundary: Tick at last period end.
        **kwargs: Extra xaxis layout kwargs.

    Returns:
        Modified figure.
    """
    start_ts = pd.Timestamp(start_date)
    end_ts = pd.Timestamp(end_date)

    # Auto-scale label font size from chart dimensions if not specified
    if label_font_size is None:
        w = getattr(fig.layout, 'width', None) or SIZE_PRESETS['full']['width']
        h = getattr(fig.layout, 'height', None) or SIZE_PRESETS['full']['height']
        fonts = compute_font_sizes(int(w), int(h))
        label_font_size = fonts['axis']
    if label_font_family is None:
        label_font_family = FONT_FAMILIES['primary']

    # Default formatters
    if label_formatter is None:
        formatters = {
            'quarter': lambda yr, q: f"Q{q} '{str(yr)[2:]}",
            'year': lambda yr, _: str(yr),
            'month': lambda yr, m: f"{pd.Timestamp(yr, m, 1).strftime('%b')} '{str(yr)[2:]}",
            'week': lambda yr, w: f"W{w}",
        }
        label_formatter = formatters.get(period, lambda yr, p: f"{p}")

    tick_vals = []
    label_annotations = []

    if period == "quarter":
        _generate_quarter_ticks(start_ts, end_ts, tick_vals, label_annotations,
                                label_formatter, label_y_position, label_font_size,
                                label_font_family, include_start_boundary, include_end_boundary)
    elif period == "year":
        _generate_year_ticks(start_ts, end_ts, tick_vals, label_annotations,
                             label_formatter, label_y_position, label_font_size,
                             label_font_family, include_start_boundary, include_end_boundary)
    elif period == "month":
        _generate_month_ticks(start_ts, end_ts, tick_vals, label_annotations,
                              label_formatter, label_y_position, label_font_size,
                              label_font_family, include_start_boundary, include_end_boundary)
    elif period == "week":
        _generate_week_ticks(start_ts, end_ts, tick_vals, label_annotations,
                             label_formatter, label_y_position, label_font_size,
                             label_font_family, include_start_boundary, include_end_boundary)
    else:
        raise ValueError(f"Unsupported period '{period}'. Use 'quarter', 'year', 'month', or 'week'.")

    tick_vals = _dedupe_adjacent_boundary_ticks(tick_vals, period)

    # Apply to x-axis
    xaxis_dict = dict(
        showgrid=False,
        tickmode='array',
        tickvals=tick_vals,
        ticktext=[''] * len(tick_vals),
        tickangle=0,
        range=[start_ts.strftime('%Y-%m-%d'), end_ts.strftime('%Y-%m-%d')],
        ticks='outside',
        ticklen=ticklen,
        tickwidth=1,
        showticklabels=False,
    )
    xaxis_dict.update(kwargs)
    fig.update_layout(**{f"{xaxis_id}axis": xaxis_dict})

    # Ensure bottom margin accommodates labels
    current_margin = fig.layout.margin or {}
    if isinstance(current_margin, dict):
        fig.update_layout(margin=dict(
            b=max(current_margin.get('b', 70), 70),
            l=current_margin.get('l', 40),
            r=current_margin.get('r', 40),
            t=current_margin.get('t', 60),
        ))

    for ann in label_annotations:
        fig.add_annotation(**ann)

    return fig


# ─────────────────────────────────────────────
# Tick generation helpers (keep the main function readable)
# ─────────────────────────────────────────────

def _make_label_annotation(x_date, text, y_pos, font_size, font_family):
    return dict(
        x=x_date.strftime('%Y-%m-%d'),
        y=y_pos,
        text=text,
        showarrow=False,
        xref='x', yref='paper',
        xanchor='center', yanchor='top',
        font=dict(size=font_size, family=font_family),
    )


def _is_period_start(ts, period):
    if period == "year":
        return ts.month == 1 and ts.day == 1
    if period == "quarter":
        return ts.month in (1, 4, 7, 10) and ts.day == 1
    if period == "month":
        return ts.day == 1
    if period == "week":
        return ts.weekday() == 0
    return False


def _dedupe_adjacent_boundary_ticks(tick_vals, period):
    """Collapse period-end/next-period-start tick pairs into the start tick."""
    if len(tick_vals) <= 1:
        return tick_vals

    deduped = []
    for tick_val in tick_vals:
        current = pd.Timestamp(tick_val)
        if deduped:
            previous = pd.Timestamp(deduped[-1])
            if (current - previous).days == 1 and _is_period_start(current, period):
                deduped[-1] = tick_val
                continue
        deduped.append(tick_val)

    return deduped


def _generate_quarter_ticks(start_ts, end_ts, tick_vals, annotations,
                            formatter, y_pos, font_size, font_family,
                            inc_start, inc_end):
    for year in range(start_ts.year, end_ts.year + 1):
        for q in range(1, 5):
            sm = (q - 1) * 3 + 1
            em = sm + 2
            qs = pd.Timestamp(f'{year}-{sm:02d}-01')
            if em == 12:
                qe = pd.Timestamp(f'{year}-12-31')
            else:
                nm = em + 1
                ny = year + 1 if nm > 12 else year
                nm = 1 if nm > 12 else nm
                qe = pd.Timestamp(f'{ny}-{nm:02d}-01') - pd.Timedelta(days=1)
            qm = qs + pd.Timedelta(days=(qe - qs).days // 2)

            if qe < start_ts or qs > end_ts:
                continue
            if qs >= start_ts and (inc_start or year != start_ts.year or q != 1):
                tick_vals.append(qs.strftime('%Y-%m-%d'))
            if start_ts <= qm <= end_ts:
                annotations.append(_make_label_annotation(qm, formatter(year, q),
                                                          y_pos, font_size, font_family))
            if qe <= end_ts:
                if not (year == end_ts.year and q == 4) or inc_end:
                    tick_vals.append(qe.strftime('%Y-%m-%d'))


def _generate_year_ticks(start_ts, end_ts, tick_vals, annotations,
                         formatter, y_pos, font_size, font_family,
                         inc_start, inc_end):
    for year in range(start_ts.year, end_ts.year + 1):
        ys = pd.Timestamp(f'{year}-01-01')
        ye = pd.Timestamp(f'{year}-12-31')
        ym = pd.Timestamp(f'{year}-07-01')
        if ye < start_ts or ys > end_ts:
            continue
        if ys >= start_ts and (inc_start or year != start_ts.year):
            tick_vals.append(ys.strftime('%Y-%m-%d'))
        if start_ts <= ym <= end_ts:
            annotations.append(_make_label_annotation(ym, formatter(year, year),
                                                      y_pos, font_size, font_family))
        if ye <= end_ts and (inc_end or year != end_ts.year):
            tick_vals.append(ye.strftime('%Y-%m-%d'))


def _generate_month_ticks(start_ts, end_ts, tick_vals, annotations,
                          formatter, y_pos, font_size, font_family,
                          inc_start, inc_end):
    current = start_ts.replace(day=1)
    while current <= end_ts:
        ms = current
        if current.month == 12:
            me = pd.Timestamp(current.year, 12, 31)
            nm = pd.Timestamp(current.year + 1, 1, 1)
        else:
            me = pd.Timestamp(current.year, current.month + 1, 1) - pd.Timedelta(days=1)
            nm = pd.Timestamp(current.year, current.month + 1, 1)

        vs = max(ms, start_ts)
        ve = min(me, end_ts)
        if vs <= ve:
            mm = vs + (ve - vs) / 2
        else:
            mm = ms + pd.Timedelta(days=14)

        if me >= start_ts and ms <= end_ts:
            if ms >= start_ts and (inc_start or current != start_ts.replace(day=1)):
                tick_vals.append(ms.strftime('%Y-%m-%d'))
            if vs <= ve and start_ts <= mm <= end_ts:
                annotations.append(_make_label_annotation(mm, formatter(current.year, current.month),
                                                          y_pos, font_size, font_family))
            if me <= end_ts and (inc_end or nm > end_ts):
                tick_vals.append(me.strftime('%Y-%m-%d'))

        current = nm


def _generate_week_ticks(start_ts, end_ts, tick_vals, annotations,
                         formatter, y_pos, font_size, font_family,
                         inc_start, inc_end):
    ws = start_ts - pd.Timedelta(days=start_ts.weekday())
    while ws <= end_ts:
        we = ws + pd.Timedelta(days=6)
        wm = ws + pd.Timedelta(days=3)

        if we >= start_ts and ws <= end_ts:
            if ws >= start_ts and (inc_start or ws != start_ts - pd.Timedelta(days=start_ts.weekday())):
                tick_vals.append(ws.strftime('%Y-%m-%d'))
            if start_ts <= wm <= end_ts:
                iso_year, iso_week, _ = wm.isocalendar()
                annotations.append(_make_label_annotation(wm, formatter(iso_year, iso_week),
                                                          y_pos, font_size, font_family))
            if we <= end_ts and (inc_end or ws + pd.Timedelta(days=7) > end_ts):
                tick_vals.append(we.strftime('%Y-%m-%d'))

        ws += pd.Timedelta(days=7)
