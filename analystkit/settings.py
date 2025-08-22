"""Settings management for API keys and configuration."""

import os
from pathlib import Path
from typing import Optional, Dict, Any
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
env_path = Path.cwd() / ".env"
if env_path.exists():
    load_dotenv(env_path)

class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Plotly settings
    plotly_theme: str = Field(default="plotly", description="Default Plotly theme")
    plotly_renderer: str = Field(default="default", description="Default Plotly renderer")
    
    # Export settings
    default_export_format: str = Field(default="svg", description="Default export format")
    default_export_scale: int = Field(default=2, description="Default export scale")
    
    # Font settings
    font_path: Optional[str] = Field(default=None, description="Path to custom fonts directory")
    
    # API keys (add as needed)
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    mapbox_token: Optional[str] = Field(default=None, description="Mapbox token for maps")
    bitwise_api_key: Optional[str] = Field(default=None, description="Bitwise API key for crypto/index data")
    
    # Chart defaults
    default_chart_width: int = Field(default=1200, description="Default chart width")
    default_chart_height: int = Field(default=800, description="Default chart height")
    
    # Color scheme
    color_scheme: str = Field(default="bitwise", description="Color scheme to use")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "allow"  # Allow extra fields from environment

def load_settings(env_file: Optional[str] = None) -> Settings:
    """Load settings from environment variables and .env file.
    
    Args:
        env_file: Optional path to .env file
    
    Returns:
        Settings instance
    """
    if env_file:
        load_dotenv(env_file)
    
    return Settings()

def get_setting(key: str, default: Any = None) -> Any:
    """Get a setting value by key.
    
    Args:
        key: Setting key
        default: Default value if setting not found
    
    Returns:
        Setting value or default
    """
    settings = load_settings()
    return getattr(settings, key, default)

def set_setting(key: str, value: Any) -> None:
    """Set a setting value (environment variable).
    
    Args:
        key: Setting key
        value: Setting value
    """
    os.environ[key.upper()] = str(value)

def get_api_key(service: str) -> Optional[str]:
    """Get API key for a specific service.
    
    Args:
        service: Service name (e.g., 'openai', 'mapbox')
    
    Returns:
        API key if found, None otherwise
    """
    settings = load_settings()
    key_name = f"{service}_api_key"
    
    if hasattr(settings, key_name):
        return getattr(settings, key_name)
    
    # Try environment variable
    env_key = f"{service.upper()}_API_KEY"
    return os.getenv(env_key)

def validate_api_keys() -> Dict[str, bool]:
    """Validate that required API keys are present.
    
    Returns:
        Dictionary mapping service names to validation status
    """
    settings = load_settings()
    validation_results = {}
    
    # Check for API keys in settings
    for field_name, field in settings.__fields__.items():
        if field_name.endswith('_api_key') and field.description:
            key_value = getattr(settings, field_name)
            validation_results[field_name.replace('_api_key', '')] = bool(key_value)
    
    return validation_results

def create_env_template(output_path: str = ".env.template") -> None:
    """Create a template .env file with all available settings.
    
    Args:
        output_path: Path to output template file
    """
    settings = Settings()
    template_lines = [
        "# AnalystKit Environment Variables Template",
        "# Copy this file to .env and fill in your values",
        "",
    ]
    
    for field_name, field in settings.__fields__.items():
        if field.description:
            template_lines.append(f"# {field.description}")
            if field.default is not None:
                template_lines.append(f"{field_name.upper()}={field.default}")
            else:
                template_lines.append(f"{field_name.upper()}=")
            template_lines.append("")
    
    with open(output_path, 'w') as f:
        f.write('\n'.join(template_lines))
    
    print(f"Environment template created at: {output_path}")

# Global settings instance
settings = load_settings()
