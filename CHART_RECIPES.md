# AnalystKit Chart Recipes for Agents

This guide is the practical companion to `AI_REFERENCE.md`. It is based on
observed production usage in Bitwise chart generator scripts and the current
composite deck quarterly report chart scripts. The main lesson is simple:
AnalystKit is usually the styling and export layer around a custom Plotly
figure.

## What the Real Charts Do

Across the reviewed examples, the common production pattern is:

- Build custom `plotly.graph_objects` figures for control.
- Call `ak.apply_theme(..., margin_preset="minimal")`.
- Add final axis ranges, unit-specific tick labels, range ticks, annotations,
  and custom legend markers.
- Keep generated chart images visually clean: do not embed slide titles,
  source notes, or axis titles in the chart unless the chart will live outside
  a deck.
- Export with `ak.save_chart()` for one-off charts or `ak.export_chart()` /
  `fig.write_image()` inside deck refresh automation.
- For deck refreshes, expose `build_figure(start_date=None, end_date=None)`.

The scan covered 142 AnalystKit-using chart generator files and 41
AnalystKit-using composite deck files. In those examples, custom Plotly plus
`apply_theme()` was much more common than the convenience `create_chart()`
path.

## Mental Model

`ak.apply_theme()` is the engine. It can brand any Plotly figure with Bitwise
colors, fonts, grid styling, legend defaults, and automatic font scaling.

Use `ak.create_chart()` only when the chart is simple and maps cleanly to
Plotly Express. If you are building a financial chart with custom ticks,
stacked areas, annotations, endpoint callouts, matrix cells, insets, semantic
colors, or deck metadata, build with Plotly graph objects and then apply the
theme.

## Current Composite Deck Style

The current quarterly report and composite deck charts are designed as slide
assets, not standalone research-page charts. Let the slide own the title,
subtitle, source, and date footer. The chart image should mostly be data,
axes, labels, legends, and any necessary inset/table overlays.

Default rules for deck-bound charts:

- Do not set chart titles, slide titles, source footers, or source prefixes in
  the generated figure.
- Do not use `xaxis_title`, `yaxis_title`, or non-empty axis title text.
- Use explicit `tickmode="array"` with deliberate `tickvals` and `ticktext`
  for finance units, percentages, bounded metrics, and any range that needs
  stable slide-to-slide comparison.
- Use `ak.apply_range_tick_marks()` for continuous date axes that span months,
  quarters, or years. Apply the theme first, then range ticks, then final axis
  and margin overrides.
- Use dummy `go.Scatter(x=[None], y=[None], mode="markers", ...)` traces for
  circular legend dots when the visible traces are lines or filled areas.
- Use `showlegend=False` for single-series charts and charts whose slide/table
  already names the series.
- Set margins per chart after the theme. Common wide-chart margins are compact
  top/right with extra bottom for range tick labels, for example
  `margin=dict(l=58, r=20, t=20, b=74)`.
- Put automation facts such as actual date coverage, table values, and overlay
  image metadata in `fig.layout.meta`; do not render them as chart furniture.

## Basic Setup

```python
import analystkit as ak
import pandas as pd
import plotly.graph_objects as go
```

If the package is not installed:

```bash
pip install -e /path/to/analystkit
```

For static exports:

```bash
pip install kaleido
```

## Decision Tree

Use `ak.create_chart()` when:

- The chart is a simple bar, line, scatter, area, pie, histogram, box, violin,
  funnel, treemap, or sunburst.
- You do not need custom traces, mixed chart types, custom legends, or deck
  metadata.

Use Plotly plus `ak.apply_theme()` when:

- The chart has multiple trace types.
- You need a stacked area, monthly flow bars, correlation line, matrix,
  heatmap, table, candlestick, inset metric box, or custom annotation.
- You need semantic colors, manual tick labels, or a specific y-axis range.
- The script will be called by a deck refresh system.

## Deck-Native Layout Pattern

Use this order for the newer chart style:

