"""Settings management for chart configuration."""

import os
from pathlib import Path
from typing import Optional, Any
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

env_path = Path.cwd() / ".env"
if env_path.exists():
    load_dotenv(env_path)

class Settings(BaseSettings):
    """Chart and export settings with environment variable support."""
    
    plotly_theme: str = Field(default="plotly", description="Default Plotly theme")
    plotly_renderer: str = Field(default="default", description="Default Plotly renderer")
    
    default_export_format: str = Field(default="svg", description="Default export format")
    default_export_scale: int = Field(default=2, description="Default export scale")
    
    font_path: Optional[str] = Field(default=None, description="Path to custom fonts directory")
    
    default_chart_width: int = Field(default=1200, description="Default chart width")
    default_chart_height: int = Field(default=800, description="Default chart height")
    
    color_scheme: str = Field(default="bitwise", description="Color scheme to use")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "allow"

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
