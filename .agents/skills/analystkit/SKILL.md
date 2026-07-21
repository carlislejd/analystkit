---
name: analystkit
description: "Create professional, Bitwise-branded Plotly charts from data. Use this skill whenever the user wants to make a chart, graph, plot, visualization, or data graphic — whether from a CSV, DataFrame, JSON, API response, or inline data. Also use when the user mentions analystkit, asks for branded charts, or wants to export charts in any format (PNG, SVG, PDF, HTML, etc.). Covers bar charts, line charts, scatter plots, area charts, pie charts, histograms, box plots, heatmaps, and any other Plotly chart type."
---

# AnalystKit — Chart Creation Skill

You have access to the **analystkit** Python library, which applies Bitwise
brand styling to Plotly charts. It handles colors, fonts, grid styling,
legend formatting, and — importantly — automatic font scaling so text
looks right at every chart size.

When you are working from the AnalystKit repository, read `CHART_RECIPES.md`
for the production recipe guide and `AI_REFERENCE.md` for exact signatures.
The real-world default is custom Plotly first, `ak.apply_theme()` second,
then range ticks / final axis overrides, then `ak.save_chart()` or
`ak.export_chart()`.

## Current Deck Style

For composite deck and quarterly report charts, the chart image should be
mostly the chart itself. The slide owns the title, source, and footer.

- Do not embed chart titles, source notes, source prefixes, or as-of footers in
  generated deck chart images.
- Keep x/y axis titles hidden unless the chart will be used standalone and the
  units are otherwise unclear.
- Prefer custom Plotly graph objects plus `ak.apply_theme()` for financial
  charts with manual ticks, range-bound dates, insets, or deck metadata.
- Use explicit `tickmode="array"` with deliberate `tickvals` and `ticktext`
  for dollars, trillions, billions, percentages, and bounded metrics.
- Use `ak.apply_range_tick_marks()` for continuous date axes spanning months,
  quarters, or years.
- Use dummy marker-only `go.Scatter(x=[None], y=[None], mode="markers", ...)`
  traces for clean circular legend dots on line and area charts.
- Put actual date coverage, table values, and overlay-image data in
  `fig.layout.meta` for downstream deck automation.

## Setup

```python
import analystkit as ak
import plotly.graph_objects as go
import pandas as pd
```

The library is installed from the user's local analystkit package. If it's
not importable, install from the repo:

```bash
pip install -e /path/to/analystkit
```

Static image export (PNG, SVG, PDF, etc.) requires kaleido:

```bash
pip install kaleido
```

## How to Create Charts

### The Two Approaches

**Approach 1 — `create_chart()` for common types:**

Good for bar, line, scatter, area, pie, histogram, box, violin, funnel,
treemap, sunburst. Handles data coercion and calls `apply_theme()` for you.

```python
fig = ak.create_chart(
    data=df,
    chart_type="bar",
    x="category",
    y="value",
    color_column="group",   # optional grouping
    size_preset="18:9",     # or width=1200, height=600
)
```

**Approach 2 — build with Plotly, then `apply_theme()`:**

Use this for anything `create_chart` doesn't cover (heatmaps, 3D, 
candlestick, waterfall, sankey, choropleth, etc.) or when you need 
full control over trace configuration.

```python
fig = go.Figure(data=go.Heatmap(z=matrix, x=cols, y=rows))
fig = ak.apply_theme(fig, size_preset="1:1")
```

### Key Parameters for Sizing

You can set dimensions two ways — by preset or explicit pixels:

```python
# Preset (recommended for standard deliverables):
fig = ak.apply_theme(fig, size_preset="18:9")

# Explicit (for custom sizes):
fig = ak.apply_theme(fig, width=900, height=500)
```

Available presets: `full` (1200×800), `half` (600×400), `18:9` (1728×864),
`3:1` (1728×576), `1:1` (1152×1152), `16:9` (1920×1080), `4:3` (1200×900),
`type_a` through `type_f`.

**Font sizes auto-scale** with chart dimensions. You never need to manually
set font sizes — the library computes them proportionally.