```python
fig = go.Figure()
fig.add_trace(...)

fig = ak.apply_theme(fig, size_preset="3:1", margin_preset="minimal", auto_colors=False)

fig = ak.apply_range_tick_marks(
    fig,
    start_date=df["date_string"].min(),
    end_date=df["date_string"].max(),
    period="year",
    ticklen=10,
    label_y_position=-0.01,
    include_end_boundary=False,
    tickcolor=ak.CHART_COLORS["grid_dark"],
    label_font_family=ak.FONT_FAMILIES["primary"],
)

fig.update_layout(
    title=None,
    showlegend=False,
    margin=dict(l=58, r=20, t=20, b=74),
    meta={
        "actual_start_date": df["date_string"].min(),
        "actual_end_date": df["date_string"].max(),
    },
)
fig.update_xaxes(title=None)
fig.update_yaxes(
    title=None,
    tickmode="array",
    tickvals=[0, 1, 2, 3, 4],
    ticktext=["$0 ", "$1T ", "$2T ", "$3T ", "$4T "],
)
```

If you need to remove partial period labels after range ticks, filter
`fig.layout.annotations` after `apply_range_tick_marks()` and before export.

## Size and Export Defaults

Common presets from production usage:

| Preset | Best for |
| --- | --- |
| `3:1` | Wide deck charts, time series, correlations, stacked areas |
| `18:9` | Standard landscape chart exports |
| `type_a` | Common Bitwise slide chart shape |
| `type_e` | Tall/sidebar-style charts |
| `1:1` | Matrices, square heatmaps, social crops |

Prefer this shape:

```python
fig = ak.apply_theme(fig, size_preset="3:1", margin_preset="minimal")

saved = ak.save_chart(
    fig,
    "Chart Name",
    output_dir="design",
    aspect_ratio="3:1",
    include_svg=True,
    include_png=True,
    png_scale=2,
)
```

Use `png_scale=4` when the chart will be heavily cropped, resized, or used in a
high-resolution presentation workflow.

## Data Prep Recipe

Before plotting:

```python
df = df.copy()
df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None).dt.normalize()
df["value"] = pd.to_numeric(df["value"], errors="coerce")
df = df.dropna(subset=["date", "value"]).sort_values("date").reset_index(drop=True)
```

Then choose the display unit before plotting:

```python
df["value_billions"] = df["value"] / 1_000_000_000
df["date_string"] = df["date"].dt.strftime("%Y-%m-%d")
```

Use ISO date strings for continuous time-series axes. Use category labels such
as `Jan '26` only when the chart is truly discrete, such as monthly bars.

## Recipe: Time-Series Line or Correlation Chart

```python
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=df["date_string"],
        y=df["correlation"],
        mode="lines",
        name="90-Day Correlation",
        line=dict(width=2),
        hovertemplate="%{x}<br>%{y:.2f}<extra></extra>",
    )
)

fig = ak.apply_theme(fig, size_preset="3:1", margin_preset="minimal")

fig = ak.apply_range_tick_marks(
    fig,
    start_date=df["date_string"].min(),
    end_date=df["date_string"].max(),
    period="year",
    include_end_boundary=False,
    tickcolor=ak.CHART_COLORS["grid_dark"],
)

fig.update_layout(
    yaxis=dict(
        range=[-1, 1],
        tickmode="array",
        tickvals=[-1, -0.5, 0, 0.5, 1],
        ticktext=["-1.0", "-0.5", "0.0", "0.5", "1.0"],
        showgrid=True,
    ),
    margin=dict(b=70, l=40, r=40, t=60),
)
```

Notes:

- Apply the theme before range tick marks so chart dimensions and font scaling
  are available.
- Set y-axis ranges deliberately for bounded metrics such as correlations.
- Add endpoint annotations only after the theme is applied.
- Leave `title=None`, and keep source/date text in the slide layer for deck
  refresh charts.

## Recipe: Monthly Net Flow Bar Chart

```python
monthly["month_label"] = monthly["date"].dt.strftime("%b '%y")
monthly["flows_billions"] = monthly["flows_usd"] / 1_000_000_000
bar_colors = [
    ak.BITWISE_COLORS[0] if value >= 0 else "#e15759"
    for value in monthly["flows_billions"]
]

fig = go.Figure()
fig.add_trace(
    go.Bar(
        x=monthly["month_label"],
        y=monthly["flows_billions"],
        marker=dict(color=bar_colors, line=dict(width=0), opacity=0.92),
        showlegend=False,
        hovertemplate="<b>%{x}</b><br>$%{y:.2f}B<extra></extra>",
    )
)

fig = ak.apply_theme(fig, size_preset="3:1", margin_preset="minimal", auto_colors=False)
fig.update_layout(
    bargap=0.26,
    xaxis=dict(type="category", tickangle=90, showgrid=False),
    yaxis=dict(
        title=None,
        tickmode="array",
        tickvals=[-6, -4, -2, 0, 2, 4, 6, 8],
        ticktext=["($6B)", "($4B)", "($2B)", "$0", "$2B", "$4B", "$6B", "$8B"],
        range=[-6.1, 8.5],
        showgrid=True,
    ),
    margin=dict(l=82, r=22, t=88, b=72),
)
```

