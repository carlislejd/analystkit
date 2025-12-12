"""Common chart wrapper functions for creating styled charts."""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Union, Callable
from datetime import datetime, timedelta
from .plotly_theme import apply_theme, get_color_palette
from .colors import SIZE_PRESETS, COLOR_HIERARCHY, OPACITY, MARGIN_PRESETS, FONT_SIZES, FONT_FAMILIES

def _apply_scatter_legend_markers(fig: go.Figure, marker_size: int = 10) -> go.Figure:
    """Apply scatter circle markers to legend for all traces.
    
    This is the standard pattern: replace all legend symbols (bar, line, area, etc.)
    with scatter circle markers for consistency across all chart types.
    
    Args:
        fig: Plotly figure to modify
        marker_size: Size of the legend markers (default: 10)
    
    Returns:
        Modified figure with scatter markers in legend
    """
    # Store original traces and their properties
    traces_to_process = []
    
    for trace in fig.data:
        # Only process traces that have names and are shown in legend
        if trace.name and trace.showlegend is not False:
            # Extract color from different trace types
            color = None
            
            # Try to get color from marker (for scatter, bar)
            if hasattr(trace, 'marker') and trace.marker:
                if isinstance(trace.marker, dict):
                    color = trace.marker.get('color')
                elif hasattr(trace.marker, 'color'):
                    color = trace.marker.color
            
            # Try to get color from line (for line charts)
            if not color and hasattr(trace, 'line') and trace.line:
                if isinstance(trace.line, dict):
                    color = trace.line.get('color')
                elif hasattr(trace.line, 'color'):
                    color = trace.line.color
            
            # Try to get color from fillcolor (for area charts)
            if not color and hasattr(trace, 'fillcolor'):
                color = trace.fillcolor
            
            # Fallback to default color if none found
            if not color:
                color = COLOR_HIERARCHY[1][0]  # Default to primary green
            
            # Handle list/array colors (take first if multiple)
            if isinstance(color, (list, np.ndarray)) and len(color) > 0:
                color = color[0] if isinstance(color[0], str) else COLOR_HIERARCHY[1][0]
            
            traces_to_process.append({
                'trace': trace,
                'name': trace.name,
                'color': color,
                'legendgroup': getattr(trace, 'legendgroup', trace.name)
            })
    
    # Hide original traces from legend and add scatter markers
    for trace_info in traces_to_process:
        trace = trace_info['trace']
        
        # Hide original trace from legend
        trace.showlegend = False
        
        # Add invisible scatter trace with marker for legend
        fig.add_trace(go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            marker=dict(
                size=marker_size,
                color=trace_info['color'],
            ),
            showlegend=True,
            name=trace_info['name'],
            legendgroup=trace_info['legendgroup'],
            hoverinfo='skip'
        ))
    
    return fig

