# AnalystKit - AI Reference

Everything is accessed via `import analystkit as ak`.

## Chart Creation

### `ak.create_bar_chart()`

```python
create_bar_chart(
    data: Union[pd.DataFrame, List, Dict],
    x: Optional[str] = None,
    y: Optional[str] = None,
    x_label: str = "",
    y_label: str = "",
    color_column: Optional[str] = None,
    orientation: str = "v",
    size_preset: str = "full",
    margin_preset: str = "minimal",
    **kwargs
) -> go.Figure
```

Data formats: DataFrame (requires x/y), dict (keys=x, values=y), list (y-values or [x,y] pairs).

### `ak.create_line_chart()`

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

Use `color_column` for multi-series grouping.

## Theme & Styling

### `ak.apply_theme()`

```python
apply_theme(fig, size_preset='full', margin_preset='minimal') -> go.Figure
```

Size presets used: `'18:9'`, `'3:1'`, `'type_a'`, `'type_e'`, `'full'`, `'half'`, `'1:1'`.
Margin presets: `'minimal'` (20px), `'standard'` (40px), `'wide'` (60px).

### `ak.get_color_palette()`

```python
get_color_palette(n_colors) -> List[str]
```

Returns N brand colors following the hierarchy.

## Export

### `ak.save_chart()`

```python
save_chart(
    fig: go.Figure,
    title: str,
    output_dir: str = "design",
    aspect_ratio: str = "18:9",
    include_svg: bool = True,
    include_png: bool = True,
    include_1x1: bool = False,
    png_scale: int = 2
) -> Dict[str, str]
```

Aspect ratios: `"18:9"` (1728x864), `"3:1"` (1728x576), `"1:1"` (1152x1152), `"type_a"` (1275x900), `"type_b"` (1200x750), `"type_c"` (1800x1050), `"type_d"` (1800x1125), `"type_e"` (825x975), `"type_f"` (825x900).

### `ak.export_chart()`

```python
export_chart(fig, filename, format="svg", width=None, height=None, scale=2) -> None
```

## Tick Marks

### `ak.apply_range_tick_marks()`

```python
apply_range_tick_marks(
    fig: go.Figure,
    start_date, end_date,
    period: str = "quarter",   # "quarter", "year", "month", "week"
    label_formatter=None,
    ticklen: int = 10,
    label_y_position: float = -0.01,
    include_start_boundary: bool = True,
    include_end_boundary: bool = True,
    **kwargs
) -> go.Figure
```

Tick marks at period boundaries, labels at midpoints.

## Constants

### Colors

```python
ak.BITWISE_COLORS  # ['#45b979', '#a7d8b5', '#006472', '#62a0ad', '#6c6b71', '#b7b6b9', '#4f2984', '#927fb5', '#00b6c9', '#91d6e0', '#f05b72']

ak.COLOR_HIERARCHY[1]  # ['#45b979']
ak.COLOR_HIERARCHY[2]  # ['#45b979', '#6c6b71']
ak.COLOR_HIERARCHY[3]  # ['#45b979', '#006472', '#6c6b71']
# ... up to 11

ak.CHART_COLORS['text']        # '#1B252A'
ak.CHART_COLORS['grid']        # '#e6e6e6'
ak.CHART_COLORS['grid_dark']   # '#C1C8CD'
ak.CHART_COLORS['background']  # '#ffffff'
```

### Fonts & Sizes

```python
ak.FONT_FAMILIES['primary']  # 'PPNeueMontreal-Regular'
ak.FONT_FAMILIES['title']    # 'Items-Regular'

ak.FONT_SIZES['title']       # 25
ak.FONT_SIZES['axis']        # 25
ak.FONT_SIZES['legend']      # 25
ak.FONT_SIZES['annotation']  # 25
```

### Style Defaults

```python
ak.STYLE_DEFAULTS['font']        # {family, size, color}
ak.STYLE_DEFAULTS['title_font']  # {family, size, color}
ak.STYLE_DEFAULTS['margin']      # {l, r, t, b}
ak.STYLE_DEFAULTS['axis']        # {showgrid, gridwidth, zeroline, ...}
ak.STYLE_DEFAULTS['xaxis']       # x-specific overrides
ak.STYLE_DEFAULTS['yaxis']       # y-specific overrides
ak.STYLE_DEFAULTS['legend']      # {borderwidth, bgcolor, orientation, ...}
ak.STYLE_DEFAULTS['grid']        # {width: 1}
```

## Design Rules

1. Axis titles hidden by default -- only shown when `x_label`/`y_label` are provided
2. Y-axis horizontal grid lines only -- no vertical grid
3. Colors applied automatically from brand palette based on series count
4. PPNeueMontreal-Regular for all text, Items-Regular for titles only
5. Legend: horizontal, top-right, no border, transparent background