Notes:

- Use semantic positive/negative colors for flow charts.
- Use category x-axis labels when every bar is a discrete month.
- Format negative dollar labels with parentheses when that is the intended
  finance style.

## Recipe: Stacked Area Chart

```python
series = [
    ("bitcoin_trillions", "Bitcoin"),
    ("ethereum_trillions", "Ethereum"),
    ("others_trillions", "Others"),
]
colors = ak.get_color_palette(len(series))

fig = go.Figure()
for i, (column, label) in enumerate(series):
    fig.add_trace(
        go.Scatter(
            x=df["date_string"],
            y=df[column],
            mode="lines",
            fill="tonexty",
            stackgroup="one",
            line=dict(width=0.5, color=colors[i]),
            fillcolor=colors[i],
            name=label,
            showlegend=False,
            hovertemplate=f"<b>{label}</b><br>%{{y:.2f}}T<extra></extra>",
        )
    )

fig = ak.apply_theme(fig, size_preset="3:1", margin_preset="minimal", auto_colors=False)

for i, (_, label) in enumerate(series):
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            marker=dict(size=10, color=colors[i]),
            showlegend=True,
            name=label,
            hoverinfo="skip",
        )
    )

fig.update_layout(
    yaxis=dict(
        tickmode="array",
        tickvals=[0, 1, 2, 3, 4],
        ticktext=["$0", "$1T", "$2T", "$3T", "$4T"],
    ),
    legend=dict(traceorder="reversed"),
)
```

Notes:

- For stacked areas, manually assign colors and disable auto-colors.
- Add dummy scatter traces for clean circular legend markers.
- Reverse legend order when the visual stack reads top-to-bottom.
- If the legend sits outside the plot, reserve right margin explicitly, for
  example `margin=dict(b=80, t=60, r=220)`.

## Recipe: Circular Dot Legends for Lines and Areas

Plotly line traces produce line-style legend swatches. The newer deck charts
usually prefer small circular legend dots. Hide the visible traces from the
legend and add invisible marker-only traces:

```python
for name, color, final_value in legend_items:
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            marker=dict(size=10, color=color, symbol="circle", line=dict(width=0)),
            showlegend=True,
            name=f"{name} {final_value:+.0f}%",
            hoverinfo="skip",
        )
    )

fig.update_layout(
    showlegend=True,
    legend=dict(
        orientation="v",
        yanchor="top",
        y=1,
        xanchor="left",
        x=1.02,
        tracegroupgap=0,
    ),
    margin=dict(b=80, t=60, r=220),
)
```

Sort legend items by the final displayed metric when that makes the chart
easier to scan, such as constituent performance charts ranked by final return.

## Recipe: Inset Metrics and Overlay Tables

Use insets sparingly when the chart needs deck-visible summary figures such as
ETF net flows or AUM. Draw them as paper-referenced shapes and annotations so
they stay fixed in the exported image:

```python
fig.add_shape(
    type="rect",
    xref="paper",
    yref="paper",
    x0=0.68,
    x1=0.815,
    y0=0.72,
    y1=1.08,
    line=dict(color="#d2d2d2", width=1),
    fillcolor="white",
    layer="above",
)
fig.add_annotation(
    x=0.7475,
    y=1.005,
    xref="paper",
    yref="paper",
    text="Net Flows<br>Since Launch<br>(USD Billions)",
    showarrow=False,
    align="center",
    font=dict(family=ak.FONT_FAMILIES["primary"], size=16, color="#4f5357"),
)
fig.add_annotation(
    x=0.7475,
    y=0.79,
    xref="paper",
    yref="paper",
    text="<b>$42.0B</b>",
    showarrow=False,
    align="center",
    font=dict(family=ak.FONT_FAMILIES["primary"], size=32, color="#171717"),
)
```

For larger tables, create a separate transparent or white-background Plotly
figure with hidden axes, fixed dimensions, zero margins, and shape/annotation
cells. Return table inputs through `fig.layout.meta`, and expose a
`save_overlay_images(fig, *, output_dir, output_basename, png_scale=1)` helper
when the deck refresh needs to place that table as a separate image.

