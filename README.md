# AnalystKit

A comprehensive Python package providing shared Plotly themes, visualization helpers, and settings for analytics projects. Built with consistency and reusability in mind.

## Features

- **Consistent Styling**: Pre-defined color palettes and typography for professional visualizations
- **Theme Management**: Easy theme registration and application for Plotly charts
- **Chart Helpers**: Wrapper functions for common chart types with built-in styling
- **Formatting Utilities**: Number, percentage, currency, and date formatting helpers
- **Settings Management**: Environment-based configuration with Pydantic validation
- **Export Support**: High-quality chart export in multiple formats

## Installation

### From GitHub (Recommended for Team Use)

```bash
# Install directly from GitHub
pip install git+https://github.com/carlislejd/analystkit.git

# Or with Poetry
poetry add git+https://github.com/carlislejd/analystkit.git

# For a specific version/tag
pip install git+https://github.com/carlislejd/analystkit.git@v0.1.2
```

### Optional Dependencies

**Chart Export (Optional):** If you need to export charts to static images (PNG, SVG, PDF), install kaleido manually:

```bash
# With Poetry (let Poetry choose the best version for your platform)
poetry add kaleido

# With pip (let pip choose the best version for your platform)
pip install kaleido

# For specific platforms, you may need to specify a version:
# pip install kaleido==0.2.1  # For Plotly 5.x compatibility
# pip install kaleido>=1.0.0  # For Plotly 6.x compatibility
```

**Note:** Chart export functionality requires kaleido. Without it, you can still create and display charts, but export will raise an ImportError with helpful installation instructions. The package is designed to work with any kaleido version compatible with your Plotly version.

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

Manage configuration and API keys:

```python
from analystkit import load_settings, get_api_key, create_env_template

# Load settings
settings = load_settings()

# Get API key
api_key = get_api_key('openai')

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

# API keys
OPENAI_API_KEY=your_openai_key_here
MAPBOX_TOKEN=your_mapbox_token_here

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
- Plotly 5.24.0+ (compatible with any version including 6.x)
- Pandas 2.0.0+
- Pydantic 2.7.0+
- python-dotenv 1.0.1+
- requests 2.31.0+

### Optional Dependencies
- **kaleido**: Required only for chart export functionality (PNG, SVG, PDF)

**Note:** The package will install and work without kaleido, but chart export will raise an ImportError with helpful installation instructions. 

**Version Compatibility:**
- **Plotly 5.x + kaleido 0.2.1+** = Works great
- **Plotly 6.x + kaleido 1.0+** = Also works great

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

### For Users (Your Coworkers)

```bash
# Update to latest version
pip install --upgrade git+https://github.com/carlislejd/analystkit.git

# Or with Poetry
poetry update analystkit
```

### For Developers (You)

```bash
# Make your changes
git add .
git commit -m "Description of changes"
git push origin main

# Tag a new release
git tag v1.1.0
git push origin v1.1.0
```

## Compatibility Notes

- **Python**: 3.8+ required
- **Plotly**: 5.24.0+ (compatible with any version including 6.x)
- **Kaleido**: Any version compatible with your Plotly version (optional)

**Cross-Platform Support**: The package now handles ARM64 (Apple Silicon) compatibility by making kaleido optional. Users can install the kaleido version that works best for their platform and Plotly version.

**Version Compatibility Guide:**
- **Plotly 5.x + kaleido 0.2.1+** = Works great
- **Plotly 6.x + kaleido 1.0+** = Also works great

For troubleshooting, see the [GitHub issues](https://github.com/carlislejd/analystkit/issues) or check your Poetry environment with `poetry env info`.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]

## Support

For questions and support, please open an issue on the repository or contact [your-email@example.com].