def create_bar_chart(
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
) -> go.Figure:
    """Create a styled bar chart.
    
    Args:
        data: DataFrame, list, or dict containing the data
        x: Column name or values for x-axis
        y: Column name or values for y-axis
        x_label: X-axis label
        y_label: Y-axis label
        color_column: Column to use for color grouping
        orientation: Chart orientation ('v' for vertical, 'h' for horizontal)
        size_preset: Size preset to use
        margin_preset: Margin preset to use ('minimal', 'standard', 'wide')
        **kwargs: Additional arguments passed to go.Bar
    
    Returns:
        Styled Plotly figure
    """
    if isinstance(data, pd.DataFrame):
        if x and y:
            if color_column:
                fig = px.bar(
                    data, 
                    x=x, 
                    y=y, 
                    color=color_column,
                    orientation=orientation,
                    **kwargs
                )
            else:
                fig = px.bar(
                    data, 
                    x=x, 
                    y=y,
                    orientation=orientation,
                    **kwargs
                )
        else:
            raise ValueError("Both x and y must be specified for DataFrame input")
    else:
        # Handle list/dict input
        if isinstance(data, dict):
            x_vals = list(data.keys())
            y_vals = list(data.values())
        elif isinstance(data, list):
            if isinstance(data[0], (list, tuple)) and len(data[0]) == 2:
                x_vals = [item[0] for item in data]
                y_vals = [item[1] for item in data]
            else:
                x_vals = list(range(len(data)))
                y_vals = data
        else:
            raise ValueError("Data must be DataFrame, dict, or list")
        
        fig = go.Figure(data=[
            go.Bar(
                x=x_vals if orientation == "v" else y_vals,
                y=y_vals if orientation == "v" else x_vals,
                orientation=orientation,
                **kwargs
            )
        ])
    
    # Explicitly hide axis titles by default (before applying theme)
    fig.update_xaxes(title=None)
    fig.update_yaxes(title=None)
    
    # Apply styling
    fig = apply_theme(
        fig, 
        size_preset=size_preset
    )
    
    # Auto-apply Bitwise colors with hierarchy if no custom colors specified
    if 'color_discrete_sequence' not in kwargs and 'color' not in kwargs:
        if color_column:
            unique_values = data[color_column].nunique() if hasattr(data, 'nunique') else len(set(data[color_column]))
            colors = get_color_palette(unique_values)
            # Apply colors individually to each trace
            for i, trace in enumerate(fig.data):
                if i < len(colors):
                    trace.update(marker_color=colors[i])
        else:
            # For single series, use primary Bitwise color
            fig.update_traces(marker_color=COLOR_HIERARCHY[1][0])
    
    # Apply scatter circle markers to legend (standard for all chart types)
    fig = _apply_scatter_legend_markers(fig, marker_size=10)
    
    # Only update labels if explicitly provided (no defaults)
    if x_label:
        fig.update_xaxes(title_text=x_label)
    if y_label:
        fig.update_yaxes(title_text=y_label)
    
    return fig

def create_line_chart(
    data: Union[pd.DataFrame, List, Dict],
    x: Optional[str] = None,
    y: Optional[str] = None,
    x_label: str = "",
    y_label: str = "",
    color_column: Optional[str] = None,
    size_preset: str = "full",
    **kwargs
) -> go.Figure:
    """Create a styled line chart.
    
    Args:
        data: DataFrame, list, or dict containing the data
        x: Column name or values for x-axis
        y: Column name or values for y-axis
        x_label: X-axis label
        y_label: Y-axis label
        color_column: Column to use for color grouping
        size_preset: Size preset to use
        **kwargs: Additional arguments passed to go.Scatter
    
    Returns:
        Styled Plotly figure
    """
    if isinstance(data, pd.DataFrame):
        if x and y:
            if color_column:
                fig = px.line(
                    data, 
                    x=x, 
                    y=y, 
                    color=color_column,
                    **kwargs
                )
            else:
                fig = px.line(
                    data, 
                    x=x, 
                    y=y,
                    **kwargs
                )
        else:
            raise ValueError("Both x and y must be specified for DataFrame input")
    else:
        # Handle list/dict input
        if isinstance(data, dict):
            x_vals = list(data.keys())
            y_vals = list(data.values())
        elif isinstance(data, list):
            if isinstance(data[0], (list, tuple)) and len(data[0]) == 2:
                x_vals = [item[0] for item in data]
                y_vals = [item[1] for item in data]
            else:
                x_vals = list(range(len(data)))
                y_vals = data
        else:
            raise ValueError("Data must be DataFrame, dict, or list")
        
        fig = go.Figure(data=[
            go.Scatter(
                x=x_vals,
                y=y_vals,
                mode='lines+markers',
                **kwargs
            )
        ])
    
    # Explicitly hide axis titles by default (before applying theme)
    fig.update_xaxes(title=None)
    fig.update_yaxes(title=None)
    
    # Apply styling
    fig = apply_theme(
        fig, 
        size_preset=size_preset
    )
    
    # Auto-apply Bitwise colors with hierarchy if no custom colors specified
    if 'color_discrete_sequence' not in kwargs and 'color' not in kwargs:
        if color_column:
            unique_values = data[color_column].nunique() if hasattr(data, 'nunique') else len(set(data[color_column]))
            colors = get_color_palette(unique_values)
            # Apply colors individually to each trace
            for i, trace in enumerate(fig.data):
                if i < len(colors):
                    trace.update(marker_color=colors[i], line_color=colors[i])
        else:
            # For multiple series without color_column, use color hierarchy
            if len(fig.data) > 1:
                colors = get_color_palette(len(fig.data))
                for i, trace in enumerate(fig.data):
                    if i < len(colors):
                        trace.update(marker_color=colors[i], line_color=colors[i])
            else:
                # For single series, use primary Bitwise color
                fig.update_traces(marker_color=COLOR_HIERARCHY[1][0], line_color=COLOR_HIERARCHY[1][0])
    
    # Apply scatter circle markers to legend (standard for all chart types)
    fig = _apply_scatter_legend_markers(fig, marker_size=10)
    
    # Only update labels if explicitly provided (no defaults)
    if x_label:
        fig.update_xaxes(title_text=x_label)
    if y_label:
        fig.update_yaxes(title_text=y_label)
    
    return fig

