import requests
import json
import os
import time
from typing import Optional, Tuple

import os

# Use absolute path relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(BASE_DIR, "geo_cache.json")

# Keys provided by user
PLACES_API_KEY = "AIzaSyCIKJCUEqspAM0qSYso7neKsY_OAisK3ZU"
GEOCODING_API_KEY = "AIzaSyBtrMP5uGgBY8UcJP8GGrKf2NAUuIs-l28"

PLACES_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
GEOCODING_URL = "https://maps.googleapis.com/maps/api/geocode/json"

# Load cache
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        try:
            geo_cache = json.load(f)
        except:
            geo_cache = {}
else:
    geo_cache = {}

def save_cache():
    with open(CACHE_FILE, "w") as f:
        json.dump(geo_cache, f, indent=2)

def geocode_venue(query: str) -> Optional[Tuple[float, float, str]]:
    """
    Geocodes a venue name using Google APIs.
    Tries Places API first, then Geocoding API.
    Returns (lat, lng, display_name) or None.
    """
    query = query.strip()
    if not query:
        return None

    # Check cache first
    if query in geo_cache:
        # print(f"[Geo] Cache hit for '{query}'")
        return tuple(geo_cache[query])

    # Append "Bengaluru" to ensure context if not present
    if "bengaluru" not in query.lower() and "bangalore" not in query.lower():
        search_query = f"{query}, Bengaluru"
    else:
        search_query = query

    # 1. Try Places API (Text Search)
    try:
        params = {
            "query": search_query,
            "key": PLACES_API_KEY
        }
        # print(f"[Geo] Requesting Places API for: {search_query}")
        response = requests.get(PLACES_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "OK" and data.get("results"):
                result = data["results"][0]
                lat = result["geometry"]["location"]["lat"]
                lng = result["geometry"]["location"]["lng"]
                name = result["name"]
                formatted_address = result.get("formatted_address", "")
                display_name = f"{name}, {formatted_address}"
                
                geo_cache[query] = [lat, lng, display_name]
                save_cache()
                return lat, lng, display_name
            elif data.get("status") == "REQUEST_DENIED":
                print(f"[Geo] Places API Denied. Trying Geocoding API...")
    except Exception as e:
        print(f"[Geo] Places API Exception: {e}")

    # 2. Fallback to Geocoding API
    try:
        params = {
            "address": search_query,
            "key": GEOCODING_API_KEY
        }
        # print(f"[Geo] Requesting Geocoding API for: {search_query}")
        response = requests.get(GEOCODING_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "OK" and data.get("results"):
                result = data["results"][0]
                lat = result["geometry"]["location"]["lat"]
                lng = result["geometry"]["location"]["lng"]
                formatted_address = result.get("formatted_address", "")
                
                geo_cache[query] = [lat, lng, formatted_address]
                save_cache()
                return lat, lng, formatted_address
            else:
                 print(f"[Geo] Geocoding API returned: {data.get('status')}")
    except Exception as e:
        print(f"[Geo] Geocoding API Exception: {e}")

    return None
