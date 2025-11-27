import requests
import json
import random
import string

BASE_URL = "http://localhost:8000/api/v1"

def get_random_string(length=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def test_flow():
    # 1. Register
    email = f"vendor_{get_random_string()}@test.com"
    password = "testpassword123"
    print(f"Registering {email}...")
    
    reg_payload = {
        "email": email,
        "password": password,
        "business_name": "Test Vendor",
        "category": "Food",
        "is_vendor": True
    }
    
    resp = requests.post(f"{BASE_URL}/auth/register", json=reg_payload)
    if resp.status_code != 200:
        print(f"Registration failed: {resp.text}")
        return
    print("Registration successful.")

    # 2. Login
    print("Logging in...")
    login_data = {
        "username": email,
        "password": password
    }
    resp = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    if resp.status_code != 200:
        print(f"Login failed: {resp.text}")
        return
    
    token = resp.json()["access_token"]
    print(f"Login successful. Token: {token[:10]}...")

    # 2.5 Update Profile with Location
    print("Updating profile with location...")
    headers = {"Authorization": f"Bearer {token}"}
    update_payload = {
        "location": {
            "type": "Point",
            "coordinates": [77.5946, 12.9716] # Bengaluru Center
        },
        "travel_radius_km": 10
    }
    resp = requests.put(f"{BASE_URL}/vendors/me", json=update_payload, headers=headers)
    if resp.status_code != 200:
        print(f"Profile update failed: {resp.text}")
        return
    print("Profile updated.")

    # 3. Get Recommendations
    print("Fetching recommendations...")
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{BASE_URL}/recommendations/", headers=headers)
    
    if resp.status_code != 200:
        print(f"Recommendations failed: {resp.text}")
        return
        
    events = resp.json()
    print(f"Received {len(events)} recommendations.")
    if len(events) > 0:
        print(f"Top event: {events[0]['title']}")
        print(f"Location: {events[0]['location']}")

if __name__ == "__main__":
    test_flow()
