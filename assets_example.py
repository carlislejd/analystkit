#!/usr/bin/env python3
"""
Example usage of the AnalystKit assets module.

This script demonstrates how to fetch crypto and index data
and create charts with the data.
"""

import analystkit as ak
import pandas as pd

def main():
    """Main demonstration function."""
    print("AnalystKit Assets Demo")
    print("=" * 50)
    
    # 1. Register the custom theme
    print("\n1. Registering custom theme...")
    ak.register_theme()
    print("✓ Theme registered successfully")
    
    # 2. List available assets
    print("\n2. Available assets...")
    cryptos = ak.list_available_cryptos()
    indices = ak.list_available_indices()
    
    print(f"Available cryptos: {', '.join(cryptos[:5])}...")
    print(f"Available indices: {', '.join(indices)}")
    
    # 3. Fetch crypto data
    print("\n3. Fetching crypto data...")
    print("Note: This requires a valid Bitwise API key in your .env file")
    
    try:
        # Try to fetch BTC data
        btc_data = ak.fetch_crypto_history('BTC')
        
        if 'error' not in btc_data:
            print(f"✓ BTC data fetched successfully")
            print(f"  - Data points: {btc_data.get('data_points', 0)}")
            print(f"  - Date range: {btc_data.get('first_date', 'N/A')} to {btc_data.get('last_date', 'N/A')}")
            print(f"  - Price range: ${btc_data.get('min_price', 0):,.2f} - ${btc_data.get('max_price', 0):,.2f}")
            print(f"  - Last price: ${btc_data.get('last_price', 0):,.2f}")
            
            # Get as DataFrame for charting
            btc_df = ak.get_crypto_dataframe('BTC')
            if btc_df is not None:
                print(f"  - DataFrame shape: {btc_df.shape}")
                
                # Create a simple price chart
                if len(btc_df) > 0:
                    print("\n4. Creating crypto price chart...")
                    
                    # Sample last 100 data points for demo
                    sample_df = btc_df.tail(100)
                    
                    fig = ak.create_line_chart(
                        data=sample_df,
                        x='timestamp',
                        y='price',
                        x_label='Date',
                        y_label='Price (USD)',
                        size_preset='half'
                    )
                    
                    print("✓ BTC price chart created successfully")
                    print("  - Use fig.show() to display in Jupyter/notebook")
                    
        else:
            print(f"✗ Error fetching BTC data: {btc_data['error']}")
            print("  - Make sure you have BITWISE_API_KEY in your .env file")
            
    except Exception as e:
        print(f"✗ Error: {e}")
        print("  - Make sure you have BITWISE_API_KEY in your .env file")
    
    # 4. Fetch index data
    print("\n5. Fetching index data...")
    
    try:
        # Try to fetch DEFI index data
        defi_data = ak.fetch_index_history('DEFI')
        
        if 'error' not in defi_data:
            print(f"✓ DEFI index data fetched successfully")
            print(f"  - Data points: {defi_data.get('data_points', 0)}")
            print(f"  - Date range: {defi_data.get('first_date', 'N/A')} to {defi_data.get('last_date', 'N/A')}")
            print(f"  - Value range: {defi_data.get('min_value', 0):,.2f} - {defi_data.get('max_value', 0):,.2f}")
            print(f"  - Last value: {defi_data.get('last_value', 0):,.2f}")
            
            # Get as DataFrame for charting
            defi_df = ak.get_index_dataframe('DEFI')
            if defi_df is not None:
                print(f"  - DataFrame shape: {defi_df.shape}")
                
                # Create a simple index chart
                if len(defi_df) > 0:
                    print("\n6. Creating index chart...")
                    
                    # Sample last 100 data points for demo
                    sample_df = defi_df.tail(100)
                    
                    fig = ak.create_line_chart(
                        data=sample_df,
                        x='timestamp',
                        y='index_value',
                        x_label='Date',
                        y_label='Index Value',
                        size_preset='half'
                    )
                    
                    print("✓ DEFI index chart created successfully")
                    print("  - Use fig.show() to display in Jupyter/notebook")
                    
        else:
            print(f"✗ Error fetching DEFI data: {defi_data['error']}")
            
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "=" * 50)
    print("Assets demo completed!")
    print("\nTo use the assets module:")
    print("1. Set BITWISE_API_KEY in your .env file")
    print("2. Fetch data: ak.fetch_crypto_history('BTC')")
    print("3. Get DataFrame: ak.get_crypto_dataframe('BTC')")
    print("4. Create charts: ak.create_line_chart(...)")

if __name__ == "__main__":
    main()
