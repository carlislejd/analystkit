#!/usr/bin/env python3
"""
Simple test script to verify the AnalystKit package works correctly.
"""

def test_imports():
    """Test that all modules can be imported."""
    try:
        import analystkit as ak
        print("✓ Main package imported successfully")
        
        # Test individual module imports
        from analystkit.colors import BITWISE_COLORS, COLOR_HIERARCHY
        print("✓ Colors module imported successfully")
        
        from analystkit.plotly_theme import register_theme, apply_theme
        print("✓ Plotly theme module imported successfully")
        
        from analystkit.formats import format_number, format_percentage
        print("✓ Formats module imported successfully")
        
        from analystkit.charts import create_bar_chart
        print("✓ Charts module imported successfully")
        
        from analystkit.settings import load_settings
        print("✓ Settings module imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality without external dependencies."""
    try:
        import analystkit as ak
        
        # Test color constants
        assert len(ak.BITWISE_COLORS) == 6, "Should have 6 primary colors"
        assert ak.COLOR_HIERARCHY[3] == ['#66b77d', '#2c6271', '#45454b'], "Color hierarchy should match expected"
        
        # Test formatting functions
        formatted = ak.format_number(1234.56, decimals=2)
        assert "1,234.56" in formatted, "Number formatting should work"
        
        formatted_pct = ak.format_percentage(0.1234, decimals=1)
        assert "12.3%" in formatted_pct, "Percentage formatting should work"
        
        print("✓ Basic functionality tests passed")
        return True
        
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False

def test_settings():
    """Test settings functionality."""
    try:
        import analystkit as ak
        
        # Test settings loading
        settings = ak.load_settings()
        assert hasattr(settings, 'default_export_format'), "Settings should have export format"
        assert hasattr(settings, 'default_chart_width'), "Settings should have chart width"
        
        print("✓ Settings tests passed")
        return True
        
    except Exception as e:
        print(f"✗ Settings test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("AnalystKit Package Tests")
    print("=" * 40)
    
    tests = [
        ("Import Tests", test_imports),
        ("Basic Functionality", test_basic_functionality),
        ("Settings", test_settings),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nRunning {test_name}...")
        if test_func():
            passed += 1
            print(f"✓ {test_name} passed")
        else:
            print(f"✗ {test_name} failed")
    
    print("\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The package is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