### Labels, Titles, and Sources

Axis titles are hidden by default (the Bitwise design standard). Add them only
when the chart is standalone and the data needs context:

```python
fig = ak.create_chart(df, "bar", x="month", y="revenue",
                       x_label="", y_label="Revenue ($M)")
```

For deck charts, do not set a title:

```python
fig.update_layout(title=None)
fig.update_xaxes(title=None)
fig.update_yaxes(title=None)
```

For a truly standalone chart, use Plotly's native `update_layout`:

```python
fig.update_layout(title="Monthly Revenue by Region")
```

### Custom Annotations

When adding annotations manually, use `compute_font_sizes()` to get
sizes that match the chart's scale:

```python
fonts = ak.compute_font_sizes(1200, 800)
fig.add_annotation(text="Peak", font_size=fonts['annotation'], ...)
```

## Exporting Charts

### Single File Export

```python
# Static images (require kaleido):
ak.export_chart(fig, "output/chart", format="png")   # retina by default
ak.export_chart(fig, "output/chart", format="svg")
ak.export_chart(fig, "output/chart", format="pdf")
ak.export_chart(fig, "output/chart", format="webp")

# Interactive (no kaleido needed):
ak.export_chart(fig, "output/chart", format="html")
ak.export_chart(fig, "output/chart", format="json")
```

Supported formats: `svg`, `png`, `jpg`, `jpeg`, `pdf`, `webp`, `eps`, `html`, `json`.

### Batch Export (Multiple Formats + Aspect Ratios)

```python
files = ak.save_chart(
    fig, "Revenue Chart",
    output_dir="design",
    aspect_ratio="18:9",
    formats=["svg", "png", "html"],   # any combination
    include_1x1=True,                  # also export square versions
)
```

### Export Tips

- Default `scale=2` produces retina-quality PNGs (2× resolution).
- HTML exports include Plotly.js via CDN — great for sharing interactive charts.
- For presentations, use `aspect_ratio="16:9"` or `"4:3"`.

## Color Palette

The Bitwise palette is applied automatically. To access colors directly:

```python
colors = ak.get_color_palette(3)  # ['#45b979', '#006472', '#6c6b71']
ak.BITWISE_COLORS                 # Full 11-color list
ak.CHART_COLORS['text']           # '#1B252A'
```

The palette hierarchy is curated for 1–11 series. The library picks the
optimal subset based on how many data series you have.

## Time-Series Tick Marks

For quarterly/yearly charts, use range tick marks — ticks at period
boundaries, labels centered in each period:

```python
fig = ak.apply_range_tick_marks(
    fig,
    start_date="2023-01-01",
    end_date="2025-12-31",
    period="quarter",  # or "year", "month", "week"
    tickcolor=ak.CHART_COLORS["grid_dark"],
    label_font_family=ak.FONT_FAMILIES["primary"],
)
```

Apply the theme before range tick marks, then apply final axis and margin
overrides.

### Circular Legend Dots

For line and area charts, hide the visible traces from the legend and add
marker-only legend traces:

```python
fig.add_trace(
    go.Scatter(
        x=[None],
        y=[None],
        mode="markers",
        marker=dict(size=10, color=color, symbol="circle", line=dict(width=0)),
        showlegend=True,
        name=label,
        hoverinfo="skip",
    )
)
```

## Workflow Summary

1. Load/prepare data (DataFrame, dict, list, CSV, etc.)
2. Create figure via `create_chart()` or build with Plotly + `apply_theme()`
3. Add range ticks, manual tick labels, circular legend markers, or annotations
   as needed
4. Export with `export_chart()` or `save_chart()`
5. Present the file to the user

Always save exported files to the workspace output directory so the user
can access them.

## Deck-Ready Scripts

For charts that will be refreshed into decks, expose:

```python
def build_figure(start_date=None, end_date=None):
    ...
    return fig
```

Keep file export in `save_outputs()` or `main()`, not at import time. Put
downstream facts such as `actual_end_date`, `actual_start_date`,
`aum_actual_end_date`, `table_values`, or overlay image instructions in
`fig.layout.meta`.
