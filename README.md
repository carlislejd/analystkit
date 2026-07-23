# AnalystKit

Bitwise brand theme, chart utilities, and ad hoc report-building materials.
Applies brand colors, fonts, grid styling, and automatic font scaling to any
Plotly figure, and provides a canonical HTML/PDF report shell for polished
Bitwise research and client-request readouts.

## For AI Assistants

Start with [`AGENTS.md`](AGENTS.md) for agent instructions, then use
[`CHART_RECIPES.md`](CHART_RECIPES.md) for production chart patterns and
[`REPORT_RECIPES.md`](REPORT_RECIPES.md) for ad hoc report patterns. Use
[`AI_REFERENCE.md`](AI_REFERENCE.md) for the complete API reference.

## Quick Start

```python
import analystkit as ak
import pandas as pd

data = pd.DataFrame({'category': ['A', 'B', 'C'], 'value': [10, 20, 30]})

# Convenience wrapper (bar, line, scatter, area, pie, histogram, etc.)
fig = ak.create_chart(data, chart_type='bar', x='category', y='value')
fig.show()

# Or: build any Plotly figure and brand it
import plotly.graph_objects as go
fig = go.Figure(data=go.Heatmap(z=[[1,2],[3,4]]))
fig = ak.apply_theme(fig, size_preset='1:1')
```

## Installation

```bash
pip install git+https://github.com/carlislejd/analystkit.git

# Static image export (PNG, SVG, PDF, etc.) requires kaleido:
pip install kaleido
```

## API Surface

### Core Theme
- `apply_theme(fig)` — brand any Plotly figure (the main entry point)
- `get_color_palette(n)` — get N colors from the brand palette
- `compute_font_sizes(w, h)` — get auto-scaled font sizes for given dimensions

### Chart Creation
- `create_chart()` — convenience wrapper supporting bar, line, scatter, area, pie, histogram, box, violin, funnel, treemap, sunburst
- `create_bar_chart()` / `create_line_chart()` — backward-compatible aliases

### Export
- `export_chart()` — export to svg, png, jpg, pdf, webp, eps, html, or json
- `save_chart()` — batch export in multiple formats with predefined aspect ratios

### Time-Series
- `apply_range_tick_marks()` — boundary ticks with midpoint labels for quarter/year/month/week periods

### Reports
- `ReportDocument`, `ReportPage`, `ReportMetric`, `ReportMetaItem` — canonical Bitwise report shell
- `metric_grid()`, `panel()`, `html_table()`, `chart_panel()` — common report components
- `line_chart_svg()`, `horizontal_bar_svg()` — compact report-native SVG charts
- `export_report_pdf()`, `render_pdf_pages()`, `make_contact_sheet()` — HTML-to-PDF and QA helpers

### Constants
- `BITWISE_COLORS`, `COLOR_HIERARCHY`, `CHART_COLORS`
- `FONT_FAMILIES`, `FONT_SIZES`, `SIZE_PRESETS`, `MARGIN_PRESETS`

## Key Design Principles

1. **Font sizes auto-scale** — text adjusts proportionally to chart dimensions
2. **Deck charts stay chart-focused** — slide titles, sources, and footers live
   in the presentation layer
3. **Axis titles hidden by default** — shown only when explicitly provided for
   standalone charts
4. **Horizontal y-axis gridlines only** — no vertical grid
5. **Automatic color assignment** from the brand hierarchy based on series count
6. **Any Plotly chart type** — `apply_theme()` works on any figure
7. **Ad hoc reports share one house style** — dark Bitwise cover, compact KPI
   cards, restrained pages, and rendered PDF QA

## Dependencies

- Python 3.8+
- Plotly >= 6.1.1
- Pandas >= 2.0.0
- NumPy >= 1.21
- kaleido (optional, for static image export)
- playwright (optional, for report PDF export)
- pillow (optional, for report contact sheets)
