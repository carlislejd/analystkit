"""
AnalystKit — Bitwise brand theme and chart utilities for Plotly.

The main entry point is ``apply_theme(fig)`` which brands any Plotly
figure. Convenience wrappers like ``create_chart()`` handle common
data patterns and call ``apply_theme`` under the hood.

Chart export requires kaleido for static images (pip install kaleido).
HTML and JSON export work out of the box.
"""

from .colors import (
    BITWISE_COLORS,
    COLOR_HIERARCHY,
    CHART_COLORS,
    FONT_FAMILIES,
    FONT_SIZES,
    STYLE_DEFAULTS,
    SIZE_PRESETS,
    MARGIN_PRESETS,
    compute_font_sizes,
    compute_font_scale,
)
from .plotly_theme import apply_theme, get_color_palette
from .charts import (
    create_chart,
    create_bar_chart,
    create_line_chart,
    export_chart,
    save_chart,
    apply_range_tick_marks,
)

__version__ = "0.5.0"
__author__ = "Josh Carlisle <josh@bitwiseinvestments.com>"

__all__ = [
    # Core theme
    "apply_theme",
    "get_color_palette",

    # Chart constructors
    "create_chart",
    "create_bar_chart",
    "create_line_chart",

    # Export
    "export_chart",
    "save_chart",

    # Time-series tick marks
    "apply_range_tick_marks",

    # Colors & styling constants
    "BITWISE_COLORS",
    "COLOR_HIERARCHY",
    "CHART_COLORS",
    "FONT_FAMILIES",
    "FONT_SIZES",
    "STYLE_DEFAULTS",
    "SIZE_PRESETS",
    "MARGIN_PRESETS",

    # Dynamic font scaling
    "compute_font_sizes",
    "compute_font_scale",
]
