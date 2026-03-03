# AnalystKit

A comprehensive Python package providing shared Plotly themes, visualization helpers, and settings for analytics projects. Built with consistency and reusability in mind.

## For AI Assistants

**Quick Reference**: See [`AI_REFERENCE.md`](AI_REFERENCE.md) for a comprehensive guide designed for AI assistants.

**Quick Start Pattern:**
```python
import analystkit as ak
import pandas as pd

# Create chart from DataFrame
fig = ak.create_bar_chart(data=df, x='category', y='value')
fig.show()

# Or save with consistent aspect ratio
ak.save_chart(fig, "Chart Title", aspect_ratio="18:9")
```

**Key Functions:**
- `create_bar_chart()`, `create_line_chart()`, `create_scatter_chart()`, `create_heatmap()` - Create styled charts
- `save_chart()` - Save with consistent aspect ratios (18:9, 1:1, type_a-type_f)
- `apply_theme()` - Apply styling to any Plotly figure
- `format_number()`, `format_percentage()`, `format_currency()`, `format_date()` - Formatting utilities

**Design Defaults:**
- Axis titles hidden by default (use `x_label`/`y_label` to show)
- Automatic Bitwise brand colors
- Horizontal grid lines only (y-axis)
- PPNeueMontreal-Regular font (Items-Regular for titles)

## Features

- **Consistent Styling**: Pre-defined color palettes and typography for professional visualizations
- **Theme Management**: Easy theme registration and application for Plotly charts
- **Chart Helpers**: Wrapper functions for common chart types with built-in styling
- **Formatting Utilities**: Number, percentage, currency, and date formatting helpers
- **Settings Management**: Environment-based configuration with Pydantic validation
- **Export Support**: High-quality chart export in multiple formats
- **Auto-Coloring**: Automatic Bitwise brand colors with intelligent hierarchy
- **Clean Design**: Horizontal grid lines only (no vertical clutter), no default axis titles, no legend borders
- **Smart Export**: One-line chart saving with consistent aspect ratios (18:9, 1:1)

## Design Philosophy

AnalystKit follows a clean, professional design approach:

### Grid Lines
- **X-axis**: No vertical grid lines (clean, uncluttered look)
- **Y-axis**: Horizontal grid lines only (helps with value reading)
- **Zero line**: Only on Y-axis for reference

### Colors
- **Automatic**: All charts automatically use Bitwise brand colors
- **Hierarchy**: Colors follow a logical progression based on data complexity
- **Consistent**: Same color scheme across all chart types
- **Override**: Users can still specify custom colors if needed

### Axis Titles
- **No defaults**: Clean look without unnecessary labels
- **Optional**: Add titles only when explicitly needed
- **Professional**: Minimalist approach for business presentations

### Typography
- **Brand fonts**: Uses PP Neue Montreal Book and Items Regular
- **Readable sizes**: Optimized for both screen and print
- **Consistent**: Same font family across all chart elements

### Legend
- **No borders**: Clean, borderless legend design
- **Transparent background**: Seamless integration with chart background
- **Consistent fonts**: Matches chart typography standards

### Smart Export (`save_chart`)

One-line chart saving with consistent aspect ratios:

```python
from analystkit import create_bar_chart, save_chart

# Create your chart
fig = create_bar_chart(data, x='x', y='y')

# Save in multiple formats with 18:9 aspect ratio
files = save_chart(fig, "My Analysis", aspect_ratio="18:9")
# Output: {'svg': 'design/My_Analysis.svg', 'png': 'design/My_Analysis.png'}

# Save with both 18:9 and 1:1 ratios
files = save_chart(fig, "My Analysis", aspect_ratio="18:9", include_1x1=True)
# Output: {'svg': 'design/My_Analysis.svg', 'png': 'design/My_Analysis.png', 
#          'svg_1x1': 'design/My_Analysis_1x1.svg', 'png_1x1': 'design/My_Analysis_1x1.png'}
```

**Features:**
- **Consistent sizing**: Predefined aspect ratios (18:9, 1:1)
- **Multiple formats**: SVG and PNG in one call
- **Auto-directory**: Creates output directory if needed
- **Clean filenames**: Sanitizes titles for file system compatibility
- **High quality**: PNG exports with configurable scale factor

## Installation

### From GitHub (Recommended for Team Use)

```bash
# Install directly from GitHub
pip install git+https://github.com/carlislejd/analystkit.git

# Or with Poetry
poetry add git+https://github.com/carlislejd/analystkit.git

# For a specific version/tag
pip install git+https://github.com/carlislejd/analystkit.git@v0.3.0
```

### Optional Dependencies

**Chart Export (Optional):** If you need to export charts to static images (PNG, SVG, PDF), install kaleido manually:

```bash
# With Poetry (let Poetry choose the best version for your platform)
poetry add kaleido

# With pip (let pip choose the best version for your platform)
pip install kaleido
```

**Note:** Chart export functionality requires kaleido. Without it, you can still create and display charts, but export will raise an ImportError with helpful installation instructions.

### Local Development

```bash
cd packages/analystkit
poetry install

# If you need chart export functionality
poetry add kaleido
```

### Using pip (Local)

```bash
pip install -e packages/analystkit
```

## Quick Start

