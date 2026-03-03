"""
AnalystKit - Shared Plotly theme, visualization helpers, and chart utilities for analytics projects.

Chart export requires kaleido (install with: pip install kaleido)
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
)
from .plotly_theme import apply_theme, get_color_palette
from .charts import create_bar_chart, create_line_chart, export_chart, save_chart, apply_range_tick_marks

__version__ = "0.4.0"
__author__ = "Josh Carlisle <josh@bitwiseinvestments.com>"

__all__ = [
    # Colors and styling
    "BITWISE_COLORS",
    "COLOR_HIERARCHY",
    "CHART_COLORS",
    "FONT_FAMILIES",
    "FONT_SIZES",
    "STYLE_DEFAULTS",
    "SIZE_PRESETS",
    "MARGIN_PRESETS",

    # Theme
    "apply_theme",
    "get_color_palette",

    # Charts
    "create_bar_chart",
    "create_line_chart",
    "export_chart",
    "save_chart",
    "apply_range_tick_marks",
]