def create_scatter_chart(
    data: Union[pd.DataFrame, List, Dict],
    x: Optional[str] = None,
    y: Optional[str] = None,
    x_label: str = "",
    y_label: str = "",
    color_column: Optional[str] = None,
    size_column: Optional[str] = None,
    size_preset: str = "full",
    **kwargs
) -> go.Figure:
    """Create a styled scatter chart.
    
    Args:
        data: DataFrame, list, or dict containing the data
        x: Column name or values for x-axis
        y: Column name or values for y-axis
        x_label: X-axis label
        y_label: Y-axis label
        color_column: Column to use for color grouping
        size_column: Column to use for marker size
        size_preset: Size preset to use
        **kwargs: Additional arguments passed to go.Scatter
    
    Returns:
        Styled Plotly figure
    """
    if isinstance(data, pd.DataFrame):
        if x and y:
            if color_column and size_column:
                fig = px.scatter(
                    data, 
                    x=x, 
                    y=y, 
                    color=color_column,
                    size=size_column,
                    **kwargs
                )
            elif color_column:
                fig = px.scatter(
                    data, 
                    x=x, 
                    y=y, 
                    color=color_column,
                    **kwargs
                )
            elif size_column:
                fig = px.scatter(
                    data, 
                    x=x, 
                    y=y, 
                    size=size_column,
                    **kwargs
                )
            else:
                fig = px.scatter(
                    data, 
                    x=x, 
                    y=y,
                    **kwargs
                )
        else:
            raise ValueError("Both x and y must be specified for DataFrame input")
    else:
        # Handle list/dict input
        if isinstance(data, dict):
            x_vals = list(data.keys())
            y_vals = list(data.values())
        elif isinstance(data, list):
            if isinstance(data[0], (list, tuple)) and len(data[0]) == 2:
                x_vals = [item[0] for item in data]
                y_vals = [item[1] for item in data]
            else:
                x_vals = list(range(len(data)))
                y_vals = data
        else:
            raise ValueError("Data must be DataFrame, dict, or list")
        
        fig = go.Figure(data=[
            go.Scatter(
                x=x_vals,
                y=y_vals,
                mode='markers',
                **kwargs
            )
        ])
    
    # Explicitly hide axis titles by default (before applying theme)
    fig.update_xaxes(title=None)
    fig.update_yaxes(title=None)
    
    # Apply styling
    fig = apply_theme(
        fig, 
        size_preset=size_preset
    )
    
    # Auto-apply Bitwise colors with hierarchy if no custom colors specified
    if 'color_discrete_sequence' not in kwargs and 'color' not in kwargs:
        if color_column:
            unique_values = data[color_column].nunique() if hasattr(data, 'nunique') else len(set(data[color_column]))
            colors = get_color_palette(unique_values)
            fig.update_traces(marker_color=colors)
        else:
            # For single series, use primary Bitwise color
            fig.update_traces(marker_color=COLOR_HIERARCHY[1][0])
    
    # Apply scatter circle markers to legend (standard for all chart types)
    fig = _apply_scatter_legend_markers(fig, marker_size=10)
    
    # Only update labels if explicitly provided (no defaults)
    if x_label:
        fig.update_xaxes(title_text=x_label)
    if y_label:
        fig.update_yaxes(title_text=y_label)
    
    return fig

