#!/usr/bin/env python3
"""
Example usage of the AnalystKit package.

This script demonstrates the key features of the package including:
- Theme registration
- Chart creation
- Formatting utilities
- Settings management
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Import the analystkit package
import analystkit as ak

def main():
    """Main demonstration function."""
    print("AnalystKit Demo")
    print("=" * 50)
    
    # 1. Register the custom theme
    print("\n1. Registering custom theme...")
    ak.register_theme()
    print("✓ Theme registered successfully")
    
    # 2. Demonstrate formatting utilities
    print("\n2. Formatting utilities demo...")
    
    # Number formatting
    large_number = 1234567.89
    formatted_num = ak.format_number(large_number, decimals=2)
    print(f"Number formatting: {large_number} → {formatted_num}")
    
    # Percentage formatting
    percentage = 0.1234
    formatted_pct = ak.format_percentage(percentage, decimals=1)
    print(f"Percentage formatting: {percentage} → {formatted_pct}")
    
    # Currency formatting
    amount = 1234.56
    formatted_currency = ak.format_currency(amount, currency="USD")
    print(f"Currency formatting: {amount} → {formatted_currency}")
    
    # Date formatting
    date_str = "2024-01-15"
    formatted_date = ak.format_date(date_str, format_str="%B %d, %Y")
    print(f"Date formatting: {date_str} → {formatted_date}")
    
    # 3. Create sample data
    print("\n3. Creating sample data...")
    
    # Time series data
    dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
    np.random.seed(42)  # For reproducible results
    
    data = pd.DataFrame({
        'Date': dates,
        'Sales': np.random.normal(1000, 200, len(dates)).cumsum(),
        'Profit': np.random.normal(200, 50, len(dates)).cumsum(),
        'Category': np.random.choice(['A', 'B', 'C'], len(dates))
    })
    
    print(f"✓ Created dataset with {len(data)} rows")
    
    # 4. Create and display charts
    print("\n4. Creating charts...")
    
    # Bar chart
    print("Creating bar chart...")
    bar_fig = ak.create_bar_chart(
        data=data.groupby('Category')['Sales'].sum().reset_index(),
        x='Category',
        y='Sales',
        x_label='Product Category',
        y_label='Total Sales ($)'
    )
    
    # Line chart
    print("Creating line chart...")
    line_fig = ak.create_line_chart(
        data=data,
        x='Date',
        y='Sales',
        color_column='Category',
        x_label='Date',
        y_label='Sales ($)'
    )
    
    # Scatter plot
    print("Creating scatter plot...")
    scatter_fig = ak.create_scatter_chart(
        data=data,
        x='Sales',
        y='Profit',
        color_column='Category',
        x_label='Sales ($)',
        y_label='Profit ($)'
    )
    
    print("✓ All charts created successfully")
    
    # 5. Display charts (if in interactive environment)
    try:
        print("\n5. Displaying charts...")
        print("Note: In a Jupyter notebook or interactive environment, charts will be displayed automatically")
        
        # Show charts
        bar_fig.show()
        line_fig.show()
        scatter_fig.show()
        
    except Exception as e:
        print(f"Note: Charts cannot be displayed in this environment: {e}")
        print("You can save them to files instead")
    
    # 6. Export charts
    print("\n6. Exporting charts...")
    
    try:
        # Export charts to SVG format
        ak.export_chart(bar_fig, 'sales_by_category', format='svg')
        ak.export_chart(line_fig, 'sales_over_time', format='svg')
        ak.export_chart(scatter_fig, 'sales_vs_profit', format='svg')
        
        print("✓ Charts exported successfully as SVG files")
        print("  - sales_by_category.svg")
        print("  - sales_over_time.svg")
        print("  - sales_vs_profit.svg")
        
    except Exception as e:
        print(f"Note: Chart export failed: {e}")
        print("This might be due to missing kaleido dependency")
    
    # 7. Settings demonstration
    print("\n7. Settings management...")
    
    try:
        settings = ak.load_settings()
        print(f"✓ Settings loaded successfully")
        print(f"  - Default export format: {settings.default_export_format}")
        print(f"  - Default chart width: {settings.default_chart_width}")
        print(f"  - Default chart height: {settings.default_chart_height}")
        
        # Create environment template
        ak.create_env_template()
        print("✓ Environment template created (.env.template)")
        
    except Exception as e:
        print(f"Note: Settings management failed: {e}")
    
    # 8. Color palette demonstration
    print("\n8. Color palette demo...")
    
    print("Primary colors:")
    for i, color in enumerate(ak.BITWISE_COLORS):
        print(f"  {i+1}. {color}")
    
    print("\nColor hierarchy for different numbers of items:")
    for n in range(1, 7):
        colors = ak.COLOR_HIERARCHY[n]
        print(f"  {n} item(s): {colors}")
    
    print("\n" + "=" * 50)
    print("Demo completed successfully!")
    print("\nTo use AnalystKit in your own projects:")
    print("1. Import: import analystkit as ak")
    print("2. Register theme: ak.register_theme()")
    print("3. Create charts: ak.create_bar_chart(...)")
    print("4. Format data: ak.format_number(...)")
    print("5. Export charts: ak.export_chart(...)")

if __name__ == "__main__":
    main()
