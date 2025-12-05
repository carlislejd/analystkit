"""Font loading and registration utilities for custom fonts."""

import os
import sys
import shutil
from pathlib import Path
from typing import List, Optional

def get_fonts_directory() -> Path:
    """Get the path to the fonts directory in the package."""
    # Get the directory where this file is located
    package_dir = Path(__file__).parent
    fonts_dir = package_dir / 'fonts'
    return fonts_dir

def get_system_fonts_directory() -> Optional[Path]:
    """Get the system fonts directory based on the platform."""
    platform = sys.platform
    
    if platform == 'darwin':  # macOS
        return Path.home() / 'Library' / 'Fonts'
    elif platform == 'win32':  # Windows
        return Path(os.environ.get('LOCALAPPDATA', '')) / 'Microsoft' / 'Windows' / 'Fonts'
    elif platform.startswith('linux'):  # Linux
        user_fonts = Path.home() / '.local' / 'share' / 'fonts'
        if user_fonts.exists():
            return user_fonts
        # Try system fonts directory (requires sudo)
        return Path('/usr/share/fonts')
    else:
        return None

def list_package_fonts() -> List[Path]:
    """List all font files in the package fonts directory."""
    fonts_dir = get_fonts_directory()
    if not fonts_dir.exists():
        return []
    
    font_extensions = {'.otf', '.ttf', '.ttc', '.woff', '.woff2'}
    fonts = [f for f in fonts_dir.iterdir() 
             if f.is_file() and f.suffix.lower() in font_extensions]
    return sorted(fonts)

def is_font_installed(font_name: str) -> bool:
    """Check if a font is installed in the system."""
    system_fonts_dir = get_system_fonts_directory()
    if not system_fonts_dir or not system_fonts_dir.exists():
        return False
    
    # Check if font file exists in system fonts directory
    font_files = list(system_fonts_dir.glob(f'*{font_name}*'))
    return len(font_files) > 0

def install_fonts(force: bool = False) -> dict:
    """
    Install fonts from the package to the system fonts directory.
    
    Args:
        force: If True, overwrite existing fonts. If False, skip already installed fonts.
    
    Returns:
        dict: Installation results with 'installed', 'skipped', and 'failed' lists
    """
    package_fonts = list_package_fonts()
    system_fonts_dir = get_system_fonts_directory()
    
    if not system_fonts_dir:
        return {
            'installed': [],
            'skipped': [],
            'failed': [str(f) for f in package_fonts],
            'error': 'Unsupported platform'
        }
    
    # Create system fonts directory if it doesn't exist
    system_fonts_dir.mkdir(parents=True, exist_ok=True)
    
    results = {
        'installed': [],
        'skipped': [],
        'failed': []
    }
    
    for font_path in package_fonts:
        font_name = font_path.name
        dest_path = system_fonts_dir / font_name
        
        # Check if already installed
        if dest_path.exists() and not force:
            results['skipped'].append(font_name)
            continue
        
        try:
            # Copy font to system fonts directory
            shutil.copy2(font_path, dest_path)
            results['installed'].append(font_name)
        except Exception as e:
            results['failed'].append(f'{font_name}: {str(e)}')
    
    return results

def check_fonts_installed() -> dict:
    """
    Check which required fonts are installed.
    
    Returns:
        dict: Status of each required font
    """
    required_fonts = {
        'PPNeueMontreal-Regular': 'Primary font for all text',
        'Items-Regular': 'Title font'
    }
    
    status = {}
    for font_name, description in required_fonts.items():
        status[font_name] = {
            'installed': is_font_installed(font_name),
            'description': description
        }
    
    return status

def setup_fonts(auto_install: bool = False) -> dict:
    """
    Set up fonts for use with Plotly charts.
    
    This function checks if required fonts are installed and optionally
    installs them if they're missing.
    
    Args:
        auto_install: If True, automatically install missing fonts.
                     If False, only check status.
    
    Returns:
        dict: Setup results with font status and installation info
    """
    # Check current font status
    font_status = check_fonts_installed()
    
    # Check if any fonts are missing
    missing_fonts = [name for name, info in font_status.items() 
                     if not info['installed']]
    
    result = {
        'status': font_status,
        'all_installed': len(missing_fonts) == 0,
        'missing_fonts': missing_fonts
    }
    
    # Auto-install if requested and fonts are missing
    if auto_install and missing_fonts:
        install_results = install_fonts()
        result['installation'] = install_results
        
        # Re-check status after installation
        font_status = check_fonts_installed()
        result['status'] = font_status
        result['all_installed'] = all(info['installed'] 
                                      for info in font_status.values())
    
    return result

# Auto-setup fonts on import (non-blocking, just checks status)
def _auto_setup():
    """Automatically check font status on import."""
    try:
        setup_fonts(auto_install=False)
    except Exception:
        # Silently fail - fonts might not be critical for basic functionality
        pass

# Run auto-setup when module is imported
_auto_setup()