```python
import analystkit as ak
import pandas as pd

# Register the custom theme
ak.register_theme()

# Create sample data
data = pd.DataFrame({
    'Category': ['A', 'B', 'C', 'D'],
    'Value': [10, 25, 15, 30]
})

# Create a styled bar chart
fig = ak.create_bar_chart(
    data=data,
    x='Category',
    y='Value',
    x_label='Categories',
    y_label='Values'
)

# Display the chart
fig.show()

# Optional: Export the chart (requires kaleido)
# ak.export_chart(fig, 'sample_chart', format='svg')
```

## Core Components

### Colors and Styling (`colors.py`)

Pre-defined color palettes and styling constants:

```python
from analystkit import BITWISE_COLORS, COLOR_HIERARCHY, STYLE_DEFAULTS

# Use the primary color palette
print(BITWISE_COLORS)  # ['#66b77d', '#b1d6b7', '#2c6271', ...]

# Get appropriate colors for different numbers of items
colors = COLOR_HIERARCHY[3]  # ['#66b77d', '#2c6271', '#45454b']
```

### Theme Management (`plotly_theme.py`)

Register and apply custom themes:

```python
from analystkit import register_theme, apply_theme

# Register the custom theme
register_theme()

# Apply theme to existing figure
fig = apply_theme(
    fig, 
    size_preset='full',
    show_source=True,
    source_text='Source: Your Data Source'
)
```

### Chart Helpers (`charts.py`)

Create styled charts with minimal code:

```python
from analystkit import create_bar_chart, create_line_chart, create_scatter_chart

# Bar chart
fig = create_bar_chart(
    data=df,
    x='x_column',
    y='y_column',
    title='My Chart',
    show_source=True
)

# Line chart
fig = create_line_chart(
    data=df,
    x='date',
    y='value',
    color_column='category'
)

# Scatter plot
fig = create_scatter_chart(
    data=df,
    x='x',
    y='y',
    color_column='group',
    size_column='size'
)
```

### Formatting Utilities (`formats.py`)

Format numbers, percentages, and dates consistently:

```python
from analystkit import format_number, format_percentage, format_currency, format_date

# Number formatting
formatted = format_number(1234567, decimals=2, thousands_sep=",")
# Result: "1,234,567.00"

# Percentage formatting
formatted = format_percentage(0.1234, decimals=1)
# Result: "12.3%"

# Currency formatting
formatted = format_currency(1234.56, currency="USD")
# Result: "$1,234.56"

# Date formatting
formatted = format_date("2024-01-15", format_str="%B %d, %Y")
# Result: "January 15, 2024"
```

### Settings Management (`settings.py`)

Manage chart configuration:

```python
from analystkit import load_settings, create_env_template

# Load settings
settings = load_settings()

# Create environment template
create_env_template()
```

## Configuration

### Environment Variables

Create a `.env` file in your project root:

```bash
# Plotly settings
PLOTLY_THEME=plotly
PLOTLY_RENDERER=default

# Export settings
DEFAULT_EXPORT_FORMAT=svg
DEFAULT_EXPORT_SCALE=2

# Chart defaults
DEFAULT_CHART_WIDTH=1200
DEFAULT_CHART_HEIGHT=800
```

### Font Configuration

To use custom fonts, place your `.ttf` or `.otf` files in the `fonts/` directory and update the font settings in `colors.py`.

## Chart Types Supported

- **Bar Charts**: Vertical and horizontal orientations
- **Line Charts**: With optional color grouping
- **Scatter Plots**: With optional color and size mapping
- **Heatmaps**: 2D data visualization
- **Custom Charts**: Apply themes to any Plotly figure

## Export Formats

- SVG (default, scalable vector graphics)
- PNG (raster format)
- JPG (compressed raster format)
- PDF (print-ready format)

## Dependencies

### Required Dependencies
- Python 3.8+
- Plotly 6.1.1+
- Pandas 2.0.0+
- Pydantic 2.7.0+
- python-dotenv 1.0.1+

### Optional Dependencies
- **kaleido**: Required only for chart export functionality (PNG, SVG, PDF)

## Development

### Project Structure

```
analystkit/
├── analystkit/
│   ├── __init__.py          # Main package interface
│   ├── colors.py            # Color palettes and styling
│   ├── plotly_theme.py      # Theme management
│   ├── charts.py            # Chart helper functions
│   ├── formats.py           # Formatting utilities
│   ├── fonts.py             # Font management
│   ├── settings.py          # Configuration management
│   └── fonts/               # Custom font files
├── pyproject.toml           # Poetry configuration
├── README.md                # This file
└── LICENSE                  # License information
```

### Adding New Features

1. **New Chart Types**: Add functions to `charts.py`
2. **New Formats**: Extend `formats.py` with additional formatting functions
3. **New Colors**: Update `colors.py` with additional palettes
4. **New Settings**: Extend the `Settings` class in `settings.py`

### Testing

```bash
# Run tests (when implemented)
poetry run pytest

# Check code quality
poetry run flake8
poetry run black --check .
```

## Updating the Package

### For Users

```bash
# Update to latest version
pip install --upgrade git+https://github.com/carlislejd/analystkit.git

# Or with Poetry
poetry update analystkit
```

### For Developers

```bash
# Make your changes
git add .
git commit -m "Description of changes"
git push origin main

# Tag a new release
git tag v0.3.0
git push origin v0.3.0
```

## Compatibility Notes

- **Python**: 3.8+ required
- **Plotly**: 6.1.1+ (compatible with any version including 6.x)
- **Kaleido**: Any version compatible with your Plotly version (optional)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]

## Support

For questions and support, please open an issue on the repository or contact josh@bitwiseinvestments.com.
