import requests
import json

import random
import string

url = "http://localhost:8000/api/v1/auth/register"
random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
payload = {
    "email": f"debug_{random_str}@test.com",
    "password": "shortpassword",
    "is_vendor": True
}
headers = {
    "Content-Type": "application/json"
}

try:
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
