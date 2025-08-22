"""Asset data fetching utilities for crypto and indices."""

import os
import requests
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Union
from .settings import get_api_key

# API Configuration
BASE_URL = "https://api.bitwiseinvestments.com/"
API_KEY = get_api_key('bitwise')

def fetch_crypto_history(symbol: str) -> Dict:
    """
    Fetch complete price history for a crypto asset.
    
    Args:
        symbol (str): Crypto symbol (e.g., 'BTC', 'ETH', 'SOL')
        
    Returns:
        dict: Processed price history data with statistics
    """
    try:
        # Set up the endpoint
        endpoint = f"assets/{symbol}/quotes"
        url = f"{BASE_URL}api/v1/{endpoint}"
        
        # Make the API request (no date limits - gets all available data)
        response = requests.get(url, params={'apiKey': API_KEY})
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        
        # Check if data is an array as expected
        if not isinstance(data, list):
            return {"error": "Unexpected response format from API"}
        
        # Process the data
        processed_data = {
            'symbol': symbol,
            'data_points': len(data),
            'results': data
        }
        
        # Add statistics if data exists
        if data:
            try:
                df = pd.DataFrame(data)
                
                # Add date range info
                timestamps = [item.get('timestamp') for item in data if item.get('timestamp')]
                if timestamps:
                    processed_data['first_date'] = min(timestamps)
                    processed_data['last_date'] = max(timestamps)
                
                # Add price statistics if price field exists
                if 'price' in df.columns:
                    processed_data['min_price'] = float(df['price'].min())
                    processed_data['max_price'] = float(df['price'].max())
                    processed_data['last_price'] = float(df['price'].iloc[-1])
                    
            except Exception as stats_error:
                # Continue even if statistics fail
                pass
                
        return processed_data
        
    except Exception as e:
        return {"error": f"Error fetching crypto data for {symbol}: {str(e)}"}

def fetch_index_history(symbol: str = 'DEFI') -> Dict:
    """
    Fetch complete historical data for a Bitwise index.
    
    Args:
        symbol (str): Index symbol (e.g., 'DEFI', 'BIT10', 'BITW')
        
    Returns:
        dict: Processed index history data with results array
    """
    try:
        # Set up the endpoint
        endpoint = f"indexes/{symbol}/history"
        url = f"{BASE_URL}api/v1/{endpoint}"
        
        # Make the API request (no date limits - gets all available data)
        params = {
            'exclude_backtests': 'true',
            'apiKey': API_KEY
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        
        # Check if data is an array as expected
        if not isinstance(data, list):
            return {"error": "Unexpected response format from API"}
        
        # Convert to DataFrame for processing
        df = pd.DataFrame(data)
        
        # Rename columns if data is available
        if not df.empty and len(df.columns) >= 2:
            df.rename(columns={0: 'timestamp', 1: 'index_value'}, inplace=True)
            df['symbol'] = symbol
            
            # Convert DataFrame to dict for API response
            results = df.to_dict(orient='records')
            
            processed_data = {
                'symbol': symbol,
                'data_points': len(results),
                'results': results
            }
            
            # Add statistics
            if results:
                try:
                    timestamps = [item.get('timestamp') for item in results if item.get('timestamp')]
                    if timestamps:
                        processed_data['first_date'] = min(timestamps)
                        processed_data['last_date'] = max(timestamps)
                    
                    # Add index value statistics
                    index_values = [item.get('index_value') for item in results if item.get('index_value')]
                    if index_values:
                        processed_data['min_value'] = float(min(index_values))
                        processed_data['max_value'] = float(max(index_values))
                        processed_data['last_value'] = float(index_values[-1])
                        
                except Exception as stats_error:
                    # Continue even if statistics fail
                    pass
            
            return processed_data
        else:
            return {
                'symbol': symbol,
                'data_points': 0,
                'results': []
            }
            
    except Exception as e:
        return {"error": f"Error fetching index data for {symbol}: {str(e)}"}

def get_crypto_dataframe(symbol: str) -> Optional[pd.DataFrame]:
    """
    Get crypto data as a pandas DataFrame for easy analysis.
    
    Args:
        symbol (str): Crypto symbol (e.g., 'BTC', 'ETH')
        
    Returns:
        pd.DataFrame: DataFrame with timestamp and price columns, or None if error
    """
    data = fetch_crypto_history(symbol)
    
    if 'error' in data:
        print(f"Error: {data['error']}")
        return None
    
    if not data.get('results'):
        print(f"No data available for {symbol}")
        return None
    
    # Convert to DataFrame
    df = pd.DataFrame(data['results'])
    
    # Ensure timestamp column exists and convert to datetime
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
    
    return df

def get_index_dataframe(symbol: str = 'DEFI') -> Optional[pd.DataFrame]:
    """
    Get index data as a pandas DataFrame for easy analysis.
    
    Args:
        symbol (str): Index symbol (e.g., 'DEFI', 'BIT10')
        
    Returns:
        pd.DataFrame: DataFrame with timestamp and index_value columns, or None if error
    """
    data = fetch_index_history(symbol)
    
    if 'error' in data:
        print(f"Error: {data['error']}")
        return None
    
    if not data.get('results'):
        print(f"No data available for {symbol}")
        return None
    
    # Convert to DataFrame
    df = pd.DataFrame(data['results'])
    
    # Ensure timestamp column exists and convert to datetime
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
    
    return df

def list_available_cryptos() -> List[str]:
    """
    Get a list of available crypto symbols.
    
    Returns:
        List[str]: List of available crypto symbols
    """
    # Common crypto symbols - you can expand this list
    common_cryptos = [
        'BTC', 'ETH', 'SOL', 'ADA', 'DOT', 'LINK', 'UNI', 'AVAX',
        'MATIC', 'ATOM', 'LTC', 'BCH', 'XRP', 'DOGE', 'SHIB'
    ]
    return common_cryptos

def list_available_indices() -> List[str]:
    """
    Get a list of available Bitwise index symbols.
    
    Returns:
        List[str]: List of available index symbols
    """
    # Common Bitwise indices - you can expand this list
    common_indices = [
        'DEFI', 'BIT10', 'BITW', 'BITQ', 'BITC', 'BITI'
    ]
    return common_indices
