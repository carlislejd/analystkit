"""Style guide constants and dynamic scaling for charts and visualizations."""

import math

# ─────────────────────────────────────────────
# Color palettes
# ─────────────────────────────────────────────

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

# Color hierarchy — curated subsets for N data series.
# Designed so 1-series uses primary green, 2-series adds contrast, etc.
COLOR_HIERARCHY = {
    1: ['#45b979'],
    2: ['#45b979', '#6c6b71'],
    3: ['#45b979', '#006472', '#6c6b71'],
    4: ['#45b979', '#a7d8b5', '#006472', '#6c6b71'],
    5: ['#45b979', '#a7d8b5', '#006472', '#62a0ad', '#6c6b71'],
    6: ['#45b979', '#a7d8b5', '#006472', '#62a0ad', '#6c6b71', '#b7b6b9'],
    7: ['#45b979', '#a7d8b5', '#006472', '#62a0ad', '#6c6b71', '#b7b6b9', '#4f2984'],
    8: ['#45b979', '#a7d8b5', '#006472', '#62a0ad', '#6c6b71', '#b7b6b9', '#4f2984', '#927fb5'],
    9: ['#45b979', '#a7d8b5', '#006472', '#62a0ad', '#6c6b71', '#b7b6b9', '#4f2984', '#927fb5', '#00b6c9'],
    10: ['#45b979', '#a7d8b5', '#006472', '#62a0ad', '#6c6b71', '#b7b6b9', '#4f2984', '#927fb5', '#00b6c9', '#91d6e0'],
    11: ['#45b979', '#a7d8b5', '#006472', '#62a0ad', '#6c6b71', '#b7b6b9', '#4f2984', '#927fb5', '#00b6c9', '#91d6e0', '#f05b72'],
}

CHART_COLORS = {
    'background': '#ffffff',
    'grid': '#e6e6e6',
    'grid_dark': '#C1C8CD',
    'text': '#1B252A',
}

# ─────────────────────────────────────────────
# Font families
# ─────────────────────────────────────────────

FONT_FAMILIES = {
    'primary': 'PPNeueMontreal-Book',
    'axis': 'PPNeueMontrealMono-Variable',
    'title': 'Items-Regular',
}

# ─────────────────────────────────────────────
# Base font sizes (at reference dimensions 1200x800)
# ─────────────────────────────────────────────

# These are the "ideal" sizes at the reference resolution.
# Use compute_font_sizes() to get scaled sizes for other dimensions.
_BASE_FONT_SIZES = {
    'title': 25,
    'axis': 25,
    'legend': 25,
    'annotation': 25,
}

# Reference dimensions for font scaling calculations.
_REFERENCE_WIDTH = 1200
_REFERENCE_HEIGHT = 800

# Font scale clamp range — prevents text from becoming unreadably
# small on tiny charts or comically large on huge ones.
_FONT_SCALE_MIN = 0.55
_FONT_SCALE_MAX = 1.6


def compute_font_scale(width: int, height: int) -> float:
    """Compute a font scale factor relative to the reference dimensions.

    Uses the geometric mean of (width, height) compared to the reference
    so that both dimensions contribute. The result is clamped to keep
    text readable at extremes.

    Args:
        width: Chart width in pixels.
        height: Chart height in pixels.

    Returns:
        A multiplier (e.g. 0.7 means "70 % of base size").
    """
    ref_diag = math.sqrt(_REFERENCE_WIDTH * _REFERENCE_HEIGHT)
    cur_diag = math.sqrt(width * height)
    raw = cur_diag / ref_diag
    return max(_FONT_SCALE_MIN, min(_FONT_SCALE_MAX, raw))


def compute_font_sizes(width: int, height: int) -> dict:
    """Return a dict of font sizes scaled for the given chart dimensions.

    Args:
        width: Chart width in pixels.
        height: Chart height in pixels.

    Returns:
        Dict with keys 'title', 'axis', 'legend', 'annotation' — each
        an integer point size.
    """
    scale = compute_font_scale(width, height)
    return {k: max(8, round(v * scale)) for k, v in _BASE_FONT_SIZES.items()}


