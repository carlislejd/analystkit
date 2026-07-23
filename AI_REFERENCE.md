# AnalystKit — AI Reference

Everything is accessed via `import analystkit as ak`.

For production chart-building patterns, deck-ready script contracts, and
examples derived from real Bitwise chart usage, see `CHART_RECIPES.md`.
For ad hoc Bitwise reports, see `REPORT_RECIPES.md`.

## Core Concept

**`apply_theme()` is the engine.** It can brand ANY Plotly figure — bar,
line, scatter, heatmap, 3D surface, anything. Build your figure however
you like with Plotly, then call `ak.apply_theme(fig)` and it handles
colors, fonts, grid, legend, and automatic font scaling.

`create_chart()` is a thin convenience wrapper for common chart types.
Use it when your data is a simple DataFrame/dict/list. Use `apply_theme()`
directly when you need full control over the Plotly figure.

For composite deck and quarterly report charts, generated chart images should
not embed slide titles, sources, or footers. Keep those in the slide layer and
use the figure for data, axes, tick labels, legends, annotations, insets, and
automation metadata.

---

## Theme & Styling

### `ak.apply_theme()`

```python
apply_theme(
    fig,                          # Any go.Figure
    size_preset: str = 'full',    # 'full', 'half', '18:9', '3:1', '1:1', '16:9', '4:3', 'type_a'…'type_f'
    margin_preset: str = 'minimal',  # 'minimal', 'standard', 'wide'
    width: int = None,            # Explicit width (overrides preset)
    height: int = None,           # Explicit height (overrides preset)
    auto_colors: bool = True,     # Apply Bitwise palette automatically
) -> go.Figure
```

**Font sizes scale automatically** based on dimensions. A 825px chart
gets proportionally smaller text than a 1800px chart. No manual sizing
needed.

### `ak.get_color_palette(n_colors)`

```python
get_color_palette(n_colors) -> List[str]
```

Returns N brand colors from the curated hierarchy (1–11) or cycles the
full palette for >11 colors.

### `ak.compute_font_sizes(width, height)`

```python
compute_font_sizes(width, height) -> Dict[str, int]
```

Returns `{'title': N, 'axis': N, 'legend': N, 'annotation': N}` scaled
for the given dimensions. Useful when adding custom annotations.

---

## Chart Creation

### `ak.create_chart()`

```python
create_chart(
    data,                         # DataFrame, list, or dict
    chart_type: str = "bar",      # See supported types below
    x: str = None,
    y: str = None,
    x_label: str = "",
    y_label: str = "",
    color_column: str = None,
    size_preset: str = "full",
    margin_preset: str = "minimal",
    width: int = None,
    height: int = None,
    scatter_legend: bool = True,
    **kwargs                      # Passed to Plotly Express
) -> go.Figure
```

**Supported chart types:** `bar`, `line`, `scatter`, `area`, `pie`,
`histogram`, `box`, `violin`, `funnel`, `treemap`, `sunburst`.

For anything else (heatmap, 3D, candlestick, etc.), build with Plotly
and call `ak.apply_theme(fig)`.

**Data formats:**
- DataFrame → requires `x` and `y` column names
- Dict → keys become x, values become y
- List → y-values (auto-indexed) or list of `[x, y]` pairs

### `ak.create_bar_chart()` / `ak.create_line_chart()`

Backward-compatible aliases for `create_chart(chart_type="bar"|"line")`.

---

## Export

### `ak.export_chart()`

```python
export_chart(
    fig,
    filename: str,
    format: str = "svg",          # svg, png, jpg, jpeg, pdf, webp, eps, html, json
    width: int = None,
    height: int = None,
    scale: int = 2
) -> str                          # Returns the file path written
```

Static formats (svg, png, jpg, pdf, webp, eps) require **kaleido**.
HTML and JSON export work without extra dependencies.

### `ak.save_chart()`

```python
save_chart(
    fig,
    title: str,
    output_dir: str = "design",
    aspect_ratio: str = "18:9",   # Any SIZE_PRESETS key
    formats: List[str] = None,    # e.g. ['svg', 'png', 'html']
    include_svg: bool = True,     # Legacy — ignored when formats given
    include_png: bool = True,     # Legacy — ignored when formats given
    include_1x1: bool = False,
    png_scale: int = 2
) -> Dict[str, str]
```

