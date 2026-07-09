# AnalystKit Agent Instructions

AnalystKit is the Bitwise chart styling and export kit for Plotly. Treat it as
an agent-facing chart production toolkit, not just a Python theme package.

## Start Here

1. Read `CHART_RECIPES.md` for the production workflow and examples.
2. Read `AI_REFERENCE.md` for exact function signatures and constants.
3. Import the package as `import analystkit as ak`.
4. For most real charts, build a normal Plotly `go.Figure`, then call
   `ak.apply_theme(fig, size_preset=..., margin_preset="minimal")`.
5. Use `ak.create_chart()` only for simple bar, line, scatter, area, pie,
   histogram, box, violin, funnel, treemap, or sunburst charts.

## Default Chart Workflow

1. Load and normalize data into a tidy pandas DataFrame.
2. Build the figure with Plotly graph objects when you need control.
3. Apply AnalystKit theme before final axis, annotation, or export tweaks.
4. Use `ak.apply_range_tick_marks()` for date ranges with quarterly, yearly,
   monthly, or weekly boundary ticks.
5. Export with `ak.save_chart()` for common deliverables or `ak.export_chart()`
   for one explicit file.

## Production Defaults

- Prefer `margin_preset="minimal"`.
- Prefer `size_preset="3:1"` for wide deck charts and time series.
- Use `size_preset="18:9"` for standard landscape charts.
- Use `size_preset="type_a"` when matching the common Bitwise slide chart shape.
- Use `size_preset="1:1"` for matrices, square heatmaps, and social crops.
- Hide axis titles unless the unit or context is otherwise unclear.
- Let AnalystKit assign colors unless the chart has semantic colors.
- When using custom colors, pull from `ak.get_color_palette()` or
  `ak.BITWISE_COLORS`.
- Static PNG, SVG, PDF, WEBP, JPG, and EPS export requires Kaleido.

## Deck-Compatible Scripts

When creating a chart script meant for a deck refresh system, expose this
contract:

```python
def build_figure(start_date=None, end_date=None):
    ...
    return fig
```

Keep file writing in a separate `save_outputs()` or `main()` function. Put
machine-readable facts such as `actual_end_date`, `actual_start_date`,
`table_values`, or `overlay_images` in `fig.layout.meta` when downstream deck
automation needs them.

## Quality Bar

- Use explicit date parsing, numeric coercion, sorting, and unit conversion.
- Set tick labels deliberately for dollars, billions, trillions, and percents.
- Verify exported image dimensions and inspect the image when layout matters.
- Save outputs into a predictable directory such as `design/`, `outputs/png/`,
  or the caller-provided output folder.
- Do not commit API keys, private datasets, generated credentials, or local
  output folders unless explicitly requested.