def create_heatmap(
    data: Union[pd.DataFrame, List[List], np.ndarray],
    x_labels: Optional[List] = None,
    y_labels: Optional[List] = None,
    x_label: str = "",
    y_label: str = "",
    color_scale: str = "Viridis",
    size_preset: str = "full",
    **kwargs
) -> go.Figure:
    """Create a styled heatmap.
    
    Args:
        data: 2D data for heatmap
        x_labels: Labels for x-axis
        y_labels: Labels for y-axis
        x_label: X-axis label
        y_label: Y-axis label
        color_scale: Color scale to use
        size_preset: Size preset to use
        **kwargs: Additional arguments passed to go.Heatmap
    
    Returns:
        Styled Plotly figure
    """
    if isinstance(data, pd.DataFrame):
        z_data = data.values
        x_labels = x_labels or list(data.columns)
        y_labels = y_labels or list(data.index)
    else:
        z_data = data
        if x_labels is None:
            x_labels = list(range(z_data.shape[1]))
        if y_labels is None:
            y_labels = list(range(z_data.shape[0]))
    
    fig = go.Figure(data=[
        go.Heatmap(
            z=z_data,
            x=x_labels,
            y=y_labels,
            colorscale=color_scale,
            **kwargs
        )
    ])
    
    # Explicitly hide axis titles by default (before applying theme)
    fig.update_xaxes(title=None)
    fig.update_yaxes(title=None)
    
    # Apply styling
    fig = apply_theme(
        fig, 
        size_preset=size_preset
    )
    
    # Only update labels if explicitly provided (no defaults)
    if x_label:
        fig.update_xaxes(title_text=x_label)
    if y_label:
        fig.update_yaxes(title_text=y_label)
    
    return fig

def export_chart(
    fig: go.Figure, 
    filename: str, 
    format: str = "svg",
    width: Optional[int] = None,
    height: Optional[int] = None,
    scale: int = 2
) -> None:
    """Export a chart to a file.
    
    Args:
        fig: Plotly figure to export
        filename: Output filename
        format: Export format (svg, png, jpg, pdf)
        width: Export width (uses chart width if None)
        height: Export height (uses chart height if None)
        scale: Scale factor for raster formats
    
    Raises:
        ImportError: If kaleido is not installed (required for export)
        ValueError: If export format is not supported
    """
    # Check if kaleido is available
    try:
        import kaleido
    except ImportError:
        raise ImportError(
            "Chart export requires kaleido. Install with: "
            "poetry add kaleido "
            "or pip install kaleido"
        )
    
    if not filename.endswith(f".{format}"):
        filename = f"{filename}.{format}"
    
    export_width = width or fig.layout.width or SIZE_PRESETS['full']['width']
    export_height = height or fig.layout.height or SIZE_PRESETS['full']['height']
    
    fig.write_image(
        filename,
        width=export_width,
        height=export_height,
        scale=scale
    )

