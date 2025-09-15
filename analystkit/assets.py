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

def fetch_crypto_history(symbol: str) -> Dict[str, Union[str, int, float, List, None]]:
    """
    Fetch complete price history for a crypto asset.
    
    This function automatically capitalizes the symbol and fetches all available
    historical price data from the Bitwise API without date restrictions.
    
    Args:
        symbol (str): Crypto symbol (e.g., 'btc', 'ETH', 'sol') - will be auto-capitalized
        
    Returns:
        Dict[str, Union[str, int, float, List, None]]: Dictionary containing:
            - symbol (str): The crypto symbol (always uppercase)
            - data_points (int): Number of data points returned
            - results (List): Raw price data from API
            - first_date (str, optional): Earliest date in dataset
            - last_date (str, optional): Most recent date in dataset
            - min_price (float, optional): Lowest price in dataset
            - max_price (float, optional): Highest price in dataset
            - last_price (float, optional): Most recent price
            - error (str, optional): Error message if request failed
            
    Example:
        >>> data = fetch_crypto_history('btc')
        >>> print(f"Fetched {data['data_points']} data points for {data['symbol']}")
        >>> print(f"Price range: ${data['min_price']} - ${data['max_price']}")
    """
    try:
        # Auto-capitalize symbol for consistency
        symbol = symbol.upper()
        
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

def fetch_index_history(symbol: str = 'DEFI') -> Dict[str, Union[str, int, float, List, None]]:
    """
    Fetch complete historical data for a Bitwise index.
    
    This function automatically capitalizes the symbol and fetches all available
    historical index data from the Bitwise API without date restrictions.
    
    Args:
        symbol (str): Index symbol (e.g., 'defi', 'BIT10', 'bitw') - will be auto-capitalized.
                      Defaults to 'DEFI' if not specified.
        
    Returns:
        Dict[str, Union[str, int, float, List, None]]: Dictionary containing:
            - symbol (str): The index symbol (always uppercase)
            - data_points (int): Number of data points returned
            - results (List): Raw index data from API
            - first_date (str, optional): Earliest date in dataset
            - last_date (str, optional): Most recent date in dataset
            - min_value (float, optional): Lowest index value in dataset
            - max_value (float, optional): Highest index value in dataset
            - last_value (float, optional): Most recent index value
            - error (str, optional): Error message if request failed
            
    Example:
        >>> data = fetch_index_history('bit10')
        >>> print(f"Fetched {data['data_points']} data points for {data['symbol']}")
        >>> print(f"Index range: {data['min_value']} - {data['max_value']}")
    """
    try:
        # Auto-capitalize symbol for consistency
        symbol = symbol.upper()
        
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
    
    This function automatically capitalizes the symbol and returns a clean DataFrame
    with timestamp and price columns, sorted chronologically.
    
    Args:
        symbol (str): Crypto symbol (e.g., 'btc', 'ETH', 'sol') - will be auto-capitalized
        
    Returns:
        Optional[pd.DataFrame]: DataFrame with columns:
            - timestamp (datetime): Timestamp of the data point
            - price (float): Price at that timestamp
            - Additional columns from API response
            Returns None if error occurs or no data available
        
    Example:
        >>> df = get_crypto_dataframe('btc')
        >>> if df is not None:
        ...     print(f"Data for {df['symbol'].iloc[0]}: {len(df)} rows")
        ...     print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
        ...     print(f"Price range: ${df['price'].min():.2f} - ${df['price'].max():.2f}")
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
    
    This function automatically capitalizes the symbol and returns a clean DataFrame
    with timestamp and index_value columns, sorted chronologically.
    
    Args:
        symbol (str): Index symbol (e.g., 'defi', 'BIT10', 'bitw') - will be auto-capitalized.
                      Defaults to 'DEFI' if not specified.
        
    Returns:
        Optional[pd.DataFrame]: DataFrame with columns:
            - timestamp (datetime): Timestamp of the data point
            - index_value (float): Index value at that timestamp
            - symbol (str): The index symbol
            Returns None if error occurs or no data available
        
    Example:
        >>> df = get_index_dataframe('bit10')
        >>> if df is not None:
        ...     print(f"Data for {df['symbol'].iloc[0]}: {len(df)} rows")
        ...     print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
        ...     print(f"Index range: {df['index_value'].min():.2f} - {df['index_value'].max():.2f}")
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
    
    Returns a curated list of common cryptocurrency symbols that are typically
    available through the Bitwise API. This list can be expanded as needed.
    
    Returns:
        List[str]: List of available crypto symbols in uppercase
        
    Example:
        >>> cryptos = list_available_cryptos()
        >>> print(f"Available cryptos: {', '.join(cryptos)}")
        >>> # Use any symbol with fetch_crypto_history()
        >>> data = fetch_crypto_history(cryptos[0])  # 'BTC'
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
    
    Returns a curated list of Bitwise index symbols that are typically
    available through the Bitwise API. This list can be expanded as needed.
    
    Returns:
        List[str]: List of available index symbols in uppercase
        
    Example:
        >>> indices = list_available_indices()
        >>> print(f"Available indices: {', '.join(indices)}")
        >>> # Use any symbol with fetch_index_history()
        >>> data = fetch_index_history(indices[0])  # 'DEFI'
    """
    # Common Bitwise indices - you can expand this list
    common_indices = [
        'DEFI', 'BIT10', 'BITW', 'BITQ', 'BITC', 'BITI'
    ]
    return common_indices
