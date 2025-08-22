"""Common chart wrapper functions for creating styled charts."""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Union
from .plotly_theme import apply_theme, get_color_palette
from .colors import SIZE_PRESETS

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
    
    # Update labels
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
    
    # Update labels
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
    
    # Update labels
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
    
    # Apply color hierarchy if no custom colors specified
    if 'color_discrete_sequence' not in kwargs and 'color' not in kwargs:
        from .plotly_theme import get_color_palette
        if color_column:
            unique_values = data[color_column].nunique() if hasattr(data, 'nunique') else len(set(data[color_column]))
            colors = get_color_palette(unique_values)
            fig.update_traces(marker_color=colors)
    
    # Update labels
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
    """
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