def save_chart(
    fig: go.Figure,
    title: str,
    output_dir: str = "design",
    aspect_ratio: str = "18:9",
    include_svg: bool = True,
    include_png: bool = True,
    include_1x1: bool = False,
    png_scale: int = 2
) -> Dict[str, str]:
    """Save a chart in multiple formats with consistent aspect ratios.
    
    This function automatically exports charts in SVG and PNG formats with
    predefined aspect ratios, making it easy to maintain consistent sizing
    across all visualizations.
    
    Args:
        fig: Plotly figure to save
        title: Chart title (used for filename)
        output_dir: Directory to save files (default: "design")
        aspect_ratio: Aspect ratio for exports ("18:9", "3:1", or "1:1")
        include_svg: Whether to export SVG format (default: True)
        include_png: Whether to export PNG format (default: True)
        include_1x1: Whether to also export 1:1 ratio versions (default: False)
        png_scale: Scale factor for PNG exports (default: 2 for optimal quality)
    
    Returns:
        Dict[str, str]: Dictionary mapping format names to file paths
        
    Raises:
        ImportError: If kaleido is not installed (required for PNG export)
        ValueError: If aspect_ratio is not supported
        OSError: If output directory cannot be created
    
    Example:
        >>> fig = ak.create_bar_chart(data, x='x', y='y')
        >>> files = ak.save_chart(fig, "My Chart", aspect_ratio="18:9")
        >>> print(f"Saved: {files}")
        # Output: {'svg': 'design/My Chart.svg', 'png': 'design/My Chart.png'}
    """
    import os
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Clean title for filename
    clean_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
    clean_title = clean_title.replace(' ', '_')
    
    # Define aspect ratios and their dimensions (in pixels at 96 DPI)
    aspect_ratios = {
        "18:9": {"width": 18 * 96, "height": 9 * 96},  # 1728x864
        "3:1": {"width": 18 * 96, "height": 6 * 96},   # 1728x576
        "1:1": {"width": 12 * 96, "height": 12 * 96},  # 1152x1152
        "type_a": {"width": 1275, "height": 900},      # 4.25x3
        "type_b": {"width": 1200, "height": 750},      # 4x2.5
        "type_c": {"width": 1800, "height": 1050},     # 6x3.5
        "type_d": {"width": 1800, "height": 1125},     # 6x3.75
        "type_e": {"width": 825, "height": 975},       # 2.75x3.25
        "type_f": {"width": 825, "height": 900},       # 2.75x3
    }
    
    if aspect_ratio not in aspect_ratios:
        raise ValueError(f"Unsupported aspect ratio: {aspect_ratio}. Supported: {list(aspect_ratios.keys())}")
    
    saved_files = {}
    dimensions = aspect_ratios[aspect_ratio]
    
    # Export SVG
    if include_svg:
        svg_path = os.path.join(output_dir, f"{clean_title}.svg")
        try:
            export_chart(fig, svg_path, format="svg", 
                        width=dimensions["width"], height=dimensions["height"])
            saved_files["svg"] = svg_path
        except ImportError:
            print("Warning: SVG export failed - kaleido not installed")
    
    # Export PNG
    if include_png:
        png_path = os.path.join(output_dir, f"{clean_title}.png")
        try:
            export_chart(fig, png_path, format="png", 
                        width=dimensions["width"], height=dimensions["height"], 
                        scale=png_scale)
            saved_files["png"] = png_path
        except ImportError:
            print("Warning: PNG export failed - kaleido not installed")
    
    # Export 1:1 ratio versions if requested
    if include_1x1:
        square_dimensions = aspect_ratios["1:1"]
        
        if include_svg:
            svg_1x1_path = os.path.join(output_dir, f"{clean_title}_1x1.svg")
            try:
                export_chart(fig, svg_1x1_path, format="svg",
                            width=square_dimensions["width"], height=square_dimensions["height"])
                saved_files["svg_1x1"] = svg_1x1_path
            except ImportError:
                print("Warning: 1:1 SVG export failed - kaleido not installed")
        
        if include_png:
            png_1x1_path = os.path.join(output_dir, f"{clean_title}_1x1.png")
            try:
                export_chart(fig, png_1x1_path, format="png",
                            width=square_dimensions["width"], height=square_dimensions["height"],
                            scale=png_scale)
                saved_files["png_1x1"] = png_1x1_path
            except ImportError:
                print("Warning: 1:1 PNG export failed - kaleido not installed")
    
    return saved_files

