"""Style guide constants for charts and visualizations."""

# Color palettes
BITWISE_COLORS = [
    '#45b979',  # Green
    '#a7d8b5',  # Light green
    '#006472',  # Dark teal
    '#62a0ad',  # Light teal
    '#6c6b71',  # Dark grey
    '#b7b6b9',  # Light grey
    '#4f2984',  # Purple
    '#927fb5',  # Light purple
    '#00b6c9',  # Turquoise
    '#91d6e0',  # Light turquoise
    '#f05b72',  # Red
]

# Color hierarchy for different numbers of items
COLOR_HIERARCHY = {
    1: ['#45b979'],  # Green
    2: ['#45b979', '#6c6b71'],  # Green, Dark grey
    3: ['#45b979', '#006472', '#6c6b71'],  # Green, Dark teal, Dark grey
    4: ['#45b979', '#a7d8b5', '#006472', '#6c6b71'],  # Green, Light green, Dark teal, Dark grey
    5: ['#45b979', '#a7d8b5', '#006472', '#62a0ad', '#6c6b71'],  # Green, Light green, Dark teal, Light teal, Dark grey
    6: ['#45b979', '#a7d8b5', '#006472', '#62a0ad', '#6c6b71', '#b7b6b9'],  # Green, Light green, Dark teal, Light teal, Dark grey, Light grey
    7: ['#45b979', '#a7d8b5', '#006472', '#62a0ad', '#6c6b71', '#b7b6b9', '#4f2984'],  # Green, Light green, Dark teal, Light teal, Dark grey, Light grey, Purple
    8: ['#45b979', '#a7d8b5', '#006472', '#62a0ad', '#6c6b71', '#b7b6b9', '#4f2984', '#927fb5'],  # Green, Light green, Dark teal, Light teal, Dark grey, Light grey, Purple, Light purple
    9: ['#45b979', '#a7d8b5', '#006472', '#62a0ad', '#6c6b71', '#b7b6b9', '#4f2984', '#927fb5', '#00b6c9'],  # Green, Light green, Dark teal, Light teal, Dark grey, Light grey, Purple, Light purple, Turquoise
    10: ['#45b979', '#a7d8b5', '#006472', '#62a0ad', '#6c6b71', '#b7b6b9', '#4f2984', '#927fb5', '#00b6c9', '#91d6e0'],  # Green, Light green, Dark teal, Light teal, Dark grey, Light grey, Purple, Light purple, Turquoise, Light turquoise
    11: ['#45b979', '#a7d8b5', '#006472', '#62a0ad', '#6c6b71', '#b7b6b9', '#4f2984', '#927fb5', '#00b6c9', '#91d6e0', '#f05b72'],  # Green, Light green, Dark teal, Light teal, Dark grey, Light grey, Purple, Light purple, Turquoise, Light turquoise, Red
}

CHART_COLORS = {
    'background': '#ffffff',
    'grid': '#e6e6e6',
    'grid_dark': '#C1C8CD',  # Light gray for axis lines and tick marks
    'text': '#1B252A',  # Dark gray for all text
}

# Font families
FONT_FAMILIES = {
    'primary': 'PPNeueMontreal-Regular',
    'title': 'Items-Regular',
}

# Font sizes - 6 pt / 25 px for all text
FONT_SIZES = {
    'title': 25,
    'axis': 25,
    'legend': 25,
    'annotation': 25,
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
        'family': FONT_FAMILIES['primary'],  # PPNeueMontreal-Regular for all text except title
        'size': FONT_SIZES['axis'],
        'color': CHART_COLORS['text'],
    },
    'title_font': {
        'family': FONT_FAMILIES['title'],  # Items-Regular for chart titles only
        'size': FONT_SIZES['title'],
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
        'gridwidth': 1,  # 0.25 pt / 1 px
        'gridcolor': CHART_COLORS['grid_dark'],
        'zeroline': False,  # No zero line by default
        'zerolinewidth': 1,  # 0.25 pt / 1 px
        'zerolinecolor': CHART_COLORS['grid_dark'],
        'showline': False,  # Remove border lines around plot area
        'title': None,  # No axis titles by default
        'ticklen': 19,  # 0.0625 in / 19 px tick mark height
        'tickwidth': 1,  # 0.25 pt / 1 px tick mark width
        'tickcolor': CHART_COLORS['grid_dark'],
    },
    'xaxis': {
        'showgrid': False,  # No x-axis vertical lines
        'zeroline': False,
        'showline': False,
        'title': None,
        'tickangle': 0,  # Default to horizontal labels
        'ticklen': 19,  # 0.0625 in / 19 px tick mark height
        'tickwidth': 1,  # 0.25 pt / 1 px tick mark width
        'tickcolor': CHART_COLORS['grid_dark'],
    },
    'yaxis': {
        'showgrid': True,  # Keep y-axis horizontal lines
        'gridwidth': 1,  # 0.25 pt / 1 px
        'gridcolor': CHART_COLORS['grid_dark'],
        'zeroline': True,  # Keep y-axis zero line
        'zerolinewidth': 1,  # 0.25 pt / 1 px
        'zerolinecolor': CHART_COLORS['grid_dark'],
        'showline': False,
        'title': None,
        'ticklen': 19,  # 0.0625 in / 19 px tick mark height
        'tickwidth': 1,  # 0.25 pt / 1 px tick mark width
        'tickcolor': CHART_COLORS['grid_dark'],
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
            'family': FONT_FAMILIES['primary'],  # PPNeueMontreal-Regular
            'size': FONT_SIZES['legend'],
            'color': CHART_COLORS['text'],
        },
    },
}

# Margin presets
MARGIN_PRESETS = {
    'minimal': {
        'l': 20,
        'r': 20,
        't': 20,
        'b': 20,
    },
    'standard': {
        'l': 40,
        'r': 40,
        't': 40,
        'b': 40,
    },
    'wide': {
        'l': 60,
        'r': 60,
        't': 60,
        'b': 60,
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
    'type_a': {
        'width': 1275,  # 4.25x3
        'height': 900,
    },
    'type_b': {
        'width': 1200,  # 4x2.5
        'height': 750,
    },
    'type_c': {
        'width': 1800,  # 6x3.5
        'height': 1050,
    },
    'type_d': {
        'width': 1800,  # 6x3.75
        'height': 1125,
    },
    'type_e': {
        'width': 825,   # 2.75x3.25
        'height': 975,
    },
    'type_f': {
        'width': 825,   # 2.75x3
        'height': 900,
    },
}

EXPORT_CONFIG = {
    'format': 'svg',
    'width': SIZE_PRESETS['full']['width'],
    'height': SIZE_PRESETS['full']['height'],
    'scale': 2
}
