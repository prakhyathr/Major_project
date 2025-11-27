import requests
import json

API_URL = "http://localhost:8000/api/v1/events/"

def verify_api():
    try:
        print(f"Fetching events from {API_URL}...")
        response = requests.get(API_URL)
        
        if response.status_code != 200:
            print(f"Error: Status {response.status_code}")
            print(response.text)
            return

        events = response.json()
        print(f"Fetched {len(events)} events.")
        
        if not events:
            print("No events found to check.")
            return

        # Check first event
        first_event = events[0]
        print("First Event Keys:", first_event.keys())
        
        if "category" in first_event:
            print(f"SUCCESS: 'category' field found! Value: {first_event['category']}")
            
            # Count categories
            categories = set()
            for e in events:
                if e.get("category"):
                    categories.add(e["category"])
            print(f"Unique Categories: {categories}")
        else:
            print("FAILURE: 'category' field MISSING in response.")
            
    except Exception as e:
        print(f"Connection failed: {e}")
        print("Make sure the backend is running.")

if __name__ == "__main__":
    verify_api()
