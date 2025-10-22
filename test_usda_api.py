#!/usr/bin/env python3
"""Test USDA API to see what data is returned"""

import requests
import json

USDA_API_KEY = "1buWLv3vMzAeQ1319oRbWWP7myxHVjKchC5MqseI"
USDA_SEARCH_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

# Search for chicken
params = {
    'query': 'chicken',
    'pageNumber': 1,
    'pageSize': 5,
    'api_key': USDA_API_KEY
}

try:
    response = requests.get(USDA_SEARCH_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    print("USDA API Response Structure:")
    print(json.dumps(data, indent=2)[:2000])
    
    if 'foods' in data and len(data['foods']) > 0:
        print("\n\n=== FIRST FOOD ITEM ===")
        print(json.dumps(data['foods'][0], indent=2)[:3000])
        
except Exception as e:
    print(f"Error: {e}")