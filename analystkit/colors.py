"""Style guide constants for charts and visualizations."""

# Color palettes
BITWISE_COLORS = [
    '#66b77d',  # Green
    '#b1d6b7',  # Light green
    '#2c6271',  # Dark turquoise
    '#719eab',  # Light turquoise
    '#45454b',  # Dark grey
    '#838287',  # Light grey
]

# Color hierarchy for different numbers of items
COLOR_HIERARCHY = {
    1: ['#66b77d'],  # Green
    2: ['#66b77d', '#45454b'],  # Green, Dark grey
    3: ['#66b77d', '#2c6271', '#45454b'],  # Green, Dark turquoise, Dark grey
    4: ['#66b77d', '#b1d6b7', '#2c6271', '#45454b'],  # Green, Light green, Dark turquoise, Dark grey
    5: ['#66b77d', '#b1d6b7', '#2c6271', '#719eab', '#45454b'],  # Green, Light green, Dark turquoise, Light turquoise, Dark grey
    6: ['#66b77d', '#b1d6b7', '#2c6271', '#719eab', '#45454b', '#838287'],  # Green, Light green, Dark turquoise, Light turquoise, Dark grey, Light grey
}

CHART_COLORS = {
    'background': '#ffffff',
    'grid': '#e6e6e6',
    'grid_dark': '#cccccc',  # Darker grid color for visible tick marks and grid lines
    'text': '#333333',
}

# Font families
FONT_FAMILIES = {
    'primary': 'PP Neue Montreal Book',
    'title': 'Items Regular',
}

# Font sizes (increased by 20%)
FONT_SIZES = {
    'title': 19,
    'axis': 19,
    'legend': 19,
    'annotation': 14,
}

# Opacity settings
OPACITY = {
    'bars': 0.9,
    'lines': 0.8,
    'markers': 0.7,
    'areas': 0.6,
    'background': 1.0,
}

# Style defaults
STYLE_DEFAULTS = {
    'font': {
        'family': FONT_FAMILIES['primary'],
        'size': FONT_SIZES['axis'],
        'color': CHART_COLORS['text'],
    },
    'margin': {
        'l': 20,
        'r': 20,
        't': 20,
        'b': 20,
    },
    'axis': {
        'showgrid': False,  # No grid by default
        'gridwidth': 1,
        'gridcolor': CHART_COLORS['grid_dark'],
        'zeroline': False,  # No zero line by default
        'zerolinewidth': 1,
        'zerolinecolor': CHART_COLORS['grid'],
        'showline': False,  # Remove border lines around plot area
        'title': None,  # No axis titles by default
    },
    'xaxis': {
        'showgrid': False,  # No x-axis vertical lines
        'zeroline': False,
        'showline': False,
        'title': None,
        'tickangle': 0,  # Default to horizontal labels
    },
    'yaxis': {
        'showgrid': True,  # Keep y-axis horizontal lines
        'gridwidth': 1,
        'gridcolor': CHART_COLORS['grid_dark'],
        'zeroline': True,  # Keep y-axis zero line
        'zerolinewidth': 1,
        'zerolinecolor': CHART_COLORS['grid'],
        'showline': False,
        'title': None,
    },
    'grid': {
        'width': 1,
    },
    'legend': {
        'borderwidth': 0,  # Remove legend border
        'bgcolor': 'rgba(0,0,0,0)',  # Transparent background
        'orientation': "h",  # Horizontal legend
        'yanchor': "bottom",  # Anchor to bottom
        'y': 1.02,  # Position above chart
        'xanchor': "right",  # Anchor to right
        'x': 1,  # Position at right edge
        'title': None,  # Hide legend title
        'font': {
            'family': FONT_FAMILIES['primary'],
            'size': FONT_SIZES['legend'],
            'color': CHART_COLORS['text'],
        },
    },
}

# Margin presets
MARGIN_PRESETS = {
    'minimal': {
        'l': 40,
        'r': 40,
        't': 40,
        'b': 40,
    },
    'standard': {
        'l': 60,
        'r': 60,
        't': 60,
        'b': 60,
    },
    'wide': {
        'l': 80,
        'r': 80,
        't': 80,
        'b': 80,
    },
}

# Size presets
SIZE_PRESETS = {
    'full': {
        'width': 1200,
        'height': 800,
    },
    'half': {
        'width': 600,
        'height': 400,
    },
    '18:9': {
        'width': 18 * 96,  # 1728px
        'height': 9 * 96,  # 864px
    },
    '3:1': {
        'width': 18 * 96,  # 1728px
        'height': 6 * 96,  # 576px
    },
    '1:1': {
        'width': 12 * 96,  # 1152px
        'height': 12 * 96,  # 1152px
    },
}

EXPORT_CONFIG = {
    'format': 'svg',
    'width': SIZE_PRESETS['full']['width'],
    'height': SIZE_PRESETS['full']['height'],
    'scale': 2
}
