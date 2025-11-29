import requests
import sys

def test_security():
    url = "http://localhost:8000/api/v1/classify"
    payload = {"text": "test email"}
    
    print("1. Testing without API Key...")
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 401 or response.status_code == 403:
            print("✅ SUCCESS: Access denied as expected")
        else:
            print("❌ FAILURE: Access granted unexpectedly")
    except Exception as e:
        print(f"Error: {e}")

    print("\n2. Testing with API Key...")
    try:
        headers = {"X-API-Key": "default-dev-key"}
        response = requests.post(url, json=payload, headers=headers)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ SUCCESS: Access granted")
            print(response.json())
        else:
            print(f"❌ FAILURE: Access denied. Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_security()