---

## Report Building

AnalystKit also includes the house style for ad hoc Bitwise reports: polished
HTML/PDF reports with a dark cover, compact KPI cards, report-native SVG
charts, tables, panels, and visual-QA helpers.

### Core Classes

```python
ReportDocument(title, pages, report_date=None, css_overrides="")
ReportPage(title, content="", kicker="", intro="", cover=False, subtitle="", eyebrow="", meta=[], note="", page_number=None, footer_label="", extra_class="")
ReportMetaItem(label, value)
ReportMetric(label, value, note="", tone="default")
```

### Component Helpers

```python
metric_grid(metrics) -> str
panel(title, body, trusted_html=False, class_name="") -> str
bullet_list(items) -> str
html_table(rows, columns=None, numeric_columns=()) -> str
chart_panel(svg_or_html, compact=False, tall=False, class_name="") -> str
image_panel(path, alt="", height="3.6in") -> str
line_chart_svg(rows, x, y, title, width=760, height=280, color=REPORT_COLORS["teal"]) -> str
horizontal_bar_svg(rows, label, value, title, width=760, height=300, limit=10, colors=None) -> str
```

### Export / QA Helpers

```python
ReportDocument.save_html(path) -> Path
ReportDocument.export_pdf(path, html_path=None) -> Path
export_report_pdf(html_path, pdf_path) -> Path
render_pdf_pages(pdf_path, output_prefix, pdftoppm="pdftoppm", resolution=130) -> list[Path]
make_contact_sheet(pages, output_path, thumb_size=(260, 340), columns=3) -> Path
report_css() -> str
```

PDF export requires Playwright. Contact-sheet generation requires Pillow.

---

## Tick Marks

### `ak.apply_range_tick_marks()`

```python
apply_range_tick_marks(
    fig,
    start_date, end_date,
    period: str = "quarter",      # "quarter", "year", "month", "week"
    label_formatter = None,       # fn(year, period_num) -> str
    ticklen: int = 10,
    label_y_position: float = -0.01,
    include_start_boundary: bool = True,
    include_end_boundary: bool = True,
    **kwargs
) -> go.Figure
```

Tick marks at period boundaries, labels at midpoints. Label font sizes
auto-scale with the chart dimensions.

---

## Constants

### Colors

```python
ak.BITWISE_COLORS     # 11-color palette
ak.COLOR_HIERARCHY[3]  # ['#45b979', '#006472', '#6c6b71']

ak.CHART_COLORS['text']        # '#1B252A'
ak.CHART_COLORS['grid']        # '#e6e6e6'
ak.CHART_COLORS['grid_dark']   # '#C1C8CD'
ak.CHART_COLORS['background']  # '#ffffff'
```

### Fonts

```python
ak.FONT_FAMILIES['primary']  # 'PPNeueMontreal-Book'
ak.FONT_FAMILIES['axis']     # 'PPNeueMontrealMono-Variable'
ak.FONT_FAMILIES['title']    # 'Items-Regular'
```

### Size Presets

```python
ak.SIZE_PRESETS['full']    # {'width': 1200, 'height': 800}
ak.SIZE_PRESETS['18:9']    # {'width': 1728, 'height': 864}
ak.SIZE_PRESETS['16:9']    # {'width': 1920, 'height': 1080}
ak.SIZE_PRESETS['4:3']     # {'width': 1200, 'height': 900}
ak.SIZE_PRESETS['1:1']     # {'width': 1152, 'height': 1152}
ak.SIZE_PRESETS['type_a']  # {'width': 1275, 'height': 900}
# ... type_b through type_f
```

### Design Rules

1. Chart titles and source notes omitted by default for deck-bound charts
2. Axis titles hidden by default — shown only with explicit `x_label`/`y_label`
   for standalone charts
3. Y-axis: horizontal gridlines. X-axis: no gridlines.
4. Colors auto-applied from brand hierarchy based on series count
5. PPNeueMontreal-Book for body text, Items-Regular for standalone titles only
6. PPNeueMontrealMono-Variable for axis tick labels when numeric readability
   matters
7. Legend: no border, transparent background; use dummy marker traces for
   circular dot legends on line/area charts
8. Font sizes scale proportionally with chart dimensions (no manual sizing)
9. Deck automation metadata belongs in `fig.layout.meta`, not rendered text
