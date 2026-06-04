"""Test script for ticket upload functionality."""
import requests
import json
import os

BASE_URL = "http://localhost:8000"

def get_token(email: str, password: str) -> str:
    """Login and get JWT token."""
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"email": email, "password": password}
    )
    if response.status_code != 200:
        print(f"❌ Login failed: {response.json()}")
        return None
    return response.json()["access_token"]


def print_response(title: str, response):
    """Pretty print response."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)


def test_upload():
    """Test ticket upload functionality."""
    print("Testing Ticket Upload API...")
    print(f"Base URL: {BASE_URL}\n")
    
    # 1. Login
    print("1. Logging in...")
    token = get_token("admin@example.com", "Admin@123456")
    if not token:
        return
    print(f"✓ Got token: {token[:30]}...")
    
    # 2. Test upload with sample CSV
    sample_file = "ml/data/sample_tickets.csv"
    if not os.path.exists(sample_file):
        print(f"\n❌ Sample file not found: {sample_file}")
        print("Please run from project root directory")
        return
    
    print(f"\n2. Uploading tickets from {sample_file}...")
    headers = {"Authorization": f"Bearer {token}"}
    
    with open(sample_file, "rb") as f:
        files = {"file": f}
        response = requests.post(
            f"{BASE_URL}/api/tickets/upload",
            files=files,
            headers=headers
        )
    
    print_response("Upload Response", response)
    
    if response.status_code != 200:
        print("❌ Upload failed")
        return
    
    upload_data = response.json()
    print(f"\n✓ Upload completed:")
    print(f"  - Valid rows: {upload_data['valid_rows']}")
    print(f"  - Invalid rows: {upload_data['invalid_rows']}")
    print(f"  - Upload ID: {upload_data['upload_id']}")
    
    # 3. List tickets
    print("\n3. Listing uploaded tickets...")
    response = requests.get(
        f"{BASE_URL}/api/tickets?limit=5",
        headers=headers
    )
    print_response("List Tickets", response)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✓ Found {data['total']} total tickets")
        if data['items']:
            print(f"✓ First ticket: {data['items'][0]['ticket_id']}")
    
    # 4. Get upload history
    print("\n4. Checking upload history...")
    response = requests.get(
        f"{BASE_URL}/api/tickets/upload-history/",
        headers=headers
    )
    print_response("Upload History", response)
    
    # 5. Test filtering
    print("\n5. Testing filters (priority=P1)...")
    response = requests.get(
        f"{BASE_URL}/api/tickets?priority=P1&limit=10",
        headers=headers
    )
    print_response("Filtered Tickets (P1)", response)
    
    print("\n" + "="*70)
    print("✓ Upload tests completed!")
    print("="*70)


if __name__ == "__main__":
    try:
        test_upload()
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to {BASE_URL}")
        print("Please start backend: run.bat (Windows) or bash run.sh (Unix)")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