# Legacy constant — kept for backward compatibility when callers
# reference ak.FONT_SIZES directly. These are the *unscaled* base sizes.
FONT_SIZES = dict(_BASE_FONT_SIZES)

# ─────────────────────────────────────────────
# Style defaults (unscaled — apply_theme patches these dynamically)
# ─────────────────────────────────────────────

STYLE_DEFAULTS = {
    'font': {
        'family': FONT_FAMILIES['primary'],
        'size': FONT_SIZES['axis'],
        'color': CHART_COLORS['text'],
    },
    'title_font': {
        'family': FONT_FAMILIES['title'],
        'size': FONT_SIZES['title'],
        'color': CHART_COLORS['text'],
    },
    'axis_tickfont': {
        'family': FONT_FAMILIES['axis'],
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
        'showgrid': False,
        'gridwidth': 1,
        'gridcolor': CHART_COLORS['grid_dark'],
        'zeroline': False,
        'zerolinewidth': 1,
        'zerolinecolor': CHART_COLORS['grid_dark'],
        'showline': False,
        'title': None,
        'ticklen': 19,
        'tickwidth': 1,
        'tickcolor': CHART_COLORS['grid_dark'],
    },
    'xaxis': {
        'showgrid': False,
        'zeroline': False,
        'showline': False,
        'title': None,
        'tickangle': 0,
        'ticklen': 19,
        'tickwidth': 1,
        'tickcolor': CHART_COLORS['grid_dark'],
    },
    'yaxis': {
        'showgrid': True,
        'gridwidth': 1,
        'gridcolor': CHART_COLORS['grid_dark'],
        'zeroline': True,
        'zerolinewidth': 1,
        'zerolinecolor': CHART_COLORS['grid_dark'],
        'showline': False,
        'title': None,
        'ticklen': 19,
        'tickwidth': 1,
        'tickcolor': CHART_COLORS['grid_dark'],
    },
    'grid': {
        'width': 1,
    },
    'legend': {
        'borderwidth': 0,
        'bgcolor': 'rgba(0,0,0,0)',
        'orientation': "h",
        'yanchor': "bottom",
        'y': 1.02,
        'xanchor': "right",
        'x': 1,
        'title': None,
        'traceorder': 'normal',
        'font': {
            'family': FONT_FAMILIES['primary'],
            'size': FONT_SIZES['legend'],
            'color': CHART_COLORS['text'],
        },
    },
}

# ─────────────────────────────────────────────
# Margin presets
# ─────────────────────────────────────────────

MARGIN_PRESETS = {
    'minimal': {'l': 20, 'r': 20, 't': 20, 'b': 20},
    'standard': {'l': 40, 'r': 40, 't': 40, 'b': 40},
    'wide': {'l': 60, 'r': 60, 't': 60, 'b': 60},
}

# ─────────────────────────────────────────────
# Size presets (width × height in pixels)
# ─────────────────────────────────────────────

SIZE_PRESETS = {
    'full':   {'width': 1200, 'height': 800},
    'half':   {'width': 600,  'height': 400},
    '18:9':   {'width': 1728, 'height': 864},
    '3:1':    {'width': 1728, 'height': 576},
    '1:1':    {'width': 1152, 'height': 1152},
    '16:9':   {'width': 1920, 'height': 1080},
    '4:3':    {'width': 1200, 'height': 900},
    'type_a': {'width': 1275, 'height': 900},
    'type_b': {'width': 1200, 'height': 750},
    'type_c': {'width': 1800, 'height': 1050},
    'type_d': {'width': 1800, 'height': 1125},
    'type_e': {'width': 825,  'height': 975},
    'type_f': {'width': 825,  'height': 900},
}
