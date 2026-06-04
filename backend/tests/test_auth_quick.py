"""
Simple script to test authentication endpoints.
Run after starting the backend: python backend/tests/test_auth_quick.py
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def print_response(title, response):
    """Pretty print response."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)


def test_auth():
    """Test authentication flow."""
    
    # 1. Test health
    print("\n1. Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response)
    
    # 2. Test login with admin
    print("\n2. Testing admin login...")
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={
            "email": "admin@example.com",
            "password": "Admin@123456"
        }
    )
    print_response("Admin Login", response)
    
    if response.status_code != 200:
        print("❌ Login failed. Stopping tests.")
        return
    
    token = response.json()["access_token"]
    print(f"\n✓ Got token: {token[:30]}...")
    
    # 3. Test listing users with token
    print("\n3. Testing list users (admin only)...")
    response = requests.get(
        f"{BASE_URL}/api/users",
        headers={"Authorization": f"Bearer {token}"}
    )
    print_response("List Users", response)
    
    # 4. Test registration
    print("\n4. Testing user registration...")
    response = requests.post(
        f"{BASE_URL}/api/auth/register",
        json={
            "email": "testuser@example.com",
            "password": "TestPass123",
            "password_confirm": "TestPass123",
            "full_name": "Test User"
        }
    )
    print_response("User Registration", response)
    
    # 5. Test login with new user
    if response.status_code == 200:
        print("\n5. Testing new user login...")
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={
                "email": "testuser@example.com",
                "password": "TestPass123"
            }
        )
        print_response("New User Login", response)
    
    # 6. Test logout
    print("\n6. Testing logout...")
    response = requests.post(f"{BASE_URL}/api/auth/logout")
    print_response("Logout", response)
    
    print("\n" + "="*60)
    print("✓ All tests completed!")
    print("="*60)


if __name__ == "__main__":
    print("Testing Authentication API...")
    print(f"Base URL: {BASE_URL}")
    
    try:
        test_auth()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to backend at", BASE_URL)
        print("Please start the backend first: run.bat (Windows) or bash run.sh (Unix)")
    except Exception as e:
        print(f"❌ Error: {e}")