def apply_range_tick_marks(
    fig: go.Figure,
    start_date: Union[str, pd.Timestamp, datetime],
    end_date: Union[str, pd.Timestamp, datetime],
    period: str = "quarter",
    label_formatter: Optional[Callable[[int, int], str]] = None,
    ticklen: int = 10,
    label_y_position: float = -0.01,
    label_font_size: Optional[int] = None,
    label_font_family: Optional[str] = None,
    xaxis_id: str = "x",
    include_start_boundary: bool = True,
    include_end_boundary: bool = True,
    **kwargs
) -> go.Figure:
    """Apply tick marks at period boundaries with labels at midpoints.
    
    This creates a powerful visualization pattern where:
    - Tick marks appear at the START and END of each period (e.g., quarters)
    - Labels appear at the MIDPOINT of each period (via annotations)
    - Labels are positioned below the x-axis with no tick marks directly under them
    
    This makes it easy to see when periods begin and end, while keeping labels
    cleanly positioned in the middle of each range.
    
    Args:
        fig: Plotly figure to modify
        start_date: Start date of the data range (string, Timestamp, or datetime)
        end_date: End date of the data range (string, Timestamp, or datetime)
        period: Period type - "quarter", "year", "month", "week", or "day"
        label_formatter: Optional function(year, period_num) -> str for custom labels.
                        Default: "Q{quarter} '{year}" for quarters, "{year}" for years
        ticklen: Length of tick marks (default: 10)
        label_y_position: Y position for labels in paper coordinates (default: -0.01, below axis)
        label_font_size: Font size for labels (default: FONT_SIZES['axis'])
        label_font_family: Font family for labels (default: FONT_FAMILIES['primary'])
        xaxis_id: X-axis identifier (default: "x")
        include_start_boundary: Whether to include tick at first period start (default: True)
        include_end_boundary: Whether to include tick at last period end (default: True)
        **kwargs: Additional arguments passed to fig.update_layout for xaxis
    
    Returns:
        Modified Plotly figure with range tick marks and midpoint labels
    
    Example:
        >>> fig = go.Figure()
        >>> fig.add_trace(go.Scatter(x=dates, y=values))
        >>> # Apply quarter-based range tick marks
        >>> fig = ak.apply_range_tick_marks(
        ...     fig, 
        ...     start_date='2023-01-01',
        ...     end_date='2025-12-31',
        ...     period='quarter'
        ... )
        >>> # Custom label formatter
        >>> fig = ak.apply_range_tick_marks(
        ...     fig,
        ...     start_date='2020-01-01',
        ...     end_date='2024-12-31',
        ...     period='year',
        ...     label_formatter=lambda year, _: f"{year}"
        ... )
    """
    # Convert dates to Timestamps
    start_ts = pd.Timestamp(start_date)
    end_ts = pd.Timestamp(end_date)
    
    # Default label formatters
    if label_formatter is None:
        if period == "quarter":
            label_formatter = lambda year, q: f"Q{q} '{str(year)[2:]}"
        elif period == "year":
            label_formatter = lambda year, _: str(year)
        elif period == "month":
            label_formatter = lambda year, month: f"{pd.Timestamp(year, month, 1).strftime('%b')} '{str(year)[2:]}"
        elif period == "week":
            label_formatter = lambda year, week_num: f"W{week_num}"
        else:
            label_formatter = lambda year, p: f"{p}"
    
    # Set defaults for font
    if label_font_size is None:
        label_font_size = FONT_SIZES['axis']
    if label_font_family is None:
        label_font_family = FONT_FAMILIES['primary']
    
    tick_vals = []  # Boundary positions (for tick marks)
    label_annotations = []  # Labels at midpoints (via annotations)
    
    # Generate periods based on type
    if period == "quarter":
        # Q1 2023 through Q4 of end year
        start_year = start_ts.year
        end_year = end_ts.year
        
        for year in range(start_year, end_year + 1):
            for quarter in range(1, 5):
                # Quarter boundaries
                quarter_start_month = (quarter - 1) * 3 + 1
                quarter_end_month = quarter_start_month + 2
                
                # Calculate quarter start date (first day of quarter)
                quarter_start = pd.Timestamp(f'{year}-{quarter_start_month:02d}-01')
                
                # Calculate quarter end date (last day of quarter)
                if quarter_end_month == 12:
                    quarter_end = pd.Timestamp(f'{year}-12-31')
                else:
                    # Get last day of the month
                    next_month = quarter_end_month + 1
                    if next_month > 12:
                        next_month = 1
                        next_year = year + 1
                    else:
                        next_year = year
                    quarter_end = pd.Timestamp(f'{next_year}-{next_month:02d}-01') - pd.Timedelta(days=1)
                
                # Calculate quarter midpoint (for label)
                days_in_quarter = (quarter_end - quarter_start).days
                quarter_midpoint = quarter_start + pd.Timedelta(days=days_in_quarter // 2)
                
                # Only add if period overlaps with our data range
                if quarter_end >= start_ts and quarter_start <= end_ts:
                    # Add start boundary tick
                    if quarter_start >= start_ts and (include_start_boundary or year != start_year or quarter != 1):
                        tick_vals.append(quarter_start.strftime('%Y-%m-%d'))
                    
                    # Add midpoint label as annotation
                    if quarter_midpoint >= start_ts and quarter_midpoint <= end_ts:
                        label_annotations.append(dict(
                            x=quarter_midpoint.strftime('%Y-%m-%d'),
                            y=label_y_position,
                            text=label_formatter(year, quarter),
                            showarrow=False,
                            xref='x',
                            yref='paper',
                            xanchor='center',
                            yanchor='top',
                            font=dict(size=label_font_size, family=label_font_family)
                        ))
                    
                    # Add end boundary tick (only if not last quarter of last year, or if include_end_boundary is True)
                    if quarter_end <= end_ts:
                        if not (year == end_year and quarter == 4) or include_end_boundary:
                            tick_vals.append(quarter_end.strftime('%Y-%m-%d'))
    
    elif period == "year":
        # Years from start to end
        start_year = start_ts.year
        end_year = end_ts.year
        
        for year in range(start_year, end_year + 1):
            year_start = pd.Timestamp(f'{year}-01-01')
            year_end = pd.Timestamp(f'{year}-12-31')
            
            # Calculate year midpoint
            year_midpoint = pd.Timestamp(f'{year}-07-01')  # Mid-year
            
            # Only add if year overlaps with data range
            if year_end >= start_ts and year_start <= end_ts:
                # Add start boundary tick
                if year_start >= start_ts and (include_start_boundary or year != start_year):
                    tick_vals.append(year_start.strftime('%Y-%m-%d'))
                
                # Add midpoint label
                if year_midpoint >= start_ts and year_midpoint <= end_ts:
                    label_annotations.append(dict(
                        x=year_midpoint.strftime('%Y-%m-%d'),
                        y=label_y_position,
                        text=label_formatter(year, year),
                        showarrow=False,
                        xref='x',
                        yref='paper',
                        xanchor='center',
                        yanchor='top',
                        font=dict(size=label_font_size, family=label_font_family)
                    ))
                
                # Add end boundary tick
                if year_end <= end_ts and (include_end_boundary or year != end_year):
                    tick_vals.append(year_end.strftime('%Y-%m-%d'))
    
    elif period == "month":
        # Months from start to end
        current = start_ts.replace(day=1)  # Start of first month
        
        while current <= end_ts:
            # Month boundaries
            month_start = current
            if current.month == 12:
                month_end = pd.Timestamp(current.year, 12, 31)
                next_month = pd.Timestamp(current.year + 1, 1, 1)
            else:
                month_end = pd.Timestamp(current.year, current.month + 1, 1) - pd.Timedelta(days=1)
                next_month = pd.Timestamp(current.year, current.month + 1, 1)
            
            # Calculate month midpoint (approximately day 15)
            month_midpoint = month_start + pd.Timedelta(days=14)
            
            # Only add if month overlaps with data range
            if month_end >= start_ts and month_start <= end_ts:
                # Add start boundary tick
                if month_start >= start_ts and (include_start_boundary or current != start_ts.replace(day=1)):
                    tick_vals.append(month_start.strftime('%Y-%m-%d'))
                
                # Add midpoint label
                if month_midpoint >= start_ts and month_midpoint <= end_ts:
                    label_annotations.append(dict(
                        x=month_midpoint.strftime('%Y-%m-%d'),
                        y=label_y_position,
                        text=label_formatter(current.year, current.month),
                        showarrow=False,
                        xref='x',
                        yref='paper',
                        xanchor='center',
                        yanchor='top',
                        font=dict(size=label_font_size, family=label_font_family)
                    ))
                
                # Add end boundary tick
                if month_end <= end_ts and (include_end_boundary or next_month > end_ts):
                    tick_vals.append(month_end.strftime('%Y-%m-%d'))
            
            current = next_month
    
    elif period == "week":
        # Weeks from start to end (Monday to Sunday)
        # Find the Monday of the week containing start_date
        current = start_ts
        # Get to Monday (weekday 0 = Monday)
        days_since_monday = current.weekday()
        week_start = current - pd.Timedelta(days=days_since_monday)
        
        week_num = 1
        while week_start <= end_ts:
            # Week boundaries (Monday to Sunday)
            week_end = week_start + pd.Timedelta(days=6)  # Sunday
            
            # Calculate week midpoint (Thursday)
            week_midpoint = week_start + pd.Timedelta(days=3)
            
            # Only add if week overlaps with data range
            if week_end >= start_ts and week_start <= end_ts:
                # Add start boundary tick (Monday)
                if week_start >= start_ts and (include_start_boundary or week_start != start_ts - pd.Timedelta(days=start_ts.weekday())):
                    tick_vals.append(week_start.strftime('%Y-%m-%d'))
                
                # Add midpoint label (Thursday)
                if week_midpoint >= start_ts and week_midpoint <= end_ts:
                    # Calculate ISO week number for the year
                    iso_year, iso_week, _ = week_midpoint.isocalendar()
                    label_annotations.append(dict(
                        x=week_midpoint.strftime('%Y-%m-%d'),
                        y=label_y_position,
                        text=label_formatter(iso_year, iso_week),
                        showarrow=False,
                        xref='x',
                        yref='paper',
                        xanchor='center',
                        yanchor='top',
                        font=dict(size=label_font_size, family=label_font_family)
                    ))
                
                # Add end boundary tick (Sunday)
                if week_end <= end_ts and (include_end_boundary or week_start + pd.Timedelta(days=7) > end_ts):
                    tick_vals.append(week_end.strftime('%Y-%m-%d'))
            
            # Move to next week (next Monday)
            week_start = week_start + pd.Timedelta(days=7)
            week_num += 1
    
    else:
        raise ValueError(f"Unsupported period type: {period}. Supported: 'quarter', 'year', 'month', 'week'")
    
    # Update x-axis with tick marks at boundaries, empty labels
    xaxis_dict = dict(
        showgrid=False,
        tickmode='array',
        tickvals=tick_vals,
        ticktext=[''] * len(tick_vals),  # Empty labels for all tick marks
        tickangle=0,
        range=[start_ts.strftime('%Y-%m-%d'), end_ts.strftime('%Y-%m-%d')],
        ticks='outside',
        ticklen=ticklen,
        tickwidth=1,
        showticklabels=False  # Hide tick labels since we're using annotations
    )
    
    # Merge any additional kwargs
    xaxis_dict.update(kwargs)
    
    # Update layout
    fig.update_layout(**{f"{xaxis_id}axis": xaxis_dict})
    
    # Increase bottom margin to accommodate labels (if not already set)
    current_margin = fig.layout.margin or {}
    if isinstance(current_margin, dict):
        bottom_margin = current_margin.get('b', 70)
        fig.update_layout(margin=dict(
            b=max(bottom_margin, 70),  # Ensure at least 70px for labels
            l=current_margin.get('l', 40),
            r=current_margin.get('r', 40),
            t=current_margin.get('t', 60)
        ))
    
    # Add annotations for labels AFTER layout is set
    for annotation in label_annotations:
        fig.add_annotation(**annotation)
    
    return fig
