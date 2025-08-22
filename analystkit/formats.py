"""Number and date formatting utilities."""

import locale
from typing import Union, Optional
from datetime import datetime, date

def format_number(
    value: Union[int, float], 
    decimals: int = 0, 
    thousands_sep: str = ",", 
    decimal_sep: str = ".",
    prefix: str = "",
    suffix: str = ""
) -> str:
    """Format a number with custom decimal places and separators.
    
    Args:
        value: Number to format
        decimals: Number of decimal places
        thousands_sep: Thousands separator
        decimal_sep: Decimal separator
        prefix: Prefix to add before the number
        suffix: Suffix to add after the number
    
    Returns:
        Formatted number string
    """
    if value is None:
        return ""
    
    # Handle negative numbers
    is_negative = value < 0
    abs_value = abs(value)
    
    # Format the number
    if decimals == 0:
        formatted = f"{int(abs_value):,}".replace(",", thousands_sep)
    else:
        formatted = f"{abs_value:.{decimals}f}".replace(",", thousands_sep)
        if decimal_sep != ".":
            formatted = formatted.replace(".", decimal_sep)
    
    # Add separators
    if thousands_sep:
        parts = formatted.split(decimal_sep if decimal_sep != "." else ".")[0]
        if len(parts) > 3:
            formatted = formatted.replace(parts, f"{int(parts):,}".replace(",", thousands_sep))
    
    # Add prefix, suffix, and sign
    result = f"{prefix}{formatted}{suffix}"
    if is_negative:
        result = f"-{result}"
    
    return result

def format_percentage(
    value: Union[int, float], 
    decimals: int = 1, 
    multiply_by_100: bool = True,
    prefix: str = "",
    suffix: str = "%"
) -> str:
    """Format a number as a percentage.
    
    Args:
        value: Number to format (0.05 for 5%)
        decimals: Number of decimal places
        multiply_by_100: Whether to multiply by 100 (True for 0.05 -> 5%, False for 5 -> 5%)
        prefix: Prefix to add before the number
        suffix: Suffix to add after the number
    
    Returns:
        Formatted percentage string
    """
    if value is None:
        return ""
    
    if multiply_by_100:
        value = value * 100
    
    return format_number(value, decimals, prefix=prefix, suffix=suffix)

def format_currency(
    value: Union[int, float], 
    currency: str = "USD", 
    decimals: int = 2,
    thousands_sep: str = ",",
    decimal_sep: str = "."
) -> str:
    """Format a number as currency.
    
    Args:
        value: Number to format
        currency: Currency code (USD, EUR, GBP, etc.)
        decimals: Number of decimal places
        thousands_sep: Thousands separator
        decimal_sep: Decimal separator
    
    Returns:
        Formatted currency string
    """
    if value is None:
        return ""
    
    # Currency symbols
    currency_symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥",
        "CAD": "C$",
        "AUD": "A$",
        "CHF": "CHF",
        "CNY": "¥",
    }
    
    symbol = currency_symbols.get(currency, currency)
    
    return format_number(
        value, 
        decimals=decimals, 
        thousands_sep=thousands_sep, 
        decimal_sep=decimal_sep,
        prefix=symbol
    )

def format_date(
    date_obj: Union[datetime, date, str], 
    format_str: str = "%Y-%m-%d",
    locale_name: Optional[str] = None
) -> str:
    """Format a date object or string.
    
    Args:
        date_obj: Date object, datetime object, or date string
        format_str: Format string (e.g., "%Y-%m-%d", "%B %d, %Y")
        locale_name: Locale for localized formatting (e.g., "en_US", "de_DE")
    
    Returns:
        Formatted date string
    """
    if date_obj is None:
        return ""
    
    # Convert string to datetime if needed
    if isinstance(date_obj, str):
        try:
            # Try common date formats
            for fmt in ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S"]:
                try:
                    date_obj = datetime.strptime(date_obj, fmt)
                    break
                except ValueError:
                    continue
            else:
                raise ValueError(f"Could not parse date string: {date_obj}")
        except ValueError:
            return str(date_obj)
    
    # Set locale if specified
    if locale_name:
        try:
            locale.setlocale(locale.LC_TIME, locale_name)
        except locale.Error:
            pass  # Fall back to default locale
    
    try:
        return date_obj.strftime(format_str)
    except (AttributeError, ValueError):
        return str(date_obj)

def format_abbreviated_number(value: Union[int, float], decimals: int = 1) -> str:
    """Format large numbers with abbreviations (K, M, B, T).
    
    Args:
        value: Number to format
        decimals: Number of decimal places for abbreviated values
    
    Returns:
        Formatted abbreviated number string
    """
    if value is None:
        return ""
    
    if abs(value) < 1000:
        return format_number(value, decimals=0)
    elif abs(value) < 1000000:
        return f"{value/1000:.{decimals}f}K"
    elif abs(value) < 1000000000:
        return f"{value/1000000:.{decimals}f}M"
    elif abs(value) < 1000000000000:
        return f"{value/1000000000:.{decimals}f}B"
    else:
        return f"{value/1000000000000:.{decimals}f}T"

def format_duration(seconds: Union[int, float], format_type: str = "auto") -> str:
    """Format duration in seconds to human-readable format.
    
    Args:
        seconds: Duration in seconds
        format_type: Format type ("auto", "short", "long")
    
    Returns:
        Formatted duration string
    """
    if seconds is None:
        return ""
    
    seconds = int(seconds)
    
    if format_type == "short":
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"{minutes}m"
        elif seconds < 86400:
            hours = seconds // 3600
            return f"{hours}h"
        else:
            days = seconds // 86400
            return f"{days}d"
    else:
        # Long format
        if seconds < 60:
            return f"{seconds} seconds"
        elif seconds < 3600:
            minutes = seconds // 60
            remaining_seconds = seconds % 60
            if remaining_seconds == 0:
                return f"{minutes} minutes"
            else:
                return f"{minutes} minutes, {remaining_seconds} seconds"
        elif seconds < 86400:
            hours = seconds // 3600
            remaining_minutes = (seconds % 3600) // 60
            if remaining_minutes == 0:
                return f"{hours} hours"
            else:
                return f"{hours} hours, {remaining_minutes} minutes"
        else:
            days = seconds // 86400
            remaining_hours = (seconds % 86400) // 3600
            if remaining_hours == 0:
                return f"{days} days"
            else:
                return f"{days} days, {remaining_hours} hours"
