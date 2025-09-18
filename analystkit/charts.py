"""Common chart wrapper functions for creating styled charts."""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Union
from .plotly_theme import apply_theme, get_color_palette
from .colors import SIZE_PRESETS, COLOR_HIERARCHY

def create_bar_chart(
    data: Union[pd.DataFrame, List, Dict],
    x: Optional[str] = None,
    y: Optional[str] = None,
    x_label: str = "",
    y_label: str = "",
    color_column: Optional[str] = None,
    orientation: str = "v",
    size_preset: str = "full",
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
            fig.update_traces(marker_color=colors, line_color=colors)
        else:
            # For single series, use primary Bitwise color
            fig.update_traces(marker_color=COLOR_HIERARCHY[1][0], line_color=COLOR_HIERARCHY[1][0])
    
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
    png_scale: int = 4
) -> Dict[str, str]:
    """Save a chart in multiple formats with consistent aspect ratios.
    
    This function automatically exports charts in SVG and PNG formats with
    predefined aspect ratios, making it easy to maintain consistent sizing
    across all visualizations.
    
    Args:
        fig: Plotly figure to save
        title: Chart title (used for filename)
        output_dir: Directory to save files (default: "design")
        aspect_ratio: Aspect ratio for exports ("18:9" or "1:1")
        include_svg: Whether to export SVG format (default: True)
        include_png: Whether to export PNG format (default: True)
        include_1x1: Whether to also export 1:1 ratio versions (default: False)
        png_scale: Scale factor for PNG exports (default: 4 for high quality)
    
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
        "1:1": {"width": 12 * 96, "height": 12 * 96},  # 1152x1152
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
