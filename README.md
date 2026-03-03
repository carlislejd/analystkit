# AnalystKit

Shared Plotly theme, visualization helpers, and chart utilities for analytics projects. Applies Bitwise brand styling automatically.

## For AI Assistants

See [`AI_REFERENCE.md`](AI_REFERENCE.md) for a complete API reference.

## Quick Start

```python
import analystkit as ak
import pandas as pd

data = pd.DataFrame({'category': ['A', 'B', 'C'], 'value': [10, 20, 30]})

fig = ak.create_bar_chart(data, x='category', y='value')
fig.show()

ak.save_chart(fig, "My Chart", aspect_ratio="18:9")
```

## Installation

```bash
pip install git+https://github.com/carlislejd/analystkit.git

# Or with Poetry
poetry add git+https://github.com/carlislejd/analystkit.git
```

Chart export requires kaleido:

```bash
pip install kaleido
```

## API Surface

### Chart Creation
- `create_bar_chart()` -- bar charts (vertical/horizontal)
- `create_line_chart()` -- line charts with optional grouping

### Theme & Styling
- `apply_theme()` -- apply Bitwise styling to any Plotly figure
- `get_color_palette()` -- get N colors from the brand palette

### Export
- `save_chart()` -- export in SVG/PNG with predefined aspect ratios
- `export_chart()` -- export a single format to a file path

### Tick Marks
- `apply_range_tick_marks()` -- boundary tick marks with midpoint labels for time series

### Constants
- `BITWISE_COLORS` -- full 11-color palette
- `COLOR_HIERARCHY` -- palette subsets keyed by item count (1-11)
- `CHART_COLORS` -- background, grid, text colors
- `FONT_FAMILIES` -- primary (PPNeueMontreal) and title (Items) fonts
- `FONT_SIZES` -- standardized sizes for title, axis, legend, annotation
- `STYLE_DEFAULTS` -- complete style config (fonts, margins, axes, legend)
- `SIZE_PRESETS` -- dimension presets (full, half, 18:9, 3:1, 1:1, type_a-f)
- `MARGIN_PRESETS` -- margin presets (minimal, standard, wide)

## Dependencies

- Python 3.8+
- Plotly >= 6.1.1
- Pandas >= 2.0.0
- kaleido (optional, for chart export)

## Project Structure

```
analystkit/
├── analystkit/
│   ├── __init__.py        # Public API
│   ├── colors.py          # Palettes, fonts, style constants
│   ├── plotly_theme.py    # Theme application and color palette logic
│   └── charts.py          # Chart creation, export, tick marks
├── pyproject.toml
├── README.md
└── AI_REFERENCE.md
```
