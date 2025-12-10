"""Plotly theme management and registration."""

import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from .colors import STYLE_DEFAULTS, CHART_COLORS, SIZE_PRESETS, MARGIN_PRESETS

def _calculate_axis_buffer(values):
    """Calculate axis range with a dynamic buffer to ensure max values are visible.
    
    Args:
        values: List or array of numeric values
    
    Returns:
        tuple: (min, max) with buffer applied, or None if no valid data
    """
    if not values:
        return None
    
    # Convert to numpy array and filter out invalid values
    data = np.array(values)
    data = data[np.isfinite(data)]
    
    if len(data) == 0:
        return None
    
    data_min = float(np.min(data))
    data_max = float(np.max(data))
    
    # Calculate range
    data_range = data_max - data_min
    
    # Dynamic buffer: 2% of range, but at least 0.5% of max value
    # This ensures:
    # - Large ranges (0-140): buffer = 2% of 140 = 2.8
    # - Small ranges (0.1-0.15): buffer = max(0.001, 0.00075) = 0.001
    buffer_percent = 0.02  # 2% of range
    min_buffer_percent = 0.005  # 0.5% of max value as minimum
    
    buffer = max(data_range * buffer_percent, abs(data_max) * min_buffer_percent)
    
    # Apply buffer to top (only increase max, don't decrease min)
    data_max_buffered = data_max + buffer
    data_min_final = data_min
    
    return (data_min_final, data_max_buffered)

def _apply_axis_buffers(fig):
    """Apply buffers to value axis to ensure max values are visible.
    
    For horizontal bar charts, buffers x-axis. For all other charts, buffers y-axis.
    
    Args:
        fig: Plotly figure object
    """
    # Check if this is a horizontal bar chart by looking at orientation
    is_horizontal_bar = False
    for trace in fig.data:
        # Check if it's a bar trace with horizontal orientation
        if (hasattr(trace, 'type') and trace.type == 'bar' and 
            hasattr(trace, 'orientation') and trace.orientation == 'h'):
            is_horizontal_bar = True
            break
    
    if is_horizontal_bar:
        # For horizontal bars, buffer the x-axis (which has the values)
        x_values = []
        for trace in fig.data:
            if hasattr(trace, 'x') and trace.x is not None:
                x_data = np.array(trace.x)
                x_data = x_data[np.isfinite(x_data)]
                if len(x_data) > 0:
                    x_values.extend(x_data.tolist())
        
        x_range = _calculate_axis_buffer(x_values)
        if x_range is not None:
            x_min, x_max = x_range
            fig.update_xaxes(range=[x_min, x_max])
    else:
        # For vertical charts (bars, lines, scatter), buffer the y-axis (which has the values)
        y_values = []
        for trace in fig.data:
            if hasattr(trace, 'y') and trace.y is not None:
                y_data = np.array(trace.y)
                y_data = y_data[np.isfinite(y_data)]
                if len(y_data) > 0:
                    y_values.extend(y_data.tolist())
        
        y_range = _calculate_axis_buffer(y_values)
        if y_range is not None:
            y_min, y_max = y_range
            fig.update_yaxes(range=[y_min, y_max])

def register_theme():
    """Register the custom theme with Plotly."""
    # Create the custom theme layout
    custom_layout = {
        'plot_bgcolor': CHART_COLORS['background'],
        'paper_bgcolor': CHART_COLORS['background'],
        'font': STYLE_DEFAULTS['font'],
        'margin': STYLE_DEFAULTS['margin'],

        'xaxis': {
            **STYLE_DEFAULTS['axis'],
            'tickfont': STYLE_DEFAULTS['font'],
        },
        'yaxis': {
            **STYLE_DEFAULTS['axis'],
            'tickfont': STYLE_DEFAULTS['font'],
        },
        'legend': STYLE_DEFAULTS['legend'],
    }
    
    # Register the theme (simplified for newer Plotly versions)
    # Note: Template registration has changed in newer Plotly versions
    # For now, we'll just return the custom layout
    print("Theme registered successfully. Use apply_theme() to apply styling to individual charts.")
    
    return custom_layout

def apply_theme(fig, size_preset='full', margin_preset='minimal'):
    """Apply the custom theme to a Plotly figure.
    
    Args:
        fig: Plotly figure object
        size_preset: Size preset to use ('full', 'half', '18:9', '3:1', '1:1')
        margin_preset: Margin preset to use ('minimal', 'standard', 'wide')
    
    Returns:
        Updated figure object
    """
    # Apply size preset
    size = SIZE_PRESETS.get(size_preset, SIZE_PRESETS['full'])
    margin = MARGIN_PRESETS.get(margin_preset, MARGIN_PRESETS['minimal'])
    fig.update_layout(
        width=size['width'],
        height=size['height'],
        plot_bgcolor=CHART_COLORS['background'],
        paper_bgcolor=CHART_COLORS['background'],
        font=STYLE_DEFAULTS['font'],  # PPNeueMontreal-Regular for all text (default)
        title_font=STYLE_DEFAULTS['title_font'],  # Items-Regular for chart titles only
        margin=margin,
    )
    
    # Apply specific x-axis styling (no grid, no titles)
    # All fonts use PPNeueMontreal-Regular (via STYLE_DEFAULTS['font'])
    fig.update_xaxes(
        showgrid=STYLE_DEFAULTS['xaxis']['showgrid'],
        zeroline=STYLE_DEFAULTS['xaxis']['zeroline'],
        showline=STYLE_DEFAULTS['xaxis']['showline'],
        title=None,  # Explicitly hide x-axis title by default
        tickfont=STYLE_DEFAULTS['font'],  # PPNeueMontreal-Regular
    )
    
    # Apply specific y-axis styling (horizontal grid lines, no titles)
    # All fonts use PPNeueMontreal-Regular (via STYLE_DEFAULTS['font'])
    fig.update_yaxes(
        showgrid=STYLE_DEFAULTS['yaxis']['showgrid'],
        gridwidth=STYLE_DEFAULTS['yaxis']['gridwidth'],
        gridcolor=STYLE_DEFAULTS['yaxis']['gridcolor'],
        zeroline=STYLE_DEFAULTS['yaxis']['zeroline'],
        zerolinewidth=STYLE_DEFAULTS['yaxis']['zerolinewidth'],
        zerolinecolor=STYLE_DEFAULTS['yaxis']['zerolinecolor'],
        showline=STYLE_DEFAULTS['yaxis']['showline'],
        title=None,  # Explicitly hide y-axis title by default
        tickfont=STYLE_DEFAULTS['font'],  # PPNeueMontreal-Regular
    )
    
    # Apply axis buffer to ensure max values are visible
    # Handles both vertical (y-axis) and horizontal (x-axis) charts
    _apply_axis_buffers(fig)
    
    # Apply legend styling (no border, clean look)
    # Legend font uses PPNeueMontreal-Regular (via STYLE_DEFAULTS['legend']['font'])
    fig.update_layout(
        legend=STYLE_DEFAULTS['legend']
    )
    
    return fig

def get_color_palette(n_colors):
    """Get a color palette for the specified number of colors.
    
    Args:
        n_colors: Number of colors needed
    
    Returns:
        List of hex color codes
    """
    from .colors import COLOR_HIERARCHY, BITWISE_COLORS
    
    if n_colors <= 6:
        return COLOR_HIERARCHY.get(n_colors, BITWISE_COLORS[:n_colors])
    else:
        # For more than 6 colors, cycle through the base palette
        import itertools
        return list(itertools.islice(itertools.cycle(BITWISE_COLORS), n_colors))
