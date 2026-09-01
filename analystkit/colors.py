"""Style guide constants and dynamic scaling for charts and visualizations.

Colour follows the DS – Charts rules (Audrey, 25 Aug 2026).
Authority: ~/Claude/AudreyVault/DS-Charts-Rules.md
Sibling implementation: ~/Claude/report-chart-builder/index.template.html (`ROLES`, `SEQ`).
"""

import math
import re

# ─────────────────────────────────────────────
# Color palette — REPORT context
# ─────────────────────────────────────────────

# These are the REPORT values, sampled from the printed Q3 2025 review.
#
# They are deliberately NOT the Social values. The two palettes diverge on purpose —
# ink on paper versus screen — and must never be unified. Social green is #67B77E
# against Report's #45B979, Social aqua #2DB3C6 against Report's #00B7C9. If this
# module ever needs to serve social assets, that palette gets its own dict; it does
# not get merged into this one.
#
# Twelve roles: five base inks, their 50% tints, black, and three greys. Only six are
# independent — the tints should ultimately derive from their base ink rather than be
# hand-entered, so a corrected base does not silently leave its tints wrong.
REPORT_COLORS = {
    'green':        '#45B979',
    'green-light':  '#A7D7B5',
    'teal-dark':    '#006472',
    'teal-light':   '#62A0AD',
    'purple-dark':  '#4F2A84',
    'purple-light': '#927FB5',
    'aqua':         '#00B7C9',
    'aqua-light':   '#A0D4DE',  # provisional — no print source yet
    'grey':         '#6C6C71',
    'grey-light':   '#B7B6B9',  # provisional
    'grey-dark':    '#24272E',  # provisional
    'black':        '#111921',
    'bitwise':      '#111921',  # semantic role, see bitwise_color_for()
}

# The full ramp in palette order. Families enter Green, Teal, Purple, Aqua, then the
# neutrals; within a family, dark before light. This is the 10+ series sequence and
# the canonical reading order of the palette — it excludes grey-dark (short sequences
# only) and black (the Bitwise role, which takes no palette slot).
PALETTE_ORDER = [
    'green', 'green-light', 'teal-dark', 'teal-light',
    'purple-dark', 'purple-light', 'aqua', 'aqua-light',
    'grey', 'grey-light',
]

BITWISE_COLORS = [REPORT_COLORS[role] for role in PALETTE_ORDER]

# Series colour is assigned by LEGEND COUNT, never picked freely. Two regimes that do
# not overlap: one to nine run the short sequences, which always end on a grey so no
# chart is ever all-colour; ten or more abandon that for the full ramp, which already
# ends on two greys of its own.
_SHORT_SEQUENCES = {
    1: ['green'],
    2: ['green', 'grey-dark'],
    3: ['green', 'teal-dark', 'grey-dark'],
    4: ['green', 'green-light', 'teal-dark', 'grey-dark'],
    5: ['green', 'green-light', 'teal-dark', 'teal-light', 'grey-dark'],
    6: ['green', 'green-light', 'teal-dark', 'teal-light', 'grey-dark', 'grey'],
    7: ['green', 'green-light', 'teal-dark', 'teal-light', 'purple-dark', 'grey-dark', 'grey'],
    8: ['green', 'green-light', 'teal-dark', 'teal-light', 'purple-dark', 'purple-light',
        'grey-dark', 'grey'],
    9: ['green', 'green-light', 'teal-dark', 'teal-light', 'purple-dark', 'purple-light',
        'aqua', 'grey-dark', 'grey'],
}


def sequence_for(n: int) -> list:
    """Return the ROLE NAMES for a chart with n legend items.

    One to nine take the matching short sequence whole — you take the row for your
    count, you do not slice a longer one. Ten or more run the full ramp in palette
    order, wrapping if the chart somehow exceeds ten.

    Args:
        n: Number of legend items (excluding any Bitwise product line, which does
           not consume a palette slot).

    Returns:
        List of n role names, keys into REPORT_COLORS.
    """
    if n <= 0:
        return []
    if n <= 9:
        return list(_SHORT_SEQUENCES[n])
    return [PALETTE_ORDER[i % len(PALETTE_ORDER)] for i in range(n)]


def colors_for(n: int) -> list:
    """Return the hex colours for a chart with n legend items.

    Args:
        n: Number of legend items.

    Returns:
        List of n hex strings.
    """
    return [REPORT_COLORS[role] for role in sequence_for(n)]


