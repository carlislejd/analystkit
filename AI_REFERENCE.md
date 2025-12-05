# AnalystKit - AI Assistant Reference Guide

This document provides a comprehensive reference for AI assistants to quickly understand and use AnalystKit for creating charts and visualizations.

## Quick Start Pattern

```python
import analystkit as ak
import pandas as pd

# 1. Create or load data (pandas DataFrame, dict, or list)
data = pd.DataFrame({
    'x': ['A', 'B', 'C'],
    'y': [10, 20, 30]
})

# 2. Create chart using helper function
fig = ak.create_bar_chart(
    data=data,
    x='x',
    y='y',
    x_label='Category',  # Optional
    y_label='Value'      # Optional
)

# 3. Display or save
fig.show()
# OR
ak.save_chart(fig, "My Chart", aspect_ratio="18:9")
```

## Available Chart Functions

### `create_bar_chart()`
Creates a styled bar chart with automatic Bitwise colors.

**Signature:**
```python
create_bar_chart(
    data: Union[pd.DataFrame, List, Dict],
    x: Optional[str] = None,
    y: Optional[str] = None,
    x_label: str = "",
    y_label: str = "",
    color_column: Optional[str] = None,
    orientation: str = "v",  # "v" for vertical, "h" for horizontal
    size_preset: str = "full",
    margin_preset: str = "minimal",
    **kwargs
) -> go.Figure
```

**Data Input Formats:**
- `pd.DataFrame`: Requires `x` and `y` column names
- `dict`: Keys become x-axis, values become y-axis
- `list`: Single list becomes y-axis (x is auto-generated), or list of [x, y] pairs

**Examples:**
```python
# DataFrame
fig = ak.create_bar_chart(df, x='category', y='value')

# Dict
fig = ak.create_bar_chart({'A': 10, 'B': 20, 'C': 30})

# List
fig = ak.create_bar_chart([10, 20, 30])  # y-values only
fig = ak.create_bar_chart([['A', 10], ['B', 20]])  # [x, y] pairs
```

### `create_line_chart()`
Creates a styled line chart with automatic Bitwise colors.

**Signature:**
```python
create_line_chart(
    data: Union[pd.DataFrame, List, Dict],
    x: Optional[str] = None,
    y: Optional[str] = None,
    x_label: str = "",
    y_label: str = "",
    color_column: Optional[str] = None,
    size_preset: str = "full",
    **kwargs
) -> go.Figure
```

**Examples:**
```python
# Single line
fig = ak.create_line_chart(df, x='date', y='price')

# Multiple lines (grouped by color_column)
fig = ak.create_line_chart(df, x='date', y='value', color_column='category')
```

### `create_scatter_chart()`
Creates a styled scatter plot with automatic Bitwise colors.

**Signature:**
```python
create_scatter_chart(
    data: Union[pd.DataFrame, List, Dict],
    x: Optional[str] = None,
    y: Optional[str] = None,
    x_label: str = "",
    y_label: str = "",
    color_column: Optional[str] = None,
    size_column: Optional[str] = None,
    size_preset: str = "full",
    **kwargs
) -> go.Figure
```

**Examples:**
```python
# Basic scatter
fig = ak.create_scatter_chart(df, x='x', y='y')

# With color grouping
fig = ak.create_scatter_chart(df, x='x', y='y', color_column='group')

# With size mapping
fig = ak.create_scatter_chart(df, x='x', y='y', size_column='size')
```

### `create_heatmap()`
Creates a styled heatmap.

**Signature:**
```python
create_heatmap(
    data: Union[pd.DataFrame, List[List], np.ndarray],
    x_labels: Optional[List] = None,
    y_labels: Optional[List] = None,
    x_label: str = "",
    y_label: str = "",
    color_scale: str = "Viridis",
    size_preset: str = "full",
    **kwargs
) -> go.Figure
```

**Examples:**
```python
# DataFrame
fig = ak.create_heatmap(df)

# 2D array
fig = ak.create_heatmap([[1, 2], [3, 4]], 
                        x_labels=['A', 'B'], 
                        y_labels=['X', 'Y'])
```

## Chart Export Functions

### `save_chart()`
Saves chart in multiple formats with consistent aspect ratios.

**Signature:**
```python
save_chart(
    fig: go.Figure,
    title: str,
    output_dir: str = "design",
    aspect_ratio: str = "18:9",  # Options: "18:9", "3:1", "1:1", "type_a" through "type_f"
    include_svg: bool = True,
    include_png: bool = True,
    include_1x1: bool = False,
    png_scale: int = 2
) -> Dict[str, str]
```

**Available Aspect Ratios:**
- `"18:9"` - Wide format (1728x864)
- `"3:1"` - Ultra-wide (1728x576)
- `"1:1"` - Square (1152x1152)
- `"type_a"` - 4.25x3 (1275x900)
- `"type_b"` - 4x2.5 (1200x750)
- `"type_c"` - 6x3.5 (1800x1050)
- `"type_d"` - 6x3.75 (1800x1125)
- `"type_e"` - 2.75x3.25 (825x975)
- `"type_f"` - 2.75x3 (825x900)

**Example:**
```python
files = ak.save_chart(fig, "My Analysis", aspect_ratio="18:9")
# Returns: {'svg': 'design/My_Analysis.svg', 'png': 'design/My_Analysis.png'}
```