## Recipe: Matrix, Heatmap, or Custom Shape Chart

Use a blank `go.Figure`, apply the theme, then draw shapes and annotations.

```python
fig = go.Figure()
fig.add_trace(go.Scatter(x=[None], y=[None], mode="markers", showlegend=False))
fig = ak.apply_theme(fig, size_preset="1:1", margin_preset="minimal", auto_colors=False)

fonts = ak.compute_font_sizes(fig.layout.width, fig.layout.height)

for row in cells:
    fig.add_shape(
        type="rect",
        x0=row["x0"],
        x1=row["x1"],
        y0=row["y0"],
        y1=row["y1"],
        line=dict(color="#d4d6dd", width=0.7),
        fillcolor=row["fill"],
    )
    fig.add_annotation(
        x=row["x"],
        y=row["y"],
        text=row["label"],
        showarrow=False,
        font=dict(
            family=ak.FONT_FAMILIES["axis"],
            size=fonts["annotation"],
            color=ak.CHART_COLORS["text"],
        ),
    )

fig.update_layout(
    xaxis=dict(visible=False, fixedrange=True),
    yaxis=dict(visible=False, fixedrange=True),
)
```

Notes:

- Use `auto_colors=False` when the shape colors encode meaning.
- Compute annotation font sizes from final chart dimensions.
- Hide axes when the chart is a custom canvas.

## Recipe: Deck-Ready Chart Script

Deck automation works best when the chart source is importable and has no
write side effects during import.

```python
import analystkit as ak
import pandas as pd
import plotly.graph_objects as go

CHART_TITLE = "Example Deck Chart"
CHART_START_DATE = "2024-01-01"
CHART_END_DATE = "2026-06-30"


def fetch_data(start_date: str, end_date: str) -> pd.DataFrame:
    ...


def create_chart(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(...)
    fig = ak.apply_theme(fig, size_preset="3:1", margin_preset="minimal")
    fig.update_layout(meta={"actual_end_date": df["date"].max().date().isoformat()})
    return fig


def build_figure(start_date=None, end_date=None):
    resolved_start = start_date or CHART_START_DATE
    resolved_end = end_date or CHART_END_DATE
    df = fetch_data(resolved_start, resolved_end)
    return create_chart(df)


def save_outputs(fig):
    return ak.save_chart(
        fig,
        CHART_TITLE,
        output_dir="design",
        aspect_ratio="3:1",
        include_svg=True,
        include_png=True,
        png_scale=2,
    )


def main():
    fig = build_figure()
    save_outputs(fig)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Composite deck config typically points at the source script and records:

- `generator`: usually `script_build_figure`
- `source_script`: path to the script
- `output_basename`: stable output filename stem
- `aspect_ratio`: export preset such as `3:1`
- `png_scale`: usually `1` or `2`
- `date_mode`: how to resolve start/end dates
- `targets`: slide/image object IDs for replacement
- `text_updates`: regex replacements for source footers or as-of dates in the
  slide, not in the generated chart image

## Common Footguns

- Do not manually set font sizes unless the chart uses custom annotations or
  shape labels. Use `ak.compute_font_sizes()` for those.
- Do not use `create_chart()` for complex finance charts just because it can
  make a line or bar chart.
- Do not embed slide titles, source notes, source prefixes, or as-of footers in
  deck chart images. Keep those in the presentation layer.
- Do not rely on local current dates inside deck scripts. Accept `start_date`
  and `end_date` and put actual data coverage in `fig.layout.meta`.
- Do not apply the theme after manually setting final semantic colors unless
  `auto_colors=False` is used.
- Do not export static images without Kaleido and, in server environments,
  a Chrome path available to Kaleido.
- Do not hard-code private absolute paths in reusable chart scripts.

## Final Agent Checklist

Before handing back a chart:

- Data is sorted and numeric columns are coerced.
- Units are visible in tick labels or annotations.
- Chart titles, source notes, and axis titles are absent for deck assets unless
  there is a specific standalone-chart requirement.
- `ak.apply_theme()` has been called.
- Date axes use range tick marks when the chart spans quarters or years.
- Legends use circular marker traces when line/area swatches are visually noisy.
- Exported files are saved in a predictable output directory.
- PNG/SVG dimensions match the intended aspect ratio.
- Any deck chart exposes `build_figure(start_date=None, end_date=None)`.
- Any source/date facts needed downstream are in `fig.layout.meta`.
