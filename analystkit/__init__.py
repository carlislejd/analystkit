"""
AnalystKit - Shared Plotly theme, visualization helpers, and settings for analytics projects.

A comprehensive package providing consistent styling, color palettes, and chart utilities
for creating professional visualizations with Plotly.

Note: Chart export functionality requires kaleido (install with: poetry add --group export kaleido)
"""

from .colors import (
    BITWISE_COLORS,
    COLOR_HIERARCHY,
    CHART_COLORS,
    FONT_FAMILIES,
    FONT_SIZES,
    STYLE_DEFAULTS,
    SIZE_PRESETS,
    EXPORT_CONFIG
)
from .plotly_theme import register_theme, apply_theme, get_color_palette
from .formats import format_number, format_percentage, format_currency, format_date
from .charts import create_bar_chart, create_line_chart, create_scatter_chart, export_chart
from .settings import Settings, load_settings, create_env_template
from .assets import (
    fetch_crypto_history,
    fetch_index_history,
    get_crypto_dataframe,
    get_index_dataframe,
    list_available_cryptos,
    list_available_indices
)

__version__ = "0.1.3"
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
    "EXPORT_CONFIG",
    
    # Theme management
    "register_theme",
    "apply_theme",
    "get_color_palette",
    
    # Formatting utilities
    "format_number",
    "format_percentage", 
    "format_currency",
    "format_date",
    
    # Chart helpers
    "create_bar_chart",
    "create_line_chart",
    "create_scatter_chart",
    "export_chart",
    
    # Settings
    "Settings",
    "load_settings",
    "create_env_template",
    
    # Asset data
    "fetch_crypto_history",
    "fetch_index_history", 
    "get_crypto_dataframe",
    "get_index_dataframe",
    "list_available_cryptos",
    "list_available_indices",
]
