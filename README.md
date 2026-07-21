# AnalystKit

Bitwise brand theme and chart utilities for Plotly. Applies brand colors, fonts, grid styling, and automatic font scaling to any Plotly figure.

## For AI Assistants

Start with [`AGENTS.md`](AGENTS.md) for agent instructions, then use
[`CHART_RECIPES.md`](CHART_RECIPES.md) for production chart patterns and
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

## Dependencies

- Python 3.8+
- Plotly >= 6.1.1
- Pandas >= 2.0.0
- NumPy >= 1.21
- kaleido (optional, for static image export)