### `export_chart()`
Exports a single chart to a file.

**Signature:**
```python
export_chart(
    fig: go.Figure,
    filename: str,
    format: str = "svg",  # "svg", "png", "jpg", "pdf"
    width: Optional[int] = None,
    height: Optional[int] = None,
    scale: int = 2
) -> None
```

## Theme and Styling

### `apply_theme()`
Applies Bitwise theme to any Plotly figure.

**Signature:**
```python
apply_theme(
    fig: go.Figure,
    size_preset: str = "full",
    margin_preset: str = "minimal"
) -> go.Figure
```

**Size Presets:**
- `"full"` - 1200x800
- `"half"` - 600x400
- `"18:9"` - 1728x864
- `"3:1"` - 1728x576
- `"1:1"` - 1152x1152
- `"type_a"` through `"type_f"` - Custom sizes

**Margin Presets:**
- `"minimal"` - 20px all sides
- `"standard"` - 40px all sides
- `"wide"` - 60px all sides

**Example:**
```python
# Apply theme to existing figure
fig = ak.apply_theme(fig, size_preset='full', margin_preset='minimal')
```

## Color System

### Automatic Colors
All chart functions automatically apply Bitwise brand colors based on data complexity:
- 1 item: Green (#45b979)
- 2 items: Green, Dark grey
- 3+ items: Follows COLOR_HIERARCHY

### Manual Color Access
```python
from analystkit import BITWISE_COLORS, COLOR_HIERARCHY

# Get colors for N items
colors = COLOR_HIERARCHY[3]  # Returns list of 3 colors

# Full palette
all_colors = BITWISE_COLORS
```

## Size Presets

Access size presets directly:
```python
from analystkit import SIZE_PRESETS

# Get dimensions
size = SIZE_PRESETS['type_a']  # {'width': 1275, 'height': 900}
```

## Formatting Utilities

### `format_number()`
```python
ak.format_number(1234567, decimals=2, thousands_sep=",")
# Returns: "1,234,567.00"
```

### `format_percentage()`
```python
ak.format_percentage(0.1234, decimals=1)
# Returns: "12.3%"
```

### `format_currency()`
```python
ak.format_currency(1234.56, currency="USD")
# Returns: "$1,234.56"
```

### `format_date()`
```python
ak.format_date("2024-01-15", format_str="%B %d, %Y")
# Returns: "January 15, 2024"
```

## Font Management

### `setup_fonts()`
Check and optionally install fonts.

```python
from analystkit import setup_fonts

# Check status
result = setup_fonts(auto_install=False)

# Auto-install missing fonts
result = setup_fonts(auto_install=True)
```

### `install_fonts()`
Manually install fonts from package.

```python
from analystkit import install_fonts

result = install_fonts()
print(result['installed'])  # List of installed fonts
```

## Common Patterns

### Pattern 1: Simple Bar Chart
```python
import analystkit as ak
import pandas as pd

data = pd.DataFrame({
    'category': ['A', 'B', 'C'],
    'value': [10, 20, 30]
})

fig = ak.create_bar_chart(data, x='category', y='value')
fig.show()
```

### Pattern 2: Time Series Line Chart
```python
fig = ak.create_line_chart(
    df, 
    x='date', 
    y='price',
    x_label='Date',
    y_label='Price ($)'
)
ak.save_chart(fig, "Price Over Time", aspect_ratio="18:9")
```

### Pattern 3: Multi-Series Chart
```python
# Automatically groups by color_column
fig = ak.create_line_chart(
    df,
    x='date',
    y='value',
    color_column='category'  # Creates separate line for each category
)
```

### Pattern 4: Custom Styling
```python
# Create chart
fig = ak.create_bar_chart(data, x='x', y='y')

# Apply custom size
fig = ak.apply_theme(fig, size_preset='type_a', margin_preset='wide')

# Add custom Plotly updates
fig.update_layout(title_text="Custom Title")
```

## Key Design Principles

1. **Axis Titles**: Hidden by default. Only show if explicitly provided via `x_label`/`y_label`
2. **Grid Lines**: Only horizontal (y-axis). No vertical grid lines.
3. **Colors**: Automatic Bitwise brand colors. No need to specify unless custom needed.
4. **Fonts**: PPNeueMontreal-Regular for all text, Items-Regular for titles only.
5. **Legend**: Horizontal, top-right, no border, transparent background.

## Important Notes for AI

1. **Data Format Flexibility**: Functions accept DataFrame, dict, or list - choose based on user's data format
2. **Automatic Styling**: All charts are automatically styled - no manual theme application needed
3. **Color Hierarchy**: Colors automatically assigned based on number of data series
4. **Size Presets**: Use `size_preset` parameter, not manual width/height
5. **Export**: Use `save_chart()` for consistent aspect ratios, `export_chart()` for custom sizes
6. **Fonts**: May need installation on first use - suggest `setup_fonts(auto_install=True)`

## Error Handling

- Missing columns: Functions will raise `ValueError` with clear message
- Missing fonts: Charts will render but may use fallback fonts
- Export errors: Will raise `ImportError` if kaleido not installed (with helpful message)

## Return Types

- Chart functions return `plotly.graph_objects.Figure`
- Can be displayed with `.show()`
- Can be saved with `save_chart()` or `export_chart()`
- Can be further customized with Plotly's `.update_layout()` and `.update_traces()`