# Prebuilt hex sequences by legend count, for callers that want a lookup rather than
# a call. Generated from sequence_for() so the two can never drift apart.
COLOR_HIERARCHY = {n: colors_for(n) for n in range(1, 13)}

# ─────────────────────────────────────────────
# The Bitwise product line
# ─────────────────────────────────────────────

# A Bitwise product (e.g. "Bitwise 10 Large Cap Crypto Index") is black and bold in
# the legend — a semantic role, not a series slot. It sits at whatever rank its data
# lands on rather than leading, and it does NOT consume a palette position: every
# other series is coloured as if it were not on the chart.
_BITWISE_NAME = re.compile(r'^bitwise\b', re.IGNORECASE)


def is_bitwise(name) -> bool:
    """True if a series name identifies a Bitwise product line."""
    return bool(_BITWISE_NAME.match(str(name or '').strip()))


def colors_for_series(names) -> list:
    """Map series names to hex colours, honouring the Bitwise role.

    Bitwise rows take black and are skipped when counting legend items, so a chart
    with five series one of which is Bitwise uses the four-series sequence.

    Args:
        names: Iterable of series names, in the order they appear in the legend.

    Returns:
        List of hex strings, parallel to `names`.
    """
    names = list(names)
    seq = sequence_for(sum(1 for s in names if not is_bitwise(s)))
    out, k = [], 0
    for s in names:
        if is_bitwise(s):
            out.append(REPORT_COLORS['bitwise'])
        else:
            out.append(REPORT_COLORS[seq[k]] if k < len(seq) else REPORT_COLORS['grey'])
            k += 1
    return out


# Legend rows for the Bitwise line are bold — name and value both. Every other row
# stays regular. Hand-applying this is how it ends up half-applied across a report.
BITWISE_LEGEND_WEIGHT = 'bold'
DEFAULT_LEGEND_WEIGHT = 'normal'

# ─────────────────────────────────────────────
# Highlight one bar
# ─────────────────────────────────────────────


def highlight_colors(n: int, subject_index: int) -> list:
    """Colours for a ranked single-series bar chart with one highlighted bar.

    The subject is Green and every other bar is Dark Grey — the two-item sequence
    applied to "subject versus everyone else", which is why it reuses those two
    colours rather than introducing an emphasis colour of its own.

    Args:
        n: Total number of bars.
        subject_index: Index of the bar to highlight.

    Returns:
        List of n hex strings.
    """
    return [REPORT_COLORS['green'] if i == subject_index else REPORT_COLORS['grey-dark']
            for i in range(n)]


# ─────────────────────────────────────────────
# Opacity
# ─────────────────────────────────────────────

# Marks on the plot render at 80% so gridlines read through; a legend swatch has
# nothing behind it to reveal and shows the true ink at 100%. Confirmed by measuring
# swatch against fill on a stacked bar chart, and it holds for areas too.
SERIES_OPACITY = 0.8
LEGEND_SWATCH_OPACITY = 1.0


def to_rgba(hex_color: str, alpha: float = SERIES_OPACITY) -> str:
    """Convert a hex colour to an ``rgba()`` string at the given alpha.

    Args:
        hex_color: Colour as ``#RRGGBB`` (or ``#RGB``).
        alpha: Alpha channel, 0.0–1.0. Defaults to the 80% plot opacity.

    Returns:
        An ``rgba(r,g,b,a)`` string.
    """
    h = hex_color.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return f'rgba({r},{g},{b},{alpha})'


# ─────────────────────────────────────────────
# Semantic colours — NOT series colours
# ─────────────────────────────────────────────

# Red is not one of the twelve palette roles and must never be handed out as a series
# colour by the sequences above. It is kept here as a named role for the cases where
# a chart genuinely encodes loss or alarm. Introducing it to a series chart is a
# palette conversation, not a code one.
SEMANTIC_COLORS = {
    'negative': '#F05B72',
}

CHART_COLORS = {
    'background': '#ffffff',
    # NOTE: the DS – Charts rules put the axis at #C8C9CB and the gridline at #E3E3E4,
    # both deliberately neutral rather than off the blue-cast Slate ramp, with body
    # ink at #111921. The values below predate that and are left as-is by request —
    # this pass was scoped to the palette and the legend sequences only.
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
