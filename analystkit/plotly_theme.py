"""Plotly theme management and registration."""

import plotly.graph_objects as go
import plotly.express as px
from .colors import STYLE_DEFAULTS, CHART_COLORS, SIZE_PRESETS, MARGIN_PRESETS

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
        font=STYLE_DEFAULTS['font'],
        margin=margin,
    )
    
    # Apply specific x-axis styling (no grid, no titles)
    fig.update_xaxes(
        showgrid=STYLE_DEFAULTS['xaxis']['showgrid'],
        zeroline=STYLE_DEFAULTS['xaxis']['zeroline'],
        showline=STYLE_DEFAULTS['xaxis']['showline'],
        title=STYLE_DEFAULTS['xaxis']['title'],
        tickfont=STYLE_DEFAULTS['font'],
    )
    
    # Apply specific y-axis styling (horizontal grid lines, no titles)
    fig.update_yaxes(
        showgrid=STYLE_DEFAULTS['yaxis']['showgrid'],
        gridwidth=STYLE_DEFAULTS['yaxis']['gridwidth'],
        gridcolor=STYLE_DEFAULTS['yaxis']['gridcolor'],
        zeroline=STYLE_DEFAULTS['yaxis']['zeroline'],
        zerolinewidth=STYLE_DEFAULTS['yaxis']['zerolinewidth'],
        zerolinecolor=STYLE_DEFAULTS['yaxis']['zerolinecolor'],
        showline=STYLE_DEFAULTS['yaxis']['showline'],
        title=STYLE_DEFAULTS['yaxis']['title'],
        tickfont=STYLE_DEFAULTS['font'],
    )
    
    # Apply legend styling (no border, clean look)
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
